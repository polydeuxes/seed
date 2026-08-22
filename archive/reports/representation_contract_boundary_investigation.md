# Representation Contract Boundary Investigation

## Scope and method

This bounded investigation asks whether current implementation evidence distinguishes `responsibility -> contract -> implementation representation`, or whether the inspected representations are merely compressed data structures. It does not recover ownership, introduce a `Contract` abstraction, redesign representations, or recommend implementation changes.

Implementation evidence reviewed:

- Observation ingestion, evidence conversion, fact promotion, and secret/confidence validation in `seed_runtime/observations.py`, `seed_runtime/evidence.py`, and `seed_runtime/facts.py`.
- State projection and derived support construction boundaries in `seed_runtime/state.py`.
- Explanation composition in `seed_runtime/explanations.py`.
- Decision input composition in `seed_runtime/context.py`.
- Inquiry Orientation in `seed_runtime/inquiry_orientation.py`.
- Operational Story in `seed_runtime/operational_story.py`.
- Question-family definition/explanation composition in `seed_runtime/question_surface_inventory.py`.
- Previous investigation/audit reports that already rejected universal promotion or responsibility recovery where implementation did not support it, especially `responsibility_to_inquiry_boundary_audit.md`, `question_family_registration_boundary_audit.md`, and `structure_observation_substrate_responsibility_audit.md`.

## Executive conclusion

Implementation evidence supports a recurring discipline, but not a universal abstraction:

```text
bounded producer responsibility
-> concrete representation shape
-> documented or enforced authority boundary
-> bounded downstream consumer
```

The best implementation vocabulary is **concrete representation contract** or **bounded producer/consumer representation boundary**. That vocabulary is supported as a recurring implementation pattern, not as an implemented `Contract` type, framework, registry, or universal `Representation` abstraction.

The strongest examples are `Observation`, `Fact`, `FactSupport`, `Explanation`, `DecisionInputPacket`, `InquiryOrientationView`, `OperationalStory`, and `ComposedQuestionFamilyExplanation`. `Evidence` is also contract-like because it preserves provenance payloads for facts, but its class-level shape is intentionally broad (`payload: dict[str, Any]`), so the contract is carried by the conversion path and event kind as much as by the class fields.

No inspected implementation supports a universal `Representation` abstraction. The concrete models remain distinct and responsibility-specific.

## Producer/consumer contract inventory

| Representation | Producer responsibility | Bounded consumer responsibility | Guaranteed contract fields / assumptions | Explicitly excluded assumptions | Later recovery responsibility |
|---|---|---|---|---|---|
| `Observation` | External/source observation producers and `ObservationIngestor` input boundary | `ObservationIngestor`, then ledger/projector through emitted events | Canonical observed subject/predicate/value with `source_type`, `observed_at`, confidence in `[0,1]`, metadata/dimensions, optional expiry; secret fields rejected before model construction | Not cluster truth by itself; not necessarily promoted to fact; metadata is not guaranteed semantic authority | `ObservationIngestor` converts to `Evidence` and optionally `Fact`; `StateProjector` later projects state |
| `Evidence` | `ObservationIngestor.observation_to_evidence` and other evidence producers | Fact provenance, context selection, explanation/evidence graph consumers | Source/kind/time/workspace/payload/confidence preserving observed provenance | Does not itself assert current state truth or normalized predicate semantics; payload is source-shaped | `Fact` promotion and `StateProjector` derive current inspectable state |
| `Fact` | Observation-to-fact conversion and inference rules | `StateProjector`, fact indexes, explanation, decision context | State claim with subject, predicate, value, dimensions, evidence IDs, provenance source, confidence, observed/expiry timestamps, optional inference lineage | Does not by itself decide current winner, conflict status, aliases, aggregate support, or relationship projection | `StateProjector.finalize` builds aliases, inferred partitions, support, relationships, graph issues |
| `FactSupport` | State projection finalization support aggregation | `State.get_fact_support*`, `ExplanationBuilder`, views | Current projected support for one subject/predicate/value, support fact IDs, source types, confidence, observed/latest times, expiry and durable/measurement support mode | Not raw evidence; not complete history for measurements; not explanation text | `ExplanationBuilder` expands support into belief and recursive fact explanations |
| `Explanation` | `ExplanationBuilder` | CLI/API why views and evidence graph users | Query subject/predicate, status, current/competing beliefs, optional conflict; explanations are deterministic over projected `State` | Does not mutate state, run tools, discover new evidence, or change reasoning behavior | Rendering/API layers present it; source recovery remains in state/evidence/fact links |
| `DecisionInputPacket` | `DecisionInputComposer` | Model clients, intent classifier, evaluation decision loops | Frozen compact packet containing workspace/session/input, selected goals/entities/facts/tools/open needs/schema/evidence/retry/budget trace | Not the full state; not guaranteed all evidence for every fact; non-inferred facts intentionally omit inference lineage fields | Model/client decision code consumes bounded context; context selection owns omission due to budget |
| `InquiryOrientationView` | Inquiry orientation builder from preserved note and projected state | Formatter / operator-facing orientation surface | Raw note, deterministic related material, uncertainty, authority boundary | Not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, instruction, ownership assertion, semantic interpretation, or next action | Source navigation and fact-match functions recover lexical related material; no promotion responsibility follows |
| `OperationalStory` | Operational story builder composing existing audits | JSON/text operational-story surface | Focus, pressure, supporting evidence, capability needs, constraints, correlation gaps, impact, changes, outcomes, path, unknowns, boundary | Does not plan, record, write ledger, mutate cluster, or create facts | Existing audit builders recover pressure/capability/correlation/impact/investigation-path inputs before story composition |
| `ComposedQuestionFamilyExplanation` | Question-family explanation composer | CLI/API bounded-ask explanation surface | Known family identity and composed sections from definition, answer responsibility, boundary, diagnostic relationship | Presentation only; does not register, recover, dispatch, or create question families | Static question surface inventory and bounded dispatch maps remain authority for answerability |

## Representation-by-representation evidence

### Observation

`Observation` is not a passive dictionary. Its constructor rejects secret fields, defaults metadata, coerces and bounds confidence, and then exposes a canonical external observation shape: `id`, `source_type`, `observed_at`, `subject`, `predicate`, `value`, confidence, metadata, dimensions, and optional expiry. That is implementation evidence of a producer-side contract: an observation producer promises an externally observed claim-like payload with bounded confidence and no secret field leakage.

The consumer boundary is explicit in `ObservationIngestor`: it appends observation/evidence/fact events while preserving provenance. Batch ingestion states that every observation still produces its own observation event, evidence event, and optional fact event in repeated-ingest order. The conversion path makes `Observation` a contract into `Evidence` and `Fact`, not final cluster truth.

Guaranteed fields and assumptions:

- subject/predicate/value are present;
- source type is one of the observation source types;
- confidence is normalized to `[0.0, 1.0]`;
- dimensions and metadata exist as dictionaries;
- expiry may be absent.

Intentionally absent guarantees:

- no guarantee that the observation becomes a fact, because fact promotion can be suppressed;
- no guarantee that metadata is semantic truth;
- no guarantee of current-state winning value.

Later recovery responsibility: `ObservationIngestor` converts to `Evidence` and optional `Fact`; `StateProjector` later applies events and derives current indexes.

### Evidence

`Evidence` has the broadest shape in this inventory: source, kind, observed time, payload, and confidence. The contract is therefore not “all evidence payloads have the same domain fields.” Instead, the observed contract is provenance preservation: `ObservationIngestor.observation_to_evidence()` creates an `Evidence` record whose source is `observation:<source_type>`, kind is `observation`, and payload preserves observation ID, source type, subject, predicate, value, metadata, dimensions, and expiry.

Guaranteed fields and assumptions:

- evidence is workspace-scoped;
- it carries source/kind/observed time/confidence;
- observation-derived evidence preserves original observation identifiers and shape-relevant payload fields.

Intentionally absent guarantees:

- no direct assertion that evidence is current state truth;
- no fixed universal payload schema across all evidence producers;
- no current winner/conflict semantics.

Later recovery responsibility: `Fact` links to evidence IDs, and projection/explanation consumers decide how evidence supports current state.

### Fact

`Fact` is a stronger contract than `Evidence`. Its constructor enforces known provenance source types and confidence bounds/defaults. If `inferred` is true, it sets `source_type` to `inferred`; otherwise source type defaults to `user`. Its fields capture subject, predicate, value, dimensions, evidence IDs, provenance source, confidence, observed/expiry time, and optional inference lineage.

Producer promise:

- a fact producer promises a state claim with provenance links and bounded confidence;
- inferred facts carry lineage fields when relevant;
- non-inferred facts need not carry inference lineage.

Consumer assumptions:

- `StateProjector` can place facts into projected state and later derive aliases, relationships, support, graph issues, inferred/observed partitions, and measurement pruning;
- explanations can traverse `source_fact_id`, `inference_rule_id`, and `evidence_ids` when present.

Intentionally absent guarantees:

- a fact is not itself the current selected belief;
- a fact does not decide conflicts;
- a fact does not include projected aliases, relationship projections, graph validation status, or aggregate support.

Later recovery responsibility: projection finalization owns those derived read models.

### FactSupport

`FactSupport` is explicitly a projected support record for one subject/predicate/value claim. Its docstring distinguishes durable aggregate support from volatile measurement current-sample support. Fields preserve support fact IDs, source types, confidence, observed time, latest observed time, expiry, predicate semantics, and support kind.

Producer promise:

- `StateProjector.finalize()` produces `state.fact_supports` after inference, measurement retention, and provenance pruning;
- support consumers may use it as current projected support, not raw event history.

Consumer assumptions:

- `ExplanationBuilder` reads `FactSupport` and expands it into belief explanations by resolving supporting fact IDs still present in `state.facts` and excluding expired facts.

Intentionally absent guarantees:

- not a complete measurement history;
- not raw evidence payload;
- not final explanation text;
- not a universal representation of every fact ever observed.

Later recovery responsibility: `ExplanationBuilder` recovers user-facing explanation material from support, facts, and evidence IDs.

### Explanation

`Explanation` is a result contract for a `why` query over projected state. Its docstring says the shape intentionally separates current and competing beliefs so later query modes can reuse recursive fact explanations without changing reasoning behavior. `ExplanationBuilder` builds it entirely from projected `State`, not from live providers, tools, or new ledger writes.

Producer promise:

- query subject and predicate are preserved;
- status is one of `current`, `ambiguous`, or `no_current_belief`;
- current and competing beliefs are separated;
- conflicts can be included when projection found them.

Consumer assumptions:

- explanation consumers can present current/competing beliefs and recurse through facts/evidence;
- they should not infer that a missing current belief means no observation exists unless the projected supports are also absent.

Intentionally absent guarantees:

- no new observation collection;
- no mutation;
- no planning/action recommendation;
- no universal reasoning engine beyond projected state traversal.

Later recovery responsibility: renderers and evidence graph views present the explanation; state projection remains the source of fact/support truth.

### DecisionInputPacket

`DecisionInputPacket` is a frozen dataclass, and `DecisionInputComposer` is the producer responsibility. The composer orders goals/entities/facts/evidence, applies `ContextBudget.select_sections`, embeds only selected evidence, lists visible tools, and supplies a constrained decision schema. It also intentionally removes `source_fact_id` and `inference_rule_id` from non-inferred fact payloads.

Producer promise:

- the packet is compact selected context for a model decision;
- it includes current input, active goal, selected entities/facts/evidence/tools/open tool needs, decision schema, retry prompt, and budget trace;
- visible tools expose name, summary, schemas, policy action, and risk class.

Consumer assumptions:

- model clients and decision evaluators can make decisions only from bounded context;
- consumers must treat omitted sections as budget/selection omissions, not proof of absence.

Intentionally absent guarantees:

- not a full state export;
- not all evidence for all facts;
- no inference lineage for non-inferred facts;
- no hidden tools.

Later recovery responsibility: context selection and budget tracing explain omissions; full state remains with projection.

### Inquiry Orientation

`InquiryOrientationView` is one of the clearest boundary contracts. The module docstring says inquiry notes are stored outside the event ledger and rendering reads projected state but never mutates it, appends events, calls providers, executes tools, or creates facts/goals/tool needs/decisions/proposals/plans. The `AUTHORITY_BOUNDARY` string explicitly states the note is preserved operator prose, not fact/claim/goal/tool need/requirement/capability/decision/proposal/plan/authorization/command/runtime instruction; matches are deterministic lexical overlaps only.

Producer promise:

- preserve raw note and note metadata;
- provide deterministic related material, uncertainty, and authority boundary;
- compose evidence, answer, boundary, and limitations before rendering.

Consumer assumptions:

- formatter can display related material and boundary;
- operator can use it as orientation, not as repository truth.

Intentionally absent guarantees:

- no semantic interpretation of intent;
- no ownership assertion;
- no importance ranking beyond deterministic overlap;
- no mutation or event writes.

Later recovery responsibility: none for promotion; implementation deliberately refuses promotion from orientation to truth.

### Operational Story

`OperationalStory` is a composed read-only view from existing visibility surfaces. `build_operational_story()` explicitly composes current operational evidence without planning, recording, or mutation. Internal payload classes separate answer, reasoning, supporting evidence, boundary, and limitations; `_compose_operational_story_payloads()` returns those as separate payloads before constructing the public story.

Producer promise:

- story fields preserve focus, pressure, support, capabilities, constraints, correlation gaps, impact, recent changes, outcomes, investigation path, unknowns, and boundary;
- boundary explicitly reports `mode=read_only_view`, `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`.

Consumer assumptions:

- consumers can present a read-only operational story assembled from existing audits;
- they cannot treat it as a plan, event write, fact recording, or cluster action.

Intentionally absent guarantees:

- no direct provider calls beyond existing audit builders;
- no new facts;
- no cluster mutation;
- unknowns remain explicit when input audits lack pressure/capability/impact evidence.

Later recovery responsibility: pressure, capability needs, privilege, correlation, impact, and investigation-path audits recover the input evidence before the story composes it.

### Question-family explanation

`ComposedQuestionFamilyExplanation` is explicitly presentation composition. The builder docstring says it composes existing QuestionFamily explanation fields for presentation only. The composed result includes status, family identity, evidence source, composition source, and sections for definition, answer responsibility, boundary, and diagnostic relationship.

Producer promise:

- preserve the question family name;
- compose fields from `QuestionFamilyDefinition` / inventory-derived rows;
- report answer responsibility and boundary as existing inventory evidence, not recovered semantic truth.

Consumer assumptions:

- CLI/API can present an explanation of an already-known question family;
- consumers cannot infer registration, dispatchability, or semantic family recovery unless inventory and dispatch maps already support it.

Intentionally absent guarantees:

- no new question-family registration;
- no responsibility recovery;
- no promotion from grammar observations or candidate agreements;
- no raw answer dispatch.

Later recovery responsibility: current answerability authority remains the question surface inventory and bounded dispatch maps.

## Recurring implementation patterns

1. **Producers narrow authority before emitting a representation.** Observation rejects secrets and bounds confidence; Fact bounds source/confidence; DecisionInputComposer selects budgeted context; Inquiry Orientation and Operational Story include explicit boundary fields.

2. **Representations carry guaranteed fields but omit downstream-derived truth.** Facts omit current-winner/conflict/support status; FactSupport omits raw evidence payload; DecisionInputPacket omits full state; Inquiry Orientation omits semantic intent and promotion authority.

3. **Downstream consumers are specialized.** `ObservationIngestor` consumes `Observation`; `StateProjector` consumes events/facts/evidence; `ExplanationBuilder` consumes projected support; model clients consume `DecisionInputPacket`; formatters consume orientation/story/question-family explanation views.

4. **Authority boundaries are sometimes encoded as fields and sometimes as conversion paths.** Inquiry Orientation and Operational Story carry explicit boundary text/booleans. Observation/Evidence/Fact carry authority more through conversion and event/projection paths.

5. **Absence is often intentional.** Non-inferred facts in a decision packet lose inference lineage. Question-family explanation composes existing fields and refuses registration. Inquiry Orientation stores notes outside the ledger and refuses mutation.

## Counterexamples and compression points

### Evidence payload is broad

`Evidence.payload` is a generic dictionary. The stronger contract is created by producer-specific conversion (`observation_to_evidence`) rather than by the class alone. This is a compression point: consumers must know `kind`/`source` or producer path to interpret payload fields safely.

### No universal contract abstraction exists

No inspected code defines a `Contract` abstraction or universal `Representation` base beyond ordinary models/dataclasses. The recurring pattern exists as concrete discipline, not a reusable implementation object.

### Some contracts are documentation-heavy rather than type-heavy

Operational Story and Inquiry Orientation encode boundaries in constants, docstrings, and fields. Those are implementation evidence, but not static type constraints. For example, `authority_boundary` is a string, not a capability-safe type.

### Passive-container risk remains in presentation wrappers

`ComposedQuestionFamilyExplanation` is a frozen wrapper around a dictionary. Its contract comes from builder behavior and inventory inputs, not from a rich typed internal schema. It is still bounded by producer/consumer evidence, but more compressed than `Observation`, `Fact`, or `FactSupport`.

### Consumers mostly rely on guaranteed contracts, but dict payloads weaken static assurance

`DecisionInputPacket` facts/tools/evidence are lists of dictionaries. The composer controls their shape, but downstream model clients are not statically prevented from assuming omitted fields exist. The implementation mitigates this by selecting/omitting fields deliberately and by carrying a context budget trace, not by a stronger schema.

## Answers to central questions

### 1. Does each concrete representation define an implementation contract?

Yes, with different strengths. `Observation`, `Fact`, `FactSupport`, `Explanation`, `DecisionInputPacket`, `InquiryOrientationView`, and `OperationalStory` define clear producer/consumer contracts. `Evidence` and `ComposedQuestionFamilyExplanation` are contract-like but more compressed: their strongest guarantees come from producer functions and boundary text rather than from typed payload fields alone.

### 2. What authority does each producer promise to downstream consumers?

- Observation producers promise bounded externally observed subject/predicate/value records.
- Evidence producers promise provenance preservation, not current truth.
- Fact producers promise state claims with provenance and bounded confidence.
- Projection promises support records derived from projected facts, not raw history.
- ExplanationBuilder promises deterministic explanation over projected state.
- DecisionInputComposer promises compact budget-selected decision context.
- Inquiry Orientation promises read-only lexical orientation over preserved operator prose.
- Operational Story promises read-only composition of existing operational visibility surfaces.
- Question-family explanation promises presentation of existing inventory-backed family metadata.

### 3. What assumptions are intentionally excluded from each contract?

The most common exclusions are current truth, semantic interpretation, ownership/responsibility recovery, completeness, mutation authority, dispatch authority, and planning authority. These exclusions are explicit in Inquiry Orientation, Operational Story, and question-family explanation, and implicit but enforced by conversion/projection boundaries for Observation/Evidence/Fact/FactSupport.

### 4. Do downstream responsibilities rely only on those guaranteed contracts?

Mostly yes. `ObservationIngestor` consumes the observation fields it validates and converts. `StateProjector` treats facts/events as projection inputs and derives current state rather than assuming each fact wins. `ExplanationBuilder` reads `FactSupport` and resolves fact/evidence IDs from state. `DecisionInputPacket` consumers receive selected context. The weaker areas are dictionary payloads (`Evidence.payload`, `DecisionInputPacket` sections, composed question-family explanation dictionaries), where safety depends on producer discipline rather than static schema.

### 5. Does implementation evidence support recurring contracts between bounded responsibilities?

Yes. The recurrence is strongly supported as an implementation discipline: producer responsibilities emit concrete shapes with bounded authority; consumers consume those shapes for specific next responsibilities; absent information is recovered later by projection, explanation, audit composition, inventory lookup, or not recovered at all when promotion is intentionally forbidden.

### 6. Where does implementation violate or compress those contracts?

No direct violation was found in the inspected paths, but several compression points remain:

- evidence payloads are generic dictionaries;
- decision context sections are dictionaries;
- question-family composed explanations are dictionary sections;
- some authority boundaries are strings/booleans rather than typed capability boundaries;
- there is no universal contract registry or schema linking each producer/consumer pair.

These are compression points, not proof that the discipline is absent.

### 7. What implementation vocabulary best characterizes this recurring discipline?

The best implementation-backed vocabulary is:

```text
bounded producer/consumer representation boundary
```

or, shorter:

```text
concrete representation contract
```

This wording avoids implying a universal `Contract` abstraction while accurately describing the observed discipline.

## Supported conclusions

1. Current implementation supports recurring concrete contracts between bounded responsibilities.
2. Concrete representations are not merely passive data containers in the main inspected paths; they encode producer promises, omitted assumptions, and consumer boundaries.
3. Implementation does not support a universal `Representation` abstraction.
4. Implementation does not support introducing a universal `Contract` abstraction as a conclusion of this investigation.
5. Some contract boundaries are stronger in behavior and tests than in static type shape.
6. The contract discipline is strongest where constructors/builders validate or explicitly compose bounded fields, and weakest where generic dictionaries carry payloads.

## Unsupported conclusions

1. Unsupported: every representation has an equally explicit statically typed contract.
2. Unsupported: `Evidence.payload` is a universal evidence schema.
3. Unsupported: question-family explanation recovers or registers new families.
4. Unsupported: Inquiry Orientation promotes operator prose into repository knowledge.
5. Unsupported: Operational Story writes facts, records events, or plans actions.
6. Unsupported: the repository implements a generic `Contract` or universal `Representation` model.

## Confidence

High confidence that implementation follows a recurring concrete representation-contract discipline across the inspected models.

Medium confidence about the completeness of the inventory, because the repository contains many additional diagnostic and audit representations not exhaustively inspected here.

High confidence that no universal `Representation` abstraction is supported by the inspected implementation evidence.

## Recommended next investigation

Investigate dictionary-shaped contract compression points only:

```text
Evidence.payload
DecisionInputPacket dict sections
ComposedQuestionFamilyExplanation section dictionaries
OperationalStory nested dict payloads
```

The bounded question should be whether each dictionary shape has enough producer/consumer tests to preserve its current contract, not whether to introduce a new abstraction.
