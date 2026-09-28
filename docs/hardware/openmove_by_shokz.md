---
type: Device
title: OpenMove by Shokz
description: An open-ear bone-conduction Bluetooth headset that offers SBC for music and mSBC for
  voice, advertises no vendor or product ID, and is used here in the lower-quality profile.
tags:
- hardware
- bluetooth
- audio
- shokz
- linux
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T08:58:20Z'
sources:
- id: shokz-openmove
  resource: https://shokz.com/products/openmove
  title: 'Shokz: OpenMove'
  last_modified: '2026-09-28'
---
The OpenMove is a bone-conduction headset: it sits in front of the ear rather than over or in
it, and conducts through bone, leaving the ear canal open.[^shokz-openmove] That is the whole
reason it is used here, and it is also why the profile it runs in matters more than it would on
a pair of headphones.

| | |
| --- | --- |
| Vendor | Shokz |
| Type | Open-ear, bone conduction |
| Bluetooth name | `OpenMove by Shokz` |
| Device class | Reported to BlueZ as `audio-headphones` |
| A2DP codecs | SBC, and SBC-XQ |
| HFP codecs | mSBC, and CVSD |
| Identification | Advertises no vendor or product ID |

## The four profiles it offers

PipeWire presents these as card profiles, and the priorities are the part worth writing down,
because profile selection falls back to them:

| Profile | Transport and codec | Format | Priority |
| --- | --- | --- | --- |
| `a2dp-sink` | A2DP, SBC | 48 kHz stereo | 132 |
| `a2dp-sink-sbc_xq` | A2DP, SBC-XQ | 48 kHz stereo | 131 |
| `headset-head-unit` | HSP/HFP, mSBC | 16 kHz mono, with the microphone | 5 |
| `headset-head-unit-cvsd` | HSP/HFP, CVSD | 8 kHz mono, with the microphone | 4 |

Nothing beyond SBC is on offer for music: no AAC, no aptX, no LDAC. The choice is therefore not
between a good codec and a bad one but between a stereo playback-only profile and a mono
profile that also carries the microphone.

The two A2DP profiles outrank the two headset profiles by a factor of twenty-six, which is the
mechanism behind
[A Bluetooth headset reconnects in A2DP instead of the saved profile](../findings/20260928_a_bluetooth_headset_reconnects_in_a2dp_instead_of_the_saved_profile.md).
This device is deliberately used in `headset-head-unit`, so that ordering has to be overridden
rather than accepted.

## It cannot be matched by vendor or product

The headset advertises ten service UUIDs, including Handsfree, Advanced Audio Distribution and
both sides of AVRCP, alongside a Serial Port entry and a PnP Information record. The PnP record
is empty in the way that matters:

```text
bluetooth:v000ApFFFFdFFFF
```

Product and device identifiers are `FFFF`, the unset value. A rule that wants to single this
device out therefore cannot key off vendor and product the way a USB rule would, and has to
match on the card name that BlueZ derives from the device address instead. Both configuration
fragments in the findings below do exactly that, which is also why they cannot be copied
between machines unedited.

## What has cost time here

- [A Bluetooth headset reconnects in A2DP instead of the saved profile](../findings/20260928_a_bluetooth_headset_reconnects_in_a2dp_instead_of_the_saved_profile.md), the priority ordering above meeting a saved profile that loses to it
- [Bluetooth A2DP fails with Protocol not available after resume](../findings/20260928_bluetooth_a2dp_fails_with_protocol_not_available_after_resume.md), which is not about this device at all, but presents as this device refusing to connect

Met on [the Precision 5470](dell_precision_5470.md).
