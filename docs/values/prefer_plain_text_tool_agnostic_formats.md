---
type: Value
title: Prefer plain-text, tool-agnostic formats
description: Wherever content can be stored in an open format (or simply plain text), prefer that over a proprietary
  or binary format tied to one application.
tags:
- value
- software
- plain-text
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-10T07:25:00Z'
---
!!! note "This is a [value](index.md)"
    What I care about, ahead of any particular project. These sit under
    everything else in the bundle.

**Value.** Wherever content can be stored as plain text or in an open,
widely-supported format (Markdown, plain files, open JSON),
prefer that over a proprietary or binary format tied to one application.

**Why it matters to me.** Plain text is both human- and machine-readable, diffs
cleanly in git, and outlives any single tool - I can read it in `cat`, edit it in
`nvim`, grep it, script over it, and still open it in twenty years when today's
app is gone. It keeps my data *mine*, not hostage to a vendor's file format
or a running service.

**What it implies.** This value generates concrete choices and principles:
Markdown for prose over a WYSIWYG database; portable `.excalidraw` JSON over an
app-locked drawing format; config as readable files over opaque state.

**Tensions.** Plain text sometimes costs convenience - a rich app UI, live
rendering, structured queries. The resolution is usually a *convenience layer over
plain files* (an editor or generator that reads the plain source) rather than
moving the source of truth into the tool. When richness genuinely can't be plain
(images, diagrams), keep the *canonical* form as open as possible and render from
it.
