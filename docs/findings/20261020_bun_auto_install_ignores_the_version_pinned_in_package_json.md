---
type: Finding
title: Bun's auto-install ignores the version pinned in package.json
description: Running a script with bun and no node_modules resolves the latest release of each
  dependency, whatever package.json declares, so the clean working directory costs the pin.
tags:
- finding
- bun
- npm
- uv
- agent-skills
- supply-chain
status: stable
stale_after: '2027-04-20'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-20T16:40:00+02:00'
---
Packaging an agent skill that wraps a node library, the question was where its dependencies
should live. A skill directory holding 143 MB of `node_modules` is unappealing, and
[bun](https://bun.sh)'s auto-install appears to solve it: run the script with no
`node_modules` present and bun resolves the imports into a shared cache, leaving the directory
untouched.

It does exactly that, and it also quietly stops honouring the version you pinned.

## The measurement

A directory holding one script and a `package.json` pinning an exact version, with no
`node_modules`:

```json
{ "name": "t", "type": "module", "dependencies": { "ms": "2.0.0" } }
```

```text
$ bun run v.mjs
ms version: 2.1.3

$ bun install
+ ms@2.0.0 (v2.1.3 available)
$ bun run v.mjs
ms version: 2.0.0
```

The exact pin is in the file both times. Auto-install reads the import and fetches the current
release; `bun install` reads the manifest and honours it, at the cost of writing
`node_modules/` and `bun.lock` back into the directory.

Pinning in the import specifier instead does not work either. `import {x} from 'pkg@6.10.8'`
fails with `Unexpected while resolving package`, on bun 1.4.2.

On the real skill the gap was two minor versions: the lockfile pins `db-vendo-client` 6.10.8,
and auto-install produced 6.11.3. The audited tree and the running tree were not the same tree,
and nothing said so.

## The three layouts, and what each costs

| Model | In the skill directory | Packages live in | Pinned |
| --- | --- | --- | --- |
| `npm ci` against a lockfile | `node_modules/`, 143 MB, 45 entries | the skill directory | yes |
| `bun run` auto-install | nothing | `~/.bun/install/cache` | **no** |
| `uv run --script` with [PEP 723](https://peps.python.org/pep-0723/) | nothing | `~/.cache/uv` | yes |

The Python row is the one that gets both, and it is worth naming why rather than envying it.
Inline metadata puts the dependency declaration **in the file being run**, so there is no
second manifest for the resolver to disagree with, and `uv lock --script` writes a lockfile
beside it without putting an environment there. Node has no equivalent short of changing
runtime: Deno's `npm:pkg@version` specifiers would do it, which is a third toolchain to install
to run one script.

## What this settles for a skill

Take the `node_modules`, and populate it with `npm ci` rather than `npm install`. A skill is
installed by copying a directory, so an artefact beside `SKILL.md` is in the one place the
format can carry, and 143 MB buys a dependency tree that matches the one that was read. A
shared cache that silently floats is the wrong trade for anything whose contents were audited,
which is the position any skill that reaches the network is in; the case that prompted this is
[the deutsche-bahn skill](../investigations/deutsche_bahn_skill_security_and_telemetry.md).

**`npm ci` is the half of that worth stating separately.** It treats the committed lockfile as
authoritative and refuses when the manifest disagrees with it, where `npm install` may update
the lockfile to resolve the difference. A command that can rewrite the pin is the wrong one to
reach for when the pin is the entire reason for choosing this layout.

This is the same shape as
[an unpinned puppeteer replacing the Chrome pinned beside it](20261009_an_unpinned_puppeteer_replaces_the_chrome_pinned_beside_it.md):
a version was stated, something else decided which version ran, and the arrangement looked
pinned from the outside. Here the deciding thing is not a library but the choice of install
command, which is easier to miss because neither command announces that it overrode anything.
