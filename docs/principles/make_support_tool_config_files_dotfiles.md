---
type: Principle
title: Make support-tool config files dotfiles
description: Name support-tool config files as dotfiles so the repo root shows the project's content and
  tool plumbing recedes.
tags:
- principle
- software
- repo-hygiene
- dx
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Name every support-tool configuration file as a dotfile
(`.taplo.toml`, `.markdownlint-cli2.jsonc`, `.biome.json`) rather than a plain
name in the repo root, so the root shows the project's actual content and tool
plumbing recedes into the hidden layer.

**When to apply.** Any repo with several linter/formatter/build-tool configs.
The more tools you add, the more a plain-named config set clutters `ls` and
buries the files that matter (source, README, the one or two real manifests).

**Why.** A repo root is a table of contents. Every `biome.json`, `taplo.toml`,
`checkmake.ini` sitting there competes for attention with the code and docs a
newcomer actually needs to find. Most tools already treat their dotfile and
plain-file config names as equivalent (they search for both), so hiding them
costs nothing and keeps the root legible. It also groups "this is tool wiring,
not project content" visually, the same signal `.git`, `.github`, and
`.editorconfig` already send.

**How enforced.** Convention when adding a tool: reach for the dotted config
name first. Verify the tool actually discovers it before renaming - **some tools
hardcode a non-dot name** and only read the dotfile via an explicit flag. Two
real cases:

- **taplo** auto-discovers both `.taplo.toml` and `taplo.toml` - rename freely.
- **checkmake** auto-reads only `checkmake.ini`; to use `.checkmake.ini` you must
  pass `--config=.checkmake.ini` in the hook. Do it, and leave a one-line comment
  on the flag so nobody "cleans it up" and silently reverts to built-in defaults
  (a [Verify a pre-commit hook's file-type filter actually matches your file](verify_a_pre_commit_hooks_file_type_filter_actually_matches_your_file.md)-style
  silent-no-op trap).

The exception is a config that is *itself* project content or a documented entry
point (a published `workspace.okf.yaml.example`, a root `package.json` consumers
install) - those stay plainly named on purpose.
