---
type: Finding
title: Git LFS fails when the remote URL has a trailing slash
description: A trailing slash on the remote path is tolerated by git and rejected by the LFS
  authentication endpoint, which reports it as a permissions error on a repository that cannot be found.
tags:
- finding
- git
- git-lfs
- authentication
- ssh
status: stable
stale_after: '2027-03-28'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
---
A remote URL ending in `/` works for every ordinary git operation and breaks Git LFS alone.
Clone, fetch and push are unaffected, because git normalises the path before it asks for
anything; Git LFS passes it through verbatim to `git-lfs-authenticate` over SSH, where GitHub
treats `owner/repo/` as a different repository from `owner/repo.git`, and answers accordingly:

```console
$ ssh git@HOST git-lfs-authenticate owner/repo/ download
{"auth_status":"bad_permissions","body":"Repository not found."}

$ ssh git@HOST git-lfs-authenticate owner/repo.git download
{"href": "https://lfs.github.com/owner/repo", "header": {"Authorization": "RemoteAuth ..."}}
```

The same credential, the same host, one character apart. The fix is to remove the slash:

```console
git remote set-url origin git@HOST:owner/repo.git
```

## Why it costs time

The response names the two things that are not wrong. `bad_permissions` points at the token
and `Repository not found` points at the URL's *existence*, so the search goes to scopes, to
single sign-on authorisation, to whether the account still has access, and to the SSH key.
Every one of those checks passes, and `ssh -T git@HOST` greets the right user by name whilst it
does, which is what makes the credential look exonerated rather than untested. Nothing in the
message distinguishes a path the server declines to serve from one it declines to acknowledge,
and that is the distinction the whole finding turns on.

A host alias from `~/.ssh/config` deepens it. `git lfs env` reports an endpoint built from the
alias rather than from `github.com`:

```text
Endpoint=https://HOST-ALIAS/owner/repo.git/info/lfs (auth=none)
```

That line is a plausible culprit and an innocent one. Git LFS guesses an HTTPS endpoint from
the remote URL and then replaces it with whatever the SSH round trip returns, so the alias
never reaches the network, and `auth=none` describes an empty cache rather than a missing
credential. Reproducing the error with the alias removed is what rules it out, and is worth
doing early, because a wrong hostname printed by the tool's own diagnostic is the most
convincing wrong answer available here.

## The failure is not confined to the object

The LFS smudge filter runs during checkout, so its failure aborts the checkout partway. A
`git reset --hard` that hits this leaves the index holding staged deletions for every file it
had already processed, which presents as a repository that has deleted itself:

```console
$ git reset --hard
...
Error downloading object: docs/diagram.png (0a1b2c3): Smudge error: ...
  batch request: {"auth_status":"bad_permissions","body":"Repository not found."}
fatal: docs/diagram.png: smudge filter lfs failed

$ git status --porcelain | wc -l
147
```

Nothing is lost, and the state is the aborted reset rather than the original problem, but the
volume of it invites a response aimed at the deletions. Repeating the reset once the URL is
corrected restores the tree and empties the index in one step. Running `git lfs ls-files` and
opening one of the files afterwards confirms the objects arrived as content rather than as
pointer text, which a clean `git status` on its own does not.

## Where the slash comes from

Nobody types it. It arrives from a clone command copied out of a web interface, an onboarding
document, or a setup script that joins a base URL to a repository name, and it survives
because every check anyone would run on a fresh clone passes. Correcting one working copy
leaves the source of it in place, so the next clone on that machine, or the first clone on a
colleague's, reproduces the whole search from the beginning.
