# Ordered-coordinate recurrence runtime implementation 001

Date: 2026-08-20

## Boundary

This change implements the smallest durable proof requested after
`32fa17be`. It does not amend the active Book, register an automatic runtime
dispatcher, run the sixteen-Book corpus, or restore the removed
equality-signature implementation.

The implementation vocabulary in this report and in Python names describes
the mechanics of this proof. It establishes no additional Seed grammar.

## Recorded road

The producer begins with the exact ordered source-position population already
carried by the direct pair-position Measurement result.

```text
adjacent ordered coordinates
        ↓
every exact pair receives separate Compare work
        ↓
complete same-content / difference result for that bound
        ↓
Measurement groups exact complete results
        ↓
count
        ↓
recurrence only where count > 1
```

Every recurrence finding preserves the exact result occurrences that support
it. An extension uses each such result and the next source-order coordinate.
It retains every prior Compare result reference and records only the Compare
relations introduced by the added coordinate.

For coordinate counts 2, 3, and 4, newly introduced Compare counts are 1, 2,
and 3 per production respectively. Previously recorded Compare work is not
reconstructed.

The first consumer accepts the complete recurrence Measurement result. It does
not accept a selected recurrence finding, coordinate role, or material value.
For every recurrent result population it exhausts:

```text
every coordinate role
        ↓
every exact carried material value at that role
        ↓
exact supporting production/source references
        ↓
count
        ↓
recurrence only where count > 1
```

Count 1 carries no negative recurrence coordinate.

## Positive witness

Supplied material:

```text
2+2=
3+3=
4+4=
```

The coordinate populations and durable growth were:

| coordinate count | produced bounds | new events |
|---:|---:|---:|
| 2 | 13 | 120 |
| 3 | 12 | 183 |
| 4 | 11 | 234 |

The complete internal Compare surface containing equal roles 0 and 2 recurred
three times. Its exact producing bounds begin at source positions 0, 5, and
10.

The corresponding-coordinate Measurement exhausted every role and material
under that exact production population. It established:

```text
role 1, material "+", count 3, recurrence
role 3, material "=", count 3, recurrence
```

The caller supplied neither role nor material value.

For the in-memory witness:

| phase | wall seconds | new events |
|---|---:|---:|
| source and direct position setup | 0.008 | 12 |
| internal Compare and recurrence producer | 4.120 | 537 |
| corresponding-coordinate consumer | 4.514 | 9 |
| complete proof | 8.643 | 558 total |

Three corresponding-coordinate Measurement results were recorded because
three complete internal result populations recurred. The table above isolates
the population containing the requested observer rendering.

## Control witness

Supplied material:

```text
2+2=
3-3#
4x4?
```

The same complete internal same-content/difference surface recurred three
times. Corresponding material did not:

```text
role 1: "+", "-", "x" each count 1
role 3: "=", "#", "?" each count 1
```

No recurrence finding was recorded for those six role/material subjects. This
separates recurrence of internal structure from recurrence of literal carried
material.

## Durability and Standing

The focused SQLite witness closes and reopens the ledger, then validates the
ordered-coordinate results, recurrence results, and corresponding-coordinate
Measurement results from their durable coordinates.

The producer and consumer advance current Standing through exactly the events
they record. The bounded advance agrees with complete Locality replay,
including its event-count contract, without rereading the earlier Locality at
each result.

## Remaining hand-written continuation

The first explicit Producer-to-Consumer seam is still visible:

```python
record_corresponding_coordinate_material_measurements(
    ledger,
    recurrence_result_event_identity=final_recurrence.identity,
    locality_standing=run.locality_standing,
)
```

The producer returns the exact complete recurrence result and current
Standing. The caller then names that complete result for the consumer. The
consumer itself chooses no recurrence group, coordinate role, or material
value.

The proof also receives `extension_count=2` as an implementation limit so this
slice demonstrates exactly two successive extensions. No generic result
uptake or self-continuing elevator is claimed.

## Verification

```text
tests/test_variable_extent_recurrence.py
4 passed in 49.16s

Book admission and grammar
29 passed in 0.09s

focused runtime Fidelity sirens
5 passed in 3.44s

ordered-path source-position Compare witnesses
7 passed in 6.74s
```

The runtime-wide record-word siren still reports 2,098 existing migration
violations. A direct scan of the new module's authored durable material reports
no additional refused word.

The next vacancy is automatic uptake of the yielded complete recurrence result
by the already-addressable corresponding-coordinate Measurement
Responsibility. Corpus scale was not attempted in this change.
