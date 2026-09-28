---
type: Finding
title: pymarkdown's fix mode dedents YAML frontmatter
description: With the front-matter extension disabled, pymarkdown reads a concept's frontmatter as a
  thematic break and a paragraph, and fix mode strips the indentation off every nested key.
tags:
- finding
- pymarkdown
- markdown
- frontmatter
- pre-commit
- configuration
status: stable
stale_after: '2027-03-28'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
---
A file whose frontmatter carries a nested mapping comes back from a `pymarkdown fix` run with the
nesting gone:

```yaml
generated:
by: opencode/claude-opus-5
at: '2026-09-28T00:00:00Z'
```

The YAML still parses, which is what makes this expensive. It parses to three sibling keys and a
`generated` of `null`, so whatever consumes the frontmatter sees the field as absent rather than
malformed, and nothing upstream of the renderer complains.

## What it is

pymarkdown's front-matter extension is **disabled by default**, and an extension that is off is
off for parsing, not merely for linting. Without it, the opening `---` is an ordinary thematic
break and everything under it is an ordinary paragraph. In CommonMark, leading whitespace on a
paragraph's continuation lines is insignificant, so fix mode is within its rights to normalise it
away, and does.

markdownlint-cli2 handles frontmatter by default, which is why a repository running both hooks
sees only one of them do this, and why the reflex is to suspect the rule set rather than the
parser.

## How to get past it

Enable the extension in `.pymarkdown.json`:

```json
{
    "extensions": {
        "front-matter": {
            "enabled": true
        }
    }
}
```

Two things about that file are worth checking at the same time, because a configuration that has
this bug tends to have them too.

**`extensions` and `plugins` are objects, not arrays.** Written as `[]` they are accepted, and
nothing is configured.

**There is no top-level `config` key.** Rule settings go under `plugins`. A block of rule
configuration parked under `config:` is read by nothing, reported by nothing, and leaves every
rule at its default while looking deliberate.

The failing and working cases differ by one flag, which makes this quick to confirm on a scratch
file before touching the repository:

```bash
pymarkdown --set 'extensions.front-matter.enabled=$!True' -c .pymarkdown.json fix a.md
```

Enabling the extension changes what the parser sees, not just what it reports: the block that was
a thematic break plus a paragraph becomes frontmatter, so heading rules such as MD001 now measure
the body alone. Expect the first scan after the change to have something to say, and read it as
the rule finally seeing the document rather than as a regression.
