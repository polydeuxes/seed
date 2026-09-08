# Exact operator-material shared ownership and interpretation-district boundary recovery 001

## 1. Governing answer and bounded recovery

This report inspects merged `main` at `a7cfe56` (PR 2153) and makes no
implementation change. The current topology answers the governing question as
follows:

* **The live owner of exact operator material and source addressability is the
  operator-ingress addressable-material responsibility.** It alone constructs the
  production values, establishes their identities, verifies their recorded ingress
  lineage, validates their full-span coordinates, serializes/reconstructs them, and
  places them in the live operator-ingress projected view.
* `SourceSpan` and `ExactOperatorMaterial` are nevertheless *defined* in
  `contextual_interpretation_warrant_set.py`. That file originally introduced them
  together with the warrant model; the live addressability implementation was added
  later. Current topology therefore shows **historical co-location in a mixed-
  responsibility module**, not faithful present ownership.
* The live dependency points from
  `operator_ingress_addressable_material` **into**
  `contextual_interpretation_warrant_set` for those two value shapes and the latter's
  error class. The semantic direction is the reverse: contextual warrant accepts
  exact material formed elsewhere. The Python direction is therefore a dependency
  inversion and is not constitutionally faithful.
* Only `SourceSpan` and `ExactOperatorMaterial` cross from that file into the live
  road. Every candidate, correction, evidence, warrant, selection, applicability,
  admission, admitted-interpretation goal, and horizon artifact is confined to the
  externally demandless constructible district (or its tests/exports).

The smallest coherent retention boundary is the recorded-ingress-to-addressable-
material projection, including these two shapes. The smallest coherent deletion
boundary is the whole warrant-to-horizon district, but deleting it now while leaving
the shapes in place would strand a module named for a responsibility it no longer
contained. The smallest lawful next action is therefore one **relocation-only PR**:
move exactly `SourceSpan` and `ExactOperatorMaterial` to their existing live owner,
reverse the warrant module's import, update affected imports/tests, and change no
behavior. A later, independently reviewed PR can delete the demandless district.

## 2. Method and current-topology limits

The recovery used current Python definitions, imports, constructors, projection
wiring, serializers, package exports, CLI entry wiring, dedicated tests, and active
Book/documentation searches. Repository-wide searches found no non-test constructor
of an interpretation candidate or warrant input, no non-test invocation of any
warrant-to-horizon producer, and no non-test terminal consumer. History was consulted
only to explain location: PR 2054 introduced all warrant-file shapes together; PR
2111 later made the separate live addressable-material owner import the two shapes.
That sequence is locator/testimony, while the ownership judgment below rests on
current producers and consumers.

“Non-test consumer” below excludes annotations or a type's own producer. “Independent
demand” requires an actual current entrance or terminal responsibility, not import,
construction capability, freezing, hashing, serialization, package export, or test
coverage.

## 3. Recovery A — complete shared-type inventory

Every class defined by `contextual_interpretation_warrant_set.py` is included.

| Type | Current defining module | Current non-test constructors | Current non-test consumers | Live road use | Interpretation-district use | Independent demand | Shared or exclusive |
|---|---|---|---|---|---|---|---|
| `ContextualInterpretationWarrantSetError` | contextual warrant | none explicitly; raised by warrant-file value validation | addressable deserializer catches it; warrant producer callers would receive it | accidental validation/error dependency | warrant validation | live code needs an error boundary, but not this responsibility-named class | co-located support; not a shared constitutional artifact |
| `SourceSpan` | contextual warrant | addressable formation; addressable JSON reconstruction | nested validation/projection; warrant producer and later snapshots | canonical full ingress span | candidate source and residual spans | **yes**, as live source-addressability shape | **shared live type, misowned** |
| `ExactOperatorMaterial` | contextual warrant | addressable formation; addressable JSON reconstruction | addressable artifact/projection; warrant and selection carriage | exact decoded ingress plus span/provenance | warrant input and selection result field | **yes**, as live exact-material shape | **shared live type, misowned** |
| `InterpretationCandidate` | contextual warrant | no non-test constructor | warrant producer only | none | proposes caller-authored label/meaning and span refs | no | demandless district type, exclusive |
| `CorrectionCandidate` | contextual warrant | no non-test constructor; warrant producer constructs none | warrant producer and `CandidateWarrant` | none | caller-authored proposed correction | no | demandless district type, exclusive |
| `RetrospectiveEvidence` | contextual warrant | no non-test constructor | warrant producer and `CandidateWarrant` | none | caller-authored disposition/material/rationale | no | demandless district type, exclusive |
| `ClarificationEvidence` | contextual warrant | no non-test constructor | warrant producer and `CandidateWarrant` | none | caller-authored candidate-local clarification | no | demandless district type, exclusive |
| `CandidateWarrant` | contextual warrant | warrant producer only | warrant set and contextual selection | none | candidate-scoped aggregation and standing | no external entrance; internally consumed only | demandless district type, exclusive |
| `ContextualInterpretationWarrantSet` | contextual warrant | warrant producer only | contextual selection | none (the live addressable module imports the error name, not this artifact) | warrant-to-selection handoff | no external entrance | demandless district type, exclusive |

Thus, co-location is not joint ownership. `ExactOperatorMaterial` is used both by a
live road and a demandless chain, but the chain's use does not independently demand
it. Conversely, nested use by the live projection *does* rely on the exact-content
and source-addressing responsibility: identities and invariants are computed over
and validated against those values. The shared seam extends no farther than
`SourceSpan` and `ExactOperatorMaterial`.

## 4. Recovery B — the complete live exact-material road

| Stage | Producer | Input artifact | Output artifact | Occurrence standing | Persistence standing | Consumer | Responsibility owned |
|---|---|---|---|---|---|---|---|
| captured representation | `capture_stdin_material` called by the persistent console | process input bytes | `CapturedOperatorMaterial` | process-local capture | not durable by itself | `run_operator_ingress_attempt` | boundary byte capture |
| raw-material occurrence | `_capture_representation` / `_record` | captured bytes and capture testimony | `operator.ingress.raw_material_captured` Event | **recorded** occurrence | Event ledger (memory or SQLite) | representation examination and state projection | exact raw occurrence preservation |
| representation examination | `examine_text_representation`, then `_record` | captured material/raw-event lineage | examination result and `operator.ingress.representation_examined` Event | decoder examination **recorded** | Event ledger | ingress occurrence producer and projection | representation availability evidence, not meaning |
| ingress occurrence | `run_operator_ingress_attempt` / `_record` | decoded representation plus raw/examination ids | `operator.ingress.ingress_occurred` Event with `decoded_text` | **recorded** decoded ingress; meaning Unknown | Event ledger | state projector/addressable formation | operator ingress occurrence |
| addressable-material formation | `form_operator_ingress_addressable_material` | supplied ingress Event plus ledger verification of all three Events | `SourceSpan`, `ExactOperatorMaterial`, `OperatorIngressAddressableMaterial` | **projected/reconstructed**, not a new Event | deterministic view value; no ledger write | operator-ingress projector | exact content preservation and source addressability |
| operator-ingress projection | `project_operator_ingress_events` during `StateProjector.project` | recorded ingress Event and ledger | nested JSON-safe `addressable_operator_material` in attempt view | projected current view | replay-reconstructible; view itself is not a separately recorded occurrence | returned attempt view, tests, and any caller of projected state | read-only ingress visibility |
| current renderer/consumer | console invokes the attempt and returns no renderer for this field | projected attempt dictionary | no dedicated human/CLI rendering | no additional standing | none | programmatic caller only | none beyond projection availability |

The console in `scripts/seed_local.py` is the current non-test entrance: it captures
stdin and calls `run_operator_ingress_attempt`. `StateProjector` dispatches every
operator-ingress Event back through `project_operator_ingress_events`, so in-memory
and SQLite replay reconstruct the same addressable value.

### Exact answers about formation

1. Production constructs each `SourceSpan` only in
   `form_operator_ingress_addressable_material`; `from_json_dict` reconstructs the
   same projected value rather than originating a new occurrence.
2. The same two paths construct `ExactOperatorMaterial`: formation originates it,
   deserialization reconstructs it.
3. Formation requires the exact supplied ingress Event to equal `ledger.get(id)`,
   and verifies the linked raw and successful representation-examination Events.
4. The full-span identity is a SHA-256-based stable id over `(ingress_event_ref,
   exact_text)`. `source_ref`, offsets `(0, len(exact_text))`, and duplicated span
   text are validated against the material and ingress identity. Formation reads
   `decoded_text` from the verified Event. Validation without the ledger proves
   only internal canonical consistency; it cannot re-verify the Event content.
5. They are frozen reconstructed value objects inside a deterministic projection,
   not durable Events. Their source Events are durable; replay deterministically
   recreates them.
6. The enclosing addressable artifact validates and serializes them, and the
   operator-ingress projected view exposes them. Contextual warrant/selection can
   consume them only when an absent external caller supplies the chain.
7. Yes. `to_json_dict` uses `asdict`; the projected view contains every nested field
   and span coordinate.
8. No other live responsibility uses them. The interpretation modules are
   constructible and internally connected but have no current non-test entrance.
9. Yes. Deleting the warrant module today would break the live ingress import solely
   because `SourceSpan`, `ExactOperatorMaterial`, and the caught responsibility-
   named error are located there—not because live ingress invokes contextual warrant.

## 5. Recovery C — intrinsic exact-material responsibility

The best classification is **operator-ingress exact content preservation plus source
addressability**. It supports later examination or interpretation without asserting
either. It is not contextual-interpretation support as an owning responsibility, is
not general evidence addressing, and is not mixed at the shape level.

### `SourceSpan` fields

| Field | Current owner of value | Purpose and standing |
|---|---|---|
| `span_ref` | addressable-material owner | repository convention: deterministic identity over ingress Event id and exact text; derived, not observed |
| `source_ref` | addressable-material owner from recorded Event id | identifies the recorded ingress occurrence; derived from recorded evidence |
| `start` | addressable-material owner | canonical interpreted coordinate `0`, not observed metadata |
| `end` | addressable-material owner | canonical Python string length of decoded text; derived convention, not raw-byte offset |
| `exact_text` | copied from recorded ingress `decoded_text` | preserves the exact substring covered; observed only after decoder examination, then recorded |

### `ExactOperatorMaterial` fields

| Field | Current owner of value | Purpose and standing |
|---|---|---|
| `material_ref` | addressable-material owner from ingress Event id | binds material identity to the recorded ingress occurrence |
| `exact_text` | copied from recorded ingress `decoded_text` | exact decoded representation including delimiter; not the trimmed dimensional content |
| `source_spans` | addressable-material owner | one canonical whole-material span today; source addressability, not meaning |
| `provenance` | addressable-material owner from verified ledger lineage | ordered raw Event, examination Event, ingress Event ids |

Exact text duplication is intentional in current validation: material text carries the
whole exact value while span text makes the addressed region self-contained, and the
owner proves equality. The full-span id is stable for one recorded ingress id/text
pair and therefore workspace/session scoped indirectly by the globally generated
Event identity; it does not include coordinates because only one canonical full span
is permitted. It is sufficiently scoped for the present invariant, but not evidence
of a future partial-span identity scheme. Neither type asserts intent, proposition,
support, truth, applicability, or any other meaning relation. Their stronger
validation already lives in addressable material, demonstrating that validation
belongs with ingress/addressability rather than warrant production.

## 6. Recovery D — module ownership

Current module ownership is classified **historical co-location + mixed
responsibility**, producing a **dependency inversion** for the live road. It is not a
faithful owner, temporary scaffold, or compatibility holdout on current evidence.

The warrant file introduced the exact-material shapes as inputs beside candidates and
evidence. Current warrant production only reads them; it neither forms their
provenance nor validates source content. The later live addressability module imports
them, originates all production instances, supplies canonical ids, owns strong
invariants, reconstructs serialization, and projects them. That evidence defeats the
module-name implication without assuming that any importer necessarily owns an
imported type.

The error-class coupling further exposes mixed responsibility: addressable JSON
reconstruction catches `ContextualInterpretationWarrantSetError` only because the
co-located dataclasses raise it. A relocation should make invalid exact-material
construction report through the addressable owner's existing
`OperatorIngressAddressableMaterialError`, not retain a reverse dependency merely for
an exception name.

## 7. Recovery E — interpretation-district graph

Current import/artifact direction is:

```text
operator_ingress
  -> operator_ingress_addressable_material
       -> contextual_interpretation_warrant_set

contextual_interpretation_warrant_set
  -> contextual_interpretation_selection
       -> interpretation_applicability_projection
            -> downstream_interpretation_admission
                 -> bounded_operator_goal_establishment
                      -> bounded_advancement_horizon
```

The first arrow into the warrant module is the misowned shared-type seam. Later
modules do not import `InterpretationCandidate` or evidence types directly. Selection
imports `CandidateWarrant`, `ContextualInterpretationWarrantSet`, and
`ExactOperatorMaterial`; applicability consumes only the selection result; admission
consumes selection plus applicability; BOGE consumes admission; horizon consumes
BOGE. `SourceSpan` reaches later stages only nested in candidate warrants/snapshots.

| Module | Types/functions owned | Input producer | Internal consumer | Independent external consumer | Shared live dependency | Terminal standing |
|---|---|---|---|---|---|---|
| contextual warrant | candidates, corrections/evidence, candidate warrants, warrant set/producer; co-located exact shapes | no non-test input producer | contextual selection | none | `SourceSpan`, `ExactOperatorMaterial` are imported by live addressability | internally consumed only |
| contextual selection | selection evidence/result/producer | warrant producer, but no non-test caller | applicability and admission | none | carries exact material only inside demandless chain | internally consumed only |
| applicability projection | purpose/requirement evidence/projection/producer | selection, but no non-test caller | admission | none | none | internally consumed only |
| downstream admission | admission evidence/artifact/producer | selection/applicability, but no non-test caller | admitted-interpretation BOGE | none | none | internally consumed only |
| bounded operator goal establishment | meaning-relation examination plus admitted-interpretation goal artifact/producer | no non-test caller | horizon | package export only, not consumption | none | internally consumed only in district |
| bounded advancement horizon | evidence snapshot, horizon/producer/JSON helper | no non-test caller | none | package export only | none | **terminal** |

Classification by demand:

* **Required by live ingress:** `SourceSpan`, `ExactOperatorMaterial`, and presently
  the co-located error only as an implementation accident.
* **Required only by demandless district:** all remaining warrant-file types and all
  types in selection, applicability, admission, admitted-interpretation BOGE, and
  horizon.
* **Required by both:** the two exact shapes at the Python-use level; only ingress
  independently demands them.
* **Required only by tests:** all caller-side candidate/evidence/purpose/admission/
  horizon inputs in practice.
* **Publicly exported but otherwise unused:** BOGE and horizon classes, errors,
  producers/helpers, and `EvidenceSnapshotReference` listed in `seed_runtime.__init__`.

## 8. Recovery F — shared versus adjacent

`InterpretationCandidate` has no production constructor or external consumer.
`CorrectionCandidate`, `RetrospectiveEvidence`, and `ClarificationEvidence` likewise
have no live external producer. Their apparent consumers all lie inside the same
demandless chain. `CandidateWarrant` is internally produced and consumed, but that is
not independent demand. Public importability and dedicated tests establish a usable
demonstration API, not a live responsibility. Therefore the shared boundary is
exactly two types; no candidate or warrant-evidence shape belongs in retention merely
because future interpretation might use it.

## 9. Recovery G — lawful ownership alternatives

| Alternative | Responsibility coherence / dependency direction | Files and public/test impact | Deletion implications / abstraction / residue risk |
|---|---|---|---|
| A. Keep current location | poor: warrant remains upstream of live source formation | no immediate changes | district behavior can be deleted, but leaves misleading owner; highest residue risk |
| B. Move both types into `operator_ingress_addressable_material.py` | **strongest**: formation, validation, ids, reconstruction, and projection already live there; warrant imports its input | addressable and warrant modules; direct imports in three dedicated test files plus BOGE/applicability tests; no package export change because neither is exported | permits whole warrant module deletion later; no new abstraction; lowest residue risk |
| C. Move into another existing live owner | weak: `operator_ingress.py` owns occurrences, not the separate deterministic addressable shape; representation module owns decoding, not post-Event addressing | would broaden another module and still require imports | obscures addressability; no support found |
| D. Extract narrow exact-material module | coherent only if exact material has consumers independent of addressable ingress | new file, imports and tests; potential future public surface | real concept but currently only one live owner; extraction would be dependency cleanup and premature abstraction |
| E. Inline into sole live owner | same concrete result as B because Python classes remain module members | same as B | lawful; “inline” is simply relocation here |
| F. Delete district and retain/rename current file | could become coherent after deleting all warrant content and renaming to exact material | wider combined rename/deletion and documentation/test churn | effectively B plus deletion; unsafe naming residue if rename omitted |
| G. Further recovery | unnecessary for ownership; remaining implementation deletion scope is sufficiently known | no changes | would delay a topology already evidenced |

No generic shared-model package is warranted. Alternative B/E uses an already-
existing responsibility and changes dependency direction for semantic reasons, not
merely to eliminate an import.

## 10. Recovery H — independent deletion boundaries

### Boundary 1 — warrant-to-horizon behavior only

It is mechanically possible to delete warrant production/artifacts, selection,
applicability, admission, admitted-interpretation BOGE, and horizon while retaining
`SourceSpan` and `ExactOperatorMaterial` in the current file. Live ingress would keep
working if the error and two shapes remained. The residue would be a module named
`contextual_interpretation_warrant_set` containing no contextual warrant set and
serving a live ingress responsibility. That is lawful only as a temporary staging
state, not a coherent final boundary.

### Boundary 2 — move live types, then delete the warrant module

Move `SourceSpan` and `ExactOperatorMaterial` into
`operator_ingress_addressable_material.py`; have
`contextual_interpretation_warrant_set.py` import them; remove the latter error from
live addressable catches by using the addressable error. Update direct test imports.
After that, deletion of the whole warrant module requires no live ingress change.
The later deletion removes all its remaining types/function/constants, then selection,
applicability, admission, BOGE, and horizon in dependency order, their dedicated
tests, and BOGE/horizon package exports.

### Boundary 3 — complete post-addressability district in one PR

Relocation and deletion are sufficiently specifiable, but one combined PR would mix
a live ownership migration with deletion of six demandless modules, seven test
files, package exports, and active-text corrections. That is larger than necessary
and makes proof of behavior-preserving relocation harder to review. The seam is safe
to resolve in one bounded relocation PR; district deletion should follow separately.

### Boundary 4 — smaller interpretation kernel

No lawful kernel remains on present demand. Warrant is the chain's only entrance and
has no candidate/evidence producer; each intermediate has only the next internal
consumer; horizon is terminal. Conceptually sound distinctions and serializers do
not create independent demand. Retaining only selection/applicability/admission, or
only BOGE/horizon, would preserve disconnected constructor APIs.

## 11. Recovery I — test ownership

| Test file | What it verifies | Standing and later disposition |
|---|---|---|
| `tests/test_operator_ingress_addressable_material.py` | live unit + integration behavior: Event verification, exact text/span invariants, projection JSON, replay, malformed/foreign refusal, and no interpretation call | **must survive**; owns all live exact-material behavior; imports move with types |
| `tests/test_contextual_interpretation_warrant_set.py` | constructible demonstration with caller-authored material, candidates, evidence, corrections, Unknown/conflict/loss | district-only; delete with warrant behavior |
| `tests/test_contextual_interpretation_selection.py` | constructible selection/refusal demonstrations with caller-authored fixtures | district-only; delete with selection |
| `tests/test_interpretation_applicability_projection.py` | constructible purpose-local outcomes from fully caller-built chain | district-only; delete with applicability |
| `tests/test_downstream_interpretation_admission.py` | constructible consumer-local admission outcomes | district-only; delete with admission |
| `tests/test_bounded_operator_goal_establishment.py` | caller-built admitted chain plus caller-authored meaning-relation occurrence examinations | no live integration; district demonstration only; delete if the module is deleted |
| `tests/test_bounded_advancement_horizon.py` | direct/caller-authored BOGE and movement-boundary construction/refusal | constructible public-API demonstration; delete with terminal horizon |

`tests/test_operator_ingress.py` also owns the broader live capture/Event/projected-
view integration and must survive, although it is not one of the seven minimum files.
There is no public-compatibility requirement and no deletion guard is proposed.

## 12. Recovery J — public surfaces and serialization

Neither `SourceSpan`, `ExactOperatorMaterial`, `OperatorIngressAddressableMaterial`,
nor any warrant/selection/applicability/admission symbol appears in package
`seed_runtime.__all__`. They remain directly importable by module path.

The package root actively exports only the district's:

* `BoundedOperatorGoalEstablishment`, its error, JSON helper, and admitted-
  interpretation producer; and
* `BoundedAdvancementHorizon`, `EvidenceSnapshotReference`, its JSON helper, and
  producer.

Repository search found no non-test consumer of those exports. They are compatibility-
like/publicly constructible surfaces, not independently demanded surfaces.

Every district artifact implements `to_json_dict` (generally `asdict`), and BOGE and
horizon add module JSON helpers. None is registered as a CLI diagnostic, Event,
projection owner, or serializer consumed by `scripts/seed_local.py`. Serialization
capability does not establish occurrence or demand.

The live serializers are
`OperatorIngressAddressableMaterial.to_json_dict` and `from_json_dict`; the former is
stored in the operator-ingress projected view and the latter reconstructs the frozen
nested shapes. Addressable-material stable-id helpers also belong to live behavior.
The live projector writes no Event: it derives a view from Events and reports
`read_only=true`, `writes_event_ledger=false`, `mutates_state=false`, and
`mutates_cluster=false` on the nested artifact.

## 13. Recovery K — Book and active documentation anchors

Search results separate constitutional grammar from implementation testimony:

| Anchor | Current claim | Classification | Later adjustment if relocation/deletion occurs |
|---|---|---|---|
| `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md` | external representation may become source-attributed/addressable without becoming Constitutional Grammar | constitutional grammar | none; it names no Python owner |
| `book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md` | representative repository anchor is `BoundedAdvancementHorizon` | current implementation anchor | remove/replace this exact runtime anchor if horizon is deleted |
| `book_of_seed/selection_warrant_observability_district_survey_001.md` | names warrant/selection owners and says producer pair recovered | historical survey/testimony with a present-tense implementation claim | later mark historical or remove active-owner claim when district is deleted |
| `book_of_seed/selection_act_classification_recovery_001.md` and `book_of_seed/selection_producer_recovery_001.md` | classify contextual warrant as candidate warranting and selection separately | historical recovery testimony | no constitutional rewrite required; any active index/summary treating them as current must be corrected |
| `docs/bounded_goal_dimensional_establishment_recovery_001.md` | presents exact-material-to-warrant-to-admission BOGE road as active runtime API/test-active | stale/current implementation claim after recent deletions | update/remove admitted-road, public-export, direct-consumer, and horizon claims |
| `docs/operator_material_bounded_goal_frontier_connection_recovery_001.md` | calls exact material and full warrant-to-horizon/frontier road constructible current witnesses | historical testimony containing stale implementation anchors | update exact type owner on relocation; remove district road/active-status tables on deletion |
| `docs/bounded_goal_priority_focus_selection_recovery_001.md` | names horizon implementation, flags, and runtime/test-active standing | current implementation anchor | remove/replace horizon-specific implementation assertions on deletion |
| `docs/bounded_goal_relation_topology_horizon_connection_recovery_001.md` and `docs/bounded_goal_construction_establishment_topology_recovery_001.md` | name horizon/BOGE as current producer/consumer topology | current implementation testimony | revise the named runtime crossings and consumer claims |
| `book_of_seed/pr1970_1974_goal_relation_and_consumer_uptake_reconciliation_001.md`, `book_of_seed/goal_to_question_connection_survey_001.md`, and other numbered recoveries | preserve PR-era horizon descriptions | historical testimony | retain as history unless an active concordance presents them as current; do not rewrite history |
| `docs/operator_expression_interpretation_current_road_recovery_001.md` | mentions another `SourceSpan` belonging to a separate operator-expression interpreter | historical testimony about a different same-named type | no owner change; do not conflate it with this dataclass |

No active Book clause says that contextual warrant constitutionally owns the two
shapes. No canonical clause establishes the warrant-to-horizon road as present
repository truth. The strongest active implementation anchor is the explicit horizon
path in the representative anchors chapter; most other hits are numbered recovery
reports and must remain identifiable as historical testimony rather than authority.

## 14. Recovery L — current constitutional standing

| Artifact | Observed / recorded / projected | Constructible / internally consumed | Independent demand / exposure | Terminal classification |
|---|---|---|---|---|
| `ExactOperatorMaterial` | derived from a verified **recorded** ingress and **projected**; not itself recorded | constructible and reconstructed | independently demanded by live ingress projection; module-path exposed | shared live type, misowned |
| `SourceSpan` | derived/projected coordinate over recorded decoded content | constructible and reconstructed | independently demanded by live source addressability | shared live type, misowned |
| `ContextualInterpretationWarrantSet` | neither observed, recorded, nor projected | constructible; internally consumed by selection | no independent demand; direct module import only | demandless district |
| `ContextualInterpretationSelectionResult` | neither observed nor recorded/projected into state | constructible; internally consumed by applicability/admission | no independent demand | demandless district |
| `InterpretationApplicabilityProjection` | named “projection” but not a StateProjector view | constructible; internally consumed by admission/BOGE | no independent demand | demandless district |
| `DownstreamInterpretationAdmission` | neither recorded nor consumed by a live caller | constructible; internally consumed by BOGE | no independent demand | demandless district |
| `BoundedOperatorGoalEstablishment` | neither observed nor recorded/projected | constructible; internally consumed by horizon | package-public but unused | internally consumed only |
| `BoundedAdvancementHorizon` | neither observed nor recorded/projected | constructible | package-public but unused | terminal |

Frozen/hash/JSON/type-checked standing changes none of these classifications.

## 15. Required direct answers

1. **What current responsibility owns exact operator material?** Operator-ingress
   exact-content preservation within addressable-material formation/projection.
2. **What current responsibility owns source spans?** Operator-ingress source
   addressability, presently the canonical whole-ingress span.
3. **Who constructs `SourceSpan` in non-test production?**
   `form_operator_ingress_addressable_material`; `from_json_dict` reconstructs it.
4. **Who constructs `ExactOperatorMaterial` in non-test production?** The same
   formation function; `from_json_dict` reconstructs it.
5. **Who consumes them?** The enclosing addressable artifact's validator/serializer
   and live operator-ingress projector; the demandless warrant/selection chain can
   carry them when called.
6. **Are they independently demanded by the live ingress road?** Yes: their exact
   nested structure, identities, offsets, replay, and validation are exercised.
7. **Does contextual warrant independently demand them?** No; it has no non-test
   candidate/material supplier or caller.
8. **Is their current defining module a faithful owner?** No; it is historical
   co-location in a mixed-responsibility module.
9. **Which types in that module are shared with a live road?** Exactly `SourceSpan`
   and `ExactOperatorMaterial`.
10. **Which types are exclusive to the demandless district?**
    `InterpretationCandidate`, `CorrectionCandidate`, `RetrospectiveEvidence`,
    `ClarificationEvidence`, `CandidateWarrant`, and
    `ContextualInterpretationWarrantSet`; its error primarily belongs there, although
    live code currently catches it accidentally.
11. **Does `InterpretationCandidate` have any live external consumer?** No.
12. **Does any warrant evidence type have a live external producer?** No.
13. **What is the exact import direction?** Live
    `operator_ingress_addressable_material -> contextual_interpretation_warrant_set`;
    demandless selection also imports higher-level warrant artifacts and exact
    material from that same file.
14. **Is it constitutionally faithful?** No. Exact material is prior input to
    interpretation, while the current Python graph makes live addressability depend
    on the contextual-warrant owner.
15. **Can the interpretation district be deleted without moving shared types?** Yes,
    mechanically, if those types and the error remain in the file.
16. **What misleading residue remains?** A file/module named contextual warrant that
    contains only ingress exact-material shapes and supports no warrant.
17. **Can the types move without inventing a responsibility?** Yes.
18. **Strongest lawful owner?** Existing
    `seed_runtime/operator_ingress_addressable_material.py`.
19. **Is a new exact-material module warranted?** No on current demand.
20. **Real responsibility or dependency cleanup?** Exact preservation/addressability
    is real, but a separate new module would currently only split its sole live owner
    for dependency cleanup.
21. **Which public exports survive relocation?** All current exports; the two types
    are not package-root exports. Direct module imports change to the new owner.
22. **Which serializers belong to live behavior?** Addressable
    `to_json_dict`, `from_json_dict`, and its stable-id/canonical-span helpers.
23. **Which tests own live exact-material behavior?** Primarily
    `tests/test_operator_ingress_addressable_material.py`, with broader live ingress
    projection assertions in `tests/test_operator_ingress.py`.
24. **Which tests are interpretation demonstrations?** The six dedicated warrant,
    selection, applicability, admission, BOGE, and horizon files listed in section
    11 (everything except the addressable-material file).
25. **Which Book/docs anchors later require editing?** The active horizon anchor in
    `demands-and-opened-movement.md`; current-owner claims in the selection-warrant
    survey; and the current-runtime road/consumer claims in the bounded-goal and
    operator-material docs enumerated in section 13. Historical reports remain
    history unless surfaced as current anchors.
26. **Smallest coherent retention boundary?** Capture/examination/recorded ingress
    through deterministic `OperatorIngressAddressableMaterial`, including the two
    nested shapes, serializer/reconstructor, projector, and live tests.
27. **Smallest coherent deletion boundary?** All post-addressability interpretation
    behavior from candidate/warrant formation through terminal horizon, after the
    shared shapes no longer reside inside it.
28. **Is one-PR relocation-and-deletion sufficiently specified?** Mechanically yes,
    but it is not the smallest or clearest review boundary.
29. **Is staged relocation then deletion safer or more faithful?** Yes. It first
    proves unchanged live behavior under corrected ownership, then permits residue-
    free deletion.
30. **What Unknowns remain?** Whether any unsearched dynamic consumer imports symbols
    by computed string cannot be proven statically; no repository evidence does so.
    A future need for partial spans or an independent exact-material consumer is
    Unknown and cannot govern current ownership. The precise later wording changes
    to historical reports versus active indexes should be decided during deletion.
31. **Single smallest lawful next action?** Perform the relocation-only PR specified
    below.

## 16. Exactly one recommended next operation

**Recommend: move only the live shared types in one behavior-preserving ownership
PR.** Do not delete or repair the interpretation district in that PR.

Exact operation:

* In `seed_runtime/operator_ingress_addressable_material.py`, define `SourceSpan` and
  `ExactOperatorMaterial` with their current fields, frozen standing, and invariants;
  make their invalid construction use the existing addressable-material error
  boundary; remove imports of those types and
  `ContextualInterpretationWarrantSetError` from the warrant module.
* In `seed_runtime/contextual_interpretation_warrant_set.py`, import the two types
  from `operator_ingress_addressable_material.py`; retain every candidate/evidence/
  warrant type and producer unchanged for this stage. This direction is acyclic
  because addressable material will no longer import contextual warrant.
* Change direct type imports in
  `tests/test_operator_ingress_addressable_material.py`,
  `tests/test_contextual_interpretation_warrant_set.py`,
  `tests/test_contextual_interpretation_selection.py`,
  `tests/test_interpretation_applicability_projection.py`, and
  `tests/test_bounded_operator_goal_establishment.py` to the live owner where
  applicable. Retain and run all tests; do not add deletion guards.
* Change no package-root export: neither shared type is currently in
  `seed_runtime.__init__`. Change no serializer shape, stable id, Event, projection
  field, CLI, schema, fixture, or Book text.
* Make no Book change in the relocation PR: no canonical Book clause assigns these
  Python types to the warrant module. Update exactly the current exact-material owner
  statements/table rows in
  `docs/operator_material_bounded_goal_frontier_connection_recovery_001.md`; no other
  documentation anchor is required for relocation. Do not rewrite numbered
  historical testimony merely because its old import path records history.
* Leave the later deletion PR to remove the six district modules, their six
  demonstration test files, BOGE/horizon exports, and the exact active Book/docs
  anchors inventoried in sections 11–13.

This operation introduces no new responsibility or generic shared package, preserves
the only independently demanded road, and makes the eventual deletion boundary
coherent without preserving demandless code for convenience.

Exact operator-material shared ownership and interpretation-district boundary recovery complete.
