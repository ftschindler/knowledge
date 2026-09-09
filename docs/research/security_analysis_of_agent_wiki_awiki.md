---
type: Reference
title: Security Analysis of Agent Wiki (awiki)
description: A security review of the agent-wiki CLI, asking what its potential for data leaks is and
  whether it phones home.
tags:
- security
- agent-wiki
- ai-agents
- data-privacy
- pkb
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-08-27T00:00:00Z'
---
**Context** – A security review of [TacoTakumi/agent-wiki](https://github.com/TacoTakumi/agent-wiki)
(PyPI: `agent-wiki-kb`), a CLI-driven markdown knowledge base that AI agents search before
reaching for the web and write back to when they learn something. The driving question:
**what is the potential for data leaks, and are there any deliberate reporting or
'phone-home' mechanisms built in?**

- **Version audited**: `0.8.1` (commit `b4b3dfe`, latest tag at time of review)
- **Date**: 2026-08-24
- **Method**: Full source read of `src/agent_wiki/`, an independent literal scan for every
  network primitive (`httpx`, `urllib`, `requests`, `socket`, `subprocess`) and every URL
  in the tree, plus data-flow tracing of the three paths that touch a network (URL ingest,
  the remote-vault client, the optional summariser) and the HTTP server's auth and path
  handling.

## Verdict

**No hidden data egress and no telemetry, analytics or reporting of any kind was found.**
There is no 'phone-home', no crash reporting, no usage metrics, no vendor SDK (searched:
sentry, posthog, mixpanel, segment, amplitude, google-analytics, telemetry, beacon,
metrics, track). Every outbound network call in the codebase goes to a destination **you
supply** - a URL you ask it to ingest, a remote vault server you configured, or a local LLM
endpoint you pointed it at. Nothing leaves the machine unless a command you ran sends it
somewhere you named.

The tool is, by design, **local-first and offline-capable**: the default summariser makes
zero LLM calls, search is local (ripgrep or a Python fallback), and the auto-context hook
is silent-fail and never blocks a prompt. The main data-leak considerations are therefore
**not** covert channels but the ordinary consequences of what the tool is *for*: it
deliberately reads your agent transcripts and shared secrets get baked into a plain-text
vault you may sync or serve.

!!! note "The real risk is aggregation, not exfiltration"
    Agent Wiki's whole purpose is to concentrate hard-won knowledge - conversation
    transcripts, decisions, tool configs - into **one plain-text vault shared across every
    project and machine**. That concentration is the point, and it is also the primary
    security consideration: a single vault becomes a high-value, plain-text target, and
    (once you `serve` it) a network-reachable one. There is no covert leak; there is a very
    deliberate, well-signposted pile of your own data.

## Every network destination in the codebase

The entire tree was scanned for network primitives. Real outbound traffic originates from
exactly **three** places, all of them destinations the user chooses:

| Origin | Destination | Owner | What is sent |
| --- | --- | --- | --- |
| `HttpFetcher.fetch` ([`fetch.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/fetch.py)) | the URL **you pass to `awiki ingest <url>`** | the site you named | an HTTP `GET` with `User-Agent: agent-wiki (awiki)`; follows redirects. No data of yours beyond the request itself |
| `RemoteVaultService` ([`remote.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/remote.py)) | the vault server **you set with `awiki init --remote <url>`** | your own server | every command's payload (search queries, page contents on ingest, bundles) over HTTP, with your bearer token |
| `LocalOpenAISummarizer` ([`summarize.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/summarize.py)) | `base_url` from `wiki.yaml` (**default `http://127.0.0.1:8080/v1`**) | your local LLM | the conversation transcript, for summarisation - only if you opt in |

Two more paths *look* like egress but are not:

- **`ClaudePSummarizer`** shells out to the local `claude` CLI (`claude -p`) with the
  transcript on stdin. Whatever that binary does with its own credentials is Claude Code's
  behaviour, not awiki's - awiki itself opens no socket here. This is opt-in via `wiki.yaml`.
- **`search.py`** shells out to `ripgrep` (local binary) with a 10-second timeout, purely to
  grep the local vault. No network.

There are **no** hardcoded third-party endpoints anywhere. The only literal URLs in the
Python are the `127.0.0.1` summariser default, `http://` scheme checks and example strings
in help text.

## Where the deliberate data collection is (by design, not covert)

Agent Wiki's job is to ingest your knowledge, so it reads several sensitive local stores. All
of this is documented and user-triggered, but it belongs in a data-leak assessment because it
is what actually ends up in the vault:

- **Claude Code transcripts** - the `claude-code` adapter reads `~/.claude/projects/<slug>/*.jsonl`
  and renders full user/assistant turns, tool calls and file paths into a conversation bundle.
- **OpenCode sessions** - the `opencode` adapter opens `~/.local/share/opencode/opencode.db`
  (read-only) and does the same.
- **Any dropped bundle** - the `drop-zone` adapter picks up pre-written bundles from
  `<vault>/incoming/`.
- **Ingested files and URLs** - copied byte-identically into an immutable `raw/` archive.

All of this lands as **plain text** in the vault. Nothing is encrypted at rest. If you sync
that vault (git, Dropbox, `awiki serve`), you sync everything in it.

### Redaction exists, but treat it as a lint, not a guarantee

[`redact.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/redact.py)
runs **unconditionally** on conversation bodies during `ingest-conversation`, replacing a set
of regexes with `[REDACTED]`: emails, `sk-`/`sk-ant-` keys, `ghp_`-style GitHub tokens, Slack
`xox…` tokens, Google `AIza…` keys and PEM private-key blocks, plus your local username
(replaced with `[USER]`). This is a **useful, cheap best-effort filter**, and worth knowing its
limits:

!!! warning "Redaction is regex-only and covers conversation bundles, not file/URL ingest"
    - It only catches secrets that **match the built-in patterns** (or extra ones you add in
      `wiki.yaml`). A bespoke internal token, a password in prose, a connection string or an
      AWS key format not on the list passes straight through.
    - It is applied in the **conversation** path. Plain `awiki ingest <file>` and URL ingest
      copy the source into `raw/` **without** this redaction - an ingested `.env` or config
      dump is archived verbatim.
    - Treat it as defence-in-depth, not a control you can rely on for regulated data.

## The auto-context hook and the debug log

The `awiki context` hook (wired into Claude's `UserPromptSubmit`) receives **every prompt you
type**, extracts keywords with YAKE and searches the vault. Its normal output is a tiny block
of page *pointers* - no page bodies are injected. It is silent-fail by design and never blocks
a prompt. Two things to note:

- **Prompt logging.** With `AWIKI_CONTEXT_DEBUG` enabled, the hook writes a JSONL trace to
  `~/.cache/agent-wiki/context.log` / `context.debug.log` containing the **first 200 chars of
  each prompt** and the rendered block. This is local-only and off by default, but it is a
  plain-text record of your prompts on disk if you turn it on. (A separate non-debug
  `context.log` records only error diagnostics.)
- **Injected pointers are agent-controlled context.** The block is a comment plus page titles
  and paths pulled from the vault. Since vault content can come from ingested web pages, a
  maliciously crafted ingested page *could* place attacker-chosen text into a page title that
  later surfaces in the hook block. The blast radius is small (titles, capped at 5 pointers,
  no bodies), but it is the one indirect prompt-injection surface worth flagging.

## Server-side findings (only relevant once you `awiki serve`)

The vault is local-only until you run `awiki serve`. The server is sensibly scoped -
loopback bind by default, bearer tokens stored only as SHA-256 hashes in
`~/.config/agent-wiki/server.yaml` (never in the vault), reader/writer/admin roles, and
`doctor`'s destructive `--reconcile-raw` is server-local with no HTTP path. A few points for a
threat model:

- **Path traversal is guarded.** `resolve_in_vault` resolves the joined path and rejects
  anything that escapes the vault root (`..`, absolute paths, escaping symlinks) - see
  [`show.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/show.py). The
  `show` route serves files strictly inside the vault. This is correctly implemented.
- **Token comparison is not constant-time.** `role_for_token` compares the request token's
  hash against stored hashes with a plain `==`
  ([`server_config.py`](https://github.com/TacoTakumi/agent-wiki/blob/main/src/agent_wiki/server_config.py)).
  Because it compares **SHA-256 hashes** rather than the raw secrets, a timing side-channel is
  largely academic - but `secrets.compare_digest` would be the textbook choice. **LOW.**
- **Plain HTTP by design.** `serve` speaks HTTP and expects you to terminate TLS at a reverse
  proxy. If you expose it beyond loopback **without** that proxy, both the bearer token and all
  vault traffic cross the network in clear text. This is documented, but it is the easiest way
  to turn a local tool into an actual leak. **MEDIUM if misconfigured.**
- **`auto_context: false` does not travel over the wire.** A remote vault flagged
  `auto_context: false` server-side is still included by the client's hook (the flag is not in
  the wire contract). Not a leak, but a surprising opt-out gap.
- **No rate-limiting or audit of auth failures.** Fine for a loopback/single-user tool; note it
  if you ever widen exposure.

## Supply chain

- Runtime dependencies are mainstream and pinned by floor: `httpx`, `trafilatura`,
  `pymupdf4llm`, `fastapi`, `uvicorn`, `pyyaml`, `ruamel.yaml`, `yake`, `click`,
  `python-multipart`, plus **`agentsquire`** (the author's own skill-installer library, used
  only to copy bundled `SKILL.md` files into local agent harnesses - no network path in awiki's
  use of it). None are invoked to phone home.
- The repo-local `.agent-wiki/config.yaml` mechanism is **trust-gated**: a checked-in config is
  ignored (with a one-line stderr notice) until you run `awiki vault trust <dir>`, so a hostile
  repo cannot silently repoint your CLI at an attacker's vault or token. Good default.
- `agent-wiki-kb` is installed from PyPI; standard supply-chain caveats for any pip package
  apply (you are trusting the published wheel).

## Recommendations for using it safely

1. **Be deliberate about what you ingest and sync.** The vault is plain text with no
   at-rest encryption. Treat it as you would any shared notes directory: do not ingest `.env`
   files, credential dumps or regulated data you would not want aggregated in one place.
2. **Do not rely on redaction for secrets.** It is a regex best-effort on conversation bundles
   only; file and URL ingest are not redacted. Add your own `redaction.patterns` for
   internal token formats, and review before syncing.
3. **Keep `serve` on loopback, or put TLS in front of it.** Never expose the plain-HTTP server
   beyond `127.0.0.1` without a reverse proxy terminating TLS - otherwise tokens and vault
   contents travel in clear text.
4. **Leave `AWIKI_CONTEXT_DEBUG` off** unless debugging; it writes your prompts to
   `~/.cache/agent-wiki/`.
5. **Trust repo-local vault configs consciously.** `awiki vault trust` is the gate; only trust
   directories whose `.agent-wiki/config.yaml` you have read.
6. **Pin the dependency** and review upgrades, as with any pip-installed tool that reads your
   agent transcripts.

## Bottom line on the original question

> What is the potential for data leaks, and are there deliberate reportings built in?

**There are no deliberate reportings, telemetry or covert egress - none.** Every network call
targets a destination you explicitly configured (a URL you ingest, your own remote vault, your
own local LLM), and the default configuration is fully offline. The genuine data-leak potential
is **not** a hidden channel but the tool doing exactly what it advertises: it deliberately reads
your Claude Code and OpenCode transcripts and concentrates them, plus anything you ingest, into a
**single plain-text vault** that you may then sync or serve. The exposure is therefore governed
by *your* choices - what you ingest, whether you sync the vault, and whether you serve it with
proper TLS - not by anything the code hides. The built-in redaction helps but is best-effort and
partial, so the vault should be treated as sensitive plain text at rest.
