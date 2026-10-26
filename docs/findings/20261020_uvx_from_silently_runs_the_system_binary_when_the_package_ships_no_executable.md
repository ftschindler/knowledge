---
type: Finding
title: uvx --from silently runs the system binary when the package ships no executable
description: A command named after a distribution that declares no console scripts resolves on PATH
  instead, so the run succeeds, reports a plausible version, and never touches the package.
tags:
- finding
- uv
- node
- tooling
- supply-chain
status: stable
stale_after: '2027-04-20'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-20T17:10:00+02:00'
---
Checking whether a node toolchain could be fetched on demand the way [uv](../tools/uv.md)
fetches a Python one, the obvious command answered correctly:

```text
$ uvx --from nodejs-wheel-binaries node --version
 Downloaded nodejs-wheel-binaries
Installed 1 package in 59ms
v26.8.1
```

A download, an install, and a version. The distribution does bundle a 126 MB node binary, so
every part of that reads as the thing working.

It was the system node. `process.execPath` is what says so:

```text
$ uvx --from nodejs-wheel-binaries node -e "console.log(process.execPath)"
/usr/bin/node
```

The version matched because the machine happened to have the same release installed, which is
what made the result convincing rather than merely wrong.

## What is actually happening

`nodejs-wheel-binaries` declares **no console entry points**. Its binaries sit inside the
package directory and no script is installed into the ephemeral environment's `bin`. When the
named command is not there, `uvx` resolves it on `PATH` like any other command, and runs it.

The fallthrough is not node-specific. Any name on `PATH` will do:

```text
$ uvx --from nodejs-wheel-binaries ls /etc/hostname
/etc/hostname
```

The part worth keeping is that **uv knows, and says so only when it cannot fall through**:

```text
$ uvx --from nodejs-wheel-binaries definitely-not-a-real-cmd
Package `nodejs-wheel-binaries` does not provide any executables.
```

That sentence is the whole diagnosis, and it is printed exactly when it is not needed. Ask for
a command that exists on the machine and the same condition produces a silent success instead.
`--with` behaves the same way.

## Getting the bundled binary

The package exposes its executables as Python callables, with a `__main__` for node only:

```sh
uvx --from nodejs-wheel-binaries python -m nodejs_wheel -e "console.log(process.execPath)"
# /home/felix/.cache/uv/archive-v0/.../nodejs_wheel/bin/node

uvx --from nodejs-wheel-binaries python -c \
  "import sys; from nodejs_wheel import npm; sys.exit(npm(['install','--ignore-scripts']))"
```

There is no `-m` form for `npm`, `npx` or `corepack`. `nodejs-bin`, the sibling distribution,
falls through in the same way.

## How to not be fooled by it

**Ask the binary where it is, not what version it is.** A version string is the weakest
possible evidence here, because the likeliest reason a command is on `PATH` at all is that the
same software is installed system-wide, so the two answers agree precisely when they are two
different programs. `process.execPath`, `which`, `sys.executable` or `--version` compared
against a *deliberately different* pinned version all distinguish them; the bare version does
not.

This generalises past `uvx`. Any tool that runs a named command in an environment it prepared
can fall back to the ambient one, and the failure is invisible whenever the ambient one is
close enough to work. It is the same reading error as
[an unpinned puppeteer replacing the Chrome pinned beside it](20261009_an_unpinned_puppeteer_replaces_the_chrome_pinned_beside_it.md):
output that looks like the isolated thing succeeding, produced by the machine's own copy.
