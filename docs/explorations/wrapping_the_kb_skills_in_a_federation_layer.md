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
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-09-14T00:00:00Z'
---
**A stub.** The work happened and was retired; this page is the account of it, and is not
written yet. What it needs to cover:

- **What I wanted.** A federation layer over
  [the `kb-*` skills](../tools/agent_knowledge.md) that reimplemented nothing: the upstream
  skills vendored unmodified as the single-bundle mechanic, a thin layer above them owning
  only the manifest-aware concerns. The architecture is
  [Federated OKF knowledge bases](../research/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md),
  whose skill-layer section this design originally filled.
- **What I built.** Roughly twenty commits and fifty-six passing tests, so this was not
  abandoned at the sketch stage. Worth saying what actually worked.
- **Why I stopped.** A federated skill invoked its single-bundle counterpart and then
  executed the prose that came back, which is control flow through prompt obedience rather
  than through a call. The `SKILL.md` accumulated three shouted warnings against an
  indirection the design had introduced itself, which is the tell worth recording: a
  document arguing with its own architecture.
- **The second reason, which is structural.** Skills have no dependency resolution.
  `npx skills add` copies a directory and verifies nothing, so a layer that requires another
  skill cannot state that requirement anywhere a machine will check. The `kb-*` skills were
  not installed on the machine whilst the global `AGENTS.md` advertised the layer above them.
- **What I kept.** The manifest, the `referenceable_by` rule, fail-closed defaults, the
  commit-time leak guard, and the rule that replaced the delegation: a skill may run a
  command; a skill never invokes another skill. Also the upstream bundle itself, which is
  now a read-only source here rather than a dependency.
