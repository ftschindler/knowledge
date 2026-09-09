---
type: Finding
title: KDE Plasma - Phantom Pointer After Hibernate Resume (Unresolved)
description: An unresolved investigation into a phantom pointer after hibernate resume on KDE Plasma,
  recording what the fault is not and how it was measured.
tags:
- kde
- plasma
- x11
- libinput
- evdev
- hibernate
- input-devices
- troubleshooting
- unresolved
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Status: UNRESOLVED.** This records an investigation that eliminated the
entire input stack below the X server without finding the culprit. Its value is
the negative space - what the fault is *not* - plus the measurement techniques,
so the next attempt starts from evidence rather than from scratch.

- **Hardware**: Dell laptop, I2C-HID touchpad `VEN_0488:00 0488:1031`, Wacom HID
  49BB digitiser (pen + 10-touch touchscreen), internal i8042 controller
- **Software**: Manjaro, KDE Plasma, X11 session (`kwin_x11`), LUKS + LVM
- **Date**: 2026-08-27

## Symptom

After resuming from hibernate and unlocking, the session behaved normally for
roughly two minutes, then the pointer began **moving constantly and dragging
items** without user input. It **reproduced after a subsequent lock/unlock
cycle**, so it is deterministic rather than a one-off glitch.

Note this is a *different* symptom from the previously diagnosed sticky/snapping
pointer on the same machine - see
Sticky Mouse on KDE - I2C-HID Touchpad Exposing a Duplicate Pointer. That
fault was *sticking*; this one is *autonomous motion plus a latched drag*. The
earlier analysis explicitly anticipated a distinct "resume-time failure mode",
and this appears to be it.

## Timeline reconstruction (the useful trick)

`Xorg.0.log` timestamps are `CLOCK_MONOTONIC`, which **does not advance across
hibernation**. That lets you pin log entries to wall-clock events without any
timestamps in the log itself - the hibernate gap shows up as a suspiciously
tiny monotonic delta spanning many wall-clock hours:

| Xorg clock | Wall clock | Event |
| --- | --- | --- |
| `33604` | 22:20 (prev day) | Hibernate entry - logind revokes fds, all input devices removed |
| `33623` | 06:55 | Resume - all devices re-added (`event8`–`event12`) |
| `33623`→`33781` | **158 s** | Login, normal use, then pointer goes haywire |
| `33781` | 06:57:43 | All devices removed, `AIGLX: Suspending AIGLX clients for VT switch` |

A 19-second monotonic gap spanning 8.5 hours of wall clock is the hibernate
boundary. A later re-add/remove pair only **6.3 s** apart captured the
reproduction attempt - long enough to unlock and bail out.

## What was proven clean

Every layer below the X server was measured and is silent:

| Layer | Method | Result |
| --- | --- | --- |
| Hardware IRQs | `/proc/interrupts` sampled twice, 5 s apart | **zero delta** on `i8042` (1, 12), `i2c_designware.0/.1` (27, 40), touchpad GPIO (183) |
| evdev raw | `cat /dev/input/event{3,8,9,10,11,12}` for 10 s, untouched | **0 bytes** on every device |
| libinput | `libinput debug-events`, 10 s idle | `DEVICE_ADDED` lines only, then total silence |
| Existing quirk | `libinput quirks list /dev/input/event8` | `AttrEventCode=-REL_X;-REL_Y` - **still applied** |

Kernel logs after resume contain **no** `i2c_hid`, `hid-multitouch`,
`hid-generic`, `psmouse` or Wacom lines at all: the drivers resumed silently
with no reset and no error.

## Hypotheses killed

- **Wacom touchscreen latching a phantom touch** - the leading theory, given
  that a stuck touch point reads as button-down plus moving coordinates.
  **Disproven**: `event11` emitted zero bytes.
- **KDE Connect remote input** - `kdeconnectd` was running, and its virtual-input
  plugin injects via XTEST, which fits the symptom exactly. **Disproven**:
  `~/.config/kdeconnect/` contains **no paired device directories**, so it has
  nothing to inject from.
- **Other XTEST injectors** - synergy, input-leap, barrier, x11vnc, krfb,
  ydotool, xdotool, input-remapper, touchegg, autokey: none present.
- **The July duplicate-pointer fault regressing** - quirk verified still active.
- **`plasmashell`** - restarted during the session with no effect, as expected:
  it is the panel/desktop shell and sits nowhere on the pointer path
  (`kernel HID → libinput → xf86-input-libinput → X → kwin_x11 → apps`).

## A correction worth recording

`xinput list` run from another TTY showed **every physical device as
`[floating slave]`**, with only XTEST attached to the master pointer. This looks
alarming and was initially mistaken for the root cause.

It is not. When a session is VT-inactive, **logind revokes the device fds** and
the X server detaches the devices; they reattach on switching back. This is
the *normal* appearance of an inactive session, not a fault. Do not chase it.

## Why it stayed unresolved

The fault exists **only while the session is VT-active**, but every diagnostic
above was necessarily run from another TTY, where the session is inactive. So
the clean results prove only that *no device is stuck emitting at rest* - they
cannot see the fault window.

A during-the-fault capture was attempted (raw evdev plus `xinput test-xi2
--root`, run from a second TTY against the live display) and **yielded
nothing**. Investigation was stopped there.

## Measurement techniques worth reusing

- **Root reads of `/dev/input/*` are unaffected by logind's revocation.**
  `EVIOCREVOKE` applies to the fd the X server holds; a fresh `open()` as root
  still sees everything. So the kernel layer can be observed from another TTY
  *while* a session misbehaves.
- **`xinput test-xi2 --root` reports `sourceid`**, which cleanly separates
  synthetic from physical input: `sourceid: 4` is XTEST (some client is driving
  the cursor), anything else is a real device.
- **Reach a graphical session from a TTY** by lifting its credentials out of a
  running client's environment:

  ```bash
  XPID=$(pgrep -u "$USER" -x plasmashell | head -1)
  export DISPLAY=$(tr '\0' '\n' < /proc/$XPID/environ | sed -n 's/^DISPLAY=//p')
  export XAUTHORITY=$(tr '\0' '\n' < /proc/$XPID/environ | sed -n 's/^XAUTHORITY=//p')
  xinput list
  ```

- **Recovery**: a VT switch away and back forces X to remove and re-add every
  input device, which clears any latched button state. Often enough to make a
  wedged session usable again.

## Untested leads for next time

- **A stuck modifier key**, not a stuck mouse button. A latched `Ctrl`, `Alt` or
  `Super` turns ordinary pointer motion into a drag or a window-move, which fits
  "dragging things" without requiring any phantom button. Check with
  `xinput query-state` on the master keyboard *while the fault is live*. This
  was never tested and is the cheapest remaining hypothesis.
- Log XI2 events to a file with timestamps across the whole unlock window,
  rather than sampling a fixed interval that may miss onset.
- Start `Xorg` with `-logverbose 6` to capture device arbitration detail.
- Disable the spurious `event8` and the phantom `PS/2 Generic Mouse` (`event12`)
  outright and see whether the fault survives.
- Try a Wayland session - if the fault vanishes, it localises to X11 device
  handling rather than the kernel or libinput.

## Related

- Sticky Mouse on KDE - I2C-HID Touchpad Exposing a Duplicate Pointer
- [fs.protected_regular Blocks Root Writes in Sticky tmp](fsprotected_regular_blocks_root_writes_in_sticky_tmp.md) - hit while writing
  the diagnostic scripts for this investigation
