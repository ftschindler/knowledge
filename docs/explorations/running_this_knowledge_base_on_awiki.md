---
type: Exploration
title: Running this knowledge base on awiki
description: The phase in which this knowledge base was an agent-wiki vault, what that proved about
  agent-first authoring, and the four things that ended it.
tags:
- exploration
- awiki
- llm-wiki
- pkb
- knowledge-management
- agent-first
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
---
!!! note "This is an [exploration](../index.md#explorations)"
    Something I committed to, built on, and withdrew from. It is a record of what the
    work taught, not a description of how anything is done now.

Most of the pages in this bundle were first written inside the vault described
below, which is why several of them still carry an `awiki` tag.

## What I wanted

[Building my visual PKB](../decisions/building_my_visual_pkb.md) had already
resolved the [Wishes for a personal knowledge base](../wishes/wishes_for_a_personal_knowledge_base.md)
into a substrate: plain Markdown in git, MkDocs Material to publish it, Obsidian
as an optional editor. Those wishes still stood, and none of what follows was
allowed to cost them. What they did not cover is what changes once an **agent**
becomes the primary author rather than an occasional helper, which added two
more:

- **Agent-first, without ceasing to be human-readable.** An agent writes the
  pages; a person can still read, browse and edit them in a plain editor.
- **One stack, not two.** Reuse the MkDocs shape rather than invent a second
  system beside it: content confined to `docs/`, build and quality gates around
  that folder, the same as the site already had.

## What I tried

The pattern comes from
[Karpathy's LLM-wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
an LLM incrementally builds and maintains a persistent, interlinked Markdown
wiki as a *compounding artefact*, knowledge compiled once and kept current,
rather than re-derived from sources on every query as in the RAG model. Its
three layers (immutable raw sources, an LLM-owned wiki, and a schema file such
as `AGENTS.md`) and its operations (ingest, query, lint including orphan
detection) are the shape I set out to follow.

The tool was [agent-wiki (awiki)](https://github.com/TacoTakumi/agent-wiki),
which implements that concept directly. I ran it as a **multi-vault** setup: a
`public` vault (the ancestor of this bundle), a private sink for captured agent
conversations, and internal vaults for work, all reached through one CLI with a
routing convention for the agent (publishable content to `public`, anything
naming an employer or client to an internal vault, raw capture to the private
sink). The intention was to make the engine a first-class citizen of the quality
gate, with `awiki lint --strict` and `awiki index` running as pre-commit hooks in
the same way every other invariant here is guarded.

Before trusting it with real conversation history and a public repository I read
its source, which became
[Security Analysis of Agent Wiki (awiki)](../research/security_analysis_of_agent_wiki_awiki.md).
That review found no covert egress and no telemetry of any kind, so nothing below
is a complaint about the tool's integrity. It is a good tool that turned out to
be the wrong tool for this.

## Why I stopped

Four reasons, in the order they became apparent. None of them alone would have
been decisive.

### The link convention conflicted with a value

awiki's backlink and orphan graph is built exclusively from wikilink syntax;
ordinary Markdown links are invisible to it, verified empirically in
[awiki tracks backlinks via wikilinks only, not Markdown links](../findings/20260827_awiki_tracks_backlinks_via_wikilinks_only_not_markdown_links.md).
Keeping the graph working therefore meant authoring wikilinks, which are portable
only across wikilink-aware tools, in direct conflict with
[Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md).
The published MkDocs site and the GitHub web interface both want standard
Markdown links; the engine wanted the other kind.

I recorded this at the time as a tension I was **deliberately accepting** rather
than fighting mid-build. That was the right call for a week and the wrong call
for a year: a documented conflict with a value does not stop being a conflict
because it is documented.

### The raw-and-rendered split was circular for content already in Markdown

awiki copies an ingested file into an immutable `raw/` archive and renders a
second page from it, with a sidecar to guard against the two drifting apart.
That is exactly right for a PDF or a web page. For a note I authored *as
Markdown*, it means the thing I edit and the thing that publishes are two
different files, and a mechanism exists to police the gap between them. There is
no version of that which is not circular.

Wanting to edit the published file directly is a small wish that turns out to
have large consequences: it rules out every design with an ingest pipeline in the
middle, which is most of them.

### The CLI was the only door in

Every operation went through the tool. That conflicts with
[Do not make a tool a prerequisite for work it is not needed for](../principles/do_not_make_a_tool_a_prerequisite_for_work_it_is_not_needed_for.md),
and it is not what the pattern asks for: Karpathy's gist makes the *schema file*
the discipline mechanism and labels CLI tooling explicitly optional. Git and
pre-commit were already the control plane in this repository. Adding a second
one, which the first could not see into, bought nothing.

The point at which this stopped being theoretical was
[awiki title extraction breaks on frontmatter-led source files](../findings/20260827_awiki_title_extraction_breaks_on_frontmatter_led_source_files.md):
ingesting a file authored under this bundle's own convention, where the title
lives in frontmatter and the body starts at `##`, silently produced a garbage
title and a garbage slug. Two authoring conventions, one of which I could not
change, meeting in a pipeline I did not control.

### One vault is the wrong shape for several privacy tiers

The security review's real finding was not a leak but an aggregation: the tool's
purpose is to concentrate transcripts, decisions and configuration into a single
plain-text vault, unencrypted at rest, and its redaction is a regex best-effort
applied to conversation ingest only. The multi-vault routing I was running was a
**convention the agent was asked to follow**, not a boundary anything enforced.
Nothing rejected a commit that put client specifics into the public vault.

That is the requirement the whole design was missing, and it is the one that
pointed at what came next: the separation has to be enforced where commits
happen, per repository, not by an agent remembering which vault it was told to
write to.

## What I kept

Almost all of it, which is why this page is worth its length:

- **The pattern.** The compounding wiki, its three layers, ingest/query/lint as
  the operations. This bundle still is that. What changed is that a contract and
  pre-commit hooks play the engine's part.
- **Agent-first authoring works.** An agent as primary author with a human as
  editor and reviewer produced better-maintained pages than I write by hand, and
  it is how this bundle is still written. That is the exploration's positive
  result.
- **The engine belongs in the quality gate.** The instinct to run the knowledge
  tool's own checks as pre-commit hooks survived; the hooks in this repository
  are the same idea with the engine replaced by scripts.
- **[Open Knowledge Format](../research/open_knowledge_format_okf_findings.md).**
  Reached through awiki's alignment with it, and kept once it became clear the
  format mandates no tooling, no raw-and-rendered split, and standard Markdown
  links, meaning it grants everything I wanted from the engine and imposes none
  of the costs.
- **Privacy tiers as a first-class requirement**, promoted from a routing
  convention to something enforced.

## What I gave up

Capabilities, not polish, and rebuildable if they turn out to matter:

- The auto-context hook, which injected pointers to relevant pages on every
  prompt.
- The conversation-transcript adapters for Claude Code and OpenCode.
- A served vault with token auth for multi-machine access.

For a write-first personal knowledge base these are conveniences. Recorded here
so that if one of them is later missed, it is missed knowingly.

## What it led to

The survey of what to use instead is
[Substrate options for an OKF-based agent-first LLM wiki: investigation](../research/substrate_options_for_an_okf_based_agent_first_llm_wiki_investigation.md),
which scored candidates against requirements written directly out of the four
failures above and deliberately stopped short of choosing. The choice itself is
[Federating my knowledge base as privacy-tiered OKF bundles](../decisions/federating_my_knowledge_base_as_privacy_tiered_okf_bundles.md).
