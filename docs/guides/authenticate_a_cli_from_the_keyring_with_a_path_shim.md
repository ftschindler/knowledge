---
type: Guide
title: Authenticate a CLI from the keyring with a PATH shim
description: How to feed a token to a CLI that reads one only from the environment, without
  exporting it into every shell, and why a shell function cannot do the job on a machine that runs
  coding agents.
tags:
- guide
- secrets
- keyring
- secret-tool
- cli
- agents
- linux
status: stable
stale_after: '2027-04-23'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-23T11:05:00+02:00'
---
Several CLIs take their credential from one environment variable and nowhere else.
[jira-cli](https://github.com/ankitpokhrel/jira-cli) keeps the account and the auth type in
`~/.config/.jira/.config.yml` but reads the token only from `JIRA_API_TOKEN`. The obvious place to
put that is `~/.bashrc`, which then hands the token to every process started from any terminal for
the rest of the session.

A shim removes the export without the CLI noticing. The token is fetched from the system keyring
at the moment of the call, lives in one process, and is gone when that process exits.

Commands are as of `secret-tool` from libsecret 0.21 on a KDE desktop, where the Secret Service is
KWallet. GNOME Keyring answers the same interface.

## 1. Put the secret in the keyring

```bash
secret-tool store --label='Jira API token' service jira account felix.schindler@example.com
```

It reads the value from stdin and prints nothing. The attribute pairs after the label are
arbitrary, and they are also the lookup key, so whatever is chosen here has to be repeated
verbatim in step 2.

## 2. Write the shim

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/jira <<'EOF'
#!/bin/bash
# jira-cli reads its token only from JIRA_API_TOKEN. Fetch it from the keyring for the
# duration of this one process rather than exporting it into every shell.
export JIRA_API_TOKEN="$(secret-tool lookup service jira account felix.schindler@example.com)"
exec /usr/bin/jira "$@"
EOF
chmod +x ~/.local/bin/jira
```

Two details that are not decoration. **`exec` with the absolute path**, because a shim that calls
the bare name finds itself and recurses. And `~/.local/bin` has to precede the real binary's
directory in `PATH`, which is the default on most distributions; `command -v jira` says which one
wins.

## 3. Check it from a shell that is not yours

```bash
env -u JIRA_API_TOKEN bash -c 'jira me'
```

This is the check worth running, because the interactive shell is the one case that would have
worked anyway. It answers with the account name when the shim is doing its job.

## Why not a shell function

A function in `~/.bashrc` looks like it solves the same problem for a third of the typing. It does,
for a human typing at a prompt, and for nobody else.

**Bash does not read any rc file when it is neither interactive nor a login shell.** That is the
shell a coding agent gets: `declare -F` in one of them lists nothing, on a machine whose `.bashrc`
defines several functions. The CLI an agent invokes is the real binary, with no token in its
environment, and the failure surfaces as an authentication error from a tool the agent was told
was authenticated. It then retries, or goes looking for credentials, neither of which ends well.

A shim is a file on disk with an executable bit. It serves the prompt, the agent, a Makefile and a
systemd unit identically, because none of them has to be a shell at all.

## What this does and does not buy

The token stops being ambient. It is absent from `env`, from `/proc/<pid>/environ`, and from every
process that did not ask for it by name, which is most of them.

It remains reachable: anything that can run `secret-tool lookup` can read it, including an agent
with a shell. The difference is that reading it becomes a command somebody can see in a log rather
than a side effect of inheritance. Treat that as a reduction in exposure, not a boundary.

Two rough edges worth knowing before relying on it:

- **A locked wallet prompts.** `secret-tool` against a locked KWallet raises a GUI unlock dialog,
  which from a background agent run arrives with no obvious cause. KDE unlocks the wallet at login
  when its password matches the login password; confirm that before depending on the shim in
  unattended work.
- **`env` becomes a dead end for debugging.** Anyone, human or agent, who checks for the variable
  finds nothing and may conclude the tool is unauthenticated. The comment inside the shim covers
  whoever opens the file, and a line in the repository's `AGENTS.md` covers the agent that does
  not.

For variables that are settings rather than secrets, scoping them to a project with
[direnv](get_started_with_direnv_on_linux.md) is the lighter tool, and the two compose: direnv
carries the harmless ones, the shim carries the credential.
