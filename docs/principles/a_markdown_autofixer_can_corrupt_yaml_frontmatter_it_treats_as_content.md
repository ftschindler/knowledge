---
type: Principle
title: A markdown autofixer can corrupt YAML frontmatter it treats as content
description: A markdown auto-fixer that does not recognise YAML frontmatter will reflow it as prose and
  silently break it.
tags:
- principle
- software
- pre-commit
- markdown
- frontmatter
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** Before enabling a markdown auto-fixer (pymarkdown, and others) on files
that carry YAML frontmatter, make it *recognise* the frontmatter block - otherwise
its `fix` mode reflows the leading `---` block as if it were prose and silently
breaks the YAML.

**Why.** Markdown linters that do not parse front-matter see the frontmatter as an
ordinary paragraph. A reflow/normalise fixer then rewrites it - most damagingly, it
strips the indentation of a `description: >-` (or `|`) block scalar down to column
0, which turns valid YAML into invalid YAML. The document still *looks* fine to a
skim, but any consumer that reads the frontmatter (a static-site generator, a skill
loader like `skills.sh` keying on `name`/`description`, an OKF ingester) now sees an
empty or unparseable field. The corruption is committed-in and easy to miss because
the markdown body is untouched.

The case that motivated this: pymarkdown's `fix` de-indented the `description: >-`
block scalar in several `SKILL.md` files to column 0, breaking `skills.sh`
discovery. A commit-time guard asserting `name`+`description` are present caught it
immediately - an instance of [Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md).

**How enforced.** Enable the fixer's front-matter extension so it skips the block:

```json
// .pymarkdown.json
{ "extensions": { "front-matter": { "enabled": true } } }
```

And keep a cheap guard that parses the frontmatter of the affected files and fails
if a required field is missing - the fixer's mistake then fails the commit instead
of shipping. A related concern when several fixers touch one file type is
[Order auto-fixers so later ones do not re-dirty earlier output](order_auto_fixers_so_later_ones_do_not_re_dirty_earlier_output.md); a distinct one
is that two linters over the same filetype can disagree on a rule (e.g. code-block
style MD046), so assign each rule a single owner and disable it in the other.
