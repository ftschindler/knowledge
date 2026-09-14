---
type: Reference
title: 'Substrate options for an OKF-based agent-first LLM wiki: investigation'
description: What tool or substrate to adopt for an agent-first LLM wiki that is also a human PKB, given
  an already-adopted OKF target.
tags:
- okf
- llm-wiki
- pkb
- agent-wiki
- knowledge-management
- agent-first
- research
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
What tool or substrate to adopt for an agent-first LLM wiki that is also a human
PKB, given hardened requirements and an already-adopted OKF target. It deliberately
stops short of choosing. Sibling context
lives in the exploration
[Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md),
the decision
[Building my visual PKB](../decisions/building_my_visual_pkb.md),
and the research
[Open Knowledge Format (OKF): findings](open_knowledge_format_okf_findings.md).

## The requirements this was scored against

- **R1** - agent-first AND human-readable/editable plain markdown (nvim + Obsidian
  both equal paths).
- **R2** - no `raw/`-vs-rendered duplication for notes that are *already* markdown.
  ([awiki](../tools/agent_wiki.md) copies an authored `.md` into `raw/` then renders a second page copy with
  a drift-guard sidecar - circular for already-markdown authored content.)
- **R3** - ties into agent skills + an AGENTS.md/CLAUDE.md contract, but a bespoke
  CLI must be **optional, not the only door in** - git + pre-commit already exist as
  the control plane.
- **Cross-cutting** - OKF alignment, and standard **markdown links** (NOT
  `[[wikilinks]]`). The published MkDocs PKB forbids wikilinks for GitHub/site
  portability; the current awiki vault requires them. Resolving that tension is in
  scope.

## The two reframing facts

1. **Karpathy's original LLM-wiki pattern does not prescribe an engine.** The
   [gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) makes
   the *schema file* (AGENTS.md/CLAUDE.md) the discipline mechanism and explicitly
   labels CLI tools **"Optional."** awiki's "CLI is the only door" is awiki's design
   choice, not the pattern's requirement.
2. **OKF itself mandates no tooling and standard markdown links.** From
   [OKF v0.2 SPEC.md](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md):
   *"no required tooling"* (intro/§1), one concept = *"one markdown document"* with
   every non-reserved `.md` a concept doc (§2–4, so **no raw/rendered split**), and
   links *"using standard markdown links"* (§6.1). Conformance is file-structural
   (§11). The [launch blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
   frames OKF as *"format, not platform... no new runtime, no required SDK."*

Consequence: **OKF + existing git/pre-commit + an AGENTS.md contract satisfies
R1/R2/R3 by construction.** awiki's raw/rendered split (R2 fail) and wikilink-only
backlink/orphan graph (link-convention fail) are precisely the two things OKF does
not impose.

## The unification unlock

The human MkDocs PKB and the agent wiki currently use **opposite link conventions**
(standard markdown links vs required wikilinks). That tension dissolves:

- **Obsidian backlinks AND graph work with standard markdown links** -
  `[[wikilinks]]` are not required, and Obsidian can be set to *emit* markdown
  links. Sources: Obsidian [Internal links](https://obsidian.md/help/links),
  [Backlinks](https://obsidian.md/help/plugins/backlinks),
  [Graph view](https://obsidian.md/help/plugins/graph). Vault is plain files an
  agent can maintain with no app running ([data storage](https://obsidian.md/help/data-storage)).
- **MkDocs Material** gives tags/search/backlinks/nav/orphan-validation with
  standard links, none forcing wikilinks: `mkdocs-backlinks`, Material `tags`
  plugin, core `validation.*` for orphans/broken links, `mkdocs-awesome-nav`.
  `roamlinks`/`ezlinks` support wikilinks only *optionally*.

So one standard-markdown-linked tree can serve **both** the human PKB and the agent
wiki.

## Ranked options

| Rank | Path | R1 | R2 | R3 | OKF | Links |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **OKF files + thin pre-commit scripts + AGENTS.md contract, NO engine** | pass | pass (decisive) | pass (native) | pass | md |
| 2 | **Unify into one Obsidian+MkDocs standard-md tree, agent-maintained by contract** | pass | pass | pass | pass | md |
| 3 | Adopt a different engine: NimaChu/my-wiki or [stjbrown/agent-knowledge](../tools/agent_knowledge.md) | pass | pass | pass (skill optional) | pass/partial | md |
| reject | SamurAIGPT/llm-wiki-agent, jesse-lane-ai, xinhuagu, h4pplness | - | - | - | - | force `[[wl]]` / CLI-centric |

Options 1 and 2 are the same spine (no engine; contract + pre-commit as control
plane); 2 additionally folds the human PKB and agent wiki into one tree.

## Candidate engines (if a tool is still wanted)

- **NimaChu/my-wiki** (MIT, ~123★, active) - skill *optional*, standard markdown
  links, OKF v0.2-compatible guidance. Strongest ready-made fit.
- **[stjbrown/agent-knowledge](../tools/agent_knowledge.md)** (MIT, active) - portable skills over plain markdown
  bundles, Janet CLI optional, explicit Google OKF v0.2. Best architectural match
  to "skill + contract, CLI optional".
- **langchain-ai/openwiki** (MIT, very active) - technically strong, OKF v0.2
  output, standard markdown links, but more CLI/lifecycle-opinionated.
- **Rejected for these requirements:** SamurAIGPT/llm-wiki-agent, jesse-lane-ai,
  xinhuagu (all force `[[wikilinks]]`; xinhuagu also uses a *non-Google* OKF with a
  `raw/`+`wiki/` split and unclear license), h4pplness (CLI-centric, minimal).

## No-engine toolbox (each CLI job → a real hook)

- Link integrity: `tcort/markdown-link-check`, `lycheeverse/lychee-action`,
  `remarkjs/remark-validate-links`.
- Frontmatter schema: `python-jsonschema/check-jsonschema`,
  `giantswarm/frontmatter-validator`.
- Orphans / index drift / structural lint: `sidequery/mdlint`,
  `SingggggYee/kb-lint`.
- Index/TOC generation: `thlorenz/doctoc`, `jonschlinkert/markdown-toc`.
- Search: `ripgrep`.
- Orchestration: `pre-commit`.

## OKF-native tooling (all optional utilities, not runtimes)

- [GoogleCloudPlatform/open-knowledge-format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
  (Apache-2.0) - spec + reference producer + visualizer; tooling is PoC, not required.
- [scaccogatto/okf-skills](https://github.com/scaccogatto/okf-skills) (MIT) - agent
  skills + validator script + GitHub Action for OKF v0.2. Usable as just a
  validator/action.
- [jyjeanne/okf-rs](https://github.com/jyjeanne/okf-rs) (MIT/Apache-2.0) - Rust
  generator/validator/search, optional.
- [openknowledge-sh/openknowledge](https://github.com/openknowledge-sh/openknowledge)
  (Apache-2.0) - fuller OKF CLI/runtime; mandatory only if adopted as a platform.

## The honest cost of dropping awiki

Real capabilities lost (rebuildable only if later needed), not just polish:

- **Auto-context hook** - per-prompt injection of relevant pages.
- **Conversation-transcript ingestion adapters** (Claude Code / OpenCode → vault).
- **Served shared-vault + token auth** for multi-machine access.

For a write-first personal PKB these are conveniences, not core knowledge-base
capability.

## Bottom line (research result, decision deferred)

The evidence points to **OKF plain-markdown files, standard links, maintained by an
AGENTS.md contract + skills + existing git/pre-commit - no dedicated engine** as the
only path satisfying R1/R2/R3 without compromise while hitting the OKF target and
collapsing the wikilink tension between the agent wiki and the human PKB. A concrete
decision (adopt no-engine vs a markdown-link engine like my-wiki/agent-knowledge;
unify into one tree vs two vaults sharing conventions) is **intentionally not made
here** and remains open.
