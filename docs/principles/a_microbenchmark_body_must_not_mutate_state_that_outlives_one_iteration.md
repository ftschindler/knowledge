---
type: Principle
title: A microbenchmark body must not mutate state that outlives one iteration
description: A benchmark harness runs its body many times, so a body that mutates state prepared outside
  it measures the first iteration and then something else entirely.
tags:
- principle
- benchmarking
- performance
- testing
- software
status: stable
generated:
  by: opencode/claude-opus-5
  at: '2026-09-16T11:46:13Z'
---
**Claim.** The callable a benchmark harness times is run an unknown number of
times, chosen by the harness at runtime. It must therefore be idempotent with
respect to anything that survives between iterations: whatever it mutates has to
be created inside it, or restored before it returns. A body that mutates
expensive state prepared once outside the measured region times the first
iteration honestly and every subsequent one against a different input.

**When to apply.** Any harness that scales iteration count to reach a target
sample size, which is all of the usual ones: nanobench, Google Benchmark,
Criterion, `timeit`. The pattern that triggers it is the natural one, which is
what makes it worth a page. Setup is slow and you do not want to measure it, so
you hoist it out of the lambda and capture it by reference.

```cpp
// BAD: solve() mutates `model`; iterations 2..N solve an already-solved model
auto model = prepare(n);
bench.run("solve", [&] { solve(model); });
```

**Why.** The two failure modes pull in opposite directions and neither announces
itself.

- Work that is *idempotent-cheap* reports a time somewhere between the real cost
  and nothing, weighted by an iteration count the harness picked. A solver that
  finds its results already present and returns early is the case, as is a cache
  that is cold once and warm thereafter. The number then moves when the machine
  gets faster for unrelated reasons.
- Work that *accumulates* reports something worse than the truth, and drifts with
  the sample size. Appended results, growing containers, and a convergence path
  that starts from the previous answer all do this.

In both cases the harness reports a tight error percentage, because the
measurement is precise. It is the thing being measured that is not what you
named.

**How.** Prefer constructing the state inside the body and paying for it, which
is honest and often fine when the measured work dominates. Where setup genuinely
dwarfs the work, three options, in order of preference:

1. Use the harness's per-iteration setup hook if it has one: Criterion's
   `iter_batched`, Google Benchmark's `PauseTiming`/`ResumeTiming`.
2. Restore the mutated state explicitly at the end of the body, and accept that
   the restore is inside the measurement.
3. Pin the harness to a single iteration and a single epoch, and accept the much
   wider error bars.

Pinning is the weakest of the three, because it gives up the repetition the
harness exists to provide. It is also the only one available when the state is a
large object with no cheap reset.

**How enforced.** Read every captured reference in a benchmark body and ask what
the body writes to it. A body whose captures are all `const`, or all constructed
within, is fine by construction; anything else needs an argument.

Kin to
[A sandbox test must use the live working-tree source and rebuild fresh each run](a_sandbox_test_must_use_the_live_working_tree_source_and_rebuild_fresh_each_run.md),
which is the same trap in a test harness: a run that reuses state from the last
one produces a number, and the number is about the wrong thing.
