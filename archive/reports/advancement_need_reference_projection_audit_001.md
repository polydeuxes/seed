# Advancement Need Reference Projection Audit 001

## Question

Determine the lawful read-only reference boundary:

```text
GoalAdvancementNeedSet
→ AdvancementNeedReferenceSet
```

for one exact selected goal and one exact bounded advancement horizon.

The purpose is to give each native need record one stable operator-facing reference suitable for exact focus and later consideration selection, without flattening the native schemas, deriving identity from serialized payload fingerprints, interpreting need labels, prioritizing, routing, selecting, authorizing, executing, recording, writing the event ledger, or mutating state.

Repository authority wins. This audit is documentary only. It does not implement a diagnostic surface, CLI flag, recordable output, selection surface, operational action, event-ledger write, cluster mutation, or state mutation.

## Guardrails preserved

```text
reference projection
!= need reclassification

stable reference
!= payload fingerprint

shared reference envelope
!= shared native need schema

reference visible
!= reference selectable

native standing established
!= automatically selected
```

The reference projection must preserve unsupported, unknown, conflicting, excluded, outside-scope, unclassified-here, and unclassified native records as visible non-selectable references. Visibility is not selection evidence.

## Evidence reviewed

- `seed_runtime/goal_advancement_need_set.py`
- `tests/test_goal_advancement_need_set.py`
- `seed_runtime/clarification_need_projection.py`
- `seed_runtime/inquiry_need_projection.py`
- `seed_runtime/authority_need_projection.py`
- `seed_runtime/operational_realization_need_projection.py`
- `seed_runtime/goal_advancement_sufficiency_projection.py`
- `tests/test_goal_advancement_sufficiency_projection.py`
- `advancement_need_consideration_selection_audit_001.md`
- `goal_advancement_need_evidence_topology_audit_001.md`
- `goal_advancement_need_set_slice_001.md`
- `goal_advancement_sufficiency_projection_audit_001.md`
- `advancement_need_family_coverage_audit_001.md`

## Current implemented boundary

`GoalAdvancementNeedSet` already preserves supplied, absent, and explicitly excluded native family projections for one exact horizon. It binds those family records to a selected goal, goal establishment, and bounded horizon. It also preserves projection identity conflicts and refuses to reinterpret supplied stage-owned native projections.

The native families already preserve item buckets:

- `ClarificationNeedProjection`: `established`, `unsupported`, `unknown`, `conflicting`, `excluded_family`, and `unclassified`.
- `InquiryNeedProjection`: `established`, `unsupported`, `unknown`, `conflicting`, `excluded_family`, and `unclassified`.
- `AuthorityNeedProjection`: `established`, `unsupported`, `unknown`, `conflicting`, `outside_current_scope`, and `unclassified`.
- `OperationalRealizationNeedProjection`: `established`, `unsupported`, `unknown`, `conflicting`, `unclassified_here`, and `unclassified`.

Those buckets are native standing records. They are not a shared schema, not a priority order, and not a selection list by themselves.

## Existing native lineage that can lawfully identify items

A lawful reference can bind to existing native lineage, but the identity needs to be named as lineage, not reconstructed from an opaque serialized payload hash.

| Family | Native item lineage available now | Lawful item identity basis | Current gap |
| --- | --- | --- | --- |
| Clarification | `projection_id`, bucket name, `testimony_ref`, `source_ref`, `bounded_uncertainty_component_ref`, `owning_stage`, `standing`, `evidence_ref` | one operator-meaning uncertainty testimony record in one native projection bucket | no explicit `native_item_id` field |
| Inquiry | `projection_id`, bucket name, `testimony_ref`, `source_ref`, `bounded_uncertainty_component_ref`, `repository_world_subject_ref`, `owning_stage`, `standing`, `evidence_ref`, freshness, availability | one repository/world uncertainty testimony record in one native projection bucket | no explicit `native_item_id` field |
| Authority | `projection_id`, bucket name, `requirement_testimony_ref`, `authority_testimony_ref`, `bounded_authority_component_ref`, `required_authority_class_ref`, `applicable_scope_ref`, `owning_stage`, separate requirement, authority, scope, materiality, and need standings, `evidence_refs` | one authority requirement/standing join, or one unclassified authority standing witness, in one native projection bucket | no explicit `native_item_id` field; unclassified standing-only records have no requirement testimony ref |
| Operational realization | `projection_id`, bucket name, `requirement_testimony_ref`, `standing_testimony_ref`, `bounded_realization_component_ref`, `required_transformation_ref`, `applicable_scope_ref`, `owning_stage`, separate requirement, availability, coverage, blocker ownership, scope, materiality, and need standings, `evidence_refs` | one operational-realization requirement/standing join, or one unclassified standing-only witness, in one native projection bucket | no explicit `native_item_id` field; unclassified standing-only records have no requirement testimony ref |

The lawful lineage is therefore family-specific and component-backed. The shared reference envelope should preserve this lineage by fields, not collapse the item into a generic payload or infer identity from a full JSON fingerprint.

## Does native item identity already exist?

Native item identity exists partially but not explicitly.

The projections already expose enough stable lineage to address many items in practice: projection id, standing bucket, testimony refs, bounded component refs, scope or subject refs, owning stage, and evidence refs. However, no reviewed native item type exposes a first-class `native_item_id` or `need_item_id` field.

Therefore the reference boundary should not pretend that native item identity is already complete. The minimum lawful approach is:

1. preserve an explicit `native_item_key` assembled from native lineage fields already present on the item;
2. define the key separately for each family, because the local schemas differ;
3. ensure the key is deterministic from standing bucket plus native lineage, not from serialized payload fingerprints;
4. treat duplicate keys inside the same projection and bucket as a reference conflict rather than repairing them by appending order numbers or hashes; and
5. recommend a later local addition of first-class native item ids to the four projection item types if downstream selection needs durable references across representation changes.

This keeps stable reference identity separate from payload fingerprinting while acknowledging that native item identity is not yet a first-class implementation field.

## Shared `AdvancementNeedReference` envelope

The shared envelope should be intentionally thin. It should identify and expose; it should not normalize native need semantics.

Minimum fields:

```text
AdvancementNeedReference
- reference_id
- artifact_type = AdvancementNeedReference
- need_set_id
- selection_id
- goal_establishment_id
- horizon_id
- family
- family_record_disposition = supplied
- native_projection_id
- native_projection_type
- native_standing_bucket
- native_standing
- selectable_for_consideration
- non_selectable_reason: optional
- native_item_key
- native_item_lineage
- component_lineage
- evidence_refs
- source_refs
- owning_stage: optional
- duplicate_reference_conflict: bool
- read_only = true
- reclassifies_need = false
- interprets_labels = false
- inspects_sufficiency_reasons = false
- prioritizes = false
- routes = false
- selects_need = false
- opens_inquiry = false
- requests_clarification = false
- requests_authority = false
- selects_realization = false
- authorizes_work = false
- starts_execution = false
- starts_recording = false
- writes_event_ledger = false
- mutates_cluster = false
```

`native_item_lineage` should be a family-specific record, not a flattened shared need schema. Examples:

- clarification lineage: testimony ref, source ref, bounded uncertainty component ref, owning stage, evidence ref;
- inquiry lineage: testimony ref, source ref, bounded uncertainty component ref, repository/world subject ref, owning stage, evidence ref;
- authority lineage: requirement testimony ref, authority testimony ref, bounded authority component ref, required authority class ref, applicable scope ref, owning stage, evidence refs;
- operational-realization lineage: requirement testimony ref, standing testimony ref, bounded realization component ref, required transformation ref, applicable scope ref, owning stage, evidence refs.

`component_lineage` should expose the component refs used for exact focus without pretending that all families share the same component model.

## Reference binding requirements

Each reference must bind conjunctively to all of the following:

1. **Need set.** The `need_set_id` that preserved the supplied native projection.
2. **Selected goal.** The `selection_id` carried by the need set and native projection.
3. **Goal establishment.** The `goal_establishment_id` carried by the need set and native projection.
4. **Bounded horizon.** The `horizon_id` carried by the need set and native projection.
5. **Family.** One native family: `clarification`, `inquiry`, `authority`, or `operational_realization`.
6. **Native projection.** The exact supplied `native_projection_id` and type for that family.
7. **Native item.** The family-specific `native_item_key` plus lineage fields.
8. **Standing.** The native standing bucket and native standing value, preserved without reinterpretation.
9. **Component lineage.** The bounded uncertainty, authority, or realization component refs and any subject, class, scope, or transformation refs that locally distinguish the item.
10. **Evidence and source lineage.** Evidence refs and source refs already carried by native items or their testimony lineage.

A mismatch at any binding layer should produce a visible reference-set conflict or omitted reference with conflict testimony, not a repaired identity.

## Selectable and non-selectable records remain visible

The reference set should include visible references for every native item in every supplied native projection, not only established needs.

The reason is boundary preservation: exact operator focus may be directed at an unsupported, unknown, conflicting, excluded, outside-scope, unclassified-here, or unclassified native record. The reference projection must make that record addressable so a later selection boundary can say, precisely and read-only, that the focused record is not selectable as an established need.

Selectable status should be derived only from native standing, not from family order, label text, sufficiency reasons, priority, severity, or uniqueness:

| Native bucket | Reference visible? | Selectable for later consideration selection? | Reason |
| --- | --- | --- | --- |
| `established` | yes | yes | native family established need standing |
| `unsupported` | yes | no | family did not establish need |
| `unknown` | yes | no | preserved uncertainty, not established need |
| `conflicting` | yes | no | preserved conflict, not selectable need |
| `excluded_family` | yes | no | outside this bounded family/horizon boundary |
| `outside_current_scope` | yes | no | outside current bounded scope |
| `unclassified_here` | yes | no | not classified as operational-realization need here |
| `unclassified` | yes | no | not classified as native need here |

A reference being visible therefore means only that the native item can be exactly named. It does not mean the need is selected, established across families, prioritized, routed, authorized, or executable.

## All native items or only established needs?

The reference set should include all native items in supplied native projections.

Including only established needs would hide the exact records that the guardrails explicitly require to remain visible: unsupported, unknown, conflicting, excluded, outside-scope, and unclassified native records. It would also force later focus/selection boundaries to report non-selectable focus imprecisely, because the operator-facing reference would not exist for the non-selectable item.

Absent family records and excluded family assembly records are different: they do not contain native items. The reference set should preserve family-level absence or exclusion in summary fields, but should not invent item references for absent native items.

## Does an existing owner already perform this projection?

No reviewed owner performs this projection.

Existing owners stop before this responsibility:

- Native need projections own family-specific testimony classification and native standing buckets.
- `GoalAdvancementNeedSet` owns preservation of supplied, absent, and excluded native projections for one horizon, but does not expose one shared reference per native item.
- `GoalAdvancementSufficiencyProjection` owns bounded sufficiency conclusion over need set plus coverage, but does not create exact item references and must not select, rank, or route needs.
- `AdvancementNeedConsiderationSelection` has been audited as a later focus-selection boundary, but that audit depends on exact native need identity and does not itself supply the missing reference projection.

Therefore `AdvancementNeedReferenceSet` is a missing interstitial visibility boundary between need-set assembly and consideration selection.

## Smallest missing responsibility

The smallest missing responsibility is:

```text
Read one exact GoalAdvancementNeedSet, enumerate every item in each supplied native need projection, and emit one stable read-only AdvancementNeedReference per native item that binds need set, selected goal, goal establishment, horizon, family, native projection, native standing, native item lineage, component lineage, evidence lineage, visibility, and selectable status without reclassifying, ranking, selecting, routing, authorizing, executing, recording, writing the event ledger, or mutating state.
```

This responsibility should reject or preserve conflicts for duplicate native item keys and projection identity mismatches rather than deriving fallback identity from serialized payload fingerprints.

## Is one read-only implementation slice warranted?

Yes. One narrow read-only implementation slice is warranted if Seed needs exact operator focus or later consideration selection to become executable.

The slice should add only:

- `AdvancementNeedReference` and `AdvancementNeedReferenceSet` dataclasses;
- a family-specific native item key builder for each of the four current projection item types;
- an assembler over one exact `GoalAdvancementNeedSet`;
- visible references for every native item in supplied projections;
- selectable status only for `established` bucket references;
- non-selectable reasons for unsupported, unknown, conflicting, excluded, outside-scope, unclassified-here, and unclassified records;
- duplicate-key conflict preservation;
- tests proving all four families receive references;
- tests proving non-established records remain visible but non-selectable;
- tests proving reference projection does not select, prioritize, route, inspect sufficiency reasons, request authority, select realization, authorize, execute, record, write the event ledger, or mutate cluster state.

The slice should not expose a CLI diagnostic unless explicitly requested. If exposed as a diagnostic, audit, probe, view, operational CLI flag, or recordable output, the repository operational visibility contract requires diagnostic inventory registration, diagnostic shape-audit specs, and tests for both surfaces.

## Exact next bounded question

```text
What is the minimal read-only `AdvancementNeedReferenceSet` schema and assembler that consumes one exact `GoalAdvancementNeedSet`, emits one stable non-fingerprint `AdvancementNeedReference` for every native item in each supplied clarification, inquiry, authority, and operational-realization projection, marks only established native records selectable for later consideration selection, preserves all non-established records as visible non-selectable references, and proves no need is reclassified, prioritized, selected, routed, authorized, executed, recorded, written to the event ledger, or used to mutate state?
```

## Conclusion

Each native need record can lawfully receive one stable read-only reference by binding the exact `GoalAdvancementNeedSet`, selected goal, goal establishment, horizon, family, native projection, native standing bucket, family-specific native lineage, component lineage, evidence refs, and source refs. Native item identity is currently recoverable as family-specific lineage but is not yet a first-class item id, so the minimum boundary should define deterministic native item keys and treat duplicate keys as conflicts rather than relying on serialized payload fingerprints. The `AdvancementNeedReferenceSet` should include all native items from supplied projections, not only established needs, because non-established records must remain exactly visible while non-selectable. No reviewed owner already performs this projection. The smallest missing responsibility is an interstitial read-only reference assembler between `GoalAdvancementNeedSet` and later consideration selection.

Advancement need reference projection audit complete.
