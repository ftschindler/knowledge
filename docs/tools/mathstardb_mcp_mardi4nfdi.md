---
type: Tool
title: Math*DB MCP (MaRDI4NFDI)
description: A public MCP server over MaRDI's two mathematical knowledge graphs, MathModDB for
  models and their equations and MathAlgoDB for algorithms, problems and software, with tools
  that cross from one to the other.
tags:
- tools
- mcp
- mardi
- mathematics
- sparql
status: draft
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-18T14:30:00+01:00'
sources:
- id: mathstardb-repo
  resource: https://github.com/MaRDI4NFDI/MathModDB-MCP
  title: 'MaRDI4NFDI/MathModDB-MCP: Repo for the MCP development for MathModDB'
  last_modified: '2026-11-03'
---
Math*DB[^mathstardb-repo] is an MCP server that lets an agent query two knowledge graphs
from the [MaRDI](https://www.mardi4nfdi.de/) project, the German national research data
infrastructure for mathematics. One graph describes mathematical models, the other the
algorithms and software that solve the problems those models lead to, and the server can
walk from one to the other.

| | |
| --- | --- |
| Author | MaRDI4NFDI |
| Licence | GPL-3.0 |
| Language | Python, on FastMCP |
| Distribution | A hosted endpoint, `https://mathstardb.mardi4nfdi.de/mcp`, over streamable HTTP with no authentication |
| Source | [github.com/MaRDI4NFDI/MathModDB-MCP](https://github.com/MaRDI4NFDI/MathModDB-MCP) |
| Version read | 0.2.0 live, from its `initialize` and `tools/list` responses; 0.1.0 in the repository |

## What it is

**MathModDB** holds mathematical models: their formulations as LaTeX formulas, the quantity
every symbol stands for, the assumptions they make, and how models relate to one another, as
specialisations, approximations, linearisations and discretisations. It lives in the MaRDI
portal's Wikibase and is queried with SPARQL. The server asks for one discovery call,
`Explore_Ontology`, before any query, so the agent learns the item and property ids first.
`model_formulation` and `model_relations` answer the common questions without writing SPARQL.

**MathAlgoDB** holds algorithms, problems, software, benchmarks and publications, linked by
relations such as *solves*, *implemented by* and *specialises*. Most questions have a
dedicated tool rather than a query: `algorithms_for_problem`, `software_for_algorithm`,
`benchmarks_for_problem`, `hierarchy` for the taxonomy around an entry, and `literature` for
the papers that introduced, surveyed or analysed it. `sparql_query` remains for anything else.

**The bridge is what makes it one server rather than two.** `algorithms_for_model` starts from
a model in MathModDB and returns the algorithms and software in MathAlgoDB that apply to it,
and `models_for_problem` goes the other way. Twenty-two tools in all.

The public repository is behind the deployment. It holds version 0.1.0, with the three
MathModDB tools only, whilst the endpoint reports 0.2.0 with all twenty-two.
