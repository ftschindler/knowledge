---
type: Wish
title: Local-first, but not local-required
description: The canonical store works fully offline with nothing but a text editor, yet stays editable
  through a hosted path needing no local setup.
tags:
- wish
- situational
- software
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Wish.** The canonical store works fully offline with nothing but a text editor,
yet the same content stays editable through a hosted path that needs no local
setup at all.

**Why I want this.** Local-first gives me speed, offline access and ownership - my
data is a folder on my disk, not a row in someone's database. But *local-required*
would be a tax: it means I (or any contributor) can't fix a typo from a borrowed
machine, a phone, or without a toolchain install. I want the floor (works locally,
offline, mine) without the ceiling (must be local to touch it).

**What it implies.** A git-backed store of plain files satisfies local-first
(clone it, point an editor at it). Hosting it somewhere with a web editor
(e.g. GitHub's browser editing) satisfies not-local-required - edits from the web
become commits like any other. The convenience editor stays *optional* on top,
never the gate.

**Tensions.** The hosted path usually can't run the full local quality pipeline
(pre-commit hooks, local preview), so feedback there is slower and leans on CI to
catch issues - an acceptable trade for always-editable. Note this is a *wish*, not
a value or principle: it's a requirement I chose for this project, discovered via
the why-test in
[Layer build-knowledge as a values-to-blueprints derivation pipeline](../knowledge_management/layer_build_knowledge_as_a_values_to_blueprints_derivation_pipeline.md).
