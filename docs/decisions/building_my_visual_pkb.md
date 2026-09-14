---
type: Decision
title: Building my visual PKB
description: The decision that resolved my wishes, values and principles for a personal knowledge base
  into a concrete publishing stack.
tags:
- decision
- software
- pkb
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [decision](index.md)"
    What I chose, given my values, wishes and principles, and the reasoning
    that got me there. A decision here is one I still stand behind.

A decision record for how I built my personal knowledge base.
It resolves my wishes, values and principles into a concrete
[MkDocs Material PKB publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md).

## What I wanted

The [Wishes for a personal knowledge base](../wishes/wishes_for_a_personal_knowledge_base.md), in short: a real wiki/KB; content
that stays human- and machine-readable; first-class visual knowledge management;
local-first but not local-required; an optional convenience layer.

## What I care about

- [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md) - my knowledge should outlive any
  one tool.
- [Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md) - auditable, no lock-in, long-lived.

## What that led me to

Working wish by wish, each choice resting on the value or principle above it:

- **Human + machine readable → plain Markdown files** as the source of truth. Not a
  database, not a proprietary note format.
- **Visual KM → Excalidraw**, with drawings stored as portable `.excalidraw` JSON
  (not the app-locked `.excalidraw.md` wrapper), rendered client-side so the
  canonical form stays open.
- **Convenience without lock-in → Obsidian as an *optional* layer** over the plain
  files: it's FOSS-friendly, reads the folder as-is, and never becomes the source
  of truth. `nvim` on the same folder is always an equal path.
- **Local-first → a git-backed folder** I can clone and edit offline with any
  editor.
- **...not local-required → host it with web editing** (GitHub), so edits from the
  browser become ordinary commits. (See [Local-first, but not local-required](../wishes/local_first_but_not_local_required.md).)
- **A browsable, published site → MkDocs + Material**, building the Markdown into a
  searchable static site.

Quality and reproducibility then pull in the principle layer: the build pins its
toolchain, guards invariants at commit-time and mirrors them in CI - see the
blueprint for the full list of principles it instantiates.

## What I built

→ [MkDocs Material PKB publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md)

## What I gave up / would reconsider

- **MkDocs 2.0 incompatibility** - Material for MkDocs needs MkDocs `<2` for now,
  so the stack is pinned below 2 until a drop-in replacement is ready.
