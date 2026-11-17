---
type: Investigation
title: 'Type annotations for a Python library: the options'
description: The choices behind annotating a Python library - where the types live, which syntax and so
  which Python floor, which checker and how strictly - with one pyMOR pull request placed among them.
tags:
- python
- typing
- type-checking
- tooling
- pymor
status: stable
stale_after: '2027-05-17'
generated:
  by: opencode/claude-opus-5.5
  at: '2026-11-17T20:00:00+01:00'
sources:
- id: pep-604
  resource: https://peps.python.org/pep-0604/
  title: 'PEP 604: Allow writing union types as X | Y'
  last_modified: '2026-11-17'
- id: pep-673
  resource: https://peps.python.org/pep-0673/
  title: 'PEP 673: Self Type'
  last_modified: '2026-11-17'
- id: pep-695
  resource: https://peps.python.org/pep-0695/
  title: 'PEP 695: Type Parameter Syntax'
  last_modified: '2026-11-17'
- id: pep-696
  resource: https://peps.python.org/pep-0696/
  title: 'PEP 696: Type Defaults for Type Parameters'
  last_modified: '2026-11-17'
- id: pep-649
  resource: https://peps.python.org/pep-0649/
  title: 'PEP 649: Deferred Evaluation Of Annotations Using Descriptors'
  last_modified: '2026-11-17'
- id: basedpyright
  resource: https://github.com/DetachHead/basedpyright
  title: 'DetachHead/basedpyright: README'
  last_modified: '2026-11-17'
- id: ty
  resource: https://github.com/astral-sh/ty
  title: 'astral-sh/ty: README'
  last_modified: '2026-11-17'
- id: pyrefly
  resource: https://github.com/pyrefly-org/pyrefly
  title: 'pyrefly-org/pyrefly: README'
  last_modified: '2026-11-17'
- id: zuban
  resource: https://github.com/zubanls/zuban
  title: 'zubanls/zuban: README'
  last_modified: '2026-11-17'
- id: pymor-2680
  resource: https://github.com/pymor/pymor/pull/2680
  title: 'pymor#2680: Add type annotations for pymor.vectorarrays'
  last_modified: '2026-11-17'
---
**Context** - an open pull request adds type annotations to [pyMOR](../tools/pymor.md)'s
`vectorarrays` package[^pymor-2680], and the question was how its approach compares with the other
ways a library can be typed. Annotating a library is several independent choices, and a pull
request makes all of them at once without naming any. This page separates them.

The checker landscape was read from each project's README on 2026-11-17. It moves monthly, so
read that section against the `generated` date.

## Where the types live

**In docstrings.** A numpydoc `Parameters` section states types in prose. Readers see them;
no tool checks them.

**Inline, in the signatures.** The mainstream choice, and the only one a checker reads against
the code it describes.

**In separate `.pyi` stub files.** Used when the source cannot change, or must keep running on
interpreters older than the annotation syntax. The cost is a second copy of every signature,
which drifts from the first.

## The syntax sets the Python floor

Each Python release has added annotation syntax, and using it drops every older interpreter.

| Python | What it adds |
| --- | --- |
| 3.10 | `X \| Y` unions at runtime[^pep-604] |
| 3.11 | `typing.Self`, for a method returning its own class[^pep-673] |
| 3.12 | `class C[T]: ...` and `type Alias = ...`, replacing `TypeVar` and `TypeAlias`[^pep-695] |
| 3.13 | Defaults for type parameters, so a bare `C` means `C[Default]`[^pep-696] |
| 3.14 | Annotations evaluated lazily, so a forward reference needs no quotes[^pep-649] |

**The syntax is the only thing a newer floor buys.** `from __future__ import annotations`,
`TypeVar` and `typing_extensions` express the same types on 3.10, and a checker sees no
difference. Raising the floor is therefore a decision about users' interpreters, made for the
sake of shorter source.

## Which checker

| Checker | What distinguishes it |
| --- | --- |
| mypy | The reference implementation, with the largest plugin ecosystem; the slowest of these |
| pyright | Microsoft's, behind VS Code's Pylance; fast, and infers more than mypy does |
| basedpyright | A fork of pyright with stricter checks and Pylance's editor features[^basedpyright] |
| ty | Astral's, in Rust; in beta on `0.0.x` versions, with diagnostics that may change between any two releases[^ty] |
| pyrefly | Meta's, in Rust; declares itself stable, releases monthly, and checks NumPy and SciPy among others[^pyrefly] |
| zuban | In Rust, by the author of Jedi; offers a mypy-compatible mode, and is AGPL-3.0 or commercially licensed[^zuban] |

Checkers disagree at the edges, so a project picks one and treats its verdict as the
definition. pyrefly's use on NumPy and SciPy matters for numerical code, because those are the
stubs such a library leans on hardest.

Runtime checkers, beartype and typeguard among them, check values as the code runs, typically
under the test suite. Numerical code rarely uses them, because the checks sit on hot paths.

## How strictly

Gradual typing checks what is annotated and ignores the rest, and strictness is raised a module
at a time: mypy's `[[tool.mypy.overrides]]`, pyright's `strict` list. Two settings keep the
suppressions honest. mypy's `warn_unused_ignores` reports a `# type: ignore` that no longer
suppresses anything. Ruff's `PGH003` rejects a bare `# type: ignore` in favour of one naming the
error code, which is
[Document a rationale for every disabled lint rule](../principles/document_a_rationale_for_every_disabled_lint_rule.md)
applied to types.

**Where the checker runs is its own decision**, and
[Run a type checker against the project environment in CI, not in an isolated hook](../principles/run_a_type_checker_against_the_project_environment_in_ci_not_an_isolated_hook.md)
makes the case for CI.

## How an interface is typed

**Nominally**: a class is compatible because it inherits from the interface, an abstract base
class made generic over its parts. **Structurally**: a `typing.Protocol` accepts any class with
the right methods, with no inheritance at all. Structural typing suits an interface that outside
code should satisfy without depending on the library; nominal typing costs nothing extra where
outside code subclasses the interface anyway.

A method returning "the same kind of object" has three spellings. `Self` returns the caller's
own subclass. An explicit type parameter, `-> A`, ties the return to a parameter of the class.
The base class, `-> VectorArray`, is the loosest: correct, and silent about which subclass comes
back.

## Arrays

A bare `np.ndarray` names neither element type nor shape. `numpy.typing.NDArray[np.float64]`
adds the element type, which is what separates a real result from a complex one. Shape typing
exists in third-party libraries such as jaxtyping, and in pyrefly's experimental tensor shape
checks for PyTorch[^pyrefly], but neither is routine for NumPy code.

## The pyMOR pull request, placed

Read on 2026-11-17, whilst the pull request was open and its CI failing[^pymor-2680].

- **Where**: inline.
- **Syntax**: the newest available. PEP 695 generics, `VectorArray[S, I]` and
  `VectorSpace[A]`, and `type Ind = list[int] | slice | None`. That puts the floor at 3.12,
  whilst `pyproject.toml` still declares 3.10 and CI still tests it, which is why the 3.10 jobs
  cannot pass.
- **Checker**: none in the repository. Neither `pyproject.toml` nor `.pre-commit-config.yaml`
  runs one, so the annotations are, for now, what
  [A declared-but-inert config documents intent, not enforcement](../principles/a_declared_but_inert_config_documents_intent_not_enforcement.md)
  describes. The `# type: ignore` comments suggest a checker run locally.
- **Strictness**: `PGH003` is switched off, so bare `# type: ignore` comments are allowed.
- **Interface**: nominal, which fits, because external solver bindings already subclass
  `VectorArrayImpl`. `Self` appears on the `Impl` methods and, deliberately, not on the public
  `VectorArray` ones, which return the base class.
- **Arrays**: bare `np.ndarray` throughout.

One change in it is not an annotation. `numbers.Integral` and `numbers.Number` checks became
`int` and `int | float | complex`, which changes what the code accepts at runtime, not only
what a checker believes.
