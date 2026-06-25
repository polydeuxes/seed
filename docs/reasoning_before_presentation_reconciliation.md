---
doc_type: reconciliation
status: implementation-backed finding
scope: deterministic reasoning, presentation projection, authority-aware ownership slices
---

# Reasoning before presentation reconciliation

## Boundary

This reconciliation is observational only.

It asks whether the current repository already demonstrates deterministic
reasoning with presentation acting only as a projection. It does not propose a
reasoning framework, reasoning engine, presentation engine, conversation engine,
planner, generic inquiry runtime, or implementation roadmap.

Repository authority wins.

## Central answer

For the reviewed ownership and authority implementations, Seed already computes
ordered reasoning results before rendering them.

The strongest implementation-backed statement is:

```text
For the reviewed authority and capability diagnostics, presentation does not
create the reasoning fields. Presentation projects structured results that were
already computed by implementation logic.
```

The broader statement below is too strong without qualification:

```text
Reasoning is a repository capability.
Presentation is a projection of repository reasoning.
```

A bounded supported version is:

```text
The reviewed repository surfaces contain deterministic, implementation-backed
reasoning slices. Their human and JSON presentations are downstream projections
of those computed slices.
```

This recognizes existing implementation. It does not discover a new general
reasoning architecture.

## Files inspected

Required implementation files:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/ownership_discrepancies.py`

Required reconciliation documents reviewed:

- `docs/bounded_inquiry_identity_state_reconciliation.md`
- `docs/bounded_inquiry_explanation_reconciliation.md`
- `docs/presentation_conversation_responsibility_reconciliation.md`
- `docs/inquiry_shapes_emerged_reconciliation.md`

Commands used during inspection:

```text
pwd && rg --files -g 'AGENTS.md' -g '*.md' -g '*.py' | sed -n '1,120p'
sed -n '1,240p' seed_runtime/container_ownership_authority.py
sed -n '1,260p' seed_runtime/service_ownership_authority.py
sed -n '1,260p' seed_runtime/capability_needs.py
sed -n '240,520p' seed_runtime/service_ownership_authority.py
sed -n '1,320p' seed_runtime/privilege_discovery.py
sed -n '1,360p' seed_runtime/ownership_discrepancies.py
sed -n '360,760p' seed_runtime/ownership_discrepancies.py
rg --files | rg 'reconciliation\.md$|reconciliations|bounded_inquiry|presentation_conversation|inquiry_shapes'
sed -n '1,220p' docs/bounded_inquiry_identity_state_reconciliation.md docs/bounded_inquiry_explanation_reconciliation.md docs/presentation_conversation_responsibility_reconciliation.md docs/inquiry_shapes_emerged_reconciliation.md
```

## 1. Recurring ordered reasoning components

Across the reviewed implementations, the recurring reasoning order is visible in
code before any formatter runs.

### Authority-slice order

The container and service authority slices recur in this order:

1. desired observation;
2. current strategy;
3. required observations;
4. required authority;
5. available authority;
6. reachable and/or blocked observations;
7. remaining observations;
8. uncertainty and remaining uncertainty;
9. outcome and strategy status;
10. blocking boundary;
11. read-only operational boundary.

Container ownership has the narrower single-strategy form. It fixes the desired
observation, strategy, constrained authority profile, required container-runtime
observations, authority keys, and Docker/root blocking boundary as implementation
constants. The evaluator then normalizes available authority from the supplied
profile, filters required observations through the container-runtime domain,
derives required authority from privilege guidance, determines whether Docker or
root authority is blocked, computes outcome, remaining observations, uncertainty,
and blocking boundary, and only then returns the dataclass result.

Service ownership has the composite form. It fixes the desired observation,
strategy, constrained authority profile, required service-observation family,
authority keys, and Docker/root blocking boundary as implementation constants.
The evaluator then normalizes available authority, derives required observations,
derives per-observation authority, computes reachable observations, computes
blocked observations, determines outcome, builds uncertainty, determines whether
the Docker/root boundary applies, and returns the dataclass result.

### Capability and privilege order

`capability_needs` follows an upstream diagnostic-to-need order:

1. read current ownership discrepancy rows;
2. convert each row into diagnostic capability-need records;
3. merge recorded `diagnostic_run:*` capability-need facts;
4. filter by subject and diagnostic when requested;
5. aggregate subjects, diagnostics, needed evidence, and diagnostic runs by
   capability;
6. sort the capability needs by pressure and priority;
7. expose JSON or human formatting from the aggregated entries.

`privilege_discovery` then follows a capability-to-authority order:

1. read current capability needs;
2. look up registered privilege guidance for each capability;
3. count pressure from affected subjects;
4. emit access level, operational benefit, suggested next step, and notes;
5. preserve a visibility-only, non-mutating boundary;
6. project the result as JSON or human text.

### Ownership discrepancy order

`ownership_discrepancies` follows an evidence-to-conflict order:

1. select storage and service subjects from facts;
2. collect candidate ownership evidence for each subject;
3. match endpoint-only service evidence against local listener facts;
4. match listener facts against listener-process facts where available;
5. order candidates by confidence;
6. assign conflict and reason when evidence remains ambiguous or insufficient;
7. emit capability needs from conflicts;
8. project rows as JSON or human text.

The ordering is deterministic in the reviewed code. It is not represented as one
named generic reasoning object, but the order is implementation behavior.

## 2. Reasoning versus presentation

Current implementation distinguishes reasoning from presentation structurally,
not as a named architecture.

The reasoning side is implemented by evaluators and builders that return
structured dataclasses or rows:

- `evaluate_container_ownership_authority_slice` returns a
  `ContainerOwnershipAuthoritySlice`.
- `evaluate_service_ownership_authority_slice` returns a
  `ServiceOwnershipAuthoritySlice`.
- `build_capability_needs` returns aggregated `CapabilityNeedEntry` values.
- `build_privilege_discovery` returns a `PrivilegeDiscoveryAudit`.
- `build_ownership_discrepancies` returns `OwnershipDiscrepancyRow` values.

The presentation side is implemented by `*_json` and `format_*` functions that
consume those already-computed values. These functions shape dictionaries,
lists, section headings, tables, and text ordering. They do not gather authority,
select facts, match listener evidence, compute conflicts, decide reachability, or
reduce uncertainty.

Therefore the distinction is more than human interpretation for the reviewed
files: the code has separate compute functions and projection functions. It is
less than a repository-wide `Reasoning`/`Presentation` architecture: no reviewed
implementation declares those abstractions as general runtime types.

## 3. Is this statement implementation-backed?

```text
Presentation
does not create
reasoning.

Presentation
projects
existing reasoning.
```

Supported with bounded wording:

```text
For the reviewed authority, capability-need, privilege-discovery, and ownership
-discrepancy surfaces, presentation does not create the computed reasoning
fields. It projects already-computed results into JSON or human-readable text.
```

This is supported because the formatters consume result objects and rows already
containing desired observation, required observations, required authority,
available authority, reachability or blockage, remaining observations,
uncertainty, outcome, conflict, reason, pressure, and boundary.

Unsupported broadening:

- every repository surface follows the same separation;
- Seed has a generic presentation projection engine;
- all human explanations are fully implementation-owned;
- presentation can never affect operator interpretation.

The presentation-conversation reconciliation remains important contradictory
pressure: presentation owns operator encounter order for at least one constrained
slice. That ordering is a real repository responsibility, even though it does not
create the underlying answer fields.

## 4. Where reasoning currently terminates

Reasoning currently terminates in structured result fields, not in prose.

Implementation-backed termination points include:

- `outcome` and `strategy_status` in the authority slices;
- `reachable_observations`, `blocked_observations`, and
  `remaining_observations` in service ownership;
- `remaining_observations` in container ownership;
- `uncertainty` and `remaining_uncertainty` in the authority slices;
- `blocking_boundary` and explicit read-only boundary flags in the authority
  slices;
- `conflict`, `reason`, `candidate_owner`, `confidence`, `evidence_count`, and
  evidence refs in ownership discrepancy rows;
- `capability`, `subjects`, `diagnostics`, and `needed_evidence` in capability
  needs;
- `access_level`, `pressure`, `operational_benefit`, `suggested_next_step`,
  `notes`, and the visibility-only boundary in privilege discovery.

The reasoning does not terminate in a complete operator narrative. The bounded
inquiry explanation reconciliation already found that the full explanation is
composed across multiple existing subsystems. That means the repository supports
structured reasoning endpoints, while the complete narrative remains partly
human-synthesized across surfaces.

## 5. Where presentation begins

Presentation begins when structured results are converted into externally
encountered shapes:

- JSON rendering begins in functions such as `container_ownership_authority_json`,
  `service_ownership_authority_json`, `capability_needs_json`,
  `privilege_discovery_json`, and `ownership_discrepancies_json`.
- Human text rendering begins in functions such as
  `format_container_ownership_authority`, `format_service_ownership_authority`,
  `format_capability_needs`, `format_privilege_discovery`, and
  `format_ownership_discrepancies`.
- CLI ordering is presentation when it controls section order, headings, labels,
  and table layout over existing result fields.
- Operations briefs, storyboards, and operator prose are only implementation-
  backed here to the extent that they project fields already produced by these
  surfaces. The reviewed files do not make those narratives first-class reasoning
  endpoints.

The implementation-backed boundary is therefore:

```text
Reasoning computes structured result fields.
Presentation starts when those fields are rendered, ordered, labeled, or grouped
for JSON or human consumption.
```

## 6. Does any reviewed implementation require presentation to perform reasoning?

No reviewed implementation requires presentation in order to perform its
reasoning.

The authority evaluators compute their result dataclasses before JSON or text
formatting. Capability-needs aggregation completes before its JSON and text
formatters. Privilege discovery completes the audit before formatting. Ownership
discrepancy diagnosis completes rows before JSON and table formatting.

The reverse dependency exists: presentation requires computed results. The
reviewed reasoning functions do not call their formatters to determine outcome,
authority, reachability, conflict, pressure, uncertainty, or boundary.

## 7. Is this repository-supported?

```text
Reasoning
is a repository capability.

Presentation
is a projection
of repository reasoning.
```

Supported only in bounded form.

Implementation supports:

```text
The reviewed repository surfaces contain deterministic reasoning capabilities:
ownership discrepancy diagnosis, capability-need aggregation, privilege guidance,
and constrained authority-slice evaluation.

Their JSON and human presentations are projections of those computed results.
```

Implementation does not support the unbounded architecture claim:

```text
Seed has one repository-wide reasoning architecture and presentation is always a
projection of that architecture.
```

The current evidence shows repeated local reasoning slices, not a generic
reasoning architecture.

## Strongest supporting evidence

The strongest supporting evidence is the repeated compute-then-project structure:

- authority evaluators compute bounded state and terminate in dataclass values;
- JSON functions serialize those values without recomputing authority logic;
- human formatters arrange those values into operator-facing sections;
- capability-needs, privilege-discovery, and ownership-discrepancy builders all
  compute structured rows or audits before formatting.

The reviewed reconciliations support the same boundary:

- bounded inquiry identity and state are structurally separated by fields whose
  behavior changes differently under authority changes;
- explanation is composed across implementation-backed subsystems;
- presentation owns encounter order, not truth or reasoning;
- inquiry shapes emerged from implementation differences without a new framework.

## Strongest contradictory evidence

The strongest contradictory evidence is that the repository does not expose one
first-class reasoning architecture.

Specific limits:

- no reviewed file defines a generic reasoning object or reasoning runtime;
- no reviewed file owns the complete inquiry-level explanation as a single
  runtime record;
- presentation has an independent responsibility for operator encounter order,
  so presentation is not a meaningless pass-through;
- operations briefs, storyboards, and operator prose can be downstream of
  reasoning only when they stay anchored to existing fields;
- some complete explanations remain human-composed across existing surfaces.

These limits reject the broad claim that the repository has discovered a general
reasoning architecture.

## Acceptance answers

### Does Seed already reason before it presents?

Yes, for the reviewed implementations. The code computes authority state,
capability needs, privilege guidance, ownership conflicts, uncertainty,
outcomes, and boundaries before JSON or human formatting projects those results.

### Is presentation downstream of reasoning?

Yes, bounded to the reviewed surfaces. JSON and human formatting consume already
computed results. Presentation is downstream of reasoning for these slices, while
still owning operator encounter order.

### Have we discovered a reasoning architecture, or simply recognized existing implementation?

We have recognized existing implementation.

The repository demonstrates deterministic reasoning slices and downstream
presentation projections. It does not yet demonstrate a generic reasoning
architecture, and this reconciliation does not recommend one.

## Report

### Files inspected

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/ownership_discrepancies.py`
- `docs/bounded_inquiry_identity_state_reconciliation.md`
- `docs/bounded_inquiry_explanation_reconciliation.md`
- `docs/presentation_conversation_responsibility_reconciliation.md`
- `docs/inquiry_shapes_emerged_reconciliation.md`

### Files changed

- `docs/reasoning_before_presentation_reconciliation.md`

### LOC changed

- Added 417 lines.

### Tests run

- Documentation-only reconciliation; no automated tests were required.
- `python -m pytest -q` was not run because no executable code, diagnostic
  inventory, diagnostic shape-audit surface, CLI flag, audit, probe, recordable
  output, or operational surface changed.

### Recommended bounded implementation slice

None for this observational task.

If future work asks for implementation, the bounded slice should stay within
existing surfaces and tests, but this report makes no implementation
recommendation.
