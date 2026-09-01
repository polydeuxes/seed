# Incremental State / Lawful Revision Bridge Audit

## Status

This is a characterization, not a replay audit, performance audit, proposal, or architecture rewrite.

Question:

```text
Does incremental state already implement the recurring grammar of lawful revision,
or does it merely resemble it?
```

Smallest answer:

```text
Yes, incremental state unknowingly recovered part of the same recurring discipline:
preserve lawful existing structure, bound work to implementation-backed evidence,
identify an insufficiency or stale boundary, preserve compatibility, perform the
smallest allowed reconstruction, and stop.

No, incremental state is not identical to lawful revision. Incremental state acts
on projected runtime state and read models. Lawful revision, as currently
recovered, acts on explanations, owner boundaries, visibility contracts, and
architectural characterization. The shared grammar is preservation-and-bounded-
repair discipline, not a shared implementation owner.
```

Repository authority wins: current implementation evidence supports a bridge only at the level of recurring discipline. It does not support merging the families.

## Evidence reviewed

### Incremental-state evidence

Reviewed implementation and reports:

- `seed_runtime/state.py`: `_AffectedScope`, `_AffectedProjectionSet`, `_ProjectionInfluenceLineage`, replay scope assessment, replay target selection, replay execution, projection publication, `StateProjector.project_from_state`, `StateProjector.apply`, and `StateProjector.finalize`.
- `seed_runtime/projection_store.py`: state projection snapshots, cache hit/miss behavior, tail replay, snapshot save, and `_events_after_snapshot`.
- `tests/test_state_projector.py`: tests for affected scope recovery, affected projection recovery, replay scope assessment, replay selection, replay execution, and projection publication.
- `tests/test_projection_store.py`: tests proving incremental replay matches full replay, preserves order, never skips events after a snapshot, and surfaces cache status.
- Incremental-state reports: `incremental_state_evolution_architecture_investigation.md`, `incremental_state_scope_visibility_slice_001.md`, `incremental_state_projection_visibility_slice_002.md`, `incremental_state_replay_selection_slice_003.md`, `incremental_state_replay_execution_slice_004.md`, `incremental_state_preoptimization_chain_audit.md`, `constitutional_state_reconciliation.md`, `state_build_cache_debug_investigation.md`, `state_build_cache_debug_family_completion_audit.md`, and state-build cache debug slices.

### Lawful-revision and neighboring-family evidence

Reviewed reports:

- `lawful_revision_smallest_owner_audit.md`
- `continuity_preserving_change_characterization.md`
- `docs/implementation_relationship_grammar_investigation.md`
- `architectural_neighborhood_topology_characterization.md`
- `architectural_locality_significance_characterization.md`
- `orientation_insufficiency_transition_characterization.md`
- `current_lawful_condition_characterization.md`
- `current_lawful_condition_compression_reconciliation.md`
- `constitutional_transition_family_characterization.md`

The lawful-revision side is mostly report-backed characterization and local implementation patterns, not a single runtime class or function named `LawfulRevision`.

## Incremental state grammar

Current incremental-state work already exhibits this implementation grammar:

```text
Existing projected state / cached read model
↓
Incoming ledger events or current last-event boundary
↓
Specific stale or affected boundary identified
↓
Compatible snapshot, ledger history, event order, and consumer-visible shapes preserved
↓
Smallest compatible replay/rebuild path allowed by current projector
↓
Projection published and cache status reported
```

### Existing structure preserved

Incremental state preserves:

- append-only ledger authority;
- previously materialized projected `State` snapshots when version and event boundary allow reuse;
- event order after snapshot boundaries;
- public projected-State compatibility;
- deterministic full finalization after event application;
- dependent read-model identity based on state projection version and last event id.

The strongest implementation evidence is `StateProjector.project_from_state`: it applies events to an existing projected `State`, requires those events to follow the snapshot's `last_event_id` in ledger order, and states that event history remains authority.

### Scope determination

Incremental state has multiple scope owners, and they are not the same owner:

| Owner | Scope determined | Evidence | Boundary |
|---|---|---|---|
| `_recover_affected_scope` | Direct state collection/record touched by one event | Event kind to collection/id mapping | Visibility only; not a dirty-state engine |
| `_recover_affected_projections` | Derived projection names that may read an affected scope | Facts and evidence map to candidate derived projections | Descriptive only; no scheduling authority |
| `_recover_projection_influence_lineage` | Batch of source events, direct scopes, and candidate projections | Composes per-event scope/projection recovery | Not a replay plan |
| `_assess_replay_scope` | Whether compatible projector requires replay | Always `replay_required=True` today | Does not narrow targets |
| `_select_replay_targets` | Executable replay targets | Returns compatible targets: event replay plus projection finalization | Full compatible replay only |
| `_events_after_snapshot` | Tail events after cached snapshot | Finds snapshot id in event order and returns only later events | If snapshot id is missing, refuses tail replay |
| `project_state_with_cache` | Cache hit, incremental replay, or full rebuild | Snapshot version/current last-event comparison and materialization | Boundary invalidation, not dirty-scope invalidation |

### What remains untouched

Incremental replay intentionally leaves untouched:

- ledger history before the snapshot;
- unchanged snapshot payload when it is current and materializes successfully;
- public projection versions and cache compatibility contracts;
- unrelated CLI or schema surfaces during visibility-only slices;
- consumer-visible projected state shape after publication.

### What is rebuilt

Even when event application is incremental, current code rebuilds derived projection indexes globally through `finalize`. That includes alias projection, measurement-history retention, inferred facts, observed/inferred fact partitions, fact supports, relationships, entity type assertions, graph issues, aliases, and fact conflicts.

This is the exact boundary: incremental state currently narrows event replay but not derived-index finalization.

### Evidence permitting replay

Replay is permitted when:

- a snapshot loads for the same workspace/projection/version;
- the payload materializes into a `State`;
- the snapshot is stale rather than current;
- the snapshot does not already contain inferred facts in the guarded cache path;
- `_events_after_snapshot` can find the snapshot event id in current ledger order;
- the projector supports `project_from_state`.

### Evidence refusing replay

Tail replay is refused or bypassed when:

- no snapshot exists;
- snapshot version/name does not match;
- snapshot materialization fails;
- the current last event already equals the snapshot last event, causing a cache hit rather than replay;
- the snapshot id is not found in ledger order;
- the projector cannot accept `project_from_state`;
- the cache path determines a full projection rebuild is required.

### Repair, reconstruction, or recomputation?

Incremental state does not repair explanations. It reconstructs projected runtime state from authoritative events and recomputes derived indexes. More precisely:

- event application is replay/reconstruction into `State`;
- finalization is deterministic recomputation of derived projection indexes;
- dependent read-model cache misses are whole-model recomputation;
- affected-scope/projection lineage is explanation-like visibility, but it does not authorize partial replay.

### Lawful termination

Incremental state terminates lawfully when it publishes a finalized projected State, saves a compatible snapshot when a store is available, and reports cache status such as hit/miss, events applied, and `incremental_replay`.

## Lawful revision grammar

The recent lawful-revision family characterizes this recurring grammar:

```text
Current lawful structure
↓
Incoming implementation-backed evidence
↓
Specific insufficiency identified
↓
Still-valid structure preserved
↓
Smallest lawful revision
↓
Lawful stop
```

Implementation-backed investigations show this grammar across local owners and audit methodology, but do not recover a single implementation-local universal owner. The strongest current authority says lawful revision is a cross-family discipline plus methodology-local audit pattern: local structures remain authoritative until evidence proves a specific insufficiency; repair narrows to that insufficient boundary; neighboring responsibilities remain distinct.

Lawful revision therefore acts mainly on:

- explanations;
- owner boundaries;
- compatibility handoffs;
- diagnostic visibility contracts;
- authority claims;
- typed unknowns;
- architectural characterization.

It does not, in current implementation evidence, act as a runtime replay engine.

## Boundary audit

### Incremental Replay != Lawful Revision

Incremental replay advances projected state by applying ledger events after a snapshot and then finalizing projections. Lawful revision revises an explanation or owner boundary after implementation evidence exposes insufficiency.

They share bounded preservation grammar, but not object, authority, or owner.

### Projection Reconstruction != Explanation Revision

Projection reconstruction produces consumer-visible `State`. Explanation revision produces a more truthful characterization of what implementation supports. Projection reconstruction can be tested by equality with full replay. Explanation revision is constrained by repository evidence and typed unknowns.

### Replay Scope != Revision Scope

Replay scope is derived from ledger position, affected scopes, candidate projections, and compatible replay targets. Revision scope is derived from the explanation or ownership boundary that evidence has made insufficient.

In current code, replay target selection always selects full event replay plus full projection finalization. In lawful revision, smallest revision may be a documentation boundary, a local implementation owner, or a compatibility-preserving slice.

### Replay Selection != Revision Admission

Replay selection answers: what replay work will this projector execute? Current answer: event replay and projection finalization.

Revision admission answers: is there enough implementation-backed evidence to change an architectural claim or owner boundary? Current lawful-revision evidence does not expose a universal admission function.

### Projection Preservation != Explanation Preservation

Projection preservation preserves valid cached state and consumer shape. Explanation preservation preserves still-valid claims, neighboring owners, compatibility contracts, and typed unknowns.

Both preserve lawful structure, but the preserved things are different.

## Structural recurrence

Both families independently exhibit the following discipline:

| Recurrence | Incremental state | Lawful revision | Shared? |
|---|---|---|---|
| Preservation of lawful structure | Reuse compatible snapshots; preserve ledger authority and consumer-visible state shape | Preserve valid explanation, local owners, compatibility, typed unknowns | Yes, as discipline |
| Bounded working scope | Tail events after snapshot; affected scope/projection visibility; cache identity | Specific insufficiency or owner boundary | Yes, but different objects |
| Explicit locality | Event kind to collection/id; facts to derived projection candidates; snapshot last-event boundary | Local owner, local report boundary, exact insufficiency | Yes |
| Smallest affected region | Apply only remaining events when allowed; current finalization remains global | Revise only insufficient claim/boundary | Partial: event replay only; not finalization |
| Compatibility preservation | Same projected State publication and cache versions | Public behavior and neighboring owners remain valid | Yes |
| Lawful termination | Finalized State published; snapshot saved; status returned | Characterization stops without overclaim/recommendation | Yes |

Determination:

```text
The recurrence is real but partial.

Incremental state recovered the preservation/bounded-reconstruction half of the
lawful revision discipline before the repository had language for lawful
revision. It did not implement lawful revision itself.
```

## Negative authority

### `Incremental state is merely optimization` is rejected

Implementation evidence rejects reducing incremental state to mere optimization because the cache path preserves ledger authority, event order, snapshot identity, projection version compatibility, materialization validity, replay status, and equality with full projection behavior. Optimization may be an effect, but the implementation boundary is correctness-preserving projection reconstruction.

### `Lawful revision is merely replay` is rejected

Lawful revision is not replay because it governs evidence-backed changes to explanations, owner boundaries, and compatibility claims. It does not consume ledger events, does not materialize `State`, and does not finalize projection indexes.

### `Both families are identical` is rejected

They differ by object and authority:

- incremental state acts on runtime projected state;
- lawful revision acts on explanations and architectural/owner claims;
- incremental state has concrete runtime owners in `state.py` and `projection_store.py`;
- lawful revision currently has local patterns and methodology, not one universal runtime owner.

### `Similarity alone proves shared ownership` is rejected

Similarity proves only recurring discipline. It does not prove a shared owner, shared constitutional participant, or converged architecture. Current implementation contains no owner that jointly governs replay and explanation revision.

## Exact boundary

The exact bridge is:

```text
Preserve still-valid structure
+ identify an implementation-backed affected/stale boundary
+ perform only compatible reconstruction/revision
+ stop without overclaim.
```

The exact separation is:

```text
Incremental state reconstructs projected state from event authority.
Lawful revision reconstructs architectural explanation from implementation authority.
```

Incremental state's boundary is ledger/projection/cache/read-model authority. Lawful revision's boundary is explanatory sufficiency, implementation-backed ownership, compatibility, and typed uncertainty.

## Typed unknowns

- **Shared underlying owner:** unknown. No implementation owner currently governs both replay reconstruction and explanation revision.
- **Constitutional relationship:** unknown. Both families exhibit constitutional discipline, but current evidence does not prove a shared constitutional participant.
- **Future convergence:** unknown. The bridge may become implementation-significant later, but this audit does not recommend convergence.
- **Implementation gaps:** incremental state lacks dirty-scope finalization, dependency-local recomputation, partial read-model refresh, and partial answer refresh.
- **Lawful-revision gaps:** no universal revision admission function, retirement mechanism, or cross-family revision coordinator is implemented.
- **Apparent similarity lacking implementation support:** the six-stage grammar is strongly recurring, but not all stages are owned by one implementation object in either family.

## Smallest truthful answer

```text
Did incremental state unknowingly recover part of the implementation grammar later
recognized as lawful revision?
```

Yes, but only part.

Recovered recurring discipline:

```text
Do not discard lawful existing structure.
Use implementation-backed evidence to find the stale or insufficient boundary.
Preserve everything still compatible.
Advance/rebuild/revise only through the smallest currently lawful path.
Stop at the boundary the implementation supports.
```

Precise boundary:

```text
Incremental state implements bounded projection reconstruction.
Lawful revision characterizes bounded explanation revision.
The shared grammar is lawful preservation under evidence-backed change;
the families remain distinct because their objects, authorities, and owners differ.
```

## Lawful termination

This audit stops at characterization. It does not recommend partial finalization, dirty-scope execution, new lawful-revision owners, cache policy changes, diagnostic changes, or architecture rewrites.

## Remaining questions

1. Can implementation evidence ever prove a shared constitutional owner for preservation under evidence-backed change?
2. Should affected projection lineage remain visibility-only, or can future implementation prove it is safe to control finalization scope?
3. Is lawful revision intentionally methodology-local, or is there an unrecovered implementation owner?
4. Can dependent read models acquire local recomputation without violating current compatibility boundaries?
5. Can explanation revision receive implementation-level admission/retirement semantics without becoming a universal architecture engine?

## Confidence

**Medium-high.** Confidence is high that incremental replay and lawful revision are not identical, and high that both preserve lawful structure under bounded evidence-backed change. Confidence is medium that no shared underlying owner exists, because this audit reviewed the requested families and primary implementation surfaces but does not prove absence across every repository file.
