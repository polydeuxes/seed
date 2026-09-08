# Seed egress versus external-realization grammar recovery 001

## Scope and negative authority

This is one bounded, report-only Fidelity recovery of the surviving `HandoffPlan` district on the current merged `main` after PR 1915. It changes no production code, tests, CLI behavior, event kinds, models, Book clauses, generated artifacts, projection/runtime wiring, or replacement architecture.

The governing question is whether the surviving `HandoffPlan` district represents a lawful Seed-owned egress responsibility or imports the external consumer's provider, backend, execution, approval, credential, retry, and job-management grammar into Seed. The second question is the smallest current implementation boundary that can later be removed without deleting independently warranted capability testimony, observation, projection, or bounded egress distinctions.

This report uses `book_of_seed/repository_constitutional_dimensionality_survey_011.md` as orientation only. Its counts are approximate. Its classification is preserved: acts, constraints, roads / handoffs / uptake, lenses / projections, composition, and movement are not automatically peer dimensions; they are acts, operators, relations, projections, composition, or movement topology operating over dimension-bearing subjects.

Explicit exclusions were honored. `ExecutionStatus`, execution timing, progress cadence, status emission/consumption, diagnostic timing, duration measurement, `PolicyDecision` generally, `Actor` generally, `ToolNeed` lifecycle decompression, `ActionPlan` lifecycle generally, `PendingAction`, `request_tool`, `call_tool`, `ToolkitCandidate`, and `model_visible` were not followed beyond recording adjacency where they surfaced.

## Dimensional orientation

The dimensionality survey supports recurring macro-dimensional families of subject / identity, assertion / content, standing, source / provenance, responsibility, authority / warrant, scope / locality, and occurrence / preservation. The handoff district must therefore be read as material moving through fields, records, projections, and displays that may preserve some coordinates while losing others. Field presence is not standing; projection presence is not delivery; rendering is not receipt.

## City-level ingress / Seed / egress topology

The topology tested here remains:

```text
operator ingress
        ↓
bounded admission / addressability
        ↓
Seed-native dimension-bearing material
        ↓
examination / recording / selection / projection / composition
        ↓
bounded expression
        ↓
Seed egress
        ↓
external receipt / interpretation / realization
```

Current implementation evidence supports internal construction, ledger recording, projection preservation, snapshot serialization, and CLI display of a `HandoffPlan`. It does not evidence external delivery, receipt, interpretation, reliance, or external realization.

## Dimension-bearing material versus boundary roads

Observations and views are not a second city-level axis parallel to ingress/egress. They are possible dimension-bearing material inside the larger boundary topology and may be carried across a boundary road if the road preserves identity, content, standing, provenance, responsibility, authority, scope, and occurrence limits. Likewise, `HandoffPlan` construction is not itself a handoff road to an external consumer.

The following distinctions remain controlling:

- observation != ingress;
- view != egress;
- projection != establishment;
- expression != delivery;
- delivery != receipt;
- receipt != interpretation;
- interpretation != reliance;
- reliance != external realization;
- external realization != Seed occurrence.

## Current HandoffPlan topology

`HandoffPlan` is defined as a legacy/experimental external-provider handoff for an `ActionPlan`, retained for historical projection compatibility and explicit side-path tests, not canonical Runtime or Core MVP behavior. Its constructor rejects secret fields, approval/execution/credential/trust/registration claims, and any `executable` value other than `False`.

`HandoffPlanService.create_handoff_plan(...)` requires a projected `State`, an existing `ActionPlan` id, and an accepted source `ActionPlan`. It optionally uses the capability catalog to find a provider-matching recommendation. It constructs fields from the action plan, recommendation metadata, projected facts, and helper strings. If a ledger is present, it appends `handoff_plan.created`. The CLI `--handoff` command is the current non-test caller and prints the returned plan.

Activity standing by road:

- `HandoffPlan` construction: Active as a current non-test CLI/service path.
- `handoff_plan.created` recording: Recorded locally when the service has a ledger.
- projected-state preservation: Active for replay/snapshot compatibility.
- CLI consumption: Active local display.
- external delivery: not evidenced.
- external receipt: not evidenced.
- external realization: not evidenced.

## Field-by-field artifact standing

### Handoff field matrix

| Field | Source | Derivation | Dimension or local coordinates carried | Standing established | Standing not established | Current consumer | Seed-owned or external-realization grammar | Fidelity classification | Strongest Unknown |
|---|---|---|---|---|---|---|---|---|---|
| `provider` | Accepted `ActionPlan.provider`; catalog lookup uses slug match only. | Copied from action plan after accepted-status check. | identity/content for named recommendation or action-plan provider. | A provider name exists on the source plan. | Provider selected, available, trusted, reached, or responsible. | Ledger projection and CLI display; catalog matching helper. | Mixed: Seed stores testimony/name, but handoff wording treats it as external owner. | mixed compression / foreign grammar when read as owner. | Whether any current consumer independently relies on provider as more than a label. |
| `backend_type` | Matched `CapabilityRecommendation.backend_type` or default `manual`. | Copied from catalog metadata if present; otherwise defaulted. | content/local compatibility coordinate for provider recommendation metadata. | A backend label is present or defaulted. | Backend registration, availability, recipient implementation, or chosen realization strategy. | Handoff model, secret-boundary string, CLI display. | External-realization grammar inside `HandoffPlan`; recommendation metadata may be testimony. | foreign grammar in handoff; independently useful testimony in catalog. | Whether any backend declaration was observed from a provider versus authored catalog compatibility. |
| `operation` | Matched `CapabilityRecommendation.operation` or `ActionPlan.capability`. | Copied from recommendation or defaulted from capability. | content/address label candidate. | An operation string can be displayed. | Addressable external act, registered operation, executable command, or recipient interpretation. | Handoff model and CLI display. | External-realization grammar when treated as remote command; catalog-side metadata may be testimony. | foreign grammar / mixed compression. | Whether operation strings are maintained only for handoff or also for independent capability testimony. |
| `target` | Projected `State.facts`, then `ToolNeed.id`, then `ActionPlan.id`. | Derived by scanning selected predicates and formatting text; multiple hits are de-duplicated by formatted string and flattened. | identity/content/scope hints: host/container/service strings or fallback ids. | Textual target hint exists. | Subject binding, reachability, verified host/container/service identity, provenance, confidence, contradiction handling, or locality preservation. | Handoff model and CLI display. | Handoff-specific external target grammar. | unfaithful / foreign grammar. | Whether any real consumer would understand the flattened target text. |
| `policy_summary` | `ActionPlan.risk_class` and `ActionPlan.requires_approval`. | Formatted helper string. | standing/content about risk and refusal to authorize execution. | Risk class and approval-required bit from source plan are represented. | Approval occurrence, egress authority, external policy acceptance, or delivery permission. | Handoff model and CLI display. | Mostly Seed-owned refusal/boundary text, compressed with external approval language. | mixed compression. | Whether this should survive as independent bounded expression testimony after handoff removal. |
| `secret_boundary` | `ActionPlan.provider` plus derived `backend_type`. | Formatted helper string. | responsibility/content claim about non-secret boundary and external ownership. | Seed does not include secret fields in the plan; model rejects secret/credential claim fields. | Provider possession of credentials, approvals, execution, retries, or job state. | Handoff model and CLI display. | External-realization responsibility grammar imported into Seed. | foreign grammar / overstrong. | Whether any external recipient has such responsibility by separate contract. |
| `requires_external_approval` | `ActionPlan.requires_approval`. | Copied as boolean. | standing/content warning that external approval is required. | Source plan says approval is required. | Approval request, approval grant, provider approval process, or egress authority. | Handoff model; not printed by formatter. | Mixed: Seed can preserve warning; external approval workflow is foreign. | mixed compression. | Whether any current user sees or consumes it outside JSON/state. |
| `executable` | Caller supplies `False`; constructor enforces `False`. | Default/enforced refusal. | standing/refusal coordinate. | The artifact is non-executable. | Seed-shaped lawful egress, delivery, external execution absence, or provider non-execution. | Model validation, tests, projected record. | Seed-owned refusal boundary. | faithful as refusal; not sufficient to save artifact. | Whether non-executable refusal is independently needed once district is removed. |
| `action_plan_id` | Accepted source `ActionPlan.id`. | Copied reference. | identity/provenance link to source plan. | Source record identity is preserved. | Authority for egress, current source freshness, delivery, or provider selection. | Projection, CLI display, causation id default. | Seed-owned reference, though attached to legacy district. | faithful reference / historical compatibility. | Whether source action plan itself remains warranted after separate recovery. |

## Producer act recovery

`HandoffPlanService.create_handoff_plan(...)` performs these current acts:

1. Looks up an `ActionPlan` in `State.action_plans`.
2. Requires `status == "accepted"`.
3. Looks up a capability catalog entry by `action_plan.capability`.
4. Slug-matches recommendation provider names against `action_plan.provider`.
5. Derives `backend_type`, `operation`, `target`, `policy_summary`, and `secret_boundary` using local helper functions.
6. Constructs a `HandoffPlan` with `executable=False`.
7. Optionally appends `handoff_plan.created` to the event ledger.
8. Returns the object to the caller.

The accepted `ActionPlan` contributes source identity, provider text, capability text, risk class, approval-required text, and status eligibility. It does not contribute authority for egress, provider selection standing, backend availability, operation addressability, target validity, external approval occurrence, delivery, receipt, or realization.

The catalog recommendation contributes advisory provider/capability metadata and optional `backend_type` / `operation`. It does not register a provider, select a backend, assert external availability, or authorize invocation.

State facts contribute unscoped textual target hints. The current target helper does not preserve fact ids, supporting evidence ids, subject ids, entity aliases, support/conflict status, confidence, source type, or locality beyond the literal formatted value.

Therefore the service constructs a representation. It does not perform projection itself except through event recording for later projection; it does not perform composition in a constitutionally warranted sense beyond field assembly; it does not form a delivered request; it does not perform a handoff; it does not assign responsibility to an external provider by evidence-backed transfer.

## Provider/backend grammar recovery

| Surface | Current standing | Recovery |
|---|---|---|
| `provider` | Copied/recommended name. | Observed or catalog-authored capability testimony may be useful, but `HandoffPlan` overreads the name as an external owner. |
| `backend_type` | Literal enum `ansible`, `mcp`, `temporal`, `manual`; copied/defaulted into handoff. | In catalog it may be provider recommendation metadata. In handoff it becomes a realization strategy label without evidence that the recipient uses it. |
| `manual` | Default backend. | Historical compatibility/fallback vocabulary; no external consumer availability established. |
| `ansible` | Catalog/test backend label and observation-provider word elsewhere. | Could be independent capability testimony, but handoff does not establish AWX/Ansible recipient standing. |
| `mcp` | Enum/catalog-capable backend label. | External implementation grammar unless separately evidenced as observed capability testimony. |
| `temporal` | Enum/catalog-capable backend label. | External job/workflow grammar; no current handoff delivery or worker evidence. |
| `operation` | Recommendation metadata or capability fallback. | Does not establish an addressable external act, registered operation, or remote command. |
| `target` | Derived formatted text. | Does not preserve enough identity/provenance/scope/standing to be a lawful external execution target. |

Seed has no current evidence that an external recipient uses the named backend. A catalog declaration establishes recommendation metadata, not availability. An accepted `ActionPlan` establishes only accepted plan status, not provider selection. Backend and operation labels describe compatibility-shaped metadata at best and external realization grammar when carried as a handoff plan.

## Target-construction recovery

`_target_for(...)` scans all projected facts for normalized predicates `host`, `service.host`, `target.host`, `container`, `service.container`, `container.name`, `service`, and `service.name`. String values become `host:<value>`, `container:<value>`, or `service:<value>`. The helper de-duplicates formatted strings and joins them with spaces. If no such facts exist, it returns `tool_need:<id>` if the source tool need exists, otherwise `action_plan:<id>`.

Coordinates lost or compressed:

- identity: fact id, subject id, entity identity, alias standing, and exact source subject disappear;
- content: only raw string value survives;
- standing: current support/conflict, confidence, and admissibility disappear;
- provenance: evidence ids, source types, observation ids, and event lineage disappear;
- responsibility: no producer/examiner/recorder boundary survives;
- authority: no warrant for external addressability survives;
- scope/locality: workspace survives only outside the target string; host/container/service locality and multiplicity collapse;
- occurrence/preservation: no occurrence of external target selection or addressability is recorded.

Thus fact value found != target selected; matching predicate != correct subject binding; host text != reachable host; container name != verified container identity; service name != addressable operation target; fallback identifier != external target.

## Secret-boundary and external-responsibility claims

`HandoffPlan` and `HandoffPlanService` are strongest where they make negative Seed claims: no execution, approval/authorization, provider trust, tool registration, credentials, retries, schedules, or long-running provider jobs. The model constructor enforces part of that boundary by rejecting secret fields and approval/trust/registration claims.

The positive claim in `secret_boundary` is overstrong: "provider via backend owns credentials, approvals, execution, retries, and job state." Current repository evidence supports that Seed does not carry secret fields in `HandoffPlan` and does not execute through this service. It does not support that the named provider possesses credentials, owns approvals, owns execution, owns retries, or owns job state.

| Claim | Classification | Evidence standing |
|---|---|---|
| Seed passes only non-secret plan boundary | supported as model/field absence and constructor rejection, though "passes" is overstrong without delivery. |
| Provider owns credentials | unsupported / overstrong. |
| Provider owns approvals | unsupported / overstrong. |
| Provider owns execution | unsupported / overstrong. |
| Provider owns retries | unsupported / overstrong. |
| Provider owns job state | unsupported / overstrong. |
| Seed does not retain credentials in the handoff plan | supported. |
| Seed does not execute through the service | supported. |

Negative Seed ownership does not establish positive provider ownership.

## Event/projection/CLI activity standing

`handoff_plan.created` records construction of a local handoff-plan artifact. It is appended by the service with a `handoff_plan` payload, projected by `StateProjector` into `State.handoff_plans`, serialized by projection snapshots, and included in projection-shape output as a produced projection member. The CLI `--handoff` path constructs and prints the plan.

Projection strengthens local preservation only. It does not strengthen external handoff standing. CLI rendering is the only current non-test consumer of a newly produced plan found in this recovery; state replay/snapshot code consumes historical/local records.

## External delivery and receipt standing

No current non-test road was found that sends a produced `HandoffPlan` to Ansible, MCP, Temporal, a manual operator endpoint, another process, a queue, an API, or any external consumer. No current evidence was found that a consumer receives, interprets, relies on, or realizes a produced `HandoffPlan`.

## Road occurrence matrix

| Road | Current evidence | Activity class | Occurrence standing | Preservation standing | Responsible boundary | Strongest forbidden inference |
|---|---|---|---|---|---|---|
| ActionPlan accepted | Service requires `state.action_plans[id].status == "accepted"`. | Partially active adjacency. | Accepted-plan state exists before handoff construction. | Preserved in `State.action_plans`; not followed generally. | ActionPlan district / legacy side path. | Accepted ActionPlan != authority for egress. |
| HandoffPlan constructed | CLI calls service; service returns object. | Active. | Local object construction. | Optional ledger record if ledger provided. | HandoffPlanService. | Object construction != handoff occurrence. |
| `handoff_plan.created` recorded | Service appends event when ledger present. | Recorded locally. | Records construction/preservation. | Replayed into state and snapshots. | Event ledger / projection. | Ledger append != external delivery. |
| HandoffPlan projected | StateProjector handles event; projection store serializes/deserializes field. | Active/local compatibility. | Projection occurrence from replay. | Local state preservation. | Projection boundary. | Projected HandoffPlan != delivered request. |
| HandoffPlan displayed by CLI | `format_handoff_plan(...)` prints fields. | Active local consumer. | Local rendering occurrence. | Terminal output only unless caller records elsewhere. | CLI/operator display. | CLI display != external receipt. |
| HandoffPlan delivered externally | No evidence found. | Unknown / not evidenced. | None established. | None established. | Unknown external boundary. | Constructible artifact != delivered artifact. |
| External consumer received it | No evidence found. | Unknown / not evidenced. | None established. | None established. | Unknown external consumer. | Delivery != receipt. |
| External consumer interpreted it | No evidence found. | Unknown / not evidenced. | None established. | None established. | External recipient if any. | Receipt != interpretation. |
| External realization occurred | No evidence found. | Unknown / not evidenced. | None established. | None established. | External realization boundary. | External realization != Seed occurrence. |

## Egress dimensional relationship

| Abstract responsibility | Classification | Current recovery |
|---|---|---|
| bounded expression of dimension-bearing material | independently evidenced Seed responsibility / current implementation witness in general, weak in `HandoffPlan`. | CLI display expresses fields locally, but the artifact compresses foreign realization grammar. |
| projection of observations or views | independently evidenced Seed responsibility / current implementation witness. | Projection exists, but not egress. |
| preservation of standing and forbidden inference | independently evidenced Seed responsibility; partial current witness. | Non-executable refusals survive; target/provenance/authority standing is lost. |
| preservation of provenance and locality | independently evidenced Seed responsibility; missing current witness for target. | Source `action_plan_id` survives; target construction drops fact provenance/locality. |
| addressability to a bounded external consumer | Book-only expectation / missing current witness. | No recipient identity or delivery road found. |
| recording of expression occurrence | independently evidenced Seed responsibility; partial witness. | CLI display is not recorded as an expression occurrence. `handoff_plan.created` records construction. |
| recording of delivery occurrence | missing current witness. | No delivery event or transport found. |
| recording of external receipt | foreign realization concern or missing witness depending future boundary. | No receipt record found. |
| recording of external result | foreign realization concern unless separately bounded; no current witness. | No result road found. |

## Fidelity classifications

| Responsibility/surface | Classification | Basis |
|---|---|---|
| Non-executable refusal | faithful | Model/service explicitly deny execution/approval/credentials/trust/registration/job management. |
| Local construction record | faithful as local record | Event records construction when ledger is present. |
| Projection preservation | faithful as compatibility preservation | State and snapshot support retain historical/local record. |
| Provider as external owner | foreign grammar / unfaithful | Name is treated as owner without transfer evidence. |
| Backend enum in handoff | foreign grammar | Chooses or renders recipient implementation vocabulary. |
| Operation as external act | foreign grammar | String lacks addressability/registration/receipt standing. |
| Target construction | unfaithful / foreign grammar | Flattens facts into execution-target text without provenance/scope/standing. |
| Secret-boundary positive ownership claims | foreign grammar / overstrong | Negative Seed ownership is converted into positive provider ownership. |
| CLI local display | faithful as local display, not egress | Current display does not deliver externally. |
| Capability recommendation metadata | mixed but independently useful testimony | Catalog says read-only recommendations do not execute tools. |

## Foreign-grammar findings

The strongest foreign external-realization grammar in the current district is:

1. `backend_type` as `ansible` / `mcp` / `temporal` / `manual` inside `HandoffPlan`.
2. `operation` as a supposed remote operation string.
3. `target` as a constructed host/container/service execution target.
4. `secret_boundary` positive claims that provider/backend owns credentials, approvals, execution, retries, and job state.
5. `requires_external_approval` if read as evidence of an external approval workflow rather than a copied warning.
6. Documentation and tests that describe provider/operator handoff as if a recipient boundary exists, while current implementation evidence only shows local construction/record/display.

## Independently warranted capability testimony

Useful recovered knowledge need not require current `HandoffPlan` survival. The following should remain outside any future handoff deletion boundary unless separately recovered:

- capability catalog entries exist;
- provider recommendations exist;
- recommendation summaries, reasons, risk/source/notes, and ranking behavior can remain useful as advisory testimony;
- observed capability testimony and registered-operation testimony, where separately evidenced, can remain useful;
- `CapabilityRecommendation.backend_type` and `CapabilityRecommendation.operation` may require separate recovery because they are shared recommendation metadata, not solely handoff state;
- bounded external expression distinctions from the Book and dimensionality survey remain useful even if implementation absence is the lawful result.

## Candidate excision boundary

A coherent future excision boundary is visible, but it should not maximize deletion. The smallest coherent candidate boundary is the locally recorded `HandoffPlan` district: model, service, event, state/projection/snapshot support, CLI flag/formatter, handoff-specific target derivation, handoff-specific policy/secret-boundary strings, dedicated tests, and active docs that exist solely to preserve or exercise `HandoffPlan`.

`CapabilityRecommendation.backend_type` and `CapabilityRecommendation.operation` should not be automatically deleted in that same operation. They are shared with capability-catalog recommendation testimony and capability-resolution handoff candidates. Their own standing should be recovered separately before removal or retention is decided.

### Candidate deletion matrix

| Item | District-owned | Shared independent responsibility | Historical requirement | Candidate treatment | Strongest Unknown |
|---|---|---|---|---|---|
| `HandoffPlan` | Yes. | No independent responsibility found beyond local refusal/reference shape. | Historical projection compatibility. | Candidate delete in future bounded excision. | Migration tolerance for old snapshots/events. |
| `HandoffPlanService` | Yes. | No. | Legacy CLI/tests. | Candidate delete. | Whether any hidden external caller imports service. |
| `HandoffBackendType` | Partly. | Shared by `CapabilityRecommendation.backend_type`. | Compatibility. | Do not delete with handoff unless recommendation metadata is separately recovered. | Whether backend metadata is independently observed testimony. |
| `handoff_plan.created` | Yes. | Projection compatibility only. | Historical event replay. | Candidate remove/stop emitting; historical migration requires separate plan. | How to handle old ledgers. |
| `State.handoff_plans` | Yes. | Projection compatibility only. | Historical snapshots/events. | Candidate remove after migration policy. | Snapshot compatibility expectation. |
| projection support | Yes for handoff entries. | Projection system itself is independent. | Historical replay/snapshot. | Remove only handoff-specific entries. | Legacy state payload handling. |
| CLI `--handoff` | Yes. | No independent external delivery found. | Legacy/experimental side path. | Candidate delete. | Operator dependence on local report display. |
| backend_type recommendation metadata | No. | Yes: capability recommendation / capability resolution metadata. | May also be historical. | Preserve pending separate recovery. | Testimony versus realization split. |
| operation recommendation metadata | No. | Yes: capability recommendation / capability resolution metadata. | May also be historical. | Preserve pending separate recovery. | Address label versus executable command. |
| target derivation | Yes. | No. | Test/service helper. | Candidate delete with service. | None beyond hidden caller risk. |
| `policy_summary` | Yes as handoff field/string. | Risk/refusal content may be independently expressible elsewhere. | Handoff tests/docs. | Candidate delete as field; preserve underlying risk/approval testimony elsewhere. | Whether any consumer expects this exact text. |
| `secret_boundary` | Yes. | Negative no-secret boundary is independently useful; positive provider ownership is not. | Handoff tests/docs. | Candidate delete; preserve negative secret-boundary principle outside this artifact. | Whether any external contract supports positive claims. |
| dedicated tests | Yes. | Some tests assert useful refusals. | Regression/historical. | Candidate delete/update with excision. | Which refusal tests should move to another district. |
| active docs | Mixed. | Some docs preserve useful quarantine/refusal findings. | Historical and active audit. | Remove or revise only HandoffPlan-specific active docs after code excision. | Which docs are historical records that should remain. |

## Preservation boundary

A later deletion must preserve independently warranted material outside the handoff district:

- capability catalog existence and read-only recommendation behavior;
- recommendation ranking if separately used;
- provider recommendation reason/score/source/risk notes;
- observed provider capability testimony and registered-operation metadata where implementation-backed;
- dimensionality survey findings and Book distinctions about expression, delivery, receipt, uptake, reliance, realization, occurrence, authority, scope, and provenance;
- negative constraints that Seed should not silently claim credentials, provider trust, approval, execution authorization, retries, schedules, or long-running provider jobs.

## Relationship-transition report search

The exact separate repository result involving approximately three relationship or transition types was not located as a stable three-part taxonomy. The closest current evidence found is:

- `repository_constitutional_dimensionality_survey_011.md` defines relation as comparison, applicability, binding, mismatch, or dependency among dimension-bearing subjects, and movement topology as lawful transition structure among subjects, acts, standings, responsibilities, and scopes.
- `characterization_pass_001.md` uses a compact classification of artifact, lens, and road. It defines a road as a producer assertion accepted by a consumer for a declared purpose, requiring compatible identity, provenance, invariants, applicability, and consumer acceptance; adjacency and constructibility are insufficient.
- `external_grammar_promotion_and_relation_compression_repair_001.md` warns that uptake names a bounded consumer-side relation family, not a universal act or stage, and that receipt, reliance, refusal, and use may be plural consumer-local relations or acts.

Because no exact three-type relationship-transition result was recovered, this report does not manufacture a three-part taxonomy. It uses only the dimensionality survey's operator / relation / topology distinctions plus the recovered artifact/lens/road characterization where directly applicable. The effect on this inquiry is that `HandoffPlan` construction can be an artifact occurrence, projection can be a lens/projection preservation road internal to Seed, but no producer-consumer road to an external recipient is established without external consumer acceptance.

## Adjacent dependency classification

| Adjacent surface | Classification for this recovery |
|---|---|
| `ActionPlan` | Required input to current handoff road; lifecycle standing otherwise excluded / Unknown. |
| `ToolNeed` | Identity/reference fallback only; lifecycle decompression excluded / Unknown. |
| `ToolNeedService` | Shared source for capability-resolution handoff candidates; not fully recovered. |
| `CapabilityCatalog` | Shared source / independently useful testimony. |
| `CapabilityRecommendation` | Shared source / independently useful testimony; backend/operation metadata needs separate recovery. |
| `ProviderRecommendation` wording | Shared source / independently useful testimony where advisory. |
| `ToolRecommendationService` | Recommendation ranking adjacency; independently useful if read-only, not followed fully. |
| recommendation ranking | Adjacent independent capability testimony; not handoff execution. |
| `ToolSpec` | Identity/reference only where docs compare registered operation; not followed. |
| provider registration | Adjacent contrast: no registration established by handoff. |
| capability metadata | Shared source. |
| precondition reporting | Adjacent legacy side path; not followed. |

## Unknowns

- Whether any out-of-repository operator process parses CLI `--handoff` output as an external receipt. No repository evidence proves one.
- Whether old ledgers/snapshots in user environments require long-term `handoff_plan.created` replay compatibility.
- Whether `CapabilityRecommendation.backend_type` and `operation` are merely historical handoff vocabulary or independently observed capability testimony.
- Whether a future lawful egress boundary should record expression, delivery, receipt, or external result; this report must not design it.
- Whether any positive provider responsibility claim is supported by an external contract not present in this repository.

## Smallest lawful next operation

The smallest lawful next operation is a bounded removal-design or excision-preparation report for the `HandoffPlan` district only, with a separate preservation plan for historical replay/snapshot compatibility and a separate recovery for `CapabilityRecommendation.backend_type` / `operation` testimony. No code removal should happen until that operation states migration/test/doc treatment explicitly.

## Lawful stopping point

This inquiry stops at report-only recovery. It does not delete `HandoffPlan`, does not delete backend metadata, does not alter capability recommendations, does not change `ActionPlan`, CLI, events, projection, tests, docs, Book clauses, or runtime wiring, and does not introduce any replacement egress architecture.

## Final direct answers

1. **What is the city-level relationship between operator ingress, Seed, and Seed egress?** Operator ingress admits/addressably presents material to Seed; Seed examines, records, selects, projects, composes, and may express bounded dimension-bearing material; Seed egress is a later bounded expression boundary before external receipt, interpretation, reliance, or realization.
2. **Are observations and views a second independent axis, or dimension-bearing material inside the larger boundary topology?** They are dimension-bearing material inside the larger boundary topology, not a second independent city-level axis.
3. **What does `HandoffPlan` actually establish?** It establishes a locally constructed, non-executable, legacy/experimental record with copied/derived provider/backend/operation/target/policy/secret-boundary fields and refusal constraints. It does not establish handoff, delivery, receipt, external responsibility, or realization.
4. **Does `HandoffPlanService` perform a handoff?** No. It constructs a representation and optionally records it locally.
5. **What current external consumer receives a produced `HandoffPlan`?** None evidenced.
6. **What does `handoff_plan.created` record?** It records local construction/preservation of a `HandoffPlan` payload, not external delivery or handoff occurrence.
7. **Does projected-state presence establish delivery?** No.
8. **Does CLI rendering establish external receipt?** No.
9. **Does `provider` preserve testimony or selection?** In the handoff it preserves a copied provider name from an accepted `ActionPlan`; catalog matching may reflect recommendation testimony. It does not establish provider selection, availability, trust, or responsibility.
10. **Does `backend_type` describe observed capability or choose external realization?** In `HandoffPlan` it imports external-realization grammar. In capability recommendations it may be advisory testimony, but that requires separate recovery.
11. **Does `operation` establish an addressable external act?** No. It is a recommendation string or capability fallback, not an addressable external act.
12. **Does `target` preserve sufficient identity, provenance, scope, and standing?** No. It flattens facts into text and drops binding, provenance, scope, confidence, contradiction, and authority.
13. **What supports the secret-boundary responsibility claims?** Only negative Seed boundaries are supported: no secret fields, no execution, no approval/authorization/trust/registration/job management in the service/model. Positive provider ownership claims are unsupported.
14. **Does negative Seed ownership establish positive provider ownership?** No.
15. **Which current fields are foreign external-realization grammar?** `backend_type`, `operation`, `target`, and the positive ownership part of `secret_boundary` are strongest; `provider` and `requires_external_approval` become foreign grammar when read as external selection/approval workflow rather than copied labels/warnings.
16. **Which capability/provider testimony is independently useful?** Capability catalog entries, provider recommendation metadata, recommendation reasons/summaries/scores/source/risk notes, observed capability testimony, and registered-operation testimony where separately evidenced.
17. **Is the HandoffPlan district active, partially active, locally recorded, constructible, or historical?** Mixed: construction and CLI display are active local side paths; event/projection are locally recorded; external delivery/receipt/realization are not evidenced; the district is also legacy/historical compatibility.
18. **Is there any current external delivery road?** No current external delivery road was evidenced.
19. **What exact relationship-transition taxonomy was recovered, if any?** No exact three-type taxonomy was located. The closest recovered categories are artifact/lens/road, plus relation examples of comparison/applicability/binding/mismatch/dependency and movement topology distinctions.
20. **What is the smallest coherent candidate excision boundary?** The `HandoffPlan` district: `HandoffPlan`, `HandoffPlanService`, `handoff_plan.created` emission/projection/state/snapshot support, CLI `--handoff` and formatter, handoff-specific target derivation, policy/secret-boundary strings, dedicated tests, and active docs that exist solely for that district, subject to historical migration planning.
21. **What must remain outside that deletion boundary?** Capability catalog/recommendation testimony, recommendation ranking if independently used, observed capability and registered-operation testimony, dimensionality/egress distinctions, and negative constraints against secret/execution/approval/trust/job claims.
22. **Does any replacement egress architecture need to be built now?** No.
23. **What is the smallest lawful next operation?** A bounded excision-preparation/migration report for the `HandoffPlan` district, plus separate recovery of recommendation `backend_type` / `operation` standing.
24. **Where must this inquiry stop?** At this report-only boundary, before code deletion, metadata deletion, CLI/event/projection changes, Book amendments, tests, or replacement architecture.
