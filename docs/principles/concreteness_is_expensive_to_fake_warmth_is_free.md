---
type: Principle
title: Concreteness is expensive to fake, warmth is free
description: Asking prose to be warm produces the enthusiasm and chumminess it was meant to avoid; specificity
  and restraint are what read as human.
tags:
- principle
- documentation
- writing
- dx
- clarity
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
---
**Claim.** Prose that reads as written by a person is not warm prose. It is
specific prose. Warmth is the cheapest register to imitate, so anything asked
to be warm reaches for enthusiasm, second-person chumminess and exclamation,
which is the register the request was meant to escape. Specificity cannot be
faked the same way, because it requires knowing something.

**When to apply.** Any brief given to a writer or an agent that reaches for a
tone word. It is the trap behind instructions like "make it friendlier", "warm
it up", "less robotic" and "write like a human".

**The failure it prevents.** An agent told to be warm has one lever, and it is
adjectives. Back comes *"Great question! This is a really elegant approach, and
you're going to love how smoothly it works."* Every clause is warm and none of
it is about the subject. The same agent told to name what the thing gave up
produces *"This costs an extra 40ms per request, and drops the cache entirely
on a schema change"*, which reads as a person because only a person who looked
could have written it.

**The rule.**

1. **Ask for specificity, never for tone.** Name what the reader should be able
   to learn from the paragraph rather than how it should feel.
2. **Say what was given up.** A page that names its own cost has done something
   no generic register can imitate.
3. **Quantify where a number exists**, and admit the variance where one does
   not.
4. **Decline to hedge.** Warmth and hedging arrive together, because both are
   ways of avoiding a claim.

**Why.** Tone words are cheap to satisfy and impossible to verify, so they
select for the most generic prose available. A demand for a concrete fact is
expensive to satisfy and trivial to verify, so it selects for prose that had to
be earned. This is the mechanism behind the register described in
[Write in a calm, quantified, settled-fact voice - not a promotional one](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md):
that page says what the voice is, and this one says why asking for it directly
by name fails.

**Snippet (asked for warmth → asked for specificity).**

| Brief | What comes back |
| --- | --- |
| "Make the README friendlier" | *"Welcome! We're so glad you're here. Getting started is a breeze."* |
| "Say what the setup costs the reader" | *"The first run downloads 1.2GB and takes about four minutes."* |
| "Write it in a warmer voice" | *"This elegant little tool handles everything for you."* |
| "Say which cases it does not handle" | *"It does not follow symlinks, and it stops at the first parse error."* |

**How enforced.** Convention, and a check on the brief rather than on the draft:
if an instruction names a feeling, replace it with the fact you actually want
present. In this bundle the register itself is guarded by the `prose-tells`
hook, which fires on the adjectives warmth reaches for.
