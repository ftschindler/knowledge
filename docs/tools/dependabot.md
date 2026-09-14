---
type: Tool
title: Dependabot
description: GitHub's built-in dependency update bot, which opens pull requests for new versions and
  for packages named in a security advisory.
tags:
- tools
- dependabot
- supply-chain
- ci-cd
- github
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-11T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-11T12:14:00Z'
sources:
- id: dependabot-docs
  resource: https://docs.github.com/en/code-security/dependabot
  title: 'GitHub: Dependabot documentation'
  last_modified: '2026-09-11'
---
Dependabot[^dependabot-docs] is GitHub's dependency
update bot: it reads a repository's manifests and lockfiles, and opens pull requests when a
dependency has moved. It is built into GitHub rather than installed, and it is the update
mechanism behind [Batch dependency updates with a cooldown, not a firehose](../principles/batch_dependency_updates_with_a_cooldown_not_a_firehose.md).

| | |
| --- | --- |
| Author | GitHub |
| Licence | MIT, for the `dependabot-core` engine |
| Language | Ruby, with a per-ecosystem updater for each package manager |
| Distribution | Hosted by GitHub; enabled per repository, configured by `.github/dependabot.yml` |
| Source | [github.com/dependabot/dependabot-core](https://github.com/dependabot/dependabot-core) |

## What it is

Three separate things share the name, and conflating them is the usual source of confusion.

**Alerts** come from the dependency graph meeting the advisory database. They need no
configuration and appear whether or not `.github/dependabot.yml` exists.

**Version updates** are the scheduled job: on your `schedule`, for each
`package-ecosystem`, propose whatever has moved. This is what `groups`, `cooldown` and
`allow` shape, and what the "Check for updates" button in the dependency graph re-runs.

**Security updates** are a separate job class, triggered by an alert rather than by the
schedule, and scoped to the one package the advisory names. They ignore `cooldown` entirely.
A version update and a security update can therefore behave differently on the same
repository and the same configuration, and re-running one tells you nothing about the other.

Support is per-ecosystem and uneven. Each package manager has its own updater in
`dependabot-core`, so a behaviour verified for one ecosystem should not be assumed for
another; `uv` support is comparatively recent, and
[declines transitive security updates it has already resolved](../findings/20260911_dependabot_declines_transitive_security_updates_in_uv_lock.md).

## Reading what it actually did

Every run is a GitHub Actions job whose log opens with the **job definition**, the JSON
GitHub handed the updater. It is the only honest statement of what the run was permitted to
consider, and it is worth more than the summary at the end:

```json
"command":"version", "security-updates-only":false,
"allowed-updates":[{"dependency-type":"direct","update-type":"all"}],
"update-subdependencies":false
```

After it, one `Checking if <package> needs updating` line per package examined, and a
`Dependency Snapshot:` line listing everything found. Comparing those two is how you tell a
bot that found nothing from a bot that looked at almost nothing.
