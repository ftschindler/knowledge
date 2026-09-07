# GitHub Copilot Instructions

This repository is a knowledge base: concepts in plain markdown, published as a MkDocs site
and editable as an Obsidian vault or directly on GitHub.

It is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle. `docs/` is the bundle root, so **every markdown file in it is a concept** and carries
frontmatter accordingly. Pages that describe the site rather than carry knowledge live in
`about/`, outside the bundle.

## General Guidelines

This site relies on an interplay of many tools, and we can only make use of the subset of
Markdown features supported by mkdocs, obsidian, markdownlint-cli2 and pymarkdown.
When creating new content, ensure to check if Markdown features work across all tools.
If not, add a corresponding pre-commit hook to prohibit addition and document the exception.

- Ensure to run `prek` and respect linting and formatting as defined in
  [.pre-commit-config.yaml](../.pre-commit-config.yaml).

## Content Guidelines

- When creating or editing content, prioritise creating a coherent, well-connected knowledge
  base whilst maintaining high standards of British English and technical accuracy.

### Language and Grammar

- Always use British English spelling and grammar conventions:
  - Use "ise" endings (e.g., "realise", "optimise", "organised")
  - Use "our" endings (e.g., "behaviour", "colour", "favour")
  - British punctuation (e.g., single quotes for emphasis, logical punctuation placement)
  - British terminology (e.g., "whilst" instead of "while", "amongst" instead of "among")
  - no Oxford Comma

### File Structure and Naming

- Concepts live in `docs/`, one file per idea, in a directory naming what the concept *is*
- Use lowercase filenames, words separated by hyphens (e.g., `some-concept.md`)
- Store assets like `image.jpg` required for an entry `foo.md` beside it, named after it
  (e.g., `foo-image.jpg`), so a concept and its pictures move together
- `index.md` and `log.md` are reserved by the format: an index of concepts and a dated
  update log. Neither is a concept and neither takes frontmatter, except that the bundle
  root `index.md` may carry `okf_version`

### Frontmatter Requirements

Every concept requires the fields listed in [docs/okf-floor.yaml](../docs/okf-floor.yaml):

```yaml
---
type: Principle
title: Your concept title
description: A single sentence summarising the concept.
tags: [example]
status: stable
generated: { by: <harness>/<model>, at: 2026-09-07T10:00:00Z }
---
```

- `generated.by` names what did the writing: `<harness>/<model>` for an agent,
  `human:<id>` for a person, `process:<id>` for a job
- Never write `verified:`. Its absence records that nobody has confirmed the content, and it
  is added by whoever confirms it, never by the author
- Dates in `stale_after` and `sources[].last_modified` are written `YYYY-MM-DD`

### Internal Linking

- Always create meaningful cross-references to related content within the repository
- Use relative paths for internal links (e.g., `[some topic](../some-topic.md)`), never
  absolute ones: only relative links resolve in an editor, on the GitHub web UI and in the
  rendered site alike
- Link to relevant concepts, related proposals, supporting rationales and background
- Ensure links work correctly by checking the relative path structure
- When referencing concepts that have dedicated pages, always link to them

### Content Structure

- Do not repeat the title as a heading in the body. The `title` from the frontmatter is the
  page heading: MkDocs renders it as the `h1`, and repeating it stores the same string twice
  where the two can drift. Start the body at `##`
- Include a brief summary or introduction for substantial documents
- Use bullet points for lists and structured information

### Formatting Guidelines

- Use *italics* for emphasis of technical terms and concepts
- Use **bold** for strong emphasis and important action items
- Use `inline code` for file names and commands
- Use proper markdown syntax for lists, headings and links

### Technical Content

- Maintain consistency with existing technical terminology
- Reference specific technologies, tools and frameworks mentioned in other documents
- Ensure technical accuracy and alignment with team practices
- Include practical examples and implementation details where relevant

### Quality Standards

- All content should provide value
- Ensure information is current and actionable
- Write with the target audience in mind (technical professionals)
- Review content for clarity, completeness and usefulness
- Maintain consistency with existing content style and structure
