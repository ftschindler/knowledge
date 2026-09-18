---
type: Tool
title: opencode
description: The terminal coding agent this knowledge base is written through, and the layered config
  model that lets one machine hold several isolated provider setups.
tags:
- tools
- opencode
- agents
- config-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: opencode-repo
  resource: https://github.com/anomalyco/opencode
  title: 'anomalyco/opencode: the open source coding agent'
  last_modified: '2026-09-18'
- id: felix-opencode-config
  resource: https://github.com/ftschindler/opencode
  title: 'ftschindler/opencode: my opencode configuration'
  author: human:felix_schindler
  last_modified: '2026-09-18'
---
opencode[^opencode-repo] is a coding agent that runs in a terminal rather than in an editor.
It is the harness named in the `generated.by` field of nearly every page here, so it is
already the most-cited tool in this bundle and has until now been the only one without a page
of its own.

| | |
| --- | --- |
| Author | Anomaly (`anomalyco`), with the project's own site at [opencode.ai](https://opencode.ai) |
| Licence | MIT |
| Language | TypeScript, with a Go terminal interface |
| Distribution | A standalone installer, npm, and distro packages; on Manjaro it arrives as the AUR package `opencode-bin` |
| Source | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) |
| Version read | 1.18.23 |
| My configuration | [github.com/ftschindler/opencode](https://github.com/ftschindler/opencode)[^felix-opencode-config], cloned to `~/.config/opencode` |

## What it is

A session is a model, a set of tools and a working directory. What makes it configurable
rather than fixed is that four separate things extend it, and they are worth keeping apart
because they fail in different ways:

| | |
| --- | --- |
| **Providers** | Who serves the model. Enabled per config, authenticated either by an API key or by an interactive sign-in |
| **Plugins** | npm packages or local TypeScript files that add agents, commands and behaviour |
| **Skills** | Directories of Markdown instructions, loaded on demand when a task matches one |
| **MCP servers** | External processes speaking [Model Context Protocol](https://modelcontextprotocol.io), each contributing tools |

The last of those is the one whose provenance is easiest to misread. The servers a session
lists are not all declared in the config: a plugin may inject its own, so `opencode mcp list`
routinely shows more than the config file explains, and a name chosen without checking that
list can collide with one that was never written down.

Two commands answer almost every question about what a session actually resolved to, and both
are worth reaching for before reading a config file and inferring:

| | |
| --- | --- |
| `opencode debug config` | The fully resolved configuration, after every layer has been merged |
| `opencode mcp list` | Each MCP server and whether it is connected, disabled or failing |

## How I configure it

`OPENCODE_CONFIG_DIR` points opencode at a directory other than `~/.config/opencode`, and my
configuration uses that to keep **one directory per provider**, so a session sees exactly one
provider and never two at once. That isolation is the point: providers differ in what they may
be shown, and a base config that enables nothing at all means a missing environment variable
fails loudly instead of quietly picking one.

The part that is not obvious from the outside, and that I got wrong until I tested it, is that
a profile does **not** replace the base config:
[opencode merges a profile over the base config rather than replacing it](../findings/20260918_opencode_merges_a_profile_over_the_base_config_rather_than_replacing_it.md).
So the split is between what varies by provider and what does not. Credentials, the enabled
provider and the default model live in the profile. Anything provider-agnostic is written once
in the base config, which is where [markitdown](markitdown.md) is declared, and every profile
inherits it.
