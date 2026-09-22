---
title: Adding a blog to this site
date: 2026-09-22
description: Why the append-only log and the git history were not enough, and where the posts sit.
---

This site now has a blog, and this is the first post on it. The short version: the knowledge
base already records how it's evolving, but nothing in there is a good entry point for humans to read what I did when and why.

I realised this when struggling to note down how [ponytail](../../docs/tools/ponytail_gebert.md) could interact with my [opencode](../../docs/tools/opencode.md) stack: it was a bit of research, and a proposal for a decision on what to do. However, I never did it, just because I did not need to or wanted to at that point in time. That turned it into a [decision](../../docs/decisions/index.md) with _draft_ status, which I found quite unsatisfactory: it's reads like a decision carried out and only the status in the rendered provenance card identified it as something that _did not induce an action yet_. I did not want to introduce a new `actions` category, because the result of a decision either lives in the knowledgebase as a [guide](../../docs/guides/index.md) or a [blueprint](../../docs/blueprints/index.md), or is just a change in the world (as in: editing some config files on my machine, or installing something).

So, long story short: I wanted a place on this site to talk _about_ the things in the knowledge base. I already have an [about](../../about/welcome.md) section sitting outside the knowledgebundle (hosted in `docs/`), which is more about guidance on how to interact with the site and knowledge bundle. A `blog/` dir beside `about/` and `docs/` felt like a natural addition.

Technically, I'm using Material's blog plugin, together with a bit of magic in a hook to ensure the blog posts, the about, and the knowledge bundle all end up on the final site without interfering with each other (say, because a blog entry is not a concept, and must not be part of the okf checks, and the like). See also [the tech stack page](../../about/tech_stack.md) and [the publishing stack](../../docs/blueprints/mkdocs_material_pkb_publishing_stack.md).
