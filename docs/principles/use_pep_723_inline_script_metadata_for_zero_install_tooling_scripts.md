---
type: Principle
title: Use PEP 723 inline script metadata for zero-install tooling scripts
description: Declare a standalone tooling script's dependencies inline with PEP 723, so it runs without
  a project install or virtualenv.
tags:
- principle
- software
- uv
- python
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** For small standalone tooling scripts, declare their dependencies in an
inline PEP 723 metadata block and run them with a launcher that provisions those
deps on the fly - so the script needs no project install or virtualenv.

**When to apply.** Small, self-contained utility/guard scripts (CI checks,
one-off tools). Not for application code that belongs to a project's own
dependency set.

**Why.** A guard script that imports `packaging` shouldn't force every consumer
to first install a project environment, nor should it silently depend on whatever
happens to be on the system Python. Inline metadata makes the script's
dependencies explicit and self-contained: the launcher reads the header, builds
an ephemeral environment, and runs it - reproducibly, with zero prior setup.

**Snippet.**

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["packaging"]
# ///
"""Ensure .python-version is consistent with requires-python."""
```

**How enforced.** Convention: standalone scripts carry a `# /// script` block and
are invoked via `uv run --script` (or equivalent). Pairs well with keeping such
guards runnable from pre-commit without a project sync.
