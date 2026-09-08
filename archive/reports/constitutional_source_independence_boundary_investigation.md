# Constitutional Source Independence Boundary Investigation

Repository authority wins.

## Boundary and bounded question

This document performs exactly one bounded constitutional investigation focused only on:

```text
Source Independence != Source Count
```

Bounded question:

```text
Across recurring repository evidence, what constitutional boundary, if any, separates independent support / independent source path / corroboration from multiple sources / repeated claims / copied repetition / syndication / shared-origin amplification, and under what conditions, if any, can multiple source packets lawfully contribute to evidence as independent corroboration rather than merely source count?
```

This is not world ingestion, source scoring, credibility scoring, authority scoring, corroboration scoring, legal research, public-world evaluation, a truth engine, an implementation design, or a new diagnostic surface. It does not evaluate Flock cameras, fetch public-world evidence, implement the Eye, promote public-world source categories into ontology, or create implementation pressure.

## App-visible evidence used

The app was used as bounded repository evidence, not as an oracle:

- `python -m scripts.seed_local --diagnostic-inventory --json > /tmp/diag.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject "source independence" --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_source_independence.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject "source count" --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_source_count.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject corroboration --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_corroboration.json`
- `python -m scripts.seed_local --knowledge-reachability-audit --knowledge-reachability-audit-subject syndication --knowledge-reachability-audit-json --knowledge-reachability-audit-limit 20 > /tmp/kr_syndication.json`

App-visible findings used only within their boundary:

- Diagnostic inventory returned registered diagnostic surfaces with explicit `record_scope`, `writes_event_ledger`, `emits_cluster_facts`, and `mutates_cluster` fields. This supports the repository distinction between visibility, recording, event-ledger writes, diagnostic facts, cluster facts, and cluster mutation.
- Knowledge reachability in the empty/default run treated `source independence` as a `presentation_label` candidate with first loss at `not_preserved`.
- Knowledge reachability treated `source count`, `corroboration`, and `syndication` as queried candidates that were not promoted into current projected knowledge in that run. This does not prove that the words lack prose evidence. It only preserves the app-visible non-promotion boundary for this run.
- The reachability outputs scanned no projected facts or fact-support rows in the default state. Therefore the app output cannot establish a live source-independence model; it can only reinforce caution about promoting the vocabulary.

## Reviewed repository evidence

Reviewed repository evidence included:

- `AGENTS.md`
- `docs/archive/original_book_of_seed/13-knowledge-and-evidence.md`
- `constitutional_external_source_role_boundary_investigation.md`
- `constitutional_repetition_proof_boundary_investigation.md`
- `constitutional_authority_volume_boundary_investigation.md`
- `constitutional_narrative_history_boundary_investigation.md`
- `constitutional_boundary_confusion_projection_vs_implementation_pressure_investigation.md`
- `constitutional_warrant_characterization.md`
- `constitutional_reliance_characterization.md`
- `constitutional_lawful_acceptance_characterization.md`
- `artifact_bounded_lawful_reliance_characterization.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- `docs/fact_confidence_and_corroboration_reconciliation.md`
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/host_observation_reconciliation.md`
- `docs/source_navigation_surface_reconciliation.md`
- implementation-adjacent evidence around observations, evidence, fact support, source navigation, diagnostic inventory, diagnostic shape audit, knowledge reachability, reasoning path, selection path, Unknown preservation, and lawful stop.

## 1. What repository evidence already means by source independence, if anything

Repository evidence does not support a general public-world source-independence ontology or scoring model.

It does support a smaller constitutional distinction:

```text
source independence = meaningful separation of support paths, source paths, methods, vantage points, times, dependency chains, or failure domains for a bounded claim
```

That distinction appears most clearly in corroboration and fact-promotion documentation. Corroboration asks both how much evidence supports a claim and how independent that support is. Independent corroboration is described as support from meaningfully different source paths or failure domains, not merely repeated reports.

The constitutional work is negative and boundary-preserving: independence prevents copied, syndicated, shared-origin, same-adapter, same-vantage, or same-failure-domain repetition from being counted as independent support. It does not create truth, authority, ingestion permission, legal authority, source rank, credibility score, or implementation mandate.

## 2. What repository evidence already means by source count or source volume

Repository evidence treats source count and source volume as count-like, recurrence-like, or visibility-like evidence:

- number of sources, observations, facts, records, rows, samples, warnings, documents, headings, or diagnostic entries;
- repeated appearance of a claim or label;
- high visibility in a projection, summary, diagnostic, or corpus;
- volume of operational output or measurement samples.

`constitutional_authority_volume_boundary_investigation.md` already recovers that source count is not source authority. Count asks how many appearances exist. Authority asks whether a competent source or boundary can support the claim in the role and strength asserted. Count can support count, recurrence, distribution, coverage, pressure, or visibility claims. Count alone cannot support truth, warrant, independence, or authority claims.

## 3. What distinguishes independent support from multiple appearances of the same assertion

Independent support requires preserved evidence that the support paths are meaningfully separated for the bounded claim.

Multiple appearances of the same assertion show only that the assertion appeared multiple times unless the repository also preserves:

- source identity;
- provenance;
- temporal provenance;
- claim form;
- source role;
- source authority boundary;
- dependency path;
- method or observation path;
- vantage point or scope;
- support path;
- confidence limits;
- conflicts and negative authority.

Without those preserved conditions, the lawful conclusion is:

```text
The assertion appeared multiple times.
```

not:

```text
The assertion has independent support.
```

## 4. What distinguishes corroboration from copied repetition

Corroboration is a support relationship among evidence items and a compatible bounded claim. Copied repetition is repeated transmission of the same assertion or same upstream support.

Corroboration requires at least:

1. a bounded claim whose form is identified;
2. exact overlap or compatible overlap on the dimensions being corroborated;
3. scope, time, predicate, dimensions, and vantage point preservation;
4. provenance for each packet;
5. dependency analysis sufficient to distinguish independent paths from copied paths;
6. contradiction/conflict preservation;
7. confidence limits and Unknown preservation.

Copied repetition lacks enough preserved independence to do corroborative work. It may support a recurrence or visibility claim, or a claim that a phrase was republished. It does not support independent corroboration merely by being numerous.

## 5. What distinguishes independent source path from shared-origin amplification

An independent source path has a separate route by which support became available for the bounded claim. Separation may involve different observation methods, evidence producers, vantage points, records, instruments, institutions, time windows, or failure domains, but only when repository evidence preserves that separation.

Shared-origin amplification occurs when multiple packets depend on one origin, one source feed, one copied statement, one syndication wire, one adapter, one report, one database, one scraper, one institutional release, or one failure domain. Amplification can increase visibility. It does not multiply independent support.

The lawful distinction is dependency, not publisher count:

```text
many publishers + one upstream assertion = source count / amplification
multiple preserved non-dependent support paths = possible independent corroboration
```

## 6. What distinguishes syndication from independent observation

Syndication republishes, mirrors, quotes, copies, summarizes, or distributes material from an upstream source. It can prove that the upstream material was distributed or visible through many outlets. It does not by itself prove the target proposition independently.

Independent observation is a source-attributed report generated through a distinct observation act, method, vantage point, or evidence path. It answers what that source observed or generated, not merely what it received and repeated.

The repository must preserve Unknown when it cannot distinguish:

```text
this packet independently observed X
```

from:

```text
this packet repeated someone else's assertion that X
```

## 7. What distinguishes agreement from warrant

Agreement means multiple packets, observations, or claims are compatible or say similar things within some scope. Warrant means evidence-bound lawful reliance under a preserved authority boundary.

Agreement can contribute to warrant only when agreement is admissible for the claim form and preserves provenance, source role, source authority, support path, independence, claim-strength matching, confidence, contradiction handling, and Unknowns. Agreement alone remains agreement, not truth, proof, authority, lawful reliance, or implementation pressure.

## 8. What distinguishes disagreement or contradiction from disproof

Disagreement means claims do not align. Contradiction is stronger: evidence supports incompatible claims within the same relevant scope, predicate, dimensions, and time semantics.

Neither disagreement nor contradiction is automatic disproof. Repository evidence treats contradiction as a visible evidence condition that may block selection, lower confidence, expose conflict, or require lawful stop. It does not prove the opposite claim unless a competent boundary, claim form, and support path authorize that stronger conclusion.

## 9. Roles of provenance, source role, source authority, claim form, temporal provenance, support path, confidence, and Unknown preservation

| Condition | Constitutional work |
| --- | --- |
| Provenance | Keeps origin, source, payload, and preservation path inspectable; without it, source count may be copy count. |
| Source role | Bounds how a packet may be considered, such as reported claim, official statement, secondary analysis, contextual background, corroborating relation, or contradictory relation. The role does not create truth. |
| Source authority | Identifies what the source is competent to support for this bounded claim, if anything. It is not publisher prominence or repetition. |
| Claim form | Separates count claims, visibility claims, recurrence claims, reported-claim claims, current-state claims, historical claims, authority claims, and implementation claims. |
| Temporal provenance | Preserves when a packet was observed, published, copied, refreshed, stale, or relevant; without it, repetition may be stale amplification. |
| Support path | Shows how evidence reaches the claim and whether paths are independent, derivative, copied, inferred, or unknown. |
| Confidence | Calibrates support or selection strength; it is not certainty, truth, authority, or independence. |
| Unknown preservation | Prevents missing independence, provenance, authority, support, claim form, or confidence from being inferred through. |

## 10. Unknowns that must remain when source independence cannot be established

The following must remain Unknown rather than filled by source count:

- whether sources are independent;
- whether packets share an upstream source;
- whether repetition is copied, syndicated, summarized, or independently observed;
- whether agreement covers the exact claim or only an adjacent detail;
- whether source authority reaches the claim;
- whether the claim form permits corroborative use;
- whether temporal provenance aligns;
- whether sources share method, vantage point, data source, adapter, or failure domain;
- whether contradiction exists in the same scope;
- whether confidence should increase;
- whether lawful reliance is permitted;
- whether any implementation change is warranted.

## 11. When multiple sources can lawfully increase evidentiary weight

Multiple sources can lawfully increase evidentiary weight only when all of the following are repository-supported for the bounded claim:

1. the claim form is identified;
2. each packet has provenance;
3. each packet's source role and authority boundary are preserved;
4. overlap or compatibility is exact enough for the claim;
5. dependency analysis supports meaningful independence or separates repeated support from independent support;
6. time, scope, predicate, dimensions, and vantage point are preserved;
7. contradictions and conflicts remain visible;
8. confidence is calibrated rather than converted to certainty;
9. Unknowns are preserved;
10. a competent local boundary permits the evidence to support the claim at the asserted strength.

Even then, the lawful result is increased evidentiary support or confidence for that scoped claim, not truth by count and not general authority.

## 12. When multiple sources must remain only source count, visibility, or repetition

Multiple sources must remain only source count, visibility, repetition, copied assertion, syndication, or shared-origin amplification when the repository lacks preserved evidence for independence, provenance, source role, authority, temporal alignment, dependency, support path, claim-form match, or confidence calibration.

Examples of lawful weak conclusions:

- `many packets say X`;
- `X appears in multiple places`;
- `X was syndicated or copied`;
- `one upstream assertion became visible through many outlets`;
- `this claim has high visibility but unknown independence`.

Examples of overclaims that must be refused:

- `many packets independently corroborate X`;
- `agreement proves X`;
- `syndication supports X as independent evidence`;
- `source count creates authority`;
- `contradiction disproves X automatically`.

## 13. Lawful stop

The lawful stop condition is:

```text
Stop when source count, source volume, repetition, agreement, syndication, copied assertion, or shared-origin amplification is offered as independent corroboration without preserved provenance, source role, source authority, claim form, temporal provenance, support path, dependency/independence evidence, confidence limits, and Unknown preservation.
```

At that stop, Seed may report count, visibility, recurrence, copied repetition, possible syndication, or Unknown independence. It must not promote the material into independent support, warrant, truth, disproof, source authority, source scoring, or implementation pressure.

## 14. Does this investigation create implementation pressure?

No.

This investigation is constitutional clarification only. It does not identify a failing command, diagnostic gap, app surface defect, schema gap, test gap, or concrete repository behavior that requires implementation.

## 15. Does repository evidence support implementation work yet?

No.

Repository evidence supports the boundary discipline but not implementation work. Existing app-visible surfaces and documents are sufficient for this bounded investigation: diagnostic inventory, diagnostic shape audit, knowledge reachability, evidence/fact-support/source-navigation concepts, warrant, lawful reliance, lawful acceptance, claim strength, corroboration, contradiction, Unknown preservation, and lawful stop.

No source-independence schema, source scoring, corroboration scoring, authority scoring, credibility scoring, truth engine, legal research engine, public-world workflow, diagnostic surface, or ontology promotion is supported.

## Supported conclusions

1. Source independence is constitutionally recoverable only as meaningful support-path separation for a bounded claim, not as a public-world source ontology.
2. Source count and source volume are count, recurrence, or visibility evidence, not independence, warrant, proof, truth, authority, or confidence by themselves.
3. Independent support differs from repeated appearance by preserved provenance, dependency, method, vantage point, temporal, source-role, source-authority, claim-form, support-path, confidence, and conflict boundaries.
4. Corroboration requires compatible support from multiple meaningfully separated paths for the scoped claim.
5. Copied repetition, syndication, and shared-origin amplification may increase visibility but do not multiply independent support.
6. Agreement is not warrant; disagreement and contradiction are not automatic disproof.
7. Missing independence evidence must remain Unknown.
8. Multiple sources can increase evidentiary weight only when repository evidence preserves independence and a competent boundary permits that support for the claim form.
9. No implementation work is supported.

## Unsupported conclusions

1. Unsupported: Source count proves source independence.
2. Unsupported: Source volume creates warrant.
3. Unsupported: Repetition creates proof.
4. Unsupported: Copied assertion is corroboration.
5. Unsupported: Syndication is independent observation.
6. Unsupported: Shared-origin amplification is independent support.
7. Unsupported: Agreement is warrant.
8. Unsupported: Contradiction is automatic disproof.
9. Unsupported: Source role creates truth, rank, score, ingestion authority, legal authority, historical completeness, or implementation pressure.
10. Unsupported: The repository currently needs a source-independence implementation.

## Implementation recommendation

No implementation work is recommended.
