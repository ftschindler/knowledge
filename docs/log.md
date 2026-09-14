# Log

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
