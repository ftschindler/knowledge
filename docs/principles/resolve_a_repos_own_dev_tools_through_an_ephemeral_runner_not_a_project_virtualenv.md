---
type: Principle
title: Resolve a repo's own dev tools through an ephemeral runner, not a project virtualenv
description: Resolve tools a repo runs on itself through an ephemeral runner, so a git hook does not depend
  on a virtualenv that is easily absent.
tags:
- principle
- software
- dx
- tooling
- ci
- git
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** When a tool a repository uses on itself must keep working outside the
project environment - most sharply, a **git hook** - resolve it through an
ephemeral runner (`uvx`, `pipx run`, `npx`) rather than the project virtualenv or
a required system install. The hook then depends only on the ephemeral runner
being present, not on a `.venv` that is easily absent or stale.

**When to apply.** Any tool invoked by machinery that runs on a bare checkout:
git hooks installed into `.git/hooks`, `bootstrap`-style setup targets, anything
a contributor hits before (or without) syncing the project environment. It is
the counter-case to running dev tools via the project venv, which is otherwise
fine for CI and interactive use.

**Why.** A pre-commit installer bakes an **absolute path to whichever executable
ran it** into `.git/hooks/pre-commit`, then falls back to the tool's name on
`PATH`:

```sh
PREK="/repo/.venv/bin/prek"
if [ ! -x "$PREK" ]; then PREK="prek"; fi
exec "$PREK" hook-impl ...
```

Install via the project venv (`uv run prek install`) and that baked path points
into `.venv`. The hook does not re-resolve per commit; it runs the path it was
given at install time. So the moment the venv is rebuilt, wiped, relocated, or
simply never created (a fresh clone that has not synced yet), the path goes
stale and every commit silently degrades to the `PATH` fallback - or errors, if
nothing is on `PATH` either. Install via `uvx prek install` and the baked path
points into the runner's own tool cache, which is independent of the project
venv and survives all of those. The hook keeps working with only the runner
installed and no `.venv` at all.

**Snippet.**

```console
# venv-independent: hook path survives a missing/rebuilt .venv
$ uvx prek install
# vs. fragile: hook points at .venv/bin/prek, breaks when the venv moves
$ uv run prek install
```

**How enforced.** Convention: the `bootstrap` target and setup docs use the
ephemeral form (`uvx prek install`), never `uv run … install`, for anything that
writes a git hook. This narrows the [frozen -lockfile-everywhere](install_from_a_frozen_lockfile_in_ci.md) reflex: freezing is right for CI and reproducible runs,
but a git hook is not a CI step - it must survive a missing environment, so it
trades lockfile-pinning for path stability. Keep the tool in the dependency
manifest only if something else still resolves it from the lock; otherwise see
[Do not make a tool a prerequisite for work it is not needed for](do_not_make_a_tool_a_prerequisite_for_work_it_is_not_needed_for.md).
