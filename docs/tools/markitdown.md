---
type: Tool
title: markitdown
description: Microsoft's converter from PDF, Office documents and other binary formats into Markdown,
  shipped both as a CLI and as an MCP server an agent can call.
tags:
- tools
- markitdown
- markdown
- agents
- python
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-18T00:00:00Z'
sources:
- id: markitdown-repo
  resource: https://github.com/microsoft/markitdown
  title: 'microsoft/markitdown: Python tool for converting files and office documents to Markdown'
  last_modified: '2026-09-18'
---
markitdown[^markitdown-repo] converts the formats a knowledge base keeps arriving in, and that
a text-only agent cannot read, into Markdown: PDF, DOCX, PPTX, XLSX, HTML, images, audio, ZIP,
EPub, and a YouTube URL. It is Microsoft's, and it exists in two shapes that are easy to
conflate, a command and an MCP server.

| | |
| --- | --- |
| Author | Microsoft |
| Licence | MIT |
| Language | Python |
| Distribution | PyPI, as `markitdown` for the CLI and `markitdown-mcp` for the server; both run without installing through [uv](uv.md)'s `uvx` |
| Source | [github.com/microsoft/markitdown](https://github.com/microsoft/markitdown) |
| Versions read | `markitdown` 0.1.7, `markitdown-mcp` 0.0.1a7 |

## What it is

The conversion target is explicitly Markdown *for an LLM to read*, not Markdown that
reproduces the source. Structure that carries meaning survives, so a DOCX heading becomes a
heading, a bullet list a bullet list, and a table a pipe table. Presentation does not survive,
and is not meant to.

The two packages differ only in how they are driven:

| | |
| --- | --- |
| `markitdown <file>` | Writes Markdown to standard output. Nothing to configure |
| `markitdown-mcp` | An MCP server over stdio, exposing exactly one tool, `convert_to_markdown(uri)`, taking a `file:`, `http:` or `data:` URI |

The single-tool surface is the reason the server is cheap to leave enabled: it adds one tool
schema to a session, and it handles remote URIs, which the CLI on its own does not.

## The extra that does not exist

The optional dependencies are declared on `markitdown`, where `markitdown[all]` pulls in the
converters for the heavier formats. **`markitdown-mcp` declares no extras at all**, and asking
for `markitdown-mcp[all]` is therefore a no-op that pip reports as a warning rather than an
error, which is the sort of instruction that looks obeyed and is not.

It is also unnecessary. `markitdown-mcp` 0.0.1a7 depends on `markitdown[all]<0.2.0,>=0.1.1`
outright, so the server always has the full converter set. That is visible before installing
anything, in the package metadata:

```bash
curl -s https://pypi.org/pypi/markitdown-mcp/json | python3 -c \
  "import json,sys; print(json.load(sys.stdin)['info']['requires_dist'])"
```

The cost of that dependency is worth knowing before wiring it into a tool that starts on
demand: the full set resolves to 74 packages, including onnxruntime, pandas and lxml. Through
`uvx` they are fetched once and cached, so the first invocation is slow and later ones are not,
and a wiped cache makes the next start slow again rather than broken.

## Why it matters here

An agent that cannot read a PDF cannot file what is in one, and this bundle is written by
agents. Declaring it as an MCP server rather than leaving it to the shell means the capability
is present without anyone remembering the command, which matters for exactly the tool you reach
for twice a month.

It is declared in the base layer of [my opencode configuration](opencode.md), because which
model is answering has no bearing on how a DOCX is parsed. That is the general shape:
[a profile merges over the base config rather than replacing it](../findings/20260918_opencode_merges_a_profile_over_the_base_config_rather_than_replacing_it.md),
so a provider-agnostic tool is written once rather than copied into every profile and kept in
sync by hand.
