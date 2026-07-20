# Executive Summary

Response caveats are **partially present** in Seed. Caveat-producing conditions already exist across integrity, explainability, capability, confidence, state, context, and CLI surfaces. The repository already communicates unsupported facts, contradictions, fact conflicts, stale facts, graph issues, confidence limits, capability verification status, missing evidence, no-current-belief status, and response/runtime limitations.

However, caveat communication is distributed and fragmented. Projection Integrity Summary is the strongest partial unifier because it aggregates several caveat-producing integrity signals and includes explicit summary caveats. It does not make caveats a general response contract, does not classify all caveat kinds, and does not answer “what caveats apply to this answer/current fact/capability/response?” consistently across surfaces.

The characterization finds behavior before vocabulary:

- Caveat sources exist.
- Caveat signals exist.
- Caveat outputs exist.
- Caveat communication exists.
- Caveat ownership is distributed.
- Caveat categories are mostly implicit or partial.
- A new caveat engine, response engine, runtime integration, ToolExecutor integration, read model, route, adapter, schema class, inventory, or projection mutation is not justified by this audit.

Recommended outcome: **B. Caveats partially present**. A documentation-only Response Caveat Vocabulary, Response Caveat Reconciliation, or Caveat Communication Characterization may be justified if operators need a shared language for already-existing caveat signals. Implementation work is not justified unless a future audit identifies a concrete unanswered operator question that cannot be answered by composing existing surfaces.

# Purpose

This document characterizes caveats in Seed's Response concern. It asks what caveats are, where caveat information already exists, how caveat information is communicated, who owns caveat information, how fragmented caveat communication is, which caveat-related operator questions are already answerable, and which questions remain hard to answer consistently.

This is an audit only. It documents existing behavior and architecture boundaries without implementing caveats, inventories, summaries, navigation, response engines, read models, routes, adapters, schema classes, runtime behavior, provider behavior, projection mutation, or event appends.

# Scope

In scope:

- existing caveat-producing conditions in projected State and read-only views;
- existing caveat signals such as unsupported, contradicted, conflicted, stale, expired, unverified, unknown, graph-invalid, missing evidence, confidence-limited, ambiguous, and no-current-belief;
- existing surfaces that communicate caveat information;
- existing ownership boundaries among Integrity, Explainability, Capability Inventory, State Views, Context/Selection, Response surfaces, and CLI presentation;
- fragmentation and composition opportunities.

Out of scope:

- implementing caveat inventories, summaries, navigation, read models, routes, adapters, or schema classes;
- modifying `Runtime`, `ToolExecutor`, `EventLedger`, `ProjectionStore`, providers, model clients, projections, or event append paths;
- adding a `CaveatEngine`, `ResponseEngine`, `IntegrityEngine`, `ExplainabilityEngine`, `ReasoningEngine`, `ContextEngine`, planner, workflow engine, universal formatter, or parallel caveat/truth/response system;
- mutating projections or appending events;
- changing tests except if documentation invariant tests require it.

# Files Inspected

Required files inspected:

- `docs/response_characterization.md`
- `docs/response_vocabulary.md`
- `docs/response_reconciliation.md`
- `docs/explainability_reconciliation.md`
- `docs/explanation_contract_vocabulary.md`
- `docs/selection_rationale_reconciliation.md`
- `docs/projection_integrity_summary_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/knowledge_classification_vocabulary.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `seed_runtime/explanations.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/contradictions.py`
- `seed_runtime/confidence.py`
- `seed_runtime/state_views.py`
- `seed_runtime/context_views.py`
- `scripts/seed_local.py`

Additional caveat-, confidence-, integrity-, explanation-, capability-, issue-, summary-, state-, response-, and CLI-related files inspected:

- `docs/context_composition_reconciliation.md`
- `docs/context_composition_vocabulary.md`
- `docs/selection_rationale_characterization.md`
- `docs/selection_rationale_vocabulary.md`
- `docs/selection_rationale_summary_characterization.md`
- `docs/why_not_explanation_characterization.md`
- `docs/explainability_audit.md`
- `docs/explainability_inventory_audit.md`
- `docs/explainability_contract_characterization.md`
- `docs/capability_verification_audit.md`
- `docs/capability_verification_fit_audit.md`
- `docs/capability_verification_reconciliation.md`
- `docs/capability_verification_vocabulary.md`
- `docs/capability_ownership_matrix.md`
- `docs/contradiction_handling_audit.md`
- `docs/knowledge_maintenance_reconciliation.md`
- `docs/knowledge_acquisition_and_selection.md`
- `docs/state.md`
- `seed_runtime/evidence_graph.py`
- `seed_runtime/facts.py`
- `seed_runtime/integrity_summary.py`
- `seed_runtime/state.py`
- `seed_runtime/runtime.py`
- `seed_runtime/models.py`
- `seed_runtime/decisions.py`

Inspection commands used:

- `rg --files docs seed_runtime scripts | rg '(response|explain|explanation|selection|projection_integrity|knowledge_|confidence|integrity|capability|issue|summary|state|cli|caveat|contradiction|context)'`
- `rg -n "unsupported|contradict|conflict|stale|expiry|graph|confidence|verification|unverified|missing|unknown|limitation|caveat|refresh|issue|why" docs seed_runtime scripts/seed_local.py`
- targeted `sed -n` reads of the files listed above.

# What Is A Caveat

A **caveat** in Seed is an existing communicated limitation, qualification, warning, uncertainty marker, or non-guarantee attached to projected knowledge, selected knowledge, response content, capability status, evidence, integrity signals, or presentation.

A caveat is not a new knowledge object by itself. It is a response-relevant communication of conditions under which existing knowledge should not be overinterpreted as truth, correctness, freshness, support, verification, availability, completeness, or actionability.

In Seed terms, caveats currently appear as:

| Candidate caveat form | Finding | Evidence from inspection |
| --- | --- | --- |
| Uncertainty | Present | Confidence aggregation exposes confidence, weak support, unsupported status, contradicted status, and reasons. |
| Limitations | Present | Response Vocabulary defines response as communicating selected projected knowledge and limitations, and Integrity Summary includes explicit caveats that counts are not truth/correctness judgments. |
| Unsupported status | Present | Evidence Summary counts unsupported facts; Confidence marks unsupported facts; CLI exposes `--unsupported-facts`. |
| Contradiction status | Present | `Contradiction` outputs expose conflicting fact IDs, values, severity, reasons, evidence, and supporting events. |
| Conflict status | Present | `FactConflict` records values, winning value, best fact ID, conflicting fact IDs, and reason. |
| Stale status | Present | Facts can expire; stale facts are excluded from current support and surfaced through stale fact outputs and refresh recommendations. |
| Expiry metadata | Present | `Fact` and `FactSupport` expose `expires_at`; capability support exposes expired state and expiry metadata. |
| Graph issues | Present | Graph validation issues expose severity, subject, relationship, object, expected/actual type information, reason, and source fact IDs. |
| Missing evidence | Present | Unsupported facts and confidence reasons communicate no linked supporting evidence. |
| Unverified capability status | Present | Capability Inventory reports `unverified` when no `capability_verified` fact is present. |
| Unknown capability status | Present | Capability Inventory has `unknown` status for values outside known verification vocabulary. |
| Provider-reported status | Present | Capability Inventory distinguishes `provider_reported` from evidence-backed verification. |
| Confidence limitations | Present | Confidence reasons communicate support counts, explicit confidence preservation, and contradiction penalties. |
| Rationale limitations | Partial | Selection rationale and why-not audits found selection/rationale information exists but is not uniformly summarized; Response Reconciliation found rationale communication fragmented. |
| Observation limitations | Partial | Observation/source type/confidence/observed-at metadata exists, but no general response caveat category consistently communicates observation limits across all surfaces. |
| Runtime limitations | Present as local wording | CLI and docs repeatedly state read-only commands do not execute runtime behavior, tools, providers, policy, or append events. Runtime response envelopes also represent refusals, invalid decisions, and unsupported outcomes. |

Therefore, a caveat should be characterized as a response-level communication of an existing limitation or integrity/selection/explanation/capability condition, not as a new engine-owned domain object.

# Existing Caveat Sources

The audit distinguishes caveat sources, caveat signals, and caveat outputs:

- A **caveat source** is the underlying projected condition or metadata from which a caveat can be derived.
- A **caveat signal** is a named status, count, field, reason, or flag that communicates the condition in structured form.
- A **caveat output** is a response or presentation surface that exposes the signal to an operator or consumer.

| Existing item | Source | Signal | Output | Finding |
| --- | --- | --- | --- | --- |
| Unsupported facts | Facts without linked evidence | `unsupported_fact_count`, `unsupported=True`, evidence count `0`, reason text | Evidence Summary, Confidence, Decision Context, CLI `--unsupported-facts`, Integrity Summary | Caveat source, signal, and output. |
| Missing evidence | Empty evidence links/support | unsupported counts, evidence count, confidence reasons | Evidence Graph, Fact Evidence View, Confidence, CLI | Caveat source and signal; output is distributed. |
| Contradictions | Multiple values for exclusive predicates with supporting facts/evidence | `Contradiction` severity, reason, values, fact IDs, supporting events | Contradiction outputs, Confidence, Decision Context issues, Integrity Summary | Caveat source, signal, and output. |
| Fact conflicts | Projected disagreement in State support selection | `FactConflict` values, winning value, best fact, conflicting facts, reason | State current/best/conflict outputs, Integrity Summary | Caveat source, signal, and output. |
| Stale facts | Expired facts | `expired`, `expires_at`, stale fact count | State stale facts, CLI `--stale-facts`, Integrity Summary | Caveat source, signal, and output. |
| Expiry metadata | `Fact.expires_at`, `FactSupport.expires_at`, capability support expiry | expiry fields, `expired` flag | Fact support, stale facts, capability inventory | Caveat source and signal. |
| Refresh recommendations | Stale fact plus deterministic capability mapping | `StaleFactRefreshRecommendation.reason`, `recommended_capability` | CLI `--stale-fact-refreshes`, Integrity Summary count | Caveat output and follow-up hint; not execution. |
| Graph issues | Relationship/type validation over projected State | `GraphValidationIssue` severity, reason, expected/actual type data | Issue Views, graph issue CLI, unhealthy output, Decision Context, Integrity Summary | Caveat source, signal, and output. |
| Confidence | Evidence support, explicit fact confidence, contradiction penalty | `confidence`, support count, weak/strong bucket, reasons | Confidence outputs, Decision Context, explanations, Integrity Summary indirectly | Caveat signal and output. |
| Verification status | `capability_verified` facts/support/evidence | `verified`, `unverified`, `stale`, `provider_reported`, `unknown` | Capability Inventory, CLI `--capability-status`, Integrity Summary counts | Caveat source, signal, and output. |
| Capability status | Tools, ToolNeeds, verification facts, provider recommendations | inventory state, ToolNeed status, recommendation reasons | Capability Inventory, Runtime `tool_need` response, CLI summaries | Caveat source and output; verification and recommendation are separate. |
| Missing observations | Absence of projected facts/observations for query | `no_current_belief`, unverified capability reason, empty view counts | Explanation, State Views, Capability Inventory | Caveat source and partial signal. |
| Ambiguity | Multiple supports with no selected best current belief | `Explanation.status="ambiguous"`, competing beliefs, conflict | Explanation outputs | Caveat signal and output. |
| No current belief | No support for a subject/predicate | `Explanation.status="no_current_belief"` | Explanation outputs | Caveat signal and output. |
| Rationale limits | Existing rationale spread over support, context, confidence, conflicts, explanations | reasons, budget traces, support metadata, competing facts | Selection, context, explanation, response docs | Partial caveat signal; no single caveat output. |
| Runtime/read-only limits | CLI/read model boundary statements | text that commands do not execute, append events, call providers, or mutate | CLI help and docs | Caveat output about operational scope, not projected truth. |

# Existing Caveat Surfaces

| Surface | Exposes caveats directly? | Exposes caveats indirectly? | Finding |
| --- | --- | --- | --- |
| Projection Integrity Summary | Yes | Yes | Direct counts for unsupported facts, conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability verification states; includes explicit caveats. |
| Integrity Navigation / Drilldown characterization | Yes | Yes | Characterizes drill-down paths from summary counts to source views; documentation-only, not runtime behavior. |
| Explanation outputs | Yes | Yes | Directly expose `current`, `ambiguous`, `no_current_belief`, competing beliefs, conflicts, support confidence, evidence IDs, source types, observation times, inferred confidence, confidence caps, and source facts. |
| Explanation Contract Vocabulary | Yes | Yes | Names explanation statuses and limitations; does not implement caveats. |
| Capability Inventory | Yes | Yes | Directly exposes `verified`, `unverified`, `stale`, `provider_reported`, `unknown`, evidence/support, age, reason, and expiry metadata. |
| State Views | Yes | Yes | Expose current facts, observations, requirements, capabilities, issues, summary counts, graph issue details, projection metadata, and last event IDs. |
| Issue Views | Yes | Yes | Graph issues are direct caveat outputs with severity and summary. |
| Contradiction outputs | Yes | Yes | Direct contradiction caveats with severity, reason, values, fact IDs, evidence, and events. |
| Confidence outputs | Yes | Yes | Direct confidence caveats with support count, unsupported/contradicted booleans, confidence value, and reasons. |
| Why / Why-Fact outputs | Yes | Yes | Explain support, evidence, conflict, ambiguity, and missing current belief for fact-level questions. |
| Why-Not characterization | Documentation only | Yes | Finds why-not partially represented but not first-class as a universal answer. |
| Decision Context View | Partial | Yes | Communicates selected facts with confidence, contradicted status, evidence count, issue summaries, and unsupported counts when included. It is selection/response-adjacent rather than a caveat contract. |
| Context packet / Context Composition | Partial | Yes | Budget traces and selected facts can imply caveats, but context composition is not a caveat communication surface by itself. |
| Runtime response envelopes | Partial | Yes | Answer/question/refusal/tool_need/tool_result/state patch/invalid responses communicate response state and some limitations; caveat communication is local and not cross-surface. |
| CLI output | Yes | Yes | Many CLI flags expose caveats directly; formatting is distributed and command-specific. |
| Capability resolution / recommendations | Partial | Yes | Recommendation reasons and missing capability/tool_need outputs can communicate limitations but do not verify capabilities. |
| Model/client/provider outputs | No general caveat surface | Partial | Provider/model boundaries may produce failures or invalid decisions, but they are not caveat owners. |

Surfaces that expose no general caveat contract: `Runtime` as a global owner, `ToolExecutor`, `EventLedger`, `ProjectionStore`, provider clients, and model clients. They may produce or transport responses, but inspection does not support assigning caveat generation or caveat unification to them.

# Existing Caveat Communication

Current caveat communication is field-, status-, reason-, count-, and command-specific.

Observed caveat terms and communication styles include:

| Communication | Existing location/type | Consistency finding |
| --- | --- | --- |
| `unsupported` | Evidence, Confidence, CLI, Integrity Summary | Fairly consistent for facts without evidence, but not a general response caveat category. |
| `contradicted` / `contradiction` | Contradictions, Confidence, Decision Context, Integrity Summary | Consistent as a conflict caveat, but contradiction and fact conflict remain distinct surfaces. |
| `conflict` / `conflicted` | State fact conflicts, Explanation conflict, docs vocabulary | Partially consistent; `FactConflict` and `Contradiction` have related but not identical semantics. |
| `stale` | Stale facts, capability inventory, integrity summary | Consistent at a high level, but stale facts and stale capabilities have different source semantics. |
| `expired` | Fact/FactSupport/capability support metadata | Consistent as temporal metadata; not always presented as user-facing caveat prose. |
| `unverified` | Capability Inventory, Integrity Summary | Consistent for no projected `capability_verified` fact, but should not be read as provider absence or execution failure. |
| `provider_reported` | Capability Inventory | Distinguishes provider report from verification; surface-specific. |
| `unknown` | Capability Inventory and graph/entity typing | Existing term has multiple local meanings; requires caution before global vocabulary. |
| `graph issue` / graph validation severity | State graph validation, Issue Views, CLI, Integrity Summary | Consistent within graph/integrity surfaces. |
| `low confidence` / weak support | Confidence summary and values | Confidence values exist, but cross-surface phrasing for “low confidence” is not centralized. |
| `missing evidence` | Evidence/Confidence reasons and Integrity Summary caveat | Present, but usually communicated as unsupported or no linked evidence rather than a universal phrase. |
| `no_current_belief` | Explanation | Consistent within explanations; not always surfaced elsewhere. |
| `ambiguous` | Explanation | Consistent within explanations; not a global caveat status. |
| “does not execute / append / mutate / verify / call providers” | CLI help and docs | Common operational caveat wording; not structured response metadata. |

Overall consistency: **partial**. Seed has coherent local vocabularies, especially for Integrity Summary, Confidence, Capability Inventory, and Explanation. It lacks a single caveat communication vocabulary that says how to combine multiple caveats, how to order them, when to present them as response content versus metadata, or how to render them consistently across CLI, explanation, integrity, capability, state, and runtime response surfaces.

# Existing Caveat Ownership

| Ownership area | Owns caveat generation? | Owns caveat communication? | Owns caveat presentation? | Finding |
| --- | --- | --- | --- | --- |
| Integrity | Yes for integrity conditions | Yes for integrity summaries/signals | Partial via summary output and CLI formatting | Integrity characterizes caveat-producing conditions such as unsupported, conflicted, contradicted, stale, graph issue, confidence, and verification state. |
| Explainability | No for underlying truth/integrity | Yes for explaining caveat conditions | Partial via explanation formatters | Explainability explains support, evidence, ambiguity, conflicts, and no-current-belief; it should not own caveat generation globally. |
| Capability Inventory | Yes for verification-state caveats derived from projected facts | Yes for capability status reasons/support/evidence | Partial via inventory/CLI | Owns capability verification caveat communication from projected facts, not provider execution or actual availability. |
| State / State Views | Yes for projected conflicts, stale facts, graph issues, current-state issues | Yes through views | Partial via CLI | Owns projected-state caveat source data and view-specific communication. |
| Confidence | Yes for confidence caveat signals | Yes for confidence records and summaries | Partial via CLI | Owns confidence aggregation and reasons, not truth. |
| Contradictions | Yes for conservative contradiction reports | Yes for contradiction objects/summaries | Partial via CLI | Owns contradiction caveat detection/reporting, not resolution. |
| Evidence Graph | Yes for support/missing-evidence signals | Yes for evidence views/summaries | Partial via CLI | Owns evidence-link communication and unsupported counts. |
| Context / Selection | No for original caveat production | Partial for selected caveat-producing signals | Partial via context views | Selection can include/exclude facts using caveat-producing signals and communicate some selected caveats indirectly. |
| Response surfaces | No for caveat generation | Yes for communication of selected caveats | Yes locally | Response communicates caveats generated elsewhere; it should not own projection truth, integrity, selection, or verification. |
| CLI | No for caveat generation | Yes for command-specific communication | Yes for terminal presentation | CLI owns presentation only. |
| Runtime | No global caveat owner | Partial through response envelope kinds/payloads | Partial | Runtime owns routing/envelopes, not caveat generation or universal caveat composition. |
| ToolExecutor | No | No | No | Tool execution results may be communicated, but ToolExecutor should not own caveat systems. |
| EventLedger / ProjectionStore | No | No | No | Storage/projection ownership does not imply caveat ownership. |

Ownership finding: caveat ownership is deliberately distributed by source semantics. Generation belongs to the component that already owns the underlying condition. Communication belongs to the surface that exposes that condition. Presentation belongs mostly to CLI or local response formatters. A global caveat owner is not supported.

# Existing Caveat Categories

| Category | Status | Existing support |
| --- | --- | --- |
| Integrity Caveat | Implemented / Partial | Integrity Summary aggregates unsupported, conflicts, contradictions, graph issues, stale facts, refresh recommendations, and capability counts with explicit caveats. It is not universal. |
| Evidence Caveat | Implemented / Partial | Evidence Graph, unsupported facts, confidence reasons, and why-fact outputs expose support gaps. No single “Evidence Caveat” category is canonical. |
| Capability Caveat | Implemented / Partial | Capability Inventory exposes verification states, reasons, evidence/support, stale status, unknown/provider-reported states. It does not verify or execute. |
| Temporal Caveat | Partial | Expiry, stale facts, `observed_at`, `latest_observed_at`, age, current-sample behavior, and refresh recommendations exist. Unified stale/as-of/replacement rationale is missing. |
| Confidence Caveat | Implemented / Partial | Confidence aggregation exposes confidence, weak/strong buckets, unsupported/contradicted status, and reasons. It is not consistently attached to all responses. |
| Selection Caveat | Partial / Implicit | Decision Context and context selection use confidence/support/contradiction signals; selection rationale information exists but is fragmented and summary implementation was not justified. |
| Observation Caveat | Partial / Implicit | Observations/facts expose source type, confidence, observed time, evidence IDs, and imported/provider/user distinction. No general observation caveat communication contract exists. |
| Response Caveat | Partial / Implicit | Response Vocabulary names limitations/caveats as response language; Response Reconciliation finds caveats fragmented. No dedicated Response Caveat Vocabulary exists yet. |
| Runtime Caveat | Partial / Local | CLI/help docs communicate read-only/no-execution/no-provider/no-event-append limits; runtime refusals/invalid decisions communicate local response limitations. No caveat category exists. |
| Graph Caveat | Implemented / Partial | Graph validation issues and issue views expose severity and reasons; not framed as a global caveat category. |
| Rationale Caveat | Partial / Implicit | Confidence reasons, recommendation reasons, explanation conflicts, support metadata, and selection-rationale docs exist, but no common rationale-limitation category exists. |
| Unknown/Absence Caveat | Partial | Explanation `no_current_belief`, capability `unknown`, graph unknown type warnings, and empty/missing views exist, but `unknown` has local meanings. |

# Existing Operator Questions Already Answerable

Seed can already answer many caveat-related questions through existing surfaces:

| Operator question | Already answerable? | Existing surface(s) |
| --- | --- | --- |
| Why is this unsupported? | Yes, for facts/evidence | Evidence Graph, Fact Evidence View, Confidence reasons, CLI `--unsupported-facts`, `--why-fact`. |
| Which facts lack evidence? | Yes | Evidence Summary, unsupported facts output, Confidence Summary, Integrity Summary. |
| Why is this contradicted? | Yes, for conservative contradictions | Contradiction output with values, fact IDs, severity, reason, evidence, and supporting events. |
| Which facts are contradicted? | Yes | Contradictions, Confidence, Decision Context, Integrity Summary. |
| Why is this conflicted? | Yes, for projected fact conflicts | `FactConflict` outputs include values, winning value/best fact, conflicting fact IDs, and reason. |
| Why is this stale? | Partially yes | Stale fact output and expiry metadata show expired facts and `expires_at`; refresh recommendations explain recommended capability. Unified stale rationale is missing. |
| Which facts are stale? | Yes | State stale facts, CLI `--stale-facts`, Integrity Summary. |
| What should refresh a stale fact? | Yes, deterministically | Stale fact refresh recommendations and CLI `--stale-fact-refreshes`. |
| Why is this capability unverified? | Yes, within projected verification facts | Capability Inventory says no `capability_verified` fact is present or maps verification values; it cannot prove external absence. |
| Why is this capability stale? | Yes, within capability inventory | Capability support exposes expired verification facts and reason. |
| Is this capability provider-reported rather than verified? | Yes | Capability Inventory state `provider_reported`. |
| Why is confidence limited? | Yes, locally | Confidence reasons show support counts, explicit confidence use, unsupported status, and contradiction penalties. |
| Is there no current belief? | Yes, in explanation queries | Explanation status `no_current_belief`. |
| Is the belief ambiguous? | Yes, in explanation queries | Explanation status `ambiguous`, competing beliefs, and conflict. |
| What graph/type issues exist? | Yes | Graph issues, Issue Views, `--graph-issues`, unhealthy output, Integrity Summary. |
| What integrity caveats exist at aggregate level? | Yes | Projection Integrity Summary counts and caveats. |
| What response/runtime command limits apply to this CLI command? | Partially yes | CLI help text and documentation indicate read-only, no execution, no event append, no provider calls for many commands. |

# Existing Operator Questions Not Easily Answerable

The following questions are not easily answerable consistently across existing surfaces. These are findings from inspection, not feature requests.

| Operator question | Finding |
| --- | --- |
| What caveats apply to this answer? | Not consistently answerable. Runtime answer responses do not include a general caveat composition rule that joins integrity, confidence, evidence, capability, and selection caveats. |
| What caveats apply to this response? | Not consistently answerable. Response surfaces communicate local caveats, but no shared response caveat contract or cross-surface caveat list exists. |
| What caveats apply to this current fact? | Partially answerable by joining fact support, confidence, evidence graph, contradictions, conflicts, stale status, and explanation. No single current-fact caveat output exists. |
| What caveats apply to this capability? | Partially answerable through Capability Inventory, ToolNeed, recommendations, and verification facts. Not consistently joined with graph, evidence, confidence, runtime availability, or response-level limitations. |
| What caveats apply to selected context? | Partially answerable through Decision Context View and confidence/contradiction fields. Budget/selection caveats and integrity caveats are not uniformly composed. |
| How should multiple caveats be communicated together? | Not answered. Integrity Summary aggregates counts but does not define ordering, severity, grouping, suppression, or cross-surface presentation. |
| Which caveat should be most prominent? | Not answered globally. Local severity exists for graph issues and contradictions; confidence thresholds exist; no shared caveat prominence policy exists. |
| Is `unknown` the same kind of caveat across surfaces? | No. Capability `unknown`, graph unknown types, no-current belief, and missing evidence are related but not equivalent. |
| Does an unverified capability imply unavailable? | Existing docs/code imply no. Capability Inventory cannot prove absence or runtime availability, but this limitation is not necessarily attached to every capability response. |
| Does stale imply false? | Existing Integrity Summary says no, but this caveat is not guaranteed on every stale-fact surface. |
| Does unsupported imply false? | Existing Integrity Summary says no, but unsupported outputs are surface-specific. |
| Why was a fresher fact selected over a stale/older fact? | Partially represented through support timestamps and stale filtering, but no replacement rationale object exists. |
| Why was a caveat not shown on a response? | Not answerable. No caveat selection/composition policy exists. |

# Relationship To Integrity

Finding: **validated** — Integrity characterizes many caveat-producing conditions.

Integrity owns or aggregates conditions that naturally become response caveats:

- unsupported facts and missing evidence;
- fact conflicts;
- contradictions;
- graph validation issues;
- stale facts and expiry;
- refresh recommendations;
- capability verification state counts;
- confidence-related support limits.

Projection Integrity Summary is the strongest existing caveat composition surface. It aggregates existing integrity signals and includes explicit caveats that integrity counts are projection-backed signals, not truth or correctness judgments; that unsupported, unverified, stale, contradicted, or missing evidence does not mean false; and that refresh recommendations do not execute refresh or verification.

Boundary: Integrity characterizes caveat-producing conditions. It does not create knowledge, decide truth, repair projections, refresh facts, verify capabilities, execute tools, mutate State, append events, own Runtime, or own response presentation globally.

# Relationship To Explainability

Finding: **validated** — Explainability may explain caveats; Response may communicate caveats.

Explainability already explains caveat-adjacent conditions:

- why a belief is current, ambiguous, or absent;
- which evidence and fact IDs support a belief;
- which source types and observation times apply;
- which competing beliefs exist;
- whether conflict information is attached;
- confidence caps and inferred/source fact chains.

Explainability should not become a caveat engine. It can explain caveat sources and signals owned by State, Evidence Graph, Confidence, Contradictions, Capability Inventory, or Integrity Summary. Response surfaces can then communicate those explanations as response content.

Boundary: Explainability owns explanation content and explanation vocabulary. It does not own truth selection, projection mutation, capability verification, runtime execution, or universal response presentation.

# Relationship To Selection

Finding: **validated with limits** — Selection may use caveat-producing signals and may communicate caveats indirectly.

Selection/context surfaces already consume or expose caveat-producing signals:

- Decision Context View selects facts from confidence items and can exclude unsupported facts by default;
- selected facts include confidence, contradicted status, and evidence count;
- context issues include contradictions and graph issues;
- context summaries include unsupported and contradicted counts;
- context composition and budget traces can communicate why content was included or omitted.

Boundary: Selection does not own caveat generation. It may use caveat-producing signals to select or shape context, but response caveat communication remains local and partially fragmented. Prior Selection Rationale work found selection rationale is partially unified and that summary implementation was not justified.

# Relationship To Response

Finding: caveats are already response content in several surfaces, partially response metadata in some surfaces, and response limitations in documentation/CLI wording.

- **Response content:** unsupported fact lists, contradiction reports, graph issue lists, capability verification entries, confidence reports, stale fact lists, refresh recommendations, explanation statuses, and integrity summaries are caveat-containing response content.
- **Response metadata:** projection version, last event ID, support counts, confidence values, evidence counts, severity, age, `observed_at`, `latest_observed_at`, `expires_at`, and source types often serve as caveat metadata.
- **Response limitations:** CLI/help/docs repeatedly communicate that read-only views do not execute runtime behavior, call providers, verify capabilities, refresh facts, mutate projections, or append events.

Response does not own the underlying caveat-producing conditions. Response communicates selected caveats and limitations produced by existing owners. Existing Response Vocabulary already names limitations, caveats, uncertainty, metadata, integrity signals, and response boundaries. Existing Response Reconciliation found caveats and uncertainty among the strongest unresolved response themes.

# Fragmentation Assessment

This is the central finding.

Caveat information is **distributed, fragmented, duplicated in places, and partially unified**.

## Centralized

Limited centralization exists in Projection Integrity Summary:

- unsupported fact count;
- fact conflict count;
- contradiction count;
- graph issue count;
- stale fact count;
- refresh recommendation count;
- capability verification state counts;
- explicit caveat text.

This centralization is aggregate-level only. It is not a per-answer, per-response, per-fact, per-capability, or cross-surface caveat contract.

## Distributed

Caveat sources are distributed by legitimate ownership:

- Evidence Graph owns evidence/missing evidence views.
- Confidence owns confidence/support/contradicted/unsupported reasons.
- Contradictions owns conservative contradiction reports.
- State owns fact supports, conflicts, stale facts, graph issues, and current-state helpers.
- Capability Inventory owns capability verification caveats from projected facts.
- Explanation owns why/current/ambiguous/no-current communication.
- Context Views own selected decision-context caveat-adjacent summaries.
- CLI owns presentation.

This distribution is appropriate because each owner preserves source semantics.

## Fragmented

Fragmentation exists because answering cross-surface caveat questions requires joining multiple surfaces manually:

- current fact caveats require support, evidence, confidence, contradiction, conflict, stale, and explanation joins;
- capability caveats require capability inventory, verification facts, support/evidence, ToolNeed/capability resolution, and possibly confidence joins;
- answer/response caveats require Runtime response payloads plus selected context/integrity/explanation/capability signals, but no shared composition rule exists;
- stale/expired/refresh semantics are split among `Fact`, `FactSupport`, State stale helpers, refresh recommendations, capability inventory, Integrity Summary, and CLI outputs;
- “unknown” and absence states are local concepts rather than a single caveat category.

## Duplicated

Some concepts intentionally recur across surfaces:

- unsupported appears in Evidence Summary, Confidence, Decision Context, CLI, and Integrity Summary;
- contradicted/conflict information appears in `FactConflict`, `Contradiction`, Confidence, Explanation, Decision Context, and Integrity Summary;
- stale appears in State stale facts, Capability Inventory, refresh recommendations, CLI, and Integrity Summary;
- confidence appears in facts, fact support, evidence nodes, capability evidence/support, explanations, confidence views, and context views.

This duplication is not necessarily wrong; it is often local presentation over the same projected conditions. The risk is semantic drift if a new parallel caveat system redefines these concepts.

## Partially Unified

Partial unification exists through:

- Response Vocabulary naming caveats, limitations, uncertainty, integrity signals, response content, response metadata, and response boundaries;
- Projection Integrity Summary aggregating key integrity caveat counts and explicit caveats;
- Explanation Contract Vocabulary naming explanation status and explanation fields;
- Selection Rationale documents identifying distributed rationale and rejecting unjustified summary implementation;
- Knowledge Lifecycle Reconciliation placing Integrity before Selection and Response, with Response communicating selected knowledge and limitations.

Finding: caveat information already exists but is scattered. The gap is shared caveat vocabulary/composition guidance, not missing raw caveat-producing behavior.

# Composition Opportunities

Documentation-only opportunities supported by inspection:

1. **Response Caveat Vocabulary**
   - Define caveat, caveat source, caveat signal, caveat output, caveat metadata, caveat presentation, and caveat non-goals.
   - Preserve existing owners and avoid implementation.

2. **Response Caveat Reconciliation**
   - Reconcile caveat language across Response Vocabulary, Integrity Summary, Explanation Contract, Capability Verification, Selection Rationale, and CLI surfaces.
   - Identify whether a small canonical status vocabulary is enough.

3. **Caveat Classification Characterization**
   - Classify existing caveats as integrity, evidence, capability, temporal, confidence, selection, observation, response, graph, rationale, or operational caveats.
   - Keep classifications documentation-only unless a future concrete operator need requires implementation.

4. **Caveat Communication Characterization**
   - Characterize how caveats are phrased, grouped, ordered, and suppressed across current surfaces.
   - Focus on communication consistency, not new behavior.

5. **Per-surface caveat mapping table**
   - Document which existing surfaces already expose which caveat signals.
   - Avoid adding a runtime inventory or read model unless future evidence proves manual documentation is insufficient.

Implementation opportunities are not recommended by this characterization.

# Rejection Criteria

Caveat implementation work should **not** occur when any of the following conditions hold:

- existing caveat communication already answers the operator question;
- the proposed change only renames existing statuses without improving operator understanding;
- the proposed change duplicates Integrity Summary, Confidence, Evidence Graph, Contradictions, Capability Inventory, State Views, Explanation, or Context Views;
- the proposed change creates a parallel owner for truth, support, contradiction, confidence, stale status, verification, or response composition;
- the proposed change requires Runtime integration only to display information already available in read-only surfaces;
- the proposed change requires ToolExecutor integration to communicate verification or availability caveats already represented as projected facts;
- the proposed change mutates projections, appends events, executes refreshes, verifies capabilities, calls providers, or changes selection rules;
- no unanswered operator question is identified;
- the only benefit is a universal formatter or universal caveat layer;
- the work cannot preserve source ownership and source semantics.

Caveat implementation work may become worth reconsidering only if a future audit identifies a concrete operator-facing question that is important, recurring, not answerable by existing surfaces, and not addressable by documentation/vocabulary/reconciliation alone.

# Complexity Traps

| Trap | Why it is a trap |
| --- | --- |
| `CaveatEngine` | Would create a parallel owner for caveat-producing conditions already owned by Integrity, Confidence, Evidence Graph, State, Contradictions, Capability Inventory, Explainability, and Context Views. |
| `ResponseEngine` | Prior response work rejected this; response behavior is already distributed and partially present. A new engine risks centralizing presentation while duplicating source semantics. |
| `IntegrityEngine` | Integrity already exists as read-only characterization and summary/navigation surfaces. An engine would imply repair/truth/mutation authority that is not justified. |
| `ExplainabilityEngine` | ExplanationBuilder and explanation vocabulary already exist; a new engine risks owning support, contradiction, rule, capability, and temporal semantics incorrectly. |
| `ReasoningEngine` | Caveats do not require model reasoning or a new reasoning owner; existing deterministic projection views already produce the relevant signals. |
| `ContextEngine` | Context composition/selection already exists. Caveat communication should not centralize context ownership or selection policy. |
| Planner / WorkflowEngine | Caveats are communication/qualification signals, not planning or workflow execution requirements. |
| Universal Caveat Layer | Would flatten local semantics like unsupported, unverified, stale, unknown, contradicted, graph-invalid, and ambiguous into a potentially misleading universal status system. |
| Universal Formatter | CLI and surfaces have local presentation needs. A universal formatter would not solve ownership or semantic differences. |
| Runtime integration by default | Runtime owns routing and envelopes, not caveat generation. Integrating caveats there first would couple response communication to execution paths. |
| ToolExecutor integration by default | ToolExecutor execution status is not capability verification or caveat ownership. Integrating caveats there would blur execution, verification, and projected knowledge. |
| Parallel caveat system | Recomputing support, conflicts, confidence, stale status, or verification outside existing owners would create semantic drift. |
| Parallel truth system | Caveats qualify projected knowledge; they must not become truth or correctness decisions. |
| Projection mutation/event append | Caveat characterization is read-only. Mutating projections or appending events to represent caveats would violate the audit boundary. |

# Recommended Outcome

Recommended outcome: **B. Caveats partially present**.

Justification:

- Caveat-producing behavior already exists across evidence, confidence, contradictions, fact conflicts, stale facts, graph validation, capability verification, explanations, state views, context views, integrity summary, runtime responses, and CLI outputs.
- Caveat communication already exists through statuses, flags, counts, reasons, severity, metadata, and command-specific wording.
- Projection Integrity Summary partially unifies integrity caveats but only at aggregate level.
- Response Vocabulary already names caveats and limitations as response language, but there is no dedicated Response Caveat Vocabulary or cross-surface communication rule.
- Operator questions about unsupported, contradicted, conflicted, stale, unverified, confidence-limited, ambiguous, and no-current-belief conditions are often answerable locally.
- Operator questions about all caveats applying to an answer, current fact, capability, selected context, or whole response are not consistently answerable without manual joins.
- Existing findings support documentation/vocabulary/reconciliation, not implementation.

Rejected outcomes:

- **A. Caveats largely present** is too strong because cross-response caveat composition and per-answer/per-response caveat questions remain difficult.
- **C. Caveats missing major concepts** is too strong because the major caveat-producing concepts already exist.
- **D. More audit required** is not necessary for this characterization; enough evidence exists to conclude partial presence, though future targeted audits may refine communication vocabulary.

# Non-Goals

This characterization does not:

- implement caveats;
- implement caveat inventories;
- implement caveat summaries;
- implement caveat navigation;
- implement response engines;
- implement read models;
- implement routes;
- implement adapters;
- implement schema classes;
- modify `Runtime`;
- modify `ToolExecutor`;
- modify `EventLedger` ownership;
- modify `ProjectionStore` ownership;
- mutate projections;
- append events;
- execute tools;
- call providers;
- verify capabilities;
- refresh stale facts;
- change selection rules;
- add a parallel truth, caveat, integrity, explanation, selection, or response system.

# Conclusion

Seed already has substantial caveat-producing information and substantial caveat communication. The information appears as unsupported facts, missing evidence, contradictions, fact conflicts, stale/expired facts, refresh recommendations, graph issues, confidence limitations, unverified/stale/provider-reported/unknown capability states, ambiguous and no-current-belief explanations, selected-context confidence and issue signals, and operational read-only/no-execution limitations.

The repository pattern remains consistent: behavior exists first, vocabulary and composition lag behind, and new engines are usually not justified. Caveats follow that pattern. The next safe step, if one is needed, is documentation-only vocabulary or reconciliation that preserves existing owners and avoids implementation. The recommended outcome is **B. Caveats partially present**.
