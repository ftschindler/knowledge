---
type: Principle
title: Do not make a tool a prerequisite for work it is not needed for
description: Before listing a tool as required, verify it lies on a path the contributor's workflow actually
  exercises.
tags:
- principle
- software
- dx
- tooling
- dependencies
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** Before listing a tool as a requirement - in a dependency manifest, a
setup guide, or a required-install list - verify it actually lies on a path the
contributor's workflow exercises. A tool that only matters under a trigger that
never fires is documentation, not a dependency, and listing it as required is
cost without benefit.

**When to apply.** Whenever you write or prune a "system requirements" list, a
dependency group, or a `bootstrap` step. Especially when removing: a requirement
earns its place only if some real command path reaches it.

**Why.** Requirements creep is silent and one-directional - tools accumulate,
nobody removes them, and each one is friction on every fresh clone (install it,
keep it current, debug it when absent). Two common cases both dissolve on
inspection:

- **A dependency nothing resolves.** A pinned dev dependency whose only consumer
  has been rewired away is dead weight; removing it and relocking loses nothing.
  Check `grep` across the repo for who invokes it before keeping it.
- **A tool whose config is dormant.** Some declarations do nothing until a
  matching input exists - `git-lfs` filters in `.gitattributes` are inert with
  no matching files tracked, so git never invokes `git-lfs` to clone, commit, or
  test. Requiring it up front makes everyone pay for a capability only the person
  who first adds a binary will ever exercise.

The discipline is to trace the actual path from "contributor runs X" to "tool is
invoked". If no path reaches the tool, it is not a prerequisite; at most it is a
[documented intent](a_declared_but_inert_config_documents_intent_not_enforcement.md) that becomes required only at its trigger.

**Snippet.**

```console
# Who actually resolves prek? If only CI did, and CI moved to uvx, the
# dependency-group pin is dead weight — drop it and relock.
$ grep -rn 'prek' pyproject.toml uv.lock .github/ Makefile
```

**How enforced.** Review discipline: when adding a requirement, name the command
that reaches it; when auditing, drop any whose path you cannot trace. Pairs with
[Resolve a repo's own dev tools through an ephemeral runner, not a project virtualenv](resolve_a_repos_own_dev_tools_through_an_ephemeral_runner_not_a_project_virtualenv.md) - an ephemeral runner often removes the need to require the tool at
all, since it is fetched on demand rather than pre-installed.
