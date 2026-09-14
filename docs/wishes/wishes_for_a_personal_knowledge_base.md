---
type: Wish
title: Wishes for a personal knowledge base
description: The requirements I wanted a personal knowledge base to satisfy, as the wish layer that drives
  the decision below it.
tags:
- wish
- software
- pkb
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-10T07:34:55Z'
---
!!! note "This is a [wish](index.md)"
    What I wanted from a specific thing, where a value is what I want
    generally.

The requirements I wanted a personal knowledge base (PKB) to satisfy, which
together with my values and principles drive the
[Building my visual PKB](../decisions/building_my_visual_pkb.md) decision. Another
project would have different ones; see
[Layer build-knowledge as a values-to-blueprints derivation pipeline](../knowledge_management/layer_build_knowledge_as_a_values_to_blueprints_derivation_pipeline.md)
for why that makes them their own layer.

## The wishes

- **A wiki / knowledge base**, not just a pile of files - cross-linked, browsable,
  searchable.
- **Maximally human- and machine-readable** - as much content as possible in plain
  text I can read, grep, script over, and still open years from now.
- **Visual knowledge management** - first-class diagrams that interact nicely with
  the notes, not bolted on as opaque images.
- **Local-first** - I can just point `nvim` at a folder and work, fully offline,
  with no service required.
- **...but not local-required** - I can also edit from anywhere through a hosted path
  (the web) with zero local setup, so contribution never *demands* a local
  environment. (See [Local-first, but not local-required](local_first_but_not_local_required.md).)
- **A convenience layer, optionally** - a richer editing UX available on top of the
  plain files for when I want it, without becoming the source of truth or a hard
  dependency.

## What these rest on

The wishes lean on values - [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md) and
[Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md) - and are resolved into concrete tool
choices in the [Building my visual PKB](../decisions/building_my_visual_pkb.md)
decision record.
