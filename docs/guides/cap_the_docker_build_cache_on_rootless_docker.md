---
type: Guide
title: Cap the Docker build cache on rootless Docker
description: Turning on BuildKit's own garbage collection with a size limit in the rootless
  daemon.json, and checking the limit through buildx, since the daemon log never mentions it.
tags:
- guide
- docker
- rootless
- buildkit
- linux
- arch
- disk-space
status: stable
stale_after: '2027-05-10'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-10T11:30:00+01:00'
sources:
- id: docker-build-gc
  resource: https://docs.docker.com/build/cache/garbage-collection/
  title: 'Docker docs: Build garbage collection'
  last_modified: '2026-11-10'
- id: archwiki-rootless
  resource: https://wiki.archlinux.org/title/Docker#Rootless_Docker_daemon
  title: 'ArchWiki: Docker, Rootless Docker daemon'
  last_modified: '2026-11-10'
- id: archwiki-configuration
  resource: https://wiki.archlinux.org/title/Docker#Configuration
  title: 'ArchWiki: Docker, Configuration'
  last_modified: '2026-11-10'
---
**Versions**: [Docker](../tools/docker.md) 29.7.2, docker-buildx 0.36.1 and
docker-rootless-extras 29.9.2, on Manjaro, November 2026.

The BuildKit build cache has no limit worth the name by default, and it is invisible to
`docker images`. On one machine it reached 74 GB before anything noticed, which is the story in
[Deleting every image and container leaves rootless Docker using 100 GB](../findings/20261110_deleting_every_image_and_container_leaves_rootless_docker_using_100g.md).
BuildKit can clean up after itself[^docker-build-gc]; it needs a size to clean up to.

This is the Docker-native way of doing it. A systemd user timer running
`docker builder prune` would also work, but it is one more unit to maintain to reach what one
setting does.

## 1. Find the right config file

The ArchWiki puts the daemon configuration in `/etc/docker/daemon.json`[^archwiki-configuration].
That is the rootful daemon. **The rootless daemon**, run as a user unit from the AUR package
`docker-rootless-extras`[^archwiki-rootless], reads `~/.config/docker/daemon.json` instead, and
ignores the one in `/etc`. Editing the wrong one does nothing, silently.

## 2. Set the limit

`~/.config/docker/daemon.json`:

```json
{
  "builder": {
    "gc": {
      "enabled": true,
      "defaultKeepStorage": "10GB"
    }
  }
}
```

If the file already exists, merge the `builder` key into it rather than replacing the file.

## 3. Restart the user daemon

```sh
systemctl --user restart docker
systemctl --user is-active docker
```

This stops every running container, as any daemon restart does.

## 4. Check the limit was taken

**This step is silent when skipped.** A daemon that cannot parse `daemon.json` fails to start,
which is loud. But the journal from a successful start says nothing about garbage collection at
all, so it cannot tell a limit that was applied from a file the daemon never read, such as one
written to `/etc`. `journalctl --user -u docker` shows only that nothing went wrong.

Ask BuildKit instead:

```sh
docker buildx inspect
```

The output should show `GC Policy` rules whose `Reserved Space` is `10GiB`. Without the setting
the size reflects BuildKit's default, a share of the disk rather than the number you chose.

`docker system df` then shows the current size of the cache on its `Build Cache` line, which is
the number to watch over the next few weeks.

## What this leaves alone

Build cache only. Untagged images still need `docker image prune` now and then, and volumes
are deliberately out of reach of anything automatic, for the reason in
[docker volume prune -a deletes a Compose database while the stack is down](../findings/20261110_docker_volume_prune_a_deletes_a_compose_database_while_the_stack_is_down.md).
