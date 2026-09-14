---
type: Practice
title: Split orthogonal classification axes across folders and tags
description: When knowledge classifies along two independent axes, put one on folders and the other on
  tags rather than forcing both into one tree.
tags:
- principle
- knowledge-management
- taxonomy
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
!!! note "This is a [knowledge-management practice](index.md)"
    How knowledge gets organised, independently of any tool that stores it.

When you classify knowledge along **two independent axes at once**, don't try to
express both in one folder tree. Put one axis on folders, the other on tags.

## The problem

A single hierarchical folder tree encodes exactly *one* axis cleanly. The moment
you have two orthogonal axes - for example:

- **Nature**: is this a *principle*, a *blueprint*, a *research finding*, a *tool
  fix*?
- **Domain**: is this about *software*, *philosophy*, *your house*, *health*?

...you face a bad trilemma if you insist on folders alone:

1. **Encode both in the folder name** (`tech-principles`, `life-principles`,
   `house-blueprints`, ...) - the names multiply combinatorially: every new domain
   *times* every new nature. This is topic explosion.
2. **Collapse to one axis** and lose the other - now a philosophy principle and a
   git principle sit in the same `principles/` folder with no way to separate
   them.
3. **Pick one axis arbitrarily** and strand anything that cuts across the other.

## The rule

**One axis → folders. The other axis → tags.**

Folders give you the primary, browsable structure; tags give you the orthogonal
slice. Retrieval combines them: *"software principles"* = the `principles/`
folder filtered by the `software` tag.

Choose which axis gets the scarce folder slot by asking **which axis is fixed and
which is open-ended**. Put the *bounded, stable* axis on folders and let the
*open-ended, growing* axis ride on tags - because adding a folder is a schema
change, but adding a tag value is free. If natures are few and stable while
domains will grow unpredictably, folders = nature, tags = domain.

## How it drifts back

Naming the rule does not settle it, because the pressure to file by domain
arrives one page at a time and always looks reasonable locally. This bundle put
its tool findings in `tools/` and its one Linux finding in `linux/`, each time on
the sensible-sounding grounds that the page was *about* that subject. The result
was a nature with no folder of its own, two natures sharing `tools/`, and a
`linux/` directory holding exactly one file - a folder tree quietly re-growing
along the domain axis it was supposed to keep off. It was fixed by giving
`Finding` the folder its siblings already had and demoting the subject to a tag.

Two tells, both cheap to check. A **directory holding one file** is usually a
domain that got a folder. And a **nature with no folder**, whose pages are
scattered across several, can only be found by reading an index that reassembles
them - which is the retrieval the folder axis was meant to provide.

One exception stands here deliberately: `knowledge_management/` is a domain
folder, holding principles and practices about this bundle itself. Consistency
says it should dissolve into the nature folders behind a tag. It has not, because
it is the one subject whose pages are read as a group rather than found
individually, and naming a live exception is more honest than pretending the rule
is applied everywhere.

## Why it generalises

This is tool-agnostic: it holds for a filesystem, a wiki, Notion, a photo
library - anywhere you have hierarchy + labels. The insight is recognising that
*two axes exist* in the first place; once named, the folder/tag split falls out
mechanically.

This only works because a third axis, *who may read this*, is kept out of the tree
entirely: see
[Separate audiences with separate bundles, not with folders or tags](separate_audiences_with_separate_bundles.md).
Were audience a folder or a tag, it would compete for the same scarce slots and the
trilemma above would have three horns instead of two.

Related: [Categorize by what content is, not why you made it](categorize_by_what_content_is_not_why_you_made_it.md) tells you *what
the nature axis even is* for a given item; this page tells you what to do once
you have two axes to reconcile.
