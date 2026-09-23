---
type: Reference
title: Sharing one user-level AGENTS.md across harnesses
description: Where each coding-agent harness looks for a user-level instruction file, why no standard
  covers that location, and which of the three adapter mechanisms survives Windows.
tags:
- research
- ai-agents
- agents
- opencode
- config-management
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
- id: claude-memory
  resource: https://code.claude.com/docs/en/memory
  title: How Claude remembers your project
  last_modified: '2026-09-23'
- id: codex-agents-md
  resource: https://developers.openai.com/codex/guides/agents-md
  title: Custom instructions with AGENTS.md - OpenAI Codex
  last_modified: '2026-09-23'
---
**Context** - Felix keeps one always-on instruction file for every agent session, the
digest described in
[Teaching my agents to write better](../decisions/teaching_my_agents_to_write_better.md).
It currently sits at `~/.config/opencode/AGENTS.md`, which is a path
[opencode](../tools/opencode.md) invented and nothing else reads. The question is what
"portable" can mean for that file across operating systems and across harnesses.

- **Read on**: 2026-09-23
- **Method**: the vendor documentation for each harness, read directly rather than
  through a summary. Claims that appeared only in a research summary and not in a vendor
  page are marked below as unconfirmed.

## The standard stops at the project root

`AGENTS.md` is a real convention with real reach: one file, read by Codex, opencode,
Amp, Cursor, Gemini CLI, Jules, Zed, Warp, Factory and others, now stewarded by the
Agentic AI Foundation[^agents-md]. **It specifies nothing about a user-level file.**
The format is "a README for agents" placed at the root of a repository, and every
statement it makes about discovery is about walking a directory tree inside a project.

So the thing this investigation set out to find does not exist. There is no
`~/.agents/AGENTS.md` that harnesses agree on, and Claude Code goes as far as naming
`.agents/` in its list of paths it deliberately does not read[^claude-memory].

What each harness does instead:

| Harness | User-level file | Set by |
| --- | --- | --- |
| opencode | `~/.config/opencode/AGENTS.md`, falling back to `~/.claude/CLAUDE.md` | fixed path[^opencode-rules] |
| Claude Code | `~/.claude/CLAUDE.md`, plus every `.md` in `~/.claude/rules/` | fixed path[^claude-memory] |
| Codex CLI | `~/.codex/AGENTS.override.md`, else `~/.codex/AGENTS.md` | `CODEX_HOME`[^codex-agents-md] |
| Gemini CLI | `~/.gemini/GEMINI.md` | `context.fileName` in `settings.json`[^agents-md] |
| Aider | none; reads what `read:` names | `~/.aider.conf.yml`[^agents-md] |

Three different filenames, five different directories, and the one harness that reads a
file called `AGENTS.md` at user level (Codex) reads it from a directory named after
itself. A survey summary also offered `~/.config/amp/AGENTS.md` for Amp and a Settings-UI-only
answer for Cursor CLI; neither was confirmed against a vendor page here.

## Three mechanisms, and only one of them travels

Every harness above can be pointed at a file it would not otherwise find, but the three
mechanisms behave very differently.

**Symlink.** Put the content anywhere, link each harness's expected path at it. Works for
opencode and Codex, whose loaders only open a path. It is the mechanism that fails first:
creating a symlink on Windows needs Administrator rights or Developer Mode, and git checks
a committed symlink out as a one-line text file unless `core.symlinks` is enabled - which
leaves that machine with a `CLAUDE.md` containing the string `AGENTS.md` and no
instructions at all. **Claude Code's own documentation says this, and recommends the import
over the symlink for exactly this reason**[^claude-memory].

**Reference.** The harness reads a small file of its own that names the canonical one.
Claude Code expands `@path` imports, four hops deep, and the worked example in its docs is
`@~/.claude/my-project-instructions.md`, so the tilde resolves there. Aider takes
`read:` in `~/.aider.conf.yml`. opencode takes an `instructions` array in `opencode.json`,
which accepts relative paths, globs and even remote URLs fetched with a five-second
timeout; whether it expands `~` is not documented.

Two properties make this the mechanism to build on. It is ordinary file content, so it
works identically on every operating system. And it composes: harness-specific additions
sit below the import, in the harness's own file, rather than having to be conditionalised
inside a single shared one.

**Rename.** Gemini CLI takes `{"context": {"fileName": "AGENTS.md"}}` and Codex takes
`project_doc_fallback_filenames`. These change which name is looked for, not which
directory, so they solve half the problem and only the half that was not the obstacle.

## One free pairing, and why it is still the wrong home

opencode falls back to `~/.claude/CLAUDE.md` when no `~/.config/opencode/AGENTS.md`
exists[^opencode-rules]. Putting the canonical content there therefore feeds two harnesses
with no adapter, no symlink and no config key - the cheapest working setup in the whole
survey.

It is still the wrong home. A file every harness shares should not be named after one
vendor, and the fallback is a compatibility shim that opencode can retire or that a user
switches off with `OPENCODE_DISABLE_CLAUDE_CODE_PROMPT=1`. **A canonical location is
chosen, not discovered**, and `~/.agents/AGENTS.md` is the neutral name - already the
cross-harness home for skills in
[ftschindler/agents-skills](https://github.com/ftschindler/agents-skills) - as long as it
is understood that no harness finds it on its own.

## The constraint that decides the content

The file has to stay short, and the limits are not the same. Codex stops adding
instruction files once the combined size reaches `project_doc_max_bytes`, 32 KiB by
default[^codex-agents-md]. Claude Code asks for under 200 lines per file and says plainly
that longer files reduce adherence[^claude-memory]. A user-level file is prepended to every
session in every repository, so its cost is paid on every turn and never amortised.

This is the same argument
[Route a rule to the layer that reaches whoever must obey it](../principles/route_a_rule_to_the_layer_that_reaches_whoever_must_obey_it.md)
makes from the other direction: the always-on layer carries imperatives and refuses to
carry reasoning, because that is what its budget affords. Felix's current file is 64 lines
and sits well inside every limit.

## Bottom line

One canonical file at `~/.agents/AGENTS.md`, and a one-line adapter per harness that
references it rather than links to it. Concretely: `@~/.agents/AGENTS.md` in
`~/.claude/CLAUDE.md`, `read: [~/.agents/AGENTS.md]` in `~/.aider.conf.yml`, an
`instructions` entry in opencode's config, `context.fileName` for Gemini. Codex is the one
harness with no reference mechanism, so it takes the symlink and accepts the Windows
caveat, or a copy written by whatever already provisions the machine.

Two things worth settling before any of this is built. Whether opencode's `instructions`
expands `~` is undocumented and decides whether that entry can be committed to a
repository shared across machines or has to be generated per machine. And the file is
currently version-controlled inside the opencode config repository, so moving it to
`~/.agents` moves it into a different repository with a different publishing posture -
a decision about where the content lives, not a path change.
