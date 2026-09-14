---
type: Principle
title: Install from a frozen lockfile in CI
description: Install dependencies in CI from the committed lockfile in frozen mode, failing when it is
  stale rather than silently resolving.
tags:
- principle
- software
- ci-cd
- supply-chain
- reproducibility
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** In CI, install dependencies from the committed lockfile in
**frozen** mode - fail if the lockfile is out of date rather than silently
resolving or updating it.

**When to apply.** Any CI job that installs dependencies with a lockfile-aware
tool (`uv run --frozen`, `npm ci`, `pnpm install --frozen-lockfile`, `cargo
build --locked`, `poetry install`). Broadly applicable.

**Why.** A plain install command may re-resolve versions, pull "latest
compatible", or quietly rewrite the lockfile - so CI runs against a dependency
set that differs from what the developer committed and what a fresh checkout
would get. That reintroduces "works on my machine" at the CI layer and lets
dependency drift pass review unnoticed. Frozen mode makes the lockfile the
single source of truth: CI installs *exactly* the pinned graph, and a stale or
hand-edited lockfile becomes a hard, visible failure instead of silent drift.

**Snippet.**

```yaml
# uv: --frozen refuses to update uv.lock; runs exactly the committed graph
- name: Run pre-commit hooks
  run: uv run --frozen --all-groups prek run --all-files
```

**How enforced.** The `--frozen` / `--locked` / `ci` install flag on the CI
install step. Part of the reproducibility family alongside
[Pin transitive runtime dependencies, not just the tool](pin_transitive_runtime_dependencies_not_just_the_tool.md) and
[Pin GitHub Actions to full commit SHAs](pin_github_actions_to_full_commit_shas.md) - freeze each layer so the same
commit always yields the same build.
