---
type: Tool
title: Docker
description: The container engine and CLI, run here as a rootless user daemon on Arch, and where
  that puts its configuration and its data.
tags:
- tools
- docker
- rootless
- containers
- linux
- arch
status: draft
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-10T11:30:00+01:00'
sources:
- id: archwiki-docker
  resource: https://wiki.archlinux.org/title/Docker
  title: 'ArchWiki: Docker'
  last_modified: '2026-11-10'
- id: archwiki-rootless
  resource: https://wiki.archlinux.org/title/Docker#Rootless_Docker_daemon
  title: 'ArchWiki: Docker, Rootless Docker daemon'
  last_modified: '2026-11-10'
- id: docker-rootless
  resource: https://docs.docker.com/engine/security/rootless/
  title: 'Docker docs: Rootless mode'
  last_modified: '2026-11-10'
---
Docker[^archwiki-docker] builds and runs containers: a daemon, `dockerd`, that does the work, and
the `docker` CLI that asks it to. Here it runs **rootless**[^docker-rootless]: the daemon is an
ordinary process of my own user, so a container breaking out lands as me rather than as root.

| | |
| --- | --- |
| Author | Docker, Inc., on the open-source Moby project |
| Licence | Apache-2.0 (Engine and CLI) |
| Language | Go |
| Distribution | Arch packages `docker`, `docker-buildx`, `docker-compose`; rootless mode from the AUR package `docker-rootless-extras` |
| Source | [github.com/moby/moby](https://github.com/moby/moby) |
| Version read | 29.7.2 |

## Rootless, the Arch way

The ArchWiki covers the setup[^archwiki-rootless]: install `docker-rootless-extras`, give the
user a subordinate UID and GID range in `/etc/subuid` and `/etc/subgid`, and enable `docker` as a
**user** unit rather than a system one. The AUR package ships those units in place of upstream's
`dockerd-rootless-setuptool.sh`. The client then needs a context or `DOCKER_HOST` pointing at
the socket under `$XDG_RUNTIME_DIR`.

Everything that would live in a system path moves into the home directory, and most advice
written for rootful Docker points at the wrong place as a result:

| What | Rootful | Rootless |
| --- | --- | --- |
| Daemon config | `/etc/docker/daemon.json` | `~/.config/docker/daemon.json` |
| Data | `/var/lib/docker` | `~/.local/share/docker` |
| Service | `systemctl restart docker` | `systemctl --user restart docker` |
| Logs | `journalctl -u docker` | `journalctl --user -u docker` |

A new install of Docker 29 or later also uses the containerd image store, so even inside the
data directory the layers are under `containerd/daemon/`, not `overlay2/`.

## What is known about it here

- [Deleting every image and container leaves rootless Docker using 100 GB](../findings/20261110_deleting_every_image_and_container_leaves_rootless_docker_using_100g.md) - where the space goes once `docker images` is empty
- [docker volume prune -a deletes a Compose database while the stack is down](../findings/20261110_docker_volume_prune_a_deletes_a_compose_database_while_the_stack_is_down.md) - how Compose names volumes, and why a prune cannot tell a database from debris
- [Cap the Docker build cache on rootless Docker](../guides/cap_the_docker_build_cache_on_rootless_docker.md) - the one setting that stops the cache growing back

## To fill in

A draft, written so the page exists and can be linked at. Still missing: how rootless
networking differs in practice (port binding below 1024, and the slirp or pasta layer in
between), and how `act` and the VS Code dev containers behave against a rootless socket.
