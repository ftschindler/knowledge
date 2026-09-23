---
type: Reference
title: Sharing one user-level AGENTS.md across harnesses
description: A survey of the rule-file generator category, why every mature tool in it solves the
  project problem rather than the user-level one, and the two config lines that make a generator
  unnecessary here.
tags:
- research
- ai-agents
- agents
- opencode
- config-management
- tooling
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-23T00:00:00Z'
sources:
- id: agents-md
  resource: https://agents.md/
  title: 'AGENTS.md: a simple, open format for guiding coding agents'
  last_modified: '2026-09-23'
- id: opencode-rules
  resource: https://opencode.ai/docs/rules/
  title: Rules - opencode docs
  last_modified: '2026-09-22'
- id: opencode-src
  resource: https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/session/instruction.ts
  title: 'opencode: session/instruction.ts'
  last_modified: '2026-09-23'
- id: claude-memory
  resource: https://code.claude.com/docs/en/memory
  title: How Claude remembers your project
  last_modified: '2026-09-23'
- id: codex-agents-md
  resource: https://developers.openai.com/codex/guides/agents-md
  title: Custom instructions with AGENTS.md - OpenAI Codex
  last_modified: '2026-09-23'
- id: ruler
  resource: https://github.com/intellectronica/ruler
  title: 'Ruler: apply the same rules to all coding agents'
  last_modified: '2026-09-16'
- id: rulesync-global
  resource: https://rulesync.dyoshikawa.com/guide/global-mode
  title: 'Rulesync: Global Mode'
  last_modified: '2026-09-23'
- id: rulesync-tools
  resource: https://rulesync.dyoshikawa.com/reference/supported-tools
  title: 'Rulesync: Supported Tools and Features'
  last_modified: '2026-09-23'
---
**Context** - Felix keeps one always-on instruction file for every agent session, the digest
described in
[Teaching my agents to write better](../decisions/teaching_my_agents_to_write_better.md). It
sits at `~/.config/opencode/AGENTS.md`, a path [opencode](../tools/opencode.md) invented and
nothing else reads. The question was how to make that file portable across operating systems
and harnesses.

- **Read on**: 2026-09-23
- **Method**: vendor documentation read directly; repository metadata via `gh`; the two leading
  tools cloned and their READMEs read; opencode's instruction loader read at source.

There is a mature tool category for this, and surveying it answers the question by showing
that the question was the wrong size.

## The generators, and what they are for

Two tools lead a category of perhaps a dozen. **Ruler** has 2.9k stars and targets around
thirty agents[^ruler]. **Rulesync** has 1.5k stars and targets around fifty, across eight
surfaces - not just rules but ignore files, MCP servers, commands, subagents, skills, hooks
and permissions[^rulesync-tools]. Both are actively developed, both are TypeScript, both take
one source directory and compile it into each tool's native files.

The category is real, it is maintained, and adopting it would be the ordinary answer. It also
does not solve this problem, and the two tools fail to in different and instructive ways.

**Ruler writes only into the project.** Its `--global` flag creates a configuration at
`~/.config/ruler` used "when no local `.ruler/` directory is found" - a global *source*, whose
*outputs* still land in the repository[^ruler]. The README states the boundary as a safety
property: "Ruler never writes MCP configuration files outside your project root. Any
historical references to user home directories ... have been removed; only project-local paths
are targeted."[^ruler] Writing to `$HOME` is not a missing feature. It is a thing the tool
removed on purpose.

**Rulesync has a global mode, and it is three tools wide.** The tool matrix marks global
support against most of its fifty targets, but the Global Mode guide is narrower than the
matrix: "Currently, supports rules generation for Claude Code, GitHub Copilot, and
OpenCode."[^rulesync-global] Commands in global mode are Claude Code only.

So the category is built for a repository handing instructions to whichever agent a
contributor brought. The user-level file - one person, many harnesses, many machines - is the
long tail, and the coverage numbers that make these tools look decisive are project-scope
numbers.

## The three harnesses that do have global support

The reframing is that the narrow answer lands exactly on target. Rulesync's global rule
generation covers Claude Code, GitHub Copilot and opencode[^rulesync-global] - which is the
harness in use here, plus the two most likely to be added. Measured against the harnesses that
matter rather than against a catalogue, coverage is complete.

That makes rulesync a genuine option rather than a near-miss, and the decision becomes a
comparison rather than a search. What it costs is a compile step: a source directory, a
generate command, generated files in three home directories that no longer say where they came
from, and a fourth tool in the chain that has to keep tracking fifty moving targets. What it
buys, beyond the file itself, is the other seven surfaces - skills, commands, MCP servers,
permissions - kept in step by the same run.

## The two lines that make it unnecessary

opencode's `instructions` config key expands a leading tilde. The loader is one line:

```ts
const instruction = raw.startsWith("~/") ? path.join(global.home, raw.slice(2)) : raw
```

from `packages/opencode/src/session/instruction.ts`[^opencode-src]. This was the open question
left by the first version of this page, and the answer settles it: `"instructions":
["~/.agents/AGENTS.md"]` is machine-independent, so it can be committed to a config repository
shared across machines. The same file also shows opencode falling back to
`~/.claude/CLAUDE.md` when no global `AGENTS.md` exists[^opencode-src], which the documentation
describes as Claude Code compatibility[^opencode-rules].

Claude Code reaches the same file with `@~/.agents/AGENTS.md` in `~/.claude/CLAUDE.md`. Its
`@path` imports go four hops deep, and imports in a user-scope file are trusted without the
approval dialog a project file's external import triggers[^claude-memory].

**Two harnesses, two lines of configuration, no build step and nothing generated.** A
generator earns its keep when the ratio is worse than this - more harnesses, or more surfaces
than instructions alone. It is the wrong shape for two lines.

Codex is the one harness with no reference mechanism at all: it reads
`~/.codex/AGENTS.override.md` or `~/.codex/AGENTS.md` from `CODEX_HOME` and nothing
else[^codex-agents-md]. It takes a symlink, a copy, or rulesync - and it is the case that would
tip the decision if it arrived.

## Why no standard rescues this

`AGENTS.md` is a genuine convention, read by Codex, opencode, Amp, Cursor, Gemini CLI, Zed,
Warp, Aider and others, now stewarded by the Agentic AI Foundation[^agents-md]. **Every
statement it makes about discovery is about walking a directory tree inside a repository.** It
specifies nothing at user level, which is why five harnesses invented five paths and three
filenames, and why Claude Code lists `.agents/` among the directories it deliberately does not
read[^claude-memory].

`~/.agents/AGENTS.md` is therefore a name chosen rather than a location discovered. It is the
right name here because it is already the cross-harness home for skills in
[ftschindler/agents-skills](https://github.com/ftschindler/agents-skills), and because a file
every harness shares should not be named after one vendor.

Two constraints hold whatever mechanism is picked. **Symlinks lose on Windows**: creating one
needs Administrator rights or Developer Mode, and git checks a committed symlink out as a
one-line text file unless `core.symlinks` is set, which leaves that machine holding a
`CLAUDE.md` whose entire contents are the string `AGENTS.md`. Claude Code's own documentation
recommends the import over the symlink for exactly this reason[^claude-memory]. And **the file
stays short**: Codex stops adding instruction files at `project_doc_max_bytes`, 32 KiB by
default[^codex-agents-md], and Claude Code asks for under 200 lines and says plainly that
longer files reduce adherence[^claude-memory]. A user-level file is prepended to every session
in every repository, so its cost is paid every turn and never amortised - the same budget
argument
[Route a rule to the layer that reaches whoever must obey it](../principles/route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md)
makes from the other side.

## Bottom line

The generator category is mature and aimed elsewhere. Ruler will not write to `$HOME` by
design; rulesync will, for three tools, which happen to be the right three - so it is a real
alternative, not an absent one.

It is still the wrong size for two harnesses. One canonical file at `~/.agents/AGENTS.md`, an
`instructions` entry in opencode's config and an `@` import in `~/.claude/CLAUDE.md` gets the
content to both with no compile step and nothing generated. Revisit rulesync when a third
harness arrives without a reference mechanism, or when the thing being synchronised stops
being one markdown file and becomes skills, commands and MCP servers as well - which is the
threshold it was actually built for.

One thing this does not settle: the file is currently version-controlled inside the opencode
config repository, and `~/.agents` is a different repository with a different publishing
posture. That is a decision about where the content lives, not a path change.
