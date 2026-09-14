---
type: Principle
title: Split CI jobs for attributable failure and minimal dependencies
description: Split a CI workflow along the lines where failure should be attributable, and give each job
  only the toolchain it uses.
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
**Claim.** Split a CI workflow into separate jobs along the lines where a failure
should be *attributable*, and give each job only the toolchain it actually uses.
A red check should name the culprit by its job, and no job should install a
dependency it does not run.

**When to apply.** Any CI workflow covering more than one independent concern -
multiple languages, multiple test layers, build vs. lint. Not a single-purpose
pipeline where one linear sequence is the whole job.

**The two rules.**

1. **Split along failure-attribution lines.** One job per independently-failing
   concern. Node-script tests and Python-script tests become `node_tests` and
   `python_tests`, not one `fast` job running both - so a red X names the layer
   at fault before you open the log. The split axis is *what could fail
   independently*, not *what runs fast*; speed is a side effect, attribution is
   the goal.
2. **Give each job only its own dependencies.** The node job sets up node and no
   uv; the python job sets up uv and no node. A combined job that installs both
   toolchains couples them: the python layer waits on a node install it never
   uses, and a failure in either setup taints both concerns. Minimal per-job
   setup is the CI form of single-responsibility.

**Why.** CI's product is a *signal*, and a signal is only useful if it localizes.
A single job spanning two languages gives one bit ("something broke") where two
jobs give two ("the python layer broke"); the reader skips straight to the
failing layer. Minimal dependencies compound this: each job's setup is smaller,
faster, and cannot fail for a reason unrelated to what it tests - a wedged node
install can no longer redden a pure-python concern. The jobs also parallelize for
free once decoupled, but that is the dividend, not the reason.

**Snippet (coupled → split).**

```yaml
# Coupled: one job, both toolchains, failure names neither layer
jobs:
  fast:
    steps:
      - uses: actions/setup-node@…
      - uses: astral-sh/setup-uv@…
      - run: make test_node_scripts
      - run: make test_python_scripts

# Split: one job per attributable concern, each with only its own setup
jobs:
  node_tests:
    steps:
      - uses: actions/setup-node@…
      - run: make test_node_scripts
  python_tests:
    steps:
      - uses: astral-sh/setup-uv@…
      - run: make test_python_scripts
```

**How enforced.** Review the workflow by asking, of each job: if this goes red,
does its name tell me what broke? And: does it install anything it does not run?
Split on the first, trim on the second. Pairs with [Bound every CI job with an explicit timeout](bound_every_ci_job_with_an_explicit_timeout.md) (a per-job timeout is only attributable once jobs are split) and [Run CI steps under a strict shell (errexit, pipefail)](run_ci_steps_under_a_strict_shell_errexit_pipefail.md). Earned splitting a combined `fast` CI job into node-only and python-only jobs, each carrying just its own toolchain.
