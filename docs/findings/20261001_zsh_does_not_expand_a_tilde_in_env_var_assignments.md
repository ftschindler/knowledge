---
type: Finding
title: zsh does not expand a tilde in env VAR=~/path, and opencode creates the literal directory
description: An unexpanded tilde after env makes OPENCODE_CONFIG_DIR a relative path, which opencode
  silently creates rather than rejecting, so commands run against a provider-less config.
tags:
- finding
- opencode
- zsh
- config-management
status: stable
stale_after: '2027-04-01'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-01T16:45:00+02:00'
---
Two innocuous behaviours compose into a confusing one. `opencode run --model <anything>` failed
with `UnknownError: Unexpected server error` for every model I tried, including one I was
sitting in a working session of, which read as a provider outage or a rejected credential. It
was neither.

The command was:

```sh
env OPENCODE_CONFIG_DIR=~/.config/opencode/profiles/github-copilot opencode run ...
```

zsh expands a tilde after `=` only in a real assignment, or with `MAGIC_EQUAL_SUBST` set. In
`env VAR=~/path` the whole thing is an ordinary command argument, so the tilde survives as a
literal character and the variable holds the relative path `~/.config/opencode/...`. The same
tilde in `export VAR=~/path`, or in the command-prefix form `VAR=~/path opencode ...`, expands
normally - which is why most of my commands that day worked and three did not.

opencode then **creates a missing config directory rather than failing**, so the relative path
produced a real directory named `~` under the current working directory:

```text
./~/.config/opencode/profiles/github-copilot/
```

It contained no `opencode.json`, so the session enabled no providers - my base config sets
`enabled_providers: []` deliberately, to fail closed. The session therefore had no model to
reach and reported it as a server error rather than as a missing provider. opencode had also
populated it with a `node_modules` tree, 276 directories, which is what made it visible at all:
it showed up in a recursive diff against a backup taken an hour earlier.

## How to tell

Two cheap checks, both faster than debugging the error:

- `ls -d './~'` in the directory you ran from. A literal tilde directory is never intentional.
- Print the variable as the child sees it: `env VAR=~/x sh -c 'echo "$VAR"'` shows `~/x`,
  whilst `VAR=~/x sh -c 'echo "$VAR"'` shows the expanded path.

Use `"$HOME/..."` rather than a tilde whenever the assignment is an argument to another command.
It expands in every shell and in every position, which a tilde does not.

The general shape is worth more than the specific bug: a tool that silently creates a missing
config directory converts a typo into a plausible-looking empty configuration, and every error
after that describes the empty configuration rather than the typo. The symptom appears at the
first operation that needed a setting, arbitrarily far from the cause.

Observed with opencode 1.18.33 under zsh.
