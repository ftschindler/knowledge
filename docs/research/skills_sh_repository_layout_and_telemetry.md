---
type: Reference
title: 'skills.sh: repository layout, selective install and telemetry'
description: A source read of the skills CLI, answering where it finds skills in a repository, how a
  user installs one rather than all, and what it reports back about the install.
tags:
- research
- agent-skills
- skills-sh
- data-privacy
- ai-agents
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: skills-repo
  resource: https://github.com/vercel-labs/skills
  title: 'vercel-labs/skills: install agent skills from any git repository'
  last_modified: '2026-09-18'
---
**Context** - setting up a repository to hold several reusable agent skills, one per directory,
distributed through [the `skills` CLI](../tools/skills_vercel_labs.md). Three questions had to
be answered before the layout was fixed, because changing it later is expensive: **where does
the installer look for skills, how does a user install one rather than all of them, and what
does the CLI report back about the install?**

- **Version read**: `1.7.0`, commit `7407f38`, 2026-09-17[^skills-repo]
- **Method**: source read of `src/skills.ts`, `src/source-parser.ts`, `src/frontmatter.ts`,
  `src/telemetry.ts` and the telemetry call sites in `src/add.ts`, checked against the README;
  then empirical confirmation by building a two-skill repository in the layout under question
  and installing from it, selectively and wholesale, into scratch projects.

## Layout: the repository root is a first-class location

`discoverSkills()` walks a priority list of locations rather than searching indiscriminately.
The list begins with the **repository root**, then `skills/` and its `.curated`,
`.experimental` and `.system` variants, then around thirty agent directories such as
`.claude/skills`.

The depth differs between them, and this is the part that decides a layout. Known containers
like `skills/` are walked three levels deep, so `skills/<category>/<skill>/SKILL.md` is found.
**The root is walked one level deep, deliberately**, with a comment in the source saying why:
descending further from the root would surface unrelated `SKILL.md` files, an
`examples/foo/SKILL.md` being the case named. A `--full-depth` flag and a depth-five recursive
fallback exist for anything that neither pass found.

So `<skill-name>/SKILL.md` at the repository root is not a layout the tool tolerates, it is
exactly the depth-one case the root scan is written for. Confirmed empirically: two such
directories produced `Found 2 skills`.

There is **no repository manifest**, and nothing to add. A Claude Code `plugin.json` or
`marketplace.json` is read if one happens to be present, purely as an additional hint about
where to look. Absent, discovery is entirely filesystem-driven.

## Selective install is a first-class path, not a workaround

```sh
npx skills add owner/repo --skill one-skill     # one, by name
npx skills add owner/repo@one-skill             # the same, in shorthand
npx skills add owner/repo --skill '*'           # all of them
npx skills add owner/repo --list                # preview without installing
npx skills add owner/repo#v1.2.0                # pinned to a tag, branch or full SHA
```

`--skill` is repeatable, `--agent` narrows the targets, `-y` makes it non-interactive and
`--all` is shorthand for all skills into all agents. Both selective and wholesale installs
were run against the scratch repository; a skill's `references/` subdirectory travelled with
it intact.

## The frontmatter contract, and the one gap in it

`parseSkillMd` requires `name` and `description`, and requires both to be **strings** rather
than whatever YAML made of them: `name: 2026` parses as a number and is refused. A file
failing either check is skipped with a warning on stderr, not treated as an error. Nothing
else in the frontmatter is required. `metadata.internal: true` hides a skill unless it is
asked for by name.

That a missing field produces a warning rather than a failure is the argument for checking it
at commit time. A skill that is quietly invisible to the installer looks correct in every
other tool that reads it, which is the shape of defect
[a pre-commit hook exists to catch](../principles/autofix_in_the_hook_dont_just_flag.md).

The gap is what the two names are allowed to do to each other. **The installed directory is
named after the frontmatter `name`, not the source directory.** A directory `some-directory/`
whose `SKILL.md` declares `name: totally-different-name` installs to
`.claude/skills/totally-different-name/`, which was confirmed rather than inferred. Nothing
warns about the disagreement. Since the directory name is also the handle a user types after
`@`, letting the two drift produces a skill that is installed under one name and requested by
another, and a repository holding several skills is precisely where that stops being
noticeable.

## Telemetry: what is sent, and how to stop it

The CLI reports installs to `https://add-skill.vercel.sh/t`, which is what ranks the skills.sh
leaderboard. An install event carries the source as `owner/repo`, the **names of the skills
installed**, the agents they were installed into, a global flag, the CLI version, the detected
agent and a `ci=1` flag when it recognises a CI environment. Remove, update, find and sync
events are reported too, with their own fields.

It is disabled by either of two environment variables:

```sh
DISABLE_TELEMETRY=1
DO_NOT_TRACK=1
```

`isEnabled()` is a single negation of both, checked by every send. Honouring `DO_NOT_TRACK`
means the machine-wide setting already works without the tool having to be configured
specially, which is the better of the two to set.

Three qualifications worth knowing before switching it off or leaving it on.

**Private GitHub repositories are already excluded, and the check fails closed.** Before
sending, the CLI asks the GitHub API whether the repository is public and sends **only** when
the answer is an explicit `false`; an error or an indeterminate answer skips the event. GitHub
Enterprise sources are excluded by the same mechanism, with a comment saying the public API
must not be told an Enterprise repository's name. A private repository therefore does not leak
its name through this path by default.

**The exclusion is keyed on parsing `owner/repo`, and what fails to parse is sent anyway.**
The fallback branch reports the source when it cannot be split into exactly one owner and one
repository, on the reasoning that non-GitHub sources cannot be privacy-checked. A GitLab
project inside a subgroup has two slashes and does not match, so a private
`group/subgroup/repo` reaches the telemetry endpoint as a string. The default is safe for
GitHub and is not safe in general.

**Opting out also disables the security audit lookup.** `fetchAuditData` guards on the same
`isEnabled()`, so a machine with `DO_NOT_TRACK` set no longer fetches the partner risk ratings
that would otherwise be shown before an install. That is a real trade rather than a bug: the
audit call necessarily names the skills being installed, so it could not be exempted without
defeating the opt-out. It is worth knowing that the quieter machine is also the one told less
about what it is about to run.

## Bottom line

A repository of one skill per root-level directory needs no manifest, no `skills/` wrapper and
no publishing step, and users can take one skill or all of them from it, at a pinned revision,
with the authentication they already have. Two things are worth adding around it rather than
trusting to review: a commit-time check that `SKILL.md` carries a string `name` and
`description`, since the installer only warns, and a check that the `name` matches its
directory, since nothing anywhere else will notice when it does not.

Telemetry is on by default, reports the repository and the skill names, and is switched off by
`DO_NOT_TRACK=1`. For anything not public, set it regardless of the built-in private-repository
exclusion: that exclusion is a GitHub-shaped check with a documented hole in it, and an
environment variable is not.
