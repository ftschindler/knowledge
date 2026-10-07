---
type: Finding
title: Bluetooth A2DP fails with Protocol not available after resume
description: A headset that will not connect because WirePlumber never started its BlueZ monitor,
  because logind's per-user state file says the user is inactive whilst logind's own session and seat
  records say otherwise.
tags:
- finding
- linux
- bluetooth
- audio
- wireplumber
- pipewire
- systemd
status: stable
stale_after: '2027-03-28'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T08:58:20Z'
sources:
- id: wireplumber-bluetooth-config
  resource: https://gitlab.freedesktop.org/pipewire/wireplumber/-/blob/251d7424df15b4516ae17b4cc1181f9043150427/docs/rst/daemon/configuration/bluetooth.rst
  title: 'WirePlumber: Bluetooth configuration'
  last_modified: '2026-09-28'
- id: wireplumber-module-logind
  resource: https://gitlab.freedesktop.org/pipewire/wireplumber/-/blob/251d7424df15b4516ae17b4cc1181f9043150427/modules/module-logind.c
  title: 'WirePlumber: modules/module-logind.c'
  last_modified: '2026-09-28'
---
A paired Bluetooth headset refuses to connect after a resume, and BlueZ reports a protocol
failure. Neither BlueZ nor the adapter is at fault: WirePlumber never started its BlueZ monitor,
so no media endpoint was registered for BlueZ to offer, and it never started it because logind's
per-user state file claims the user is not active. That file contradicts logind's own seat and
session records, and every command a person reaches for to check reads the records rather than
the file.

Observed on WirePlumber 0.5.17, PipeWire 1.6.8, BlueZ 5.87 and systemd 261.

## Symptom

```text
bluetoothd: src/service.c:btd_service_connect() a2dp-sink profile connect failed
for AA:BB:CC:DD:EE:FF: Protocol not available
```

Everything that usually explains this looks correct. The adapter is powered and unblocked, the
device is still paired, `bluetooth.service` is running, and the PipeWire BlueZ plugins are
installed. Restarting `bluetooth.service` changes nothing.

**The distinguishing tell is that restarting WirePlumber changes nothing either.** A session
manager that has merely lost track of a device recovers when it is restarted. One that is being
prevented from starting the monitor at all comes back in exactly the same state, which is what
separates this from the ordinary post-suspend audio confusion.

## What the error actually means

"Protocol not available" here is not the headset refusing anything. BlueZ offers a profile only
if some client has registered a media endpoint advertising a codec for it, and
`btd_service_connect` reports this when none has. The count is visible in the journal:

```bash
journalctl -b | grep -c "Endpoint registered"
```

A working session registers these at WirePlumber startup, around twenty of them on a machine
with the usual codec set. A broken one registers none, and the last thing in the journal about
them is a block of `Endpoint unregistered` lines at the moment the machine went to sleep.

## Cause

The BlueZ monitor is deliberately gated on logind. The reasoning upstream gives is that a
graphical login manager runs as its own user with its own PipeWire instance, and would otherwise
grab the Bluetooth audio devices away from whoever logs in, so the monitor creates device and
node objects only for a user on the active logind session.[^wireplumber-bluetooth-config]

WirePlumber's logind module decides that through `sd_uid_get_state`, and additionally rewrites a
state of `active` to `online` when the user has no seat that is itself active, via
`sd_uid_get_seats` with its `require_active` argument set.[^wireplumber-module-logind] The
monitor runs on `active` and on nothing else.

After a resume, logind's bookkeeping for the user disagrees with its bookkeeping for the seat
and the session. The user file reports the user as online, with no active seat, and with the
active session given as the seatless manager session rather than the graphical one:

```text
# /run/systemd/users/1000
STATE=online
ACTIVE_SESSIONS=1
ACTIVE_SEATS=
ONLINE_SEATS=seat0
```

Both of the other two files contradict it:

```text
# /run/systemd/seats/seat0        # /run/systemd/sessions/3
ACTIVE=3                          ACTIVE=1
ACTIVE_UID=1000                   STATE=active
```

So the graphical session is active on seat0 and owned by this user, whilst the user is recorded
as having no active seat. Either half of the user file is enough on its own to stop the monitor:
the state is already `online` before WirePlumber's own downgrade is reached, and the empty
`ACTIVE_SEATS` would trigger that downgrade even if it were not.

## Why every check says the session is active

`loginctl` answers from logind's live objects over D-Bus. `sd_uid_get_state` reads the file. The
two disagree, and WirePlumber believes the library:

```text
$ loginctl show-user "$USER" -p State
State=active
```

This is the part that costs the time. Session state, seat state and user state all read
correctly, the adapter is fine, the plugins are present, and nothing anywhere reports an error.
WirePlumber logs the decision at debug level only, as a single line naming the state it settled
on:

```text
s-monitors-bluez: <WpLogind> Seat state changed: online
```

## Confirming it

Ask the library directly rather than asking `loginctl`, which is the only check that
distinguishes this from every other cause:

```python
import ctypes, ctypes.util, os
lib = ctypes.CDLL(ctypes.util.find_library("systemd"))
st = ctypes.c_char_p()
lib.sd_uid_get_state(os.getuid(), ctypes.byref(st))
print("state:", st.value)
print("active seats:", lib.sd_uid_get_seats(os.getuid(), 1, None))
```

`state: b'online'` with `active seats: 0`, on a machine where `loginctl` says the session is
active, is this finding and not another one.

## Fix

Disable the seat gate for the BlueZ monitor. The fragment is the one upstream
documents,[^wireplumber-bluetooth-config] in a file under
`~/.config/wireplumber/wireplumber.conf.d/`:

```text
wireplumber.profiles = {
  main = {
    monitor.bluez.seat-monitoring = disabled
  }
}
```

Restart WirePlumber, and the endpoints register immediately.

**Repairing the logind state instead does not work.** `loginctl activate` on the graphical
session, which is already the seat's active session, leaves `STATE`, `ACTIVE_SESSIONS` and
`ACTIVE_SEATS` in the user file exactly as they were. Nothing short of ending the session
rebuilds it, so on a machine that is resumed rather than rebooted the configuration change is
the remedy rather than a workaround for one.

What the gate is given up in exchange is arbitration between simultaneous users: the login
manager's PipeWire instance, or a second logged-in user, may now hold the Bluetooth audio
device whilst inactive. On a single-user machine that is not a cost. On a shared one it is the
behaviour the gate exists to provide.

## Scope

The gate is WirePlumber's, but the disagreement underneath it is not. Anything that decides
whether a user is present by calling `sd_uid_get_state` sees `online` here whilst the desktop is
plainly in use, and will behave as though nobody is logged in.
