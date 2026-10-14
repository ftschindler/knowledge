---
type: Tool
title: federated-agent-kits (Felix Schindler)
description: The CLI that subscribes to skills and rules from ordinary git repositories and renders
  them into whatever file each agent harness reads.
tags:
- tools
- self-authored
- agents
- agent-skills
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T10:05:00Z'
sources:
- id: akit-readme
  resource: https://github.com/ftschindler/federated-agent-kits
  title: 'ftschindler/federated-agent-kits: README'
  author: human:felix_schindler
  last_modified: '2026-10-14'
---
`akit`[^akit-readme] fetches a skill or a rule from the git repository it lives in, pins the
commit, and writes the copy each harness expects. One line in a manifest replaces the several
hand-made copies that would otherwise sit in several files and drift apart. It is
[Felix](../people/felix_schindler.md)'s, and it is how the
[`fkb`](federated_knowledge_skills_schindler.md) skill and its rule reach this machine.

| | |
| --- | --- |
| Author | [Felix Schindler](../people/felix_schindler.md) |
| Licence | MIT |
| Language | Python 3.11+, published to PyPI and run without installing through [uv](uv.md) |
| Version | 0.12.1, alpha: the shape holds, the edges move |
| Platforms | Linux and Windows, both running the full suite in CI |
| Source | [github.com/ftschindler/federated-agent-kits](https://github.com/ftschindler/federated-agent-kits) |

## What it does

**A source is any git repository that keeps skills or rules in it.** It needs no manifest, no
registration and no permission, and it never learns that anyone subscribed. `akit` looks in
the places each ecosystem keeps these things, so a repository laid out normally needs nothing
doing to it.

**A kit is a name, and it may carry several kinds under it.** Subscribing to `fkb` takes both
the skill an agent opens and the rule that makes it reach for the skill at all, which is the
pairing that gets broken when the two are installed separately.

**A render writes into the region it owns**, between markers, in whichever shape each detected
harness wants: a skill directory for one, a block in an instructions file for another. What
the reader wrote themselves sits outside those markers and is left alone. `akit list` says
what is subscribed, which harnesses are on the machine, where each part landed, and whether
two kits collide on a name. It writes nothing.

Two manifests, so the same mechanism serves both audiences: `--global` for the subscriptions
that apply to every session, and a per-repository one for what only that project needs.

## Why it exists

The argument is
[Subscribe to shared instruction text rather than pasting a copy](../principles/subscribe_to_shared_instruction_text_rather_than_pasting_a_copy.md).
A block pasted by hand is one no later version can reach: the wording in the repository moves
on, the copy does not, and nothing reads both halves to notice.

`fkb` is the case that produced it. Its rule used to ship as a page saying "paste this into
your instructions file", which made every installed copy a fork. The rule now lives at
`rules/fkb.md` in that project and `akit` carries it, under the same name as the skill, so an
upgrade brings both.

## What it does not do

It installs nothing beyond what it writes, and it resolves no dependencies between kits: a
skill that needs another cannot say so anywhere a machine will check. Agent definitions, the
third kind, are still being built, and a subscription to one says which task it is waiting
for.
