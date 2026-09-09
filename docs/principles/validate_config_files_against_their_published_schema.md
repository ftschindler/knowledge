---
type: Principle
title: Validate config files against their published schema
description: Lint your configuration as well as your content, by validating each config file against its
  tool's published JSON schema.
tags:
- principle
- software
- ci-cd
- linting
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Don't only lint your *content* - lint your *configuration* too, by
validating each config file against its tool's published JSON schema.

**When to apply.** Any config format with an available schema (most linters,
CI systems, `package.json`, etc.). Broadly applicable wherever a schema exists.

**Why.** A typo or stale key in a linter/CI config fails silently or, worse,
disables a check you thought was running - and content linting won't catch it
because the config itself is never inspected. Schema-validating the config turns
"this rule name is misspelt so it does nothing" into an immediate error. Pin the
schema to a specific version so it can't drift out from under you.

**Snippet.**

```yaml
- id: check-jsonschema
  name: Validate markdownlint-cli2 config schema
  files: .markdownlint-cli2.jsonc
  args: [--schemafile, 'https://.../v0.18.1/schema/....json']
```

**How enforced.** A `check-jsonschema` pre-commit hook, with the schema URL
pinned to the same tool version you actually run - a case of
[Keep declared toolchain versions in sync, and guard it](keep_declared_toolchain_versions_in_sync_and_guard_it.md).
