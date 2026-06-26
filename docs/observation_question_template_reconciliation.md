# Observation Question Template Reconciliation

This is a documentation-only reconciliation. It does not add an observation framework, subject framework, inquiry framework, dashboard, planner, runtime redesign, diagnostic surface, CLI flag, probe, recordable output, or operational behavior.

## Central answer

The implementation shows a recurring observation-oriented question shape, but not for every observed subject as a subject-owned property.

The earned shape is strongest where a bounded inquiry already defines the desired observation and required evidence. In those implemented slices, Seed can ask what observations are required or known, which are reachable or blocked, what authority governs them, and what boundary prevents additional conclusions. The shape is weaker for arbitrary subjects because observation inventory is provider/predicate oriented, facts carry optional freshness metadata, and missingness is not globally computable without an inquiry-owned expectation set.

Therefore, the candidate template is currently best characterized as a property of bounded inquiries over observed subjects, not as an intrinsic property of every observed subject.

## Reviewed implementation surfaces

- Observation inventory: `seed_runtime/observation_inventory.py`
- Observation sources and runtime self-observation: `seed_runtime/observation_sources.py`
- Observation ingestion and timestamps: `seed_runtime/observations.py`
- Container ownership authority slice: `seed_runtime/container_ownership_authority.py`
- Service ownership authority slice: `seed_runtime/service_ownership_authority.py`
- Listener endpoint authority slice: `seed_runtime/listener_endpoint_authority.py`
- Freshness and stale fact handling: `seed_runtime/facts.py`, `seed_runtime/state.py`
- Knowledge reachability: `seed_runtime/knowledge_reachability.py`
- Projection/state cache: `seed_runtime/projection_store.py`, `seed_runtime/state.py`
- Tests sampled for surface guarantees: `tests/test_observation_inventory.py`, `tests/test_runtime_self_observation.py`, `tests/test_container_ownership_authority.py`, `tests/test_service_ownership_authority.py`, `tests/test_temporal_characterization.py`, `tests/test_fact_support_aggregation.py`

## Subject findings

### Observation inventory as subject: implemented observation surfaces

**What observations exist?** Supported. `build_observation_inventory` discovers Python classes under `seed_runtime/` that implement `collect()` and are named like observation providers or declare `source_type`. It extracts predicate literals from `Observation(predicate=...)` calls and provider `_observation(...)` calls, then reports providers, predicates, and predicate families.

**What observations are missing?** Partially supported only as absence from discovered implementation. The inventory can show that a provider or predicate is not discovered, but it does not know whether that absence is unknown, unsupported, or required-but-unavailable unless another bounded inquiry supplies the expectation.

**What authority governs observations?** Not directly. Inventory metadata says how providers and predicates were discovered, but authority comes from authority slices, privilege discovery, observation permission, or source metadata, not from the inventory itself.

**Current, stale, uncollected?** Not directly. Inventory is implementation shape, not collected runtime state. It has no per-subject collection timestamp and no stale/uncollected state.

**Boundaries?** Supported as implementation boundary: it is an AST inventory of implemented provider classes and literal predicates, not a runtime claim that observations were collected.

**Confidence:** high for existing observations as implementation surfaces; low for missingness, authority, and freshness as inventory-native capabilities.

### Seed runtime self-observation as subject: `SeedRuntimeObservationSource`

**What observations exist?** Supported for the bounded runtime-process source. `SeedRuntimeObservationSource.collect()` emits normal `Observation` objects for local process/runtime values, including process memory, thread count, uptime when available, backing database/ledger details, and other source-specific predicates.

**What observations are missing?** Not globally supported. The source conditionally emits observations only when local files or constructor inputs provide evidence. For example, process uptime requires `started_at_monotonic`, and `/proc`-derived values require parseable status fields. The absence of a returned observation can mean uncollected, unsupported in the local environment, or not applicable, but the source does not emit a missing-observation record for each absent field.

**What authority governs observations?** Supported at source metadata level. The source declares `read_only`, `local_only`, `mutates_cluster=false`, no shell/subprocess execution, no scheduling, and no runtime governance. This is authority/boundary metadata on emitted observations.

**Current, stale, uncollected?** Current collection time is supported through `observed_at`, either supplied or `datetime.now(timezone.utc)`. Staleness is not source-native unless the resulting facts carry `expires_at`; uncollected observations are not enumerated.

**Boundaries?** Strongly supported. The source docstring states it is read-only and does not persist anything itself; callers use collection and ingestion services. Metadata repeats that it is local/read-only and non-mutating.

**Confidence:** high for existing observations, authority metadata, and collection timestamp; low for complete missingness and stale/uncollected distinctions.

### Container ownership as subject

**What observations exist?** Supported as required observations, not as direct collected facts. The container ownership authority slice fixes the desired observation to `container ownership` and derives required observations from container runtime capabilities: `container_inventory` and `container_port_mapping`.

**What observations are missing?** Supported within the bounded inquiry. With the constrained profile, both required observations remain as `remaining_observations` and the outcome is `blocked`. This is required-but-unavailable, not merely unknown, because both require Docker/root authority and both root and Docker socket read are unavailable.

**What authority governs observations?** Supported. Required authority is obtained from privilege guidance for each required observation, and available authority is supplied by the profile. The implementation explicitly states that the supplied profile is the authority decision source.

**Current, stale, uncollected?** Not supported for this slice. It evaluates reachability and authority, not timestamp freshness of collected container observations. Remaining observations are blocked/uncollected for this inquiry, but not stale.

**Boundaries?** Strongly supported. The slice returns a `blocking_boundary` of `docker_or_root_container_runtime_authority_unavailable` and a boundary object declaring read-only behavior, no records, no event-ledger writes, no cluster mutation, no provider acquisition, no permission creation, and no observation execution.

**Confidence:** high for required observations, required-but-unavailable missingness, authority, and boundaries; low for freshness.

### Service ownership as subject

**What observations exist?** Supported as an inquiry-owned required observation set. The service ownership slice uses TCP listen inventory, listener process inventory, systemd unit inventory, container inventory, and container port mapping. It also consults observation inventory, observation domains, ownership discrepancy capability needs, and privilege discovery.

**What observations are missing?** Supported within this bounded inquiry. The slice distinguishes reachable observations (`tcp_listen_inventory`, `listener_process_inventory`, `systemd_unit_inventory`) from blocked observations (`container_inventory`, `container_port_mapping`) under the constrained profile. This makes container-backed attribution required-but-unavailable while local listener/systemd portions remain reachable.

**What authority governs observations?** Supported. The slice maps each observation to authority (`local_passive`, `partial_non_root`, or `docker_group_or_root`) and compares that requirement to available authority.

**Current, stale, uncollected?** Partially supported only as reachable versus blocked/uncollected. There is no service-ownership freshness decision in this authority slice. It does not inspect `observed_at`/`expires_at` for service observations.

**Boundaries?** Strongly supported. The result has read-only/non-mutating boundary flags and a Docker/root blocking boundary when container observations are blocked. It also records uncertainty that active network probes and external provider queries are not used to promote service ownership beyond local passive evidence.

**Confidence:** high for existing/required observations, missingness inside the bounded inquiry, authority, and boundaries; low for freshness.

### Local listener endpoint inventory as subject

**What observations exist?** Supported. The listener endpoint authority slice requires `listening_protocol`, `listening_address`, `listening_port`, and `local_socket_table_evidence`, and it validates implementation evidence through observation inventory and local-listener domains.

**What observations are missing?** Supported negatively for the bounded endpoint claim: with local passive authority available and implementation support present, no required endpoint observations are blocked. The slice also explicitly lists out-of-scope observations and conclusions, such as process ownership, service ownership, health, external accessibility, DNS validity, and remote reachability. Those are unsupported for the bounded claim, not required-but-unavailable endpoint observations.

**What authority governs observations?** Supported. All required endpoint observations are governed by `local_passive` authority in this slice.

**Current, stale, uncollected?** Partially supported. The slice answers reachability, not collected freshness. `LocalHostObservationSource` collections carry `observed_at`, but this authority slice does not classify endpoint observations as current or stale.

**Boundaries?** Strongly supported. The boundary object is read-only/non-mutating and declares the scope as local TCP/UDP endpoint inventory while listing excluded conclusions.

**Confidence:** high for required observations, authority, and boundaries; medium for missingness in the bounded endpoint claim; low for freshness.

### Projection/state and timestamped facts as subject

**What observations exist?** Supported after ingestion/projection. Observations become evidence and, unless suppressed, facts. Facts preserve subject, predicate, value, dimensions, evidence IDs, source type, confidence, `observed_at`, optional `expires_at`, and inference status.

**What observations are missing?** Not generally supported by projection alone. Unsupported facts are facts with no linked supporting evidence or explicit confidence, and stale facts are expired facts. That is not the same as knowing all observations that should exist for a subject.

**What authority governs observations?** Partially supported through provenance fields (`source_type`, evidence source) and source metadata. Projection itself is a deterministic cache/read model and not the source of truth. It does not independently decide acquisition authority.

**Current, stale, uncollected?** Supported for facts with expiry. `is_fact_expired` uses `expires_at`, and `State.get_stale_facts()` returns expired facts. Facts without `expires_at` are not stale by that mechanism. Uncollected is not generally represented.

**Boundaries?** Supported. Projection store documentation and code characterize projection snapshots as cached state projections/read models, not source of truth. Staleness can also mean projection-cache mismatch, which is separate from observation freshness.

**Confidence:** high for stale/current-by-expiry among facts; medium for existing observations after ingestion/projection; low for uncollected observations and acquisition authority.

### Knowledge reachability as subject

**What observations exist?** Supported as candidate reachability rows, not as generic subject observations. The audit discovers candidates from seeds, event payloads, projected state, docs, source code, and source-navigation terms, then evaluates stages: preserved, projected, read model, inquiry orientation, and rendered.

**What observations are missing?** Supported as stage loss for candidates. Rows have `first_loss`, and metadata includes loss-stage counts. This is not missing observation inventory; it is missing reachability through knowledge stages.

**What authority governs observations?** Partially supported through candidate kind/source and stage boundaries. The audit is especially useful for avoiding promotion of presentation labels into repository knowledge, but it is not a privilege/permission authority model.

**Current, stale, uncollected?** Not supported as observation freshness. It can report cache miss and stage loss, but those are reachability/cache conditions, not observation staleness.

**Boundaries?** Strongly supported as reasoning/presentation boundaries: preserved, projected, read model, inquiry orientation, rendered, and `first_loss` identify where a candidate stops being implementation-backed.

**Confidence:** high for boundaries and stage-loss missingness; medium for existing candidate reachability; low for freshness and acquisition authority.

## Candidate template element evaluation

| Candidate element | Recurs consistently? | Implementation-backed capability | Strongest supporting evidence | Strongest contradictory evidence | Confidence |
| --- | --- | --- | --- | --- | --- |
| Existing observations | Yes, but representation varies | Provider/predicate inventory, source `collect()` output, required observations in authority slices, facts/evidence after ingestion | Observation inventory discovers providers/predicates; authority slices enumerate required observations; observations/facts preserve predicates and subjects | Inventory is implementation shape, authority slices list required observations rather than collected observations, and arbitrary subjects have no universal observation list | High |
| Missing observations | Yes inside bounded inquiries; no globally | Remaining/blocked observations in authority slices; `first_loss` in reachability; absence from inventory only as implementation absence | Container/service slices expose blocked/remaining observations; reachability exposes first-loss stage | Absence is ambiguous without an expected set; inventory cannot classify unknown vs unsupported vs required-but-unavailable | Medium |
| Authority | Yes in authority-oriented slices and source metadata | Required/available authority maps, privilege guidance, read-only/non-mutating metadata | Container/service/listener slices map required authority and available authority; sources emit read-only/local/non-mutating metadata | Observation inventory and projection do not themselves decide acquisition authority; external provider query can remain unknown | High for bounded authority slices, medium overall |
| Freshness | In facts/projection, not in every observation domain | `observed_at`, optional `expires_at`, stale fact queries and refresh recommendations | Observation and Fact models carry timestamps; `is_fact_expired` and `State.get_stale_facts()` implement stale classification | Authority slices do not classify current/stale observations; uncollected is generally not represented; many observations lack `expires_at` | Medium-low |
| Boundaries | Yes, strongly | Boundary flags, excluded conclusions, blocking boundaries, stage loss, projection cache/source-of-truth separation | Authority slices are read-only/non-mutating and list blocking/exclusion boundaries; reachability reports first loss; projection is cache/read model | Boundaries are not expressed through one generic template and vary by inquiry/source | High |

## Unknown, unsupported, and required-but-unavailable

- **Unknown:** External provider query authority is explicitly `unknown` in constrained authority profiles. Subject-specific container pressure is also conditional: it exists only when ownership-discrepancy diagnostics emit matching conflicts.
- **Unsupported:** Listener endpoint inventory explicitly excludes process ownership, service ownership, application ownership, container ownership, health, responsiveness, external accessibility, DNS validity, remote network reachability, causality, and intent for the endpoint claim. Unsupported facts also exist as a separate evidence condition when facts lack supporting evidence.
- **Required but unavailable:** Container ownership requires `container_inventory` and `container_port_mapping`, both requiring Docker/root authority under the constrained profile. Service ownership similarly requires container observations for full attribution, while local listener/systemd observations remain reachable.

## Strongest supporting evidence

1. Bounded authority slices naturally ask for desired observation, required observations, required authority, available authority, reachable/blocked or remaining observations, outcome, uncertainty, and boundaries.
2. Observation inventory gives implementation-backed provider/predicate/family evidence, preventing purely aspirational observation claims.
3. Observation ingestion preserves `observed_at`, `expires_at`, source type, evidence, and confidence, so freshness is implementation-backed where expiry exists.
4. Knowledge reachability prevents presentation vocabulary from becoming knowledge without preserved/projected/read-model evidence.

## Strongest contradictory evidence

1. No implementation proves that every arbitrary observed subject can enumerate all observations it should have.
2. Missingness requires an expected observation set supplied by an inquiry, diagnostic, capability need, or audit; absence from inventory alone is ambiguous.
3. Freshness is not universal. `observed_at` records collection time, but stale/current classification depends on optional `expires_at` or cache-specific version checks.
4. Authority is distributed. It appears in authority slices, privilege guidance, permission classes, source metadata, and projection boundaries, but not as a universal per-observation registry.
5. Some reviewed surfaces answer implementation shape, not subject state: observation inventory inventories code; knowledge reachability audits candidate propagation; projection cache status audits cache validity.

## Property of inquiries or observed subjects?

The candidate shape is currently a property of bounded inquiries over observed subjects.

Implementation evidence supports this because the strongest complete answers begin with inquiry-owned expectations: container ownership fixes `DESIRED_OBSERVATION` and `CONTAINER_OBSERVATIONS`; service ownership fixes a service attribution observation set; listener endpoint inventory fixes a narrow endpoint scope and exclusions; knowledge reachability fixes candidates and stages. Those inquiries decide which observations matter and what counts as missing or boundary-limited.

Observed subjects participate in the shape because facts and observations carry subjects, predicates, timestamps, values, and provenance. But subjects do not own a universal template that can enumerate required observations, missing observations, governing authority, freshness, and boundaries without an inquiry defining the question.

## Final reconciliation

Does every observed subject share a common observation-oriented question shape?

No, not as an implementation-backed universal subject property. Current implementation demonstrates a recurring shape when an inquiry bounds the subject and declares or derives an expected observation set.

Which parts of the shape have been earned by implementation?

- Earned strongly: existing observation surfaces, inquiry-required observations, authority for bounded authority slices, and reasoning/authority/observation boundaries.
- Earned partially: missing observations, when the inquiry supplies an expectation set; freshness, when facts have expiry metadata or when cache validity is the question.
- Still hypothetical: universal per-subject missingness, universal authority per observation, universal current/stale/uncollected classification, and a single subject-owned template across all observed domains.

## Report

### Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!/.git' && git status --short
cat AGENTS.md && rg -n "observation inventory|observation source|container ownership|service ownership|privilege|SeedRuntimeObservationSource|knowledge reachability|projection|timestamp|diagnostic-inventory|diagnostic-shape-audit" -S .
sed -n '1,240p' seed_runtime/observation_inventory.py; sed -n '1,220p' seed_runtime/container_ownership_authority.py; sed -n '1,220p' seed_runtime/service_ownership_authority.py; sed -n '1,220p' seed_runtime/listener_endpoint_authority.py
sed -n '220,520p' seed_runtime/service_ownership_authority.py; sed -n '1,260p' seed_runtime/observations.py
rg -n "class .*ObservationSource|SeedRuntimeObservationSource|expires_at|stale|unsupported|uncollected|required but unavailable|unsupported" seed_runtime tests -S
sed -n '202,280p' seed_runtime/observation_sources.py; sed -n '520,620p' seed_runtime/observation_sources.py; sed -n '660,700p' seed_runtime/state.py; sed -n '1,170p' seed_runtime/facts.py; sed -n '1,220p' seed_runtime/knowledge_reachability.py
python scripts/seed_local.py --observation-inventory --json | python -m json.tool | head -n 80
python scripts/seed_local.py --container-ownership-authority --json | python -m json.tool | head -n 120
python scripts/seed_local.py --service-ownership-authority --json | python -m json.tool | head -n 160
python scripts/seed_local.py --listener-endpoint-authority --json | python -m json.tool | head -n 120
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 | python -m json.tool | head -n 80
```

### Files inspected

```text
AGENTS.md
seed_runtime/observation_inventory.py
seed_runtime/observation_sources.py
seed_runtime/observations.py
seed_runtime/container_ownership_authority.py
seed_runtime/service_ownership_authority.py
seed_runtime/listener_endpoint_authority.py
seed_runtime/facts.py
seed_runtime/state.py
seed_runtime/knowledge_reachability.py
seed_runtime/projection_store.py
tests/test_observation_inventory.py
tests/test_runtime_self_observation.py
tests/test_container_ownership_authority.py
tests/test_service_ownership_authority.py
tests/test_temporal_characterization.py
tests/test_fact_support_aggregation.py
```

### Files changed

```text
docs/observation_question_template_reconciliation.md
```

### LOC changed

```text
+235 -0
```

### Tests run

No automated tests were required for this documentation-only reconciliation. App-level read commands were run as evidence, listed above.

### Recommended bounded implementation slice

No implementation is recommended. If future work is explicitly requested, keep it bounded to preserving one existing inquiry-specific distinction in tests rather than introducing a generic observation, subject, inquiry, dashboard, planner, or runtime framework.
