---
type: Tool
title: federated-knowledge-skills (fkb)
description: The agent skill, CLI and pre-commit hooks that bind several privacy-tiered OKF bundles into
  one federation, and the tooling this knowledge base is now written through.
tags:
- tools
- self-authored
- okf
- federation
- agent-skills
- knowledge-management
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-16T00:00:00Z'
sources:
- id: fks-readme
  resource: https://github.com/ftschindler/federated-knowledge-skills
  title: 'ftschindler/federated-knowledge-skills: README'
  author: human:felix_schindler
  last_modified: '2026-09-16'
- id: fks-design
  resource: https://github.com/ftschindler/federated-knowledge-skills/blob/main/DESIGN.md
  title: 'federated-knowledge-skills: DESIGN.md'
  author: human:felix_schindler
  last_modified: '2026-09-16'
---
federated-knowledge-skills[^fks-readme] is the layer that turns several independent
[OKF](../research/open_knowledge_format_okf_findings.md) bundles into one federation an agent
can use: a skill it reads, a CLI it runs, and two pre-commit hooks each bundle pins for
itself. It is mine, and it is the tooling this bundle is now written through, so it appears
here in the same two roles that [agent-knowledge](agent_knowledge.md) does: a tool with a page,
and the thing producing the pages.

| | |
| --- | --- |
| Author | [Felix Schindler](../people/felix_schindler.md) |
| Licence | MIT, with the vendored OKF validator under its own |
| Language | Python 3.11+, run through [uv](uv.md) as PEP 723 scripts with no install step |
| Distribution | A skill directory to copy, and two pre-commit hook ids a bundle pins by revision |
| Source | [github.com/ftschindler/federated-knowledge-skills](https://github.com/ftschindler/federated-knowledge-skills) |
| Status | The skill, the CLI and the hooks are shipped and in use here; a second tier and the retirement of the old architecture are not done |

## What it is

Four things, and the split between them is the whole design.

- **A bundle** is an ordinary directory of Markdown concepts that does not know it belongs to
  a federation. It clones, publishes and lints standalone. This one does.
- **A workspace manifest**, one file per machine, says which bundles exist locally and assigns
  each a role: whether it may be written to, which bundles may cite it, and where it publishes
  if it does. `referenceable_by []` seals a bundle, so nothing that publishes can link into it.
- **A skill**, `fkb`, is the prose an agent reads: how to answer from the bundles before
  reaching for the web, and how to file something afterwards. It runs the CLI and reads its
  own references. It is replaceable by hand, which is what keeps "no mandatory tool between me
  and the content" true.
- **A CLI**, also `fkb`, owns the handful of questions that need a deterministic answer:
  `list` for what exists and what each allows, `resolve` for one bundle as JSON, `lint` for
  whether it holds up, `url` for a link into another bundle, and `init` and `add` for setting
  one up.

Underneath, `okf-concepts` and `okf-bundle` are the same checker under two blocking policies,
shipped as pre-commit hooks a bundle pins by revision. They enforce the format's hard rules
and the fields the bundle's own `fkb.yaml` declares, and nothing else: a field the floor does
not name is reported and left alone. `okf-concepts` checks the whole bundle and fails only on
the files being committed, so an unfinished concept elsewhere never blocks an unrelated
commit, and `--all-files` makes the same hook strict in CI. This is what
[Guard invariants at commit-time, not review-time](../principles/guard_invariants_at_commit_time_not_review_time.md)
looks like when the thing being guarded is prose.

## The three decisions everything follows from

**The Markdown file is the source.**[^fks-design] No ingest step, no rendered copy, no
`render_hash` reconciling two versions of one note. An agent writes the file a person then
edits, which is the property [agent-wiki](agent_wiki.md) traded away for a CLI that could hold
the vault's invariants.

**A skill may run a command; a skill never invokes another skill.** Prose calling prose through
an LLM is not control flow. That rule is what the first attempt cost, and the account of it is
[Wrapping the kb skills in a federation layer](../explorations/wrapping_the_kb_skills_in_a_federation_layer.md).

**The manifest is a guardrail, not a security boundary.** Access control is git remote
permissions and each bundle's own publish gate. The manifest can be edited by anything running
on the machine, so nothing load-bearing may rest on it, and a bundle stays safe when an agent
bypasses the federation layer entirely. The reasoning is
[Separate audiences with separate bundles, not with folders or tags](../knowledge_management/separate_audiences_with_separate_bundles.md),
taken to its conclusion: if the audience boundary is the repository, then the repository is
where it has to be enforced.

## Where it came from

[Federating my knowledge base as privacy-tiered OKF bundles](../decisions/federating_my_knowledge_base_as_privacy_tiered_okf_bundles.md)
is the decision, and
[Federated OKF knowledge bases: a workspace-manifest architecture](../research/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md)
is the architecture it settled on. The first implementation wrapped the `kb-*` skills from
[agent-knowledge](agent_knowledge.md) and was retired at twenty commits and a green test suite;
the format discipline and that project's own bundle survived, and are still read here as an
upstream source.

## What it deliberately does not do yet

There is no search command. The skill tells an agent to read the bundles with `rg` and its own
file tools, and the project keeps a journal line every time that is not good enough, so what
gets built next answers a recorded incident rather than a guess.

Composition is also ambient rather than pinned: the manifest points at whatever each bundle
currently is, and there is no reproducible "the whole knowledge base at commit X". That is
recorded as a choice in the decision above rather than discovered later as an oversight.
