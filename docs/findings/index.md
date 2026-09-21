# Findings

Things that cost time once. Each records the symptom, what it turned out to be, and how to get
past it, so the next encounter is short.

A finding is the cheapest page here to write, and deliberately so: it does not have to be
general, it does not have to connect to anything, and it only has to be true and to have cost
someone an afternoon. See
[Give a knowledge base a tier that is not asked to earn its place](../knowledge_management/give_a_knowledge_base_a_tier_that_is_not_asked_to_earn_its_place.md)
for why that tier is the one that fills, and what happens when a finding turns out to carry a
reusable claim.

Here that means four conventions. The title names the **symptom**, in the words you would have
searched for, because that is how anyone arrives. The filename leads with the date it was found,
`20260911_`, and this list runs newest first. A finding about a tool carries `stale_after`, since
its claim is a claim about a version; the reasoning is
[Date a page whose claim is about a version](../knowledge_management/date_a_page_whose_claim_is_about_a_version.md).
And the subject lives in the tags rather than in a directory, per
[Split orthogonal classification axes across folders and tags](../knowledge_management/split_orthogonal_classification_axes_across_folders_and_tags.md).

## 2026

### September

- 2026-09-21: [neo-tree's hide_hidden does not show dotfiles on Linux](20260921_neo_tree_hide_hidden_does_not_show_dotfiles_on_linux.md) - an option that is Windows-only, in the wrong place, and rejected by nothing
- 2026-09-18: [A GitHub token does not authenticate requests to github.com web pages](20260918_a_github_token_does_not_authenticate_github_com_web_pages.md) - a credential the website ignores, and a 404 that cannot be told apart from a deleted repository
- 2026-09-18: [linkspector ignores the httpHeaders in its config](20260918_linkspector_ignores_the_httpheaders_in_its_config.md) - a credential that passes validation, is dropped by both checking passes, and leaves a live link reported as broken
- 2026-09-18: [opencode merges a profile over the base config rather than replacing it](20260918_opencode_merges_a_profile_over_the_base_config_rather_than_replacing_it.md) - the marker key that settled it, and the duplicated setting that argues for the wrong answer
- 2026-09-16: [nanobench reports no Big-O estimate, or one fitted across unrelated runs](20260916_nanobench_reports_no_bigo_estimate_or_one_fitted_across_unrelated_runs.md) - a scaling sweep that collects its data and then throws it away, and a fit that spans benchmarks measuring different things
- 2026-09-11: [Dependabot declines transitive security updates in uv.lock](20260911_dependabot_declines_transitive_security_updates_in_uv_lock.md) - an error naming a version conflict that does not exist, and the two settings that actually caused it

### August

- 2026-08-27: [fs.protected_regular blocks root writes in sticky tmp](20260827_fsprotected_regular_blocks_root_writes_in_sticky_tmp.md) - a root process denied a write to a world-writable file, and the sysctl that explains it
- 2026-08-27: [awiki tracks backlinks via wikilinks only, not Markdown links](20260827_awiki_tracks_backlinks_via_wikilinks_only_not_markdown_links.md) - why an ordinary Markdown link left pages reported as orphans
- 2026-08-27: [awiki title extraction breaks on frontmatter-led source files](20260827_awiki_title_extraction_breaks_on_frontmatter_led_source_files.md) - a tool that titles a page from its first line, meeting a file that opens with YAML
