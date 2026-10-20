---
type: Investigation
title: 'The deutsche-bahn agent skill: security and telemetry'
description: A source read of one skill from the travel-hacking-toolkit, asking what it runs, where its
  traffic goes and what a German rail operator learns about the person running it.
tags:
- security
- data-privacy
- agent-skills
- supply-chain
- ai-agents
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-10-20T00:00:00Z'
sources:
- id: tht-repo
  resource: https://github.com/borski/travel-hacking-toolkit
  title: 'borski/travel-hacking-toolkit'
  last_modified: '2026-10-19'
- id: vendo-repo
  resource: https://github.com/public-transport/db-vendo-client
  title: 'public-transport/db-vendo-client'
  last_modified: '2026-10-20'
---
**Context** - the `deutsche-bahn` skill from the travel-hacking-toolkit was a candidate for
installation on a personal machine. The question asked before installing: **what does it
execute, where does its traffic go, and what does the other end learn?**

- **Version read**: commit `01426c5`, 2026-10-19[^tht-repo], with `db-vendo-client` `6.10.8`
  resolved from the skill's own lockfile[^vendo-repo]
- **Method**: full read of `SKILL.md` and `scripts/search_trains.mjs`; a package-lock walk of
  all 45 transitive dependencies for install scripts and non-npm registries; a literal scan of
  the installed `db-vendo-client` tree for every URL and every network primitive; a read of its
  request layer and the `db` profile's endpoint table; `npm audit`; and one real invocation,
  which failed at DNS resolution and named the host it had tried.

## Verdict

**No telemetry, no analytics, no phone-home, and no destination other than Deutsche Bahn.**
Every URL in the installed tree belongs to `app.vendo.noncd.db.de`, DB's own mobile backend.
The one invocation attempted exactly that host and nothing else. The script reads `argv`,
prints to stdout, writes no files and reads no environment variable of its own; the only one
consulted anywhere in the path is `HTTPS_PROXY`, by the HTTP layer, for the ordinary reason.

What the skill does expose is not covert. It queries an **undocumented internal API with a
user agent that names the toolkit**, and DB sees every journey you plan through it.

## What runs, and against what

`search_trains.mjs` is 174 lines of argument parsing and table formatting around three calls
into `db-vendo-client`: `locations`, `journeys`, `departures`. It constructs its client with
the `db` profile, whose endpoints are fixed in a JSON file:

| Called as | Endpoint |
| --- | --- |
| `stations` | `https://app.vendo.noncd.db.de/mob/location/search` |
| `journeys` | `https://app.vendo.noncd.db.de/mob/angebote/fahrplan` |
| `departures` | `https://app.vendo.noncd.db.de/mob/bahnhofstafel/` |

The host is the one behind the DB Navigator app, not an open-data service. `db-vendo-client`
is upfront about the position this puts a caller in: "strictly speaking, permission is
necessary to use this library with the DB APIs"[^vendo-repo]. The library is ISC-licensed and
published by the `public-transport` organisation, which is the long-standing maintainer of
`hafas-client`, so this is a known project rather than an anonymous wrapper, but the legal
footing is the user's, not the library's.

## What DB learns

Three identifiers travel with each request, and they behave differently.

**The user agent is a constant, and it names the toolkit.** The script passes
`'travel-hacking-toolkit'` as the client identifier. `db-vendo-client` rejects a handful of
placeholder strings outright, on the grounds that the field should tell an API operator how to
reach the caller, and this one satisfies that check whilst telling DB only which tool is being
run. The `db` profile does not set `randomizeUserAgent`, so the string goes out verbatim on
every request: traffic from this skill is trivially separable from browser traffic in DB's
logs, and attributable to the toolkit's user base rather than to a person.

**The correlation ID is fresh per request.** Requests carry `X-Correlation-ID` built from two
newly generated v4 UUIDs. It links nothing across invocations and is not a stable device
identifier.

**The query content is the real disclosure, and it is unavoidable.** A journey search sends
origin, destination, date and time. Run against your own trips, over a public IP, with a
distinguishing user agent, that is a travel-planning history held by a third party. This is
what the skill is *for*, so it is not a finding against it - but it is the exposure that
matters, and it is larger than anything a telemetry endpoint would have collected.

## Supply chain

The skill ships its own `package.json` and `package-lock.json`, so the dependency set is
pinned and readable before installing anything. It resolves to **45 packages, all from
`registry.npmjs.org`, none with an install script**. They are the ordinary small-module
substrate - `qs`, `node-fetch`, `luxon`, `uuid`, `readable-stream` - plus
`db-hafas-stations`, a local station dataset.

`npm audit` reports two moderate advisories, and neither is reachable from this code path:

- **`qs`**, two denial-of-service advisories in its *parser*. Here `qs` is used only to
  serialise outbound query strings. Nothing attacker-controlled is parsed.
- **`uuid`**, a missing buffer bounds check in v3/v5/v6 when a `buf` argument is supplied.
  The correlation ID uses v4 with no buffer.

Both are worth fixing on the next upgrade rather than before the first run.

!!! warning "The surrounding repository is a larger surface than the skill"
    The skill is self-contained, but the toolkit it lives in ships a `.mcp.json` declaring six
    MCP servers - five remote HTTP endpoints at third-party travel vendors, and one spawned as
    `npx -y @openbnb/mcp-server-airbnb@latest --ignore-robots-txt`, which pulls the latest
    published version at every start. Those are a different and much wider trust decision, and
    they have nothing to do with train schedules. Taking one skill out of the repository
    leaves all of it behind; cloning the repository and running its setup does not.

This is the argument for a per-skill subscription rather than a repository clone. One skill
from a toolkit is one 174-line script and a lockfile you can read in an afternoon, which is
roughly what this page is.

## Using it with the exposure understood

1. **Decide whether DB seeing your itineraries is acceptable**, because that is the actual
   cost and nothing in the configuration changes it.
2. **Change the user agent if you would rather not be counted as a toolkit user** - it is one
   string literal in `scripts/search_trains.mjs`, and the library only requires that it not be
   one of the known placeholders. Something that genuinely identifies you is what the field is
   asking for.
3. **Respect the rate limits the skill documents.** DB's backend enforces low ones, and the
   script applies no throttling of its own, although the library ships a `withThrottling`
   wrapper it does not use.
4. **Take the skill, not the repository**, unless the six MCP servers have been assessed on
   their own terms.
5. **Re-read the lockfile on upgrade.** Forty-five transitive dependencies with no install
   scripts today is a property of this commit, not a guarantee.

## Bottom line

The skill is clean in the sense the question was asked: it reports nothing to anyone, reaches
exactly one host, and that host is the one it says it uses. The residual risk is not hidden
anywhere in it. It is that querying an undocumented operator API, under a user agent that
names the tool, hands a German rail company a log of where you are planning to travel - and
that the repository around the skill asks for a great deal more trust than the skill itself
does.
