# Log

## 2026-09-22

- move the "What I took" section off the caveman tool page into a decision, "Adopting caveman at lite, without its init block", and leave the tool page pointing at it
- add a blog beside the bundle, in `blog/`, with a first post on adding it
- generalise the publish hook from `about/` to any sibling of the bundle, rename it to `publish_siblings.py`, and widen its link rewriting to any depth
- have that hook write the blog's entrypoint into the bundle directory as a gitignored build artefact, since the blog plugin cannot bootstrap its own in this layout
- turn off the backlinks section on `blog/`, and exclude the entrypoint from the git revision date plugin
- render a page's status into the genre note it already opens with, rather than as a second block: the note turns amber for draft and red for deprecated and leads with the status word
- let a directory say what draft means for its genre, under `status_notes`, since in `decisions/` it means decided and not yet carried out rather than unfinished
- write a decision on adopting ponytail as two halves, the ladder as instruction and the commands as tooling, and leave it at draft status until it is carried out

## 2026-09-21

- add "Teaching my agents to write like me" to decisions
- add "Route a rule to the layer that reaches whoever must obey it" to principles
- add "Concreteness is expensive to fake, warmth is free" to principles
- add the prose-tells hook and its script, and record it in the editing conventions
- drop the duplicated concrete-behaviour sentence from the editing conventions
- state in the editing conventions that a log entry records what changed and never why

- write a tool page on ponytail, the skill that has an agent climb a seven-rung ladder before writing code: the ordering is the whole idea, since reuse sits above writing on it and a generic instruction to keep things small leaves the agent to decide what small means
- record why I took only its review, audit and debt commands: the ladder's new material is narrower than my own scope rules already cover, and the opencode adapter cannot scope its injection the way the Claude Code and Codex hooks can, so a read-only search agent gets told to write one line
- note that its author retracted his own 80-94% headline in place, on the grounds that the baseline was padding with prose, and left the reasoning up

- write a tool page on caveman, the reply-compression skill: separate the MIT skill from the four commercial layers sold under the same name, since only the skill changes what a reader sees and only it is installable alone
- record what survives of it when the token argument is dropped: the Simplified Technical English clause and the ban on narrating tool calls, against a full level whose dropped articles buy nothing the file itself does not argue against

- file a finding that neo-tree's hide_hidden does not show dotfiles on Linux: the option names the NTFS hidden attribute and sits under filtered_items rather than filesystem, and setup rejects an unknown key with neither an error nor a warning
- name all three writing principles in the editing conventions rather than one, as a table of what each guards against: the voice page was linked, the concrete-behaviour page paraphrased without a link, and the pacing page mentioned nowhere, so a writer following the authority page was given the honesty axis and neither clarity axis
- rewrite the objections section of the project-wiki page in plainer terms, which is what turned that gap up: every sentence passed the voice rules and still carried three ideas at once
- open a guides section, for a procedure carried out once that would otherwise be rediscovered: what separates it from a blueprint is that a blueprint is an artefact to copy whilst a guide is a sequence of acts performed in the world, and what makes one worth keeping is the two or three steps that are silent when skipped
- write the first one, on letting CI push to a protected branch with a GitHub App rather than a maintainer's personal access token: an App installed on the one repository, holding contents write alone, minting a token that expires within the hour, committing under a bot identity whose numeric user id is looked up at run time
- record the two steps in it that look like configuration and are not: the bypass list entry is not a permission, so everything else can be correct and the push still declined, and an App token starts workflow runs where the default token does not, so a job that pushes to the branch it triggers on has to terminate by construction

## 2026-09-18

- add a tool page for skills, the Vercel Labs installer that takes agent skills out of any git repository and writes them into whichever harnesses are on the machine: a skill is discovered rather than declared, so there is no manifest and no publishing step, and a repository is however many `SKILL.md` files it happens to hold
- file the research behind it, a source read of version 1.7.0 confirmed by installing from a scratch repository: the repository root is walked one level deep on purpose, so one skill per root-level directory is the case that scan is written for, and selective install by name or at a pinned revision is a first-class path rather than a workaround
- record the two things that need guarding around it, since neither tool nor review will catch them: a `SKILL.md` missing a string `name` or `description` is skipped with a warning rather than refused, and the installed directory takes the frontmatter `name` and not the source directory, so the two are free to disagree silently
- record what the skills CLI reports back and how to stop it: install events carry the repository and the names of the skills, `DO_NOT_TRACK=1` disables every send, private GitHub repositories are already excluded by a check that fails closed, and that check is keyed on parsing exactly one owner and one repository so a private GitLab subgroup path falls through to the branch that sends anyway
- note the cost of opting out, which is a trade rather than a bug: the security audit lookup guards on the same flag, so the machine that reports nothing is also the one no longer told the risk rating of what it is about to install

- add a tool page for linkspector, the link checker this bundle has committed through since before it had a page: the two passes it resolves every link with, an HTTP request and a headless Chrome behind it, and the strict schema that rejects any key it does not define, so the configuration file cannot be annotated in its own syntax
- file a finding that linkspector ignores the httpHeaders in its config, dropped by the HTTP pass which never reads them and by the Puppeteer pass which hands them to a goto that has no such option
- file the reusable half beside it as its own finding: a GitHub token does not authenticate requests to github.com web pages at all, so the website answers a token-bearing request with the same 404 it gives a stranger, which is indistinguishable from a repository that was deleted or never existed; the API and the raw host honour the same token, and one request to the organisation endpoint separates a bad credential from a dead link
- enable the footnotes markdown extension and register hooks/concept_sources.py, which was present but never wired into the build: every page declaring sources had been rendering its citation markers literally, as `[^uv-docs]`, since the first one was written
- add a tool page for opencode, the harness named in the `generated.by` field of nearly every page here and until now the only tool in this bundle without a page of its own: what the four extension points are, the two debug commands that say what a session actually resolved to, and how my own configuration keeps one directory per provider so a session never sees two at once
- add a tool page for markitdown, Microsoft's converter from PDF and Office documents into Markdown, in both of the shapes it ships as: the command, and the MCP server exposing a single convert tool that also takes remote URIs
- record that the extras belong to markitdown and not to markitdown-mcp, so asking for markitdown-mcp[all] is a no-op reported as a warning, whilst the server already depends on the full converter set outright and resolves to 74 packages
- file a finding that an opencode profile merges over the base config rather than replacing it, settled with a marker key in the base layer and read back with a profile active, because the repeated plugin entry in every profile argues convincingly for the opposite answer
- promote the reusable half of that to a principle: test a config layering assumption with a marker key, since the keys every layer sets cannot distinguish merging from replacement and a key present in only one layer can

## 2026-09-16

- name the author in the title and filename of every tool page that is somebody's repository, so agent-wiki, agent-knowledge, project-wiki and federated-knowledge-skills now carry TacoTakumi, stjbrown, giodra96 and my own name; the names these projects give themselves are generic enough to collide with each other, and who wrote a one-person project is the thing most worth knowing before depending on it
- leave uv and Dependabot under their plain names, since a product with a vendor behind it is not going to be confused with anyone else's, and record the split in the tools index where the rest of what we do here is written
- move the CLI short names out of the titles and into the index entries, where `awiki`, `kb-*` and `fkb` still say how each one is invoked

- add a tool page for project-wiki, the agent skill that keeps a requirements, decisions and traceability wiki inside a code repository: what the five modes and five scripts do, and the two axes that separate it from the other tools here, namely that it is scoped to a repository rather than a person and fixes its taxonomy in a schema file where OKF deliberately does not
- record what I would take from it without adopting it: the provenance split between ingested evidence and canonical record, running deterministic validation before the semantic pass, and keeping unresolved contradictions as alerts rather than deleting them; not the bootstrap that writes into the repository's own always-on instruction files
- place it against the upstream agent-knowledge bundle rather than describing it alone: it straddles the ecosystem survey's agent-skills and codebase-doc-generator lanes, its intent-versus-observation rule and alerts records are a shipped answer to the truth-maintenance objection, and it has no answer at all to the one about token cost being postponed rather than eliminated

- add a tool page for federated-knowledge-skills, the skill, CLI and pre-commit hooks this bundle is now written through: what the four parts are, the three decisions the design rests on, and the search command deliberately withheld until the journal says it is needed
- file it in `tools/` rather than a new `projects/` folder, and mark it `self-authored` instead: who made a thing is a fact about it, not a kind of page, and a folder per project is the domain axis growing back one plausible page at a time; the directory's genre note no longer says "external", and my own page grows a "Built" section that lists from the tag

- add "A microbenchmark body must not mutate state that outlives one iteration", from reviewing a C++ benchmark suite where the expensive model was prepared outside the timed lambda: the harness chooses the iteration count, so hoisting setup out of the body silently changes what every iteration after the first is measuring
- add the nanobench finding beside it: `complexityN` tags a run but prints nothing without `complexityBigO`, and the fit it feeds spans every run registered on the same `Bench`, so unrelated solvers registered together are fitted as one curve

## 2026-09-15

- rename `okf-floor.yaml` to `fkb.yaml`: the `okf-` prefix claimed the format defines the file when the floor is ours, and `floor` named one of the three jobs it had grown into; the new name is the filename the federation's tooling looks for when it discovers a bundle, which is the one thing about the file nobody but that tooling owns
- point the declaration at the editing conventions, so an agent that reads the schema is told where the voice lives instead of finding the fields and stopping; the checker warns if the pointer stops resolving, which is the failure that was otherwise silent
- move the pinned conformance checker forward to the revision that understands both

## 2026-09-14

- render a page's provenance where a reader can see it: genre, status, who generated it, who verified it or that nobody has, and when to revisit it, in a card pinned to the foot of the table-of-contents column and moved under the content on narrow screens
- declare each directory's genre once in its own `.genre.yaml` and render the note from it, deleting the copy that sat in all seventy-six concepts; `type` is now held to the declaration by a hook
- render `sources[]` as footnotes, cited in prose by id, and reject a source nothing cites or a citation nothing declares

- add "Separate audiences with separate bundles, not with folders or tags", recovered from the awiki vault's dropped meta pages during a final sweep: the claim that sharing happens at the vault boundary is what frees the folder axis to carry nature, and it had not survived the import

- retitle "Federated OKF knowledge bases" and rewrite its skill-layer section: the manifest, the reference rule and the commit-time guard are current, but the layer that wrapped a second set of skills was built and retired, and the title still advertised it
- add "Wrapping the kb skills in a federation layer" as a draft stub, since the retirement is an exploration and was recorded only as a paragraph in another repository

## 2026-09-13

- trim the five concepts that opened by restating their genre in prose, which the note above them now says

- give every directory its own `index.md`, which is now where a genre is defined: what belongs here, the conventions local to it, and the listing
- cut the root index to what the bundle is, the three passes it came out of, and a link to each section in the order the ideas build; it no longer lists pages
- point each concept's genre note at its own directory's index rather than a root-index anchor
- trim the findings index to what we do here, deferring the reasoning to the two concepts below
- order the nav explicitly in `.pages`, so Explorations no longer sits between Decisions and Blueprints
- drop the three-passes paragraph from the index: it characterised the bundle by one subject among many, and the work it did is now done by the explorations index and the genre note on every exploration
- give the remaining 67 concepts their genre note, so every page says what kind of page it is and links to the index that defines the kind

- add "Give a knowledge base a tier that is not asked to earn its place" and "Date a page whose claim is about a version", the two reusable claims behind the findings directory, both drafts pending a rewrite in my own voice
- require a commit per logical change, in the editing conventions

## 2026-09-11

- date findings in the filename (`20260911_...`) and list the directory newest first, since when a finding was written is part of what it claims
- enable the theme's `navigation.indexes`, so clicking a section in the nav opens its `index.md` instead of only expanding the section
- give **Findings** a directory of its own and a sub-index, moving all four out of `tools/` and `linux/`, which dissolves: a finding's subject is a tag, not a folder
- adopt `stale_after` for findings about a tool, whose claims are claims about a version
- amend "Categorize by what content is, not why you made it", whose own worked example filed a finding under `tools/`: rejecting the circumstance of discovery is not enough if the answer you land on is a subject rather than a nature
- extend "Split orthogonal classification axes across folders and tags" with how the rule drifts back, the two tells for it, and `knowledge_management/` as a named exception
- add "Keep transitive dependencies in the regular update cycle", replacing "Tell the update bot to look at transitive dependencies", which stated one principle, one tool's configuration and one bug on a single page
- add "Dependabot declines transitive security updates in uv.lock", the finding that page's tool-specific half became
- add "uv" and "Dependabot" as tool references, giving both a home: they were named across 13 and 4 concepts respectively without one
- correct "Batch dependency updates with a cooldown, not a firehose", which implied a cooldown is a dial to back off for security: it never applies to security updates, though a package manager's own cooldown does
- add "Keep the GTD inbox inside the private bundle, not beside it", the practice behind the inbox section now living in the private bundle
- note in the same page that a section may carry its own log, and what the reserved-filename rule does to a file named `inbox.log.md`

## 2026-09-10

- add "agent-wiki (awiki)", the first entry in a new Tools section that gives an external tool one page of its own
- add "agent-knowledge (kb skills)"
- mark "Running this knowledge base on awiki" as an exploration with a note linking to the index section that defines the genre
- move the genre prefaces of "Running this knowledge base on awiki" and "Federating my knowledge base as privacy-tiered OKF bundles" into the index section blurbs, where they hold for every page in the section
- rename "Building a PKB that is mine, forever-readable, and visual" to "Building my visual PKB", filename and inbound link texts with it
- add the **Explorations** layer, for work committed to and later withdrawn
- add "Running this knowledge base on awiki", replacing the decision "Building an agent-first wiki that is also a human PKB", which was never a lasting choice
- add "Federating my knowledge base as privacy-tiered OKF bundles", the decision that exploration led to
- add "Record an abandoned exploration as an exploration, not a superseded decision"
- add "Automatic session capture is not an inbox", replacing "GTD-style inbox capture in an Agent Wiki vault"
- add "Categorize by what content is, not why you made it", with its examples rewritten against this bundle
- extend "Layer build-knowledge as a values-to-blueprints derivation pipeline" with the research and exploration layers
- drop "KDE Plasma - Phantom Pointer After Hibernate Resume (Unresolved)", an unresolved investigation nothing else rests on
- drop "About this vault" and "Why this vault uses nature-folders and domain-tags", whose role is now carried by the index and `okf-floor.yaml`

## 2026-09-09

- import the knowledge from the earlier awiki vault, one concept per commit
- add "Prefer FOSS software wherever possible"
- add "Prefer plain-text, tool-agnostic formats"
- add "Wishes for a personal knowledge base"
- add "Local-first, but not local-required"
- add "Treat warnings as errors"
- add "Guard invariants at commit-time, not review-time"
- add "Mirror every local guard in CI"
- add "Autofix in the hook, don't just flag"
- add "Order auto-fixers so later ones do not re-dirty earlier output"
- add "Verify a pre-commit hook's file-type filter actually matches your file"
- add "A markdown autofixer can corrupt YAML frontmatter it treats as content"
- add "Pin pre-commit hooks to frozen revisions"
- add "Pin GitHub Actions to full commit SHAs"
- add "Pin transitive runtime dependencies, not just the tool"
- add "Install from a frozen lockfile in CI"
- add "Batch dependency updates with a cooldown, not a firehose"
- add "Keep declared toolchain versions in sync, and guard it"
- add "Validate config files against their published schema"
- add "Document a rationale for every disabled lint rule"
- add "Grant least-privilege CI permissions at both workflow and job level"
- add "Split CI jobs for attributable failure and minimal dependencies"
- add "Name every CI step so the run log reads as a narrative"
- add "Bound every CI job with an explicit timeout"
- add "Cancel superseded CI runs with a concurrency group"
- add "Run CI steps under a strict shell (errexit, pipefail)"
- add "A test that cannot run must fail loudly, never skip into a green result"
- add "A sandbox test must use the live working-tree source and rebuild fresh each run"
- add "End-to-end test an LLM skill by driving a real agent in a disposable fake HOME"
- add "Enforce LF line endings everywhere"
- add "Declare formatting once, editor-agnostically, via .editorconfig"
- add "Keep filenames lowercase with no whitespace"
- add "Make support-tool config files dotfiles"
- add "Track every committed binary type in .gitattributes"
- add "Enforce a canonical author identity via .mailmap"
- add "Keep a linear history: block merge, fixup and squash commits"
- add "Make the build interface a self-documenting Makefile"
- add "Fail early on a missing tool with a message that names it and points at the fix"
- add "Do not make a tool a prerequisite for work it is not needed for"
- add "Resolve a repo's own dev tools through an ephemeral runner, not a project virtualenv"
- add "Use PEP 723 inline script metadata for zero-install tooling scripts"
- add "A declared-but-inert config documents intent, not enforcement"
- add "Enforce the intersection of all renderers and consumers"
- add "Structure docs as the reader's task path - lead with action, defer rationale"
- add "Hand the reader one idea at a time"
- add "Name the concrete behaviour, not its abstract label"
- add "Write in a calm, quantified, settled-fact voice - not a promotional one"
- add "Give every cross-cutting concept one definitional home"
- add "Building a PKB that is mine, forever-readable, and visual"
- add "Building an agent-first wiki that is also a human PKB"
- add "MkDocs Material PKB publishing stack"
- add "Layer build-knowledge as a values-to-blueprints derivation pipeline"
- add "Split orthogonal classification axes across folders and tags"
- add "Open Knowledge Format (OKF): findings"
- add "Substrate options for an OKF-based agent-first LLM wiki: investigation"
- add "Agent-integration layer and multi-vault interaction for an OKF-conformant PKB"
- add "Federated OKF knowledge bases: a workspace-manifest architecture with fkb-over-kb skills"
- add "Security Analysis of Agent Wiki (awiki)"
- add "fs.protected_regular Blocks Root Writes in Sticky tmp"
- add "KDE Plasma - Phantom Pointer After Hibernate Resume (Unresolved)"
- add "awiki title extraction breaks on frontmatter-led source files"
- add "awiki tracks backlinks via wikilinks only, not Markdown links"

## 2026-09-07

- created the bundle
- add an entry on Felix
