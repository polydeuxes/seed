# Constitutional Provenance Investigation

Repository authority wins.

## Boundary

This is exactly one Constitutional Provenance Investigation. It does not recover implementation ownership, redesign implementation, invent runtime tracing, invent provenance records, invent execution logs, invent explanation engines, infer provenance from architectural expectation, or promote inferred provenance into repository fact.

The bounded answer used for this investigation is the implementation-backed `current operational explanation` answer surface, because the repository already exposes it as an exact Question Family with a dispatch surface and a bounded read-only answer artifact.

## App visibility used

The app was used only for bounded repository visibility:

```text
python scripts/seed_local.py --question-surface-inventory
python scripts/seed_local.py --inquiry-artifacts
python scripts/seed_local.py ask --question-family "current operational explanation" --json
```

The first command reported `current operational explanation` as `eligible_now`, dispatching to `operational_story`, with responsibility for a broad operational explanation from existing evidence, pressure, constraints, outcomes, and investigation path, and with a read-only/no-recording/no-event-ledger/no-cluster-mutation boundary.

The second command reported inquiry artifacts as read-only and non-recording, with no event ledger writes, no cluster mutation, no inquiry graph creation, no pressure transformation inference, and no workflow or planning behavior. It classified `unknown` and `boundary` as repository-visible, `pressure`, `finding`, and `gap` as partially visible, and `supported_conclusion`, `unsupported_conclusion`, and `open_question` as document-visible.

The third command produced the selected bounded answer artifact for `current operational explanation`: an `OperationalStory` JSON answer with `focus`, `pressure`, `supporting_evidence`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`, `investigation_path`, `unknowns`, and a read-only boundary.

The app output is used only as repository-visible observation. It is not treated as semantic interpretation beyond the surface shapes it emitted.

## Reviewed implementation observations

### Question admission

`seed_runtime/question_surface_inventory.py` preserves exact Question Family admission. `BOUNDED_ASK_DISPATCH_SURFACES` maps `current operational explanation` to `operational_story`; `bounded_status_for_question_family` returns `eligible_now` for mapped families; exact lookup rejects unknown Question Families; bounded eligibility records `permitted`, required surface arguments, and reason; selection prepares the dispatch surface and selected surface value; dispatch request/result helpers preserve the CLI namespace handoff without claiming answer composition or semantic routing.

Implementation observation: question admission is directly observable for this bounded answer only as exact inventory-backed bounded-ask eligibility and dispatch selection. It is not the full constitutional Question Grammar.

### Orientation

`seed_runtime/inquiry_orientation.py` preserves a separate read-only inquiry-note orientation probe. It records notes in an isolated JSONL store; prepares a composition request from preserved operator prose; composes related material from projected state; assembles an implementation-local `_InquiryOrientationAnswer`; and emits an `InquiryOrientationView` with related material, uncertainty, and authority boundary. Its authority boundary states that orientation is read-only and that the note is preserved operator prose, not fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction.

Implementation observation: orientation artifacts exist, but the selected bounded answer `current operational explanation` does not directly traverse the inquiry-note orientation probe in the reviewed implementation. Orientation is implementation-visible as an adjacent surface, not directly observable as a required stage in this answer's execution.

### Recovery

`seed_runtime/operational_story.py` composes the bounded answer from existing visibility surfaces: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. It separates implementation-local answer payload, limitations payload, reasoning payload, supporting-evidence payload, and authority-boundary payload before returning the public `OperationalStory` artifact.

Implementation observation: recovery of operational evidence into a bounded answer is directly observable as answer composition from existing surfaces. It is not implementation ownership recovery.

### Artifact production

`OperationalStory` is the public answer artifact. It exposes answer content, supporting evidence, investigation path, Unknowns, and a boundary. The implementation-local payloads preserve answer, reason, support, authority boundary, and limitations before public artifact assembly.

Implementation observation: artifact production is directly observable for the bounded answer.

### Producer / artifact / consumer ownership

For this bounded answer, the producer is implementation-visible as `build_operational_story`; the artifact is `OperationalStory`; consumers include JSON rendering through `operational_story_json`, human rendering through `format_operational_story`, question-family dispatch through `operational_story`, and downstream reasoning-path consumption where `build_reasoning_path_audit` builds an operational story and records story impact/consumer lineage when relevant.

Implementation observation: producer/artifact/consumer boundaries are implementation-visible and partially directly observable through question inventory and JSON output. They are not preserved as a single constitutional-provenance chain.

### Governance

Implementation governance is visible through explicit read-only boundaries: `OperationalStory.boundary` sets `mode=read_only_view`, `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`. Question inventory records the same no-recording/no-event-ledger/no-cluster-mutation boundary for `current operational explanation`. Inquiry artifacts preserve read-only/no-recording/no-event-ledger/no-cluster-mutation/no-inquiry-graph/no-pressure-transformation/no-workflow-or-planning boundaries.

Implementation observation: governance boundaries are directly observable.

### Fidelity

`constitution.md` governs repository authority, evidence-before-transition, pressure-not-command, explicit authority, compatibility preservation, positive stop, artifact handoff, and local reasoning bounded by handoff artifacts. `constitutional_fidelity_characterization.md` characterizes lawful realization as boundary-preserving rather than structurally symmetrical and states that Fidelity does not own Pressure, Question Admission, Orientation, Recovery, Cross-Examination, Completion Audit, Lawful Stop, implementation ownership, or constitutional ownership.

Implementation observation: fidelity authority is constitutionally observable in documents, while implementation realization is observable only through the selected surface's boundaries and artifact shapes.

### Compatibility

Compatibility is visible in question-family dispatch preserving existing CLI surfaces and in `OperationalStory` preserving a stable JSON/human answer shape while composing existing audits. The bounded ask helpers explicitly say they do not decide answer composition, rendering, diagnostics, schema, event ledger, or semantic routing when preparing/dispatching the selected surface.

Implementation observation: compatibility realization is reconstructable from dispatch and public artifact preservation, but not directly recorded as a provenance stage in the emitted answer.

### Lawful stop

Constitutionally, lawful stop is a positive result in `constitution.md` and in `constitutional_process_reconciliation.md`. Implementation-local stop is visible in exact lookup refusal, bounded eligibility refusal, diagnostic-only/non-dispatchable refusal, required surface-argument validation, typed Unknown preservation, and read-only boundaries. For the selected successful answer, no direct emitted `Lawful Stop` stage is present; stop is visible as boundaries and Unknowns rather than a provenance event.

Implementation observation: lawful stop is reconstructable as local refusal/Unknown/boundary behavior, but the selected successful answer does not directly expose a stop movement.

## Reviewed constitutional observations

`constitution.md` records the central discipline:

```text
Null / unknown / uncommitted
-> observation
-> bounded unknown
-> inquiry
-> evidence
-> supported transition or explicit stop
-> bounded handoff artifact
```

It further requires that repository authority wins; observation precedes inquiry; evidence moves Null; inquiry is bounded work preserving observation, evidence, classification/conclusion, authority, and stop condition; every surface must know what it may and may not do; compatibility preservation is the default recovery constraint; stop is a positive result; and competencies exchange artifacts rather than shared internal state.

`constitutional_process_reconciliation.md` recovers a recurring process pattern:

```text
Pressure
    ↓
Lawful Question
    ↓
Orientation
    ↓
Recovery
    ↓
Cross-Examination
    ↓
Completion Audit
    ↓
Lawful Stop
```

It explicitly warns that this is process-level recurrence, not a universal engine, runtime pipeline, implementation topology, ownership chain, or state machine.

`constitutional_fidelity_characterization.md` governs lawful realization: constitutional authority comes from completed constitutional evidence; implementation ownership comes from implementation evidence; structural symmetry is neither required nor sufficient; implementation realization is lawful only when constitutional authority is preserved; implementation-only mechanics remain constitutionally neutral until they claim, erase, mutate, or relocate constitutional authority; and unsupported conclusions remain Unknown.

## Observable provenance

For the bounded answer `current operational explanation`, the following repository observations already exist:

1. Exact Question Family row and bounded eligibility are observable in `question_surface_inventory`.
2. Dispatch surface `operational_story` is observable in the bounded-ask dispatch map and app output.
3. Public artifact `OperationalStory` is observable in code and JSON output.
4. Answer composition from pressure, capability, privilege, correlation, impact, and investigation-path surfaces is implementation-visible in `build_operational_story`.
5. Supporting evidence, investigation path, Unknowns, and read-only governance boundary are observable in the public artifact.
6. Diagnostic/inquiry artifact boundaries are observable through `inquiry_artifacts`.
7. Constitutional authority governing evidence, authority, compatibility, handoff artifacts, Unknowns, and lawful stop is observable in `constitution.md`, `constitutional_process_reconciliation.md`, and `constitutional_fidelity_characterization.md`.

## Reconstructable provenance

The repository can reconstruct a partial provenance for one bounded answer without inventing a new provenance record:

- A lawful bounded ask can be reconstructed from exact Question Family inventory admission and bounded eligibility.
- The selected implementation surface can be reconstructed from the dispatch map and selection helpers.
- The producer and artifact can be reconstructed from `build_operational_story` and `OperationalStory`.
- The answer evidence inputs can be reconstructed from the composition calls inside `build_operational_story` and from the emitted public fields.
- Governance boundaries can be reconstructed from the artifact boundary and inventory boundary.
- Compatibility realization can be reconstructed from existing dispatch-surface preservation and public JSON/human formatter preservation.
- Lawful stop pressure can be reconstructed as refusal/Unknown/boundary behavior, but not as a directly emitted successful-answer stage.

## Movements that cannot presently be reconstructed

The repository evidence does not presently reconstruct these movements for the selected bounded answer:

1. The original pressure that caused an operator to ask this specific bounded question, unless the operator's prompt or an inquiry note is separately preserved.
2. A constitutional Lawful Question admission record beyond exact implementation-backed Question Family eligibility.
3. A direct Orientation movement between admission and `OperationalStory` production.
4. A constitutional Recovery movement distinct from implementation answer composition.
5. A single durable producer/artifact/consumer provenance chain crossing every stage.
6. A direct governance-exercised event per stage; only boundaries and field shapes are visible.
7. A direct compatibility-realization event; compatibility is inferred from preserved dispatch and public artifact behavior.
8. A direct Lawful Stop event for this successful answer; stop is visible only as boundaries, Unknowns, and refusal paths.
9. The final explanatory answer's causal path as a runtime trace; no execution log or provenance record is present, and none may be invented.

## Reconstruction classification

| Stage | Classification | Repository evidence and limit |
| --- | --- | --- |
| Pressure | implementation-visible only | Operational pressure can be observed inside `OperationalStory.pressure` and `pressure_audit`, but the pressure causing this bounded ask is not recorded. |
| Lawful Question | directly observable | Exact Question Family inventory, bounded status, eligibility, and dispatch mapping are observable for `current operational explanation`; this is narrower than full constitutional Question Grammar. |
| Orientation | implementation-visible only | Inquiry-note orientation exists as a read-only probe, but this bounded answer does not directly expose an orientation stage. |
| Recovery | reconstructable | Existing visibility surfaces are collected into answer payloads; this can be reconstructed from code and output, but no constitutional recovery record is emitted. |
| Producer | implementation-visible only | `build_operational_story` is the implementation producer; producer identity is not emitted as provenance in the answer artifact. |
| Artifact | directly observable | `OperationalStory` is emitted as public JSON/human answer artifact. |
| Consumer | reconstructable | CLI bounded ask, JSON formatter, human formatter, and reasoning-path story-impact consumption are visible in implementation, but the emitted answer does not list all consumers. |
| Governance boundaries exercised | directly observable | Read-only/no-recording/no-event-ledger/no-cluster-mutation boundaries are emitted in inventory and answer artifact. |
| Compatibility realization | reconstructable | Dispatch preserves existing CLI surface and public artifact shape; compatibility is not emitted as a provenance event. |
| Lawful Stop | constitutionally inferred | Constitutional stop authority is direct in documents, and implementation refusal/Unknown paths exist, but the selected successful answer has no direct stop event. |
| Answer | directly observable | The JSON `OperationalStory` answer is emitted by the app. |

## Missing observability

| Stage not directly observable | Missing evidence | Enough repository information to reconstruct later? | Would additional observability reduce explanatory pressure? |
| --- | --- | --- | --- |
| Pressure | Preserved prompt-to-pressure or pressure-to-ask evidence for this bounded answer. | Partially. Operational pressure exists, but originating ask pressure is absent unless prompt/inquiry note is preserved. | Yes. It would reduce pressure around why this answer was selected. |
| Orientation | Evidence that the selected bounded answer traversed Orientation or intentionally bypassed it. | No for this answer. The repository has adjacent orientation implementation, not a link. | Yes, if lawful and evidence-backed; absent that, Orientation must remain not directly reconstructed. |
| Recovery | A constitutional recovery artifact distinct from implementation composition. | Partially. Code reconstructs composition from existing surfaces; constitutional recovery remains inferred. | Somewhat. It would reduce pressure only if it preserved actual evidence rather than invented stages. |
| Producer | Emitted producer identifier or production boundary in the answer. | Yes. Code identifies the producer. | Low to medium. Current code suffices for implementation reconstruction, but not emitted provenance. |
| Consumer | Emitted consumer lineage for the produced answer. | Partially. Known consumers can be found in implementation. Actual runtime consumer remains unknown. | Medium. It would reduce pressure around downstream explanation. |
| Compatibility realization | Explicit compatibility evidence for the dispatch and artifact handoff. | Yes. Existing dispatch maps, formatter names, and public shape support reconstruction. | Low. Compatibility is already strongly reconstructable, but not directly emitted. |
| Lawful Stop | A successful-answer stop marker or terminal boundary explaining why no further constitutional movement was taken. | Partially. Boundaries and Unknowns support a stop discipline; a stage-specific stop is absent. | Yes. It would reduce pressure around why the answer is bounded rather than incomplete. |

## Provenance boundaries

### Provenance that must never be invented

- The operator's internal reason for asking the question.
- A runtime trace that was not recorded.
- A provenance record that does not exist.
- A direct Orientation stage for `OperationalStory` execution.
- A constitutional Recovery event distinct from implementation answer composition unless a repository artifact preserves it.
- Producer/artifact/consumer lineage beyond repository-visible implementation and emitted artifacts.
- Compatibility or Lawful Stop events as facts when only boundaries and code behavior are visible.

### Provenance that may be reconstructed only from repository evidence

- Exact Question Family admission and bounded eligibility.
- Selected dispatch surface and surface value.
- Implementation producer and public artifact.
- Input surfaces used by `build_operational_story`.
- Public answer fields, supporting evidence, investigation path, Unknowns, and boundary.
- Known implementation consumers and formatters.
- Constitutional authority from reviewed constitutional artifacts.
- Compatibility preservation from dispatch and artifact-shape evidence.

### Provenance that must remain Unknown

- The originating pressure for this exact ask when not preserved.
- Whether a constitutional Orientation movement occurred for this answer.
- Whether a constitutional Recovery movement occurred as a distinct act beyond implementation composition.
- Actual downstream consumer use after the answer is emitted.
- Any causal runtime path not recorded by repository-visible artifacts.
- Whether Constitutional Provenance is already a recoverable constitutional discipline rather than explanatory pressure.

### Constitutional authority governing these boundaries

`constitution.md` governs the boundary by requiring repository authority, observation before inquiry, evidence to move Null, explicit authority, compatibility preservation, positive stop, and bounded handoff artifacts. `constitutional_process_reconciliation.md` prevents treating a recurring constitutional process as a universal engine or runtime pipeline. `constitutional_fidelity_characterization.md` prevents structural-symmetry demands and requires unsupported conclusions to remain Unknown rather than becoming authority.

## Readiness

```text
Constitutional Provenance remains explanatory pressure
```

The repository already preserves enough evidence to reconstruct portions of one bounded answer's provenance: exact question admission, dispatch selection, implementation producer, public artifact, some consumers, governance boundaries, compatibility behavior, Unknown preservation, and the emitted answer. However, it does not directly preserve the full constitutional provenance chain from originating Pressure through Lawful Stop for the selected answer. Several stages are only implementation-visible, reconstructable from code, constitutionally inferred, or Unknown. Therefore Constitutional Provenance is not yet supported as a recoverable constitutional discipline without invention.

## Confidence

Confidence is **high** that exact question admission, artifact production, governance boundaries, and the answer artifact are directly observable for `current operational explanation`.

Confidence is **medium** that producer/artifact/consumer and compatibility provenance are reconstructable from implementation evidence, because the code and public surfaces expose enough structure but do not emit a single provenance chain.

Confidence is **low** that Orientation, constitutional Recovery, originating Pressure, and Lawful Stop can be reconstructed for this bounded answer as actual movements. The repository preserves adjacent constitutional and implementation evidence, but not direct stage evidence for this answer.

Constitutional Provenance investigation complete.
