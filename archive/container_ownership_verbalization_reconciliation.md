---
doc_type: reconciliation
status: implementation-backed recommendation
scope: deterministic verbalization, container ownership authority, bounded operator language
---

# Container Ownership Verbalization Reconciliation

## Central answer

Yes: Seed can speak without generating in the constrained container-ownership
slice, if "speak" means deterministic verbal projection of existing
implementation-backed artifact fields.

The supported boundary is:

```text
Presentation projects existing implementation-backed answers into deterministic
operator language.

Presentation never creates new meaning.
```

This is not LLM summarization, natural language generation, a speech engine, a
conversation engine, prompt engineering, or an answer composition framework. It
is the same architectural family as the current human CLI formatter: a bounded
projection over fields already returned by the container-ownership authority
slice.

## Scenario boundary

This report evaluates only:

```text
Determine container ownership under constrained authority.
```

It does not broaden to service ownership, listener endpoint authority, generic
conversation, voice runtime, prose generation, or autonomous planning.

## Files inspected

Required implementation files:

- `seed_runtime/container_ownership_authority.py`
- `scripts/seed_local.py`
- `tests/test_container_ownership_authority.py`

Required supporting reconciliation files:

- `docs/presentation_conversation_responsibility_reconciliation.md`
- `docs/container_ownership_answer_ordering_reconciliation.md`
- `docs/inquiry_state_reasoning_reconciliation.md`
- `docs/answer_responsibility_implementation_characterization.md`

App commands used:

```text
python scripts/seed_local.py --container-ownership-authority
python scripts/seed_local.py --container-ownership-authority --json
```

## Implementation evidence

The container ownership evaluator returns a frozen
`ContainerOwnershipAuthoritySlice` with structured fields for the desired
observation, required observations, required authority, available authority,
outcome, current strategy, strategy status, remaining observations, uncertainty,
remaining uncertainty, blocking boundary, and explicit read-only/non-mutating
boundary flags. The JSON projection serializes those fields directly.

The formatter already proves that a human-facing projection can reorder and label
those fields without changing repository truth. It emits a fixed section order:
Goal, Strategy, Authority, Execution, Remaining work, and Boundary. Tests assert
that section order and also assert that JSON keeps the implementation-shaped
fields intact.

The app output for the required scenario currently reports:

```text
Strategy status: blocked
Outcome: blocked
Blocking boundary: docker_or_root_container_runtime_authority_unavailable
```

and JSON reports the same facts as fields:

```text
"strategy_status": "blocked"
"outcome": "blocked"
"blocking_boundary": "docker_or_root_container_runtime_authority_unavailable"
```

Those fields are sufficient to support a deterministic minimal operator sentence
such as:

```text
I can't determine container ownership.
```

but only with a strict artifact-backed mapping: this sentence must mean
`desired_observation=container ownership` and `strategy_status=blocked` in this
slice. It must not mean that Seed globally cannot determine container ownership,
that no other strategy exists, that an operator could not grant authority, or
that an external provider path has been evaluated.

## Answers to required questions

### 1. Can existing implementation-backed fields be verbalized without introducing new truth?

Yes, if the verbalization is an explicit deterministic projection from one or
more existing fields and preserves the slice boundary.

Supported example:

| Artifact evidence | Safe deterministic verbal projection | Boundary |
| --- | --- | --- |
| `desired_observation=container ownership` plus `strategy_status=blocked` | `I can't determine container ownership.` | Means "this current slice cannot determine it under the supplied constrained authority profile." |
| `blocking_boundary=docker_or_root_container_runtime_authority_unavailable` | `I don't currently have the required container-runtime authority.` | Must not claim global service-runtime authority or authorization workflow behavior. |
| `required_authority` values are `docker_group_or_root` | `This requires Docker group or root authority.` | Must not request, create, store, or grant that authority. |
| `boundary.mutates_cluster=false` | `This does not mutate the cluster.` | Must remain a diagnostic/projection boundary, not a cluster fact about the target. |

The exact sentence `I can't determine container ownership.` is
implementation-backed only when read as a bounded status projection for the
current container-runtime strategy. It becomes an overclaim if it is read as a
global impossibility, as a statement about all future authority profiles, or as a
claim that every non-container-runtime path was evaluated.

### 2. Should verbalization be attached to artifacts rather than composed across multiple artifacts?

Mostly yes. The safest design is artifact-owned deterministic verbal
expressions, with only narrow template bindings where a sentence needs the target
name.

Artifact-owned examples:

- `strategy_status=blocked` owns `I can't proceed with the current strategy.`
- `desired_observation=container ownership` owns the noun phrase `container
  ownership`.
- `blocking_boundary=docker_or_root_container_runtime_authority_unavailable`
  owns `Docker or root container-runtime authority is unavailable.`
- `current_strategy=container_runtime_observation` owns `container-runtime
  observation`.
- `required_authority` owns `Docker group or root authority` for each required
  observation.

A minimal first sentence may bind two artifacts:

```text
I can't determine {desired_observation}.
```

but the truth condition remains artifact-backed: `{desired_observation}` supplies
the object, and `strategy_status=blocked` supplies the inability. Presentation
must not compose a new causal explanation unless the causal boundary is already
present as `blocking_boundary`, `required_authority`, or `available_authority`.

### 3. Can operator interaction follow progressive disclosure?

Yes, architecturally, but the current implementation supports it as a sequence of
existing fields rather than as an implemented conversation runtime.

The supported progressive disclosure for the required scenario is:

```text
Operator: Who owns this container?
Seed: I can't determine container ownership.

Operator: Why?
Seed: I don't currently have the required authority.

Operator: What authority?
Seed: Docker group or root authority for container-runtime observation.
```

This behavior is supported because each answer corresponds to an existing field
or field family:

- first answer: `desired_observation`, `strategy_status`, `outcome`;
- why answer: `blocking_boundary`, `available_authority`;
- what-authority answer: `required_authority`, `required_observations`,
  `current_strategy`.

What is not currently supported is a general dialog manager that decides when to
ask or answer follow-up questions. The repository supports a fixed progressive
projection order; it does not support autonomous conversational reasoning.

### 4. Does verbalization belong to Presentation?

Yes. Deterministic verbalization belongs to Presentation when it is limited to
projecting already-evaluated fields into operator language.

It does not introduce reasoning, composition, conversation-engine behavior, or
LLM behavior if it obeys these rules:

- no new facts;
- no new causal links;
- no unstated authority;
- no hidden uncertainty reduction;
- no global alternatives claim;
- no mutation, recording, provider acquisition, permission creation, or
  observation execution;
- no promotion of presentation vocabulary into repository knowledge.

The current CLI formatter is the implementation precedent: it turns the slice
fields into a human-readable sectioned output while JSON remains
implementation-shaped.

### 5. Is the projection principle supported?

Yes. The supported principle is:

```text
Presentation projects existing implementation-backed answers into deterministic
operator language.
Presentation never creates new meaning.
```

This is stronger and safer than saying "Presentation generates prose." The
repository evidence supports projection, ordering, labeling, and fixed sentence
selection. It does not support open-ended language generation.

### 6. Can one implementation artifact support multiple projections?

Yes. The current slice already supports at least two projections:

1. JSON: `container_ownership_authority_json(result)` returns the structured
   artifact shape.
2. CLI: `format_container_ownership_authority(result)` returns human-readable
   sections.

A spoken sentence or future structured prose view can be another projection over
the same artifact without changing repository truth, provided the mapping is
static and testable. For example:

```text
ContainerOwnershipAuthoritySlice
    -> JSON projection
    -> CLI section projection
    -> minimal verbal projection
    -> future structured prose projection
```

The artifact remains the authority. Projections must be reproducible from the
artifact and must not feed new facts back into cluster truth.

### 7. Does deterministic verbalization become another observable repository artifact?

Yes, if implemented, deterministic verbalization should be treated as an
observable projection artifact. It should be testable the same way the current
CLI and JSON projections are testable.

The supported direction is:

```text
implementation artifact
    -> verbal projection
    -> future structured input may reference the projection
```

The unsupported direction is:

```text
verbal projection
    -> new repository truth
```

Verbal output can be recorded or inspected as output, but it must not become the
source of truth for container ownership, authority, or uncertainty. The source of
truth remains the implementation artifact and its evidence sources.

## Verbalization responsibility

Presentation owns deterministic verbalization as a projection responsibility.
The evaluator owns the fields. Subsystems own the domain answers and authority
mappings. Inquiry owns the bounded question. Diagnostics own inventory and shape
visibility if a new operational surface is added.

Recommended responsibility split:

| Layer | Responsibility | Not responsible for |
| --- | --- | --- |
| Inquiry | The bounded question: determine container ownership under constrained authority. | Verbal phrasing. |
| Subsystems/evaluator | Structured answers and authority-bounded outcome. | Operator-language minimization. |
| Presentation | Deterministic field-to-language projection and progressive disclosure order. | Truth creation, reasoning, planning, or authority acquisition. |
| Diagnostics | Inventory and shape audit if the verbalization is exposed as a new CLI/diagnostic surface. | Semantic ownership of the verbalized answer. |

## Artifact-backed verbalization

Safe deterministic mappings for this slice:

| Field or artifact | Deterministic operator language |
| --- | --- |
| `desired_observation=container ownership` | `container ownership` |
| `current_strategy=container_runtime_observation` | `container-runtime observation` |
| `strategy_status=blocked` | `I can't proceed with the current strategy.` |
| `outcome=blocked` with desired observation | `I can't determine container ownership.` |
| `blocking_boundary=docker_or_root_container_runtime_authority_unavailable` | `Docker or root container-runtime authority is unavailable.` |
| `required_authority[container_inventory]=docker_group_or_root` | `Container inventory requires Docker group or root authority.` |
| `required_authority[container_port_mapping]=docker_group_or_root` | `Container port mapping requires Docker group or root authority.` |
| `available_authority[root]=unavailable` | `Root authority is unavailable.` |
| `available_authority[docker_socket_read]=unavailable` | `Docker socket read authority is unavailable.` |
| `boundary.mutates_cluster=false` | `This does not mutate the cluster.` |

## Deterministic language requirements

Deterministic language must be:

- table-driven or branch-driven from exact artifact values;
- covered by tests for the required scenario;
- reversible enough that a maintainer can identify the field that authorized the
  sentence;
- scoped to this slice unless broader evidence is added;
- incapable of introducing unsupported alternatives, plans, or authority claims.

## Projection boundaries

Supported:

- fixed minimal answer first;
- fixed follow-up order over existing fields;
- artifact-owned wording tables;
- field-preserving JSON;
- human CLI or spoken projection as non-authoritative output;
- tests proving exact sentences for exact fields.

Unsupported:

- LLM summarization;
- free-form prose generation;
- conversation engine behavior;
- speech engine implementation;
- prompt engineering;
- answer composition framework;
- claims that all alternatives are exhausted;
- claims that Seed can request or grant the missing authority;
- claims that diagnostic findings mutate cluster truth.

## Strongest supporting evidence

The strongest supporting evidence is the existing split between the evaluator,
JSON projection, CLI formatter, and tests:

- the evaluator produces structured fields and explicit boundaries;
- JSON serializes those fields without conversational reshaping;
- the CLI formatter already renders deterministic human language over the same
  artifact;
- tests assert both the JSON shape and the human section order;
- the diagnostic inventory and shape audit already declare the surface as JSON
  supporting, non-recording, non-event-writing, and non-mutating.

This proves that one implementation artifact can already support multiple
truth-preserving projections.

## Strongest contradictory evidence

The strongest contradictory evidence is absence of an implemented minimal verbal
projection function today. The current human CLI is sectioned and deterministic,
but it does not yet expose the one-sentence progressive-disclosure form. The
repository therefore supports the architecture and next step, but not an already
implemented `--spoken` or `--verbal` operator surface.

A second caution is that `I can't determine container ownership.` compresses the
slice boundary. Without a nearby or recoverable boundary sentence, an operator
could hear it as a global inability. The safer exact first implementation may be:

```text
I can't determine container ownership with the current container-runtime authority.
```

or a two-line minimal response:

```text
I can't determine container ownership.
Current strategy is blocked by missing Docker or root authority.
```

## Recommended next implementation step

Add a narrow, tested deterministic verbal projection for
`ContainerOwnershipAuthoritySlice`, without changing JSON truth shape:

```text
format_container_ownership_authority_minimal(result, detail="answer" | "why" | "authority")
```

Initial mappings should be limited to the constrained blocked scenario already
covered by tests:

- `answer`: `I can't determine container ownership.`
- `why`: `I don't currently have Docker or root container-runtime authority.`
- `authority`: `Container-runtime observation requires Docker group or root authority.`

If exposed as a new CLI flag or diagnostic surface, update the diagnostic
inventory, diagnostic shape-audit specs, and tests required by the operational
visibility contract. If kept as an internal formatter helper used by the existing
surface, update only the container ownership tests that prove exact deterministic
output.

## Final reconciliation

Can Seed speak without generating? Yes, if speaking is deterministic projection
from implementation artifacts.

Can existing repository artifacts own deterministic verbal projections? Yes. The
container ownership authority artifact already owns the fields needed for safe
minimal verbal language, and artifact-owned phrases are safer than cross-artifact
composition.

Should spoken language be treated as another projection of repository truth
rather than a new source of truth? Yes. Spoken or verbal output should be an
observable projection artifact that is reproducible from structured repository
answers and never promoted into cluster truth.
