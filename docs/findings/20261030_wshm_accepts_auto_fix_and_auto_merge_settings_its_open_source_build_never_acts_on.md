---
type: Finding
title: wshm accepts auto_fix and auto-merge settings that its open-source build never acts on
description: The features the landing page leads with are either sold separately or not written yet,
  and the free binary takes their configuration keys without complaint and does nothing.
tags:
- finding
- wshm
- ai-agents
- self-hosted
- ci-cd
status: stable
stale_after: '2027-04-30'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-30T00:00:00Z'
---
[wshm](../tools/wshm.md) is advertised as issue triage, PR review, auto-fix, merge queue and
conflict resolution in one self-hosted Apache-2.0 binary. Evaluating it as a repository agent,
the first four words of that list hold and the rest do not.

`auto_fix = true` in `.wshm/config.toml` is valid configuration. The free binary parses it,
reaches the call site, finds no implementation registered, and carries on. Nothing in the
config layer rejects the key, because the key is real; only the behaviour behind it is absent.

The mechanism is a hook registry whose own opening comment states it plainly:

```rust
//! Pro hooks registry — injected at startup by wshm-pro.
//! In the OSS build, all hooks are None (no-op).
```

Line-by-line PR review, auto-fix, AI conflict resolution and changelog generation are all
registered through that registry, so all four are inert in the repository you can clone.

## The merge queue is a third case

Worth separating, because it is not an edition split. The free feature list advertises the
merge queue as "scoring, auto-merge above threshold", and no paid edition is implied. The
scoring is real. The merge is this:

```rust
// TODO: actual merge via GitHub API
println!("Warning: Merge not yet implemented. Coming in M4.");
```

So the queue ranks pull requests and then declines to act, with `--apply` or without it. A
feature can be missing here for either of two reasons, and the README's edition table only
documents one of them.

## How to check this quickly on an open-core tool

**Read the gate, not the feature list.** A project that sells a layer on top of its own
open-source core has to have one file where the split is decided, and that file is both short
and honest in a way the README is not obliged to be. Here it is
[`src/pro_hooks.rs`](https://github.com/wshm-dev/wshm/blob/e5e7296215ee4320529c9b791f865086df77a8b0/src/pro_hooks.rs),
and it answered the question faster than the documentation did.

The second check is to grep the pipeline for the verb. `merge_queue.rs` contains no call that
merges anything, which takes a moment to establish and does not depend on trusting any prose.

A configuration key is not evidence that a feature exists. It is evidence that a struct field
exists, and in an open-core project those two things are deliberately decoupled so that one
config file serves both editions.

## The verdict for these repositories

Not adopted. The free edition classifies issues and labels them, and
[federated-agent-kits](../tools/federated_agent_kits_schindler.md) has no inbound issues to
classify: every issue on it was filed by its own author. What it does have is a queue of
dependency pull requests nobody merges, which is the one thing the free queue explicitly
cannot do.

That leaves a daemon holding a write-capable forge token in exchange for labelling your own
issues, against a project six months old with one substantive contributor and no changelog.
The work that wanted an agent here is PR-shaped and already runs in CI, which is
[opencode](../tools/opencode.md)'s GitHub action rather than a service to host.

Reconsider if the repositories start taking outside traffic, since triage against a backlog
somebody else wrote is the case the free edition is actually built for.
