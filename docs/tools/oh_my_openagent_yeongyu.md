---
type: Tool
title: oh-my-openagent (YeonGyu-Kim)
description: The plugin that supplies this opencode setup's agents, skills and orchestration, now
  one of three editions of a harness-independent product, and broken on opencode 2.x.
tags:
- tools
- oh-my-openagent
- opencode
- ai-agents
- agent-skills
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-15T23:05:00+02:00'
stale_after: '2026-12-15'
sources:
- id: omo-repo
  resource: https://github.com/code-yeongyu/oh-my-openagent
  title: 'code-yeongyu/oh-my-openagent: The Best AI Agent Harness'
  last_modified: '2026-10-15'
- id: omo-install
  resource: https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md
  title: oh-my-openagent installation guide
  last_modified: '2026-10-15'
- id: omo-rename
  resource: https://github.com/code-yeongyu/oh-my-openagent/releases/tag/v3.11.0
  title: 'Release v3.11.0: first release as an oh-my-openagent'
  last_modified: '2026-03-07'
- id: omo-issue-10089
  resource: https://github.com/code-yeongyu/oh-my-openagent/issues/10089
  title: 5.1.32 fails to load on opencode 2.0.27
  last_modified: '2026-10-15'
- id: omo-licence
  resource: https://github.com/code-yeongyu/oh-my-openagent/blob/dev/LICENSE.md
  title: oh-my-openagent LICENSE.md
  last_modified: '2026-10-15'
- id: spdx-sul
  resource: https://spdx.org/licenses/SUL-1.0
  title: 'SPDX: Sustainable Use License 1.0'
  last_modified: '2026-10-15'
---
oh-my-openagent[^omo-repo] - OmO - is what turns a bare [opencode](opencode.md) into the setup
these pages are written through: a roster of named agents, a skill loader, model routing per
task category, background agents and a set of LSP and AST tools. It is installed here as one
line of `opencode.jsonc`, which is the whole of its configuration surface and conceals how much
it brings.

| | |
| --- | --- |
| Author | YeonGyu-Kim, GitHub `code-yeongyu`, profile affiliation `@sionic-ai` |
| Licence | SUL-1.0, source-available and **not** open source |
| Distribution | npm, as `"plugin": ["oh-my-openagent@latest"]` in `opencode.jsonc` |
| Source | [github.com/code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) |
| Version read | 5.1.30 installed, against opencode 1.18.34 |

## It is no longer an opencode plugin, exactly

The name changed in March 2026, at `v3.11.0`. The release note gives the reason plainly: the
rename was to cause less confusion, because OmO is "about the whole architecture", not just a
plugin[^omo-rename].

What that became is **three editions** of one product[^omo-install]. *Ultimate* is the opencode
plugin, with the full agent registry, Team Mode and the lifecycle hooks. *Light* is a Codex CLI
plugin carrying the portable parts - rules, LSP, telemetry, `ast-grep` - but not the agent
registry or the `team_*` tools. *Native* is a standalone `omo` command with no host harness at
all.

The monorepo is organised to match: `omo-opencode`, `omo-codex` and `omo-senpi` are sibling
adapters over shared cores, and the npm `bin` block exposes five aliases from one script -
`oh-my-opencode`, `oh-my-openagent`, `omo-agent-toolkit`, `lazycodex`, `lazycodex-ai`.

**This is a widening rather than a departure.** Opencode is still the edition the docs call
Ultimate and still the build entry for the main npm package, so nothing here is being dropped.
But the project's centre of gravity has moved to a layer above any one harness, and the package
name is now the least reliable guide to what it is.

## Where it puts itself

Almost everywhere it writes is opencode's own state, with one exception that outlives opencode:
**it stores session transcripts and todos under `~/.claude`**, because its
`getClaudeConfigDir()` returns `$CLAUDE_CONFIG_DIR` and otherwise falls back to
`join(homedir(), ".claude")`.

That directory is Claude Code's by convention, and the plugin claims it whether or not Claude
Code is installed. Here it holds 96 MB of `ses_*.jsonl` across 599 sessions, written by
opencode, in a directory named after a tool this machine does not have. Anybody tidying up
after an uninstalled Claude Code will find it and reasonably conclude it is residue.

Setting `CLAUDE_CONFIG_DIR` moves it, and is the supported way out: the environment variable is
read first, with the `~/.claude` default behind it. The `coding-agent-sessions` skill reads
those transcripts, so moving the directory means moving the corpus with it.

## Versions, and what breaks

Releases are frequent to the point of being hard to track - several in a day, with published
numbers skipped where a release did not reach npm. Pinning `@latest`, as this setup does, means
taking whatever landed.

**The plugin does not work on opencode 2.x.** The v2 loader expects a default export shaped as
`effect` or `setup`; the plugin still exports the v1 `server` shape, so it fails to load. This
is reported for 5.1.32 on opencode 2.0.27 and again for 5.1.33 on 2.0.29[^omo-issue-10089]. The
maintainer has described an additive dual-host fix that keeps v1 behaviour alongside a v2 entry,
but the scaffold and its follow-on were still open pull requests in mid-October 2026.

Nothing in the package declares this. There is no `peerDependencies` entry for opencode and no
`engines` field; the opencode SDK is a build-time pin at 1.18.31 and says nothing about what
runs. So the incompatibility is discovered by the plugin silently not loading, and the fix is to
hold opencode at 1.x until the dual-host work ships.

**Known good on this machine: plugin 5.1.30 with opencode 1.18.34**, which is what wrote this
page. That pairing is a first-hand observation rather than anything the project certifies, and
it is the number to come back to if an upgrade takes the agents away.

## The licence is not an open-source one

SUL-1.0 is the Sustainable Use License[^omo-licence]. It permits use, copying, distribution and
derivative works, but confines use to "your own internal business purposes or for non-commercial
or personal use", and requires that anything passed on be free and non-commercial. Notices must
be preserved and modified copies marked.

SPDX records it as source-available with restrictions on use, and its OSI status as *Not
Submitted*[^spdx-sul]. For personal work the restriction never bites; for anything billable it
is the first thing to read, and it is easy to miss behind a repository that otherwise looks like
every other npm package.
