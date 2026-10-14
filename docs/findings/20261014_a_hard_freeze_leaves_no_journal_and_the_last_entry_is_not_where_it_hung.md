---
type: Finding
title: A hard freeze leaves no journal, and the last entry is not where it hung
description: A frozen boot's journal stops on an arbitrary driver line, because journald syncs every
  five minutes and a boot that froze after twelve seconds never reached a sync.
tags:
- finding
- linux
- systemd
- journald
- debugging
status: stable
stale_after: '2027-04-14'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:35:00+02:00'
---
A machine that froze and had to be held down leaves a journal for that boot which simply stops.
Whatever driver logged the last line looks like the thing that hung. It usually is not: the cut
is where the journal last reached disk, and that has nothing to do with where the kernel
stopped.

Observed on systemd 261 with default journald settings.

## Symptom

A boot that froze, ending mid-enumeration on a line that reads like a culprit:

```text
09:10:13 kernel: intel_ipu6_psys.psys intel_ipu6.psys.40: psys probe minor: 0
-- no further entries --
```

The camera stack is a plausible thing to hang on, and that is the trap. The same boot had no
error, no warning and no trace before it, so the last line is the only thing on offer.

## Why the journal stops there

journald does not write each entry to disk as it arrives. `SyncIntervalSec` defaults to five
minutes, and the manual page is explicit that the only thing bypassing it is priority:

> Note that syncing is unconditionally done immediately after a log message of priority CRIT,
> ALERT or EMERG has been logged. This setting hence applies only to messages of the levels
> ERR, WARNING, NOTICE, INFO, DEBUG.

A boot that froze twelve seconds in never came close to a scheduled sync. What survived is
whatever the kernel's own writeback happened to flush before power was cut, so the final entry
marks an arbitrary moment and not an interesting one.

## Telling it from a real hang

Compare the dead boot against a healthy one at the same point. If the next boot carries straight
on past that line, it is a flush boundary:

```bash
journalctl -b -1 -k | tail -5
journalctl -b  0 -k | grep -A10 'psys probe minor'
```

Here the healthy boot continued into `sof-audio`, `iwlwifi` and Bluetooth setup within the same
second, which rules the camera out. The entry counts say the same thing more bluntly: 1351 lines
against 3396 for a boot that reached a desktop.

**The absence of a high-priority message is itself evidence.** A panic, an oops or a hard lockup
logs at CRIT or above, which journald syncs immediately, so it survives a power cut that loses
everything around it. A frozen boot with nothing at priority 2 or below did not get as far as
logging a kernel failure:

```bash
journalctl -b -1 -p 2
```

`-- No entries --` means the freeze was never diagnosed by the kernel, not that the evidence was
lost.

## Keeping the next one

Two changes, both worth reverting once the problem is found. Shorten the sync interval so a
short boot still lands on disk:

```text
# /etc/systemd/journald.conf.d/debug.conf
[Journal]
SyncIntervalSec=5s
```

Then enable magic SysRq, so a frozen machine can be made to log something rather than be held
down:

```bash
echo 'kernel.sysrq = 1' | sudo tee /etc/sysctl.d/99-sysrq.conf
```

`Alt+SysRq+w` dumps blocked tasks and `Alt+SysRq+l` a backtrace from every CPU, both at a
priority that syncs. A machine too far gone for SysRq is itself a finding, since it separates a
userspace hang from one that has taken the kernel with it.

The cost of the first is an fsync every five seconds for as long as it is left in place. The cost
of the second is that the key combination also reboots the machine, which is the reason it ships
disabled.
