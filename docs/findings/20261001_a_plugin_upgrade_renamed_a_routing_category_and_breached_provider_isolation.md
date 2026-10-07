---
type: Finding
title: A plugin upgrade renamed a routing category and silently breached provider isolation
description: oh-my-openagent 5 split its deep category in two, which left the pin naming the old key
  inert and sent both new slots to a provider the profile exists to exclude.
tags:
- finding
- opencode
- oh-my-openagent
- config-management
status: stable
stale_after: '2027-04-01'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-01T16:35:00+02:00'
---
Upgrading oh-my-openagent from 4.19.4 to 5.1.7 moved my ovhcloud profile's deep-work slots onto
GitHub Copilot, across the provider boundary the profile exists to enforce. Nothing reported an
error, and the config file that caused it was unchanged and still looked correct.

The plugin split its `deep` category into `deep-low` and `deep-high`. My profile pinned `deep`,
so after the upgrade that key matched no slot and the two new ones had no pin at all. An
unpinned slot falls through to the plugin's built-in routing table, which encodes a global
preference order over providers rather than "use the one this profile enables" - and its
preferred entries for both named `github-copilot`:

```text
deep-low   STRAY    github-copilot/gpt-5.6-sol(medium)   (provider is in disabled_providers)
deep-high  STRAY    github-copilot/gpt-6-astra(xhigh)    (provider is in disabled_providers)
```

The pin was still in the file, still valid YAML, still naming real ovhcloud models. It had simply
stopped referring to anything.

## Why nothing caught it

Three separate guards were in place and none of them fired.

The profile's `disabled_providers` is read by the plugin, and only governs pins the plugin can
see; a slot resolved by the routing table was never a pin. opencode's own `enabled_providers` is
the stronger gate, but the plugin's provider cache does not consult it, so the routing table
considered an excluded provider reachable. And a dangling pin is not an error condition at all -
the plugin's contract is that an unmatched slot falls back, which is the correct behaviour for a
slot that was never pinned and indistinguishable from one whose key was renamed underneath it.

A renamed key therefore degrades exactly like a key that was never written, and the only
difference between the two is intent, which no file records.

## How it was found, and what prevents it

Only by replaying the new build's routing table against the live catalogue and comparing the
result to what the profile intends - the `check-resolution.sh` in my config's own update skill,
which labels each slot `PINNED`, `ok`, `down`, `NONE` or `STRAY`. Reading the config file could
not have found it, because the file was right. Reading the release notes might have, had the
rename been called out.

So the habit worth keeping is to **re-run resolution after every plugin upgrade, not only when
something looks wrong**. A routing table is a dependency whose keys are an interface, and nothing
in a config file is version-checked against it.

This is the mirror image of
[a declared-but-inert config documents intent, not enforcement](../principles/a_declared_but_inert_config_documents_intent_not_enforcement.md):
there an inert entry is legitimately kept as a statement of intent, because the input it waits for
may yet appear. Here the entry was live enforcement until an upgrade made it inert, and the
failure is that the two states are written identically. An inert entry is safe when it never fired;
it is dangerous when it used to.

The fix was to pin `deep-low` and `deep-high` explicitly, following the old `deep` chain's own
ordering. The same upgrade also retuned the chains for several slots that were resolving fine,
which is the other reason to look rather than assume.
