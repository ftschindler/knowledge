---
type: Finding
title: An unpinned puppeteer replaces the Chrome pinned beside it
description: Pinning a browser version next to an unpinned puppeteer pins nothing, because the library
  launches the revision compiled into its own release rather than the one just installed.
tags:
- finding
- puppeteer
- linkspector
- pre-commit
- supply-chain
- ci-cd
status: stable
stale_after: '2027-04-09'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-09T13:20:00+02:00'
---
A pre-commit hook that had passed for months started failing on every pull request, with two
different Chrome versions in one error:

```text
Check broken links (linkspector).....Failed
  chrome@152.0.7977.64 .../chrome/linux-152.0.7977.64/chrome-linux64/chrome
  💥 Main error: Failed to launch the browser process
  #0 ... /chrome/linux-155.0.8059.39/chrome-linux64/chrome
```

The first line is the install step reporting success. The stack trace is a different browser
entirely, three major versions ahead, and that is the one that crashed.

## The pin that was not a pin

The hook installed an exact Chrome and declared its dependencies like this:

```yaml
additional_dependencies: ["@umbrelladocs/linkspector@0.5.6", "puppeteer"]
```

Two versions were pinned and the third was not. [puppeteer](../tools/puppeteer.md) resolves to
whatever is current at install time, and **each puppeteer release launches the Chrome revision
compiled into it**, not the one sitting in the cache from an earlier command. So the installed
browser was never the browser under test. The arrangement worked only because the current
puppeteer happened to default to a 152 build, close enough to the pinned 152 to be
indistinguishable from the thing actually working.

That held until upstream moved: 25.11.0 defaults to Chrome 153, 25.12.0 to 154, and 25.13.0 to
155, which does not start at all on a GitHub Actions `ubuntu-latest` runner. Nothing in the
repository changed on the day it broke.

The pinned value was `chrome@152.0.7977.64`, and no puppeteer release has ever defaulted to that
build. The two had never been in step. They had only ever been adjacent.

## Why it was not noticed for a fortnight

The hook is one of several in a job that gates every pull request, so the breakage was loud in
the sense of being red and silent in the sense of saying anything about its cause. The job had
last run green on 25 September. Everything opened in between failed on something that had
nothing to do with it, which is the expensive shape: the failure arrives attached to whatever
change happens to be in flight, and reads as that change's fault.

What the outage cost separately was link checking itself. With the browser failing to launch,
nothing was being checked, and a genuinely broken link went in and sat there until the hook ran
again.

## The repair

Pin the library and derive the browser from it, rather than pinning the browser and hoping:

```yaml
additional_dependencies: ["@umbrelladocs/linkspector@0.5.6", "puppeteer@25.10.0"]
```

```javascript
const CHROME = "chrome@152.0.7977.75";
```

The two values are now one fact stated twice, and the mapping is checkable: unpack the published
tarball and read `package/src/revisions.ts`.

## What the principle was missing

[Pin transitive runtime dependencies, not just the tool](../principles/pin_transitive_runtime_dependencies_not_just_the_tool.md)
already said to pin the browser, and the snippet it carried was the configuration that broke.
The claim was right and the worked example was wrong in exactly the way that is hardest to see:
it pinned the runtime, and left unpinned the library that chooses the runtime.

**A runtime is pinned by whatever decides which runtime starts.** Naming a version somewhere in
the file is not the same thing, and an explicit version string beside an implicit one reads as
rigour whilst providing none.
