---
type: Wish
title: Following people and projects like the old days of RSS
description: One place to follow blogs, projects and people across the internet, with read status shared
  between devices and no social media accounts to tend.
tags:
- wish
- software
- rss
- self-hosting
status: stable
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T00:00:00Z'
---
What Felix wanted from a way of keeping up with projects and people, which the
[Self-hosting Miniflux as a feed reader](../decisions/self_hosting_miniflux_as_a_feed_reader.md)
decision resolves.

## The wishes

- **One inbox for updates from anywhere** - blogs, project releases, people - read in one
  list rather than on each site that published them. The usability of a feed reader in the
  days when every site had a feed.
- **No social media accounts to manage.** An account created once, purely so something can
  follow people through it programmatically, is acceptable; one that has to be visited,
  curated or kept alive is not.
- **Blogs and plain feeds are enough to start.** Social platforms are a later extension, not
  a condition of the first version.
- **Read status shared across devices.** Something read on the phone is read on the laptop.
  That means either a self-hosted service, or a local reader with a sync option.
- **FOSS throughout**, the reader and anything it syncs through.

## What these rest on

[Prefer FOSS software wherever possible](../values/prefer_foss_software_wherever_possible.md)
rules out the hosted readers whose code is closed, and
[Prefer plain-text, tool-agnostic formats](../values/prefer_plain_text_tool_agnostic_formats.md)
asks that the list of subscriptions outlive whichever reader holds it.
