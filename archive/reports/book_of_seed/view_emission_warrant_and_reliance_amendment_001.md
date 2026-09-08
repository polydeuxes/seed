# View Emission, Warrant, and Reliance Amendment 001

## Status

Canonical amendment record. This record documents the reconciliation that amended the Book after PR 1890; it is not independent constitutional authority apart from the clauses amended below.

## Book clauses examined

- `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `01-grammar-and-standing/constructors-and-production-authority.md`
- `01-grammar-and-standing/lenses-views-and-roads.md`
- `05-evidence-and-knowledge/testimony-and-established-fact.md`
- `05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `06-state-and-projection/events-facts-and-state.md`
- `06-state-and-projection/projection-and-current-state.md`
- `08-authority-communication-and-stopping/authority-scope.md`
- `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `08-authority-communication-and-stopping/refusal-and-non-performance.md`
- `concordance.md`
- `unresolved.md`
- `claim_normalization_and_fact_standing_recovery_001.md`
- `claim_normalization_and_fact_standing_amendment_001.md`
- `temporal_standing_and_relation_recovery_001.md`
- `temporal_standing_and_view_disclosure_amendment_001.md`

## Repository producers and consumers examined

- `seed_runtime/observations.py`: Observation ingestion compresses observed testimony, Evidence construction, optional Fact artifact construction, and fact event emission.
- `seed_runtime/evidence.py`: Evidence preserves source, payload, confidence, observed time, and optional source run material; it does not establish truth by being preserved.
- `seed_runtime/facts.py`: `Fact` is fact-shaped normalized claim material with provenance fields; `FactSupport` is projected support with support window, expiry, predicate semantics, and support kind.
- `seed_runtime/state.py`: current fact getters select projected support by predicate cardinality, aliases, expiry filtering, conflicts, and support ranking; `include_expired=True` reopens preserved material.
- `seed_runtime/state_views.py`: `build_observation_view` emits id, source type, summary, and supporting ids; `build_fact_view` emits compact rows from `FactSupport` or raw Fact fallback without support-window, expiry, projection as-of, establishment, or consumer-purpose disclosure.
- `seed_runtime/explanations.py`: explanation surfaces name current and competing beliefs and disclose support ids, source types, confidence, observed/support-window times, recursive facts, and conflicts.
- `seed_runtime/evidence_graph.py`: evidence-facing Views expose fact-shaped material, evidence nodes, unresolved references, derivation references, and explanations; they are provenance/explanation surfaces, not Fact establishment boundaries.
- `seed_runtime/confidence.py` and `seed_runtime/contradictions.py`: confidence and contradiction projections disclose support and conflict conditions but do not establish upstream truth or current applicability by rendering.
- `seed_runtime/projection_store.py`: persisted projection snapshots preserve cache and replay boundary material separately from source occurrence and consumer reliance.

## Operator-facing surfaces examined

- `scripts/seed_local.py --current-observations` renders `Current Observations` followed by summaries only; it does not show View class name, emitted assertion, observation time, Fact standing refusal, or currentness refusal.
- `scripts/seed_local.py --current-facts` with no subject renders `Current Facts` from `build_fact_view`; it does not disclose support-window, expiry, projection as-of, Fact establishment boundary, or consumer-purpose limits.
- `scripts/seed_local.py --current-facts SUBJECT PREDICATE` renders selected current fact values from current-fact getters rather than `FactView`; it can be read as present-facing but does not disclose the full current-standing contract in the line output.
- Explanation rendering presents `Current belief`, competing values, conflicts, support ids, evidence ids, source types, support confidence, and observation time; it is stronger as provenance disclosure than compact Views, but still does not turn explanation into establishment or universal current applicability.
- Evidence graph, unsupported fact, confidence, contradiction, diagnostic, and inquiry surfaces expose equivalent fact-shaped or evidence-shaped material under their own read-only contracts; their rendering must not be treated as FactView or current-standing emission solely because the material references facts.

## PR 1890 clauses preserved

- View selection responsibility, View assertion responsibility, and View disclosure responsibility remain distinct.
- The current `ObservationView` implementation is compact and read-only.
- The current `FactView` implementation is compact and usually consumes projected `FactSupport` rather than raw Fact rows.
- A compact View may be lawful when it refuses stronger reliance and keeps provenance reopenable.
- A View is not an establishment boundary merely because it is public or operator-facing.

## PR 1890 clauses corrected or qualified

- `ObservationView = compact observation navigation index and source-attributed testimony surface` is preserved only with a reliance limit: the lawful reliance is testimony occurrence and attribution in the emitted summary, not the testified proposition, Fact standing, verification, or current applicability.
- `FactView = compact projected normalized fact/support inventory` is accurate as a description of the current implementation surface, but not as the constitutional definition of a true standing-bearing FactView. A true FactView warrants bounded Fact standing for the proposition it emits.
- A View over Observation artifacts is not automatically an ObservationView, and a View over Fact artifacts or `FactSupport` is not automatically a FactView.
- A current-facing Fact View is not established by current selection alone; it must warrant present applicability under a declared projection, scope, purpose, as-of boundary, expiry/freshness treatment, conflict treatment, and Unknown limits.

## View kinds recovered

The Book now recovers View kind through a warranted combination of subject, input standing, formation method, emitted assertion, consumer purpose, disclosure contract, and reliance authority. For standing-bearing Views, the controlling dimension is the standing of the assertion Seed is warranted to emit, not the implementation artifact consumed by the builder. Navigation-only Views remain possible, but their kind is bounded by their navigation assertion and refusal of stronger standing.

The constitutionally real distinctions recovered in this pass are:

- navigation or inventory View: reliance on identity, availability, source location, faithful selection, or provenance pointers only;
- attributed testimony View: reliance that source or observation record reported the represented claim with preserved attribution;
- normalized representation View: reliance that Seed interpreted testimony into a canonical representation, not that the proposition is true;
- FactView in the strong constitutional sense: reliance that the proposition has bounded Fact standing;
- projected support View: reliance that a projection exposed support material under its method, not that current applicability is warranted;
- current-facing Fact View: reliance that the proposition is presently applicable under declared projection, scope, purpose, temporal boundary, conflict treatment, and Unknown limits;
- verification-facing View: reliance only on method-, scope-, evidence-, and time-bounded verification standing actually disclosed.

These distinctions do not require new classes, renamed classes, or public model repair in this pass.

## Reliance standings recovered

The recovered reliance grammar is branching rather than a single automatic ladder. Testimony, normalization, Fact standing, current applicability, and verification can support one another, but no step automatically promotes to the next.

- Testimony emission permits reliance that source S or record O reported claim C as attributed.
- Normalized representation emission permits reliance that Seed represented interpreted claim C as normalized representation N.
- Fact emission permits reliance that proposition C has bounded Fact standing under preserved evidence, scope, source authority, confidence, conflicts, and temporal limits.
- Current-standing emission permits reliance that proposition C is applicable for the declared present-facing purpose under the disclosed projection method, scope, as-of boundary, expiry/freshness treatment, conflict treatment, and Unknowns.
- Verified-standing emission permits reliance that C was confirmed under the disclosed verification method, target, scope, evidence, confidence, and time boundary.

## Surface table

| surface or View | input material | formation act | emitted assertion | warranted standing | operator reliance | standing not warranted | disclosure required | current compression or ambiguity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ObservationView` | projected `Observation` records plus evidence/fact ids found through observation provenance | `build_observation_view` sorts records and formats subject/predicate/value summary with source type and supporting ids | an observation-shaped record with source type and summary is projected and attributable to supporting ids | attributed testimony/navigation standing only | may rely that Seed is presenting an attributed observation summary and provenance pointers | testified proposition, normalized Fact standing, current applicability, verification, observation-time standing | source attribution, summary boundary, supporting ids, and explicit refusal or contract for stronger reliance | summary compresses source-reported C, Seed-normalized wording, Fact support links, and possible current wording; rendered CLI hides class name and limits |
| `FactView` current implementation | projected `FactSupport` or raw Fact fallback rows | `build_fact_view` selects support groups or fallback facts and emits compact subject/predicate/object/confidence/dimensions/provenance ids | projected fact/support-shaped material is visible under state-view formation | projected support/inventory standing; true Fact standing only when independently warranted by producer evidence | may rely on faithful compact projected material and supporting ids; may rely on Fact standing only if the View contract or provenance establishes it | universal truth, current applicability, verification, establishment time, support window, expiry/non-expiry, projection as-of | if called FactView in the strong sense, it must disclose bounded Fact standing; if only inventory, it must refuse Fact reliance | compresses normalized representation, Fact artifact/support material, possible Fact standing, and current selection; CLI title `Current Facts` strengthens ambiguity |
| `FactSupport` | projected support groups from facts | projection groups durable support or selects measurement current sample, computes confidence, support times, expiry, source types, support kind | support exists for a subject/predicate/value under projection method | projected support standing, not Fact establishment by identity | may rely on support grouping, support ids, confidence, support window, expiry fields as projection output | Fact standing, current applicability for a consumer, verification, complete provenance resolution | grouping method, support ids, source types, confidence, support times, expiry and predicate semantics when used for reliance | strong support details exist but are not all carried into current `FactView` |
| current-fact getters | state facts and support projection, alias resolution, predicate catalog, expiry filtering | `get_current_facts` / `get_fact_support` select unexpired supports and representative facts | selected current projected values for a subject/predicate are returned | projection-local current selection standing | may rely that selection followed repository projection rules | present-facing constitutional applicability, freshness sufficiency, operator-purpose fit, verification | projection method, scope, as-of/replay boundary, expiry/freshness, conflicts, Unknowns, consumer purpose if emitted as current-standing | subject-specific CLI renders values only, losing support and reliance limits |
| evidence-facing Views | Facts, Evidence, FactSupport, unresolved references, derivation links | evidence graph builders assemble nodes, links, fact evidence, references, explanations | provenance and evidence material are reachable for fact-shaped rows | evidence/provenance navigation and explanation standing | may rely on exposed evidence nodes, links, unresolved references, and derivation pointers | Fact establishment, truth, current applicability, resolved support for missing evidence | evidence identity, link relation, unresolved/derivation standing, confidence, source event/run where available | fact-shaped display can be mistaken for FactView unless contract remains visible |
| explanation surfaces | FactSupport, Facts, conflicts, aliases, evidence ids | `ExplanationBuilder.why` selects current/competing beliefs and recursive support explanation | current or competing belief explanation with support basis and conflict material | explanation/provenance standing, plus projection-local current-belief selection | may rely on reasons Seed exposes for a projected belief and reopen support | establishment by explanation alone, universal truth, consumer applicability beyond query, verification | support ids, evidence ids, source types, confidence, support-window times, conflicts, query boundary | stronger than compact Views but still named `Current belief`, so current-standing limits must remain recoverable |
| verification-facing Views | verification evidence, capability inventory, verification facts/support where present | verification inspection/inventory derives read-only status from local evidence and projected support | method/scope-bounded verification status or missing verification is exposed | verification standing only within disclosed method, evidence, scope, and time | may rely on the recorded verification status and blockers within that method | universal capability truth, future availability, current applicability after freshness limit, operational approval | method, target, evidence, scope, verification time/freshness, missing evidence, Unknowns, conflicts | some capability inventory rows derive from `FactSupport`; that does not make them FactViews |

## Compression findings

The current implementation compresses normalized claim representation, fact-shaped artifacts, support projection, possible Fact standing, and current selection in several places. The strongest compression is the `FactView` path: `build_fact_view` consumes projected support material but emits only subject, predicate, object, confidence, dimensions, a representative fact id, and supporting ids; the operator-facing no-argument `--current-facts` surface titles that output `Current Facts`. The implementation also permits a raw Fact fallback, so the builder cannot itself prove that every input has constitutional Fact standing. This means the current implementation can be characterized, but the smallest lawful repair cannot be chosen until each operator-facing emission is assessed against the amended contracts.

`ObservationView` is also compressed, but differently. It preserves observation id, source type, summary, and supporting ids. It is sufficient as a compact navigation and attributed testimony surface only if the operator is not invited to rely on Fact standing, currentness, verification, or the proposition itself without reopening provenance.

## Canonical files amended

- `01-grammar-and-standing/lenses-views-and-roads.md`
- `05-evidence-and-knowledge/testimony-and-established-fact.md`
- `06-state-and-projection/projection-and-current-state.md`
- `08-authority-communication-and-stopping/representation-emission-and-consumer-boundaries.md`
- `concordance.md`
- `unresolved.md`

## Required conclusions

Was PR 1890 correct to canonize `FactView` as a compact projected normalized fact/support inventory? It was correct as implementation characterization of the current public surface, but not as the constitutional definition of a true standing-bearing FactView.

What standing does a true FactView warrant? A true FactView warrants bounded Fact standing for the emitted proposition: evidence-backed, normalized, scoped, source-authorized, confidence- and conflict-aware Fact standing within temporal and provenance limits. It does not warrant universal truth, verification, or current applicability by identity.

What may an operator lawfully rely upon when presented with an `ObservationView`? The operator may rely on occurrence and attribution of testimony as represented by the compact observation summary and supporting ids. The operator may not rely on the testified proposition, Fact standing, current applicability, or verification without provenance reopening, consumer-local judgment, or separate explanation.

What may an operator lawfully rely upon when presented with a `FactView`? For a true constitutional FactView, the operator may rely that the emitted proposition has bounded Fact standing. For the current implementation named `FactView`, the operator may rely only on compact projected fact/support inventory unless the emission contract or reopened provenance establishes stronger standing.

Does the current implementation compress normalized claim material, Fact standing, and current applicability? Yes. The current `FactView`, no-argument `--current-facts`, subject-specific current-fact getters, and explanation wording each combine at least some of normalized representation, Fact artifact/support material, projection-local selection, and current-facing vocabulary. They do not all disclose the same standing.

Is the Book now sufficient to characterize the current View surfaces and recover the smallest lawful repair? Yes for characterization: it now distinguishes formation, emission, assertion, warrant, reliance, provenance navigation, Fact standing, and current applicability. The specific repair for each operator-facing emission remains unresolved and should be selected in a later implementation pass.

## Why production repair was not yet warranted

This pass was canonical reconciliation only. The repository evidence did not warrant modifying production code, public View models, builder inputs, projection selection, Fact promotion, operator formatting, assertion metadata, or timestamp fields. Several lawful repair families remain possible: narrowing an existing emitted assertion, making refusal text visible, adding disclosure through explanation or provenance, splitting overloaded surfaces, renaming a future public concept, changing producer admission, or preserving a surface with clearer contract. Choosing among them requires a focused inventory of current operator-facing emissions against the amended contracts.

## Unresolved questions

- Which current public and operator-facing View emissions fail the amended warrant, reliance, and temporal disclosure contracts, and which smallest repository-warranted repair mode fits each?
- Which current Fact producers, predicates, source types, and scopes establish constitutional Fact standing beyond weak source-relative observed claims?
- Which conflict-awareness, authority, corroboration, and verification thresholds are required for stronger Fact, live-state, current-facing, and verification claims?
