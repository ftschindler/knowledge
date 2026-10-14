---
type: Investigation
title: What an MCP server can be, and who can reach one
description: The two standard transports, the five shapes a server takes, and the six places a call
  can come from, read against the two variables that decide which of them are available.
tags:
- ai-agents
- agents
- mcp
- tooling
- architecture
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T12:00:00Z'
stale_after: '2027-04-30'
sources:
- id: mcp-transports
  resource: https://modelcontextprotocol.io/specification/2026-07-28/basic/transports
  title: 'Model Context Protocol: Transports'
  last_modified: '2026-10-14'
- id: mcp-architecture
  resource: https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
  title: 'Model Context Protocol: Architecture'
  last_modified: '2026-10-14'
- id: mcp-server-concepts
  resource: https://modelcontextprotocol.io/docs/2026-07-28/learn/server-concepts
  title: 'Model Context Protocol: Server concepts'
  last_modified: '2026-10-14'
- id: mcp-authorization
  resource: https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
  title: 'Model Context Protocol: Authorization'
  last_modified: '2026-10-14'
---
**Context** - the word "server" suggests something running somewhere, with a port and an
uptime. Most MCP servers are not that. The question was what an MCP server actually is as an
artefact, and which consumers can reach one, before committing to where any particular one
should live.

- **Read on**: 2026-10-14
- **Method**: the specification read directly at revision 2026-07-28; the entry points
  enumerated from the harnesses in use here and from the hosted products that consume MCP;
  [markitdown](../tools/markitdown.md) read as the worked example of a server that is also a
  command.

The survey stops short of recommending a transport for any particular server. What it does
settle is which question decides that, and the answer is not a technical preference.

## A server is a program, not a service

The specification defines two standard transports, and calls a transport a binding: it decides
how messages are framed and delivered, not what they mean[^mcp-transports].

**stdio is a subprocess the client launches**, speaking newline-delimited JSON-RPC over its
standard streams[^mcp-transports]. No port, no daemon, no network. It starts when the harness
starts and dies with it. This is most of what exists today.

**Streamable HTTP is an endpoint**, where each message is a POST and the reply arrives as JSON
or as a stream scoped to that request[^mcp-transports]. The hosted servers are this, and so is
anything that has to be reached from a machine that is not yours.

So a stdio server's configuration is a command line:

```json
{ "command": "uvx", "args": ["markitdown-mcp"] }
```

That is not a service you run. It is a program the harness launches on demand, exactly like a
command-line tool, because it is one. It happens to write JSON-RPC on stdout instead of text a
person reads.

## What the protocol adds over a command line

[markitdown](../tools/markitdown.md) ships both ways, which makes the comparison concrete.
`markitdown report.pdf` and `convert_to_markdown(uri=...)` do the same work.

Three things change in the wrapping.

**The model is told the tool exists.** It asks for the server's tool list and gets names,
descriptions and JSON schemas back[^mcp-server-concepts]. With a command, somebody has to have
put `--help` into the context, or the model guesses the flags.

**The call and the result are typed.** Arguments are a validated object rather than a string
to shell-quote, and the result comes back structured rather than as stdout to pattern-match.

**The process stays alive between calls.** State lives for as long as the process does, so a
server can hold an open browser, a warm database connection or a loaded index. A command pays
its startup cost every invocation.

The cost is a configuration entry, a process to supervise, and a tool definition occupying
context on every turn whether it gets used or not.

## Five shapes, from a script to a tenancy

The category is much wider than "wrapper around an API", and the shapes have little in common
beyond the protocol.

- **A pure function**, holding nothing: a converter, a formatter, a unit calculation. Honestly
  close to a command with a schema bolted on.
- **Scoped access to a local resource**: a filesystem, a SQLite file, a git repository. The
  value over a shell is that the server decides which paths are reachable.
- **A stateful machine**: a browser, a REPL, a long-lived kernel. The surviving process is the
  whole point, and a command cannot do this at all.
- **A facade over a remote API**: an issue tracker, a chat platform. It holds the credential so
  the model never sees it.
- **A provider of readable material rather than callable tools.** The protocol carries
  resources and prompt templates alongside tools[^mcp-server-concepts], and almost nobody uses
  them. The most interesting unexplored corner.

## Six places a call comes from

A harness with MCP enabled is the obvious consumer and about one sixth of the picture.

| Entry point | Example | Can spawn a subprocess? | Credential comes from |
| --- | --- | --- | --- |
| Interactive coding harness | opencode, VS Code, Cursor | Yes | your environment |
| Desktop chat application | Claude Desktop | Yes | your environment |
| Headless agent on someone's CI | a coding agent in a build container | In principle, but unattended | a provisioned secret |
| Hosted web product | a connector in a browser-based assistant | No | OAuth, per user |
| Your own code as the client | an SDK in a script or an application | Your choice | your choice |
| A person, by hand | an inspector or a test harness | Yes | yours |

The last row is worth keeping in view. A human calling the tool list and then a tool proves the
protocol does not require a model to be present, which is the cheapest way to test a server.

The desktop chat application is separated from the coding harness deliberately. It has the same
power to launch a subprocess and no repository, no working directory and no project
conventions, so anything assuming "there is a project here" breaks on it.

## Two variables decide which of those are available

Every row above is a position on two axes, and neither is about the protocol.

**Who launches the process.** A consumer running on a machine you control, with permission to
fork children, can use stdio. One that is not cannot, and needs the server to already exist
somewhere as an endpoint.

**Who holds the credential.** A local stdio server reads your environment variables and your
configuration files, because it runs as you. A remote server has no "you" to borrow from, so it
needs its own authorisation story, which the specification builds on OAuth[^mcp-authorization].

Those two make three tiers rather than two, and the middle one is easy to miss. A build
container and a hosted web product are both "not my machine", but the container can carry a
secret handed to it in advance whilst the web product needs a user to complete an interactive
flow. Designing for "local or remote" puts those two in one bucket and they do not behave
alike.

## Two shapes that sit outside the grid

**The gateway** is an MCP server to its clients and an MCP client to many servers upstream. It
fronts twenty of them as one endpoint, and adds authorisation, auditing, rate limits and tool
filtering on the way through. This is why client and server are roles held per connection
rather than properties of a program[^mcp-architecture].

**An agent exposed as a server** lets another agent call it as a tool. That is composition
rather than capability, and it is the point at which "what is a tool" and "what is an agent"
stop being answerable separately.

## Bottom line

**An MCP server is a calling convention for handing a model a capability**, uniform across
everything from a forty-line script to a multi-tenant service. Asking whether something "could
just be a command-line tool" usually has the answer that it already is one, and the protocol is
the adapter that makes it legible to a model rather than to a person at a prompt.

Which transport a given server speaks is therefore decided by its furthest intended consumer
rather than by its own convenience, and that choice is expensive to revisit:
[give an MCP server an HTTP surface before anything needs one](../principles/give_an_mcp_server_an_http_surface_before_anything_needs_one.md).
