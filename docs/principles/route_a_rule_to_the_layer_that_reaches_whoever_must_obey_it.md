---
type: Principle
title: Route a rule to the layer that reaches whoever must obey it
description: A rule's home follows from who has to obey it, not from what it says, because each layer
  reaches a different audience at a different cost.
tags:
- principle
- agents
- documentation
- knowledge-management
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
---
**Claim.** Where a rule lives is decided by its audience, not by its subject. A
human contributor only ever meets a page or a failing commit, because nobody
loads an agent skill by hand. An agent only ever meets an instruction, because
it does not read a page it was not pointed at. So one rule legitimately exists
at several layers at once, and the question worth asking of each copy is not
whether it repeats another but whether it reaches somebody the others cannot.

**When to apply.** Any rule that binds both people and agents: a house prose
style, a naming convention, a security invariant, a review checklist. Also any
time an instruction file has grown a section that a skill or a hook would serve
better.

**The layers, and what each costs.**

| Layer | Reaches | Costs | Decides |
| --- | --- | --- | --- |
| A concept page | anyone who reads it | nothing, and nobody reads it in time | anything, including judgement |
| A commit hook | every contributor, human included | a toolchain, and it runs late | only what a regex can decide |
| A skill | agents, in any harness, on demand | nothing until loaded, then context | anything, if it is loaded |
| An always-on instruction | every reply | context on every turn, forever | anything, but must stay short |

The two middle rows are the ones usually confused. A hook is the only layer
that stops a human, and the only one that cannot exercise judgement. A skill is
the opposite on both counts.

**The rule.**

1. **Name who must obey, before deciding where it goes.** If the answer includes
   a person, a page or a hook is required, and no amount of instruction covers
   it.
2. **Put the reasoning in exactly one layer**, the one that argues. Every other
   copy carries imperatives and a link back.
3. **Give the always-on layer only what is needed without loading anything.** Its
   cost is paid on every turn, so it holds the imperatives that govern the most
   common output and nothing else.
4. **Let the most local layer win.** A repository naming its own convention
   overrides a personal default, and both the skill and the instruction say so
   explicitly rather than leaving the precedence to be guessed.

**Why.** The instinct is to fight the duplication, since
[one definitional home](give_every_cross_cutting_concept_one_definitional_home.md)
is the right default for prose. That rule is about *definitions*, and it still
holds: only one layer defines. What the layers hold is delivery, and delivery
cannot be centralised because the audiences do not overlap. Collapsing to one
copy always drops an audience, which is how a house style ends up binding
agents and not people, or the reverse.

The discipline that keeps the copies honest is the split in rule 2. Because only
one layer argues, a drift surfaces as a flat contradiction between an imperative
and its reasoning, rather than as two arguments that quietly stopped agreeing.

**Snippet (routed by subject → routed by audience).**

| Routed by subject | Routed by audience |
| --- | --- |
| The whole prose style inlined in `AGENTS.md`, because it is about writing | Imperatives in `AGENTS.md`, the full style in a skill, the reasoning on one page, the greppable half in a hook |
| "Never commit a binary" in an agent instruction file | A `.gitattributes` guard, because a human commits binaries too |
| A naming convention documented in the contributing guide alone | The guide, plus a filename hook, because the guide is read once and the hook every time |

**How enforced.** Convention, and one question per rule: who breaks this, and
what would have stopped them. A rule that only an agent can break needs no hook.
A rule a person can break needs one, or it is decoration. Earned building the
prose style this bundle runs on, where the same three principles now exist as
pages, a hook, a skill and a digest, and each copy reaches somebody the other
three miss. The episode is
[Teaching my agents to write like me](../decisions/teaching_my_agents_to_write_like_me.md).
