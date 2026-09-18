# Tools

Tools and projects worth a page of their own: what each one is, who makes it, and what it is
for. Mostly someone else's, occasionally mine.

One page per tool, flat. The subject of a page rides on its tags rather than on a directory, so
everything learned *about* a tool lives under its own nature and links back here: a bug it has
is a [finding](../findings/index.md), a phase spent on it is an
[exploration](../explorations/index.md).

Something I wrote belongs here too, and is tagged `self-authored` rather than given a directory
of its own. Who made a thing is a fact about it, not a kind of page, and a `projects/` folder
would be the domain axis
[growing back a folder](../knowledge_management/split_orthogonal_classification_axes_across_folders_and_tags.md)
one plausible page at a time. The tag is what
[my page](../people/felix_schindler.md) lists from.

**A page about somebody's repository carries their name, in the title and in the filename**, as
`agent-wiki (TacoTakumi)` in `agent_wiki_tacotakumi.md`. Most of what is here is one person's
project rather than a product, and those names are generic enough to collide with each other and
with things that are not tools at all: "agent-wiki", "agent-knowledge" and "project-wiki" are
three pages in this directory and could as easily have been the same one. Who wrote it is also
the thing most worth knowing before depending on it, so it belongs where a reader lands rather
than in a table halfway down. Products with a vendor behind them keep their plain name, because
`uv` is Astral's and will not be anyone else's.

- [agent-wiki (TacoTakumi)](agent_wiki_tacotakumi.md) - `awiki`: a CLI-driven markdown vault agents search before the web, and what this knowledge base ran on before it was an OKF bundle
- [agent-knowledge (stjbrown)](agent_knowledge_stjbrown.md) - the `kb-*` skills rather than an engine for maintaining OKF bundles, and the upstream whose own bundle is cited here
- [federated-knowledge-skills (Felix Schindler)](federated_knowledge_skills_schindler.md) - mine: the `fkb` skill, CLI and hooks that bind privacy-tiered bundles into a federation, and what this bundle is now written through
- [project-wiki (giodra96)](project_wiki_giodra96.md) - the LLM wiki pattern aimed at a repository rather than a person, with a closed taxonomy of requirements, decisions and traceability
- [uv](uv.md) - the Python manager under everything here, and the manifest-versus-lockfile split several principles turn on
- [Dependabot](dependabot.md) - the update bot, and the three different things that share its name
- [opencode](opencode.md) - the terminal agent that writes most of these pages, and the one-directory-per-provider config my own setup is built from
- [markitdown](markitdown.md) - Microsoft's PDF-and-Office-to-Markdown converter, as a command and as the MCP server an agent calls
- [linkspector](linkspector.md) - the link checker this bundle commits through, the two passes it resolves every link with, and the schema that refuses to be annotated
- [skills (Vercel Labs)](skills_vercel_labs.md) - `npx skills add`: the installer that discovers a skill by finding its `SKILL.md`, and the leaderboard it reports installs to
