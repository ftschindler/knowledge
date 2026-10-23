---
type: Guide
title: Get started with direnv on Linux
description: Installing direnv, hooking it into the shell and writing a first .envrc, with the trust
  model that decides when it runs and the limit that makes it hygiene rather than a boundary.
tags:
- guide
- direnv
- shell
- linux
- secrets
- dx
status: stable
stale_after: '2027-04-23'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-23T10:15:00+02:00'
sources:
- id: direnv-hook
  resource: https://direnv.net/docs/hook.html
  title: 'direnv: Setup'
  last_modified: '2026-10-23'
---
direnv keeps environment variables with the directory they belong to. It hooks the shell prompt,
and on every directory change it looks for an `.envrc` in the current directory or above. Finding
one, it runs that file in a subshell and applies the resulting environment to the current shell.
Leaving the directory reverses it: variables direnv set are unset, and ones it overwrote go back
to their previous values.

The use that pays for itself is the project that needs three variables nothing else on the
machine wants. They exist whilst working on it and nowhere else, which is a smaller blast radius
than a login shell that carries them into every terminal for the rest of the week.

## 1. Install it

```bash
sudo apt-get install direnv   # Debian and Ubuntu derivatives
sudo pacman -S direnv         # Arch derivatives
```

## 2. Hook it into the shell

direnv does nothing until the shell calls it. Add the hook at the **end** of the shell's rc file,
after anything else that manipulates the prompt[^direnv-hook]:

```bash
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc   # bash
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc     # zsh
```

Restart the shell afterwards. The hook runs before each prompt, which is why the load happens on
the directory change rather than at some later point.

## 3. Write an `.envrc`, then allow it

```bash
cd ~/Projects/example
echo 'export API_BASE=https://staging.example.com' > .envrc
direnv allow
```

The second command is not a formality. `.envrc` is arbitrary shell, so direnv refuses to run one
it has not been shown: it records a hash of the approved content and blocks anything else, which
means cloning somebody's repository is not enough to execute their code. Editing a single
character invalidates the hash, and the file is blocked until `direnv allow` runs again.

Entering the directory now prints `direnv: loading .envrc` and `direnv: export +API_BASE`.
Leaving it prints `direnv: unloading`.

For secrets, keep the values out of the file and fetch them from the system keyring when the file
loads:

```bash
export EXAMPLE_API_TOKEN="$(secret-tool lookup service example-api account default)"
```

The `.envrc` is then a recipe rather than a secret, and safe to read.

## 4. Keep `.envrc` out of shared repositories

An `.envrc` in a repository that does not ignore it shows up as untracked, one `git add -A` away
from being committed. Ignore it once, globally, rather than per repository:

```bash
git config --global core.excludesfile ~/.gitignore
printf '.envrc\n.direnv/\n' >> ~/.gitignore
```

It being a dotfile is the other half of the same tidiness, for the reason
[Make support-tool config files dotfiles](../principles/make_support_tool_config_files_dotfiles.md)
gives: tool plumbing recedes and the repository root still reads as the project's contents.

## What direnv does not do

**It is not a secret store, and it is not protection against anything running in that
directory.** Once loaded, the variables sit in the environment of the shell, so every process
started from there inherits them: build scripts, package manager hooks, and any coding agent
working on that project. Reading them takes one `env`.

What it buys is that they are absent everywhere else. For a secret that must stay out of reach of
what runs in the project itself, the environment is the wrong place entirely, and a wrapper
function that fetches it into one command is the shape that delivers that:

```bash
jira() { JIRA_API_TOKEN=$(secret-tool lookup service jira account felix) command jira "$@"; }
```

The two compose. direnv carries the harmless settings, and the wrapper carries the secret.
