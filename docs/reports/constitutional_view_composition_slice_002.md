# Constitutional View Composition Slice 002

This slice implements exactly one implementation-local responsibility: `ConstitutionalViewComposition`.

Repository authority wins. The implementation composes only explicitly requested, already registered constitutional read-model views into one immutable bounded explanation. It does not implement the Eye, autonomous orchestration, planning, runtime reasoning, evidence discovery, view-selection heuristics, read-model redesign, diagnostic redesign, ownership recovery, or constitutional authority recovery.

## Implementation evidence

The implementation uses only the already registered constitutional read-model contracts and their read-only artifacts:

- `ConstitutionalReadModelContract` and `CONSTITUTIONAL_READ_MODEL_CONTRACTS` identify the supported constitutional view registrations.
- `constitutional_process` consumes `build_constitutional_process_view()` and `constitutional_process_view_json()`.
- `constitutional_governance` consumes `build_constitutional_governance_view()` and `constitutional_governance_view_json()`.
- `constitutional_fidelity` consumes `build_constitutional_fidelity_view()` and `constitutional_fidelity_view_json()`.
- Diagnostic inventory and diagnostic shape audit register the new consumer surface as read-only, JSON-capable, non-recording, non-event-ledger-writing, and non-mutating.

## Request shape

Recovered minimum request:

```text
ConstitutionalViewCompositionRequest
- requested_views: tuple[str, ...]
- composition_purpose: str
- output_format: "human" | "json"
```

Boundary notes:

- `requested_views` is explicit only and must name already registered constitutional read models.
- `composition_purpose` is only a label for the bounded explanation.
- `output_format` records the consumer rendering intent and does not change the artifact semantics.
- Unsupported view names are refused instead of discovered, inferred, routed, or planned.

## Producer

Producer:

```text
build_constitutional_view_composition(request)
```

The producer:

- checks each requested view against registered constitutional contracts;
- builds only those requested read-only constitutional view artifacts;
- consumes each view's JSON-ready immutable artifact;
- correlates existing `composition` evidence by stable first occurrence;
- prefixes preserved Unknowns and refusals with the contributing view name;
- returns one `ConstitutionalViewCompositionArtifact`.

The producer does not:

- perform runtime reasoning;
- invent evidence;
- resolve Unknowns;
- discover evidence;
- select views heuristically;
- recover constitutional authority;
- recover implementation authority;
- mutate repository state.

## Artifact

Produced artifact:

```text
ConstitutionalViewCompositionArtifact
- name
- request
- contributing_views
- bounded_summary
- correlated_existing_evidence
- preserved_unknowns
- preserved_refusals
- compatibility_answer
- read_only_boundaries
- read_only
- mutates_cluster
- writes_event_ledger
```

The artifact contains only:

- contributing views;
- bounded summary;
- correlated existing evidence;
- preserved Unknowns;
- preserved explicit refusals;
- compatibility answer;
- read-only boundaries.

The compatibility answer remains:

```text
No.
```

## Consumer

One bounded consumer is implemented:

```text
seed --constitutional-view-composition <registered-view> [<registered-view> ...]
```

Supported registered view names:

- `constitutional_process`
- `constitutional_governance`
- `constitutional_fidelity`

Consumer output:

- human rendering by default;
- JSON rendering with `--json`;
- optional purpose label with `--composition-purpose`.

The consumer does not implement planning, autonomous orchestration, the Eye, evidence discovery, or runtime view-selection heuristics.

## Preserved Unknowns

Every contributing view's `unknowns` are preserved in `preserved_unknowns` with the contributing view name as a prefix. The composition does not resolve, weaken, merge away, or promote Unknowns into authority.

## Preserved refusals

Every contributing view's `explicit_refusals` are preserved in `preserved_refusals` with the contributing view name as a prefix. Views without explicit refusals contribute none; no refusal is invented for them.

## Compatibility

Compatibility answer:

```text
No.
```

The composed artifact returns `No.` only when all contributing views return `No.`. Otherwise the composition falls back to `Unknown.` rather than inventing compatibility.

## Files changed

- `seed_runtime/constitutional_view_composition.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_constitutional_view_composition.py`
- `constitutional_view_composition_slice_002.md`

## LOC changed

Measured before commit with `git diff --stat` after adding this slice:

```text
constitutional_view_composition_slice_002.md    | 184 ++++++++++++++++++++
scripts/seed_local.py                           |  41 ++++-
seed_runtime/constitutional_view_composition.py | 212 ++++++++++++++++++++++++
seed_runtime/diagnostic_inventory.py            |  15 ++
seed_runtime/diagnostic_shape_audit.py          |  15 ++
tests/test_constitutional_view_composition.py   | 128 ++++++++++++++
6 files changed, 594 insertions(+), 1 deletion(-)
```

## Tests executed

```text
pytest -q tests/test_constitutional_view_composition.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

Result:

```text
118 passed
```

## Remaining work before autonomous constitutional composition

- Autonomous view selection remains future work.
- Planning remains future work.
- Orchestration remains future work.
- The Eye remains future work.
- Evidence discovery remains future work.
- Runtime reasoning remains future work.
- Any future recording boundary must separately prove diagnostic-run scope and preserve read-only diagnostic mutation boundaries.

Constitutional View Composition Slice 002 complete.
