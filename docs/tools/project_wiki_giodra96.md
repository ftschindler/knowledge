---
type: Tool
title: project-wiki (giodra96)
description: An IDE-neutral agent skill that keeps a prescribed, traceable knowledge base beside a codebase,
  applying the LLM wiki pattern to one repository rather than to a person.
tags:
- tools
- project-wiki
- llm-wiki
- agent-skills
- knowledge-management
- traceability
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-16T00:00:00Z'
sources:
- id: pw-readme
  resource: https://github.com/giodra96/project-wiki
  title: 'giodra96/project-wiki: README'
  author: human:giodra96
  last_modified: '2026-09-16'
- id: pw-schema
  resource: https://github.com/giodra96/project-wiki/blob/main/schema/project-wiki.yml
  title: 'project-wiki: schema manifest'
  author: human:giodra96
  last_modified: '2026-09-02'
- id: karpathy-llm-wiki
  resource: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
  title: Karpathy's LLM Wiki gist
  author: human:andrej_karpathy
  last_modified: '2026-09-16'
- id: ak-progressive-disclosure
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/concepts/progressive_disclosure.md
  title: 'Progressive Disclosure (stjbrown/agent-knowledge)'
  author: human:stjbrown
  last_modified: '2026-08-01'
- id: ak-landscape
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/ecosystem/landscape.md
  title: 'LLM Wiki Ecosystem Landscape (stjbrown/agent-knowledge)'
  author: human:stjbrown
  last_modified: '2026-08-01'
- id: ak-critiques
  resource: https://github.com/stjbrown/agent-knowledge/blob/main/knowledge/ecosystem/critiques.md
  title: 'Critiques & Open Problems (stjbrown/agent-knowledge)'
  author: human:stjbrown
  last_modified: '2026-08-01'
---
project-wiki[^pw-readme] is an agent skill that builds and maintains a knowledge base at
`.project-wiki/` inside a code repository: requirements, change requests, architectural
decisions, observed technical behaviour and a traceability matrix linking all of them to source
paths. It describes itself as an evolution of Karpathy's LLM wiki[^karpathy-llm-wiki] "built for
codebases", and that qualifier is the whole of what distinguishes it from the other tools
collected here.

| | |
| --- | --- |
| Author | giodra96 |
| Licence | MIT |
| Language | Agent Skills markdown, with Python for the deterministic scripts |
| Distribution | Copy the repository into `~/.agents/skills/` or commit it into `.agents/skills/` |
| Source | [github.com/giodra96/project-wiki](https://github.com/giodra96/project-wiki) |
| Version read | wiki schema 1.5.1[^pw-schema] |

## What it is

Prose an agent reads, plus five Python helpers where determinism pays: `wiki_scaffold.py` to
create the skeleton and refuse to overwrite one, `check_inbox.py` to hash and deduplicate
incoming documents, `ingest_document.py` to extract PDF and DOCX outside the model's context,
`validate_wiki.py` for tree, frontmatter, ID, registry and link validation, and
`check_contracts.py` to catch drift between the manifest and the documentation that quotes it.
Five user-facing modes sit on top: `init`, `scan`, `update`, `sync` and `maintain`.

The generated tree is fixed, not suggested. `requirements/functional`, `changes/decisions`,
`technical/`, `traceability/`, `alerts/`, `logs/` and eight more directories are always created,
each record carries a permanent ID matching a pattern (`REQ-*`, `ADR-*`, `CR-*`), and
`REGISTRY.yml` catalogues the lot. Navigation is
progressive disclosure[^ak-progressive-disclosure] by the book, three levels deep: root
`INDEX.md`, section index, record, so an agent loads the smallest relevant set rather than the
history of the project.

Two mechanisms are worth naming because they are the parts an ordinary vault does not have.
**Traceability is bidirectional and machine-facing**: `traceability/requirement-evidence.yml`
ties a requirement ID to the code paths and tests that satisfy it, which is what lets `maintain`
report a requirement nothing implements. And **intent is kept apart from observation**: what
`sync` reads out of the code is recorded as observed technical behaviour and never promoted to a
requirement, because a requirement needs a stated product intent behind it. Where the intent is
unclear, the skill is instructed to file an open question rather than invent one.

## Where it sits among the tools here

It shares the substrate with everything else collected here, plain Markdown and YAML in git, and
differs on the two axes that actually separate these tools: **who the knowledge is about**, and
**how much taxonomy is prescribed**.

[agent-wiki (TacoTakumi)](agent_wiki_tacotakumi.md) and this bundle are personal knowledge bases that happen to
contain software knowledge, organised by the nature of a page and scoped to a person.
project-wiki is scoped to a repository, and organised by the artefact kinds of a software
project. That is still filing
[by what content is rather than why you made it](../knowledge_management/categorize_by_what_content_is_not_why_you_made_it.md):
a decision record and a requirement are genuinely different kinds of page. The difference is that
the set of kinds is closed, and named in a schema file rather than chosen as the base grows.

Against [agent-knowledge (stjbrown)](agent_knowledge_stjbrown.md) the contrast is sharper, because the
two are the same shape - skills plus deterministic scripts, no runtime, no database - pointed at
different targets. agent-knowledge builds
[OKF](../research/open_knowledge_format_okf_findings.md) bundles, and OKF explicitly declines to
fix a taxonomy of concept types. project-wiki fixes one, completely, in
`schema/project-wiki.yml`, and gains from it what OKF gives up: `validate_wiki.py` can check that
an ADR exists for a decision a requirement references, because it knows what an ADR is. The
trade is portability. An OKF bundle is a directory anyone's tooling can read; a `.project-wiki/`
is a directory this skill's tooling can read, and the schema version in `WIKI_VERSION.yml` is
there because that contract will move. agent-knowledge's `kb-document` skill covers the same
ground from the other side, documenting a repository from its source without prescribing what the
documentation must contain.

The overlap with [federated-knowledge-skills (Felix Schindler)](federated_knowledge_skills_schindler.md) is smaller
than it first looks. fkb's problem is that one person's knowledge spans several audiences, which
is why it
[separates audiences with separate bundles](../knowledge_management/separate_audiences_with_separate_bundles.md)
and binds them with a reference rule. project-wiki has exactly one tier by construction, the
repository, and inherits its visibility from whoever can clone it. Nothing in it is designed to
be cited from outside, and a `.project-wiki/` committed to a public repository publishes every
open question and alert in it.

## Where it sits in the ecosystem

The landscape survey that [agent-knowledge](agent_knowledge_stjbrown.md) maintains groups the several
hundred implementations Karpathy's gist spawned by shape[^ak-landscape], and project-wiki
straddles two of its categories. By packaging it is an agent skill, the busiest category in the survey and the one
almost entirely Obsidian-wikilink-flavoured; by target it belongs to the codebase-doc generators,
the adjacent lane that documents a repository rather than ingesting general sources, alongside
openwiki and DeepWiki. What it has that neither lane usually does is the seam between them: an
`update` mode that ingests meeting notes and PDFs like a general-knowledge wiki, feeding the same
records that `sync` reconciles against code. The survey did not list it when I read it.

Reading that survey is also what makes the taxonomy question sharper rather than academic. A
closed schema is unusual here, and the cohort that has one has mostly reached for a database
instead: the markdown-versus-database dissent the critiques page records holds that deterministic,
strongly-typed knowledge wants SQL and an event log rather than a pile of files. project-wiki is
the middle position, taking the typed IDs and the validator whilst staying greppable and
diffable, and `WIKI_VERSION.yml` is what that position costs.

## Against the objections to the pattern

The objections to the LLM wiki are better documented than the pattern's successes, and
agent-knowledge collects them[^ak-critiques]. Two of the three bear directly on this tool, and it
answers them from opposite ends.

**Truth maintenance, and the poisoning that follows from it**, is the strongest one: once
model-authored synthesis sits beside its sources, later passes reason over AI output rather than
ground truth, and the drift is invisible because every page still reads coherently. The fixes
proposed in that thread are source-grounded, citation-first, review-gated knowledge bases where
the model proposes rather than decides. project-wiki implements roughly that shape without
citing the argument: extraction is provenance and never canon, code-derived behaviour is observed
and never a requirement, an unresolved contradiction becomes an `alerts/` record instead of a
silent edit, and the ambiguous case is an open question rather than an invention. It is the most
disciplined answer to that objection I have seen shipped in this lane, and it is the reason the
page is here rather than in a line of the index.

**Token cost is postponed, not eliminated** is the one it does not answer. Progressive disclosure
through indexes degrades past roughly 50 to 100K tokens, and the proposed fix is section-level
retrieval or a real search tool. project-wiki has neither: `REGISTRY.yml` is a catalogue, not an
index in the retrieval sense, and the routing layer is the whole of the strategy. For a wiki
bounded by one repository that ceiling is further away than it is for a personal base that
accumulates for years, which is a mitigation rather than a solution. It is the same gap the fkb
journal is being kept to measure here.

## What I would take from it

Three things, none of which require adopting the skill.

**The provenance rule.** Ingested PDFs and DOCX land in `sources/inbox/` and are extracted into
`intake/` as evidence, never read straight into a record, and become canonical only once
classified. That is the same three-layer split awiki implements with `raw/` and a render hash,
arrived at independently, and it is the mechanism that stops a source document's own phrasing
from being mistaken for a decision someone made.

**Deterministic first, semantic second.** `maintain` runs structural validation to establish
facts, and only then asks the agent about contradictions, stale meaning and traceability quality.
The ordering is the point: the agent is spent on the questions a script cannot answer, which is
the same division of labour
[guarding invariants at commit time](../principles/guard_invariants_at_commit_time_not_review_time.md)
buys in a repository.

**Open questions are resolved, not deleted.** An unresolved contradiction gets a record in
`alerts/` and stays there. A knowledge base that can only hold settled facts silently drops
everything it is most useful to remember.

What I would not take is the always-on instruction bootstrap, which writes a marked block into
both `AGENTS.md` and `.github/copilot-instructions.md` during `init` and `scan`. It is the
honest way to make the wiki actually get used, since a skill nothing invokes is a skill nothing
reads, but it is a tool editing the file that loads into every session in the repository, and
that file is the one I want to have written myself.
