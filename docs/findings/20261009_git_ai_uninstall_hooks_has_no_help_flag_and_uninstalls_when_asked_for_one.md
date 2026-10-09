---
type: Finding
title: git-ai uninstall-hooks has no help flag and uninstalls when asked for one
description: Appending --help to the subcommand does not describe it, it runs it, so a command
  issued to find out what a command would do removes the agent hooks from every installed agent.
tags:
- finding
- git-ai
- git
- agents
- dx
status: stable
stale_after: '2027-04-09'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T10:50:00+02:00'
---
`git-ai uninstall-hooks --help` does not print usage. It uninstalls the hooks, and reports what
it removed:

```text
Coding Agents
✓ Claude Code: Hooks removed
✓ VS Code: No hooks to remove
⚠ VS Code: Extension must be uninstalled manually through the editor
✓ OpenCode: Hooks removed
```

The flag is not rejected and it is not reported as unknown. It is read as an argument to a
subcommand that takes none, ignored, and the subcommand proceeds.

## What it cost

One session, planning how to remove [git-ai](../tools/git_ai.md) from a machine, asked the
command what it would do before deciding whether to run it. The hooks came off Claude Code,
GitHub Copilot and opencode, and the opencode plugin file was deleted, at the point where the
question was still being researched rather than answered.

Nothing was lost: the removal is reversible with `git-ai install-hooks`, which regenerates the
plugin with the binary's absolute path in it. What it changed was the order of the work, and that
is the shape of the risk here rather than the data loss there was not.

## Why it is worth a page

`--help` is the one flag it is safe to try on an unfamiliar command, and a CLI that treats it as
noise rather than as a request turns reconnaissance into execution. The ordinary habit for
reading a new tool, run the subcommand with `--help` and see what comes back, is unsafe against
this one.

The flag that works is at the top level. **Run the bare command and read its own listing, rather
than asking a subcommand to describe itself**, whenever the subcommand's name suggests it
changes something.

This is a claim about version 1.5.13, which is the release the shell installer put down in June
2026 and which `disable_auto_updates` held in place.
