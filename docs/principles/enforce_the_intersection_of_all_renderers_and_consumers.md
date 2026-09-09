---
type: Principle
title: Enforce the intersection of all renderers and consumers
description: When several tools process the same content, restrict it to the feature set all of them support,
  not any one tool's superset.
tags:
- principle
- software
- linting
- markdown
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** When the same content is processed by several tools, restrict it to
the feature set *all* of them support - the intersection, not any one tool's
superset.

**When to apply.** Content consumed by multiple engines (Markdown across a site
generator + editor + linters; SQL across dialects; config across parsers). Not
relevant for single-consumer content.

**Why.** A feature that renders beautifully in one tool but breaks in another
produces content that looks fine where you authored it and silently degrades
elsewhere - a class of bug you won't see until a reader hits the wrong renderer.
Constraining to the common subset guarantees uniform behaviour everywhere. When
a tool tempts you outside the intersection, block that construct at commit-time
rather than relying on memory.

**Snippet.**

```text
Markdown must work across MkDocs, Obsidian, markdownlint-cli2 and pymarkdown.
If a feature isn't supported by all four, add a hook forbidding it
(e.g. no-obsidian-embeds) and document the exception.
```

**How enforced.** Run *multiple* linters covering each consumer (here
markdownlint-cli2 **and** pymarkdown), plus targeted footgun guards - an
application of [Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md).
