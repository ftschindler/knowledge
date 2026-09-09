---
type: Principle
title: Pin GitHub Actions to full commit SHAs
description: Reference every third-party GitHub Action by full commit SHA, because a tag is mutable and
  runs with your secrets.
tags:
- principle
- software
- github-actions
- supply-chain
- security
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Reference every third-party GitHub Action by its full 40-character
commit SHA, not by a mutable tag like `@v4` or a branch.

**Why.** Tags are mutable: an attacker (or a compromised maintainer) can move
`v4` to point at malicious code, and your workflow - running with repository
secrets and write permissions - executes it silently. A SHA is immutable, so
you run exactly the code you reviewed. Keep the human-readable version in a
trailing comment so upgrades stay legible; let Dependabot bump both together.

**Snippet.**

```yaml
- uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0  # v6
- uses: astral-sh/setup-uv@fac544c07dec837d0ccb6301d7b5580bf5edae39  # v8.2.0
```

**How enforced.** Dependabot (`package-ecosystem: github-actions`) proposes SHA
bumps on a schedule; `actionlint` in pre-commit validates workflow syntax. See
[Pin pre-commit hooks to frozen revisions](pin_pre_commit_hooks_to_frozen_revisions.md) for the same principle applied one
layer down.
