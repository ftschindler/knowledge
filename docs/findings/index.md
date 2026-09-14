# Findings

Things that cost time once. Each records the symptom, what it turned out to be, and how to get
past it, so the next encounter is short.

A finding is the cheapest page here to write, and deliberately so. It does not have to be
general, it does not have to connect to anything, and it is not asked to earn its place the way
a [principle](../index.md#principles) is: it only has to be true, and to have cost someone an
afternoon. Where a finding does turn out to carry a reusable claim, the claim moves to a
principle and the finding links to it rather than restating it, per
[Give every cross-cutting concept one definitional home](../principles/give_every_cross_cutting_concept_one_definitional_home.md).

Two conventions follow from that. A finding names the **symptom** in its title, in the words
you would have searched for, because that is how anyone arrives here. And it carries
`stale_after`, because a finding about a tool is a claim about a version: when the bug is fixed
or the default changes, the page is wrong rather than merely old, and the date is what turns
"is this still true?" into something a linter can ask.

For the same reason the filename leads with the date it was found, `20260911_`, and this
directory is listed newest first, grouped by year and month. A principle is read for what it
claims and its age is beside the point; a finding is read for what was true of some version of
something, so when it was written is part of the claim. Newest first because the recent ones
are the ones still likely to hold.

The domain lives in the tags, not in a directory, per
[Split orthogonal classification axes across folders and tags](../knowledge_management/split_orthogonal_classification_axes_across_folders_and_tags.md).

## 2026

### September

- 2026-09-11: [Dependabot declines transitive security updates in uv.lock](20260911_dependabot_declines_transitive_security_updates_in_uv_lock.md) - an error naming a version conflict that does not exist, and the two settings that actually caused it

### August

- 2026-08-27: [fs.protected_regular blocks root writes in sticky tmp](20260827_fsprotected_regular_blocks_root_writes_in_sticky_tmp.md) - a root process denied a write to a world-writable file, and the sysctl that explains it
- 2026-08-27: [awiki tracks backlinks via wikilinks only, not Markdown links](20260827_awiki_tracks_backlinks_via_wikilinks_only_not_markdown_links.md) - why an ordinary Markdown link left pages reported as orphans
- 2026-08-27: [awiki title extraction breaks on frontmatter-led source files](20260827_awiki_title_extraction_breaks_on_frontmatter_led_source_files.md) - a tool that titles a page from its first line, meeting a file that opens with YAML
