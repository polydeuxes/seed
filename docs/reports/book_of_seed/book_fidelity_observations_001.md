# Book fidelity observations 001

Observations about the Book, gathered while doing other work between `#2499`
and `#2508` on 2026-08-12. **No entry here is a repair**, and not every entry
establishes a defect: each says for itself whether it records a defect, a
suspicion, an Unknown, or a target for investigation. The earlier title said
corruption, which pre-classified entries that explicitly decline to accuse.

**Every count below was measured against commit `b75785bf6b2f`** and is a
repository observation, not a durable fact. The repository moves; a number here
read later is testimony about that commit and nothing else. Recording exact
counts without their as-of boundary is the same present-tense mistake §2
accuses `05.Testimony` of making.

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
which is not mechanical.

*Proposed disposition, not an observation:* removal-only first, because a wrong
anchor is worse than no anchor.

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
assertion   load-bearing: carries 01.Standing.D.1, D.2, 01.Uptake.A and
            everything built today. Active law supplies its owner, its
            producing act, and its standing distinctions. A dedicated
            vocabulary audit has not occurred; one document exists and it
            concerns relation assertions, not the word.
session     0 occurrences in numbered chapters, 199 in recovery documents.
            Four dedicated investigations, all about projection cost, none
            asking whether the distinction is irreducible. #2504 established
            the distinction under a different name: locality.
workspace   used throughout 06.Standing.B, which #2504 added, and once in
            06.Standing.A's boundary list. An earlier draft of this entry
            said "1 occurrence in numbered chapters" -- counted before
            #2504 merged, and left standing after. This document became an
            instance of the drift it documents, in the same entry that
            cites #2504.
governor    0 occurrences anywhere in the Book. Session shorthand only.

Counted before this document existed. It uses the words it describes, so
re-running the counts now returns larger numbers this file is responsible for.
```

**`assertion` carries more than any other word here and has never been put
through the pass that removed `candidate convergence`.** Whether it would
survive that pass is not adjudicated here; a document recording that an audit
is missing should not pre-decide its outcome.

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

## 9. `premise_chain` describes itself as a support basis, and no longer is

`preserved_material_measurement.premise_chain` says:

> `05.Testimony:27` requires a consumed input's support basis to be preserved.
> This is that basis, recovered.

After `#2486` that is false. A support basis is an explicit scope, boundary,
selection rule and commitment. A chain of `premise_event_id`s records what one
finding stood on, which is a different thing from the basis of the population a
measurement consumed. Documentary, and it shows how fast the physiology outran
its own prose — the module gained `SupportBasis` and kept prose calling
something else by that name.

## 10. Three seams found in the measurement path itself

Recorded here because each is a Book question, not only a code one.

- **At the surveyed commit, no clause established that occurrence counts are
  distinguished by occurrence identity.** `01.External:28` requires the bounded
  scope to be disclosed and says nothing about identity, so the runtime refused
  a repeated occurrence on the strength of what `occurrences_examined` asserts.
  `01.External.E.1`, added in the same change as this observation, establishes
  it; the entry is kept because the gap is what produced the clause.
- **`counting_scope` is a required disclosure bound to nothing.** It is a
  non-empty string, and `#2508` proved only that declarations in one batch
  *agree* on it. Agreement among declarations is not fidelity to the population
  consumed. A measurement may declare "the complete English corpus" over three
  occurrences and nothing detects it.
- **`SupportBasis` scope is one workspace, one session, one kind, one
  boundary** — while `#2508` made a multi-locality consuming act lawful and
  `06.Standing.B` holds that same workspace is not same locality. A population
  spanning two localities cannot be described by one basis without either
  misstating the scope or silently narrowing the population.

## 11. `available` carries two meanings

`text_representation.available` records a *historical* outcome: at ingress, a
decoder formed a text representation. `#2496` governs a different thing —
present-tense material availability, asked of the holder and never read from the
ledger. One word carries both, which is enough to make a reader take the first
for a violation of the second. Recorded because the confusion cost real time.

## 12. Two words in `01.External` with no body behind them

Found while placing `01.External.E.1`, testing each nearby word against the
discriminator the lexical gate uses — whether active law defines the term, names
its occurrence, or names its boundary.

**`assimilation`** appears exactly once in the numbered chapters: in the *title*
of `01.External.B — Addressability without assimilation`. The clause body never
uses it, and says the thing plainly instead — external material may become
addressable "without becoming Constitutional Grammar." A title carrying a noun
its own body does not need.

**`aggregation`** is undefined and its runtime witness was withdrawn.
`01.External:28` says a consumer's purpose "separately governs lawful reliance,
acceptable aggregation, and acceptable representational loss." No clause states
what an aggregation is, names an aggregating occurrence, or names its boundary.
Meanwhile `recurrence_measurement.py` carries *"the old aggregate result's
Responsibility slot had been answering…"* and `tests/test_recurrence_measurement`
holds `test_the_old_aggregate_result_is_not_recorded_beside_the_assertions`.

So the shape is `context views` again: **the aggregate result was withdrawn from
the runtime and the word stayed in the clause.** It is also the word most likely
to be read as licence for the collective-standing move `01.Standing.D` refuses,
which is why it was flagged in §5 before this evidence existed. §5 said *flagged,
not accused*; this is the evidence, and it is now closer to accused.

Neither is repaired here. Both are single-word excisions of the kind `#2502` and
`#2503` performed, and both want their own scoped change.

## 13. Two words the operator saw first, and none of us caught

Recorded because the failure is instructive: both were sitting in plain sight
across a full day of vocabulary work, and four separate readings — three of them
explicitly hunting contamination — walked past them.

**`population`** appeared exactly once in the numbered chapters, in the *title*
of `01.Standing.D.2`, entered by this session's own amendment the previous day.
The clause body never used it and said the thing plainly. That is the identical
shape as `assimilation`, which the same session had excised hours earlier after
naming the pattern out loud: *a noun living in a title while the body says the
thing plainly.* Named, then committed.

**`support basis`** appears twice, both inside coordinate lists of what an
artifact must preserve — `05.Testimony:27` and `08.Emission:41` — and was never
defined. `support` as a verb is established 83 times; the noun phrase is not the
verb. `#2486` built a `SupportBasis` class on it and its module opened by citing
`05.Testimony:27` as though the clause supplied the structure. The clause names a
coordinate that must survive and says nothing about its shape.

Both are addressed in the same change as this entry: the title now says what the
body says, `05.Testimony.E` now bounds the coordinate without inventing a shape
for it, and the module records that its four parts are chosen rather than
recovered.

**Why it was missed** is the part worth keeping. Every reading was looking for
words that *sound* imported — `aggregation`, `assimilation`, `convergence`. These
two sound native, and one of them was native, in the sense that this session put
it there. A vocabulary audit that trusts its own recent output has a blind spot
exactly the size of its own recent output.

---

## What this testimony is not

It does not establish that any listed clause is void, that any listed word is
contamination, or that the Book should be trusted less than the repository. The
repository has no comparable record of its own drift, which is why this document
can list the Book's and not the code's.
