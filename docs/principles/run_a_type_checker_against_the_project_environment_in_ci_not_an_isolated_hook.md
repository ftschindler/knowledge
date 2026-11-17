---
type: Principle
title: Run a type checker against the project environment in CI, not in an isolated hook
description: A type checker needs the project's dependencies to say anything true, so it belongs in a CI
  job that installs them, with any local hook optional and reading the same configuration.
tags:
- principle
- software
- python
- type-checking
- ci-cd
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T20:00:00+01:00'
sources:
- id: mirrors-mypy
  resource: https://github.com/pre-commit/mirrors-mypy
  title: 'pre-commit/mirrors-mypy: README'
  last_modified: '2026-11-17'
- id: pre-commit-ci-13
  resource: https://github.com/pre-commit-ci/issues/issues/13
  title: 'pre-commit-ci/issues#13: Support for manual dependency management for local repos, system or script entry-points'
  last_modified: '2023-02-02'
- id: pre-commit-ci-config
  resource: https://pre-commit.ci/
  title: 'pre-commit.ci: configuration'
  last_modified: '2026-11-17'
---
**Claim.** Run a Python type checker as a CI job that installs the project's real
dependencies, not as a pre-commit hook in an environment of its own. A local hook is an
optional convenience on top, and reads the same configuration as the CI job.

**When to apply.** Any project whose code imports libraries the checker must understand, which
is every project beyond a standalone script. The sharpest case is a numerical library, whose
stack of NumPy, SciPy and compiled extras is large and hard to restate.

**Why.** A type checker is only as truthful as the imports it can resolve, and a hook cannot
resolve them.

- **The hook's environment is empty.** pre-commit installs each hook into an isolated
  virtualenv, so mypy's own hook runs without the project's dependencies and defaults to
  `--ignore-missing-imports`[^mirrors-mypy]. Every unresolved import becomes `Any`, and the
  check passes on code it never understood.
- **Restating the dependencies drifts.** The fix the hook offers is `additional_dependencies`, a
  second list beside the lockfile that nobody updates with it. That is the drift
  [Keep declared toolchain versions in sync, and guard it](keep_declared_toolchain_versions_in_sync_and_guard_it.md)
  exists to stop.
- **pre-commit.ci cannot fetch them either.** Its free tier runs hooks with no network access,
  and does not support installing anything for a `local`, `system` or `script`
  hook[^pre-commit-ci-13]. A hook that relies on the developer's environment has to be listed
  under `ci: skip`[^pre-commit-ci-config].
- **A checker needs the whole program.** pre-commit passes the changed files, whilst a type
  error usually surfaces in an unchanged caller. The hook needs `pass_filenames: false` and
  checks the whole package on every commit.
- **It cannot fix anything.** A checker only reports, so the slow feedback buys no automatic
  fix, which puts it low on the list
  [Autofix in the hook, don't just flag](autofix_in_the_hook_dont_just_flag.md) draws up.

A CI job has none of these problems. It installs the dependencies the tests install, from the
same lockfile, and its red check names the type checker rather than the test suite, as
[Split CI jobs for attributable failure and minimal dependencies](split_ci_jobs_for_attributable_failure_and_minimal_dependencies.md)
wants.

**Snippet.**

```yaml
# The authority: a CI job of its own, against the locked environment
type-check:
  runs-on: ubuntu-latest
  timeout-minutes: 15
  steps:
  - uses: actions/checkout@<sha>
  - uses: astral-sh/setup-uv@<sha>
  - name: Type-check the package against the locked dependencies
    run: uv run --frozen pyright
```

```yaml
# Optional, local only: the same checker, the developer's environment
- repo: local
  hooks:
  - id: pyright
    name: pyright
    entry: uv run --frozen pyright
    language: system
    types: [python]
    pass_filenames: false
    stages: [manual]
ci:
  skip: [pyright]
```

**How enforced.** The CI job is the gate. Both it and any hook read one configuration, in
`pyproject.toml`, so that "passed locally" and "passed CI" mean the same thing, which is
[Mirror every local guard in CI](mirror_every_local_guard_in_ci.md) applied to a check that
cannot be mirrored by running the same hook.

This deliberately cuts against
[Resolve a repo's own dev tools through an ephemeral runner, not a project virtualenv](resolve_a_repos_own_dev_tools_through_an_ephemeral_runner_not_a_project_virtualenv.md).
That principle keeps a hook working without a virtualenv; a type checker without one has
nothing true to say. That is why the local hook stays optional, here on the manual stage, rather
than guarding every commit.
