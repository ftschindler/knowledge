"""Render a concept's declared `sources[]` as the footnotes its prose cites.

A source is declared once, in frontmatter, where federation tooling reads it,
and cited in prose by its `id` as an ordinary footnote marker. This hook writes
the definitions that markers point at, so the URL, the title and the date the
source was last checked live in exactly one place.

Citation and declaration have to agree, both ways. A marker with no declaration
is a dangling footnote; a declaration nothing cites is a claim of provenance the
page never actually makes. Either fails the build, and the `source-citations`
pre-commit hook catches both before it gets that far.
"""

from __future__ import annotations

import re

MARKER = re.compile(r"\[\^([^\]]+)\]")
FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")


def cited_ids(markdown: str) -> set[str]:
    """Return the footnote ids cited in `markdown`, ignoring fenced code."""
    ids: set[str] = set()
    in_fence = False
    for line in markdown.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            ids.update(MARKER.findall(line))
    return ids


def definition(source: dict) -> str:
    """Render one declared source as a footnote definition."""
    parts = [f"[{source['title']}]({source['resource']})"]
    author = source.get("author", "")
    if author:
        parts.append(f"by {author.removeprefix('human:')}")
    if source.get("last_modified"):
        parts.append(f"last modified {source['last_modified']}")
    return f"[^{source['id']}]: " + ", ".join(parts)


def on_page_markdown(markdown, page, config, files):
    sources = (page.meta or {}).get("sources")
    if not sources:
        return markdown

    declared = {source["id"] for source in sources}
    cited = cited_ids(markdown)
    if declared != cited:
        undeclared = ", ".join(sorted(cited - declared))
        uncited = ", ".join(sorted(declared - cited))
        raise ValueError(
            f"{page.file.src_uri}: sources and citations disagree"
            + (f"; cited but not declared: {undeclared}" if undeclared else "")
            + (f"; declared but not cited: {uncited}" if uncited else "")
        )

    definitions = "\n".join(definition(source) for source in sources)
    return f"{markdown}\n\n{definitions}\n"
