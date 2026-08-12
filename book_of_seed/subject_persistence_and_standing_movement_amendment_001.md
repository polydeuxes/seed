# Subject Persistence and Standing Movement Amendment 001

## Status

Canonical amendment record. This record documents the cross-examination that amended the Book; it is not an independent source of constitutional authority apart from the clause amended below.

## What was already established, and was not amended

The investigation began expecting a large amendment. Most of it was already law, and the implementation violates law that exists rather than lacking law.

- `01.Standing.D` already refuses higher-order identity to multiplicity. *"Co-presence or multiplicity does not by itself establish membership, collection standing, relation, topology, ordering, selection, priority, focus, shared purpose, or higher-order identity."* Measuring an arrangement of two representations therefore never established the arrangement as a subject. No clause was needed to forbid it.
- `01.Standing.D.1` already bounds an Act to *"only the bounded Standing warranted by that Act's Evidence and Authority"*, and already states that *"Further movement requires an applicable responsible occurrence with its own Act, Evidence, Scope, Authority, and limits."* Movement was established; nothing was carrying it out.
- `05.Testimony:16` already admits that *"One Observation may support a bounded Fact when the Fact asserts no more than the source-relative observation can support."* No maturity gate existed to remove.
- `05.Testimony:29` already holds that *"comparison occurrence does not erase any input's standing."*
- `01.Standing.E` already holds that *"Later evidence may revise relation standing without mutating participant identity."*
- `01.Uptake` already separates applicability, admission, and consumption, and `01.Uptake.A` already refuses automatic revision on new availability.

## What was missing

One thing. No clause established **what a later Assertion's applicability is considered against**.

`01.Standing.D.1` requires an applicable responsible occurrence for movement. It does not say whether applicability is considered with respect to the current Standing concerning a subject, or with respect to every preserved Assertion concerning it. Nothing in the Book chose, so an implementation was free to choose the second, and did.

A second gap sits beside it. `05.Testimony:29` protects a Compare's *inputs* from having their standing erased. Nothing protected the *subject compared* from being replaced by the subject of the result.

## Repository witnesses examined

Measured over a store of sixteen bodies at 1,200 lines each, 597,736 occurrences.

- `seed_runtime/assertion_comparison.py`: `record_positional_result_comparison_layer` enumerates comparisons by grouping result Assertions by carried subject and taking `combinations(..., 2)` within each group. For a subject appearing in `k` bodies this is exactly `C(k, 2)` comparisons.
- The store contains 76,004 recorded Compares over 19,488 distinct compared subjects, with **76,004 distinct input pairs and zero repeated pairs**. The implementation duplicates no comparison; the pairwise population is what the enumeration is.
- The compared subject does not survive. A Compare carries `compared_subject` as an ordered pair; the signature occurrence consuming it carries `assertion_subject` = `positional_result_coordinate_distinction`, and the string `ordered_pair` does not appear in a signature payload. Seventy-eight Compares concerning `("from", "the")` produce seventy-eight signature Assertions about the shape of a comparison surface.
- Nothing accumulates about a single representation. Across 430,177 recorded findings, **zero** stand on a premise concerning the same single representation; all 385,564 premise relations cross from a single representation to a pair. The representation `from` has 13 findings about itself and appears in 2,524 findings about pairs containing it.

## Consequence measured

Comparisons grow as `C(k, 2)` in the number of bodies a subject appears in; movement against current Standing would grow as `k`.

```text
   16 bodies        76,004 compares       55,492 movements     1.4x
  100 bodies     3,727,464 compares      337,268 movements    11.1x
 1000 bodies   402,943,248 compares    3,465,836 movements   116.3x
```

At the scale every experiment has run at, the two are nearly indistinguishable, which is why the shape survived. The projection establishes the size of the difference; it does not establish that the movement topology is lawful, which is what the amended clause governs.

## Clause amended

`01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`, new `01.Standing.D.2`.

## What the amendment does not establish

- **It does not establish a new Act.** Applicability, Compare, and Standing movement remain three responsibilities with three owners. An earlier draft of this finding called them "the same missing act"; collapsing them would produce exactly the umbrella that `04.Examination` was excised for being.
- **It does not permit accumulation.** Applicability is still required, and still establishes only that an Assertion may bear on Standing.
- **It does not promise that Standing improves.** Movement may be almost nothing. The amendment permits poor Standing to exist and to persist as the same subject; it warrants no trajectory.
- **It does not license discarding preserved Assertions.** Current Standing is what a later Assertion is considered against; the Assertions that warranted it remain preserved and recoverable, exactly as `B` carries a bounded history forward without erasing it.
- **It does not promote any composite.** `01.Standing.D` governs that, unamended.

## Falsification target

Today, across roughly 430,000 findings, no finding stands on a prior finding concerning the same single representation, and no Standing concerning a compared subject survives its Compare. An implementation conforming to this clause should be able to exhibit both.
