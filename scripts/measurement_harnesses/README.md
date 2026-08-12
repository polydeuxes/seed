# Measurement harnesses

These are the scripts that produced the measurements cited in PRs #2480–#2499 and in
the subject-persistence amendment record. They lived only in `/dev/shm` until now,
which meant every number we cited had its declared method held in RAM.

`05.Testimony.B` treats the measurement method and declared conditions as part of what
a measurement is. Preserving the harness is preserving that part.

Nothing here is reachable from `seed_runtime`, and nothing here should become
reachable from it. The boundary each group sits on is different, so they are listed
separately.

## Run drivers — operator-side, must stay outside

| script | what it does |
| --- | --- |
| `sixteen.py` | feeds sixteen works through the system path, times every stage |
| `s3build.py` | builds the six-body stage-3 store the Compare profile runs against |
| `ab.py` | one tree, one toggle: runs the same build with a change on and off |

These perform ingress and call the recording layers under operator authority, the same
standing `system_material_harness.py` operates under. They drive Seed; they are not
part of it. A driver reachable from inside would let Seed supply its own material,
which is the self-injection boundary the operator has held from the start.

`ab.py` exists because three separate measurements were contaminated by comparing
across two trees at different commits. It takes the tree as `sys.argv[1]` and toggles
only the change under test inside one tree. Any future before/after claim should use
this shape rather than two checkouts.

## Diagnostics — external, deliberately not built inward

| script | what it does |
| --- | --- |
| `s3prof.py` | profiles a stage-3 Compare layer; counts ledger reads per Compare |
| `profstage.py` | the same instrumentation over the earlier stage |

These wrap `SQLiteEventLedger.get`, `integrity_of`, and `iter_session_kind_ids` to
count calls, then run under `cProfile`.

`05.Testimony.C` already establishes the kind — runtime/resource observation is
testimony about a process condition at an observed time, and "may exist without a
recording boundary." So there is no constitutional obstacle to Seed producing its own
operational observation. There is no consumer for it. The consumer of these numbers is
the operator and the reviewer deciding what to optimise, and an external consumer is
served by external tooling. Building the inward version now would be a producer with
no warranted consumer.

Known fragility: the counters attach by patching internal method names. Renaming any
of those three methods makes these scripts measure nothing rather than fail, which is
the same silent-vacuity failure that produced three void tests during this campaign.
That is the specific reason they belong beside the code they patch. Before citing a
number from either script, confirm the counts are non-zero and consistent with the
call count.

Distinct from `seed_runtime/measurement_self_survey.py`, which surveys Seed's own
*recorded measurement occurrences* — its content, not its cost. That one is inside,
and correctly so.

## Analysis

`homog.py` implements RePair over corpus chunks to answer whether homogeneity changes
the hierarchical-pointer curve. It touches no Seed code and produced the
"homogeneity buys under 7%" result. Kept as the record of that method.

## Assumptions

Paths are as run: stores under `/dev/shm/lab`, corpus at `/home/user/seed/corpus`,
tree at `/home/user/seed-visitor`. They are left verbatim rather than parameterised,
because these are the record of what was actually executed. Change them at the top of
each script when re-running.

The stores themselves are not preserved. They are derivable by re-running these
scripts against the commit that produced them.
