---
type: Decision
title: Federating my knowledge base as privacy-tiered OKF bundles
description: Why this knowledge base is now one of several independent OKF bundles bound by a workspace
  manifest, with no engine between the author and the file.
tags:
- decision
- okf
- pkb
- knowledge-management
- federation
- agent-first
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
---
A decision record in the same wish-first voice as its predecessors (see
[Layer build-knowledge as a values-to-blueprints derivation pipeline](../knowledge_management/layer_build_knowledge_as_a_values_to_blueprints_derivation_pipeline.md)).
It is the current answer to the question
[Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md)
failed to settle, and the bundle you are reading is its first instance.

It does not supersede
[Building my visual PKB](building_my_visual_pkb.md).
That decision still holds in full: this is still plain Markdown in git, still
published with the
[MkDocs Material PKB publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md),
still editable in Obsidian or `nvim`. What this decision settles is what lives
*inside* `docs/`, and how several such directories relate to each other.

## What I wanted

Everything the earlier decision asked for, plus the four requirements the awiki
exploration produced:

- **The file I edit is the file that publishes.** No ingest step, no rendered
  copy, no drift guard between two versions of one note.
- **Standard Markdown links only**, so a page reads correctly in an editor, on
  GitHub and on the site, without a tool to interpret it.
- **No mandatory tool between me and the content.** An agent, a skill or a CLI
  may help; none may be the only door in.
- **Privacy separation that a commit cannot bypass**, rather than a routing
  convention an agent is asked to honour.

## What I care about

- [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md),
  which the wikilink requirement had been quietly costing me.
- [Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md).
- [Guard invariants at commit-time, not review-time](../principles/guard_invariants_at_commit_time_not_review_time.md),
  which is the principle that turns "keep client names out of the public bundle"
  from an intention into a mechanism.

## What that led me to

- **A format instead of an engine.**
  [Open Knowledge Format](../research/open_knowledge_format_okf_findings.md)
  specifies one concept per Markdown document, standard Markdown links, and no
  required tooling, with conformance judged file-structurally. It grants what the
  engine was for and imposes none of what the engine cost. `docs/` is an OKF
  bundle; [okf-floor.yaml](https://github.com/ftschindler/knowledge/blob/main/docs/okf-floor.yaml)
  declares the handful of fields this bundle requires beyond it, in one place both
  the local hooks and any federation tooling read.
- **Git and pre-commit as the only control plane.** Each job the CLI used to do
  becomes a hook: frontmatter conformance, link resolution, index reachability,
  file naming. This is the existing quality-gate machinery pointed at the content
  rather than a second system beside it.
- **Federation instead of one vault.** Several independent OKF bundles, each its
  own git repository, each cloning and publishing standalone and unaware of the
  others, bound by a single local `workspace.okf.yaml` that assigns each a role.
  The architecture is written up in
  [Federated OKF knowledge bases: a workspace-manifest architecture with fkb-over-kb skills](../research/federated_okf_knowledge_bases_a_workspace_manifest_architecture_with_fkb_over_kb_skills.md).
- **The leak boundary in each repository, not in the skill layer.** The manifest
  is a guardrail; the actual boundary is each bundle's own pre-commit hooks and
  publish gate, so a bundle stays safe even when an agent bypasses the federation
  layer entirely. This is the direct answer to the aggregation risk the
  [security review](../research/security_analysis_of_agent_wiki_awiki.md) found.
- **A skill layer, kept thin.** Agents reach the bundles through skills rather
  than a runtime: single-bundle mechanics wrapped by a federation layer that owns
  only the manifest-aware decisions. Skills are prose an agent reads, so they are
  replaceable by hand at any point, which keeps the "no mandatory tool" property
  intact.

## What I built

The bundle you are reading, as the `public` tier: an OKF bundle over the same
MkDocs stack, with the hooks doing what the engine used to.

The federation layer around it is
[federated-knowledge-skills](https://github.com/ftschindler/federated-knowledge-skills),
currently at design stage. Its blueprint is not written here yet, deliberately,
for the same reason the previous decision deferred one: it should be documented
from a working setup rather than guessed at. This decision points forward to it.

## What I gave up, and would reconsider

- **Composition is ambient, not pinned.** The manifest points at whatever each
  bundle currently is. There is no reproducible "whole knowledge base at commit
  X". Acceptable for a personal knowledge base, and recorded so that it stays a
  choice rather than an oversight.
- **The conveniences listed in the exploration**: auto-context injection,
  transcript ingest adapters, a served vault. Each is rebuildable as a skill or a
  script if it is ever actually missed.
- **A federation of independent repositories is more moving parts than one
  vault.** The trade is worth it only because privacy tiers are a real
  requirement here. Someone with a single tier should not copy this.
