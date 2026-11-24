---
type: investigation
title: Agentic AI and Home Assistant Integration
description: Survey of skills and MCP servers for connecting AI agents to Home Assistant, with security and architecture findings
status: complete
generated:
  by: opencode/qwen3.5-397b-a17b
  at: 2026-11-24
verified:
  at: null
  by: null
tags:
- home-automation
- mcp
- agent-integration
- smart-home
- websocket-api
references:
- https://github.com/homeassistant-ai/skills
- https://github.com/tevonsb/homeassistant-mcp
- https://github.com/voska/hass-mcp
- https://skills.sh/
---

# Agentic AI and Home Assistant Integration

## Overview

This investigation surveyed the landscape of skills and MCP servers for connecting AI agent harnesses (opencode, Claude Code, Cursor) to Home Assistant instances. The goal: full remote agent access to near all aspects of HA — reading states, controlling devices, editing automations, monitoring events in real-time.

## Methods Searched

1. **skills.sh leaderboard** — `npx skills find home assistant`, `npx skills find homeassistant`, `npx skills find smart home`
2. **GitHub MCP server search** — `homeassistant mcp server`, filtered by stars and recency
3. **akit subscription** — attempted `akit add homeassistant-ai/skills`, succeeded despite no `.akit.yaml` in source

## Findings

### Skills (skills.sh ecosystem)

| Skill | Installs | Stars | Source | Capabilities |
|-------|----------|-------|--------|--------------|
| **`homeassistant-ai/skills@home-assistant-best-practices`** | **9.6K** | **1k** | homeassistant-ai/skills | Native HA patterns, safe refactoring, dashboard design, AppDaemon, blueprints, backups |
| `claude-office-skills@Home Assistant Automation` | 5.2K | - | claude-office-skills | Automation creation |
| `balloob/llm-skills@home-assistant` | 267 | 4 | balloob (HA co-founder) | Connection setup, API reference (Python/Node.js) |
| `anotb/homeassistant-skill@homeassistant-skill` | 153 | 7 | anotb | REST/WS workflows, works alongside MCP |
| `bradsjm/hassio-addons@*` (7 skills) | 500-800 each | - | bradsjm | Addon-specific guides |

**Key finding:** `homeassistant-ai/skills` is the only security-audited skill (Gen Agent Trust Hub, Socket, Snyk all pass). It teaches native HA constructs over templates — e.g., `condition: numeric_state` instead of `condition: template` — which HA validates at load time rather than failing silently at runtime.

### MCP Servers (GitHub)

| Server | Stars | Lang | Transports | Notable Capabilities |
|--------|-------|------|------------|---------------------|
| **`tevonsb/homeassistant-mcp`** | **574** | TypeScript | SSE | Add-on/HACS management, automation editing, real-time SSE updates |
| **`voska/hass-mcp`** | **353** | Python | stdio, HTTP | **Lovelace editing** (live updates + backups), history/stats, guided conversations |
| `robbrad/homeassistant-mcp` | 106 | Python | stdio | Basic control |
| `jango-blockchained/advanced-homeassistant-mcp` | 58 | TypeScript (Bun) | stdio, HTTP+WS | **50+ tools**, speech-to-text, Code Mode sandbox |
| `c1pher-cn/ha-mcp-for-xiaozhi` | 287 | Python | - | 小智 AI integration (niche) |
| `hekmon8/Homeassistant-server-mcp` | 48 | JavaScript | stdio | Basic |

**Key finding:** All MCP servers use WebSocket under the hood (`ws://HA:8123/api/websocket`) with long-lived tokens. They expose tools to the LLM while keeping credentials secure in the MCP server process.

### Architecture Patterns

**Three integration methods emerged:**

1. **WebSocket API (primary)** — Persistent connection, real-time `subscribe_events`, `call_service`, `get_states`. Used by all MCP servers.
2. **REST API (fallback)** — Stateless polling, `GET /api/states`, `POST /api/services/...`. Used by skills without MCP.
3. **MCP Server (abstraction layer)** — Agent→MCP→HA, credentials stored once, can add rate limiting/logging.

**Security architectures:**

| Pattern | Token Location | Agent Access | Exposure |
|---------|---------------|--------------|----------|
| Local LAN | MCP server env | Via MCP only | None (firewalled) |
| HA Cloud | MCP server env | Via MCP + TLS tunnel | Nabu Casa encrypted |
| VPN (Tailscale) | MCP server env | Via MCP + VPN | Zero-trust network |
| Direct skill | Skill config | Direct REST/WS | Token in skill config |

## Security Considerations

### MCP Server Advantages

- **Credential isolation** — HA token stored once in MCP env, never exposed to agent
- **Rate limiting** — Can enforce call budgets per session
- **Audit logging** — All agent actions logged at MCP layer
- **Permission scoping** — Can restrict which services/tools are exposed

### Risks Identified

1. **Long-lived tokens** — 10-year validity, full user permissions. Must be stored securely.
2. **No built-in rate limiting** — HA API doesn't throttle; MCP must enforce.
3. **Webhook security** — Webhook URLs are the only secret; if leaked, anyone can trigger.
4. **Direct exposure** — Skills that connect directly put token in agent context.

### Recommended Security Posture

- **MCP server on same LAN** as HA, agent connects to MCP (not HA directly)
- **Home Assistant Cloud** for remote access (encrypted tunnel, no port forwarding)
- **Non-admin user** for agent token, with explicit permissions only
- **Automatic backups** before any write operation (voska does this for Lovelace)

## Capability Comparison

| Capability | REST API | WebSocket | MCP Server |
|------------|----------|-----------|------------|
| Read entity states | ✅ | ✅ | ✅ |
| Control devices | ✅ | ✅ | ✅ |
| Real-time events | ❌ | ✅ | ✅ |
| Edit automations | ⚠️ Manual | ✅ | ✅ (tevonsb) |
| Lovelace editing | ❌ | ✅ | ✅ (voska) |
| History queries | ✅ | ⚠️ Limited | ✅ (voska) |
| Add-on management | ❌ | ✅ | ✅ (tevonsb) |
| Speech/voice | ❌ | ❌ | ✅ (jango) |

## Installation Findings

### akit Subscription

The `homeassistant-ai/skills` repo has no `.akit.yaml` manifest, but akit successfully subscribed anyway:

```bash
uvx --from federated-agent-kits akit add --global homeassistant-ai/skills home-assistant-best-practices
```

Result: 16 files rendered to `/home/felix/.agents/skills/home-assistant-best-practices/`, pinned to commit `166defa`.

**Gap:** akit expects `.akit.yaml` for discovery; skills.sh repos use `SKILL.md` instead. akit falls back to cloning and scanning, but this should be documented.

### MCP Server Setup

Both recommended MCP servers support Docker deployment:

**voska/hass-mcp:**
```bash
docker pull voska/hass-mcp:latest
# Add to opencode.jsonc mcpServers config
```

**tevonsb/homeassistant-mcp:**
```bash
docker compose up -d  # from repo
# Requires .env with HASS_HOST, HASS_TOKEN, HASS_SOCKET_URL
```

## Recommendations

### For Full Remote Agent Access

**Install both:**

1. **MCP Server: `voska/hass-mcp`**
   - Lovelace dashboard editing with live updates
   - Automatic backups before writes
   - History/statistics queries with date ranges
   - HTTP transport for remote access

2. **Skill: `homeassistant-ai/skills@home-assistant-best-practices`**
   - 9.6K installs, security audited
   - Teaches native HA patterns (no templates where helpers exist)
   - Safe refactoring workflow
   - Works alongside MCP — skill guides *what*, MCP executes *how*

### Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   opencode      │────►│  voska/hass-mcp │────►│  Home Assistant  │
│   (agent)       │ MCP │  (Docker, LAN)  │  WS │  (local network) │
└─────────────────┘     └─────────────────┘     └──────────────────┘
        │                       │                       │
        │              HA_TOKEN in env          Long-lived token
        │              (never exposed)          (admin for editing)
        └─────────────────────────────────────────────────────┘
              Skill: home-assistant-best-practices (read-only knowledge)
```

### Why This Combination

| Need | Solution |
|------|----------|
| Real-time control | WebSocket via MCP |
| Dashboard editing | voska Lovelace tools |
| Best practices | homeassistant-ai skill |
| History/stats | voska `get_statistics` |
| Security | MCP holds token, skill is read-only |

## Gaps Identified

1. **No akit-native HA kit** — homeassistant-ai/skills uses skills.sh format, not `.akit.yaml`
2. **No unified MCP standard** — 6+ incompatible MCP servers, no interoperability
3. **Permission scoping** — HA tokens are all-or-nothing; no fine-grained agent permissions
4. **Audit trail** — HA logs actions but doesn't attribute them to "agent" vs "user"

## References

- [homeassistant-ai/skills](https://github.com/homeassistant-ai/skills) — 1k stars, 9.6K installs
- [voska/hass-mcp](https://github.com/voska/hass-mcp) — 353 stars, Lovelace editing
- [tevonsb/homeassistant-mcp](https://github.com/tevonsb/homeassistant-mcp) — 574 stars, add-on mgmt
- [HA WebSocket API](https://developers.home-assistant.io/docs/api/websocket/)
- [HA REST API](https://developers.home-assistant.io/docs/api/rest/)
- [skills.sh leaderboard](https://skills.sh/)

## Related

- [What an MCP server can be, and who can reach one](mcp_server_entry_points_and_transports.md)
- [skills.sh: repository layout and telemetry](skills_sh_repository_layout_and_telemetry.md)
- [Agent-integration layer and multi-vault interaction](agent_integration_layer_and_multi_vault_interaction_for_an_okf_conformant_pkb.md)
