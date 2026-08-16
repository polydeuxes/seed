# Expectation Sets as Observable Artifacts Reconciliation

This reconciliation remains observational. It asks whether implementation-backed expectation sets have emerged as observable repository artifacts, not whether Seed should introduce an expectation framework.

## Answer

Yes, but only in a bounded sense. Current implementation has earned observable expectation-set artifacts where evaluators or diagnostics explicitly materialize a desired observation with required observations, authority requirements, reachable/blocked status, uncertainty, and read-only boundary. The strongest examples are the authority evaluators for container ownership, service ownership, and listener endpoint authority. Capability needs, privilege discovery, observation domains, knowledge reachability, filesystem ownership evidence, and runtime self-observation supply recurring members and supporting status vocabulary, but they do not form one general expectation framework.

Therefore expectation sets should currently be regarded as observable artifacts in these specific implemented surfaces, while remaining implementation details elsewhere. The repository does not expose a generic `expectation_set` model, CLI, registry, or comparison API.

## Reviewed implementation-backed expectation sets

| Inquiry / surface | Explicit expectation set | Implementation evidence | Confidence |
| --- | --- | --- | --- |
| Container ownership | `required_observations = (container_inventory, container_port_mapping)` with required `docker_group_or_root`; blocked under the constrained profile. | `CONTAINER_OBSERVATIONS`, `required_observations`, `_guidance_for`, `remaining_observations`, and the JSON/formatter fields in `container_ownership_authority.py`. | High |
| Service ownership | `required_observations = (tcp_listen_inventory, listener_process_inventory, systemd_unit_inventory, container_inventory, container_port_mapping)` after diagnostic need enrichment/deduplication. | `SERVICE_OBSERVATIONS`, `_required_service_observations`, reachability/blocking classifiers, blocked details, and remaining observations in `service_ownership_authority.py`. | High |
| Listener endpoint authority | `required_observations = (listening_protocol, listening_address, listening_port, local_socket_table_evidence)` under `local_passive` authority. | `LISTENER_ENDPOINT_OBSERVATIONS`, required authority construction, endpoint evidence checks, reachable/blocked observations, and boundary excludes in `listener_endpoint_authority.py`. | High |
| Filesystem ownership / storage attribution | Conflict-to-need mappings include `mount_source_inventory`, `export_visibility_inventory`, `nfs_export_inventory`, `smb_share_inventory`, and `remote_storage_export_inventory`; filesystem evidence is also preserved in state summary tests. | `_CAPABILITY_NEEDS_BY_CONFLICT` and `diagnostic_capability_need_records` in `ownership_discrepancies.py`; filesystem summary/storage candidate tests prove observable filesystem facts remain evidence rather than inferred ownership truth. | Medium-high |
| Privilege discovery | Current capability needs become capability rows with access level, guidance status, implementation evidence, limiting reason, and non-mutating boundary. | `_CAPABILITY_GUIDANCE`, `_IMPLEMENTATION_EVIDENCE`, `build_privilege_discovery`, and `_limiting_reason` in `privilege_discovery.py`. | High for status vocabulary; medium for expectation-set ownership because rows depend on capability needs. |
| Capability needs | Diagnostic-only capability needs aggregate by capability, subjects, diagnostics, needed evidence, and diagnostic runs. | `CapabilityNeedEntry`, `build_capability_needs`, `_add_capability_need`, and `capability_needs_json` in `capability_needs.py`. | High |
| Knowledge reachability | Candidate sets are observable audit inputs by family/kind/source and can be filtered; however no expectation set is promoted from presentation vocabulary without reachability evidence. | `DEFAULT_SEEDS`, `FAMILIES`, `CANDIDATE_KINDS`, metadata/candidate counts, and tests in `knowledge_reachability.py`. | Medium |
| Seed runtime self-observation | Runtime process observations are normal read-only observations with metadata stating local-only, no shell/subprocess, no mutation. Classification coverage recording stores diagnostic self-observation on `diagnostic_run:` subjects. | `SeedRuntimeObservationSource.collect` in `observation_sources.py` and classification coverage recording tests. | Medium-high |

## Observable properties

| Property | Earned? | Evidence | Confidence |
| --- | --- | --- | --- |
| Membership | Yes. Explicit tuples/lists name members in authority slices, capability needs, privilege guidance, and domain maps. | `CONTAINER_OBSERVATIONS`, `SERVICE_OBSERVATIONS`, `LISTENER_ENDPOINT_OBSERVATIONS`, `_CAPABILITY_GUIDANCE`, `CAPABILITY_TO_DOMAIN`. | High |
| Size | Yes, by observable list length in JSON outputs and tuple constants. No separate size field is exposed. | CLI JSON outputs contain arrays for `required_observations`, `reachable_observations`, `blocked_observations`, `remaining_observations`; capability needs count subjects. | High for computable size; low for first-class size property. |
| Shared observations | Yes. `container_inventory` and `container_port_mapping` recur in container and service ownership; `listener_process_inventory` recurs through capability needs, observation domains, and privilege discovery; local listener predicates recur across inventory and listener endpoint authority. | Authority evaluators, `CAPABILITY_TO_DOMAIN`, `_CAPABILITY_GUIDANCE`, `_CAPABILITY_NEEDS_BY_CONFLICT`. | High |
| Required observations | Yes in the three authority evaluators. Capability needs expose `needed_evidence` and `candidate_capability`, but not as a universal required-observation set. | `required_observations` fields and JSON renderers in authority evaluators; `diagnostic_capability_need_records` for diagnostic needs. | High for evaluators; medium across repository. |
| Optional observations | Not explicitly earned as a named property. Some observations are out-of-scope or unused under current strategy, and local passive evidence can be reachable while Docker/root evidence remains blocked, but implementation does not label optional members. | `OUT_OF_SCOPE` in listener endpoint authority and uncertainty strings in evaluators. | Low |
| Blocked observations | Yes for service and listener endpoint authority; container authority uses `remaining_observations` plus `blocking_boundary`, not a `blocked_observations` field. | `_is_blocked`, `blocked_observations`, `blocked_observation_details`; container `remaining_observations` when `outcome == blocked`. | High |

## Recurrence

Recurrence is implementation-backed for these members:

- `container_inventory`: container ownership required observation, service ownership required/blocked observation, privilege guidance entry, observation-domain pressure for `container_runtime`, and diagnostic capability need candidate.
- `container_port_mapping`: same recurrence as `container_inventory`.
- `listener_process_inventory`: service ownership required/reachable observation, privilege guidance entry, observation-domain pressure for `local_listeners`, and diagnostic capability need candidate.
- `systemd_unit_inventory`: service ownership required/reachable observation, while privilege guidance uses the related `systemd_inventory` name and maps it to available/local-passive attribution.
- `tcp_listen_inventory`: service ownership required/reachable observation and `missing_owner` diagnostic capability need candidate.
- Listener endpoint predicates (`listening_protocol`, `listening_address`, `listening_port`, `listening_endpoint`) recur in observation inventory and endpoint authority evidence.

This recurrence is not inferred from vocabulary alone. It is backed by constants, conflict maps, domain maps, privilege guidance, and CLI JSON output.

## Comparability

Expectation sets can be compared by ordinary implementation-observable properties because their members are serialized arrays or tuples. The implementation already supports conclusions such as:

- Shared members: container and service ownership share `container_inventory` and `container_port_mapping`.
- Exclusive members: listener endpoint authority has `listening_protocol`, `listening_address`, `listening_port`, and `local_socket_table_evidence`, which are not members of the container ownership set.
- Subset: the container ownership required set is a subset of the service ownership required set in current implementation output.
- Intersection: service ownership intersects listener-domain pressure through `listener_process_inventory` and local listener evidence, but it does not share the exact listener endpoint predicate set.

No comparison algorithm, comparison CLI, or first-class comparison record is currently implemented. Comparability is earned only because the sets are exposed in deterministic data structures.

## Required, reachable, blocked, unsupported, unknown

Current implementation can distinguish these statuses only partially and surface-by-surface:

- `required`: explicitly represented by `required_observations` in authority evaluators and by `needed_evidence` / `candidate_capability` in diagnostic capability needs.
- `reachable`: explicitly represented by `reachable_observations` in service and listener endpoint authority.
- `blocked`: explicitly represented by `blocked_observations` in service and listener endpoint authority; container ownership represents blocked remaining observations and a blocking boundary.
- `unsupported`: represented elsewhere for facts/context and as missing implementation evidence in privilege discovery, but not as a per-member authority-evaluator status.
- `unknown`: represented in authority profiles, evaluator outcomes, observation-domain classification/gap type, knowledge reachability candidate kind, and privilege guidance status/implementation evidence.

Thus the status vocabulary exists, but no single expectation-set artifact currently carries every status for every member.

## Removal impact

Removing these expectation sets would produce both implementation loss and observable capability loss:

- Removing authority evaluator required-observation sets would break the evaluator implementations and remove CLI JSON/text visibility into desired observation, required observations, authority, outcome, remaining work, and boundary.
- Removing capability-need mappings would remove current/recorded diagnostic pressure aggregation and weaken privilege discovery, observation domains, operational story, and pressure/relationship surfaces that consume capability needs.
- Removing privilege guidance would preserve some raw capability names but lose access-level, guidance status, implementation-evidence, limiting-reason, and missing-authority visibility.
- Removing runtime self-observation would lose an observable source for Seed process facts; removing classification coverage diagnostic-run scoping would risk diagnostic findings becoming cluster truth.

## Observable artifact or implementation detail?

The repository currently treats expectation sets as both, depending on surface.

Observable artifact evidence:

- CLI surfaces serialize `required_observations`, `required_authority`, `reachable_observations`, `blocked_observations`, `remaining_observations`, `uncertainty`, and non-mutating boundaries.
- Diagnostic inventory and shape audit register the authority surfaces, proving they are operationally visible rather than private helper code.
- Tests assert the exact members, blocked/reachable outcomes, JSON shape, and non-mutating boundaries.

Implementation-detail evidence / strongest contradiction:

- There is no `ExpectationSet` class, no generic expectation registry, no comparison API, no planner/reasoning engine, and no generic inquiry engine.
- Optional observations are not a first-class property.
- Unsupported status is not consistently attached to individual expectation-set members.
- Several expected observations are stored under capability vocabulary (`candidate_capability`, `needed_evidence`, `pressure`) rather than an expectation vocabulary.
- Knowledge reachability can reject presentation vocabulary as repository knowledge; therefore repeated labels alone do not create expectation artifacts.

## Earned properties vs hypotheses

Earned by implementation:

- Bounded membership for the three authority evaluator expectation sets.
- Required-observation arrays in evaluator JSON output.
- Authority requirements per required observation.
- Reachable and blocked partitions in service and listener endpoint authority.
- Remaining observations and blocking boundary in container/service authority.
- Recurrence of `container_inventory`, `container_port_mapping`, `listener_process_inventory`, and listener endpoint predicates across independent surfaces.
- Non-mutating, read-only boundaries for diagnostics and runtime self-observation.
- Diagnostic-run scoping for recorded diagnostic self-observation.

Still hypotheses:

- A universal expectation-set abstraction.
- Optional observation semantics.
- Complete per-member status lattice across required/reachable/blocked/unsupported/unknown.
- Repository-wide expectation-set comparison semantics.
- Expectation promotion from history, presentation vocabulary, or repeated labels.
- Any planner, reasoning engine, generic inquiry engine, or new observation subsystem.

## Final conclusion

Implementation-backed expectation sets have already become observable repository artifacts in bounded evaluator and diagnostic surfaces. The earned properties are membership, required observations, authority mapping, reachability/blocking for some sets, recurrence of specific members, remaining work, uncertainty, and non-mutating boundaries. They should not yet be regarded as a repository-wide framework. The safest current classification is: bounded observable artifacts where the implementation serializes and tests them; implementation details everywhere else.

## Commands executed

- `pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' && git status --short`
- `cat AGENTS.md && rg -n "container ownership|service ownership|listener endpoint|filesystem ownership|privilege|capability needs|knowledge reachability|self-observation|diagnostic-inventory|shape-audit|expectation|Required observations|container_inventory|listener_process_inventory|systemd_unit_inventory|container_port_mapping" .`
- `rg -n "def evaluate_.*ownership|class .*Authority|container_ownership|service_ownership|listener_endpoint|filesystem|CAPABILITY_TO_DOMAIN|needed_evidence|required_observations|blocked_observations|unsupported|unknown|reachable" seed_runtime tests scripts/seed_local.py | head -n 300`
- `sed -n '1,260p' seed_runtime/container_ownership_authority.py; sed -n '1,280p' seed_runtime/service_ownership_authority.py; sed -n '1,260p' seed_runtime/listener_endpoint_authority.py; sed -n '1,260p' seed_runtime/privilege_discovery.py`
- `sed -n '120,320p' seed_runtime/service_ownership_authority.py; sed -n '1,260p' seed_runtime/capability_needs.py; sed -n '1,240p' seed_runtime/observation_domains.py; sed -n '150,230p' seed_runtime/ownership_discrepancies.py`
- `sed -n '1,180p' seed_runtime/knowledge_reachability.py; sed -n '200,290p' seed_runtime/observation_sources.py; sed -n '520,620p' seed_runtime/observation_sources.py; sed -n '140,200p' tests/test_classification_coverage.py`
- `python scripts/seed_local.py --container-ownership-authority --json && python scripts/seed_local.py --service-ownership-authority --json && python scripts/seed_local.py --listener-endpoint-authority --json && python scripts/seed_local.py --capability-needs --json && python scripts/seed_local.py --privilege-discovery --json && python scripts/seed_local.py --observation-domains --json && python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-candidate expectation --knowledge-candidate-kind repository_concept` (failed on unsupported CLI arguments after earlier commands completed)
- `python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --candidate-kind repository_concept --knowledge-reachability-audit-limit 20`

## Files inspected

- `AGENTS.md`
- `scripts/seed_local.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/knowledge_reachability.py`
- `seed_runtime/observation_sources.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_listener_endpoint_authority.py`
- `tests/test_classification_coverage.py`
- Relevant prior reconciliations under `docs/` found by ripgrep.

## Files changed

- `docs/expectation_sets_observable_artifacts_reconciliation.md`

## LOC changed

- Added one documentation file with this reconciliation; no runtime, diagnostic registry, shape-audit, or test code changed.

## Tests run

- No automated test suite was required for this documentation-only observational reconciliation.

## Recommended bounded implementation slice

No expectation framework is recommended. If implementation work is later requested, the bounded slice should be limited to preserving current visibility: add tests or a small read-only diagnostic check proving the existing authority evaluator JSON fields (`required_observations`, `reachable_observations`, `blocked_observations`, `remaining_observations`, and boundaries) remain stable. Do not introduce a planner, reasoning engine, generic inquiry engine, new runtime abstraction, or new observation subsystem.
