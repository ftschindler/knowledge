---
type: Principle
title: Subscribe to shared instruction text rather than pasting a copy
description: Text maintained in one place and needed in many should be rendered into them by a
  subscription, because a copy pasted by hand is one no later version can reach.
tags:
- principle
- agents
- documentation
- knowledge-management
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:55:00Z'
---
**Claim.** Where the same block of text has to sit in files no release touches, pasting it is
a one-way copy: the authoritative wording moves on, the copy stays as it was, and neither half
knows about the other. A subscription renders the block instead, between markers, and an
upgrade carries it.

This is the companion to
[Route a rule to the layer that reaches whoever must obey it](route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md),
which decides *which* layer a copy belongs in. This one decides how that copy stays current
once it is there.

**When to apply.** The text lives outside any repository that ships it: the instructions a
coding agent loads before every session, a shared editor configuration, a block of CI any
repository is told to copy. The tell is a document that says "paste the following into your
`X`".

**The rule.**

1. **One authoritative copy, in a repository, versioned with whatever it describes.** A skill
   and the rule that makes an agent reach for it ship under one name, so an upgrade cannot
   bring one without the other.
2. **A tool renders it into place and owns the region it wrote**, delimited by markers it
   recognises.
3. **Anything of the reader's own goes outside the markers.** A render rewrites the region
   whole, so a line left inside survives until the next upgrade and then is gone with no
   message. This is where a migration loses something: the personal line is exactly the one
   nobody else would have written.
4. **Ask before subscribing on someone's behalf.** A file loaded at the start of every
   session, for every project, is a larger step than writing a file they asked for.
5. **Delete the old pasted copy once the rendered one is in place**, and not before. Two
   sections saying the same thing leave a reader nothing to choose between.

**Why.** A stale copy fails silently and indefinitely. Nothing reads both halves, so no check
can compare them, and the behaviour it produces is plausible rather than broken. Pinning does
not help: this is not a dependency anybody resolved, it is prose somebody transcribed.

**What it costs.** A tool in the path where there was none, and a manifest of subscriptions to
keep. Where the tool is absent the hand-pasted copy still works, which is what makes this
worth offering rather than requiring.

**How enforced.** Convention, plus whatever the subscribing tool reports about where each
block landed. An upgrade removes nothing it did not write, so a file a release deleted stays
on disk as a second copy of the text just removed, and a migration guide has to name it
explicitly. Earned subscribing to the `fkb` rule through
[federated-agent-kits](../tools/federated_agent_kits_schindler.md).
