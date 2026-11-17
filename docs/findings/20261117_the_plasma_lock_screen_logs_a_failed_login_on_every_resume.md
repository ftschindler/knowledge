---
type: Finding
title: The Plasma lock screen logs a failed login on every resume, and faillock locks the account
description: Nobody touches the keyboard; the lock screen cancels its own pending password prompt
  when the machine sleeps or wakes, pam_unix reports that as a failed password, and three of them
  trip pam_faillock.
tags:
- finding
- linux
- kde
- plasma
- kscreenlocker
- pam
- suspend
- arch
status: stable
stale_after: '2027-05-17'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T22:30:00+01:00'
sources:
- id: kde-bug-481808
  resource: https://bugs.kde.org/show_bug.cgi?id=481808
  title: 'KDE bug 481808: Sleep mode of Plasma causes a failed login attempt'
  last_modified: '2026-11-17'
---
Opening the lid shows "Unlocking failed" on the lock screen before a key has been pressed, and
after a few suspend cycles the account is locked for several minutes. It looks like phantom
input. There is none: the lock screen fails its own authentication, and the distribution's PAM
stack counts that failure like any other.

Observed with kscreenlocker 6.7.5 and pam 1.7.3 on Manjaro, on a
[Dell Precision 5470](../hardware/dell_precision_5470.md).

## Symptom

The failure lands in the same second as the resume:

```text
21:59:35 kernel: PM: suspend exit
21:59:35 kscreenlocker_greet: pam_unix(kde:auth): unexpected response from failed conversation function
21:59:35 kscreenlocker_greet: pam_unix(kde:auth): conversation failed
21:59:35 kscreenlocker_greet: pam_unix(kde:auth): auth could not identify password for [<user>]
21:59:36 kscreenlocker_greet: [PAM worker kde] Authentication attempt too soon. This shouldn't happen!
```

The same lines appear when the lock screen's own Sleep or Hibernate button starts the
transition, then on the way down rather than the way up. One cycle can log two failures, so
the default limit of three arrives quickly.

```bash
journalctl --since -14days | grep -E 'PM: suspend (entry|exit)|pam_unix\(kde:auth\)'
```

Pairing each `conversation failed` with a `suspend exit` in the same second is the check that
settles it.

## Cause

The lock screen calls `pam_authenticate()` as soon as it is shown, and the PAM conversation
then waits for a password. When the machine sleeps or wakes, the greeter cancels that waiting
call, and its conversation function returns `PAM_CONV_ERR`. `pam_unix` turns that into
`PAM_AUTHTOK_ERR`, which the Arch-derived `system-auth` treats as a failed password:

```text
auth  [success=1 default=bad]  pam_unix.so      try_first_pass nullok
auth  [default=die]            pam_faillock.so  authfail
```

`default=bad` lets the stack continue into `pam_faillock ... authfail`, which records the attempt.
With `faillock.conf` left at its defaults, `deny = 3`, three resumes lock the account. A
successful unlock runs `authsucc` and clears the tally, which is why `faillock` usually shows
nothing when checked afterwards.

**A fingerprint reader is not involved**, though it is the first suspect on a laptop that has
one. `kscreenlocker` runs a separate `kde-fingerprint` PAM service for that, and the failures
above are all in the `kde` service, the password one.

The bug is upstream's[^kde-bug-481808], open since Plasma 6.2 and fixed in 6.8 by aborting
the authentication flows on sleep rather than letting them fail.

## How to get past it

Until 6.8 arrives, stop the tally from locking the account. In `/etc/security/faillock.conf`:

```text
deny = 0
```

Wrong passwords are still logged, but no longer lock the account. pacman treats the file as
configuration, so an upgrade of `pam` leaves the edit alone and writes a `.pacnew` beside it.
Clear an existing lock with `faillock --user <user> --reset`.

The narrower alternative, from the bug thread, is an `/etc/pam.d/kde` that inlines the
`system-local-login` chain and gives `pam_unix` the action `authtok_err=die`, so this one
return code skips `authfail`. It keeps the lockout for real failures, at the cost of a private
copy of the distribution's PAM chain that no update will touch again. Neither removes the
"Unlocking failed" message on wake, because the conversation is still started and cancelled.

Revert `deny = 0` once Plasma 6.8 is installed, if the lockout is wanted back.

## What it is not

Not input. The pointer analogue on the same machine,
[a phantom touch pinning the pointer to the system tray](20261029_a_phantom_touch_pins_the_pointer_to_one_point_in_the_system_tray.md),
really was a device reporting contact that never lifted, and it is tempting to read this the
same way. The difference is in where the evidence sits: a stuck contact shows up in
`xinput query-state`, and this shows up as a PAM conversation error timed to the suspend.
