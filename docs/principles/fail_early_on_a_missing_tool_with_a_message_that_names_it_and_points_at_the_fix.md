---
type: Principle
title: Fail early on a missing tool with a message that names it and points at the fix
description: A task runner validates the tools a target assumes before running it, and aborts naming the
  missing tool and where to get it.
tags:
- principle
- software
- dx
- tooling
- make
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** A task runner should validate the tools a target assumes *before*
running the target, and abort with a message that names the missing tool and
says where to get it - not die halfway through a recipe with a bare
`command not found`.

**When to apply.** Any Makefile/`just`/script target that shells out to external
binaries a contributor might not have installed. Especially targets with
multiple steps or side effects, where a mid-recipe failure leaves partial state
and a cryptic error.

**Why.** A recipe that assumes `node`, `uvx`, or `git` and finds one missing
fails at the exact line that needed it - often after earlier steps already ran,
with an error naming a shell builtin rather than the thing the contributor must
install. A preflight guard turns that into a single, self-locating message at the
start: *what* is missing and *where* the fix is documented. The check is cheap
(`command -v`), runs once, and makes each target's real assumptions explicit and
reviewable rather than implicit in whichever command happens to run first.

**Snippet.**

```makefile
# A reusable guard: order-only prereq that aborts if a tool is absent.
guard-%:
 @command -v $* >/dev/null 2>&1 || { \
  printf 'error: required tool %s not found on PATH.\n' '$*' >&2; \
  printf 'See CONTRIBUTING.md > System requirements for how to install it.\n' >&2; \
  exit 1; \
 }

test_skills: | guard-node guard-npm guard-npx guard-uvx
 uvx --with pytest pytest -m skills
```

**How enforced.** Each target declares its binaries as `guard-<tool>` order-only
prerequisites (`| guard-node …`), so the assumption lives next to the recipe and
is checked before any step runs. The pattern rule carries no `##` doc comment, so
it stays out of a [self -documenting help listing](make_the_build_interface_a_self_documenting_makefile.md). The error names the tool and points at the same
[requirements](do_not_make_a_tool_a_prerequisite_for_work_it_is_not_needed_for.md)
doc that justifies why it is needed.
