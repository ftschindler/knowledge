---
type: Reference
title: 'Federated OKF knowledge bases: a workspace-manifest architecture'
description: An implementation-ready architecture binding independent OKF bundles into one privacy-tiered
  knowledge base through a workspace manifest and a skill layer.
tags:
- okf
- pkb
- llm-wiki
- agent-first
- knowledge-management
- federation
- mkdocs
- research
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
An **implementation-ready** architecture for binding an arbitrary number of
independent [OKF v0.2](open_knowledge_format_okf_findings.md) bundles into one
privacy-tiered personal knowledge base, driven by an agent skill layer. Written as
a starting point a fresh session can build from. It settles the questions left open
in [Agent-integration layer and multi-vault interaction for an OKF-conformant PKB](agent_integration_layer_and_multi_vault_interaction_for_an_okf_conformant_pkb.md)
and [Substrate options for an OKF-based agent-first LLM wiki: investigation](substrate_options_for_an_okf_based_agent_first_llm_wiki_investigation.md).
Substrate context: [MkDocs Material PKB publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md),
[Building my visual PKB](../decisions/building_my_visual_pkb.md). Alternatives that
were considered and rejected are in *Things we tried* at the end.

## Problem

Separate knowledge by who may see it, across an arbitrary set of bundles that **do
not know about each other**, each an OKF bundle in its own git repo (e.g. `public`,
`arup`, `team`, `person_bar`, `private`). All coupling must live in **one local
place**, never smeared across the bundles or the cross-links.

## Architecture at a glance

- **Flat, independent OKF bundles.** No nesting, no submodules. Each bundle is its
  own git repo, clones standalone, publishes standalone, and is unaware of the
  others.
- **One workspace manifest** (`workspace.okf.yaml`) is the sole artifact that knows
  the bundles are related; it assigns each bundle a role in this local context.
- **A thin skill layer** that reads the manifest and owns only the concerns a single
  bundle cannot handle for itself.
- **The leak guard is enforced in each repo's own pre-commit/CI**, not only in the
  skill layer, so a bundle is safe even when an agent writes to it directly.

```text
~/.agents/wikis/
  workspace.okf.yaml     <- THE GLUE (not a bundle; the sole coupling point)
  public/  arup/  team/  person_bar/  private/   <- independent repos + OKF bundles
```

## The workspace manifest

`workspace.okf.yaml` - four fields per bundle:

```yaml
bundles:
  public:          { path: ./public/docs,          referenceable_by: "*",     writable: true,  publish: https://me.example/kb }
  arup:            { path: ./arup/docs,             referenceable_by: [team],  writable: true,  publish: null }
  team:            { path: ./team/docs,             referenceable_by: [arup],  writable: true,  publish: null }
  private:         { path: ./private/docs,          referenceable_by: [],      writable: true,  publish: null }
  upstream_public: { path: ./upstream_public/docs,  referenceable_by: "*",     writable: false, publish: https://them.example/kb }
```

| field | question it answers | default |
| --- | --- | --- |
| `path` | where the bundle root is checked out locally | (required) |
| `referenceable_by` | who may point *at* me (the leak rule) | `[]` (no one) |
| `writable` | may an agent author into this bundle here | `false` |
| `publish` | my published URL base, if any | `null` |

Both configurable defaults **fail closed**: an unconfigured bundle is sealed
(`referenceable_by: []`) and read-only (`writable: false`) until deliberately opened
on each axis.

### Field semantics

- **`path`** - read-side resolution (URL→local): on ingest, recognise that a cited
  upstream URL is actually a local checkout and resolve it locally instead of
  fetching the internet. Also the lint/skill bundle-root, so nothing walks the
  filesystem to find boundaries. **Pointing `path` at a `./repo/docs` subdir is
  intended** - it matches the MkDocs "content in `docs/`, infra at repo top level"
  layout with zero change; the manifest looks one level in.
- **`publish`** - write-side resolution (local→URL): when authoring a cross-bundle
  link, emit the target's published URL if it has one, else a workspace-relative
  path. `publish: null` is meaningful ("not published, keep links local"). The
  published URL has **no `docs/`** segment (MkDocs strips it) while `path` does -
  which is exactly why `path` and `publish` are two independent fields.
- **`referenceable_by`** - the leak rule (below).
- **`writable`** - authoring capability; a read-only upstream repo you can't push to
  is `writable: false` yet fully readable and referenceable.

## The reference rule (leak control)

> **A concept in bundle A may reference a concept in bundle B  iff  A ∈ B.`referenceable_by`** (a bundle may always reference itself).

`referenceable_by` is **inbound-only** - it controls who may point *at* me, which is
precisely the leak axis (B's content must not surface where B may not be seen).
Outbound references a bundle makes are governed by the *target's* list. `"*"` means
"anyone" (public as shared foundation); `[]` means "no one" (private). It is a plain
allow-list - no ranks, no ordering. This directly expresses both requirements:
private is `referenceable_by: []` (never referenced); mutual peers list each other
(`arup ↔ team`), which is a symmetric, order-free permission a ranking could not
capture. One dictionary lookup enforces it.

## Read-only upstreams are first-class sources

A `writable: false` bundle (someone else's repo you cannot publish into) is a pure
**source**: freely read and referenced, never authored into. Because you cannot fix
a dangling link into it (you don't control the target), such cross-references should
also be recorded as OKF `sources[]` provenance entries (with the upstream's
`publish` URL and a `last_modified` signal), so provenance survives if the live link
breaks.

## The skill layer

Agents reach the bundles through skills rather than a runtime. A skill's first act is
to read `workspace.okf.yaml`; it then owns the manifest-aware concerns, which are the
only concerns a single bundle cannot handle for itself:

- **ingest** - read source → **classify** the target bundle (fail-closed to the
  sealed, most-private one) → **gate** (target must be `writable`; placing into a
  more-open bundle than the default needs human sign-off, since publishing is
  irreversible disclosure) → resolve cross-links via `path`/`publish` → write the
  concept, and that bundle's own `index.md` and `log.md`.
- **query** - fan out across every bundle in the manifest, since reading is
  unrestricted, then merge and cite by bundle-qualified path or URL. The asymmetry is
  read-all, write-one.
- **lint** - per-bundle conformance and within-bundle links, plus the one check a
  single bundle cannot make: the cross-bundle `referenceable_by` rule, and references
  into an upstream that no longer resolve.
- **promote** - move a concept to a more-open bundle. First-class and human-gated,
  because it is irreversible disclosure: the target's git history keeps it forever.
  This is *why* ingest fails closed to sealed - demotion cannot un-leak history.

!!! warning "Layering this over a second set of skills does not work"
    An earlier version of this architecture wrapped the single-bundle `kb-*` skills
    from [agent-knowledge](../tools/agent_knowledge.md), with each federated skill
    invoking its single-bundle counterpart per bundle and delegating every write to
    it. The attraction was obvious: nothing reimplemented, upstream improvements for
    free.

    It was built and retired. A skill is prose an LLM reads, so one skill invoking
    another is control flow through prompt obedience, and skills have no dependency
    resolution to guarantee the wrapped ones are even installed. The rule that
    replaced it: **a skill may run a command; a skill never invokes another skill.**
    See [Wrapping the kb skills in a federation layer](../explorations/wrapping_the_kb_skills_in_a_federation_layer.md).

## Enforcement: the leak guard cannot live only in the skill

An agent can always write a file directly, and a skill is a document it may not have
read. So the failure to design against is not misuse of the skill layer but
**bypassing it**: a concept written straight into a publishable bundle, skipping the
classify step, the disclosure gate and the fail-closed default, silently.

Therefore the leak boundary **must not depend on anyone remembering to use the skill
layer**.
Each bundle must be leak-safe *by itself*, enforced at commit time in its own repo,
independent of the manifest:

- **Per-repo pre-commit is the real gate.** A publishing bundle's own hooks reject
  outbound cross-bundle links except to declared-safe (public URL) targets - this
  catches an up-link leak however the file was authored, because pre-commit runs on
  the commit, not on the skill.
- **Keyword/secret scanner** per publishing bundle (client names, internal
  hostnames, codenames) - the "named-entity ⇒ not public" rule enforced at commit.
- **CI publish-gate** - human review of the diff before anything goes live, the
  second checkpoint the semantic "is this prose confidential" judgment needs
  (pre-commit cannot reliably make it).

The skill layer provides convenience and correctness; the per-repo commit-time guards
provide the actual security boundary. The manifest is a guardrail, not a security
boundary. This extends the standalone-clean property from
"clones clean" to "commits clean even under misuse."

## Suggested build order

1. **Manifest schema + loader.** Define `workspace.okf.yaml`, a JSON-schema for it,
   and a small loader that resolves `name → {path, referenceable_by, writable,
   publish}` and the local↔URL map. Everything else depends on this.
2. **Workspace-scope lint + per-repo pre-commit guards.** Build the security boundary
   before any writer exists: cross-bundle `referenceable_by` check, dangling-ref
   check, and the per-repo "no foreign outbound links" and keyword-scanner hooks.
   This is the leak boundary; it must precede ingest.
3. **Ingest** (classify → gate → write) and **query** (fan-out and merge). The core
   daily loop.
4. **Promote** and **init** last - lower-frequency operations.

Pilot on one writable bundle (`public`) plus one read-only upstream to exercise both
axes before adding the private tiers.

## Notes

- **`AGENTS.md` is not relied upon.** The manifest's `path` fully replaces the
  bundle-boundary role a per-bundle `AGENTS.md` played in earlier designs. Each repo
  may keep a top-level `AGENTS.md` for detached-agent convenience (it does not touch
  `docs/` content), but the workspace binding needs none. The maintainer *contract*
  (OKF rules, trust model, house style) lives in the skills.
- **Composition is ambient, not pinned.** The manifest points at whatever each
  bundle currently is; there is no reproducible "whole-stack at commit X". Acceptable
  for a personal KB; recorded so it is a deliberate choice.

## Things we tried (rejected alternatives)

Kept only as a record of why the flat-manifest design won.

- **Nested submodule chain** (most-private outermost, more-public bundles as
  submodules). Spec-legal (OKF §3 allows a bundle as "a subdirectory within a larger
  repository") and gives frictionless path-based cross-tier links - but couples tiers
  in git: an outer operation can disturb inner uncommitted work (**knowledge-loss
  risk**), pins go stale, and it forces a *linear* tier order the real topology does
  not have.
- **Ignored nested checkouts** (parent `.gitignore`s each inner bundle). Removes git
  coupling but keeps the awkward nesting and can double-track content if the ignore
  boundary drifts from the bundle boundary.
- **Sensitivity lattice** (partial order over trust labels, down-only reference
  rule). Expressive but over-engineered: explaining what a label like
  `arup-confidential` implies took a full page, which disqualifies it as a *setting*.
  Collapsed to the per-bundle `referenceable_by` allow-list once the real
  requirements (sealed private; mutual, unranked peers) showed a plain allow-list
  suffices.
- **Raw URL-federation** (cross-bundle links by published URL, no manifest). The
  local↔URL mapping ended up smeared across every link and every ingest, error-prone;
  centralising it in the manifest's `path`/`publish` fixed exactly this.
- **Per-bundle `AGENTS.md` as boundary marker.** Made redundant by manifest `path`.
