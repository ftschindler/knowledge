"""Render each concept's genre note from its directory's declaration.

Every concept opens with a note naming what kind of page it is and linking to
the index that defines the kind, because a reader arriving from search lands in
the middle of the bundle where nothing else says which genre they are reading.
The note is identical for every page in a directory, so it is declared once, in
that directory's `.genre.yaml`, and rendered here.

The declaration is also what `type` is checked against, by the `genre-conformance`
pre-commit hook, so the directory, the note and the frontmatter cannot disagree.
"""

from __future__ import annotations

from pathlib import Path

import yaml

GENRE_FILE = ".genre.yaml"
NOT_CONCEPTS = frozenset({"about", "stylesheets"})
RESERVED = frozenset({"index.md", "log.md"})

_declarations: dict[str, dict] = {}


def genre_of(src_uri: str, docs_dir: str) -> dict | None:
    """Return the genre declared for the concept at `src_uri`, if it is one."""
    parts = src_uri.split("/")
    if len(parts) != 2 or parts[0] in NOT_CONCEPTS or parts[1] in RESERVED:
        return None

    directory = parts[0]
    if directory not in _declarations:
        path = Path(docs_dir) / directory / GENRE_FILE
        if not path.is_file():
            raise FileNotFoundError(
                f"{src_uri}: no {path} - every concept directory declares its genre"
            )
        _declarations[directory] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return _declarations[directory]


def on_page_markdown(markdown, page, config, files):
    genre = genre_of(page.file.src_uri, config.docs_dir)
    if genre is None:
        return markdown

    page.meta["genre"] = genre
    note = "\n".join(f"    {line}" for line in genre["note"].strip().splitlines())
    title = f"This is {genre['article']} [{genre['word']}](index.md)"
    return f'!!! note "{title}"\n{note}\n\n{markdown}'
