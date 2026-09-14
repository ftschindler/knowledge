---
type: Principle
title: Write in a calm, quantified, settled-fact voice - not a promotional one
description: Technical prose reads like a maintainer narrating what the machine does as settled fact,
  not like a landing page selling the tool.
tags:
- principle
- software
- documentation
- writing
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Technical prose - especially anything an agent generates - should
read like a maintainer standing next to the reader, narrating what the machine
does as settled fact, volunteering the real costs, and handing the reader
actions. Not like a landing page selling the tool. This voice is directly
enforceable: it has recognisable tells on both sides.

**When to apply.** All READMEs, setup guides, reproducibility notes, and
agent-generated documentation. It is the target register for any prose that
should read like [a maintainer wrote it, not a marketer](../values/prefer_plain_text_tool_agnostic_formats.md).

**The voice, as rules.**

1. **Settled-fact present tense.** Narrate the tool's behaviour as fact, not
   future promise. *"This downloads Miniforge, installs it locally, creates the
   environment, and verifies all imports."* - one sentence, four verbs, no
   hedging. Not *"This will seamlessly set up your entire environment."*
2. **"We" for choices, never for hype.** Use first-person-plural for decisions
   the project made on the reader's behalf: *"We ship tests which...", "We
   recommend prek..."*. Never *"our powerful setup"*. In a walkthrough (as opposed
   to terse reference prose) "we" may also serve as a companionable teaching
   narrator guiding the reader through the task - *"We can also run individual
   test layers", "As we can only test the skills by driving an agent, these
   tests are more involved"*. That register is legitimate for
   [task-path guides](structure_docs_as_the_readers_task_path_lead_with_action_defer_rationale.md); the bar it must still clear is guiding, never
   selling.
3. **"You" only to hand over an action or expectation.** *"Each time you open a
   new shell:", "you will also need latexmk", "This should leave you with
   output/"*. Never to flatter.
4. **Honesty as courtesy, quantified.** Volunteer the inconvenient truth with
   numbers: *"regenerates similar data, though timings may differ", "required
   around 52GB and 150h on our hardware"*. `similar`, not `identical`; the real
   cost, not *"up and running in no time"*.
5. **Hedges map to real variance.** `similar`, `around`, `roughly` are precise
   admissions of a stochastic process - not nervous filler like *"this may or
   may not potentially"*.
6. **Asides go in parentheticals and blockquotes; the main line stays clean.**
   The happy path is the prose; cost, caveats, and escape hatches live in `>`
   notes and `(...)`.
7. **No throat-clearing.** No sentence opens with *"In order to", "It is
   important to note that", "As you can see", "Simply", "Just"*. Open with the
   subject and move.
8. **Earn every exclamation mark.** At most one, on the genuinely surprising
   fact (*"150h of time on our target hardware!"*), never as perkiness.

**Why.** This is the negative image of default LLM prose, which is the whole
point: an agent told "write docs" reaches for *"This powerful setup script
seamlessly handles everything, ensuring a smooth experience - simply run the
command and you'll be up and running in no time!"*. That register is
untrustworthy precisely because it hides cost and overstates certainty. The
maintainer voice is enjoyable to read *because* it respects the reader - it
states what happens, admits what varies, and never sells.

**Snippet (slop → voice).**

| Slop tell | Rewrite in this voice |
| --- | --- |
| "This will seamlessly set up your entire environment." | "This downloads Miniforge, installs it locally, and verifies all imports." |
| "Simply run the command and you're good to go!" | "Each time you open a new shell: `source 01_activate_env.bash`." |
| "Our powerful test suite ensures everything works." | "We ship tests which run the code on a simplified setup and compare against expected results." |
| "You'll be up and running in no time." | "Running them required around 52GB and 150h on our target hardware." |
| "This produces identical results." | "This regenerates similar data, though timings and speedup may differ." |

**How enforced.** Convention plus a review pass over agent-generated prose:
grep for the tells (`seamless`, `powerful`, `simply`, `just`, `effortless`, "in
no time", "will ensure", future-promise framing, bare superlatives, more than
one `!`) and rewrite each hit toward settled-fact present tense with a quantified
cost. Derived from the companion-code READMEs of the 2026 pyMOR paper, whose
voice this page distils.
