---
type: Guide
title: Pin the browser behind a pre-commit link checker
description: How to pin puppeteer so a link checker's headless Chrome is reproducible, which version
  to choose, and why a separate chrome install line is a liability rather than a safeguard.
tags:
- guide
- puppeteer
- linkspector
- pre-commit
- supply-chain
- links
status: stable
stale_after: '2027-04-09'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T17:30:00+02:00'
---
[linkspector](../tools/linkspector.md) settles whatever an HTTP request cannot by loading the
page in headless Chrome, so the browser is part of what decides whether a link is reported as
broken. [Pin transitive runtime dependencies, not just the tool](../principles/pin_transitive_runtime_dependencies_not_just_the_tool.md)
says that browser has to be pinned. This is how, and the order matters because the obvious way
round is the wrong one.

**Pin the library, then read the browser off it.** [puppeteer](../tools/puppeteer.md) launches
the Chrome revision compiled into its own release. Pinning a browser version without pinning
puppeteer pins nothing, which is
[a finding that cost a fortnight of red pull requests](../findings/20261009_an_unpinned_puppeteer_replaces_the_chrome_pinned_beside_it.md).

## 1. Find the range the checker allows

linkspector depends on puppeteer itself, with a caret range that differs by release, so the
version to pin is constrained by the linkspector version already pinned beside it:

```bash
npm view @umbrelladocs/linkspector@0.5.3 dependencies.puppeteer   # ^24.37.5
npm view @umbrelladocs/linkspector@0.5.6 dependencies.puppeteer   # ^25.2.1
```

Pinning outside that range installs two copies of puppeteer and leaves which one runs to npm's
resolution, which is the opposite of the point.

## 2. Pick the version the range resolves to today

Take the newest release inside the range. Pinning it freezes what would have been installed
anyway, so nothing changes on the day of the pin and nothing changes on any day after it:

```bash
npm view puppeteer-core versions --json
```

## 3. Read the Chrome it carries, for the comment

The mapping is not published as a table anywhere; it is a constant in the package, and the only
reliable way to get it for a release that is not current is to unpack that release:

```bash
npm pack puppeteer-core@24.39.1
tar -xzOf puppeteer-core-24.39.1.tgz package/src/revisions.ts | grep chrome
# chrome: '146.0.7680.76',
```

## 4. Write the pin with the mapping beside it

```yaml
- id: linkspector
  name: Check broken links (linkspector)
  entry: linkspector check -c .linkspector.yml
  language: node
  # puppeteer is pinned exactly, not left to linkspector's own `^24.37.5`.
  # It is what decides which Chrome launches. 24.39.1 -> Chrome 146.0.7680.76.
  additional_dependencies: ['@umbrelladocs/linkspector@0.5.3', 'puppeteer@24.39.1']
  pass_filenames: false
  files: \.md$
```

The comment is doing real work: the version pair cannot be checked against anything in the
repository, so without it the next reader has only two opaque numbers and no way to tell whether
they still agree.

## 5. Do not add a separate browser install step

The tempting shape is an extra command that installs an exact Chrome before the check:

```yaml
entry: bash -c 'npx --yes puppeteer browsers install chrome@148.0.7778.97 && linkspector check -c .linkspector.yml'
```

**This does not do what it looks like.** It populates the puppeteer cache; it does not change
which revision puppeteer launches. If the number differs from the pinned release's own default,
the install is wasted work and the browser under test is not the one named in the file. If it
matches, it is a second copy of a fact that is already stated by the pin, free to drift from it.

Delete it, and let `puppeteer` download its own default on install. One version, stated once.

## 6. Check it actually launches

A browser that fails to start reports as a broken link, so a green run is the only confirmation
that the pin works:

```bash
prek run linkspector --all-files
```

Worth doing on the machine *and* letting CI do it, because the two have different caches and a
Chrome that starts on a developer's desktop does not always start on a runner.

## Keeping it moving

Dependabot's `pre-commit` ecosystem bumps `additional_dependencies`, so the pin does not rot
quietly. A bump to linkspector that moves its puppeteer range will want step 1 again, and the
comment from step 4 is what tells a reviewer that the two numbers in the diff belong together.

Versions read: linkspector 0.5.3 and 0.5.6, puppeteer 24.39.1 and 25.10.0, on 9 October 2026.
