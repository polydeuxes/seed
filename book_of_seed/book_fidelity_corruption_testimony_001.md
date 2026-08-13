# Book fidelity: corruption testimony 001

Testimony about the Book, gathered while doing other work between `#2499` and
`#2508` on 2026-08-12. **No entry here is a repair.** Each records something
found, what establishes it, and what a repair would have to decide. Several
were found only because a clause merged the same day made them visible.

The Book is one witness. Where an entry says the Book asserts something false
about the repository, the repository was checked; where an entry says a word
has no owner, the whole Book was searched.

---

## 1. The implementation witness is almost entirely gone

```
Book → code    20 of 22 anchors in numbered chapters point at deleted files
code → Book     2 of 32 runtime modules are cited anywhere in numbered chapters
survivors      seed_runtime/events.py   seed_runtime/__init__.py
```

Absent, still cited: `state.py`, `facts.py`, `evidence.py`, `observations.py`,
`models.py`, `constitutional_pipeline.py`, `projection_store.py`,
`explanations.py`, `read_model_ownership.py`, `inquiry_orientation.py`,
`source_navigation.py`, `constitutional_view_selection.py`,
`examination_work_selection.py`, `candidate_external_grammar.py`,
`architecture_conformance_audit.py`, `inquiry_artifacts.py`,
`ownership_discrepancies.py`, `question_surface_inventory.py`,
`shared_explanation_rendering_projection.py`,
`constitutional_view_composition.py`.

Meanwhile the entire live measurement stack, `support_basis.py`,
`material_availability.py`, `system_material.py`, `operator_presentation.py`
and the rest appear in no chapter.

**A repair must decide** whether an anchor section without a live witness is
removed or refilled. Removal is honest and loses the Book's claim to be
grounded; refilling requires judging what currently witnesses each clause,
which is not mechanical. Removal-only first is the safer order, because a
wrong anchor is worse than no anchor.

## 2. `05.Testimony` describes a deleted module in the present tense

> The current repository compresses Observation intake, Evidence construction,
> claim-field normalization, optional Fact artifact construction, and fact event
> emission in `ObservationIngestor`.

All three of that chapter's cited witnesses — `observations.py`, `evidence.py`,
`facts.py` — are absent. This is not a stale citation but a false assertion
about the repository's current state, inside the chapter that owns fact
establishment.

The sentence is also the clearest surviving record of what the deleted
implementation compressed, so a repair should preserve the compression list
while withdrawing the present tense.

## 3. `express*` remains in the operator-goal road, without a usable replacement

`#2507` removed nine occurrences where active law had its own word. Twenty-eight
remain, almost all one construction: *the warranted meaning relation that
candidate G expresses bounded goal proposition M*.

They were left because the verb **is** the relation there, and both verbs
`01.Standing.E` now offers are already taken inside that chapter: `represents`
means *presented alternative A represents candidate G*, and `identifies` means
the identification act. Substituting either puts two different relations under
one verb in one paragraph.

**A repair must recover a verb for that relation**, not substitute one. That the
word persisted there may be because the chapter had no free word left.

## 4. `construction-and-establishment`'s bounded resolution is one ~250-word sentence

It carries the whole BOGE chain — presented alternative, closed choice, emission,
response capture, comparison, identification, meaning relation, applicability,
admission, establishment — in a single sentence. Dense compound sentences hide
ungrounded claims in their seams. Nothing is asserted here about whether this one
does; it has not been read clause-by-clause, and it should be before anything is
built against it.

## 5. `aggregation` in `01.External.E` is unexamined

> consumer purpose governs lawful reliance, acceptable aggregation, and
> acceptable representational loss.

Flagged, not accused. The word has the profile that has repeatedly turned out to
be contamination, and it sits in a clause about consumer purpose where it could
be read as licence for exactly the collective-standing move `01.Standing.D`
refuses. It has not been established that it names nothing.

## 6. Vocabulary that entered as implementation placeholder and was never audited

The operator records that `assertion`, `workspace`, and `session` were not
coined deliberately — they came out of generated code filling a void where the
grammar had no term. The responsibility test then sorted them differently:

```
assertion   owner, producing act, established standing — earned it.
            But never audited AS VOCABULARY. One document exists and it
            concerns relation assertions, not the word. It carries
            01.Standing.D.1, D.2, 01.Uptake.A and everything built today.
session     0 occurrences in numbered chapters, 199 in recovery documents.
            Four dedicated investigations, all about projection cost, none
            asking whether the distinction is irreducible. #2504 established
            the distinction under a different name: locality.
workspace   1 occurrence in numbered chapters, in 06.Standing.A's boundary list.
governor    0 occurrences anywhere in the Book. Session shorthand only.

Counted before this document existed. This document uses both words to
describe them, so re-running the count now returns a larger number that
this file is responsible for.
```

**`assertion` is the largest unexamined assumption in the Book.** It passes the
test on inspection; it has never been put through the pass that removed
`candidate convergence`.

## 7. Two clauses leave Unknowns that later work has drifted past

Recorded so a repair does not read them as settled:

- `06.Representations`: *"Whether forming a representation names an Act distinct
  from the exact Act that forms it remains **Unknown** unless separately
  established."* Any outward-spine design naming a formation Act establishes
  what this leaves open.
- `#2286` left the Compare/Standing crossing *unrecovered, not excluded*, and
  `01.Standing.D.2` deliberately does not settle it. An improvement loop that
  carries Standing into a Compare would establish it silently.

## 8. `06.Standing.A` was a junk drawer, and is two nouns lighter

`candidate convergence` (`#2502`) and `context views` (`#2503`) are gone. Both
were undefined, unowned, and named things that no longer existed —
`context_views.py` was deleted by `#1880`, which touched no Book file.

Recorded here because the mechanism is general: **code was withdrawn and the
Book was not checked.** That is not a subtle failure and it will recur
mechanically. Every entry in section 1 is the same mechanism.

---

## What this testimony is not

It does not establish that any listed clause is void, that any listed word is
contamination, or that the Book should be trusted less than the repository. The
repository has no comparable record of its own drift, which is why this document
can list the Book's and not the code's.
