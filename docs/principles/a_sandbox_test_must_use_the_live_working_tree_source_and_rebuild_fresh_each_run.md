---
type: Principle
title: A sandbox test must use the live working-tree source and rebuild fresh each run
description: A test that materialises your source into a sandbox must copy from the live working tree
  and rebuild the sandbox on every run.
tags:
- principle
- software
- testing
- dx
- repo-hygiene
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-31T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** When a test builds a sandbox (a fake HOME, a temp project, a container)
that copies in your source under test, it must copy from the **live working tree**
and rebuild the sandbox **fresh on every run** - never from a cached snapshot, a
committed-only copy, or a sandbox reused across runs.

**When to apply.** Any test that materialises your source into an isolated
environment before exercising it - e2e harnesses, install tests, fixtures that copy
files a tool then consumes. Especially where the source is edited in a tight
edit→test loop (skill markdown, config, templates).

**Why.** The whole point of the loop `edit → make test` is that the test reflects
what you *just changed*. If the sandbox copies from a git snapshot, a build cache,
or a home built once and reused, you silently test stale bytes: green runs prove
nothing about your edit, red runs point at code you already fixed. This is a
particularly nasty trap because it fails *invisibly* - the test runs, it just runs
against the wrong version.

**How.** Resolve the source path from the working tree (e.g. `REPO_ROOT / "skills"`
relative to the test file), copy it into a per-run temp directory that the test
framework allocates fresh each time (pytest's `tmp_path`, a new `mktemp`), and do
the copy inside setup that runs *every* test - not once at module import. Then
**verify the property holds**, because it is easy to regress: inject a unique
marker into a source file, run the sandbox builder, and assert the marker appears
in the copied artifact. If a deletion in your edit must also propagate, prefer a
fresh temp dir over `copytree(..., dirs_exist_ok=True)` into a reused one, so
removed files cannot linger.

**Tension to name.** Fresh-every-run costs time (reinstalling a runtime per run can
dominate an e2e loop). That is a real trade-off, but resolve it by caching the
*expensive immutable dependency* (the runtime binary), never the *source under
test* - the source must always be re-copied live. A long-lived manual sandbox is
fine for interactive poking, but it trades away the freshness guarantee, so it is
not what an automated test should use.
