---
type: Investigation
title: 'Travel management skills: what is portable out of a repo-shaped toolkit'
description: A survey of the travel-hacking-toolkit as an integration target, counting how much of a
  48-skill collection works outside the repository it ships in.
tags:
- agent-skills
- security
- ai-agents
- tooling
- opencode
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-20T00:00:00Z'
sources:
- id: tht-repo
  resource: https://github.com/borski/travel-hacking-toolkit
  title: 'borski/travel-hacking-toolkit'
  last_modified: '2026-10-19'
---
**Context** - looking for agent skills to cover travel planning, and finding that the largest
collection on offer is not a collection of skills at all. The question that decided the
approach: **how much of this works once it leaves the repository it ships in?**

- **Version read**: commit `01426c5`, 2026-10-19[^tht-repo]
- **Method**: full read of `README.md`, `opencode.json`, `AGENTS.md`, `.env.example` and
  `scripts/setup.sh`; counts taken across all 48 `SKILL.md` files for repo-root data
  references, repo-relative script paths, Docker requirements and package manifests.

## Three products in one repository

The thing is packaged as a skill collection and is better understood as three separable
parts, only one of which travels.

| Part | Count | Travels? |
| --- | --- | --- |
| Skills | 48 | About half, and only after repackaging |
| MCP servers | 6 | Yes. Pure configuration, already in opencode's schema |
| Agent definition | 1, copied into `AGENTS.md`, `CLAUDE.md` and `agents/travel-hacker.md` | Yes, and should not |

The repository already accommodates opencode: `opencode.json` at the root declares all six
MCP servers, and `.opencode/skills` is a symlink to the skills tree, so running the harness
from inside a clone picks up both with no configuration. The clone is not a fallback for
people whose harness lacks a plugin format. It is the only arrangement in which the whole
thing works.

## The counts that decide it

Across the 48 skills:

- **19 reference repository-root data files** as `data/alliances.json` and similar. There are
  18 JSON files under `data/`, refreshed on a schedule by a GitHub Action.
- **9 reference `skills/<name>/...` paths**, which resolve only from the repository root.
- **9 require Docker images**, seven of which ship a `Dockerfile`.
- **2 require `npm install`** against a bundled `package.json`.
- Around **10 ship Python browser-automation scripts**.

Roughly half the collection therefore has the repository as a hidden argument. This is not
hidden from the author, who put the data where it belongs for a repository; it is hidden from
the installer, because no part of the skill format can express it.

### The upstream global install is broken by construction

`scripts/setup.sh` offers to install the skills system-wide, and implements that as `cp -r` of
each `skills/*/` directory into `~/.config/opencode/skills/`. Nothing else is copied. The 19
data-dependent skills lose `data/` entirely and the repo-relative script paths stop resolving.
The option succeeds silently and produces skills that fail at first use.

That failure is the general case rather than an oversight. **A skill directory is the unit the
format can install, so anything a skill needs from outside its own directory cannot survive the
install.** An author who keeps shared data at the repository root, which is the obvious place
for data 19 skills read, has already left the format's reach.

## What a machine-wide scope would acquire

Three things argue for keeping this inside a project directory rather than installing it for
every session.

**The agent definition is a behavioural override, not a capability.** It opens with a
"PRE-OUTPUT GATE (mandatory, every response, no exceptions)" forbidding the agent from asking
before acting, with a list of banned phrases. That is defensible inside a travel-planning
session, where the user wants results rather than offers. Rendered machine-wide it governs
every session on the machine, including ones that edit a knowledge base or a repository.

**The credential surface is wider than an API key list.** `.env.example` declares 22
variables, and four of the pairs are account usernames and passwords for Chase, Amex, American
Airlines and Southwest, consumed by Dockerised browser automation that logs in as the account
holder. That is a different risk class from the five read-only API keys beside them, and it is
worth deciding separately rather than as part of a setup script's questions.

**One MCP server runs unpinned remote code at every start**, as
`npx -y @openbnb/mcp-server-airbnb@latest --ignore-robots-txt`. The other five are remote HTTP
endpoints at third-party travel vendors, which is a trust decision but not code execution.

A smaller point, specific to a machine where `~/.agents` is a git repository: `setup.sh`
defaults its Codex marketplace root to `$HOME/.agents` and writes `plugins/marketplace.json`
there. A deny-by-default `.gitignore` that allow-lists only `skills/` and repository
infrastructure keeps it out of any commit, which is the arrangement earning its keep.

## The approach this argues for

Clone the repository into a project directory and run the harness from there, which is the
arrangement the repository is built for and the only one in which the data-dependent half
functions. Skip the setup script and carry out its steps deliberately: it is interactive, it
offers the broken global install, and it pulls Docker images and a global npm package
depending on the answers. Start with no `.env`, since five of the six MCP servers and most of
the knowledge skills need no key, and add one when a specific skill is blocked.

Then treat portability as a separate and much smaller exercise. A skill with no key, no Docker
image and no repository-root data is a genuine candidate for a machine-wide subscription;
[the deutsche-bahn skill](deutsche_bahn_skill_security_and_telemetry.md) is one, once its
repo-relative paths are corrected. The split to hold onto is **clone for the product,
subscribe to the parts that deserve to escape it.**

## What this says beyond one toolkit

The useful finding is not about travel. It is that a repository can present as a skill
collection whilst being an application whose working directory is part of its interface, and
that **nothing in the skill format makes the difference visible before installing.** The
frontmatter carries a name and a description; the `compatibility` field is free text and
optional; and an installer that copies a directory cannot know the directory was never the
unit.

The counts above are cheap to take and decide the integration shape on their own. For any
collection offered for installation, the question that separates a portable skill from a
repository-shaped one is what its scripts and prose reference outside their own directory.
