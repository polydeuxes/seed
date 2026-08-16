---
doc_type: reconciliation
status: investigation-only
scope: recent inquiry branch architectural invariants
---

# Earned Architectural Invariants Reconciliation

## Boundary

This reconciliation asks what the recent inquiry branch has actually earned
through repeated implementation. It does not propose a new framework, engine,
runtime, planner, generic inquiry composition layer, presentation framework, or
implementation roadmap.

Repository authority wins. The claims below are preserved only where executable
implementation, tests, and prior implementation-backed reconciliations recur
across independent slices.

## Central answer

The branch has earned a narrow inquiry discipline, not a repository-wide
reasoning architecture.

The strongest supported statement is:

```text
Seed has repeatedly implemented bounded inquiries whose local subsystems compute
reasoning before presentation, expose stable inquiry state, compose existing
subsystem outputs through deterministic joins, and preserve diagnostic findings
as visibility rather than cluster truth.
```

The strongest unsupported widening is:

```text
Seed now has a generic inquiry framework, repository-wide reasoning engine,
planner, or first-class capability maturity model.
```

Those wider ideas remain hypotheses until more implementation owns them.

## Files inspected

Required reconciliations:

- `docs/inquiry_shapes_emerged_reconciliation.md`
- `docs/current_strategy_bounded_inquiry_reconciliation.md`
- `docs/bounded_inquiry_identity_state_reconciliation.md`
- `docs/bounded_inquiry_explanation_reconciliation.md`
- `docs/reasoning_before_presentation_reconciliation.md`
- `docs/ordinary_subsystem_existence_reconciliation.md`
- `docs/filesystem_ownership_constrained_authority_reconciliation.md`
- `docs/privilege_discovery_storage_capability_guidance_reconciliation.md`
- `docs/capability_maturity_observability_reconciliation.md`

Implementation and tests:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_privilege_discovery.py`
- `tests/test_ownership_discrepancies.py`

## 1. Observations that independently recurred

### Bounded questions determine the implemented strategy label

This recurred in container ownership and service ownership.

- Container ownership fixes `DESIRED_OBSERVATION = "container ownership"`, fixes
  `CURRENT_STRATEGY = "container_runtime_observation"`, and computes reachability
  within that bounded slice.
- Service ownership fixes `DESIRED_OBSERVATION = "service ownership"`, fixes
  `CURRENT_STRATEGY = "composite_local_service_attribution_observation"`, and
  computes reachability within that bounded slice.
- Tests assert both strategy labels directly and through CLI/JSON surfaces.

This supports only the narrow invariant that current bounded inquiries expose the
strategy implied by their implemented scope. It does not support strategy
selection, ranking, fallback, or a planner.

### Local subsystems own local deterministic reasoning

This recurred across authority slices and ownership/capability diagnostics.

- `container_ownership_authority` owns the Docker/root authority boundary for
  container-runtime observations.
- `service_ownership_authority` owns the service attribution composition over
  listener, process, systemd, and container-runtime evidence.
- `ownership_discrepancies` owns storage/service candidate extraction, conflict
  classification, and capability-need emission.
- `capability_needs` owns aggregation of current projection and recorded
  diagnostic-run needs.
- `privilege_discovery` owns registered authority guidance and unknown fallback.

The recurring pattern is not a central reasoning engine. It is responsibility
kept near the subsystem that has the evidence and vocabulary.

### Inquiries compose reasoning by joining existing subsystem outputs

This recurred in service ownership, capability needs, privilege discovery, and
storage ownership guidance.

- Service ownership joins `ownership_discrepancies` capability records to blocked
  observation details, keyed by capability name.
- Capability needs aggregates diagnostic rows from the current projection and
  facts scoped to `diagnostic_run:*`.
- Privilege discovery joins capability needs to its guidance registry and
  implementation-evidence statuses.
- Storage guidance reconciliation relies on the same existing seam: ownership
  discrepancies emit needs, capability needs aggregates them, and privilege
  discovery explains authority where registered.

The implementation-backed composition is deterministic and local. It is not a
generic inquiry composition framework.

### Presentation projects computed reasoning rather than creating it

This recurred in container ownership, service ownership, privilege discovery,
capability needs, and ownership discrepancies.

- Evaluators build dataclass results or rows first.
- JSON functions serialize those computed results.
- Human formatters render those same fields.
- CLI tests assert output shape/order, but the reasoning values come from the
  evaluator/diagnostic rows.

The presentation invariant is bounded: existing surfaces project computed
reasoning. The repository does not show a general presentation framework.

### Inquiry identity remains stable while authority changes inquiry state

This recurred in the authority slices.

- Container ownership keeps the same desired observation and strategy while a
  profile with no root/Docker authority yields `blocked`; making Docker socket
  read available removes the blocking boundary and changes outcome.
- Service ownership keeps the same desired observation and strategy while the
  constrained profile yields `partially_reachable`; making Docker socket read
  available removes blocked observations and changes outcome to `reachable`.

The invariant is therefore limited to implemented authority slices: identity
fields remain stable while authority-dependent state fields change.

### Diagnostic findings remain diagnostic unless recorded into diagnostic-run scope

This recurred in ownership discrepancies, capability needs, and authority slices.

- Authority slices expose read-only boundaries and do not record, write the event
  ledger, mutate cluster state, create permissions, acquire providers, or execute
  observations.
- Ownership discrepancies without `--record` does not change event count.
- Ownership discrepancy recording appends facts under `diagnostic_run:*`, and
  tests prove diagnostic needs do not become entity ownership or capability
  facts.
- Capability needs reads both current diagnostic rows and recorded diagnostic-run
  facts without promoting them to cluster truth.

This is an earned diagnostic boundary invariant for the implemented diagnostic
surfaces.

### Responsibilities have proved more durable than individual modules

This recurred as implementation moved through multiple narrow slices.

The durable units were responsibilities:

- authority guidance,
- capability pressure aggregation,
- ownership discrepancy classification,
- bounded authority evaluation,
- read-only diagnostic presentation,
- diagnostic-run recording boundary.

Individual modules changed or were extended, but the responsibility seams were
preserved. The best evidence is that service ownership could reuse ownership
summaries, capability needs, privilege explanations, observation inventory, and
observation domains without centralizing them.

## 2. Candidate invariants evaluated individually

| Candidate invariant | Status | Confidence | Implementation-backed support | Strongest contradictory evidence |
| --- | --- | --- | --- | --- |
| Questions discover architecture. | Supported, narrow. | Medium-high | Container ownership and service ownership each produced different strategy/reachability shapes from bounded desired observations rather than from a predeclared architecture. Prior reconciliations record the same bounded-inquiry finding. | Only two authority inquiries demonstrate this strongly; many repo areas may still be ordinary diagnostics rather than question-shaped inquiries. The code uses fixed constants, not discovered architecture at runtime. |
| Subsystems own local reasoning. | Supported. | High | Ownership discrepancies classify conflicts and emit capability needs; capability needs aggregates; privilege discovery explains authority; authority slices evaluate reachability. | Some slices import across subsystem boundaries, especially service ownership importing ownership discrepancies, capability needs, privilege discovery, inventory, and domains. That coupling limits any claim of strict subsystem independence. |
| Inquiries compose reasoning. | Supported, narrow. | Medium-high | Service ownership composes local listener/systemd/container authority with discrepancy summaries; capability and privilege surfaces compose diagnostic needs with guidance. | Composition is hand-coded per slice and keyed by existing names; no generic composition contract is implemented. |
| Presentation projects reasoning. | Supported. | High | Formatters and JSON serializers render already-computed dataclass/row fields across the reviewed surfaces; tests assert rendered shape rather than presentation-only inference. | Human-output section order varies between container and service ownership, so presentation is not uniform. Some vocabulary exists only in docs/output unless backed by implementation. |
| Inquiry identity remains stable. | Supported, narrow. | Medium | Desired observation and current strategy remain fixed in container/service authority evaluators while outcome, blocking boundary, and remaining observations change with authority. | Evidence is mostly the two authority slices; other diagnostics may not expose inquiry identity fields. |
| Inquiry state changes with authority. | Supported. | High for authority slices. | Profile changes alter container outcome/blocking boundary and service reachable/blocked observations/outcome while keeping identity stable. | Non-authority diagnostics change with facts, not authority; this should not be generalized beyond authority-aware inquiries. |
| Responsibilities are more durable than modules. | Supported as an observational finding. | Medium | Recent slices reused existing responsibility seams instead of creating engines: ownership discrepancies, capability needs, privilege discovery, inventory/domains, and formatter/JSON boundaries. | This is partly historical interpretation from the branch rather than a single runtime field; module names still remain the concrete import and test targets. |

## 3. Remaining hypotheses

The following ideas remain promising hypotheses, not established invariants:

### Repository-wide reasoning architecture

The repository shows local deterministic reasoning in several subsystems. It does
not show one repository-wide reasoning architecture. There is no shared reasoning
engine, planner, strategy registry, or repository-wide reasoning contract in the
reviewed implementation.

### Generic inquiry composition

The repository shows repeated hand-coded composition by existing seams and stable
names. It does not show a generic inquiry composition abstraction. The service
ownership slice composes reasoning, but does so directly and narrowly.

### Capability maturity as first-class knowledge

The repository exposes signals from which humans infer maturity: registered
privilege guidance, not-registered implementation evidence, unknown fallback,
implemented observation sources, and capability needs. It does not record a
normalized maturity stage such as implemented, partial, placeholder, or unknown
as first-class capability knowledge.

### Repository-wide architectural observability

Diagnostic inventory and shape audit make operational surfaces visible, and the
reviewed tests preserve that visibility. That is not the same as repository-wide
architectural observability. Architectural conclusions remain reconciliation
findings synthesized from implementation evidence.

### Universal inquiry discipline

The branch demonstrates a coherent discipline for the reviewed inquiry-style
work, especially authority-aware diagnostics. It does not prove every Seed
subsystem participates in the same discipline.

## 4. One coherent inquiry discipline, or several successful implementations?

The repository has demonstrated a coherent bounded-inquiry discipline across the
reviewed branch, but not a single generalized inquiry system.

The discipline is coherent because the following recur independently:

1. Start with a bounded desired observation or diagnostic question.
2. Let the responsible subsystem compute local evidence, conflict, authority, or
   capability state.
3. Compose existing subsystem outputs through deterministic joins rather than
   duplicating reasoning.
4. Keep identity stable while facts or authority change state.
5. Render computed state through JSON/human presentation.
6. Preserve diagnostic output as visibility, not cluster truth.

It is still only several successful implementations in the stronger architectural
sense because there is no shared runtime, framework, planner, or generic inquiry
contract. The earned conclusion is therefore:

```text
The branch discovered a coherent implementation discipline.
It did not implement a universal inquiry architecture.
```

## 5. Implementation decisions that prevented unnecessary architectural growth

### Bounded slices

Each recent implementation stayed small: container ownership evaluated only
container-runtime authority, service ownership evaluated one composite local
service attribution strategy, privilege discovery registered guidance only where
implementation evidence supported it, and capability maturity remained an
operator conclusion.

### Existing subsystem seams

The branch reused existing seams instead of creating new concepts:

- ownership discrepancy rows for conflict/capability pressure,
- capability needs for aggregation,
- privilege discovery for authority guidance,
- observation inventory/domains for implemented vocabulary,
- diagnostic inventory and shape audit for operational visibility.

### Deterministic joins

Service ownership's blocked observation explanations are joined by capability
name to existing ownership discrepancy summaries and privilege explanations.
Capability needs groups diagnostic records deterministically by capability,
subject, diagnostic, needed evidence, and diagnostic run. No scoring engine or
planner was introduced.

### Subsystem responsibility preservation

Ownership discrepancy code continued to own ambiguity and capability pressure.
Privilege discovery continued to own guidance and unknown fallback. Authority
slices used those outputs but did not absorb those responsibilities.

### Avoiding duplicated reasoning

Service ownership reused existing discrepancy summaries and privilege explanation
fields rather than reimplementing ownership conflict classification or privilege
guidance. Capability needs continued to aggregate diagnostic rows rather than
requiring each authority slice to build its own pressure model.

### Diagnostic boundary preservation

Read-only authority slices and diagnostic-run scoped recording avoided turning
findings into cluster truth. This prevented an architectural expansion from
visibility into mutation semantics.

## 6. Strongest contradictory evidence by proposed invariant

### Questions discover architecture

Contradiction: the implemented strategies are constants. The repository does not
perform runtime architectural discovery. The supported claim is that bounded
questions revealed stable architectural seams through implementation work, not
that the program discovers architecture dynamically.

### Subsystems own local reasoning

Contradiction: service ownership imports and coordinates several subsystem
outputs. Reasoning is locally owned by source subsystems, but authority answers
can still be cross-subsystem compositions.

### Inquiries compose reasoning

Contradiction: composition is bespoke. There is no common inquiry composition
interface, no shared composer, and no evidence that all inquiries can compose in
the same way.

### Presentation projects reasoning

Contradiction: presentation vocabulary can outrun repository knowledge. The repo
instructions explicitly warn that labels such as current work position, source
navigation, active edge, storage topology, state build, and projection cache are
not automatically knowledge. Therefore presentation projection is only invariant
when fields are computed by implementation.

### Inquiry identity remains stable

Contradiction: stable identity fields are not universal across diagnostics. They
are strongly visible in container/service authority slices but not necessarily in
ordinary diagnostics such as ownership discrepancies.

### Inquiry state changes with authority

Contradiction: many diagnostics are fact-sensitive rather than authority-profile
sensitive. Authority-dependent state should remain scoped to authority-aware
inquiries.

### Responsibilities are more durable than modules

Contradiction: this is an architectural interpretation over branch history and
imports, not a directly emitted runtime fact. It should remain phrased as an
observed durability pattern, not a formal repository law.

## Earned invariants

1. **Bounded inquiries expose strategy from their implemented scope.**
   Confidence: medium-high. Scope: current container/service authority slices.
2. **Subsystems compute local deterministic reasoning at their responsibility
   seams.** Confidence: high. Scope: reviewed diagnostics and authority/capability
   surfaces.
3. **Inquiry-style answers compose existing subsystem outputs through
   deterministic joins.** Confidence: medium-high. Scope: reviewed branch.
4. **Presentation surfaces serialize/render computed reasoning rather than own
   the reasoning.** Confidence: high. Scope: reviewed surfaces with evaluator/row
   outputs.
5. **Authority-aware inquiry identity remains stable while authority-dependent
   state changes.** Confidence: medium-high. Scope: container/service authority
   slices.
6. **Diagnostic findings remain visibility unless intentionally recorded as
   diagnostic-run scoped facts.** Confidence: high. Scope: reviewed diagnostic
   surfaces.
7. **Responsibility seams have been more durable than any single architectural
   module name.** Confidence: medium. Scope: branch-level observation.

## Report

### Files changed

- `docs/earned_architectural_invariants_reconciliation.md`

### LOC changed

- Added this reconciliation document.

### Tests run

- `pytest -q tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_privilege_discovery.py tests/test_ownership_discrepancies.py`

### Recommended next bounded investigation

Investigate whether one additional non-authority diagnostic that already has
JSON and human output follows the same discipline:

```text
Does its presentation render computed subsystem reasoning,
or does it introduce presentation-only knowledge?
```

This is an observational investigation only. It should not add a framework,
engine, runtime, planner, or roadmap.
