---
title: Editing Conventions
---

How content is written here. This page is the authority; the pre-commit hooks and CI
enforce what can be checked mechanically, and the rest is convention.

Most of it follows from one fact: `docs/` is an
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle, so every Markdown file in it is a *concept* and carries frontmatter accordingly.

## Where a file goes

| Directory | Holds | Published |
| --- | --- | --- |
| `docs/` | The bundle. Concepts, one per idea | Yes |
| `about/` | Pages describing the site rather than carrying knowledge, like this one | Yes |
| `raw/` | Sources the knowledge is distilled from, never edited | No |

The bundle root holds concepts and nothing else. A page that describes the site cannot live
there, because the format admits no exceptions: every non-reserved Markdown file under
`docs/` is a concept. That is why this page sits in `about/`.

## Concepts

Every concept requires the fields listed in `docs/okf-floor.yaml`:

```yaml
---
type: Principle
title: A short, declarative title
description: A single sentence summarising the concept.
tags: [example]
status: stable
generated: { by: human:felix_schindler, at: 2026-09-07T10:00:00Z }
---
```

- `type` is free text describing what kind of thing this is: `Principle`, `Person`,
  `Decision`, `Reference`. Pick something self-explanatory.
- `status` is `draft`, `stable` or `deprecated`. Absent means stable.
- `generated.by` names whatever did the writing: `human:<name>` for a person,
  `<harness>/<model>` for an agent such as `opencode/claude-opus-5`, `process:<id>` for a
  job. A person's identifier is their name, matching their page under `people/`, never a
  GitHub handle, which belongs to one account on one forge rather than to a human.
- `generated.at` is an ISO 8601 timestamp. Dates elsewhere, in `stale_after` and
  `sources[].last_modified`, are plain `YYYY-MM-DD`.

**Never write `verified:`.** Its absence is how the format records that nobody has
confirmed the content. It is added by whoever checks a concept against its sources, never by
the author about their own work.

### Reserved pages

`docs/index.md` and `docs/log.md` are reserved by the format. Neither is a concept and
neither takes frontmatter, except that `index.md` carries `okf_version` because it sits at
the bundle root.

`index.md` groups concepts under `##` headings, one line each. Write the entry in **index
voice**: shorter than the concept's own `description`, tuned to being scanned in a list
rather than read alone. Copying the description across would store the same sentence twice,
and reads worse in both places.

The index also carries what no list can: a sentence saying what the bundle is for, a line
under each heading saying what that section holds, and an order that follows how the ideas
build rather than the alphabet.

`log.md` records changes newest first, under a `## YYYY-MM-DD` heading per day. When adding
to the log, find today's heading or create one at the top; do not append at the bottom.

**A concept never links into `about/`.** The bundle has to make sense on its own, so it may
not depend on the pages that describe the site around it. Links run the other way.

## Page structure

Start the frontmatter on the first line, and start the body at `##`.

Do not repeat the title as a heading. MkDocs renders the frontmatter `title` as the page
heading, so a body `# Title` produces a second one and stores the same string twice, where
the two can drift.

## File naming

Filenames are **lowercase**, with **underscores** between words and no whitespace:

```text
autofix_in_the_hook.md      ✓
Autofix In The Hook.md      ✗
autofix-in-the-hook.md      ✗
```

Underscores rather than hyphens because a double-click selects the whole name in an editor
or a terminal, where a hyphen breaks the selection. The often-repeated preference for
hyphens in URLs is search-engine folklore from a decade ago; Wikipedia has served
underscored addresses throughout.

## Links

Use relative Markdown links, and make sure they resolve:

```markdown
[link text](../topic/some-concept.md)
[section link](some-concept.md#a-heading)
```

Relative paths are the only form that works everywhere at once: in an editor, on the GitHub
web interface, and on the rendered site. They also survive a page moving, because MkDocs
rewrites them.

What to avoid:

- **Absolute paths** such as `/topic/some-concept.md`. The format permits them and even
  prefers them, but MkDocs leaves them untouched, so a moved target breaks in silence.
- **Wiki-links**, `[[page]]`. Not standard Markdown. The shipped
  [Obsidian settings](using_obsidian.md#what-is-shipped-in-the-repository) configure link
  autocomplete to produce Markdown instead.
- **Note embeds**, an exclamation mark followed by `[[file]]`. No standard Markdown
  equivalent, and rejected by the `no-obsidian-embeds` hook.

### Linking to something not written yet

Do not link at a file that does not exist. The site build fails on it, so a dangling link
breaks the deploy rather than leaving a helpful gap.

Write the stub instead, with `status: draft` and a description saying what it will contain.
The link then resolves, the gap shows up in the index and in search, and `rg 'status:
draft'` lists everything outstanding. Fill it in later and change `status` to `stable`.

## Assets

Images and diagrams live **beside the concept that references them**, named after it:

```text
some-concept.md
some-concept-diagram.png
```

Group several in a subdirectory named after the page:

```text
some-concept.md
some-concept/
    diagram-1.excalidraw
    diagram-2.excalidraw
```

A concept and its pictures move together and read together. The cost is that renaming a
concept means renaming its assets too.

## Excalidraw diagrams

Diagrams are stored as plain `.excalidraw` JSON, not the Obsidian-specific `.excalidraw.md`
wrapper. The `check-excalidraw-settings` hook and the shipped
[Obsidian plugin settings](using_obsidian.md) keep it that way.

Create them in Obsidian with the
[Excalidraw plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin), or on
[excalidraw.com](https://excalidraw.com) and save the file into the repository. Embed one
with `![](diagram.excalidraw)`; the [mkdocs-excalidraw](tech_stack.md) plugin renders it
client-side, in light or dark mode to match the reader.

**Do not commit SVG or PNG exports of a diagram.** Rendering happens from the source file.

## What enforces this

| Rule | Enforced by |
| --- | --- |
| The frontmatter fields above | `okf-concepts` hook, reading `docs/okf-floor.yaml` |
| Every concept reachable from an index | `okf-bundle`, on pull requests |
| Links resolve | `mkdocs build --strict`, and `linkspector` |
| Filenames, embeds, diagram format | The hooks named above |
| One top-level heading per page | `markdownlint-cli2` |

A rule no hook checks is still a rule. See
[the development environment](local_dev_environment.md#pre-commit-hooks) for running these
locally.
