---
type: Principle
title: Bound every CI job with an explicit timeout
description: Set a tight explicit timeout on every CI job rather than inheriting the platform's six-hour
  default.
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
**Claim.** Set `timeout-minutes` on every CI job to a tight, realistic ceiling
instead of relying on the platform default.

**When to apply.** Any CI job. Especially valuable for jobs that shell out to
network installs, package managers, or interactive tools that can hang.

**Why.** GitHub Actions defaults each job to a **6-hour** timeout. A step that
hangs - a wedged network install, a process waiting on stdin that never comes, a
deadlock - will occupy a runner for hours, burning minutes, blocking the
concurrency slot, and delaying the failure signal you need. A tight per-job
ceiling (e.g. 5 minutes for a lint/guard suite) turns "hangs silently for hours"
into "fails loudly in minutes", which is the outcome you actually want from CI.

**Two ways to calibrate the ceiling.** They differ in intent, and the right one
depends on how noisy the job's duration is:

- **Margin above p99** - size the ceiling a comfortable margin over the observed
  worst-case so normal runs never trip it. Use when duration varies (network
  installs, variable-size test sets); the timeout is a *cost bound* that only
  fires on a genuine hang.
- **Tripwire at expected duration** - for a job whose runtime is near-constant
  and short (seconds), set the cap just above that, with a comment like
  `# something is off if we need more than this`. Here the timeout is an *anomaly
  detector*: any run that approaches it signals something changed - a stall, a
  retry loop, an unexpected input - not merely runaway cost. The tighter the
  known duration, the more the timeout earns its keep as a tripwire.

**Snippet.**

```yaml
jobs:
  governance:
    runs-on: ubuntu-latest
    timeout-minutes: 5
```

**How enforced.** An explicit `timeout-minutes:` on each job. Pairs naturally
with [Cancel superseded CI runs with a concurrency group](cancel_superseded_ci_runs_with_a_concurrency_group.md) - both keep runners
from being wasted on work that will never usefully finish.
