---
type: Decision
title: Teaching my agents to write like me
description: How the three prose principles became a commit hook, a portable skill and an always-on digest,
  and why each copy lives where it does.
tags:
- decision
- writing
- agents
- documentation
- pkb
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
---
Three pages in this bundle say how prose here should read:
[Write in a calm, quantified, settled-fact voice - not a promotional one](../principles/write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md),
[Name the concrete behaviour, not its abstract label](../principles/name_the_concrete_behaviour_not_its_abstract_label.md)
and [Hand the reader one idea at a time](../principles/hand_the_reader_one_idea_at_a_time.md).
They were convention, and read only by an agent that happened to open them. This
decision is what made them arrive on their own.

## What I wanted

**Agents write in my voice everywhere, and I maintain the rules once.**

Everywhere means more than this repository. It means a chat reply, a commit
message, an email, and a project that has nothing to do with knowledge
management. The rules had reached only the bundles, and only when something
thought to read the conventions page.

Once means what it says. Before this, the pace rules existed twice, as
[the principle page](../principles/hand_the_reader_one_idea_at_a_time.md) and as a
copy inlined in my harness configuration, and the observation that warmth is the
cheapest register to fake existed twice more, copied into conventions pages with
no definitional home at all.

## What I care about

[Plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md),
which is why the answer here is markdown and a script rather than a service.

[Guarding invariants at commit time](../principles/guard_invariants_at_commit_time_not_review_time.md),
because a rule a reviewer must remember is a rule that gets forgotten.

And [one definitional home](../principles/give_every_cross_cutting_concept_one_definitional_home.md)
per concept, which is the requirement the whole problem turns on: the rules must
arrive in four places without being written in four places.

## What that led me to

**The audience decides the layer.** A human contributor never loads a skill, so
the only things that reach them are a page and a commit hook. An agent never
reads a page it was not pointed at, so the only thing that reaches it is an
instruction. The same sentence about the word `powerful` therefore has to exist
at several layers, and which copy is authoritative follows from reach rather
than from content. That is the reusable half of this decision, and it is written
up as
[Route a rule to the layer that reaches whoever must obey it](../principles/route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md).

The corollary is that a copy is acceptable when it carries imperatives and
refuses to carry reasoning. The wiki argues, the skill instructs and links back,
the digest instructs. A contradiction between them then shows up as a
contradiction rather than passing quietly, because each layer names where its
authority sits.

I considered [Vale](https://vale.sh) first, and its `vale-ai-tells` package, which
is 111 rules for exactly these tells. I did not take it. Vale is a Go binary whose
rule packages are fetched over the network, and this repository already runs
`check_markdown_style.py` as a dependency-free
[PEP 723 script](../principles/use_pep_723_inline_script_metadata_for_zero_install_tooling_scripts.md)
doing the same class of work. The word list was still worth having, so it seeded
mine.

## What I built

Four layers, from the one that argues to the one that is always on.

| Layer | Where | Reaches |
| --- | --- | --- |
| The claim, with its reasoning | the three principle pages here | anyone who reads, whenever they read |
| The mechanical guard | the `prose-tells` hook in this repository | every contributor, human included |
| The full style, on demand | the `writing` skill in [`ftschindler/agents-skills`](https://github.com/ftschindler/agents-skills) | agents, in any harness, when loaded |
| The imperatives, always on | the writing section of my harness `AGENTS.md` | every reply I read |

The hook is `.scripts/check_prose_tells.py`, a sibling of the markdown style
check. It checks the hype adjectives, the throat-clearing openers, the
future-promise framing, the corpus tells such as `delve`, the *not just X, it is
Y* construction, and more than one exclamation mark in a page. Text inside code
fences, inline code, link targets and quotation marks is exempt, with the
open-quote state carried between lines, which is what lets the voice page print
its own table of slop without tripping the hook that enforces it.

**I calibrated the word list against this bundle before shipping it, and three
rules did not survive.** American spellings would have failed on the `Authorization`
header, the `kb-visualize` command and the page title
[Categorize by what content is, not why you made it](../knowledge_management/categorize_by_what_content_is_not_why_you_made_it.md),
whose rename cascades through every link to it. Requiring "whilst" would have failed
on the 17 uses of "while" already here, against 25 of "whilst". Forbidding `simply`
anywhere but at the start of a sentence would have failed on eight legitimate uses,
including a values page observing that the proprietary tool is sometimes better.
A hook that fires on everything guards nothing, so all three stayed convention.

## What I gave up, and would reconsider

**The judgement half is not enforced, and cannot be.** Whether a paragraph carries
one idea or three is the rule I break most, and no regex decides it. The hook says
so in its own docstring rather than implying a coverage it does not have.

**British English, the Oxford comma and "whilst" are convention only**, for the
calibration reasons above. Renaming that one page title would let the American
spelling check in, and it may be worth it later.

**The digest is a third copy**, and the layer most likely to drift, because it is
the one I will edit in a hurry. The mitigation is that it carries no reasoning, so
a drift is visible as a flat contradiction rather than as two arguments that no
longer agree.

**This covers only the bundles that want it.** A repository with its own house
style keeps it, and both the skill and the digest say that a repository naming a
style guide in its conventions wins over mine. The failure mode there is that my
style is absent rather than that the two fight, which is the right way round.
