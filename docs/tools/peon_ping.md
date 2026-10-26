---
type: Tool
title: peon-ping
description: Warcraft III voice lines played from agent lifecycle hooks, and the install footprint
  that reaches twelve hook events, a shell alias and a plaintext log of every prompt.
tags:
- tools
- peon-ping
- claude-code
- notifications
- ai-agents
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-15T22:45:00+02:00'
sources:
- id: peon-ping-repo
  resource: https://github.com/PeonPing/peon-ping
  title: 'PeonPing/peon-ping: Warcraft III Peon voice notifications (+ more!) for Claude Code,
    Codex, IDEs, and any AI agent'
  last_modified: '2026-10-15'
- id: peon-ping-site
  resource: https://www.peonping.com
  title: PeonPing
  last_modified: '2026-10-15'
---
peon-ping[^peon-ping-repo] plays a Warcraft III Peon voice line when an agent finishes a task,
hits an error or asks for permission: "Work work", "Zug zug", "Me not that kind of orc". It
answers the real problem of having to watch a terminal for a prompt that may not come for
minutes, and it answers it with sound rather than a notification you also have to look at.

| | |
| --- | --- |
| Author | `garysheng`, under the PeonPing organisation |
| Licence | MIT |
| Language | Shell |
| Distribution | `curl -fsSL https://raw.githubusercontent.com/PeonPing/peon-ping/main/install.sh \| bash` |
| Source | [github.com/PeonPing/peon-ping](https://github.com/PeonPing/peon-ping) |
| Site | [peonping.com](https://www.peonping.com) |
| Version read | 2.22.0 |

It keeps its plain name here rather than carrying its author's, because PeonPing is a vendor
with a site behind the repository[^peon-ping-site], which is the same exception [uv](uv.md)
gets.

## What it actually hooks

The sound is the feature; the hook surface is the thing worth knowing before installing. The
installer writes one command into twelve Claude Code lifecycle events - `SessionStart`,
`SessionEnd`, `Stop`, `SubagentStart`, `SubagentStop`, `UserPromptSubmit`, `PreToolUse`,
`PostToolUseFailure`, `PreCompact`, `Notification`, `PermissionRequest` - each invoking the
same 218 KB `peon.sh`. Two further scripts sit on `UserPromptSubmit` to catch its own slash
commands before they reach the model.

Events are mapped to a vendor-neutral set the project calls CESP: `session.start`,
`task.acknowledge`, `task.complete`, `task.error`, `input.required`, `resource.limit`,
`user.spam`. Each is a boolean in `config.json`, so a category can be silenced without
unhooking anything. Packs are directories of sound files behind a manifest, and six ship with
it, including GLaDOS and two StarCraft voices; a registry at `peonping.github.io` serves more.

Beyond sound it will set tab titles, raise desktop notification popups, speak through TTS,
forward to a phone via Pushover, Telegram or ntfy, and - in a feature called the trainer -
interrupt periodically to tell you to do pushups.

## Where it puts itself

Five places, of which the installer announces about two:

| Layer | What lands there |
| --- | --- |
| `~/.claude/hooks/peon-ping` | The scripts, six sound packs, config, state, the trainer and its own `uninstall.sh`. 7.2 MB |
| `~/.claude/settings.json` | Twelve hook entries, all pointing at `peon.sh` |
| `~/.claude/skills` | Four skills: `peon-ping-toggle`, `-config`, `-use`, `-log` |
| Shell startup | Three lines in `.bashrc`: a comment, `alias peon=`, and a completions `source` |
| `~/.local/bin/peon` | A symlink to `peon.sh`, in addition to the alias |
| `~/.openpeon` | An alternative pack data directory the script falls back to when the install directory has none |

Two of those deserve naming on their own. **It logs every prompt you type**, to
`hook-handle-use.log` and `hook-handle-rename.log` beside the install, in plaintext, with no
rotation, each line carrying the opening clause of a prompt. A few months of ordinary use runs
to thousands of lines. The scripts are reading `UserPromptSubmit` to find their own commands
and recording what they saw on the way past. And **it checks for updates against GitHub and the
pack registry**, so an installed copy reaches the network on its own schedule.

## Uninstalling it

`uninstall.sh` ships beside the install and does the hard parts correctly: it strips the hook
entries by matching on the command rather than rewriting the file, leaves unrelated hooks
alone, removes the `.bashrc` lines, and deletes the install directory. It runs
non-interactively unless it finds a `notify.sh.backup` to restore.

It misses three things, all of them additions that outgrew its hardcoded lists:

- `~/.local/bin/peon`, which survives as a dangling symlink on `PATH`
- `~/.openpeon`, never referenced by it
- the `peon-ping-log` skill, because the script names only the original three

A full removal is the script plus those three paths. The logs go with the install directory,
which is the right outcome but a one-shot one: anything worth keeping has to come out first.

## What it is worth

The idea is sound and the execution is a 218 KB shell script with a vendor's registry, a
phone-notification fleet and a pushup reminder attached. For an agent that already reports
completion in a way you can see, the sound is decoration; the twelve hooks and the prompt log
are not. A notification hook is a reasonable thing to want, and this is more surface than that
want justifies.

Mine went unused for months before it went, which is its own verdict on the feature.
