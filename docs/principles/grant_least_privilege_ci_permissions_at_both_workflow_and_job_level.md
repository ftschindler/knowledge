---
type: Principle
title: Grant least-privilege CI permissions at both workflow and job level
description: Declare a restrictive permissions baseline at the workflow level and narrow it per job, so
  each job holds only what it uses.
tags:
- principle
- software
- github-actions
- ci-cd
- security
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Claim.** Declare the *minimum* token permissions a workflow needs, explicitly -
set a restrictive baseline at the workflow level, then narrow (or selectively
elevate) per job, so each job holds only what it actually uses.

**When to apply.** Any CI system with scoped tokens (GitHub Actions `permissions`,
etc.). Broadly applicable.

**Why.** CI tokens run with whatever scope you grant; the platform default is
often far broader than needed, so a compromised action or dependency in *any* job
inherits write access to your repo, releases or pages. Setting a tight
workflow-level baseline and granting elevated scopes to only the one job that
needs them (e.g. the deploy job gets `pages: write`/`id-token: write`, everything
else stays read-only) contains blast radius. Prefer OIDC (`id-token`) over
long-lived stored secrets where the platform supports it.

**Snippet.**

```yaml
permissions:            # workflow-level baseline: minimal
  contents: read
jobs:
  deploy:
    permissions:        # only this job elevates
      pages: write
      id-token: write
```

**How enforced.** Explicit `permissions:` blocks at both levels; no reliance on
inherited defaults. Related: [Pin GitHub Actions to full commit SHAs](pin_github_actions_to_full_commit_shas.md) (same
supply-chain threat model).
