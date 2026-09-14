---
type: Principle
title: 'Keep a linear history: block merge, fixup and squash commits'
description: Enforce a rebase-only history by actively blocking merge commits and un-squashed fixup commits
  from landing on the main branch.
tags:
- principle
- software
- git
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

**Claim.** Enforce a rebase-only, linear history by actively blocking merge
commits and un-squashed `fixup!`/`squash!` commits from landing on the main
branch.

**Why.** A linear history is dramatically easier to read, bisect, revert and
reason about than one braided with merge commits. `fixup!`/`squash!` commits are
scaffolding for interactive rebase - if they reach the base branch, the author
forgot to autosquash, leaving noise in permanent history. Rather than hoping
contributors self-police, a CI guard makes the policy mechanical: the PR simply
cannot merge until the history is clean.

**Snippet.**

```python
# CI: fail if any commit in the PR is a merge commit
for commit in pr_commits:
    if len(commit["parents"]) > 1:
        raise RuntimeError("Merge commits are not allowed; please rebase.")
# (a sibling check greps commit messages for 'fixup!' / 'squash!')
```

**How enforced.** Two inline-Python steps in the governance workflow inspect the
PR's commits via the GitHub API. A domain-specific instance of
[Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md), enforced in CI where it
can't be bypassed.
