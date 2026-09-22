---
type: Finding
title: linkspector ignores the httpHeaders in its config
description: httpHeaders passes validation and is then dropped by both checking passes, so linkspector
  cannot authenticate a request and links behind a login are reported as broken.
tags:
- finding
- linkspector
- links
- github
- authentication
- bug
status: stable
stale_after: '2027-03-18'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
---
`httpHeaders` in `.linkspector.yml` is accepted by the schema, reported by the documentation,
and then **never reaches the network**. Neither of [linkspector](../tools/linkspector.md)'s two
checking passes sends it, so every request goes out unauthenticated and any link behind a login
is reported as broken with no indication that a credential was dropped.

The symptom is a configuration that looks correct and changes nothing. There is no warning, and
the failure is indistinguishable from the link genuinely being dead.

## Evidence

Verified empirically against 0.5.3, and the relevant code is unchanged in 0.5.6, the latest
release at the time of writing. Both passes are in `lib/batch-check-links.js`.

The **HTTP pass**, which settles anything returning a status, builds its request options without
consulting `httpHeaders` at all. The only header it will ever add is an `Authorization` it
constructs itself, from `GITHUB_TOKEN`, and only when the hostname is `github.com`.

The **Puppeteer pass** does look the configured headers up, and then passes them to
`page.goto(url, { headers })`. Puppeteer's `goto` has no `headers` option, so they are silently
discarded; `page.setExtraHTTPHeaders()` is the API that would have applied them.

Adding the missing lookup to the HTTP pass, eight lines, was enough to make a configured
`Authorization` header take effect, which confirms the diagnosis rather than merely being
consistent with it. Environment substitution works as documented in the same test, so `${VAR}`
in the configuration file is not the failing part.

The built-in `GITHUB_TOKEN` path does not rescue the case it looks like it was written for,
because [a GitHub token does not authenticate requests to github.com web pages](20260918_a_github_token_does_not_authenticate_github_com_web_pages.md)
in the first place. So that branch only ever raised the rate limit. It could not make a private
link resolve, with or without the `httpHeaders` bug.

## Why it matters

The two halves compound, and the order in which you meet them wastes the time. The obvious
reading of the configuration file is that authenticated checking is supported and that a token
in the environment is all that is missing, which sends you looking for a scope or an
authorisation problem on a token that was never sent. Establishing that the header does not
leave the process is the step that ends the search, and it takes one request to a server that
echoes what it received.

What remains is that a link into a repository requiring a credential cannot be checked by
linkspector as it ships. The link can be rewritten to the API with `replacementPatterns`, which
does work and which does discriminate correctly between a path that exists and one that does
not, but the rewritten request is still sent unauthenticated and still fails. Until the two
lookups are fixed upstream, the choices are to exclude such links with `ignorePatterns` and
check them another way, or to carry a patched build.
