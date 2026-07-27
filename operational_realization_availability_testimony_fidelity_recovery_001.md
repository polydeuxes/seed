# Operational-realization availability testimony Fidelity recovery 001

## 1. Boundary, method, and governing answer

This is one bounded, report-only recovery on merged `main` commit `8fdbece`,
after PR 2016. It changes no canonical Book, root documentation, `docs/`, prior
report, production code, test, public API, diagnostic, CLI, event, persistence,
or cluster state. Repository implementation is authority; prior reports were
used only as navigation and counterevidence.

**Governing answer:** the only current supplier of
`OperationalRealizationStandingTestimony` found by repository-wide symbol
search is test fixture code. The runtime exposes the testimony class and a
projection function, but contains no producer that observes, derives,
compiles, copies, defaults, or adjudicates realization availability. A caller
constructs the record and supplies the literal `availability_standing` value.
`source_ref` and `evidence_ref` accompany that assertion, but they are opaque
references: the projection checks only that `evidence_ref` occurs in the
horizon's evidence-reference inventory. It never resolves either reference or
tests whether the referenced material supports availability.

The exact current topology is therefore:

```text
external caller (no runtime producer occurrence found)
  -> OperationalRealizationRequirementTestimony(required_transformation_ref, ...)
  -> OperationalRealizationStandingTestimony(availability_standing, ...)
  -> project_operational_realization_demand(...)
  -> OperationalRealizationDemandProjection.{established|unsupported|unknown|
                                               conflicting|unclassified_here|
                                               unclassified}
  -> optional assemble_goal_advancement_demand_set(
         operational_realization=projection)
  -> GoalAdvancementDemandSet family record(disposition="supplied")
  -> STOP
```

The focused test is the only concrete caller of the projector and directly
constructs both testimonies. The demand-set assembler is an implemented
consumer type, but its tests do not supply an operational-realization
projection. No non-test runtime orchestration calls either road. Thus the road
is public and test-active/constructible, not demonstrated as an occurring
production road.

This is the active **missing crossing location**, but not an already completed
competency-evidence crossing. Demand genuinely relies on the caller's
availability label to classify Demand. Nothing crosses from demonstrated
realization occurrences to that label. Availability is not competency here,
and the current testimony is not proved false or intrinsically unsupported;
it may truthfully cite evidence known to its caller. The implementation merely
cannot distinguish such truthful, evidence-derived testimony from an
unsupported declaration.

## 2. Exact producer, caller, testimony, Demand, and consumer topology

| Stage | Implemented owner / occurrence | Exact input or output | What happens | Standing |
| --- | --- | --- | --- | --- |
| Requirement supplier | No production producer or caller found. The focused test `_req` is the only occurrence. | Caller constructs `OperationalRealizationRequirementTestimony`. | All semantic values and references are declared by caller. Defaults fill family, boundedness, applicability, materiality, and notes only. | Caller testimony; not a derived transformation requirement. |
| Availability supplier | No production producer or caller found. The focused test `_standing` is the only occurrence. | Caller constructs `OperationalRealizationStandingTestimony`. | Caller supplies availability, coverage, blocker ownership, identities, provenance references, and optional realization references. | Caller testimony; no observation/adjudication producer. |
| Demand classifier | `project_operational_realization_demand`. Focused test calls it twice. | Goal, horizon, requirement iterable, standing iterable. | Validates some identities, takes the first matching standing, applies `_conclude`, and buckets an item. | Implemented read-only classification. |
| Demand standing | `OperationalRealizationDemandProjectionItem`. | Joined testimony fields, two evidence references, conclusion or unclassified reason. | Preserves selected fields, but not `source_ref`, notes, optional evidence-detail references, or testimony-production kind. | Projection, not a Gap, capability, selection, or State. |
| Immediate potential consumer | `assemble_goal_advancement_demand_set`. | Optional `operational_realization` projection. | Preserves projection as a supplied family record; optionally detects goal/horizon identity mismatch. It does not reinterpret Demand. | Implemented/test-active assembler; no operational-realization supplied specimen. |
| Later consumer | None found. | `GoalAdvancementDemandSet`. | JSON conversion/display is possible; no route, ordering, sufficiency, authorization, or execution follows. | STOP. |

Package exports make both testimony records, the projection, and its projector
available to external callers. Export is not production. Likewise, the demand
set's four-family type inventory proves that operational realization is an
accepted family, not that an availability producer or a running caller exists.

There is no current connection to examination probe requests. The examination
request test expressly preserves a bound request without an operational-
realization handoff. Connecting these roads would be new architecture and is
outside this recovery.

## 3. Field-level standing and provenance audit

### 3.1 Requirement testimony

| Field | Vocabulary / default | Current production and provenance meaning | Used by Demand |
| --- | --- | --- | --- |
| `testimony_ref` | arbitrary `str` | Caller-declared occurrence identity; not resolved. | Included in item and projection-id payload. |
| `source_ref` | arbitrary `str` | Caller-declared source pointer; never checked, resolved, or preserved downstream. | No. |
| `goal_establishment_id` | arbitrary `str` | Must equal supplied goal identity. | Refusal/unclassified gate. |
| `horizon_id` | arbitrary `str` | Must equal supplied horizon identity. | Refusal/unclassified gate. |
| `evidence_ref` | arbitrary `str` | Must equal an `EvidenceSnapshotReference.evidence_ref` in the horizon. Contents, source, and support are not inspected. | Membership gate; copied into item. |
| `bounded_realization_component_ref` | nonempty `str` | Caller names the component/subject. | Nonempty gate and join key. |
| `required_transformation_ref` | nonempty `str` | Caller names transformation identity; no representation or semantics are resolved. | Nonempty gate and join key. |
| `applicable_scope_ref` | nonempty `str` | Caller names scope/locality; structure is not defined. | Nonempty gate and join key. |
| `owning_stage` | nonempty `str` | Caller declares responsibility. The value is not checked against an owner inventory. | Nonempty gate and exact join. |
| `requirement_standing` | `required`, `not_required`, `unknown`, `conflicting` | Caller conclusion. No rule derives it. | Primary Demand predicate. |
| `component_family` | defaults to `operational_realization_requirement` | Caller-overridable type label. | Exact family gate. |
| `component_bounded` | defaults `True` | Caller-overridable boundedness claim. | Truth/nonempty gate only. |
| `scope_applicability` | `applicable`, `outside_current_scope`, `unknown`, `conflicting`; defaults `applicable` | Caller conclusion, including a positive default. | Only `applicable` passes; otherwise unclassified. |
| `horizon_materiality` | `material`, `not_material`, `unknown`, `conflicting`; defaults `material` | Caller conclusion, including a positive default. | Only `material` passes; otherwise unclassified. |
| `notes` | tuple of strings; defaults empty | Unstructured caller context. | Ignored and dropped. |

### 3.2 Standing/availability testimony

| Field | Vocabulary / default | Current production and provenance meaning | Used by Demand |
| --- | --- | --- | --- |
| `testimony_ref`, `source_ref`, goal, horizon, evidence, component, transformation, scope, owner | same shapes as requirement | All caller-declared. `source_ref` remains unchecked; evidence gets reference membership only. | Same identity gates, except source is unused. |
| `availability_standing` | `available`, `unavailable`, `unknown`, `conflicting` | **Merely the availability label supplied by the caller.** No mechanism, occurrence, result, applicability, or time comparison produces it. | Primary Demand predicate. |
| `coverage_standing` | `complete_for_horizon`, `partial`, `unknown`, `conflicting` | Caller declares the completeness of the unavailable conclusion. No covered set or completeness evidence is represented. | Material only for `unavailable`; complete plus operational owner establishes Demand. |
| `blocker_family_ownership` | `operational_realization`, `authority`, `clarification`, `inquiry`, `generic`, `unknown`, `conflicting` | Caller declares which family owns the deficiency. No ownership comparison derives it. | Routes unavailable to established, Unknown, conflict, or unclassified-here. |
| family, boundedness, applicability, materiality | standing-family defaults; `True`; `applicable`; `material` | Positive caller-overridable defaults. | Exact pass/fail gates. |
| `candidate_existence_ref` | arbitrary `str`, defaults empty | Optional pointer only. | Ignored and dropped. |
| `reachability_ref` | arbitrary `str`, defaults empty | Optional pointer only. | Ignored and dropped. |
| `selection_ref`, `warrant_ref` | arbitrary `str`, default empty | Optional downstream-looking pointers. | Ignored and dropped. |
| `representation_applicability_ref` | arbitrary `str`, default empty | Optional applicability pointer. | Ignored and dropped. |
| `dependency_ref` | arbitrary `str`, default empty | Optional dependency pointer. | Ignored and dropped. |
| `behavior_support_ref` | arbitrary `str`, default empty | The only explicitly behavior-shaped pointer. It may be empty and is never resolved or compared. | Ignored and dropped. |
| `notes` | tuple of strings, defaults empty | Unstructured caller context. | Ignored and dropped. |

### 3.3 Projection preservation loss

The item preserves testimony references, the joined component/transformation/
scope/owner, the six standing dimensions, Demand conclusion, and evidence
references. It does not preserve either `source_ref`, notes, the standing's
optional realization/evidence pointers, whether a positive value was defaulted,
or whether availability was observed, derived, declared, copied, or compiled.
The projection-level `evidence_refs` is the horizon inventory, not proof of the
item's evidentiary support.

The join is also narrower than an adjudication. It selects `matches[0]` by
component, transformation, and scope. It does not detect multiple matching
standing testimonies or compare their availability values. A second matching
conflict can survive only as an unused standing later marked unclassified; it
does not make the joined Demand item conflicting. Testimony identity uniqueness
is not enforced, so repeated `testimony_ref` values can also distort the
`used` bookkeeping.

## 4. What the availability producer actually answers

There is no implemented producer, so the current road answers only the last
row below.

| Candidate meaning | Answered? | Reason |
| --- | --- | --- |
| Material exists | No | No material identity or observation is required. |
| Mechanism exists | No | `candidate_existence_ref` is optional and ignored. |
| Mechanism is reachable | No | `reachability_ref` is optional and ignored. |
| Transformation is demonstrated | No | No occurrence, operands, result, or comparison is represented. |
| Realization is applicable | Not evidentially | Scope applicability is a caller field/default, not an assessed relation. |
| Realization is currently available | Not evidentially | There is no described time, assessment time, expiry, or current horizon comparison. |
| Caller supplied this availability label | **Yes** | The dataclass accepts the enum and the projector branches on it. |

“Available” may be truthful testimony. The code does not prove it unsupported;
it simply does not preserve enough provenance to authorize reliance on it as
evidence-derived current availability.

## 5. Exact status meanings

### 5.1 Input standings

* `requirement_standing=required`: caller asserts the transformation is
  required. It is not derived from the goal or horizon.
* `not_required`: Demand is `unsupported`, regardless of availability.
* requirement `unknown` / `conflicting`: Demand remains `unknown` /
  `conflicting`.
* `availability_standing=available`: Demand is `unsupported` when requirement
  is required; this means only that the caller's positive availability
  testimony defeats this Demand classification.
* `unavailable`: may establish Demand only with
  `coverage_standing=complete_for_horizon` and
  `blocker_family_ownership=operational_realization`.
* availability `unknown` / `conflicting`: Demand remains `unknown` /
  `conflicting`.
* `complete_for_horizon`: caller asserts complete coverage; no coverage domain
  is enumerated. `partial` and `unknown` both lead to Demand `unknown` for an
  operational-realization-owned unavailability. `conflicting` leads to
  `conflicting`.
* ownership `authority`, `clarification`, `inquiry`, or `generic`: unavailable
  is `unclassified_here`. Ownership `unknown` is Demand `unknown`; ownership
  `conflicting` is Demand `conflicting`.
* non-applicable scope or non-material horizon, including their Unknown and
  conflict values, does not produce an Unknown/conflicting Demand item; it
  produces structurally `unclassified` with a coarse reason.

### 5.2 Output standings

* `established`: required + unavailable + complete-for-horizon + operational-
  realization ownership, after identity/gate checks. It establishes only this
  Demand classification, not a Gap or absence of competency.
* `unsupported`: either not required or caller-declared available. It means
  Demand is not supported by these supplied values, not that realization is
  proved available or transformation unnecessary universally.
* `unknown`: an input Unknown, or unavailable without complete operational-
   realization-owned coverage.
* `conflicting`: an explicit governing input conflict that reaches `_conclude`.
  It does not include independently detected contradictory testimonies.
* `unclassified_here`: unavailability is attributed to another known family.
* `unclassified`: testimony failed identity/family/boundedness/transformation/
  scope/owner/applicability/materiality/join gates or lacked its counterpart.
  The `unclassified_reason` records only the first failing reason.

Missing availability testimony therefore does **not** establish Demand or Gap.
A requirement without matching standing is `unclassified` with
`not_standing_component`. A standing without requirement is also unclassified.

## 6. Eight-dimensional fidelity audit

| Dimension | Required fidelity question | Current standing | Consequence |
| --- | --- | --- | --- |
| 1. Subject and occurrence | Which realization assessment occurrence concerns which subject/component? | Component reference exists; no availability-assessment occurrence, producer occurrence, or mechanism occurrence exists. | Cannot distinguish reassessment, copying, or repeated claims. |
| 2. Transformation identity | What exact input-to-output/result transformation is required and assessed? | One opaque `required_transformation_ref` must match exactly. No representations or transformation semantics are preserved. | Identity equality is possible; transformation demonstration is not. |
| 3. Locality and applicability | For which consumer, scope, environment, and dependency set does availability apply? | Opaque scope and caller/default applicability exist. No consumer identity, environment relation, or dependency comparison is required. | Cross-locality and cross-consumer reuse cannot be judged. |
| 4. Evidence and provenance | What observation/demonstration supports the standing and who produced it? | Opaque source/evidence refs; horizon membership only. Optional behavior/mechanism refs are ignored. | Truthful evidence-backed testimony and bare declaration are indistinguishable. |
| 5. Constraints and dependencies | Under what prerequisites and exclusions is realization available? | One optional ignored dependency ref; notes dropped. | Availability cannot be narrowed or refused by dependency mismatch. |
| 6. Authority and permitted reliance | Who may assert availability and what decision may rely on it? | Free-form owning stage; no producer authority or reliance warrant. Projection declares only its own negative authorities. | Caller controls a Demand predicate without an evidenced reliance boundary. |
| 7. Currentness and horizon | When was availability assessed, until when, and for which horizon? | Horizon identity/materiality and declared coverage exist; no observation time, assessed-at, expiry, freshness rule, or horizon comparison. | A stale historical success can be labelled currently available without detection. |
| 8. Conflict, counterevidence, Unknown, refusal | How are opposed testimony, failed occurrences, missing data, and refusals preserved? | Enum Unknown/conflict and structural unclassified exist; no multi-testimony conflict comparison or counterevidence relation. | Explicit labels survive; evidence-born conflict and refusal do not. |

Result: identity and classification fidelity are partial; evidentiary,
applicability, temporal, and conflict fidelity are insufficient for treating
the label as demonstrated current realization availability.

## 7. Asymmetric specimens

| Specimen | Current result | Faithful interpretation and STOP |
| --- | --- | --- |
| Caller says available with no performance evidence | `unsupported` Demand if all gates pass. | Preserve as positive caller testimony only. Do not infer competency, demonstrated occurrence, or current State. |
| Caller says unavailable while matching executable exists | Demand can be `established`; executable is invisible. | No contradiction is computed. File existence is neither availability nor competency. STOP before selection/invocation. |
| Executable exists but transformation undemonstrated | Same as caller's label. | Mechanism material does not demonstrate transformation. |
| One historical success now stale | Caller may label available; no temporal refusal occurs. | Historical demonstrated occurrence remains distinct from current availability. |
| Demonstration has different dependencies/locality | Caller may label available; dependency/locality compatibility is not compared. | Applicability remains unestablished for the present subject. |
| Conflicting availability testimony | If one record itself says `conflicting`, Demand conflicts. Two opposing matching records are not cross-compared; first wins. | Preserve both as testimony; current projection cannot adjudicate their conflict. |
| Missing availability testimony | Requirement is unclassified. | Neither Gap nor Demand is established. |
| Available for consumer A, inapplicable to B | Consumer identity is absent and scope is opaque. | No lawful transfer to B; caller must supply a separately scoped conclusion. |
| Required transformation has no named mechanism | Demand outcome still follows availability label; mechanism identity is not required. | A required transformation plus absent mechanism does not itself prove unavailability under current rules. |

Across all specimens: testimony is not observation; observation is not a
demonstrated occurrence; demonstration is not applicability; applicability is
not current availability; availability is not competency; none alone is a Gap;
Gap is not Demand; Demand is not selection; selection is not authorization;
authorization is not invocation; invocation is not successful realization.

## 8. Consumer-local P/E/S/C derivation

An active classifier genuinely relies on realization availability: `_conclude`
uses it to establish or refuse `OperationalRealizationDemand`. The following is
therefore its **local current contract**, not a generic PESC owner and not a
competency schema.

* **P — representation required:** one matching requirement testimony and one
  standing testimony, the exact goal and horizon artifacts, and the horizon's
  evidence-reference inventory. Required fields are component, transformation,
  applicable scope, owning stage, requirement, availability, coverage,
  blocker-family ownership, applicability, and materiality standings. The
  current representation is adequate to compare testimony; it is inadequate
  to assess evidence-derived availability.
* **E — comparison:** exact goal/horizon/evidence-membership/family/boundedness
  gates; nonempty component/transformation/scope/owner; exact component,
  transformation, scope, and owner joins; then the literal `_conclude` truth
  table. No behavioral, dependency, authority, currentness, or counterevidence
  compatibility rule exists.
* **S — scope:** one goal establishment, one bounded advancement horizon, one
  caller-named bounded realization component and required transformation, one
  caller-named scope and owning stage. Occurrence, concrete locality,
  dependency, consumer, and temporal assessment scope are absent rather than
  implicit.
* **C — conclusion and constrained decision:** classify only whether an
  operational-realization Demand is established, unsupported, Unknown,
  conflicting, owned elsewhere, or structurally unclassified. The conclusion
  may be preserved as an unordered demand-family projection. It constrains no
  realization selection, warrant, authorization, invocation, recording, or
  mutation.

The missing evidence crossing must not start from packages, executable paths,
byte recurrence, or compiled capability labels. If a responsible consumer is
later established, its availability representation and comparison must be
derived from the exact realization decision and accepted evidence strength.

## 9. Missing boundary, implementation judgment, and STOP conditions

### 9.1 Smallest missing boundary

The smallest missing boundary is **a responsible, consumer-local producer (or
an explicit preservation boundary) for availability standing**:

1. name the exact consumer decision for which availability matters;
2. name subject, transformation, occurrence, locality, dependencies, and time;
3. preserve whether the conclusion is declared, copied, observed, derived, or
   compiled;
4. relate evidence and counterevidence to that conclusion under an explicit
   comparison/compatibility rule; and
5. grant only the reliance needed to classify that consumer's Demand.

If the repository intends this input to remain declaration-only, the even
smaller correction is a preservation boundary that says so and prevents
`availability_standing` from being read as evidence-derived current State.
Neither boundary requires a capability registry, competency schema, selector,
execution road, or examination-probe connection.

### 9.2 Is this the missing active competency-evidence consumer crossing?

**It is the active missing crossing location, not the completed crossing.** An
implemented Demand predicate consumes a transformation identity and relies on
availability. That makes this the closest active consumer-local place where
demonstrated realization evidence could become material. Today, however, the
consumer relies only on explicit testimony. It asks neither “was T
demonstrated?” nor “is that demonstration applicable/current here?” Therefore
it is not currently a competency-evidence consumer, and availability must not
be renamed or promoted to competency.

### 9.3 Implementation judgment

**No implementation slice is warranted by current evidence.** There is no
production producer/caller occurrence, no established owner of an availability
assessment, no declared accepted evidence strength, and no active downstream
decision beyond preserving Demand. Implementing a producer, comparer, or
schema now would invent responsibility. A later slice becomes warranted only
after an active consumer explicitly owns an evidence-derived availability
question and specifies the decision/refusal it constrains. If maintainers
instead establish that the contract is intentionally declaration-only, a
small naming/preservation correction may then be warranted, separately tested.

### 9.4 Explicit STOP conditions

STOP this recovery now because the topology, reliance, and loss are identified.
For any future road, STOP and preserve Unknown/refusal when:

* no responsible availability producer or exact consumer is named;
* requirement or standing testimony is missing or identity-incompatible;
* transformation, subject, locality, dependency, occurrence, or temporal scope
  required by the consumer is absent;
* evidence provenance, comparison rule, authority, or permitted reliance is
  absent;
* evidence is stale, inapplicable, conflicting, counterevidenced, or merely
  asserts mechanism/material existence when demonstrated realization is
  required;
* testimony kind (declared/copied/observed/derived/compiled) cannot be
  distinguished and the consumer requires evidence-derived availability;
* Demand is classified: STOP before Gap, competency, selection, authorization,
  invocation, execution, recording, persistence, event emission, or mutation;
* anyone proposes connecting this road to examination probe requests without
  a separately evidenced consumer and responsibility.

## 10. Files inspected and report LOC

Exact repository files inspected for this recovery:

* `AGENTS.md`
* `seed_runtime/operational_realization_demand_projection.py`
* `seed_runtime/goal_advancement_demand_set.py`
* `seed_runtime/bounded_advancement_horizon.py`
* `seed_runtime/__init__.py`
* `tests/test_operational_realization_demand_projection.py`
* `tests/test_goal_advancement_demand_set.py`
* `tests/test_examination_probe_request.py`
* `competency_evidence_consumer_first_recovery_001.md` (prior report used only
  as navigation/counterevidence)

Repository-wide `rg` searches over `seed_runtime` and `tests` established the
producer/caller inventory; focused `git log`, `git show`, and `git blame` checks
confirmed the current post-PR-2016 boundary and history of the renamed Demand
surface. Only this new report was added. Report LOC added: **357** (as measured
after creation with `wc -l`).
