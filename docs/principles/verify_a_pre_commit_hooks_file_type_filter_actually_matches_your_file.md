---
type: Principle
title: Verify a pre-commit hook's file-type filter actually matches your file
description: 'A hook''s files: regex is ANDed with its built-in type filter, so a non-matching type makes
  the hook a no-op that still reports success.'
tags:
- principle
- software
- pre-commit
- linting
- ci-cd
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** When you point a shared pre-commit hook at a file via `files:`, confirm
the file is not silently dropped by the hook's built-in `types`/`types_or`
filter - the two are ANDed, and a non-matching type makes the hook a no-op that
still reports success.

**Why.** A hook's `files:` regex only narrows the set; the hook's own
`types_or:` (baked into its `.pre-commit-hooks.yaml`) must *also* match, or the
file never reaches the entry. The failure is silent and dangerous: the run shows
`(no files to check) Skipped` - not an error - so a schema-validation or lint
hook you believe is guarding a config is doing nothing. This is the same class
of trap as a misspelt rule name: the check exists on paper and enforces nothing.

The concrete case that motivated this: `check-jsonschema` ships
`types_or: [json, yaml]`, but `identify` tags a `.markdownlint-cli2.jsonc` file
as only `[file, text]` - neither `json` nor `yaml`. The hook silently skipped the
config it was added to validate.

**How enforced.** Two habits: (1) after adding a hook, run it and confirm it
prints `Passed`, not `Skipped` - a skip on the file you targeted is a red flag,
not a pass; (2) override the type filter to a tag `identify` actually assigns to
the file. Note the override value must be a tag the runner recognises - e.g.
`prek` rejects a bare `jsonc` tag - so widen to a known supertype:

```yaml
- id: check-jsonschema
  name: Validate markdownlint-cli2 config against schema
  files: ^\.markdownlint-cli2\.jsonc$
  types_or: [text]   # .jsonc is tagged only [file,text]; the default [json,yaml] never matches
  args: [--schemafile, 'https://.../v0.23.2/schema/....json']
```

A concrete companion to [Validate config files against their published schema](validate_config_files_against_their_published_schema.md)

- the schema check is only real if its file filter matches. Sibling of
[Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md).
