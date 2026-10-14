---
type: Guide
title: Uninstall git-ai and the state it left in every repository
description: Removing git-ai means four separate removals in a fixed order, because its daemon
  reinstalls agent hooks daily and its per-repository data outlives the binary by a long way.
tags:
- guide
- git-ai
- git
- agents
- provenance
- linux
status: stable
stale_after: '2027-04-09'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T10:40:00+02:00'
sources:
- id: git-ai-uninstall-section
  resource: https://ftschindler.github.io/running-linux/done/20260624-git-ai-integration-with-opencode/
  title: Git AI Integration with OpenCode
  author: human:felix_schindler
  last_modified: '2026-06-24'
---
[git-ai](../tools/git_ai.md) installs itself into four places that have nothing to do with each
other, and the removal instructions in general circulation cover two of them. The write-up this
machine's own installation followed[^git-ai-uninstall-section] names the home directory, the
`PATH` line and the editor extension, and stops there. What it leaves out is everything the tool
wrote whilst it was running, which on one machine after three and a half months was 125 `.git/ai`
directories and 19 repositories carrying a `refs/notes/ai` ref.

The steps below are in the order they have to run in. The first two are the ones whose order is
not arbitrary.

## 1. Take the agent hooks off first, whilst the binary still exists

```bash
git-ai uninstall-hooks
```

It reports per agent, and it removed hooks from Claude Code, GitHub Copilot and opencode here.
Running it before deleting `~/.git-ai` is what makes it available at all, and it is also what
stops the hooks being orphaned: each one is a file naming an absolute path to the binary, so a
binary deleted first leaves hooks that fail on every tool call rather than hooks that are gone.

Two things it does not do. It does not touch the VS Code extension, and says so in its own
output. And it is not a way of switching the tool off on its own, because **the daemon reinstalls
the hooks daily**: the removal holds only until step 2.

Read [the finding about this command](../findings/20261009_git_ai_uninstall_hooks_has_no_help_flag_and_uninstalls_when_asked_for_one.md)
before running anything exploratory near it.

## 2. Stop the daemon and remove the home directory

```bash
pkill -f 'git-ai bg'
rm -rf ~/.git-ai
```

`~/.git-ai` holds the binary, `config.json`, and SQLite databases of metrics and session
transcripts. It had reached 365 MB. Nothing else on the system owns it: the installer is a shell
script, so there is no package to remove and `pacman -Qo` on the binary reports no owner.

## 3. Take the `PATH` line out of every shell rc file

The installer appends to each rc file it recognises, and dates what it wrote:

```text
# Added by git-ai installer on Wed 24 Jun 14:03:34 CEST 2026
export PATH="$HOME/.git-ai/bin:$PATH"
```

It had written that into both `~/.zshrc` and `~/.bashrc` here. Some installations get a symlink
at `~/.local/bin/git-ai` instead, so check for that too.

**Read what you are about to delete rather than grepping for the name and removing every hit.**
`git-ai` is an unremarkable thing to call a shell function, and this machine had an unrelated one
of exactly that name, switching git identities for agent work. A sweep by name would have taken
it.

## 4. Remove the editor extension

```bash
code --uninstall-extension git-ai.git-ai-vscode
```

The uninstaller declines this deliberately and prints a line saying so, which is easy to miss
amongst the successes above it. The same extension id serves Cursor, Windsurf and Antigravity, so
remove it from each editor that has it.

## 5. Sweep the per-repository data

This is the step with no command in any official instruction, and the one that accounts for
almost all of what is left. Two kinds of state, in two passes.

The checkpoint logs, one directory per repository the tool ever saw:

```bash
find ~ -type d -name ai -path '*/.git/*' -not -path '*/.git/ai/*' -prune -exec rm -rf {} +
```

Then the notes, which are refs rather than files and have to be deleted through git so the
repository stays consistent:

```bash
find ~ -type f -path '*/.git/refs/notes/ai' -printf '%h/../../..\n' | while read -r repo; do
  git -C "$repo" update-ref -d refs/notes/ai
  git -C "$repo" for-each-ref --format='%(refname)' refs/notes/ai-remote \
    | xargs -r -n1 git -C "$repo" update-ref -d
done
```

List before deleting. Most of the hits are throwaway, in package manager caches and docker
volumes, and the handful that are real work are worth looking at rather than sweeping, because a
note is the only copy of what it records.

## 6. Decide about the notes that are already on a remote

A repository with a `refs/notes/ai-remote/origin` ref has pushed its notes, and steps 5 deletes
the local copy only. The remote keeps them, a fetch brings them back, and anyone who has cloned
already has them:

```bash
git push origin :refs/notes/ai
```

Run that per repository, and only where the notes are actually unwanted. This is the one step
that is visible to other people, and the one that cannot be undone from the machine you are
standing at.

## 7. Undo the per-repository git config

The June setup added two settings to each repository that used the tool, which now refer to a ref
that no longer exists:

```bash
git config --unset-all remote.origin.fetch '\+refs/notes/ai:refs/notes/ai'
git config --unset push.defaultNotesRef
```

Harmless if left: a fetch refspec for a ref the remote does not have is not an error. Worth
removing anyway, because the next person to read that config will spend a minute working out what
put it there.
