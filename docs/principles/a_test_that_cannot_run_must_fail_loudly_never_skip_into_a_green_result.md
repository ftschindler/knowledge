---
type: Principle
title: A test that cannot run must fail loudly, never skip into a green result
description: A test whose prerequisite is missing must fail, because a skip makes 'could not run' indistinguishable
  from 'ran and passed'.
tags:
- principle
- testing
- ci
- dx
- software
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-28T00:00:00Z'
---
**Claim.** When a test or verification cannot execute because its environment is
missing a prerequisite, it must fail loudly - not skip. A conditional skip on
absent tooling makes "the environment could not run this" indistinguishable from
"this ran and passed": the suite reports green while the check never happened.

**When to apply.** Any test gated on a runtime prerequisite - a binary
(`node`/`npm`/`docker`), a service, a network resource, a credential. Especially
end-to-end layers, which are both the most environment-dependent and the ones
whose silent absence is most dangerous. The escape hatch to resist is
`pytest.mark.skipif(not have("npm"), …)` and its equivalents.

**Why.** A green suite is a claim: "everything I guard, I verified." A skip on
missing tooling quietly narrows that claim without narrowing the *report* - the
run still exits 0, CI still shows a check mark, and nobody learns that the e2e
layer never ran. The failure modes are real and common: a CI runner where the
setup step silently failed, a contributor on a machine without the binary, a
config drift that removes the tool from `PATH`. Each yields a false green, and a
false green is worse than a red: it launders "untested" into "passing". If the
environment genuinely cannot run a test, the honest outcomes are *fail with a
clear reason* or *do not claim to have a passing suite* - never *pass anyway*.

The fix is usually to move the check earlier and make it a hard gate. Rather than
skip inside the test, assert the prerequisite at the entry point - a task-runner
[guard](fail_early_on_a_missing_tool_with_a_message_that_names_it_and_points_at_the_fix.md) that aborts before the tests run - so absent tooling produces a loud,
self-locating error for CI and contributors alike, never a skip.

**Snippet (silent skip → loud gate).**

```python
# BAD: absent tooling vanishes into a green run
requires_e2e = pytest.mark.skipif(
    not (have("node") and have("npm")), reason="e2e needs node/npm"
)
```

```makefile
# GOOD: the target hard-fails before pytest runs; the layer cannot silently vanish
test_skills: | guard-node guard-npm guard-npx
 pytest -m skills
```

**How enforced.** Review any `skipif`/`skip` on a prerequisite by asking: if this
skips, does the suite still report success? If yes, it is a false-green machine -
replace it with a hard gate at the runner. This is the test-harness member of the
silent-no-op family: the same trap as a [hook that reports `Skipped` on the file it was meant to guard](verify_a_pre_commit_hooks_file_type_filter_actually_matches_your_file.md), and the inverse discipline of [A declared-but-inert config documents intent, not enforcement](a_declared_but_inert_config_documents_intent_not_enforcement.md) - do not let something dormant read as
something verified. Kin to [Install from a frozen lockfile in CI](install_from_a_frozen_lockfile_in_ci.md), which
likewise turns silent drift into a hard failure.
