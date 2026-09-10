---
type: Practice
title: Layer build-knowledge as a values-to-blueprints derivation pipeline
description: Knowledge about how you build things stratifies into values, principles, wishes, decisions
  and blueprints, each derived from the ones above it.
tags:
- principle
- knowledge-management
- taxonomy
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
Knowledge about *how you build things* isn't one undifferentiated pile. It
stratifies into five layers, each answering a different question, flowing from
the general and enduring to the specific and concrete:

| Layer | Question it answers | Nature |
| --- | --- | --- |
| **Values** | Who do I want to be? What do I care about? | enduring personal stance |
| **Principles** | What is technically true or good practice? | reusable technical claim |
| **Wishes** | What do I want *this* thing to do? | project-specific requirement |
| **Decisions** | Given all the above, what did I choose, and why? | the resolving reasoning |
| **Blueprints** | What exactly do I copy to rebuild it? | the concrete artefact |

The flow is a derivation: **values + principles** (your general, reusable
beliefs) **combined with wishes** (this project's requirements) **produce a
decision** (the reasoning), which **yields a blueprint** (the buildable result).

The **decision record is the hinge**: the one place where the general meets the
specific and collapses into a concrete choice. Everything above it is reusable
across projects; the blueprint below it is the artefact that choice produces.

## Two layers that feed the hinge

Decisions are rarely made straight from values and wishes. Two further layers
sit beside the pipeline and supply the hinge with evidence:

| Layer | Question it answers | Nature |
| --- | --- | --- |
| **Research** | What is actually the case, before I commit to anything? | evidence gathered, conclusion deferred |
| **Explorations** | What did I try, what did it teach me, and why did I stop? | a commitment made and then withdrawn |

They differ by commitment, and that difference is what tells a reader how much
weight the findings carry: research is reading, an exploration is building.
Somebody who read the documentation and somebody who ran the thing for a month
know different amounts.

An exploration is emphatically **not** a decision with a `deprecated` marker on
it, and getting that wrong loses the knowledge the episode produced. The full
argument, and the page shape an exploration takes, is
[Record an abandoned exploration as an exploration, not a superseded decision](record_an_abandoned_exploration_as_an_exploration_not_a_superseded_decision.md).

## The why-test: which layer does a belief belong to?

You place a piece of knowledge by the **nature of its justification** - ask "why
do I hold this?" and see where the answer bottoms out:

- **"Because I care about X"** (autonomy, longevity, auditability, ethics) → it's
  a **value**. No technical mechanism underneath, just something you care about.
- **"Because of this mechanism and its consequence"** (e.g. mutable tags are a
  supply-chain risk) → it's a **principle**. The "why" is an engineering causal
  chain.
- **"Because I want *this* thing to behave like that"** → it's a **wish**. A
  requirement for one project, not a universal claim.
- **"Because, given those values/principles/wishes, this was the best option"** →
  it's a **decision**.
- **"Because I built it and found out"**, in the past tense, about something you
  no longer do → it's an **exploration**.

The test is generative, not just descriptive: it lets you file *future* content,
and it catches miscategorisation - e.g. "prefer FOSS" *feels* like a principle
but its why is "I care about not being locked in", so it's a value that
*motivates* principles rather than being one. Values motivate principles; they
are not derived from them.

## Decisions are friendlier ADRs

The decisions layer is [architecture decision records](https://adr.github.io/)
reframed: same virtues (explicit context, the decision, its consequences) but in
a warmer, first-person, wish-first voice - "what I wanted / what I care about /
what that led me to / what I built / what I'd reconsider" - rather than a cold
compliance artefact. Because the knowledge is *yours*, the record can be personal.

## Related

Applying this model means creating a directory per layer, which is itself an instance
of [Split orthogonal classification axes across folders and tags](split_orthogonal_classification_axes_across_folders_and_tags.md) (nature is the
folder axis). This page is the general technique; standing up the actual
`values` / `wishes` / `decisions` / `blueprints` directories, alongside `research`
and `explorations`, is its application.
