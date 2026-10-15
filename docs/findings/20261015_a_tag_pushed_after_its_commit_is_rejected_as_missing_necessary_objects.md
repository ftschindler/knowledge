---
type: Finding
title: A tag pushed after its commit is rejected as missing necessary objects
description: Pushing a release commit and its tag as two commands sends the tag in a pack of its
  own, which a receiving replica that has not caught up reads as incomplete and rejects.
tags:
- finding
- git
- github
- ci-cd
- release
status: stable
stale_after: '2027-04-15'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-15T23:55:00+02:00'
---
A release job that had shipped fifteen versions pushed its version commit, then failed on the
next line:

```text
remote: Bypassed rule violations for refs/heads/main:
To https://github.com/ftschindler/federated-agent-kits
   c1355dd..8810513  HEAD -> main
To https://github.com/ftschindler/federated-agent-kits
 ! [remote rejected] v0.13.0 -> v0.13.0 (missing necessary objects)
```

The commit the tag points at had gone up one second earlier, in the push immediately above, and
the remote had accepted it.

## Two pushes mean two packs

The job ended its release step with two commands:

```sh
git push origin HEAD:main
git push origin "v${NEXT}"
```

The second one sends **the tag object alone**. Git builds a pack from what the remote says it is
missing, and since the commit went up a moment ago, the pack contains the annotated tag and
nothing else. GitHub's receive side then resolves that pack against a replica, and a replica
that has not yet caught up with the first push cannot find the commit the tag names. An
incomplete pack is the correct reading of what arrived, and `missing necessary objects` is what
it is called.

Nothing about this release made it more likely than any other. It is a race the two-command form
has always had, and the previous fifteen releases won it.

## The repair is one push

```sh
git push --atomic origin HEAD:main "refs/tags/v${NEXT}"
```

One command sends one pack holding both refs, so there is no window in which the tag's target is
somewhere the receiving side has not seen. `--atomic` then makes the pair all-or-nothing, which
matters more here than the usual tidiness argument: the two refs are two halves of one release,
and either one landing without the other is the failure being prevented.

## What it costs when it happens mid-release

The job was arranged with the irreversible step last, so the PyPI upload never ran and nothing
was published. What did land is a `Release 0.13.0` commit on `main` with no tag, no GitHub
release and no package behind it.

That state cannot be finished by re-running the job, because the job reads the current version
from `pyproject.toml`, which the failed run already bumped. A re-run computes the next version
up and releases that instead. Tagging the orphaned commit by hand gets the tag right and still
publishes nothing, since the upload exists only inside that job.

So the version number is spent. Skipping it costs nothing downstream, because an index serves
whatever versions exist and neither PyPI nor a resolver objects to a gap in the sequence, which
is the cheapest of the available repairs and the reason to prefer the ordering that made it
available.

**The step ordering is what kept this to a lost version number.** Had the upload run before the
tag, PyPI would hold a version the repository never recorded, and PyPI has no delete-and-reuse,
only yank. The guide this job came from,
[Let CI push to a protected branch with a GitHub App](../guides/let_ci_push_to_a_protected_branch_with_a_github_app.md),
covers getting the push accepted at all; this is the failure that remains once it is.
