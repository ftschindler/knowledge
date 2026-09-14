---
type: Principle
title: Declare formatting once, editor-agnostically, via .editorconfig
description: Define basic formatting once at the repo root in .editorconfig, so every editor honours it
  independently of personal settings.
tags:
- principle
- software
- repo-hygiene
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Ship an `.editorconfig` so basic formatting (indentation, charset,
final newline, trailing whitespace) is defined once at the repo root and honoured
by every editor, independent of each contributor's personal settings.

**When to apply.** Broadly - any repo with more than one contributor or more than
one machine. Near-universal; little reason to skip.

**Why.** Without a shared baseline, formatting depends on whoever's editor touched
the file last, producing noisy diffs and pointless churn. `.editorconfig` is
understood natively (or via plugin) by essentially every editor and IDE, so the
rules apply *while you type* rather than only at commit-time - catching drift at
the earliest possible moment and keeping formatter/linter fights to a minimum.

**Snippet.**

```ini
# .editorconfig
root = true
[*]
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
charset = utf-8
indent_style = space
```

**How enforced.** Presence of `.editorconfig` at the root; editors apply it
automatically. It is the editor-time layer that complements commit-time guards
like [Enforce LF line endings everywhere](enforce_lf_line_endings_everywhere.md).
