---
type: Practice
title: Automatic session capture is not an inbox
description: A captured conversation transcript is not an atomic item you can process, so a knowledge
  base that captures sessions still needs a deliberate one-line capture path.
tags:
- gtd
- inbox
- workflow
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
---
!!! note "This is a [knowledge-management practice](index.md)"
    How knowledge gets organised, independently of any tool that stores it.

A knowledge base that captures agent conversations automatically looks like it
has solved capture. It has not, and the two are easy to conflate because both
produce a pile of unfiled material.

A transcript is not an inbox item. GTD-style capture wants a **discrete,
atomic thing you can hold one decision about**: "look into X", "this claim needs
checking", "remind me to Y". A session transcript is dozens of tangents with no
single thing to decide about, so processing it is not triage but a fresh act of
distillation. Filing the two through the same mechanism means the one-line note
you wanted to get out of your head in three seconds ends up queued behind an
hour of reading.

So a knowledge base wants both paths, and should keep them apart:

- **Distillation**, which turns captured material into concepts. Slow,
  deliberate, and the thing the knowledge base is for.
- **Capture**, which gets a thought out of your head with no decisions attached.
  Fast, and worthless if it is not.

## What the capture path has to avoid asking

An inbox exists precisely because the item's real nature is undecided. That is
not a violation of
[Categorize by what content is, not why you made it](categorize_by_what_content_is_not_why_you_made_it.md);
it is an honest admission that what the content *is* is not yet known, and the
answer arrives during review rather than at the keyboard.

The design consequence is that the capture path must ask for **nothing that a
review would answer better**: not the directory, not the tags, not the title, not
the type. Every question added to it moves work from review time to capture time,
which is the one moment the thought is most likely to be lost. A capture that
requires three decisions is a capture that does not happen.

Reviewing then does the work capture refused to do: read the item, decide what it
actually is, and move it to the directory that matches its nature. Nothing about
this needs machinery beyond moving a file, which is worth noticing before
building an inbox subsystem.

## The same argument, one level up

Automatic capture also fails as an inbox for a reason that has nothing to do with
granularity: nobody chose to write it. An inbox works because everything in it
was put there by a deliberate act, so the queue is a record of intent and reaches
zero. A queue that fills itself never reaches zero, and a queue that never
reaches zero stops being read.
