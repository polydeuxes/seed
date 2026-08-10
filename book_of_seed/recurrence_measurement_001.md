# Counting exchanges over recorded occurrences, corrected three times

Runtime amended narrowly. No Book amendment.

## What #2429 got right, and is kept

Seed computes what was a reader's tally in `#2420`. Three results, each proven
from Seed-held occurrences, partitioning the exchanges. The result stands.

## Three corrections

### 1. No new Act, and no new Responsibility

**[measured]** `#2429` wrote `cohort-measurement-over-recorded-comparisons` into
the `responsibility` of every record.

**[measured]** `#2351` recovered declared measurement and states that no new
act, noun, or grammar is required; recurrence and count are already its
findings.

**[inference]** What changed in `#2429` was the **subject** — recorded
occurrences instead of preserved material — not the Act. A distinct record shape
is warranted, because `#2399` established that a downstream shape must not
decide an upstream subject. A distinct Responsibility is not. The recorded
responsibility is now `declared-measurement`, and the subject is named
separately.

### 2. The result stood on Evidence it did not record

**[measured]** The result needs both recorded kinds. Comparisons say which
exchanges measured the distinction; measurement occurrences say which measured
the coordinate at all. `#2429` recorded only the comparisons in
`consumed_event_ids`, while using measurement occurrences to establish two of
its three result sets.

**[inference]** `#2419` holds that preservation must not erase what a result
stood on. Every occurrence of both kinds that produced the result now travels,
and a test asserts that the support contains both kinds and one measurement per
bounded exchange.

### 3. "Under the declared rule and scope" while dropping the scope

**[measured]** `#2429` grouped on left representation, equivalence rule and
measured position, and described the result as recurring "under the declared
rule and scope". `counting_scope` was not among the three. Two measurements
declaring different scopes were aggregated as one.

**[measured]** `01.External:28` requires a recurrence assertion to disclose the
representation measured, the rule by which sameness was determined, and the
bounded scope.

**Grouping now uses the whole declared identity:**

```text
  representation_measured        measured_position
  measured_left_representation   measurement_form
  equivalence_rule               counting_scope
```

A test measures the same material under two declared scopes and requires two
findings with different counts, not one.

## Vocabulary

**[inference]** `cohort`, `population`, `body`, `survey` and `exposed` were
statistical vocabulary the grammar never needed, and `survey` in particular
creates an Act-shaped shadow — the mistake `#2399` corrected when an output
shape began deciding what the upstream act was.

```text
  cohort measurement      ->  declared measurement over recorded occurrences
  Cohort                  ->  RecurrenceFinding      (a record shape)
  cohort_size             ->  recurrence_count
  population              ->  bounded_exchanges
  carried_by              ->  measured_in
  exposed_without_it      ->  measured_without_distinction
  coordinate_not_exposed  ->  coordinate_not_measured
  surveyed_occurrences    ->  recorded_*_occurrences
  population_scope        ->  counting_scope
```

**[inference]** `carried_by` was the subtlest: `carry` is legitimate — `#2419`
says inputs preserve coordinates "as that input carries them" — but
`carried_by` reads as a relation between an exchange and a distinction.
`measured_in` says what Seed established and stops.

The sentence the act reports is now:

```text
  ('of', 'the') recurs in 15 bounded exchanges at displacement 1
  under byte-for-byte equality within <declared counting scope>
```

**[measured]** `independently preserved` is kept as that exact qualified
construction, and the refusal that it is not source independence is kept with
it.

## Two smaller corrections

**[measured]** `#2429`'s payload said the scope was "the bounded exchanges
appearing in the consumed comparisons" and "which bodies were supplied to this
Seed", while the code built it from measurement records and its own test added
an exchange through a measurement alone. The recorded scope now states what was
consumed, and says that an exchange with no relevant recorded measurement does
not appear at all.

**[measured]** `#2429` offered a session-local mode. Comparisons are recorded
under one exchange's session while consuming a finding from another, so
filtering to one session would report the other exchange as never having
measured the coordinate. The mode is removed rather than repaired.

## Four further corrections

### Responsibility is not the Act

**[measured]** `#2430` removed an invented Responsibility and wrote
`declared-measurement` in its place.

**[measured]** `#2423` recovered that declared measurement has **no production
owner in active law**: "the act that would produce the finding has no named
owner", with `production owner: none found` set against operational
measurement's named one.

**[inference]** So the replacement asserts the owner that recovery says is
absent. The same slot, filled differently wrong. The coordinate now reads
`unrecovered; declared measurement has no production owner in active law
(#2423)`, and a test asserts it is not `declared-measurement`.

**[measured]** The contamination is inherited rather than invented.
`preserved_material_measurement.py:246` records
`declared-measurement-over-preserved-material` and
`measurement_self_survey.py:140` records
`declared-survey-over-recorded-measurements`, still carrying `survey`. Both are
merged and outside this branch; they are recorded here rather than silently
widened into.

### A count of one is not a recurrence

**[measured]** `01.External:28` lists exact equality, **count**, **recurrence**,
prefix occurrence, declared-predicate result and adjacency as separate findings.

**[measured]** `#2430` named the shape `RecurrenceFinding` and rendered a count
of one as `recurs in 1 bounded exchanges`.

**Now:** `exchange_count` is a finding at any value; `recurrence_established` is
true only above one, and the sentence follows it.

```text
  ('a', 'thing')  was measured in 1 bounded exchange of 4 declared, at ...
  ('a', 'word')   recurs in 3 bounded exchanges of 4 declared, at ...
```

### The bounded scope is declared, not swept

**[measured]** `#2430` built `bounded_exchanges` from every measurement
occurrence in the workspace, so an exchange entered the denominator by having
measured anything at all. A measurement of `"nothing"` set the denominator of a
finding about `"a"`.

**[inference]** That is workspace visibility choosing Applicability.
`01.External:28` requires a recurrence assertion to disclose the bounded scope
within which occurrences were counted, and a scope the act discovers is not a
scope it discloses. `bounded_exchanges` is now a required argument and an empty
declaration is refused.

**[inference]** Repairing only the *provenance* of the swept set would have made
the citation honest and left the boundary chosen by control flow. That was the
deeper defect and the reason this correction is not just an Evidence fix.

### What places an exchange in a result travels with it

**[measured]** `#2430` cited only occurrences matching the grouped identity, so
an exchange could be placed in `coordinate_not_measured` by an occurrence absent
from `consumed_event_ids`.

**Now:** every occurrence that establishes where a declared exchange stands
travels, pinned by a test that adds an exchange through an unrelated measurement
and requires that measurement in the support.

## What this does not establish

**That recurrence is a relation.** `01.Standing.D` refuses relation standing to
co-presence, and recurrence is co-presence counted. The `Unknown` every
cross-exchange comparison produces is untouched.

**That the widest recurrences are the meaningful ones.** They are function words
under a byte-equality rule. `#2408` established that a reader's categories
predict nothing about these sources, and none is assigned.

**That the count means anything beyond what it consumed.** It reports the
bounded exchanges among the occurrences this measurement read.

**That the corrected grouping produces `#2429`'s numbers.** It is a narrower
grouping and may not. The rerun result is reported as what it is.
