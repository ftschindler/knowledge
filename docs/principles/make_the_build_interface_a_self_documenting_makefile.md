---
type: Principle
title: Make the build interface a self-documenting Makefile
description: Expose common tasks through one entry point whose help listing is generated from the task
  definitions themselves.
tags:
- principle
- software
- build
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Expose the project's common tasks through a single, self-documenting
task entry point whose help listing is generated from the task definitions
themselves, so the interface documents itself. A `Makefile` is one
implementation; `just`, `task`, `npm`/`pnpm` scripts or a `scripts/` dispatcher
serve the same role.

**When to apply.** Broadly - any project with more than a couple of routine
commands. Pick whatever runner fits the ecosystem; the principle is the
*self-documenting single entry point*, not the tool.

**Why.** New contributors and CI should share one obvious entry point -
`make bootstrap`, `just serve`, `npm run build` - instead of memorising long tool
invocations that live only in someone's shell history or a wiki page. Generating
the help listing from annotated tasks means the documentation can't fall out of
date: adding a task adds its help line automatically. It also decouples *what* you
want done from *how* it's currently done, so the underlying command can change
without retraining anyone.

**Snippet.**

```makefile
## Install dependencies and pre-commit hooks
bootstrap:
 uv sync && uv run prek install

## Show available targets (generated from the ## comments above)
help:
 @grep -B1 '^[a-z]' $(MAKEFILE_LIST) | grep '^##' | sed 's/## /  /'
```

**How enforced.** Convention: each task carries a one-line description the help
target scrapes. The runner becomes the single contract shared by humans and CI
(CI calls `make site`, developers call `make serve`) - including a one-command
bootstrap that installs deps *and* hooks together.
