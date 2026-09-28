---
type: Tool
title: WirePlumber
description: The session manager that decides what exists in a PipeWire graph and how it is linked,
  configured by composable profiles and implemented as Lua hooks over a C core.
tags:
- tools
- wireplumber
- pipewire
- audio
- linux
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T08:58:20Z'
sources:
- id: wireplumber-repo
  resource: https://gitlab.freedesktop.org/pipewire/wireplumber
  title: 'PipeWire: WirePlumber'
  last_modified: '2026-09-28'
---
WirePlumber[^wireplumber-repo] is the session manager for PipeWire. PipeWire provides the media
graph and the plugins that talk to hardware; WirePlumber decides which devices become nodes in
that graph, what those nodes are called, which profile a device sits in, and what gets linked to
what. On a desktop it is the component that turns a working sound server into working sound.

| | |
| --- | --- |
| Author | Collabora, under the PipeWire project |
| Licence | MIT |
| Language | C, with policy written in Lua |
| Distribution | Distribution packages, alongside PipeWire itself |
| Source | [gitlab.freedesktop.org/pipewire/wireplumber](https://gitlab.freedesktop.org/pipewire/wireplumber) |
| Version read | 0.5.17 |

## What it is

The division of labour with PipeWire is the thing worth holding onto, because it decides where
to look when something is missing. The device monitors are SPA plugins and belong to PipeWire.
WirePlumber loads them and lets them work. So a missing Bluetooth device is rarely a missing
plugin and is usually WirePlumber having declined to load one, which is a different file to read
and a different thing to fix.

Policy is Lua. Each decision is a hook registered against an event, declaring where it runs
relative to its siblings, and returning early if an earlier hook already settled the question.
Profile selection is three such hooks in a row, which is the whole mechanism behind
[a headset reconnecting in the wrong profile](../findings/20260928_a_bluetooth_headset_reconnects_in_a2dp_instead_of_the_saved_profile.md).

## How it is configured

`wireplumber.conf` declares **components**, each naming what it `provides` and what it
`requires` or `wants`, and **profiles**, which switch named features to `required`, `optional` or
`disabled`. The default profile is `main`. A feature that is merely wanted, and is unavailable,
leaves its component running with less behaviour rather than failing to load, which is why a
disabled feature is usually silent.

Configuration is not edited in place. Fragments in `wireplumber.conf.d/`, under `/etc` or under
`~/.config/wireplumber/`, merge over the shipped file, so an override is a small file of its own
and survives a package upgrade. Both fixes recorded here are fragments of that kind.

Almost nothing is logged at the default level. `WIREPLUMBER_DEBUG=3` on the service, through a
systemd drop-in, is what makes the load decisions visible, and it is the difference between
guessing at why a monitor is absent and reading the line where it was skipped.

## Why it matters here

It is the component that failed in both Bluetooth findings on
[the Precision 5470](../hardware/dell_precision_5470.md), and in neither case was the visible
error its own. A gate it consults reported the desktop inactive, so
[no Bluetooth endpoint was ever registered](../findings/20260928_bluetooth_a2dp_fails_with_protocol_not_available_after_resume.md)
and BlueZ reported the protocol as unavailable. That pattern, where the component at fault is
upstream of the one producing the message, is the reason it is worth knowing which half of the
PipeWire stack owns which decision.
