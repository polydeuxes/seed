# Constitutional View Selection Characterization

This is exactly one implementation characterization. It determines whether `ConstitutionalViewSelection` is an irreducible implementation-local ownership boundary or whether repository evidence supports decomposing Selection into smaller lawful responsibilities.

It does not implement Selection, redesign Selection, redesign Composition, redesign projections, recover another ownership boundary, invent semantic reasoning, invent matching algorithms, invent ranking, invent heuristics, invent runtime planning, mutate repository state, or create constitutional authority.

Repository authority wins.

## Implementation evidence reviewed

Review was limited to the requested evidence set:

- Constitutional View Selection Slice 001: `constitutional_view_selection_slice_001.md`.
- Constitutional Question Projection Characterization: `constitutional_question_projection_characterization.md`.
- Constitutional Capability Projection Characterization: `constitutional_capability_projection_characterization.md`.
- Constitutional View Composition implementation: `seed_runtime/constitutional_view_composition.py`.
- Constitutional View Composition slice evidence: `constitutional_view_composition_slice_002.md`.
- Constitutional Process View implementation: `seed_runtime/constitutional_process_view.py`.

Expansion was limited to implementation files where the requested documents directly named implemented evidence. `BoundedConstitutionalQuestion`, Question Projection characterization, `ConstitutionalReadModelContract`, `ReadModelViewRegistration`, Constitutional Process View, Constitutional Governance View, Constitutional Fidelity View, Capability Projection characterization, Constitutional View Composition, diagnostic visibility, JSON rendering, human rendering, event-ledger behavior, cluster-mutation behavior, and compatibility remain preserved.

## Input analysis

### Are Selection inputs already deterministic?

Yes. Repository evidence supports Selection inputs as already deterministic before Selection acts.

Question-side input is deterministic because the Question Projection characterization concluded that Question Projection is regenerated on demand from the already recovered immutable `BoundedConstitutionalQuestion` artifact. It exposes only already-owned bounded-question fields such as operator inquiry, bounded question text or identity, constitutional intent, scope status, uncertainty notes, and read-only / non-mutating flags. It does not mutate, persist independent state, own constitutional authority, select views, compose views, or author new question knowledge.

Capability-side input is deterministic because the Capability Projection characterization concluded that Capability Projection is regenerated on demand from immutable constitutional views and their registration metadata. It exposes only already-owned registration fields, view evidence, contribution records, summaries, Unknowns, refusals, remaining candidate views, compatibility answer, and mutation / ledger flags. It does not mutate, persist independent state, own constitutional authority, or author new capability knowledge.

The implementation side of Composition also confirms deterministic consumption after Selection. `ConstitutionalViewCompositionRequest` accepts explicit `requested_views`, purpose, and output format, while its docstring refuses heuristic selection, evidence discovery, runtime reasoning, authority recovery, planning, orchestration, and repository mutation. `build_constitutional_view_composition(...)` then validates each requested name against registered constitutional contracts and the local builder map before building immutable view artifacts.

### Does Selection consume only Question Projection and Capability Projection?

Yes, for the stabilized architecture characterized here.

Earlier Selection evidence described the future producer as accepting one bounded constitutional question and inspecting registered constitutional view metadata. The later projection characterizations refine both sides without changing ownership: the bounded question side becomes Question Projection, and the registered immutable view side becomes Capability Projection. Both projections are deterministic read-model projections over already-owned artifacts.

No reviewed implementation evidence requires a third owned input for Selection. Composition consumes selected view names after Selection. Individual constitutional views own their own content before Capability Projection. Bounded-question ownership remains before Question Projection. Diagnostics, CLI dispatch, JSON rendering, human rendering, event-ledger behavior, and cluster-mutation behavior are operational surfaces or outputs around existing views and composition; they do not add an unresolved Selection input.

### Do additional owned inputs remain unresolved?

No. Repository evidence does not expose any additional owned Selection input.

The remaining Unknown about whether future Selection should consume an in-memory projection, materialized transient artifact, or another deterministic representation is a representation Unknown, not a separate input owner. It preserves uncertainty about implementation form while preserving the deterministic input relationship:

```text
Question Projection
        +
Capability Projection
        ↓
ConstitutionalViewSelection
```

## Output analysis

### Does Selection own only `SelectedConstitutionalViews`?

Yes. Repository evidence supports exactly one Selection output artifact: `SelectedConstitutionalViews`.

Constitutional View Selection Slice 001 recovered `SelectedConstitutionalViews` as the artifact/helper for preserving Selection output only. The permitted contents are the bounded constitutional question as received, selected registered constitutional view names, registered metadata consumed for those names, unsupported or uncertain selection notes when relevance cannot be proven, and read-only / non-mutating boundary flags.

The same slice explicitly excludes composed view artifacts, constitutional findings, recovered evidence, reasoning traces, plans, orchestration state, implementation mutations, and authority claims from the selection artifact. Composition remains the consumer of selected view names and the owner of the later composed explanation.

### Does repository evidence support additional independently owned Selection artifacts?

No. Repository evidence does not support another independently owned artifact adjacent to `SelectedConstitutionalViews`.

The possible adjacent pieces already have owners:

- question content belongs to `BoundedConstitutionalQuestion` and is exposed deterministically through Question Projection;
- view contribution content belongs to immutable registered constitutional views and is exposed deterministically through Capability Projection;
- composed explanation content belongs to `ConstitutionalViewCompositionArtifact` after explicit selected names are supplied;
- diagnostic inventory and shape-audit visibility belong to diagnostic surfaces only if a future implementation exposes Selection operationally.

Adding another Selection-owned artifact would either duplicate question knowledge, duplicate capability knowledge, duplicate composition output, or invent a new authority surface unsupported by reviewed evidence.

## Ownership analysis

### 1. Does Selection mutate repository state?

No. Repository evidence characterizes Selection as a pre-composition read-only decision boundary. Selection may determine relevant registered views and preserve unsupported selection uncertainty, but it must refuse repository mutation. The adjacent deterministic projections are read-only and non-persistent, and Composition preserves `read_only=True`, `mutates_cluster=False`, and `writes_event_ledger=False` on its immutable artifact.

### 2. Does Selection own constitutional authority?

No. Selection does not own constitutional authority.

Question Projection does not author question knowledge or acquire authority beyond the bounded question artifact. Capability Projection does not author constitutional contribution knowledge or acquire authority beyond immutable constitutional views and registration evidence. Composition expressly composes already requested views without adding authority. Selection sits between those surfaces and can only select relevant registered views; it cannot author constitutional law, recover evidence, resolve Unknowns, or create authority.

### 3. Does Selection own implementation authority beyond selecting relevant registered views?

No. Selection owns no implementation authority beyond selecting relevant registered constitutional views for one bounded constitutional question and preserving unsupported selection uncertainty.

It does not own bounded-question production, capability authorship, read-model registration, constitutional view construction, composition, CLI design, diagnostic registration, JSON rendering, human rendering, recording, event-ledger writes, cluster mutation, planning, orchestration, semantic reasoning, ranking, or matching algorithms.

### 4. Can Selection itself be represented as a projection?

No. Selection itself cannot be represented as a projection under reviewed repository evidence.

Question Projection and Capability Projection are projections because every field they expose is already owned elsewhere and can be regenerated deterministically from immutable artifacts. Selection is different: it is the first boundary that produces a new implementation-local selected-view artifact from the two deterministic inputs. The selected set is not already owned by the bounded question, by registered immutable views, by Capability Projection, by Question Projection, or by Composition. Composition currently requires explicit requested view names and begins after selection has already happened.

Representing Selection itself as a projection would require the selected view set to already exist in upstream owned artifacts. Reviewed evidence shows the opposite: previous slices found selection compressed into the operator, future callers, or prompt construction. The repository recovered Selection precisely because no implementation-local owner already preserved the mapping from one bounded constitutional question to selected registered constitutional views.

## Decomposability analysis

Repository evidence does not support decomposing Selection into additional immediately adjacent ownership boundaries.

The immediately adjacent upstream responsibilities have already collapsed into deterministic projections:

- bounded-question content is exposed through Question Projection;
- registered immutable view capability content is exposed through Capability Projection.

The immediately adjacent downstream responsibility is already owned by Constitutional View Composition:

- selected registered view names are consumed to build one immutable bounded explanation from explicitly requested registered views.

Inside Selection, reviewed evidence supports only one unresolved implementation-local responsibility: choose the relevant registered constitutional views for one bounded constitutional question and preserve uncertainty when selection is unsupported. Splitting that responsibility further would require inventing one of the forbidden and unsupported surfaces, such as a matching algorithm owner, ranking owner, heuristic owner, semantic-reasoning owner, planner, orchestrator, evidence-discovery owner, or authority owner.

No reviewed implementation evidence identifies a separate artifact between deterministic input projections and `SelectedConstitutionalViews`. No reviewed evidence identifies another consumer between `SelectedConstitutionalViews` and Composition. No reviewed evidence shows a lawful intermediate state that would be independently owned rather than an implementation detail of Selection.

Therefore Selection remains irreducible from implementation evidence, not from conceptual preference. It is bounded by deterministic projections on the input side and by a single immutable selected-view artifact on the output side.

## Relationship analysis

Repository evidence supports the stabilized architecture:

```text
Question Projection
        +
Capability Projection
                ↓
ConstitutionalViewSelection
                ↓
SelectedConstitutionalViews
                ↓
ConstitutionalViewComposition
```

This relationship is supported because:

1. Question Projection is a deterministic read-model projection over `BoundedConstitutionalQuestion`.
2. Capability Projection is a deterministic read-model projection over registered immutable constitutional views and registration metadata.
3. Selection is the only remaining unresolved implementation-local boundary that can consume both deterministic inputs and produce selected registered view names for one bounded question.
4. `SelectedConstitutionalViews` is the single supported Selection-owned artifact.
5. Constitutional View Composition already consumes explicit registered view names and composes only those requested views into one immutable artifact, without selecting heuristically or creating authority.

This characterization does not determine matching algorithms, ranking, heuristics, semantic reasoning, runtime planning, or view-selection implementation behavior.

## Preserved boundaries and compatibility

Preserved:

- `BoundedConstitutionalQuestion`.
- Question Projection characterization.
- `ConstitutionalReadModelContract`.
- `ReadModelViewRegistration`.
- Constitutional Process View.
- Constitutional Governance View.
- Constitutional Fidelity View.
- Capability Projection characterization.
- Constitutional View Composition.
- Compatibility.

Expected compatibility answer:

```text
No.
```

Compatibility is preserved because this characterization adds only this document and changes no implementation, registration, bounded-question behavior, projection implementation, view shape, selection behavior, composition behavior, CLI behavior, JSON rendering, human rendering, diagnostic inventory, diagnostic shape audit, recording boundary, event-ledger behavior, or cluster-mutation behavior.

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
- Whether there is a distinct constitutional governance owner remains Unknown.
- Whether Question Grammar and Inquiry Navigation are distinct competencies remains Unknown.
- Whether governance relationships require any implementation topology remains Unknown.
- Whether Constitutional Fidelity should ever become an implementation-backed public surface remains Unknown.
- Whether future Selection should consume an in-memory projection, materialized transient artifact, or another deterministic representation remains Unknown.
- Whether future work should implement Capability Projection remains Unknown.
- Whether future work should implement Question Projection remains Unknown.
- Whether future work should implement ConstitutionalViewSelection remains Unknown.

## Confidence

Confidence is high. The reviewed repository evidence independently characterizes both upstream inputs as deterministic read-model projections, identifies no third Selection input, preserves one Selection output artifact, preserves read-only and non-authoritative boundaries, and leaves Composition as the existing downstream consumer of explicit selected view names. No reviewed evidence supports speculative decomposition into matching, ranking, heuristic, planning, semantic-reasoning, or authority-owning sub-boundaries.

## Classification

ConstitutionalViewSelection is an irreducible implementation-local ownership boundary.

Constitutional View Selection characterization complete.
