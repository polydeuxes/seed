# Codex working handoff

This is a private implementation handoff for a fresh Codex session. It is not
Book material, Rosetta material, a report, or constitutional authority. Do not
commit it unless the operator explicitly requests that.

## Repository position

- Repository: `/home/user/seed`
- Branch: `agent/adjacent-byte-pair-acquisition`
- Pushed tip before the current vocabulary correction: `4139becc`
- Tip title: `Yield recurrent bounded literal results`
- Preceding Standing ownership commits: `d2a37bc5`, `8d31f042`
- Preceding source-position continuation commit: `85e5a430`
- Shared worktree: other agents can edit the same files immediately. Always run
  `git status --short` and `git diff --stat` before editing or staging.
- Preserve every unrelated untracked file. There are many operator-owned files
  at repository root, `.venv/`, SQLite ledgers, generated artifacts, and session
  recordings. Stage only explicit paths.

## Operator direction

The operator is trying to let Seed discover relations and grammar joints
without supplying the answer. The central failure to avoid is deciding which
word or relation should appear and then designing an experiment that finds it.

Current correction:

```text
do not search for a connective word
do not search for an expected relation name
do not assume the current Book relation inventory is complete

observe exact established occurrences
↓
observe a later occurrence addressing an earlier occurrence by exact identity
↓
ask whether a responsible relation occurrence accounts for that handoff
↓
repeated unwitnessed handoff = a structural hole, not a named relation
```

The operator suspects roughly ten relation distinctions may still be unknown.
They might not be admitted words. This is a hypothesis, not a target count.

## Current source-position staircase

The live road is now:

```text
exact source positions
↓
Compare every exact pair required for consecutive positions
↓
Measurement carrying all Compare results
↓
recurrence of those findings
↓
corresponding exact material across the exact recurrent results
↓
Measurement yielding reusable exact material
```

Current files:

```text
seed_runtime/source_position_recurrence.py
tests/test_source_position_recurrence.py
book_of_seed/recurrent_result_exact_material_measurement_implementation_001.md
```

Removed without compatibility names:

```text
BoundedLiteralMeasurement
coordinate_role as an ordinal
ordered_coordinate_set
variable extent
VariableExtentRun
```

The material findings need no ordinal. Each one carries exact source-position
coordinates through exact result references. The only `role` values remaining
in this road are the genuine Act-local Compare Participation roles `first
subject` and `second subject`.

The positive witness `a+aa+a` yields exact material `a+a` without the caller
naming that material, its coordinate count, a source position, or `+`. The
control `a+aa-a` yields no common exact material for the same same/different
findings. All eleven focused proofs pass when invoked in one- or two-test
commands below the one-minute boundary.

The slow-test trick is important: do not reconstruct complete Locality when a
proof asks only for exact addressed results. Pass one `_validated` dictionary
through related exact readers. The dictionary ends with the read; a later read
still detects mutation. This reduced the SQLite reader proof from the
55-second cutoff to 15.28 seconds.

## Navigate by coordinates, never by names

The repository is navigational, but only if the traveler follows exact carried
coordinates. Name-shaped search repeatedly led Codex onto parallel roads that
were real but irrelevant, especially the global Candidate implementation.

Bad navigation:

```text
Measurement stopped
↓
Candidate sounds like the next concept
↓
search every Candidate module
↓
attach a global Cartesian road
```

Coordinate navigation:

```text
What exact result occurrence was just Yielded?
↓
Which exact coordinates does that result carry?
↓
Which existing reader accepts those exact coordinates as subject positions?
↓
Which Responsibility owns that reader?
↓
Is its Applicability independently established?
↓
perform only that Responsibility's bounded work
```

Practical repository method:

1. Start with the exact event kind and exact material coordinate path in the
   observed result. Do not start with an English capability noun.
2. Locate the producer of that exact coordinate:

   ```bash
   rg -n 'exact_coordinate_key' seed_runtime tests book_of_seed/chapters
   ```

3. Locate every reader that accepts the producer's exact occurrence identity,
   result identity, Assertion address, Locality, and boundary. Search the field
   name or event-kind constant, not “Candidate,” “Compare,” “next,” or another
   guessed destination.
4. Read the closest focused test that supplies the same exact coordinate shape.
   Tests often demonstrate a road from halfway through its physiology; trace
   their fixture backward until the actual producer is visible.
5. Write the carried frontier before choosing a continuation:

   ```text
   exact occurrence P
   exact result R
   exact source occurrence S
   exact Locality L
   exact completeness boundary B
   exact Assertion addresses A1...An
   ```

6. For each possible consumer, compare its subject positions literally against
   that frontier. If the caller must invent an address, pair, cap, role, or
   relation that the frontier does not carry, the road is not adjacent yet.
7. Availability is not Applicability. A matching coordinate only makes the
   Responsibility's subject position addressable; its own Applicability work
   still has to occur before Participation.
8. A producer must only Yield its exact result. Do not encode knowledge of the
   next floor into the producer.
9. Parallel lawful consumers remain siblings. For example, one D.2 local result
   can independently feed local coordinate Compare and shared-position/path;
   neither has to be a prerequisite for the other.
10. When no reader accepts the exact carried frontier, freeze that vacancy. Do
    not jump to the largest nearby module or invent a dispatcher.

Useful coordinate-oriented searches:

```bash
# Exact event producer and all consumers
rg -n 'RECORDED_EVENT_KIND|literal\.event_kind' seed_runtime tests

# Exact occurrence reference carried forward
rg -n 'recorded_occurrence_reference|responsible_act_evidence_identity' \
  seed_runtime tests

# One exact Book coordinate, after runtime adjacency is known
rg -n '01\.Source\.D\.2|04\.Compare' \
  book_of_seed/chapters book_of_seed/witness_grammar.json tests
```

Do not use the last form to decide what should come next. It is for checking the
owner of an already-found runtime adjacency.

This same method governs relation-hole work:

```text
earlier occurrence identity
↓ exact later material path carrying that identity
later occurrence
↓ exact relation-coordinate witness, if any
relation accounted for / structural hole
```

The path is the navigation. Its spelling is only opaque material until the
structural observation is frozen.

The operator explicitly corrected these mistakes:

- The lifecycle is not exhausted by Participation, Carriage, and Yield.
- Responsibility connections and the result/current-Standing connection remain
  incomplete or unrepresented.
- Do not expect `this`, `for`, `through`, `bears`, or any other word. Those were
  examples of material pressure, not discovery targets.
- The connective problem is the point. A source word may compress several
  relation physiologies, and the grammar may omit relation content entirely.
- The Book can be corrected. Treat it as material being decompressed, not as an
  infallible answer key. The operator's phrase is: “I am the real book.”
- Search for holes first. Only after the blind artifact is frozen may source
  material be inspected post hoc.

## Vocabulary and style constraints

Avoid migrating these retired words into active law or final prose:

- `old`
- `summary`
- `uniform`
- `sufficient`

Use `report`, `earlier`, `prior`, `same shape`, or a more exact description.
Do not casually call the current observer work “ABCDEF.” ABCDEF names the
specific PGP → ABC → ABCDEF fanout experiment.

Other durable preferences:

- Honest red tests are better than compatibility layers.
- No backwards-compatibility scaffolding.
- No regex, test-name, or directory inference for constitutional admission.
- No fallback classification and no “everything else is Witness Material.”
- Admission is an explicit whitelist; uptake is separate.
- No global Cartesian Candidate population.
- Co-presence, multiplicity, chronology, and shared support establish no
  relation.
- Anything longer than one minute is a performance bottleneck. Stop, profile,
  and fix the exact seam.
- Safe constitutional implementation corrections are authorized. Commit and
  push a verified correction before continuing so the curator can inspect it.
- Useful observer mechanics belong under `scripts/`.

## Pushed performance correction: `194e3d6e`

The sixteen-book work exposed a quadratic Candidate source expansion. For N
position Assertions, Candidate called one singular reader N times, and each
singular read rescanned from position zero to its target.

The pushed correction adds one bounded ordered population read:

- `seed_runtime/measurement_of_position_coordinates_of_byte_pair_occurrences.py`
  - `_recorded_position_assertion_coordinate_population_for_locality_movement`
- `seed_runtime/candidate_results_from_exact_result_assertions.py`
  - consumes that once-validated ordered population
- `tests/test_measurement_of_position_coordinates_of_byte_pair_occurrences.py`
  - equality with every singular read
  - one result read and one assertion hash per source position
  - later changed result is refused on the next population read

Evidence:

- 61 directly affected tests: passed in 5.63 seconds during root verification.
- 156 broader affected tests passed in agent verification.
- 511 Assertions: 4.51 seconds → 0.028 seconds, about 161×.
- New scaling stayed approximately linear through 8,191 Assertions at 0.46
  seconds.

Do not undo this helper while repairing other continuation replay paths.

## Relation-hole observer scripts

These files are intentionally outside Book and are committed with this handoff:

- `scripts/observe_relation_holes.py`
- `scripts/run_relation_hole_gauntlet.py`
- `scripts/report_relation_hole_gauntlet.py`

They compile and passed smoke runs. They are not committed yet.

### `observe_relation_holes.py`

Pytest plugin. Set:

```text
SEED_RELATION_HOLE_OBSERVATION=/tmp/output.json
```

It monkeypatches both `EventLedger` and `SQLiteEventLedger` public `append` and
`append_many` methods, captures events only while one pytest test is active,
and restores the methods during unconfigure.

Important implementation tricks:

- Qualify every identity by ledger ordinal. Different ledgers can mint the same
  literal identity.
- `_seen_occurrences` prevents double capture if an override delegates to a
  wrapped base method.
- Use one per-ledger append counter. Do not scan the captured list to assign a
  new append position; that was quadratic in the discarded `/tmp` prototype.
- Follow only exact earlier Event identities found in later event material.
  Shared strings or equal result material do not become edges.
- Multiple occurrences of the same earlier identity within one later event are
  preserved as reference paths, but the newest patch also groups one exact
  source/destination occurrence pair so nested result copies do not pretend to
  be many handoffs.
- Explicit relation coordinates are recognized structurally when a mapping has
  `first_subject`, `second_subject`, and either `relation` or
  `relation_occurrence_identity`.
- A relation-shaped coordinate with endpoints and occurrence identity but no
  exact `relation` value is retained as a direct content vacancy.
- A bare handoff remains an observer question. The script never promotes it to
  a relation.
- Consequence hashing is one reverse append-order pass per depth. Do not restore
  BFS from every edge. The discarded version timed out after the one small test
  had already finished.

Smoke commands:

```bash
env SEED_RELATION_HOLE_OBSERVATION=/tmp/seed_relation_holes_standing.json \
  timeout 60 .venv/bin/pytest -q \
  -p scripts.observe_relation_holes \
  tests/test_operator_standing_continuation.py
```

Observed: 33 passed in 0.68 seconds before the newest occurrence-pair addition.

One source-position recurrence witness:

```bash
env SEED_RELATION_HOLE_OBSERVATION=/tmp/seed_relation_holes_small.json \
  timeout 60 .venv/bin/pytest -q \
  -p scripts.observe_relation_holes \
  tests/test_source_position_recurrence.py::test_recurrence_exhausts_source_and_reuses_prior_compare_work
```

Observed before occurrence-pair addition: 1 passed in 6.67 seconds, 558 events,
6,149 exact reference paths.

### `run_relation_hole_gauntlet.py`

Runs all 71 `tests/test_*.py` sources independently. It deliberately does not
load implementation-measurement admission. This is implementation testimony,
not classification of pytest occurrences as Seed occurrences.

Each file receives:

- its own pytest process;
- its own observer artifact and log;
- a 60-second time boundary;
- SIGINT, then SIGKILL after five seconds if pytest cannot finish cleanly.

Four workers were safe on this host. Example:

```bash
.venv/bin/python -u scripts/run_relation_hole_gauntlet.py \
  --output /tmp/seed-relation-gauntlet.GWpYT4 \
  --workers 4 \
  --time-limit-seconds 60
```

This ensures one slow file cannot erase the other populations. Do not hide
time-boundary files by excluding them; the manifest records each refusal or
loss.

### `report_relation_hole_gauntlet.py`

Combines the independently bounded artifacts without Book/admission lookup.
It preserves:

- repeated bare reference-path families;
- exact source/destination occurrence-pair transitions;
- explicit relation coordinates missing content;
- relation occurrence identities not rendered in the same occurrence;
- every opaque coordinate-path token, unclassified.

The newest reporter expects the newest observer field
`reference_transition_families`. The frozen gauntlet described below predates
that field, so rerun the gauntlet after active performance edits settle before
using the newest reporter.

## Frozen first gauntlet

Directory:

```text
/tmp/seed-relation-gauntlet.GWpYT4
```

Manifest digest:

```text
7e2726fae100f6f396605c79a68e2b38258ab3c30a3b6efc789eed518943ae0f
```

Population:

- 71 pytest source files
- 56 completed within their independent boundary
- 15 reached the 60-second boundary
- 21 nonzero returns, including honest test failures and interrupt exits
- 59 artifacts survived, including several partial artifacts written during a
  clean interrupt

The first combined artifact is:

```text
/tmp/seed-relation-holes-combined.json
```

It predates exact source/destination occurrence-pair aggregation but remains a
useful frozen observation:

- 59 source artifacts
- 629 captured tests
- 38,619 events
- 552,417 reference-path occurrences
- digest before transition-pair reporter changes:
  `5031a48748d8bbec5ab68751d945ba0f05462ddd8cc815f2fb4d129dbc650784`
- digest after an interim path-family transition merge:
  `ace8d27496c99c1b1c4449223f2adcf1f25ef15dc0d7ebaca603cbe64804faaf`

Direct target-free findings from that frozen population:

- 8 event/path families carry a relation coordinate with exact endpoints and a
  relation occurrence identity but omit exact relation content.
- 16 event/path families carry a relation occurrence identity without rendering
  a complete relation coordinate in that same occurrence.
- The 8 missing-content families all use `locality_relation`-shaped coordinates
  across Yield evidence, assertion movement, emission, invocation Locality,
  Standing Locality continuation, and recorded Standing-boundary Locality.
- This does not mean eight missing relation words; many may be the same omitted
  relation content in distinct runtime families.
- The path-level observer found 1,411 repeated bare handoff families. Nested
  result copies inflate this number, which is why exact source/destination
  occurrence-pair aggregation was added before the next run.

Only after freezing the artifact, an admission comparison was performed. The
opaque coordinate-path material had eight words absent from active Book
admission:

```text
identity
evidence
assignment
event
dimensions
determination
acquire
replay
```

Do not call these the missing relations. They are merely unadmitted
implementation-coordinate material surrounding the structural holes.

## Honest full-suite boundaries

The admitted full suite refuses during collection:

```text
ValueError: pytest function has no exact admission
```

Command used:

```bash
env SEED_RELATION_HOLE_OBSERVATION=/tmp/seed_relation_holes_admitted.json \
  timeout -s INT -k 5 60 .venv/bin/pytest -q \
  -p scripts.implementation_function_measurement \
  -p scripts.observe_relation_holes
```

Preserve this refusal. Do not add admission merely to obtain observer data.

Ordinary pytest without implementation-measurement admission reached a slow
boundary in `tests/test_bounded_locality_reads.py`. A verbose run showed:

```text
68 passed, 8 skipped in 60.64 seconds
active test at boundary:
tests/test_bounded_locality_reads.py::test_the_occurrences_are_identical_in_memory[s2]
```

A separate runaway process was discovered and terminated:

```text
PID 1716296
elapsed 13h41m
99.9% CPU
.venv/bin/pytest -q
  tests/test_source_position_recurrence.py
  tests/test_comparison_of_ordered_path_source_position_material.py
  tests/test_carried_locality_standing.py
```

The exact source-position quadratic repair at `194e3d6e` reduced
`test_comparison_of_ordered_path_source_position_material.py` to 8.7 seconds in
the per-file gauntlet.

Other first-gauntlet files that crossed 60 seconds:

- `tests/test_bounded_locality_reads.py`
- `tests/test_carried_locality_standing.py`
- `tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py`
- `tests/test_comparison_of_recorded_byte_pair_measurements.py`
- `tests/test_compiled_material_acquisition.py`
- `tests/test_console_locality.py`
- `tests/test_grammar_implementation.py`
- `tests/test_null_start_evidence_witness.py`
- `tests/test_operator_checkpoint.py`
- `tests/test_operator_locality_standing.py`
- `tests/test_operator_recorded_standing.py`
- `tests/test_operator_representation.py`
- `tests/test_preserved_material_later_referenceable.py`
- `tests/test_process_entry.py`
- `tests/test_representation_records_no_history_copy.py`

Completed but close to the boundary:

- `tests/test_byte_measurement.py`: 49.6 seconds
- `tests/test_measurement_of_shared_position_of_byte_pair_occurrences.py`: 46.9
  seconds
- `tests/test_operator_slash_commands.py`: 37.0 seconds
- `tests/test_compiled_material_localities.py`: 33.4 seconds
- `tests/test_operator_checkout.py`: 33.2 seconds, returned nonzero honestly

## Active performance agents

At handoff time, two existing agents still have live tasks and one has delivered
an uncommitted patch. They share this worktree; ask for status before editing
their files.

### `witness_physiology`

Task: bounded Locality reads and carried Locality Standing. Completed without a
commit; its four-file patch is present in the shared worktree.

Profile:

- s2 baseline 52.79 seconds
- 117.5 million calls
- all but 0.15 seconds is fixture setup
- ordered-path continuation: 33.2 seconds / 300 calls
- 4,394 repeated addressed-position/source reads
- 3,678 recursive bounded Locality replays: 23.2 seconds
- about 11 million deepcopy calls: 23.5 seconds

Implemented safe cut:

- initial exact-prefix validation remains complete;
- immutable validated projections serve private nested reads;
- final context-boundary validation refuses a changed prefix;
- carried result mutation remains an immediate O(1) refusal.

Modified:

- `seed_runtime/measurement_of_position_coordinates_of_byte_pair_occurrences.py`
- `seed_runtime/ordered_path_source_position_continuation.py`
- direct Measurement tests

It was explicitly told to preserve the new committed Candidate population helper
byte-for-byte, and did so.

Verification delivered by the agent:

- normal s1: about 19 seconds
- normal s2: about 19 seconds
- normal s3: 18.86 seconds
- s1+s2: 38.23 seconds
- direct affected suites: 53 passed in 8.83 seconds
- `git diff --check`: clean

The performance gain is smaller than the Candidate cut but moves each formerly
~53-second fixture population below the one-minute boundary. Review the exact
context-boundary validation carefully before committing.

### `changed_tests`

Task: profile/fix the >60-second
`tests/test_comparison_of_ordered_relation_path_with_recorded_pair_findings.py`.

Stopped at session transition with one uncommitted runtime diff:

- `seed_runtime/comparison_of_ordered_relation_path_with_recorded_pair_findings.py`
- 71 insertions / 3 deletions
- call-bounded `ContextVar` cache around five public current-Standing
  subject/lifecycle operations
- cache resets after each public operation
- one serial-assignment test: 9.32 seconds → 6.68 seconds
- cProfile: 31.54 seconds → 22.31 seconds; 73.8m → 54.3m calls
- `git diff --check`: clean

This is **not ready to commit**. It has no focused cache/mutation tests and the
full named file has not passed with the patch. The residual bottleneck is
operator Standing/source replay. Review or revert explicitly; do not call it a
completed fix.

### `egress_provenance`

Task: profile/fix the >60-second
`tests/test_comparison_of_recorded_byte_pair_measurements.py`.

Stopped at session transition with an uncommitted two-file partial cut:

- `seed_runtime/comparison_of_recorded_byte_pair_measurements.py`
- `tests/test_comparison_of_recorded_byte_pair_measurements.py`
- 17 insertions / 9 deletions
- passes exact current `locality_standing` into the existing assignment reader
  for the just-carried later pair, avoiding one historical Standing replay
- three focused validation/mutation witnesses passed in 1.39 seconds
- `git diff --check`: clean

This is **not ready to commit as a bottleneck fix**. The principal reopen test
still exceeds 60 seconds. It moved past the first replay hotspot and now stalls
when Representation rereads the just-carried Compare result through complete
pair histories. Preserve as an explicitly partial slice or revert; do not claim
the file is fixed.

Use `collaboration.list_agents` and read their messages before proceeding.

## Process and tool tricks

### Find runaway work

Use a narrow process query when possible. The broad query is noisy:

```bash
ps -eo pid,ppid,etime,rss,pcpu,args
```

Look for repository `.venv/bin/pytest` or observer scripts. The operator has
authorized stopping a clearly runaway test. Resolve the exact PID before
`kill`.

### Commands that keep an artifact on timeout

`timeout -s INT -k 5 60` lets pytest handle KeyboardInterrupt and run
`pytest_sessionfinish`; however, if observer analysis itself takes longer than
five seconds, SIGKILL still erases the artifact. That happened in the first
all-suite observer run. Per-file processes solve this.

### Tool sessions

Long `exec_command` calls can return a `session_id`. Poll them with
`write_stdin` using empty input and a bounded `yield_time_ms`. In code mode an
outer `functions.exec` can itself yield a `cell_id`; use `functions.wait` only
for that outer cell, then continue polling the returned process session.

Do not use sleeps longer than 60 seconds. Send the operator a concise update at
least once per minute while long work continues.

### Editing and staging

- Use `apply_patch` for source edits.
- Use explicit paths in `git add`.
- Never stage the repository root.
- Before committing: `git diff --check`, focused pytest, `git status --short`.
- Push each verified performance correction separately before the observer
  rerun, matching operator direction.

## Immediate next actions

1. Read messages from the three active agents.
2. Review and verify each performance patch independently.
3. Commit/push each coherent, non-overlapping correction separately. Do not mix
   observer scripts into performance commits.
4. Rerun smoke tests for `scripts/observe_relation_holes.py` after the new
   exact occurrence-pair aggregation.
5. Rerun the 71-file gauntlet from a fresh `/tmp/seed-relation-gauntlet.*`
   directory on the settled pushed tip.
6. Combine it with `scripts/report_relation_hole_gauntlet.py`.
7. Freeze the combined artifact and digest before inspecting admission, Book
   wording, runtime field names, or history.
8. Evaluate structural holes in this order:
   - exact relation coordinates whose content is absent;
   - exact relation occurrence coordinates whose endpoints/content are not
     rendered in the same occurrence;
   - repeated source/destination occurrence-pair transitions that are never
     carried inside an explicit relation coordinate;
   - later consequence depth and natural occupant substitution for each hole.
9. Only post hoc, inspect all raw source material around the surviving holes.
   Do not search for a prepared word list. Include unadmitted material and state
   clearly that an unadmitted token is not automatically a relation.
10. Write one investigation report with counts, timings, frozen digests, exact
    holes, false survivors, and the first missing responsible relation work.
11. Add focused tests for observer scripts if they are to be committed.
12. Commit/push observer scripts and report separately.

## Central intellectual guardrail

The three familiar relation examples are incomplete:

```text
subject --Participation(role)--> Act occurrence
content --Carriage-------------> Act occurrence
Act occurrence --Yield---------> result
```

Do not append a guessed fourth arrow.

Instead retain the exact observed graph:

```text
recorded occurrence A
↓ exact later reference
recorded occurrence B

explicit responsible relation occurrence found?
├── yes: preserve that exact relation
└── no: preserve the hole and follow its consequences
```

The experiment succeeds if it finds structural vacancies and leaves their
relation content Unknown. It fails if Codex starts with a word and congratulates
itself for finding that word.
