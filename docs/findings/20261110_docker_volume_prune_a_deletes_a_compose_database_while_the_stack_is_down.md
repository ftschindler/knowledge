---
type: Finding
title: docker volume prune -a deletes a Compose database while the stack is down
description: A stopped Compose stack leaves its named volumes attached to no container, so a
  blanket volume prune treats the database as unused, and a worktree in another directory gets
  volumes of its own rather than sharing the main checkout's.
tags:
- finding
- docker
- docker-compose
- data-loss
- git-worktree
status: stable
stale_after: '2027-05-10'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-10T11:30:00+01:00'
sources:
- id: compose-project-name
  resource: https://docs.docker.com/compose/how-tos/project-name/
  title: 'Docker docs: Specify a project name'
  last_modified: '2026-11-10'
- id: archwiki-compose
  resource: https://wiki.archlinux.org/title/Docker#Docker_Compose
  title: 'ArchWiki: Docker, Docker Compose'
  last_modified: '2026-11-10'
---
**Versions**: [Docker](../tools/docker.md) 29.7.2 and Docker Compose 5.5.1, from the Arch
`docker-compose` package[^archwiki-compose].

## The symptom

Clearing out a Docker data directory, `docker system df -v` listed 18 volumes, every one of them
with `LINKS 0`. Among them were two Postgres volumes holding real data, from a project whose
stack simply was not running at the time.

## What it was

Compose names a volume `<project>_<volume>`, and the project name defaults to the name of the
directory holding the compose file[^compose-project-name]. A compose file in `~/Projects/myapp`
that declares `myapp_db:` creates the volume `myapp_myapp_db`.

Two consequences follow from that, and neither is announced:

- **A stack that is down has no container using its volumes.** `docker compose down` removes
  the containers and keeps the volumes, so to Docker the database is exactly as unused as a
  volume left behind by a throwaway CI run. `docker volume prune -a` removes both.
  (Without `-a`, `prune` only removes anonymous volumes, and a Compose volume has a name.)
- **A git worktree gets its own copy of every volume.** Started from a worktree in a directory
  called `feature-x`, the same compose file creates `feature-x_myapp_db`: an empty database
  instead of the main checkout's data, and one more volume that outlives the worktree once the
  directory is deleted.

Bringing the stack up again in the original directory does find the old volume, by name, and
the data is still there.

## How to get past it

- Remove volumes one at a time with `docker volume rm <name>`, after reading the list, rather
  than with a prune.
- When a worktree should share the main checkout's data, set the project name explicitly, with
  `docker compose -p myapp up` or `name: myapp` at the top of the compose file. Do this
  deliberately, though: two checkouts sharing one database is not always what you want.
- When a worktree is removed, run `docker compose down -v` in it first, so its volumes go
  with it.

The disk-space problem that led to this is in
[Deleting every image and container leaves rootless Docker using 100 GB](20261110_deleting_every_image_and_container_leaves_rootless_docker_using_100g.md).
