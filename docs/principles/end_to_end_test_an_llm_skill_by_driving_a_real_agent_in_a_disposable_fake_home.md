---
type: Principle
title: End-to-end test an LLM skill by driving a real agent in a disposable fake HOME
description: Test an agent skill by driving a real agent runtime in a disposable fake HOME and asserting
  on the artifacts it produces.
tags:
- principle
- software
- testing
- agent-skills
- llm
- e2e
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-31T00:00:00Z'
---
**Claim.** To test an agent *skill* (a markdown procedure an LLM executes, not
code), don't just assert strings in the `SKILL.md` - build a disposable, isolated
fake `HOME`, install a real agent runtime into it, place the skills exactly as a
user would, then drive the agent non-interactively and assert on the *artifacts
and output it produces*.

**When to apply.** Any repo shipping agent skills / prompts / commands whose value
is behavioural ("does an agent, given this skill, do the right thing?"). Structural
lint (frontmatter valid, links resolve) is necessary but cannot catch a skill that
parses fine yet instructs the wrong behaviour.

**Why.** A skill is only correct in the context of an agent executing it. String
assertions ("the word *fail-closed* appears") are brittle and prove nothing about
behaviour. Running the actual agent proves the whole path: discovery, the skill's
preflight, delegation to other skills, and the files it writes. The cost is real
(installs a runtime, calls an LLM, non-deterministic) so it is a separate, slower
test layer - not a pre-commit hook.

**How.** The isolation is the trick: redirect **`HOME` and every `XDG_*`** into a
temp dir so the agent sees only the fake environment, never the developer's real
config or skills. Then, in setup:

1. Install the agent runtime into the fake home (`npm install` into a temp prefix,
   etc.). **Pin its version** - an unpinned "latest" makes the e2e non-reproducible
   and can break CI for reasons unrelated to your skills
   ([Pin transitive runtime dependencies, not just the tool](pin_transitive_runtime_dependencies_not_just_the_tool.md)).
2. Install the skills the way a *user* would (the same `skills.sh` / install command
   a real user runs), into the same directory the agent discovers - not a bespoke
   path. Model the dependency skills too: one fake home *without* a dependency to
   test the loud-failure path, one *with* it for the happy path.
3. Drive it non-interactively with a machine-readable transport
   (`opencode run --format json`) and parse the event stream.

Then **assert structural outcomes, not prose**: "a file landed in the sealed
bundle, not the public one", "no bundle was written when the dependency was
absent", "the install-me guidance appeared" - never "the reply contained sentence
X". LLM wording drifts run to run; the artifacts it leaves do not.

**Supporting practices.**

- **Preserve the sandbox on failure and print how to re-enter it.** A failed e2e is
  useless if the evidence is deleted. Keep the fake home and emit a copy-pasteable
  `cd <workdir> && env HOME=… XDG_*=… bash` command so the run can be inspected by
  hand. Pair it with a convenience script that builds the same home deliberately
  (sharing one builder with the fixtures, so there is no second definition of "how
  the sandbox is built").
- **Gate the layer so it skips cleanly when it cannot run** (offline, runtime
  missing) - but make CI *require* it, so a skip never masquerades as a pass
  ([A test that cannot run must fail loudly, never skip into a green result](a_test_that_cannot_run_must_fail_loudly_never_skip_into_a_green_result.md)).
- **Split it into its own CI job** for attributable failure and because it needs
  network the fast tests do not
  ([Split CI jobs for attributable failure and minimal dependencies](split_ci_jobs_for_attributable_failure_and_minimal_dependencies.md)).

A gotcha worth recording: an npm-installed agent may ship a per-platform binary
behind a `.exe` shim symlink; locate the real executable rather than invoking the
shim.
