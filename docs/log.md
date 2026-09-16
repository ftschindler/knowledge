# Log

## 2026-09-16

- add a tool page for project-wiki, the agent skill that keeps a requirements, decisions and traceability wiki inside a code repository: what the five modes and five scripts do, and the two axes that separate it from the other tools here, namely that it is scoped to a repository rather than a person and fixes its taxonomy in a schema file where OKF deliberately does not
- record what I would take from it without adopting it: the provenance split between ingested evidence and canonical record, running deterministic validation before the semantic pass, and keeping unresolved contradictions as alerts rather than deleting them; not the bootstrap that writes into the repository's own always-on instruction files

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
