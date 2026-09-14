---
type: Practice
title: Keep the GTD inbox inside the private bundle, not beside it
description: A capture queue belongs in the knowledge base it feeds, provided nothing is allowed to
  link to a page whose purpose is to be deleted.
tags:
- gtd
- inbox
- workflow
- knowledge-management
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-11T00:00:00Z'
---
!!! note "This is a [knowledge-management practice](index.md)"
    How knowledge gets organised, independently of any tool that stores it.

A GTD inbox holds items that are meant to stop existing. A knowledge base holds
pages that are meant to persist and be linked. Putting the first inside the
second looks like a category error, and the usual reflex is to keep captures in
a folder of loose notes beside the bundle, or in a different application
entirely.

That reflex costs more than it saves. Two places to look, two sets of
conventions, and two toolchains, for material that is on its way into the
bundle anyway. A capture point wants to be wherever you already are.

So put it in the bundle, in a top-level `inbox/`, and pay for it with three
rules.

## Nothing outside the inbox may link into it

This is the rule that makes the rest safe, and it is the one that is tempting to
break, because linking a capture to the concept it relates to feels like exactly
what a knowledge base is for.

It is backwards. A capture exists to be processed and deleted, so an inbound
link is a broken link with a delay on it, and the link checker will report it
from a page nobody was editing. Captures may link outwards as richly as they
like, and to each other; the graph edge you actually want ends up in the concept
the capture becomes, not in the capture.

The value of keeping the inbox in the bundle is one repository and one set of
hooks, not participation in the link graph. Worth being clear about, because it
means there is no reason to invest in linking captures at all.

## The type carries "unprocessed", not the status

In the [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
every markdown file under the bundle root is a concept and carries frontmatter,
so a capture needs a type and a status like anything else. `status` will not
express what is wanted: `draft` means a stub waiting to be filled in, which is a
statement about a page, whilst a capture is a statement about the world, waiting
for a decision.

Put it in `type:`, which the format leaves as free text. `type: Inbox` with
`status: draft` reads correctly in both fields, and `rg 'type: Inbox'` is then
the review queue, with no separate list to keep in step. Processing an item
means rewriting it as a concept with a real type, or deleting it.

The frontmatter is a real cost for a human typing at speed, and no cost at all
when an agent files the capture, which is the arrangement this assumes.

## The inbox keeps its own log

A bundle log that gained a line per capture would document, in permanent form, things that
ceased to exist the same afternoon, and it would bury the record of what the bundle
actually gained.

Split it instead, which the format allows for free: `index.md` and `log.md` are reserved at
every level of the tree, not only at the bundle root, so a section may carry its own. The
inbox log records what happened to captures, what arrived, what was dropped and why, what
was promoted and into what; the root log goes on recording changes to concepts. An item
that is processed produces a line in each, about different things: that a capture left the
queue, and that a concept came into being. An item that is dropped appears only in the
inbox log, which is then the sole evidence it was ever thought.

The append-only habit matters more here than anywhere. Most of what the inbox log names has
been deleted by the time anyone reads it, so entries name captures in plain text and never
link to them.

## What makes it safe, and what it does not fix

The inbox goes in the **private** bundle, which is sealed: no other bundle may
cite it, so a half-formed thought cannot surface through a link from anywhere
that publishes. The same arrangement in a published bundle would need a
different argument.

Index churn is the residual cost, since every capture and every processed item
edits an index. Give `inbox/` its own `index.md` and the churn is confined to
one file that nobody reads for meaning.

This is a capture path, not an import path. Migrating an existing pile, a Logseq
graph or an Obsidian vault, through a queue that is reviewed daily would swamp
the review and destroy the habit inside a week. Bulk migration wants its own
batched flow even though it shares a destination, and the queue must stay a
queue. That is the same distinction as
[Automatic session capture is not an inbox](automatic_session_capture_is_not_an_inbox.md),
seen from the other side: there, a firehose was mistaken for an inbox; here, an
inbox must refuse to become one.
