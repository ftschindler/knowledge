---
type: Tool
title: pyMOR
description: A free and open-source Python library of model order reduction algorithms, written against
  abstract vector, operator and model interfaces so that external solvers can supply the full-order model.
tags:
- tools
- python
- model-order-reduction
- self-authored
status: stable
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T20:00:00+01:00'
sources:
- id: pymor-pyproject
  resource: https://github.com/pymor/pymor/blob/main/pyproject.toml
  title: 'pymor/pymor: pyproject.toml'
  last_modified: '2026-11-17'
- id: pymor-preprint
  resource: https://arxiv.org/abs/2608.00082
  title: 'arXiv:2608.00082 Data-Driven Model Order Reduction with pyMOR'
  last_modified: '2026-07-29'
---
pyMOR is a library of model order reduction algorithms for Python. Its algorithms are written in
terms of three abstract interfaces, `VectorArray`, `Operator` and `Model`, so a full-order model
computed by an external solver can be reduced without being rewritten in Python. Data-driven
methods, which need only simulation or measurement data, sit beside the classical model-based
ones[^pymor-preprint]. [Felix Schindler](../people/felix_schindler.md) is one of its authors.

| | |
| --- | --- |
| Author | The pyMOR developers; maintained by Stephan Rave |
| Licence | BSD-2-Clause and BSD-3-Clause[^pymor-pyproject] |
| Language | Python, supporting 3.10 to 3.14 as of release 2026.1.1 |
| Distribution | PyPI, as `pymor` |
| Source | [github.com/pymor/pymor](https://github.com/pymor/pymor) |
| Site | [pymor.org](https://pymor.org) |

## Where it appears here

pyMOR is the worked example in
[Type annotations for a Python library: the options](../investigations/type_annotation_options_for_a_python_library.md),
which places an open pull request annotating its `vectorarrays` package among the ways a library
can be typed.
