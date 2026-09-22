---
type: Decision
title: Adopting ponytail without its always-on ruleset
description: Why ponytail's ladder went into my harness AGENTS.md whilst its plugin runs with the injection
  switched off, and why patching the agent plugin was never an option.
tags:
- decision
- agents
- ai-agents
- opencode
- ponytail
- dx
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-09-22T00:00:00Z'
---
[ponytail](../tools/ponytail_gebert.md) is a ruleset and a set of commands that push an agent to
reuse what exists before writing anything. I run [opencode](../tools/opencode.md) with the
`oh-my-openagent` plugin, whose own prompt already argues for small changes. This is how I mean
to take the half that adds something.

## What I wanted

**The agent checks this codebase, the standard library and what is already installed, in that
order, before it writes a line.**

That ordering is ponytail's contribution. My existing prompt asks for the smallest correct
change and leaves the agent to decide what small means, which is a different instruction.

## What I care about

[Route a rule to the layer that reaches whoever must obey it](../principles/route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md).
A rule arrives somewhere or it does not, and which copy is authoritative follows from reach.

## What that led me to

**Patching the agent plugin is not a layer.** It resolves as `@latest` into a cache directory,
as a 5.7MB bundled artefact. An edit there survives until the tag moves, then disappears without
failing. Owning a fork would mean an upstream merge forever, for seven lines of prose.

The ladder is an instruction, so it belongs where my instructions already live. My harness
`AGENTS.md` is loaded into every session whatever plugins are active, it is mine, and the plugin
prompt ranks user instructions above its own defaults. A rule written there is stronger than one
patched into the bundle, not weaker.

The commands are not prose and cannot go there, so the plugin goes in with its injection
off. Its `config` hook still registers the commands and its skills directory; the hook that
appends to the system prompt reads the mode and returns.

## What I will build

| Half | Where | Why there |
| --- | --- | --- |
| The middle rungs of the ladder | the writing-adjacent section of my harness `AGENTS.md` | reaches every session, survives plugin updates |
| `/ponytail-review`, `-audit`, `-debt` | the npm plugin, with `PONYTAIL_DEFAULT_MODE=off` | pull-based, so they cost nothing unused |

This is the same split I made for
[caveman](adopting_caveman_at_lite_without_its_init_block.md), and for the same reason:
the always-on part of a skill collides with the block already in that file, whilst the tooling
does not.

## What I am leaving out, and would reconsider

**The first and sixth rungs are not adopted.** I am leaving out the YAGNI framing, which I
already have, and the one-line rung, which is where the tension with test and error-handling work
sits.

**I have not measured whether the ladder changes anything.** Its author's own benchmark says the
gain is near zero on code that is already minimal, and my prompt already pushes that way. A month
of use decides this, not the number on the repository.

**The injection would not have been scopeable anyway.** On Claude Code and Codex a regular
expression picks which subagents receive the ruleset; the opencode plugin appends unconditionally,
so a read-only search agent would be told to write one line. That made the decision easier than it
would otherwise have been.
