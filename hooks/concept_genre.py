"""Render each concept's genre note from its directory's declaration.

Every concept opens with a note naming what kind of page it is and linking to
the index that defines the kind, because a reader arriving from search lands in
the middle of the bundle where nothing else says which genre they are reading.
The note is identical for every page in a directory, so it is declared once, in
that directory's `.genre.yaml`, and rendered here.

A page whose `status` is not stable says so in that same note, which changes
colour and leads with the status word rather than adding a second block above the
body. The card at the foot of the rail already carries the status, but a reader
landing mid-page from search never looks there.

What `draft` means differs by genre: an unfinished page in most directories, a
decision not yet carried out in `decisions/`. So the wording is the directory's
to override, under `status_notes`, and there is a default for the genres that do
not.

The declaration is also what `type` is checked against, by the `genre-conformance`
pre-commit hook, so the directory, the note and the frontmatter cannot disagree.
"""

from __future__ import annotations

from pathlib import Path

import yaml

GENRE_FILE = ".genre.yaml"
STATUS_ADMONITIONS = {
    "draft": ("warning", "Draft"),
    "deprecated": ("danger", "Deprecated"),
}
STABLE_ADMONITION = "note"
DEFAULT_STATUS_NOTES = {
    "draft": "Unfinished. It is here because the gap is worth showing, not because it is ready to be read as settled.",
    "deprecated": "Superseded, and kept for the record rather than to be followed.",
}
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


def note_for(genre: dict, status: object) -> str:
    """Build the one note a concept opens with, coloured by its status."""
    genre_phrase = f"This is {genre['article']} [{genre['word']}](index.md)"
    body = genre["note"].strip()

    if status in STATUS_ADMONITIONS:
        kind, word = STATUS_ADMONITIONS[status]
        title = f"{word} - {genre_phrase[0].lower()}{genre_phrase[1:]}"
        declared = genre.get("status_notes") or {}
        body = f"{declared.get(status) or DEFAULT_STATUS_NOTES[status]}\n\n{body}"
    else:
        kind, title = STABLE_ADMONITION, genre_phrase

    indented = "\n".join(f"    {line}" for line in body.strip().splitlines())
    return f'!!! {kind} "{title}"\n{indented}\n\n'


def on_page_markdown(markdown, page, config, files):
    genre = genre_of(page.file.src_uri, config.docs_dir)
    if genre is None:
        return markdown

    page.meta["genre"] = genre
    return note_for(genre, page.meta.get("status")) + markdown
