---
type: Investigation
title: 'Spell-checking prose in a pre-commit hook: corpus checkers, dictionary checkers, and what
  each one misses'
description: A measured comparison of codespell, typos and cspell against one real misspelling, showing
  that corpus and dictionary checkers fail on disjoint sets and that neither alone enforces a
  language variant.
tags:
- pre-commit
- linting
- spelling
- prose
- dx
- tooling
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
sources:
- id: typos-hooks
  resource: https://raw.githubusercontent.com/crate-ci/typos/master/.pre-commit-hooks.yaml
  title: 'crate-ci/typos: .pre-commit-hooks.yaml'
  last_modified: '2026-09-28'
- id: cspell-hooks
  resource: https://raw.githubusercontent.com/streetsidesoftware/cspell-cli/main/.pre-commit-hooks.yaml
  title: 'streetsidesoftware/cspell-cli: .pre-commit-hooks.yaml'
  last_modified: '2026-09-28'
- id: typos-pypi
  resource: https://pypi.org/pypi/typos/json
  title: 'typos on PyPI: release metadata'
  last_modified: '2026-09-28'
---
**Context** - a documentation bundle whose house rules require British English throughout had no
spell check of any kind, and the thing that prompted one was a single typo in a YAML file:
`revied`, for `reviewed`. The question was which hook to add. The answer turned out to depend on
a distinction that neither tool's description makes obvious, and that only testing against that
exact word revealed.

Everything below was run on one repository of roughly a hundred markdown files on 2026-09-28,
against `codespell`, `typos` v1.50.3 and `cspell` v10.2.0.

## Two kinds of checker, and they are not substitutes

**A corpus checker** carries a list of known misspellings paired with their corrections.
`codespell` and `typos` are both of this kind. They are fast, they suggest a fix, and they
almost never produce a false positive, because a word is only reported if somebody has
previously recorded it as a mistake.

**A dictionary checker** carries a list of words that exist. `cspell` is of this kind. It reports
anything absent from that list, usually with no suggestion, and every proper noun and domain term
in the repository is absent from it until somebody adds it.

The consequence is the finding, and it is sharper than "one is stricter":

```text
$ echo 'teh recieve revied reviewd seperate occured' | checker

codespell   teh, recieve, seperate, occured
typos       teh, recieve, seperate, occured, reviewd
cspell      recieve, revied, reviewd, seperate, occured
```

`revied` passes both corpus checkers. It is not a recorded mistake, so neither examines it.
`reviewd`, one letter away and the same kind of error, is caught by `typos`. A corpus checker's
coverage is not a property of how wrong a word is; it is a property of whether somebody typed
that particular wrong word often enough for it to be collected.

The inverse holds too. `teh` is in every corpus and, being three letters, is the kind of token a
dictionary checker's own heuristics may pass over. **The two catch overlapping but neither-contains-the-other
sets**, which is the argument for running both rather than choosing.

## Only one of the three can enforce a language variant

A written rule of "British English throughout" is unenforced unless the checker knows which
English it wants.

- `typos` takes `locale = "en-gb"` and then reports `color` as `colour`, `utilizing` as
  `utilising`, `capitalize` as `capitalise`.
- `codespell` ships builtin dictionaries named `en-GB_to_en-US` and `en_to_en-OX`, and nothing in
  the opposite direction. It can convert British spellings to American, which is the reverse of
  what a British-English rule wants, so it cannot do this job at all.
- `cspell` under `--locale en-GB` rejects `color`, but accepts `utilizing`, `capitalize` and
  `localized`. That is correct lexicography and useless as a style gate: the `-ize` endings are
  valid English, listed in Oxford dictionaries, and a dictionary checker has no grounds to object.

So the locale rule is `typos`-shaped work. On a repository that had never been spell-checked, it
found `utilizing`, `capitalize` and `localized` sitting in prose whose conventions file demanded
the opposite.

## Scope is the difference between seven hits and five hundred

Run unscoped across the repository, `typos` reported 532 occurrences of `Color` and 55 of
`center`. All of them came from Excalidraw diagrams, which are JSON files full of an American
spelling nobody wrote by hand. Scoped to tracked markdown via `git ls-files '*.md'`, the same run
reported seven distinct issues.

`cspell` over the same markdown reported 87 unknown words, of which roughly 85 were surnames,
product names and jargon. That is the real cost of a dictionary checker, and it is a one-time
cost: those words become a committed project dictionary, after which a new unknown word is either
a typo or a term nobody has written down yet. The corpus checker's equivalent cost was one
ignore entry, for a product name whose capitalisation the corpus read as a misspelling of a
common English word.

Both numbers argue the same thing from opposite ends. A content checker is pointed at the prose a
person wrote, never at a whole tree, and the file filter is doing as much work as the tool.

## The upstream hooks, and their defaults

Both projects ship a `.pre-commit-hooks.yaml`, so both pin to a SHA the way
[Pin pre-commit hooks to frozen revisions](../principles/pin_pre_commit_hooks_to_frozen_revisions.md)
asks. Neither needs a local reimplementation, and writing one would trade a commit pin for a
package-version pin, which is strictly worse.

One default is worth knowing before adopting. The `typos` hook ships
`args: [--write-changes, --force-exclude]`[^typos-hooks], so taking it as documented means a
tool that **rewrites prose in place on every commit**. For code that is usually welcome, and
[Autofix in the hook, don't just flag](../principles/autofix_in_the_hook_dont_just_flag.md)
argues for exactly that where a transform is deterministic and safe. A spelling correction in
prose is neither: the corpus offers several candidates for some words, and in a bundle whose
subject is its own wording, a silent edit is a change of meaning. Overriding `args` wholesale is
the only way to drop the flag, since pre-commit replaces the list rather than appending to it.

The `cspell` hook ends its `args` with `--files`[^cspell-hooks], which must stay last so the
paths are appended correctly, and any override has to preserve that.

Both were run under `prek` in a scratch repository before being recommended, which is how the
`--write-changes` default and the config-file pickup were established rather than assumed. That
habit generalises: see
[Verify a pre-commit hook's file-type filter actually matches your file](../principles/verify_a_pre_commit_hooks_file_type_filter_actually_matches_your_file.md),
where a hook reported success whilst looking at nothing.

## Portability

`typos` installs as `language: python` from a prebuilt wheel, and v1.50.3 publishes wheels for
macOS x86-64 and arm64, manylinux x86-64, aarch64 and i686, musllinux, and Windows 32 and
64-bit[^typos-pypi]. No Rust toolchain is involved anywhere, so it is as portable as any Python
hook.

`cspell` is `language: node`, so the hook runner provisions Node for it. That is not a new risk in
a repository that already runs a node hook, but it is not free either: a node hook's environment
and the runner's cache can drift apart, and the failure shows up as a hook that installed without
its dependencies.

Measured on the same markdown: `typos` 0.2s, `cspell` 1.9s. Neither is a reason to choose.

## Bottom line

Run both. The pair costs two seconds and one dictionary, and the case for it is a single word:
`revied` passes both corpus checkers, `teh` is what corpus checkers exist for, and no single tool
here covers both. If only one is possible, take `cspell` for the dictionary class and accept that
the `-ize` endings go unchecked, because a variant rule nobody enforces was already the status
quo.

Two things the investigation does not settle. Whether a dictionary of 85 proper nouns stays
maintained, or silently becomes a place where genuine typos get added to make a commit pass,
which is the same failure mode as an unexplained lint suppression and wants the same answer.
And what to do about mirrored documents: a bundle that reproduces somebody else's writing must
not correct its typos, since a corrected mirror is a paraphrase still claiming provenance. Four
of the seven remaining `typos` hits were inside such a mirror. Excluding the directory is the
honest fix and an allow list is not, but that is a claim about mirrors rather than about
spelling, and it belongs on a page of its own.
