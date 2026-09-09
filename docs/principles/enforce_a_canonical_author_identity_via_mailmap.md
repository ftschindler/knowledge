---
type: Principle
title: Enforce a canonical author identity via .mailmap
description: Map every contributor's name and email variants to one canonical identity in .mailmap, and
  check it mechanically.
tags:
- principle
- situational
- software
- git
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Map every contributor's name/email variants to one canonical identity
in a `.mailmap`, and check it mechanically so new unmapped identities can't creep
in.

**When to apply.** *Situational* - multi-contributor repos, or any project where
clean attribution/history matters (shortlog, changelog generation). Overkill for
a solo throwaway repo.

**Why.** People commit under several names and emails (work laptop, personal
machine, web edits), which fragments `git shortlog`, contributor counts and
changelog attribution. A `.mailmap` collapses the variants to one identity; a CI
check that flags any commit author missing from it keeps the map complete over
time instead of silently rotting.

**Snippet.**

```gitattributes
# .mailmap
Proper Name <canonical@example.com> <old-or-alt@example.com>
```

**How enforced.** A `.mailmap` plus a guard that scans `git log` for authors
absent from it (a case of [Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md)).
Mark this one **situational**: enforce only where attribution quality is worth
the friction.
