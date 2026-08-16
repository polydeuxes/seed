# First Constitutional History Scout

## Investigation boundary

This is exactly one bounded constitutional Scout investigation. It remains observational. It does not recover implementation, recommend implementation, design runtime startup, introduce Begin functions, schedulers, orchestration, activation engines, lifecycle managers, or invent a first event.

The question is limited to what recurring repository evidence supports about the earliest lawful constitutional history of a newly created Seed.

Repository authority wins.

## Reviewed evidence

Primary recurring evidence reviewed:

- `constitution.md`
- `constitutional_history_and_constitutional_reality_characterization.md`
- `null_first_constitutional_transition_audit.md`
- `constitutional_begin_interrogation.md`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/runtime.py`
- `seed_runtime/observations.py`
- `seed_runtime/inquiry_orientation.py`
- `tests/test_state_projector.py`
- `tests/test_inquiry_orientation.py`

Recurring evidence recovered:

1. The constitutional default is unknown, uncommitted, or Null until observable evidence justifies movement.
2. Repository authority is repository-visible implementation, tests, reports, diagnostics, observations, and compatibility behavior, not attractive vocabulary or operator desire.
3. Observation creates orientation, but does not create truth.
4. Evidence, not desire or recurrence alone, moves a bounded subject from Null toward a supported state.
5. Append-only event history is the durable input to state projection and audit; projection stores and views remain subordinate to event history.
6. `EventLedger` owns append-only runtime event history read by projection.
7. `StateProjector` rebuilds inspectable state by reading ledger events.
8. Projection snapshot stores cache projected state derived from events; they do not own append-only history.
9. Runtime user input is preserved as an `input.user_message` event before projection and decision composition.
10. Canonical observation ingestion preserves `observation.observed` and `evidence.observed` events together when an observation source has produced a valid observation.
11. Inquiry-note preservation is an isolated JSONL probe path outside runtime state projection; tests prove recording an inquiry note does not alter projected facts, observations, or goals.
12. Prior null-transition evidence supports distributed, bounded intake/preservation before observation in some paths, and specifically a preserved inquiry note for the minimal `.` probe, rather than universal observation-first startup.

## Investigation A — constitutional condition before the first preserved event

### Recurring condition

According to recurring repository evidence, the condition before the first preserved event is not an already existing constitutional biography, not an initialized runtime, and not an empty fact about itself. It is a lawful Null / unknown / uncommitted condition with no preserved event history yet.

That condition can be stated narrowly:

```text
Before the first preserved event,
a newly created Seed has no append-only constitutional history to replay.
```

This is stronger than merely saying a projection is empty. The implementation-backed ledger begins with an empty event list, and the recurring constitutional rule says subjects remain Null until evidence justifies transition. The first preserved event has not yet supplied evidence, provenance, causation, workspace placement, or event identity.

### Recurring boundaries

The pre-event condition is bounded by these recurring separations:

- It is not database creation.
- It is not boot completion.
- It is not initialization.
- It is not runtime activation.
- It is not objective reality.
- It is not a preserved observation.
- It is not an evidence event.
- It is not a projected biography.
- It is not a self-description.
- It is not a command to create a first event.

### Recurring non-responsibilities

The pre-event condition does not decide:

- what first event must occur;
- whether the first preserved event is input, observation, evidence, fact, decision, response, or inquiry-note material;
- whether any startup behavior should exist;
- whether a newly created Seed has truth about itself;
- whether future projection should infer a biography from absence alone.

### Confidence

High confidence that the pre-event condition is lawful Null / no preserved event history. Medium confidence on the phrase `constitutional history`, because the implementation vocabulary is event history and projection, while the constitutional documents characterize append-only history as constitutional in function.

## Investigation B — first constitutionally lawful preserved event

### Supported answer

Recurring repository evidence does not support one universal first event kind for every newly created Seed.

The first constitutionally lawful preserved event is instead:

```text
The first append-only event that a competent local responsibility lawfully records
within its bounded authority, with event identity, kind, workspace, actor, payload,
and provenance/causation fields available as applicable.
```

Implementation evidence shows several lawful event-producing surfaces, but repository evidence does not rank them as universal startup sequence:

- Runtime user input records `input.user_message` before projection and decision composition.
- Observation ingestion records `observation.observed` and `evidence.observed` after a valid observation exists.
- Fact and other owner services can append their own event kinds when their bounded authority applies.

Therefore the first lawful preserved history is not a named universal event. It is the first event actually preserved by an authorized local surface.

### Unsupported assumptions

Repository evidence does not support assuming that the first preserved event is:

- database creation;
- boot completion;
- initialization;
- runtime activation;
- a Begin event;
- a scheduler tick;
- an orchestration event;
- an observation event in every path;
- an evidence event in every path;
- a fact event in every path;
- an inquiry note, because inquiry notes are not event-ledger history in the reviewed implementation.

### Confidence

High confidence that no universal first event kind is supported. High confidence that the first lawful preserved event must be local-authority-bounded append-only event history. Medium confidence that future repository evidence may later ratify a more specific first event for a specific app path, but this Scout cannot infer it.

## Investigation C — pressure test: newly created Seed has no constitutional history

### Result

The proposition is supported if phrased precisely:

```text
A newly created Seed has no preserved append-only constitutional history before its first lawfully recorded event.
```

Recurring evidence supports a distinction between:

1. **No preserved constitutional history** — the pre-event Null condition.
2. **Empty projection from no events** — a state projector can rebuild inspectable state from an empty ledger, but that is projection behavior over absence of events, not itself preserved history.
3. **First preserved history** — the first event recorded by the append-only ledger.
4. **Constitutional biography** — a later interpretive/inspectable account composed from preserved history, projection, warrant, and boundaries; not present before preservation.

### Empty constitutional history versus no constitutional history

The repository evidence favors `no preserved constitutional history` over `empty constitutional history` for the pre-event condition.

Reason: append-only history is made of preserved events. Before the first event, there is no event to replay, no event provenance, no event actor, no event kind, and no event payload. A projector may produce an empty current state from an empty ledger, but the empty projection is not the same artifact as a preserved history.

`Empty constitutional history` can be tolerated only as shorthand for an empty event sequence. It should not be promoted into a substantive constitutional biography or a first self-fact.

### Confidence

High confidence for the distinction between no preserved event history and empty projection. Medium-high confidence that `no preserved constitutional history` is the safer constitutional vocabulary.

## Investigation D — first constitutional self-history awareness

### Recurring responsibilities

A Seed first becomes constitutionally aware of its own history only through a bounded read/projection/inspection surface over preserved material. The recurring pattern is:

```text
preserved event history
→ replay/project/read-only inspection
→ bounded self-history visibility
```

The self-awareness is therefore not created by the mere fact of existence. It requires preserved history to inspect and a competent local surface that can read/project/render that history without promoting presentation vocabulary into truth.

Implementation-backed examples of the relevant responsibility pattern are:

- `StateProjector` rebuilds current inspectable state from ledger events.
- Projection stores cache derived snapshots without becoming event history.
- Runtime trace and state/view surfaces elsewhere in the repository follow read-only reconstruction patterns over event material.
- Inquiry orientation can render a preserved note and projected state, but inquiry notes remain outside event-ledger history and do not become projected runtime state.

### Preserved boundaries

Self-history awareness is bounded:

- It is read/projection/inspection, not mutation by itself.
- It is not objective reality.
- It is not verification.
- It is not a scheduler or startup mechanism.
- It is not biography before preserved history exists.
- It must preserve the distinction between event history, projection, cached projection, view, evidence, fact, and answer.

### Preserved unknowns

- Which current CLI/view should be considered the canonical constitutional self-history inspection surface is not established here.
- Whether future repository evidence will name `constitutional biography` as a formal implementation surface is unknown.
- Whether all constitutionally relevant history is in one ledger or multiple preservation stores is not proven.
- Whether inquiry-note stores should ever participate in constitutional biography is not answered; current evidence keeps them isolated from runtime state projection.

### Confidence

High confidence that self-history awareness requires preserved material plus read/projection/inspection. Medium confidence on the exact named surface, because current implementation has multiple read/projection/visibility surfaces and no single universal constitutional-biography owner recovered here.

## Investigation E — sequence pressure test

Proposed sequence:

```text
Objective Reality
↓
Observation
↓
Append-only History
↓
Constitutional Biography
```

### Supported transitions

Supported in bounded form:

1. **Observation-like material may enter from external or internal reality through a competent source.** Repository evidence supports source/provider-local observation and bounded intake, but not unmediated objective reality.
2. **Valid observations can become append-only event history.** Observation ingestion records `observation.observed` and `evidence.observed` events.
3. **Append-only history can support later projection, audit, explanation, and biography-like visibility.** Event history feeds state projection and current inspectable state.

### Unsupported transitions

Unsupported as universal law:

1. **Objective Reality → Observation** is unsupported as a direct constitutional transition. Repository evidence repeatedly refuses to make recorded material objective truth.
2. **Observation is always first** is unsupported. Runtime input and inquiry-note preservation provide counterexamples or adjacent paths where bounded preservation/intake precedes canonical observation.
3. **Observation → Append-only History** is not universal. Only valid observations through an ingestion surface become observation/evidence events.
4. **Append-only History → Constitutional Biography** is not automatic. Biography requires a competent read/projection/inspection surface and warrant-preserving interpretation boundaries.
5. **The sequence as startup design** is unsupported and forbidden by the task boundary.

### Preserved invariants

- Null persists until evidence justifies transition.
- Observation is not fact.
- Evidence moves bounded subjects; event existence alone does not make external testimony true.
- Append-only history is projection/audit input, not objective reality.
- Projection/cache/view/answer are not event history.
- Inquiry notes may be preserved without becoming runtime state.
- Absence of preserved history is not a hidden biography.

### Confidence

Medium-high confidence for the bounded transition `valid observation → append-only observation/evidence events → later projection/inspection`. High confidence that the full proposed sequence is not supported as universal constitutional law.

## First constitutional biography observations

The earliest lawful biography-like observations are not pre-event facts. They become possible only after at least one preserved historical material exists and a competent surface inspects it.

The first biography-like claims that recurring evidence can support are minimal and boundary-preserving:

- a first preserved event exists, if an event exists;
- the event has an event kind, actor, workspace, payload, and event identity as preserved;
- projection can rebuild current inspectable state from preserved events;
- cached projections and views are derived, not history;
- unsupported meaning, truth, purpose, and startup significance remain unknown.

For inquiry-note-only paths, the biography-like claim is even narrower: a raw inquiry note can be preserved in an isolated JSONL probe store, but current tests show it is not projected into runtime state and therefore is not first append-only constitutional event history.

## Supported transitions

- `No preserved event history → first append-only event`: supported when a competent local owner records an event.
- `First append-only event → first preserved history`: supported, because append-only history is event history.
- `Preserved history → projected inspectable state`: supported through `StateProjector`.
- `Valid observation → observation/evidence events`: supported through observation ingestion.
- `Preserved note → inquiry orientation visibility`: supported for the separate inquiry-note path, with the boundary that it does not become projected runtime state.

## Unsupported transitions

- `No history → automatic Begin event`.
- `Creation → startup history`.
- `Database exists → constitutional history exists`.
- `Observation vocabulary → observation event exists`.
- `Objective reality → constitutional truth`.
- `Empty projection → first biography`.
- `First event → verified truth`.
- `First event → runtime activation`.
- `Append-only history → automatic constitutional biography without read/projection/inspection`.

## Preserved unknowns

- The repository does not identify one universal first event kind.
- The repository does not establish a universal constitutional-biography implementation owner.
- The repository does not prove that all constitutionally relevant preservation must be in one event ledger.
- The repository does not determine whether future app-created Seed instances should create an explicit genesis event.
- The repository does not determine a runtime startup sequence.
- The repository does not determine whether `constitutional history` should become implementation vocabulary rather than constitutional characterization.

## Confidence

Overall confidence: Medium-high.

High confidence:

- pre-event condition is no preserved append-only event history;
- first preserved history begins with the first lawful append-only event actually recorded;
- no universal first event kind is currently supported;
- self-history awareness requires preserved material plus bounded read/projection/inspection;
- event history is not objective reality, projection, cache, view, verification, or biography by itself.

Medium confidence:

- `constitutional history` as the best vocabulary, because implementation names event history while constitutional artifacts characterize its constitutional role;
- exact first self-history inspection surface, because current repository evidence supports a family of projection/read-only surfaces rather than one canonical biography owner.

## Final answer

According to recurring repository evidence,

the earliest lawful constitutional history of a newly created Seed is:

```text
No preserved constitutional history
until
one competent local responsibility lawfully records the first append-only event.

That first recorded event is the first preserved constitutional history.
```

Repository evidence does not support a universal event kind such as database creation, boot completion, initialization, runtime activation, Begin, observation, evidence, or fact. The first lawful preserved event is whichever append-only event is actually recorded by a competent bounded surface under repository authority.

According to recurring repository evidence,

a Seed first becomes constitutionally aware of its own history by:

```text
reading/projecting/inspecting preserved history
through a bounded visibility surface
that preserves the boundary between event history, projection, cache, view,
evidence, fact, and answer.
```

It does not become aware of a constitutional biography merely by being created. Before the first preserved event, there is no preserved history to inspect; after the first preserved event, only bounded read/projection/inspection can make that history constitutionally visible.

Scout investigation complete.
