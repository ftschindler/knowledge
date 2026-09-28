---
type: Finding
title: A Bluetooth headset reconnects in A2DP instead of the saved profile
description: WirePlumber consults a saved profile only in the first of three selection passes, so a
  headset deliberately kept in HFP returns to A2DP as soon as that saved state is not there.
tags:
- finding
- linux
- bluetooth
- audio
- wireplumber
- pipewire
status: stable
stale_after: '2027-03-28'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T08:58:20Z'
---
A Bluetooth headset switched by hand into the HSP/HFP profile comes back in A2DP after a
reconnect. The saved profile is real and it is honoured, but it is consulted in only the first of
three selection passes, and the pass that runs when it is missing decides by priority, where
A2DP outranks HFP by a factor of twenty-six.

Observed on WirePlumber 0.5.17 and PipeWire 1.6.8.

## Symptom

The card returns in `a2dp-sink`, 48 kHz stereo, after having been left in `headset-head-unit`:

```bash
$ pactl list short sinks | grep bluez
bluez_output.AA_BB_CC_DD_EE_FF.1  PipeWire  s16le 2ch 48000Hz  SUSPENDED
```

It survives for as long as nothing disturbs the saved state, which is what makes it look
intermittent: the headset behaves for days and then comes back wrong.

## How the profile is chosen

Three hooks run in a fixed order, each declaring its own position relative to the others, and
each returning immediately if a profile has already been selected:

| Order | Hook | Decides from |
| --- | --- | --- |
| 1 | `device/find-stored-profile` | `~/.local/state/wireplumber/default-profile` |
| 2 | `device/find-preferred-profile` | the `device.profile.priority.rules` configuration section |
| 3 | `device/find-best-profile` | the priority number on each profile |

The saved profile therefore wins whenever it is present, and contributes nothing whenever it is
not. On the [OpenMove](../hardware/openmove_by_shokz.md) the third pass is not close:
`a2dp-sink` carries priority 132 and `headset-head-unit` carries 5.

**The second pass does not rescue it by default.** With no rule configured, it falls back, for
BlueZ devices only, to the `bluetooth.profile-preference` setting, and both values that setting
accepts name an A2DP pseudo-profile: `quality` resolves to `a2dp-auto-prefer-quality` and
`latency` to `a2dp-auto-prefer-latency`. The setting chooses between A2DP variants. It cannot
express a preference for HFP at all, which is worth knowing before spending time on it.

## Why the saved state is not enough on its own

It is rewritten on every profile change, and it is read at exactly one point in the sequence.
Anything that clears or overwrites it drops the decision through to a pass where HFP cannot win:
a re-pair, a state reset, an automatic switch, or a deliberate switch to A2DP for one call that
is then never switched back.

## Fix

Give the second pass a rule. In a file under `~/.config/wireplumber/wireplumber.conf.d/`:

```text
device.profile.priority.rules = [
  {
    matches = [ { device.name = "bluez_card.AA_BB_CC_DD_EE_FF" } ]
    actions = { update-props = { priorities = [ "headset-head-unit", "headset-head-unit-cvsd" ] } }
  }
]
```

The card name is derived from the device address and is not portable between machines. Read the
real one with `pactl list short cards`. Listing the CVSD profile second means an absent mSBC
leaves the device in HFP rather than dropping it back to A2DP.

## Confirming it

The rule and the saved state both produce the wanted profile, so a test that leaves the saved
state in place proves nothing. Clear it first, and check the negative case as well:

```bash
printf '[default-profile]\n' > ~/.local/state/wireplumber/default-profile
systemctl --user restart wireplumber
```

| Rule | Saved state | Resulting profile |
| --- | --- | --- |
| present | cleared | `headset-head-unit` |
| absent | cleared | `a2dp-sink` |
| present | cleared, then a real disconnect and reconnect | `headset-head-unit`, codec `msbc` |

The middle row is the one that carries the argument. Without it, a headset that happens to be in
the right profile looks like a working rule.

## What it costs

HFP is bidirectional, so the wanted profile is 16 kHz mono with the microphone open, against
48 kHz stereo for A2DP. That is inherent to the profile rather than a side effect of the rule.
A deliberate switch to A2DP still works and is still remembered, by the first pass, until
something clears it and the rule takes over again.

Met whilst fixing
[Bluetooth A2DP fails with Protocol not available after resume](20260928_bluetooth_a2dp_fails_with_protocol_not_available_after_resume.md),
which had to be dealt with before any profile could be selected at all.
