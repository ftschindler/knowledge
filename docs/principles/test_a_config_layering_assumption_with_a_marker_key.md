---
type: Principle
title: Test a config layering assumption with a marker key
description: Whether a layered configuration merges or replaces is settled in a minute by a throwaway
  key present in only one layer, and is otherwise assumed wrongly for as long as it goes unchecked.
tags:
- principle
- software
- config-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
---
**Claim.** Before deciding where a setting belongs in a layered configuration, establish whether
the layers **merge** or whether the inner one **replaces** the outer, by adding a throwaway key
to the outer layer and reading back what the tool resolved. Do not infer it from the
documentation, and in particular do not infer it from what the existing files happen to
duplicate.

**Why.** The two behaviours are indistinguishable from the outside, because the keys people
actually set are the ones every layer sets. If a profile declares `model` and the base declares
`model`, the profile's value wins under either rule, so the configuration in front of you is
consistent with both and reading more of it will not help. A key present in **only** the outer
layer is what separates them, and it takes one line to add.

Getting it wrong is expensive in a way that stays hidden. Assume replacement when the tool
merges, and every shared setting gets copied into every profile: correct on the day it is
written, and silently divergent from the first time somebody updates one copy. Nothing checks
it, because each file is individually valid. Assume merging when the tool replaces, and the
setting is simply absent, which at least fails where you can see it.

The strongest evidence for the wrong conclusion is usually already in the repository. A key that
*is* duplicated across layers looks like proof that duplication is necessary, when the real
reason is often narrower than the rule it suggests: something reads that one key from the inner
layer specifically. One exception, generalised, produces exactly the duplication this principle
exists to avoid.

**How enforced.** A habit rather than a hook, in three steps:

1. Add a key to the outer layer that no inner layer sets, with an unmistakable value:
   `"username": "BASE_LAYER_MARKER"`.
2. Resolve the configuration the way the tool does, with the inner layer active, and look for
   the marker. Most tools have a command that prints what they resolved, which is the thing to
   find first; anything that pipes a large document into a reader should be redirected to a file,
   since a truncated read produces a parse error that looks like a different problem entirely.
3. Check both directions in the same run. The marker surviving proves the outer layer is read;
   an inner-layer key still overriding proves the inner one still wins. One without the other
   leaves the question half answered.

Then remove the marker. It has done its work, and a key nobody can explain is its own small
liability.

The case this came from is
[opencode merges a profile over the base config rather than replacing it](../findings/20260918_opencode_merges_a_profile_over_the_base_config_rather_than_replacing_it.md),
where the duplicated key was `plugin` and the reason for it was narrow. Sibling of
[A declared but inert config documents intent, not enforcement](a_declared_but_inert_config_documents_intent_not_enforcement.md):
both are about the gap between what a configuration appears to say and what the tool reading it
does.
