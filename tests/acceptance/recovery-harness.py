"""Isolated acceptance of protocol recovery; never installed as a runtime.

Run: python3 -B recovery-harness.py EMPTY_TEMP_DIR FIXES_ARTIFACT_DIR
Each recovery/retry starts a new process and reads only persisted test inputs.
The fixture explicitly authorizes cleanup of its observed, fingerprinted pending
file. This is not a general recovery engine or an authorization source.
"""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def markdown(record):
    return ('# 隔离恢复验收：合成 candidate 数据\n\n```json\n' +
            json.dumps(record, ensure_ascii=False, indent=2) + '\n```\n').encode()


def snapshot(folder):
    return {str(file.relative_to(folder)): digest(file.read_bytes())
            for file in sorted(folder.rglob('*')) if file.is_file()}


def capture(base, project, destination):
    shutil.copytree(project, destination)
    return {'path': str(destination.relative_to(base)), 'files': snapshot(destination)}


def reconcile(namespace, project, target_rel, before, candidate, request):
    """Execute the fixture's bounded, preauthorized recovery decision."""
    pending_rel = target_rel + '.pending'
    namespace['_check_paths'](project, {target_rel, pending_rel})
    target = project / target_rel
    pending = project / pending_rel
    observed = target.read_bytes()
    namespace['_parse'](observed)
    namespace['_parse'](candidate)
    if observed not in (before, candidate):
        return {'status': 'unknown', 'classification': 'unknown', 'cleanedPending': False}
    committed = observed == candidate
    result = {'classification': 'saved' if committed else 'not_saved', 'cleanedPending': False}
    if request['readonly']:
        return {**result, 'status': 'unchanged' if committed else 'pending'}
    allowed = set(request['allowed'])
    if not {target_rel, pending_rel}.issubset(allowed):
        return {**result, 'status': 'pending'}
    if pending.exists():
        staged = pending.read_bytes()
        # Provenance is the actual crash snapshot recorded by the test parent,
        # not an assumption that every file named .pending belongs to us.
        if (request['pendingEvidence'].get(pending_rel) != digest(staged)
                or not staged or not candidate.startswith(staged)):
            return {**result, 'status': 'unknown'}
        pending.unlink()
        result['cleanedPending'] = True
    saved = namespace['save_memory'](project, target_rel, candidate, digest(observed), allowed)
    return {**result, 'status': saved['status'], 'save': saved}


def execute(base, fixes, request, fault=None):
    namespace = runpy.run_path(str(fixes / 'save-memory.py'))
    project = base / request['project']
    # Verify the original delta's raw bytes and affected entry, not a receipt
    # alone. Remaining evidence/approval checks belong to the real primary.
    delta_bytes = (base / 'saving-input/delta.json').read_bytes()
    delta = json.loads(delta_bytes)
    candidate = (base / 'saving-input/candidate.md').read_bytes()
    record = namespace['_parse'](candidate)
    receipt = next(item for item in record['receipts'] if item['delta_id'] == delta['delta_id'])
    assert receipt['sha256'] == digest(delta_bytes)
    assert receipt['result_revision'] == record['revision']
    assert receipt['entry_ids'] == [item['entry']['id'] for item in delta['changes']]
    if request['operation'] == 'save':
        answer = reconcile(namespace, project, 'record.md',
                           (base / 'saving-input/before.md').read_bytes(), candidate, request)
        return {**answer, 'pid': os.getpid()}

    replace = os.replace

    def injected(source, destination):
        relative = str(Path(destination).relative_to(project))
        if fault == 'archive_before_replace' and relative == 'archive/record.md':
            os._exit(73)
        if relative == 'record.md':
            if fault == 'current_before_replace':
                os._exit(73)
            if fault == 'current_replace_failure':
                raise OSError(5, 'injected current-file replacement failure')
        value = replace(source, destination)
        if fault == 'current_after_replace' and relative == 'record.md':
            os._exit(73)
        return value

    os.replace = injected
    try:
        archive = reconcile(namespace, project, 'archive/record.md',
                            (base / 'archive-input/archive-before.md').read_bytes(),
                            (base / 'archive-input/archive-candidate.md').read_bytes(), request)
        if archive['status'] not in ('saved', 'unchanged'):
            return {'status': archive['status'], 'migrationCompleted': False, 'archive': archive, 'pid': os.getpid()}
        if fault == 'between_commits':
            os._exit(73)
        current = reconcile(namespace, project, 'record.md',
                            (base / 'archive-input/current-before.md').read_bytes(),
                            (base / 'archive-input/current-candidate.md').read_bytes(), request)
        complete = current['status'] in ('saved', 'unchanged')
        unchanged = archive['status'] == current['status'] == 'unchanged'
        return {'status': 'unchanged' if unchanged else ('saved' if complete else current['status']),
                'migrationCompleted': complete, 'archive': archive, 'current': current, 'pid': os.getpid()}
    finally:
        os.replace = replace


def invoke(base, fixes, request_path, fault=None):
    command = [sys.executable, '-B', str(Path(__file__).resolve()), '--child', str(base),
               str(fixes), str(request_path.relative_to(base))]
    if fault:
        command.append(fault)
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        try:
            stdout, stderr = process.communicate(timeout=20)
        except subprocess.TimeoutExpired as error:
            process.kill()
            stdout, stderr = process.communicate()
            error.output = stdout
            error.stderr = stderr
            raise
        result = json.loads(stdout) if process.returncode == 0 else None
        assert process.returncode in (0, 73), (process.returncode, stdout, stderr)
        assert not stderr, stderr
        return {'exitCode': process.returncode, 'pid': process.pid, 'result': result}


def request_for(base, project, operation, readonly=False):
    targets = ['record.md'] if operation == 'save' else ['archive/record.md', 'record.md']
    return {'scope': 'isolated-simulated-user', 'operation': operation,
            'project': str(project.relative_to(base)), 'readonly': readonly,
            'allowed': [] if readonly else [name for target in targets for name in (target, target + '.pending')],
            'pendingEvidence': {str(file.relative_to(project)): digest(file.read_bytes())
                                for file in project.rglob('*.pending')}}


def recover_twice(base, fixes, project, operation, readonly=False):
    case = project.parent
    before = capture(base, project, case / 'before')
    request_path = case / 'request.json'
    save_json(request_path, request_for(base, project, operation, readonly))
    resume = invoke(base, fixes, request_path)
    assert resume['exitCode'] == 0
    after = capture(base, project, case / 'after')
    retry = invoke(base, fixes, request_path)
    assert retry['exitCode'] == 0
    final = capture(base, project, case / 'retry')
    assert after['files'] == final['files'], 'retry changed persisted state'
    if readonly:
        assert before['files'] == after['files'], 'read-only recovery wrote files'
    return {'before': before, 'after': after, 'retry': final, 'resume': resume, 'retryProcess': retry}


def archive_inputs(base, parse):
    folder = base / 'archive-input'
    folder.mkdir()
    current_bytes = (base / 'saving-input/candidate.md').read_bytes()
    current = parse(current_bytes)
    old_entry = copy.deepcopy(current['entries'][0])
    old_entry['id'] = 'archive-existing'
    old_entry['origin']['delta_id'] = 'archive/content-creator/isolated/1'
    delta = {'delta_id': old_entry['origin']['delta_id'], 'changes': [{'operation': 'add', 'entry': old_entry}]}
    delta_bytes = (json.dumps(delta, ensure_ascii=False, indent=2) + '\n').encode()
    (folder / 'existing-delta.json').write_bytes(delta_bytes)
    old_receipt = {'delta_id': delta['delta_id'], 'sha256': digest(delta_bytes),
                   'result_revision': 1, 'entry_ids': [old_entry['id']]}
    old = {'format_version': 1, 'role_key': 'content-creator', 'revision': 1,
           'entries': [old_entry], 'receipts': [old_receipt], 'history': []}
    archived = {**copy.deepcopy(old), 'revision': 2,
                'entries': [old_entry] + current['entries'],
                'receipts': [old_receipt] + current['receipts'],
                'history': [copy.deepcopy(old), copy.deepcopy(current)]}
    emptied = {**copy.deepcopy(current), 'revision': 2, 'entries': [], 'receipts': [], 'history': []}
    for name, data in [('archive-before.md', markdown(old)), ('archive-candidate.md', markdown(archived)),
                       ('current-before.md', current_bytes), ('current-candidate.md', markdown(emptied))]:
        parse(data)
        (folder / name).write_bytes(data)


def run(base, fixes):
    assert base.is_dir() and not any(base.iterdir()), 'use an empty isolated directory'
    shutil.copytree(fixes / 'saving-input', base / 'saving-input')
    subprocess.run([sys.executable, '-B', str(fixes / 'fault-harness.py'), str(base),
                    str(fixes / 'save-memory.py')], check=True, capture_output=True, text=True, timeout=40)
    probes = json.loads((base / 'probes.json').read_text())
    namespace = runpy.run_path(str(fixes / 'save-memory.py'))
    evidence = {'scope': 'isolated-simulated-user', 'performedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'method': 'fresh OS processes; fixture-authorized recovery of actual instrumented crash remnants',
                'harnessSha256': digest(Path(__file__).read_bytes()),
                'saveCodeSha256': digest((fixes / 'save-memory.py').read_bytes()),
                'faultHarnessSha256': digest((fixes / 'fault-harness.py').read_bytes()),
                'candidateSha256': digest((base / 'saving-input/candidate.md').read_bytes()),
                'saves': {}, 'readonly': {}, 'archives': {}}
    for mode in ('during_write', 'before_replace', 'after_replace'):
        assert probes['cases'][mode]['exit_code'] == 73
        for readonly in (False, True):
            project = base / 'cases' / (('readonly_' if readonly else 'save_') + mode) / 'project'
            shutil.copytree(base / 'probes' / mode, project)
            item = recover_twice(base, fixes, project, 'save', readonly)
            item['interruptionExitCode'] = probes['cases'][mode]['exit_code']
            evidence['readonly' if readonly else 'saves'][mode] = item
            answer = item['resume']['result']
            assert answer['classification'] == ('saved' if mode == 'after_replace' else 'not_saved')
            assert answer['status'] == ('unchanged' if mode == 'after_replace' else ('pending' if readonly else 'saved'))
            if not readonly:
                assert snapshot(project) == {'record.md': evidence['candidateSha256']}
                assert item['retryProcess']['result']['status'] == 'unchanged'

    archive_inputs(base, namespace['_parse'])
    for fault in ('archive_before_replace', 'between_commits', 'current_before_replace',
                  'current_after_replace', 'current_replace_failure'):
        project = base / 'cases' / fault / 'project'
        (project / 'archive').mkdir(parents=True)
        shutil.copyfile(base / 'archive-input/current-before.md', project / 'record.md')
        shutil.copyfile(base / 'archive-input/archive-before.md', project / 'archive/record.md')
        first_request = project.parent / 'first-request.json'
        save_json(first_request, request_for(base, project, 'archive'))
        first = invoke(base, fixes, first_request, fault)
        assert first['exitCode'] == (0 if fault == 'current_replace_failure' else 73)
        if first['result']:
            assert first['result']['migrationCompleted'] is False
        # Before any recovery, a complete entry and receipt must survive.
        archive = namespace['_parse']((project / 'archive/record.md').read_bytes())
        current = namespace['_parse']((project / 'record.md').read_bytes())
        assert any(entry['id'] == 'storage-fixture' for entry in archive['entries'] + current['entries'])
        assert any(receipt['delta_id'] == 'storage/content-creator/isolated/1'
                   for receipt in archive['receipts'] + current['receipts'])
        item = recover_twice(base, fixes, project, 'archive')
        item['firstAttempt'] = first
        assert item['resume']['result']['migrationCompleted'] is True
        assert item['retryProcess']['result']['status'] == 'unchanged'
        assert (project / 'archive/record.md').read_bytes() == (base / 'archive-input/archive-candidate.md').read_bytes()
        assert (project / 'record.md').read_bytes() == (base / 'archive-input/current-candidate.md').read_bytes()
        evidence['archives'][fault] = item

    unicode_root = base / 'unicode'
    unicode_root.mkdir()
    result = namespace['save_memory'](unicode_root, 'café.md',
                                     (base / 'saving-input/candidate.md').read_bytes(), None,
                                     {'café.md', 'café.md.pending', 'cafe\u0301.md'})
    assert result['status'] == 'pending' and not any(unicode_root.iterdir())
    assert any(issue['reason'] == 'authorized_path_alias' for issue in result['issues'])
    evidence['unicode'] = {'result': result, 'files': snapshot(unicode_root)}
    save_json(base / 'replay.json', evidence)
    print(json.dumps({'saveRecoveries': len(evidence['saves']), 'readonlyRecoveries': len(evidence['readonly']),
                      'archiveRecoveries': len(evidence['archives']), 'unicodeAlias': 'rejected'}, indent=2))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        request = json.loads((Path(sys.argv[2]) / sys.argv[4]).read_text())
        print(json.dumps(execute(Path(sys.argv[2]), Path(sys.argv[3]), request,
                                 sys.argv[5] if len(sys.argv) > 5 else None), ensure_ascii=False))
    else:
        run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
