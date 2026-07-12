# Source-Local Testimony Profile Implementation Visibility Audit

This is exactly one bounded Implementation Visibility Audit. It searches for existing implementation evidence only. It does not implement source-local testimony profile preservation, does not implement a comparison gate, does not recover another constitutional characterization, and does not introduce any testimony engine, comparison engine, workflow, registry, planner, scheduler, universal testimony model, or universal profile type.

## Reviewed implementation evidence

Reviewed implementation adjacent to the requested neighborhoods:

- Grammar observation: `seed_runtime/knowledge/grammar_observation.py` and `tests/test_grammar_observation.py`.
- Observation agreement: `seed_runtime/knowledge/observation_agreement.py` and `tests/test_observation_agreement.py`.
- Inquiry orientation: `seed_runtime/inquiry_orientation.py` and `tests/test_inquiry_orientation.py`.
- Provider translation: `seed_runtime/model_client.py`, `seed_runtime/model_clients.py`, `seed_runtime/predicate_normalizers.py`, `seed_runtime/observations.py`, and nearby provider-oriented tests located by implementation search.
- Reconciliation / comparison-adjacent surfaces: implementation search for comparison and reconciliation terms in `seed_runtime/` and `tests/`.
- Diagnostic inventory: `seed_runtime/diagnostic_inventory.py`, `seed_runtime/diagnostic_shape_audit.py`, and diagnostic tests reached through the registry-backed shape-audit surface.
- Knowledge reachability: `seed_runtime/knowledge_reachability.py` and `tests/test_knowledge_reachability.py`.
- Implementation slices already recovered: nearby slice and audit reports were used only as pointers to implementation neighborhoods; classifications below rely on code and tests, not campaign vocabulary.

## Candidate occurrence 1: Observation Agreement

### Candidate producer

`observe_observation_agreements(...)` is the implementation-local producer. It consumes only already-supplied observation records and emits candidate agreement records when two or more independent streams provide exactly equal trimmed evidence text.

### Candidate artifact

`ObservationAgreementRecord` carries the preserved profile-like material. `ObservationAgreementEvidence` carries each supplied stream-local evidence reference.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: each `ObservationAgreementEvidence.stream` identifies the source stream such as documentation architectural relation, repository artifact, or relationship fact.
- **source**: each `ObservationAgreementEvidence.provenance` carries a source reference; the aggregate `ObservationAgreementRecord.provenance` preserves the record provenance tuple.
- **provenance/support**: `ObservationAgreementRecord.supporting_evidence` and `provenance` preserve supporting evidence and references.
- **authority boundary**: `non_promotion_boundary="candidate_only_not_architectural_truth"` and `OBSERVATION_AGREEMENT_BOUNDARY` reject promotion, grammar ownership, semantic interpretation, architectural truth, runtime mutation, event writes, ledger writes, repository mutation, and cluster mutation.
- **negative authority**: the boundary map explicitly marks adjacent authorities false, including `promotes_agreement`, `owns_grammar`, `semantic_interpretation`, and `architectural_truth`.
- **Unknowns**: no typed Unknown artifact is carried here. Absence of agreement is represented operationally by returning no record when independent/equal evidence is missing.
- **confidence**: no numeric or textual confidence field is preserved.
- **lawful stop**: no separate lawful-stop field is preserved; stop behavior is compressed into the no-record return path and non-promotion boundary.

### Candidate consumer

`observe_grammar_observations(...)` consumes `ObservationAgreementRecord` instances, not lower-level documentation, repository, or relationship observations.

### Lawful comparison gate

Implementation explicitly delays grammar-shaped comparison until candidate agreement profile artifacts exist: grammar observation accepts only `Sequence[ObservationAgreementRecord]`, groups by `_relation_shape(agreement.candidate_agreement)`, and emits a grammar observation only after at least two supplied agreement records share the same relation shape. Observation agreement itself also gates candidate agreement comparison by requiring two or more independent observation streams with exact evidence equality.

### Locally compressed responsibility

The profile is visible but local and compressed: source identity, source provenance, support, independence, candidate agreement, and non-promotion boundary are preserved, but constitutional fields are not named as a universal testimony profile. Unknowns, confidence, and lawful stop are not distinct artifact fields. The stop/gate is implemented as filtering and empty output rather than as a named comparison-gate artifact.

### Classification

Implementation-visible but locally compressed.

### Preserved Unknowns

Unknown whether other observation streams preserve richer testimony profiles before they become `ObservationAgreementEvidence`; this audit did not infer beyond supplied artifacts. Unknown whether absence-of-agreement should be represented as a typed Unknown in any future local surface; no current implementation evidence does so here.

### Confidence

High for implementation visibility of producer, artifact, support/provenance, independence, negative authority, and comparison delay. Medium for mapping lawful stop to no-record filtering because implementation evidence shows the behavior but does not name it as lawful stop.

## Candidate occurrence 2: Grammar Observation

### Candidate producer

`observe_grammar_observations(...)` is the implementation-local producer for recurring grammar relation observations.

### Candidate artifact

`GrammarObservationRecord` carries the implementation-local artifact.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: the producer is grammar observation over supplied observation agreement records.
- **source**: source is indirect; `supporting_agreements` preserves the agreement records and their stream-local evidence.
- **provenance/support**: `supporting_agreements`, flattened `provenance`, and `recurrence_evidence` are preserved.
- **authority boundary**: `non_promotion_boundary="grammar_observation_only_not_architectural_truth"` and `GRAMMAR_OBSERVATION_BOUNDARY` preserve non-promotion and reject adjacent authority.
- **negative authority**: the boundary map rejects grammar promotion, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, capability promotion, runtime mutation, event writes, ledger writes, repository mutation, and cluster mutation.
- **Unknowns**: no Unknown field is preserved.
- **confidence**: no confidence field is preserved.
- **lawful stop**: no explicit lawful-stop field is preserved; non-recurring shapes and malformed relation strings are ignored.

### Candidate consumer

The immediate implementation consumer is the returned tuple of grammar observations and the tests that assert grammar observation consumes agreements without semantic promotion. No broader runtime consumer was found in the searched implementation evidence.

### Lawful comparison gate

The comparison gate is direct and visible: grammar observation waits for `ObservationAgreementRecord` artifacts. It does not parse Markdown, Python, runtime state, or repositories. It compares relation shapes only after agreement records exist and emits only when at least two agreement records share the same shape.

### Locally compressed responsibility

The gate is implementation-visible but compressed into function input type, grouping, recurrence threshold, and boundary flags. The implementation does not expose a named comparison-gate artifact and does not preserve Unknowns or confidence.

### Classification

Implementation-visible but locally compressed.

### Preserved Unknowns

Unknown whether a current app or diagnostic surface consumes grammar observations; this audit found tests and module-level implementation evidence, not an operational CLI consumer.

### Confidence

High for delayed comparison after agreement records exist. Medium for consumer classification because the visible consumer evidence is test/module-level rather than a recurring app surface.

## Candidate occurrence 3: Inquiry Orientation

### Candidate producer

`record_inquiry_note(...)` preserves source-local operator testimony as an `InquiryNoteRecord`. `_prepare_inquiry_orientation_composition(...)` is the implementation-local handoff producer from preserved note to orientation composition.

### Candidate artifact

`InquiryNoteRecord` carries the preserved note. `_InquiryOrientationCompositionRequest`, `_InquiryOrientationEvidence`, `_InquiryOrientationSelectedMaterial`, `_InquiryOrientationAnswerPayload`, and `_InquiryOrientationAnswer` carry successive local artifacts for orientation composition.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: `record_inquiry_note(...)` records the note, and `_prepare_inquiry_orientation_composition(...)` prepares it for bounded orientation.
- **source**: `InquiryNoteRecord.source` defaults to `scripts.seed_local --record-inquiry-note`.
- **provenance/support**: `note_id`, `raw_note`, `recorded_at`, optional `workspace_id`, optional `session_id`, and later related-material `support` strings preserve local support for the note and matched material.
- **authority boundary**: `AUTHORITY_BOUNDARY` states that the orientation is read-only and that the note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction.
- **negative authority**: the same boundary denies ownership assertion, semantic interpretation, intent, concern, recommended action, and next safe move.
- **Unknowns**: uncertainty is preserved as `UNCERTAINTY_WITH_MATCHES` or `UNCERTAINTY_WITHOUT_MATCHES`; these are limitation strings, not typed Unknown records.
- **confidence**: no confidence field is preserved.
- **lawful stop**: no explicit lawful-stop field; the note remains preserved operator prose and orientation remains bounded/read-only.

### Candidate consumer

`build_inquiry_orientation(...)` consumes a preserved `InquiryNoteRecord`, calls `_prepare_inquiry_orientation_composition(...)`, collects evidence, selects related material, prepares an answer payload, and renders `InquiryOrientationView` through `format_inquiry_orientation(...)`.

### Lawful comparison gate

The orientation comparison/search gate is implementation-visible: related-material matching starts only after a preserved `InquiryNoteRecord` is supplied to `build_inquiry_orientation(...)` and transformed into `_InquiryOrientationCompositionRequest`. Matching is deterministic lexical overlap against projected fact supports and source-navigation matches, not comparison of unpreserved operator prose.

### Locally compressed responsibility

This is not a universal testimony profile. It preserves operator-note testimony locally, with source/provenance/support/boundary/limitations, but confidence is absent, Unknowns are limitation strings, and the comparison gate is encoded as call sequence and local request artifact rather than a named lawful comparison gate.

### Classification

Implementation-visible but locally compressed.

### Preserved Unknowns

Unknown whether inquiry orientation should preserve confidence; current implementation does not. Unknown whether unmatched notes should become typed Unknowns; current implementation preserves uncertainty text only.

### Confidence

High for note preservation, authority boundary, negative authority, and delayed lexical matching after note preservation. Medium for mapping limitation text to Unknowns because the implementation does not use typed Unknown artifacts here.

## Candidate occurrence 4: Provider Translation / Decision Prompt Rendering

### Candidate producer

`render_decision_prompt(...)` and `build_decision_prompt(...)` are provider-adjacent producers that translate a `DecisionInputPacket` into strict provider prompt text. `StrictJSONDecisionParser.parse(...)` and `parse_decision_text(...)` parse provider text back into `Decision` objects.

### Candidate artifact

Rendered prompt strings, allowed JSON decision shapes, and parsed `Decision` objects are the artifacts.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: prompt renderers and parsers are identifiable.
- **source**: rendered evidence includes selected input, state summary, visible tools, and open tool needs, but source-local testimony source is not preserved as a testimony profile.
- **provenance/support**: prompt rendering includes current input, facts, evidence, tools, and tool needs; however, provenance is selected and compacted for model decision context, not preserved as a source-local testimony profile.
- **authority boundary**: strict output instructions and parser validation constrain provider output shape.
- **negative authority**: unexpected fields, wrappers, missing kind/reason, invalid JSON, and code fences are rejected in parser paths.
- **Unknowns**: no testimony-profile Unknown field is preserved.
- **confidence**: entity/fact/evidence confidence may be rendered when present, but not as a complete source-local testimony profile.
- **lawful stop**: parser errors stop malformed provider output from becoming a `Decision`.

### Candidate consumer

`DecisionPromptModelClient.complete(...)`, `ParsedDecisionProducer.decide(...)`, local model clients, and runtime decision production consume these artifacts.

### Lawful comparison gate

No implementation evidence shows comparison waiting until a source-local testimony profile exists. The visible gate is strict provider-output parsing and allowed-shape validation, not a source-local testimony profile comparison gate.

### Locally compressed responsibility

Provider translation preserves decision-context and output-shape boundaries, but not the recovered constitutional boundary under audit. It is adjacent but not an occurrence of source-local testimony profile preservation.

### Classification

Constitutional only.

### Preserved Unknowns

Unknown whether any provider-specific adapter preserves a fuller source-local testimony profile outside the inspected prompt/parser paths. No current evidence supports that inference.

### Confidence

Medium-high that this neighborhood is not an implementation occurrence of the audited boundary, because implementation evidence points to prompt/output shape validation rather than testimony-profile preservation.

## Candidate occurrence 5: Diagnostic Inventory and Diagnostic Shape Audit

### Candidate producer

`DIAGNOSTIC_INVENTORY` entries and `DiagnosticImplementationSpec` entries are implementation-local producers/artifacts for diagnostic surface declarations and static shape audit checks.

### Candidate artifact

`DiagnosticInventoryEntry`, `DiagnosticImplementationSpec`, `DiagnosticShapeAuditRow`, and related diagnostic shape audit summaries are the artifacts.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: diagnostic inventory and shape-audit builders are identifiable.
- **source**: module paths, build/format/json/record functions, CLI flags, and marker fields identify implementation sources.
- **provenance/support**: shape audit compares declared inventory fields against static implementation markers.
- **authority boundary**: inventory fields declare `record_scope`, event-ledger writes, cluster mutation, projected-state usage, repo-file usage, diagnostic fact emission, and diagnostic fact reads.
- **negative authority**: `mutates_cluster`, `writes_event_ledger`, and related declared/observed fields can preserve negative operational authority.
- **Unknowns**: shape audit has `unknown` status.
- **confidence**: no testimony-profile confidence field is preserved.
- **lawful stop**: mismatch/warning/unknown statuses report inconsistency but do not form a testimony-profile comparison gate.

### Candidate consumer

Diagnostic inventory output and diagnostic shape audit consume these declarations/specifications. Tests consume the rows to prove inventory/shape visibility.

### Lawful comparison gate

There is a registry-backed declaration-before-audit shape: shape audit compares implementation markers to existing inventory/spec declarations. However, this is a diagnostic surface declaration gate, not source-local testimony profile preservation, and it does not require a testimony profile before comparison.

### Locally compressed responsibility

Operational profile preservation is visible for diagnostics, but the profile is diagnostic-surface shape, not source-local testimony. This neighborhood should not be promoted into the audited boundary.

### Classification

Constitutional only.

### Preserved Unknowns

Unknown whether any specific diagnostic surface separately preserves source-local testimony profiles; this audit did not infer from diagnostic registration alone.

### Confidence

High that diagnostic inventory/shape audit are adjacent visibility machinery, not an implementation occurrence of the audited source-local testimony profile boundary.

## Candidate occurrence 6: Knowledge Reachability

### Candidate producer

`build_knowledge_reachability_audit_result(...)` and related internal reachability collection functions produce rows that track candidates across preserved, projected, read-model, inquiry-orientation, and rendered stages.

### Candidate artifact

`KnowledgeReachabilityRow`, `KnowledgeReachabilityMetadata`, and `KnowledgeReachabilityAuditResult` are the artifacts.

### Preserved constitutional-profile fields

Preserved by implementation evidence:

- **producer**: knowledge reachability audit builders are identifiable.
- **source**: candidate sources and scan counts are preserved in metadata.
- **provenance/support**: candidate source counts and family/stage fields preserve reachability evidence at an aggregate level.
- **authority boundary**: candidate kinds distinguish presentation labels, repository concepts, schema fields, runtime values, platform values, generated identifiers, network identifiers, relationship labels, and unknown.
- **negative authority**: first-loss and stage booleans prevent assuming presentation vocabulary is preserved/projected knowledge.
- **Unknowns**: candidate kind includes `unknown`, and first-loss can preserve non-reachability.
- **confidence**: no testimony-profile confidence field is preserved.
- **lawful stop**: reachability can show first loss, but not as a testimony-profile comparison gate.

### Candidate consumer

The audit formatter and JSON output consume reachability rows; tests assert reachability behavior.

### Lawful comparison gate

No source-local testimony profile gate was found. Knowledge reachability checks whether candidate terms survive across implementation stages; it does not delay comparison until producer/source/provenance/support/authority/Unknown/confidence/lawful-stop profile fields exist.

### Locally compressed responsibility

Knowledge reachability is an implementation-visible guard against promoting presentation vocabulary into knowledge, but it is not the recovered source-local testimony profile boundary.

### Classification

Constitutional only.

### Preserved Unknowns

Unknown whether some candidate source inside reachability has its own source-local testimony profile; current reachability artifacts aggregate candidates rather than preserve the constitutional profile under audit.

### Confidence

High that this is adjacent boundary evidence only.

## Readiness classification summary

| Candidate occurrence | Classification | Reason |
| --- | --- | --- |
| Observation Agreement | Implementation-visible but locally compressed | Preserves stream, provenance, support, candidate agreement, independence, and non-promotion; comparison waits for independent supplied evidence; Unknown/confidence/lawful-stop fields remain compressed or absent. |
| Grammar Observation | Implementation-visible but locally compressed | Consumes only agreement records and waits for recurring shape across agreements; support/provenance/boundary visible; no named universal testimony profile, Unknown, confidence, or explicit lawful-stop field. |
| Inquiry Orientation | Implementation-visible but locally compressed | Preserves operator note before lexical orientation; source/provenance/boundary/limitations visible; comparison waits for note/request artifact; confidence and typed Unknowns absent. |
| Provider Translation / Decision Prompt Rendering | Constitutional only | Adjacent provider boundary and strict output validation exist, but no source-local testimony profile gate is implementation-visible. |
| Diagnostic Inventory / Shape Audit | Constitutional only | Diagnostic surface profile and declaration-before-audit are visible, but not source-local testimony profile preservation. |
| Knowledge Reachability | Constitutional only | Reachability prevents unsupported vocabulary promotion, but does not implement the audited testimony-profile comparison gate. |

## Preserved Unknowns for the audit

- Unknown whether broader implementation outside the inspected naturally adjacent neighborhoods contains another local occurrence; expansion stopped where implementation evidence stopped.
- Unknown whether any future local surface should expose typed Unknowns or confidence for observation agreement, grammar observation, or inquiry orientation; current implementation does not.
- Unknown whether grammar observations have a recurring operational app consumer beyond tests and module-level use; current evidence reviewed here does not prove one.
- Unknown whether provider adapters preserve richer source-local testimony profiles in uninspected external provider ecosystems; repository evidence reviewed here does not.

## Confidence

Overall confidence is high that the recurring implementation-visible occurrences are limited to observation agreement, grammar observation, and inquiry orientation, and that each is locally compressed rather than a universal profile model. Confidence is high that provider translation, diagnostic inventory/shape audit, and knowledge reachability are adjacent but not implementation occurrences of the audited boundary. Confidence is medium where constitutional vocabulary such as Unknowns and lawful stop maps only to local limitation strings, no-record filtering, parser refusal, or first-loss reporting rather than named fields.

According to recurring
implementation evidence,

where are

source-local testimony
profile preservation

and

the lawful comparison gate

already implementation-visible,

and what exact
implementation-local
responsibilities
remain compressed?

They are already implementation-visible in three local places only:

1. Observation Agreement preserves source-local testimony-like evidence as `ObservationAgreementEvidence` and `ObservationAgreementRecord`, then delays candidate agreement comparison until independent supplied observation streams provide matching evidence. Remaining compressed responsibilities: no universal testimony profile type; no typed Unknown field; no confidence field; lawful stop is represented by no emitted record and non-promotion boundary rather than a named lawful-stop artifact.

2. Grammar Observation preserves agreement-backed recurrence evidence as `GrammarObservationRecord`, then delays grammar-shape comparison until `ObservationAgreementRecord` artifacts already exist and at least two agreements share a relation shape. Remaining compressed responsibilities: no named comparison-gate artifact; source profile is indirect through supporting agreements; no typed Unknown field; no confidence field; lawful stop is represented by skipped malformed or non-recurring candidates and non-promotion boundary.

3. Inquiry Orientation preserves operator testimony as `InquiryNoteRecord`, then delays lexical related-material comparison until the note has been recorded and prepared as `_InquiryOrientationCompositionRequest`. Remaining compressed responsibilities: no universal testimony profile type; Unknowns are limitation strings rather than typed Unknown records; no confidence field; lawful stop is represented by read-only authority boundary, bounded matching, and no deterministic related-material output rather than a named lawful-stop artifact.

Implementation visibility audit complete.
