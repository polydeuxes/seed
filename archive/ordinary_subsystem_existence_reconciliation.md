# Ordinary subsystem existence reconciliation: service ownership authority

## Central answer

One ordinary implementation-backed subsystem can already explain why it exists, but only in a bounded, evidence-derived sense.

The selected subsystem is `service_ownership_authority`. It is not a projection engine and is not a general diagnostic inventory/projection-shape surface. It is a narrow read-only evaluator for one operational question: whether Seed can determine service ownership under a constrained authority profile.

The repository can explain this subsystem's existence because implementation, tests, CLI output, diagnostic inventory, diagnostic shape audit, and question-surface inventory converge on the same operator-visible purpose:

- explain the desired observation: `service ownership`;
- enumerate the evidence classes needed for that observation;
- join those evidence classes to authority requirements;
- report which observations are reachable and which remain blocked;
- preserve the boundary that the evaluator is read-only, non-recording, non-mutating, and non-acquisitive.

Removing it would produce an observable capability loss, not merely an implementation change: operators would lose the existing surface that answers "Can Seed determine service ownership under current authority?" and "Why is service ownership blocked?" as a joined strategy/authority/uncertainty explanation.

## Subsystem selected

`service_ownership_authority`

Reason for selection:

- It is ordinary relative to the prior strongest examples because it evaluates a concrete ownership-authority question rather than describing the whole diagnostic inventory or projection shape.
- It has strong implementation evidence in a dedicated runtime module, CLI path, tests, inventory registration, shape-audit coverage, and question-surface inventory.
- It already consumes other repository surfaces instead of inventing a new architecture framework.

## Files inspected

- `seed_runtime/service_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_inventory.py`
- `seed_runtime/observation_permission.py`
- `docs/service_ownership_authority_reuse_findings.md`
- `docs/bounded_inquiry_explanation_reconciliation.md`
- `docs/current_strategy_bounded_inquiry_reconciliation.md`

## Bounded responsibility

`service_ownership_authority` owns a bounded service-ownership authority evaluation.

Implementation support:

- The module docstring defines the slice as a "Narrow read-only authority slice for service ownership observation."
- `DESIRED_OBSERVATION` is fixed to `service ownership`.
- `SERVICE_OBSERVATIONS` bounds the participating observations to TCP listener inventory, listener-process inventory, systemd unit inventory, container inventory, and container port mapping.
- `CONSTRAINED_AUTHORITY_PROFILE` fixes the default profile that makes root and Docker socket reads unavailable, active network probing unauthorized, local passive observation available, and external provider queries unknown.
- `evaluate_service_ownership_authority_slice(...)` returns a `ServiceOwnershipAuthoritySlice` rather than mutating state.
- The result boundary states `read_only=true`, `records=false`, `writes_event_ledger=false`, `mutates_cluster=false`, `provider_acquisition=false`, `permission_creation=false`, and `executes_observation=false`.

So the responsibility is not "own service truth." It is: evaluate whether currently recognized service-ownership observations are reachable under a supplied authority profile, then expose the remaining authority boundary and uncertainty.

## Consumed implementation

The subsystem consumes only existing implementation-backed inputs:

1. Projected `State` supplied to `evaluate_service_ownership_authority_slice(...)`.
2. Supplied authority profile values for `root`, `docker_socket_read`, `active_network_probe`, `local_passive`, and `external_provider_query`.
3. Current capability needs from `build_capability_needs(state, diagnostic_filter="ownership_discrepancies")`.
4. Ownership discrepancy rows from `build_ownership_discrepancies(state)`.
5. Diagnostic capability records from `diagnostic_capability_need_records(row)`.
6. Capability-to-domain mapping from `observation_domains.CAPABILITY_TO_DOMAIN`.
7. Privilege guidance from `_guidance_for(...)` and `privilege_discovery_explanation_for(...)`.
8. Observation inventory from `build_observation_inventory()`.
9. Observation-domain classification from `build_observation_domains(state)`.
10. Permission-domain recognition from `SUPPORTED_OBSERVATION_CLASSES`.

The CLI invocation `python scripts/seed_local.py --service-ownership-authority --json` confirmed the existing app output consumes these inputs into required observations, required authority, available authority, reachable observations, blocked observations, and uncertainty.

## Produced implementation

The subsystem produces existing operator-visible artifacts:

1. A `ServiceOwnershipAuthoritySlice` data object.
2. JSON through `service_ownership_authority_json(...)` / `to_json_dict()`.
3. Human-readable CLI output through `format_service_ownership_authority(...)`.
4. CLI surface `--service-ownership-authority` and `--json` integration in `scripts/seed_local.py`.
5. Diagnostic inventory entry declaring that the surface uses projected state and repo files, supports JSON, does not support record, reads diagnostic facts, does not write the event ledger, and does not mutate the cluster.
6. Diagnostic shape-audit spec for build, format, and JSON functions.
7. Question-surface inventory row for authority-constrained service ownership.

Current app output includes these produced fields:

- `desired_observation: service ownership`
- `required_observations`
- `required_authority`
- `available_authority`
- `reachable_observations`
- `blocked_observations`
- `blocked_observation_details`
- `outcome: partially_reachable`
- `current_strategy: composite_local_service_attribution_observation`
- `strategy_status: partially_reachable`
- `remaining_observations`
- `uncertainty`
- `remaining_uncertainty`
- `blocking_boundary: docker_or_root_container_runtime_authority_unavailable`
- read-only/non-mutating boundary fields

## Operator-visible capability

The operator-visible capability is authority-constrained service-ownership explanation.

An operator can ask the existing app:

```bash
python scripts/seed_local.py --service-ownership-authority --json
```

and receive a joined answer explaining:

- what observation is desired;
- which evidence classes would participate;
- which evidence classes are reachable under the current constrained profile;
- which evidence classes are blocked;
- why container observations are blocked;
- which authority boundary blocks them;
- which uncertainty remains;
- that the evaluation is read-only and non-mutating.

This is a capability, not just code structure, because the app provides a direct answer to operational questions recorded in question-surface inventory:

- "Can Seed determine service ownership under current authority?"
- "Why is service ownership blocked?"

## Observable regression if removed

Removing this subsystem would remove the existing ability to obtain a single joined service-ownership authority explanation.

Observable loss would appear in multiple existing surfaces:

1. CLI behavior: `--service-ownership-authority` would no longer produce the current service ownership authority report.
2. Tests: `tests/test_service_ownership_authority.py` asserts the constrained-profile outcome, reachable listener/systemd observations, blocked container observations, JSON shape, rendered human output, inventory registration, shape-audit consistency, no mutation behavior, and ownership-discrepancy summary joining.
3. Diagnostic inventory: the declared `service_ownership_authority` surface would be missing or stale.
4. Diagnostic shape audit: the shape spec for `service_ownership_authority` would be inconsistent if the implementation disappeared.
5. Question-surface inventory: the surface that answers authority-constrained service ownership questions would be missing or inaccurate.
6. Behavioral comparison: a raw combination of `capability_needs`, `privilege_discovery`, `observation_domains`, and `observation_permission` would not, by itself, expose the same joined strategy/outcome/remaining-observation explanation.

Therefore removal would cause operator-visible capability loss: the repository would still contain some source ingredients, but the existing composed answer to the service-ownership authority question would disappear.

## Supporting evidence

Implementation-backed support is strong:

- Dedicated evaluator and result shape exist in `seed_runtime/service_ownership_authority.py`.
- Tests prove default constrained output is `partially_reachable` with listener/process/systemd reachable and container observations blocked.
- Tests prove Docker/root-dependent observations are blocked when root and Docker socket read are unavailable.
- Tests prove CLI JSON contains the required shape.
- Tests prove blocked observations include privilege explanation fields.
- Tests prove human output renders blocked observation explanations.
- Tests prove the surface is registered in diagnostic inventory with `supports_record=false`, `record_scope=none`, `writes_event_ledger=false`, and `mutates_cluster=false`.
- Tests prove diagnostic shape audit has no mismatch for this surface.
- Tests prove evaluating the slice does not mutate facts, observed facts, inferred facts, approvals, or events.
- Tests prove the evaluator can join an existing ownership discrepancy summary into blocked observation details when projected state has endpoint-only service evidence.
- Question-surface inventory names the question family and answer responsibility.

## Contradictory evidence

The repository also limits the claim:

- `service_ownership_authority` is itself registered as a diagnostic-like operational surface, so it is not evidence that every ordinary internal module can explain why it exists.
- It is intentionally narrow. It does not prove a repository-wide discipline for all subsystems.
- It does not execute observations, acquire providers, create permissions, record output, write the event ledger, or mutate cluster truth.
- It relies on existing ownership, capability, privilege, inventory, domain, and permission surfaces; it does not independently establish service ownership facts.
- Previous reconciliation notes identify maturity gaps around naming and domain coverage, especially around service-manager and endpoint inventory coverage.

These contradictions do not negate the capability. They prevent overgeneralizing it.

## Remaining uncertainty

Remaining uncertainty is bounded:

- The investigation did not remove the module to run an actual deletion experiment; the regression is inferred from tests, inventory registration, shape audit, CLI behavior, and question-surface inventory.
- The selected subsystem is ordinary relative to projection/diagnostic-inventory examples, but it is still an operational visibility surface. A deeper ordinary subsystem with no CLI surface may not currently explain why it exists.
- The subsystem explains why it exists for a specific operator question, not as a general architectural self-description facility.
- It may not cover every service-ownership evidence class; the implemented bounded list is the authority.

## Answers to required questions

### 1. What bounded responsibility does the subsystem own?

It owns read-only authority-constrained evaluation of service-ownership observation reachability. It identifies required service-ownership observations, maps them to authority requirements, applies a supplied authority profile, reports reachable and blocked observations, reports the blocking boundary, and preserves uncertainty and non-mutating boundaries.

### 2. What implementation-backed inputs does it consume?

It consumes projected state, an authority profile, current ownership-derived capability needs, ownership discrepancies, diagnostic capability records, observation-domain mappings, privilege guidance, observation inventory, observation-domain classification, and permission-domain recognition.

### 3. What implementation-backed outputs does it produce?

It produces a service ownership authority slice, JSON and human CLI reports, diagnostic inventory metadata, diagnostic shape-audit coverage, question-surface inventory coverage, reachable/blocked observation lists, authority maps, uncertainty, blocking boundary, and read-only/non-mutating boundary fields.

### 4. What architectural capability would disappear if removed?

The operator-visible capability to ask why service ownership is only partially reachable under constrained authority would disappear. Operators would lose the single composed answer that ties desired observation, required evidence, authority limits, blocked container-runtime observations, uncertainty, and non-mutating boundary together.

### 5. Would existing repository surfaces naturally expose that capability loss?

Yes. The loss would be exposed by CLI behavior, tests, diagnostic inventory, diagnostic shape audit, question-surface inventory, and behavioral comparison against the existing JSON/human report.

### 6. Can the subsystem currently explain why it exists, or only what it does?

It can explain why it exists in a bounded operator-facing sense. It does more than list mechanics: the question-surface inventory states the questions it answers, the output names the desired observation and strategy, and the evaluator reports remaining observations, blocking boundary, and uncertainty. However, it does not provide a universal self-description of all service-ownership architecture. It explains why this slice exists: to answer authority-constrained service-ownership reachability and blockage.

### 7. Does this strengthen or weaken the claim that architectural observability is a recurring implementation discipline?

It strengthens the claim modestly. Architectural observability has expanded beyond the previously strongest diagnostic-inventory and projection-shape examples into at least one ordinary bounded authority subsystem. It does not prove universality. Diagnostics and projections remain the strongest and most systematic examples, but they are no longer the only implementation-backed examples.

## Final acceptance answers

### Can one ordinary subsystem already explain why it exists?

Yes. `service_ownership_authority` can explain why it exists for one bounded operational question: service-ownership reachability under constrained authority.

### Does removing that subsystem produce observable capability loss, or merely implementation change?

Observable capability loss. The composed operator answer would disappear from CLI output, tests, diagnostic inventory, shape audit, and question-surface inventory.

### Has architectural observability expanded beyond diagnostics and projections?

Yes, but narrowly. It has expanded to a bounded authority evaluator for service ownership. Diagnostics and projections remain the most mature examples; this investigation should not be generalized into a repository-wide architecture framework.

## Files changed

- `docs/ordinary_subsystem_existence_reconciliation.md`

## LOC changed

- Added 247 lines.

## Tests and checks run

- `python scripts/seed_local.py --service-ownership-authority --json`
- `python scripts/seed_local.py --question-surface-inventory --json`
- `pytest -q tests/test_service_ownership_authority.py`

## Recommended next bounded investigation

Investigate exactly one lower-level support subsystem that lacks a dedicated CLI flag, such as `capability_relationship`, to determine whether architectural observability still holds when the subsystem is consumed by other surfaces but is not itself the primary operator-facing report.
