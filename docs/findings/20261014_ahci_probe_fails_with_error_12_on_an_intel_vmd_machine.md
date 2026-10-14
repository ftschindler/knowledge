---
type: Finding
title: ahci probe fails with error -12 on an Intel VMD machine
description: A kernel line that reads as a storage controller running out of memory, logged at every
  boot since the machine was installed, because ahci matches Intel RAID-class devices generically and
  Volume Management Device is one.
tags:
- finding
- linux
- kernel
- storage
- nvme
- hardware
status: stable
stale_after: '2027-04-14'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T09:30:00+02:00'
---
A machine with Intel Volume Management Device enabled logs an `ahci` probe failure on every
boot. Nothing is wrong with the drive, and the message is not new, which is the part worth
knowing before it is read as evidence of anything.

Observed on kernel 6.18.49, with an SK hynix PC801 NVMe behind VMD on a
[Dell Precision 5470](../hardware/dell_precision_5470.md).

## Symptom

```text
kernel: ahci 0000:00:0e.0: probe with driver ahci failed with error -12
```

`-12` is `-ENOMEM`. A storage controller that cannot be brought up for want of memory is an
alarming thing to find in a journal, and it sits near the top of every boot where it is easy to
reach for.

## What the device is

`00:0e.0` is not a SATA controller. It is the Volume Management Device, which presents itself in
the RAID class and hides the NVMe drive behind a PCI domain of its own:

```text
0000:00:0e.0 RAID bus controller [0104]: Intel Corporation Volume Management Device NVMe RAID Controller [8086:467f]
 Kernel driver in use: vmd
10000:e1:00.0 Non-Volatile memory controller [0108]: SK hynix Platinum P41/PC801 NVMe Solid State Drive
 Kernel driver in use: nvme
```

The domain number is the tell. `10000` is synthetic, created by `vmd` for the devices it carries,
and a drive addressed there is a drive reached through VMD rather than off the root complex.

`ahci` carries a catch-all match for Intel storage devices in the RAID class, so it attempts this
one and gets nowhere. Its own device table never names the part:

```bash
$ modinfo ahci | grep -c 467f
0
```

The probe failing is the two drivers sorting out which owns the device, and `vmd` is the one that
ends up bound.

## Confirming it is old news

Count the line across every boot the journal still holds, rather than reading it in the one boot
being investigated:

```bash
for b in $(journalctl --list-boots -q | awk '{print $1}'); do
  printf '%s: %s\n' "$b" "$(journalctl -b "$b" -k 2>/dev/null | grep -c 'ahci.*error -12')"
done
```

A constant `1` is the answer that settles it. On this machine it was 1 in all 72 recorded boots,
including every boot that worked.

## The general case

A kernel error found whilst investigating a fresh failure is worth counting before it is
believed. The journal holds every boot, so the question "was this here last week, when everything
worked?" is one command, and it is the cheapest way to tell a cause from a constant. It is also
the step most easily skipped, because a message that looks like the answer discourages looking
for another one.
