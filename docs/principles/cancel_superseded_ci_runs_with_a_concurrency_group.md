---
type: Principle
title: Cancel superseded CI runs with a concurrency group
description: Group CI runs by ref and cancel in-progress runs when a newer commit arrives, so runners
  are not spent on stale commits.
tags:
- principle
- software
- github-actions
- ci-cd
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Group CI runs by branch/ref and cancel in-progress runs when a newer
commit arrives, so runners aren't spent finishing work on stale commits.

**When to apply.** Push/PR-triggered pipelines where only the latest commit
matters. *Not* for jobs that must complete once started (deployments mid-flight,
release publishing) - there, cancellation can leave partial state.

**Why.** Without concurrency control, pushing three commits in quick succession
launches three full pipelines that all run to completion, wasting minutes and
delaying feedback on the commit you actually care about. A concurrency group
keyed on the ref cancels the obsolete runs automatically, giving faster feedback
and cheaper CI.

**Snippet.**

```yaml
concurrency:
  group: deploy_${{ github.head_ref || github.ref_name }}
  cancel-in-progress: true
```

**How enforced.** A `concurrency` block per workflow. Mind the exception above -
scope the group so long-running deploys you *don't* want cancelled use a
different (or no) cancellation policy. Pairs with
[Bound every CI job with an explicit timeout](bound_every_ci_job_with_an_explicit_timeout.md) - both stop runners being spent
on work that will never usefully finish.
