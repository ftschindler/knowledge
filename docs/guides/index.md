# Guides

A procedure to be carried out, written so it can be followed without rediscovering why each step is there.

A guide is not a [blueprint](../blueprints/index.md): a
blueprint is the artefact a decision produced, a thing to copy, whilst a guide is a sequence of
acts to perform.

Conventions:

- **name the version or date of the interface being driven**, if applicable; the reasoning is
[Date a page whose claim is about a version](../knowledge_management/date_a_page_whose_claim_is_about_a_version.md).

- [Let CI push to a protected branch with a GitHub App](let_ci_push_to_a_protected_branch_with_a_github_app.md) - an App installed on one repository, minting an hour-long token, instead of a maintainer's personal token in a secret
- [Uninstall git-ai and the state it left in every repository](uninstall_git_ai.md) - four removals in a fixed order, because the daemon reinstalls the hooks it just lost and the data outlives the binary
- [Pin the browser behind a pre-commit link checker](pin_the_browser_behind_a_pre_commit_link_checker.md) - which puppeteer version to choose, how to read the Chrome it carries, and why a separate browser install line is a liability
- [Decide whether a Linux freeze is failing hardware](decide_whether_a_linux_freeze_is_failing_hardware.md) - six checks that read a component's own error counters, ordered so the one that usually settles it runs first
- [Get started with direnv on Linux](get_started_with_direnv_on_linux.md) - install, hook, first `.envrc`, and why the allow step is the whole trust model
- [Authenticate a CLI from the keyring with a PATH shim](authenticate_a_cli_from_the_keyring_with_a_path_shim.md) - feeding a token to a CLI that reads only the environment, and why a shell function reaches the prompt but never an agent
