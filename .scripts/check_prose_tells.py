#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
"""Forbid the prose tells of default LLM register.

This is the mechanical half of the three writing principles in
`docs/principles/`. It checks the tells those pages name as greppable, and
nothing else: a rule that needs judgement stays convention, enforced by a
review pass rather than by this script.

What is checked, and which principle owns the reasoning:

- Hype adjectives and adverbs (`seamless`, `powerful`, `effortless`), the
  dismissive `simply` and `just`, throat-clearing openers, future-promise
  framing, and more than one exclamation mark in a file. Owned by
  `write_in_a_calm_quantified_settled_fact_voice_not_a_promotional_one.md`.
- The LLM corpus tells: `delve`, `tapestry`, `testament to`, `navigate the
  complexities`, and the `not just X, it is Y` construction.

What is deliberately *not* checked, because the corpus shows it cannot be
without false positives:

- American spellings. `Authorization` is an HTTP header, `kb-visualize` is a
  command name, and `Categorize by what content is` is a page title whose
  rename would cascade through every link to it.
- `while` for `whilst`. The bundle already contains 17 of them against 25
  `whilst`, so a hook would block every commit rather than guard anything.
- The Oxford comma, which no regex distinguishes from a list's final clause.

Exemptions. Text inside fenced code blocks, inline code spans, link targets
and double quotes is skipped, because all four quote something else rather
than assert it. That exemption is what lets the voice principle page print its
own slop table without tripping this hook.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE = re.compile(r"^\s{0,3}(?:```|~~~)")
INLINE_CODE = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
# `!!! tip` opens an mkdocs admonition, and `![alt](src)` an image. Neither is
# an exclamation, so only a `!` closing a word is counted as one.
ADMONITION = re.compile(r"^\s*(?:!!!|\?\?\?)")
SENTENCE_BANG = re.compile(r"(?<=[A-Za-z0-9)\"'])!")

Rule = tuple[str, re.Pattern[str], str]

RULES: list[Rule] = [
    (
        "hype",
        re.compile(
            r"\b(seamless|effortless|powerful|robust|blazing|cutting[- ]edge|"
            r"state[- ]of[- ]the[- ]art|game[- ]chang|revolutionary|supercharge|"
            r"unlock the|elevate your|delightful|magical)\w*",
            re.IGNORECASE,
        ),
        "hype adjective - name what it does instead",
    ),
    (
        "dismissive",
        re.compile(r"(?:^|(?<=[.!?]\s))\s*(Simply|Just)\b"),
        "dismissive opener - open with the subject and move",
    ),
    (
        "throat-clearing",
        re.compile(
            r"(?:^|(?<=[.!?]\s))\s*(In order to|It is important to note|"
            r"It'?s worth noting|As you can see|Needless to say|"
            r"At the end of the day)\b",
            re.IGNORECASE,
        ),
        "throat-clearing - open with the subject",
    ),
    (
        "future-promise",
        re.compile(
            r"\b(will ensure|will seamlessly|you'?ll be up and running|"
            r"in no time|out of the box experience)\b",
            re.IGNORECASE,
        ),
        "future promise - narrate behaviour in the settled-fact present",
    ),
    (
        "llm-tell",
        re.compile(
            r"\b(delve|tapestry|testament to|navigate the complexities|"
            r"in today'?s fast[- ]paced|let'?s dive in|buckle up|"
            r"it'?s not just|ever[- ]evolving landscape)\b",
            re.IGNORECASE,
        ),
        "LLM corpus tell - rewrite in your own register",
    ),
    (
        "not-just",
        re.compile(
            r"\bnot (?:just|merely|only) [^.,;]{1,60}, (?:it|this|that)'?s\b",
            re.IGNORECASE,
        ),
        "`not just X, it is Y` construction - make the claim once",
    ),
]


def strip_quotations(line: str, quote_open: bool) -> tuple[str, bool]:
    """Blank out the spans that quote something rather than assert it.

    A quotation may run over several lines, and in this bundle regularly does,
    so the open-quote state is carried between lines rather than reset at each
    one. Quote characters are counted after the code spans are blanked, so an
    apostrophe inside backticks cannot unbalance the tally.
    """
    for pattern in (INLINE_CODE, LINK_TARGET):
        line = pattern.sub(lambda match: " " * len(match.group()), line)

    result: list[str] = []
    for character in line:
        if character in '"\u201c\u201d':
            quote_open = not quote_open
            result.append(character)
            continue
        result.append(" " if quote_open else character)
    return "".join(result), quote_open


def check(path: Path) -> list[str]:
    """Return one message per offending line in `path`."""
    lines = path.read_text(encoding="utf-8").splitlines()
    frontmatter_close = None
    if lines and lines[0].strip() == "---":
        for number, line in enumerate(lines[1:], start=2):
            if line.strip() == "---":
                frontmatter_close = number
                break

    problems: list[str] = []
    exclamations = 0
    in_fence = False
    quote_open = False
    for number, raw in enumerate(lines, start=1):
        if FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or (frontmatter_close is not None and number <= frontmatter_close):
            continue
        if ADMONITION.match(raw):
            continue
        line, quote_open = strip_quotations(raw, quote_open)
        exclamations += len(SENTENCE_BANG.findall(line))
        for name, pattern, fix in RULES:
            match = pattern.search(line)
            if match:
                found = match.group().strip()
                problems.append(f"{path}:{number}: {name} `{found}` - {fix}")
    if exclamations > 1:
        problems.append(
            f"{path}: {exclamations} exclamation marks - earn one, on the genuinely surprising fact"
        )
    return problems


def main(argv: list[str]) -> int:
    problems = [message for name in argv for message in check(Path(name))]
    for message in problems:
        print(message)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
