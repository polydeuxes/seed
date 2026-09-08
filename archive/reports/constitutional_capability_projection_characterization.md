# Constitutional Capability Projection Characterization

This is exactly one implementation characterization. It determines whether Capability Projection requires implementation ownership or is another deterministic constitutional read-model projection over existing immutable constitutional view evidence.

It does not implement Capability Projection, redesign Selection, redesign Composition, redesign registration, invent semantic reasoning, invent runtime caching, invent constitutional authority, or recover another ownership boundary.

Repository authority wins.

## Implementation evidence reviewed

Review was limited to the requested evidence set:

- Constitutional Process View: `seed_runtime/constitutional_process_view.py`.
- Constitutional Governance View: `seed_runtime/constitutional_governance_view.py`.
- Constitutional Fidelity View: `seed_runtime/constitutional_fidelity_view.py`.
- Constitutional View Capability Characterization: `constitutional_view_capability_characterization.md`.
- `ConstitutionalReadModelContract`: `seed_runtime/read_model_ownership.py`.
- `ReadModelViewRegistration`: `seed_runtime/read_model_ownership.py`.

Expansion was not required. Constitutional View Selection, Constitutional View Composition, CLI behavior, JSON rendering, human rendering, diagnostic inventory, diagnostic shape audit, read-model registration, and compatibility remain preserved.

## Projection construction analysis

Capability Projection can be deterministically constructed from stable registration evidence plus each immutable constitutional view artifact.

### Registration-owned projected fields

The existing `ConstitutionalReadModelContract` already owns the stable implementation metadata that a projection would need to identify a registered constitutional view:

- `name`;
- `cli_flag`;
- `builder`;
- `renderer`;
- `json_renderer`;
- `inventory_name`;
- `shape_audit_name`;
- `read_only`;
- `supports_json`;
- `supports_record`;
- `record_scope`;
- `writes_event_ledger`;
- `mutates_cluster`.

The existing `ReadModelViewRegistration` already owns the consumable read-model registration metadata:

- `name`;
- `cli_flag`;
- `builder`;
- `renderer`;
- `read_only`.

Therefore a Capability Projection does not need to author registered identity, operational entry points, JSON support, diagnostic visibility names, recording boundary, event-ledger boundary, or cluster-mutation boundary.

### Constitutional Process View-owned projected fields

The Constitutional Process View already owns the process contribution surface:

- view `name`;
- `compatibility_answer`;
- evidence `composition`;
- process `stages`;
- each stage `name`, `status`, `support_level`, `evidence`, and `summary`;
- preserved `unknowns`;
- `remaining_candidate_views`;
- `read_only`;
- `mutates_cluster`;
- `writes_event_ledger`.

Those fields deterministically produce the Process capability projection: this registered view contributes process-stage evidence, process summaries, process Unknowns, remaining adjacent view candidates, and read-only operational boundaries. No process capability field needs to be authored outside the Process View and registration evidence.

### Constitutional Governance View-owned projected fields

The Constitutional Governance View already owns the governance contribution surface:

- view `name`;
- `compatibility_answer`;
- evidence `composition`;
- governance `relationships`;
- each relationship `name`, `status`, `support_level`, `evidence`, and `summary`;
- preserved `unknowns`;
- `explicit_refusals`;
- `remaining_candidate_views`;
- `read_only`;
- `mutates_cluster`;
- `writes_event_ledger`.

Those fields deterministically produce the Governance capability projection: this registered view contributes governance-relationship evidence, governance summaries, governance Unknowns, explicit refusals, remaining adjacent view candidates, and read-only operational boundaries. No governance capability field needs to be authored outside the Governance View and registration evidence.

### Constitutional Fidelity View-owned projected fields

The Constitutional Fidelity View already owns the fidelity contribution surface:

- view `name`;
- `compatibility_answer`;
- view `summary`;
- evidence `composition`;
- fidelity `classifications`;
- each classification `name`, `status`, `support_level`, `evidence`, and `summary`;
- `recurring_constitutional_discipline`;
- preserved `unknowns`;
- `explicit_refusals`;
- `read_only_boundaries`;
- `remaining_candidate_views`;
- `read_only`;
- `mutates_cluster`;
- `writes_event_ledger`.

Those fields deterministically produce the Fidelity capability projection: this registered view contributes fidelity classifications, recurring discipline, fidelity evidence, fidelity Unknowns, explicit refusals, read-only boundaries, remaining adjacent view candidates, and read-only operational boundaries. No fidelity capability field needs to be authored outside the Fidelity View and registration evidence.

### Required projection construction answers

1. Existing view fields that deterministically produce Capability Projection are the registered identity fields from `ConstitutionalReadModelContract` and `ReadModelViewRegistration`, plus each immutable view's name, compatibility answer, evidence composition, contribution records, contribution evidence, contribution summaries, Unknowns, refusals where present, read-only boundaries where present, remaining candidate views, and mutation/ledger flags.
2. Every projected capability field is already owned elsewhere: contracts own stable implementation metadata, registrations own consumable registration metadata, and each constitutional view owns its constitutional contribution evidence.
3. Capability Projection introduces no new authored constitutional knowledge. It only re-exposes already-owned constitutional view evidence in selection-adjacent form.

## Ownership analysis

### Does Capability Projection mutate?

No. Reviewed evidence shows constitutional views are frozen read-only artifacts, contracts are frozen implementation-local records, and registrations are frozen read-model registration records. The projection would read those artifacts and expose derived selection input without writing back to them.

### Does Capability Projection persist independent state?

No. Reviewed evidence supports regeneration from `ConstitutionalReadModelContract`, `ReadModelViewRegistration`, and immutable constitutional view artifacts. No reviewed evidence requires a stored capability table, a cache, a ledger record, a cluster mutation, or an independently maintained capability document.

### Does Capability Projection own constitutional authority?

No. Constitutional authority remains owned by completed constitutional evidence as preserved inside the constitutional views. The contract explicitly refuses to create constitutional authority or define future constitutional view contents, and registration explicitly refuses constitutional-content declaration. Projection cannot acquire authority that neither the contract nor registration owns.

### Or is Capability Projection regenerated on demand from immutable constitutional views?

Capability Projection is regenerated on demand from immutable constitutional views and their registration metadata. The only lawful construction path supported by the reviewed repository evidence is deterministic derivation from existing view fields and existing registration fields.

## Duplication analysis

Independent implementation ownership would duplicate constitutional knowledge already owned by the registered views:

- a separate Process capability artifact would repeat process stages, stage evidence, stage summaries, Unknowns, and process boundaries;
- a separate Governance capability artifact would repeat governance relationships, relationship evidence, relationship summaries, Unknowns, explicit refusals, and governance boundaries;
- a separate Fidelity capability artifact would repeat fidelity classifications, recurring discipline, classification evidence, classification summaries, Unknowns, explicit refusals, read-only boundaries, and fidelity boundaries.

That duplication would create a second authored representation of constitutional contribution scope. If the underlying view changed, the separate capability artifact could become stale unless maintained in lockstep. Repository evidence instead supports projecting from the owning source of truth: registered immutable constitutional views.

## Relationship analysis

Repository evidence supports this relationship:

```text
Registered Constitutional View
        ↓
Immutable Constitutional View
        ↓
Capability Projection
        ↓
ConstitutionalViewSelection
```

The relationship is supported because:

1. `ConstitutionalReadModelContract` and `ReadModelViewRegistration` identify registered constitutional views without owning constitutional content.
2. Constitutional Process View, Constitutional Governance View, and Constitutional Fidelity View each build immutable read-only artifacts that own their own contribution records, evidence, Unknowns, refusals where present, and mutation boundaries.
3. Capability Projection can expose those already-owned fields in selection-adjacent form without authoring, mutating, caching, or persisting independent constitutional knowledge.
4. ConstitutionalViewSelection remains the later relevance decision and is not redesigned by this characterization.

Repository evidence does not support inserting an independent Capability owner between immutable views and Selection.

## Preserved boundaries and compatibility

Preserved:

- `ConstitutionalReadModelContract`.
- `ReadModelViewRegistration`.
- Constitutional Process View.
- Constitutional Governance View.
- Constitutional Fidelity View.
- Constitutional View Selection.
- Constitutional View Composition.
- Compatibility.

Expected compatibility answer:

```text
No.
```

Compatibility is preserved because this characterization adds only this document and changes no implementation, registration, view shape, selection behavior, composition behavior, CLI behavior, JSON rendering, human rendering, diagnostic inventory, diagnostic shape audit, recording boundary, event-ledger behavior, or cluster-mutation behavior.

## Preserved Unknowns

The following Unknowns remain preserved and are not resolved by this characterization:

- Whether every constitutional inquiry starts only as Pressure remains Unknown.
- Whether every Recovery requires a separate Cross-Examination artifact remains Unknown.
- Whether every Cross-Examination requires a separate Completion Audit remains Unknown.
- Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains Unknown.
- Whether a single named constitutional process owner exists remains Unknown.
- Whether there is a distinct constitutional governance owner remains Unknown.
- Whether Question Grammar and Inquiry Navigation are distinct competencies remains Unknown.
- Whether governance relationships require any implementation topology remains Unknown.
- Whether Constitutional Fidelity should ever become an implementation-backed public surface remains Unknown.
- Whether future Selection should consume an in-memory projection, materialized transient artifact, or another deterministic representation remains Unknown.
- Whether future work should implement Capability Projection remains Unknown.

## Confidence

Confidence is high. The reviewed implementation evidence directly identifies the existing owners of every field a Capability Projection would expose, directly preserves read-only and non-mutating boundaries, and directly refuses independent constitutional authority in the contract and registration layers. No reviewed evidence requires mutation, persistence, independent implementation state, or independent constitutional authorship for Capability Projection.

## Classification

Capability Projection is a deterministic read-model projection.

Capability Projection characterization complete.
