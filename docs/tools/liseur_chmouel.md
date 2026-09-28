---
description: EPUB reader and sync server for self-hosted book libraries with reading-position synchronization across devices
type: concept
tags:
  - tools
  - reading
  - epub
  - self-hosted
resource:
  liseur: https://github.com/chmouel/liseur
  liseur-sync: https://github.com/chmouel/liseur-sync
generated:
  by: opencode/qwen3.5-397b-a17b
  on: 2026-09-28
---

# Liseur and Liseur-Sync (Chmouel Boudjnah)

An open-source EPUB reader for Android paired with a self-hosted sync server, designed for reading-position synchronization across devices and integration with personal book libraries.

## What it is

**Liseur** is the Android client: an EPUB reader using the Readium engine with support for local files, OPDS catalogs, and sync servers. **Liseur-sync** is the companion server: a single Go binary that provides reading-position synchronization, library management, and statistics.

Together they form a self-hosted alternative to commercial ebook ecosystems, with explicit support for KOReader synchronization and Calibre library integration.

## Key capabilities

### Reading synchronization

Reading positions are stored as an append-only log rather than replacing the previous state. This allows the server to resolve updates from multiple devices without older clients blindly overwriting newer state. The same history derives reading sessions and statistics.

Book identity is independent of filesystem path—clients resolve books using content and metadata identifiers before exchanging reading state. Reader preferences (typeface, theme, margins) sync as a small map of opaque strings per account, resolving by last-writer-wins.

### Library management

The server can index either:
- A directory containing EPUB files
- A Calibre library using `metadata.db`

Folders are granted to accounts individually and are read-only by default. Uploads and deletions require explicit configuration via `liseur-sync admin folder-uploads <folder-id> on`.

### Web reader with offline PWA

A browser-based EPUB reader is included, using the same synchronization API as native clients. When another device has read further, the reader offers to continue there, naming both pages and how long ago the other device was there.

The web UI ships as a PWA: choose "Save offline" for each book, install via "Add to Home Screen", and read without a network connection. Positions, highlights, notes, and reading sessions are stored locally until reconnection.

### Interfaces

- Native REST API
- KOReader-compatible kosync API
- OPDS 1.2 catalog
- Per-user reading statistics and sessions
- Per-user series claims
- Browser-based administration interface

## Installation

### Quick install

```bash
curl -fsSL https://raw.githubusercontent.com/chmouel/liseur-sync/main/scripts/install.sh | bash
```

### Docker Compose

SQLite (simplest):
```bash
docker compose --profile sqlite up -d
```

Bundled PostgreSQL:
```bash
docker compose --profile postgres up -d
```

External PostgreSQL:
```bash
docker compose --profile external up -d
```

### Build from source

```bash
go build ./cmd/liseur-sync
./liseur-sync serve
```

## Initial setup

The web interface is at `/ui/`. When the database contains no accounts, the setup page creates the initial administrator account and can watch a first folder of books in the same step.

Users, folders, API tokens, folder grants, and reader pairing are managed from the administration interface or with the `admin` CLI.

## Client integration

Liseur uses the native API. Protocol and synchronization details are documented in [`docs/integrating.md`](https://github.com/chmouel/liseur-sync/blob/main/docs/integrating.md) in the server repository.

OpenAPI specification: [`docs/openapi.yaml`](https://github.com/chmouel/liseur-sync/blob/main/docs/openapi.yaml)

## Related projects

- **liseur-desktop**: Desktop version (abandoned)
- **KOReader**: Supported via kosync-compatible API
- **Calibre**: Integration via `metadata.db` catalog

## License

MIT

## Author

Chmouel Boudjnah
- Fediverse: [@chmouel@chmouel.com](https://fosstodon.org/@chmouel)
- Twitter: [@chmouel](https://twitter.com/chmouel)
- Blog: https://blog.chmouel.com