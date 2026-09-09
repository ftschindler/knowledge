---
type: Principle
title: Structure docs as the reader's task path - lead with action, defer rationale
description: 'Organise a task-oriented document by the reader''s path through the task: lead with the
  runnable command, defer the rationale.'
tags:
- principle
- documentation
- writing
- dx
- structure
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** A task-oriented document (setup guide, README, runbook) is organised
by the reader's *actual path through the task*, not by the author's mental model
of the system. At each step, lead with what the reader must **do** - the runnable
command - and defer the *why* to a following aside or a nested section they can
descend into only if they care. This is orthogonal to sentence-level register
(see [Write in a calm, quantified, settled-fact voice - not a promotional one](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md)):
that page governs *how each sentence reads*; this one governs *what appears
where, and in what order*.

**When to apply.** Any prose whose reader arrives to *accomplish* something -
contributing guides, install instructions, "getting started". Not reference docs,
whose reader arrives to *look something up* and is better served by dense tables.

**The rules.**

1. **Lead with the action, defer the rationale.** At a section's entry, the first
   thing is what to do - the command, the requirement - not the causal theory
   behind it. A requirements table whose "why we chose Node" reasoning greets a
   first-time contributor delivers rationale before it is wanted. State
   *"we require uv and Node"*; move *why uv cannot provide Node* to a later line
   or a `>` aside. This extends [the aside rule](write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md) from the sentence to the section:
   asides live not just in parentheticals but in demoted paragraphs and nested
   headings.

2. **Follow the task's real order.** The document's spine is the contributor's
   actual sequence - clone, bootstrap, run, inspect - each step as
   copy-pasteable commands, not prose *describing* commands. Do not start at
   step two (the classic omission: jumping to "install the hooks" without the
   `git clone` that precedes it). Do not make the reader reconstruct the order
   from scattered mentions.

3. **Explode caveats into navigable structure, not dense paragraphs.** When one
   path carries a mechanism worth explaining, give it its own heading and reach
   it by a link from the happy path; sequence multi-step behaviour as a bulleted
   list, not a comma-spliced sentence. The happy path stays a clean spine; depth
   lives one click down. A wall of caveats in a single paragraph forces every
   reader through detail most of them do not need yet.

**Why.** Density and walkability trade off. A packed table with a "Used for /
Notes" column puts everything on one screen - optimal for someone re-checking a
fact, hostile to someone doing the task for the first time, who must now read
rationale to reach the one command they need. Task docs are read *while acting*:
the reader wants the next command, then the option to go deeper. Ordering by the
task path, and demoting the why, means the fast reader is never blocked and the
curious reader is never denied - the same courtesy the voice page pays at the
sentence level, applied to the page's shape.

**Snippet (dense-reference shape → task-path shape).**

| Reference shape (author's model) | Task-path shape (reader's path) |
| --- | --- |
| A requirements table leading with per-tool rationale | *"We require uv and Node"* first; why-this-tool demoted to a `>` aside |
| "Install the git hooks:" as the opening step | `git clone … && cd … && make bootstrap` - the real first step, runnable |
| One paragraph + two blockquotes covering the whole e2e harness | `make test_skills` first; the harness mechanism factored into a linked `####` section, its steps a bulleted list |

**How enforced.** Review the document by walking it as the reader: can a
first-timer reach the first command without reading rationale? Does the heading
order match the doing order? Is any paragraph a wall of caveats that should be a
sub-section plus a link? Pairs with [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md)

- navigable structure (headings, anchors, lists) is exactly what plain-text
formats render walkable.
