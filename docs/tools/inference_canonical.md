---
type: Tool
title: Inference Manager (Canonical)
description: Canonical's CLI and local proxy over its inference snaps, the one-snap-per-model packages
  that pick a hardware-specific engine and serve an OpenAI-compatible API on localhost.
tags:
- tools
- inference
- local-llm
- snap
- ubuntu
- openai-api
status: draft
stale_after: '2027-02-16'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-16T00:00:00Z'
sources:
- id: inference-repo
  resource: https://github.com/canonical/inference
  title: 'canonical/inference: Inference Manager'
  last_modified: '2026-11-16'
- id: inference-snaps-repo
  resource: https://github.com/canonical/inference-snaps
  title: 'canonical/inference-snaps: install, run, and serve AI models as snaps'
  last_modified: '2026-11-16'
- id: snaps-reference
  resource: https://documentation.ubuntu.com/inference-snaps/reference/snaps/
  title: 'Inference Snaps documentation: Available snaps'
  last_modified: '2026-11-16'
- id: opencode-howto
  resource: https://documentation.ubuntu.com/inference-snaps/how-to/integration/opencode/
  title: 'Inference Snaps documentation: Use inference snaps in OpenCode'
  last_modified: '2026-11-16'
- id: announcement
  resource: https://canonical.com/blog/canonical-releases-inference-snaps
  title: 'Canonical: Introducing silicon-optimized inference snaps'
  last_modified: '2025-10-23'
- id: cfg-test
  resource: https://computingforgeeks.com/ubuntu-inference-snaps/
  title: 'ComputingForGeeks: Ubuntu Inference Snaps Tested: Gemma 4 vs Ollama'
  last_modified: '2026-11-11'
---
The Inference Manager[^inference-repo] is one command and one local endpoint in front of
Canonical's inference snaps. The two are easy to conflate: the **inference snaps** are the
models, one snap each, and the **Inference Manager** is the `inference` snap that finds,
installs and routes to them. This page is written from the documentation; nothing here has
been run on my machines yet.

| | |
| --- | --- |
| Author | Canonical |
| Licence | GPL-3.0 for the manager; each model snap carries its model's own licence |
| Language | Go |
| Distribution | The Snap Store, as `sudo snap install inference` |
| Source | [github.com/canonical/inference](https://github.com/canonical/inference) |
| Version read | 1.0.1, from the README and the store listing |

## What it is

Inference snaps arrived as a public beta in October 2025[^announcement]. A model snap bundles
several weight files and several engines, detects the hardware at install time, and selects
the pair it judges best: a generic CPU build, Intel OpenVINO, CUDA, ROCm, Vulkan, or a vendor
NPU, depending on the model[^snaps-reference]. Each snap then serves an OpenAI-compatible API
on a port of its own and runs offline once installed[^inference-snaps-repo]. The catalogue
holds about twenty models, from Gemma, Qwen, Nemotron and DeepSeek R1 to an embedding model
and two decision models.

The manager adds the layer above that:

| | |
| --- | --- |
| `inference find <term>` | Search the available providers and their capabilities |
| `inference install <snap>` | Install a model snap |
| `inference models` | List the models reachable through the proxy |
| `inference info <snap>` | Show a snap's endpoints, and which engine can run which model size |
| Proxy | One OpenAI-compatible endpoint, `http://127.0.0.1:8400/v1`, routing to whichever snaps are running |

`inference info` is the useful one for understanding what a snap actually contains. For
`gemma4` it lists the proxy and the snap's own upstream port, then an engine-by-size grid:

```text
API: http://127.0.0.1:8400/v1 (proxy)
     └── http://localhost:8336/v1 (upstream)

ENGINE         gemma4-e2b  gemma4-e4b  gemma4-12b  gemma4-26b-a4b
amd-gpu        ✓           ✓           ✓           ✓
cpu            ✓           ✓           ✓           ✓
intel-cpu                  ✓
nvidia-gpu     ✓           ✓           ✓           ✓
```

A model's licence does not follow the manager's. Most snaps ship Apache-2.0 or MIT weights,
but not all: OpenJev, one of the decision models, is CC BY-NC 4.0, so check the snap's
store page before using one for work.

## Why it matters here

The point is a single stable endpoint for local models, which [opencode](opencode.md) could
take as a provider. Canonical document doing that per snap, as an `openai` provider whose
`baseURL` is the snap's endpoint and whose model name comes from `<snap> status`
[^opencode-howto]. Pointing the provider at the manager's proxy instead would make it one
provider for every local model, and that would fit my one-directory-per-provider layout as
a profile of its own; that is untested.

## Reported by others

Not observed here, and kept short on purpose. One CPU-only test on Ubuntu 26.04 in November
2026 reported[^cfg-test]:

- even the stable channel carried a `2.0.0-beta` model snap
- engine auto-selection did not always pick the fastest engine
- the Nemotron 3 Nano snap installed its 30B model on a 6 GB machine, ignoring a pinned 4B variant
