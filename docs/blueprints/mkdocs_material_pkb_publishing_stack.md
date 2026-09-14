---
type: Blueprint
title: MkDocs Material PKB publishing stack
description: The concrete, copyable component stack for a git-backed plain-Markdown personal knowledge
  base that publishes to a static site.
tags:
- blueprint
- software
- mkdocs
- pkb
- static-site
- ci-cd
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [blueprint](index.md)"
    The concrete, copyable artefact a decision produced.

The stack for a git-backed, plain-Markdown personal knowledge base that publishes
to a static site, produced by the
[Building my visual PKB](../decisions/building_my_visual_pkb.md) decision. It is
set out in three parts: the component manifest, the principles it instantiates,
and the operating manual.

## Manifest - what is assembled, and why each piece

- **[MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)**
  - static site generator + theme; builds plain Markdown into a searchable site.
  Pin MkDocs `<2` (Material is not yet 2.0-compatible).
- **Plugins** - `awesome-pages` (nav without a hand-maintained tree),
  `obsidian-support` (Obsidian callouts → Material admonitions), `excalidraw`
  (client-side `.excalidraw` rendering, light/dark), `backlinks-section`,
  `glightbox` (image lightbox), `git-revision-date-localized`.
- **[uv](https://docs.astral.sh/uv/)** - the single toolchain: manages the Python
  version and all dependencies; no other global install required.
- **Git + Git LFS** - LFS stores binary/opaque assets (`.png`, `.svg`,
  `.excalidraw`) out of line.
- **Pre-commit (via [prek](https://prek.j178.dev/))** - markdown lint, link
  checking, formatting and repo-hygiene guards.
- **GitHub Actions → GitHub Pages** - on push to `main`, build with
  `mkdocs build --strict` and deploy.

## Principles it instantiates

This stack is a worked example of many atomic principles - copy them, not just the
config: [Pin GitHub Actions to full commit SHAs](../principles/pin_github_actions_to_full_commit_shas.md),
[Pin pre-commit hooks to frozen revisions](../principles/pin_pre_commit_hooks_to_frozen_revisions.md),
[Pin transitive runtime dependencies, not just the tool](../principles/pin_transitive_runtime_dependencies_not_just_the_tool.md),
[Guard invariants at commit-time, not review-time](../principles/guard_invariants_at_commit_time_not_review_time.md),
[Mirror every local guard in CI](../principles/mirror_every_local_guard_in_ci.md),
[Validate config files against their published schema](../principles/validate_config_files_against_their_published_schema.md),
[Enforce the intersection of all renderers and consumers](../principles/enforce_the_intersection_of_all_renderers_and_consumers.md),
[Grant least-privilege CI permissions at both workflow and job level](../principles/grant_least_privilege_ci_permissions_at_both_workflow_and_job_level.md),
[Cancel superseded CI runs with a concurrency group](../principles/cancel_superseded_ci_runs_with_a_concurrency_group.md),
[Batch dependency updates with a cooldown, not a firehose](../principles/batch_dependency_updates_with_a_cooldown_not_a_firehose.md),
[Use PEP 723 inline script metadata for zero-install tooling scripts](../principles/use_pep_723_inline_script_metadata_for_zero_install_tooling_scripts.md),
[Treat warnings as errors](../principles/treat_warnings_as_errors.md) (`--strict`),
[Track every committed binary type in .gitattributes](../principles/track_every_committed_binary_type_in_gitattributes.md),
[Declare formatting once, editor-agnostically, via .editorconfig](../principles/declare_formatting_once_editor_agnostically_via_editorconfig.md) and
[Make the build interface a self-documenting Makefile](../principles/make_the_build_interface_a_self_documenting_makefile.md).

## Operating manual - the shape, not the repo

The reusable skeleton (details are repo-specific):

- **Bootstrap** - one command installs deps + hooks (`uv sync && uv run prek
  install`, exposed as `make bootstrap`).
- **Preview** - a live-reloading local server (`mkdocs serve` / `make serve`).
- **Multiple entry points** - three equally valid contribution paths: a local
  editor, an optional Obsidian convenience layer over the same folder, and
  in-browser editing on the host
  (satisfying [Local-first, but not local-required](../wishes/local_first_but_not_local_required.md)).
- **Conventions the stack imposes** - frontmatter `title`, no second `#` heading,
  lowercase-no-whitespace filenames, standard Markdown links (not wiki-links),
  Excalidraw as portable JSON - each backed by a pre-commit guard.
