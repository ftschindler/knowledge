---
type: Finding
title: awiki title extraction breaks on frontmatter-led source files
description: awiki's plain-file ingest derives a page title from the first line, so a file that leads
  with YAML frontmatter gets a nonsense title.
tags:
- agent-wiki
- bug
- frontmatter
- markdown
- ingest
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
Found while ingesting a page from [Security Analysis of Agent Wiki (awiki)](../research/security_analysis_of_agent_wiki_awiki.md)
into this vault - noted here as a standalone tool gotcha.

**Version**: agent-wiki-kb `0.8.1` - verified against the installed source at
`agent_wiki/ingest.py`. May be fixed in a later release; re-check before
relying on this if you're on a newer version.

## The bug

`awiki`'s plain-file ingest path extracts a page's title with:

```python
match = re.match(r"^#\s+(.+)$", content, re.MULTILINE)
```

`re.match` only tries the pattern **at position 0 of the whole string** - per
the Python docs, *"even in MULTILINE mode, `re.match()` will only match at the
beginning of the string and not at the beginning of each line."* So if the
source file starts with a YAML frontmatter block (`---\ntitle: ...\n---`), the
first character is `-`, not `#`, and the regex never matches - **no matter
where a `# Heading` sits later in the file.** Title extraction silently falls
back to the filename stem, producing an ugly slugified title (and page path)
that has nothing to do with the content.

This is inconsistent with awiki's own **URL-ingest** path, which uses a
different helper (`_first_h1`, built on `re.search`) that correctly scans the
whole string - so `awiki ingest <url>` handles a leading frontmatter block
fine, while `awiki ingest <file>` does not.

## The second symptom

If you then add an `# H1` *underneath* the existing frontmatter block (a
reasonable first fix attempt, since most frontmatter-aware tools strip the
leading `---...---` before scanning for a heading), it does not help - same
`re.match` limitation - **and** the source's own untouched frontmatter block
ends up duplicated as stray, unparsed literal text at the top of the rendered
page body, since only the *page's own* regenerated frontmatter is treated
specially; anything else the raw file contains is just body content.

## Who this bites

Any source authored under a convention where the **title lives in YAML
frontmatter and the body has no literal `# H1`** - for example a site built
with MkDocs Material, where the theme renders the frontmatter `title:` as the
page heading automatically and the content deliberately starts at `##`. Such
a file ingests into awiki with a garbage title every time, silently.

## The fix

Before ingesting such a file, edit it (or a scratch copy) so the **first line
is the literal `# Heading`**, with no frontmatter above it:

- Strip the source's `---title: ...---` block entirely (safe if the title is
  already duplicated in the H1, or you don't need the original frontmatter
  preserved in the vault's `raw/` archive), **or**
- write a standalone copy for ingest that leads with the H1.

If you've already ingested with the wrong title, fix the vault's `raw/<name>`
copy the same way, then `awiki reingest <name>`. Note this **changes the
page's slug** (the path is derived from the title), so the page moves -
expected, not a bug, per `reingest`'s own H1-stability warning.

## Takeaway

Diff the source's title-convention against awiki's rule (*"first `# heading`,
or derived from the filename"*, per the CLI help and skill docs) **before**
running `awiki ingest`, rather than discovering the mismatch afterward in
search results. This is a systemic clash for any frontmatter-title-only
authoring convention (MkDocs, Obsidian setups that rely on the frontmatter
title), not a one-off.
