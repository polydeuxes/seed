# Constitutional Legal Authority / Warrant Boundary Investigation

Repository authority wins.

## Bounded question

Across recurring repository evidence, when a human-provided public-world evidence packet contains legal materials such as constitutional text, amendments, ratification history, statutes, court opinions, regulations, contracts, or legal commentary, what constitutional boundary, if any, prevents Seed from treating:

```text
a legal source's claimed authority
```

as:

```text
constitutional warrant
```

without separately preserving source-of-law lineage, holding boundary, procedural posture, facts before the court, precedent dependency, temporal provenance, jurisdiction, authority limits, Unknowns, and lawful stop?

This is exactly one bounded constitutional investigation focused only on:

```text
Legal Authority != Constitutional Warrant
Court Holding Boundary != Constitutional Authority Boundary
```

It is not legal research, not case evaluation, not implementation, not a legal validity engine, not a constitutional validity engine, not a precedent engine, not source scoring, and not a source-of-law graph.

## App-visible evidence used

The app was used as bounded repository evidence only. It was not treated as an oracle and was not used to fetch or evaluate public-world legal material.

Reviewed commands:

```text
python scripts/seed_local.py --help
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-subject "legal authority" --knowledge-reachability-audit-limit 20
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-subject "constitutional warrant" --knowledge-reachability-audit-limit 20
python scripts/seed_local.py --question-surface-inventory
```

App-visible findings:

- The CLI exposes repository visibility surfaces including `--diagnostic-inventory`, `--diagnostic-shape-audit`, `--reasoning-path`, `--selection-path`, `--reference-selection`, `--knowledge-reachability-audit`, `--question-surface-inventory`, and related read-only inquiry/diagnostic surfaces.
- `--knowledge-reachability-audit --knowledge-reachability-audit-subject "legal authority"` classified the phrase `legal authority` as a `presentation_label` with `Preserved=no`, `Projected=no`, `Read Model=no`, `Inquiry Orientation=no`, `Rendered=no`, and first loss at `not_preserved`.
- `--knowledge-reachability-audit --knowledge-reachability-audit-subject "constitutional warrant"` likewise classified the operator phrase as a `presentation_label` with first loss at `not_preserved` in that app run. That does not erase existing warrant documents; it shows that a bare operator-supplied phrase is not automatically a preserved runtime/read-model candidate.
- `--question-surface-inventory` reports that `knowledge reachability` is an eligible read-only audit over projected and repository evidence with no recording and no mutation. It also reports read-only/no-recording/no-mutation boundaries for surfaces such as operational pressure, operational story, reasoning path, and selection path.

These app surfaces support only bounded visibility about current repository surfaces, reachability, and public inquiry/diagnostic boundaries. They do not decide legal meaning, public-world truth, constitutional validity, or implementation readiness.

## Reviewed repository evidence

Reviewed repository evidence included:

- `constitutional_public_evidence_packet_readiness_investigation.md`
- `constitutional_external_source_role_boundary_investigation.md`
- `constitutional_source_independence_boundary_investigation.md`
- `constitutional_authority_volume_boundary_investigation.md`
- `constitutional_narrative_history_boundary_investigation.md`
- `constitutional_repetition_proof_boundary_investigation.md`
- `constitutional_warrant_characterization.md`
- `constitutional_warrant_global_characterization.md`
- `constitutional_authority_characterization.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/corroboration_and_fact_promotion_reconciliation.md`
- implementation and diagnostic visibility evidence where relevant: question surface inventory, knowledge reachability, diagnostic inventory, diagnostic shape audit, reasoning path, selection path, source navigation, fact support, event/history/provenance boundary documents, and Unknown/lawful-stop investigations.

## Legal-authority analysis

Repository evidence does not currently define a full legal-source model or a general legal-authority ontology.

The smaller supported meaning is source-local and domain-local:

```text
legal authority = a bounded source-role or domain-role claim that a legal artifact, issuer, forum, or instrument has authority for a particular legal-source function, not general truth authority and not constitutional warrant by itself.
```

The public evidence packet readiness investigation already states that legal text, court opinions, statutes, regulations, and contracts may have source-local or domain-local authority for bounded legal artifacts: text existed, an issuing body spoke, a contract says particular words, or a court published an opinion. It also says legal source status is not general truth authority about all factual, historical, technical, vendor, or social claims contained in or surrounding the document.

That is the strongest repository-supported legal-authority boundary. A legal source can support narrower source-attributed claim forms such as:

- `this constitution text contains these words at this cited version`;
- `this amendment text is represented by this source as adopted text`;
- `this statute source says these enacted words`;
- `this regulation source says this agency promulgated text`;
- `this court opinion states this holding/reasoning/background`;
- `this contract contains these terms between these parties`;
- `this commentary argues or summarizes X`.

But legal-source authority does not automatically support broader claims such as:

- `the legal source is constitutionally warranted`;
- `the court's claimed boundary equals the Constitution's boundary`;
- `the factual premises are historically true`;
- `the precedent chain is independently warranted`;
- `the doctrine is valid for all jurisdictions or times`;
- `Seed may treat the source as truth, legality, invalidity, or implementation pressure`.

## Constitutional-warrant analysis

Repository evidence already gives a stronger and more general meaning to constitutional warrant than to legal authority:

```text
Constitutional warrant is evidence-bound lawful reliance under preserved authority boundary.
```

The warrant characterization says a bounded subject, relation, value, claim, agreement, unknown, or inquiry condition may be lawfully relied upon only when repository evidence, provenance/support, role, authority limit, negative authority, Unknowns, and confidence limit have been preserved. The global warrant characterization further treats warrant as a constitutional reliance invariant that prevents content from becoming more than the evidence authorizes when it moves across forms, neighborhoods, districts, and inquiry artifacts.

Therefore constitutional warrant requires at least:

- evidence binding;
- provenance/support preservation;
- selected bounded content;
- preserved role;
- granted authority boundary;
- negative authority;
- Unknown preservation;
- confidence or evidence-strength calibration where supported;
- stop or non-promotion discipline when evidence ends.

Legal source status can be one input into role or provenance. It is not the warrant itself.

## What distinguishes legal authority from constitutional warrant?

Legal authority is source-role authority. Constitutional warrant is repository-supported lawful reliance under preserved boundary.

The distinction is:

| Concern | Legal authority | Constitutional warrant |
| --- | --- | --- |
| Primary question | What legal-source function does this artifact, issuer, court, statute, regulation, contract, or commentary claim or possess? | What may Seed lawfully rely on, in what bounded role, with what evidence/support, limits, Unknowns, confidence, and stop condition? |
| Scope | Source-local, jurisdictional, temporal, procedural, role-bound. | Claim-bound and repository-evidence-bound. |
| Typical support | Artifact identity, issuer, forum, citation, version/date, jurisdiction, text, procedural status, legal-source role. | Evidence binding, source/support provenance, role, authority boundary, negative authority, Unknowns, confidence, non-promotion. |
| Failure mode | Treating legal formality as truth or constitutional correctness. | Dropping support/limits and promoting beyond evidence. |
| Lawful output when incomplete | Unknown legal role, unknown jurisdiction, unknown posture, unknown currentness. | Unknown or lawful stop. |

A court may have legal authority to decide a case and publish an opinion. That does not make every statement in the opinion constitutionally warranted for Seed. A statute may be enacted legal text. That does not prove its constitutionality, historical accuracy, or lawful boundary for all claim forms. A contract may bind parties under some legal regime. That does not prove performance or public-world truth.

## Court-opinion / court-holding analysis

Repository evidence does not provide a legal doctrine engine for holdings. The smaller supported distinction is a source-role/claim-form distinction:

```text
court opinion = legal artifact containing a court's published text, including disposition, holding-like statements, reasoning, factual background, procedural posture, cited authorities, dicta-like statements, and narrative.

court holding = the bounded decision rule or resolved issue necessary to the court's disposition, only insofar as the reviewed legal source and competent support identify it.
```

Seed must not infer a holding merely because an opinion contains emphatic language, broad framing, repeated citations, or self-described scope. If the packet does not expose competent holding identification, the holding boundary remains Unknown.

A court opinion can support `the court said X`. It does not automatically support `X is the holding`, `X is constitutional warrant`, or `X is historical truth`.

## Holding / dicta / reasoning / fact / posture analysis

Repository evidence supports preserving different claim forms rather than collapsing them:

- **Holding boundary:** what was necessary to decide the dispute, if competent source support identifies it.
- **Dicta-like material:** statements not shown to be necessary to the disposition; may be source-attributed text but not holding unless separately supported.
- **Reasoning path:** arguments, analogies, tests, doctrines, interpretive moves, and precedent chains used by the court; they can explain the holding but are not automatically independent warrant.
- **Factual premises:** facts asserted, assumed, stipulated, found, noticed, or narrated in the opinion; they are not historical truth merely because the opinion states them.
- **Procedural posture:** appeal posture, motion posture, standard of review, record limits, party admissions, preservation, burden, remedy, and jurisdictional posture; these constrain what the court actually decided.
- **Narrative background:** story-like framing or history in the opinion; repository evidence rejects narrative as history without provenance and support.

The public packet, source-role, repetition/proof, and narrative/history boundaries all require that these roles remain separate. Missing posture, facts, record, or source support must remain Unknown rather than silently converted into holding or warrant.

## Self-described-boundary / source-derived-boundary analysis

A court's self-described boundary is evidence that the court claimed or framed a boundary. It is not proof that the claimed boundary equals the Constitution's lawful boundary.

A source-derived constitutional boundary would require separately preserved source-of-law support: constitutional text, amendment text, ratification provenance where relevant, jurisdiction, temporal provenance, lawful source chain, competent interpretation support if the repository has authority to rely on it, negative authority, Unknowns, and lawful stop. The repository does not currently implement a source-of-law graph or constitutional validity engine, so Seed must not promote a court's self-description into constitutional authority.

The supported claim form is narrower:

```text
This opinion describes its boundary as X.
```

Unsupported without separate warrant:

```text
The Constitution's lawful boundary is X because the opinion says so.
```

## Precedent-dependency analysis

Precedent dependency is not independent constitutional support.

A precedent chain may show that one legal source relies on earlier legal sources. That can be useful provenance for doctrine movement, legal-source lineage, or source-attributed reasoning. But dependency is not independence. If Case C cites Case B, which cites Case A, that may be a chain of authority within a legal system, not multiple independent source-of-law warrants.

For Seed, the lawful questions are:

- What source did this opinion rely on?
- Is the cited source legal text, prior holding, reasoning, factual assertion, commentary, or background?
- Is the support path circular, dependent, stale, overruled, jurisdiction-limited, procedurally limited, or Unknown?
- Does any cited source independently connect to constitutional text, amendment text, ratification provenance, or source-of-law support?

If the chain only repeats prior doctrine without source-of-law support visible to the packet/repository, Seed preserves precedent dependency as dependency, not independent warrant.

## Repeated-citation analysis

Repeated citation of a case is not independent warrant.

The repetition/proof investigation states that repeated assertion can show recurrence, salience, or pattern, but proof of a stronger claim requires local support, source independence, authority boundary, claim-strength match, and Unknown preservation. The source-independence investigation similarly distinguishes independent support paths from copied, circular, syndicated, derivative, same-origin, or merely repeated support.

Therefore:

```text
many legal sources cite Case X
```

may support a bounded recurrence/source-navigation claim:

```text
Case X is repeatedly cited in this packet/corpus for proposition Y.
```

It does not by itself support:

```text
Proposition Y is constitutionally warranted.
```

Repeated citation remains weak or source-dependent unless the packet exposes independent source-of-law support, non-circular provenance, jurisdiction/temporal fit, and competent claim-form boundaries.

## Legal validity / enforceability / constitutional warrant / historical truth

Repository evidence supports keeping these separate:

| Term | Bounded meaning in this investigation | Not the same as |
| --- | --- | --- |
| Legal validity | A legal-system status claim that a source, rule, judgment, contract, statute, regulation, or doctrine is valid under some authority, time, jurisdiction, and procedure. Repository evidence does not currently let Seed decide this generally. | Constitutional warrant, historical truth, legal enforceability, Seed truth. |
| Legal enforceability | A claim that a source or obligation can be enforced by a competent legal institution under specific conditions. Not currently decidable by Seed absent competent support. | Text existence, constitutional warrant, historical truth. |
| Constitutional warrant | Seed's evidence-bound lawful reliance under preserved authority boundary. | Legal authority, legal validity, enforceability, truth. |
| Historical truth | A claim that an event occurred or a condition existed in the world. Repository event/history evidence distinguishes recorded history/provenance from objective truth. | Narrative, court factual background, repeated statement, legal authority. |

A court opinion might be legally authoritative for its holding, enforceable as a judgment, source-attributable as published text, historically relevant as an event, and still not constitutionally warranted for broader claims without separate support.

## Source-of-law provenance analysis

Source-of-law provenance is the preserved path showing why a legal source can support a legal or constitutional claim. Repository evidence supports the need to preserve provenance/support for warrant, but does not support implementing a source-of-law graph here.

For legal materials, source-of-law provenance may include:

- artifact identity and stable citation;
- issuer/adopter/forum/parties;
- jurisdiction;
- date/version/effective period;
- amendment or ratification provenance where relevant;
- enactment/promulgation/adoption path where relevant;
- case procedural posture and holding boundary where relevant;
- precedent dependency and negative treatment where relevant;
- record/facts before the court where relevant;
- claim form and support path;
- confidence and Unknowns.

Without this provenance, legal material may still be preserved as `source said/contains X`, but not promoted into constitutional warrant.

## Constitutional-text / amendment / ratification / statute / regulation / contract / commentary source-role analysis

Repository evidence supports source roles as warrant-bounding provenance roles, not truth hierarchy. Applied narrowly:

| Source role | What it may support, if provenance is preserved | What it does not automatically support |
| --- | --- | --- |
| Constitutional text | The source's text and artifact/version identity; possible source material for source-of-law analysis. | Self-executing interpretation, every claimed boundary, modern doctrine, historical truth. |
| Amendment text | The text represented as amendment language and its source identity. | Proper ratification, scope, validity, current application, unless separately supported. |
| Ratification history | Source-attributed records or narratives about ratification events, debates, votes, procedures, or timing. | Historical truth or valid ratification by mere narrative or repetition. |
| Statute | Enacted or published statutory text within a jurisdiction/version. | Constitutionality, enforceability, factual truth, universal legality. |
| Regulation | Agency or administrative text within source/jurisdiction/version. | Statutory/constitutional validity, factual truth, universal enforceability. |
| Court opinion | Published court artifact, what the court said, and possibly a holding if competently identified. | Constitutional truth, historical truth, all reasoning as holding, self-described boundary as source-of-law boundary. |
| Contract | Text/terms represented in an agreement among parties. | Performance, enforceability, legality, public truth. |
| Legal commentary | A commentator's analysis, summary, argument, or interpretation. | Legal truth, constitutional warrant, source-of-law authority, independent support by itself. |

## Jurisdiction / temporal-provenance analysis

Jurisdiction and temporal provenance are authority boundaries.

A legal source's authority may depend on forum, sovereign, court hierarchy, agency authority, parties, territory, date, effective period, procedural posture, later amendment, later enactment, later overruling, later repeal, or later interpretive change. The time provenance audit's broader repository lesson applies: a timestamp is not self-authorizing, and publication time, occurrence time, observation time, retrieval time, preservation time, effective time, and revision time can differ.

Missing jurisdiction or temporal provenance prevents strong claims. Seed may preserve `source contains X` or `packet included X`; it must not infer current legal validity, controlling authority, constitutional warrant, or historical truth.

## Authority-boundary analysis

Authority is a constitutional boundary condition that governs lawful movement, reliance, promotion, and stop. Legal-source authority is one bounded role inside that larger authority discipline.

The boundary prevents these promotions unless separately supported:

```text
legal source -> truth
legal source -> constitutional warrant
court opinion -> holding for all statements
holding -> constitutional authority boundary
precedent chain -> source-of-law support
repeated citation -> independent warrant
court factual background -> historical truth
legal validity -> enforceability -> constitutional warrant
```

The authority boundary permits narrower preservation:

```text
legal source -> source-attributed artifact/text/claim
court opinion -> court said/published/decided under identified limits
holding candidate -> Unknown unless competent support identifies holding boundary
precedent citation -> dependency/provenance marker
repetition -> recurrence marker
```

## Confidence / claim-strength analysis

Claim strength must match evidence strength.

High confidence may be appropriate for a narrow claim such as `this repository document says legal sources are not general truth authority` when directly reviewed. Lower confidence is appropriate for legal-domain distinctions not implemented by the repository, such as dicta/holding mechanics, negative legal authority, or constitutional source-of-law lineage. Those can be preserved as investigation boundaries, not as runtime semantics.

The lawful claim-strength ladder is:

1. Strongest supported: repository evidence requires source role, authority, provenance, claim form, Unknowns, confidence, and lawful stop before relying on public-world/legal materials.
2. Supported: legal-source status is source-local/domain-local and not general truth authority.
3. Supported by analogy and packet-readiness evidence: court opinion status is not the same as holding, and holding is not the same as constitutional warrant.
4. Unsupported: Seed currently has a legal validity, constitutional validity, precedent, or source-of-law engine.

## Unknown preservation

The following must remain Unknown when not exposed by packet materials or repository evidence:

- whether Seed has a legal-source model beyond source-role boundaries;
- legal provenance;
- source-of-law lineage;
- constitutional text version and source identity;
- amendment ratification provenance;
- jurisdiction;
- currentness and temporal provenance;
- legal authority scope;
- holding boundary;
- dicta/reasoning/fact/posture distinction;
- procedural posture;
- facts before the court and record limits;
- precedent dependency and negative authority;
- whether cited sources are independent or circular;
- whether repeated citations add independent support;
- whether a source's claimed boundary matches a source-derived constitutional boundary;
- legal validity;
- legal enforceability;
- constitutional validity;
- constitutional warrant beyond the narrow source-attributed claim;
- historical truth of narratives or factual premises;
- confidence/evidence strength where not supported.

Unknown preservation is a lawful result, not a failure.

## Lawful stop

Seed must stop before declaring invalidity, validity, legality, enforceability, historical truth, or constitutional warrant when support is missing.

The lawful stop condition is:

```text
If the evidence only supports source-attributed legal material, Seed may preserve that source-attributed role and its limits, but must stop before promoting it into constitutional warrant, legal validity, legal invalidity, enforceability, historical truth, implementation pressure, or repository ontology.
```

Specific stop triggers include:

- missing source-of-law lineage;
- missing jurisdiction;
- missing temporal provenance or currentness;
- missing ratification provenance;
- missing procedural posture;
- missing facts before the court;
- missing holding boundary;
- missing precedent dependency/negative authority review;
- repeated citation without independence support;
- court self-description without source-derived support;
- legal commentary without competent source-of-law support;
- operator request pressure without repository implementation failure.

## Required analysis answers

1. **What does repository evidence already mean by legal authority, if anything?** It means, at most here, bounded source-local/domain-local authority for a legal artifact or issuer's legal-source function. It is not general truth authority and not constitutional warrant.

2. **What does repository evidence already mean by constitutional warrant?** Evidence-bound lawful reliance under preserved authority boundary, including evidence/support, provenance, role, authority limit, negative authority, Unknowns, confidence, and stop discipline.

3. **What distinguishes legal authority from constitutional warrant?** Legal authority identifies a legal-source role or claim of authority; constitutional warrant identifies what Seed may lawfully rely on after repository evidence and boundary preservation. Legal authority may contribute role/provenance; it is not sufficient warrant.

4. **What distinguishes a court opinion from a court holding?** An opinion is the published artifact. A holding is the bounded decision rule or resolved issue necessary to disposition, only if competently identified. The repository does not authorize Seed to infer all opinion text as holding.

5. **What distinguishes holding from dicta, reasoning, factual premises, procedural posture, or narrative background?** Claim form and necessity to disposition distinguish them. Reasoning explains; facts are asserted/assumed/found within record limits; posture constrains what was decided; narrative frames. None automatically becomes holding or historical truth.

6. **What distinguishes a court's self-described boundary from a source-derived constitutional boundary?** Self-description is what the court says. A source-derived constitutional boundary would require preserved constitutional/source-of-law support beyond the court's assertion. The latter is unsupported here as an engine or adjudication.

7. **What distinguishes precedent dependency from independent constitutional support?** Dependency traces reliance on prior legal sources. Independent constitutional support requires non-circular source-of-law support such as constitutional text/provenance within proper boundaries. A citation chain alone is dependency, not independence.

8. **What distinguishes repeated citation of a case from independent warrant?** Repeated citation shows recurrence or source salience. Independent warrant requires independent support paths, provenance, authority boundary, claim-strength match, and Unknown preservation.

9. **What distinguishes legal validity, legal enforceability, constitutional warrant, and historical truth?** Legal validity and enforceability are legal-system status claims under specific authority. Constitutional warrant is Seed's evidence-bound reliance boundary. Historical truth concerns what happened. None collapses into the others.

10. **What distinguishes constitutional text, amendment text, ratification history, statute, regulation, court opinion, contract, and legal commentary as source roles?** Each has a different source-local claim form: text, represented amendment, ratification record/narrative, enacted text, agency text, published court artifact, agreement terms, or commentary. None automatically supplies truth or constitutional warrant for stronger claims.

11. **What role do provenance, jurisdiction, temporal provenance, source-of-law lineage, claim form, authority boundary, negative authority, confidence, and Unknown preservation play?** They bound lawful reliance and prevent overpromotion. Missing values narrow the lawful claim to source attribution or require stop.

12. **What Unknowns must remain when legal source provenance, ratification provenance, precedent dependency, jurisdiction, procedural posture, facts, or source-of-law support are missing?** The corresponding authority scope, currentness, validity, holding boundary, fact truth, independence, source-of-law support, legal enforceability, constitutional warrant, and confidence must remain Unknown.

13. **What lawful stop condition prevents Seed from declaring invalidity, truth, legality, or constitutional warrant beyond supported evidence?** Stop when evidence supports only source-attributed material or role but lacks competent support for invalidity, truth, legality, constitutional warrant, or implementation movement.

14. **Does this investigation create implementation pressure?** No. It preserves a constitutional boundary and refuses implementation pressure.

15. **Does repository evidence support implementation work yet?** No concrete repository failure was found. Repository evidence supports documentation-only boundary preservation, not implementation.

## Supported conclusions

1. Legal-source status is source-local/domain-local and claim-bounded; it is not general truth authority.
2. Constitutional warrant is evidence-bound lawful reliance under preserved authority boundary.
3. A legal source's claimed authority may be preserved as a claim/role, but cannot be promoted into constitutional warrant without separate evidence binding, provenance/support, authority boundary, negative authority, Unknown preservation, and confidence calibration.
4. A court opinion is not identical to a court holding. Holding identification requires competent support; absent that support, holding boundary remains Unknown.
5. Holding, dicta-like statements, reasoning, factual premises, procedural posture, and narrative background must not be collapsed.
6. A court's self-described boundary is not proof of a source-derived constitutional boundary.
7. Precedent dependency and repeated citation are not independent constitutional support.
8. Legal validity, legal enforceability, constitutional warrant, and historical truth are distinct claim forms.
9. Constitutional text, amendment text, ratification history, statutes, regulations, court opinions, contracts, and commentary are different source roles, not a truth hierarchy.
10. Missing provenance, jurisdiction, temporal provenance, procedural posture, facts, precedent dependency, source-of-law lineage, ratification evidence, authority, claim form, confidence, or support must remain Unknown.
11. Lawful stop prevents Seed from declaring invalidity, truth, legality, enforceability, or constitutional warrant beyond supported evidence.
12. No implementation work is supported by this investigation.

## Unsupported conclusions

Repository evidence does not support concluding that:

- Seed already has a legal-source ontology;
- Seed should implement a legal research engine;
- Seed should implement a legal validity or constitutional validity engine;
- Seed should implement a precedent engine;
- Seed should implement a source-of-law graph;
- Supreme Court authority, court authority, statutory authority, or legal commentary is constitutional truth;
- a court's claimed boundary proves the Constitution's boundary;
- repeated citation proves independent warrant;
- legal validity, enforceability, constitutional warrant, and historical truth are interchangeable;
- any real case, doctrine, amendment, statute, regulation, contract, or commentary is valid or invalid;
- any public-world legal conclusion is ready for ingestion, projection, scoring, or implementation.

## Implementation recommendation

No implementation recommendation.

This investigation found boundary discipline, not a concrete repository failure. It does not add or modify diagnostics, audits, CLI flags, records, app surfaces, schemas, source scoring, legal scoring, authority scoring, or event-ledger behavior. Therefore no diagnostic inventory or diagnostic shape-audit change is required.
