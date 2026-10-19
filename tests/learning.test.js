const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const suite = path.join(__dirname, 'acceptance');
const output = path.join(suite, 'results/learning');
const read = (file) => fs.readFileSync(file, 'utf8');
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const json = (file) => JSON.parse(read(file));
const memory = (file) => JSON.parse(read(file).match(/```json\n([\s\S]*?)\n```/)[1]);
// shortcut: saved fixture TOML uses JSON-quoted strings; the live run also parses it with tomllib.
const role = (file) => Object.fromEntries([...read(file).matchAll(/^(\w+) = (".*")$/gm)]
  .map(([, key, value]) => [key, JSON.parse(value)]));

test('a role corrects a real draft and a fresh context uses the persisted project memory', () => {
  const evidence = json(path.join(output, 'replay.json'));
  const project = path.join(output, 'project');
  const fixed = read(path.join(project, 'outputs/repair.md'));
  const reused = read(path.join(project, 'outputs/reuse.md'));
  assert.match(fixed, /周一/);
  assert.doesNotMatch(fixed, /周日/);
  assert.match(reused, /周二/);
  assert.notEqual(evidence.repair.agent, evidence.reuse.agent, 'reuse requires a fresh agent context');
  assert.equal(evidence.reuse.forkTurns, 'none');
  assert.doesNotMatch(read(path.join(output, evidence.reuse.prompt)), /周二|0.*周一|1.*周二/, 'dispatch must not reveal the tested answer');
  const saved = memory(path.join(project, '.codex/agent-memory/content-creator.md'));
  assert.equal(saved.role_key, 'content-creator');
  assert.equal(saved.entries.length, 1);
  assert.equal(saved.entries[0].status, 'active');
  assert.equal(saved.entries[0].kind, 'correction');
  const contract = saved.entries[0].sources.find((source) => source.path === 'day-contract.md');
  assert.equal(contract.sha256, hash(path.join(project, contract.path)));
  const deltaFile = path.join(project, 'outputs/repair-delta.json');
  const delta = json(deltaFile);
  assert.equal(saved.receipts[0].delta_id, delta.delta_id);
  assert.equal(saved.receipts[0].sha256, hash(deltaFile));
  assert.equal(saved.receipts[0].result_revision, saved.revision);
  assert.deepEqual(saved.receipts[0].entry_ids, [saved.entries[0].id]);
  assert.equal(evidence.noIncrement.before, evidence.noIncrement.after);
  assert.equal(evidence.noIncrement.after, hash(path.join(project, '.codex/agent-memory/content-creator.md')));
});

test('legacy migration preserves customization and a renamed role retains its stable memory', () => {
  const lifecycle = path.join(output, 'lifecycle');
  const file = '.codex/agents/content-creator.toml';
  const before = role(path.join(lifecycle, 'legacy-before', file));
  const after = role(path.join(lifecycle, 'legacy-after', file));
  const guidance = read(path.join(__dirname, '../skills/agent-dispatch/assets/role-learning.txt'))
    .replaceAll('ROLE_KEY', 'content-creator');
  assert.deepEqual(after, { ...before, developer_instructions: before.developer_instructions + guidance });
  assert.ok(read(path.join(lifecycle, 'legacy-after/AGENTS.md'))
    .startsWith(read(path.join(lifecycle, 'legacy-before/AGENTS.md'))));
  const active = role(path.join(output, 'project', file));
  const renamed = role(path.join(lifecycle, 'renamed/.codex/agents/community-editor.toml'));
  assert.deepEqual(renamed, { ...active, name: 'Community Editor' });
  const memoryPath = '.codex/agent-memory/content-creator.md';
  assert.equal(read(path.join(lifecycle, 'renamed', memoryPath)), read(path.join(output, 'project', memoryPath)));
  assert.equal(fs.existsSync(path.join(lifecycle, 'renamed/.codex/agent-memory/community-editor.md')), false);
  assert.ok(read(path.join(lifecycle, 'renamed/AGENTS.md')).includes('| content-creator | Community Editor |'));
});

test('saved boundary exercises retain actual inputs and read-only project bytes', () => {
  const evidence = json(path.join(output, 'replay.json'));
  assert.equal(evidence.scope, 'isolated-simulated-user');
  assert.deepEqual(evidence.readonly.before, evidence.readonly.after);
  const expected = ['candidate', 'missing', 'attribution', 'authority', 'changed-source', 'instances',
    'writer', 'interrupted', 'archive', 'readonly', 'lifecycle', 'stopping', 'standalone-doc'];
  assert.deepEqual(Object.keys(evidence.boundaries).sort(), expected.sort());
  for (const [name, result] of Object.entries(evidence.boundaries)) {
    assert.ok(result.agent && result.assessment, `${name}: missing actual evaluator and main assessment`);
    assert.equal(result.outcome, 'PASS', `${name}: unresolved exercise`);
    assert.equal(hash(path.join(output, result.response)), result.sha256);
    assert.ok(fs.statSync(path.join(output, result.input)).size > 0, `${name}: missing input`);
  }
});
