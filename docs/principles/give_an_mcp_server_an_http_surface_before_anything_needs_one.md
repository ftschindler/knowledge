---
type: Principle
title: Give an MCP server an HTTP surface before anything needs one
description: Speak streamable HTTP from the first version, because the consumer that cannot launch a
  subprocess turns every later move into a rewrite rather than a deployment.
tags:
- principle
- mcp
- ai-agents
- agents
- architecture
status: draft
generated:
  by: opencode/claude-opus-5
  at: '2026-10-14T12:00:00Z'
---
**Claim.** Build an MCP server to speak streamable HTTP from its first version, even whilst the
only thing calling it is a harness on the same machine that would be happy with stdio.

**Why.** A stdio server is a subprocess its client launches, so it can only be reached by a
consumer that runs on a machine you control and may fork children. A build container, a hosted
assistant and a colleague's laptop are all outside that. The moment one of them wants the
capability, a stdio-only server has to grow an endpoint, an identity it never had and a
concept of which user a call acts as, which is a rewrite dressed as a configuration change.
Binding the same handlers to an HTTP listener whilst the server is small costs a dependency and
an afternoon, and it converts every later move into a deployment question.

**Keep stdio as well.** This is not a choice between the two. Local development stays faster
over stdio, an inspector attaches to it more easily, and a harness on the same machine has no
reason to pay for HTTP. Ship both bindings over one set of handlers and let the consumer pick.

**The authorisation work is the part worth starting early**, and it is the part a local server
never forces. Running as the logged-in user means reading their environment and acting as them,
which is an answer you get for free and lose the moment the process moves. Writing the server
so a caller's identity arrives as an argument rather than as ambient state keeps that answer
replaceable.

**What this is not.** It is not an argument for hosting the server. Where it runs is a separate
decision with its own costs, and most servers should stay on the machine that needs them. This
principle only says that the decision should remain open.

The survey this rests on is
[What an MCP server can be, and who can reach one](../investigations/mcp_server_entry_points_and_transports.md).
