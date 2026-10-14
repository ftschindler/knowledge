---
type: Principle
title: A version stamp is bookkeeping about capabilities, not a lock
description: Where a tool is installed by copying and keeps state the user owns, record which release
  that state has been brought up to, and use it to raise questions rather than to block work.
tags:
- principle
- dx
- agents
- versioning
- knowledge-management
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T10:15:00Z'
---
**Claim.** Software installed by copying arrives without announcement: files are replaced, and
nothing on the machine notices. Where that software also keeps state the user owns, a release
that wants something of that state has no way to ask for it. Recording which release the state
has been brought up to gives it one, and the stamp earns its place only if it never blocks
anything.

**When to apply.** A skill, a dotfile set, a template or a scaffold that is copied into place,
alongside a workspace, vault or configuration the person edits themselves. Not a package with
a resolver, which already knows what it replaced.

**The rule.**

1. **Stamp the state, not the install.** The file that records the version is the one the user
   owns, and the number in it means "this setup has been brought up to here", which is a
   different fact from which copy of the tool is on disk.
2. **Notice at a command they already run.** A separate check is one nobody runs. The ordinary
   listing command compares the two numbers and prints a notice when they differ.
3. **Name the guide; do not perform the change.** The notice points at prose, oldest guide
   first, because most of what a release wants is a decision rather than an edit.
4. **Put each decision to the person, and take no for an answer.** These are usually new
   capabilities: "there is now a way to share a bundle with your team, do you want that here"
   is the shape of it.
5. **Stamp a declined change as migrated.** The question was asked. Leaving it unrecorded asks
   it again next week, which teaches the person to ignore the notice.
6. **Never stamp a guide nobody read**, and never edit the number by hand. The field's only
   job is to be trustworthy about what has actually been put to this person.
7. **Block nothing.** A setup that ignores the notice keeps working, and the notice comes back.

**Why.** The alternative is a tool refusing to run against state it did not create and cannot
see the history of, over a release the user never asked for. That spends their attention on
the author's cadence. A stamp that only ever raises a question costs one line of output and
keeps the state theirs.

**What it costs.** Every code path has to tolerate the old shape, for as long as the guide
remains optional, which is indefinitely. And an upgrade replaces the files a release changed
without removing the ones it deleted, so a guide has to name any stale file explicitly; the
leftover is often a second copy of the very text the release removed.

**How enforced.** One field in the manifest, a comparison in the listing command, and a
migrate command that lists outstanding guides and records them as read. Earned in
[federated-knowledge-skills](../tools/federated_knowledge_skills_schindler.md), where each
release since the first has asked something of setups already on disk.
