---
type: Tool
title: Voxtype (Peter Jackson)
description: Push-to-talk voice dictation for Linux and macOS, a single Rust binary running local
  speech-to-text engines and typing the result into whatever has focus.
tags:
- tools
- voxtype
- dictation
- speech-to-text
- linux
- wayland
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
sources:
- id: voxtype-site
  resource: https://voxtype.io/
  title: 'Voxtype: Push-to-Talk Voice-to-Text for Linux and macOS'
  last_modified: '2026-09-28'
---
Voxtype[^voxtype-site] records whilst a key is held, transcribes locally, and types the text into
the focused window. It is written in Rust and ships as one binary with a systemd user service,
rather than as a Python tree with an activation script.

| | |
| --- | --- |
| Author | Peter Jackson, at Faster Agile |
| Licence | MIT |
| Language | Rust |
| Distribution | AUR, `.deb`, `.rpm`, AppImage, a Nix flake, Homebrew on macOS |
| Source | [github.com/peteonrails/voxtype](https://github.com/peteonrails/voxtype) |
| Version read | 1.1.0 |

## To fill in

A stub, written so the page exists and can be linked at. What belongs here once it has been
used: which engine of the eight is worth configuring and at what accuracy, how the hotkey is
bound under a compositor as against the evdev fallback, and how the typing path behaves when
`wtype` is unavailable. The comparison against
[Vocalinux (VocaHQ)](vocalinux_vocahq.md), which solves the same problem in Python under
AGPL-3.0, is the other half of it.
