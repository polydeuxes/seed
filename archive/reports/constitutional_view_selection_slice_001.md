# Constitutional View Selection Slice 001

This is exactly one implementation ownership audit for bounded constitutional view selection. It does not implement selection, the Eye, planning, orchestration, constitutional recovery, ownership recovery, implementation recovery, runtime reasoning, evidence discovery, evidence invention, repository mutation, or authority creation.

Repository authority wins.

## Investigation scope

Reviewed implementation evidence was limited to:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition.

Expansion was limited to adjacent CLI dispatch and tests where needed to confirm current consumption and compatibility behavior.

## Implementation evidence

### ConstitutionalReadModelContract

`ConstitutionalReadModelContract` records recurring implementation obligations shared by registered constitutional read-model views:

- name;
- CLI flag;
- builder;
- renderer;
- JSON renderer;
- diagnostic inventory name;
- diagnostic shape-audit name;
- read-only mutation boundary;
- JSON support;
- recording boundary;
- event-ledger boundary;
- cluster-mutation boundary.

It explicitly refuses to construct views, render output, dispatch CLI requests, register diagnostics, create constitutional authority, create implementation authority, or define future constitutional view contents.

The registered constitutional contracts are exactly:

- `constitutional_process`;
- `constitutional_governance`;
- `constitutional_fidelity`.

Every registered constitutional contract preserves `read_only=True`, `supports_json=True`, `supports_record=False`, `record_scope="none"`, `writes_event_ledger=False`, and `mutates_cluster=False`.

### ReadModelViewRegistration

`ReadModelViewRegistration` records an already-consumable read-model view by name, CLI flag, builder, renderer, and read-only boundary. It explicitly refuses read-model construction, output rendering, CLI dispatch, argument parsing, projection publication, ledger writes, cluster mutation, and constitutional-content declaration.

`constitutional_read_model_registration(contract)` consumes each `ConstitutionalReadModelContract` into the registration family. This proves registered constitutional views expose implementation-local metadata that a later selection boundary could inspect without constructing constitutional authority or redesigning registration.

### Constitutional Process View

The Constitutional Process View is an immutable read-only view over existing process evidence. It has `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves process stages, evidence, Unknowns, and remaining candidate views without selecting among other constitutional views for a bounded operator question.

### Constitutional Governance View

The Constitutional Governance View is an immutable read-only view over existing governance evidence. It has `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves governance relationships, evidence, Unknowns, explicit refusals, and remaining candidate views without selecting among registered views for a bounded operator question.

### Constitutional Fidelity View

The Constitutional Fidelity View is an immutable read-only view over completed fidelity evidence. It has `compatibility_answer="No."`, `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`. It preserves classifications, recurring discipline, Unknowns, explicit refusals, read-only boundaries, and remaining candidate views without selecting among registered views for a bounded operator question.

### Constitutional View Composition

`ConstitutionalViewCompositionRequest` accepts `requested_views`, `composition_purpose`, and `output_format`. Its docstring states that the request owns only explicit registered-view selection, purpose labeling, and output-format intent, and does not select views heuristically, discover evidence, reason at runtime, recover authority, plan, orchestrate, or mutate repository state.

`build_constitutional_view_composition` composes only explicitly requested registered constitutional views. It validates requested names against `CONSTITUTIONAL_READ_MODEL_CONTRACTS` and the local builder map, builds those view artifacts, correlates their already-existing evidence, preserves their Unknowns and refusals, and returns one immutable `ConstitutionalViewCompositionArtifact`.

The composition artifact summary and read-only boundaries preserve the same negative boundary: no added authority, no Unknown resolution, no evidence discovery, no planning, no orchestration, no runtime reasoning, no recording, no event-ledger writes, and no cluster mutation.

### CLI dispatch evidence

The CLI exposes separate flags for `--constitutional-process`, `--constitutional-governance`, `--constitutional-fidelity`, and `--constitutional-view-composition`. For composition, the operator supplies one or more view names through the CLI argument. The dispatch path passes those explicitly supplied names into `constitutional_view_composition_request(...)` and then into `build_constitutional_view_composition(...)`.

This confirms that the current implementation supports explicit composition but does not own the prior question: which registered constitutional views are relevant to one bounded constitutional question?

## Current ownership

### 1. Who presently owns constitutional view selection?

No implementation-local component presently owns bounded constitutional view selection.

Repository evidence shows ownership of adjacent responsibilities only:

- `ConstitutionalReadModelContract` owns recurring constitutional read-model obligations and metadata;
- `ReadModelViewRegistration` owns consumable view registration metadata;
- each constitutional view owns its own bounded immutable read-only artifact;
- `ConstitutionalViewComposition` owns composition of explicitly requested registered constitutional views.

None of those boundaries accepts one bounded constitutional question, inspects registered constitutional view metadata, determines relevant registered views, preserves unsupported selection uncertainty, and returns a selection artifact.

### 2. Is view selection currently compressed into the operator?

Yes.

The operator must decide which registered constitutional view names to pass to `--constitutional-view-composition`. Composition begins only after that explicit selection is already supplied.

### 3. Is view selection currently compressed into future callers?

Yes.

Any future caller that wants a bounded constitutional explanation must decide which registered constitutional read models are relevant before invoking composition, because composition accepts requested view names and refuses unsupported names but does not determine relevance.

### 4. Is view selection currently compressed into prompt construction?

Yes, for prompt-driven usage.

When the bounded constitutional question originates in a prompt, the prompt or caller must encode the selected view names before repository composition can run. Repository implementation evidence does not show a separate selection artifact between the bounded question and `ConstitutionalViewCompositionRequest`.

### 5. Does repository evidence expose one immediately adjacent implementation-local ownership boundary?

Yes.

Repository evidence exposes exactly one immediately adjacent implementation-local ownership boundary: **ConstitutionalViewSelection**.

The boundary is adjacent because it sits after bounded-question intake and registered constitutional view metadata, and before `ConstitutionalViewCompositionRequest`. It does not replace the existing contract, registration, views, CLI behavior, JSON output, human rendering, diagnostic inventory, diagnostic shape audit, or compatibility behavior.

## Selected ownership boundary

Selected boundary: `ConstitutionalViewSelection`.

Repository evidence selects this boundary because the implemented system already has:

1. registered constitutional view metadata;
2. immutable read-only constitutional view producers and artifacts;
3. an explicit composition owner that requires preselected registered view names;
4. no implementation-local owner for mapping one bounded constitutional question to selected registered view names.

The missing responsibility is not composition, another read-model contract, another registration layer, a redesigned view, a CLI redesign, a planner, an orchestrator, the Eye, runtime reasoning, or authority creation. It is the narrower pre-composition act of selecting already registered constitutional read models relevant to one bounded constitutional question.

## Before

Before this audit:

```text
Operator or caller
        ↓
Explicit requested registered view names
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

Selection was external to the repository implementation. The operator, future caller, or prompt construction had to decide relevance before composition could operate.

## After

After this audit, no code behavior changes. The recovered implementation-local boundary for a possible later slice is:

```text
Bounded Question
        ↓
ConstitutionalViewSelection
        ↓
Selected Views
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

This is an ownership recovery only. Selection is not implemented here.

## Recovered producer

Recovered producer: `ConstitutionalViewSelection`.

If implemented later, the producer may only:

- accept one bounded constitutional question;
- inspect registered constitutional view metadata;
- determine which already registered views are relevant;
- preserve uncertainty when selection is unsupported;
- produce one immutable selection artifact.

The producer must explicitly refuse:

- constitutional recovery;
- ownership recovery;
- implementation recovery;
- evidence discovery;
- evidence invention;
- runtime reasoning;
- planning;
- orchestration;
- composition;
- repository mutation;
- authority creation.

## Recovered artifact/helper

Recovered artifact/helper: `SelectedConstitutionalViews`.

If implemented later, the artifact should preserve only selection output, such as:

- the bounded constitutional question as received;
- selected registered constitutional view names;
- registered metadata consumed for those names;
- unsupported or uncertain selection notes when relevance cannot be proven;
- read-only and non-mutating boundary flags.

It should not contain composed view artifacts, constitutional findings, recovered evidence, reasoning traces, plans, orchestration state, implementation mutations, or authority claims.

## Recovered consumer

Recovered consumer: `ConstitutionalViewComposition`.

The existing composition boundary can remain the consumer because it already accepts explicit registered view names and composes only those requested views. A later selection slice could hand selected view names to `constitutional_view_composition_request(...)` without changing composition ownership.

## Relationship to ConstitutionalViewComposition

Repository evidence supports the separation:

```text
Bounded Question
        ↓
ConstitutionalViewSelection
        ↓
Selected Views
        ↓
ConstitutionalViewComposition
        ↓
Bounded Constitutional Explanation
```

The reason is implementation-local:

- registered constitutional metadata exists before composition;
- composition requires explicitly requested registered view names;
- composition validates and consumes the explicit names but does not determine relevance from a bounded question;
- composition builds and correlates immutable view artifacts only after selection has already happened;
- composition explicitly refuses heuristic selection, discovery, runtime reasoning, planning, orchestration, mutation, and authority creation.

Therefore selection is a pre-composition responsibility, and composition remains a post-selection responsibility.

## Compatibility

Expected compatibility answer:

```text id="e8v0sx"
No.
```

Compatibility is preserved because this slice changes only one audit document and does not modify:

- `ConstitutionalReadModelContract`;
- `ReadModelViewRegistration`;
- Constitutional Process View;
- Constitutional Governance View;
- Constitutional Fidelity View;
- Constitutional View Composition;
- CLI behavior;
- JSON output;
- human rendering;
- diagnostic inventory;
- diagnostic shape audit;
- tests;
- runtime compatibility.

## Files changed

- `constitutional_view_selection_slice_001.md`

## LOC changed

- Added: 296 lines
- Removed: 0 lines
- Net: +296 lines

## Tests executed

- `pytest -q tests/test_constitutional_view_composition.py tests/test_read_model_ownership.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

## Remaining work before bounded constitutional attention

Before bounded constitutional attention can use this boundary, a future implementation slice would still need to:

1. implement `ConstitutionalViewSelection` without expanding its authority;
2. define an immutable `SelectedConstitutionalViews` artifact or equivalent helper;
3. add tests proving selection inspects only registered constitutional view metadata;
4. add tests proving unsupported relevance remains uncertain rather than invented;
5. prove the selected artifact can feed existing `ConstitutionalViewComposition` without changing composition;
6. update diagnostic inventory and diagnostic shape audit only if selection becomes an exposed diagnostic, audit, probe, view, operational CLI flag, or recordable output;
7. preserve autonomous attention, planning, orchestration, and the Eye as future work.

## Lawful stop

This slice identifies exactly one immediately adjacent implementation-local ownership boundary responsible only for selecting already registered constitutional read models relevant to one bounded constitutional question. It preserves existing implementation contracts and compatibility, separates selection from composition, introduces no new authority, performs no runtime reasoning, and leaves autonomous attention, planning, orchestration, and the Eye as future work.

Repository authority wins.
