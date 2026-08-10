# Recurrence across bounded exchanges, and #2429's over-reach corrected

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
