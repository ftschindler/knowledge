---
type: Blueprint
title: Sharing one knowledge bundle on two branches
description: The branch shape, manifest field, workflow and command that let several people file
  into one knowledge bundle whose published branch takes no direct pushes.
tags:
- blueprint
- okf
- federation
- knowledge-management
- ci-cd
- collaboration
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:40:00Z'
---
The shape a knowledge bundle takes once more than one person files into it, produced by
[Federating my knowledge base as privacy-tiered OKF bundles](../decisions/federating_my_knowledge_base_as_privacy_tiered_okf_bundles.md)
and shipped in
[federated-knowledge-skills](../tools/federated_knowledge_skills_schindler.md) v0.2.0. The
bundle you are reading runs it, and so does one shared with an employer's team.

The constraint it answers: a bundle anyone publishes from has a default branch that takes no
direct pushes, so a change reaches it through a pull request and a review. That gate is
measured in days. The knowledge it gates is written in minutes.

## Manifest - what is assembled

**Two branches, each with one job.**

| | the default branch | the shared branch |
| --- | --- | --- |
| Holds | what has been reviewed, and what the site is built from | everything reviewed, plus what is not ready |
| Protected | yes: pull request and review | no: open to anyone with write access |
| Who works here | nobody directly | every checkout, every agent |
| Reaches the other by | a release pull request, on a cadence | a merge, after every change to the default |

- **Merge commits only**, on both routes. Squash and rebase merging write a new commit with
  the same content and no shared ancestry, so the two branches stop knowing they ever met.
  The next release then re-displays everything already released.
- **One manifest field**, `sync: staging`, naming the branch this machine's checkout belongs
  on. It says three things at once: check this branch out, commits here may leave the
  machine, and somebody else is writing here so read it fresh.
- **A reusable merge-back workflow**, called by the bundle on every push to the default
  branch and pinned by full commit SHA:

  ```yaml
  on:
    push:
      branches: [main]

  jobs:
    merge_back:
      uses: ftschindler/federated-knowledge-skills/.github/workflows/merge-back.yml@<sha>
      with:
        branch: staging
      permissions:
        contents: write
        pull-requests: write
  ```

- **The governance checks run on the shared branch too**, not only on pull requests. A page
  edited in the forge's web editor has no working copy, so the bundle's own pre-commit hooks
  never ran on it, and the shared branch is where such a change lands first.

## Principles it instantiates

[Pin GitHub Actions to full commit SHAs](../principles/pin_github_actions_to_full_commit_shas.md),
which matters more here than usual: this workflow holds write access to the shared branch.
[Grant least-privilege CI permissions at both workflow and job level](../principles/grant_least_privilege_ci_permissions_at_both_workflow_and_job_level.md),
[Guard invariants at commit-time, not review-time](../principles/guard_invariants_at_commit_time_not_review_time.md)
and [Mirror every local guard in CI](../principles/mirror_every_local_guard_in_ci.md), which is
what the web-editor case above is. The branch shape itself is
[Give a shared repository two clocks when review is slower than the work](../principles/give_a_shared_repository_two_clocks_when_review_is_slower_than_the_work.md).

One principle this departs from on purpose:
[Keep a linear history](../principles/keep_a_linear_history_block_merge_fixup_and_squash_commits.md)
cannot hold where two long-lived branches have to keep meeting. Shared ancestry is the thing
being protected, and a merge commit is what records it.

## Operating manual

- **Before reading the bundle**, `fkb sync <bundle>`. This is what stops an answer coming from
  a page a teammate corrected this morning.
- **After filing**, commit through the bundle's hooks, then `fkb sync <bundle>` again. Pushing
  is part of filing here in the way committing is.
- **The command refuses rather than resolves.** It does not stash, switch branches or finish a
  rebase. Uncommitted work in the tree, a checkout on another branch, a conflict: the commit
  stands, nothing is pushed, and the reason is one line of output. An unpushed commit costs a
  teammate an hour's delay; a guess about whose work was in the tree costs the work.
- **Cutting a release is `gh pr create`** from the shared branch to the default one, on
  whatever cadence suits. Nothing automates it, because a command that did would put a forge
  inside the CLI.

## What it costs

**A concept is shared with the team before it is reachable by URL.** It sits on the shared
branch, where every checkout sees it, whilst the site still carries the last release. A
cross-bundle citation written today therefore points at a page the world cannot open yet, and
nothing detects this: the link checker asks whether the file exists on this disk, and it does.

**A conflict stops the machine every time.** Two people writing the same concept is a question
about what is true, which is the last thing to hand to an agent working quickly.
