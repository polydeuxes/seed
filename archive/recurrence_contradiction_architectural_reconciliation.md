---
title: Recurrence and Contradiction Architectural Reconciliation
status: reconciliation
authority: architecture-focused reconciliation only; no implementation change, behavior proposal, schema proposal, runtime design, or ontology promotion
created: 2026-06-27
scope: repository-evidence reconciliation of recurrence and contradiction as architectural discovery mechanisms
---

# Recurrence and Contradiction Architectural Reconciliation

## Purpose

This document reconciles whether recurrence and contradiction already function as
complementary architectural discovery mechanisms in Seed.

This is documentation-only. It does not implement code, normalize relationships,
modify repository architecture, add commands, change behavior, or propose new
runtime surfaces.

## Method and authority boundary

Repository authority wins. The review used existing architecture documents,
recent investigations, implementation diagnostics, and tests as evidence. The
`seed` app was used through existing read-only surfaces; those commands are
listed at the end.

The strongest existing repository authority is not that recurrence and
contradiction are named as first-class ontology terms. The stronger authority is
that Seed is already organized around preserving observations, accumulating
evidence, normalizing supportable claims, projecting selected knowledge, and
preserving authority and boundaries.

The README states the operating thesis in question form:

```text
Inquiry owns the questions.
Subsystems own the answers.
Responsibilities define the boundaries.
Authority constrains the answers.
Questions discover the architecture.
```

`docs/seed.md` gives the same architecture as bounded paths rather than rigid
pipelines: Observation -> Evidence -> Claim -> Fact / Relationship ->
Projection, Event -> Change -> State -> Projection, and Operator Intent ->
Question -> Goal -> Assessment -> Consequence -> Recommendation -> Decision.
`docs/ontology.md` then preserves the boundaries that prevent those recurring
paths from being merged: Claim != Fact, Relationship != Identity, Event !=
State, Projection != Authority, Recommendation != Decision, Capability !=
Execution, and Contradiction Discovery != Contradiction Creation.

Therefore this reconciliation treats recurrence and contradiction as
implementation-visible discovery pressures over the existing claim/evidence/
projection/boundary architecture, not as new primitives.

## Architectural summary

Repository evidence supports this formulation:

```text
Recurring structures reveal candidate architecture.
Contradictions expose the comparison boundary that prevents over-merge.
Repository evidence reconciles both into bounded, supportable architecture.
```

The shorter statement is supported with a caveat:

```text
Recurrence increases coherence.
Contradiction defines boundaries.
Together they recover architecture.
```

The caveat is that contradiction does not itself define a boundary by authority.
Contradiction is a pressure or discovery event. The boundary is recovered only
after implementation evidence, documentation authority, tests, or existing
projection semantics show how the concepts are actually distinct.

## Recurrence findings

### 1. Question / answer / responsibility recurred into architectural shape

What recurred:

- bounded questions;
- answer responsibility;
- subsystem responsibility;
- authority and boundary language.

Structure made visible:

- Seed is not organized around free-form response generation. It is organized
  around bounded questions whose answer ownership belongs to specific
  subsystems.

Implementation and repository evidence:

- `README.md` states that Seed maintains evidence-backed answers to bounded
  questions by asking responsible subsystems while preserving authority,
  uncertainty, and boundaries.
- The question-family surface is an implementation-backed dispatch surface:
  `--question-family` dispatches an exact Question Family identifier through an
  existing inquiry surface.
- `tests/test_implementation_trait_characterization.py` proves that
  `bounded_status`, `dispatch_surface`, and `required_surface_args` recur as the
  dispatchability concern, while `answer_responsibility` is inventory metadata,
  not a generic implementation trait.

Conclusion:

- Recurrence exposed the architectural division between inquiry, answer
  ownership, dispatchability, and authority metadata.

### 2. Projection recurred into a bounded read-side architecture

What recurred:

- projected state;
- read-only state views;
- selection;
- derivation;
- explanation;
- cache boundaries.

Structure made visible:

- projection is a recurring read-side operation over preserved events/facts, not
  source authority and not execution.

Implementation and repository evidence:

- `README.md` identifies observations, evidence, claim normalization,
  relationship/entity-type projection, contradiction/confidence/staleness/graph
  issue characterization, read-only state views, and explanation surfaces as
  Seed-owned knowledge-path responsibilities.
- `docs/seed.md` repeatedly places Projection at the end of the knowledge and
  temporal paths while stating that projections select and communicate preserved
  knowledge; they do not become authority.
- `seed --projection-shape --json` exposes implementation-backed stages such as
  `event_replay`, `alias_projection`, `measurement_retention`, `inference`,
  `fact_support_projection`, `legacy_relationship_projection`, and
  `catalog_relationship_projection`, each with consumes/produces/influences,
  does-not-influence fields, and authority boundaries.
- `tests/test_projection_shape.py` proves that projection shape is visible,
  read-only, registered in diagnostic inventory, checked by diagnostic shape
  audit, and explicitly reports `read_only=true`, `writes_event_ledger=false`,
  and `mutates_cluster=false`.

Conclusion:

- Recurrence exposed projection as an architectural family, while the stage
  fields prevented it from becoming one undifferentiated cache or truth layer.

### 3. Diagnostic visibility recurred into an operational contract

What recurred:

- diagnostic inventory;
- shape audit;
- JSON support;
- record support;
- record scope;
- event-ledger writes;
- cluster mutation boundaries.

Structure made visible:

- operational visibility is part of the architecture. New diagnostic or audit
  surfaces are expected to be discoverable and shape-audited.

Implementation and repository evidence:

- `AGENTS.md` requires diagnostic inventory updates, diagnostic shape-audit
  specs, tests for `seed --diagnostic-inventory`, tests for
  `seed --diagnostic-shape-audit`, proof of `record_scope=diagnostic_run` for
  recording diagnostics, and proof of `mutates_cluster=false` for read-only
  diagnostics.
- `seed --diagnostic-inventory --json` exposes recurring surface fields such as
  `supports_json`, `supports_record`, `record_scope`, `writes_event_ledger`,
  `mutates_cluster`, `uses_projected_state`, and `uses_repo_files`.
- `tests/test_diagnostic_inventory.py` proves that recording diagnostics declare
  `diagnostic_run` scope, writes to the event ledger are explicit, and current
  diagnostics do not mutate the cluster.

Conclusion:

- Recurrence made diagnostic governance visible as architecture rather than
  incidental CLI metadata.

### 4. Ownership / authority / support recurred as evidence-sensitive concerns

What recurred:

- ownership;
- authority;
- support;
- missing owner;
- candidate owner;
- diagnostic-only findings.

Structure made visible:

- ownership is a supportable claim family constrained by authority and evidence;
  diagnostic pressure must not silently become cluster truth.

Implementation and repository evidence:

- `seed --investigation-path ownership --json` routes ownership through
  `ownership_discrepancies`, `capability_needs`, `privilege_discovery`,
  `correlation_audit`, and `impact_audit`.
- `seed_runtime/ownership_discrepancies.py` is explicitly a read-only
  operational ownership discrepancy diagnostic.
- `tests/test_ownership_discrepancies.py` proves diagnostic recording uses
  diagnostic-run-scoped subjects and does not create ownership facts.
- `seed_runtime/container_ownership_authority.py` is a narrow read-only authority
  slice for container ownership observation, separating authority to observe
  from ownership itself.

Conclusion:

- Recurrence exposed ownership and authority as stable pressures, but only
  implementation evidence decided which claims are supported, diagnostic-only,
  or missing authority.

## Contradiction findings

### 1. Runtime trace vs execution status

Observed contradiction:

- Runtime trace-like output and execution status-like output can appear similar:
  both describe runtime activity.

Implementation evidence:

- `seed_runtime/execution_status.py` defines `ExecutionStatusConsumer` as a
  protocol that consumes transient execution status without owning execution
  state.
- `seed_runtime/events.py`, `seed_runtime/observations.py`, `seed_runtime/state.py`,
  and `seed_runtime/fact_index.py` accept optional execution status consumers,
  showing status as a consumption channel around existing operations rather than
  a ledger-owning trace model.

Reconciled conclusion:

- The apparent contradiction resolves as a true implementation boundary:
  transient status consumption is not execution-state ownership.

Resulting architectural boundary:

- Runtime/operator feedback != durable execution trace/state.

### 2. Projection snapshot vs audit snapshot

Observed contradiction:

- Both projection snapshots and audit snapshots can look like saved views of
  state.

Implementation evidence:

- `docs/seed.md` and `docs/ontology.md` separate Projection from Authority and
  Event from State.
- `seed --projection-shape --json` shows projection as read-only, event-ledger
  consuming, and non-mutating.
- `seed --diagnostic-inventory --json` shows audit snapshot-related surfaces as
  diagnostics with their own read-only and event-ledger metadata.
- `tests/test_architecture_invariants.py` preserves the separation between
  event ledgers and projection snapshot methods.

Reconciled conclusion:

- The similarity resolves as a true architectural boundary. Projection snapshots
  are cached/projected read models derived from events. Audit snapshots are
  diagnostic records or comparisons of diagnostic output.

Resulting architectural boundary:

- Projection cache/read model != diagnostic audit record.

### 3. `supports_json` vs supporting evidence

Observed contradiction:

- The word `supports` appears both in implementation capability metadata
  (`supports_json`) and in knowledge/evidence support.

Implementation evidence:

- `tests/test_implementation_trait_characterization.py` classifies
  `supports_json`, `json_support`, and `json_capable` as
  `implementation_capability`, while `evidence`, `uses_projected_state`,
  `uses_repo_files`, and related fields are `evidence_source`.
- `README.md` and `docs/seed.md` use support/evidence language for claims,
  provenance, and projected knowledge.

Reconciled conclusion:

- This resolves as an incorrect vocabulary assumption. Identical surface words
  do not imply the same architectural concern.

Resulting architectural boundary:

- Implementation capability metadata != evidential support for a claim.

### 4. Projection consumes vs `ExecutionStatusConsumer.consume()`

Observed contradiction:

- Both use consumption language.

Implementation evidence:

- `seed --projection-shape --json` exposes stage `consumes` fields for inputs to
  deterministic projection stages.
- `ExecutionStatusConsumer.consume()` consumes transient status events without
  owning execution state.
- `tests/test_implementation_trait_characterization.py` classifies
  `consumer_kind` as implementation capability and separately classifies
  `uses_projected_state` as evidence source.

Reconciled conclusion:

- This resolves as an incorrect assumption caused by shared vocabulary. One is
  projection dependency shape; the other is runtime feedback interface shape.

Resulting architectural boundary:

- Projection dependency consumption != status event consumption.

### 5. Authority vs ownership

Observed contradiction:

- Authority and ownership recur together, especially around containers,
  services, listeners, and diagnostics.

Implementation evidence:

- `seed_runtime/container_ownership_authority.py` evaluates authority to observe
  container ownership; it does not assert ownership.
- `seed_runtime/listener_endpoint_authority.py` explicitly says the authority
  slice does not acquire providers, grant permissions, record facts, or infer
  ownership.
- `tests/test_listener_endpoint_authority.py` proves required/available
  authority reporting and diagnostic registration.
- `tests/test_ownership_discrepancies.py` proves ownership diagnostics can record
  diagnostic facts without creating service ownership facts.

Reconciled conclusion:

- This resolves as a true architectural boundary. Authority constrains what may
  be observed or claimed; ownership is a claim requiring support.

Resulting architectural boundary:

- Authority to observe or act != ownership claim.

### 6. Projection cache vs read-model cache

Observed contradiction:

- Projection cache and read-model cache can look like duplicate names for the
  same thing.

Implementation evidence:

- `docs/archive/original_book_of_seed/01-architecture.md` describes `EventLedger` as append-only facts about what
  happened and `ProjectionStore` as cached projected state derived from events.
- `docs/archive/original_book_of_seed/02-domain-model.md` says `ProjectionStore` is a deterministic cache of
  current projected state, cache not source of truth.
- `tests/test_architecture_invariants.py` checks that projection store protocols
  do not own event methods and event ledgers do not own projection snapshot
  methods.

Reconciled conclusion:

- The contradiction resolves as a missing visibility / naming clarification more
  than a new architecture. Read-model cache and projection cache both point at
  the projection boundary when backed by `ProjectionStore`, but they must not be
  confused with the event ledger.

Resulting architectural boundary:

- Rebuildable projected read model != append-only source of truth.

## How apparent contradictions most commonly resolve

Across the representative cases, contradictions most commonly resolved as:

1. **true architectural boundaries** — Event != State, Projection != Authority,
   Relationship != Identity, Capability != Execution, Authority != Ownership;
2. **incorrect assumptions caused by vocabulary collision** — `supports_json`
   vs supporting evidence; projection consumes vs status consumer consumes;
3. **missing visibility** — the architecture already had the boundary, but the
   relevant inventory, projection shape, diagnostic registration, or tests had
   to be consulted;
4. **true implementation differences** — transient status consumers differ from
   durable traces; audit snapshots differ from projection snapshots;
5. **missing relationships** — less often as the final answer; missing
   relationships are usually the thing an audit or contradiction exposes, not
   the final architectural principle.

This ordering is supported by the existing ontology boundary list,
contradiction-discovery reconciliation, diagnostic inventory contract,
projection-shape stages, implementation-trait characterization, and ownership
/ authority tests.

## Would recurrence alone over-merge concepts?

Yes. Repository evidence shows recurrence alone would have incorrectly merged:

- Projection, state views, caches, and authority. The recurring word
  `projection` only remains safe because `docs/ontology.md`, `docs/seed.md`,
  `seed --projection-shape --json`, and projection-shape tests preserve
  consumes/produces/does-not-influence/authority-boundary distinctions.
- Ownership and authority. They recur together, but authority slices explicitly
  do not infer ownership and ownership diagnostics record diagnostic-only facts.
- Implementation capability support and evidential support. The repeated word
  `support` is separated by implementation trait characterization.
- Capability, command, execution, and action. `docs/seed.md` and
  `docs/ontology.md` preserve these as distinct execution-plane concepts even
  though operational language often groups them.

## Would contradiction alone obscure broader recurrence?

Yes. Repository evidence also shows contradiction alone would fragment the
architecture if recurrence were ignored:

- Projection stages differ, but recurrence shows them as one read-side family
  over events, facts, relationships, inference, validation, selection, and
  explanation.
- Diagnostic surfaces differ, but recurring inventory fields and shape-audit
  expectations show one operational visibility contract.
- Ownership, capability needs, privilege discovery, correlation audit, and
  impact audit differ, but the ownership investigation path shows a recurring
  ownership/evidence/authority path across surfaces.
- Question Families, dispatchability fields, surface arguments, and answer
  responsibility differ, but recurrence shows bounded inquiry as an architectural
  entry pattern rather than unrelated CLI flags.

## Iterative progression recovered from repository evidence

Repository evidence supports this iterative pattern with one adjustment:

```text
observe recurrence
↓
notice a possible over-merge or contradiction
↓
recover implementation/documentation evidence
↓
classify the evidence source and authority
↓
reconcile the comparison boundary
↓
preserve the boundary in documentation, tests, inventory, or diagnostics
↓
allow the bounded recurring structure to remain coherent
```

The adjustment is important: contradiction does not automatically define the
boundary. Evidence and authority classify it.

## Recent investigation review

| Investigation area | Primary mechanism | Evidence-backed conclusion |
| --- | --- | --- |
| Question Families | Both | Recurrence exposed bounded ask/dispatch shape; contradiction separated answer responsibility metadata from generic traits. |
| Answer responsibility | Both | Recurs as architecture, but implementation-trait tests keep it inventory metadata rather than implementation capability. |
| Authority | Both | Recurs across operator, observation, ownership, and capability concerns; contradictions separate authority from ownership and execution. |
| Implementation traits | Both | Recurrence exposed reusable fields; contradictions classified fields into evidence source, operational boundary, dispatchability, implementation capability, metadata, and container fields. |
| Projected-state consumers | Both | Recurrence exposed consumers over projected state; contradictions preserve read-only/non-mutating/recording boundaries. |
| Execution characterization | Both | Recurring execution terms are separated by Decision != Command != Execution != Action and by status consumers not owning execution state. |
| Execution vocabulary | Both | Shared words such as consume/support are insufficient; tests and protocols define meaning. |
| Implementation relationship grammar | Both | Relationship recurrence is architectural, but relationship != identity and definition observation does not prove behavior, reachability, authority, or ownership. |
| Runtime responsibility | Both | Runtime paths recur, but Seed does not become workflow engine, executor, secret handler, or autonomous action platform. |
| Projection | Both | Projection recurs as a family, while stages and authority boundaries prevent over-merge. |
| Selection | Both | Selection recurs in projection and decision context, but projection selection is not authority, decision, or truth. |
| Reasoning | Both | Deterministic inference/projection recurs, but `docs/seed.md` and README reject Seed as a generic reasoning engine. |
| Diagnostic inventory | Both | Recurrence established visibility governance; contradictions distinguish recordable diagnostic facts from cluster mutation. |

## Operator observations that identify contradictions

Operator observations identifying contradictions should be understood primarily
as:

```text
hypotheses requiring reconciliation
```

They can become implementation evidence when preserved as observations with
provenance. They can become implementation requirements only when repository
scope and tests require behavior. They can become architectural requirements
only after reconciliation against existing authority. Standing alone, operator
contradiction observations are not architecture authority.

This follows Seed's core thesis: natural language can support claims about what
an operator requested or asserted, but it is not direct environmental truth or
architectural authority. It also follows the contradiction reconciliation:
discovery is not creation, visibility is not truth, and resolution is not
history erasure.

## Recovered architectural boundaries

- Claim != Fact.
- Fact != Truth.
- Relationship != Identity.
- Event != State.
- Projection != Authority.
- Contradiction Discovery != Contradiction Creation.
- Contradiction Visibility != Contradiction Existence.
- Recommendation != Decision.
- Decision != Command.
- Capability != Execution.
- Authority to observe or act != ownership claim.
- Diagnostic recording != cluster mutation.
- Diagnostic-run-scoped findings != cluster truth.
- Projection/read-model cache != append-only event ledger.
- Implementation capability metadata != evidential support.
- Projection dependency consumption != transient status consumption.

## Recovered recurring structures

- bounded questions;
- answer responsibility;
- authority boundaries;
- observation -> evidence -> claim -> fact/relationship -> projection;
- event -> change -> state -> projection;
- support aggregation and provenance;
- relationship projection and entity-type validation;
- contradiction/confidence/staleness/graph-issue characterization;
- read-only views and explanation surfaces;
- diagnostic inventory and diagnostic shape auditing;
- diagnostic-run-scoped recording;
- ownership discrepancy -> capability need -> privilege/authority -> correlation
  -> impact investigation paths;
- deterministic projection stages with consumes/produces/influences and
  does-not-influence fields.

## Representative examples

1. **Question Families**: bounded questions recur as an architectural entry
   point; answer responsibility is preserved as metadata rather than collapsed
   into a generic trait.
2. **Projection**: projection recurs across facts, relationships, inference,
   validation, current facts, decision context, and explanation; contradiction
   separates selection, derivation, validation, identity resolution, and
   explanatory boundaries.
3. **Ownership / authority**: ownership and authority recur together; tests and
   authority slices separate authority to observe from ownership claims.
4. **Diagnostic inventory**: diagnostics recur as operational visibility
   surfaces; shape audit and inventory separate supports-json capability,
   recording behavior, ledger writes, and cluster mutation.
5. **Execution vocabulary**: status consumption and projection consumption share
   words but not architecture.

## Reconciliation finding

The repository already embodies a reconciliation process where recurrence and
contradiction are complementary, but not as new standalone architecture.

The implementation-backed formulation is:

```text
Recurrence reveals candidate structure.
Contradiction reveals where the candidate structure may be over-broad.
Evidence and authority reconcile the boundary.
The reconciled boundary lets the recurring structure remain coherent without
collapsing distinct responsibilities.
```

This supports the operator's statement with the evidence-backed caveat that
contradiction is a discovery pressure, not boundary authority by itself.

## Commands executed

```bash
python scripts/seed_local.py --help
python scripts/seed_local.py --documentation-structure --recurrence --summary-only --top 10
python scripts/seed_local.py --projected-state-consumers --json
python scripts/seed_local.py --implementation-trait-characterization --json
python scripts/seed_local.py --projection-shape --json
python scripts/seed_local.py --diagnostic-inventory --json
python scripts/seed_local.py --investigation-path ownership --json
rg --files -g 'AGENTS.md' -g '*.md'
rg -n "recurrence|contradiction|Question Families|answer responsibility|authority|implementation traits|projected-state consumers|execution characterization|execution vocabulary|relationship grammar|runtime responsibility|projection|selection|reasoning|diagnostic inventory" docs tests seed_runtime *.md
rg -n "recurrence|contradiction|contradictions|missing visibility|missing relationship|Question Families|answer responsibility|projected-state consumers|ExecutionStatusConsumer|supports_json|supporting evidence|runtime trace|execution status|projection cache|read-model cache|authority vs ownership|ownership|bounded answers|responsibility" docs README.md seed_runtime tests
```

## Files inspected

- `AGENTS.md`
- `README.md`
- `docs/README.md`
- `docs/seed.md`
- `docs/ontology.md`
- `docs/contradiction_discovery_and_visibility_reconciliation.md`
- `docs/repository_self_explanation_investigation.md`
- `docs/archive/original_book_of_seed/01-architecture.md`
- `docs/archive/original_book_of_seed/02-domain-model.md`
- `seed_runtime/projection_shape.py`
- `seed_runtime/execution_status.py`
- `seed_runtime/events.py`
- `seed_runtime/observations.py`
- `seed_runtime/state.py`
- `seed_runtime/fact_index.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `tests/test_projection_shape.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_implementation_trait_characterization.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_listener_endpoint_authority.py`
- `tests/test_architecture_invariants.py`

## Files changed

- `docs/recurrence_contradiction_architectural_reconciliation.md`

## LOC changed

- Added 630 lines.
- Removed 0 lines.

## Tests run

No test suite was required for this documentation-only reconciliation. The app
surfaces listed above were executed as read-only evidence-gathering commands.
