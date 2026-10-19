"""Replay a real agent-produced save in isolated processes with bounded faults.

This is acceptance instrumentation, not a project runtime or merge engine.
"""
import hashlib
import json
import os
from pathlib import Path
import runpy
import shutil
import stat
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def child(base, code, mode):
    folder = base / 'probes' / mode
    target_rel = 'archive/record.md' if mode == 'archive_create' else 'record.md'
    target = folder / target_rel
    pending = folder / (target_rel + '.pending')
    before = (base / 'saving-input/before.md').read_bytes()
    candidate = (base / 'saving-input/candidate.md').read_bytes()
    changed = (base / 'saving-input/changed.md').read_bytes()
    allowed = {target_rel, target_rel + '.pending'}
    if mode == 'missing_pending_authorization':
        allowed = {target_rel}
    real_replace, real_fsync, real_fdopen = os.replace, os.fsync, os.fdopen
    altered = False

    class PartialWrite:
        def __init__(self, output):
            self.output = output

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return self.output.__exit__(*args)

        def write(self, data):
            self.output.write(data[:max(1, len(data) // 3)])
            self.output.flush()
            real_fsync(self.output.fileno())
            os._exit(73)

    def fdopen(descriptor, flags, *args, **kwargs):
        output = real_fdopen(descriptor, flags, *args, **kwargs)
        if mode == 'during_write' and 'w' in flags:
            return PartialWrite(output)
        return output

    def fsync(descriptor):
        nonlocal altered
        info = os.fstat(descriptor)
        if mode == 'directory_sync_failure' and stat.S_ISDIR(info.st_mode):
            raise OSError(5, 'injected directory sync failure')
        answer = real_fsync(descriptor)
        if mode == 'stale_target' and not altered and stat.S_ISREG(info.st_mode):
            altered = True
            target.write_bytes(changed)
        return answer

    def replace(source, destination, *args, **kwargs):
        if mode == 'before_replace':
            os._exit(73)
        if mode == 'replace_failure':
            raise OSError(5, 'injected replace failure')
        if mode == 'unsupported_replace':
            raise NotImplementedError('injected unsupported replace')
        answer = real_replace(source, destination, *args, **kwargs)
        if mode == 'after_replace':
            os._exit(73)
        return answer

    os.fdopen, os.fsync, os.replace = fdopen, fsync, replace
    namespace = runpy.run_path(str(code))
    expected = None if mode in ('first_create', 'archive_create') else digest(before)
    result = namespace['save_memory'](folder, target_rel, candidate, expected, allowed)
    print(json.dumps(result, ensure_ascii=False))


def run(base, code):
    modes = ['normal', 'during_write', 'before_replace', 'after_replace',
             'first_create', 'archive_create', 'missing_pending_authorization',
             'pending_exists', 'stale_target', 'replace_failure',
             'unsupported_replace', 'pending_symlink', 'target_alias',
             'directory_sync_failure']
    before = (base / 'saving-input/before.md').read_bytes()
    candidate = (base / 'saving-input/candidate.md').read_bytes()
    changed = (base / 'saving-input/changed.md').read_bytes()
    evidence = {'method': 'actual isolated save calls; os._exit(73) at three injected process boundaries',
                'before_sha256': digest(before), 'candidate_sha256': digest(candidate),
                'changed_sha256': digest(changed), 'cases': {}}
    for mode in modes:
        folder = base / 'probes' / mode
        folder.mkdir(parents=True)
        target_rel = 'archive/record.md' if mode == 'archive_create' else 'record.md'
        target = folder / target_rel
        pending = folder / (target_rel + '.pending')
        if mode not in ('first_create', 'archive_create'):
            target.write_bytes(before)
        if mode == 'pending_exists':
            pending.write_bytes(b'preexisting partial candidate; never overwrite')
        linked = folder / 'protected.md'
        if mode in ('pending_symlink', 'target_alias'):
            linked.write_bytes(before)
            if mode == 'pending_symlink':
                pending.symlink_to('protected.md')
            else:
                target.unlink()
                os.link(linked, target)
        pending_before = pending.read_bytes() if pending.exists() else None
        linked_before = linked.read_bytes() if linked.exists() else None
        process = subprocess.run([sys.executable, '-B', __file__, '--child', str(base), str(code), mode],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
        actual = target.read_bytes() if target.exists() else None
        result = json.loads(process.stdout) if process.returncode == 0 else None
        item = {'exit_code': process.returncode, 'target': str(target.relative_to(base)),
                'before_sha256': digest(changed if mode == 'stale_target' else before),
                'target_sha256': digest(actual) if actual is not None else None,
                'pending_exists': pending.exists(), 'result': result, 'stderr': process.stderr}
        if pending_before is not None:
            item['pending_unchanged'] = pending.exists() and pending.read_bytes() == pending_before
        if linked_before is not None:
            item['linked_file_unchanged'] = linked.read_bytes() == linked_before
        evidence['cases'][mode] = item
        if mode in ('during_write', 'before_replace', 'after_replace'):
            assert process.returncode == 73, (mode, process.stdout, process.stderr)
            assert actual == (candidate if mode == 'after_replace' else before), mode
        else:
            assert process.returncode == 0, (mode, process.stderr)
            if mode in ('normal', 'first_create', 'archive_create', 'directory_sync_failure'):
                assert result['status'] == 'saved' and actual == candidate, (mode, result)
            else:
                assert result['status'] != 'saved', (mode, result)
                assert actual == (changed if mode == 'stale_target' else before), (mode, result)
        if pending_before is not None:
            assert item['pending_unchanged'], mode
        if linked_before is not None:
            assert item['linked_file_unchanged'], mode
    (base / 'probes.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({name: {'exit': case['exit_code'], 'status': case['result']['status'] if case['result'] else 'process interrupted'}
                      for name, case in evidence['cases'].items()}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--child':
        child(Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4])
    else:
        run(Path(sys.argv[1]), Path(sys.argv[2]))
