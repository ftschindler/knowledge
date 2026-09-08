---
title: Tech Stack
---

This site is a git-backed static site built from Markdown files and
[Excalidraw](https://excalidraw.com) diagrams.

## Knowledge format

- **[Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
  (OKF) v0.2** - `docs/` is an OKF *bundle*, so every Markdown file in it is a *concept*
  carrying frontmatter, and `index.md` and `log.md` are reserved. Pages describing the site
  live in `about/`, outside the bundle, and sources it is distilled from live in `raw/`.
- **`docs/okf-floor.yaml`** - what this bundle requires of a concept beyond the format's one
  mandatory field, and the only thing that decides it. See
  [Editing Conventions](editing_conventions.md).

## Static site generator

- **[MkDocs](https://www.mkdocs.org/)** with
  **[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)** as the theme

## MkDocs plugins

- **[mkdocs-awesome-pages-plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin)** -
  flexible navigation ordering without maintaining a full nav tree
- **[mkdocs-excalidraw](https://github.com/qdeli187/mkdocs-excalidraw)** - client-side rendering
  of `.excalidraw` diagrams with automatic light/dark mode support
- **[mkdocs-obsidian-support-plugin](https://github.com/ndy2/mkdocs-obsidian-support-plugin)** -
  converts Obsidian callouts to Material admonitions
- **[mkdocs-backlinks-section-plugin](https://github.com/six-two/mkdocs-backlinks-section-plugin)**
  - automatic backlink sections
- **[mkdocs-glightbox](https://github.com/blueswen/mkdocs-glightbox)** - image lightbox support

## Build hook

`hooks/publish_about.py` reconciles the bundle with the site, without changing anything on
disk. It publishes `about/`, which sits outside the MkDocs source directory; gives the site
its landing page; moves the bundle's own index to `/index/` so that page can take the root;
and rewrites links from `about/` into the bundle, so a single spelling resolves both in an
editor and on the rendered site.

## Tooling

- **[uv](https://docs.astral.sh/uv/)** - Python toolchain (manages Python version and
  dependencies)
- **Git LFS** - large file storage for `.excalidraw` files
- **[Pre-commit](https://pre-commit.com/)** - enforces markdown quality, link integrity and
  repository hygiene (see [Editing Conventions](editing_conventions.md) and
  [Local Dev Environment](local_dev_environment.md) for setup)

## Conformance checking

- **[federated-knowledge-skills](https://github.com/ftschindler/federated-knowledge-skills)**
  - publishes the pre-commit hooks this repository pins by revision. `okf-concepts` checks
  format conformance and the declared floor on every commit; `okf-bundle` additionally
  checks that every concept is reachable from an index, and runs per pull request.
- Those hooks wrap the OKF reference validator rather than reimplementing it. Nothing here
  needs the wider tooling installed: the bundle checks itself, which is what lets it stand
  on its own.

## CI / CD

On push to `main`, a GitHub Actions workflow builds the site with
`uv run mkdocs build --strict` and deploys it to GitHub Pages.
