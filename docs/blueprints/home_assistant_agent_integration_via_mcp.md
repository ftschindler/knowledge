---
type: blueprint
title: Home Assistant Agent Integration via MCP
description: Full remote agent access to Home Assistant through MCP server and best-practices skill, without oh-my-openagent
status: implemented
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
- blueprint
references:
- ../investigations/agentic_ai_homeassistant_integration.md
- https://github.com/voska/hass-mcp
- https://github.com/homeassistant-ai/skills
---

# Home Assistant Agent Integration via MCP

## Overview

This blueprint delivers **full remote agent access** to a Home Assistant instance through two components:

1. **MCP Server** (`voska/hass-mcp`) — Real-time WebSocket connection for device control, Lovelace editing, history queries
2. **Best-Practices Skill** (`homeassistant-ai/skills`) — Read-only knowledge that prevents anti-patterns (native HA constructs over templates)

**What the agent can do:**
- Read all entity states in real-time
- Control lights, locks, climate, media, covers, fans, switches
- Edit Lovelace dashboards with live preview + automatic backups
- Query historical data and statistics
- List and trigger automations
- All via secure MCP layer (token never exposed to agent)

**What this blueprint does NOT require:**
- oh-my-openagent plugin (not used here)
- Docker (runs via `uvx` directly)
- Root access (fully rootless)
- Public internet exposure (local LAN only)

## Prerequisites

| Requirement | Why | How to verify |
|-------------|-----|---------------|
| Home Assistant instance (2024.x+) | MCP server connects via WebSocket API | `https://your-ha.local:8123` reachable |
| Long-lived access token | Authentication for MCP→HA connection | Profile → Security → Create token |
| opencode with MCP support | Loads MCP servers from config | `opencode --version` ≥ 2.x |
| `uv` package manager | Runs `hass-mcp` without Docker | `uv --version` |
| Local network access | HA must be reachable from opencode machine | `curl http://ha.local:8123/api/` |

### Create Long-Lived Access Token

1. Open Home Assistant UI
2. Click your user profile (bottom left)
3. Go to **Security** tab
4. Click **Create Long-Lived Access Token**
5. Name it `opencode-agent` (or similar)
6. Copy the token (starts with `eyJ...`)
7. Store securely — valid for 10 years, full user permissions

## Installation

### Step 1: Install the Skill (already done)

The best-practices skill is already installed via akit:

```bash
# Already executed:
# uvx --from federated-agent-kits akit add --global homeassistant-ai/skills home-assistant-best-practices
```

**Location:** `/home/felix/.agents/skills/home-assistant-best-practices/` (16 files)

**What it does:** Teaches native HA patterns — e.g., use `condition: numeric_state` instead of `condition: template`, which HA validates at load time rather than failing silently at runtime.

### Step 2: Configure MCP Server

**Config file:** `~/.config/opencode/opencode.jsonc`

The MCP entry has been added:

```jsonc
"hass-mcp": {
  "type": "local",
  "command": ["uvx", "hass-mcp@latest"],
  "env": {
    "HA_URL": "{file:.env.hass_mcp_voska}",
    "HA_TOKEN": "{file:.env.hass_mcp_voska}"
  },
  "enabled": true
}
```

**Env file:** `~/.config/opencode/.env.hass_mcp_voska`

```bash
HA_URL=http://homeassistant.local:8123
HA_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your_token_here
```

**Action required:** Fill in your actual `HA_URL` and `HA_TOKEN` in the env file.

### Step 3: Restart opencode

```bash
# Quit opencode if running
# Then restart:
opencode
```

The MCP server starts automatically on first agent request that needs HA access.

## Configuration Details

### Network Considerations

**Local LAN (this blueprint):**
- `HA_URL` = `http://homeassistant.local:8123` or `http://192.168.x.x:8123`
- opencode machine must be on same network as HA
- No firewall changes needed
- Token transmitted unencrypted (LAN only)

**Remote via Home Assistant Cloud:**
- `HA_URL` = `https://your-url.nabu.casa`
- Requires HA Cloud subscription (~$5/month)
- Encrypted tunnel, no port forwarding
- Same config, just different URL

**Remote via VPN (Tailscale/ZeroTier):**
- `HA_URL` = `http://100.x.y.z:8123` (Tailscale IP)
- VPN must be active on opencode machine
- Encrypted, no public exposure

### Security Model

| Layer | Protection |
|-------|------------|
| **Token storage** | `.env.hass_mcp_voska` (mode 600, gitignored) |
| **Token exposure** | Never sent to agent — MCP holds it |
| **Network** | Local LAN only (unless HA Cloud/VPN) |
| **Rate limiting** | None built-in — agent self-limits |
| **Permissions** | Full user permissions — use non-admin user if concerned |
| **Audit trail** | HA logs all actions, attributed to token owner |

### File Permissions

```bash
chmod 600 ~/.config/opencode/.env.hass_mcp_voska
```

The env file is already set to mode 600 (owner read/write only).

## Capabilities

### What the Agent Can Do

| Capability | Tool | Example |
|------------|------|---------|
| **Read entity state** | `get_entity` | "What's the temperature in the living room?" |
| **List entities** | `list_entities` | "Show me all lights in the bedroom" |
| **Control devices** | `entity_action` | "Turn off all kitchen lights" |
| **Call any service** | `call_service_tool` | "Activate the 'Movie Night' scene" |
| **Edit Lovelace** | `add_card`, `update_card`, etc. | "Add a temperature card to the dashboard" |
| **Query history** | `get_history`, `get_statistics` | "Show me energy usage last week" |
| **List automations** | `list_automations` | "What automations run at sunset?" |
| **Trigger automation** | `call_service_tool` | "Run the 'Good Morning' automation" |

### Lovelace Dashboard Editing

The voska MCP server supports **live Lovelace editing**:

- `list_dashboards` — List all dashboards (storage mode only)
- `get_dashboard_config` — Get full dashboard config
- `add_card` / `update_card` / `remove_card` / `move_card` — Edit cards
- `list_view_sections` — List sections in a "sections"-type view
- `add_view` / `remove_view` / `update_view` — Edit views

**Automatic backups:** Before every write, the current config is saved to `~/.hass-mcp/dashboard-backups/`. Can restore via `restore_dashboard`.

**Important:** Only works with **storage-mode** dashboards (UI-managed). YAML-mode dashboards must be edited directly.

## Testing

### First Commands to Verify Connection

After filling in the env file and restarting opencode, try these:

1. **Basic connectivity:**
   ```
   What's the current state of the sun entity?
   ```
   Expected: Returns `above_horizon` or `below_horizon`

2. **List entities:**
   ```
   List all lights in my home
   ```
   Expected: List of `light.*` entities with states

3. **Read a sensor:**
   ```
   What's the temperature in the living room?
   ```
   Expected: Current temperature from your sensor

4. **Control a device:**
   ```
   Turn on the hallway light at 50% brightness
   ```
   Expected: Light turns on, agent confirms

5. **Query history:**
   ```
   Show me the living room temperature over the last 24 hours
   ```
   Expected: Historical data points

### Troubleshooting Connection

**"Connection refused" or "Cannot connect to HA":**
- Verify `HA_URL` is correct and reachable: `curl http://your-ha:8123/api/`
- Check HA is running: `systemctl status home-assistant@homeassistant` (if systemd)
- Ensure opencode machine is on same network

**"Invalid token" or "Unauthorized":**
- Re-create the long-lived token in HA
- Ensure no trailing whitespace in `.env.hass_mcp_voska`
- Token must be for an existing HA user

**"No Lovelace dashboards found":**
- Only **storage-mode** dashboards are editable
- YAML-mode dashboards must be edited directly
- Check: HA → Settings → Dashboards → see which are "Storage" vs "YAML"

**MCP server not starting:**
- Check opencode logs for MCP startup errors
- Verify `uv` is installed: `uv --version`
- Test manually: `uvx hass-mcp --help`

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│   opencode      │────►│  voska/hass-mcp │────►│  Home Assistant  │
│   (agent)       │ MCP │  (uvx process)  │  WS │  (local network) │
└─────────────────┘     └─────────────────┘     └──────────────────┘
        │                       │                       │
        │              HA_TOKEN in .env         Long-lived token
        │              (mode 600, never          (full user perms)
        │               exposed to agent)
        │
        └─ home-assistant-best-practices skill (read-only knowledge)
           /home/felix/.agents/skills/home-assistant-best-practices/
```

**Key properties:**
- MCP server runs as local process (no Docker)
- Token stored in env file, read by MCP only
- Agent never sees token — calls MCP tools
- Skill guides *what* to write, MCP executes *how*

## Maintenance

### Updating the MCP Server

```bash
# MCP server updates automatically via @latest in config
# To force update, clear uv cache:
uv cache clean
```

### Updating the Skill

```bash
# Skill is pinned by akit to commit 166defa
# To update:
uvx --from federated-agent-kits akit update --global home-assistant-best-practices
```

### Rotating the Token

If the token is compromised:

1. Revoke old token: HA → Profile → Security → Revoke
2. Create new token
3. Update `.env.hass_mcp_voska`
4. Restart opencode

### Backups

**Lovelace backups:** Automatic, stored in `~/.hass-mcp/dashboard-backups/`

**HA instance backups:** Use HA's built-in backup system (Settings → System → Backups)

**Config backups:** The `.env.hass_mcp_voska` file is your responsibility — back it up securely.

## Related

- [Investigation: Agentic AI and Home Assistant Integration](../investigations/agentic_ai_homeassistant_integration.md) — full survey of skills and MCP servers
- [What an MCP server can be, and who can reach one](../investigations/mcp_server_entry_points_and_transports.md) — MCP architecture patterns
- [voska/hass-mcp documentation](https://github.com/voska/hass-mcp) — upstream MCP server docs
- [homeassistant-ai/skills](https://github.com/homeassistant-ai/skills) — best-practices skill source

## Changelog

- **2026-11-24** — Initial blueprint, based on investigation findings
  - Skill installed via akit (16 files rendered)
  - MCP config added to `opencode.jsonc`
  - Env file template created (`.env.hass_mcp_voska`)
  - Awaiting user to fill in actual HA_URL and HA_TOKEN
