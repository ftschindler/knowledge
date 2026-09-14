---
type: Principle
title: Order auto-fixers so later ones do not re-dirty earlier output
description: Chain auto-fixers so a later one cannot reintroduce changes an earlier one just made; run
  broad hygiene fixers last.
tags:
- principle
- situational
- software
- dx
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** When chaining multiple auto-fixers over the same files, order them so a
later fixer cannot reintroduce changes an earlier one just made - run the broad
whitespace/line-ending hygiene fixers last.

**When to apply.** *Situational* - only relevant once you have several fixers that
touch overlapping files (a formatter pipeline, a pre-commit chain). A single
fixer needs no ordering thought.

**Why.** Fixers aren't commutative: a formatter may rewrite a block that a
trailing-whitespace or end-of-file fixer then has to touch again, and if they run
in the wrong order you get a hook that reports "files were modified" on a second
pass, or an unstable result that never converges. Putting the general
file-hygiene fixers (line endings, final newline, trailing whitespace) *last* -
after the content formatters - lets each stage settle before the next.

**Snippet.**

```yaml
# ... content formatters (markdownlint --fix, ruff-format, yamlfmt) first ...
# general hygiene LAST so it cleans up after everything else:
- id: trailing-whitespace
- id: mixed-line-ending
- id: end-of-file-fixer
```

**How enforced.** Deliberate ordering in the hook config. **Situational** - a
pre-commit-flavoured instance; the general lesson is "fixer pipelines have
order-dependence, sequence them to converge". See also
[Autofix in the hook, don't just flag](autofix_in_the_hook_dont_just_flag.md).
