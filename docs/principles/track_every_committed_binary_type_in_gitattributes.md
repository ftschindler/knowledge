---
type: Principle
title: Track every committed binary type in .gitattributes
description: Give every committed binary file type an explicit .gitattributes entry rather than relying
  on Git's content auto-detection.
tags:
- principle
- software
- git
- git-lfs
- repo-hygiene
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** For every binary file type you commit, add an explicit
`.gitattributes` entry that routes it to Git LFS and marks it `-text`. Don't
rely on Git's content auto-detection.

**Why.** Git's heuristic for "is this binary" is imperfect: an SVG is XML text
by content but you want it treated as an opaque asset, and a new image type you
add later won't be covered until you say so. An unlisted binary gets stored
inline (bloating history irrecoverably) and may be line-ending-mangled as if it
were text. Listing each type explicitly makes storage and diff behaviour a
deliberate, reviewable decision rather than an accident of heuristics.

**Snippet.**

```gitattributes
*.png       filter=lfs diff=lfs merge=lfs -text
*.svg       filter=lfs diff=lfs merge=lfs -text
*.excalidraw filter=lfs diff=lfs merge=lfs -text
```

**How enforced.** Convention plus review: every PR that introduces a new asset
type should add its `.gitattributes` line in the same change. Pairs with
[Enforce LF line endings everywhere](enforce_lf_line_endings_everywhere.md) (the `* text eol=lf` default) - the
`-text` override is what exempts true binaries from that normalisation.

**Order matters - track before you commit.** The `.gitattributes` line only
takes effect for files added *after* it exists and after LFS is installed in the
repo. Run `git lfs install` (writes the clean/smudge filters into the repo) and
have the pattern in `.gitattributes` *before* the first matching binary is
staged - otherwise Git stores the raw bytes inline and no later edit un-bloats
that history. Verify a stage actually became a pointer rather than trusting it:

```console
$ git add logo.png
$ git show :logo.png            # the staged blob, not the working file
version https://git-lfs.github.com/spec/v1
oid sha256:…
size 16
$ git check-attr filter text -- logo.png
logo.png: filter: lfs
logo.png: text: unset            # -text applied, so eol=lf won't touch it
```

If `git show :<file>` prints binary bytes instead of the three-line pointer, the
attribute did not apply (wrong pattern, or LFS not installed) - fix it before
committing.

**Inert until matched - so listing types costs nothing.** The `filter=lfs` lines
do nothing until a file matching one is added: with none tracked, `git check-attr
filter -- notes.md` reports `unspecified` and git never invokes `git-lfs` to
clone, commit, or test. So keeping the block in a repo with zero such assets is
legitimate as [documented intent](a_declared_but_inert_config_documents_intent_not_enforcement.md) ("images belong in LFS"), and does **not** justify requiring
git-lfs of every contributor - see [Do not make a tool a prerequisite for work it is not needed for](do_not_make_a_tool_a_prerequisite_for_work_it_is_not_needed_for.md).

**Without `git lfs install`, a missing git-lfs does not fail loudly.** The clone/
commit-abort safety net exists only when `filter.lfs.required=true`, which
`git lfs install` sets in the repo config. In a clone where nobody ran it,
`filter.lfs.required` is unset, so staging a matching binary with git-lfs absent
does **not** abort - git warns and stores the raw bytes inline, the exact bloat
this page prevents. If a repo drops `git lfs install` from its `bootstrap`, the
loud-failure guarantee goes with it; a pre-commit guard rejecting staged binaries
when LFS is inactive restores enforcement without making git-lfs a hard install
requirement.
/home/felix/.agents/wikis/public/docs/raw/gitattributes-cover-binary-types.md
