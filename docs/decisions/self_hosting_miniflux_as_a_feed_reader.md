---
type: Decision
title: Self-hosting Miniflux as a feed reader
description: Why Miniflux and its Postgres database, behind the existing Traefik on a rootless Docker server,
  meet the feed-reading wishes, and why RSSHub waits.
tags:
- decision
- software
- rss
- self-hosting
- docker
status: draft
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T00:00:00Z'
---
How Felix chose to follow people and projects: a self-hosted
[Miniflux](https://miniflux.app) on the dedicated server that already runs Traefik on
[rootless Docker](../tools/docker.md).

## What was wanted

The [Following people and projects like the old days of RSS](../wishes/following_people_and_projects_like_the_old_days_of_rss.md)
wishes, in short: one inbox, no accounts to tend, read status on every device, FOSS.

## What it rests on

- [Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md) -
  Miniflux is Apache-2.0, and every client considered is FOSS.
- [Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md) -
  subscriptions leave the reader as OPML, a plain XML list any other reader imports.

## What that led to

**Miniflux, over FreshRSS.** Both are FOSS, self-hostable and speak the same sync protocols.
Miniflux is one Go binary and a Postgres database, with a deliberately small interface;
FreshRSS is a PHP application with extensions, multi-user setup and a built-in scraper for
pages without feeds. The extra surface is what tipped it: a reader is meant to sit in the
background, and Miniflux has less of it to maintain.

**The server is the sync.** Read, starred and saved state lives in Miniflux's database, so
every device that talks to the server sees the same state. Nothing else needs running for it.
The browser interface covers any device; native apps (Newsflash on Linux, Read You or Capy
Reader on Android, NetNewsWire on Apple) connect through the Google Reader API, which is a
setting in Miniflux with its own credentials rather than another service.

**Most sources already publish feeds, so no accounts are needed.**

| Source | Feed address |
| --- | --- |
| Mastodon and the Fediverse | the profile URL with `.rss` appended |
| Bluesky | `https://bsky.app/profile/<handle>/rss` |
| GitHub releases, tags, commits | `/releases.atom`, `/tags.atom`, `/commits/<branch>.atom` on the repository |
| GitHub user activity | `https://github.com/<user>.atom` |
| YouTube channel | `https://www.youtube.com/feeds/videos.xml?channel_id=<id>`, found by Miniflux from the channel URL |
| Reddit | most pages, with `.rss` appended |

**The compose service is two containers.** Miniflux joins the Traefik network and an internal
one; Postgres joins only the internal one, with a named volume. Only Traefik publishes ports.

**Backups cover what only the server knows.** A nightly `pg_dump` holds the read state. A
scheduled OPML export through the API, committed to git, keeps the subscription list as a file
Felix owns independently of the database.

## What is left out, and would be reconsidered

**RSSHub is deferred.** It turns pages without a feed, such as X profiles, Telegram channels
or many news sites, into feeds Miniflux can follow, and is the place a throwaway account would
come in, since some of its routes need login cookies. It scrapes, so routes break when sites
change, and its recommended setup adds Redis and a headless browser. It joins the internal
network, without Traefik labels, the first time a wanted source has no feed of its own.

**Walled gardens stay out.** X and LinkedIn are fragile through any bridge, account or not,
and nothing here is built around them.

**Nothing is deployed yet.** The compose file, its Traefik labels and the backup timer become
a blueprint once they have run on the server, not before.
