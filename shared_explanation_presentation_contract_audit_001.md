# Shared Explanation Presentation Contract Audit 001

## Scope

This audit performs exactly one bounded Shared Explanation Presentation Contract Audit over the two currently implemented stage-local explanation owners:

- `OperatorAuthorityScopeBindingProjection` -> `MinimumLawfulAdvancementExplanation`.
- `RepresentationGrammarApplicabilityProjection` -> `RepresentationGrammarApplicabilityAdvancementExplanation`.

It does not implement a contract, adapter, protocol, renderer, composition layer, or normalized explanation artifact. It does not modify source or tests. It treats repository implementation as authority.

## Reviewed evidence

Primary evidence reviewed:

- Ingress authority/scope binding implementation and its explanation implementation in `seed_runtime/operator_authority_scope_binding.py`.
- Ingress slice report `minimum_lawful_advancement_explanation_slice_001.md`.
- Ingress tests in `tests/test_operator_authority_scope_binding.py`.
- Representation grammar applicability implementation and its explanation implementation in `seed_runtime/representation_grammar_applicability.py`.
- Representation applicability explanation slice report `representation_grammar_applicability_advancement_explanation_slice_001.md`.
- Representation applicability tests in `tests/test_representation_grammar_applicability.py`.

This evidence was sufficient; no broader implementation expansion was required.

## Independent ingress explanation inspection

### Source artifact owner

The decision owner is `OperatorAuthorityScopeBindingProjection`. Its source projection preserves ingress authority/scope fields including operator identity, workspace/session authority, requested/resolved/permitted/excluded/unresolved scope, authority-bearing expressions, authority source references, required authority, operator-stated constraints, binding state, binding reason, Unknowns, conflicts, future bounded-question handoff, and read-only flags.

The explanation artifact is `MinimumLawfulAdvancementExplanation`. It is derived from the source projection and is not a new decision owner.

### Movement explained

The explained movement is:

```text
advance one interpreted operator request from authority/scope binding to bounded constitutional question formulation
```

That movement is ingress-local. It is not realization selection, diagnostic selection, execution, event emission, knowledge admission, or cluster mutation.

### State and reason preserved

Ingress preserves `binding_state` as `source_state` and `binding_reason` as `source_reason`.

Implemented source states include:

- `permitted`
- `blocked`
- `unknown`
- `conflict`

These states are constitutional ingress meanings, not generic presentation statuses. The explanation may display them, but must not normalize them into another stage's vocabulary.

### Evidence established

Ingress currently compresses established source evidence into one presentation string named `established`, containing:

- requested activity class;
- requested scope;
- permitted scope;
- excluded scope;
- unresolved scope;
- authority sources;
- required authority;
- operator-stated effect constraints.

This is a current compression, not a typed constitutional schema for all stages.

### Handoff permitted or refused

Ingress does not expose a generic `handoff_permitted` field. It exposes:

- `movement_blocked`, which is true only for `blocked` and `conflict`;
- `first_missing_boundary`, which is `none` for `permitted`;
- a future bounded-question handoff on the source projection only when `binding_state == "permitted"`.

For a permitted result, the explanation removes `formulate_bounded_constitutional_question` from prohibited downstream movement while continuing to prohibit realization selection and execution.

### Reconsideration evidence preserved

Ingress uses one string field, `reconsideration_transition`, to state the minimum lawful source-artifact transition that could permit reconsideration. Examples include:

- an exact bounded operator authority grant for missing ingress authority;
- scope evidence or exact scope permission for excluded scope;
- scope evidence or operator clarification for unresolved referents;
- authority or scope evidence resolving preserved Unknowns;
- request or constraint change for conflicts.

This field is stage-owned because its lawful meaning depends on ingress authority and scope semantics.

### Downstream movement prohibited

Ingress prohibits downstream movement through `prohibited_downstream_movement`. The list is stage-specific:

- `formulate_bounded_constitutional_question` while the ingress handoff is not available;
- `select_diagnostic_view_capability_or_realization`;
- `authorize_or_execute_movement`.

For permitted ingress, formulation is no longer prohibited by the explanation, but selection and execution remain prohibited.

### Unknowns, conflicts, provenance, and known loss

Ingress explanation preserves:

- `preserved_unknowns`;
- `preserved_conflicts`.

The explanation artifact does not currently preserve explicit provenance or known loss fields, even though the source projection and handoff contain provenance and the future handoff can preserve known loss inherited from interpretation. Therefore provenance and known loss are not supported recurring explanation fields for ingress at the explanation-artifact level.

### Read-only and non-mutation guarantees

The explanation artifact sets:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The slice report states that the artifact is immutable, read-only, non-recording, non-event-ledger-writing, and non-mutating, and tests prove the flags appear in both JSON and human rendering.

### Constitutional meaning vs presentation-only fields

Ingress constitutional meaning includes:

- source artifact owner and source projection identity;
- attempted ingress movement;
- `source_state`/`source_reason` as ingress `binding_state`/`binding_reason`;
- established authority/scope evidence;
- `first_missing_boundary`;
- `movement_blocked` as defined by ingress blocked/conflict states;
- `authority_resolvable` and its strict meaning of exact bounded ingress authority grant;
- `reconsideration_transition`;
- prohibited downstream movement;
- preserved Unknowns and conflicts;
- read-only/non-event/non-mutation guarantees.

Presentation-only fields are limited to display labels and rendering order in `format_minimum_lawful_advancement_explanation`. The labels `Minimum Lawful Advancement Explanation`, `source_artifact_ref:`, `producer:`, `attempted_movement:`, and list headings are renderer vocabulary, not independent constitutional knowledge.

## Independent grammar-applicability explanation inspection

### Source artifact owner

The decision owner is `RepresentationGrammarApplicabilityProjection`. Its source projection preserves grammar, demand, mechanism, contract, compatibility dimensions, applicability state, reason, support references, provenance, Unknowns, conflicts, boundary notes, read-only guarantees, known limitations/loss, and future candidate-realization handoff when applicable.

The explanation artifact is `RepresentationGrammarApplicabilityAdvancementExplanation`. It is stage-local and explicitly does not reuse the ingress producer or create a shared cross-stage explanation artifact.

### Movement explained

The explained movement is:

```text
advance one recovered representation grammar applicability result toward the existing future candidate-realization handoff
```

That movement is representation-applicability-local. It is not authority binding, grammar recovery, realization construction, warrant, authorization, emission, execution, or capability reachability.

### State and reason preserved

Grammar applicability preserves `applicability_state` as `source_state` and `applicability_reason` as `source_reason`.

Implemented source states include:

- `applicable`
- `not_applicable`
- `unknown`
- `conflict`

These states are constitutional grammar-applicability meanings, not ingress states. The slice explicitly says the explanation does not reclassify them as ingress `permitted`, ingress `blocked`, or authority failures.

### Evidence established

Grammar applicability preserves established evidence as a tuple named `established_applicability_evidence`, including standings for:

- grammar;
- material compatibility;
- source representation compatibility;
- target representation compatibility;
- invocation contract compatibility;
- lexical support;
- applicability boundary;
- fidelity;
- attribution;
- claim treatment.

This is richer and more typed than the ingress explanation's current one-string `established` compression. It is stage-owned compatibility evidence, not a generic explanation schema.

### Handoff permitted or refused

Grammar applicability exposes `handoff_permitted` directly. Only `applicable` permits the existing future candidate-realization handoff. `not_applicable`, `unknown`, and `conflict` refuse that handoff. The explanation reports handoff permission but emits no handoff.

The boundary field is named `next_handoff_boundary`, not `first_missing_boundary`, and covers both the permitted case and refusal cases:

- applicable: grammar applicability boundary permits the existing handoff;
- not_applicable: bounded positive applicability evidence establishes incompatibility;
- unknown: required bounded support is absent or unresolved;
- conflict: preserved applicability evidence supports incompatible conclusions.

### Reconsideration evidence preserved

Grammar applicability uses tuple field `reconsideration_evidence`, not a transition string. It names source-artifact evidence that would have to change or be supplied:

- changed source-artifact evidence for incompatible standings;
- bounded applicability evidence resolving unknown standings or preserved Unknowns;
- changed evidence removing conflicts without ordering, source count, preferred grammar, or mechanism availability.

This field is stage-owned because it depends on compatibility, lexical support, applicability boundary, fidelity, attribution, claim-treatment, known-loss, and conflict semantics.

### Downstream movement prohibited

Grammar applicability prohibits downstream movement through `prohibited_downstream_movement`. The list is stage-specific:

- `construct_candidate_realization`;
- `select_or_warrant_realization`;
- `authorize_emit_or_execute`;
- `project_capability_reachability`;
- `recover_or_broaden_grammar`.

### Unknowns, conflicts, provenance, and known loss

Grammar applicability explanation preserves:

- `preserved_unknowns`;
- `preserved_conflicts`;
- `preserved_known_loss`;
- `preserved_provenance`.

Known loss and provenance are therefore supported in this explanation artifact, but not across both explanation artifacts.

### Read-only and non-mutation guarantees

The explanation artifact sets:

```text
read_only = true
writes_event_ledger = false
mutates_cluster = false
```

The slice report states those guarantees and tests prove they appear in both JSON and human rendering.

### Constitutional meaning vs presentation-only fields

Grammar-applicability constitutional meaning includes:

- source artifact owner and source projection identity;
- attempted representation-applicability movement;
- examined grammar, demand, mechanism, and contract;
- `source_state`/`source_reason` as grammar `applicability_state`/`applicability_reason`;
- established compatibility/support evidence;
- `next_handoff_boundary`;
- `handoff_permitted`;
- `reconsideration_evidence`;
- `authority_treatment` as an explicit negative relevance finding for operator authority in this stage;
- prohibited downstream movement;
- preserved Unknowns, conflicts, known loss, and provenance;
- compatibility boundary unchanged;
- read-only/non-event/non-mutation guarantees.

Presentation-only fields are limited to display labels and rendering order in `format_representation_grammar_applicability_advancement_explanation`. The labels `Representation Grammar Applicability Advancement Explanation`, `examined_grammar:`, `next_handoff_boundary:`, and list headings are renderer vocabulary, not independent constitutional knowledge.

## Comparison after independent inspections

### Recurring implemented fields and classification

| Recurring concern | Ingress field(s) | Grammar-applicability field(s) | Classification | Finding |
| --- | --- | --- | --- | --- |
| Source owner | `source_artifact_ref`, `source_artifact_type`, `producer` | `source_artifact_ref`, `source_artifact_type`, `producer` | shared presentation field | Presentation may show which stage artifact owns the explanation. Ownership remains stage-local. |
| Artifact identity | `artifact_type`, `explanation_id`, `explanation_convention` | `artifact_type`, `explanation_id`, `explanation_convention` | shared presentation field | Displayable metadata only; not a shared constitutional artifact type. |
| Attempted movement | `attempted_movement` | `attempted_movement` | shared presentation field with stage-local value | Field recurs, but movement semantics remain stage-owned. |
| State/outcome | `source_state` from `binding_state` | `source_state` from `applicability_state` | shared presentation field with stage-local semantic field | Presentation may label it source state. It must not normalize `permitted/blocked` to `applicable/not_applicable` or vice versa. |
| Reason | `source_reason` from `binding_reason` | `source_reason` from `applicability_reason` | shared presentation field with stage-local semantic field | Presentation may label it source reason. Meanings remain source-owned. |
| Established evidence | `established` string | `established_applicability_evidence` tuple | optional stage-owned field | Recurs as an evidence section, but shape and content are not shared enough for a typed semantic contract. |
| Boundary/handoff status | `first_missing_boundary`, `movement_blocked`; source handoff only when permitted | `next_handoff_boundary`, `handoff_permitted` | stage-local semantic field | Both explain boundary/handoff, but one names ingress first missing boundary and one names candidate-realization handoff boundary. Do not normalize. |
| Reconsideration | `reconsideration_transition` string | `reconsideration_evidence` tuple | stage-local semantic field | Both answer reconsideration, but ingress transition and grammar evidence have different constitutional meanings. |
| Prohibited downstream movement | `prohibited_downstream_movement` | `prohibited_downstream_movement` | shared presentation field containing stage-local values | A rendering section can recur; prohibited movement tokens remain stage-owned. |
| Unknowns | `preserved_unknowns` | `preserved_unknowns` | shared presentation field | Both preserve Unknowns without resolving them. |
| Conflicts | `preserved_conflicts` | `preserved_conflicts` | shared presentation field | Both preserve conflicts without precedence or normalization. |
| Provenance | not present on explanation artifact | `preserved_provenance` | optional stage-owned field | Supported only by grammar explanation at explanation level. |
| Known loss | not present on explanation artifact | `preserved_known_loss` | optional stage-owned field | Supported only by grammar explanation at explanation level. |
| Read-only guarantees | `read_only`, `writes_event_ledger`, `mutates_cluster` | `read_only`, `writes_event_ledger`, `mutates_cluster` | shared presentation field | Strongest shared operational guarantee. |
| Authority relevance | `authority_resolvable` | `authority_treatment` | stage-local semantic field | Ingress can answer exact authority resolvability; grammar can only state authority is not a resolution for its evidence. These must not be normalized. |
| Compatibility boundary changed | not present | `compatibility_boundary_changed` | optional stage-owned field | Grammar-only field. |
| Examined grammar/demand/mechanism/contract | not present | `examined_grammar`, `examined_demand`, `examined_mechanism`, `examined_contract` | optional stage-owned field | Grammar-only field. |
| Explanation boundary | `explanation_boundary` | `explanation_boundary` | shared presentation field with stage-local text | Both render a self-limiting boundary statement; the text remains stage-owned. |
| Human renderer labels/order | formatter labels and ordering | formatter labels and ordering | renderer-only field | Label order and headings are presentation conventions only. |

### Shared presentation fields

The exact fields constitutionally supportable as presentation-owned across both artifacts are:

- `artifact_type` as display metadata only;
- `explanation_id` as display identity only;
- `source_artifact_ref`;
- `source_artifact_type`;
- `producer`;
- `attempted_movement`, with stage-owned value semantics;
- `source_state`, with stage-owned state vocabulary;
- `source_reason`, with stage-owned reason vocabulary;
- `prohibited_downstream_movement`, with stage-owned values;
- `preserved_unknowns`;
- `preserved_conflicts`;
- `explanation_boundary`, with stage-owned text;
- `read_only`;
- `writes_event_ledger`;
- `mutates_cluster`;
- `explanation_convention` as display metadata only.

These fields may be shared for presentation as names, ordering conventions, or read-only display slots. They may not become a shared constitutional schema that interprets, compares, orders, normalizes, resolves, or replaces stage-owned meanings.

### Stage-local semantic fields

The following must remain stage-local semantic fields:

- ingress `established` authority/scope compression;
- grammar `established_applicability_evidence` compatibility/support tuple;
- ingress `first_missing_boundary`;
- grammar `next_handoff_boundary`;
- ingress `movement_blocked`;
- grammar `handoff_permitted`;
- ingress `authority_resolvable`;
- grammar `authority_treatment`;
- ingress `reconsideration_transition`;
- grammar `reconsideration_evidence`;
- ingress binding state vocabulary: `permitted`, `blocked`, `unknown`, `conflict`;
- grammar applicability state vocabulary: `applicable`, `not_applicable`, `unknown`, `conflict`;
- ingress binding reasons;
- grammar applicability reasons;
- each stage's prohibited downstream movement values.

### Optional stage-owned fields

The following are implementation-supported in only one explanation artifact and should remain optional stage-owned fields, not shared requirements:

- grammar `examined_grammar`;
- grammar `examined_demand`;
- grammar `examined_mechanism`;
- grammar `examined_contract`;
- grammar `preserved_known_loss`;
- grammar `preserved_provenance`;
- grammar `compatibility_boundary_changed`.

Ingress source and handoff artifacts may contain provenance and known loss elsewhere, but the ingress explanation artifact does not currently expose `preserved_provenance` or `preserved_known_loss`. They are therefore not recurring supported explanation fields across both implemented explanation artifacts.

### Presentation-only fields

Presentation-only fields and conventions include:

- section headings;
- human-renderer title strings;
- ordering of rendered lines;
- list labels such as `preserved_unknowns:` and `prohibited_downstream_movement:`;
- whether established evidence is currently shown as one string or multiple bullet entries;
- JSON renderer function names.

These conventions can be documented but should not carry constitutional meaning.

### Unsupported recurrence

The following apparent recurrences are unsupported as shared constitutional fields:

- generic `blocked` / `not blocked` outcome: ingress has `movement_blocked`, grammar has `handoff_permitted`; these are not equivalent.
- generic `handoff_boundary`: ingress first missing boundary is not grammar candidate-realization boundary.
- generic `authority_resolvable`: grammar has no authority-resolution question; its authority treatment is a stage-local negative relevance statement.
- generic `known_loss`: only grammar explanation currently preserves known loss.
- generic `provenance`: only grammar explanation currently preserves provenance at explanation-artifact level.
- generic `established_evidence` schema: ingress compresses authority/scope evidence into a single string, while grammar emits compatibility standings.
- universal source state taxonomy: `permitted` and `applicable` are not the same state; `blocked` and `not_applicable` are not the same state.
- shared blocker precedence: neither implementation creates one.

## Authority-relevance finding

Authority is constitutionally relevant to ingress authority/scope binding. The ingress explanation's `authority_resolvable` field has a narrow stage-local meaning: only missing ingress activity authority may be marked resolvable by one exact bounded operator authority grant.

Authority is not a constitutional applicability input in the grammar-applicability explanation. Its `authority_treatment` field states that additional operator authority is not a resolution for missing, incompatible, or conflicting representation-grammar applicability evidence.

Therefore:

```text
authority absent from grammar applicability
!= authority_resolvable = false
```

Grammar applicability does not answer a missing-authority question negatively. It treats authority as inapplicable to its evidence boundary. A shared presentation boundary must preserve that distinction and must not require authority fields for grammar applicability.

## Human and JSON findings

Both explanation implementations provide JSON renderers through `to_json_dict` wrappers and human renderers through formatter functions. Tests prove overlapping core fields appear in both human and JSON outputs:

- ingress: state, reason, first missing boundary, authority-resolvable value, reconsideration transition, writes-event-ledger flag, and mutates-cluster flag;
- grammar applicability: state, reason, next handoff boundary, handoff permission, authority treatment, writes-event-ledger flag, and mutates-cluster flag.

The renderers support a recurring presentation shape, but not a shared constitutional schema. They prove that a read-only rendering view could display common slots while deferring all semantic interpretation to the source stage.

## Dynamic-view implications

The recurring shape is evidence for a possible reusable dynamic-view boundary:

```text
stage-owned explanation
-> shared presentation representation
-> later bounded composition
```

However, current evidence supports only the middle representation as a read-only rendering projection or documented rendering convention. It does not support composition, shared state normalization, shared blocker precedence, shared recovery planning, or universal explanation ownership.

A future dynamic view, if ever implemented, would need to consume stage-owned explanations without changing them. It would display recurring presentation-owned fields and carry stage-specific payloads as opaque stage-owned sections.

## Ownership classification

Classification: **B. One shared rendering projection is warranted, but stage explanation artifacts remain independent.**

This is stronger than documented conventions only because both implementations already expose recurring read-only display fields, JSON renderers, human renderers, non-mutation guarantees, source artifact metadata, attempted movement, state/reason preservation, Unknown/conflict preservation, prohibited downstream movement, and explanation boundary statements.

It is weaker than a typed presentation contract or composition-facing interface because key fields differ materially in shape and meaning:

- `established` vs `established_applicability_evidence`;
- `first_missing_boundary` vs `next_handoff_boundary`;
- `movement_blocked` vs `handoff_permitted`;
- `authority_resolvable` vs `authority_treatment`;
- `reconsideration_transition` vs `reconsideration_evidence`;
- ingress provenance/known loss absence at the explanation-artifact level;
- distinct state vocabularies and reasons.

A typed contract would be premature if it implies common constitutional meanings. A composition-facing interface would also be premature because no bounded composition owner has been implemented or tested and composition was explicitly out of scope.

## Strongest supporting evidence

The strongest evidence for a shared presentation boundary is that both explanations are immutable read-only dataclasses with stable IDs, source artifact references, producer labels, attempted movement text, source state/reason fields, prohibited downstream movement, preserved Unknowns/conflicts, explanation boundary text, JSON rendering, human rendering, and `read_only=true`, `writes_event_ledger=false`, `mutates_cluster=false` guarantees.

The strongest evidence that this boundary should be rendering-only is that both slice reports explicitly keep the explanations stage-local and non-mutating while forbidding reclassification, authorization, execution, event writing, or broader generalization.

## Strongest counterevidence

The strongest counterevidence against one shared typed contract is that recurring outer shape hides incompatible constitutional meanings:

- ingress explains authority/scope movement to bounded question formulation;
- grammar applicability explains compatibility movement toward a candidate-realization handoff;
- ingress authority can sometimes be a lawful reconsideration transition;
- grammar explicitly rejects additional operator authority as a resolution;
- ingress uses `permitted` and `blocked`; grammar uses `applicable` and `not_applicable`;
- ingress `movement_blocked` does not map onto grammar `handoff_permitted`;
- provenance and known loss are not both preserved at the explanation-artifact level.

## Exact current compressions

Current ingress compressions:

- established evidence is a single semicolon-delimited string;
- boundary is one `first_missing_boundary` string;
- reconsideration is one `reconsideration_transition` string;
- authority relevance is one boolean `authority_resolvable`;
- provenance and known loss are not exposed on the explanation artifact.

Current grammar-applicability compressions:

- established evidence is a tuple of `label=value` strings;
- boundary is one `next_handoff_boundary` string;
- reconsideration is a tuple of evidence statements;
- authority relevance is one explanatory string `authority_treatment`;
- compatibility boundary change is compressed to `compatibility_boundary_changed=False`;
- known loss and provenance are preserved as tuples.

These compressions are implementation facts. A shared rendering projection could display them, but should not reinterpret them as normalized types.

## Whether one implementation slice is warranted

One implementation slice is warranted only if it is bounded to a read-only shared rendering projection that:

- consumes already-produced stage-local explanation artifacts;
- preserves stage-local artifacts unchanged;
- presents only the shared presentation fields listed in this audit;
- carries stage-specific fields as opaque stage-owned sections;
- does not normalize state, reason, boundary, authority, reconsideration, evidence, or prohibited movement;
- does not create a universal explanation artifact, manager, registry, router, planner, base decision class, or state normalizer;
- does not authorize, observe, emit, execute, write events, or mutate cluster state.

No implementation should be attempted until the next bounded question is answered.

## Exact next bounded question

Given one already-produced stage-local explanation artifact from either ingress authority/scope or representation grammar applicability, what smallest read-only rendering projection may display source owner, attempted movement, source state/reason, preserved Unknowns/conflicts, prohibited downstream movement, read-only guarantees, and opaque stage-specific sections without normalizing states, requiring authority fields, emitting handoffs, composing explanations, writing events, or mutating cluster state?

## Preserved Unknowns

- Whether future explanation owners in capability reachability, warrant, policy authorization, remediation, or recovery will preserve the same presentation fields.
- Whether provenance and known loss should remain optional stage-owned sections or become recurring if future implementations also expose them.
- Whether a later bounded composition owner is needed after a rendering projection exists.
- Whether ingress should ever expose provenance or known loss at explanation-artifact level; this audit does not recommend that change.
- Whether a formal typed contract can be lawful after more stages are implemented; current evidence is insufficient.

## Confidence

Confidence: high for the two audited implementation slices; medium for the dynamic-view implication because no shared rendering projection or composition owner exists yet.

## Final answer

What explanation meaning may be shared for presentation:

- source explanation identity and source artifact ownership;
- attempted movement as stage-authored text;
- source state and source reason as displayed stage-owned values;
- preserved Unknowns and preserved conflicts;
- prohibited downstream movement as displayed stage-owned values;
- explanation boundary as stage-authored text;
- read-only, non-event-ledger, and non-mutation guarantees;
- renderer ordering and section conventions.

What explanation meaning must remain owned by each constitutional stage:

- ingress authority/scope state and reason meanings;
- grammar-applicability state and reason meanings;
- authority relevance and authority resolvability;
- compatibility, lexical support, applicability boundary, fidelity, attribution, claim treatment, known loss, and provenance meanings;
- boundary/handoff meaning;
- reconsideration meaning;
- established evidence shape and interpretation;
- prohibited movement semantics;
- any decision to permit, refuse, or reconsider a stage handoff.

Shared explanation presentation contract audit complete.
