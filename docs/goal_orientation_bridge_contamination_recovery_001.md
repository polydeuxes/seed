# Goal Orientation Bridge Contamination Recovery 001

## Governing question

Do `GoalOrientationInventory`, its six goal dimensions, `GoalConsiderationCandidateTestimony`, and `GoalConsiderationCandidateResolution` perform any independently warranted Seed responsibility between `BoundedOperatorGoalEstablishment` and `BoundedAdvancementHorizon`, or are they foreign orientation/LLM-era compatibility scaffolding that merely reclassifies and re-attests an already-established goal?

## Central finding

The inspected bridge does not currently show an independently warranted Seed responsibility between bounded-goal establishment and horizon construction. It is runtime-constructible, publicly exported, and test-covered, but the live implemented acts are: caller-supplied category association, read-only inventory bucketing, caller-supplied identity testimony, and exact identity comparison against visible inventory records. The six goal dimensions are not recovered as Seed constitutional dimensions; they stand as caller-facing orientation/presentation buckets of unknown origin. The horizon consumes the bridge's resolved identity and resolution id because its type contract requires them, not because horizon construction uses the six category meanings, inventory topology, association standing, testimony provenance, or multiple-goal ambiguity semantics.

District-level disposition: **delete as one district**, if contamination is accepted, with protected boundary excluding bounded-goal establishment, present movement boundary and horizon construction, need-family projection, and inquiry/frontier responsibilities.

## 1. Exact bridge topology

Current constructible road:

```text
BoundedOperatorGoalEstablishment
→ association_from_bounded_goal(...)
→ GoalOrientationAssociation
→ build_goal_orientation_inventory(...)
→ GoalOrientationInventory.dimensions[*].bounded_goals
→ visible_bounded_goal_candidates(...)
→ GoalConsiderationCandidateTestimony
→ resolve_goal_consideration_candidate(...)
→ GoalConsiderationCandidateResolution
→ establish_bounded_advancement_horizon(...)
→ BoundedAdvancementHorizon
```

The road is not evidenced as an automatic runtime pipeline. Searches recovered direct production in tests and downstream projection test helpers; exports make it publicly constructible. No inspected CLI path or event/persistence road actively emits the bridge.

## 2. Direct producer → artifact → consumer evidence

| Crossing | Exact producer | Source standing | Evidence or warrant | Artifact/relation | Consumer | Identity/provenance preserved or lost | Authority and negative authority | Standing |
|---|---|---|---|---|---|---|---|---|
| bounded goal → association | `association_from_bounded_goal(goal, dimension_refs=..., source_ref=...)` | established/provisional/refused bounded-goal object plus caller-supplied dimensions | Copies goal id, ingress/source ref, intended outcome label, and conflicts; does not derive dimensions | `GoalOrientationAssociation` | `build_goal_orientation_inventory` | Preserves `goal_establishment_id` as `artifact_ref`; preserves source ref; loses establishment state, scope, sufficiency, ingress lineage, acceptance provenance except through source ref | Association docstring says explicit inventory evidence; boundary notes deny inference from wording | constructible/test-active |
| association → inventory | `build_goal_orientation_inventory` | supplied association iterable | Buckets by supported dimension strings; sends no dimension to unknown; unsupported to unmatched; conflicts to conflicting | `GoalOrientationInventory` and `GoalOrientationDimensionEntry`/views | `visible_bounded_goal_candidates`; JSON formatter; tests | Preserves artifact ref, source ref, association state, label, conflict refs; does not preserve full source artifact | Read-only; not registry/planner/queue/priority; no activation, movement, authority, recording, ledger, mutation | constructible/test-active |
| inventory → visible candidates | `visible_bounded_goal_candidates` | inventory dimensions | Flattens `dimension.bounded_goals` with `artifact_kind == "bounded_goal"` | tuple of `GoalOrientationArtifactView` | `goal_consideration_candidate_set_id`; `resolve_goal_consideration_candidate` | Preserves only view fields; duplicate goal ids can remain ambiguous | Visibility is not selection or focus | constructible/test-active |
| inventory + testimony → resolution | `resolve_goal_consideration_candidate` | caller-supplied testimony plus visible candidate set | Handles no testimony, missing/unknown, ambiguous, conflict, exact mismatch, duplicate visible matches | `GoalConsiderationCandidateResolution` | `establish_bounded_advancement_horizon`; need projection producers receive it as context | Preserves candidate set hash, testimony/source refs, resolved goal id/source, visible candidates, unknowns/conflicts; no full goal lineage | Boundary notes deny selection, focus, priority, advancement, inquiry applicability, need classification, recording, mutation | constructible/test-active |
| resolution + bounded goal + boundary → horizon | `establish_bounded_advancement_horizon` | resolved candidate identity plus full bounded-goal artifact plus caller-supplied movement boundary | Requires resolution state `resolved`, matching goal id, non-refused goal, present boundary, and reasons for excluded need families | `BoundedAdvancementHorizon` | downstream need projections and frontier road | Reintroduces full goal ingress lineage from `BoundedOperatorGoalEstablishment`; preserves candidate resolution id and resolved source ref | Explicitly denies goal selection, constitutional focus, priority, need classification, inquiry opening, authorization, execution, recording, mutation | constructible/test-active; downstream projections tested |

## 3. Origin and standing of the six goal dimensions

The six strings are declared only as `SUPPORTED_GOAL_DIMENSIONS`:

```text
operator_interaction
operational_continuity
resource_stewardship
capability_recovery
knowledge_quality
implementation_maintenance
```

Recovered standing:

| Six-label value | Current producer of value | Current derivation from constitutional evidence? | Downstream consumer of meaning? | Classification |
|---|---|---:|---:|---|
| `operator_interaction` | constant and test/caller literals | No | No; bucket membership only | arbitrary caller bucket / orientation label |
| `operational_continuity` | constant and test/caller literals | No | No; bucket membership only | arbitrary caller bucket / orientation label |
| `resource_stewardship` | constant and test/caller literals | No | No; bucket membership only | arbitrary caller bucket / orientation label |
| `capability_recovery` | constant and test/caller literals | No | No; bucket membership only | arbitrary caller bucket / orientation label |
| `knowledge_quality` | constant and frequent test/caller literal | No | No; bucket membership only | arbitrary caller bucket / orientation label |
| `implementation_maintenance` | constant and test/caller literals | No | No; bucket membership only | arbitrary caller bucket / orientation label |

No current producer derives these labels from constitutional evidence. `association_from_bounded_goal` explicitly accepts caller-supplied `dimension_refs`; `build_goal_orientation_inventory` only validates those refs against the supported tuple. Downstream candidate resolution flattens visible bounded goals and ignores the dimension labels themselves. Horizon construction never imports or reads `SUPPORTED_GOAL_DIMENSIONS`.

## 4. Comparison with the established eight constitutional dimensions

The Book's recovered eight macro-dimensional families are:

1. subject / identity;
2. assertion / content;
3. standing;
4. source / provenance;
5. responsibility;
6. authority / warrant;
7. scope / locality;
8. occurrence / preservation.

The Book explicitly says these characterize exact subjects and relations and do not classify all families. The six goal-orientation labels do not map onto this grammar. They are topics or buckets such as operator interaction, continuity, resources, capability, knowledge quality, and implementation maintenance. Some may evoke localities or operational concerns, but matching the word `dimension` is not evidence of equivalence. Current code does not bind any of the six labels to subject identity, assertion content, standing, provenance, responsibility, authority/warrant, scope/locality, or occurrence/preservation.

## 5. Exact act performed by association, inventory, testimony, and resolution

| Stage | Exact act | Not performed | Classification |
|---|---|---|---|
| `GoalOrientationAssociation` | Stores caller-supplied artifact kind/ref/source, dimension refs, association state, label, conflict refs | Does not establish goal, select goal, prove category, derive dimension, preserve full bounded-goal lineage, open inquiry, authorize, mutate | compatibility-only / foreign taxonomy |
| `GoalOrientationInventory` | Buckets supplied associations into supported dimensions; preserves unknown/unmatched/conflicting material and read-only negative flags | Does not select, prioritize, schedule, activate, establish focus, classify need, move inquiry, mutate, write ledger | compatibility-only / foreign taxonomy |
| `GoalConsiderationCandidateTestimony` | Stores attributed caller testimony naming or failing to name candidate goal identity | Does not originate from an inspected Seed selection producer; does not itself select or bind subject for horizon | duplicated / compatibility-only |
| `GoalConsiderationCandidateResolution` | Compares testimony against visible bounded-goal views and returns resolved/missing/ambiguous/conflict/mismatch states | Does not select goal, establish focus, establish priority, classify advancement needs, require/open inquiry, authorize, mutate | duplicated identity confirmation / compatibility-only |

## 6. Selection and focus findings

Required distinctions recovered:

```text
goal established != goal associated with a category
goal associated != goal visible
goal visible != goal nominated
goal nominated != identity resolved
identity resolved != goal selected
goal selected != focus established
focus established != horizon bounded
horizon bounded != inquiry opened
```

The district contains real implementation acts for association, visibility, nomination storage, and identity resolution. It does **not** contain a real act of goal selection or focus establishment. Both `GoalConsiderationCandidateResolution` and `BoundedAdvancementHorizon` carry `selects_goal=False` and `establishes_focus=False`. Horizon construction bounds a supplied movement boundary for a matching resolved goal identity; it does not produce constitutional focus or select the goal.

Recovered act classification:

| Claimed act | Present in district? | Producer/warrant/consumer evidence | Classification |
|---|---:|---|---|
| subject binding | Partial only as exact id comparison | resolution matches one visible `artifact_ref`; horizon checks same id against full goal | duplicated / compatibility-only |
| goal selection | No | explicit negative fields and boundary notes | absent |
| focus establishment | No | explicit negative fields and boundary notes | absent |
| ambiguity preservation | Yes, local | resolution can report ambiguous testimony or duplicate visible matches | compressed but constructible-only |
| multiple-goal disambiguation | No as constitutional act | exact testimony must already name one id; resolver only compares | absent / compatibility-only |
| scope characterization | No | scope carried by goal/horizon inputs, not inventory/resolution | absent in bridge |
| priority | No | explicit negative flags | absent |
| visibility | Yes | inventory buckets and visible candidate flattening | compatibility-only |
| presentation | Yes, via JSON/exportable views | formatters/export only | compatibility-only |
| inventory | Yes | read-only bucketing of supplied associations | compatibility-only / foreign taxonomy |

## 7. Re-attestation problem

The current road requires an already-established bounded goal to be made visible through caller-supplied category association, then separately named by caller-supplied testimony, then resolved back to the same goal identity. This is not recovered as necessary independent testimony. It is not a genuine multiple-goal ambiguity boundary because ambiguity is only represented after a caller supplies ambiguous testimony or duplicate visible rows; no Seed producer selects among multiple established goals. It is not exact subject binding for the horizon in a constitutional sense because `BoundedOperatorGoalEstablishment` already preserves goal identity and horizon receives the full goal artifact and checks identity.

Classification: **foreign compatibility ceremony with duplicated identity confirmation**, with a small compressed ambiguity/mismatch guard that is constructible but not independently warranted as this bridge.

## 8. Horizon's real dependency on the bridge

`establish_bounded_advancement_horizon(...)` consumes these fields from `GoalConsiderationCandidateResolution`:

- `resolution_state` and `resolved_goal_establishment_id` to refuse unresolved candidates;
- `resolved_goal_establishment_id` to compare with `goal.goal_establishment_id`;
- `resolution_id` for `candidate_resolution_id` and horizon identity payload;
- `resolved_goal_source_ref` for horizon source field and payload;
- `unknowns` and `conflicts` for horizon preserved unknown/conflict fields.

It does not consume:

- six goal-category meanings;
- inventory dimension structure;
- association standing beyond the already-materialized source/id in the resolution;
- testimony provenance except as resolution payload fields already stored;
- multiple-goal ambiguity except through the coarse non-`resolved` refusal state;
- inventory candidate set id for horizon logic;
- labels/topic similarity.

Horizon dependency classification: **type-contract dependency on compatibility fields**, not constitutional dependency on the whole bridge. The horizon's independent responsibility is preserving a caller-supplied present movement boundary for one bounded goal whose identity matches the supplied bounded-goal artifact and is not refused.

## 9. Runtime versus constructible/test-only standing

| Surface | Public export | Tests | Non-test runtime/CLI producer found | Formatter | Standing |
|---|---:|---:|---:|---:|---|
| `GoalOrientationAssociation` | Yes | Yes | No | through inventory JSON | constructible/test-active |
| `GoalOrientationArtifactView` | Yes | Yes | No | yes | constructible/test-active |
| `GoalOrientationDimensionEntry` | Yes | Yes | No | yes | constructible/test-active |
| `GoalOrientationInventory` | Yes | Yes | No | `goal_orientation_inventory_json` | constructible/test-active |
| `SUPPORTED_GOAL_DIMENSIONS` | Yes | Yes | No producer; constant only | n/a | public vocabulary constant |
| `GoalConsiderationCandidateTestimony` | Yes | Yes | No | through resolution JSON | constructible/test-active |
| `GoalConsiderationCandidateResolution` | Yes | Yes | Horizon/projection tests consume; no CLI/event road found | `goal_consideration_candidate_resolution_json` | constructible/test-active |
| `visible_bounded_goal_candidates` | Yes | Yes | No CLI/event road found | n/a | constructible/test helper/API |
| `goal_consideration_candidate_set_id` | Yes | Yes | No CLI/event road found | n/a | compatibility identity helper |
| `association_from_bounded_goal` | Yes | Yes | No automatic producer found | n/a | convenience constructor |
| `build_goal_orientation_inventory` | Yes | Yes | No automatic producer found | n/a | convenience builder |
| `resolve_goal_consideration_candidate` | Yes | Yes | No automatic producer found | n/a | compatibility resolver |

## 10. Independent-warrant matrix

| Artifact/responsibility | Classification | Rationale |
|---|---|---|
| `GoalOrientationAssociation` | foreign taxonomy / compatibility-only | Caller-supplied category association with no producer-derived constitutional warrant. |
| `GoalOrientationArtifactView` | compatibility-only | View projection of association fields; loses full bounded-goal standing. |
| `GoalOrientationDimensionEntry` | foreign taxonomy | Buckets arbitrary six-label dimensions; not constitutional eight-dimensional characterization. |
| `GoalOrientationInventory` | compatibility-only / foreign taxonomy | Read-only bucketing and visibility, not selection, focus, priority, or horizon requirement. |
| `SUPPORTED_GOAL_DIMENSIONS` | foreign taxonomy | Six labels have no recovered constitutional origin or semantic consumer. |
| `GoalConsiderationCandidateTestimony` | duplicated / compatibility-only | Caller-supplied re-naming of an already established goal identity; no producer recovered. |
| `GoalConsiderationCandidateResolution` | duplicated / compatibility-only | Resolves identity already preserved by goal establishment and rechecked by horizon. |
| visible candidate set identity | compatibility-only | Stable hash for visible views; not a Seed selection/focus act. |
| unknown/unmatched/conflicting inventory material | compressed | Real preservation behavior, but local to foreign inventory taxonomy and not enough to warrant district. |
| ambiguity/conflict/mismatch resolution states | compressed | Real guard behavior, but no independent selector/focus producer or semantic consumer beyond horizon refusal. |
| horizon matching of resolved id to goal id | independently warranted in horizon | Horizon must bind supplied movement boundary to the supplied goal identity; it does not require this bridge's taxonomy. |

## 11. Protected neighboring responsibilities

This operation does not question, delete, or redesign:

- attributed operator material;
- consumer-local interpretation admission;
- `BoundedOperatorGoalEstablishment`;
- goal identity and ingress lineage;
- present movement boundary;
- `BoundedAdvancementHorizon`;
- `InquiryNeedProjection`;
- Demand / NeedFamily distinctions;
- need selection;
- `InquiryFrontierBoundaryTestimony`;
- `BoundedInquiryFrontier`.

## 12. Exact deletion district if contamination is established

If deletion is later implemented, the deletion district would be exactly the bridge artifacts and their direct tests/exports/formatters/callers:

```text
seed_runtime/goal_orientation_inventory.py
seed_runtime/goal_consideration_candidate_resolution.py
exports of their public names from seed_runtime/__init__.py
formatters: goal_orientation_inventory_json, goal_consideration_candidate_resolution_json
direct tests: tests/test_goal_orientation_inventory.py, tests/test_goal_consideration_candidate_resolution.py
bridge construction in horizon/projection tests that exists only to satisfy candidate-resolution type contract
Book/report references that assert this district as warranted authority rather than historical testimony
```

Protected from that district: bounded-goal establishment, horizon construction responsibility, need-family projections, inquiry/frontier construction, and any existing separate selector/focus owner not inspected as part of this named bridge.

## 13. Strongest Unknowns

1. Whether PR 1946 introduced any external non-repository authority for the six labels; this report treats it as immutable testimony, not authority.
2. Whether an out-of-repo or downstream package uses the public exports semantically; repository search cannot prove external absence.
3. Whether older reports intentionally used the six labels as a temporary presentation vocabulary only; their presence does not create implementation warrant.
4. Whether the compressed ambiguity/mismatch guard should survive elsewhere is out of scope; no replacement producer is proposed here.
5. Whether a separate current goal-selection/focus producer exists outside this exact bridge. This report did not promote any replacement architecture.

## 14. Smallest next operation

Perform a deletion-readiness impact census limited to direct imports, direct tests, public exports, and Book/report assertions for this exact bridge. The census should not design replacement architecture and should preserve the protected neighboring responsibilities listed above.

## Checks performed

- `find .. -name AGENTS.md -print`
- `git status --short`
- `git branch --show-current`
- `cat AGENTS.md`
- `rg -n "GoalOrientationAssociation|GoalOrientationArtifactView|GoalOrientationDimensionEntry|GoalOrientationInventory|SUPPORTED_GOAL_DIMENSIONS|GoalConsiderationCandidateTestimony|GoalConsiderationCandidateResolution|visible_bounded_goal_candidates|goal_consideration_candidate_set_id|association_from_bounded_goal|build_goal_orientation_inventory|resolve_goal_consideration_candidate|constitutional dimension|constitutional dimensions|operator_interaction|operational_continuity|resource_stewardship|capability_recovery|knowledge_quality|implementation_maintenance" .`
- `sed -n '1,240p' seed_runtime/goal_orientation_inventory.py`
- `sed -n '1,260p' seed_runtime/goal_consideration_candidate_resolution.py`
- `sed -n '1,220p' seed_runtime/bounded_operator_goal_establishment.py`
- `sed -n '1,260p' seed_runtime/bounded_advancement_horizon.py`
- `sed -n '260,520p' seed_runtime/bounded_advancement_horizon.py`
- `sed -n '1,220p' seed_runtime/__init__.py`
- `rg -n "from seed_runtime.goal_orientation_inventory|goal_orientation_inventory|goal_consideration_candidate|GoalConsiderationCandidateResolution|GoalOrientationInventory" seed_runtime tests book_of_seed docs *.md --glob '!docs/goal_orientation_bridge_contamination_recovery_001.md'`
- `rg -n "eight constitutional|constitutional dimensions|Representation|Occurrence|Assertion|Authority|Provenance|Unknown|Refusal|Consumer|Selection|Time" book_of_seed docs *.md seed_runtime | head -200`
- `rg -n "identity, provenance, authority, scope|constitutional requirements|eight" book_of_seed docs *.md | head -100`
- `sed -n '70,100p' book_of_seed/constitutional_family_topology_orientation_001.md`
- `sed -n '616,628p' book_of_seed/repository_constitutional_dimensionality_survey_011.md`
- `nl -ba seed_runtime/goal_orientation_inventory.py | sed -n '1,210p'`
- `nl -ba seed_runtime/goal_consideration_candidate_resolution.py | sed -n '1,260p'`
- `nl -ba seed_runtime/bounded_advancement_horizon.py | sed -n '1,280p'`
- `nl -ba seed_runtime/bounded_operator_goal_establishment.py | sed -n '1,120p'`
- `nl -ba book_of_seed/constitutional_family_topology_orientation_001.md | sed -n '74,92p'`
- `nl -ba seed_runtime/__init__.py | sed -n '160,264p'`
