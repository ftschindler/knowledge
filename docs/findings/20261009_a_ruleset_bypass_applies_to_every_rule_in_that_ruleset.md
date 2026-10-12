---
type: Finding
title: A ruleset bypass applies to every rule in that ruleset
description: Bypass is granted per ruleset rather than per rule, so overriding a red status check
  also hands over whatever else that ruleset enforces unless the rules are split across rulesets.
tags:
- finding
- github
- repo-hygiene
- permissions
- security
status: stable
stale_after: '2027-04-09'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T18:30:00+02:00'
---
A repository ruleset carries a list of rules and a list of `bypass_actors`. The two are not
paired: **an actor on the bypass list is exempt from everything in that ruleset**, not from one
rule in it.

The practical shape of the problem is a reasonable request that cannot be expressed. "Let me
merge when a required check is stuck, but still make me open a pull request" is two different
answers to two rules that had been written into one ruleset:

```text
main-requires-checks-and-prs
  required_status_checks   build, governance
  pull_request             1 approval, thread resolution
```

Adding a repository-admin bypass there grants the override on the check *and* the right to push
straight to `main`. There is no field that narrows it, because the rule entries have no bypass of
their own.

## The repair is layout, not configuration

Split by what you might one day want to override, one rule family per ruleset:

```text
main-cant-be-overwritten   deletion, non_fast_forward   bypass: none
main-requires-prs          pull_request                 bypass: none
main-requires-checks       required_status_checks       bypass: repository admin
```

The effective rules on the branch are identical, since GitHub unions every ruleset that matches
a ref. What changes is that the bypass now has somewhere to attach that does not drag the rest
with it.

**This is worth deciding before the rulesets are written rather than after.** Splitting later
means deleting a ruleset and recreating two, and for the window between those two acts the
branch is enforcing less than it should.

## Migrating from classic branch protection is not a translation

Classic protection is one object per branch with `enforce_admins` as a single boolean over the
whole of it. Copying that arrangement into one ruleset reproduces the limitation that made it
blunt. The migration is the moment the granularity becomes available, and taking it literally is
how a repository ends up with either an admin who can delete `main` or a maintainer who cannot
merge past a runner outage.

Two things to check rather than assume whilst doing it. `enforce_admins: false` was permission to
bypass *everything*, so a faithful-looking translation almost certainly over-grants. And
`RepositoryRole 5` is every repository admin, which on a personal repository is one person and on
a team repository is not.

Confirm the result by reading the effective rules back, which is the only view that accounts for
several rulesets and classic protection applying at once:

```bash
gh api repos/<owner>/<repo>/rules/branches/main --jq '[.[].type] | unique'
```

Create the rulesets before deleting the classic protection, and check that command in between.
The two coexist, so there is no moment where the branch is unguarded.
