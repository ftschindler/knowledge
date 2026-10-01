---
type: Finding
title: A config symlink makes every omo migration fail on start
description: oh-my-openagent resolves ~/.omo/omo.jsonc through its symlink and then rejects the real
  path for not being named omo.jsonc, so a pending migration retries and fails on every start.
tags:
- finding
- opencode
- oh-my-openagent
- config-management
status: stable
stale_after: '2027-04-01'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-01T18:10:00+02:00'
---
Every opencode start printed the same warning, naming a file nobody had asked it to write:

```text
Migration target is not an omo config path: /home/felix/.config/opencode/omo.jsonc.PROFILES
```

The plugin accepts a migration target only when its resolved path is literally
`~/.omo/omo.json`, `~/.omo/omo.jsonc`, or the same two filenames inside a project's `.omo/`
directory. Felix's `~/.omo/omo.jsonc` is a symlink into the opencode config repository, where the
file is called `omo.jsonc.PROFILES` so that a single checkout can carry several profile sets.
The symlink is followed before the check, so the directory is wrong and the basename is wrong,
and the write is refused.

Reading the config was never affected, which is why the arrangement had worked for a month. The
rejection is in the writer alone.

## What was trying to write

A migration whose work had already been done by hand. `~/.omo/.migration-journal.json` held
`2026-09-category-deep-split` with `targetWritten: false`, left behind by
[the upgrade that split the deep category in two](20261001_a_plugin_upgrade_renamed_a_routing_category_and_breached_provider_isolation.md).
The rename had been applied to the config directly, but the `_migrations` array in that file
still listed only the two older markers, so the plugin saw an unapplied migration, tried to
apply it, and hit the symlink. Every start, identically.

The journal is worth opening rather than deleting on sight. Its stored `targetWrite` payload is
a snapshot of what the config looked like when the migration was first attempted, and in this
case several model pins had been edited since. Had the path problem been fixed and the migration
allowed to run in its `replace-target` mode, it would have written the stale snapshot back over
a fortnight of later edits. A repair that makes the write succeed is the more dangerous of the
two available repairs.

## The repair that does not touch the symlink

Both the journal-resume path and the ordinary plan path check for the migration's marker in the
target document *before* anything validates the target path. Recording the migration as applied
therefore stops the attempt early enough that the symlink is never examined:

```jsonc
"_migrations": [
  "2026-07-opencode-config-unification",
  "2026-08-reasoning-unification",
  "2026-09-category-deep-split"
]
```

Deleting `~/.omo/.migration-journal.json` removes the resume attempt as well. After both, a real
`opencode run` starts clean and the journal does not reappear.

Reversing the symlink would be the fix that addresses the cause, by putting the real file at
`~/.omo/omo.jsonc` and pointing the repository copy at it. That is not available where the
repository layout requires the differently-named file to be the real one, and the marker repair
costs one line.

## What it leaves behind

The next migration oh-my-openagent ships will attempt the same write and fail the same way, with
a different migration id in the message. The repair is the same each time: confirm the change is
already present in the config, add the marker, clear the journal.

That recurrence is the actual finding. A warning that returns on a schedule set by someone else's
release cadence reads as noise by the third occurrence, and the one time it names a migration
that has *not* been applied by hand is indistinguishable from the times it does not.
