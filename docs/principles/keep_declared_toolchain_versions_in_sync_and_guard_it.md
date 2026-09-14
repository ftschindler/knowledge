---
type: Principle
title: Keep declared toolchain versions in sync, and guard it
description: When the same fact is declared in two files, add an automated guard that fails on drift instead
  of documenting 'keep these in sync'.
tags:
- principle
- software
- uv
- python
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** When the same fact (e.g. the Python version) is declared in two
files, don't just document "keep these in sync" - add an automated guard that
fails when they drift.

**Why.** Any invariant maintained by human diligence eventually breaks: someone
bumps `pyproject.toml`'s `requires-python` and forgets `.python-version`, and CI
silently builds against a different interpreter than developers use. A comment
saying "keep in sync" records the intent but enforces nothing. A tiny check that
parses both and compares them turns a latent inconsistency into an immediate,
local failure.

**Snippet.**

```python
# .scripts/check_python_version.py (run as a pre-commit hook)
pinned = Path(".python-version").read_text().strip()
specifier = SpecifierSet(pyproject["project"]["requires-python"])
if Version(pinned) not in specifier:
    sys.exit(f"{pinned!r} not in requires-python {specifier!r}")
```

**How enforced.** A `local` pre-commit hook triggered on both files
(`files: '^(\.python-version|pyproject\.toml)$'`). A concrete case of
[Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md).

Where a machine check isn't practical, at least make the coupling *legible*: put
a comment at **each** site pointing at the other (`# ATTENTION: keep in sync with
X`). A paired reminder doesn't enforce the invariant, but it stops the drift
being invisible - the next editor sees the dependency before they break it. A
guard is better; paired comments are the floor.
