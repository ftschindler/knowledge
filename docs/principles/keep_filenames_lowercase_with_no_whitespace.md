---
type: Principle
title: Keep filenames lowercase with no whitespace
description: Restrict committed filenames to lowercase without spaces, enforced by a guard, wherever portability
  matters.
tags:
- principle
- situational
- software
- repo-hygiene
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Restrict committed filenames to lowercase with no spaces (use hyphens
or underscores), enforced by a guard.

**When to apply.** *Situational* - strong default for portability-sensitive repos
(cross-OS, URLs, static sites), but plenty of ecosystems legitimately require
mixed-case or specific names (`README.md`, `Makefile`, `CODEOWNERS`, Java class
files), so maintain an explicit exception list rather than applying blindly.

**Why.** Mixed-case and whitespace filenames cause real breakage: case-insensitive
filesystems (macOS, Windows) collide `File.md` with `file.md`, spaces break URLs
and shell scripts, and static-site generators derive slugs from filenames. A
lowercase-no-whitespace rule makes paths portable and predictable across every
consumer - with a short allowlist for the well-known exceptions.

**Snippet.**

```yaml
- id: lowercase-no-whitespace-filenames
  language: fail
  files: '[\sA-Z]'
  exclude: '^(README\.md|CONTRIBUTING\.md|LICENSE|Makefile)$'
```

**How enforced.** A pattern-matching pre-commit guard with an explicit `exclude`
allowlist. **Situational**: keep and curate the exception list per ecosystem.
