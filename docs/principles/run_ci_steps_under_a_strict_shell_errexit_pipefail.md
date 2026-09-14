---
type: Principle
title: Run CI steps under a strict shell (errexit, pipefail)
description: Run CI steps under a strict shell with errexit and pipefail, so a failure anywhere in a pipe
  fails the step.
tags:
- principle
- software
- ci-cd
- github-actions
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Run CI `run:` steps under a strict shell - errexit, nounset-where-safe,
and crucially `pipefail` - instead of the platform's lenient default, so any
failure in a command *or anywhere in a pipe* fails the step.

**When to apply.** Any CI `run:` step, especially ones that pipe (`cmd | tee`,
`cmd | grep`) or chain multiple commands.

**Why.** By default a shell reports only the exit status of the *last* command in
a pipeline. `failing-check | tee log.txt` exits 0 because `tee` succeeded, so a
red check renders as a green step - a silent false pass, the worst CI failure
mode. `set -o pipefail` propagates the failure of any pipe element; `-e`
(errexit) aborts on the first failing command rather than plowing ahead. Setting
this once at the job level makes every step fail honestly by construction,
instead of relying on each script author to remember.

**Snippet.**

```yaml
jobs:
  governance:
    defaults:
      run:
        shell: bash -elo pipefail {0}   # -e errexit, -l login, -o pipefail
```

**How enforced.** A job-level `defaults.run.shell`, so it applies to every step
without per-step boilerplate. Complements [Mirror every local guard in CI](mirror_every_local_guard_in_ci.md):
mirroring the guards is pointless if a piped guard can fail without failing the
build.
