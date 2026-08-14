# Capability Demand / Realization Testimony / Reachability Topology Audit 001

## 1. Bounded question

Given one bounded requested transformation, what is the ownership order among capability demand, realization testimony, invocation-grammar evidence, behavioral evidence, and capability-reachability projection?

## 2. Fixed constitutional orientation

This audit uses the supplied orientation: capability is the warranted reachability of a bounded transformation under current State, evidence, recovered grammar, constraints, dependencies, and authority. It preserves these separations: mechanism possession is not capability; mechanism existence is not capability reachability; registered implementation is not validated invocation grammar; invocation grammar is not behavioral evidence; behavioral evidence is not general competency; demand is not projection; realization testimony is not selected realization; reachable transformation is not authorized execution; and the same mechanism with different evidence may warrant different bounded capability projections.

## 3. Methodology

I performed a read-only implementation-backed audit. I inspected the current examination handoff path, capability request precedent, inventory/projection owners, catalog/recommendation owners, registered operation schemas, precondition/authority-adjacent owners, direct tests, and grammar/examination records. I did not implement missing owners and did not inspect out-of-scope districts except where direct consumers or counterevidence required local context.

Read-only probes executed are listed in section 37. Baseline tests were run only for current behavior and failures were recorded rather than fixed.

## 4. Inspected owners

Inspected owners/artifacts:

- `ExaminationProbeRequest` and `OperationalRealizationHandoff` bind selected examination meaning, preserve exact artifact and representation identities, and explicitly do not choose an operational realization, authorize, execute, or create runtime Evidence/Fact. 【F:seed_runtime/examination_probe_request.py†L15-L22】【F:seed_runtime/examination_probe_request.py†L30-L45】
- `CandidateExaminationWorkSet` composes corpus member representation visibility with examination work contracts and emits compatibility observations such as `compatible`, `capability_unavailable`, `contract_unknown`, and `representation_unknown`. 【F:seed_runtime/candidate_examination_work.py†L60-L74】【F:seed_runtime/candidate_examination_work.py†L89-L107】
- `ToolNeed` preserves a requested capability name, reason, and desired input/output lists. 【F:seed_runtime/models.py†L112-L124】
- `ToolSpec` preserves registered-operation schema, policy action, implementation binding, status, visibility, capabilities, and examples. 【F:seed_runtime/models.py†L243-L260】
- `CapabilityCatalog` is read-only metadata for capability-to-provider recommendations and does not execute operations. 【F:seed_runtime/capability_catalog.py†L34-L44】【F:seed_runtime/capability_catalog.py†L81-L90】
- `CapabilityInventoryEntry` is a read-only verification belief over a capability string; inventory is built from registered operation labels, requested capabilities, and `capability_verified` facts, while explicitly separating registered operation metadata from admitted capability knowledge. 【F:seed_runtime/capability_inventory.py†L98-L127】【F:seed_runtime/capability_inventory.py†L145-L185】
- `SingleCapabilityStateProjection` correlates existing owner-produced artifacts for one normalized capability string and states that requested state proves demand only, catalog proves metadata only, provider recommendations are advisory, registered operations are contract associations, and no selection/execution/authorization occurs. 【F:seed_runtime/single_capability_state_projection.py†L19-L35】【F:seed_runtime/single_capability_state_projection.py†L66-L161】
- `PreconditionReport` is inspect-only readiness for legacy action plans and separates plan readiness from proposal authorization. 【F:seed_runtime/preconditions.py†L1-L6】【F:seed_runtime/preconditions.py†L33-L43】【F:seed_runtime/preconditions.py†L70-L111】
- Constitutional capability projection projects read-model capabilities from registrations and contracts but performs no selection, composition, persistence, semantic inference, or operator-testimony interpretation. 【F:seed_runtime/constitutional_view_selection.py†L172-L185】

## 5. Current examination handoff

`ExaminationProbeRequest` is the current strongest demand binder on the examination path. Its boundary notes say it binds selected examination meaning, contains no provider/tool/arguments, does not authorize/schedule/execute, and may remain operationally unrealizable. 【F:seed_runtime/examination_probe_request.py†L15-L22】 The handoff preserves `probe_request_id`, inquiry, artifact identity/hash, work contract, capability identity, input/output representations, and method constraint reference. 【F:seed_runtime/examination_probe_request.py†L30-L45】 The binder validates that selection, handoff, frontier, candidate work, and method applicability agree on inquiry, selected work, artifact, contract, capability, and method applicability before producing the request. 【F:seed_runtime/examination_probe_request.py†L52-L79】

This is demand plus constraints, not realization. The current handoff has no mechanism reference, invocation grammar reference, behavioral support reference, dependency report, authority report, or reachability conclusion.

## 6. Capability-demand analysis

Capability demand is the preserved claim that a bounded transformation is required. For the current examination path, it includes: bounded inquiry identity, artifact identity/version, work kind, capability identity, required input representation, requested output representation, requested outcome, method constraints, fidelity/attribution/claim-treatment constraints, provenance, unknowns, and read-only/mutation boundaries.

Closest current pure demand artifact: `ExaminationProbeRequest`, because it binds exact selected work meaning while explicitly excluding provider/tool name/operation arguments, authorization, scheduling, execution, and runtime Evidence/Fact creation. 【F:seed_runtime/examination_probe_request.py†L15-L22】【F:seed_runtime/examination_probe_request.py†L35-L45】

Current precedent: `ToolNeed` is a broader capability-gap request artifact with `capability`, `reason`, `desired_inputs`, and `desired_outputs`. 【F:seed_runtime/models.py†L112-L124】 It is useful precedent for demand but is less exact for examination because it lacks artifact identity/hash, selected work, work contract, method constraints, and representation provenance.

What Seed knows merely because a capability has been demanded: Seed knows that a requirement has been expressed and can preserve its name/reason/desired representations or, for examination, exact artifact-bound transformation meaning. It does not know that any mechanism exists, grammar is understood, behavior is validated, dependencies are available, authority is available, policy authorizes execution, or the transformation is reachable.

## 7. Mechanism-availability testimony

Potential sources and classification:

- `/bin/bash exists`: direct observation of executable availability if obtained by a presence probe. It establishes that an executable path appears available at the observed time/version/platform. It does not establish Bash-language competency, invocation grammar, quoting preservation, pipeline semantics, redirection semantics, behavioral correctness, or any Bash-backed higher-order transformation reachability.
- `ToolSpec.implementation`: implementation binding/static registered-operation testimony; it names a code binding but does not prove current availability or validated grammar. 【F:seed_runtime/models.py†L243-L260】
- `ToolSpec.status`: static registered-operation status, relevant to execution validation, not a behavioral observation by itself. 【F:seed_runtime/models.py†L243-L260】
- `ToolSpec.capabilities`: static label/contract metadata; inventory says these labels are not evidence that a capability is present, available, verified, authorized, or callable. 【F:seed_runtime/capability_inventory.py†L188-L195】
- `CapabilityCatalogEntry`/`CapabilityRecommendation`: static/attributed advisory metadata; recommendation can suggest a provider or handoff but does not execute. 【F:seed_runtime/capability_catalog.py†L13-L31】【F:seed_runtime/capability_catalog.py†L34-L44】
- `capability_verified` facts: verification conclusions admitted into State; inventory consumes them but does not create them. 【F:seed_runtime/capability_inventory.py†L29-L36】【F:seed_runtime/capability_inventory.py†L119-L127】
- `PreconditionReport`: dependency/authority-adjacent readiness evidence for legacy action plans; inspect-only and not execution. 【F:seed_runtime/preconditions.py†L1-L6】【F:seed_runtime/preconditions.py†L103-L111】

## 8. Invocation-grammar testimony

Current schema/contract records preserve declared invocation grammar pieces:

- `ToolSpec.input_schema`, `output_schema`, `policy_action`, `implementation`, `examples`, `status`, and capability labels. 【F:seed_runtime/models.py†L243-L260】
- `ExaminationWorkContract.accepted_input_representation`, `produced_output_representation`, `convention`, `availability`, and applicable member ids. 【F:seed_runtime/candidate_examination_work.py†L55-L58】
- `ExaminationProbeRequest.required_input_representation`, `requested_output_representation`, `contract_convention`, and method constraints. 【F:seed_runtime/examination_probe_request.py†L35-L45】

Declared invocation grammar is a claim or contract. Recovered invocation grammar is derived from external material, structural projection, examples, and candidate interpretations. Validated invocation grammar requires behavioral observations and comparison against expected behavior. A static schema cannot establish competency: it can constrain an invocation and provide a declared representation shape, but it cannot prove that Seed can construct valid inputs, preserve quoting, interpret outputs, or predict errors. An internal producer can expose an invocation grammar without being called a tool: constitutional read-model builders are deterministic producers consumed by projection, and projectors do not need executable-centric naming. 【F:seed_runtime/constitutional_view_selection.py†L172-L185】 An executable can have several possible invocation grammars, such as `bash -c`, script-file execution, interactive stdin, restricted POSIX fragments, or validated `echo`-only subsets.

## 9. Behavioral-evidence analysis

Current owners for behavior-like observations are fragmented. Execution/policy paths know stdout/stderr/exit status in some operational areas, but within this scoped road there is no implementation-backed owner that attaches exact request representation, exact mechanism/artifact version, stdout, stderr, exit status, produced artifacts, expected-result comparison, contradiction, and Unknowns to a capability demand and invocation grammar.

What changes after the Bash dungeon is crawled is not mechanism possession. The shell boundary, `/bin/bash`, and machine remain unchanged. New evidence is produced: attributed external testimony, structural grammar projections, candidate interpretations, bounded probes, exact stdout/stderr/status observations, comparisons to expected behavior, validated/contradicted grammar fragments, and limitations/Unknowns. Those new durable evidence records allow different realization testimony and therefore different bounded capability-reachability projection.

## 10. Operational-realization testimony

Smallest stable relationship: one exact demand may be realizable by one possible mechanism under one invocation grammar with evidence and constraints. It should include demand reference, mechanism reference, invocation-contract/reference, accepted/produced representations, grammar-support evidence, behavioral-support evidence, availability, dependency requirements, authority requirements, methodological compatibility, provenance, unknowns, and conflicts.

Realization testimony may exist even when unavailable, partially recovered, unverified, authority-blocked, representation-incompatible, or one of several candidates. It must not imply selection. Current artifacts contribute fragments: `CandidateExaminationWorkRecord` composes representation/contract compatibility but not mechanism invocation or behavior; `SingleCapabilityStateProjection` correlates requested/catalog/registered/candidate/verification fragments for one string but says no operation/provider selection and no execution/authorization; `ToolNeedService.resolve_capability` returns read-only catalog/registry metadata and explicitly does not execute, authorize, create pending actions, or mutate registry/catalog state. 【F:seed_runtime/candidate_examination_work.py†L60-L74】【F:seed_runtime/single_capability_state_projection.py†L19-L35】【F:seed_runtime/tool_needs.py†L67-L83】

## 11. Capability-reachability analysis

Reachability conclusion requires the exact demand, artifact/representation availability, at least one realization candidate, invocation grammar evidence, behavioral validation or an explicit validated-evidence exception, mechanism availability, dependencies, authority reachability, methodological constraints, and conflict handling. Current vocabulary includes verified/unverified/stale/provider_reported/unknown for inventory, and compatible/capability_unavailable/contract_unknown/representation_unknown for candidate examination work, but there is no final artifact that says the requested bounded transformation is reachable/partially reachable/unreachable/Unknown/conflict.

Policy authorization should not be inside mechanical reachability. Current artifacts separate execution/authorization from demand and projections: `ExaminationProbeRequest` does not authorize/schedule/execute, and `SingleCapabilityStateProjection` says no execution or authorization. 【F:seed_runtime/examination_probe_request.py†L15-L22】【F:seed_runtime/single_capability_state_projection.py†L30-L35】 A better distinction is operationally reachable versus constitutionally authorized for this invocation.

## 12. Competing topology analysis

### Topology A

`CapabilityDemand -> CapabilityReachabilityProjection -> CandidateOperationalRealizations` is unsupported. Repository evidence makes inventory/projection owners consume existing facts, tool specs, needs, catalog, and candidate/verification artifacts; it does not show final reachability can be projected before realization evidence. 【F:seed_runtime/single_capability_state_projection.py†L66-L161】

### Topology B

`CapabilityDemand -> OperationalRealizationTestimony -> CandidateOperationalRealizationSet -> CapabilityReachabilityProjection` is strongly supported for final reachability. Existing candidate examination work already composes candidate records before a request/handoff is bound, and single-capability projection correlates owner-produced artifacts rather than preceding them. 【F:seed_runtime/candidate_examination_work.py†L76-L110】【F:seed_runtime/single_capability_state_projection.py†L77-L161】

### Topology C

A preliminary evidence projection is also needed, but it is not final reachability. Candidate composition requires preliminary evidence such as corpus representation visibility, work contracts, availability observations, catalog metadata, registered operation labels, verification evidence, and constraints. The current implementation has such preliminary fragments (`CandidateExaminationWorkSet`, inventory source union, single-capability string correlation), but none owns final reachability. 【F:seed_runtime/candidate_examination_work.py†L76-L110】【F:seed_runtime/capability_inventory.py†L145-L185】

### Topology D

No direct evidence warrants merging candidate set and reachability into one responsibility. Current boundary notes repeatedly separate compatibility/candidate metadata from capability sufficiency, verification, selection, and authorization. 【F:seed_runtime/candidate_examination_work.py†L60-L68】【F:seed_runtime/single_capability_state_projection.py†L19-L35】

Selected topology: C. A preliminary evidence projection constrains realization composition, followed by a final capability-reachability projection.

## 13. Bash before/during/after trace

### Before crawl

Known mechanism evidence: shell process boundary and `/bin/bash` executable availability if directly observed. Known demands Seed could bind: observe artifacts, start one bounded local process, invoke `/bin/bash` opaquely, capture stdout/stderr/exit status, perform executable-presence probes. Invocation grammar: unknown except opaque process invocation. Behavioral evidence: only presence/probe execution observations if performed. Candidate realizations supportable: presence probes and opaque bounded local process execution. Capability projections supportable: executable-presence observation reachable; Bash-language transformations Unknown. Unknowns: interpreting Bash programs, constructing Bash programs, validating syntax, preserving quoting, composing pipelines, redirection, exit behavior prediction, bounded scripts, and Bash as higher-order realization.

### During crawl

Material examined: attributed Bash dungeon artifacts containing examples, exercises, expected outputs, and explanations. Grammar candidates projected: fragments such as simple command invocation and `echo` literal-output behavior. Probes constructed: bounded Bash invocations with exact input. Observations produced: stdout/stderr/status and produced artifacts. Comparisons: observed behavior versus expected examples. Evidence strengthened: grammar fragments whose observations match expected behavior. Evidence weakened/contradicted: candidates whose outputs/status/diagnostics disagree. Unknown remains for unprobed grammar regions.

### After crawl

Newly supported grammar competencies: only validated fragments. Newly supported realization testimony: `/bin/bash` plus validated invocation fragments can realize bounded literal-output and other probed transformations. Newly reachable bounded transformations: recognize validated fragments, construct expressions within validated fragments, invoke Bash with understood input, interpret expected outputs/diagnostics, compose only validated process grammar, construct bounded scripts within validated fragments, and use recovered Bash competency to examine further mechanisms. Still unsupported: unvalidated pipelines, redirection, command substitution, general scripting, version-specific behavior not covered by probes, and any authority-blocked execution. Authority constraints and platform/version bounds remain separate.

What changed: evidence and State changed, not executable possession. The same mechanism, same executable, and same authority now sit under different external testimony, recovered grammar, behavioral observations, and realization testimony; therefore a different bounded reachability projection is warranted.

## 14. Exact State change

The crawl adds durable evidence: external artifacts or references, structural grammar projections, candidate interpretations, behavioral probe records, observed stdout/stderr/status, comparison results, validation/contradiction facts, known limitations, and Unknowns. Derived projections should be recomputed when `/bin/bash` version changes, the dungeon changes, authority changes, dependency availability changes, or a behavioral probe contradicts earlier evidence.

## 15. Bounded Bash competency analysis

Bash competency is many bounded capability projections, not one global flag. Seed may project `simple literal-output Bash invocation reachable` after validating a simple `echo` fragment while preserving pipelines, redirection, command substitution, and general Bash scripting as Unknown. This follows the inventory precedent that one capability string state is not a global capability identity and the single-capability projection is only normalized-string correlation. 【F:seed_runtime/single_capability_state_projection.py†L19-L35】【F:seed_runtime/single_capability_state_projection.py†L187-L201】

## 16. Internal-producer trace

Existing deterministic internal producer: constitutional capability projection/read-model builders. Mechanism reference: registered source/view builder plus read-model contract/registration. Invocation contract: function-level builder contract and capability keys from source. Behavioral evidence: deterministic tests and implementation constraints; the projection helper says it consumes existing contracts, registrations, and immutable builders, and performs no selection/composition/persistence/semantic inference/operator-testimony interpretation. 【F:seed_runtime/constitutional_view_selection.py†L172-L185】

Compared to `/bin/bash`: `/bin/bash` mechanism reference is an executable path plus version/platform observation; invocation contract may be `bash -c`, script file, or stdin grammar; behavioral evidence is process observation. Internal producers need implementation registration or importable binding where repository architecture requires it, but they do not require the word `tool`. Reachability is projected differently because internal producers may have direct deterministic implementation evidence, while `/bin/bash` requires executable availability plus recovered/validated shell grammar. Neither case constitutionally requires the word `tool`.

## 17. No-mechanism trace

For a bounded demanded transformation with no mechanism evidence: `CapabilityDemand -> no known realization testimony -> no known realization / Unknown`, not proved impossible. Current candidate examination work can emit empty candidate sets or unknown observations without proving absence, and single-capability projection states empty candidate evidence is not capability absence. 【F:seed_runtime/candidate_examination_work.py†L70-L74】【F:seed_runtime/single_capability_state_projection.py†L197-L199】

## 18. Partial-grammar trace

With `/bin/bash` and only one recovered `echo` fragment, Seed may project reachability for simple literal-output Bash invocation while preserving pipelines, redirection, command substitution, functions, traps, globbing, arithmetic, and general scripting as Unknown. This is bounded and compositional; it must not become a global Bash capability flag.

## 19. Authority trace

If grammar and behavior are understood but required authority is unavailable, the lawful result is mechanically realizable but authority-blocked, unless current legacy architecture compresses it in a precondition report. `PreconditionReport` separates `plan_ready`, `authorization_required`, and `proposal_authorized`, showing authority is a distinct readiness dimension. 【F:seed_runtime/preconditions.py†L33-L43】【F:seed_runtime/preconditions.py†L86-L111】 `ExaminationProbeRequest` and single-capability projection also exclude authorization/execution. 【F:seed_runtime/examination_probe_request.py†L20-L22】【F:seed_runtime/single_capability_state_projection.py†L30-L35】

## 20. Capability-inventory analysis

Current capability inventory represents a verification belief for one capability string. It consumes registered operation labels, requested capabilities, and admitted `capability_verified` fact subjects. 【F:seed_runtime/capability_inventory.py†L119-L127】【F:seed_runtime/capability_inventory.py†L145-L185】 It legitimately represents verification status/freshness over a capability label, not demand, exact representation compatibility, mechanism availability, invocation grammar validation, behavioral support for the current demand, dependency availability, authority reachability, policy authorization, or final bounded reachability.

Can `CapabilityInventoryEntry` lawfully say a bounded transformation is reachable? No. It lacks an exact demand binding, artifact identity/version, input/output representation binding, mechanism reference, invocation grammar evidence, behavioral observations, dependency/authority evidence, methodological compatibility, and policy separation.

## 21. Single-capability-projection analysis

`SingleCapabilityStateProjection` is advisory/preliminary evidence composition and compatibility summary by normalized string, not final reachability. It can consume a capability string, not an exact `ExaminationProbeRequest`, and would lose artifact identity, input/output representations, method constraints, exact demand identity, and provenance if used as the sole owner. Its boundary notes directly say demand only, metadata only, advisory unselected recommendations, contract associations only, candidate evidence not availability, no provider/operation selection, no verification, and no execution/authorization. 【F:seed_runtime/single_capability_state_projection.py†L19-L35】

## 22. Realization-testimony sources

- Capability catalog entries: capability metadata, provider/handoff suggestion, provenance if present; no availability, behavior, selection, or authorization. 【F:seed_runtime/capability_catalog.py†L34-L44】
- Provider recommendations: attributed/advisory provider testimony; no reachability alone. 【F:seed_runtime/capability_catalog.py†L13-L24】
- Registered implementation records/ToolSpec: mechanism binding, declared schemas, status, examples, capability labels; no validated grammar or behavioral proof alone. 【F:seed_runtime/models.py†L243-L260】
- Implementation bindings: static binding testimony; availability unknown without import/executable observation.
- Operation schemas: declared invocation grammar; not behavioral validation.
- Internal producer identities: deterministic mechanism testimony with repository implementation evidence.
- State facts: verification/admission evidence if `capability_verified`; not realization for an exact demand without binding. 【F:seed_runtime/capability_inventory.py†L203-L209】
- Precondition reports: dependency/authority readiness evidence for legacy plans; not final reachability alone. 【F:seed_runtime/preconditions.py†L70-L111】

## 23. Candidate-set-versus-reachability analysis

The system needs both candidate-realization composition and reachability projection. Candidate set owns what realization testimony exists and how each candidate stands. Reachability projection owns the warranted conclusion about the requested transformation. Zero candidates means no known realization/Unknown unless evidence proves impossibility. One compatible but authority-blocked candidate means mechanically reachable or partially reachable but not authorized. Multiple candidates strengthen or diversify reachability but do not require selection. Conflicting realization evidence should produce conflict/partial/Unknown, not silent reachability. Selection is not required to establish reachability; selection occurs later when deciding which reachable realization to invoke.

## 24. Terminology reconciliation

| Current term | Actual responsibility in this topology |
| --- | --- |
| capability | Currently overloaded label/verification subject; should be bounded projected reachability in this road. |
| tool need | Demand precedent: requested capability gap with reason and desired I/O, not reachability. |
| capability catalog | Static capability metadata and provider/handoff recommendation testimony. |
| capability inventory | Verification/freshness presentation over capability labels; not final bounded reachability. |
| provider recommendation | Advisory attributed realization source; not selected and not reachable by itself. |
| tool spec | Registered operation contract/schema/implementation testimony; not validated invocation grammar. |
| registered operation | Mechanism/contract association and policy/action metadata; not behavior or reachability alone. |
| implementation | Binding testimony for a producer/mechanism; availability and behavior still need evidence. |
| operation schema | Declared invocation grammar; not recovered/validated grammar. |
| precondition | Dependency/authority/readiness evidence for a possible plan. |
| policy authorization | Invocation authorization decision; separate from mechanical reachability. |

## 25. Ownership matrix

| Responsibility | Current producer | Current artifact | Current consumer | Current status | Required evidence | Missing owner or handoff |
| --- | --- | --- | --- | --- | --- | --- |
| bounded transformation demand | examination selection binder / ToolNeedService precedent | `ExaminationProbeRequest`, `ToolNeed` | handoff/projection consumers | partial/established for examination demand | exact artifact, reps, method, reason, provenance | demand-to-realization binding |
| mechanism availability testimony | registry, State facts, direct probes | `ToolSpec`, facts, executable observations | inventory/projections | partial/testimony source | observed mechanism/version/path/service | mechanism availability evidence artifact |
| invocation-grammar testimony | schemas/contracts/external testimony | `ToolSpec` schemas, `ExaminationWorkContract` | candidate/projection consumers | testimony source | accepted input, output, env/cwd/stdin, examples | declared/recovered/validated split |
| recovered grammar projection | external material/candidate grammar owners | candidate external grammar/structural projections | examination consumers | partial | source material, structural projection, candidates | connection to realization testimony |
| behavioral probe observation | execution/probe records | fragmented stdout/stderr/status records | not current road | absent/partial | exact request, mechanism version, stdout, stderr, status | behavioral evidence owner for capability road |
| grammar validation/comparison | expected-vs-observed comparison | no scoped owner | none | absent | expected behavior, observation, contradiction | validation/comparison owner |
| realization testimony | catalog/registry/candidate fragments | no single artifact | manual reasoning | compressed/absent | demand+mechanism+grammar+behavior+deps+authority | OperationalRealizationTestimony |
| realization candidate composition | candidate examination work for work contracts only | `CandidateExaminationWorkSet` | frontier/request | partial | candidate standing per exact demand | CandidateOperationalRealizationSet |
| capability verification | State facts/inventory | `CapabilityInventoryEntry` | integrity/projection views | established for verification labels | `capability_verified` support/freshness | not final reachability |
| capability reachability projection | none closest: single-capability projection | none / `SingleCapabilityStateProjection` residue | manual | absent/compressed | exact demand + candidate set + evidence | CapabilityReachabilityProjection |
| authority reachability | precondition/permission owners | `PreconditionReport`, authority reports | plan/report consumers | partial | approvals/authority class/scope | handoff into realization/reachability |
| policy authorization | execution policy | policy decision | executor | established elsewhere | request, action, risk, approval | separate from reachability |
| realization selection | examination selection/operation selection elsewhere | selected work/pending action | executor/handoff | separate | reachable candidates + policy | out of scope after projection |
| invocation request | probe request/executor input | `ExaminationProbeRequest` / tool args | handoff/execution | partial | selected realization grammar + args | realization-to-invocation binder |

## 26. Strongest supporting evidence

- `ExaminationProbeRequest` explicitly binds selected meaning while excluding provider/tool/operation args, authorization, scheduling, execution, and runtime Evidence/Fact. 【F:seed_runtime/examination_probe_request.py†L15-L22】
- Registered operation labels are explicitly not evidence that capability is present, available, verified, authorized, or callable. 【F:seed_runtime/capability_inventory.py†L188-L195】
- `SingleCapabilityStateProjection` explicitly says requested state proves demand only, catalog metadata only, provider recommendations advisory, registered operations contract associations only, candidate evidence not availability, and no selection/execution/authorization. 【F:seed_runtime/single_capability_state_projection.py†L19-L35】
- `ToolNeedService.resolve_capability` returns read-only metadata and does not execute, authorize, create pending actions, or mutate registry/catalog state. 【F:seed_runtime/tool_needs.py†L75-L83】
- Candidate examination work distinguishes compatibility, unknown representation, unavailable capability, and unknown contract, and says compatibility does not establish capability sufficiency. 【F:seed_runtime/candidate_examination_work.py†L60-L68】【F:seed_runtime/candidate_examination_work.py†L89-L107】

## 27. Strongest counterevidence

- `CapabilityInventoryEntry.state` has values such as verified/unverified/stale/provider_reported/unknown, which could be mistaken for reachability. But its docstring and sources restrict it to verification belief over a capability string. 【F:seed_runtime/capability_inventory.py†L98-L127】
- `SingleCapabilityStateProjection` already composes demand, catalog, registered operations, candidate evidence, verification evidence, freshness, and unknowns, so it is closest to an existing reachability-like owner. But its boundary notes reject global identity, availability, selection, execution, authorization, and final verification ownership. 【F:seed_runtime/single_capability_state_projection.py†L19-L35】
- `ToolSpec.input_schema`/`output_schema` and examples could be treated as invocation grammar. But schema is declared contract testimony only and current inventory says registered contract labels are not callable/verified/available evidence. 【F:seed_runtime/models.py†L243-L260】【F:seed_runtime/capability_inventory.py†L188-L195】
- Candidate examination work composes candidates before final reachability and may suggest reachability/candidate composition could merge. But it preserves compatibility observations and boundary notes saying candidate work is not selected, eligible, authorized, scheduled, executed, and compatibility does not establish capability sufficiency. 【F:seed_runtime/candidate_examination_work.py†L60-L74】

## 28. Supported conclusions

1. Capability demand establishes a requirement and no reachability conclusion.
2. `/bin/bash exists` establishes executable availability only.
3. Invocation grammar must be declared, recovered, and validated as distinct evidence states.
4. Behavioral evidence is required for warranted reachability where behavior matters; declared schemas cannot fully substitute.
5. Realization testimony is the missing bridge from exact demand to possible mechanism under grammar/evidence/constraints.
6. Reachability follows candidate realization composition, with preliminary evidence needed to constrain candidates.
7. Candidate realization and reachability are distinct owners.
8. Selection occurs after reachability, not before.
9. Bash competency is bounded and compositional, not one global capability flag.
10. Internal producers and executables can participate in the same topology without using the word `tool`.

## 29. Unsupported conclusions

Unsupported by scoped repository evidence:

- Capability inventory already owns final bounded reachability.
- Single-capability projection already owns final bounded reachability for an exact `ExaminationProbeRequest`.
- Mechanism registration or declared schemas are sufficient for reachability.
- Provider recommendation establishes reachability.
- Reachability must precede realization discovery.
- Candidate set and reachability must be one artifact.
- Selection is required before reachability can be known.
- Authority should be hidden inside mechanical reachability.
- Bash should be one global competency state.
- Internal producers need a separate executable-centric constitutional road.

## 30. Primary topology classification

C. A preliminary evidence projection constrains realization composition, followed by a final capability-reachability projection.

## 31. Capability classification

3. Capability is projected reachability of a bounded transformation.

## 32. Bash-change classification

III. Crawling the dungeon changes evidence, recovered grammar, realization testimony, and therefore bounded capability projections.

## 33. First-missing-boundary classification

γ. Realization-testimony composition is first.

## 34. Exact next bounded boundary

Responsibility to recover: realization-testimony composition for one exact `OperationalRealizationHandoff`.

Current missing/compressed owner: no artifact composes exact demand with mechanism availability, invocation grammar testimony, behavioral evidence, dependencies, authority, methodological compatibility, provenance, unknowns, and conflicts.

Producer: a future read-only operational-realization testimony composer.

Input artifacts: `OperationalRealizationHandoff`, mechanism availability testimony, invocation-contract/grammar testimony, behavioral evidence records, representation constraints, dependency/precondition evidence, authority evidence, catalog/registry/internal-producer testimony, and current State facts.

Output artifact: one `OperationalRealizationTestimony` or candidate set record for the exact demanded transformation.

Immediate consumer: future `CapabilityReachabilityProjection` owner.

Exact bounded question: for this exact examination handoff, what evidence-backed manners of realization are supportable and how does each candidate stand?

Manual responsibility eliminated: manually deciding whether catalog/registry/schema/provider/inventory fragments amount to a candidate realization.

Compatibility treatment: preserve legacy `ToolNeed`, `ToolSpec`, catalog, inventory, and single-capability projection as testimony inputs, not canonical final reachability.

Explicit exclusions: no source/test/catalog/registry/policy/execution changes; no selection; no authorization; no execution; no result admission; no broad tool-district renaming.

## 35. Implementation-warrant decision

One bounded implementation slice is warranted.

## 36. Files changed

- Added `capability_demand_realization_reachability_topology_audit_001.md` only.

## 37. Probes executed

- `pwd && find .. -name AGENTS.md -print && git status --short`
- `cat AGENTS.md && git status --short`
- `rg -n "ExaminationProbeRequest|OperationalRealizationHandoff|capability_identity|required_input_representation|requested_output_representation" seed_runtime tests`
- `rg -n "CapabilityInventory|CapabilityInventoryEntry|SingleCapabilityStateProjection|capability_verified|reachable|unreachable|stale|unverified" seed_runtime tests`
- `rg -n "ToolNeed|CapabilityCatalog|CapabilityRecommendation|RankedRecommendation|capabilities" seed_runtime tests`
- `sed -n '1,220p' seed_runtime/examination_probe_request.py` and related focused file inspections
- `nl -ba seed_runtime/models.py | sed -n '100,280p'` and related focused line-number inspections
- `rg -n "input_schema|output_schema|implementation|precondition|dependency|authority|availability|status" seed_runtime tests | head -n 200`
- `rg -n "structural projection|surface feature|grammar|comparison|expected output|stdout|stderr|exit status" seed_runtime tests campaigns | head -n 200`
- `pytest -q tests/test_examination_probe_request.py tests/test_candidate_examination_work.py tests/test_capability_inventory.py tests/test_single_capability_state_projection.py tests/test_capability_catalog.py tests/test_tool_needs.py tests/test_registry.py tests/test_preconditions.py tests/test_constitutional_capability_projection.py`

Baseline test result: 75 passed, 2 failed. The two failures are current baseline failures in `tests/test_capability_catalog.py`: runtime returned `unsupported` instead of expected `tool_need` for recommendation responses. No fixes were made.

## 38. Confidence statement

Confidence is high for the bounded topology classification because the inspected files repeatedly separate demand, metadata, registered operation contracts, verification, compatibility, selection, execution, and authorization. Confidence is medium for the exact next implementation slice because this audit intentionally did not inspect broader execution/result-admission districts and did not design schemas.

## Required question answers

1. Capability demand is a preserved bounded transformation requirement.
2. `ExaminationProbeRequest` preserves it for examination, with artifact identity, representation, method, provenance, and constraints.
3. Mechanism existence establishes only apparent availability of a mechanism at an observation boundary.
4. `/bin/bash exists` establishes executable availability, not Bash-language competency or transformation reachability.
5. Before dungeon examination, Bash grammar, quoting, pipelines, redirection, exit behavior, bounded scripts, and higher-order Bash realization remain Unknown.
6. During the crawl, external testimony, structural grammar projections, candidate interpretations, bounded probe observations, stdout/stderr/status, comparisons, validations, contradictions, and Unknowns are produced.
7. After the crawl, State preserves new evidence and derived projections; the executable is unchanged.
8. Newly reachable transformations are only bounded validated Bash fragments and transformations composed from them.
9. Bash competency is many bounded capability projections.
10. Seed can understand Bash grammar from testimony without `/bin/bash` being currently available, but cannot behaviorally validate current executable behavior without execution availability.
11. Seed can invoke `/bin/bash` opaquely without understanding Bash grammar.
12. Mechanism testimony becomes realization testimony when bound to one exact demand with invocation grammar, representation, behavioral, availability, dependency, authority, provenance, Unknown, and conflict evidence.
13. Realization testimony becomes reachability when at least one candidate warrants a conclusion for the exact demand under current State and constraints.
14. Behavioral evidence is required for warranted reachability where behavior/grammar correctness matters.
15. Declared schemas cannot generally substitute for behavioral evidence.
16. Registration cannot establish reachability.
17. Provider recommendation cannot establish reachability.
18. One compatible realization can establish operational reachability if grammar, behavior, availability, dependencies, authority reachability, and constraints are sufficient.
19. If that realization lacks authority, it is mechanically realizable but authority-blocked / partially reachable, not authorized.
20. Several realizations form a candidate set; selection remains later.
21. No known realization means no known realization / Unknown, not proved impossible.
22. Known mechanism with Unknown grammar remains Unknown or partial for grammar-free probes only.
23. Known grammar with contradicted behavior weakens or blocks reachability for that bounded fragment.
24. Partial grammar validation supports only partial bounded reachability.
25. Final reachability is projected after candidate-realization composition.
26. Preliminary evidence projection is needed before candidate composition.
27. Candidate-realization composition and reachability projection are distinct owners.
28. Selection occurs after reachability.
29. Closest existing owner is `SingleCapabilityStateProjection`.
30. It is insufficient because it correlates one normalized string and excludes global identity, availability, selection, execution, authorization, and exact demand representation binding.
31. Current testimony inputs include catalog entries, provider recommendations, ToolSpecs, operation schemas, implementation bindings, State facts, candidate work records, and precondition reports.
32. First missing owner on the examination critical path is realization-testimony composition.
33. Smallest bounded implementation slice warranted is one read-only composer from `OperationalRealizationHandoff` plus testimony/evidence inputs to an operational-realization testimony artifact.
