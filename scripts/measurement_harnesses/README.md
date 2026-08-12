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

They stay outside because nothing needs to be built inward to reach these numbers.
Diagnostic output is material, and `seed_runtime/system_material.py` already carries
the boundary that material would arrive through. An earlier draft of this file said
there was no consumer for it. That was wrong, and the correction removes the reason to
build inward rather than supplying one.

### What the clauses do and do not give

`05.Testimony.C` establishes the *kind*: runtime/resource observation is testimony
about a process condition at an observed time, and "may exist without a recording
boundary." It does not establish Seed as the Producer of that observation, and nothing
here should be read as establishing one.

No Eye competency is required either, which matters, because
`eye_competency_composition_locality_characterization_009.md` records "Seed itself as
observer" as *not established as a Book subject* and "single bounded competency" as
*contradicted*; the best-supported characterizations are constitutional frontier and
orientation. A design where the Eye *owns* an observation responsibility would rest on
that gap. Nothing described here does.

### The path, and why it is the lawful one

```text
  operator invokes the harness      an act under operator authority, outside Seed
  the harness observes and writes   the observation is produced by the harness
  the output is system-origin       the third boundary #2493 recovered
  Seed may later preserve it        ordinary material consumption
```

`#2493` describes that third boundary as "the first Evidence available to Seed that
neither the operator supplied nor Seed produced," and refuses one thing specifically:
*"It is not Seed observing itself. Seed's own emission is an act Seed performed and an
occurrence already recorded directly; discovering it through an observer would
manufacture a second testimony path about something Seed knows first-hand."*

An operational diagnostic is not that refused shape. Seed knows its own emissions
first-hand; it has no direct account of how many ledger reads a Compare cost. The
harness observes something Seed has no first-hand account of, which is what makes this
system-origin material rather than a second path to something already recorded.

### On invocation

Nothing here is invoked by Seed, and this file establishes nothing about whether it
could be. `#2493` holds that "an invocation and the material that followed it are two
occurrences; whether one is the answer to the other is a third thing," and that no
invocation is required for system material to exist at all. So a Seed-performed
invocation is not the same subject as an emission, and neither is settled by the fact
that readable output exists. If Seed ever performs one, it needs its own responsible
occurrence, and the relation between that occurrence and any material that follows is
its own bounded subject.

An earlier draft of this file called a Seed-performed invocation "egress." That
collapsed three distinct subjects into one word.

### Two constraints on the reading, when it happens

- `material_origin` is `system`. The harness produced the observation; Seed did not
  measure itself, and preserving it otherwise would misattribute the producer.
- What may be recorded is that the system testified to a value — not that Seed is slow.
  Testimony about Seed is still testimony from a witness, consumed under
  `05.Testimony:24`. `#2490` records the reason attribution comes first: Seed's account
  of a fire must never become material asserting a fire.

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
