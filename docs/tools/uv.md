---
type: Tool
title: uv
description: A Rust-written Python package and project manager that resolves a declared pyproject.toml
  into an exactly pinned uv.lock.
tags:
- tools
- uv
- python
- packaging
- supply-chain
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-11T00:00:00Z'
verified:
  by: human:felix_schindler
  at: '2026-09-11T12:11:36Z'
sources:
- id: uv-docs
  resource: https://docs.astral.sh/uv/
  title: 'uv: documentation'
  last_modified: '2026-09-11'
---
[uv](https://docs.astral.sh/uv/) is a Python package and project manager that replaces the
`pip` / `pip-tools` / `pipx` / `venv` stack with one binary. It is the tool this knowledge
base and its publishing stack install through, and the reason a Python environment here is
reproducible rather than merely described.

| | |
| --- | --- |
| Author | Astral |
| Licence | Apache-2.0 (dual-licensed with MIT) |
| Language | Rust |
| Distribution | A standalone installer, `pipx install uv`, Homebrew, and most distro repositories |
| Source | [github.com/astral-sh/uv](https://github.com/astral-sh/uv) |
| Version read | 0.12.13 |

## What it is

Two files carry the state, and the distinction between them is the whole point.
`pyproject.toml` is the **manifest**: what you declare, usually loosely, as
`mkdocs-material` with no version or `mkdocs>=1.6,<2`. `uv.lock` is the **lockfile**: the
exact resolution of that manifest, every package with a pinned version and hashes, across
every platform the project supports.

The lockfile is always the larger of the two, because it also pins everything your
dependencies depend on. A manifest naming ten packages routinely locks fifty, and the forty
that appear in only one of the files are the ones nobody chose deliberately. That asymmetry
is what
[Keep transitive dependencies in the regular update cycle](../principles/keep_transitive_dependencies_in_the_update_cycle.md)
is about.

The commands that matter for that split:

| | |
| --- | --- |
| `uv lock` | Resolve the manifest into the lockfile |
| `uv lock --upgrade` | Re-resolve everything to the newest versions the manifest permits, transitive packages included |
| `uv lock --upgrade-package <name>` | Re-resolve one package and whatever that forces, leaving the rest pinned |
| `uv sync` | Make the environment match the lockfile exactly |
| `uv sync --frozen` | The same, but fail rather than update a stale lockfile - the CI form, per [Install from a frozen lockfile in CI](../principles/install_from_a_frozen_lockfile_in_ci.md) |
| `uv run` | Run a command in that environment, syncing first |

`uv run` also executes a single file's
[PEP 723 inline metadata](../principles/use_pep_723_inline_script_metadata_for_zero_install_tooling_scripts.md)
without a project at all, which is how the standalone scripts here declare their own
dependencies.

## Why it matters here

It is the substrate under
[the publishing stack](../blueprints/mkdocs_material_pkb_publishing_stack.md), and the
reason several principles in this bundle can be stated concretely rather than as good
intentions: a frozen lockfile in CI, a guarded Python version, and dev tooling resolved
through an ephemeral runner instead of an activated virtualenv.

It is also one half of an automation problem. An update bot has to understand both files to
do its job, and
[Dependabot's uv support declines transitive security updates it has resolved](../findings/20260911_dependabot_declines_transitive_security_updates_in_uv_lock.md)
records what happens when it is pointed at the manifest and left there.
