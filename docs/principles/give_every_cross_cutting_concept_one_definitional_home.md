---
type: Principle
title: Give every cross-cutting concept one definitional home
description: A concept that surfaces in several places in a document is defined in exactly one section;
  every other mention references it.
tags:
- principle
- documentation
- writing
- dx
- structure
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** In any document longer than a screen, a concept that surfaces in
several places - a trust model, a security invariant, a naming convention -
must be *defined* in exactly one section; every other mention *references* that
home rather than restating it. This is the single-source-of-truth discipline
applied to prose. It operates at **document scope**, above the section-scope
rule that caveats get their own heading and the sentence-scope rule that asides
go in parentheticals
(see [Structure docs as the reader's task path - lead with action, defer rationale](structure_docs_as_the_readers_task_path_lead_with_action_defer_rationale.md)).

**When to apply.** READMEs, design docs, runbooks - any prose where one idea
legitimately threads through the getting-started, a field table, a diagram, and
the rationale. Not short single-purpose notes, where an idea appears once by
nature.

**The failure it prevents.** Following only local rules produces text that is
correct in isolation at every site and wrong in aggregate. A concept stated at
seven places - each a clean, honest, well-voiced sentence - forces the reader to
assemble the whole from fragments, and no single place can be pointed to as *the*
definition. Worse, a later sentence can say "the trust model" as if it were
already defined when it never was; the phrase orbits a center of gravity that
does not exist. The smear is the same anti-pattern good architecture avoids:
coupling spread across many sites instead of centralized in one.

**The rule.**

1. **Name the recurring concept.** Before finalizing, list the ideas that appear
   more than twice. Each is a candidate for a single home.
2. **Pick the definitional home.** Usually the first place the reader needs the
   *full* idea, not the first place it is merely touched. Give it a heading if it
   earns one.
3. **Demote every other mention to a reference.** Elsewhere, state only the
   local slice needed there, then link to the home (`see [trust
   model](#...)`). A field table names the field and its default; the *why* lives
   at the home. A diagram may label the concept; its definition does not travel
   with it.
4. **Check the back-references resolve.** Any sentence that says "the X" must
   follow, not precede, X's definition - or link forward to it. A named concept
   with no reachable definition is the tell that this rule was skipped.

**Why.** A reader looking for "how does this actually prevent leaks?" should
find one section that owns the answer, not seven partial answers to reconstruct.
One home also means one place to edit when the concept changes - the same
dividend centralizing coupling pays in code. Local structure rules make each
sentence and section walkable; this rule makes the *concept* findable across the
whole document.

**Snippet (smeared → homed).**

| Smeared (locally correct, globally scattered) | Homed (one definition, N references) |
| --- | --- |
| Trust model restated in getting-started, field table, two diagrams, and rationale | One `### Trust model` section; the table says "default `[]`", the diagram labels "read-all", both defer the *why* to the section |
| "The asymmetry is the trust model: you may learn from anything, but..." (re-derives it) | "This read-all/write-one split is the `[trust model](#...)` in action" (references it) |
| A caveat's honest limits buried in a `> Note` far from where the concept is defined | The limit lives *in* the concept's home section, under a "What this does not guarantee" line |

**How enforced.** After drafting, grep for each recurring concept's keywords;
if it is *explained* (not merely referenced) in more than one place, collapse
the extras into references to the chosen home. Confirm every `"the <concept>"`
phrase has a definition it can reach. Pairs with
[Structure docs as the reader's task path - lead with action, defer rationale](structure_docs_as_the_readers_task_path_lead_with_action_defer_rationale.md) (section/sentence
scope) and [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md) (anchors/links are what
make a single home referenceable). Earned rewriting a README that stated its
trust model seven times; consolidating to one section made a forward reference
that had pointed at nothing finally point at something.
