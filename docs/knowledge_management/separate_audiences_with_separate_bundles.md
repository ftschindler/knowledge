---
type: Practice
title: Separate audiences with separate bundles, not with folders or tags
description: Who may see a page is a property of the repository it lives in, which is what frees the
  folder axis to carry something else.
tags:
- knowledge-management
- taxonomy
- federation
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-14T00:00:00Z'
---
!!! note "This is a [knowledge-management practice](index.md)"
    How knowledge gets organised, independently of any tool that stores it.

A knowledge base that outlives its first subject eventually holds things not everyone should
read: work under a client's name, notes about people, a half-formed opinion. The reflex is to
put the boundary where the other structure already is, in a folder called `private` or a tag
called `internal`.

Neither is a boundary. A folder is a path and a tag is a label; both are conventions that hold
only as long as everyone publishing remembers them, and the thing you are guarding against is
exactly a moment of not remembering. **The boundary that holds is the repository**: a separate
remote, separate permissions, a separate publish gate, and a `git push` that cannot reach the
wrong place because it is not configured to.

So visibility is decided one level up from the content, at the bundle. You publish a bundle.
You never publish a folder.

## What that buys the structure inside

This is the part worth noticing, because it is not obvious until the decision is made.

Two jobs pull in opposite directions when both must be expressed in one tree. **Composition**
wants organisation by nature, so you can take every principle regardless of subject and
assemble a new repository from them. **Sharing** wants organisation by domain, so you can hand
someone the home-and-family slice without the software one. A single hierarchy cannot serve
both, and trying produces the folder-name explosion that
[Split orthogonal classification axes across folders and tags](split_orthogonal_classification_axes_across_folders_and_tags.md)
describes.

Deciding visibility at the bundle dissolves the conflict rather than resolving it. Each bundle
already has one audience, so there is no sharing pressure *inside* it, and the folder axis is
free to carry nature while tags carry domain. Adding an audience becomes adding a bundle, not
reorganising an existing one.

## What it costs

- **A concept cannot be half-visible.** A page that is mostly publishable with two sentences
  that are not has to be split, or written to the stricter audience. This is a real cost and
  the correct one: the alternative is a page whose visibility depends on how it is read.
- **Cross-bundle links become their own problem**, since a link from a public page into a
  private one leaks the private page's existence and often its title. That needs a rule of its
  own; in this knowledge base it is the `referenceable_by` allow-list in
  [Federated OKF knowledge bases](../research/federated_okf_knowledge_bases_a_workspace_manifest_architecture.md).
- **Moving a page to a wider audience is irreversible**, because the target's history keeps it.
  That makes promotion a deliberate, gated act rather than a drag-and-drop, which is why
  [Federating my knowledge base as privacy-tiered OKF bundles](../decisions/federating_my_knowledge_base_as_privacy_tiered_okf_bundles.md)
  treats it as a first-class operation.

## The tell that a tag is being asked to do this

You are about to write `tags: [private]`, or to name a folder after who may read it. Both are
the same mistake wearing different clothes: an audience expressed as content metadata, inside
an artefact that is published or not published as a whole.
