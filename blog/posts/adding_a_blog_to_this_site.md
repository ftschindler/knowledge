---
title: Adding a blog to a knowledge base that already has a log
date: 2026-09-22
description: Why the append-only log and the git history were not enough, and the twelve lines of hook
that put dated posts next to the bundle without putting them in it.
---

This site now has a blog, and this is the first post on it. The short version: the knowledge
base already recorded everything I do, in two places nobody reads.

<!-- more -->

## What was already there

Every change here lands in `log.md`, append-only, newest first, one line per logical change. It
is a good record and a bad read. Entries carry no links, on purpose, because the log is
append-only whilst its subjects get renamed and moved, so a link there rots and cannot be
repaired without falsifying the record.

The git history is the same trade taken further. Both are written for whoever already knows what
I am working on, which on most days is nobody but me.

## What was missing

A page that says what I did and hands you the door. The concepts here each carry one idea and
open in the middle of an argument, which is right for a knowledge base and unhelpful as an
introduction. Nothing on the site was addressed to somebody arriving without the thread.

So the blog carries no reasoning at all. A post is a date, what changed, and the links out.

## Where it lives

Not in the bundle. Every non-reserved markdown file under `docs/` is a concept in the
[Open Knowledge Format](https://github.com/GoogleCloudPlatform/open-knowledge-format) sense, so a
post there would need a type, a genre and a place in an index. It sits in `blog/` instead, a
sibling of `docs/`, exactly as `about/` already does.

The hook that publishes `about/` now publishes both. It injects the files into the MkDocs build
and rewrites the links that cross from a sibling into the bundle, because `../../docs/tools/x.md`
is true on disk and `../../tools/x.md` is what MkDocs resolves. Authors write the form the editor
and GitHub follow, and the build corrects it.

**The link rule is what keeps this honest.** A post links into concepts; no concept ever links to
a post. The bundle stays readable and portable on its own, and the blog is a reading surface laid
over it rather than a part of it.

## The part I got wrong first

I assumed Material's blog plugin would not see files a hook injects, because MkDocs runs hooks
after plugins. Reading the plugin says otherwise: its `on_files` carries `@event_priority(-50)`,
with a comment that it runs late on purpose so other code can add posts first. It was built for
this. One line of configuration, and it discovers posts by path in the injected directory.

Worth the two minutes it took to read the source instead of trusting what I remembered.

## What it took

A rename, twelve lines in the hook, one plugin entry, and one line of navigation. Details, with
the reasoning, in [the publishing stack](../../docs/blueprints/mkdocs_material_pkb_publishing_stack.md)
and [the tech stack page](../../about/tech_stack.md).
