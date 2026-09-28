---
type: Device
title: Dell Precision 5470
description: A 14-inch Alder Lake mobile workstation whose audio path runs over SoundWire rather than
  classic HD Audio, and whose Bluetooth radio shares a die with its Wi-Fi.
tags:
- hardware
- dell
- linux
- audio
- bluetooth
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T08:58:20Z'
---
The Precision 5470 is Dell's 14-inch mobile workstation on Intel's Alder Lake-P platform. It is
the machine this bundle is written on, and the one every Linux finding here was found on unless
a page says otherwise.

| | |
| --- | --- |
| Vendor | Dell |
| Form factor | Notebook, 14-inch, DMI chassis type 10 |
| Processor | Intel Core i7-12800H, Alder Lake-P, 14-core hybrid |
| Memory | 32 GB, of which 30 GiB is visible to the kernel |
| Graphics | Intel Iris Xe, Alder Lake-P GT2, at `00:02.0` |
| Display | eDP-1, 2560x1600, 301 x 188 mm |
| Audio | Alder Lake PCH-P High Definition Audio controller at `00:1f.3`, driving a SoundWire codec through SOF |
| Wireless | Intel AX211 CNVi, `iwlwifi` for Wi-Fi and `btusb` for Bluetooth |
| Firmware | BIOS 1.31.1, board 08DX30 |
| Read through | Manjaro Linux, kernel 6.18.49 |

Everything above was read off the running machine rather than from a specification sheet, per
[the convention for this genre](index.md).

## The processor enumerates without SMT

The kernel presents 14 logical CPUs, one thread per core, and
`/sys/devices/system/cpu/smt/control` reads `notsupported`. That matches the physical core count
of the part, six performance cores and eight efficiency cores, but not the thread count its
performance cores would normally contribute. Anything that sizes a thread pool from
`nproc` on this machine gets 14, and anything expecting hyperthreading to be togglable at
runtime finds the control unavailable rather than merely off.

## Audio runs over SoundWire

The audio controller is enumerated as ordinary Intel HD Audio, but the codec behind it is
reached over SoundWire and driven by the Sound Open Firmware stack, so ALSA presents a single
card named `sof-soundwire` rather than the `HDA Intel PCH` a classic setup would show. The
consequence that surfaces most often is the node names, which carry `platform-sof_sdw` and a
`HiFi__` prefix:

```text
alsa_output.pci-0000_00_1f.3-platform-sof_sdw.HiFi__Speaker__sink
alsa_output.pci-0000_00_1f.3-platform-sof_sdw.HiFi__Headphones__sink
```

A configuration snippet written against a `HDA Intel PCH` node name will not match anything
here, which is worth knowing before concluding that a rule has been ignored.

## Bluetooth and Wi-Fi are one part

The AX211 is a CNVi design, so the Wi-Fi side attaches through the chipset whilst the Bluetooth
side appears on the USB bus as `8087:0033` and is driven by `btusb`. `rfkill` therefore lists
four entries rather than two: the two Dell platform switches, `dell-wifi` and `dell-bluetooth`,
and the two radios themselves, `phy0` and `hci0`. A radio can be blocked at either level, and
the platform switch is the one a function key toggles.

## No discrete GPU, despite the drivers

The 5470 is offered with a discrete workstation GPU. This unit does not have one: `lspci`
enumerates only the integrated Iris Xe, and no NVIDIA module is loaded. The NVIDIA userspace
packages are nonetheless installed, which means `nvidia-hibernate.service` and its siblings
appear in the journal on every suspend, skipped by their own `ExecCondition`:

```text
systemd[1]: nvidia-hibernate.service: Skipped due to 'exec-condition'.
```

That line is noise on this machine rather than a symptom, and it sits close enough to the sleep
transition to look relevant when reading a journal for something else.

## What has cost time here

- [Bluetooth A2DP fails with Protocol not available after resume](../findings/20260928_bluetooth_a2dp_fails_with_protocol_not_available_after_resume.md), which is a logind bookkeeping problem rather than a Bluetooth one, and survives a hibernate cycle on this machine specifically because hibernation works
- [A Bluetooth headset reconnects in A2DP instead of the saved profile](../findings/20260928_a_bluetooth_headset_reconnects_in_a2dp_instead_of_the_saved_profile.md), met with [the OpenMove](openmove_by_shokz.md)
