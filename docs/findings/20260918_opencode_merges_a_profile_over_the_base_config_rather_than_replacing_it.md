---
type: Finding
title: opencode merges a profile over the base config rather than replacing it
description: An OPENCODE_CONFIG_DIR profile is a layer over the base config, not a substitute for it,
  so a provider-agnostic setting is written once and inherited everywhere.
tags:
- finding
- opencode
- config-management
status: stable
stale_after: '2027-03-18'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
---
Pointing `OPENCODE_CONFIG_DIR` at a directory does not make opencode ignore
`~/.config/opencode/opencode.jsonc`. The two are **merged key by key, with the profile
winning**, so the base file is a real shared layer and not a fallback that an active profile
switches off.

The practical consequence is the whole reason to know it: a setting that does not vary by
provider belongs in the base config **once**. Writing it into every profile instead produces
copies that have to be kept in step by hand, and nothing in the tooling notices when they drift
apart.

## Evidence

Verified empirically against opencode 1.18.23, because the documentation I had, my own, stated
the layering in one sentence and then showed `plugin` repeated in every profile, which reads
like evidence of the opposite.

A marker key was added to the base config, `"username": "BASE_LAYER_MARKER"`, and the resolved
configuration read back with a profile active:

```bash
OPENCODE_CONFIG_DIR=~/.config/opencode/profiles/<id> opencode debug config
```

The marker appeared, whilst `enabled_providers` still came from the profile. Both halves
matter: the first shows the base is read, the second that the profile still overrides what it
declares. A key present in only one of the two files settles the question, where a key both
files set cannot, since the profile winning looks identical to the base being ignored.

`opencode debug config` writes enough output to be truncated by a pipe into a short-reading
consumer, which produced a JSON parse error unrelated to the question. Redirect it to a file
and read that.

## Why it matters

The repeated `plugin` entry is the thing most likely to mislead, and it is a genuine exception
rather than a counterexample: it is duplicated because opencode's config doctor looks for it in
the active profile's own file, not because it would otherwise be lost. Reading that duplication
as the general rule is how every future shared setting ends up copied into every profile.

With the layering established, the split follows without further thought. `enabled_providers`,
the default model and credentials vary by provider and belong in the profile, which is also
what keeps one provider's key out of another's session. Everything else, and `mcp` in
particular, is written once in the base config.

The generalisation is
[a config layering assumption is cheap to test and expensive to assume](../principles/test_a_config_layering_assumption_with_a_marker_key.md):
one throwaway key and one command answered in a minute what the prose could not, and the
alternative was a duplicated block in every profile that would have looked correct for as long
as nobody changed one of them.
