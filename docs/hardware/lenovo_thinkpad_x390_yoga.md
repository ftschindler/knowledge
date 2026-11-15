---
type: Device
title: Lenovo ThinkPad X390 Yoga
description: A 13-inch Whiskey Lake convertible with a Wacom pen and touch digitizer, a classic
  Realtek HDA codec rather than SoundWire, and no discrete GPU.
tags:
- hardware
- lenovo
- thinkpad
- convertible
- linux
- audio
- bluetooth
status: stable
generated:
  by: opencode/glm-5.2
  at: '2026-11-15T12:00:00+01:00'
---
The ThinkPad X390 Yoga is Lenovo's 13-inch convertible on Intel's Whiskey Lake-U platform,
with a 360-degree hinge and a Wacom pen and touch digitizer.

| | |
| --- | --- |
| Vendor | Lenovo |
| Form factor | Notebook, 13-inch, convertible, DMI chassis type 31 |
| Processor | Intel Core i5-8365U, Whiskey Lake-U, 4-core |
| Memory | 16 GB, two 8 GiB DDR4 SODIMMs at 2400 MT/s (2667 MT/s rated) |
| Storage | A 2 TB Samsung SSD 860 EVO M.2 over SATA, carrying LUKS and LVM |
| Graphics | Intel UHD Graphics 620, WhiskeyLake-U GT2, at `00:02.0` |
| Display | eDP-1, 1920x1080, 294 x 165 mm |
| Audio | Cannon Point-LP HD Audio controller at `00:1f.3`, driving a Realtek ALC257 codec |
| Wireless | Intel Cannon Point-LP CNVi, Wireless-AC 9560, `iwlwifi` for Wi-Fi |
| Bluetooth | Intel Bluetooth 9460/9560 (JfP) on the USB bus as `8087:0aaa`, `btusb` |
| Ethernet | Intel Ethernet Connection (6) I219-LM at `00:1f.6` |
| Thunderbolt | JHL6240 Alpine Ridge LP 2016, at `07:00.0` |
| Pen and touch | Wacom Pen and multitouch sensor on USB as `056a:51af`, finger and pen inputs |
| Touchpad | Synaptics TM3469-010 over RMI4 |
| TrackPoint | TPPS/2 Elan TrackPoint |
| Camera | Syntek Integrated Camera, `174f:2435` |
| Fingerprint | Synaptics Prometheus MIS Touch Fingerprint Reader, `06cb:00bd` |
| SD card | Genesys Logic GL9750 SD Host Controller at `02:00.0` |
| Firmware | BIOS N2LET71W (1.71), 2019-12-05; ThinkPad EC firmware N2LHT33W |
| Read through | Manjaro Linux, kernel 6.12.112-1-MANJARO |

Everything above was read off the running machine rather than from a specification sheet, per
[the convention for this genre](index.md).

## The processor has no hyperthreading

The i5-8365U is a 4-core, 4-thread part: there is no hyperthreading to toggle, and
`/sys/devices/system/cpu/smt/control` reads `notsupported` because the hardware does not
provide it rather than because it is disabled. Anything that sizes a thread pool from
`nproc` on this machine gets 4. This is the same end result as
[the Dell Precision 5470](dell_precision_5470.md) on a different part and for a different
reason: the Precision's i7-12800H has performance cores that would normally contribute a
second thread each, and the firmware does not expose them, whilst the i5-8365U simply does
not have SMT.

## Audio is classic HDA, not SoundWire

The audio controller enumerates as Intel HD Audio and the codec behind it is a Realtek
ALC257 reached directly over the HD Audio link, not over SoundWire. ALSA therefore presents
the card as `HDA Intel PCH` with the node names that classic setup implies:

```text
alsa_output.pci-0000_00_1f.3.analog-stereo
```

A configuration snippet written against a `sof-soundwire` node name, as
[the Dell Precision 5470](dell_precision_5470.md) requires, will not match anything here.
There is a second ALSA card, `ThinkPadEC` at card 29, which is the ThinkPad's console audio
control rather than a codec: it exposes volume and mute knobs through the embedded
controller, and carries no playback or capture streams of its own.

## Bluetooth and Wi-Fi are one part

The Wireless-AC 9560 is a CNVi design, the same architecture as the AX211 in
[the Dell Precision 5470](dell_precision_5470.md) one generation back: the Wi-Fi side
attaches through the chipset at `00:14.3` whilst the Bluetooth side appears on the USB bus
as `8087:0aaa` and is driven by `btusb`. `rfkill` on this machine lists two entries rather
than four, because a ThinkPad does not carry the platform radio switches a Dell does: only
the two radios themselves, `phy0` and `hci0`, with no `dell-wifi` or `dell-bluetooth`
intermediate. A radio can still be blocked, but only at the one level.

## The pen and touch digitizer

The Wacom digitizer is a USB device at `056a:51af`, presenting two input devices: a finger
input for multitouch and a separate pen input for the stylus. The hinge rotates 360 degrees
to tablet mode, and the ThinkPad ACPI layer reports tablet mode through
`/sys/devices/platform/thinkpad_acpi/hotkey_tablet_mode`, which a desktop environment can
read to disable the keyboard and touchpad when folded. The digitizer itself needs no
configuration beyond the `wacom` kernel module, which is built into Manjaro's default
initramfs.

## There is no discrete GPU

This configuration carries only the integrated UHD Graphics 620. There is no NVIDIA or AMD
part on the PCI bus, no modprobe blacklist to maintain, and no mode-switching tool such as
EnvyControl needed. The x16 bridge at `00:01.0` is present but empty, which is the normal
state for a ThinkPad that was not ordered with a dGPU and not the sign of a device removed at
boot.
