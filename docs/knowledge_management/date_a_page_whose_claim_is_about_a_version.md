---
type: Practice
title: Date a page whose claim is about a version
description: A claim about a tool is a claim about one version of it, so the page carries when it was
  written and when to doubt it, where a claim about an idea does not.
tags:
- knowledge-management
- taxonomy
- documentation
- provenance
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-09-13T00:00:00Z'
---
"Treat warnings as errors" was true in 2019 and will be true in 2035. "The
resolver refuses this upgrade unless both settings are present" was true of one
version of one tool, and something changed it three releases later. Both are
worth writing down. Only the second has an expiry date, and a knowledge base
that stores them identically is lying about one of them.

The rule: **when a page's claim is bound to a version, make the binding visible**
on the page, in its name, and in the order it is listed.

## Three places it shows

- **A date in the filename.** `20260911_dependabot_declines_transitive_security_updates.md`
  says when the claim was made before anything is opened. A page arrived at from
  search is read out of context, and the date is the context that matters most.
- **An explicit expiry**, such as OKF's `stale_after`. This is the part that turns
  a human worry into a mechanical question: without it, "is this still true?" is
  asked by whoever happens to wonder, which is nobody. With it, a linter asks.
- **Newest first.** Version-bound pages are listed with the recent ones at the
  top, because recency is a proxy for still being true. Idea-bound pages are
  ordered by how the argument builds, because their age is beside the point.

## Why not date everything

Uniformity is tempting and wrong here. A date on a principle invites a reader to
discount it for being old, which is precisely the wrong inference: an idea that
has survived six years is better evidence than one written last week. Dating it
imports a signal that does not apply and reverses its meaning.

So the date is not metadata about the page. It is **part of the claim**, and it
belongs only on pages whose claim includes it.

## What this is not

It is not `updated:`. A last-touched timestamp records activity on the file and
says nothing about whether the world still matches it; a page can be edited for
typography and remain wrong. The date here records **when the claim was
observed to hold**, which is a statement about the subject rather than the
document.

Nor is it a substitute for checking. An expiry date does not make a page correct
until it passes, and it does not make it wrong afterwards. It marks the moment
the claim stops being load-bearing without evidence, which is all a date can
honestly do.
