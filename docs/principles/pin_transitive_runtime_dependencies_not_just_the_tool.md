---
type: Principle
title: Pin transitive runtime dependencies, not just the tool
description: When a tool drives a heavyweight external runtime, pin that runtime too, not only the tool's
  own version.
tags:
- principle
- software
- supply-chain
- pre-commit
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** When a tool drives an external runtime (a browser, an interpreter, a
container image), pin *that* too - not only the tool's own version.

**When to apply.** Any tool whose behaviour depends on a heavyweight runtime it
launches (headless browsers, Docker images, language runtimes). Skip for
self-contained binaries.

**Why.** Pinning the tool but letting it pull "whatever browser is latest" leaves
a mutable dependency in your supposedly-reproducible pipeline: the tool version
is frozen, yet results change when the runtime updates underneath it. A
link-checker that installs "latest Chrome" can start failing (or passing)
differently on the same commit. Pin the runtime to an explicit version and tie
it to the tool version with a comment so upgrades move together.

**Snippet.**

```yaml
# linkspector, the puppeteer that chooses the browser, and the exact Chrome
# that puppeteer release defaults to. All three move together.
entry: bash -c 'npx --yes puppeteer browsers install chrome@152.0.7977.75
                && linkspector check -c .linkspector.yml'
additional_dependencies: ['@umbrelladocs/linkspector@0.5.3', 'puppeteer@25.10.0']
```

The runtime here is not incidental: [linkspector](../tools/linkspector.md) resolves a link it
cannot settle with an HTTP request by loading the page in headless Chrome, so the browser is
part of what decides the answer.

**Pin whatever decides which runtime starts, not only the runtime.** An earlier version of this
snippet pinned Chrome and left `puppeteer` floating, which pins nothing, because
[puppeteer](../tools/puppeteer.md) launches the revision compiled into its own release rather
than the one just installed. That is
[a finding that cost a fortnight of red pull requests](../findings/20261009_an_unpinned_puppeteer_replaces_the_chrome_pinned_beside_it.md).

**How enforced.** Explicit version pins for the runtime alongside the tool, with
a paired comment. Extends the SHA-pinning family:
[Pin GitHub Actions to full commit SHAs](pin_github_actions_to_full_commit_shas.md), [Pin pre-commit hooks to frozen revisions](pin_pre_commit_hooks_to_frozen_revisions.md).
Same reproducibility goal, one layer up: [Install from a frozen lockfile in CI](install_from_a_frozen_lockfile_in_ci.md).
