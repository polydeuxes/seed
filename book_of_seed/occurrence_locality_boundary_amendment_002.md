# Occurrence Locality Boundary Amendment 002

## Status

Proposed. Adds `06.Standing.B` to
`06-standing-and-projection/events-facts-and-standing.md`.

## What was already established, and was not amended

- `01.Standing.E.1` already requires an applicability determination to preserve
  the act's *"purpose, scope and locality, authority, participants and roles,
  consumer context, and preserved limits."* Before this amendment, both `scope and
  locality` and `consumer context` appeared exactly once in the numbered chapters —
  in that list — and neither was defined anywhere. They were named coordinate slots
  with nothing stated about what fills them.
- `06.Standing.A` already bounds current standing *"within the applicable Seed,
  workspace, corpus, question, authority, projection rule, confidence limit, and
  Unknown boundary."* `workspace` is one member of that list, and is the only
  occurrence of the word in any numbered chapter.
- `02.Acts` already holds that an act *"consumes the subject plus the warrant and
  conditions appropriate to that occurrence and produces or preserves an
  attributed result."*

## What was missing

Nothing established that occurrences within one workspace may belong to distinct
bounded groups, or that such grouping is carried rather than derived. The
implementation has recorded `session_id` on every event for a long time; the Book
has never carried the distinction. `session` appears 199 times across the Book's
recovery documents and **zero** times in any numbered chapter.

Four prior documents investigate sessions — `bounded_session_reads_001`,
`console_session_lifetime_001`, `session_standing_continuation_experiment_001`,
`session_standing_continuation_investigation_001`. All four concern projection
mechanics and cost: quadratic rebuilds, forward folds, `as_of_event_id`
continuation. None asks whether the distinction is irreducible.

## Repository witnesses examined

`/dev/shm/lab/sixteen.db`, the sixteen-work store, rebuildable from `d5ce9cb`:

```
597,736 events across 18 sessions
120     session pairs whose event ranges interleave
33      session switches walking the log in recorded order
17      switches would indicate perfectly contiguous blocks
```

Occurrences of one session are not contiguous in the ledger. Membership is
therefore not any range of the recorded order, and removing the coordinate
destroys the information rather than making it costly to recover.

`seed_runtime/assertion_comparison.py::record_positional_result_comparison_layer`
takes `source_session_ids` as its scope and `recording_session_id` as its target.
That act consumes from one set of localities and records into another. Without
the coordinate it cannot state what it consumed, cannot distinguish that from
what it produced, and on a later run would consume its own output as though it
had been given. That is a fidelity failure, not an inconvenience.

## Clause added

`06-standing-and-projection/events-facts-and-standing.md`, new `06.Standing.B`.

## On the word

The clause establishes **locality**, not **session**. `01.Standing.E.1` already
names `scope and locality`, so locality is the Book-native word this distinction
was reaching for, and adopting it fills a named slot rather than importing a new
noun.

`session` was also the wrong name for what the evidence shows. The word implies a
live interaction with a consumer. The measured interleaving comes from
measurement sessions with no consumer and no interaction at all, so naming the
coordinate `session` would claim more than the witness supports. `session_id`
is recorded in the clause as an implementation witness, which is what it is.

This is a decision the reviewer should accept or reject explicitly, since the
conversation that produced this amendment used `session` throughout.

## What the amendment does not establish

- **It does not make a locality a subject.** It owns nothing, performs nothing,
  and carries no standing of its own. `06.Standing.A` remains the only account of
  how support becomes standing, and it locates that in the consuming act.
- **It does not establish a lifetime, container, coordinator, or current
  context.** Nothing here warrants a locality that begins, ends, holds material,
  or governs what is active.
- **It does not warrant projecting standing for a locality.**
  `seed_runtime/operator_session_standing.py` currently projects standing *for a
  session*. This amendment does not support that, and the gap between them should
  be resolved rather than read as endorsement.
- **It does not require a producer or producing act.** A carried coordinate needs
  none, as scope and authority need none.
- **It does not establish ordering authority.** Locality does not rank, sequence,
  or prioritize occurrences, and recency remains distinct from membership.
- **It does not establish that operator interaction is a locality.** The witness
  is measurement work. That the same coordinate serves a live operator exchange is
  expected but unmeasured, and remains **Unknown** until an exchange is recorded.

## Falsification target

A store in which every locality's occurrences are contiguous in recorded order
would show membership recoverable from position, and the clause would be carrying
a coordinate that derivation could supply. The measured store refutes this at
120 interleaving pairs; a pipeline that never interleaves would not refute the
clause but would narrow where it earns its keep.
