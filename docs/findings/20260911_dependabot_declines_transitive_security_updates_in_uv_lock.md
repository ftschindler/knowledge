---
type: Finding
title: Dependabot declines transitive security updates in uv.lock
description: Dependabot resolves a fix for a transitive Python package and then refuses to write it,
  reporting security_update_not_possible with no conflicting dependencies.
tags:
- finding
- dependabot
- uv
- supply-chain
- ci-cd
- bug
status: stable
stale_after: '2027-03-11'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-11T00:00:00Z'
sources:
- id: dc-14073
  resource: https://github.com/dependabot/dependabot-core/issues/14073
  title: 'dependabot-core#14073: uv transitive dependencies are not updated under lockfile-only'
  last_modified: '2026-09-02'
---
**Versions**: [Dependabot](../tools/dependabot.md) as hosted in September 2026, against a
[uv](../tools/uv.md) project. The `uv` updater is young and moving; re-check before
relying on any of this.

## The symptom

Security alerts against packages in `uv.lock` stay open for months and no
security pull request is ever raised, whilst ordinary version-update pull
requests arrive and merge normally. `vulnerability-alerts` and
`automated-security-fixes` are both enabled, so the configuration looks correct.

The security-update jobs do run, and they fail:

```text
| security_update_not_possible | {                                            |
|                              |   "dependency-name": "cryptography",         |
|                              |   "latest-resolvable-version": "50.0.0",     |
|                              |   "lowest-non-vulnerable-version": "50.0.0", |
|                              |   "conflicting-dependencies": []             |
```

That error reads as an unsatisfiable version constraint, and it is not one. The
two versions agree: Dependabot found a resolvable, non-vulnerable version and
then declined to write it. `conflicting-dependencies` is empty because nothing
conflicts.

## What it turned out to be

The affected packages were transitive: present in `uv.lock`, absent from
`pyproject.toml`. Two settings, each reasonable-looking, kept them out of reach.

**`allow` defaults to direct dependencies.** With no `allow` block, the job
definition in the run log reads
`"allowed-updates":[{"dependency-type":"direct","update-type":"all"}]` and
`"update-subdependencies":false`. The run then logged exactly ten
`Checking if ... needs updating` lines against a fifty-package
`Dependency Snapshot:` in the same log. The bot had never looked at the
vulnerable packages at all.

**`versioning-strategy: lockfile-only` makes it worse, not better.** It reads as
"only write the lockfile", which is precisely the intent for a uv project. For
the `uv` updater it also stops transitive dependencies being resolved
(dependabot-core#14073[^dc-14073]),
so it forbids the only edit that could have fixed them.

Two things it was *not*, both of which cost time as hypotheses. `cooldown` does
not apply to security updates, so it cannot be the cause; a cooldown configured
in the *package manager* rather than the bot is a different matter and does block
them. And the "Check for updates" button in the dependency graph re-runs
**version** updates only, so a null result from it says nothing about the
security-update path.

## How to get past it

Ask for the whole lockfile, and delete the strategy:

```yaml
- package-ecosystem: uv
  directories: ["/"]
  allow:
  - dependency-type: all     # without this, direct dependencies only
  schedule: {interval: weekly}
```

Where the manifest's own requirements are unpinned or range-pinned, dropping
`versioning-strategy` does not invite Dependabot to rewrite `pyproject.toml`:
there is nothing to widen, and it writes `uv.lock` alone as before.

This also routes around the security-update path rather than waiting for it. The
weekly **version** update now proposes the transitive bumps, which clears the
alerts whether or not the security job ever works.

To unblock an alert immediately, without the bot:

```bash
uv lock --upgrade-package cryptography
```

## Takeaway

Read the job definition at the top of the run log, not the error at the bottom.
The error described a version conflict that did not exist; the job definition
stated the actual cause in two fields. The general form is
[Keep transitive dependencies in the regular update cycle](../principles/keep_transitive_dependencies_in_the_update_cycle.md).
