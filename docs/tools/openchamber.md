---
type: Tool
title: OpenChamber
description: A desktop, web and mobile workspace that drives an opencode server rather than replacing
  it, and what it adds and gives up against running the opencode terminal interface directly.
tags:
- tools
- opencode
- agents
- openchamber
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-07T12:00:00+02:00'
sources:
- id: openchamber-repo
  resource: https://github.com/openchamber/openchamber
  title: 'openchamber/openchamber: Agentic Development Environment based on OpenCode AI agent'
  last_modified: '2026-10-07'
- id: openchamber-docs-server
  resource: https://docs.openchamber.dev/opencode-server/
  title: 'OpenChamber: OpenCode Server'
  last_modified: '2026-10-07'
- id: openchamber-docs-providers
  resource: https://docs.openchamber.dev/providers/
  title: 'OpenChamber: Providers, Models and Agents'
  last_modified: '2026-10-07'
- id: openchamber-docs-environment
  resource: https://docs.openchamber.dev/environment/
  title: 'OpenChamber: Environment Variables'
  last_modified: '2026-10-07'
- id: openchamber-docs-repository-config
  resource: https://docs.openchamber.dev/repository-config/
  title: 'OpenChamber: Repository Configuration'
  last_modified: '2026-10-07'
---
OpenChamber[^openchamber-repo] is a workspace around [opencode](opencode.md) rather than a
second agent. It starts an opencode server and talks to its API[^openchamber-docs-server], so
the agent loop, the providers and the configuration all stay opencode's, and what OpenChamber
owns is everything around a session: a chat window with a diff viewer, review and release
workflow, and the same sessions reachable from another device.

| | |
| --- | --- |
| Author | The `openchamber` organisation, with the project's own site at [openchamber.dev](https://openchamber.dev/). Independent of the opencode team |
| Licence | MIT |
| Language | TypeScript, built with bun; the desktop application is Electron |
| Distribution | `@openchamber/web` from npm for the CLI and server, an installer script, Linux AppImages for x86\_64 and ARM64, a VS Code extension, iOS and Android clients |
| Source | [github.com/openchamber/openchamber](https://github.com/openchamber/openchamber) |
| Version read | 2.1.1, released 2026-10-04 |

## How it reaches opencode

The server process spawns `opencode serve` and makes its calls through opencode's own client
library. It will also attach to a server somebody else started, through `OPENCODE_HOST` and
`OPENCODE_SKIP_START`[^openchamber-docs-server].

Which opencode binary that is depends on the surface. The CLI, the web interface and the VS Code
extension use whatever `opencode` is on the machine. The desktop application ships its own,
pinned to the version it was built against[^openchamber-repo], so installing the desktop app on a
machine that already runs opencode gives that machine two of them.

The configuration is read, not replaced. `OPENCODE_CONFIG_DIR` is honoured, falling back to
`$XDG_CONFIG_HOME/opencode` and then `~/.config/opencode`[^openchamber-docs-environment], and
agents, plugins, skills and MCP servers come from the config layers opencode already resolves.
OpenChamber puts a settings page in front of several of those: providers, agents, skills, MCP
servers, and the `AGENTS.md` sitting at the config directory. A provider added through that page
is written into opencode's config and its key into opencode's auth store, which the documentation
is explicit about: credentials are "stored by OpenCode, not
OpenChamber"[^openchamber-docs-providers].

It keeps a little state of its own, beside opencode's rather than inside it:
`~/.config/openchamber` for its data directory, and `.openchamber/project.json` in a repository
for per-project settings[^openchamber-docs-repository-config].

## What it adds

The features are about the work around a session rather than about the model answering it:

| | |
| --- | --- |
| **Session goals** | A finish line per session. The result is checked after each turn and the agent keeps going until the goal is met, it is blocked, or a limit is reached, including after the app is closed |
| **Multi-run and fusion** | The same task given to up to five models, each in its own session and optionally its own worktree, then one result chosen or the strongest parts combined |
| **Changes walkthrough** | A large diff turned into an ordered, grouped tour of the change |
| **Preview** | The application under development opened beside the conversation; pointing at an element sends the agent its screenshot, styles, position and browser errors |
| **Scheduled work** | A prompt run once, daily, weekly or on a cron schedule, optionally carrying a session goal |
| **Device reach** | Desktop, browser or PWA, VS Code, iOS and Android against the same sessions, paired by QR code over an end-to-end encrypted relay, with tunnels, LAN and SSH as alternatives |

## Where it sits against a terminal opencode setup

The comparison worth making is against opencode driven from a terminal with a configuration like
[the one this bundle's opencode page describes](opencode.md#how-i-configure-it), because the two
are not alternatives in the usual sense: one is running inside the other.

| | opencode in a terminal | OpenChamber |
| --- | --- | --- |
| **Invocation** | A binary in a shell, in whatever directory and multiplexer you were already in | A server plus a client. `openchamber --ui-password ...` binds to localhost, and a browser, the desktop app or a phone connects to it |
| **Portability** | One binary; wherever a terminal reaches, including a plain `ssh` one-liner | Node 22 or newer for the CLI and server, Electron for the desktop app, FUSE for the AppImage. The server runs headless with `--api-only`, which is the shape that travels |
| **Configuration** | Files you edit and commit; `OPENCODE_CONFIG_DIR` picks which set | The same files, plus settings pages that write them, plus `.openchamber/` for its own |
| **Agents, skills, rules** | opencode's, resolved from the config layers | opencode's, resolved the same way. Nothing to port, and nothing it gives that a terminal session does not already have |
| **Credentials** | opencode's `auth.json` | The same file, written through a different front end |
| **What it is for** | Running the agent | Watching several of them, from somewhere that is not this machine |

The thing to take from that table is that **everything provider-side and agent-side is inherited,
so adopting it is not a migration.** A profile-per-provider layout keeps working, because the
variable that selects the profile is the variable OpenChamber reads. What is genuinely new is the
remote access, the parallel runs and the review surface, and the cost of those is an Electron
application or a long-lived server process where there used to be a binary and a shell.

Two caveats sit on the GitHub side rather than the agent side. The issue and pull request
integration authenticates through its own device flow against `github.com`, falling back to a
token from the `gh` CLI; a personal access token is refused outright, and no Enterprise host is
offered. And whilst opencode's `github-copilot` provider is reachable through OpenChamber like any
other, nothing in the documentation says anything about which kind of GitHub account that provider
will sign in, so a tenancy that constrains the device flow constrains OpenChamber exactly as much
as it constrains opencode, and no more.
