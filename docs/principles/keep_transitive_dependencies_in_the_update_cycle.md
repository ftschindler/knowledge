---
type: Principle
title: Keep transitive dependencies in the regular update cycle
description: An update process that only considers the dependencies a manifest names has never examined
  most of what the project actually runs.
tags:
- principle
- software
- supply-chain
- ci-cd
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-11T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-11T12:19:50Z'
---
**Claim.** Whatever keeps your dependencies current must consider every package
in the lockfile, not just the ones the manifest names. A process scoped to
direct dependencies has never examined most of what you ship.

**When to apply.** Any project with a lockfile, which is to say any project whose
manifest declares less than it installs. The stakes scale with how much of the
updating is automated: a bot restricted to direct dependencies is not a partial
process, it is a process with a blind spot that nobody is watching, because the
bot reports success from inside it.

**Why.** A manifest of ten packages routinely locks fifty. The forty you did not
name are not a lesser class of dependency - they execute in the same process with
the same privileges, and an advisory lands on them at the same rate. They are
simply the ones no human chose, which makes them the ones no human is watching.

The failure mode is not a red build, it is a green one. An update run that was
never allowed to look at a package reports nothing to do about it, truthfully,
and keeps doing so every week whilst the advisory count climbs somewhere you are
not looking. Nothing in that output names the package that was out of scope,
because from the run's point of view it does not exist. This is
[Verify a pre-commit hook's file-type filter actually matches your file](verify_a_pre_commit_hooks_file_type_filter_actually_matches_your_file.md)
at the scale of a supply chain: a check that passed without having looked.

Two habits follow. **Scope the process to the lockfile**, explicitly, rather than
accepting a default - most update tooling defaults to direct dependencies,
because that is the smaller and less alarming set. And **keep a route that does
not depend on the bot**: the package manager's own "re-resolve everything"
command will relock a transitive package in one step, which is worth knowing
before the day an advisory is open and the automation is declining to act on it.

**How enforced.** Count, once. Take the number of packages the last update run
*examined* and compare it to the number the lockfile *pins*. Ten against fifty is
not a quiet week, it is a scope problem, and it is visible in any run log that
names what it checked. Repeat after changing the update configuration, because
this is exactly the setting that silently reverts to its default when an option
is renamed or an ecosystem is added.

For the configuration that achieves this with a specific bot, and the misleading
error you get when it does not, see
[Dependabot declines transitive security updates in uv.lock](../findings/20260911_dependabot_declines_transitive_security_updates_in_uv_lock.md).
Complements [Batch dependency updates with a cooldown, not a firehose](batch_dependency_updates_with_a_cooldown_not_a_firehose.md),
which shapes how the updates arrive once the right set is in scope, and
[Install from a frozen lockfile in CI](install_from_a_frozen_lockfile_in_ci.md),
which is the same file taken seriously at the other end of the pipeline.
