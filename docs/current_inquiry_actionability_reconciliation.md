# Current Inquiry Actionability Reconciliation

## Central answer

Yes, current inquiry outputs already expose a limited structured actionable state, but only as read-only inquiry/presentation state. The implementation can safely project a few bounded dispositions from existing fields such as `outcome`, `reachable_observations`, `blocked_observations`, `remaining_observations`, `required_authority`, `available_authority`, `blocking_boundary`, `limiting_reason`, `guidance_status`, `implementation_evidence`, `uncertainty`, and `boundary`.

No current implementation demonstrates planning, scheduling, retry timing, automatic observation execution, authority acquisition, operator notification priority, or idle self-inquiry. Those remain non-derivable.

## Required surfaces reviewed

- `service_ownership_authority`
- `container_ownership_authority`
- `listener_endpoint_authority`
- `privilege_discovery`
- `capability_needs`
- `question_surface_inventory`

## Existing actionable fields

| Field | Existing meaning | Actionability supported |
| --- | --- | --- |
| `outcome` | Evaluator result such as `reachable`, `partially_reachable`, `blocked`, or `unknown`. | Strongest direct field for bounded answer state. |
| `strategy_status` | Present on service/container authority slices and assigned from `outcome`. | Presentation-compatible status, not independent planning state. |
| `reachable_observations` | Observations available under the constrained authority profile. | Supports partial-vs-complete reachability. |
| `blocked_observations` | Observations unavailable under the constrained authority profile. | Supports blocked-by-authority and remaining observation projection. |
| `remaining_observations` | Service/container slices set this to blocked observations. | Supports a bounded `waiting_for_observation` projection only when paired with authority/limiting fields. |
| `required_authority` / `available_authority` | Required access per observation and supplied authority profile. | Supports authority-blocked distinctions. |
| `blocking_boundary` | Names the current blocking boundary when Docker/root authority is unavailable. | Supports `waiting_for_authority` for Docker/root constrained slices. |
| `blocked_observation_details` | Service slice adds guidance, implementation evidence, and limiting reason per blocked observation. | Supports distinguishing missing authority, missing implementation evidence, and missing guidance where details exist. |
| `guidance_status`, `implementation_evidence`, `limiting_reason` | Privilege discovery explanation fields. | Supports reason-class projection without adding new reasoning. |
| `uncertainty` / `remaining_uncertainty` | Bounded caveats and still-unresolved evidence notes. | Supports incomplete-answer explanation, not autonomous action. |
| `boundary` | Read/write, recording, provider acquisition, permission creation, observation execution, event ledger, and mutation limits. | Prevents unsafe escalation from answer state into runtime action. |
| `answer_responsibility` / `authority_boundary` | Question-surface ownership and safety boundary. | Places the result in answer presentation / inquiry state rather than runtime decision. |

## Distinctions current outputs can make

Current implementation can distinguish these states in bounded ways:

1. **Answer complete / reachable**: `listener_endpoint_authority` returns `outcome="reachable"`, all required observations as reachable, and no blocked observations under local passive authority.
2. **Answer partial**: `service_ownership_authority` returns `outcome="partially_reachable"`, non-empty reachable observations, and non-empty blocked observations.
3. **Blocked by authority**: container/service authority slices expose Docker/root-dependent required authority, unavailable root/docker authority, blocked observations, and `blocking_boundary="docker_or_root_container_runtime_authority_unavailable"`.
4. **Blocked by missing implementation evidence**: `privilege_discovery` can emit `implementation_evidence="not_registered"` and `limiting_reason="missing_implementation_evidence"` when guidance is registered but implementation evidence is missing.
5. **Blocked by missing guidance**: `privilege_discovery` can emit `guidance_status="unknown"` and `limiting_reason="missing_guidance"` for unknown capability needs.
6. **Blocked by missing observation**: current authority slices expose remaining observations, but they usually explain them through authority. A pure missing-observation state is only partially supported by `remaining_observations`/`uncertainty`; it is not a complete standalone disposition across all inquiry outputs.
7. **Waiting for explicit operator input**: not currently derivable. Surfaces say some flags require explicit arguments or explicit authorization, but no common inquiry output field says an answer is waiting on an operator response.

## Safest derivable dispositions now

These can be projected from current outputs without adding new reasoning:

| Disposition | Safe derivation | Notes |
| --- | --- | --- |
| `complete` | `outcome == "reachable"` and `blocked_observations`/`remaining_observations` are empty for that slice. | Safer to call this answer-complete-for-slice, not globally complete. |
| `blocked` | `outcome == "blocked"` with non-empty blocked/remaining observations. | Safe for bounded authority slices. |
| `waiting_for_authority` | `limiting_reason == "missing_authority"`, or Docker/root `blocking_boundary` with unavailable root/docker authority. | Strongly supported for container/service authority. |
| `waiting_for_observation` | Non-empty `remaining_observations`, only if not already classified by authority/guidance/implementation limits. | Weak; should remain conservative. |
| `no_further_action` | Empty capability needs in `capability_needs` or empty privilege-discovery capabilities means no unavailable capability needs identified by current audit inputs. | Only means no current diagnostic capability pressure, not no work in the system. |

## Non-derivable dispositions today

- `waiting_for_operator_input` as a general state: no shared field records an outstanding operator question, requested input, or awaited answer.
- Retry state or retry time: no field models time-to-retry, backoff, cooldown, freshness expiry, or scheduling.
- Notification priority: no field models urgency, recipient, escalation path, or operator notification policy.
- Background task creation: boundaries explicitly say surfaces do not execute observations, acquire providers, create permissions, or mutate the cluster.
- Authority acquisition: privilege discovery suggests visibility/guidance but records no grant request and performs no escalation.
- Automatic observation execution: boundary fields explicitly preserve `executes_observation=false` on reviewed authority slices.

## Responsibility placement

A disposition projection would belong first to **inquiry state / answer presentation**, not runtime decision or background scheduling.

Supporting evidence:

- Authority evaluators are read-only answer surfaces that compute reachability, blockers, uncertainty, and boundaries.
- `question_surface_inventory` maps question families to answering surfaces and authority boundaries; it explicitly says inventory rows do not route or infer operator questions.
- Boundary fields on reviewed slices forbid provider acquisition, permission creation, observation execution, event-ledger writes, and cluster mutation.

Therefore, a disposition would currently be a projection of existing inquiry state, not a new runtime artifact. It becomes a new artifact only if persisted, recorded, scheduled, or consumed by runtime behavior.

## Strongest supporting evidence

- Service ownership has a direct partial-answer shape: `outcome`, `strategy_status`, `reachable_observations`, `blocked_observations`, `remaining_observations`, `blocking_boundary`, and detailed limiting reasons.
- Container ownership has a direct authority-blocked shape under constrained Docker/root authority.
- Listener endpoint authority has a direct reachable shape with no blocked observations while preserving out-of-scope boundaries.
- Privilege discovery has reason-class fields (`guidance_status`, `implementation_evidence`, `limiting_reason`) that distinguish missing authority, missing implementation evidence, missing guidance, and no limiting reason.
- Tests assert the JSON shapes and boundary behavior, including read-only/no-write/no-mutation properties.

## Strongest contradictory evidence

- `strategy_status` is not independent strategy state; service/container slices set it equal to `outcome`.
- `capability_needs` can be empty even while an authority slice still has domain-level blocked observations, so absence of capability needs is not global completion.
- `question_surface_inventory` is a static inventory and explicitly does not route questions, infer arguments, or classify intent.
- Boundary fields explicitly reject execution, provider acquisition, permission creation, event-ledger writes, and cluster mutation.
- No reviewed implementation models queued work, operator prompts, deadlines, retries, priority, or background scheduling.

## Missing evidence before idle self-inquiry could safely exist

Before any idle self-inquiry, Seed would need implementation-backed evidence for at least:

1. A persisted inquiry-state artifact or projection with stable schema and scope.
2. A clear distinction between answer presentation state and executable work.
3. Explicit operator-input request/response state.
4. Observation eligibility separate from observation execution.
5. Authority request/acquisition boundaries separate from privilege guidance.
6. Scheduling/retry/freshness semantics, if any retry is desired.
7. Safety tests proving no implicit cluster mutation, provider acquisition, permission creation, event-ledger write, or diagnostic finding promotion occurs.

## Recommended bounded implementation slice

If a next slice is justified, keep it non-operational: add a read-only inquiry disposition projection for the existing authority slices only. It should accept an already-produced slice payload or evaluator result and return a small non-persisted structure such as:

- `disposition`
- `source_surface`
- `source_outcome`
- `reasons`
- `blocked_observations`
- `remaining_observations`
- `boundary`

It should not schedule, retry, notify, execute observations, acquire authority, record facts, or write the event ledger. Tests should prove projections from reachable listener endpoint, partially reachable service ownership, blocked container ownership, and privilege-discovery missing-guidance/missing-implementation/missing-authority cases.

## Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!*.pyc' -g '!__pycache__'
cat AGENTS.md && rg -n "service_ownership_authority|container_ownership_authority|listener_endpoint_authority|privilege_discovery|capability_needs|question_surface_inventory|remaining_observations|blocked_observations|required_authority|strategy_status|blocking_boundary|limiting_reason" .
sed -n '1,240p' seed_runtime/service_ownership_authority.py; sed -n '1,240p' seed_runtime/container_ownership_authority.py; sed -n '1,240p' seed_runtime/listener_endpoint_authority.py
sed -n '240,430p' seed_runtime/service_ownership_authority.py; sed -n '1,220p' seed_runtime/capability_needs.py; sed -n '1,260p' seed_runtime/privilege_discovery.py; sed -n '1,180p' seed_runtime/question_surface_inventory.py
sed -n '180,340p' seed_runtime/question_surface_inventory.py; python scripts/seed_local.py --service-ownership-authority --json | head -c 4000; python scripts/seed_local.py --container-ownership-authority --json | head -c 4000; python scripts/seed_local.py --listener-endpoint-authority --json | head -c 3000; python scripts/seed_local.py --privilege-discovery --json | head -c 3000; python scripts/seed_local.py --capability-needs --json | head -c 3000; python scripts/seed_local.py --question-surface-inventory --json | head -c 3000
sed -n '1,220p' tests/test_service_ownership_authority.py; sed -n '1,150p' tests/test_container_ownership_authority.py; sed -n '1,150p' tests/test_listener_endpoint_authority.py; sed -n '1,180p' tests/test_privilege_discovery.py
sed -n '180,260p' tests/test_privilege_discovery.py
python -m py_compile seed_runtime/service_ownership_authority.py seed_runtime/container_ownership_authority.py seed_runtime/listener_endpoint_authority.py seed_runtime/privilege_discovery.py seed_runtime/capability_needs.py seed_runtime/question_surface_inventory.py
wc -l docs/current_inquiry_actionability_reconciliation.md
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/question_surface_inventory.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_listener_endpoint_authority.py`
- `tests/test_privilege_discovery.py`

## Files changed

- `docs/current_inquiry_actionability_reconciliation.md`

## LOC changed

- Added 160 lines.

## Tests run

No code behavior was changed. Validation used read-only CLI output inspection listed above and Python bytecode compilation for inspected implementation modules.
