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

`visible = true` and `hide_dotfiles = false` are not the same setting. The first keeps the files
in the filter and renders them dimmed, so `H` still toggles them away; the second takes them out
of filtering altogether.

## Evidence

`setup()` validates nothing, so the misplaced key produces no error and no warning, which is what
makes this cost an afternoon rather than a minute. Read the resolved state back instead:

```bash
nvim --headless -c "lua print(require('neo-tree.sources.manager').get_state('filesystem').filtered_items.hide_dotfiles)" -c qa
```

With the option written as `filesystem.hide_hidden = false` this still reported `true`. That is
the general shape of it: a plugin that merges user options into its defaults will carry an
unknown key along quietly, and the only thing that settles whether a setting arrived is reading
it back out of the running plugin.
