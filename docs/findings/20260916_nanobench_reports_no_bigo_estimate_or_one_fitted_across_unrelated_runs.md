---
type: Finding
title: nanobench reports no Big-O estimate, or one fitted across unrelated runs
description: complexityN() scales a run but prints nothing on its own, and the fit it feeds spans every
  run registered on the same Bench, including ones measuring different work.
tags:
- finding
- nanobench
- benchmarking
- performance
- cpp
status: stable
stale_after: '2027-03-16'
generated:
  by: opencode/claude-opus-5
  at: '2026-09-16T11:46:13Z'
sources:
- id: nb-tutorial
  resource: https://github.com/martinus/nanobench/blob/master/src/docs/tutorial.rst
  title: 'nanobench tutorial: asymptotic complexity'
  last_modified: '2026-09-16'
---
**Versions**: [nanobench](https://github.com/martinus/nanobench) as documented in
September 2026.

## The symptom

A benchmark file is written to measure how a solver scales, each run tagged with
its problem size:

```cpp
for (const int n : {10, 20})
{
    auto prep = PrepareModel(n);
    bench.complexityN(n * n).run("stage_1 with n=" + std::to_string(n), [&] { ... });
}
```

It compiles, it runs, it prints a timing table, and it prints no complexity
estimate at all - whilst announcing in its own banner that it is estimating one.
Nothing warns, because nothing has gone wrong from nanobench's point of view.

## What it turned out to be

Two separate facts about the API, neither of them surprising once seen, and both
easy to miss because the failure is silent.

**`complexityN()` only tags a run; `complexityBigO()` computes and returns the
fit.** The fit is a value you print, not a side effect of running. The
tutorial[^nb-tutorial] ends its example with an explicit
`std::cout << bench.complexityBigO() << std::endl;`, and without that line the
scaling data is collected and discarded.

**The fit spans every run on that `Bench` object.** The tutorial is explicit that
a single `Bench` instance is reused across runs and that the object aggregates
their results. That is exactly what you want when the runs measure one operation
at ten sizes. It is not what you want when one file registers several unrelated
groups - a seepage solve, a stress-initialisation solve, a consolidation solve -
against the same `bench`, because they are then fitted together as though they
were one curve, and the output is a plausible-looking table of coefficients about
nothing.

A third thing is not a bug but limits what the output is worth: the tutorial fits
over ten sizes. Two points can be fitted by every candidate complexity exactly, so
a two-size sweep yields a ranking with no information in it.

## How to get past it

One `Bench` per operation being characterised, each with enough sizes to
discriminate, each printing its own fit:

```cpp
ankerl::nanobench::Bench stage_1;
for (const int n : {5, 10, 20, 40, 80})
{
    stage_1.complexityN(n * n).run(..., [&] { ... });
}
std::cout << stage_1.complexityBigO() << "\n";
```

Where the work is too slow to afford five sizes - which is the usual reason a
sweep ends up with two - drop the complexity framing rather than keeping a fit
nobody can trust, and report the absolute times per size. Two timings and their
ratio is an honest thing to publish; a ranked table of six complexity classes
derived from those same two timings is not.

## Takeaway

An API that separates "collect the data" from "compute the result" has a silent
middle state, and a banner printed by the benchmark itself is not evidence that
the benchmark does what the banner says. The neighbouring trap in the same file is
[A microbenchmark body must not mutate state that outlives one iteration](../principles/a_microbenchmark_body_must_not_mutate_state_that_outlives_one_iteration.md).
