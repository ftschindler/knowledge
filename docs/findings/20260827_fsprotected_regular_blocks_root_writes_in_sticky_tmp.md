---
type: Finding
title: fs.protected_regular Blocks Root Writes in Sticky tmp
description: A file in a sticky /tmp owned by another user cannot be opened for writing even by root,
  because the restriction keys off ownership rather than permission bits.
tags:
- finding
- linux
- sysctl
- permissions
- security
- tmp
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
A file in `/tmp` owned by another user cannot be opened for writing -
**even by root** - and `chmod 777` does not help, because the restriction keys
off *ownership*, not permission bits.

## Symptom

A root process gets `EACCES` / "Permission denied" writing a file whose mode
plainly permits it:

```text
-rwxrwxrwx 1 felix felix 0 Aug 27 07:09 /tmp/debug.log
```

```bash
sudo /tmp/debug.sh          # -> "permission denied" on /tmp/debug.log
```

The mode is `777` and the writer is root, so by classic Unix rules this must
succeed. It fails anyway, which makes it look like a bug in the script.

## Cause

```bash
$ sysctl fs.protected_regular
fs.protected_regular = 1
```

With `fs.protected_regular=1` (the systemd default on most distributions), the
kernel refuses to open a **regular file for writing** when all of the following
hold:

- the file sits in a **world-writable, sticky** directory (`/tmp`, `/var/tmp`,
  `/dev/shm` - mode `drwxrwxrwt`), **and**
- the file is **owned by a different user** than the opener, **and**
- the open requests write access

**Root is not exempt.** This is deliberate: it defends against a classic attack
where an unprivileged user pre-creates or swaps a predictably-named file in
`/tmp` so that a privileged process later writes through it. `fs.protected_fifo`
and `fs.protected_symlinks` guard the FIFO and symlink variants of the same
trick.

## Fix

**Delete and recreate.** Root may always unlink in a sticky directory, so the
stale file goes away and the new one is created root-owned:

```bash
rm -f "$LOG"
: > "$LOG"
chmod 644 "$LOG"     # so the unprivileged user can still read it afterwards
```

Do **not** try to fix it by loosening the mode - `chmod 777` changes nothing,
because the check never looks at the mode.

## Guidance for scripts

- In any root script that writes to a fixed path in `/tmp`, **unlink first**,
  then create. Never assume an existing file is writable just because its mode
  says so.
- Create the log **after** the privilege check, not before. Truncating at the
  top of the script means every accidental non-root run silently destroys the
  previous run's results.
- Be alert to this whenever a shared scratch path is touched by *both* a normal
  user and root - for example a file created by an earlier unprivileged test
  run, then reused by a later `sudo` run. That mixed-ownership sequence is the
  usual way people trip over it.

## Diagnosing it

The tell is EACCES on a file whose mode clearly allows the write. Confirm with:

```bash
ls -l <file>                          # note the OWNER, not the mode
ls -ld $(dirname <file>)              # is it drwxrwxrwt ?
sysctl fs.protected_regular           # 1 = enforced
```

If the owner differs from the writer and the directory is sticky and
world-writable, this is the cause.
