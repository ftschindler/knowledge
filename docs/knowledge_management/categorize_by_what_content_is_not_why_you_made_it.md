---
type: Practice
title: Categorize by what content is, not why you made it
description: File a note by what it fundamentally is, not by the activity that happened to produce it;
  the context that produced it belongs in links.
tags:
- categorization
- information-architecture
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
While setting up this bundle, two findings - a security review of `agent-wiki`
and a bug hit while ingesting into it - both got filed under
`knowledge_management`. That was wrong: neither is *about* managing
knowledge. They landed there because **that is what I happened to be doing**
when I found them, not because of what they actually are.

Corrected:
[Security Analysis of Agent Wiki (awiki)](../research/security_analysis_of_agent_wiki_awiki.md)
is a security review, so it belongs in `research`.
[awiki title extraction breaks on frontmatter-led source files](../tools/awiki_title_extraction_breaks_on_frontmatter_led_source_files.md)
is a verified tool defect with a workaround, so it belongs in `tools`. Both
stand on their own merits as durable, hard-won knowledge. Neither needed the
knowledge-management framing to justify existing.

## The rule

**Directory = what the content fundamentally is. Links = why it exists, and the
context that produced it.**

Do not let the circumstance of discovery leak into the category. If you are
mid-way through building or adopting a tool and learn something, ask "what *is*
this, independent of what I was doing" before filing it. If the answer is "a
research finding", "a tool fix" or "a technique", it goes in the directory that
matches that nature, tagged for findability. The narrative of *why* you were
looking gets its own page and links out to the substantive findings, rather than
absorbing them: here that page is
[Running this knowledge base on awiki](../explorations/running_this_knowledge_base_on_awiki.md),
which is where both findings above are cited as evidence, and where neither of
them lives.

This generalises past awiki: any knowledge base with fixed-ish categories
(directories, topics, notebooks) is vulnerable to the same drift, since "what was
I doing" is always the most available and least correct classification signal in
the moment of saving.
