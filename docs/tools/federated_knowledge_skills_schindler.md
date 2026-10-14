---
type: Tool
title: federated-knowledge-skills (Felix Schindler)
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
  last_modified: '2026-10-14'
- id: fks-design
  resource: https://github.com/ftschindler/federated-knowledge-skills/blob/main/DESIGN.md
  title: 'federated-knowledge-skills: DESIGN.md'
  author: human:felix_schindler
  last_modified: '2026-10-14'
---
federated-knowledge-skills[^fks-readme] is the layer that turns several independent
[OKF](../investigations/open_knowledge_format_okf_findings.md) bundles into one federation an agent
can use: a skill it reads, a CLI it runs, and two pre-commit hooks each bundle pins for
itself. It is mine, and it is the tooling this bundle is now written through, so it appears
here in the same two roles that [agent-knowledge](agent_knowledge_stjbrown.md) does: a tool with a page,
and the thing producing the pages.

| | |
| --- | --- |
| Author | [Felix Schindler](../people/felix_schindler.md) |
| Licence | MIT, with the vendored OKF validator under its own |
| Language | Python 3.11+, run through [uv](uv.md) as PEP 723 scripts with no install step |
| Distribution | A kit `akit` subscribes to, or a skill directory to copy; plus two pre-commit hook ids a bundle pins by revision |
| Source | [github.com/ftschindler/federated-knowledge-skills](https://github.com/ftschindler/federated-knowledge-skills) |
| Status | Released at v0.3.0 and in daily use since September, across four bundles at three privacy tiers |

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
  whether it holds up, `url` for a link into another bundle, `sync` for moving a shared
  bundle's commits, and `init`, `add` and `migrate` for setting one up and keeping it current.

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
edits, which is the property [agent-wiki](agent_wiki_tacotakumi.md) traded away for a CLI that could hold
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

## A bundle several people file into

A bundle names the branch it is shared on, and that one field means three things: this
checkout belongs there, commits here may leave the machine, and somebody else is writing here
so it has to be read fresh. `fkb sync` fetches, rebases and pushes, and refuses rather than
resolving: uncommitted work in the tree, a checkout on another branch or a conflict all leave
the commit standing and nothing pushed.

The branch shape around it is
[Sharing one knowledge bundle on two branches](../blueprints/sharing_one_knowledge_bundle_on_two_branches.md),
which this bundle and one shared with an employer's team both run. The one piece the project
ships rather than documents is the merge back, as a reusable workflow, because it is the only
part of the shape whose absence nobody sees.

## How an upgrade reaches a setup

The skill is installed by copying, so a new release arrives without announcement. `fkb list`
compares the copy on disk against the version recorded in the workspace manifest and says when
something since then wants a decision; `fkb migrate` names the guides and `fkb migrate --done`
records them. Nothing is blocked in the meantime, which is
[the point of the stamp](../principles/a_version_stamp_is_bookkeeping_about_capabilities_not_a_lock.md).

The rule that makes a session reach for the skill at all ships beside it rather than inside
it, and [akit](federated_agent_kits_schindler.md) carries both under one name. A skill nothing
points at is never loaded, and nothing appears to go wrong when that happens.

## Where it came from

[Federating my knowledge base as privacy-tiered OKF bundles](../decisions/federating_my_knowledge_base_as_privacy_tiered_okf_bundles.md)
is the decision, and
[Federated OKF knowledge bases: a workspace-manifest architecture](../investigations/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md)
is the architecture it settled on. The first implementation wrapped the `kb-*` skills from
[agent-knowledge](agent_knowledge_stjbrown.md) and was retired at twenty commits and a green test suite;
the format discipline and that project's own bundle survived, and are still read here as an
upstream source.

## What it deliberately does not do yet

There is no search command. The skill tells an agent to read the bundles with `rg` and its own
file tools, and the project keeps a journal line every time that is not good enough, so what
gets built next answers a recorded incident rather than a guess.

Composition is also ambient rather than pinned: the manifest points at whatever each bundle
currently is, and there is no reproducible "the whole knowledge base at commit X". That is
recorded as a choice in the decision above rather than discovered later as an oversight.
