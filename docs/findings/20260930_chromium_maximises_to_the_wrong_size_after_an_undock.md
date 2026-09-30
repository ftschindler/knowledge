---
type: Finding
title: Chromium maximises to the wrong size after an undock, and closing every window does not
  restart it
description: A browser window that loses its maximised state when the display it was laid out on
  disappears, and a PWA window that keeps the process alive so the restart which would clear it
  never happens.
tags:
- finding
- linux
- chromium
- kde
- plasma
- x11
- kwin
status: stable
stale_after: '2027-03-30'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-30T12:40:00Z'
---
Undocking a laptop leaves Chromium windows that maximise to the wrong rectangle, draw no window
decoration, and register clicks several centimetres from where the pointer is. Nothing in the
display configuration is wrong: the process is carrying a model of a screen that no longer
exists, and only a genuine restart clears it. The reason it looks unfixable is separate and is
the part worth keeping, because a PWA window holds the browser process open, so closing every
browser window restarts nothing.

Observed on Chromium 153.0.8010.47 under Plasma 6 on X11.

## Symptom

A Chromium window that was open across an undock behaves as though its geometry and its drawing
disagree. Maximising it fills part of the screen rather than the work area, the title bar
vanishes, and clicks land somewhere other than the element under the pointer. Other windows of
the same process may be perfectly fine, which makes it look like a per-window rendering glitch.

The configuration all reads correctly, which is what sends the first hour elsewhere. The output
is enabled at its native mode, the X screen dimensions match it, and the scale settings are
whatever they always were.

## Cause

Chromium builds its model of the attached displays at startup and does not rebuild it when an
output is destroyed. The damaging case is not a monitor being added or removed alongside others
but the display a window was laid out on ceasing to exist, which is what an undock does when the
external screen was the only enabled output and the internal panel was switched off.

The visible consequence is in the window's X properties. The affected window has lost its
maximised state entirely:

```bash
$ xprop -id <window> _NET_WM_STATE
_NET_WM_STATE(ATOM) =
```

So the window manager sizes and places it as an ordinary free-floating window whilst Chromium
continues to draw it as a maximised one. The pointer offset follows from that disagreement
rather than from any scaling problem: the two sides are working from different rectangles, and
the gap between them is what a click is wrong by.

**The drop shadow is not the tell, and reads like one.** A healthy unmaximised Chromium window
carries `_GTK_FRAME_EXTENTS` of `20, 20, 13, 40`, so its raw geometry is larger than the area a
person can see and taller than the screen it fits on. Subtracting the extents gives the visible
rectangle, and on a healthy window that rectangle is flush with the work area. A geometry that
looks impossible is therefore the normal case, and only the missing state atoms distinguish this
finding from a window that is merely not maximised.

## Why the restart appears not to work

Closing every Chromium window does not necessarily quit Chromium. A progressive web app opened
from Chromium runs in the same browser process, and its window keeps that process alive after
the last ordinary browser window is gone. Reopening the browser then attaches to the surviving
process and inherits the same stale display model, so the symptom returns immediately and the
restart appears to have been tried and failed.

This is the whole of the difficulty. A transient fault that a restart would clear is
indistinguishable from a persistent one when the restart silently does not happen, and every
subsequent conclusion is drawn from evidence that says "survives a restart" when nothing of the
sort has been established.

## Confirming it

Compare the age of the process owning the window against the moment the display changed. A
process older than the undock is carrying the stale model:

```bash
pid=$(xprop -id <window> _NET_WM_PID | grep -o '[0-9]*$')
ps -o pid,lstart= -p "$pid"
```

The display change itself is dated by the configuration the desktop wrote when it happened, the
newest file under `~/.local/share/kscreen/`, whose contents also record which outputs were
enabled and where they sat.

## Fix

Quit Chromium properly, confirm that nothing survives, then relaunch:

```bash
pkill -x chromium
pgrep -x chromium          # must print nothing before relaunching
```

The second command is the point of the sequence. A new process rebuilds its display model from
the current outputs, and windows maximise correctly again, including windows restored into the
same session.

## Recovering one window without restarting

Where a restart is not wanted, forcing the window through the maximised state repairs that
window, which is enough to make it usable whilst work is finished in it:

```bash
xdotool windowstate --add MAXIMIZED_HORZ <window>
xdotool windowstate --add MAXIMIZED_VERT <window>
```

**The two calls are required, and a combined one does not work.** Passing both flags to a single
invocation applies the horizontal maximise and silently drops the vertical, leaving a window the
full width of the screen and its former height. Splitting them across two calls applies both.

This repairs geometry only. The process keeps its stale display model, so every other window
already open stays affected and each new window is laid out from the same wrong screen. It is a
way to finish what is in front of you, not a fix.
