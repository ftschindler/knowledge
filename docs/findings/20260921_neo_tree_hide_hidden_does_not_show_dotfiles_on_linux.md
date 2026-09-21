---
type: Finding
title: neo-tree's hide_hidden does not show dotfiles on Linux
description: hide_hidden is a Windows-only option and belongs under filtered_items, so setting it
  on filesystem is accepted in silence and changes nothing.
tags:
- finding
- neovim
- neo-tree
- config-management
status: stable
stale_after: '2027-03-21'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-21T00:00:00Z'
---
Dotfiles stay hidden in neo-tree because `hide_hidden` is two things wrong at once: it refers to
the NTFS hidden attribute and so does nothing on Linux, and it lives under
`filesystem.filtered_items` rather than on `filesystem`, where an unrecognised key is accepted
without complaint. On Linux the keys that matter are `hide_dotfiles` and `hide_gitignored`:

```lua
require('neo-tree').setup {
  filesystem = {
    filtered_items = {
      visible = true,
      hide_dotfiles = false,
      hide_gitignored = false,
    },
  },
}
```
