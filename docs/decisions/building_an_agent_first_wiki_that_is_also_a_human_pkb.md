---
type: Decision
title: Building an agent-first wiki that is also a human PKB
description: Why and how to build a knowledge base an agent writes into first, without making it unusable
  as a human personal knowledge base.
tags:
- decision
- software
- awiki
- pkb
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
A decision record - friendly, first-person, wish-first (see
[Layer build-knowledge as a values-to-blueprints derivation pipeline](../knowledge_management/layer_build_knowledge_as_a_values_to_blueprints_derivation_pipeline.md) for the
model). This is a *general* pattern for building an agent-first knowledge base
that stays usable as a human personal knowledge base (PKB), of which this vault is
the first instance. It is a sibling to, and consciously mirrors,
[Building a PKB that is mine, forever-readable, and visual](building_a_pkb_that_is_mine_forever_readable_and_visual.md).

## Lineage

This is not an invention from scratch - it stands on an existing pattern and an
existing tool:

- **The pattern** comes from [Karpathy's LLM-wiki concept](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
  an LLM incrementally builds and maintains a persistent, interlinked Markdown
  wiki as a *compounding artifact* - knowledge compiled once and kept current,
  rather than re-derived from raw sources on every query (the RAG model). Its three
  layers (immutable raw sources → LLM-owned wiki → a schema file like AGENTS.md)
  and its operations (ingest / query / lint, including orphan detection) are the
  shape this vault follows.
- **The tool** is [agent-wiki (awiki)](https://github.com/TacoTakumi/agent-wiki),
  which explicitly implements that concept. Notably, awiki's headline design makes
  Obsidian-style wikilinks (double square brackets around a page title) a
  *first-class feature* (tied to its Obsidian/Logseq
  compatibility and OKF-alignment) - so the wikilink constraint below is a
  deliberate choice of the tool, not an accident.

## What I wanted

- A knowledge base that is **agent-first** - an AI agent is the primary author and
  reader - yet **still usable by a human** as a PKB: browsable, searchable,
  readable in a plain editor.
- To **reuse the MkDocs PKB approach as closely as possible** rather than invent a
  new stack: plain Markdown as the source of truth, the wiki content confined to a
  `docs/` folder, and a build/quality-gate infrastructure built around it.

## What I care about

- [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md) - content stays human- and
  machine-readable, outliving any one tool.
- [Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md) - the substrate is open, so I can
  change it when it disagrees with me.

## What that led me to

- **Agent-first substrate → agent-wiki (awiki)** as the engine: it is built for
  agent authoring/retrieval, renders plain Markdown, and its vault *is* a folder of
  Markdown files a human can read directly.
- **Mirror the MkDocs setup → keep the vault in `docs/` only**, and build the repo
  infrastructure (build, checks, CI) around that folder - the same shape as the
  MkDocs PKB, so the two are structurally familiar.

## The tension I am accepting for now

awiki's backlink and orphan graph is driven **only** by wikilink syntax; standard
Markdown links are not tracked (see
[awiki tracks backlinks via wikilinks only, not Markdown links](../tools/awiki_tracks_backlinks_via_wikilinks_only_not_markdown_links.md)). So to keep
awiki's graph working I must author **wikilinks** - which **conflicts with**
[Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md), since wikilinks are portable only
across wikilink-aware tools.

I am **accepting this ambiguity deliberately** rather than fighting the tool
mid-build: wikilinks for now, with the conflict recorded here instead of hidden.
The path to resolving it - teaching awiki to understand Markdown links, by
forking or upstreaming - is captured as a separate investigation and is not a
blocker for building the wiki.

## Where the infrastructure will differ from the MkDocs stack

Unlike the generic MkDocs stack, the wiki engine becomes a **first-class citizen
of the quality gate**: the pre-commit/CI layer would run *awiki's own commands* as
checks - e.g. `awiki lint --strict` as a gate ([Treat warnings as errors](../principles/treat_warnings_as_errors.md)),
`awiki index` to keep the index fresh, plus guards for wiki-specific footguns
(such as the newline-inside-a-wikilink breakage). This applies
[Guard invariants at commit-time, not review-time](../principles/guard_invariants_at_commit_time_not_review_time.md) and
[Mirror every local guard in CI](../principles/mirror_every_local_guard_in_ci.md) to the wiki engine itself.

## What I have not decided yet

The concrete blueprint - the exact `docs/`-only layout, the awiki-in-pre-commit
wiring, how `awiki lint`/`index` behave as hooks - is deliberately **not written
yet**. It is blocked on actually standing up the repo, so it can be documented
from a validated setup rather than guessed. This decision points forward to that
future blueprint.
