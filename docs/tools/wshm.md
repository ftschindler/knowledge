---
type: Tool
title: wshm
description: A self-hosted repository agent in one Rust binary, whose open-source edition triages
  issues and scores pull requests whilst the review and auto-fix it advertises are sold separately.
tags:
- tools
- ai-agents
- self-hosted
- ci-cd
- github
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-30T00:00:00Z'
sources:
- id: wshm-repo
  resource: https://github.com/wshm-dev/wshm
  title: 'wshm-dev/wshm: repository'
  last_modified: '2026-10-30'
- id: wshm-readme
  resource: https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/README.md
  title: 'wshm-dev/wshm: README at e5e7296'
  last_modified: '2026-10-21'
- id: wshm-pro-hooks
  resource: https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/src/pro_hooks.rs
  title: 'wshm-dev/wshm: src/pro_hooks.rs at e5e7296'
  last_modified: '2026-10-21'
- id: wshm-merge-queue
  resource: https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/src/pipelines/merge_queue.rs
  title: 'wshm-dev/wshm: src/pipelines/merge_queue.rs at e5e7296'
  last_modified: '2026-10-21'
- id: wshm-config
  resource: https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/docs/configuration.md
  title: 'wshm-dev/wshm: configuration reference at e5e7296'
  last_modified: '2026-10-21'
- id: wshm-daemon
  resource: https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/docs/daemon.md
  title: 'wshm-dev/wshm: daemon guide at e5e7296'
  last_modified: '2026-10-21'
---
wshm[^wshm-repo] is a repository agent that runs on your own machine: it fetches a forge's
issues and pull requests into a local database, classifies them with a model you point it at,
and can write labels and comments back. It ships as one Rust binary under Apache-2.0, and it
covers GitHub, GitLab, Gitea and Azure DevOps rather than GitHub alone.

It is open-core. The repository is the free edition, and a paid edition registers extra
behaviour into it at startup. Which half a given feature lives in is the thing to establish
before planning anything around it.

| | |
| --- | --- |
| Author | `wshm-dev`, with one account carrying almost all commits |
| Licence | Apache-2.0 |
| Language | Rust |
| Version | 0.32.0, released 21 October 2026; first commit 10 April 2026 |
| Distribution | Release binaries, Debian packages, a multi-architecture Docker image |
| Storage | SQLite by default, PostgreSQL as an alternative |
| Source | [github.com/wshm-dev/wshm](https://github.com/wshm-dev/wshm) |

## What the free edition does

Four things, and they are all read-then-annotate rather than write-code.

**Sync** pulls issues and pull requests into a local SQLite file. Everything else reads from
that, so the agent works against a snapshot rather than the live API.

**Issue triage** classifies an issue by kind, priority and confidence, and can apply labels and
a comment. It declines to close an issue it classified `wontfix`, on the grounds that the
classification is attacker-influenced text, but it does close one it classified as a duplicate
when given a target.

**Pull request analysis** produces a risk level, a type, a summary and a review checklist, and
can label by them. This is a verdict about the pull request, not a reading of the diff.

**Merge queue** scores open pull requests and ranks them.

## What is sold separately

The split matters because the names overlap with the free features and the marketing does not
always separate them. Line-by-line review of a diff, auto-fix that generates a pull request
from an issue, AI conflict resolution, changelog generation and the chat integrations are all
in the paid edition.[^wshm-readme]

The mechanism is a hook registry whose own first comment states the position: "In the OSS
build, all hooks are None (no-op)."[^wshm-pro-hooks] The free binary therefore contains the
configuration keys for these features and the call sites that would invoke them, and does
nothing when asked. Setting `auto_fix = true` in a config file is accepted and has no effect.

One claim is weaker still. The free feature list advertises the merge queue as "scoring,
auto-merge above threshold", and the queue does score. The merge is a `println!` behind
`// TODO: actual merge via GitHub API`, which prints "Warning: Merge not yet implemented.
Coming in M4."[^wshm-merge-queue] Nothing is merged, with `--apply` or without it.

## How it runs

Three shapes, and only the third needs anything reachable from outside.

**One-shot CLI.** `wshm sync`, `wshm triage`, `wshm pr analyze`, or `wshm run` for the whole
cycle. Outbound network only. Mutating actions require `--apply`; without it every command is
a dry run, which makes the first evaluation cheap and safe.

**Polling daemon.** `wshm daemon --poll --no-server` holds several repositories and polls each
on an interval. Still outbound only, and this is the shape that suits a laptop or a box behind
NAT.

**Webhook daemon.** A `POST /webhook` receiver that GitHub delivers to, which needs a public
URL or a relay. Deliveries are HMAC-verified and rejected when no secret is set, unless an
override is enabled.[^wshm-daemon]

Configuration is TOML: `.wshm/config.toml` per repository, `~/.wshm/global.toml` for the daemon
and its repository list.[^wshm-config] Credentials stay out of both, supplied as environment
variables or through an encrypted secret store. GitHub authentication takes either a personal
token or a GitHub App installation, the App preferred where configured.

Per-repository daemon features default off. `collect_issues` and `collect_prs` are the only
things a fresh daemon does; `triage_issues`, `analyze_prs`, `auto_pr` and `auto_merge` each
have to be turned on by name. A legacy `apply = true` switches on several at once, which is the
one setting worth not reaching for.

## Models

Fourteen providers, including Anthropic, OpenAI, Google, Mistral, Groq, DeepSeek and xAI, plus
Ollama for a local model and a `custom` provider that takes any OpenAI-compatible `base_url`.
Azure OpenAI is handled separately. Keys come from the provider's usual environment variable.

## What to know before adopting it

The project is six months old, has two listed contributors with one of them at two commits, and
carries no changelog. That is a thin base for something holding a write-capable forge token.

Two defaults are documented inconsistently with the source. The daemon guide calls polling the
default whilst the config field defaults to false, and the bind address is `127.0.0.1:3000` in
the config but `0.0.0.0:3000` in the CLI flag's own comment. Set `--poll` and `--bind`
explicitly rather than inheriting either.

The GitHub Action is planned rather than shipped, so the deployment is a daemon or a cron job
you run, not a workflow you add. Where the question is review on a pull request inside CI, the
free edition answers none of it, and [opencode](opencode.md)'s own GitHub action is the thing
that does.
