---
type: Reference
title: Agent-integration layer and multi-vault interaction for an OKF-conformant PKB
description: How an agent reaches an OKF-conformant personal knowledge base, and how several vaults at
  different privacy tiers interact.
tags:
- okf
- pkb
- llm-wiki
- agent-first
- knowledge-management
- mkdocs
- research
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
Two open questions about running a
[Karpathy-style LLM wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
as an [OKF v0.2](open_knowledge_format_okf_findings.md)-conformant personal
knowledge base whose substrate is already settled (the
[MkDocs Material PKB publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md) + git + pre-commit). Sibling context:
[Substrate options for an OKF-based agent-first LLM wiki: investigation](substrate_options_for_an_okf_based_agent_first_llm_wiki_investigation.md),
[Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md),
[Building my visual PKB](../decisions/building_my_visual_pkb.md).

## Question 1: how OKF-conformant vaults interact

**OKF has no native cross-bundle link mechanism - the bundle is the boundary.**
"How vaults interact" is therefore a design decision layered on top of OKF, built
from three primitives the spec (v0.2) does give:

- **The bundle is the unit of distribution (§2).** Each vault = one OKF bundle.
  Concept IDs are *bundle-relative* paths; a `/`-absolute link means "relative to
  *this* bundle root" (§6.1), not a global namespace. There is deliberately no
  `/other-vault/concept.md` form.
- **Links stay inside a bundle; URLs cross the boundary (§6.2).** The spec-blessed
  way one vault points at another is to treat the target as an **external
  resource** - an absolute URL in a `resource` or `sources[].resource` field. In a
  MkDocs setup that is the *published URL* of the target concept, which survives
  the target being a separate repo, deploy, and access boundary.
- **Broken/dangling links are legal (§6.1, §11).** Consumers MUST tolerate a link
  whose target is not in the bundle, which is what makes loose cross-vault coupling
  conformant.

**Interaction model: N independent OKF bundles, federated by published-URL
references and provenance `sources`, never a shared link namespace.** Concretely:

- Each vault is its own bundle with its own `index.md` (may carry
  `okf_version: "0.2"`), `log.md`, and conformance. Do not fuse vaults into one
  giant bundle - the spec pushes federation, not fusion.
- Within a vault: bundle-relative `/`-absolute standard markdown links (already
  OKF-conformant in the MkDocs stack, which forbids wikilinks).
- Across vaults: reference by published URL, recorded as a `sources[]` entry (with
  credibility signals) for provenance, or an inline link for narrative.
- Privacy falls out by construction: enforce a **one-way reference rule**
  (`private`/`arup` → `public` allowed, never the reverse) as a pre-commit
  link-domain check.
- `sources[].resource` also accepts a **scope descriptor** (§5.1) - "all X in vault
  Y" - for whole-vault derivation with no resolvable link.

Design fork (deferred): cross-vault refs as **rendered-site URLs** (portable,
respects deploy boundary - recommended, matches
[Local-first, but not local-required](../wishes/local_first_but_not_local_required.md)) vs **relative git paths** assuming a
monorepo checkout (offline-resolvable but couples on-disk layout).

## Question 2: the agent-integration layer

The gap is not technology but the **skill + contract layer** that turns a generic
LLM into a disciplined OKF wiki maintainer.
[stjbrown/agent-knowledge](https://github.com/stjbrown/agent-knowledge) is the
closest existing template, and its central lesson is architectural: **the
discipline lives in skills + an AGENTS.md contract; the CLI (Janet) is optional
and only adds runtime/UI/auth/memory.** Take the pattern, skip the engine - the
same conclusion the substrate investigation reached, now confirmed against a real
implementation.

### What agent-knowledge is (the reusable pattern)

A **hub-and-spoke skill pack**: one `kb` hub skill (shared vocabulary + routing,
never writes) plus action skills `kb-init`, `kb-ingest`, `kb-query`, `kb-lint`,
`kb-visualize`, `kb-document` - each a `SKILL.md` procedural prompt. Ingest/query
are **agent-instruction-driven**; only the mechanical conformance check shells out
to a deterministic Node script. The key split:

> The agent does the judgment (read, plan, synthesize, relink, log). A
> deterministic checker does the mechanical verdict (conformance, orphans, drift).
> The LLM is never trusted to self-certify conformance.

Links are standard markdown (no wikilinks); backlinks/`cited_by` and orphans are
**computed** from the markdown links (as `kb-visualize`/`kb-lint` do), not from a
wikilink graph.

### Target architecture for a MkDocs + git PKB

- **Layer 1 - Contract (`AGENTS.md` per vault root).** The missing artifact;
  Karpathy's "schema file." Encodes OKF v0.2 as a hard invariant (one concept =
  one `.md`, required `type`, reserved `index.md`/`log.md`, standard
  bundle-relative links), the trust model (`generated`/`sources`/`verified`/
  `status`/`stale_after` + actor convention `human:felix`, `<agent>/<version>`,
  `process:<id>`), append-only-on-meaning, "file good answers back as concepts,"
  and existing house conventions (which already match).
- **Layer 2 - Skills** (portable across Claude Code / OpenCode, like the existing
  `awiki-*` skills): `pkb-ingest`, `pkb-query`, `pkb-lint` (agent report over a
  deterministic script), optionally `pkb-document` / `pkb-visualize`.
- **Layer 3 - Deterministic checks in the existing pre-commit/CI** (no engine):
  OKF frontmatter conformance (`check-jsonschema`), link integrity + orphans
  (`markdown-link-check` / `remark-validate-links`), `index.md`/`log.md`
  structural lint. The MkDocs side already owns the consumer + graph layer
  (`backlinks-section`, `mkdocs build --strict`, `validation.*`) - the piece
  agent-knowledge leaves you to build is already built.

### Take vs skip

| Take (pattern) | Skip (engine) |
| --- | --- |
| Hub + action skill split | Janet CLI runtime/UI/auth/memory |
| `AGENTS.md` OKF + trust contract | The Node `conformance.mjs` (rewrite as a pre-commit hook) |
| Agent-driven ingest/query, deterministic lint | Bespoke query planner (MkDocs search + `index.md` suffices at PKB scale) |
| Trust frontmatter + append-on-meaning | Multi-bundle catalog engine (use the URL-federation model from Q1) |

### How the two questions cohere

Skills operate **one bundle at a time**; Q1 federates bundles by URL. So each of
`public` / `arup` / `private` gets its own `AGENTS.md` + the shared skill pack +
its own per-vault conformance gate, with cross-vault URL links direction-checked
in lint.

### Caveat: dual-author, not agent-only

agent-knowledge's trust model assumes the *agent* is the primary author. This PKB
is genuinely dual-author (human writes in nvim/Obsidian too), so the
"append-only, LLM maintains everything" stance needs the
**human-correction-survival** discipline flagged in the gist's comment thread:
record the human's *intent/claim* (not a text diff), and re-check it after each
regeneration - keep if still satisfied, surface (don't silently drop) if a newer
source contradicts it. This is the one place to *extend* the agent-knowledge
pattern rather than copy it.

## Bottom line

A coherent, engine-free design: **N independent OKF bundles federated by
published-URL references**, each maintained by a per-vault `AGENTS.md` contract + a
shared portable skill pack + deterministic OKF/link checks folded into the existing
MkDocs + git + pre-commit stack. Concrete next step (implementation, not yet done):
seed one vault (`public`) with an `AGENTS.md` contract + a `pkb-ingest` skill + an
OKF conformance pre-commit hook as an end-to-end vertical slice before rolling the
pattern across all three vaults.
