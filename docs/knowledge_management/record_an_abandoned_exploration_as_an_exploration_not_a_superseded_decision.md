---
type: Practice
title: Record an abandoned exploration as an exploration, not a superseded decision
description: A commitment you made and then withdrew is a finished piece of work, not a stale page;
  filing it as a deprecated decision loses the knowledge it produced.
tags:
- knowledge-management
- taxonomy
- documentation
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-10T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-10T10:08:05Z'
---
You adopt a tool, build on it for a while, learn why it does not fit, and move
to something else. The decision record you wrote at the time now asserts
something untrue. There are three obvious things to do with it and two of them
are wrong.

**Deleting it** throws away the only account of why the alternative was chosen,
which is the most expensive knowledge the episode produced. **Marking it
`deprecated`** is closer but still misreports what happened: `deprecated` says
the page has gone stale and should not be relied on. The page has not gone
stale. The work it describes ran to completion and returned a verdict. It is
*finished*, which is a different thing, and its verdict is precisely what a
reader wants.

**Rewrite it as an exploration**, in its own layer, with a shape that admits the
ending:

- **What I was after**, unchanged from the original record. The wishes usually
  survive the tool.
- **What I tried**, in enough detail that a reader can tell whether their own
  situation resembles yours.
- **Why I stopped**, one section per reason, each linked to the evidence that
  established it.
- **What I kept.** Normally the longest section, and the reason the page exists
  at all.
- **What I gave up**, so that a capability lost is lost knowingly.

Then `status: stable` is honest. A finished exploration is as settled as a page
gets.

## Why it needs its own layer rather than a tag

The [derivation pipeline](layer_build_knowledge_as_a_values_to_blueprints_derivation_pipeline.md)
places knowledge by the nature of its justification. A decision's justification
is *"given those values, wishes and principles, this was the best option"*, in
the present tense, and a reader is entitled to assume that a decision record
describes something you still stand behind. An exploration's justification is
*"because I built it and found out"*, in the past tense. Those are different
claims about the world, and a status field on a page whose header says
**Decision** cannot carry the difference: the reader has already accepted the
frame by the time they reach it.

Research is the nearer neighbour, and still not the same thing. Research is
evidence gathered without committing; an exploration is a commitment made and
then withdrawn. The distinction is worth keeping because it tells the reader how
much weight the findings carry. Somebody who read the documentation and somebody
who ran the thing for a month know different amounts.

## The tell that you have one

You are hesitating over whether a page is a decision or research, and the reason
is that you *did* decide, and it *is* no longer true. That hesitation is the
exploration layer asking to exist.
