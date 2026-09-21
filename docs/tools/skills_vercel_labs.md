---
type: Tool
title: skills (Vercel Labs)
description: The `skills` CLI and the skills.sh directory it feeds, which install agent skills from any
  git repository into whichever agents are on the machine.
tags:
- tools
- agent-skills
- ai-agents
- skills-sh
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: skills-repo
  resource: https://github.com/vercel-labs/skills
  title: 'vercel-labs/skills: install agent skills from any git repository'
  last_modified: '2026-09-18'
- id: skills-docs
  resource: https://skills.sh/docs
  title: Documentation | Skills
  last_modified: '2026-09-18'
---
`skills`[^skills-repo] installs *agent skills* - directories holding a `SKILL.md` and whatever
references and scripts it reads - from a git repository into the agent harnesses on your
machine. It is run as `npx skills add <owner>/<repo>`, and it is the installer that
[federated-knowledge-skills](federated_knowledge_skills_schindler.md) writes its `SKILL.md`
frontmatter to be discovered by.

| | |
| --- | --- |
| Author | Vercel, under the `vercel-labs` organisation |
| Licence | Apache-2.0 |
| Language | TypeScript |
| Distribution | npm, as `skills`; ordinarily invoked through `npx` |
| Source | [github.com/vercel-labs/skills](https://github.com/vercel-labs/skills) |
| Directory | [skills.sh](https://skills.sh) |
| Version read | 1.7.0, commit `7407f38`, 2026-09-17 |

## What it is

Two things share the name, and separating them early saves confusion. The **CLI** is the part
that does the work: it clones a repository, finds the skills in it, and writes each one into
every agent directory you selected. The **directory at skills.sh** is a leaderboard of
publicly installed skills, ranked by install counts the CLI reports back[^skills-docs]. The
first is a local tool; the second is a website the first feeds. An install event names the
repository and the skills taken from it; `DO_NOT_TRACK=1` switches the reporting off, at the
cost of the pre-install security audit lookup, which is guarded by the same flag. What the
event carries in full, and where the built-in private-repository exclusion does not hold, is
[the research page](../research/skills_sh_repository_layout_and_telemetry.md).

A skill is discovered, never declared. There is no manifest, no registry entry and no
packaging step: a directory containing a `SKILL.md` whose YAML frontmatter carries a `name`
and a `description` is a skill, and a repository is however many of those it happens to hold.
Anything else in the directory travels with it.

The consequence worth holding onto is that **publishing is not a step**. A repository becomes
installable by containing skills, which also means a repository becomes *mis*-installable the
same way: a `SKILL.md` missing a required field is skipped with a warning rather than
rejected, so a skill can be invisible to the installer whilst looking entirely correct in the
editor.

## What it installs into

One canonical copy per skill, with a symlink from each agent's own directory, or independent
copies under `--copy`. Project scope writes to `./<agent>/skills/` and is the default; `-g`
writes to the equivalent under the home directory. Around thirty harnesses are recognised,
`.claude/skills` and `.opencode/skills` amongst them.

Installation is recorded in a `skills-lock.json` in the project, holding each skill's source
and a content hash, which is what `skills update` later compares against.

## Where the skills come from

The source argument accepts GitHub shorthand, a full GitHub, GitLab or Azure Repos URL, any
git URL, or a local path. A fragment pins a revision and an `@` selects a single skill, so
`owner/repo#v1.2.0@some-skill` is one skill at one tag.

Private repositories use the same command as public ones. The CLI reuses whatever
authentication is already configured for the URL, trying ordinary git credentials, then
`gh repo clone`, then SSH; `GITHUB_TOKEN` and `GH_TOKEN` are read if set but are not required.
It deliberately never runs `gh auth token` or reads the stored GitHub CLI credential into its
own process, which is the right shape: the credential stays where its owner put it.
