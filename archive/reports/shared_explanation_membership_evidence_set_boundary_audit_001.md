# Shared Explanation Membership Evidence Set Boundary Audit 001

## Scope

This is exactly one bounded **Shared Explanation Membership Evidence Set Boundary Audit**. It does not implement a set, selector, diagnostic surface, CLI flag, source code, or tests. It answers only whether several independently produced per-candidate `SharedExplanationMembershipEvidenceProjection` results for one bounded inquiry warrant an intermediate read-only collection artifact with constitutional responsibilities of its own.

## Core answer

Given several per-candidate membership evidence results for one bounded inquiry, repository evidence supports **B. A lightweight read-only set is warranted only to enforce one-inquiry and preservation invariants**.

A separate membership-evidence set would not own eligibility selection, ranking, sequencing, deduplication, view composition, semantic relevance inference, or membership-state interpretation. It would own only a small collection boundary that can be tested independently:

1. every supplied result must be preserved without loss;
2. every accepted result must share the same explicit bounded inquiry and bounded demand reference;
3. source-result identity and duplicate visibility must remain visible rather than collapsed;
4. the already-produced `belongs`, `does_not_belong`, `unknown`, and `conflict` states must remain partitionable as existing states, without interpreting them;
5. empty and partial input must remain input facts, not fabricated Unknown results or completeness claims;
6. the artifact must remain read-only, non-event-writing, and non-mutating.

That is a constitutional boundary only if kept this narrow. Anything more would become membership selection or composition.

## Reviewed evidence

### Implemented per-candidate membership evidence projection and tests

The current implementation defines exactly four membership states: `belongs`, `does_not_belong`, `unknown`, and `conflict`. It also defines `BoundedInquiryReference`, `PreservedLineageEvidence`, and one frozen `SharedExplanationMembershipEvidenceProjection` output record with explicit bounded inquiry, bounded demand, candidate projection/source identity, state, references, duplicate visibility, input boundary, non-selection boundary, and read-only/non-mutation flags.

The producer consumes exactly one bounded inquiry reference, one rendering projection, and one explicit lineage evidence record. It performs no source lookup and no semantic inference from shared wording, source state, stage, or explanation text. Its result construction independently chooses `conflict`, `belongs`, `does_not_belong`, or `unknown` based only on supplied positive, incompatible, and missing lineage references.

The tests prove each state exists at the per-result layer: target-positive lineage yields `belongs`; incompatible lineage yields `does_not_belong`; missing lineage yields `unknown`; target-positive plus incompatible lineage yields `conflict`. They also prove duplicate source identity is preserved in the per-result record and is not deduplicated, shared wording/state does not establish membership, human and JSON output preserve the same membership meaning, and the projection writes no events, mutates no cluster, and does not expose a selected candidate.

### Rendering projection boundary

`SharedExplanationRenderingProjection` consumes exactly one already-produced stage-local explanation and explicitly refuses to compare, aggregate, order, or compose explanations. Its rendering boundary says shared field names are display labels only and all constitutional meaning remains authored and owned by the source stage. That means a membership-evidence set cannot infer membership from rendering labels or source-state vocabulary; it may only collect already-produced membership evidence results.

### Existing candidate-set and read-only collection precedent

`CandidateExternalGrammarSet` is a caller-supplied read-only candidate collection with its own narrow set responsibilities: preserve supplied candidates, preserve set-level Unknowns, reject duplicate candidate IDs within that specific set, and refuse selection, verification, promotion, semantic truth, readiness, or capability claims. Its formatter treats zero candidates as a zero-candidate set, not failure. This proves the repository allows read-only collection artifacts when they own explicit collection invariants rather than selection.

That precedent does not transfer duplicate rejection to membership evidence. In the membership-evidence road, duplicate source identity visibility is already a preserved evidence feature, and the user's proving case forbids deduplication. Therefore a membership-evidence set, if implemented later, would preserve duplicates rather than reject or collapse them.

### Candidate-set to projection handoff precedent

`CapabilityReachabilityProjection` validates that a future handoff belongs to the supplied candidate set, matches probe-request and capability-demand identities, preserves candidate references/order, preserves candidate standings, and preserves Unknown/conflict references. It then partitions candidate states into supporting, blocked, unsupported, unknown, and conflicting references without selecting a realization. Its boundary notes expressly say reachability does not select a realization, multiple supported realizations establish no preference, unsupported requires positive evidence, and absence alone produces Unknown.

This is the strongest analogy for a membership-evidence set: a collection/handoff boundary may validate same-bounded-input identity and preserve state partitions without deciding downstream selection.

### Constitutional view selection and composition precedent

`ConstitutionalViewSelection` selects registered view names only by deterministic exact-key comparison, preserves unsupported selection uncertainty, and refuses semantic reasoning, ranking, heuristics, planning, orchestration, evidence discovery, repository mutation, event-ledger writes, and cluster mutation. That is selection, not collection.

`ConstitutionalViewCompositionRequest` owns only explicit registered-view selection already supplied by a caller plus purpose/output-format intent. `build_constitutional_view_composition` then composes explicitly requested registered constitutional views and rejects unsupported view names. This proves composition starts after selection is supplied; it does not create a prior collection artifact merely because multiple views exist.

### Reasoning-path and selection-path collection boundaries

`SelectionPathAudit` preserves selected value, candidate set, selection factors, non-selected candidates, evidence, outcome, Unknowns, and read-only boundary. Its internal payloads separate result, reason, support, candidate set, non-selected list, factors, Unknowns, and lineage. That surface is a selection trace, not a membership evidence set. It shows that later membership selection should remain responsible for selected eligible renderings, non-members, Unknown candidates, conflicting candidates, and duplicate visibility explanations.

## Existing producer-versus-output construction finding

The current producer/output boundary is clean but per-candidate only:

```text
BoundedInquiryReference
+
SharedExplanationRenderingProjection
+
PreservedLineageEvidence
→ SharedExplanationMembershipEvidenceProjection
```

The producer constructs one output record and stops before any collection, set-level validation, selector handoff, or selection. The output record itself carries bounded inquiry fields, candidate identity fields, membership state, references, duplicate source identity visibility, non-selection text, and read-only flags. Because those fields already exist in every result, a later set would not need to recompute membership or inspect source artifacts; it would only validate and preserve a group of already-produced outputs.

## Candidate set-owned invariants

| Candidate responsibility | Classification | Finding |
| --- | --- | --- |
| One bounded inquiry across every result | **real set-owned invariant** | The per-result projection records `bounded_inquiry_ref` and `bounded_demand_ref`, but only a collection boundary can test that every supplied result in the collection shares the same explicit bounded inquiry/demand. This is the strongest set-owned invariant. |
| Preservation of every supplied candidate result | **real set-owned invariant** | A set can own lossless retention of all supplied per-result records, including their state and references. This is not selection. |
| Stable source-result identity | **real set-owned invariant / per-result responsibility** | Each result already owns `candidate_projection_ref` and `candidate_source_explanation_ref`; a set can preserve the ordered or supplied identities as collection-visible facts without defining identity semantics. |
| Duplicate identity visibility | **real set-owned invariant / per-result responsibility** | The per-result layer exposes duplicate source identity evidence when supplied. Across several results, only a collection can make repeated candidate/source identities visible without deduplicating. |
| `belongs` / `does_not_belong` / `unknown` / `conflict` partitions | **composition responsibility if purely grouped; real set-owned invariant only as mechanical partition visibility** | A set may expose partitions by already-existing `membership_state` values. It must not interpret states, rank them, or decide eligibility. |
| Mixed or conflicting inquiry references | **real set-owned invariant** | If a set claims one bounded inquiry, mixed inquiry/demand fields must be rejected or preserved as a set-boundary conflict. Repository precedent favors validation errors for identity mismatches where a downstream projection requires same bounded demand. |
| Set-level Unknowns or conflicts | **unsupported except boundary conflicts/collection limitations** | Per-result Unknowns/conflicts are already owned by per-result projections. A set may preserve a boundary conflict such as mixed inquiry references or unknown completeness; it must not fabricate candidate-level Unknowns. |
| Set provenance | **implementation plumbing / composition responsibility** | The current per-result records preserve references. Repository evidence does not require a richer provenance owner for the set beyond preserving supplied result identities and perhaps supplied collection provenance. |
| Read-only and non-mutation guarantees | **real set-owned invariant** | A collection artifact can independently assert and test that it writes no ledger events and mutates no cluster while consuming read-only results. |

## Per-result responsibilities

The per-result projection already owns:

- deciding one candidate's membership evidence state from explicit supplied lineage only;
- preserving `belongs`, `does_not_belong`, `unknown`, and `conflict` states;
- preserving supporting, incompatible, missing, and conflicting references;
- exposing duplicate source identity references supplied to that result;
- refusing source lookup, wording-based inference, stage-based inference, ranking, sequencing, composition, authorization, execution, event-ledger writes, and cluster mutation;
- carrying the explicit bounded inquiry and demand reference for that result.

A set must not re-open these conclusions.

## Selector-owned responsibilities

The later selector remains responsible for:

- choosing eligible rendering projections from `belongs` results, if repository authority later defines that rule;
- preserving or explaining non-members from `does_not_belong` results;
- preserving Unknown candidates without converting them into non-members;
- preserving conflicting candidates without resolving conflict by severity, rank, or blocker status;
- preserving duplicate visibility and deciding whether duplicate source identities affect selected output, only if repository authority later defines that selector rule;
- explaining non-selected alternatives and selection uncertainty;
- refusing eligibility decisions when evidence is missing or conflicting.

The set must not decide eligibility.

## Proving cases

### One inquiry, mixed states

Several results for one inquiry may include all four membership states. Preserving them together does warrant a lightweight set only if the artifact enforces same bounded inquiry/demand and lossless preservation. It does not warrant a selector. Mechanical partitioning by existing state is acceptable as preservation visibility; interpreting `unknown` or `conflict` is not.

### Mixed inquiry references

If results claim different bounded inquiries or bounded demands, a one-inquiry membership-evidence set cannot silently collect them as lawful members of the same set. Repository precedent in reachability validation favors rejecting identity mismatch when a downstream projection/handoff claims a single bounded demand. A weaker alternative would be a read-only set-boundary conflict, but the current strongest evidence supports rejection for a set that is explicitly defined as one bounded inquiry. It has no authority to infer that different inquiries are semantically equivalent.

### Duplicate candidate identity

Several results may preserve the same candidate projection identity, source explanation identity, or source identity references. The set must not deduplicate. Duplicate visibility is set-owned only as cross-result visibility: preserve repeated records and expose the repeated identities. It is not duplicate resolution.

### Empty collection

Zero results is not a fabricated Unknown result. Existing candidate-set precedent treats a zero-candidate set as not failure, while reachability treats no candidates as `unknown` only inside a projection that owns reachability conclusion. A membership-evidence set would own no reachability-like conclusion, so empty input should be either a lawful empty read-only evidence set or, if a caller required non-empty input, a missing input validation condition. Repository evidence does not support fabricating a candidate-level Unknown.

### Partial collection

A set may preserve supplied results only. It may not claim completeness over all expected stages, all possible renderings, all expected candidates, or all source explanations unless a future caller supplies an explicit completeness claim and repository authority defines it. Set completeness is not the same as all expected stages existing.

### Selection boundary

After a lawful read-only set, the selector still receives:

- `belongs` candidate results as possible eligible rendering projections, not automatically selected projections;
- `does_not_belong` candidate results as non-member evidence;
- `unknown` candidate results as unknown membership evidence;
- `conflict` candidate results as conflicting membership evidence;
- duplicate candidate/source identity visibility exactly as preserved;
- any collection-boundary uncertainty such as partial input or mixed inquiry rejection/conflict.

The selector must not receive a pre-filtered, ranked, deduplicated, or interpreted eligibility list from the set.

## Unknown and conflict treatment

Per-result Unknowns and conflicts stay per-result. A set may group them by existing state but cannot reinterpret them.

Set-level Unknowns are not supported as candidate membership states. The only supported set-level uncertainty is collection-boundary uncertainty, such as partial supplied input, no completeness claim, or an unresolved decision between rejecting and conflict-preserving mixed inquiry references.

Set-level conflicts are supported only for collection-boundary contradictions if repository authority later chooses conflict preservation instead of rejection. They do not resolve per-result conflicts.

## Mixed-inquiry treatment

For a set claiming one bounded inquiry, mixed inquiry references are outside the lawful collection invariant. The strongest implementation precedent supports a validation failure rather than a mixed set. If a future implementation chooses conflict preservation, the conflict must be a set-boundary conflict over collection identity, not a candidate-level membership conflict and not a semantic relevance comparison.

## Duplicate treatment

Duplicate visibility is preserved; deduplication is forbidden. The set may expose repeated `candidate_projection_ref`, repeated `candidate_source_explanation_ref`, repeated source identity references, and repeated complete result records. It may not merge, discard, rank, or normalize them.

## Empty and partial collection treatment

- **Empty collection:** lawful only as an empty supplied-result collection if the set artifact exists; not an Unknown result and not proof that no candidate belongs.
- **Missing input:** only if the caller contract requires at least one result; not currently proven by repository evidence.
- **Partial collection:** lawful as supplied-result preservation; no completeness claim.
- **All expected stages missing:** unsupported because the set has no authority to invent expected stages.

## Topology classification

**B. A lightweight read-only set is warranted only to enforce one-inquiry and preservation invariants.**

The supported topology is:

```text
per-candidate membership results
→ read-only membership-evidence set
→ membership selection
```

Only the middle node's narrow boundary is supported. It is not a constitutional selector, eligibility ranker, blocker selector, severity normalizer, global composition manager, or registry.

## Strongest supporting evidence

1. The per-result projection exposes explicit bounded inquiry and demand fields on every output, making a same-inquiry set invariant implementable without source lookup.
2. The per-result projection explicitly stops before selection, deduplication, sequencing, composition, authorization, execution, event-ledger writes, and cluster mutation.
3. Candidate-set and reachability precedents show the repository accepts read-only collection/handoff boundaries that validate exact shared identity and preserve state partitions without selecting.
4. Selection and composition precedents keep collection, selection, and composition separate.

## Strongest counterevidence

1. The existing implementation already carries all important membership evidence fields per result, so a set that only stores a tuple would be an implementation wrapper.
2. No current source or test defines `SharedExplanationMembershipEvidenceSet`.
3. Per-result duplicate visibility exists inside the projection tests, so duplicate handling is not entirely set-owned.
4. Selection-path audit already knows how to preserve candidates/non-selected/unknowns for selection traces, so a future selector could consume per-result membership projections directly if it does not need same-inquiry validation or lossless collection provenance.

## Exact current compressions

- There is no implemented multi-result membership evidence boundary.
- Same bounded inquiry across several membership evidence results is currently implicit in caller discipline, not enforced by an artifact.
- Cross-result duplicate source/candidate identity visibility is not currently exposed by an artifact.
- Mixed inquiry references have no current owner between per-result projection and future selector.
- Empty and partial supplied-result collection semantics are not currently explicit.
- Membership-state partition visibility across several results is not currently exposed except by ad hoc caller code.

## Whether one implementation slice is warranted

Yes, but only one narrow implementation slice is warranted if the project continues this road: a lightweight read-only `SharedExplanationMembershipEvidenceSet` that consumes already-produced `SharedExplanationMembershipEvidenceProjection` records for one explicit bounded inquiry/demand, preserves every supplied result, exposes same-inquiry validation, cross-result duplicate visibility, mechanical partitions by existing state, empty/partial input semantics, and read-only/non-mutation flags.

That slice must not implement membership selection, eligibility, ranking, sequencing, deduplication, stage expectation, semantic relevance inference, view composition, authorization, execution, event-ledger writes, or cluster mutation.

## Exact next bounded question

Given an explicit bounded inquiry reference and a supplied tuple of already-produced `SharedExplanationMembershipEvidenceProjection` records, what smallest read-only set artifact can validate same bounded inquiry/demand, preserve every supplied result and duplicate identity occurrence, expose mechanical state partitions, and preserve empty/partial collection semantics without selecting, deduplicating, ranking, sequencing, composing, or fabricating Unknown results?

## Preserved Unknowns

- Whether a future implementation should reject mixed inquiry references or preserve a set-boundary conflict remains Unknown, with rejection currently better supported by existing validation precedent.
- Whether the set should preserve a caller-supplied collection provenance field is Unknown; existing per-result references may be sufficient.
- Whether the future selector will treat `belongs` as eligible by itself is Unknown and selector-owned.
- Whether empty input should be allowed for every caller is Unknown; empty input must not fabricate candidate Unknowns either way.

## Confidence

Medium-high. Repository evidence strongly supports same-inquiry validation, preservation, duplicate visibility, read-only boundaries, and collection/selection separation. Confidence is not high because no set implementation or tests exist yet, and the strongest counterevidence is that a careless set would be only a tuple wrapper.

## Final answer

Does a membership-evidence set own a real constitutional boundary,
and if so,
what exactly does it preserve
without selecting?

Yes, but only as a lightweight read-only constitutional collection boundary. It preserves one explicit bounded inquiry/demand across every accepted per-candidate membership evidence result, preserves every supplied result without loss, preserves source-result identity and duplicate identity visibility without deduplication, preserves existing `belongs`, `does_not_belong`, `unknown`, and `conflict` states as mechanical partitions without interpreting them, preserves empty and partial supplied-result collection semantics without fabricating Unknowns or completeness claims, and preserves read-only, no-event-ledger, no-cluster-mutation guarantees. It does not select eligible candidates, rank, sequence, deduplicate, infer semantic relevance, compose a view, or resolve Unknowns/conflicts.

Shared explanation membership evidence
set boundary audit complete.
