---
type: Tool
title: ponytail (Dietrich Gebert)
description: A skill that makes an agent climb a seven-rung ladder before writing code, so that reuse comes
  before writing and the smallest thing that works wins.
tags:
- tools
- ponytail
- agent-skills
- ai-agents
- opencode
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
sources:
- id: ponytail-repo
  resource: https://github.com/DietrichGebert/ponytail
  title: 'DietrichGebert/ponytail: Makes your AI agent think like the laziest senior dev in the room'
  last_modified: '2026-09-21'
- id: ponytail-benchmark
  resource: https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md
  title: Agentic benchmark, 2026-06-18
  last_modified: '2026-09-21'
---
ponytail[^ponytail-repo] is a ruleset that tells an agent to reach for the smallest thing that
already exists before it writes anything. It ships as a skill plus a per-harness plugin, and
covers around twenty agents, [opencode](opencode.md) amongst them.

| | |
| --- | --- |
| Author | Dietrich Gebert |
| Licence | MIT |
| Distribution | npm, as `@dietrichgebert/ponytail`, plus plugin marketplaces per harness |
| Source | [github.com/DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) |
| Version read | v4.10.0, commit `e3ba2aa`, 2026-09-21 |

## The ladder

The whole idea is one ordered list, and the agent stops at the first rung that holds: does this
need to exist at all, is it already in this codebase, does the standard library do it, is it a
native platform feature, is it in an installed dependency, does it fit on one line, and only
then write the minimum that works.

The ordering is the content. A generic instruction to keep things small leaves the agent to
decide what small means, whilst the ladder says which cheap option to exhaust first, and reuse
sits above writing on it. It runs *after* the agent has understood the problem, which is the
guard against the obvious failure mode: lazy about the solution, never about reading the code
the change touches.

Validation at trust boundaries, data-loss handling, security and accessibility are named as
never cuttable. That is what separates it from a prompt that just asks for fewer lines, and the
repository's own benchmark is where the difference shows.

## On the headline number

The claim is 54% less code, measured on a headless Claude Code session editing a real FastAPI
and React repository, twelve feature tickets, scored on the `git diff` left behind[^ponytail-benchmark].
The figure is a mean and the spread is the interesting part: 94% where the agent would otherwise
over-build, near zero where the code is already minimal. A "YAGNI plus one-liners" control prompt
got two thirds of the way there whilst dropping one safety guard.

The repository publishes an earlier 80-94% single-shot number and then retracts it in place, on
the grounds that the bare-model baseline pads its answers with prose and options, so the gap was
partly an artefact of comparing against conversation. Withdrawing your own best number and
leaving the reasoning up is worth more than the number was.

## What I have not taken

I read it against my [opencode](opencode.md) setup and did not install the always-on part. Two
reasons, both about what is already there.

The agent prompt I run already carries a scope section that says much the same thing, so the
genuinely new material is the middle of the ladder: check this codebase, then the standard
library, then what is already installed, in that order. That is a real addition, and it is
smaller than a ruleset injected into every turn of every session.

The other is that the opencode adapter has no way to scope the injection. On Claude Code and
Codex a regular expression decides which subagents get the ruleset; the opencode plugin appends
to the system prompt unconditionally, so a read-only search agent and an architecture
consultation receive "write one line" alongside everything else. That is the wrong instruction
for both.

What survives the objection is the pull-based half: `/ponytail-review` reads the current diff for
over-engineering and hands back a delete-list, `/ponytail-audit` does the same for a whole
repository, and `/ponytail-debt` collects the `ponytail:` shortcut comments into a ledger. Those
cost nothing when unused, which is the opposite trade from the ruleset.

It is the same shape of decision as [caveman](caveman_brussee.md), and the two are easy to
confuse because both make things shorter. They do not compress the same thing: caveman is about
the prose an agent writes back to me, ponytail is about the code it leaves in the repository.
ponytail's own benchmark uses caveman as the control arm for exactly that reason.
