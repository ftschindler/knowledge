---
type: Exploration
title: Tracking AI authorship with git-ai
description: Three and a half months of recording which lines an agent wrote, ended because the data
  was never read and the notes it wrote cluttered every history view that shows all refs.
tags:
- exploration
- git-ai
- git
- provenance
- agents
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T14:00:00+02:00'
sources:
- id: felix-git-ai-opencode
  resource: https://ftschindler.github.io/running-linux/done/20260624-git-ai-integration-with-opencode/
  title: Git AI Integration with OpenCode
  author: human:felix_schindler
  last_modified: '2026-06-24'
---
[git-ai](../tools/git_ai.md) was installed on 24 June 2026 and removed on 9 October. In between
it did exactly what it promised, without once being asked for anything.

## What it was for

Most of the code in these repositories is written by an agent, and the question of which lines
those are has no answer in git itself. `git blame` names whoever ran the commit. A tool that
records the agent, the model and the prompt behind each line promises to turn that into
something answerable, and `git ai blame` renders it beside the ordinary blame.

The setup was done carefully and written up at the time[^felix-git-ai-opencode]: telemetry off,
version checks off, auto-updates off, so the tool ran entirely locally. `prompt_storage` was set
to `notes` deliberately, so attribution and prompts travelled with the repository rather than
sitting in a database on one machine. Each repository was configured to fetch and push
`refs/notes/ai` alongside its branches.

## What actually happened

Nothing, which is the finding.

The collection worked. Three and a half months later, 125 repositories held a `.git/ai`
directory and 19 carried notes. All of it was recorded passively, pushed with the code, and
**never read once**. Not a single `git ai blame`, `git ai stats` or `git ai log` was run against
a real question.

That is not a failure of the tool, and it is worth separating from one. The attribution data was
accurate and present the whole time. What was missing was a question to put to it.

## Why it stopped

**The value is in the analysis, and the analysis is the commercial product.** What the open
source CLI gives one person is a per-file, per-commit view, answered one command at a time. The
things the data would actually be interesting for - how much agent-written code survives review,
which models produce work that needs reworking, what a change really cost - are aggregations
across many commits and many repositories, and those live in the Teams product. Collecting the
data locally without that is keeping records for an audit nobody is going to run.

**The notes clutter every history view that shows all refs.** `refs/notes/ai` is a ref like any
other, so anything drawing `--all` draws it, and the note commits carry no subject line:

```text
15ee53d (HEAD -> redesign-as-skill) design the redesign: this config as an installable skill
abd9bf4
1171be4 (origin/main, main) add a getting-started guide for fresh machines
1414586
69660c8 update my AGENTS.md
```

Two of those five rows are notes. In `gitk`, which is where a branch view gets read rather than
grepped, they interleave with the real history as blank entries and have to be looked past every
time. A background cost, paid at every glance, against a benefit taken zero times.

## What it cost to leave

More than it cost to adopt, which is the asymmetry worth recording. The installer wrote into
four unrelated places and the removal had to reach all four, including per-repository state in
125 repositories and notes already pushed to remotes. The procedure is
[Uninstall git-ai and the state it left in every repository](../guides/uninstall_git_ai.md), and
it is longer than the install instructions by a wide margin.

**A tool that needs no per-repository setup leaves per-repository state anyway.** That is the
general shape, and it is not specific to this tool: the property that makes something frictionless
to adopt is usually the same property that spreads it somewhere nothing is tracking.

## What would bring it back

A question worth asking of the data. If the aggregate view ever matters here - measuring what
agent-written code costs over its life rather than at the moment it is written - then this is the
tool that already has the standard, the agent coverage and the git-native storage to answer it.
Nothing about the implementation was the problem.

Until then the honest position is that the data was collected because collecting it was easy, not
because anyone intended to use it.
