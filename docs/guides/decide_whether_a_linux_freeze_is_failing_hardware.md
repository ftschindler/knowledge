---
type: Guide
title: Decide whether a Linux freeze is failing hardware
description: Six checks that separate a one-off freeze from a machine on its way out, each asking a
  component to report its own error counters rather than inferring from symptoms.
tags:
- guide
- linux
- hardware
- debugging
- storage
- systemd
status: stable
stale_after: '2027-04-14'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:40:00+02:00'
---
A machine that froze two or three times in a morning raises one question before any other:
is this hardware on its way out? The checks below answer it in a few minutes, and they are
worth running in order, because the cheapest one is also the most decisive.

Every component here keeps its own error counters. The point of the sequence is to read
those counters rather than reason from symptoms, which is what makes the answer defensible
either way.

Commands are as of smartmontools 7.5 and systemd 261.

## 1. Count the short boots

```bash
journalctl --list-boots -q -o json | python3 -c '
import sys, json, datetime
for b in json.load(sys.stdin):
    d = (b["last_entry"] - b["first_entry"]) / 1e6
    t = datetime.datetime.fromtimestamp(b["first_entry"] / 1e6)
    mark = "  <-- short" if d < 300 else ""
    print("%5d  %s  %8.1fs%s" % (b["index"], t.strftime("%Y-%m-%d %H:%M"), d, mark))
'
```

**This is the check that usually settles it.** Hardware degrades, so a failing machine leaves
a trail: boots that get shorter, or a scattering of short ones over weeks. One isolated
cluster of short boots in a journal going back months is an event, not a trend.

Run this first. If it shows a trend, the rest of the sequence tells you which component; if
it shows one cluster, the rest is confirmation and goes quickly.

## 2. Ask the drive

```bash
sudo smartctl -a /dev/nvme0n1
```

Four fields carry the answer, and the overall assessment is not among them:

| Field | A healthy drive |
| --- | --- |
| `Media and Data Integrity Errors` | `0` |
| `Error Information Log Entries` | `0` |
| `Available Spare` | at or near `100%`, and above the threshold below it |
| `Percentage Used` | well under `100` |

`SMART overall-health self-assessment test result: PASSED` is a summary that only fails once
a drive has crossed a threshold it sets itself, so it passes on drives with a real problem.
Read the counters.

`Unsafe Shutdowns` counts up every time the machine is held down, so it rises during an
investigation like this one and says nothing about the drive.

## 3. Ask the memory controller

```bash
journalctl -k | grep -iE 'edac|machine check|hardware error'
```

On Intel client parts the `igen6_edac` module reports memory errors, and the useful output is
the module announcing itself and nothing further. Any line counting corrected errors means
memory worth replacing, whether or not it has caused a freeze yet.

Memory with no error-correcting code reports nothing at all, in which case this check is
silent for a different reason and `memtest86+` is the only answer.

## 4. Ask the CPU

A machine check exception is the kernel being told by the processor that something failed in
hardware. The grep above catches them. They are rare, specific and unambiguous: a machine
logging MCEs has a hardware fault and the investigation is over.

## 5. Rule out heat

```bash
sudo smartctl -a /dev/nvme0n1 | grep -i 'Temperature Time'
sensors
```

`Warning Comp. Temperature Time` and `Critical Comp. Temperature Time` are lifetime counters
in minutes. Both at `0` means the drive has never once been hot, across its whole service
life, which is a stronger statement than any instantaneous reading.

`sensors` gives the present picture. Compare the package temperature against the `crit` value
beside it rather than against a number you remember.

## 6. Discount the constants

```bash
journalctl -b 0 -p err | sort -u -k5 | head -40
```

A fresh look at a boot log turns up alarming lines that have always been there. Count any
candidate across previous boots before treating it as a cause;
[the VMD one](../findings/20261014_ahci_probe_fails_with_error_12_on_an_intel_vmd_machine.md)
is the worked example, and it appeared in all 72 boots on the machine this guide came from.

## Reading the frozen boot itself

The boot that froze is the least informative thing available, and
[its last entry is not where it hung](../findings/20261014_a_hard_freeze_leaves_no_journal_and_the_last_entry_is_not_where_it_hung.md).
Check it for a message at priority CRIT or above, which would have been synced, and otherwise
spend the time on the six checks instead.

## What the answer looks like

All six quiet, against one isolated cluster of freezes, is a software or firmware fault and
not a dying machine. That conclusion is worth stating with the counters behind it, because
the honest version of it is narrow: the components that keep error counters are reporting
none, which is not the same as a guarantee.

What it does buy is the right next step. A machine with no hardware evidence against it gets
its firmware updated, its recent package upgrades examined and its instrumentation improved
for the next occurrence, rather than being replaced on a suspicion.
