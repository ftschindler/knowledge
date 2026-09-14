---
type: Principle
title: Hand the reader one idea at a time
description: Prose that is honest and calm can still be hard work; the fix is to serialise it into one
  idea per sentence and one point per paragraph.
tags:
- principle
- documentation
- writing
- dx
- clarity
- communication
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-02T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Prose can be honest, calm and free of jargon and still be hard work,
because it delivers three ideas per sentence to a reader who can hold one. The
fix is not to cut content. It is to serialise it: one idea per sentence, one
point per paragraph, and nothing the reader must look up mid-flow.

**When to apply.** Any prose read by someone who may not be holding the context

- a tired reader, a cold session, a colleague returning after a week. Unlike the
two companion pages, this one applies to *conversational* replies as much as to
documents, because a reply is where the writer most often assumes shared state
that the reader has already lost.

**How it differs from its neighbours.** Three orthogonal axes, three pages:

| Page | Guards against | Question it asks |
| --- | --- | --- |
| [Write in a calm, quantified, settled-fact voice - not a promotional one](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md) | dishonest language | Is this overselling? |
| [Name the concrete behaviour, not its abstract label](name_the_concrete_behaviour_not_its_abstract_label.md) | jargon-dense honest language | Is this the right *word*? |
| This page | correct language delivered too fast | How much arrives *at once*? |

The middle page owns word choice, so this one does not repeat it.

**The rules.**

1. **Restate the question in one line before answering.** The reader may not have
   the thread loaded. Give them the anchor rather than assuming it.
2. **One idea per sentence. One point per paragraph.** Two or three sentences per
   paragraph. A sentence carrying three subordinate clauses is three sentences
   wearing a coat.
3. **Label options by what they mean, not by their technical name.** *"Don't have
   several styles"* beats *"converge the bundles we own on one house style"*. The
   plain label is the idea; the technical one is a translation step the reader
   performs before they can even weigh the option.
4. **Lead each option with the recommendation, then the plain reason.** *"That's
   cheaper than building anything"* beats *"the cheapest fix by a distance"*.
5. **Keep cross-references out of the body.** Every `§4` or *(see below)* mid-
   sentence is a lookup the reader must either perform or feel guilty about
   skipping. Collect them into one line at the end.
6. **Bold the claim, not the keywords.** Scattered bold makes the eye jump and
   marks nothing. One bold sentence per section tells a skimmer what the section
   says.
7. **One insight per reply, at the end.** Burying a *"here's the thing worth
   remembering"* in every paragraph means none of them lands.

**Why.** Density and pace are different things. A dense text names a concept and
expects the reader to unpack it; a readable text does the unpacking. That costs
words, not substance - the same recommendation, the same reasoning, the same
rejected alternatives, arriving one at a time instead of three at once. The
writer pays a little length; the reader stops re-reading.

**Snippet (dense → serialised).**

| Dense | Serialised |
| --- | --- |
| "Derived facts cannot drift, need no declaration, and work on an upstream that will never adopt our conventions." | "Because it reads reality, it can't go out of date. And it works on other people's bundles too." |
| "§4 is what rules it out rather than taste." | "The manifest holds two kinds of thing. House style is neither." |
| "the asymmetry that makes derived-over-declared the right default" | "the bundles most likely to surprise your agent are the ones you don't control" |

**How enforced.** Convention plus a review pass. Read a paragraph and count the
ideas; if it is more than one, split it. Grep the draft for mid-sentence section
references and move them to the end. Check that each option's label reads as a
sentence a tired person would understand without decoding. The tell that a draft
needs this pass is a reader asking for it again in simpler terms - which is late,
but it is the signal that earned this page.
