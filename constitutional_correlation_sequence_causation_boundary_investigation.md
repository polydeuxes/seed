# Constitutional Correlation / Sequence / Causation Boundary Investigation

## Bounded question

Across recurring repository evidence, when Seed receives or produces a claim that `X` and `Y` are associated, sequenced, adjacent, co-occurring, similarly patterned, or narratively linked, what prevents Seed from treating that relationship as proof that `X caused Y` without separately preserved event evidence, causal mechanism or dependency evidence, temporal provenance, affected-subject or impact evidence where relevant, source authority, claim form, support path, confidence limits, Unknowns, and lawful stop?

This is exactly one bounded constitutional investigation: **Correlation / Sequence != Causation**. It does not implement anything, create a causation schema, create a causal graph, create a statistical/scientific/legal/root-cause engine, evaluate any real-world claim, or promote causation vocabulary into ontology.

## App-visible evidence used

The app was used as bounded repository evidence, not as an oracle.

### `python scripts/seed_local.py --correlation-audit --json`

The current app output reported one read-only correlation finding for Consumer Audit. The finding said predicates or diagnostics without implementation consumers remain explanatory only. Its guardrails were `diagnostic_only`, `does_not_infer_ownership`, `does_not_write_facts`, and `does_not_mutate_cluster`. Metadata reported `mode=read_only`, `records_facts=false`, `mutates_cluster=false`, and scope `current_projection_and_repository_surfaces`.

This is direct app-visible evidence that the repository already treats correlation-like visibility as a bounded audit surface, not as fact-writing, cluster mutation, ownership inference, or implementation authority.

### `python scripts/seed_local.py --history-brief --json`

The current app output reported:

- `historical_confidence.correlation = visible when repository and operational state are both observed`;
- `historical_confidence.causation = not proven`;
- unsupported conclusion: `causal link between repository change and operational change`, with reason `correlation may be visible, but causation is not proven by existing surfaces`;
- `writes_event_ledger=false` and `mutates_cluster=false`.

This is direct app-visible evidence that the repository already distinguishes visible correlation from proven causation.

### `python scripts/seed_local.py --diagnostic-inventory --json`

The app-visible diagnostic inventory declares read-only and diagnostic surfaces with fields including `writes_event_ledger`, `record_scope`, `emits_diagnostic_facts`, `mutates_cluster`, `uses_projected_state`, and `uses_repo_files`. For `knowledge_reachability`, the inventory says it audits knowledge reachability across projected, repository, inquiry, and rendered surfaces, supports JSON, uses projected state and repo files, writes no event ledger, and does not mutate cluster.

This supports a diagnostic-boundary rule: diagnostic presence or adjacency must preserve its own surface shape and mutation boundary before it can be used as evidence for any stronger claim.

### `python scripts/seed_local.py --diagnostic-shape-audit --json`

The current app output showed declared and observed fields such as `supports_record`, `supports_json`, `record_scope`, `emits_diagnostic_facts`, `writes_event_ledger`, `uses_repo_files`, `uses_projected_state`, and `mutates_cluster` matching for diagnostic surfaces. This supports the repository rule that operational outputs have auditable shape boundaries rather than implicit authority.

## Reviewed repository evidence

Reviewed repository evidence included:

- `seed_runtime/correlation_audit.py`, especially the read-only correlation audit, guardrails, and metadata.
- `seed_runtime/history_brief.py`, especially confidence fields and unsupported causation conclusions.
- `seed_runtime/knowledge/relationship_observation.py`, especially import/definition relationship boundaries.
- `constitutional_risk_harm_boundary_investigation.md`, especially harm/causation distinction, causal support, affected-subject evidence, impact evidence, confidence, Unknown preservation, and lawful stop.
- `constitutional_capability_use_boundary_investigation.md`, especially enabled/use, use/causation, feature/event, logs, and source-role distinctions.
- `constitutional_translation_rendering_source_equivalence_boundary_investigation.md`, especially transformed representation/source authority, confidence/evidence strength, and lawful stop.
- `docs/evidence_trust_and_source_authority_reconciliation.md`, especially repetition, independent corroboration, confidence, and trust boundaries.
- `docs/claim_strength_and_assertion_semantics_reconciliation.md`, especially claim form and non-interchangeability of observation, evidence, fact, relationship, projection, response, current-state, historical, verified, and believed claims.
- `unknown_currency_survey.md`, especially Unknown as a lawful stop / insufficient-evidence preservation artifact.
- `time_selection_relationship_spymaster.md`, especially temporal provenance and authority separation.
- `docs/cross_substrate_structural_coincidence_audit.md`, especially coincidence observation not proving semantic alignment, ownership, behavior, invocation, reachability, family completion, or architectural authority.

## 1. What repository evidence already means by correlation, association, sequence, adjacency, or pattern

Repository evidence does not support a general statistical or causal definition of correlation. It supports smaller, bounded meanings:

- **Correlation**: visible co-presence or comparable movement across repository/operational surfaces. The history brief can report that correlation is visible when repository and operational state are both observed, while causation remains not proven.
- **Association**: a relationship-like or support-path connection that may be preserved as a claim, relationship, or candidate boundary, but not as behavior or causation.
- **Co-occurrence**: two items appear in the same packet, output, snapshot, narrative, or evidence set. Current evidence treats that as visibility only unless a separate claim form and support path make a stronger assertion lawful.
- **Temporal sequence**: one preserved time or event appears before another. Time evidence distinguishes occurrence time, observation time, source assertion time, knowledge time, and preservation time; sequence does not merge those authorities.
- **Proximity / adjacency**: closeness in time, logs, diagnostics, text, output rows, repository paths, or narrative presentation. It is a candidate investigative signal, not a mechanism or dependency.
- **Pattern / trend / coincident change**: repeated or comparable shape over observations. Repetition can support a bounded repeated-observation claim, but repository evidence separates repetition from independent corroboration and from truth.
- **Narrative linkage**: presentation or history can place items in relation, but narrative is not itself causal evidence.
- **Diagnostic adjacency / log adjacency**: bounded visibility inside an operational output or event record. It is constrained by diagnostic inventory, shape audit, record scope, event-ledger boundary, and mutation boundary.

## 2. What repository evidence already means by causation

Repository evidence supports only narrow existing uses:

1. **Runtime/event metadata** has a `causation_id`, but this is event lineage/context metadata, not a constitutional model that proves public-world or system causation.
2. **History Brief** explicitly says causation is `not proven` and preserves causal-link conclusions as unsupported when only correlation is visible.
3. **Risk/Harm and Capability/Use investigations** treat causation as a stronger relationship requiring separate causal support, not as a consequence of risk, harm, use, sequence, or adjacency.

The repository does not currently support a general causation ontology, causal graph, causal mechanism engine, legal causation engine, scientific causation engine, root-cause engine, or statistical-correlation engine.

## 3. Sequence / causation distinction: `X happened before Y` vs `X caused Y`

`X happened before Y` is a temporal-order claim. It requires event identity, source material, time boundary, observation/source time distinctions, clock/version caveats, and support path.

`X caused Y` is a causal-attribution claim. It requires the temporal claim plus causal support appropriate to the asserted strength: mechanism, dependency, contribution, affected subject or impact where relevant, source authority, confidence limits, alternative-path/Unknown preservation, and lawful authority to make the causal assertion.

Sequence is compatible with causation, but not sufficient for causation. Sequence can support investigation pressure: `X is a candidate predecessor to inspect`. It cannot by itself support `X caused Y`, `X was necessary`, `X was sufficient`, `X materially contributed`, `X legally caused`, `X explains`, or `X proves conduct`.

## 4. Temporal proximity / mechanism distinction

Temporal proximity says `X` and `Y` happened close together or were observed close together. Mechanism says there is a preserved process, dependency, pathway, rule, technical linkage, legal theory, scientific account, or other competent explanatory bridge by which `X` could produce `Y` under the claim's domain.

Proximity may help select a question. It does not describe the production path. A log line before an error, a diagnostic row before another row, or a narrative paragraph before another paragraph is not a mechanism.

## 5. Co-occurrence / dependency distinction

Co-occurrence says `X` and `Y` appear together. Dependency says `Y` requires, imports, invokes, relies on, consumes, or is otherwise dependent on `X` under a preserved relation and scope.

Even repository relationship observations preserve this boundary. Import relationships are only dependency/name-availability evidence and do not prove behavior, calls, routes, boundaries, or ownership. Definition relationships are declaration evidence only and do not prove invocation, behavior, reachability, capability authority, or runtime ownership. Therefore co-occurrence is weaker than dependency, and dependency itself is weaker than causal effect unless the causal claim is separately supported.

## 6. Correlation / explanation distinction

Correlation can make a candidate relation visible. Explanation says why something occurred or why a claim should be accepted. Explanation requires a claim form, evidence path, warrant, confidence limits, and preserved Unknowns. Correlation without mechanism, dependency, source authority, temporal provenance, and alternatives is not explanation.

## 7. Repeated narrative linkage / causal-evidence distinction

Repeated narrative linkage proves, at most, that the narrative linkage repeated under preserved source, time, and transformation boundaries. Repository evidence separates repetition from independent corroboration. Repetition from one source path is not independent support, and repeated presentation is not truth.

A repeated story that `X caused Y` can support a bounded claim such as `source family S repeatedly attributed Y to X`. It cannot support `X caused Y` without independent causal support or competent authority for that stronger claim.

## 8. Source-attributed causation / independently supported causation distinction

A source-attributed causal claim says `source S says X caused Y`. Independently supported causation says separate support paths establish the causal relation under the relevant claim form.

Source role matters. A source may be competent to report its own assertion, log output, document, policy, contract, or observation. That does not automatically make it competent to prove causation, legal causation, scientific causation, or proof of conduct. Independent support requires support-path separation and authority boundaries, not source volume or repetition.

## 9. Model-inferred causation / causal-evidence distinction

A model-inferred causal claim says a model generated or inferred a causal relation. Repository evidence around model output, transformation, source authority, and claim strength blocks treating generated output as primary evidence.

Model output can be an orientation artifact, hypothesis, or transformed representation. It is not event evidence, source authority, mechanism evidence, affected-subject evidence, legal authority, scientific authority, or proof of conduct unless separately supported by repository evidence competent for the claim.

## 10. Diagnostic adjacency / implementation causation distinction

Diagnostic adjacency says a diagnostic surface exposed `X` near `Y`, or before `Y`, or in the same output. Implementation causation says a code path, event, state transition, dependency, or execution produced a result.

Diagnostic inventory and shape audit preserve whether a surface supports JSON, record, event-ledger writes, diagnostic facts, projected state, repository files, and cluster mutation. A diagnostic output that is read-only or diagnostic-scoped cannot become implementation causation or implementation pressure by adjacency. If a diagnostic supports `--record`, the diagnostic recording boundary still prevents diagnostic-only findings from becoming cluster truth.

## 11. Log adjacency / system causation distinction

Log adjacency says two log records, event records, or runtime trace entries are near each other. System causation says one system action produced another result.

Logs may support event occurrence if source identity, generation path, time, scope, retention, integrity, parsing, and deployment boundary are preserved. But a log showing an event before a result is not automatically a log showing cause. Causation requires a supported relationship between the event and result, not merely shared log source, actor, system, time, or correlation id.

## 12. Risk-and-harm co-presence / risk-caused-harm distinction

Risk-and-harm co-presence says risk material and harm material both exist in the same packet, narrative, source set, time window, or investigation. Risk-caused-harm says the risk produced the harm.

The risk/harm investigation already says harm is not causation. Risk, vulnerability, exposure, concern, unsafe design, possible harm, probable harm, alleged harm, and actual harm must not automatically become proof that a specific cause produced a specific effect. `risk X caused harm Y` requires bounded support that risk existed, bounded support that harm occurred, causal support linking X to Y, event sequence or mechanism where required, affected-subject and impact evidence, temporal provenance, source authority, confidence limits, alternatives, Unknowns, and authority to make the causation claim.

## 13. Actual use / caused result distinction

Actual use is occurrence or invocation. Caused result is a relationship between that use and an effect. A use-related record may be temporally adjacent to a result, but temporal adjacency is not causation.

Seed may say `X was used` only when use evidence supports occurrence. Seed may say `X caused Y` only when the support path also establishes the causal relation at the stated strength.

## 14. Harm / caused-by-X harm distinction

Harm is an injury, adverse effect, rights impact, operational damage, loss, deprivation, privacy invasion, security compromise, or other consequence claim. Caused-by-X harm adds a causal attribution.

Harm requires affected-subject and impact evidence. Caused-by-X harm requires those plus causal support connecting X to that harm. Actual harm is not legal harm, and harm is not proof of conduct.

## 15. Causal possibility / causal probability distinction

Causal possibility means the evidence has not ruled out that `X` could have caused or contributed to `Y`, or that a mechanism is plausible enough to investigate. It is a candidate/hypothesis/investigation-pressure claim.

Causal probability means support justifies a stronger likelihood claim under a preserved method, domain, evidence base, comparison set, source authority, and confidence rule. Possibility does not become probability merely because X preceded Y, appeared near Y, was risky, was used, or was named by a source/model.

## 16. Causal probability / proven causation distinction

Causal probability is an evidence-strength claim. Proven causation is an acceptance/proof claim under a specific domain, standard, source authority, method, and claim form.

Repository confidence evidence says confidence is not truth. Therefore even high confidence, probability language, repetition, source authority, or model confidence does not become proven causation without the separate proof conditions applicable to the claim.

## 17. Factual causation / legal causation distinction

Factual causation is a claim that X actually produced, contributed to, or was necessary/sufficient for Y under a fact/evidence path. Legal causation is a legal conclusion involving source-of-law authority, jurisdiction, legal standard, procedural posture, scope, limitations, negative authority, and warrant.

Repository evidence around legal authority and lawful reliance prevents policy, statute, warrant vocabulary, source assertion, factual sequence, or factual causation from becoming legal causation. This investigation performs no legal research and makes no legal causation determination.

## 18. Causation evidence / proof of conduct distinction

Causation evidence concerns a relationship between an alleged cause and an effect. Proof of conduct concerns whether a person, system, actor, process, or deployment did something. The same material may be relevant to both, but neither claim form proves the other.

For example, mechanism evidence may support how X could produce Y without proving a particular actor did X. A log may support event occurrence without proving legal conduct, culpability, intent, policy violation, or causation. Proof of conduct needs actor/system identity, event evidence, scope, authority, time, and confidence appropriate to the conduct claim.

## 19. Role of required evidence classes

- **Event evidence** preserves what happened, when, from which source/vantage point, and under what event boundary. It prevents possibility, availability, risk, documentation, or narrative from becoming occurrence.
- **Mechanism evidence** preserves how X could produce Y. It prevents proximity from becoming explanation.
- **Dependency evidence** preserves whether Y relies on X under a defined relation. It prevents co-occurrence from becoming dependence.
- **Temporal provenance** preserves occurrence time, observation time, source assertion time, knowledge time, projection time, and preservation time. It prevents sequence from becoming causal authority.
- **Affected-subject evidence** identifies who or what was affected where relevant. It prevents concern or generalized harm from becoming subject-specific effect.
- **Impact evidence** preserves injury, damage, effect, loss, output, or system impact. It prevents event or exposure from becoming harm.
- **Source authority** preserves what a source is competent to support. It prevents source-attributed causation from becoming independently supported causation.
- **Claim form** preserves whether Seed is making an association, temporal, observation, evidence, fact, relationship, projection, explanation, legal, scientific, conduct, probability, or proof claim.
- **Support path** preserves how the claim is supported and whether paths are independent.
- **Confidence / evidence strength** prevents possible, probable, source-reported, model-inferred, diagnostic, or repeated claims from becoming proven claims.
- **Unknown preservation** provides the lawful non-promotion result when support is missing, ambiguous, unsupported, stale, outside authority, or only presentation vocabulary.

## 20. Conditions for lawful bounded causation-related support from correlation, sequence, or association

Correlation, sequence, association, pattern, proximity, and adjacency can lawfully support bounded causation-related claims only when Seed states the smaller claim actually supported. Lawful examples:

- `X and Y were observed in the same packet P from source S at time T`.
- `X was observed before Y within source/log/output S under clock boundary C`.
- `X and Y changed together across comparable snapshots A and B`.
- `source S attributed Y to X`.
- `diagnostic D surfaced X before Y in read-only output O`.
- `X is a candidate causal hypothesis requiring separate mechanism/event/dependency support`.
- `causation remains Unknown / not proven`.

These claims must preserve source material, provenance, claim form, support path, authority boundary, confidence, and Unknowns. They must not be strengthened into causation, explanation, legal causation, scientific causation, proof of conduct, or implementation pressure.

## 21. Before Seed may say `X was associated with Y`

Seed must preserve:

1. the association claim form;
2. the observed relation or co-presence surface;
3. source material and source identity;
4. scope, packet/log/output/document/snapshot boundary;
5. time/provenance where relevant;
6. whether association means same source, same actor, same place, same time, same narrative, same diagnostic, same support path, or same relationship record;
7. confidence and support-path limits;
8. Unknowns and non-causation stop condition.

## 22. Before Seed may say `X happened before Y`

Seed must preserve:

1. event evidence for X;
2. event evidence for Y;
3. event identity and scope for each;
4. timestamps or ordering evidence;
5. clock/source/observation/preservation-time boundaries;
6. uncertainty, missing timestamps, ordering ambiguity, delayed logs, sampling, transformation, or retention caveats;
7. source authority for the temporal claim;
8. confidence and Unknowns;
9. explicit non-promotion into causation.

## 23. Before Seed may say `X caused Y`

Seed must preserve:

1. support that X occurred/existed under the relevant claim form;
2. support that Y occurred/existed under the relevant claim form;
3. causal mechanism, dependency, contribution, or other domain-appropriate causal evidence;
4. temporal provenance sufficient for the causal claim;
5. affected-subject and impact evidence where the effect is subject-specific or impact/harm-based;
6. source authority for causation, not merely source authority for reporting X or Y;
7. support path and independence where independent support is claimed;
8. confidence/evidence-strength limits;
9. alternatives, insufficiencies, contradictions, and Unknowns;
10. lawful authority to make a causal-attribution claim rather than merely report an attribution.

## 24. Before Seed may say `X legally caused Y`, `X scientifically caused Y`, or `X explains Y`

For `X legally caused Y`, Seed must preserve all factual-causation evidence plus legal authority, jurisdiction, legal standard, procedural posture, source-of-law lineage, scope, limitations, negative authority, temporal authority, confidence, and Unknowns. This investigation does not supply those.

For `X scientifically caused Y`, Seed must preserve domain-appropriate scientific method, data, measurement, mechanism, study/evaluation authority, assumptions, uncertainty, alternative explanations, reproducibility or methodological limits where relevant, and source authority. This investigation does not supply those.

For `X explains Y`, Seed must preserve the explanation claim form, evidence path, mechanism or explanatory warrant, scope, confidence, alternatives, Unknowns, and a lawful stop. Correlation alone does not explain.

## 25. Lawful stop condition

The lawful stop condition is reached whenever Seed has only correlation, association, co-occurrence, temporal sequence, proximity, adjacency, pattern, trend, coincident change, repeated narrative linkage, source-attributed causal claim, model-inferred causal claim, diagnostic adjacency, log adjacency, risk/harm co-presence, actual use plus later result, or harm evidence without separately preserved causal support and authority for the stronger claim.

At that point Seed must preserve the bounded smaller claim and stop at one of:

- association observed;
- sequence observed;
- co-occurrence observed;
- pattern/trend observed;
- source-attributed causation reported;
- model-inferred hypothesis only;
- diagnostic/log adjacency observed;
- candidate causal hypothesis;
- insufficient causal evidence;
- unsupported conclusion;
- Unknown;
- investigation pressure only.

Seed must not promote the material into causation, necessary cause, sufficient cause, contributing cause, proximate cause, legal causation, scientific causation, explanation, proof of conduct, or implementation pressure.

## 26. Does this investigation create implementation pressure?

No. This investigation is a bounded constitutional investigation. It does not add or modify diagnostics, audit surfaces, CLI flags, recordable output, schemas, graphs, engines, or runtime behavior. The reviewed app-visible surfaces already preserve the relevant read-only/non-mutation and causation-not-proven boundaries for their current scopes.

## 27. Does repository evidence support implementation work yet?

No concrete repository failure was found. Repository evidence supports a constitutional boundary and lawful stop condition, not implementation work. If future operational evidence shows a specific app surface silently promoting correlation, sequence, narrative linkage, diagnostic adjacency, or log adjacency into causation, then that concrete failure could warrant a bounded implementation investigation. Current evidence does not warrant implementation.

## Supported conclusions

1. Repository evidence supports the negative constitutional boundary: **Correlation / Sequence != Causation**.
2. Correlation, association, co-occurrence, sequence, proximity, adjacency, pattern, trend, coincident change, narrative linkage, source-attributed causal claim, model-inferred causal claim, diagnostic adjacency, and log adjacency are lawful investigation pressure only unless separately supported by claim-appropriate evidence.
3. Visible correlation may be reported as visible correlation, but History Brief evidence says causation remains not proven by that surface.
4. The existing Correlation Audit is read-only, writes no facts, mutates no cluster, and carries guardrails against ownership inference and mutation.
5. Relationship evidence can preserve dependency/name-availability or declaration, but it does not prove behavior, invocation, ownership, reachability, runtime authority, or causation.
6. Repetition is not independent corroboration. Repeated narrative linkage is not causal evidence unless the claim is only that the linkage repeated.
7. Source-attributed causation is not independently supported causation.
8. Model-inferred causation is not causal evidence.
9. Diagnostic adjacency is not implementation causation.
10. Log adjacency is not system causation.
11. Risk-and-harm co-presence is not risk-caused-harm.
12. Actual use is not caused result.
13. Harm is not caused-by-X harm.
14. Causal possibility is not causal probability.
15. Causal probability is not proven causation.
16. Factual causation is not legal causation.
17. Causation evidence is not proof of conduct.
18. Event evidence, mechanism/dependency evidence, temporal provenance, affected-subject/impact evidence, source authority, claim form, support path, confidence limits, Unknown preservation, and lawful stop are the core brakes.
19. The repository does not currently support a causation schema, causal graph, root-cause engine, statistical-correlation engine, legal-causation engine, scientific-causation engine, truth engine, source scoring, authority scoring, or credibility scoring.
20. No implementation work is recommended on current evidence.

## Unsupported conclusions

The reviewed evidence does not support concluding that:

- Seed has a general causation model;
- Seed has a causal graph or causal schema;
- Seed has a statistical inference engine;
- Seed has a scientific causation engine;
- Seed has a legal causation engine;
- Seed has a diagnostic root-cause engine;
- correlation currently proves explanation;
- sequence currently proves causation;
- proximity currently proves mechanism;
- co-occurrence currently proves dependency;
- repeated narrative linkage currently proves causal evidence;
- source-attributed causation currently proves independently supported causation;
- model-inferred causation currently proves causal evidence;
- diagnostic/log adjacency currently proves implementation or system causation;
- risk/harm co-presence currently proves risk-caused-harm;
- actual use currently proves caused result;
- harm currently proves caused-by-X harm;
- causal possibility or probability currently proves causation;
- factual causation currently proves legal causation;
- causation vocabulary should be promoted into ontology;
- any public-world X caused any public-world Y;
- implementation work is supported yet.

## Implementation recommendation

No implementation recommendation is made. Preserve this as a constitutional breadcrumb and lawful-stop discipline only.
