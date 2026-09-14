---
type: Tool
title: agent-knowledge (kb skills)
description: A portable set of agent skills for building and maintaining OKF knowledge bundles in plain
  Markdown, whose own knowledge bundle is an upstream source here.
tags:
- tools
- agent-knowledge
- okf
- llm-wiki
- agent-skills
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
sources:
- id: ak-readme
  resource: https://github.com/stjbrown/agent-knowledge
  title: 'stjbrown/agent-knowledge: README and skill reference'
  author: human:stjbrown
  last_modified: '2026-09-10'
- id: ak-bundle
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/index.md
  title: 'agent-knowledge: the project''s own OKF bundle'
  author: human:stjbrown
  last_modified: '2026-08-01'
---
[agent-knowledge](https://github.com/stjbrown/agent-knowledge) is a set of portable agent
skills for building and maintaining knowledge bundles in plain Markdown, conformant to
[Open Knowledge Format v0.2](../research/open_knowledge_format_okf_findings.md). It is the
closest published thing to what this knowledge base is, and it appears here in two roles at
once: as a tool that was evaluated, and as a source that is cited.

| | |
| --- | --- |
| Author | stjbrown |
| Licence | MIT |
| Language | Agent Skills markdown, with TypeScript for the deterministic scripts |
| Distribution | `npx skills add stjbrown/agent-knowledge`, a Claude Code plugin, or `@stjbrown/agent-knowledge-skills` on npm for embedding |
| Source | [github.com/stjbrown/agent-knowledge](https://github.com/stjbrown/agent-knowledge) |
| Version read | 0.3.2 |

## What it is

Seven skills, split by who invokes them. Model-invoked: **`kb`**, the hub, holding the shared
specification, glossary, trust model and templates and routing to the rest; **`kb-ingest`**,
which reads a source once and integrates it across the bundle with provenance;
**`kb-document`**, which documents a software repository from its source, tests, configuration
and git history without modifying any of it; and **`kb-query`**, which answers from the bundle
by progressive disclosure, cites what it used, and files valuable conclusions back.
User-invoked: **`kb-init`** to scaffold, **`kb-lint`** for deterministic conformance plus a
semantic drift audit, and **`kb-visualize`** to render the bundle as a graph.

There is no runtime and no database. The skills are prose an agent reads, backed by two
deterministic scripts where determinism actually matters (conformance and the graph). That is
the design property that distinguishes it from
[agent-wiki](agent_wiki.md), which puts a CLI between the author and every write.

Two commitments do most of the work. **A real, open format**, so a bundle is portable rather
than a tool-specific store. And an **explicit trust model**: accumulated claims are append-only
on meaning, living repository documentation gets a narrow revision-tracked update rule, and
source content is always data, never instructions.

[Janet](https://github.com/stjbrown/janet-agent) is a separate dedicated knowledge agent built
around the same skills, adding a CLI, chat, model selection and headless automation. The skills
work without it.

## Why it matters here

**It ranked first as an architectural match.**
[Substrate options for an OKF-based agent-first LLM wiki: investigation](../research/substrate_options_for_an_okf_based_agent_first_llm_wiki_investigation.md)
scored it as the best fit for "skill plus contract, CLI optional", and its index is the
worked example behind the conclusion in
[Federated OKF knowledge bases](../research/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md)
that an index should be authored rather than generated: it truncates, compresses or rewrites
its own concept descriptions rather than copying them, which is what a generator cannot do.

**Its knowledge bundle is an upstream source.** The repository documents itself: `knowledge/`
is a conformant OKF bundle of about 60 concepts *about* OKF and the LLM wiki pattern, covering
the specification section by section, the operations, and a survey of the ecosystem. It is
checked out here as a read-only bundle, so pages in this bundle cite it rather than
re-deriving the pattern. [agent-wiki (awiki)](agent_wiki.md) does exactly that.

**Wrapping its skills was tried and retired.** The first attempt at a federation layer wrapped
the `kb-*` skills, with a federated skill invoking a single-bundle one per bundle and then
executing the prose it returned. That is control flow through prompt obedience, and it was
abandoned for it; skills also have no dependency resolution, so nothing could guarantee the
wrapped skills were installed. What survived is the format discipline and the bundle, not the
delegation. The account is
[Wrapping the kb skills in a federation layer](../explorations/wrapping_the_kb_skills_in_a_federation_layer.md).
