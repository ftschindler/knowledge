---
type: Tool
title: agent-wiki (awiki)
description: A CLI-driven markdown knowledge vault that agents search before the web and write back to,
  and the tool this knowledge base ran on for a while.
tags:
- tools
- agent-wiki
- llm-wiki
- okf
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
sources:
- id: awiki-readme
  resource: https://github.com/TacoTakumi/agent-wiki
  title: 'TacoTakumi/agent-wiki: README and command reference'
  last_modified: '2026-09-10'
- id: ak-llm-wiki
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/concepts/llm_wiki.md
  title: 'LLM Wiki (stjbrown/agent-knowledge)'
  author: human:stjbrown
  last_modified: '2026-08-01'
- id: ak-three-layer
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/concepts/three_layer_architecture.md
  title: 'Three-Layer Architecture (stjbrown/agent-knowledge)'
  author: human:stjbrown
  last_modified: '2026-08-01'
---
[agent-wiki](https://github.com/TacoTakumi/agent-wiki) (`awiki`) is a single plain-markdown
vault that AI agents search before reaching for the web, and write back to when they learn
something worth keeping. It is an implementation of the
[LLM wiki](https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/concepts/llm_wiki.md)
pattern, and it is the tool this knowledge base ran on before it became an OKF bundle.

| | |
| --- | --- |
| Author | TacoTakumi |
| Licence | GPL-3.0-or-later |
| Language | Python, 3.10+ |
| Distribution | PyPI `agent-wiki-kb`, installing `awiki` and `aw` |
| Source | [github.com/TacoTakumi/agent-wiki](https://github.com/TacoTakumi/agent-wiki) |
| Version I ran | 0.8.1 |

## What it is

The vault is files: markdown with YAML frontmatter, `[[wikilinks]]` between pages, topic
folders, a generated `index.md` and an append-only `log.md`. No database. It opens in Obsidian
or Logseq as-is, and greps like any other directory.

It follows the
[three-layer architecture](https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/concepts/three_layer_architecture.md)
the pattern describes, and follows it literally: an immutable `raw/` archive of ingested
sources, the wiki pages rendered *from* those sources, and `wiki.yaml` as the schema layer.
Each page carries a `render_hash`, so a page edited by hand is detected as drift and
`awiki reingest` prints a diff rather than clobbering the edit.

Around that sit the things a vault needs to be useful daily: full-text search over ripgrep,
conversation-transcript adapters for Claude Code and OpenCode, a `UserPromptSubmit` hook that
surfaces relevant page titles on every prompt, a tag vocabulary with a lint gate, a linter
covering broken links, orphans, drift, staleness and index gaps, and `awiki serve` to share
one vault over HTTP with reader, writer and admin tokens.

## The design decision everything follows from

**The CLI is the only door in.** That is deliberate and stated as such: because every write
goes through `awiki`, the tool can hold the vault's invariants no matter who is driving, so a
small local model needs to know a handful of commands rather than the vault's layout. The same
commands work against a local folder or a remote vault, which is what makes one shared brain
across several machines cheap.

It is also the property that decided against it here, for a knowledge base whose control plane
was already git and pre-commit. That argument, and three others, are in
[Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md).

## On its OKF claim

The README describes the vault as roughly 80% conformant with the
[Open Knowledge Format](../research/open_knowledge_format_okf_findings.md) *by convergent
design* rather than by implementing the spec: markdown with frontmatter, generated `index.md`
and `log.md`, no prescribed taxonomy, arbitrary frontmatter keys preserved. That is an honest
framing, and the missing fraction is where it matters. OKF §6.1 specifies standard markdown
links and awiki's graph reads only wikilinks; OKF makes every non-reserved markdown file a
concept, whilst awiki splits each one into a raw source and a rendered page.

## What I learned using it

- [awiki tracks backlinks via wikilinks only, not Markdown links](../findings/20260827_awiki_tracks_backlinks_via_wikilinks_only_not_markdown_links.md)
- [awiki title extraction breaks on frontmatter-led source files](../findings/20260827_awiki_title_extraction_breaks_on_frontmatter_led_source_files.md)
- [Security Analysis of Agent Wiki (awiki)](../research/security_analysis_of_agent_wiki_awiki.md) - a full source read, asking what it does with your data
- [Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md) - the phase spent running on it, and why it ended

## Where it sits among the alternatives

[stjbrown/agent-knowledge](https://github.com/stjbrown/agent-knowledge) maintains a survey of
this space, including a
[landscape](https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/ecosystem/landscape.md)
of the tools implementing the pattern and a
[comparison](https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/ecosystem/competitor_comparison_v2.md)
of the OKF-authoring ones. It is a bundle in this workspace, so it is worth reading there
rather than restating here. The narrower question of what to use *instead*, scored against
requirements, is
[Substrate options for an OKF-based agent-first LLM wiki: investigation](../research/substrate_options_for_an_okf_based_agent_first_llm_wiki_investigation.md).
