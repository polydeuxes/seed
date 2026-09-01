# Container Ownership Inquiry-State Shape Audit

## Current implementation shape

The current container ownership authority slice is a narrow, read-only diagnostic. It evaluates a fixed desired observation of `container ownership`, maps it to `container_inventory` and `container_port_mapping` when those capabilities belong to the `container_runtime` observation domain, derives required authority from privilege guidance, accepts a supplied authority profile as authoritative, and reports `blocked` when both `root` and `docker_socket_read` are unavailable.

Current JSON shape:

```text
desired_observation
required_observations
required_authority
available_authority
outcome
remaining_observations
uncertainty
boundary
```

Current bounded result for the constrained profile:

```text
desired_observation: container ownership
required_observations: container_inventory, container_port_mapping
required_authority: docker_group_or_root for both required observations
available_authority: root unavailable; docker_socket_read unavailable; active_network_probe unauthorized; local_passive available; external_provider_query unknown
outcome: blocked
remaining_observations: container_inventory, container_port_mapping
uncertainty: external provider unknown; local passive insufficient; docker socket recognized but profile authoritative; subject pressure conditional
boundary: read_only true; records false; writes_event_ledger false; mutates_cluster false; provider_acquisition false; permission_creation false; executes_observation false
```

The diagnostic inventory and shape audit already classify this surface as JSON-capable, non-recording, non-mutating, non-event-ledger-writing, projected-state-based, and diagnostic-fact-reading.

## Proposed inquiry-state shape

The proposed bounded shape is:

```text
Desired observation:
    container ownership

Current strategy:
    container runtime inspection

Strategy status:
    blocked

Blocking boundary:
    service-runtime authority unavailable

Alternative strategies:
    none currently known

Operator interaction:
    authorization required
```

This audit treats the proposal as a possible presentation/output extension for the existing container ownership authority slice only. It does not treat the proposal as a reasoning-chain feature, planner, answer framework, ontology, or general inquiry-state framework.

## Field-by-field support assessment

| Proposed field | Current support | Assessment |
| --- | --- | --- |
| `desired_observation` | Directly present as `container ownership`. | Safe to preserve. |
| `current_strategy` | Not directly present. Can be inferred narrowly from required observations belonging to the `container_runtime` domain. | Safe only if labeled as an output derivation such as `container_runtime_observation` or `container runtime inspection`, and only for this slice. |
| `required_authority` | Directly present per required observation as `docker_group_or_root`. | Safe to preserve. |
| `available_authority` | Directly present from the supplied profile for `root`, `docker_socket_read`, `active_network_probe`, `local_passive`, and `external_provider_query`. | Safe to preserve; profile remains authoritative. |
| `strategy_status` | Not directly present, but equivalent to current `outcome` for this slice. | Safe derivation from `outcome`, with no broader state-machine semantics. |
| `blocking_boundary` | Not directly present. Current evidence supports `root unavailable` plus `docker_socket_read unavailable` blocking Docker/root container runtime evidence. | A specific boundary can be derived, but `service-runtime authority unavailable` overclaims current vocabulary. Prefer `docker_or_root_container_runtime_authority_unavailable` or keep the existing explicit authority fields. |
| `alternative_strategies` | Not directly present. Existing uncertainty says `external_provider_query` is unknown and not mapped to this first slice, and `local_passive` is available but insufficient. | Safe to report only as `not_evaluated`/`not_mapped_in_this_slice`, not as `none currently known`. |
| `remaining_uncertainty` | Directly present as `uncertainty`; could be renamed or duplicated for inquiry-state presentation. | Safe if values remain evidence-backed. |
| `operator_interaction` | Not directly present in container authority output. Observation-permission code has `requires_operator_expression` language for unapproved known observation domains, but container authority currently uses a supplied profile and does not consult permission state to authorize. | Requires new implementation logic if surfaced as a field. `authorization required` risks overclaiming; safer language is `operator expression would be required before any privileged observation execution, but this diagnostic does not request or create authorization`. |
| `boundary` | Directly present. | Safe to preserve. |

## Safe derivations

The following derivations are safe because they are already mechanically supported by current fields or repository evidence:

1. `strategy_status` can be derived from `outcome` for this diagnostic only. In the constrained profile, `outcome=blocked` can produce `strategy_status=blocked`.
2. A narrow strategy label can be derived from the required observations and `CAPABILITY_TO_DOMAIN`: both `container_inventory` and `container_port_mapping` map to `container_runtime`, so a presentation label such as `container_runtime_observation` or `container runtime inspection` is defensible.
3. A narrow blocking boundary can be derived from the existing blocked condition: `root` and `docker_socket_read` are both `unavailable`, while the required authority for the remaining observations is `docker_group_or_root`.
4. `remaining_uncertainty` can reuse the existing `uncertainty` list.
5. The operational boundary can be repeated unchanged: read-only, no records, no event-ledger writes, no cluster mutation, no provider acquisition, no permission creation, and no observation execution.

## Unsafe claims

The following language should be avoided until repository evidence supports it:

- `service-runtime authority unavailable`: the current implementation names `container_runtime` as an observation domain and `docker_group_or_root` as the privilege guidance. It does not define `service-runtime authority` as an authority domain.
- `alternative strategies: none currently known`: the current slice does not enumerate all strategies. It explicitly leaves `external_provider_query` unknown and not mapped, and it says `local_passive` is insufficient for Docker/root container runtime evidence. That supports `no alternative strategy evaluated/mapped in this slice`, not global absence.
- `authorization required`: the container authority slice does not request, enforce, create, or store authorization. Observation-permission code supports `requires_operator_expression` for unapproved known observation domains, but using `authorization required` in this slice would need explicit implementation logic and tests tying the phrase to known permission semantics.
- Any phrase implying a planner, reasoning-chain state, or general inquiry-state lifecycle.
- Any phrase implying that diagnostic-only findings have become cluster truth.

## Recommended smallest implementation change

Do not implement this report's shape yet.

If implementation is later approved, the smallest safe output extension would be limited to this existing diagnostic and would add derived presentation fields without changing authority semantics:

```text
current_strategy: container_runtime_observation
strategy_status: <same value as outcome>
blocking_boundary: docker_or_root_container_runtime_authority_unavailable
remaining_uncertainty: <same values as uncertainty>
```

`alternative_strategies` should either be omitted or reported as `not_evaluated_in_this_slice` / `not_mapped_in_this_slice`. `operator_interaction` should be omitted until there is explicit implementation logic connecting this diagnostic to observation-permission states. If included later, it should avoid `authorization required` unless tests prove that language against repository permission semantics.

The implementation should continue saying `docker_group_or_root` as the required authority because that is the vocabulary registered by privilege guidance for `container_inventory` and `container_port_mapping`. A more general strategy/boundary label can be added only as a derived presentation label; it should not replace the concrete required authority.

## Tests required before implementation

Before adding any output field, tests should prove:

1. JSON output includes each new field only on `--container-ownership-authority --json` and preserves existing fields.
2. Text output renders the new fields without replacing `required_authority` or `available_authority`.
3. `strategy_status` equals `outcome` for the current slice.
4. The blocking boundary appears only when required observations all require `docker_group_or_root` and both `root` and `docker_socket_read` are unavailable.
5. Any strategy label is derived from `container_inventory` and `container_port_mapping` mapping to `container_runtime`.
6. `alternative_strategies` does not claim none exist globally; tests should assert the safer value if the field is added.
7. `operator_interaction` is absent unless explicit permission-state logic is added; if added, tests must prove the exact condition and vocabulary.
8. Diagnostic inventory and diagnostic shape audit stay updated for any modified recordable or operational surface, and the existing required command remains green:

```text
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```

## Non-goals

- No implementation of the proposed shape.
- No new ontology.
- No planner.
- No general inquiry-state framework.
- No new commands.
- No new authority domains.
- No promotion of presentation vocabulary into repository knowledge.
- No event-ledger writes or cluster mutation.

## Answer to acceptance criteria

Can we safely extend the existing container ownership authority slice to preserve the inquiry-state shape?

Partially. The slice can safely preserve the existing desired observation, concrete required/available authority, blocked status, uncertainty, and boundary. It can safely add a small number of derived presentation fields if they remain bound to the existing container-runtime/Docker-root evidence. It cannot safely preserve the proposed shape exactly as written because `service-runtime authority unavailable`, `alternative strategies: none currently known`, and `authorization required` are stronger than current implementation evidence.

What language must be avoided until repository evidence supports it?

Avoid `service-runtime authority`, `none currently known` for alternatives, and unqualified `authorization required`. Prefer concrete implementation-backed language: `container_runtime`, `docker_group_or_root`, `root unavailable`, `docker_socket_read unavailable`, `external_provider_query unknown and not mapped to this first slice`, and `local_passive available but not sufficient for docker/root container runtime evidence`.

## Files inspected

Required files inspected:

- `seed_runtime/container_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Directly relevant files inspected:

- `seed_runtime/observation_domains.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`

## Files changed

- `docs/container_ownership_inquiry_state_audit.md`

## LOC changed

- Added 181 lines in one documentation report.

## Tests run

- `python scripts/seed_local.py --container-ownership-authority --json` — passed; used to confirm the current output shape and constrained blocked result.
- `python scripts/seed_local.py --diagnostic-inventory --json | python -c 'import json,sys; data=json.load(sys.stdin); print([e for e in data if e["name"]=="container_ownership_authority"][0])'` — passed; used to confirm inventory metadata.
- `python scripts/seed_local.py --diagnostic-shape-audit --json | python -c 'import json,sys; data=json.load(sys.stdin); print([r for r in data if r["diagnostic"]=="container_ownership_authority"])'` — passed; used to confirm shape-audit consistency for this diagnostic.
