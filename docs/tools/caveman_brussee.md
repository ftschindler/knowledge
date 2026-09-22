---
type: Tool
title: caveman (Julius Brussee)
description: An MIT-licensed skill that compresses agent replies by cutting filler and tool-call narration,
  and the four commercial token-reduction layers sold alongside it.
tags:
- tools
- caveman
- agent-skills
- ai-agents
- writing
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
sources:
- id: caveman-repo
  resource: https://github.com/JuliusBrussee/caveman
  title: 'JuliusBrussee/caveman: ultra-compressed communication mode for coding agents'
  last_modified: '2026-09-21'
- id: caveman-site
  resource: https://caveman.so/
  title: Caveman - the token-efficient stack for agent-native development
  last_modified: '2026-09-21'
---
Caveman[^caveman-repo] is a skill that tells an agent to answer in fewer words: drop filler and
hedging, drop the narration around tool calls, and answer in the shape
`[thing] [action] [reason]. [next step].` It is one `SKILL.md` and nothing else, and it is the
free layer of a commercial stack[^caveman-site].

| | |
| --- | --- |
| Author | Julius Brussee |
| Licence | MIT, for the skill |
| Distribution | `npx -y github:JuliusBrussee/caveman`, or the vendored `install.sh` |
| Source | [github.com/JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) |
| Site | [caveman.so](https://caveman.so) |
| Version read | commit `ae26f3a`, 2026-09-21 |

## What is actually being offered

Five layers share the name, and only the first is prose. The skill is MIT-licensed and local. The proxy
and middleware below it compress context on its way to a provider and keep the original for
recovery. The platform and enterprise layers above are a gateway with caching, routing and a
signed savings ledger, both still in development.

Everything except the skill is about spending less money. **The skill is the only layer that
changes what a reader sees**, and it is installable on its own, with no account.

## The part worth having

The skill defines graded levels. `lite` cuts filler, hedging and pleasantries whilst keeping
articles and full sentences. `full` additionally drops articles and allows fragments, which is
the register the name promises. `ultra` strips conjunctions on top of that. Three further
levels answer in classical Chinese.

Two of its rules are about reading rather than counting, and they are where the value is. It
mixes in ASD-STE100 Simplified Technical English, the aerospace documentation standard: one
idea per sentence, twenty words, active voice, one term per concept, imperatives for
instructions. And it forbids narrating tool calls, which is where an agent's reply length
mostly comes from.

It also argues against its own folklore, which is the most interesting thing in the file.
Invented abbreviations such as `cfg` and `impl` tokenise the same as the full word, so they
save nothing and cost the reader a decode. Causal arrows are their own token. Mangled verb
agreement is the same length as correct agreement. The instruction that follows is to use plain
phrasing wherever caveman phrasing is not shorter, which makes `full` and `ultra` a smaller
change than they appear.

Compression is suspended for security warnings, confirmations of irreversible actions, and
anywhere terseness would make an order of operations ambiguous. It applies to replies only:
code, comments, commits, documentation and anything written for another human stay in ordinary
prose.

## Installing it

The installer recognises around a dozen harnesses and writes each one its native form, with
[opencode](opencode.md) amongst them; `--with-init` additionally drops an always-on rule body
into `AGENTS.md` and the per-agent rule directories. For Claude Code it also installs hook
scripts that track the active level and render it into the statusline, which is the only place
the level survives being pushed out of context.

Installing the skill by hand is a copy of one file, because a skill is discovered by its
`SKILL.md` rather than declared, the same property
[the skills installer](skills_vercel_labs.md) is built on.

## What I took

I copied the file into my own skills directory rather than running the installer, and changed
three things. The default level is `lite` rather than `full`, so asking for it gets tight prose
instead of dropped articles. Article-dropping moved out of the baseline rules into `full` and
above, where upstream applies it at every level including the one whose description promises
full sentences. The classical Chinese levels are gone.

The always-on part went into my `AGENTS.md` by hand, as three rules: fire tools without
narrating them, skip the opening acknowledgement, do not recap what was just said. Running
`--with-init` would have appended a second style block beside the one already there, and the two
disagree about register.

That disagreement is the thing to decide before installing. This bundle's voice is
[calm and settled](../principles/write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md)
and [paced one idea at a time](../principles/hand_the_reader_one_idea_at_a_time.md); caveman at
`full` is neither, because it is optimising for a different quantity. The overlap is real but
partial: both want the filler gone, and only one of them wants the grammar gone with it.

## On the headline number

The site's claim is 65% fewer output tokens, measured across ten prompts, with code, commands
and errors byte-for-byte exact. It is an output-token measurement and says nothing about
whether the shorter answers were easier to read, which is the axis that matters if the bill is
not what you are trying to reduce.
