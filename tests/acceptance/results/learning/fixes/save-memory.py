"""One serial, authorized save of a complete version-1 project memory record.

The caller owns merging, evidence/approval checks, the single-writer guarantee,
and recovery of an existing .pending. This module performs no work on import.
"""

import errno
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import unicodedata


class _Invalid(ValueError):
    pass


def _relative(value):
    if not isinstance(value, str) or not value or '\\' in value or '\x00' in value:
        raise _Invalid('invalid_relative_path')
    parts = value.split('/')
    if value.startswith('/') or any(part in ('', '.', '..') for part in parts):
        raise _Invalid('noncanonical_relative_path')
    return PurePosixPath(value)


def _path_key(value):
    return unicodedata.normalize('NFC', value).casefold()


def _digest(data):
    return hashlib.sha256(data).hexdigest()


def _is_hash(value):
    return isinstance(value, str) and re.fullmatch(r'[0-9a-fA-F]{64}', value) is not None


def _walk(root, relative):
    """Reject aliases rather than silently broadening an exact authorization."""
    path = root
    parts = _relative(relative).parts
    for index, part in enumerate(parts):
        if path.is_dir():
            if any(name != part and _path_key(name) == _path_key(part)
                   for name in os.listdir(path)):
                raise _Invalid('case_alias')
        path = path / part
        try:
            info = path.lstat()
        except FileNotFoundError:
            return None
        if stat.S_ISLNK(info.st_mode):
            raise _Invalid('symlink_path')
        if index < len(parts) - 1:
            if not stat.S_ISDIR(info.st_mode):
                raise _Invalid('nondirectory_parent')
        elif not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise _Invalid('nonregular_or_hardlinked_file')
        if os.path.commonpath((str(root), os.path.realpath(path))) != str(root):
            raise _Invalid('path_outside_root')
    return info


def _check_paths(root, allowed):
    inodes = {}
    for relative in sorted(allowed):
        info = _walk(root, relative)
        if info is not None:
            identity = (info.st_dev, info.st_ino)
            if identity in inodes:
                raise _Invalid('file_alias')
            inodes[identity] = relative


def _parents(root, relative, allowed):
    path = root
    for part in _relative(relative).parts[:-1]:
        path = path / part
        try:
            path.mkdir(mode=0o700)
        except FileExistsError:
            pass
        _check_paths(root, allowed)
        info = path.lstat()
        if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise _Invalid('unsafe_parent')


def _read(path):
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0)
    descriptor = os.open(path, flags)
    with os.fdopen(descriptor, 'rb') as source:
        before = os.fstat(source.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
            raise _Invalid('nonregular_or_hardlinked_file')
        data = source.read()
        after = os.fstat(source.fileno())
        fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns')
        if any(getattr(before, field) != getattr(after, field) for field in fields):
            raise _Invalid('file_changed_during_read')
    return data


def _json_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _Invalid('duplicate_json_key')
        result[key] = value
    return result


def _parse(data):
    text = data.decode('utf-8')
    if text.lstrip().startswith('{'):
        body = text
    else:
        fence = None
        lines = []
        body = None
        for line in text.splitlines():
            if fence is None:
                match = re.fullmatch(r' {0,3}(`{3,}|~{3,})([^\r\n]*)', line)
                if match:
                    marker, info = match.groups()
                    fence = (marker[0], len(marker), info.strip() == 'json')
                    lines = []
            elif re.fullmatch(r' {0,3}' + re.escape(fence[0]) +
                              '{' + str(fence[1]) + r',}[ \t]*', line):
                if fence[2]:
                    body = '\n'.join(lines)
                    break
                fence = None
            elif fence[2]:
                lines.append(line)
        if body is None:
            raise _Invalid('missing_complete_json_block')
    def nonfinite(_value):
        raise _Invalid('nonfinite_json_number')
    record = json.loads(body, object_pairs_hook=_json_pairs, parse_constant=nonfinite)
    if not isinstance(record, dict) or type(record.get('format_version')) is not int or record['format_version'] != 1:
        raise _Invalid('unsupported_record_format')
    if not isinstance(record.get('role_key'), str) or not record['role_key']:
        raise _Invalid('missing_role_key')
    if 'history' not in record:
        raise _Invalid('missing_history')
    all_ids, all_receipts, fingerprints = set(), [], {}

    def snapshot(item):
        if not isinstance(item, dict) or type(item.get('revision')) is not int or item['revision'] < 0:
            raise _Invalid('invalid_revision')
        for field in ('entries', 'receipts'):
            if not isinstance(item.get(field), list):
                raise _Invalid('invalid_' + field)
        entry_ids = set()
        for entry in item['entries']:
            fields = {'id', 'kind', 'status', 'summary', 'scope', 'sources',
                      'verification', 'action', 'recheck_when', 'origin'}
            if not isinstance(entry, dict) or not fields.issubset(entry):
                raise _Invalid('incomplete_entry')
            if not isinstance(entry['id'], str) or not entry['id'] or entry['id'] in entry_ids:
                raise _Invalid('invalid_or_duplicate_entry_id')
            if entry['kind'] not in ('fact', 'decision', 'correction', 'responsibility'):
                raise _Invalid('invalid_entry_kind')
            if entry['status'] not in ('candidate', 'active', 'recheck', 'archived'):
                raise _Invalid('invalid_entry_status')
            for field in ('summary', 'scope', 'action', 'recheck_when'):
                if not isinstance(entry[field], str) or not entry[field].strip():
                    raise _Invalid('invalid_entry_' + field)
            if not isinstance(entry['sources'], list):
                raise _Invalid('invalid_sources')
            for source in entry['sources']:
                if not isinstance(source, dict):
                    raise _Invalid('invalid_source')
                _relative(source.get('path'))
                if not _is_hash(source.get('sha256')) and not (
                        isinstance(source.get('version'), str) and source['version'].strip()):
                    raise _Invalid('missing_source_version_or_hash')
            if not isinstance(entry['verification'], (dict, str)) or not entry['verification']:
                raise _Invalid('missing_verification')
            if not isinstance(entry['origin'], dict) or not entry['origin']:
                raise _Invalid('missing_origin')
            entry_ids.add(entry['id'])
        all_ids.update(entry_ids)
        delta_ids = set()
        for receipt in item['receipts']:
            if not isinstance(receipt, dict):
                raise _Invalid('invalid_receipt')
            delta_id = receipt.get('delta_id')
            ids = receipt.get('entry_ids')
            revision = receipt.get('result_revision')
            if (not isinstance(delta_id, str) or not delta_id or delta_id in delta_ids
                    or not _is_hash(receipt.get('sha256')) or type(revision) is not int or revision < 0
                    or not isinstance(ids, list) or not ids
                    or any(not isinstance(identity, str) or not identity for identity in ids)
                    or len(set(ids)) != len(ids)):
                raise _Invalid('incomplete_or_duplicate_receipt')
            fingerprint = (receipt['sha256'].lower(), revision, tuple(sorted(ids)))
            if delta_id in fingerprints and fingerprints[delta_id] != fingerprint:
                raise _Invalid('conflicting_receipt')
            fingerprints[delta_id] = fingerprint
            delta_ids.add(delta_id)
            all_receipts.append(receipt)
        history = item.get('history', [])
        if not isinstance(history, list):
            raise _Invalid('invalid_history')
        for previous in history:
            snapshot(previous)

    snapshot(record)
    if any(not set(receipt['entry_ids']).issubset(all_ids) for receipt in all_receipts):
        raise _Invalid('receipt_without_entry')
    return record


def _sync(descriptor):
    try:
        os.fsync(descriptor)
        return 'synced'
    except OSError as error:
        unsupported = {errno.EINVAL, errno.ENOSYS, getattr(errno, 'ENOTSUP', -1),
                       getattr(errno, 'EOPNOTSUPP', -1)}
        if error.errno in unsupported:
            return 'unsupported'
        raise


def save_memory(root, target_rel, candidate_bytes, expected_sha256, allowed_paths):
    """Save one complete candidate using its exact authorized .pending path.

    expected_sha256=None asserts that the target did not exist. Return status is
    saved, unchanged, pending, or unknown. `pending` describes this save attempt,
    not proof that a delta is absent from all project history/archives. A saved
    result establishes complete bytes/record equality, not truth of its entries.
    Inspect `sync` and `issues` for a durability gap even when status is saved.
    """
    result = {'status': 'pending', 'learning_status': '待保存', 'committed': False,
              'reason': '', 'phase': 'preflight', 'target': target_rel,
              'pending_retained': None, 'sync': {'file': 'not_attempted', 'directory': 'not_attempted'},
              'issues': []}
    root_path = target = pending = candidate = original = original_record = None
    allowed = None
    replace_started = replace_returned = False

    def issue(error):
        result['issues'].append({'type': type(error).__name__, 'errno': getattr(error, 'errno', None),
                                 'reason': str(error) if isinstance(error, _Invalid) else 'operation_failed'})

    def state(status, reason):
        result['status'] = status
        result['learning_status'] = {'saved': '已保存', 'unchanged': '无增量',
                                     'pending': '待保存', 'unknown': '状态未知'}[status]
        result['reason'] = reason
        if status == 'unknown':
            result['committed'] = None
        elif status == 'saved':
            result['committed'] = True
        if pending is not None:
            try:
                result['pending_retained'] = pending.lstat() is not None
            except FileNotFoundError:
                result['pending_retained'] = False
            except OSError:
                result['pending_retained'] = None
        return result

    def after_error():
        try:
            _check_paths(root_path, allowed)
            try:
                observed = _read(target)
            except FileNotFoundError:
                observed = None
            if observed is not None:
                observed_record = _parse(observed)
                result['target_sha256'] = _digest(observed)
                result['observed_revision'] = observed_record['revision']
                if replace_started and observed == candidate_bytes and observed_record == candidate:
                    return state('saved', 'candidate_verified_after_error')
            if not replace_returned and observed == original:
                return state('pending', 'save_failed_original_preserved')
        except Exception as error:
            issue(error)
        return state('unknown', 'target_requires_reconciliation')

    try:
        _relative(target_rel)
        result['pending'] = target_rel + '.pending'
        if not isinstance(allowed_paths, (set, frozenset)):
            raise _Invalid('allowed_paths_must_be_set')
        allowed = set(allowed_paths)
        for relative in allowed:
            _relative(relative)
        if target_rel not in allowed or result['pending'] not in allowed:
            raise _Invalid('both_exact_paths_must_be_authorized')
        folded = [_path_key(str(_relative(relative))) for relative in allowed]
        if len(set(folded)) != len(folded):
            raise _Invalid('authorized_path_alias')
        folded_set = set(folded)
        if any('/'.join(relative.split('/')[:length]) in folded_set
               for relative in folded for length in range(1, len(relative.split('/')))):
            raise _Invalid('authorized_file_directory_conflict')
        if expected_sha256 is not None and not _is_hash(expected_sha256):
            raise _Invalid('invalid_expected_sha256')
        if not isinstance(candidate_bytes, bytes):
            raise _Invalid('candidate_must_be_bytes')
        candidate = _parse(candidate_bytes)
        result['candidate_sha256'] = _digest(candidate_bytes)
        result['candidate_revision'] = candidate['revision']
        root_path = Path(root).resolve(strict=True)
        if not root_path.is_dir():
            raise _Invalid('root_must_be_directory')
        target = root_path.joinpath(*_relative(target_rel).parts)
        pending = root_path.joinpath(*_relative(result['pending']).parts)
        _check_paths(root_path, allowed)
        result['phase'] = 'read_current'
        try:
            original = _read(target)
        except FileNotFoundError:
            original = None
        if original is not None:
            try:
                original_record = _parse(original)
            except Exception as error:
                issue(error)
                return state('unknown', 'current_record_not_verified')
            result['target_sha256'] = _digest(original)
            result['observed_revision'] = original_record['revision']
        actual_hash = None if original is None else _digest(original)
        expected = None if expected_sha256 is None else expected_sha256.lower()
        if actual_hash != expected:
            return state('pending', 'expected_target_changed')
        try:
            pending.lstat()
        except FileNotFoundError:
            pass
        else:
            return state('pending', 'existing_pending_requires_recovery')
        if original == candidate_bytes:
            return state('unchanged', 'no_increment')
        if original_record is not None:
            if candidate['role_key'] != original_record['role_key']:
                raise _Invalid('role_key_changed')
            if candidate['revision'] <= original_record['revision']:
                raise _Invalid('revision_must_increase')
        result['phase'] = 'create_parents'
        _parents(root_path, target_rel, allowed)
        _check_paths(root_path, allowed)
        result['phase'] = 'stage'
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
        descriptor = os.open(pending, flags, 0o600)
        with os.fdopen(descriptor, 'wb') as output:
            output.write(candidate_bytes)
            output.flush()
            result['sync']['file'] = 'failed'
            result['sync']['file'] = _sync(output.fileno())
        result['phase'] = 'verify_pending'
        _check_paths(root_path, allowed)
        staged = _read(pending)
        if staged != candidate_bytes or _parse(staged) != candidate:
            raise _Invalid('pending_not_equal_to_candidate')
        result['phase'] = 'recheck_target'
        try:
            current = _read(target)
        except FileNotFoundError:
            current = None
        if current is not None:
            current_record = _parse(current)
            result['target_sha256'] = _digest(current)
            result['observed_revision'] = current_record['revision']
        if current != original or (current is not None and current_record['revision'] != original_record['revision']):
            return state('pending', 'target_changed_after_staging')
        _check_paths(root_path, allowed)
        if _read(pending) != candidate_bytes:
            raise _Invalid('pending_changed_before_replace')
        result['phase'] = 'replace'
        replace_started = True
        os.replace(pending, target)
        replace_returned = True
        result['phase'] = 'verify_target'
        _check_paths(root_path, allowed)
        committed = _read(target)
        if committed != candidate_bytes or _parse(committed) != candidate:
            raise _Invalid('target_not_equal_to_candidate')
        result['target_sha256'] = _digest(committed)
        result['observed_revision'] = candidate['revision']
        result['phase'] = 'sync_directory'
        result['sync']['directory'] = 'failed'
        directory = os.open(target.parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0)
                            | getattr(os, 'O_NOFOLLOW', 0))
        try:
            try:
                result['sync']['directory'] = _sync(directory)
            except Exception:
                result['sync']['directory'] = 'failed'
                raise
        finally:
            os.close(directory)
        result['phase'] = 'complete'
        return state('saved', 'candidate_verified')
    except Exception as error:
        issue(error)
        if result['phase'] in ('stage', 'verify_pending', 'recheck_target', 'replace', 'verify_target', 'sync_directory'):
            return after_error()
        return state('pending', 'preflight_or_parent_creation_failed')
