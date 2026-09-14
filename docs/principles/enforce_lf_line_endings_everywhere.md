---
type: Principle
title: Enforce LF line endings everywhere
description: Normalise all text files to LF and enforce it in more than one place rather than trusting
  each contributor's editor.
tags:
- principle
- software
- git
- repo-hygiene
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Normalise all text files to LF line endings, and enforce it in more
than one place - `.gitattributes`, `.editorconfig`, and a commit-time hook -
rather than trusting each contributor's editor.

**Why.** Mixed CRLF/LF endings produce noisy diffs, break shell scripts and
heredocs, and cause spurious "whole file changed" churn when a Windows editor
rewrites a file. Declaring LF once at the repository level makes the outcome
independent of who checks out the repo on which OS. Layering the three
mechanisms covers different moments: `.gitattributes` at checkout/commit,
`.editorconfig` while typing, the hook as a backstop.

**Snippet.**

```gitattributes
* text eol=lf
```

```ini
# .editorconfig
[*]
end_of_line = lf
```

```yaml
# .pre-commit-config.yaml
- id: mixed-line-ending
  args: [--fix=lf]
```

**How enforced.** Belt-and-braces: Git normalises on checkout, EditorConfig-aware
editors normalise on save, and `mixed-line-ending` fixes anything that slips
through. An instance of [Mirror every local guard in CI](mirror_every_local_guard_in_ci.md) applied to whitespace.
