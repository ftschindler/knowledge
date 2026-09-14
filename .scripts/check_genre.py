#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Hold every concept to the genre its directory declares.

One directory, one genre, declared in that directory's `.genre.yaml` and
rendered into each page by `hooks/concept_genre.py`. Two ways that can come
apart, both checked here:

- A concept whose `type` is not the one its directory declares. The note the
  reader sees would then name a different kind of page than the frontmatter
  federation tooling reads.
- A concept still carrying a genre note in its body. It renders twice, and the
  copy in the file is the one that drifts.

Only files directly inside a concept directory are concepts: `index.md` and
`log.md` are reserved by the format, and `about/` is outside the bundle.
"""

import re
import sys
from pathlib import Path

import yaml

BUNDLE_ROOT = Path("docs")
GENRE_FILE = ".genre.yaml"
RESERVED = frozenset({"index.md", "log.md"})
NOT_CONCEPTS = frozenset({"stylesheets"})
WRITTEN_NOTE = re.compile(r'^!!! note "This is an? \[[^\]]+\]\(index\.md\)"', re.M)
TYPE = re.compile(r"^type:\s*(.+?)\s*$", re.M)


def check(path: Path) -> list[str]:
    """Return one message per way `path` disagrees with its declared genre."""
    try:
        relative = path.resolve().relative_to(Path.cwd() / BUNDLE_ROOT)
    except ValueError:
        return []
    if len(relative.parts) != 2 or relative.parts[0] in NOT_CONCEPTS:
        return []
    if relative.name in RESERVED:
        return []

    declaration = BUNDLE_ROOT / relative.parts[0] / GENRE_FILE
    if not declaration.is_file():
        return [
            f"{path}: {declaration} is missing - a concept directory declares its genre"
        ]

    genre = yaml.safe_load(declaration.read_text(encoding="utf-8"))
    text = path.read_text(encoding="utf-8")
    problems = []

    declared_type = TYPE.search(text)
    if declared_type and declared_type.group(1) != genre["type"]:
        problems.append(
            f"{path}: type is `{declared_type.group(1)}`, but {declaration} declares "
            f"`{genre['type']}` - one directory holds one genre"
        )

    note = WRITTEN_NOTE.search(text)
    if note:
        line = text[: note.start()].count("\n") + 1
        problems.append(
            f"{path}:{line}: genre note written out - delete it, {declaration} is rendered in its place"
        )
    return problems


def main(argv: list[str]) -> int:
    problems = [message for name in argv for message in check(Path(name))]
    for message in problems:
        print(message)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
