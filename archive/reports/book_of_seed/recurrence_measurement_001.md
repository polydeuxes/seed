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

### Declaring a Scope does not establish its members

**[measured]** `#2431` accepted any name in `bounded_exchanges`. A declaration
of `workspace:w;session:ghost` placed `ghost` in `coordinate_not_measured`, with
no Evidence that any such exchange occurred.

**[inference]** Having just removed *workspace visibility choosing
Applicability*, `#2431` replaced it with *caller declaration creating a
subject*. The correct split:

```text
  declaring the measurement Scope   chooses among established exchanges
  establishing an exchange          a recorded occurrence carries it
```

A declared exchange with no recorded occurrence is now refused.

**The first attempt picked the wrong witness.** It established existence from
`dimensions.scope_locality` — the coordinate this same report leaves Unknown two
sections down — and read `ledger.list(workspace_id)` to gather it, reinstating
the whole-workspace-read shape `#2416` removed and measured at 20x. Both are
corrected:

```text
  a bounded exchange IS      the recorded session boundary
  established by             a recorded occurrence within it
  read through               ledger.list_session(workspace, session)
  costing                    one bounded read per declared exchange
```

**[measured]** `session_id` is a top-level recorded coordinate of every event.
`scope_locality` is a payload description a record can say anything in, and a
test now writes `scope_locality = ...ghost` into an occurrence recorded under
`s1` and requires `ghost` to remain unestablished.

**[measured]** A second test traces the durable ledger's SQL and requires every
read to name a session, one per declared exchange, with none sweeping the
workspace. It is asserted on SQLite because the in-memory `list_session` is a
comprehension over the workspace list, as `#2416` recorded — the in-memory
ledger cannot witness this.

**[inference]** Bounding the reads also bounded the act: the module no longer
reads the workspace at all, where `#2430` and `#2431` gathered every comparison
and measurement in it.

**[measured]** One existing test was passing for the wrong reason and now fails
correctly — it declared four exchanges that never existed in its ledger, and
reached the intended refusal by a different route.

### A test that asserted nothing

**[measured]** `#2432` followed its refusal test with:

```python
findings = measure_exchange_counts(..., bounded_exchanges=("s1",))
assert all(f.bounded_exchanges == ("s1",) for f in findings)
```

commented "the established ones alone are fine". Declaring one exchange yields
**zero** findings — a comparison consumes two, so every comparison involving
`s1` has its other input outside the declared Scope and is correctly rejected —
and `all([])` is `True`.

**[inference]** The assertion was green because it ran over nothing. The
refusal it followed was real; the reassurance after it was not. Split into
three: the refusal, an acceptance asserted on a result that exists, and the
empty case recorded as correct behaviour that no assertion over the result can
witness.

## Two questions this exposed, and did not answer

### Producer, recovered as its own coordinate

**[measured]** `#2423` established `production owner: none found` for declared
measurement — an **owner**, a Responsibility. That was then reported, here and
in three other places, as though declared measurement had no **Producer**.

**[measured]** They are different coordinates. `01.External:31` requires a
candidate to preserve "each applicable **producer**, source-role,
formation-occurrence, scope, authority, and provenance dimension", listing
producer beside provenance rather than as it. `01.Kinds:73` keeps represented
provenance and verified producer occurrence apart. `02.Acts:10` and `:25` treat
producer occurrence as its own subject.

**[inference]** Letting *owner* swallow *Producer* is the compression this
project punishes elsewhere. The partial shape is ordinary:

```text
  Producer          this Seed
  Producer Evidence the exact recorded producing occurrence
  Act               declared measurement
  result            count finding
  Standing          measured
  Responsibility    Unknown
```

**[measured]** `06.Constructors:13` both licenses and limits it: a live producer
return is not durable producer-to-result Evidence *unless recorded or
represented*. The findings are recorded, with digests, so the condition is met —
and the Producer rests on the recorded occurrence rather than on a function
having run.

**[inference]** The occurrence is Evidence **for** the Producer, not the
Producer. Recording `producer: evt_X` would collapse a participant coordinate
into an occurrence coordinate — the same compression in different nouns. Four
tests pin the distinction, including that the producer is neither the event id
nor the provenance string.

**[inference]** An earlier objection of this report's author — that `this Seed`
is constant and therefore vacuous — does not survive. A coordinate is not
meaningless because one bounded system currently has one value; it distinguishes
the moment one Seed egresses to another, and that is the topology being built
toward.

### The Responsibility that is still Unknown

**[measured]** The same event now records:

```text
  responsibility   unrecovered; declared measurement has no production owner
  standing         measured
```

**[Unknown]** Whether an Act whose producing Responsibility is unrecovered may
lawfully produce Standing at all. Under a Responsibility-first topology the
answer is plausibly no, and amending from that intuition would be exactly the
move this session keeps catching.

**[measured]** The question reaches backward. `preserved_material_measurement`
and `measurement_self_survey` record `measured` Standing under the same
unrecovered **Responsibility**, so this is not a property of the new module.

**[measured]** That sentence read "unrecovered producer" until this correction.
It is the compression this report's Producer section removes: `#2423`
established that no production **owner** is recovered, and the Producer is a
separate coordinate that was never missing.

**[inference]** Making the contradiction visible is worth more than resolving
it by inventing an owner. It may mean the whole measurement campaign has been a
useful witness implementation running ahead of the Responsibility that would
make its findings Seed's Standing — which matters before Acquisition Seed
depends on them.

### `scope_locality` may be occurrence locality, not claim Scope

**[measured]** `record_measured_count` sets
`dimensions.scope_locality = workspace:w;session:<the session it was appended
under>`, while the finding's declared Scope is the N bounded exchanges. The
comparison recorder does the same.

**[Unknown]** Whether `scope_locality` names where the occurrence happened or
what the record asserts about. If a consumer reads it as claim Scope, that is a
compression:

```text
  where the record occurred  !=  Scope of what the record asserts
```

Not folded into this correction, because a coordinate used by several recorders
should be recovered rather than reinterpreted in one of them.

### The sweep, and a count that was not checked

**[measured]** `#2439` said the owner/Producer compression had been reported
"here and in three other places". A sweep of every report mentioning a missing
production owner finds **one** surviving statement — the line corrected just
above. `#2423`'s own text says "production owner" and "no named owner"
throughout, which is accurate, and the remaining occurrences quote the runtime
string, which also says owner.

**[inference]** The claim of three was itself unverified: a count asserted in
the middle of a correction about unverified claims. The compression was real and
narrower than reported.

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
