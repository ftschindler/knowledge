---
title: Local Dev Environment
---

A local environment lets you preview the site, run linters before pushing, and work with
any text editor. See also [Editing on GitHub](editing_on_github.md).

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) - the only global
dependency. uv manages the Python version and all Python packages for this project.

## Clone and preview

```bash
git clone https://github.com/ftschindler/knowledge.git
cd knowledge
uv run mkdocs serve
```

Open the printed URL, typically `http://127.0.0.1:8000`, to see the site. Changes to Markdown files are reflected
immediately.

!!! tip

    A `Makefile` is included as an optional convenience. `make serve` is equivalent to the
    command above, and `make bootstrap` installs dependencies and pre-commit hooks in one step.
    Run `make` with no arguments to see all available targets.

## Pre-commit hooks

We use [prek](https://prek.j178.dev/)
(as a drop-in replacement for [pre-commit](https://pre-commit.com/)) to automatically run
code quality checks (formatters, linters, link checker)
as well as OKF conformance checks on the knowledge bundle. See
[`.pre-commit-config.yaml`](https://github.com/ftschindler/knowledge/blob/main/.pre-commit-config.yaml)
for the full list of checks.

!!! tip

    prek is installed as a dev dependency via uv - no extra global tools required.

### Install hooks for this repository

```bash
uv run prek install
```

Or use the Makefile shortcut, which also syncs dependencies:

```bash
make bootstrap
```

### Using **prek** manually

Once the repository is bootstrapped you can invoke any of the supported prek commands directly via `uv run`:

* **Run all configured hooks on the current tree**

  ```bash
  uv run prek run --all-files
  ```

* **Run a specific hook** (e.g. `ruff-check`)

  ```bash
  uv run prek run ruff-check
  ```

* **Show which hooks are configured**

  ```bash
  uv run prek list
  ```

All of the above honour the same virtual‑environment setup that `make bootstrap` creates, so you never need to install anything globally.

## Pull request workflow

All changes are made via
[pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).
