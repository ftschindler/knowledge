---
type: Finding
title: An MCP server without tool annotations looks destructive to every client
description: Tool annotations are optional and their absence defaults to the worst case, so a
  server that leaves them out presents every query tool as one that may overwrite or delete.
tags:
- finding
- mcp
- agent-tooling
status: draft
stale_after: '2027-05-18'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-18T14:30:00+01:00'
sources:
- id: mcp-schema
  resource: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-06-18/schema.ts
  title: 'Model Context Protocol schema, 2025-06-18: ToolAnnotations'
  last_modified: '2026-11-18'
---
A server's `tools/list` came back with tools that had a name, a description and an input
schema, and nothing else. Every one of them only queried a database, but nothing in the
response said so.

This is a reading of the specification rather than a client caught misbehaving: no client was
watched treating the tools differently.

## How to check

`tools/list` over HTTP, printing each tool's hints:

```sh
curl -sS -X POST "$MCP_URL" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' |
python -c 'import json,sys
for t in json.load(sys.stdin)["result"]["tools"]:
    print(t["name"], t.get("annotations"))'
```

`None` on every line is the symptom.

## What it means

Since the 2025-03-26 revision a tool may carry four hints, all optional, and the schema gives
each a default for when it is absent[^mcp-schema]:

| Hint | Says | Default when absent |
| --- | --- | --- |
| `readOnlyHint` | the tool does not modify its environment | `false` |
| `destructiveHint` | if it modifies, it may overwrite or delete | `true` |
| `idempotentHint` | calling it twice has no further effect | `false` |
| `openWorldHint` | it reaches entities outside the server | `true` |

Every default is the cautious one. A tool with no annotations therefore claims to be a
non-idempotent, destructive write that reaches the outside world. A client that auto-approves
read-only tools has to ask about every query, and a client that warns about destructive ones
has to warn about all of them, so the one tool that does have a side effect looks no different
from the rest.

## How to get past it

On the server, declare the hints. In FastMCP that is one argument per tool:

```python
from mcp.types import ToolAnnotations

READ_ONLY = ToolAnnotations(readOnlyHint=True, openWorldHint=False)

@app.tool(name="SPARQL_Query", annotations=READ_ONLY)
def sparql_query(query: str) -> str: ...
```

`openWorldHint` stays `true` for a tool that leaves the server even when it only reads, such as
one that resolves a DOI. A tool that sends mail or files a ticket is `readOnlyHint=False`, and
`destructiveHint=False` if it only adds.

On the client the hints change nothing about trust. The schema calls them hints and says a
client should not rely on them from a server it does not trust, so a client's own allow and
deny list stays the control; the hints only make a trustworthy server describe itself
accurately.
