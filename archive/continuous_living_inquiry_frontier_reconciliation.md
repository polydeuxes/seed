---
doc_type: reconciliation
status: frontier investigation
scope: continuous inquiry, blocked work, inquiry pressure, external idea source
---

# Continuous Living Inquiry Frontier Reconciliation

## Central finding

When operator-requested work is exhausted or blocked, the current repository does **not** show an implementation-backed scheduler, daemon, planner, autonomous worker, or execution governor.

It does show implementation-backed pressures that can remain legitimately worth asking about:

```text
new observations
repository inconsistencies
capability gaps
authority boundaries
uncertainty
runtime / operational visibility gaps
consumer gaps
ledger-preserved evidence changes
```

The strongest supported answer is therefore:

```text
Continuous living primarily extends observation, inquiry, event-ledger preservation,
repository diagnostics, capability reasoning, and runtime self-observation.
```

It does not currently require a fundamentally new architecture for discovering questions. It would require new architecture only if discovery were collapsed into scheduling, autonomous execution, or resource governance. This report does not recommend those responsibilities.

## Acceptance answers

### When Seed has nothing immediately actionable, what questions remain legitimately worth asking?

Implementation-backed questions remain around:

1. **What has changed?** Observation sources and the observation ingestor already preserve observations, evidence, and facts.
2. **What is inconsistent?** Diagnostic, contradiction, graph, shape, consumer, and pressure surfaces already expose repository and projection inconsistencies.
3. **What remains unsupported or weakly supported?** Evidence, confidence, contradiction, unsupported-fact, and consumer-audit surfaces preserve uncertainty and missing support.
4. **What capability is missing for an already visible concern?** Capability needs are derived from diagnostic records and current projected discrepancies.
5. **What authority blocks the current bounded inquiry?** Existing authority slices expose required observations, available authority, blocked observations, remaining observations, and uncertainty without executing observations.
6. **What operational resource or visibility pressure is present?** Current pressure audit already ranks diagnostic-shape, ownership, capability, orphaned predicate, and fragile predicate pressure; runtime self-observation work found that process/resource self-observation is architecturally natural but not fully implemented.

These are questions, not execution decisions.

### Can externally proposed ideas flow through the existing inquiry architecture without becoming decisions or execution?

Yes, if they enter as observed inputs or bounded inquiry artifacts. The repository already treats natural-language communication as observation rather than authority, validates structured decisions before routing, rejects unsupported decision kinds, and routes only specific validated decisions. Externally proposed hypotheses can therefore be preserved as candidate observations or inquiry notes without becoming decisions, execution, cluster truth, or authority.

The current gap is that there is no single implementation-backed field that distinguishes an externally proposed hypothesis from an operator-requested inquiry or from a self-initiated inquiry. That is an observable attribution/provenance gap, not evidence that proposals must bypass inquiry.

### Does continuous living extend the current architecture or require a fundamentally new one?

For discovery of worthwhile inquiry, it primarily extends the current architecture:

```text
observation -> evidence -> projection -> diagnostics/inquiry/capability pressure -> bounded questions
```

A fundamentally new architecture would be required only for scheduling, autonomous execution, or resource-governance responsibilities, which are outside this investigation and outside the current core boundary.

## 1. Pressures remaining when current concerns are blocked

### Supported remaining pressures

| Pressure | Implementation-backed support | Boundary |
| --- | --- | --- |
| New observations | `ObservationSource.collect()` returns observations; `ObservationIngestor` records `observation.observed`, `evidence.observed`, and `fact.observed` / `fact.inferred` events. | Observations become evidence-backed claims, not automatic decisions. |
| Repository inconsistencies | `PressureAudit` includes diagnostic-shape pressure and consumer-audit pressure for orphaned and fragile predicates. | The audit ranks pressure and recommends inspection; it does not plan or mutate. |
| Knowledge/evidence gaps | The README identifies contradiction, confidence, staleness, graph-issue, explanation, and capability-gap surfaces as owned knowledge-path responsibilities. | Projection and diagnostics communicate selected knowledge, not authority by themselves. |
| Capability gaps | `build_capability_needs()` derives capability needs from ownership discrepancies and recorded diagnostic facts scoped to `diagnostic_run:*`. | Capability pressure is downstream of projected evidence; it is not execution. |
| Authority blocks | Container and service ownership authority slices expose required authority, available authority, blocked/remaining observations, outcome, and uncertainty. | Supplied authority profile is authoritative for those diagnostics; approvals in projected state do not grant authority. |
| Operational / runtime pressure | `PressureAudit` ranks operational pressure from existing visibility surfaces. Runtime self-observation work identifies a supported model but an implementation gap for first-class Seed process metrics. | Current support is diagnostic and observational, not self-regulating policy. |
| Operator preference / request pressure | Runtime records `input.user_message`, composes state, validates decisions, and routes only bounded decision kinds. README treats natural language as observation of communicative acts. | Request evidence is not environmental truth and does not bypass validation. |
| Environment change | Local-host, repository, repository-source, Prometheus, and other observation sources are collection adapters; current facts can change when observations change. | Collection is explicit through current surfaces, not continuously scheduled by core runtime. |

### Strongest supporting evidence

- Seed's top-level scope is continuous maintenance of evidence-backed answers to bounded questions, with inquiry owning questions and subsystems owning answers.
- The observation pipeline has a stable source protocol and append-only observation/evidence/fact ingestion.
- The event ledger is append-only event history read by projection and owner services.
- Pressure audit already transforms diagnostic, ownership, capability, orphaned-predicate, and fragile-predicate evidence into ranked pressure items.
- Authority slices already expose blocked and remaining work without executing or recording operational changes.

### Strongest contradictory evidence

- No current component continuously wakes up to discover questions.
- The canonical runtime routes user-message-triggered validated decisions; it does not autonomously select inquiries.
- Runtime self-observation is not yet a first-class observation source for process memory, ledger growth, projection cost, or queue depth.

## 2. Operator-requested inquiry vs self-initiated inquiry

The repository has an implementation-backed distinction between **operator input** and other observation sources, but not a complete implementation-backed distinction between **operator-requested inquiry** and **self-initiated inquiry**.

Supported distinctions:

- Runtime records operator input as `input.user_message` with actor `user`.
- Observations have source types such as `user`, `discovery`, `provider`, `imported`, and `inferred`.
- Inquiry notes can be recorded by CLI as inquiry artifacts, and inquiry artifacts are visible as repository-facing inquiry state.
- Diagnostics can identify current pressure without recording facts or mutating cluster state.

Unsupported distinction:

```text
self_initiated_inquiry
```

There is no current canonical event kind, source type, concern state, or inquiry artifact field that proves a question was self-initiated by Seed rather than requested by an operator, derived from diagnostics, imported from documentation, or produced as a provider/decision artifact.

### Smallest observable gap

The smallest observable gap is attribution of inquiry origin:

```text
question / inquiry artifact / candidate hypothesis
    lacks a canonical origin distinction for operator_requested vs diagnostic_derived vs external_proposal vs self_initiated
```

This is only a gap statement. It is not an implementation recommendation.

## 3. Concern states: waiting, deferred, resolved

The existing concern model partially supports these states, but mostly as bounded inquiry outputs rather than a general concern state machine.

Supported by current implementation:

| State-like concept | Evidence | Evaluation |
| --- | --- | --- |
| waiting on authority | Authority slices expose blocked observations, `blocking_boundary`, `outcome`, and `remaining_observations` when required authority is unavailable. | Strong support for bounded authority diagnostics. |
| waiting on capability | Capability needs derive missing capability records from diagnostics and projected discrepancies. | Strong support for capability pressure, not a general concern lifecycle. |
| unresolved / remaining | Authority slices expose `remaining_observations` and `remaining_uncertainty`; pressure audit reports unresolved operational pressure. | Strong bounded support. |
| resolved | Some diagnostics can report no pressures or no entries; runtime can return answers/questions/refusals/tool needs. | Weak as a general concern state; absence of pressure is surface-specific. |
| waiting on operator | Runtime can ask a question and record `response.question`; authority slices identify boundaries that would require operator-governed authority outside the diagnostic. | Partial support; no general concern field named waiting_on_operator. |
| deferred | Legacy pending/action-plan surfaces may have lifecycle vocabulary, but canonical runtime scope is narrower and planning artifacts are quarantined as legacy/experimental. | Weak support for current inquiry architecture. |

Conclusion:

```text
The current architecture naturally supports state-like inquiry answers,
not a general concern-state machine.
```

## 4. Runtime self-observation as inquiry pressure

Runtime self-observation could naturally become another source of inquiry pressure, but current support is incomplete.

Supported:

- Observation sources already collect read-only facts from scoped sources.
- Observation ingestion already preserves provenance and derived facts.
- Event ledger and projection cache are explicit runtime/persistence components.
- Pressure audit already converts existing diagnostics into pressure items.
- Prior runtime self-observation investigation found that continuous execution for observation would be an extension of existing observation, while scheduling/governance would be new responsibility.

Unsupported today:

- No first-class observation source emits Seed process memory pressure, CPU pressure, thread count, ledger file size, projection-cache size, projection cost, queue depth, or event-ledger growth as Seed-subject observations.
- Current host resource observations are host observations, not self-process observations.
- No implemented policy turns resource pressure into automatic deferral, scheduling, or execution.

Conclusion:

```text
Runtime self-observation is architecturally compatible as observation pressure,
but not currently implemented as continuous self-regulation.
```

## 5. Existing owner candidates for discovering new worthwhile inquiry

No single current subsystem owns universal discovery of worthwhile inquiry. Existing responsibilities divide naturally:

| Candidate | Existing responsibility | Fit for discovery pressure | Limitation |
| --- | --- | --- | --- |
| Inquiry | Owns questions; inquiry-state work preserves bounded question/current-answer structure. | Best conceptual owner for deciding what is a legitimate question. | Current implementation is artifacts/surfaces, not an autonomous discoverer. |
| Observation | Owns bounded observation provenance. | Best source of new evidence and changed conditions. | Does not decide significance by itself. |
| Repository diagnostics | Own operational surfaces such as pressure, shape, consumer, reachability, and inventory audits. | Best current implementation for surfacing inconsistencies and gaps. | Diagnostic pressure is inspection-oriented, not execution-oriented. |
| Capability reasoning | Owns missing capability and recommendation pressure downstream of projected state. | Best for capability-gap inquiry. | Does not acquire providers or execute capabilities by itself. |
| Runtime | Routes validated decisions and records runtime events. | Owns interaction and response routing. | Not an autonomous inquiry discoverer in current core. |
| Event ledger | Owns append-only historical facts of record. | Preserves changes that inquiry can inspect. | Does not interpret pressure by itself. |

The most implementation-backed answer is distributed:

```text
observation and diagnostics surface pressure;
inquiry owns whether a pressure is a legitimate question;
capability reasoning owns capability-gap interpretation;
runtime routes bounded validated responses;
event ledger preserves evidence.
```

## 6. Architectural role of an external idea source

A bounded external idea source whose purpose is proposing hypotheses, suggesting possibilities, identifying unexplored capabilities, or offering alternative observations fits the current architecture only if its outputs enter as observed inputs.

Natural fit:

```text
external proposal
    -> observed communicative act / candidate hypothesis
    -> evidence with provenance
    -> inquiry artifact or bounded question
    -> authority/evidence/capability filtering
```

Bypass risk:

```text
external proposal
    -> decision / execution / cluster truth
```

The bypass path contradicts existing boundaries because:

- Natural language is evidence of what a speaker requested, asserted, forbade, or prioritized, not direct authority about environmental truth.
- Runtime validates structured decisions before routing.
- Decision validation rejects unsupported decision kinds and requires specific fields for accepted kinds.
- Tool calls are separately validated and routed through `ToolExecutor`; tool needs are recorded as needs and capability resolution, not execution.

Conclusion:

```text
Externally proposed ideas naturally become observed inputs or candidate inquiry artifacts.
They should not bypass existing inquiry responsibilities as decisions or execution.
```

## 7. Can current inquiry architecture reject poor ideas?

Partially yes.

Current filters already available:

| Filter | Existing support | What it rejects or weakens |
| --- | --- | --- |
| Authority | Authority slices, privilege discovery, and README authority boundaries. | Ideas requiring unavailable or unauthorized authority. |
| Evidence | Observation/evidence/fact pipeline and explanation/evidence graph surfaces. | Unsupported environmental truth claims. |
| Capability | Capability-needs and capability-resolution paths. | Ideas requiring absent or unverified capabilities. |
| Uncertainty | Authority slices and inquiry-state reasoning preserve remaining uncertainty. | Overconfident claims or premature closure. |
| Boundary | README non-goals and diagnostic inventory fields such as mutates-cluster / record scope. | Ideas that imply planning, execution, mutation, or authority bypass. |
| Validation | Decision validator rejects malformed or unsupported runtime decisions. | Invalid direct runtime actions. |

Insufficient today:

- There is no universal hypothesis-quality classifier.
- There is no canonical externally-proposed-hypothesis lifecycle.
- Rejection is currently surface-specific: validation rejects decisions, authority slices block observations, diagnostics expose mismatches, and evidence surfaces weaken unsupported claims.

Conclusion:

```text
The architecture can reject poor ideas when they are forced through authority,
evidence, capability, uncertainty, boundary, and validation surfaces.
It cannot reject a poor idea as a first-class hypothesis lifecycle object because
that object is not currently implemented.
```

## 8. Continuous living: new architecture or extension?

Continuous living for inquiry discovery appears to extend existing architecture:

```text
observation
    receives new or changed inputs

event ledger
    preserves observed changes and provenance

projection / diagnostics
    reveal contradictions, shape gaps, consumer gaps, capability needs, and pressure

inquiry
    frames bounded questions and preserves uncertainty / authority boundaries

runtime self-observation
    could add Seed's own process and persistence state as another observed domain
```

It would become fundamentally new architecture only if the responsibility were changed from:

```text
discovering worthwhile questions
```

to:

```text
scheduling, executing, governing resources, or autonomously doing work
```

Those responsibilities are outside the current supported boundary.

## Remaining unanswered questions

1. What canonical attribution should distinguish operator-requested, diagnostic-derived, externally proposed, imported, and self-initiated inquiry?
2. Which existing inquiry artifact is the authoritative durable representation of a candidate hypothesis?
3. How should runtime self-observation facts name Seed process, ledger, and projection-cache subjects without confusing host facts with Seed facts?
4. Which current diagnostic pressures are inquiry-worthy versus merely visible inspection findings?
5. How should current concern-state vocabulary remain bounded without becoming a planner or lifecycle engine?
6. Can repository diagnostics expose enough pressure provenance to explain why a question is worth asking now?

## Smallest implementation-backed next questions

These are investigation questions only:

1. Does any existing inquiry artifact already preserve `origin` or `source` strongly enough to distinguish operator request, diagnostic pressure, and external proposal?
2. Do pressure-audit items have enough provenance to be rendered as bounded questions without adding scheduling semantics?
3. Which current self-observation metrics can be represented as ordinary observations without inventing new authority or resource-governance concepts?
4. Which existing rejection surfaces would evaluate an externally proposed hypothesis: evidence graph, authority slice, capability need, diagnostic shape, or decision validation?
5. Are `remaining_observations` and `remaining_uncertainty` sufficient as bounded state-like concern output across more than ownership authority slices?

## Strongest supporting evidence

- README defines Seed as continuously maintaining evidence-backed answers to bounded questions and explicitly assigns inquiry ownership of questions.
- README states Seed begins with observation, provenance, justified claims, relationships, and projections; it also limits natural-language authority.
- `ObservationSource` and `ObservationIngestor` implement the observation-to-evidence-to-fact path.
- `EventLedger` is append-only event history feeding projection.
- `PressureAudit` already ranks operational pressure from current diagnostics without mutation.
- Capability needs are derived from diagnostics and `diagnostic_run:*` facts.
- Authority slices expose blocked/remaining observations and uncertainty without event-ledger writes or cluster mutation.
- Runtime decision validation and routing prevent arbitrary proposals from becoming execution.

## Strongest contradictory evidence

- There is no implemented continuous inquiry loop.
- There is no canonical self-initiated inquiry event, concern state machine, or hypothesis lifecycle.
- Current runtime is input-triggered and decision-routed, not a discoverer of work.
- Runtime self-observation is not yet a first-class observation source for Seed process or persistence pressure.
- Some lifecycle/planning-like artifacts exist historically, but current architecture quarantines them as legacy/experimental rather than canonical core.

## Recommended future investigation order

1. Inquiry-origin attribution across existing inquiry artifacts and runtime events.
2. Pressure-audit-to-question transformation boundaries.
3. Runtime self-observation subject naming and authority boundary.
4. External proposal intake as observation/inquiry artifact rather than decision.
5. Cross-surface concern-state vocabulary limited to current-answer fields.
6. Rejection/filtering matrix for externally proposed hypotheses.

## Report

### Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' && git status --short`
- `cat AGENTS.md && rg -n "inquiry|concern|authority|observation|capability|event ledger|event-ledger|runtime|diagnostic|knowledge|blocked|deferred|resolved|waiting" . -g '!**/.git/**'`
- `find docs -maxdepth 2 -type f | sort | sed -n '1,220p'`
- `find docs -maxdepth 1 -type f | sort | sed -n '220,520p'`
- `sed -n '1,220p' README.md && sed -n '1,220p' docs/inquiry_state_reasoning_reconciliation.md && sed -n '1,220p' docs/runtime_self_observation_investigation.md && sed -n '1,220p' docs/pressure_integration_and_orphaned_pressure_investigation.md && sed -n '1,220p' docs/current_strategy_bounded_inquiry_reconciliation.md`
- `sed -n '1,260p' seed_runtime/observations.py; sed -n '1,260p' seed_runtime/observation_sources.py; sed -n '1,220p' seed_runtime/events.py; sed -n '1,220p' seed_runtime/container_ownership_authority.py; sed -n '1,220p' seed_runtime/service_ownership_authority.py; sed -n '1,180p' seed_runtime/runtime.py`
- `sed -n '180,380p' seed_runtime/runtime.py; sed -n '1,260p' seed_runtime/decisions.py; sed -n '1,180p' seed_runtime/capability_needs.py; sed -n '1,220p' seed_runtime/pressure_audit.py`
- `python scripts/seed_local.py --pressure-audit | sed -n '1,120p'; python scripts/seed_local.py --diagnostic-inventory | sed -n '1,80p'; python scripts/seed_local.py --knowledge-reachability-audit --candidate inquiry --candidate observation --candidate capability --candidate runtime --candidate "event ledger" | sed -n '1,160p'`

### Files inspected

- `AGENTS.md`
- `README.md`
- `docs/inquiry_state_reasoning_reconciliation.md`
- `docs/runtime_self_observation_investigation.md`
- `docs/pressure_integration_and_orphaned_pressure_investigation.md`
- `docs/current_strategy_bounded_inquiry_reconciliation.md`
- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/events.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/runtime.py`
- `seed_runtime/decisions.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/pressure_audit.py`

### Files changed

- `docs/continuous_living_inquiry_frontier_reconciliation.md`

### LOC changed

- Added 385 lines.

### Tests run

- `python -m pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`

These diagnostic visibility tests were run as a precaution; the change adds an exploratory documentation report and no diagnostic, audit, probe, CLI flag, or recordable output surface.
