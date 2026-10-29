---
type: Finding
title: A phantom touch pins the pointer to one point in the system tray
description: A touchscreen contact that never lifts holds the pointer at a fixed coordinate, and
  because the device reports absolute positions, every attempt to move the mouse away is undone
  by the next report.
tags:
- finding
- linux
- kde
- plasma
- x11
- input
- libinput
- touchscreen
status: stable
stale_after: '2027-10-29'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-29T10:58:00Z'
---
The pointer sits in one corner of the screen, jitters by a few pixels, and returns there within
a moment of being moved anywhere else. Nothing is wrong with the mouse. The laptop's touchscreen
is reporting a contact that never lifted, and an absolute device does not nudge the pointer, it
states where the pointer is.

Observed on a [Dell Precision 5470](../hardware/dell_precision_5470.md) under Plasma 6.7.4 on
X11, with libinput 1.31.3 and xf86-input-libinput 1.5.0.

## Symptom

The pointer cannot be kept away from a single point, which on a 2560x1600 panel was the task
area of the system tray at the top right. Moving the mouse works for as long as the hand keeps
moving, and the pointer snaps back as soon as it stops.

Sampling the position shows the destination is stable and the jitter is small:

```bash
$ for i in 1 2 3; do xdotool getmouselocation; sleep 0.7; done
x:2054 y:0 screen:0 window:27263026
x:2056 y:0 screen:0 window:27263026
x:2048 y:0 screen:0 window:27263026
```

A few pixels of movement with no input is the tell that something is still reporting, rather
than the pointer having been parked somewhere and left.

## Cause

The touchscreen is held in proximity with a contact that was never released. `xinput
query-state` on the touch device shows it, and keeps showing it:

```bash
$ xinput query-state 16 | grep -E 'Proximity|valuator\[0\]|valuator\[1\]'
ValuatorClass Mode=Absolute Proximity=In   valuator[0]=52612  valuator[1]=8
ValuatorClass Mode=Absolute Proximity=In   valuator[0]=52639  valuator[1]=8
ValuatorClass Mode=Absolute Proximity=In   valuator[0]=52504  valuator[1]=8
```

`Proximity=In` that never becomes `Out` is the whole finding. X is being told a finger is on the
glass, continuously, and the small variation in the first valuator is sensor noise under that
stuck contact rather than anything moving.

**Mode=Absolute is why it fights back rather than drifting.** Both touch axes run 0 to 65535
across the panel, so each report asserts a position outright:

```bash
$ xinput list 16
  Label: Abs MT Position X   Range: 0.000000 - 65535.000000   Current value: 52547.500207
  Label: Abs MT Position Y   Range: 0.000000 - 65535.000000   Current value: 8.690492
```

Scaling those against the panel gives `52547/65535 x 2560 = 2052` and `9/65535 x 1600 = 0`,
which is the position the pointer was measured at. A relative device with a stuck button would
leave the pointer wherever it was last pushed; an absolute one restores its own coordinate every
report, so moving the mouse away is a change the next report simply overwrites.

**The destination means nothing.** Landing on the system tray invites a search through panel
widgets and tray applets, and the coordinate is just wherever the contact happened to be. The
same fault anywhere else on the glass reads as a different bug.

## Finding the device

Only one pointer device needs to be wrong, so check each in turn and look for the one in
absolute mode with buttons up:

```bash
xinput list
xinput query-state <id>
```

A mouse and a touchpad in this state report all buttons `up` and no valuator activity, which
clears them in one line each. On this machine the digitiser presents as two devices, a pen and a
finger, and only the finger was at fault; the pen is a separate device and a separate id.

## Fix

Disable the device:

```bash
xinput disable 16
```

The pointer is usable immediately, and the device drops to `floating slave` with `Device
Enabled` at 0. Confirm it with a move that is supposed to stick:

```bash
$ xdotool mousemove 800 600; sleep 1.2; xdotool getmouselocation
x:800 y:600 screen:0 window:92274728
```

Pen, touchpad and mouse are unaffected. Touch input is gone until the device is enabled again,
which is the entire cost.

**This does not survive the session, and that is the useful part.** `xinput` changes live in the
running X server, so a logout or a reboot brings the touchscreen back enabled. A latched contact
does not generally survive a reboot either, so the default behaviour is the wanted one: the fix
lasts exactly as long as the fault usually does, and nothing has to be remembered and undone
later. Making it persistent, through a libinput quirk or a udev rule, would turn a transient
fault into a permanently disabled touchscreen.

`xinput enable 16` is the thing to try first when the call or the task is over. If the ghost
returns at once the contact is still latched in the hardware, and rebinding the hid driver for
the device clears it without a reboot.

## What it is not

An undock is a plausible trigger, since lifting the machine off a dock flexes the chassis and
disturbs the i2c-hid digitiser, and the journal dates the dock teardown a few minutes before the
symptom. It is not the mechanism, though, and it is a different fault from
[Chromium maximising to the wrong size after an undock](20260930_chromium_maximises_to_the_wrong_size_after_an_undock.md),
which is about a process carrying a model of a display that no longer exists. Nothing here
involves a display, a window or a toolkit, and no application restart touches it.

Recently installed software is the other place the search goes, because a cursor behaving oddly
feels like something new taking control of it. An application cannot hold the pointer at a
coordinate this way, and the evidence against it is in the device state rather than in any
process: a stuck `Proximity=In` is a report arriving at the X server, from below everything a
desktop application can reach.
