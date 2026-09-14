---
type: Principle
title: Name the concrete behaviour, not its abstract label
description: A sentence can pass every honesty check and still force a re-read, because it names an abstract
  category instead of the observable behaviour.
tags:
- principle
- documentation
- writing
- dx
- clarity
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** A sentence can pass every honesty and voice check - settled-fact
tense, no hype, no throat-clearing - and still force the reader to re-read it,
because it names an abstract *category* instead of the concrete *behaviour* the
reader can observe. Clarity is a separate axis from honesty: the voice rules in
[Write in a calm, quantified, settled-fact voice - not a promotional one](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md)
guard against *dishonest* language; this rule guards against *jargon-dense
honest* language. Prefer the observable mechanism over its label - doubly so when
the concrete form is already visible nearby.

**When to apply.** Any explanatory prose, especially where a design has coined
abstractions ("fail-closed", "sealed", "idempotent", "eventually consistent").
These labels are precise among people who already hold the concept and opaque to
a first-time reader who must decode each one back into what actually happens.

**The failure it prevents.** *"Both security-relevant defaults fail closed: an
unconfigured bundle is sealed and read-only until you open each axis
deliberately."* Every word is honest and calm. It still needs three reads,
because it stacks four abstractions - *fail closed*, *sealed*, *read-only*, *open
each axis* - over exactly two concrete facts: nobody may reference it, nobody may
write to it. The reader must unpack each metaphor to the same two behaviours the
prose could have stated directly. Abstraction-on-abstraction is clean and
unreadable at once.

**The rule.**

1. **State the observable behaviour first.** "A new bundle can't be referenced
   and can't be written to" beats "an unconfigured bundle is sealed and
   read-only." The reader sees the *effect*, not a category name for it.
2. **Introduce the label only after the behaviour, if at all.** If the
   abstraction ("we call this fail-closed") earns its keep as shorthand for later
   reuse, name it *after* the concrete form has landed - never as the first
   encounter.
3. **Don't re-encode what's already on screen.** The strongest tell: the concrete
   facts sit in a table or code block right next to the prose, and the sentence
   restates them as abstractions. If `referenceable_by: []` and `writable: false`
   are in the table above, the prose should say "can't be referenced, can't be
   written to" - not translate them back up into "sealed and read-only."
4. **One abstraction per sentence, at most.** Stacking two or more categories in
   one clause is the re-read trigger; split, or drop to the concrete.

**Why.** A label is a compression of a behaviour, and compression only helps a
reader who already has the codebook. First-time readers don't; they decompress
every term, and stacked terms multiply the cost. Naming the behaviour skips the
decode step entirely - and when the concrete form is already adjacent, the
abstraction adds nothing but a second thing to reconcile. This is the clarity
companion to the voice page's honesty: that page says *don't oversell*; this one
says *don't over-abstract*.

**Snippet (abstract label → concrete behaviour).**

| Abstraction-stacked (honest but opaque) | Concrete behaviour (honest and clear) |
| --- | --- |
| "Both defaults fail closed: an unconfigured bundle is sealed and read-only." | "A new bundle can't be referenced and can't be written to until you say so." |
| "The gate is idempotent across re-invocation." | "Running it twice changes nothing the second time." |
| "Reads are unrestricted; the boundary is the write path." | "Any bundle can be read; only writing is checked." |

**How enforced.** Review pass: for each explanatory sentence, ask "what does the
reader actually *see happen*?" and whether the sentence says that or a category
name for it. Grep your own coined abstractions (`sealed`, `fail-closed`,
`gated`, `idempotent`) and confirm each is either preceded by its concrete form
or genuinely earning reuse. Flag any sentence stacking two+ labels. Pairs with
[Write in a calm, quantified, settled-fact voice - not a promotional one](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md) as
its orthogonal clarity axis. Earned rewriting a defaults sentence a reader had to
read three times: the fix was to name the two behaviours already sitting in the
field table above it.
