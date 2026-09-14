---
type: Principle
title: Document a rationale for every disabled lint rule
description: Every disabled or reconfigured lint rule carries an inline comment explaining why, so no
  suppression is indistinguishable from an accident.
tags:
- principle
- software
- linting
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Every lint rule you disable (or reconfigure away from its default)
must carry an inline comment explaining *why*. No silent, unexplained
suppressions.

**Why.** A bare `"MD013": false` is indistinguishable from an accident: a future
maintainer can't tell whether it's a considered decision or leftover cruft, so
they either cargo-cult it or remove it and reintroduce the problem it was
solving. A one-line rationale converts tribal knowledge into durable,
in-context documentation - read exactly where the decision lives - and makes it
safe to revisit later. The same logic extends to any per-line
`# noqa` / `# type: ignore`: name the reason.

**Snippet.**

```jsonc
{
  "config": {
    // MD013: Line length — disabled; prose wraps naturally, enforcing hurts readability
    "MD013": false,
    // MD046: Code block style — MkDocs admonitions look like indented code to the linter
    "MD046": false
  }
}
```

**How enforced.** Convention upheld in review: a disabled rule without a
rationale is a review blocker. Kin to
[Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md) - here the "invariant" is
that decisions stay explained.
