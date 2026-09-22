---
type: Finding
title: A GitHub token does not authenticate requests to github.com web pages
description: A token sent to a github.com page is ignored, so a private repository returns the same 404
  it returns to a stranger; only the API and the raw host honour it.
tags:
- finding
- github
- authentication
- api
- links
status: stable
stale_after: '2027-03-18'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: github-rest-auth
  resource: https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
  title: 'GitHub: Authenticating to the REST API'
  last_modified: '2026-09-18'
---
An `Authorization` header sent to a `github.com` **web page** is ignored. A repository you can
read in the browser, whilst signed in, answers a token-bearing request with the same `404` it
gives an anonymous stranger, and the token changes nothing about the response. Tokens
authenticate the REST API[^github-rest-auth], and separately the raw content host, not the
website.

The trap is that `404` rather than `401` is what a private resource returns, deliberately, so
that its existence is not disclosed. That means the response to a request you thought was
authenticated is byte-identical to the response for a repository that was deleted, renamed, or
never existed. Nothing in it says "your credential was not used".

## Evidence

Verified empirically on 2026-09-18, against a repository in an organisation the token's account
can read:

```console
$ curl -o /dev/null -w '%{http_code}\n' https://github.com/ORG                       # no token
404
$ curl -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
    https://github.com/ORG                                                           # token
404
$ curl -o /dev/null -w '%{http_code}\n' -H "Authorization: Bearer $TOKEN" \
    https://api.github.com/orgs/ORG
200
```

The first two responses being identical is the whole finding. The API accepts the same token on
the same host name suffix, as does `raw.githubusercontent.com`, which returns the file body for
a private path given the same header.

The API also discriminates correctly rather than merely answering, which matters if you intend
to check anything with it. A path that exists returns `200` and a path that does not returns
`404`, on the same repository and with the same credential, so a negative answer is
informative:

```console
$ curl ... "https://api.github.com/repos/ORG/REPO/contents/README.md?ref=BRANCH"
200
$ curl ... "https://api.github.com/repos/ORG/REPO/contents/NOPE.md?ref=BRANCH"
404
```

## Why it matters

Anything that follows a `github.com` URL on your behalf inherits this. A link checker, a
documentation build, a script that verifies references: adding a token to it is a change that
looks like it should work, produces no error, and leaves every private link reported as broken.
The time is lost afterwards, on the assumption that the token is at fault, checking scopes and
single sign-on authorisation on a credential that was never sent anywhere that would have read
it. This is the half of
[linkspector ignores the httpHeaders in its config](20260918_linkspector_ignores_the_httpheaders_in_its_config.md)
that would still bite after the bug in that tool is fixed.

Two things follow. First, **check the API rather than the page**. The ordinary web URLs map
onto it mechanically, which is a rewrite a link checker can be configured to do:

| Web URL | API equivalent |
| --- | --- |
| `github.com/ORG/REPO` and most paths under it | `api.github.com/repos/ORG/REPO` |
| `github.com/ORG/REPO/{blob,edit,tree}/REF/PATH` | `api.github.com/repos/ORG/REPO/contents/PATH?ref=REF` |

The mapping is not total. A pull request, a release tag or a discussion needs its own endpoint,
so a rewrite that silently passes what it does not recognise is worse than one that refuses it.

Second, **probe before you conclude**. One request to `api.github.com/orgs/ORG` separates the
two cases the `404` conflates, because a credential problem surfaces there as `401 Bad
credentials` whilst a working credential returns the organisation. Run it before reporting
anything as missing, and the difference between "this link is dead" and "I am not who I think I
am" stops costing an afternoon.
