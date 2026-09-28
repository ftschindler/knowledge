---
type: Device
title: Dell Precision 5470
description: A 14-inch Alder Lake mobile workstation
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
sources:
- id: envycontrol
  resource: https://github.com/bayasdev/envycontrol
  title: 'EnvyControl: a tool to switch between hybrid and dedicated graphics'
  last_modified: '2026-09-28'
---
The Precision 5470 is Dell's 14-inch mobile workstation on Intel's Alder Lake-P platform.

| | |
| --- | --- |
| Vendor | Dell |
| Form factor | Notebook, 14-inch, DMI chassis type 10 |
| Processor | Intel Core i7-12800H, Alder Lake-P, 14-core hybrid |
| Memory | 32 GB, of which 30 GiB is visible to the kernel |
| Graphics | Intel Iris Xe, Alder Lake-P GT2, at `00:02.0`, alongside a discrete NVIDIA GPU at `01:00.0` currently switched off |
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

## The discrete GPU is switched off

This unit has the discrete NVIDIA GPU, on the x16 bridge at `00:01.0`. It does not appear in
`lspci`, and that absence is the thing to be careful about: the device is removed at boot rather
than missing.

EnvyControl[^envycontrol] holds the machine in `integrated` mode, which it does with two files.
A modprobe blacklist refuses `nouveau` and every `nvidia` module, and a udev rule removes the
hardware as it is enumerated:

```text
# /etc/udev/rules.d/50-remove-nvidia.rules
ACTION=="add", SUBSYSTEM=="pci", ATTR{vendor}=="0x10de", ATTR{class}=="0x03[0-9]*", \
  ATTR{power/control}="auto", ATTR{remove}="1"
```

So the rule fires on any NVIDIA display controller, sets it to autosuspend and unbinds it. By the
time anything asks `lspci` what is on the bus, bridge `00:01.0` has an empty secondary bus behind
it. Two things still record that the GPU exists: EnvyControl's own cache names its address, and
the bridge is there with nowhere to lead.

```bash
$ envycontrol --query
integrated
$ cat /var/cache/envycontrol/cache.json
{ "nvidia_gpu_pci_bus": "PCI:1:0:0" }
```

The NVIDIA driver packages are installed and current for the same reason, rather than being
leftovers: `envycontrol -s hybrid` and a reboot bring the card back, and it needs its drivers to
be there when it returns. The visible consequence in the meantime is that `nvidia-suspend`,
`nvidia-resume` and `nvidia-hibernate` are enabled units that skip themselves on every sleep:

```text
systemd[1]: nvidia-hibernate.service: Skipped due to 'exec-condition'.
```

That line sits close enough to the sleep transition to look relevant when reading a journal for
something else, and on this machine it is noise.

## Findings related to this machine

- [Bluetooth A2DP fails with Protocol not available after resume](../findings/20260928_bluetooth_a2dp_fails_with_protocol_not_available_after_resume.md), which is a logind bookkeeping problem rather than a Bluetooth one, and survives a hibernate cycle on this machine specifically because hibernation works
- [A Bluetooth headset reconnects in A2DP instead of the saved profile](../findings/20260928_a_bluetooth_headset_reconnects_in_a2dp_instead_of_the_saved_profile.md), met with [the OpenMove](openmove_by_shokz.md)
