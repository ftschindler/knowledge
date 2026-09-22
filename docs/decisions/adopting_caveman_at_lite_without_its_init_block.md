---
type: Decision
title: Adopting caveman at lite, without its init block
description: Why the terseness skill went into my skills directory by hand with its default level lowered,
  and why the installer's always-on block would have contradicted the one already in my AGENTS.md.
tags:
- decision
- agents
- ai-agents
- writing
- caveman
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-22T00:00:00Z'
---
[caveman](../tools/caveman_brussee.md) is a skill that tells an agent to answer in fewer words.
Its free layer is one `SKILL.md`, and its installer also writes an always-on rule body into
`AGENTS.md`. I took the first and not the second.

## What I wanted

**Replies that have lost their filler, and kept their grammar.**

The part of an agent's reply I actually want gone is the narration around tool calls and the
opening acknowledgement. Dropped articles are a different thing, arrived at for a different
reason: they are there to spend fewer tokens, and I am not paying attention to that.

## What I care about

[Write in a calm, quantified, settled-fact voice](../principles/write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md)
and [Hand the reader one idea at a time](../principles/hand_the_reader_one_idea_at_a_time.md).
Both of those want full sentences, and a register that drops articles cannot deliver either.

[Route a rule to the layer that reaches whoever must obey it](../principles/route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md),
which decides where each half of the skill goes once the two halves turn out to want different
homes.

## What that led me to

**The skill and the always-on block reach different audiences, so they are not one thing to
install.** A skill is pulled in when a session asks for terseness. A rule body in `AGENTS.md`
is loaded into every session whether or not it is wanted, and mine already carries a writing
section that argues for the opposite register. `--with-init` would have appended a second style
block beside the first, and the two disagree.

**The upstream default is stronger than its own description promises.** `lite` is described as
keeping full sentences, whilst article-dropping sits in the baseline rules and therefore applies
at every level including that one. Lowering the default is not enough on its own; the rule has
to move.

## What I built

A hand-copied `SKILL.md`, changed in three places, and three sentences written into `AGENTS.md`
by hand rather than by the installer.

| Half | Where | What changed |
| --- | --- | --- |
| The skill | my own skills directory | default level `lite` rather than `full`; article-dropping moved out of the baseline into `full` and above; the classical Chinese levels dropped |
| The always-on part | the writing section of my harness `AGENTS.md` | three rules: fire tools without narrating them, skip the opening acknowledgement, do not recap what was just said |

Installing by hand is a copy of one file, because a skill is discovered by its `SKILL.md` rather
than declared.

## What I gave up, and would reconsider

**The statusline hooks, which only the installer writes.** For Claude Code they track the active
level and render it, and that is the only place the level survives being pushed out of context.
Copying one file means the level is whatever the skill was last told, and nothing shows me which.

**Whether the register question is settled.** The overlap between caveman and this bundle's
voice is real but partial: both want the filler gone, and only one of them wants the grammar
gone with it. At `lite` that collision does not arise, which is the reason `lite` is the
default rather than a considered view that `full` is wrong.

This is the same split as
[Adopting ponytail without its always-on ruleset](adopting_ponytail_without_its_always_on_ruleset.md),
made first and for the same reason.
