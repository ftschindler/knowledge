---
type: Guide
title: Let CI push to a protected branch with a GitHub App
description: How to give a workflow write access past branch protection using an App installed on one
  repository, minting an hour-long token, rather than a maintainer's personal access token.
tags:
- guide
- github
- github-actions
- ci-cd
- authentication
- secrets
status: stable
stale_after: '2027-03-21'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
sources:
- id: gh-app-installation-tokens
  resource: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
  title: 'GitHub: Authenticating as a GitHub App installation'
  last_modified: '2026-09-21'
- id: create-github-app-token
  resource: https://github.com/actions/create-github-app-token
  title: actions/create-github-app-token
  last_modified: '2026-09-21'
---
Some workflows have to write to the branch they are protecting: a release job that stamps a
version file and tags it, a bot that regenerates a lockfile, a docs build that commits what it
rendered. The token a job is handed by default cannot do it. `GITHUB_TOKEN` is deliberately
excluded from bypassing branch protection, and pushes made with it start no further workflow
runs, both of which are the right defaults everywhere except here.

The usual answer is a personal access token in a repository secret, and it works. What it costs
is that the credential is a **person's** standing access: it carries whatever that account can
reach, it does not expire, the commits it makes are attributed to a human who did not make them,
and revoking it disturbs that human's own work. A GitHub App installed on the one repository is
smaller in every one of those directions. It holds a single permission, the token it mints
expires about an hour after it is issued[^gh-app-installation-tokens], it is not a person, and
the commits read as a bot's.

Four things have to exist, and only the last of them lives in the repository. Three are done
once, by hand, by somebody with admin on it.

## 1. Create the App

Your account's **Settings → Developer settings → GitHub Apps → New GitHub App**. An App is
owned by an account or organisation, not by a repository, which is the first thing that surprises
people looking for it under the repository's settings.

- **Name** it for what it does, because the name becomes the committer: `something-release`
  appears in the history as `something-release[bot]`.
- **Repository permissions: Contents → Read and write.** That one permission covers pushing a
  commit, pushing a tag and creating a release. Nothing else is needed, and per
  [Grant least-privilege CI permissions at both workflow and job level](../principles/grant_least_privilege_ci_permissions_at_both_workflow_and_job_level.md)
  nothing else should be granted. Metadata read-only is added for you and cannot be removed.
- **Uncheck "Active" under Webhook.** GitHub never calls this App; the workflow calls GitHub
  with it. Leaving the webhook active asks for a URL that does not exist.
- **Where can this App be installed: only on this account**, unless you mean to share it.

Then **generate a private key**, at the bottom of the App's settings page. The `.pem` downloads
once and cannot be downloaded again. It is the credential: everything else on this page is
public configuration.

## 2. Install it on the repository

From the App's page, **Install App**, and select **only the repository that needs it**. An App
is created and installed in two separate acts, and an App that exists but is installed nowhere
produces a token request that fails with a message about the installation rather than about
permissions, which reads like a permissions problem for as long as you let it.

Note the **App ID** from the App's settings page whilst you are there.

## 3. Put two secrets on the repository

**Settings → Secrets and variables → Actions**, on the repository, not on the App:

| Secret | Value |
| --- | --- |
| `RELEASE_APP_ID` | the numeric App ID |
| `RELEASE_APP_PRIVATE_KEY` | the entire `.pem`, including the `-----BEGIN` and `-----END` lines |

The App ID is not sensitive and could be a repository *variable* instead; keeping it beside the
key as a secret costs nothing and keeps the pair together. The `.pem` now belongs nowhere else:
not in the repository, not in a password manager as a working copy. If it leaks or is lost,
generate a new key from the App's page, which invalidates the old one, and update the secret.

Repository secrets are not exposed to workflows triggered by a pull request from a fork. That is
correct, and it is why a job like this is triggered by `push` to the protected branch rather than
by the pull request that preceded it.

## 4. Mint the token in the workflow

`actions/create-github-app-token`[^create-github-app-token] exchanges the App ID and private key
for an installation token, pinned by full commit SHA like every other action, per
[Pin GitHub Actions to full commit SHAs](../principles/pin_github_actions_to_full_commit_shas.md):

```yaml
- name: Mint a token for the release bot
  id: token
  uses: actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1  # v3.2.0
  with:
    app-id: ${{ secrets.RELEASE_APP_ID }}
    private-key: ${{ secrets.RELEASE_APP_PRIVATE_KEY }}

- name: Checkout
  uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1  # v7.0.1
  with:
    fetch-depth: 0
    token: ${{ steps.token.outputs.token }}
```

The token has to be given to `checkout`, not only to the step that pushes: `checkout` is what
writes the remote's credentials into the working copy, and a later `git push` uses whatever it
left behind.

## 5. Allow the App past the branch rule

This is the step that is not a permission, and the one that gets forgotten. **Settings → Rules →
the ruleset protecting the branch → Bypass list → Add → the App.** Classic branch protection
has the same control under "Allow specified actors to bypass required pull requests".

Without it everything above is correct and the job still fails, at the last step, with
`protected branch hook declined`. Which is the right failure, being loud and before anything is
tagged, but it looks like a permissions problem and is not one: `Contents: write` says the App
may write to the repository, whilst the bypass list says the branch rule does not apply to it.
Two different questions, asked in two different places.

## 6. Give the bot its committer identity

A commit is attributed to an account by its email address, and a bot's address has to carry the
bot's **numeric user id**. Get it wrong and the commits render with a grey avatar and link
nowhere, which is how a history quietly stops answering "who did this".

Ask for the id at run time rather than pasting it in, so the workflow keeps working when the App
is recreated:

```yaml
- name: Work out who the bot commits as
  id: identity
  env:
    GH_TOKEN: ${{ steps.token.outputs.token }}
    SLUG: ${{ steps.token.outputs.app-slug }}
  run: |
    set -euo pipefail
    id=$(gh api "/users/${SLUG}[bot]" --jq .id)
    echo "name=${SLUG}[bot]" >> "${GITHUB_OUTPUT}"
    echo "email=${id}+${SLUG}[bot]@users.noreply.github.com" >> "${GITHUB_OUTPUT}"
```

## What changes once it works

**Pushes made with an App token do start workflows**, unlike pushes made with `GITHUB_TOKEN`.
This is the one behavioural difference that can bite after everything is configured correctly,
because a job that pushes to the branch it triggers on now triggers itself. Make the recursion
terminate by construction rather than by a `[skip ci]` in a commit message: the job I wrote this
for releases only when the merge it is reacting to came in on a labelled pull request, and its
own push comes in on none, so the second run finds nothing to do and stops. A path filter or a
committer check does the same job.

**The token dies within the hour.** A run log leaked tomorrow is worth nothing, which is the
practical difference from a PAT and the reason to prefer this even where a PAT would be
permitted.

**Revocation is cheap.** Uninstalling the App from the repository ends its access without
touching anyone's own account, and nothing has to be rotated anywhere else.

A worked example of all six steps is the release job in
[federated-knowledge-skills](../tools/federated_knowledge_skills_schindler.md), which stamps a
version file into the default branch and tags it on every merge.
