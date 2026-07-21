# Claim Normalization and Fact Standing Recovery 001

## Recovery scope

This is a report-only constitutional recovery. It does not rename `Fact`, create a `NormalizedClaim` model, change schemas, change ingestion, change projection, change tests, rewrite canonical Book chapters, or begin temporal canonization.

Primary finding: the current evidence supports a combined answer closest to Candidates B, C, and D. The Book now distinguishes testimony from established fact and says fact standing requires explicit ingestion, support, normalization, and conflict-aware establishment. The older claim-centric reconciliation intentionally weakened `Fact` to prevent truth-centric ontology and often used `Fact` for a normalized, provenance-backed claim. The implementation still compresses construction, normalization, evidence linking, and establishment in several producer paths, while direct construction and replay can create fact-shaped artifacts without proving the constitutional production boundary.

Therefore the smallest recovered boundary is:

```text
claim expression
  -> interpretation and normalization
  -> normalized claim representation
  -> support-bound, scoped, conflict-aware establishment act
  -> Fact with bounded fact standing
  -> projection/current selection, if any
  -> verification, if any
```

Unknown remains where the Book does not specify exact conflict-handling mechanics, source-authority thresholds, or whether every public `Fact` construction path is a lawful establishment boundary.

## 1. Vocabulary lineage

| term | original role | reason for introduction | governing reconciliation | later reuse | current standing |
| --- | --- | --- | --- | --- | --- |
| Claim | Central semantic proposition that can be reported, supported, normalized, selected, assessed, contradicted, verified, explained, and communicated. | To prevent Seed from being fact-centric or truth-centric while preserving what is being said across objects. | `docs/foundational_ontology_reconciliation.md` establishes claim-centric ontology; `docs/claim_strength_and_assertion_semantics_reconciliation.md` defines claim as the proposition, not a storage object. | Reused across ontology, knowledge representation, state/projection, and Book testimony language. Repetition is reuse, not independent warrant. | Semantic content / proposition, not necessarily a separate constitutional artifact subject. Book asks about source claims and testimony but does not canonize a `Claim` model as a durable kind. |
| normalized claim | Canonical subject/predicate/value/dimensions/time/provenance representation of a claim. | To say `Fact` is a representational shape and support-bearing record, not objective truth. | `docs/corroboration_and_fact_promotion_reconciliation.md` says facts normalize and promotion moves evidence-backed input into a normalized fact claim. | Later docs often copy the formula "Facts are normalized claim forms." | A representation state, not by itself standing. The Book's artifact-standing chapter prevents treating shape or dataclass existence as constitutional standing. |
| Fact | Implementation model and normalized, provenance-backed claim form. | Originally central noun; weakened to avoid `Fact = truth about the world`. | `docs/foundational_ontology_reconciliation.md` and `docs/claim_strength_and_assertion_semantics_reconciliation.md`. | State, confidence, evidence graph, contradiction, explanation, and views all consume `Fact` artifacts. | Both an artifact shape and, when lawfully produced, a bounded fact-standing representation. Book warrants "established facts" and says facts carry supported claims, but implementation sometimes only proves artifact shape. |
| fact promotion | Movement from evidence-backed input into a normalized fact claim. | To distinguish observation preservation, evidence existence, fact representation, current selection, and verification. | `docs/corroboration_and_fact_promotion_reconciliation.md`. | In code, `ObservationIngestor` optionally suppresses promotion and otherwise emits `fact.observed` / `fact.inferred`. | Ambiguous term. Historically implementation terminology; constitutionally it must be read as a production/establishment boundary only when support, scope, and conflict-aware constraints are preserved. |
| fact standing | Bounded standing of a normalized claim that Seed may treat as an established fact under scope and support limits. | Exposed by Book recovery to separate testimony from established fact. | Book chapter `testimony-and-established-fact.md`. | State/projection Book chapters use "established facts" as replay material. | Warranted by the Book as distinct from testimony, current standing, verification, and truth. Exact thresholds remain partly Unknown. |
| current fact | A projection-selected current support/value, not the same thing as a historical fact. | To prevent preserved history from being read as live state. | `docs/claim_strength_and_assertion_semantics_reconciliation.md`; Book `projection-and-current-state.md`. | `FactView` builder renders current projected claims from `FactSupport`, and State exposes `get_current_facts`. | Projection-local characterization. Current standing requires a later consumer/projection boundary; it is not inherent in `Fact`. |
| verified fact | A scoped verification claim or verification-produced fact-shaped record. | To avoid treating confidence, corroboration, or selection as verification. | `docs/claim_strength_and_assertion_semantics_reconciliation.md`; verification-related runtime tests use `capability_verified`. | Capability verification producers append `fact.observed` with verification predicates. | Not universal truth. Verification standing requires method, scope, and time; current code can represent verification claims as Facts, but the stronger verification boundary is consumer-specific. |

### Historical reconciliation audit

The earlier chain weakened `Fact` because Seed needed a claim-centric ontology: observations report, evidence preserves provenance, claims are central, facts normalize claims, projections communicate selected knowledge, and reasoning qualifiers do not become truth. "Normalized claim" was intended to prevent direct equivalence between fact artifacts and truth, current state, or verification. Normalization was treated as semantic canonicalization into subject/predicate/value/dimensions/time/provenance shapes. `fact promotion` was mostly implementation terminology for converting evidence-backed inputs into normalized fact claims; it was not allowed to imply current belief or verified truth. No inspected historical reconciliation conclusively established `Fact` as an independent constitutional kind with all standing mechanics; the Book later introduced stronger standing grammar. Later repeated wording should be traced back primarily to the foundational ontology and corroboration/promotion reconciliations.

## 2. Producer inventory

| producer | input standing | normalization | support | establishment | output | claimed standing | classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ObservationIngestor.ingest_many` | `Observation` source-attributed record. | Copies subject, predicate, value, dimensions, observed time, expiry. | Always creates `Evidence` from observation; `Fact` links one evidence id unless suppressed. | No independent conflict handling or authority check in the method; compresses evidence creation and fact event emission. | `observation.observed`, `evidence.observed`, optional `fact.observed` / `fact.inferred`. | Observed or inferred Fact artifact with bounded source confidence. | Lawful combined responsibility for weak source-relative facts when claim strength does not exceed the observation; otherwise potentially normalized-claim-named-Fact. |
| `ObservationIngestor.observation_to_evidence` | Observation testimony. | Payload preserves the same proposition plus metadata. | The evidence itself is provenance/support material. | None. | `Evidence`. | Evidence, not Fact. | Lawful testimony/evidence preservation. |
| `ObservationIngestor.observation_to_fact` | Observation plus Evidence. | Direct subject/predicate/value/dimensions mapping. | Exactly the supplied evidence id. | Constructor validates source type/confidence; no contradiction review. | `Fact`. | Observed Fact artifact. | Boundary compression; constitutionally safe only for weak, source-relative observed facts. |
| Direct `Fact(...)` in production and tests | Caller-supplied assertion, sometimes fixture/replay material. | Whatever caller provides. | Optional `evidence_ids`; many tests provide none or synthetic ids. | Constructor validates known source type and confidence range only. | Fact-shaped object. | Depends on caller. | Fixture, trusted reconstruction, or unclear; constructor availability is not lawful production. |
| Event replay in `StateProjector` | Recorded `fact.observed` / `fact.inferred` event payload. | Rehydrates `Fact(**data)`. | Preserves linked evidence ids if present. | Trusts prior event; does not re-establish fact warrant. | State facts. | Projected historical fact material. | Trusted reconstruction of prior standing, not original establishment. |
| Inference producers | Existing facts/rules. | Produce derived subject/predicate/value facts with `inferred=True`, source fact/rule links. | Source fact or rule lineage; may have no direct evidence ids. | Rule/catalog boundary and source links; conflict handled later by projection. | `fact.inferred` / inferred `Fact`. | Inferred bounded Fact artifact. | Lawful if rule support is within scope; evidence-to-fact and fact-to-inference compressed. |
| Relationship-related normalization | Fact rows consumed by relationship catalog/projection. | Fact predicate/value becomes edge semantics. | Source fact id/confidence. | Catalog determines relationship validity; graph validation flags issues. | `EntityRelationship` / issues. | Relationship projection, not Fact standing. | Projection-local characterization; not every relationship claim becomes a new Fact. |
| Repository/documentation observation producers | Repository artifacts and text-derived observations. | Often turn existence/structure/document claims into observation-like or repository-artifact records. | File/testimony/provenance refs. | Depends on producer-specific warrant. | Observations, artifact facts, reconciliation docs. | Repository-local claim standing. | Mixed; do not infer Fact standing from claim family. |
| Projection snapshots and summaries | Built State. | Serialize projected material. | Derived from replay. | Snapshot boundary explicitly non-mutating. | Cache/read-model artifacts. | Projection visibility only. | Implementation convenience; not new fact establishment. |

## 3. Consumer inventory

| consumer or View | required input | standing relied upon | whether it needs normalization only | whether it needs established Fact standing | forbidden inference |
| --- | --- | --- | --- | --- | --- |
| `ObservationView` | `State.observations` plus related evidence/fact ids for support display. | Source-attributed testimony / observation occurrence. | No; it summarizes raw observation proposition. | No. | Do not infer Fact promotion, truth, current state, or verification. |
| Evidence Graph / `FactEvidenceView` | `State.facts`, `State.evidence`, `FactSupport`. | Fact artifact plus resolved/unresolved support references. | Needs normalized fact shape. | It reports "Seed has this fact" but can expose unsupported facts. | Do not infer that unsupported or unresolved support establishes standing. |
| Confidence projection | Facts, evidence graph, contradictions. | Support/integrity signals over fact artifacts. | Needs normalized shape for grouping. | Can operate on unestablished artifacts; flags unsupported. | Confidence is not truth, authority, currentness, or verification. |
| Contradiction detection | Facts and optional evidence graph. | Comparable normalized predicates/dimensions and evidence links. | Yes. | Does not require final establishment; detects incompatible projected facts. | Contradiction does not delete facts or prove falsehood. |
| `FactView` | `State.fact_supports` or raw facts fallback. | Current projected claims/support groups. | Needs normalized shape and support aggregation. | It implies projection-selected fact material, not necessarily original establishment proof. | Do not read as universal truth, verified live state, or exhaustive history. |
| `State` current getters / projector | Event replay facts and support records. | Historical facts as projection input; current selection rules for outputs. | Needs normalized facts. | Relies on fact records as replay material but selection is separate. | Do not collapse Fact into current standing. |
| ExplanationBuilder | FactSupport and Facts. | Current beliefs and competing beliefs from projected supports. | Needs normalized shape plus support details. | Relies on projected fact/support material. | Explanation does not verify the underlying world. |
| Capability/verification consumers | Fact predicates such as package installed and capability verified. | Predicate-specific facts and expiry. | Needs normalized predicate/value. | Needs sufficient scope-specific facts. | `capability_verified` fact is not universal verification outside method/scope/time. |
| Projection store/summary views | Projected State. | Snapshot/read-model validity and freshness. | Needs serialized projected shape. | No new fact standing. | Cache existence does not create truth or mutation authority. |

## 4. Boundary comparison

| boundary | what it is | minimum warrant | standing before | standing after | forbidden stronger inference |
| --- | --- | --- | --- | --- | --- |
| claim expression | Natural-language, payload, diagnostic, or operator assertion. | Identified speaker/source and content. | Uninterpreted or attributed assertion. | Source-attributed claim expression. | Truth, support, normalization. |
| normalized claim representation | Canonical subject/predicate/value/dimensions/time/scope representation. | Interpretation and canonicalization rule. | Claim expression/testimony. | Normalized representation. | Support, establishment, currentness. |
| Fact artifact | Public `Fact` shape with id, subject, predicate, value, dimensions, evidence ids, source type, confidence, observed time, inference fields. | Constructor/schema validity. | Caller assertion. | Fact-shaped artifact. | Lawful production or standing solely from shape. |
| Fact standing | Bounded fact established from normalized claim with support, scope, and applicable production boundary. | Evidence support; source-relative scope; conflict-aware establishment; no claim-strength escalation. | Supported or candidate normalized claim. | Established bounded fact. | Current standing, verification, universal truth. |
| selected current standing | Projection/consumer-selected current material under freshness/cardinality/conflict rules. | Projected facts/supports plus consumer rules and Unknown/conflict preservation. | Historical fact/support material. | Current view or bounded current standing for that consumer. | Historical truth, universal current truth, verification. |
| verified standing | Scoped verification confirmation through method and time. | Verification method, scope, time, provenance. | Candidate/current/historical claim. | Verification claim/standing under its method. | Timeless truth, independence, all-scope validity. |

## 5. Compression ledger

| compression | location | classification | recovery note |
| --- | --- | --- | --- |
| Observation -> Evidence | `ObservationIngestor.observation_to_evidence` | Lawful combined responsibility | Preserves attributed testimony and provenance without fact standing. |
| Evidence -> Fact | `ObservationIngestor.observation_to_fact` and `ingest_many` | Lawful for weak source-relative observed facts; Unknown/unsafe for stronger claims | No local conflict or authority check; safe only when claim strength is scoped to the single observation. |
| normalization -> establishment | `Fact(...)` creation and fact event emission | Historical residue / implementation convenience | Constructor validates shape; Book requires establishment boundary. |
| Fact -> current selection | `build_fact_view`, State support projection, ExplanationBuilder | Lawful projection responsibility if read as view material | FactView uses support projection/current projected claims and must not imply truth. |
| Fact -> verification | Capability verification facts/tests | Implementation convenience | Verification is represented as a predicate; standing depends on verification method/scope/time, not the word Fact. |
| Event replay -> Fact | `StateProjector` rehydrates fact event payloads | Trusted reconstruction | Replay reconstructs prior event material; it does not newly justify the original promotion. |
| Support aggregation -> stronger claim | `FactSupport`, confidence, contradiction, current selection | Lawful when projection-local; unsafe if read as verification | More support increases confidence/selection; corroboration is not proof or authority. |

## 6. View distinction

| View | source stores | builder | public fields | support references | ordering/filtering/freshness | constitutional comparison |
| --- | --- | --- | --- | --- | --- | --- |
| `ObservationView` | `State.observations`, plus evidence/fact ids for support display. | `build_observation_view`. | observation id/type, textual summary, supporting event ids. | Includes observation id, evidence ids whose payload references it, and fact ids linked to those evidence ids. | Sorted by subject, predicate, value, id; no current support aggregation; no expiry filtering. | Exposes source-attributed testimony/observation occurrence. It can exist without Fact promotion. |
| Evidence-facing View | `EvidenceGraph`, especially `FactEvidenceView`. | `build_evidence_graph`, `build_fact_evidence_view`. | fact id, subject, predicate, object, confidence, evidence nodes, unresolved/derivation refs, supporting ids, explanation. | Resolved evidence nodes, unresolved evidence refs, source fact derivation refs. | Ordered by fact subject/predicate/value/id and node keys. | Exposes why a fact artifact is linked, unsupported, or unresolved. It is not an ObservationView and not current standing. |
| `FactView` | `State.fact_supports` or raw facts fallback. | `build_fact_view`. | fact id, subject, predicate, object, confidence, dimensions, supporting event ids. | Evidence ids and source fact ids from supporting facts. | Sorted by subject, predicate, value, dimensions, support ids; uses support projection, not raw append-only rows. | Exposes normalized projected fact/support material. It may reflect established standing if producer was lawful, but the view itself is presentation/projection, not establishment. |
| current-standing View | No single named constitutional view; implemented by State current getters, support projection, FactView, explanations, and summaries. | State finalization/support selection and read-model builders. | Current facts/supports/beliefs/counts depending on consumer. | FactSupport supporting fact ids and evidence ids via downstream builders. | Freshness, expiry, cardinality, confidence, support count, and conflict rules are projection-specific. | Projection/consumer boundary, not inherent Fact standing. |
| verification View | No general named view inspected. Verification is represented through predicates and capability inspection consumers. | Capability verification and projected-state consumers. | Predicate-specific verification facts/statuses. | Evidence/facts per producer. | Expiry/freshness may matter for verification facts. | Verification standing is scoped to method/time; not universal truth and not supplied by FactView alone. |

Answers to the cross-examination: `ObservationView` exposes claims as source-attributed testimony. `FactView` exposes projected normalized fact/support material, not merely raw normalized claims, because it is built from `FactSupport` when available. `FactView` can imply that a fact artifact crossed a producer boundary, but it does not prove the boundary was lawful. The same proposition can appear in both: once as observation testimony and once as a source-relative fact. A `FactView` can safely represent a one-observation source-relative Fact only when the proposition remains scoped to what the observation directly supports. Operators distinguish the views through observation id/type/summary versus fact id/subject/predicate/object/confidence/dimensions/supporting evidence ids.

## 7. Reconciliation with the Book

The existing Book warrants both under different contexts, but not conclusively enough to repair implementation semantics without a later pass.

* The Book warrants Fact as established standing when it says the constitutional subject is the boundary between source claim/diagnostic finding and a fact with established standing, and that fact standing requires explicit ingestion, support, normalization, and conflict-aware establishment.
* The Book also preserves older normalized-claim grammar when it says facts carry supported claims and state projections consume established facts.
* The Book does not answer exact source-authority thresholds, whether every one-observation Fact is lawful, or exact conflict-aware establishment mechanics.
* The Book clearly rejects using artifact shape, public dataclass availability, projection visibility, or cache existence as constitutional standing by identity.

Question-by-question Book audit:

| Book question | recovered answer |
| --- | --- |
| Does Claim name a constitutional subject or only semantic content? | Mostly semantic content/testimony; no durable `Claim` kind is canonized in inspected chapters. |
| Does normalization produce a new constitutional subject? | Unknown as a subject; it produces a canonical representation, not standing by itself. |
| Does Fact name a representation shape, a standing, or both? | Both under different contexts: implementation shape and, if lawfully established, bounded standing. |
| What establishes Fact standing? | Explicit ingestion, support, normalization, conflict-aware establishment, and applicable boundary. Exact algorithm Unknown. |
| Can one Observation establish a weak source-relative Fact? | Historical docs say yes when claim strength does not exceed support. Book does not explicitly forbid it; current implementation assumes it. |
| Must all Facts preserve source-relative claim strength? | Yes as a safety invariant; stronger claims need stronger support. |
| Can fact establishment occur without independent corroboration? | Yes for weak scoped claims per governing promotion reconciliation; Unknown for broader claims. |
| Can a Fact be contradicted, stale, or unselected while retaining historical fact standing? | Yes in historical docs and consistent with Book projection/current-state distinction. |
| Does current standing require a later consumer/projection boundary? | Yes. |
| Does the Book distinguish fact occurrence, fact establishment, and fact visibility? | Partly. It distinguishes events, facts, projected material, visibility, and current standing; exact occurrence/establishment mechanics remain incomplete. |

## Candidate model determination

* Candidate A is insufficient: current Book language says fact standing requires more than normalization, and implementation consumers distinguish support, contradiction, projection, and verification.
* Candidate B is constitutionally strongest: it preserves Claim -> normalized representation -> supported/conflict-aware establishment -> Fact standing.
* Candidate C describes much of the current ingestion implementation: Observation + Evidence are compressed into a source-relative Fact for direct weak claims.
* Candidate D is also true operationally: direct construction, fixture facts, replay, inference, and promotion paths use the same `Fact` class with different degrees of warrant.

## Fact-strength ladder audit

These are not recovered as separate constitutional kinds in this pass. They are standing effects or projection-local characterizations over claims/facts:

| candidate standing | producer | minimum evidence | scope/time | conflict treatment | consumer | forbidden stronger inference | classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| normalized claim | normalizer or Fact constructor | interpretation only | supplied fields | none required | Fact producers, projections | fact standing | representation state |
| source-relative observed fact | ObservationIngestor | one observation/evidence record | source/vantage/observed_at | later detection | FactView, EvidenceGraph, State | broad truth/current state | bounded Fact standing if scoped |
| evidence-supported fact | ObservationIngestor or direct event with evidence ids | linked evidence | support scope | confidence/contradiction views later | EvidenceGraph, Confidence | verification | standing effect |
| corroborated fact | support aggregation | multiple compatible supports | support-group scope | conflicts visible | State support, confidence | proof/truth | support characterization |
| historical fact | recorded/replayed fact event | prior fact event | observed_at/event history | may be stale/contradicted | State replay/history | current truth | standing effect |
| current selected fact | State projector/read view | projected supports/freshness | projection time/current rules | selection/conflict rules | FactView, explanations | verification | projection-local |
| verified fact | verification producer/predicate | method-specific verification evidence | verification scope/time | consumer-specific | capability verification consumers | universal truth | method-scoped standing/effect |

## Direct construction audit

`Fact` is public and direct construction is common in tests, fixtures, and helper producers. This is acceptable as fixture or trusted reconstruction when the test is about downstream projection behavior. It is not constitutional proof that construction itself establishes fact standing. Direct construction in production must be classified by caller boundary:

* Lawful establishment boundary: only when caller has already performed support, scope, and authority checks appropriate to the claim.
* Trusted reconstruction: replay from `fact.observed` / `fact.inferred` event payloads.
* Fact-shaped fixture only: many tests that populate `State.facts` directly.
* Unwarranted promotion: any direct construction that asserts a stronger claim than its evidence supports.
* Unclear: imported/repository/inference paths until each producer's specific warrant is audited.

## Claim producers and consumers outside `Fact`

| family | proposition | asserter | normalization | support required | becomes Fact? | view standing |
| --- | --- | --- | --- | --- | --- | --- |
| Documentation claims | Architecture/constitutional assertions. | Authors/operators/reconciliations. | Markdown sections/tables. | File lineage and governing reconciliation. | Usually no. | Documentary testimony unless Book/adopted reconciliation governs. |
| Existence claims | Artifact/entity exists. | Source adapters, repository scans, operators. | subject/predicate/value or artifact records. | Observation/source evidence. | Sometimes. | Observation, repository-local, or Fact depending on producer. |
| Structure claims | Code/document structure. | Structural probes/tests. | artifact/path/symbol representations. | File/test evidence. | Sometimes via repository artifacts; not automatically. | Diagnostic/repository standing. |
| Ownership claims | Responsibility/owner relation. | Docs, catalogs, operators, tests. | relationship/claim fields. | Stronger evidence than import/mention. | Sometimes relationship/fact-shaped. | Must not infer from visibility alone. |
| Relationship claims | Edges between entities/artifacts. | Catalog/projector/producers. | relationship projection. | Source fact/catalog support. | Often not a new Fact; may derive relationships from Facts. | Relationship projection standing. |
| Diagnostic findings | Tool/audit findings. | Diagnostic surface. | diagnostic rows/records. | diagnostic-run scope. | Should not become cluster Fact unless separately warranted. | Diagnostic testimony. |
| Operator assertions | Intent, desired config, claims. | Operator. | observation/evidence/fact if ingested. | Authority/scope and claim strength. | May become weak source-relative Fact. | Operator-attributed standing. |
| Observation payload propositions | Source reported subject/predicate/value. | Observation source. | Observation fields and optional Fact fields. | One evidence record. | Often optional. | ObservationView testimony; FactView if promoted. |
| Evidence-supported claims | Payload supports considering a proposition. | Evidence source. | Evidence payload links. | Provenance. | Only through promotion/establishment. | Evidence-facing view. |
| Explanation claims | Why Seed selected/believes. | ExplanationBuilder. | BeliefExplanation/FactExplanation. | Projected support. | No. | Explanation of view, not new truth. |
| Projection-local assertions | Current selected state/support. | Projector/read view. | support/current view rows. | Facts/supports/projection rules. | No new Fact by identity. | Projection-local current standing. |
| Verification claims | Method says capability/condition verified. | Verification producer. | predicate such as `capability_verified`. | Verification method evidence. | Often represented as Fact. | Scoped verification standing only. |

## Required conclusion

### Is Claim the semantic proposition while Fact is one possible standing-bearing representation of that proposition?

Yes, with a caveat. Historical docs establish Claim as the central proposition and not identical to any storage object. The Book does not canonize a separate `Claim` artifact kind in the inspected chapters. A `Fact` is one possible normalized, support-bearing representation of that proposition; when lawfully produced it carries bounded fact standing.

### Does normalization alone establish Fact standing?

No. Normalization produces a canonical representation. The Book requires explicit ingestion, support, normalization, and conflict-aware establishment for fact standing. Artifact shape, constructor availability, view visibility, or repeated wording do not establish standing by identity.

### What exact evidence, support, scope, conflict, and production conditions currently establish a Fact?

Currently established by implementation only in a compressed and uneven way:

1. `ObservationIngestor` creates Evidence from an Observation and then creates a Fact with one evidence id, source type, confidence, observed time, dimensions, and optional expiry.
2. That production is constitutionally sufficient only for weak source-relative claims whose strength does not exceed the observation.
3. Broader claims require stronger or specific support; corroboration is required only when claim strength demands it.
4. Conflict handling is mostly projection-time detection/selection, not pre-promotion establishment.
5. Direct constructor use establishes only fact shape unless a caller has an external warrant or is replaying prior recorded fact material.

Exact authority thresholds and conflict-aware preconditions remain Unknown.

### Is current `ObservationIngestor` producing Facts, normalized claims named Facts, or a mixture depending on claim scope?

A mixture depending on claim scope. For direct source-relative observations such as "source S reported predicate P/value V at time T," it lawfully produces weak bounded Facts by combining observation, evidence, normalization, and fact event emission. If the observation predicate/value is read as a stronger external-world, current, verified, or authority-heavy claim, then the same artifact is only a normalized claim named `Fact` until a separate establishment boundary is recovered.

### Does `ObservationView != FactView` reflect a constitutional standing distinction or only a presentation distinction?

It reflects both, but the constitutional distinction is conditional. Implementation-wise they are different read views with different source stores and fields. Constitutionally, `ObservationView` exposes attributed testimony; `FactView` exposes projected normalized fact/support material. That distinction can represent different standing for the same proposition. However, `FactView` alone does not prove lawful fact establishment, because direct construction and replay can supply fact-shaped artifacts without showing the original warrant.

### Can Seed safely restore the word “Fact” as constitutional vocabulary without returning to truth-centric ontology?

Yes, if and only if `Fact` is restored as bounded established standing over a normalized, supported, scoped claim, not as objective truth, current truth, verified truth, or universal ontology. The Book already contains the required safeguards: artifact shape is not standing, testimony is not established fact, facts carry supported claims, projected material is not current standing by identity, and constitutional standing is repository-governed rather than objective reality.

## 8. Smallest warranted next step

Smallest warranted next step: **producer characterization tests and a Book chapter repair proposal**, not implementation split. The next pass should characterize which existing producers intentionally establish source-relative Facts, which merely construct fact-shaped artifacts for replay/fixtures, and where conflict-aware establishment is missing or projection-local. Only after that should Seed decide whether documentation reconciliation, view vocabulary clarification, fact-establishment boundary recovery, or implementation split is required.

Required stop: do not begin temporal reconciliation.

Next bounded question:

> Once Claim, normalization, and Fact standing are distinguished, which temporal standings belong to each production, establishment, projection, and consumption boundary?
