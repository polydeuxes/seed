# Constitutional Question Projection Characterization

This is exactly one implementation characterization. It determines whether the bounded constitutional question should expose a deterministic **Question Projection** for selection, or whether repository evidence requires another independently authored implementation boundary.

It does not implement Question Projection, redesign `BoundedConstitutionalQuestion`, redesign Constitutional View Selection, redesign Constitutional View Composition, invent semantic reasoning, invent matching heuristics, invent runtime planning, invent constitutional authority, or recover another ownership boundary.

Repository authority wins.

## Implementation evidence reviewed

Review was limited to the requested evidence set:

- Bounded Constitutional Question Slice 001: `bounded_constitutional_question_slice_001.md`.
- Constitutional View Capability Characterization: `constitutional_view_capability_characterization.md`.
- Constitutional Capability Projection Characterization: `constitutional_capability_projection_characterization.md`.
- Constitutional View Selection Slice 001: `constitutional_view_selection_slice_001.md`.
- Constitutional Process View Slice 001: `constitutional_process_view_slice_001.md`.

Expansion was not required. `BoundedConstitutionalQuestion`, `ConstitutionalReadModelContract`, `ReadModelViewRegistration`, Constitutional Process View, Constitutional Governance View, Constitutional Fidelity View, Constitutional View Selection, Constitutional View Composition, Capability Projection characterization, CLI behavior, diagnostic inventory, diagnostic shape audit, JSON rendering, human rendering, runtime compatibility, event-ledger behavior, and cluster-mutation behavior remain preserved.

## Projection construction analysis

Repository evidence supports Question Projection only as a deterministic selection-adjacent projection over the already recovered immutable `BoundedConstitutionalQuestion` artifact.

### Existing bounded-question fields that would deterministically produce Question Projection

`bounded_constitutional_question_slice_001.md` recovered the only adjacent artifact/helper as `BoundedConstitutionalQuestion`. If implemented later, that immutable artifact may contain only fields needed to preserve the bounded question for selection:

- the operator inquiry as received;
- the preserved bounded question text or bounded-question identity;
- constitutional intent as received or preserved;
- scope status;
- uncertainty notes when bounded scope cannot be established;
- read-only / non-mutating boundary flags.

Those existing recovered fields would deterministically produce Question Projection:

- **Question identity / text** projects from the preserved bounded question text or bounded-question identity.
- **Inquiry provenance** projects from the operator inquiry as received.
- **Constitutional intent** projects from constitutional intent as received or preserved.
- **Scope boundary** projects from scope status.
- **Selection uncertainty input** projects from uncertainty notes when bounded scope cannot be established.
- **Operational boundary flags** project from read-only / non-mutating boundary flags.

No projected field requires a second authoring surface beyond the recovered `BoundedConstitutionalQuestion` artifact.

### Existing owners of every projected question field

Every projected question field is already owned elsewhere if `BoundedConstitutionalQuestion` is implemented according to the recovered boundary:

- The operator inquiry as received is owned by the bounded-question artifact as preserved input, not by Selection.
- The preserved bounded question text or bounded-question identity is owned by the bounded-question artifact, not by Projection.
- Constitutional intent as received or preserved is owned by the bounded-question artifact, not by Projection.
- Scope status is owned by the bounded-question artifact, not by Projection.
- Uncertainty notes are owned by the bounded-question artifact, not by Projection.
- Read-only and non-mutating flags are owned by the bounded-question artifact and by the preserved repository boundary discipline, not by Projection.

Selection remains the consumer. It may accept one bounded constitutional question, inspect registered constitutional view metadata, determine which already registered views are relevant, preserve unsupported selection uncertainty, and produce one immutable `SelectedConstitutionalViews` artifact. It does not produce the bounded question and does not need Question Projection to author or own any question content.

### No newly authored constitutional knowledge

Question Projection introduces no newly authored constitutional knowledge.

The bounded-question characterization already constrained the future artifact to preserve one operator constitutional inquiry as one immutable bounded constitutional question artifact, including uncertainty where scope cannot be established. It explicitly refused selected view names, composed view artifacts, recovered evidence, invented evidence, runtime reasoning traces, plans, orchestration state, repository mutations, implementation ownership claims, and constitutional authority claims.

A projection over that artifact would only re-expose already-owned question fields in selection-adjacent form. It would not admit a new question, recover evidence, discover constitutional knowledge, infer intent, select views, compose views, resolve uncertainty, rank capabilities, or author constitutional authority.

### Required projection construction answers

1. Existing bounded-question fields that would deterministically produce Question Projection are the operator inquiry as received, preserved bounded question text or bounded-question identity, constitutional intent as received or preserved, scope status, uncertainty notes, and read-only / non-mutating boundary flags.
2. Every projected question field is already owned elsewhere: the recovered `BoundedConstitutionalQuestion` artifact owns the question content, scope, intent, uncertainty, and boundary flags; Selection owns later selected views; Composition owns later composition; registered views and Capability Projection own the view-side contribution evidence.
3. Question Projection introduces no newly authored constitutional knowledge. It only exposes already-preserved bounded-question fields for the selection boundary.

## Ownership analysis

### Does Question Projection mutate?

No. Repository evidence supports Question Projection only as a read-only derivation from `BoundedConstitutionalQuestion`. It writes nothing back to the question, registered views, selection artifact, composition artifact, event ledger, cluster state, CLI behavior, diagnostics, tests, or repository files.

### Does Question Projection persist independent state?

No. Repository evidence does not require a stored question-projection table, cache, ledger event, diagnostic record, cluster mutation, or independently maintained document of question knowledge. Independent persistence would create another representation of the bounded question and risk divergence from the owning `BoundedConstitutionalQuestion` artifact.

### Does Question Projection own constitutional authority?

No. The bounded-question characterization recovered a narrow implementation-local artifact boundary that preserves inquiry, intent, boundedness, and uncertainty while refusing authority creation. Projection cannot acquire constitutional authority that the bounded-question artifact itself refuses to create.

### Or is Question Projection regenerated on demand from `BoundedConstitutionalQuestion`?

Question Projection is regenerated on demand from `BoundedConstitutionalQuestion`. The lawful construction path supported by reviewed repository evidence is deterministic derivation from the bounded-question artifact's already-owned fields.

## Duplication analysis

Independent implementation ownership would duplicate question knowledge already assigned to `BoundedConstitutionalQuestion`:

- a separate Question Projection owner would repeat the operator inquiry;
- repeat the preserved bounded question text or identity;
- repeat constitutional intent;
- repeat scope status;
- repeat uncertainty notes;
- repeat read-only and non-mutating boundary flags.

That duplication would create a second authored representation of bounded constitutional-question content. If the bounded question changed, the independent projection owner could become stale unless maintained in lockstep. Repository evidence instead supports projecting from the owning source of truth: the immutable bounded constitutional question.

## Matching symmetry analysis

Repository evidence supports the requested symmetric architecture before Constitutional View Selection:

```text
Bounded Constitutional Question
                ↓
Question Projection

Immutable Constitutional Views
                ↓
Capability Projection

Question Projection
        +
Capability Projection
                ↓
ConstitutionalViewSelection
```

The support is structural, not algorithmic:

1. `BoundedConstitutionalQuestion` owns the already-bounded question fields immediately before selection.
2. Question Projection can expose those already-owned question fields in selection-adjacent form without authoring, mutating, caching, persisting independent state, or creating authority.
3. Immutable constitutional views own their own evidence, contribution records, Unknowns, refusals where present, and read-only boundaries.
4. Capability Projection can expose those already-owned view fields in selection-adjacent form without authoring, mutating, caching, persisting independent state, or creating authority.
5. Constitutional View Selection remains the later relevance decision. It is not redesigned by this characterization.

This characterization determines only that the repository supports the symmetry. It does not determine matching algorithms, ranking, heuristics, semantic reasoning, runtime planning, or view-selection behavior.

## Preserved boundaries and compatibility

Preserved:

- `BoundedConstitutionalQuestion`.
- `ConstitutionalReadModelContract`.
- `ReadModelViewRegistration`.
- Constitutional Process View.
- Constitutional Governance View.
- Constitutional Fidelity View.
- Constitutional View Selection.
- Constitutional View Composition.
- Capability Projection characterization.
- Compatibility.

Expected compatibility answer:

```text id="g7m2xp"
No.
```

Compatibility is preserved because this characterization adds only this document and changes no implementation, registration, bounded-question behavior, view shape, projection implementation, selection behavior, composition behavior, CLI behavior, JSON rendering, human rendering, diagnostic inventory, diagnostic shape audit, recording boundary, event-ledger behavior, or cluster-mutation behavior.

## Preserved Unknowns

The following Unknowns remain preserved and are not resolved by this characterization:

- Whether every constitutional inquiry starts only as Pressure remains Unknown.
- Whether every Recovery requires a separate Cross-Examination artifact remains Unknown.
- Whether every Cross-Examination requires a separate Completion Audit remains Unknown.
- Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains Unknown.
- Whether a single named constitutional process owner exists remains Unknown.
- Whether Asymmetrical Question Construction is a distinct constitutional responsibility or only pressure inside or adjacent to admission remains Unknown.
- Whether future implementation should introduce question construction before exact `QuestionFamily` admission remains Unknown.
- Whether bounded ask should ever require inquiry orientation before selected dispatch remains Unknown.
- Whether future Selection should consume an in-memory projection, materialized transient artifact, or another deterministic representation remains Unknown.
- Whether future work should implement Capability Projection remains Unknown.
- Whether future work should implement Question Projection remains Unknown.

## Confidence

Confidence is high. The reviewed implementation evidence directly identifies the recovered owner of every field a Question Projection would expose, directly preserves read-only and non-mutating boundaries, and directly refuses independent constitutional authority. No reviewed evidence requires mutation, persistence, independent implementation state, or independent constitutional authorship for Question Projection.

## Classification

Question Projection is a deterministic read-model projection.

Question Projection characterization complete.
