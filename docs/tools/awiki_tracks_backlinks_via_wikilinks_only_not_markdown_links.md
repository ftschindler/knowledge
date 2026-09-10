---
type: Finding
title: awiki tracks backlinks via wikilinks only, not Markdown links
description: awiki builds its link graph exclusively from wikilink syntax, so ordinary Markdown links
  to internal pages never count as backlinks.
tags:
- tools
- awiki
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
awiki's link graph - the backlink section, the `[ORPHAN]` and `[LINK]` findings
in `awiki lint` - is built **exclusively from Obsidian-style wikilink syntax**
(double square brackets around a page title). Standard
Markdown links to internal pages (`[text](page.md)`) are **not** counted as
backlinks and do not clear a target's orphan status.

## Evidence

Verified empirically (2026-08-27): two throwaway pages were ingested where the
source linked the target via a standard Markdown link
(`[the target](markdown-link-test-target.md)`). After `awiki index`, `awiki lint`
still reported the target as `[ORPHAN] ... has no incoming wikilinks` - note the
literal wording keys on *wikilinks*. The Markdown link produced neither a
tracked backlink nor a broken-`[LINK]` warning; it was simply ignored by the
graph.

Separately confirmed: awiki does **not** rewrite links at render time. Whatever
link syntax is authored in `raw/` passes through verbatim to the rendered page -
so wikilinks are an authoring convention (from the `awiki-save` skill and awiki's
Logseq-compatibility claim), not something the renderer imposes.

## Why it matters

This is the concrete tradeoff when choosing a link convention in an awiki vault:

- wikilinks (double square brackets around a page title) - tracked by awiki's
  graph and orphan-lint; portable only across wikilink-aware tools (Obsidian,
  Logseq, awiki).
- `[md](path.md)` - portable across every Markdown renderer (GitHub, nvim, any
  previewer); invisible to awiki's backlink/orphan tracking.

So a preference for tool-agnostic Markdown links collides with a real awiki
feature. Resolving that collision (e.g. by forking/upstreaming awiki to
understand Markdown links too) is tracked separately in the inbox.
