const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const root = path.join(__dirname, 'acceptance/results/learning/recovery');
const hash = (bytes) => crypto.createHash('sha256').update(bytes).digest('hex');
const read = (file) => fs.readFileSync(path.join(root, file));
const json = (file) => JSON.parse(read(file));
const memory = (file) => JSON.parse(read(file).toString().match(/```json\n([\s\S]*?)\n```/)[1]);

function snapshot(folder) {
  function files(directory) {
    return fs.readdirSync(directory, { withFileTypes: true }).flatMap((item) => {
      const file = path.join(directory, item.name);
      return item.isDirectory() ? files(file) : [file];
    });
  }
  return Object.fromEntries(files(folder).sort().map((file) =>
    [path.relative(folder, file), hash(fs.readFileSync(file))]));
}

function checkStages(item) {
  for (const stage of ['before', 'after', 'retry']) {
    assert.deepEqual(snapshot(path.join(root, item[stage].path)), item[stage].files);
  }
  assert.equal(item.resume.exitCode, 0);
  assert.equal(item.retryProcess.exitCode, 0);
  assert.equal(item.resume.result.pid, item.resume.pid);
  assert.equal(item.retryProcess.result.pid, item.retryProcess.pid);
  assert.notEqual(item.resume.pid, item.retryProcess.pid);
  assert.deepEqual(item.after.files, item.retry.files, 'retry changed persisted state');
}

test('fresh processes recover real interrupted saves and a repeated delta makes no changes', () => {
  const evidence = json('replay.json');
  assert.equal(evidence.harnessSha256, hash(fs.readFileSync(path.join(__dirname, 'acceptance/recovery-harness.py'))));
  for (const [field, file] of [['saveCodeSha256', 'save-memory.py'], ['faultHarnessSha256', 'fault-harness.py']]) {
    assert.equal(evidence[field], hash(fs.readFileSync(path.join(root, '../fixes', file))));
  }
  for (const mode of ['during_write', 'before_replace', 'after_replace']) {
    const item = evidence.saves[mode];
    checkStages(item);
    assert.equal(item.interruptionExitCode, 73);
    assert.deepEqual(item.before.files, snapshot(path.join(root, 'probes', mode)));
    assert.equal(item.resume.result.classification, mode === 'after_replace' ? 'saved' : 'not_saved');
    assert.equal(item.resume.result.cleanedPending, mode !== 'after_replace');
    assert.equal(item.after.files['record.md'], evidence.candidateSha256);
    assert.deepEqual(Object.keys(item.after.files), ['record.md']);
    const record = memory(`${item.after.path}/record.md`);
    assert.equal(record.revision, 1);
    assert.equal(record.receipts.length, 1);
    assert.equal(record.receipts[0].sha256, hash(read('saving-input/delta.json')));
    assert.equal(item.retryProcess.result.status, 'unchanged');
  }
});

test('read-only recovery inspects real crash remnants without cleaning or writing them', () => {
  const evidence = json('replay.json');
  for (const mode of ['during_write', 'before_replace', 'after_replace']) {
    const item = evidence.readonly[mode];
    checkStages(item);
    assert.deepEqual(item.before.files, snapshot(path.join(root, 'probes', mode)));
    assert.deepEqual(item.before.files, item.after.files);
    assert.equal(item.resume.result.cleanedPending, false);
    assert.equal(item.resume.result.status, mode === 'after_replace' ? 'unchanged' : 'pending');
  }
});

test('archive migration retains existing entries and recovers each two-commit failure boundary', () => {
  const evidence = json('replay.json');
  assert.deepEqual(Object.keys(evidence.archives).sort(), ['archive_before_replace', 'between_commits',
    'current_after_replace', 'current_before_replace', 'current_replace_failure'].sort());
  for (const [mode, item] of Object.entries(evidence.archives)) {
    checkStages(item);
    assert.equal(item.firstAttempt.exitCode, mode === 'current_replace_failure' ? 0 : 73);
    if (mode === 'current_replace_failure') assert.equal(item.firstAttempt.result.migrationCompleted, false);
    assert.equal(item.resume.result.migrationCompleted, true);
    assert.equal(item.retryProcess.result.status, 'unchanged');
    const archive = memory(`${item.after.path}/archive/record.md`);
    const current = memory(`${item.after.path}/record.md`);
    const originalArchive = memory('archive-input/archive-before.md');
    assert.equal(archive.revision, 2);
    assert.equal(current.revision, 2);
    assert.deepEqual(archive.entries[0], originalArchive.entries[0]);
    assert.deepEqual(archive.receipts[0], originalArchive.receipts[0]);
    assert.deepEqual(archive.entries.map((entry) => entry.id).sort(), ['archive-existing', 'storage-fixture']);
    assert.equal(archive.receipts.length, 2);
    assert.deepEqual(current.entries, []);
    assert.deepEqual(current.receipts, []);
    assert.deepEqual(Object.keys(item.after.files), ['archive/record.md', 'record.md']);
    const beforeArchive = memory(`${item.before.path}/archive/record.md`);
    const beforeCurrent = memory(`${item.before.path}/record.md`);
    assert.equal(item.before.files['archive/record.md'], hash(read(`archive-input/${mode === 'archive_before_replace' ? 'archive-before' : 'archive-candidate'}.md`)));
    assert.equal(item.before.files['record.md'], hash(read(`archive-input/${mode === 'current_after_replace' ? 'current-candidate' : 'current-before'}.md`)));
    assert.equal(archive.receipts[0].sha256, hash(read('archive-input/existing-delta.json')));
    assert.equal(archive.receipts[1].sha256, hash(read('saving-input/delta.json')));
    assert.ok([...beforeArchive.entries, ...beforeCurrent.entries].some((entry) => entry.id === 'storage-fixture'));
    assert.ok([...beforeArchive.receipts, ...beforeCurrent.receipts].some((receipt) => receipt.delta_id === archive.receipts[1].delta_id));
  }
});

test('NFC-equivalent authorized paths are rejected before creating files', () => {
  const item = json('replay.json').unicode;
  assert.equal(item.result.status, 'pending');
  assert.ok(item.result.issues.some((issue) => issue.reason === 'authorized_path_alias'));
  assert.deepEqual(item.files, {});
});

test('live timeout regression kills and reaps the child, preserves diagnostics and propagates failure', () => {
  const evidence = json('timeout/green.json');
  const red = json('timeout/red.json');
  const checks = evidence.checks;
  assert.equal(evidence.outcome, 'PASS');
  assert.equal(evidence.harnessSha256, hash(fs.readFileSync(path.join(__dirname, 'acceptance/recovery-harness.py'))));
  assert.equal(evidence.testSha256, hash(fs.readFileSync(path.join(__dirname, 'acceptance/test_recovery_timeout.py'))));
  assert.equal(red.outcome, 'FAIL');
  assert.equal(red.harnessSha256, hash(read('timeout/prior-recovery-harness.py')));
  assert.equal(red.testSha256, evidence.testSha256);
  assert.equal(red.checks.killCalls, 0);
  assert.ok(red.checks.elapsedSeconds >= red.checks.upperBoundSeconds);
  assert.equal(checks.exception, 'TimeoutExpired');
  assert.equal(checks.killCalls, 1);
  assert.ok(Number.isInteger(checks.childReturnCode));
  assert.notEqual(checks.childReturnCode, 0);
  assert.equal(checks.reaped, true);
  assert.ok(checks.elapsedSeconds < checks.upperBoundSeconds);
  assert.equal(checks.stdout, '{"status":"saved"}\n');
  assert.equal(checks.stderr, 'child waiting\n');
});
