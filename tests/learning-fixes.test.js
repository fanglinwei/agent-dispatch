const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const root = path.join(__dirname, 'acceptance/results/learning/fixes');
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const json = (file) => JSON.parse(read(file));
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex');
const memory = (file) => JSON.parse(read(file).match(/```json\n([\s\S]*?)\n```/)[1]);

test('configuration handles reserved names and preserves existing stable keys with real paths', () => {
  const mappings = json('paths.json');
  for (const [scenario, item] of Object.entries(mappings)) {
    if (!['new_role', 'existing_role'].includes(scenario)) continue;
    const targets = [item.protocol, item.memory, item.archive, item.pending, item.archive_pending];
    assert.equal(new Set(targets.map((name) => path.normalize(name).toLowerCase())).size, targets.length);
    assert.equal(item.pending, `${item.memory}.pending`);
    assert.equal(item.archive_pending, `${item.archive}.pending`);
    assert.ok(item.guidance.includes(item.memory));
    assert.ok(item.guidance.includes(item.protocol));
    assert.ok(item.guidance.includes(item.role_key));
    const project = `configuration/${scenario}`;
    assert.equal(memory(`${project}/${item.memory}`).role_key, item.role_key);
    assert.equal(read(`${project}/${item.protocol}`), fs.readFileSync(path.join(__dirname, '../skills/agent-dispatch/assets/learning-protocol.md'), 'utf8'));
    const role = Object.fromEntries([...read(`${project}/.codex/agents/protocol.toml`).matchAll(/^(\w+) = (".*")$/gm)]
      .map(([, key, value]) => [key, JSON.parse(value)]));
    assert.equal(role.developer_instructions, read('configuration/original-instructions.txt') + item.guidance);
    const rules = read(`${project}/AGENTS.md`);
    for (const target of targets) assert.ok(rules.includes(target));
    assert.equal(fs.existsSync(path.join(root, project, item.pending)), false);
  }
  assert.notEqual(mappings.new_role.role_key, 'protocol');
  assert.notEqual(mappings.new_role.role_key, 'protocol-role', 'another role already holds this key');
  assert.equal(mappings.existing_role.role_key, 'protocol');
  assert.equal(mappings.existing_role.memory, 'records/protocol.md');
  assert.equal(read('configuration/existing_role/records/protocol.md'), read('configuration/existing-before.md'));
  assert.equal(hash('configuration/existing_role/records/protocol.md'), json('verification.json').preservedExistingMemory);
});

test('actual interrupted save processes leave complete old or new memory at the target', () => {
  const evidence = json('probes.json');
  const expected = { during_write: 'before', before_replace: 'before', after_replace: 'candidate' };
  for (const [name, state] of Object.entries(expected)) {
    const result = evidence.cases[name];
    assert.equal(result.exit_code, 73, `${name}: no actual injected process termination`);
    assert.equal(result.target_sha256, hash(result.target));
    assert.equal(result.target_sha256, evidence[`${state}_sha256`]);
    assert.deepEqual(memory(result.target), memory(`saving-input/${state}.md`));
  }
  const committed = memory(evidence.cases.after_replace.target);
  assert.equal(committed.receipts[0].result_revision, committed.revision);
  assert.equal(committed.receipts[0].sha256, hash('saving-input/delta.json'));
});

test('safe saves honor exact authorization, pending files, versions and replacement failures', () => {
  const evidence = json('probes.json');
  for (const name of ['normal', 'first_create', 'archive_create']) {
    const result = evidence.cases[name];
    assert.equal(result.exit_code, 0);
    assert.equal(result.target_sha256, evidence.candidate_sha256);
    assert.equal(hash(result.target), evidence.candidate_sha256);
    assert.equal(result.pending_exists, false);
  }
  for (const name of ['missing_pending_authorization', 'pending_exists', 'stale_target', 'replace_failure', 'unsupported_replace', 'pending_symlink', 'target_alias']) {
    const result = evidence.cases[name];
    assert.equal(result.exit_code, 0);
    assert.equal(result.target_sha256, result.before_sha256, `${name}: target was overwritten`);
    assert.equal(hash(result.target), result.before_sha256);
    assert.notEqual(result.result.status, 'saved');
  }
  assert.equal(evidence.cases.missing_pending_authorization.pending_exists, false);
  assert.equal(evidence.cases.pending_exists.pending_unchanged, true);
  assert.equal(evidence.cases.pending_symlink.linked_file_unchanged, true);
  assert.equal(evidence.cases.target_alias.linked_file_unchanged, true);
});

test('a directory sync failure reports the gap without rolling back a verified commit', () => {
  const evidence = json('probes.json');
  const result = evidence.cases.directory_sync_failure;
  assert.equal(result.exit_code, 0);
  assert.equal(hash(result.target), evidence.candidate_sha256);
  assert.equal(result.result.status, 'saved');
  assert.equal(result.result.sync.directory, 'failed');
  assert.ok(result.result.issues.length > 0);
});
