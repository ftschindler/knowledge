# GitHub Copilot Instructions

This repository is a knowledge base: concepts in plain Markdown, published as a MkDocs site
and editable as an Obsidian vault or directly on GitHub.

**[about/editing_conventions.md](../about/editing_conventions.md) is the authority on how
content is written here.** Read it before adding or changing content. What follows is the
short version, not a substitute.

## Where a file goes

`docs/` is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle, so every Markdown file in it is a concept and carries frontmatter accordingly. Pages
describing the site live in `about/`. Sources the knowledge is distilled from live in `raw/`
and are never edited.

`docs/index.md` and `docs/log.md` are reserved by the format. Neither is a concept, and
neither takes frontmatter.

## The four rules worth stating twice

- **Every concept carries the fields in [docs/okf-floor.yaml](../docs/okf-floor.yaml).**
  Nothing else is required, and nothing else is enforced.
- **Never write `verified:`.** Its absence is how the format records that nobody has
  confirmed the content. It is added by whoever confirms it, never by the author.
- **Links are relative and must resolve.** To promise a page that does not exist yet, write
  it as a stub with `status: draft` rather than linking at nothing; a dangling link fails the
  site build.
- **Do not repeat the title as a heading.** The frontmatter `title` is rendered as the page
  heading, so start the body at `##`.

## Language

- British English throughout: "ise" endings, "our" endings, "whilst" rather than "while",
  no Oxford comma.
- Write for a technical reader. Prefer the concrete behaviour over its abstract label.
- Cross-reference related concepts by linking them, so the bundle stays connected rather
  than becoming a pile of pages.

## Before committing

Run `prek` and respect what it reports; the same hooks run in CI. They check the frontmatter
fields, that every concept is reachable from an index, that links resolve, and the file
naming and Markdown rules. See [Local Dev Environment](../about/local_dev_environment.md)
and in particular [.pre-commit-config.yaml](../.pre-commit-config.yaml).
