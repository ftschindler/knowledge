---
type: Finding
title: Deleting every image and container leaves rootless Docker using 100 GB
description: docker images and docker ps both come back empty whilst ~/.local/share/docker still
  holds 100 GB, because the BuildKit build cache and untagged images are counted separately and
  neither listing shows them.
tags:
- finding
- docker
- rootless
- linux
- arch
- disk-space
status: stable
stale_after: '2027-05-10'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-10T11:30:00+01:00'
sources:
- id: archwiki-images-location
  resource: https://wiki.archlinux.org/title/Docker#Images_location
  title: 'ArchWiki: Docker, Images location'
  last_modified: '2026-11-10'
- id: archwiki-rootless
  resource: https://wiki.archlinux.org/title/Docker#Rootless_Docker_daemon
  title: 'ArchWiki: Docker, Rootless Docker daemon'
  last_modified: '2026-11-10'
- id: docker-containerd-store
  resource: https://docs.docker.com/engine/storage/containerd/
  title: 'Docker docs: containerd image store'
  last_modified: '2026-11-10'
---
**Versions**: [Docker](../tools/docker.md) 29.7.2 in rootless mode on Manjaro, through
`docker-rootless-extras` from the AUR[^archwiki-rootless], using the containerd image store.

## The symptom

`~/.local/share/docker` measured 100 GB. Every container had been removed, and `docker images`
listed nothing worth keeping, so there was apparently nothing left to delete.

## What it was

`du` placed 92 GB under `containerd/daemon` and 8 GB under `volumes/`. `docker system df -v`
accounted for the rest:

| What | Size | Shown by `docker images` / `docker ps -a` |
| --- | --- | --- |
| BuildKit build cache | 73.7 GB | no |
| Five untagged `<none>` images, three of about 10 GB each | about 33 GB, sharing layers with the cache | only with `-a`, and easy to read past |
| Volumes, mostly left behind by `act` runs of GitHub workflows | 8.1 GB | no |

The figures overlap, which is why they add up to more than the directory. Removing images and
containers removes what those two commands list, and nothing else: the build cache belongs to
BuildKit, not to any image, and survives every `docker rmi`.

The location adds to the confusion. Since Docker 29, a new install uses the containerd image
store[^docker-containerd-store], as the ArchWiki also notes[^archwiki-images-location], so the layers sit under
`containerd/daemon/io.containerd.snapshotter.v1.overlayfs` rather than the `overlay2/` that most
advice about Docker disk usage tells you to look in. `docker info -f '{{ .DriverStatus }}'`
prints `[[driver-type io.containerd.snapshotter.v1]]` when this is the case.

## How to tell

```sh
du -xh --max-depth=2 ~/.local/share/docker | sort -rh | head
docker system df -v
```

The second command is the one that names each consumer. Its `Build Cache` line is the first
place to look.

## How to get past it

```sh
docker builder prune -a    # the build cache
docker image prune -a      # untagged and unused images
```

Leave volumes to a separate, named `docker volume rm`. A blanket prune deletes the database of
every Compose stack that is currently down, as
[docker volume prune -a deletes a Compose database while the stack is down](20261110_docker_volume_prune_a_deletes_a_compose_database_while_the_stack_is_down.md)
explains.

To keep the cache from growing back, give BuildKit a size limit:
[Cap the Docker build cache on rootless Docker](../guides/cap_the_docker_build_cache_on_rootless_docker.md).
