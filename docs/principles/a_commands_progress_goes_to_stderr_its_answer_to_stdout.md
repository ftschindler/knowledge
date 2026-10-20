---
type: Principle
title: A command's progress goes to stderr, its answer to stdout
description: Progress lines depend on which work happened to be slow, so they cannot share the stream whose
  bytes a pipe, a log and a pull request comment all read.
tags:
- principle
- cli
- dx
- observability
- software
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-20T14:00:00Z'
---
**Claim.** A command that takes long enough to need a live account must write
that account to `stderr`. `stdout` carries the answer, and the answer has to be
the same bytes whether a person is watching, a pipe is reading or a log is
being pasted into a pull request. Progress is not those bytes: which lines
appear, and in what order, depends on which sources happened to be cold.

**When to apply.** Any command whose slow part is a loop a person sits
through - fetching per dependency, uploading per file, probing per host. The
sign that it applies is somebody asking whether the command has hung.

**The objection to answer first.** "`stderr` is for errors" is the common
reading and it is not what the stream is. POSIX calls it *diagnostic output*,
and progress is the textbook case: `git clone`'s "Receiving objects", `curl`'s
meter and `pip`'s bars all go there, for one reason - so `|` gets the data and
nothing else. The split is not severity, it is **data versus everything said
about producing it**.

**The rule.**

1. **Decide by reproducibility, not by severity.** Ask whether two runs that did
   the same work would produce the same line. A summary of what changed: yes,
   `stdout`. A line naming whichever source is currently being fetched: no,
   `stderr`.
2. **Nothing may be said only on the live account.** Every fact it shows must
   also reach the report, so output nobody captured loses nothing. The moment
   progress is the only record of something, it has stopped being progress and
   become a second report on the wrong stream.
3. **An answer is not progress, even when it is one line.** "No subscriptions
   found, not looking for updates" *is* the result; it belongs on `stdout`. The
   tell is that redirecting to a file would otherwise leave it empty.
4. **Machine-readable modes emit nothing live.** Under `--json` the live account
   is silent, so what a consumer reads is a document rather than a document with
   a progress log in front of it.

**Why.** Mixing them costs on both sides. On `stdout`, progress makes the output
non-deterministic, so snapshot tests capture timing, a pull request comment
carries noise, and a consumer parsing the stream has to learn which lines to
discard. Suppressing progress entirely costs the opposite: the slow part of the
command becomes indistinguishable from a hang, and the usual reaction to a
command that appears hung is to kill it. Two streams already exist precisely so
neither cost has to be paid.

**The shape that keeps rule 2 honest.** One narrow sink, fed from the same value
the report is built from, so there is no second source of truth to drift:

```python
for key in keys:
    moved = resolve(key)      # the work
    watching.resolved(moved)  # live, now, to stderr
    record.append(moved)      # the report, later, to stdout
```

A sink whose default is silence costs callers nothing, keeps `--json` clean by
construction, and lets a test collect progress into a buffer rather than
capturing a file descriptor and reasoning about interleaving.

**How enforced.** Review: for each line a command prints, ask whether a second
run doing identical work would print it identically, and whether anything is
said *only* there. Test that the machine-readable mode writes zero bytes to
`stderr`, and that redirecting `stdout` alone still yields a complete record.
Pairs with
[Name the concrete behaviour, not its abstract label](name_the_concrete_behaviour_not_its_abstract_label.md):
both are about what the reader can actually act on. Earned on a command whose
only slow step - one network fetch per subscription - was also its only silent
one, where the first instinct was to put the progress lines in the report and
the stream question turned out to decide the shape of the whole output.
