---
okf_version: "0.2"
---

# Index

This is the public part of [Felix](people/felix_schindler.md) knowledge base.
This is where I note knowledge worth keeping, written to be read by people and agents alike.
Each page states one idea and links to the ones it rests on, so this is meant to be followed rather than
searched.

## People

Who appears in these notes, and in what capacity.

- [Felix Schindler](people/felix_schindler.md) - applied mathematician, computational
  scientist, and the person whose notes these are.

## Values

What I care about, ahead of any particular project. These sit under everything else here.

- [Prefer FOSS software wherever possible](values/prefer_foss_software_wherever_possible.md) - why an open tool wins a tie, and what it takes for a closed one to win anyway
- [Prefer plain-text, tool-agnostic formats](values/prefer_plain_text_tool_agnostic_formats.md) - keeping the data mine by keeping it readable without the tool that wrote it

## Wishes

What I wanted from a specific thing. Project-scoped, unlike the values above.

- [Wishes for a personal knowledge base](wishes/wishes_for_a_personal_knowledge_base.md) - the full list of requirements the knowledge base had to meet
- [Local-first, but not local-required](wishes/local_first_but_not_local_required.md) - one wish worth its own page: offline by default, never offline-only

## Principles

Reusable technical claims, each one a thing I would want true in any repository I work in. Start here if you are setting up a project and want the settled answers.

- [Treat warnings as errors](principles/treat_warnings_as_errors.md) - the most general of these: keep the warning count at zero so a new one is visible
- [Guard invariants at commit-time, not review-time](principles/guard_invariants_at_commit_time_not_review_time.md) - the case for spending automation instead of reviewer attention
- [Mirror every local guard in CI](principles/mirror_every_local_guard_in_ci.md) - why the commit hook alone is not the boundary
- [Autofix in the hook, don't just flag](principles/autofix_in_the_hook_dont_just_flag.md) - when a hook should edit the file rather than complain about it
- [Order auto-fixers so later ones do not re-dirty earlier output](principles/order_auto_fixers_so_later_ones_do_not_re_dirty_earlier_output.md) - what goes wrong once you have more than one fixer
- [Verify a pre-commit hook's file-type filter actually matches your file](principles/verify_a_pre_commit_hooks_file_type_filter_actually_matches_your_file.md) - how a hook can pass without ever having looked at your file
- [A markdown autofixer can corrupt YAML frontmatter it treats as content](principles/a_markdown_autofixer_can_corrupt_yaml_frontmatter_it_treats_as_content.md) - the specific way an autofixer eats a frontmatter block
- [Pin pre-commit hooks to frozen revisions](principles/pin_pre_commit_hooks_to_frozen_revisions.md) - hooks run arbitrary code on your tree, so pin them like dependencies
- [Pin GitHub Actions to full commit SHAs](principles/pin_github_actions_to_full_commit_shas.md) - the same argument for CI, where a tag is a mutable pointer at your secrets
- [Pin transitive runtime dependencies, not just the tool](principles/pin_transitive_runtime_dependencies_not_just_the_tool.md) - pinning the tool is not enough when the tool launches a browser
- [Install from a frozen lockfile in CI](principles/install_from_a_frozen_lockfile_in_ci.md) - making CI fail on a stale lockfile instead of quietly resolving around it
- [Batch dependency updates with a cooldown, not a firehose](principles/batch_dependency_updates_with_a_cooldown_not_a_firehose.md) - how to keep an update bot from becoming noise you learn to ignore
- [Keep declared toolchain versions in sync, and guard it](principles/keep_declared_toolchain_versions_in_sync_and_guard_it.md) - what to do when the same fact has to live in two files
- [Validate config files against their published schema](principles/validate_config_files_against_their_published_schema.md) - linting the configuration, not just the content
- [Document a rationale for every disabled lint rule](principles/document_a_rationale_for_every_disabled_lint_rule.md) - why a bare suppression is indistinguishable from an accident
- [Grant least-privilege CI permissions at both workflow and job level](principles/grant_least_privilege_ci_permissions_at_both_workflow_and_job_level.md) - scoping a CI token twice, so a job holds only what it uses
- [Split CI jobs for attributable failure and minimal dependencies](principles/split_ci_jobs_for_attributable_failure_and_minimal_dependencies.md) - cutting a workflow where you want the red check to point
- [Name every CI step so the run log reads as a narrative](principles/name_every_ci_step_so_the_run_log_reads_as_a_narrative.md) - making a failing run readable before you expand anything
- [Bound every CI job with an explicit timeout](principles/bound_every_ci_job_with_an_explicit_timeout.md) - the six-hour default, and why it is never what you meant
- [Cancel superseded CI runs with a concurrency group](principles/cancel_superseded_ci_runs_with_a_concurrency_group.md) - not spending a runner on a commit nobody is waiting for any more
- [Run CI steps under a strict shell (errexit, pipefail)](principles/run_ci_steps_under_a_strict_shell_errexit_pipefail.md) - the failure a lenient shell swallows in the middle of a pipe
- [A test that cannot run must fail loudly, never skip into a green result](principles/a_test_that_cannot_run_must_fail_loudly_never_skip_into_a_green_result.md) - the difference between a check that passed and a check that never ran
- [A sandbox test must use the live working-tree source and rebuild fresh each run](principles/a_sandbox_test_must_use_the_live_working_tree_source_and_rebuild_fresh_each_run.md) - how a sandbox test starts testing a stale copy of itself
- [End-to-end test an LLM skill by driving a real agent in a disposable fake HOME](principles/end_to_end_test_an_llm_skill_by_driving_a_real_agent_in_a_disposable_fake_home.md) - testing a markdown procedure by running an agent against it, not by grepping it
- [Enforce LF line endings everywhere](principles/enforce_lf_line_endings_everywhere.md) - declaring line endings in more than one place, because one is not believed
- [Declare formatting once, editor-agnostically, via .editorconfig](principles/declare_formatting_once_editor_agnostically_via_editorconfig.md) - the one formatting declaration every editor already reads
