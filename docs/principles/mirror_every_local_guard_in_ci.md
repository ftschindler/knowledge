---
type: Principle
title: Mirror every local guard in CI
description: Run the exact same guard suite in CI that developers run locally, because commit hooks are
  trivially bypassed and CI is not.
tags:
- principle
- software
- ci-cd
- pre-commit
- github-actions
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Run the exact same pre-commit suite in CI that developers run
locally - don't let the two drift into different rule sets.

**Why.** Commit-time hooks give fast feedback but are trivially bypassed
(`git commit --no-verify`, a misconfigured environment, a contributor who never
installed them). CI is the boundary that *can't* be skipped, so it must be the
authority. Running the identical config in both places (rather than
reimplementing a subset in CI) guarantees "passes locally" and "passes CI" mean
the same thing, and removes the class of bug where a check exists in one place
but not the other.

**Snippet.**

```yaml
# governance.yml — CI runs the same prek/pre-commit config, on all files
- name: Run pre-commit hooks
  run: uv run --frozen --all-groups --all-extras prek run --all-files
```

**How enforced.** One CI job invokes the whole `.pre-commit-config.yaml` against
`--all-files`, so local and CI enforcement are the same set by construction. The
fast-feedback half is [Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md). Mind
that a mirrored guard only fails honestly under
[Run CI steps under a strict shell (errexit, pipefail)](run_ci_steps_under_a_strict_shell_errexit_pipefail.md).
