const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const root = path.join(__dirname, '..');
const names = ['agent-dispatch', 'agent-dispatch-doc'];
const readJson = (file) => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8'));

test('package, plugin and marketplace expose the same two skills', () => {
  const pkg = readJson('package.json');
  const plugin = readJson('.codex-plugin/plugin.json');
  const marketplace = readJson('.agents/plugins/marketplace.json');
  assert.equal(pkg.name, plugin.name);
  assert.equal(pkg.version, plugin.version);
  const entry = marketplace.plugins.find((item) => item.name === plugin.name);
  assert.ok(entry, 'marketplace must contain this plugin');
  assert.deepEqual(entry.source, {
    source: 'url',
    url: 'https://github.com/fanglinwei/agent-dispatch.git',
    ref: 'main',
  });
  const skills = path.resolve(root, plugin.skills);
  assert.equal(skills, path.join(root, 'skills'));
  assert.deepEqual(fs.readdirSync(skills).sort(), names);
  for (const name of names) {
    assert.ok(fs.statSync(path.join(skills, name, 'SKILL.md')).isFile());
    assert.ok(fs.statSync(path.join(skills, name, 'agents/openai.yaml')).isFile());
  }
});

function markdownFiles(folder) {
  return fs.readdirSync(folder, { withFileTypes: true }).flatMap((entry) => {
    const file = path.join(folder, entry.name);
    return entry.isDirectory() ? markdownFiles(file) : file.endsWith('.md') ? [file] : [];
  });
}

for (const name of names) {
  test(`${name} standalone install contains all local references`, (t) => {
    const temporary = fs.mkdtempSync(path.join(os.tmpdir(), 'agent-dispatch-skill-'));
    t.after(() => fs.rmSync(temporary, { recursive: true, force: true }));
    const installed = path.join(temporary, name);
    fs.cpSync(path.join(root, 'skills', name), installed, { recursive: true });
    for (const file of markdownFiles(installed)) {
      const markdown = fs.readFileSync(file, 'utf8');
      for (const [, href] of markdown.matchAll(/\]\(([^)]+)\)/g)) {
        if (/^[a-z][a-z0-9+.-]*:/i.test(href) || href.startsWith('#')) continue;
        const target = path.resolve(path.dirname(file), decodeURIComponent(href.split('#')[0]));
        const relative = path.relative(installed, target);
        assert.ok(relative !== '..' && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative),
          `${name}: reference must stay within the installed skill: ${href}`);
        assert.ok(fs.existsSync(target), `${name}: missing reference: ${href}`);
      }
    }
  });
}
