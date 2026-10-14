---
type: Exploration
title: Wrapping the kb skills in a federation layer
description: The first federation layer put a skill in front of another skill, reached a green test
  suite, and was retired for making prose the control flow.
tags:
- exploration
- agent-knowledge
- agent-skills
- okf
- federation
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T10:30:00Z'
---
The first attempt at a federation layer was built on top of
[the `kb-*` skills](../tools/agent_knowledge_stjbrown.md) rather than beside them. It worked,
in the sense that the tests passed, and it was retired anyway. What replaced it is
[federated-knowledge-skills](../tools/federated_knowledge_skills_schindler.md).

## What it was meant to be

A layer that reimplemented nothing. The upstream skills would be vendored unmodified as the
single-bundle mechanic, and a thin layer above them would own only the concerns that need the
manifest: which bundles exist, which may be written to, which may cite which. The architecture
it was filling in is
[Federated OKF knowledge bases: a workspace-manifest architecture](../investigations/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md),
whose skill-layer section this design originally was.

Roughly twenty commits and fifty-six passing tests went into it, so what follows is not an
account of a sketch.

## Why it was retired

**A skill invoked another skill.** The federated skill told the agent to load its
single-bundle counterpart, and then to carry out the prose that came back. That is control
flow through prompt obedience: nothing calls anything, and whether the step happens depends on
how persuasive the paragraph was.

The tell was in the document rather than in the tests. `SKILL.md` had accumulated three
shouted warnings against an indirection the design itself had introduced, which is a document
arguing with its own architecture.

**The second reason is structural, and nothing in the design could have fixed it.** Skills
have no dependency resolution. A skill installer copies a directory and verifies nothing, so a
layer that requires another skill cannot state that requirement anywhere a machine will check.
The failure duly happened on a real machine: the `kb-*` skills were not installed whilst the
user-level instructions advertised the layer above them, and nothing reported it.
[akit](../tools/federated_agent_kits_schindler.md) later fixed how a skill and its rule travel
together, and still does not resolve a dependency between two skills, because there is nowhere
to declare one.

## What survived

The manifest, the `referenceable_by` rule, the fail-closed defaults and the commit-time leak
guard all went into the rewrite unchanged. So did the upstream bundle itself, which is now a
read-only source read here rather than a dependency anything runs.

And one rule, which is what the episode cost and what it bought: **a skill may run a command;
a skill never invokes another skill.**
