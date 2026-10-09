---
type: Tool
title: puppeteer
description: Google's browser automation library, and the reason a project that pins a browser version
  can still launch a different one, because each release hardcodes a default Chrome revision of its own.
tags:
- tools
- puppeteer
- supply-chain
- pre-commit
- testing
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T13:10:00+02:00'
sources:
- id: puppeteer-repo
  resource: https://github.com/puppeteer/puppeteer
  title: 'puppeteer/puppeteer: JavaScript API for Chrome and Firefox'
  last_modified: '2026-10-09'
- id: puppeteer-revisions
  resource: https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-core/src/revisions.ts
  title: 'puppeteer-core: PUPPETEER_REVISIONS'
  last_modified: '2026-10-09'
---
puppeteer[^puppeteer-repo] drives a browser from JavaScript. It is rarely a direct dependency
here: it arrives underneath something else, which is what makes the one fact on this page worth
writing down.

| | |
| --- | --- |
| Author | Google, from the Chrome DevTools team |
| Licence | Apache-2.0 |
| Language | TypeScript |
| Distribution | npm, as `puppeteer` and as `puppeteer-core` |
| Source | [github.com/puppeteer/puppeteer](https://github.com/puppeteer/puppeteer) |
| Version read | 25.13.0, the latest release |

## Every release carries its own browser version

`PUPPETEER_REVISIONS` in `puppeteer-core` names one exact Chrome build per
release[^puppeteer-revisions]. `puppeteer` downloads that build on install and launches it by
default; `puppeteer-core` ships the same constant but downloads nothing, leaving the caller to
say which browser to use.

The constant moves roughly every two releases, and quickly:

| Release | Default Chrome |
| --- | --- |
| 25.4.0 | 151.0.7922.47 |
| 25.6.0 | 151.0.7922.77 |
| 25.8.0 | 152.0.7977.42 |
| 25.9.0 | 152.0.7977.54 |
| 25.10.0 | 152.0.7977.75 |
| 25.11.0 | 153.0.8010.36 |
| 25.12.0 | 154.0.8037.57 |
| 25.13.0 | 155.0.8059.39 |

Those were read out of the published tarballs, from `package/src/revisions.ts`, which is the way
to answer the question for a release that is not the current one.

**`puppeteer browsers install chrome@<version>` adds a browser to the cache. It does not change
which one gets launched.** The two look interchangeable and are not: one populates a directory,
the other is a constant compiled into the library. A project that installs a pinned Chrome and
leaves the library version floating has pinned nothing, which is
[the finding this page exists for](../findings/20261009_an_unpinned_puppeteer_replaces_the_chrome_pinned_beside_it.md).

## Where it turns up here

Underneath [linkspector](linkspector.md), whose second checking pass loads a page in headless
Chrome for any link an HTTP request could not settle. The browser is part of what decides
whether a link is reported as broken, which is why
[Pin transitive runtime dependencies, not just the tool](../principles/pin_transitive_runtime_dependencies_not_just_the_tool.md)
names it rather than treating it as an implementation detail of the link checker.
