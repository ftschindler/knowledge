---
type: Principle
title: Batch dependency updates with a cooldown, not a firehose
description: Group automated dependency updates per ecosystem and impose a cooldown, so fresh releases
  settle before they are offered.
tags:
- principle
- software
- dependabot
- supply-chain
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Group automated dependency updates per ecosystem into a single
proposal, and impose a cooldown so freshly-released versions settle before
they're offered.

**When to apply.** Any automated dependency bot (Dependabot, Renovate, ...) on a
repo where a flood of individual PRs would be noise. Set the cooldown by how long
you want a release to settle, and leave security out of the calculation: a
cooldown applies to version updates only, so a security update is offered the day
its advisory lands however long the cooldown is. There is no tension to tune
here, and no reason to shorten a cooldown in the name of security.

**Why.** One PR per dependency per week buries you in review noise and CI runs,
so updates get rubber-stamped or ignored - defeating the point. Grouping bumps
into one reviewable PR per ecosystem, and waiting a cooldown period before
proposing a just-released version, both cuts noise and dodges the worst of
broken/yanked releases and freshly-published malicious versions.

**Snippet.**

```yaml
- package-ecosystem: uv
  schedule: {interval: weekly}
  cooldown: {default-days: 7, semver-patch-days: 7}
  groups:
    all_uv: {patterns: ["*"]}
```

**How enforced.** `groups` + `cooldown` in the bot config. Keep the cooldown in
the bot's config and out of the package manager's: a native cooldown setting
(`BUNDLE_COOLDOWN` and its equivalents) is obeyed by the resolver the bot shells
out to, and will hold back a security update the bot itself would have offered.
Grouping only covers the dependencies the bot was told to consider, which is not
all of them by default:
[Keep transitive dependencies in the regular update cycle](keep_transitive_dependencies_in_the_update_cycle.md).
Complements the supply-chain posture of
[Pin transitive runtime dependencies, not just the tool](pin_transitive_runtime_dependencies_not_just_the_tool.md).
