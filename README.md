# Felix' knowledge base

A knowledge base of concepts in plain markdown, written to be read and maintained by both
people and agents.

It is an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format)
bundle, published as a [MkDocs](https://www.mkdocs.org) site and editable as an
[Obsidian](https://obsidian.md) vault, in any editor, or directly on GitHub.

## Layout

| | |
| --- | --- |
| `docs/` | The bundle. Every markdown file in it is a concept, with frontmatter to match |
| `docs/index.md`, `docs/log.md` | Reserved by the format: an index of concepts, and a dated update log |
| `docs/okf-floor.yaml` | What this bundle requires of a concept, beyond the format's single mandatory key |
| `about/` | Pages describing the site rather than carrying knowledge, kept outside the bundle |
| `hooks/` | A MkDocs build hook that publishes `about/` and gives the site its landing page |

## Working on it

```bash
make bootstrap   # install dependencies and the pre-commit hooks
make serve       # live-reloading dev server
make site        # build the static site into site/
```

## Licence

Two licences, because this repository holds two kinds of thing.

- **The knowledge** - everything except the directories below - is licensed under
  [CC BY 4.0](LICENSE). Use it, adapt it, build on it, including commercially; credit it.
- **The code** - `hooks/` and `.scripts/` - is licensed under [MIT](LICENSE-CODE). Creative
  Commons licences are not intended for software, and MIT keeps these files reusable in
  projects that expect an ordinary open-source licence.

These terms cover the concepts written here. Material reproduced from elsewhere - quoted
articles, mirrored sources, transcripts of third-party content - remains under whatever
terms it already carried, and is not relicensed by its presence in this repository.
