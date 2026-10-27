---
type: Guide
title: Pin an AUR package to an older version with a paru PKGBUILD repo
description: How to hold an AUR package at the version a lagging distribution can satisfy, by
  checking out the matching commit into a local PKGBUILD repository that masks the AUR, and the
  Mode setting that silently stops it working.
tags:
- guide
- paru
- aur
- manjaro
- arch
- linux
- package-management
status: stable
stale_after: '2027-04-27'
generated:
  by: opencode/claude-opus-5
  at: '2026-10-27T15:10:00+01:00'
sources:
- id: paru-pkgbuild-repo
  resource: https://github.com/Morganamilo/paru/discussions/1068
  title: 'Install specific version of an AUR package, paru discussion 1068'
  last_modified: '2024-12-27'
---
An AUR package whose `depends` names an exact version cannot be installed on a distribution whose
repositories are behind Arch. `virtualbox-ext-oracle` is the standing example: its PKGBUILD
carries `depends=("virtualbox=${pkgver}")`, so the 7.2.22 package demands `virtualbox=7.2.22`,
and a Manjaro stable machine holding 7.2.16 cannot satisfy it. The same shape appears wherever a
packager pins a plugin to its host, and the delay is structural rather than a mistake: Manjaro
stable batches Arch's packages behind its own testing branches, so the gap opens again on every
upstream release.

Editing the PKGBUILD by hand works once and then fights every refresh, because the AUR's copy is
still newer and the helper keeps offering it. A PKGBUILD repository does not, because paru treats
the local copy as authoritative.

Commands are as of paru 2.1.0 on Manjaro, driving an AUR clone of `virtualbox-ext-oracle`.

## What a PKGBUILD repo is, and what it is not

paru reads a `[reponame]` section in its config as a directory of PKGBUILDs, scanned recursively,
and **packages found there take priority over the AUR**. That priority is the whole mechanism:
the masked package's version is whatever the local checkout says, so a checkout of the matching
commit both satisfies the dependency and stops the upgrade being offered, with no ignore list to
maintain.

This is a different kind of thing from the local repository at `/var/lib/repo/aur`, which paru's
`LocalRepo` fills with **built** packages and pacman serves as `[aur]`. One holds build recipes
and is read before the AUR; the other holds `.pkg.tar.zst` files and is read by pacman. They sit
side by side under `/var/lib/repo` because they are both parts of the same local AUR workflow,
not because they do the same job.

## 1. Clone the package into the repo

```bash
mkdir -p /var/lib/repo/aur-pins
git clone https://aur.archlinux.org/virtualbox-ext-oracle.git /var/lib/repo/aur-pins/virtualbox-ext-oracle
```

One directory per pinned package, each a full clone. Keeping the git history rather than copying
the files out is what makes the next step and the unpin in step 5 single commands, and it is why
the version to pin gets chosen here rather than in a scratch directory somewhere.

## 2. Check out the commit that matches

The AUR serves every package as a git repository, so each released version is a commit. Read the
log of the clone just made:

```bash
git -C /var/lib/repo/aur-pins/virtualbox-ext-oracle log --oneline -- PKGBUILD
```

```text
6672263 commit virtualbox-ext-oracle 7.2.22-1
f943bc0 commit virtualbox-ext-oracle 7.2.20-1
e0a291f commit virtualbox-ext-oracle 7.2.18-1
04af6cd commit virtualbox-ext-oracle 7.2.16-1
```

Restricting the log to `PKGBUILD` is worth the extra argument. Packages accumulate commits that
touch only `.SRCINFO` or the maintainer's tooling, and those produce log lines that look like
releases but are not.

Match against what is actually installed, not against what the AUR wants:

```bash
pacman -Q virtualbox
```

Then check out the commit whose version that is:

```bash
git -C /var/lib/repo/aur-pins/virtualbox-ext-oracle checkout 04af6cd
```

## 3. Declare it in `paru.conf`

Append a section to the `paru.conf` paru actually reads, which on a machine with a user config is
`~/.config/paru/paru.conf`; step 4 says how to tell:

```ini
[aur-pins]
Path = /var/lib/repo/aur-pins
```

`Path` takes a plain filesystem path, not a `file://` URL. The distinction matters: `Path` reads
the directory directly, so an edit or a checkout is visible to the next paru invocation and there
is no review step, whilst `Url` treats the target as a git remote to clone and refresh on
`paru -Sya`. For a directory being hand-curated on the same machine, `Path` is the one that
behaves as expected.

## 4. Allow paru to act on PKGBUILD repos

**This is the step that is silent when skipped.** A config carrying `AurOnly` restricts paru to
the AUR, and a PKGBUILD repo is not the AUR, so the section declared in step 3 is ignored
entirely. There is no warning; `paru -Si` simply keeps answering with the AUR's version, which
reads exactly like the pin not having been written.

The setting lives in the same `[options]` section the rest of the general configuration is in,
which paru reads from `$PARU_CONF`, then `$XDG_CONFIG_HOME/paru/paru.conf`, then
`~/.config/paru/paru.conf`, then `/etc/paru.conf`. **Only the first of those that exists is
read**, so a user config masks the system one completely rather than extending it, and `AurOnly`
has to be dealt with wherever it actually sits:

```bash
grep -rn 'AurOnly\|^Mode' ~/.config/paru/paru.conf /etc/paru.conf
```

Edit that file, replacing the `AurOnly` line under `[options]` with the mode list that includes
both:

```ini
[options]
Mode = aur pkgbuilds
```

The `[aur-pins]` section from step 3 goes at the end of the same file, after every `[options]`
key. An ini section runs until the next header, so a `Mode` line written below `[aur-pins]` is
read as a setting of the PKGBUILD repo rather than a general option.

**The separator is whitespace, not a comma**, though `paru.conf(5)` writes the values as
`aur|repo|pkgbuilds` and invites the comma that every other list-valued setting takes.
`Mode = aur,pkgbuilds` fails with `unknown mode aur,pkgbuilds`, which at least fails loudly.

Omitting `repo` preserves what `AurOnly` was doing: a `paru` sysupgrade still leaves repository
packages alone, which is the right division on a machine where arch-update owns those.

## 5. Check it, install, and unpin later

```bash
paru -Si virtualbox-ext-oracle
```

The pin is working when `Repository` reads `aur-pins`, the version is the pinned one, and a
`Path` line appears at the foot of the output pointing into the repo:

```text
Repository      : aur-pins
Name            : virtualbox-ext-oracle
Version         : 7.2.16-1
Depends On      : virtualbox=7.2.16
Path            : /var/lib/repo/aur-pins/virtualbox-ext-oracle
```

`paru -S virtualbox-ext-oracle` then resolves and builds normally. Because paru sees 7.2.16 as
the latest version in existence, the package is also not offered for upgrade, so nothing needs
adding to `IgnorePkg` and arch-update stops reporting it as pending.

When the distribution catches up, move the checkout forward:

```bash
git -C /var/lib/repo/aur-pins/virtualbox-ext-oracle checkout master
```

Or delete the directory, which hands the package back to the AUR. Leaving a stale pin in place is
the failure mode to watch for, since a pin is invisible once it stops being the thing blocking
an install, and silently holding a package a year behind is not what it was for.

## What this does not fix

**The pin applies to one machine and one helper.** pacman knows nothing about it, so a
`pacman -Syu` that wants to upgrade `virtualbox` past the pinned extension pack still reports a
dependency conflict, and the answer there is still to remove the extension pack, upgrade, and
reinstall from the pin.

**An old version is an old version.** For `virtualbox-ext-oracle` the content is a binary blob
from Oracle and holding it back alongside a matching VirtualBox is exactly what upstream asks
for, so the pin costs nothing. For a package carrying security fixes, the same mechanism quietly
declines them, and the pin is then a decision to be revisited rather than a fix.
