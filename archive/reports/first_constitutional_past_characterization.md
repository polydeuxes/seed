# First Constitutional Past Characterization

## Scope

This is exactly one bounded constitutional characterization. It recovers only recurring constitutional responsibilities, boundaries, unknowns, and confidence from repository evidence. It does not recover implementation, determine a startup sequence, determine a universal first event kind, introduce a Begin function, introduce a genesis framework, introduce lifecycle management, or recommend runtime behavior.

Repository authority wins. Implementation-specific event kinds remain outside the characterization.

## Reviewed evidence

### Constitutional discipline

- `constitution.md` states that the default state is unknown/uncommitted until observable evidence justifies movement.
- `constitution.md` states that only evidence may move a subject from Null toward a supported state.
- `constitution.md` distinguishes visibility from authority, projection from verification, observation from fact, and answer from mutation.
- `constitution.md` identifies the smallest self-sustaining inquiry loop as observation, bounded unknown, inquiry, evidence, supported transition, and next observation.

### Append-only history evidence

- `seed_runtime/events.py` identifies the event ledger as append-only runtime event history that feeds projection.
- `seed_runtime/events.py` records events by appending them to ordered in-memory and workspace indexes, and rejects duplicate event IDs.
- `seed_runtime/events.py` exposes list operations that return events in append order.
- `seed_runtime/state_patches.py` describes state patches as append-only ledger events and translates patch operations into ledger appends, but the first event kind remains operation-specific.

### Projection and read evidence

- `seed_runtime/state.py` describes state as projection from append-only events.
- `seed_runtime/projection_store.py` states that event ledgers own append-only historical events, while projection stores own reusable snapshots derived from those events.
- `seed_runtime/projection_store.py` identifies projection cache snapshots as derived from the event ledger, not as event history itself.
- `seed_runtime/inquiry_orientation.py` provides a read-only orientation example: it may read projected state and preserved notes, but it does not mutate projected state, append events, create facts, create goals, create plans, call providers, execute tools, or claim semantic authority.

### Boundary evidence

- The repository repeatedly separates preservation, projection, inspection, orientation, and authority. Event history is preserved by append-only ledger behavior. Projection derives state or snapshots from event history. Inspection/orientation surfaces may read projected material, but their output is bounded and read-only unless explicitly different.
- The repository does not support a universal first event kind. `StatePatchService` can append different operation-specific event kinds, and the event ledger accepts a `kind` supplied by the caller.
- The repository does not show that recognition of constitutional history is identical to projection. Projection is a derived state/snapshot mechanism; orientation/inspection may consume projected state but remains separately bounded and explicitly non-authoritative.

## Recurring responsibility of the first preserved event

According to recurring repository evidence, the first preserved event uniquely fulfills this constitutional responsibility:

> It converts the Seed's constitutional condition from no preserved history into a minimally preserved constitutional past by making the first lawful, append-only, ordered historical record available for later bounded derivation, inspection, orientation, and explanation.

The responsibility is unique because only the first preserved event can create the initial non-empty historical boundary. Later events can extend, qualify, correct through additional append-only evidence, or become material for projection and inspection, but they do not perform the first transition from no preserved event history to preserved event history.

This characterization intentionally does not say that the first event has a universal kind. The recurring responsibility belongs to its position in preserved history, not to an implementation-specific event label.

## Recurring boundaries

The first preserved event:

- begins preserved append-only history for its scope;
- establishes the first constitutional past that can be read later;
- provides the first historical input that projection or other bounded read surfaces may derive from;
- preserves a record rather than a total worldview;
- creates evidence that later inquiry can inspect, but does not make every interpretation of that evidence true.

The first preserved event does not:

- determine a universal event kind;
- define a startup sequence;
- instantiate a lifecycle manager;
- create a complete architecture, ontology, goal system, planner, or map;
- by itself produce projected state, verification, orientation, explanation, or self-history rendering;
- authorize diagnostic findings to become cluster truth;
- promote presentation vocabulary into constitutional law.

## Characterization of constitutional past

A constitutional past is the repository-supported condition in which at least one lawful append-only event has been preserved and can serve as historical evidence for later bounded reads. It is not merely memory, presentation vocabulary, projection cache state, or operator intuition. It is preserved history in an append-only historical record.

The first constitutional past begins when the first event is preserved. Before that boundary, the repository supports no preserved constitutional history. After that boundary, the Seed has at least one preserved historical fact of occurrence: an event exists in append order, with identity, kind, workspace, actor, payload, timestamp, and correlation fields as modeled by repository events.

The constitutional past remains bounded. It does not imply that the Seed has already interpreted the event, projected it into current state, inspected it, oriented around it, or explained it.

## Characterization of first constitutional self-history

First constitutional self-history is not the first event itself. It is the first bounded recognition or account that the Seed has a preserved constitutional past.

Recurring evidence supports this as a later read/inspection/orientation responsibility over preserved history, not as the event's own responsibility. A Seed first becomes capable of recognizing its constitutional past when both prerequisites are present:

1. at least one lawful preserved event exists, creating a constitutional past; and
2. a bounded read, inspection, orientation, replay, or explanation surface can access preserved history or derived projected state while preserving its authority boundary.

This capability is not necessarily projection. Projection may be one prerequisite or input for many current-state views, but the repository does not support equating recognition itself with projection. Recognition is better characterized as bounded inspection/orientation/explanation over preserved or derived evidence, subject to explicit authority limits.

## Investigation A: unique responsibility

The recurring responsibility is beginning preserved constitutional history. More precisely, it is preserving the first constitutional past as an append-only historical record that later bounded surfaces can read.

Confidence: high for the responsibility of beginning preserved append-only history; medium for the phrase "constitutional past" because it is a characterization built from recurring repository evidence rather than a named implementation primitive.

## Investigation B: pressure test of "creates constitutional history"

The proposition is partly supported only if "creates constitutional history" means "begins preserved history by making the first constitutional past available." It is too strong if it implies creating a complete history, a universal event kind, a startup framework, an ontology, or recognized self-history.

The better supported wording is:

> The first preserved event begins preserved constitutional history by preserving the first constitutional past.

Confidence: high.

## Investigation C: when Seed can first recognize a constitutional past

A Seed first becomes capable of recognizing that it has a constitutional past only after a preserved event exists and after some bounded read/inspection/orientation/explanation path can access that preserved or derived evidence.

Required prerequisites:

- preserved append-only event history is non-empty;
- the evidence remains readable in append order or through a derived state/snapshot that declares its dependency on event history;
- the recognizing surface preserves authority boundaries and does not silently turn visibility into truth.

Preserved boundaries:

- the first event creates the past but does not recognize it;
- projection may derive current state or snapshots but is not verification;
- orientation may relate material and help recognition but is not semantic authority;
- recognition does not mutate cluster truth unless a separate lawful append-only event records such a mutation.

Preserved unknowns:

- the repository does not prove a universal first recognition surface;
- the repository does not prove a universal timing sequence between first append, first projection, first inspection, and first explanation;
- the repository does not prove that recognition must be projection.

Confidence: medium-high.

## Investigation D: pressure test of "Recognition of constitutional history is projection"

The proposition is unsupported as stated.

Repository evidence supports projection as a derived-state mechanism from append-only events, while orientation/inspection examples are read-only surfaces with their own authority boundaries. Projection may enable some recognitions, especially recognitions about current projected state, but recognition of constitutional history is not constitutionally identical to projection.

The better supported boundary is:

> Recognition of constitutional history is bounded inspection, orientation, replay, or explanation over preserved history or derived evidence, with projection as a possible input rather than the constitutional identity of recognition.

Confidence: medium-high.

## Investigation E: sequence pressure test

Candidate sequence:

```text
No preserved history
↓
First preserved history
↓
Recognition that history exists
↓
Current constitutional orientation
```

### Supported transitions

- No preserved history to first preserved history is supported when the first lawful append-only event is preserved.
- First preserved history to possible recognition that history exists is supported only when a bounded read/inspection/orientation/explanation surface can access preserved or derived evidence.
- Recognition can contribute to current constitutional orientation when the orientation surface remains read-only and bounded by repository authority.

### Unsupported transitions

- The sequence is unsupported as a required startup sequence.
- The sequence is unsupported as a universal implementation order.
- The sequence is unsupported if "first preserved history" is treated as a universal event kind.
- The sequence is unsupported if recognition is equated with projection.
- The sequence is unsupported if current constitutional orientation is promoted into law without recurring implementation evidence.

### Preserved invariants

- Null persists until evidence justifies transition.
- Event history is append-only and ordered.
- Projection derives from history; it does not replace history.
- Visibility is not authority.
- Read-only orientation and inspection do not mutate cluster truth.
- Unsupported conclusions must remain explicit stops.

Confidence: medium-high for the supported transitions as a constitutional characterization; low for any attempt to use the sequence as implementation or startup architecture.

## Preserved unknowns

- The first event kind remains implementation-specific and not universal.
- The repository does not establish a universal first recognition mechanism.
- The repository does not establish that recognition must pass through projection rather than direct ledger inspection or another bounded read path.
- The repository does not establish a universal timing relationship between event append, projection, inspection, orientation, explanation, and current self-history.
- The repository does not establish that orientation vocabulary is constitutional law.

## Confidence

Overall confidence: medium-high.

The strongest evidence supports append-only preserved history, projection as derivation, and read-only authority boundaries. The weaker part is vocabulary: "constitutional past" and "constitutional self-history" are characterization terms rather than implementation primitives. Therefore this document preserves them as bounded constitutional responsibilities and conditions, not as runtime concepts.

## Final answer

According to recurring repository evidence, the first preserved event uniquely fulfills the responsibility of beginning preserved constitutional history: it preserves the first constitutional past as a lawful append-only historical record available for later bounded derivation, inspection, orientation, and explanation.

A Seed first becomes capable of recognizing its own constitutional past after at least one lawful preserved event exists and a bounded read, inspection, orientation, replay, or explanation surface can access that preserved history or derived evidence while preserving its authority boundary.

Characterization complete.
