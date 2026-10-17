const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const names = ['agent-dispatch', 'agent-dispatch-doc'];
const root = path.join(__dirname, '..', 'skills');
const quoted = '("(?:[^"\\\\\\r\\n]|\\\\.)*")';

function validateMetadata(markdown, yaml, name) {
  // shortcut: validate this repository's fixed YAML layout; use a YAML parser if the layout expands.
  const frontmatter = markdown.replace(/\r\n/g, '\n').match(
    new RegExp(`^---\nname: ([a-z0-9-]+)\ndescription: ${quoted}\n---\n`));
  assert.ok(frontmatter, 'frontmatter must contain name and a JSON-quoted description');
  assert.equal(frontmatter[1], name, 'skill name must match its directory');
  const description = JSON.parse(frontmatter[2]);
  assert.ok(description.trim() && description.length <= 1024, 'description must be nonempty and at most 1024 characters');
  const policy = yaml.replace(/\r\n/g, '\n').match(new RegExp(
    `^interface:\n  display_name: ${quoted}\n  short_description: ${quoted}\n  default_prompt: ${quoted}\npolicy:\n  allow_implicit_invocation: false\n?$`));
  assert.ok(policy, 'metadata must contain the interface and boolean allow_implicit_invocation: false');
  const [, displayName, shortDescription, defaultPrompt] = policy.map((value, index) => index ? JSON.parse(value) : value);
  assert.ok(displayName.trim() && defaultPrompt.trim(), 'display name and default prompt must be nonempty');
  assert.ok(shortDescription.trim() && shortDescription.length >= 25 && shortDescription.length <= 64, 'short description must be nonempty and 25–64 characters');
}

for (const name of names) {
  const markdown = fs.readFileSync(path.join(root, name, 'SKILL.md'), 'utf8');
  const yaml = fs.readFileSync(path.join(root, name, 'agents/openai.yaml'), 'utf8');
  test(`${name} has valid required metadata and explicit-only invocation`, () => {
    validateMetadata(markdown, yaml, name);
    validateMetadata(markdown.replace(/\n/g, '\r\n'), yaml.replace(/\n/g, '\r\n'), name);
  });
  for (const [reason, changedMarkdown, changedYaml] of [
    ['wrong skill name', markdown.replace(`name: ${name}\n`, 'name: wrong-name\n'), yaml],
    ['missing frontmatter', markdown.replace(/^---\n/, ''), yaml],
    ['missing description', markdown.replace(/^description:.*\n/m, ''), yaml],
    ['invalid quoted scalar', markdown.replace(/description: "/, 'description: "\\q'), yaml],
    ['empty description', markdown.replace(/^description:.*$/m, 'description: ""'), yaml],
    ['implicit invocation', markdown, yaml.replace('invocation: false', 'invocation: true')],
    ['missing policy', markdown, yaml.replace(/policy:\n[\s\S]*/, '')],
    ['string instead of boolean', markdown, yaml.replace('invocation: false', 'invocation: "false"')],
    ['duplicate policy', markdown, `${yaml}policy:\n  allow_implicit_invocation: true\n`],
  ]) {
    test(`${name} rejects ${reason}`, () => assert.throws(() => validateMetadata(changedMarkdown, changedYaml, name)));
  }
}
