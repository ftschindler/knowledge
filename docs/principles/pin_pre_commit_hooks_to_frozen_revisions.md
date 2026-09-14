---
type: Principle
title: Pin pre-commit hooks to frozen revisions
description: Pin every pre-commit hook repo to an immutable revision, because hooks run arbitrary code
  against your working tree.
tags:
- principle
- software
- pre-commit
- supply-chain
- security
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Pin every pre-commit hook `repo` to an immutable revision (a frozen
tag resolved to its SHA), not a floating branch or bare tag.

**Why.** Pre-commit hooks run arbitrary code on every commit and in CI, with
access to your working tree. A floating `rev` means the toolchain can change
under you between two clean checkouts - silently altering lint results or, worse,
executing tampered code. Freezing to a SHA (with the tag in a comment) makes the
toolchain reproducible and auditable; upgrades become explicit, reviewable diffs.

**Snippet.**

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: c59bba8fb259db0fec2bbb77ad8ba51ea7341b56  # frozen: v0.15.20
  hooks:
  - id: ruff-check
  - id: ruff-format
```

**How enforced.** `pre-commit autoupdate --freeze` (or Dependabot's `pre-commit`
ecosystem) resolves tags to SHAs; the `# frozen: <tag>` comment keeps them
legible. Sibling of [Pin GitHub Actions to full commit SHAs](pin_github_actions_to_full_commit_shas.md).
