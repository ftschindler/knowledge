---
type: Principle
title: Give a shared repository two clocks when review is slower than the work
description: Where a protected branch gates output produced faster than it can be reviewed, a second
  long-lived branch carries the work and a merge back keeps the two from drifting.
tags:
- principle
- ci-cd
- collaboration
- knowledge-management
- git
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:45:00Z'
---
**Claim.** A repository whose default branch is protected has one clock: the review cadence.
Where the work arrives faster than that, the usual answers are to loosen the gate or to let
people sit on local commits, and both give up something that was wanted. A second long-lived
branch gives the repository a second clock, and an automatic merge back is what stops the two
telling different times.

**When to apply.** The work is produced in minutes and reviewed in days, and both of those are
correct. A knowledge base several people file into is the case this came from. Generated
documentation, a shared vocabulary file and a datasets registry have the same shape.

**The rule.**

1. **The default branch keeps the review gate, and nobody works on it.** It holds what was
   reviewed and it is what anything downstream is built from.
2. **One long-lived shared branch takes every push.** Every checkout sits on it, so a clone is
   ready to work without anyone choosing a branch.
3. **Merge in both directions, never squash or rebase.** A squashed merge writes the same
   content as a commit with no shared ancestry, after which the two branches no longer know
   they met: the next release re-displays everything already released, and the merge back
   conflicts the content against a copy of itself.
4. **Automate the merge back, on every change to the default branch.** Not on the release
   alone: work reaches the default branch by other routes, such as a web edit or a pull
   request from somebody's own checkout.
5. **Run the same checks on the shared branch as on a pull request.** A change made in the
   forge's web editor had no working copy, so no commit hook ran on it.

**Why.** The failure the merge back prevents is the only one here nobody sees. Branch
protection left off means unreviewed material in public, and a person notices. Squash merging
left on means a confusing release, and a person notices. The merge back missing means the two
branches drift, every working copy goes quietly stale, and the first symptom is a duplicate
written by somebody who could not see the original. That asymmetry is the argument for
shipping the merge back as a pinned reusable workflow rather than as four lines each
repository is trusted to copy correctly.

**What it costs.** Linear history, which
[the usual principle](keep_a_linear_history_block_merge_fixup_and_squash_commits.md) asks for
and this shape cannot have: shared ancestry is the thing being protected and a merge commit is
what records it. And a lag between what the team can see and what the world can, which is the
review gate working rather than a defect, but it does mean a link written today may not
resolve in public until the next release.

**How enforced.** Branch protection on the default branch, the merge method fixed in the
repository settings, and the merge-back workflow pinned by commit SHA. The worked example is
[Sharing one knowledge bundle on two branches](../blueprints/sharing_one_knowledge_bundle_on_two_branches.md).
