# Claim Normalization and Fact Standing Amendment 001

## Status

This is an amendment record. It records why canonical Book clauses were amended after receiving `claim_normalization_and_fact_standing_recovery_001.md` as testimony. It is not a second constitutional authority, does not rename implementation models, does not create a `NormalizedClaim` class or schema, does not modify production behavior, and does not begin the temporal investigation.

## Book clauses examined

- `book_of_seed/README.md`
- `book_of_seed/concordance.md`
- `book_of_seed/unresolved.md`
- `book_of_seed/01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md`
- `book_of_seed/01-grammar-and-standing/constructors-and-production-authority.md`
- `book_of_seed/01-grammar-and-standing/lenses-views-and-roads.md`
- `book_of_seed/01-grammar-and-standing/external-and-constitutional-grammar.md`
- `book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md`
- `book_of_seed/05-evidence-and-knowledge/evidence-provenance-and-explanation.md`
- `book_of_seed/05-evidence-and-knowledge/recording-and-knowledge-extraction.md`
- `book_of_seed/06-state-and-projection/events-facts-and-state.md`
- `book_of_seed/06-state-and-projection/projection-and-current-state.md`

## Repository witnesses examined

- `seed_runtime/observations.py`: `ObservationIngestor` records `observation.observed`, creates `Evidence`, optionally creates a `Fact`, and emits `fact.observed` or `fact.inferred`; `observation_to_fact` copies subject, predicate, value, dimensions, confidence, observed time, expiry, and one evidence id.
- `seed_runtime/evidence.py`: `Evidence` preserves source, kind, observed time, payload, and confidence.
- `seed_runtime/facts.py`: `Fact` validates known source type and confidence, carries normalized fact fields and evidence/inference references, while `FactSupport` is a projection support record.
- `seed_runtime/state.py`: replay and finalization build projected facts, fact supports, current fact selection, expiry filtering, measurement current samples, relationship projections, and conflicts.
- `seed_runtime/state_views.py`: `ObservationView` summarizes observations; `FactView` renders current projected claims from `FactSupport` or raw fact fallback.
- `seed_runtime/evidence_graph.py`: evidence graph views expose resolved and unresolved support references and can report projected facts with no resolved supporting evidence.
- `seed_runtime/contradictions.py`, `seed_runtime/confidence.py`, and `seed_runtime/explanations.py`: contradiction, confidence, and explanation are read-only/projection consumers that qualify projected fact material without resolving truth or deleting facts.
- Relevant tests were inspected through repository search for documentation and invariant coverage. Existing tests mostly characterize runtime projection, evidence, contradiction, and bounded-question distinctions rather than canonical Book text.

## Historical doctrine examined

- `docs/foundational_ontology_reconciliation.md`
- `docs/ontology.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/architectural_documentation_alignment_reconciliation.md`
- `docs/seed.md`

The valid historical doctrine is that Seed is claim-centric because the proposition is not identical to a storage object; source testimony may be wrong; normalized representation is not objective truth; projected current state is not preserved history; verification is scoped; and facts may be contradicted, stale, superseded, or unselected without deleting provenance.

The incomplete or overbroad wording was the repeated shorthand that Facts are normalized claim forms. That wording remains useful only if it is read as representational shape or as bounded standing after support and establishment. It is unsafe when read as normalization alone establishing Fact standing.

## Clauses amended

- `05-evidence-and-knowledge/testimony-and-established-fact.md` now states what Claim names, what normalization does, what Fact safely means, what establishes Fact standing, when one Observation may support a bounded Fact, why a Fact artifact does not prove its own standing, and what remains Unknown about producer-specific boundaries.
- `01-grammar-and-standing/constitutional-kinds-and-artifact-standing.md` now explicitly applies artifact-standing grammar to normalized fact-shaped artifacts.
- `06-state-and-projection/events-facts-and-state.md` now distinguishes established Facts from fact-shaped recorded material and separates Fact standing from current and verified standing.
- `06-state-and-projection/projection-and-current-state.md` now states the ObservationView / FactView distinction and refuses to treat FactView as establishment, truth, verification, or exhaustive history.
- `concordance.md` now indexes Claim, normalization, Fact standing, ObservationView, and FactView without granting equivalence.
- `unresolved.md` now preserves producer-specific Fact standing, conflict-awareness mechanics, authority/corroboration thresholds, and the next temporal-standing question as Unknown.

## Clauses preserved

- The Book README remains sufficient: implementation and historical reports are evidence, not automatic constitutional authority.
- Constructors and production authority remains sufficient: public construction is not lawful production authority.
- Lenses, views, and constitutional roads remains sufficient: visibility, read models, and consumer use do not by themselves change upstream standing.
- Evidence, provenance, and explanation remains sufficient: evidence, provenance, and explanation qualify support but do not establish upstream truth.
- Recording and knowledge extraction remains sufficient: recording preserves assertion-bearing material but does not itself establish knowledge.

## Clauses relocated

No clause was moved. The existing chapter seams were sufficient. The distinction belongs primarily in testimony/fact standing, with narrow supporting amendments in artifact standing and projection chapters.

## Before/after standing table

| subject | prior Book wording | problem or ambiguity | repository evidence | amended Book wording | remaining limits |
| --- | --- | --- | --- | --- | --- |
| Claim | Testimony chapter named a source's claim but did not define Claim. Historical docs said claim is the central proposition. | Could be read as a constitutional subject, assertion standing, implementation object, or universal claim store. | Claims appear through observations, evidence payloads, facts, relationships, views, explanations, and docs; no inspected canonical `Claim` artifact model governs all knowledge. | Claim is semantic proposition carried through artifacts and standings; claim-centricity does not mean every knowledge artifact is itself a Claim artifact. | Future work may recover more specific claim artifacts or support structures. |
| Normalization | Historical shorthand said facts normalize claims. | Could imply normalization creates standing or demands `NormalizedClaim`. | `ObservationIngestor.observation_to_fact` canonicalizes fields into `Fact`; no separate class exists; support/projection/conflict are separate modules. | Normalization canonicalizes interpreted claims into Seed vocabulary; it does not create a new constitutional subject, support, or standing by itself. | Exact predicate-specific normalization authority is not globally audited. |
| Fact artifact | Book representative anchors named `Fact`; artifact-standing chapter already denied shape-based standing. | Needed explicit application to fact-shaped normalized claim records. | `Fact` constructor validates source type/confidence and preserves fields; direct construction and replay can create fact-shaped rows without original establishment proof. | A Fact artifact is normalized fact-shaped representation; it does not prove its own standing. | Some producers may already be lawful; each boundary requires producer evidence. |
| Fact standing | Testimony chapter required ingestion, support, normalization, conflict-aware establishment. | Did not say whether Fact meant artifact, standing, or both; did not answer one-observation support. | Observation ingestion links one evidence id and emits facts; support/conflict/current selection occur later; evidence graph can expose unsupported or unresolved references. | Constitutional Fact is established evidence-backed normalized scoped claim whose standing does not exceed evidence, authority, scope, and production boundary. One Observation may support a weak source-relative Fact. | Exact thresholds and stronger claims remain Unknown. |
| Contradicted/stale/expired/unselected Fact | State chapter said facts carry supported claims and projection supplies current standing. | Needed explicit preservation of historical/provenance standing after conflict or loss of current selection. | State preserves facts, filters expiry for supports, detects conflicts, computes confidence penalties, and selects current representatives. | Contradiction, staleness, expiry, supersession, and unselection do not delete preserved Fact material; they affect confidence, conflict, projection, current standing, or verification. | Temporal standing investigation is intentionally not begun. |
| Current standing | Projection chapter separated projection from standing. | Needed stronger contrast with Fact standing and FactView. | `get_current_facts`, `FactSupport`, and `FactView` select/project current material by predicate and support rules. | Current standing arises only through responsible consumer/projection boundary preserving limits; it is not Fact standing by identity. | Future temporal work must recover as-of relations. |
| Verified standing | Historical docs scoped verification. | Book did not tie verified standing into Fact distinction. | Verification can be represented as predicates/facts, but consumers require method/scope/time. | Verified standing is separate from selected current standing and universal truth. | Producer-specific verification boundaries remain outside this amendment. |
| ObservationView | Concordance indexed view/lens but not this concrete view. | Difference from FactView could be read as presentation only. | `build_observation_view` reads `State.observations` and summarizes source-attributed observations with support ids. | ObservationView exposes source-attributed observation testimony, not promotion/current/verification/Fact standing. | It may include ids related to evidence/facts for display; those ids do not strengthen standing by visibility. |
| FactView | Projection chapter covered views generally. | FactView could be read as established/current/verified truth. | `build_fact_view` renders `FactSupport` or raw fact fallback; it is read-only and does not inspect producer lawfulness. | FactView exposes projected normalized fact/support material; it is not an establishment boundary, universal truth, verified state, or exhaustive history. | Whether displayed material has Fact standing depends on producer evidence. |

## Canonical answers recovered

- **What is a Claim?** A Claim is the semantic proposition carried by testimony, observation, evidence, facts, relationships, projection, explanation, documentation, or consumer assertion. It is not currently canonized as a universal durable artifact kind.
- **What does normalization do?** It canonicalizes an interpreted claim into Seed's fact vocabulary for comparison, support, projection, contradiction, and explanation. It does not create support or standing.
- **What is a Fact?** Implementation `Fact` is a normalized fact-shaped artifact. Constitutional Fact is an established, evidence-backed, normalized, scoped claim with bounded standing.
- **What establishes Fact standing?** Claim-appropriate evidence support, normalization, source/producer authority sufficient for the claim strength, scope preservation, and conflict awareness at the applicable establishment or consumer boundary.
- **Does a Fact artifact prove its own standing?** No.
- **Can one Observation support a Fact?** Yes, when the Fact asserts no more than the source-relative observation supports.
- **What must remain preserved when it does?** Source, vantage or source role, observed time, dimensions, value, confidence, expiry/freshness limits, evidence link, and claim-strength boundary.
- **Does contradiction remove Fact standing?** No. It qualifies later confidence, conflict, projection, current standing, or verification without deleting provenance.
- **What is the difference between Fact standing, current standing, and verified standing?** Fact standing is bounded establishment of a normalized supported claim; current standing is projection/consumer-selected standing under freshness, conflict, support, and authority limits; verified standing is method-, scope-, and time-specific confirmation and is not universal truth.
- **What does ObservationView expose?** Source-attributed observation testimony and supporting ids.
- **What does FactView expose?** Projected normalized fact/support material; not proof of establishment or verification.
- **Which parts remain Unknown?** Producer-specific stronger Fact standing, exact conflict-awareness mechanics, source authority and corroboration thresholds, and temporal standings across expression, normalization, production/establishment, projection, and consumer uptake.

## Why each amendment was warranted

The amendment was warranted because the Book had enough grammar to reject truth-centric Fact ontology and shape-based standing, but not enough explicit language to reconcile historical claim-centric shorthand with later testimony-versus-established-fact grammar. Current repository witness shows separate Observation, Evidence, Fact, support, conflict, confidence, explanation, State, ObservationView, and FactView responsibilities. Those witnesses require the Book to distinguish semantic content, normalized representation, artifact shape, established standing, current selection, and verification.

## Why broader amendment was not warranted

Broader changes were not warranted because the current task is canonical grammar only. The repository does not yet establish universal producer thresholds, a required establishment service, a `NormalizedClaim` artifact, a universal one-observation promotion rule, or a temporal standing model. Historical `docs/` files remain historical testimony and were not synchronized. Production behavior, schemas, class names, ingestion, projection, and Fact promotion behavior were left unchanged.

## Required conclusion

The Book needed to change by making explicit that Claim names semantic content, normalization canonicalizes without standing, Fact names both an implementation artifact and a bounded constitutional standing when lawfully established, and FactView/ObservationView expose different material without proving stronger standing.

Earlier claim-centric findings remain valid: Seed is not fact-centric or truth-centric; propositions are not identical to storage objects; source testimony may be wrong; normalized representation is not objective truth; projected current state is not preserved history; verification is scoped; and facts may be contradicted, stale, superseded, historical, or unselected without losing provenance.

Earlier wording was incomplete where it said or implied that Facts are normalized claim forms without naming the additional distinction between a fact-shaped artifact and established Fact standing.

The amended Book gives Fact this constitutional meaning: an established, evidence-backed, normalized, scoped claim whose standing is bounded by support, source or producer authority, scope, confidence, conflict awareness, and the applicable production boundary, and which is not truth, current standing, or verification by identity.

The amended Book refuses to decide without further producer evidence which current producers and predicates establish broader Fact standing, which construct only fact-shaped normalized claims or replay prior standing, which conflict checks must precede production rather than projection or consumer uptake, and which authority/corroboration thresholds govern stronger claims.

The Book is now sufficient to investigate temporal standing across Claim expression, normalization, Fact production or establishment, projection, and consumer uptake, but that investigation has not begun here.

## Next bounded question preserved

Under the amended Book grammar, which temporal standings and relations govern Claim expression, normalization, Fact production or establishment, projection, and consumer uptake?
