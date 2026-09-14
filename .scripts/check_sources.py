#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Check that a concept's declared sources and its citations agree, both ways.

A source is declared once in `sources[]` and cited in prose as `[^id]`, which
`hooks/concept_sources.py` renders as a footnote. A citation with no declaration
is a dangling footnote the site build would reject; a declaration nothing cites
is a claim of provenance the page never makes. Both are reported here, before a
build gets the chance.

Citations inside fenced code blocks are ignored: a snippet quotes syntax rather
than citing anything.
"""

import re
import sys
from pathlib import Path

import yaml

MARKER = re.compile(r"\[\^([^\]]+)\]")
FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")


def split(text: str) -> tuple[str, str]:
    """Return the frontmatter and body of `text`, either possibly empty."""
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 3)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def cited(body: str) -> set[str]:
    """Return the footnote ids cited in `body`, ignoring fenced code."""
    ids: set[str] = set()
    in_fence = False
    for line in body.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            ids.update(MARKER.findall(line))
    return ids


def check(path: Path) -> list[str]:
    """Return one message per source cited but not declared, or the reverse."""
    frontmatter, body = split(path.read_text(encoding="utf-8"))
    if not frontmatter:
        return []
    meta = yaml.safe_load(frontmatter) or {}
    declared = {source["id"] for source in meta.get("sources") or []}
    citations = cited(body)

    return [
        f"{path}: `[^{identifier}]` cited but not declared in `sources[]`"
        for identifier in sorted(citations - declared)
    ] + [
        f"{path}: source `{identifier}` declared but never cited - a source no page refers to "
        "claims a provenance the page does not have"
        for identifier in sorted(declared - citations)
    ]


def main(argv: list[str]) -> int:
    problems = [message for name in argv for message in check(Path(name))]
    for message in problems:
        print(message)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
