const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const root = path.join(__dirname, '..');
const suite = path.join(__dirname, 'acceptance');
const read = (file) => fs.readFileSync(file, 'utf8');
const json = (file) => JSON.parse(read(file));
const hash = (file) => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');

function files(folder) {
  return fs.readdirSync(folder, { withFileTypes: true }).filter((entry) => entry.name !== '.DS_Store').flatMap((entry) => {
    const file = path.join(folder, entry.name);
    return entry.isDirectory() ? files(file) : [file];
  });
}

function snapshot(folder) {
  return Object.fromEntries(files(folder).sort().map((file) => [path.relative(folder, file), hash(file)]));
}

function role(file) {
  // shortcut: replay output uses JSON-quoted single-line TOML strings; native TOML parsing is also recorded in the live run.
  return Object.fromEntries(read(file).split('\n').filter((line) => line && !line.startsWith('#')).map((line) => {
    const match = line.match(/^(\w+) = (".*")$/);
    assert.ok(match, `${file}: expected a JSON-quoted TOML assignment`);
    return [match[1], JSON.parse(match[2])];
  }));
}

test('saved replay artifacts have validation for the current skill content', () => {
  const evidence = json(path.join(suite, 'results/replay.json'));
  assert.equal(evidence.version, json(path.join(root, 'package.json')).version);
  assert.deepEqual(evidence.skills, snapshot(path.join(root, 'skills')), 'skill content changed: rerun behavioral acceptance');
  assert.deepEqual(evidence.fixtures, snapshot(path.join(suite, 'fixtures')), 'fixture changed: rerun behavioral acceptance');
  const outputs = snapshot(path.join(suite, 'results'));
  delete outputs['replay.json'];
  assert.deepEqual(evidence.outputs, outputs, 'artifacts changed after the live replay');
  assert.equal(evidence.nativeTomlParse, 'PASS');
  assert.equal(evidence.scope, 'isolated-simulated-user');
  if (evidence.revalidation || evidence.priorSkills) {
    assert.ok(evidence.revalidation && evidence.priorSkills, 'retain prior provenance when reusing unaffected evidence');
    assert.ok(fs.existsSync(path.join(suite, 'results', evidence.revalidation.report)));
  }
});

test('first configuration and actual addition preserve upstream bodies, provenance and license', () => {
  const fixture = path.join(suite, 'fixtures/team');
  const source = json(path.join(fixture, 'source.json'));
  assert.match(source.commit, /^[a-f0-9]{40}$/);
  for (const entry of source.files) {
    assert.equal(hash(path.join(fixture, 'upstream', entry.path)), entry.sha256);
    assert.equal(entry.url, `https://raw.githubusercontent.com/msitarzewski/agency-agents/${source.commit}/${entry.path}`);
  }
  const initial = path.join(suite, 'results/team/initial/.codex/agents');
  const added = path.join(suite, 'results/team/after-addition/.codex/agents');
  assert.deepEqual(fs.readdirSync(initial).sort(), ['LICENSE.agency-agents', 'content-creator.toml']);
  assert.deepEqual(fs.readdirSync(added).sort(), ['LICENSE.agency-agents', 'content-creator.toml', 'legal-compliance-checker.toml']);
  for (const [upstream, output, folder] of [
    ['marketing/marketing-content-creator.md', 'content-creator.toml', initial],
    ['support/support-legal-compliance-checker.md', 'legal-compliance-checker.toml', added],
  ]) {
    const original = read(path.join(fixture, 'upstream', upstream));
    const frontmatter = original.match(/^---\n([\s\S]*?)\n---\n/);
    const configured = role(path.join(folder, output));
    assert.equal(configured.name, frontmatter[1].match(/^name: (.*)$/m)[1]);
    assert.equal(configured.description, frontmatter[1].match(/^description: (.*)$/m)[1]);
    const roleKey = output.replace(/\.toml$/, '');
    const guidance = read(path.join(root, 'skills/agent-dispatch/assets/role-learning.txt')).replaceAll('ROLE_KEY', roleKey);
    assert.equal(configured.developer_instructions, original.slice(frontmatter[0].length) + guidance);
    assert.ok(read(path.join(folder, output)).includes(`/blob/${source.commit}/${upstream}`));
    assert.equal(read(path.join(folder, 'LICENSE.agency-agents')), read(path.join(fixture, 'upstream/LICENSE')));
  }
});

test('generated learning is project local, preserves upstream duties and starts without invented experience', () => {
  for (const stage of ['initial', 'after-addition']) {
    const project = path.join(suite, 'results/team', stage);
    const protocol = path.join(project, '.codex/agent-memory/protocol.md');
    assert.equal(read(protocol), read(path.join(root, 'skills/agent-dispatch/assets/learning-protocol.md')));
    const keys = stage === 'initial' ? ['content-creator'] : ['content-creator', 'legal-compliance-checker'];
    for (const key of keys) {
      const file = path.join(project, '.codex/agent-memory', `${key}.md`);
      const record = JSON.parse(read(file).match(/```json\n([\s\S]*?)\n```/)[1]);
      assert.equal(record.format_version, 1);
      assert.equal(record.role_key, key);
      assert.equal(record.revision, 0);
      assert.deepEqual(record.entries, []);
      assert.deepEqual(record.receipts, []);
      assert.ok(read(path.join(project, 'AGENTS.md')).includes(`.codex/agent-memory/${key}.md`));
    }
    assert.ok(!fs.existsSync(path.join(project, '.codex/agent-memory/archive')), 'empty archives are not needed');
  }
});

test('addition preserves existing customization and repeated dispatch makes no changes', () => {
  const team = path.join(suite, 'results/team');
  const oldFile = path.join(team, 'before-addition/.codex/agents/content-creator.toml');
  const newFile = path.join(team, 'after-addition/.codex/agents/content-creator.toml');
  assert.equal(read(oldFile), read(newFile));
  const original = role(oldFile);
  assert.equal(original.model, 'gpt-6.1-sol');
  assert.equal(original.model_reasoning_effort, 'high');
  assert.ok(original.developer_instructions.includes('用户定制：本项目审稿'));
  const beforeRules = read(path.join(team, 'before-addition/AGENTS.md'));
  assert.ok(read(path.join(team, 'after-addition/AGENTS.md')).startsWith(beforeRules));
  const repeated = json(path.join(suite, 'results/repeat.json'));
  assert.deepEqual(repeated.before, snapshot(path.join(team, 'after-addition')));
  assert.deepEqual(repeated.after, repeated.before);
  assert.deepEqual(repeated.workspaceAfter, repeated.workspaceBefore);
  assert.equal(repeated.action, 'reuse');
});

test('team documentation has real contributions and reviews while preserving the confirmation gate', () => {
  const fixture = path.join(suite, 'fixtures/documents');
  const output = path.join(suite, 'results/documents');
  const evidence = json(path.join(suite, 'results/replay.json')).documents;
  const roles = fs.readdirSync(path.join(fixture, 'roles')).map((name) => name.replace(/\.toml$/, '')).sort();
  assert.deepEqual(Object.keys(evidence.participants).sort(), roles);
  for (const [name, contribution] of Object.entries(evidence.participants)) {
    assert.ok(contribution.agent, `${name}: missing actual invocation identity`);
    for (const kind of ['contribution', 'review']) {
      const file = path.join(suite, 'results', contribution[kind]);
      assert.ok(fs.statSync(file).size > 0, `${name}: missing ${kind} artifact`);
      assert.equal(hash(file), contribution[`${kind}Sha256`]);
    }
    assert.ok(read(path.join(suite, 'results', contribution.review)).includes(evidence.implementationSha256), `${name}: review does not identify this draft`);
  }
  assert.equal(read(path.join(output, 'AGENTS.md')), read(path.join(fixture, 'AGENTS.md')));
  assert.deepEqual(snapshot(path.join(output, 'roles')), snapshot(path.join(fixture, 'roles')));
  assert.deepEqual(snapshot(path.join(output, 'skills')), snapshot(path.join(fixture, 'skills')));
  assert.equal(read(path.join(output, 'docs/legacy-design.md')), read(path.join(fixture, 'docs/legacy-design.md')));
  assert.equal(evidence.status, 'DRAFT');
  assert.equal(evidence.contentConfirmed, false);
  assert.equal(evidence.projectExecution, 'NOT_RUN');
  assert.match(read(path.join(output, 'docs/README.md')), /\bDRAFT\b/);
  const implementation = path.join(output, 'docs/implementation.md');
  assert.equal(hash(implementation), evidence.implementationSha256, 'draft changed after professional review');
  for (const [name, contribution] of Object.entries(evidence.participants)) {
    const content = read(path.join(suite, 'results', contribution.contribution)).replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').trim();
    assert.ok(read(implementation).includes(content), `${name}: contribution was not integrated`);
  }
});

test('only the separately simulated content confirmation promotes the implementation entry', () => {
  const evidence = json(path.join(suite, 'results/replay.json')).promotion;
  assert.equal(evidence.simulatedUser, true);
  assert.equal(evidence.professionalReviewComplete, true);
  assert.equal(evidence.contentConfirmed, true);
  const draft = path.join(suite, 'results/documents');
  const promoted = path.join(suite, 'results/promoted');
  const decision = read(path.join(suite, 'results/plans/content-confirmation.md'));
  assert.ok(decision.includes(json(path.join(suite, 'results/replay.json')).documents.implementationSha256), 'approval must identify the reviewed draft');
  assert.ok(read(path.join(promoted, 'AGENTS.md')).startsWith(read(path.join(draft, 'AGENTS.md'))));
  assert.ok(read(path.join(promoted, 'AGENTS.md')).includes('docs/README.md'));
  assert.match(read(path.join(promoted, 'docs/README.md')), /\bCONFIRMED\b/);
  assert.equal(read(path.join(promoted, 'docs/implementation.md')), read(path.join(draft, 'docs/implementation.md')));
  assert.equal(read(path.join(promoted, 'docs/legacy-design.md')), read(path.join(draft, 'docs/legacy-design.md')));
  assert.deepEqual(snapshot(path.join(promoted, 'roles')), snapshot(path.join(draft, 'roles')));
  assert.deepEqual(snapshot(path.join(promoted, 'skills')), snapshot(path.join(draft, 'skills')));
});

test('new documentation resolves local references without depending on legacy design', () => {
  const folder = path.join(suite, 'results/documents/docs');
  for (const name of ['README.md', 'implementation.md']) {
    const file = path.join(folder, name);
    for (const [, href] of read(file).matchAll(/\]\(([^)]+)\)/g)) {
      if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('#')) continue;
      const target = path.resolve(path.dirname(file), decodeURIComponent(href.split('#')[0]));
      assert.notEqual(target, path.join(folder, 'legacy-design.md'), 'new implementation must stand on its own');
      assert.ok(fs.existsSync(target), `${file}: unresolved reference ${href}`);
    }
  }
});
