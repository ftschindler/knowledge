---
type: Tool
title: Vocalinux (VocaHQ)
description: Voice dictation for X11 and Wayland, a Python desktop app running whisper.cpp and four
  other local engines behind a tray icon and a settings dialog.
tags:
- tools
- vocalinux
- dictation
- speech-to-text
- linux
- wayland
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
sources:
- id: vocalinux-repo
  resource: https://github.com/VocaHQ/vocalinux
  title: 'VocaHQ/vocalinux: voice dictation for Linux'
  last_modified: '2026-09-28'
---
Vocalinux[^vocalinux-repo] turns speech into typed text in whatever application has focus, with
transcription on the machine once a model has been downloaded. It is the Linux entry in VocaHQ's
one-app-per-platform set, and it is driven from a tray icon and a settings dialog rather than
from a configuration file.

| | |
| --- | --- |
| Author | VocaHQ |
| Licence | AGPL-3.0 |
| Language | Python |
| Distribution | An install script, PyPI, AUR, AppImage, Snap on edge, Flatpak bundles off the releases page |
| Source | [github.com/VocaHQ/vocalinux](https://github.com/VocaHQ/vocalinux) |
| Version read | 0.17.0 |

## To fill in

A stub, written so the page exists and can be linked at. What belongs here once it has been
used: which of the five engines is worth running, how the text reaches the focused window on
Wayland through the `ydotool` and clipboard fallbacks, and what the AGPL and the optional remote
API mean for using it at work. It is the direct alternative to
[Voxtype (Peter Jackson)](voxtype_jackson.md), and the pair is worth one comparison rather than
two separate verdicts.
