---
type: Principle
title: Treat warnings as errors
description: Configure builds, linters and test runners to fail on warnings, so the count stays at zero
  and each new warning is seen.
tags:
- principle
- software
- dx
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [principle](index.md)"
    A reusable technical claim: something I would want true in any
    repository I work in.

**Claim.** Configure your build, compiler, linter and test tools to fail on
warnings, rather than letting them accumulate as ignorable noise.

**When to apply.** Broadly - compilers, build tools, linters, type checkers, test
runners. The most domain-general principle in this set. Loosen deliberately for
third-party/generated code you don't control, or during a large migration where a
temporary allowlist beats a blocked pipeline.

**Why.** Warnings that don't fail anything are warnings nobody reads: they pile up
until the signal (the *new* warning that matters) is lost in hundreds of tolerated
ones. Promoting them to errors keeps the count at zero, so each new warning is
seen and dealt with immediately, while the fix is cheap and the context is fresh.
It also prevents "works on my machine" drift where one environment warns and
another doesn't.

**Snippet.**

```bash
mkdocs build --strict          # docs: warnings fail the build
cc -Werror ...                 # C/C++
RUSTFLAGS="-D warnings" cargo build
pytest -W error                # Python: warnings become test failures
```

**How enforced.** A strict/`-Werror`-style flag in every build and CI invocation.
The general form of the docs site's `mkdocs build --strict`; siblings live under
[Guard invariants at commit-time, not review-time](guard_invariants_at_commit_time_not_review_time.md) in spirit but this one
reaches far beyond CI.
