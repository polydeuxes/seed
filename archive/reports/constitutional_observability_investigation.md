# Constitutional Observability Investigation

Repository authority wins.

## Boundary

This is exactly one Constitutional Observability Investigation.

It reviews only:

- `constitutional_provenance_investigation.md`
- `constitutional_process_reconciliation.md`
- `constitutional_fidelity_characterization.md`
- implementation corresponding to the investigated bounded answer, `current operational explanation`

It does not recover Constitutional Provenance, redesign implementation, invent runtime tracing, invent execution logs, invent provenance records, invent explanation engines, infer visibility from architectural preference, or promote reconstructed evidence into direct observation.

The bounded answer remains the implementation-backed `current operational explanation` answer surface previously selected by the Constitutional Provenance Investigation. Repository authority wins.

## App visibility used

The app was used only for bounded repository visibility:

```text
python scripts/seed_local.py --question-surface-inventory
python scripts/seed_local.py --inquiry-artifacts
python scripts/seed_local.py ask --question-family "current operational explanation" --json
```

The question-surface inventory directly emitted `current operational explanation` as `eligible_now`, dispatched by `operational_story`, JSON-supported, human-rendered by `format_operational_story`, and bounded as a read-only view with no recording, no event-ledger writes, and no cluster mutation.

The inquiry-artifacts surface directly emitted a read-only/no-recording/no-event-ledger/no-cluster-mutation boundary. It classified `unknown` and `boundary` as repository-visible; `pressure`, `finding`, and `gap` as partially visible; and `supported_conclusion`, `unsupported_conclusion`, and `open_question` as document-visible.

The bounded ask emitted an `OperationalStory` JSON artifact containing `focus`, `pressure`, `supporting_evidence`, `capabilities`, `constraints`, `correlation_gaps`, `impact`, `recent_changes`, `observed_outcomes`, `investigation_path`, `unknowns`, and a read-only boundary. The current run reported an orphaned-predicates focus, direct pressure evidence from consumer audit, a correlation gap, impact metrics whose result remained `unknown`, investigation-path surfaces, and typed Unknowns for capabilities and impact.

The app output is used only as repository-visible observation. It is not treated as provenance, runtime trace, execution log, or semantic explanation beyond the surface shapes it emitted.

## Reviewed observations

### Reviewed constitutional observations

`constitutional_process_reconciliation.md` recovers a recurring constitutional movement:

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

It explicitly limits that movement to a bounded recurring process pattern, not a universal engine, runtime pipeline, implementation topology, ownership chain, state machine, or recovered implementation owner.

`constitutional_fidelity_characterization.md` governs the realization boundary. Constitutional authority comes from completed constitutional evidence. Implementation ownership and mechanics come from implementation evidence. Structural symmetry is neither required nor sufficient. Unsupported conclusions remain Unknown. Diagnostic and orientation findings must not silently become cluster truth.

`constitutional_provenance_investigation.md` reviewed the same bounded answer and concluded that Constitutional Provenance remains explanatory pressure. It found that the repository can observe or reconstruct portions of one bounded answer, but does not preserve a full provenance chain from originating Pressure through Lawful Stop.

### Reviewed implementation observations

`seed_runtime/question_surface_inventory.py` directly maps `current operational explanation` to `operational_story`; classifies mapped families as `eligible_now`; performs exact Question Family lookup; prepares bounded eligibility; selects dispatch surface and surface value; validates required surface arguments where needed; prepares dispatch requests; applies CLI namespace handoff; and preserves refusal paths for diagnostic-only or not-dispatchable families.

`seed_runtime/operational_story.py` defines the public `OperationalStory` artifact and composes it from existing implementation-visible surfaces: pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit. It separates implementation-local answer, reasoning, supporting-evidence, boundary, and limitations payloads before returning the public artifact. Its public boundary is `mode=read_only_view`, `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`.

No reviewed implementation emits a constitutional provenance record, runtime trace, execution log, or direct constitutional-stage ledger for the bounded answer. That absence is itself an observability boundary, not permission to invent one.

## Observability classifications

| Recovered constitutional movement | Classification for this bounded answer | Repository evidence and limit |
| --- | --- | --- |
| Pressure | directly observable for emitted operational pressure; Unknown for originating ask pressure | The `OperationalStory.pressure` field and app JSON directly emit operational pressure and supporting evidence. The repository does not establish the original constitutional pressure that caused this bounded question to be asked. |
| Lawful Question | directly observable as exact implementation-backed admission; constitutionally narrower than full Question Grammar | The inventory and implementation directly show exact Question Family eligibility for `current operational explanation`, dispatch mapping to `operational_story`, and refusal boundaries for non-admitted families. This does not recover the full Constitutional Question Grammar as a runtime stage. |
| Orientation | implementation-visible only as adjacent surface; Unknown as a movement in this answer | Inquiry-note orientation exists in the repository according to the provenance investigation, but the reviewed bounded-answer implementation does not directly traverse it or emit it for `current operational explanation`. |
| Recovery | reconstructable | `build_operational_story` reconstructably collects existing audits into answer, reasoning, supporting-evidence, boundary, and limitation payloads. No separate constitutional Recovery artifact is emitted. |
| Cross-Examination | constitutionally inferred for the recurring process; implementation-visible only as selected audit evidence | The process reconciliation supports Cross-Examination as a recurring constitutional movement, and the operational story may include correlation gaps or investigation-path audit surfaces. The bounded answer does not emit a constitutional Cross-Examination stage. |
| Completion Audit | constitutionally inferred; not directly established for this answer | The process reconciliation supports Completion Audit for completed districts. The bounded answer emits Unknowns and boundaries, but does not emit a completion-audit stage or sufficiency decision for this answer. |
| Lawful Stop | constitutionally inferred; reconstructable only through refusal, Unknown, and boundary behavior; not directly emitted | Constitutional documents support Lawful Stop. Implementation refusal paths, typed Unknowns, and read-only boundaries are visible. The successful answer does not emit a direct Lawful Stop event. |
| Fidelity / lawful realization boundary | constitutionally observable; implementation realization reconstructable | Fidelity is directly characterized in the reviewed document. Its implementation realization for this answer is visible through read-only boundaries, Unknown preservation, exact admission, and non-mutation behavior, not through a separate Fidelity runtime stage. |
| Governance boundary | directly observable | The inventory, inquiry-artifacts surface, and `OperationalStory.boundary` directly emit read-only/no-recording/no-event-ledger/no-cluster-mutation boundaries. |
| Artifact handoff | directly observable for the public artifact; reconstructable for dispatch handoff | The `OperationalStory` JSON artifact is emitted directly. Dispatch handoff from bounded ask to CLI namespace is reconstructable from implementation helpers, not emitted as constitutional movement. |

## Observable evidence

### 1. Observations emitted directly

The following observations are directly emitted by reviewed app or public artifact surfaces:

1. Exact Question Family visibility for `current operational explanation` in question-surface inventory.
2. Bounded status `eligible_now` for that Question Family.
3. Dispatch surface `operational_story`.
4. JSON support and human formatter identity for the answer surface.
5. Read-only/no-recording/no-event-ledger/no-cluster-mutation boundary in inventory and in the `OperationalStory` artifact.
6. Inquiry-artifact visibility classes for unknown, boundary, pressure, finding, supported conclusion, unsupported conclusion, open question, and gap.
7. The emitted `OperationalStory` answer fields.
8. Operational pressure, supporting evidence, correlation gap, impact Unknowns, investigation path, observed outcomes, and typed Unknowns emitted in the bounded answer.

### 2. Observations requiring implementation reconstruction

The following observations may be reconstructed from reviewed implementation, but must not be treated as directly emitted observations:

1. Exact lookup and bounded-eligibility preparation before dispatch.
2. Dispatch-surface and surface-value selection.
3. CLI namespace dispatch handoff and post-dispatch compatibility handling.
4. `build_operational_story` as the implementation producer.
5. Composition from pressure audit, capability needs, privilege discovery, correlation audit, impact audit, and investigation path audit.
6. Internal separation of answer, reasoning, supporting-evidence, limitations, and authority-boundary payloads.
7. Compatibility preservation through existing dispatch and rendering surfaces.
8. Local refusal behavior for diagnostic-only, unknown, non-dispatchable, or incorrectly parameterized bounded work.

### 3. Observations existing only constitutionally

The following observations exist in reviewed constitutional documents, not as direct emitted runtime evidence for this bounded answer:

1. Pressure is not command authority.
2. Lawful Question / Question Admission is a recurring constitutional discipline.
3. Orientation precedes Recovery in the recovered recurring process pattern.
4. Recovery is evidence-bounded and changes visibility only when admitted and oriented evidence exposes a lawful recoverable boundary.
5. Cross-Examination tests relation, dependency, non-collapse, and artifact consumption.
6. Completion Audit determines bounded sufficiency for visible evidence.
7. Lawful Stop is a positive constitutional result.
8. Constitutional Fidelity protects recovered authority during implementation realization without requiring structural symmetry.

### 4. Observations that cannot presently be established

The following cannot presently be established from reviewed repository evidence:

1. The originating constitutional pressure that caused this specific bounded ask.
2. That the selected answer traversed a direct Orientation movement.
3. That the selected answer emitted or preserved a constitutional Recovery artifact distinct from implementation composition.
4. That the selected answer executed a constitutional Cross-Examination movement.
5. That the selected answer executed a Completion Audit movement.
6. That the selected successful answer emitted a Lawful Stop event.
7. A full stage-by-stage constitutional provenance chain.
8. Any runtime trace, execution log, provenance record, explanation engine output, or durable constitutional-stage ledger for the answer.

## Reconstructable evidence

Repository evidence may reconstruct bounded implementation visibility where code and emitted surfaces provide enough evidence:

- exact admission and bounded eligibility from the inventory and selection helpers;
- selected dispatch surface from the dispatch map;
- public artifact shape from `OperationalStory` and `to_json_dict`;
- evidence input classes from the calls inside `build_operational_story`;
- limitations from typed Unknown preservation;
- governance boundaries from inventory and artifact fields;
- compatibility handoff from dispatch and formatter helpers;
- local refusal/stop pressure from exact lookup, eligibility, argument validation, Unknowns, and read-only boundaries.

This reconstruction remains implementation reconstruction. It must not be promoted into direct constitutional observation or provenance.

## Implementation-visible evidence

The following evidence is implementation-visible without being direct public observation of constitutional movement:

- the producer function `build_operational_story`;
- implementation-local payload dataclasses for answer, limitations, reasoning, supporting evidence, and boundary;
- exact lookup, eligibility, refusal, surface-argument, selection, presentation-handoff, dispatch-request, dispatch-result, namespace-update, and message-clear helper objects;
- neighboring inquiry orientation visibility described in the provenance investigation;
- local refusal paths and Unknown preservation mechanisms;
- downstream or adjacent consumption such as JSON rendering, human formatting, and reasoning-path interaction described by the provenance investigation.

Implementation-visible evidence may answer what the current implementation can show. It may not answer what constitutional provenance exists.

## Constitutionally inferred evidence

The following evidence is constitutionally inferred for this bounded answer only because reviewed constitutional documents establish the recurring discipline:

- Pressure must not be treated as command.
- Lawful admission must precede bounded inquiry.
- Orientation and Recovery are distinct constitutional disciplines even if not emitted by this implementation path.
- Cross-Examination and Completion Audit are recurring constitutional disciplines for recovered neighborhoods or districts, not mandatory emitted stages for every answer.
- Lawful Stop remains positive and may be represented by refusal, Unknown preservation, or bounded handoff where evidence supports it.
- Fidelity requires implementation realization not to collapse constitutional authority into implementation convenience or vocabulary.

These inferences govern boundaries. They do not create missing observations.

## Unknown evidence

The following Unknowns are preserved:

- Whether this specific bounded ask had a recoverable originating constitutional pressure.
- Whether Orientation was intentionally bypassed, unnecessary, or simply not represented for this answer.
- Whether implementation composition corresponds to a constitutional Recovery movement in this specific run.
- Whether any Cross-Examination occurred for this answer beyond implementation-visible correlation and investigation-path surfaces.
- Whether any Completion Audit occurred for this answer.
- Whether a successful-answer Lawful Stop occurred as a distinct movement.
- Whether a recurring observability discipline is recoverable as a named constitutional discipline rather than remaining explanatory pressure.
- Whether future repository evidence will support a durable constitutional observability artifact.

## Observability boundaries

### 1. What evidence may be reconstructed?

Evidence may be reconstructed when reviewed repository implementation or emitted app surfaces expose a bounded relation without requiring speculation. For this answer, exact admission, dispatch selection, producer identity, public artifact shape, evidence-input classes, limitations, governance boundaries, compatibility handoff, and local refusal behavior may be reconstructed.

### 2. What evidence must never be reconstructed?

The following must never be reconstructed from preference, vocabulary, or architectural expectation:

- Constitutional Provenance.
- Runtime tracing or execution logs.
- A stage-by-stage constitutional ledger.
- Originating operator pressure where no preserved prompt or inquiry note is reviewed.
- Direct Orientation, Cross-Examination, Completion Audit, or Lawful Stop events where the bounded answer does not emit them.
- Constitutional authority from implementation helper names alone.
- Implementation ownership from constitutional vocabulary alone.
- Cluster truth from diagnostic, inquiry, or orientation findings.

### 3. What evidence must remain Unknown?

Evidence must remain Unknown when it would require inventing missing observations, treating adjacent implementation as actual execution, or promoting constitutional recurrence into direct runtime fact. For this bounded answer, the originating pressure, direct Orientation traversal, distinct constitutional Recovery artifact, direct Cross-Examination, direct Completion Audit, direct successful-answer Lawful Stop, and full provenance chain remain Unknown.

### 4. Which constitutional disciplines govern those boundaries?

The boundaries are governed by:

- Constitutional Question Grammar / Lawful Question, because exact admission and bounded authority determine whether pressure becomes lawful work.
- Orientation, because admitted inquiry must not be replaced by unreviewed attention or presentation labels.
- Recovery, because visibility may change only from evidence-bounded recovery.
- Cross-Examination, because relation and non-collapse must be tested rather than assumed.
- Completion Audit, because bounded sufficiency is not automatic from local output.
- Lawful Stop, because Unknown preservation and refusal are positive outcomes.
- Constitutional Fidelity, because implementation realization must preserve constitutional authority without requiring or inventing structural symmetry.

## Coverage observations

Repository evidence supports a recurring observability coverage pattern, but not Constitutional Provenance.

The supported coverage classes are:

1. **Directly emitted public observation.** Evidence emitted by app surfaces or public artifacts, such as inventory rows, inquiry-artifact visibility classes, JSON answer fields, boundaries, pressure, Unknowns, and investigation path.
2. **Implementation-reconstructable observation.** Evidence reconstructable from reviewed implementation, such as exact lookup, bounded eligibility, dispatch selection, producer function, payload separation, composition inputs, and compatibility handoff.
3. **Implementation-visible-only observation.** Adjacent or internal implementation evidence visible in code but not emitted as public answer movement, such as inquiry orientation as an adjacent probe or internal payload classes.
4. **Constitutionally inferred observation.** Constitutional discipline visible in documents and applicable as boundary governance, such as Pressure-not-command, Orientation-before-Recovery, Completion Audit, Lawful Stop, and Fidelity.
5. **Preserved Unknown.** Evidence not established by reviewed repository sources, including originating pressure, direct Orientation for this answer, direct Cross-Examination, direct Completion Audit, direct successful-answer Lawful Stop, full provenance chain, and runtime trace.

This is an observability coverage pattern only. It does not characterize provenance, propose implementation, or recover a new implementation surface.

## Readiness

The repository evidence supports an observability classification pattern for one bounded answer. It supports distinguishing direct observation, reconstruction, implementation-visible-only evidence, constitutional inference, and Unknown.

However, the reviewed evidence does not yet establish Constitutional Observability as a recovered constitutional discipline with its own responsibility, artifacts, dependencies, consumers, stop conditions, and authority boundary. Current evidence supports an investigation result and coverage classes, not a recoverable named discipline.

Classification:

```text
Constitutional Observability remains explanatory pressure
```

## Confidence

- **High confidence** that direct observations for exact bounded admission, public artifact fields, operational pressure, typed Unknowns, investigation path, and read-only governance boundaries are presently observable.
- **High confidence** that implementation reconstruction is available for dispatch selection, producer identity, payload composition, evidence-input classes, compatibility handoff, and local refusal behavior.
- **Medium confidence** that the five coverage classes recur across the reviewed bounded answer and constitutional documents.
- **Low confidence** for any claim that Orientation, Cross-Examination, Completion Audit, or Lawful Stop are directly emitted movements in the selected answer.
- **Low confidence** for any claim that Constitutional Observability is ready for characterization as a recovered constitutional discipline rather than explanatory pressure.

Constitutional Observability investigation complete.
