---
type: Finding
title: opencode writes its session transcripts into the Claude config directory
description: The oh-my-openagent plugin stores transcripts and todos under ~/.claude, so that directory
  fills up on a machine where Claude Code has never run.
tags:
- finding
- opencode
- oh-my-openagent
status: stable
stale_after: '2027-03-28'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-28T00:00:00Z'
---
A machine that has never run anything from Anthropic still accumulates hundreds of files in
`~/.claude/transcripts`, one per session, named `ses_<id>.jsonl`. They are opencode sessions.
The oh-my-openagent plugin resolves its own storage against the Claude config directory:

```js
var TRANSCRIPT_DIR = join75(getClaudeConfigDir(), "transcripts");
function getClaudeConfigDir() {
  const envConfigDir = process.env.CLAUDE_CONFIG_DIR;
  if (envConfigDir) return envConfigDir;
  return join28(homedir14(), ".claude");
}
```

The same constant appears again in the plugin's `session-manager` tools, alongside a sibling
`todos/` directory, so the tools that list and search sessions read back from the same place.

Telling the two apart takes one look at the filenames. opencode names a session
`ses_f4b95fe3bffeZm7KqJHiiNpxtH`; Claude Code uses a UUID, and files it under
`~/.claude/projects/<slugified-cwd>/` rather than a flat directory. A `~/.claude` holding
`transcripts/` and no `projects/` was written entirely by opencode.

`CLAUDE_CONFIG_DIR` moves all of it, since the plugin reads that variable before falling back to
the home directory. That is the whole fix, with one consequence worth knowing in advance: it
moves the todos and the session history together, and any real Claude Code install on the same
machine follows it too.

## Why it surfaced

The transcripts are worth finding because `session_search` will not find them for you. It scans
`MAX_SESSIONS_TO_SCAN = 50` sessions and stops, so on a machine with 489 transcripts it covers
about the last fortnight. A session from ten days earlier is absent from the results whilst its
file sits on disk, and the search reports no matches rather than reporting a truncated scan.

`rg` over `~/.claude/transcripts` answers the same question against every session, which is the
workaround for any search that has to reach further back than the cap.

Observed with opencode 1.18.32 and oh-my-openagent 4.19.4.
