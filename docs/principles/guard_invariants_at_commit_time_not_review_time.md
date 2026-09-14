---
type: Principle
title: Guard invariants at commit-time, not review-time
description: Encode every repository invariant as an automated commit-time check rather than a rule a
  human reviewer must remember.
tags:
- principle
- software
- pre-commit
- ci-cd
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Encode every repository invariant you care about as an automated
check that runs at commit-time (pre-commit), not as a rule a human reviewer is
expected to remember.

**Why.** Human review is scarce, inconsistent, and forgetful: conventions
enforced only by "the reviewer will catch it" degrade the moment the reviewer is
busy, new, or the author self-merges. A machine check runs identically every
time, gives the author feedback in seconds instead of hours, and frees review
for judgement that *can't* be automated. The cost of writing a small guard is
paid once; the cost of manual vigilance is paid on every single change forever.

**Snippet.**

```yaml
# A local guard: forbid a footgun outright, with a rationale in the name
- id: no-obsidian-embeds
  name: Forbid Obsidian note embeds
  entry: '!\[\['
  language: pygrep
  files: '\.md$'
```

**How enforced.** This is the meta-principle behind the whole
`.pre-commit-config.yaml`. Its counterpart is [Mirror every local guard in CI](mirror_every_local_guard_in_ci.md)

- commit-time for fast feedback, CI so it can't be bypassed with `--no-verify`.

A common special case is the **footgun guard**: when a specific construct breaks
your toolchain, forbid it outright at commit-time rather than documenting "please
don't". The `no-obsidian-embeds` hook above, `no-horizontal-rules`, and
`no-pip-install-in-workflows` are all this pattern - a one-line grep guard is
cheaper and more reliable than a convention nobody remembers.
