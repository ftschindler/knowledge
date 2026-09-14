---
type: Principle
title: A declared-but-inert config documents intent, not enforcement
description: A config entry that does nothing until a matching input exists is a statement of intent,
  and must not be mistaken for enforcement.
tags:
- principle
- software
- dx
- configuration
- git
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** A configuration entry that does nothing until a matching input exists
is legitimate to keep as a statement of intent, even when it enforces nothing
today. Distinguish the two roles explicitly: an inert declaration says "this is
how we would handle X," while enforcement requires a trigger that actually fires.

**When to apply.** Any config whose effect is conditional on inputs that may not
be present - `.gitattributes` filters for file types not yet committed, lint
rules for languages not yet in the tree, CI matrix entries for platforms not yet
targeted. Also when auditing requirements: an inert declaration is not a reason
to require the tooling it names.

**Why.** Config carries two separable jobs that are easy to conflate. One is
*enforcement* - actively rejecting or transforming real inputs. The other is
*documentation of intent* - recording a decision so the next contributor inherits
it rather than re-deciding. A `filter=lfs` line for `*.png` in a repo with no
images enforces nothing (git never invokes the filter), yet it usefully tells the
next person "images belong in LFS here." Keeping it is correct; but treating its
presence as active enforcement is a mistake - it will not fire, and may not fail
loudly, until its input appears. Naming which role a given entry plays prevents
two errors: deleting useful intent because "it does nothing," and trusting a
dormant rule as if it were a live guard.

**Snippet.**

```console
# Inert: the .gitattributes lfs filter exists, but no matching file does,
# so git resolves nothing and never calls git-lfs.
$ git check-attr filter -- notes.md
notes.md: filter: unspecified
```

**How enforced.** Judgement, not automation: label each conditional entry by
role in review. If it is intent, keep it and do not let it inflate the
requirements list - see [Do not make a tool a prerequisite for work it is not needed for](do_not_make_a_tool_a_prerequisite_for_work_it_is_not_needed_for.md). If it must actually enforce, verify its trigger fires and fails
loudly rather than assuming it does; the [LFS case](track_every_committed_binary_type_in_gitattributes.md) shows a rule that silently stores raw bytes instead of
aborting unless `git lfs install` has armed it.
