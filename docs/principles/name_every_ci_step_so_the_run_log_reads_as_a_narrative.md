---
type: Principle
title: Name every CI step so the run log reads as a narrative
description: Give every CI step an explicit name, so a red run localises the failure before a single step
  is expanded.
tags:
- principle
- software
- ci-cd
- github-actions
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** Give every CI step an explicit `name:`, so the run log is a labeled
sequence of what happened rather than a wall of anonymous action references. The
log is read under pressure - when something is red - and a self-describing log
localizes the failure before you expand a single step.

**When to apply.** Any CI workflow. The payoff is highest on jobs with several
`uses:` actions, whose default labels are opaque `owner/action@sha` strings.

**Why.** An unnamed step renders in the log as its raw `uses:` reference -
`actions/checkout@3d3c42e5…` - which tells a reader nothing about *why* that step
exists here. A workflow of five anonymous steps is five SHA strings the reader
must decode against the YAML to follow. Named steps (`Checkout`, `Setup node`,
`Run Node tests`) turn the log into a readable sequence: the eye lands on the
failing stage by its purpose, not by cross-referencing action IDs. This is the
same reader-respect that [Structure docs as the reader's task path - lead with action, defer rationale](structure_docs_as_the_readers_task_path_lead_with_action_defer_rationale.md) pays a human reader, applied to machine output - the log should say what happened without the reader decoding it.

**Snippet (anonymous → named).**

```yaml
# Anonymous: the log shows raw action SHAs, purpose implicit
steps:
  - uses: actions/checkout@3d3c42e5…
  - uses: actions/setup-node@82076278…
  - run: make test_node_scripts

# Named: the log reads Checkout → Setup node → Run Node tests
steps:
  - name: Checkout
    uses: actions/checkout@3d3c42e5…
  - name: Setup node
    uses: actions/setup-node@82076278…
  - name: Run Node tests
    run: make test_node_scripts
```

**How enforced.** A `name:` on every step. Review by reading the job's step list
top to bottom as prose: does it narrate the job without reference to the actions'
identities? Complements [Run CI steps under a strict shell (errexit, pipefail)](run_ci_steps_under_a_strict_shell_errexit_pipefail.md) and [Split CI jobs for attributable failure and minimal dependencies](split_ci_jobs_for_attributable_failure_and_minimal_dependencies.md) - the first makes failures honest, the second attributes them to a job, this one attributes them to a step. Earned naming every step in a tests workflow whose steps had been bare `uses:` references.
