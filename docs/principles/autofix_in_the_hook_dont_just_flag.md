---
type: Principle
title: Autofix in the hook, don't just flag
description: Where a transform is deterministic and safe, have the hook fix the file in place instead
  of reporting it for a human to fix.
tags:
- principle
- software
- dx
- linting
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Where a tool can safely auto-correct an issue, have it *fix* the file
in place rather than merely reporting it for a human to fix manually.

**When to apply.** Deterministic, safe transforms (formatting, import sorting,
trailing-whitespace, canonical JSON, line endings). *Not* for changes needing
judgement (logic fixes, ambiguous lint rules) - those should flag, not auto-edit.

**Why.** A tool that only *reports* "line 40 has trailing whitespace" spends human
attention on mechanical toil and creates a nag-loop: run, read, hand-fix, re-run.
If the fix is deterministic, the machine should just apply it, leaving humans to
review a clean result. This shrinks review noise and makes the canonical form the
path of least resistance instead of a chore.

**Snippet.**

```yaml
- id: markdownlint-cli2
  args: [--config=.markdownlint-cli2.jsonc, --fix]   # fix, don't just report
- id: ruff-format
- id: pretty-format-json
  args: [--autofix]
```

**How enforced.** Prefer formatters and `--fix`/`--autofix` modes in the hook
chain. Order matters when several fixers touch the same files - see
[Order auto-fixers so later ones do not re-dirty earlier output](order_auto_fixers_so_later_ones_do_not_re_dirty_earlier_output.md).
