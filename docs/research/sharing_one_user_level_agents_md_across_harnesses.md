---
type: Reference
title: Sharing one user-level AGENTS.md across harnesses
description: A survey of the tools that distribute one ruleset to many coding agents, why almost all
  of them refuse the home directory, and the two config lines that make one unnecessary here.
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
- id: vibe-rules
  resource: https://www.npmjs.com/package/vibe-rules
  title: 'vibe-rules: a utility for managing Cursor rules, Windsurf rules and other AI prompts'
  last_modified: '2025-08-21'
- id: ai-rules-sync
  resource: https://www.npmjs.com/package/ai-rules-sync
  title: 'ai-rules-sync: synchronize, manage and share your AI rules, skills, commands and subagents'
  last_modified: '2026-08-20'
---
**Context** - Felix keeps one always-on instruction file for every agent session, the digest
described in
[Teaching my agents to write better](../decisions/teaching_my_agents_to_write_better.md). It
sits at `~/.config/opencode/AGENTS.md`, a path [opencode](../tools/opencode.md) invented and
nothing else reads. The question was how to make that file portable across operating systems
and harnesses.

- **Read on**: 2026-09-23
- **Method**: vendor documentation read directly; the tool population enumerated by repeated
  GitHub repository search and npm registry search, then each candidate's star count and last
  push read through `gh` and its README read for the words `global`, `$HOME` and `~/.`;
  opencode's instruction loader read at source.

There is a crowded tool category for this, and surveying it answers the question by showing
that the question was the wrong size.

## The population, and the two things it splits into

Searching for these tools returns dozens, which is the expected shape for anything in this
ecosystem. Nearly all of them are answering a different question.

**The bulk of the count is content generators**: point one at a repository and it inspects the
package manager, scripts and CI and writes an `AGENTS.md` describing what it found. A single
search phrase returns thirty of these, almost all under ten stars. They produce a first draft
of a project file, which is not a distribution problem and has nothing to say about where a
user-level file lives.

**The distributors are the relevant category**, and there the count is smaller and the
adoption curve brutal:

| Tool | Stars | Last push | Writes to `$HOME`? |
| --- | --- | --- | --- |
| Ruler | 2.9k | 2026-09 | No, by explicit design[^ruler] |
| Rulesync | 1.5k | 2026-09 | Rules, for three tools[^rulesync-global] |
| vibe-rules | 528 | 2025-08 | Yes, four tools[^vibe-rules] |
| ai-rulez | 143 | 2026-09 | No |
| ai-rules-sync | 38 | 2026-08 | Yes, `--user`[^ai-rules-sync] |
| airul | 34 | 2025-09 | No |
| rulix, airules, dev-spec | 0-4 | 2025-10 to 2026-09 | Not documented |

Two tools hold the category, a third is an order of magnitude behind, and below that is a tail
of projects with no users. So the explosion is real in count and thin in adoption, which is a
different thing from the category being empty.

## Writing to the home directory is the rare feature

**Ruler writes only into the project, and says so as a safety property**: "Ruler never writes
MCP configuration files outside your project root. Any historical references to user home
directories ... have been removed; only project-local paths are targeted."[^ruler] Its
`--global` flag creates a configuration at `~/.config/ruler` used "when no local `.ruler/`
directory is found" - a global *source* feeding project *outputs*[^ruler]. Not a missing
feature; a thing the tool removed on purpose. ai-rulez is project-scoped the same way, where
"global" means the npm install.

Three tools do write to `$HOME`, and each carries a catch:

- **Rulesync** has a global mode whose reach is narrower than its fifty-target
  matrix[^rulesync-tools] suggests: "Currently, supports rules generation for Claude Code,
  GitHub Copilot, and OpenCode."[^rulesync-global] Commands in global mode are Claude Code only.
- **vibe-rules** has the best-shaped mechanism found. `--global` writes `~/.claude/CLAUDE.md`,
  `~/.gemini/GEMINI.md`, `~/.codex/AGENTS.md` and `~/.cursor/rules/`, and it edits inside a
  delimited `<!-- vibe-rules Integration -->` block rather than owning the
  file[^vibe-rules], so hand-written content survives a regeneration. It has had no commit
  since 2025-08 and has no opencode target.
- **ai-rules-sync** is the only one built for this case on purpose, with a `--user` flag and an
  `ais user install` for a new machine[^ai-rules-sync]. Its mechanism is a git repository
  cloned to a cache with symlinks into place - which is a dotfile manager, and inherits the
  Windows symlink problem below.

The asymmetry has an obvious cause once the two categories are separated. Shared rules
committed to a repository are a team problem, with onboarding and drift and a reviewer; one
person's instruction file across their own machines is a dotfiles problem, and dotfiles are
already solved. The tools go where the teams are.

## What this costs against two lines of config

Rulesync's three global targets are Claude Code, GitHub Copilot and opencode - the harness in
use here plus the two most likely to be added. Measured against the harnesses that matter
rather than against a catalogue, that is full coverage, so it is a real alternative rather than
an absent one.

What it costs is a compile step: a source directory, a generate command, generated files in
three home directories that no longer say where they came from, and a fourth tool in the chain
that has to keep tracking fifty moving targets. What it buys, beyond the file itself, is the
other seven surfaces - skills, commands, MCP servers, permissions - kept in step by the same
run.

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

The category is crowded and aimed elsewhere. Most of its headcount writes project files from a
repository scan; of the handful that distribute one source to many tools, the two with real
adoption treat the home directory as out of scope or nearly so, and the three that do write
there are narrow, unmaintained or symlink-based.

Rulesync is the one worth holding onto, because its three global targets happen to be the
right three. It is still the wrong size for two harnesses. One canonical file at
`~/.agents/AGENTS.md`, an `instructions` entry in opencode's config and an `@` import in
`~/.claude/CLAUDE.md` gets the content to both with no compile step and nothing generated.
Revisit it when a third harness arrives without a reference mechanism, or when the thing being
synchronised stops being one markdown file and becomes skills, commands and MCP servers as
well - which is the threshold it was actually built for.

The more useful thing the survey settles is what kind of problem this is. The tools decline
the home directory because a user-level instruction file is not an agent problem at all: it is
one person's configuration across their own machines, which is a dotfiles problem wearing a
new hat. ai-rules-sync is the tool that noticed, and its answer - a git repository, a cache
and symlinks - is what a dotfile manager already does.

One thing this does not settle: the file is currently version-controlled inside the opencode
config repository, and `~/.agents` is a different repository with a different publishing
posture. That is a decision about where the content lives, not a path change.
