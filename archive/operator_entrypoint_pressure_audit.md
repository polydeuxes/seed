---
status: audit
scope: operator entrypoint pressure around State Summary
created: 2026-06-18
---

# Operator Entrypoint Pressure Audit

## Status

This is an implementation-adjacent architectural audit only. It does not modify implementation, State Summary, Inquiry Orientation, command structure, ontology, runtime concepts, policy, or operator workflow.

Findings are exploratory. Repository evidence is treated as stronger than recent framing, and observed operator behavior is treated as evidence rather than authority.

## Question

Central audit question:

```text
Why does an operator arrive at State Summary?

What needs is State Summary currently satisfying?

Which of those needs appear to belong to State Summary?

Which appear to belong elsewhere?

Is the pressure actually about State Summary,
or about operator entrypoints into repository knowledge?
```

The audit does not assume that State Summary is wrong, overloaded, or in need of redesign.

## Repository evidence reviewed

Required documents reviewed:

- `docs/state_summary_scope_review.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/view_authority_and_surface_responsibility_reconciliation.md`
- `docs/view_branch_continuity_reconciliation.md`
- `docs/participant_orientation_view_selection_observation.md`
- `docs/bounded_consequence_discipline_observation.md`

Implementation and test surfaces sampled only to understand current operator interaction patterns:

- `scripts/seed_local.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/state_views.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/candidate_requests.py`
- `tests/test_seed_local_script.py`
- `tests/test_projection_store.py`
- `tests/test_inquiry_orientation.py`
- `tests/test_candidate_requests.py`

Searches sampled CLI entrypoints and related tests for:

```text
--state-build
--current-facts
--impact
--source-navigation
--inquiry-orientation
--integrity-summary
candidate summary routing
```

## Operator journey investigation

Common operator questions do not map to one repository surface.

| Operator question | Closest pressure | Evidence-based reading |
| --- | --- | --- |
| `What changed?` | State / Continuation / unresolved | State Summary shows projection identity and projected counts, but reviewed evidence does not show it as a change-history or continuation authority. It may help establish the current read-model shape after a change, while actual change lineage remains elsewhere. |
| `What should I look at?` | Navigation / Orientation | View authority separates navigation surfaces from evidence and interpretation surfaces. Participant-orientation work found pressure around attention, activation, and view selection, but no implemented view-selection mechanism. State Summary can supply cues, but those cues are not clearly its authority. |
| `What is wrong?` | Integrity / View / unresolved | State Summary exposes conflicts, stale facts, and graph issue counts as integrity-adjacent accounting. Integrity Summary, graph issues, contradictions, fact conflicts, and stale-fact surfaces are more direct integrity surfaces. State Summary may be a first warning light, not the full authority. |
| `What does Seed currently know?` | State / Evidence | Current Facts is the clearest evidence surface in the reviewed taxonomy. State Summary answers a smaller inventory question: how large and structurally visible the projected State is. |
| `Where do I begin?` | Entrypoint / Navigation / Orientation | No reviewed authority establishes a canonical beginning surface. State Summary likely attracts this pressure because it is broad, compact, and named as a summary. This is operator-entrypoint pressure more than clear State authority. |
| `What is relevant right now?` | Orientation / Inquiry / View / unresolved | Inquiry Orientation explicitly refuses importance, intent, concern, recommended action, and next safe move. State Summary has prominence and availability cues, but repository authority warns that ranking, grouping, and attention shaping are lens/view choices rather than raw State. |

Exploratory finding: State Summary appears to receive mixed operator questions because it is one of the few broad, runnable, compact surfaces. The pressure is not solely about State Summary content. It also appears to be about the absence of a single authorized operator entrypoint into repository knowledge.

## State Summary investigation

Repository evidence supports State Summary as a deterministic, read-only summary of projected State/read model. The strongest State-owned responsibilities are projection identity, read-model cardinality, fact lifecycle accounting, provenance/source accounting, and count-level integrity visibility.

Observed responsibilities classify as follows:

| Responsibility | Support level | Reading |
| --- | --- | --- |
| Projection description | Strong | Compact State Summary includes projection identity fields and counts. This belongs naturally to State Summary. |
| Knowledge inventory | Strong to moderate | Entity, fact, observation, requirement, capability, issue, relationship, durable-fact, and measurement-current counts are inventory-like. They fit State Summary when framed as projected-State accounting. |
| Availability visibility | Moderate, boundary-sensitive | Availability is represented as projected facts and grouped by scope, but repository evidence warns it can be misread as live health. It appears lens/view-shaped unless framed strictly as availability-fact accounting. |
| Entity prominence | Moderate, lens-like | Top entities by kind are derived from State, but ranking, suppression, limits, and buckets are selection choices. This is a likely source of attention pressure. |
| Storage visibility | Weak for default State Summary; stronger for separate projection helper | Default State Summary intentionally rejects storage detail and topology counts in tests, while a separate storage projection helper exists. Storage interpretation appears outside core State Summary responsibility. |
| Integrity information | Strong at count level; weaker for drilldown | Conflict, stale fact, and graph issue counts fit State Summary as accounting. Explaining uncertainty or directing repair belongs more naturally to integrity surfaces. |
| Navigation cues | Weak to moderate | Top entities, kind buckets, and counts can help an operator choose a next surface, but reviewed authority does not make State Summary a navigation surface. |
| Orientation cues | Weak and boundary-sensitive | Prominence and availability can orient attention, but orientation-related documents preserve uncertainty and avoid promotion into recommended action or next move. |

State Summary currently satisfies at least four operator needs:

1. A compact snapshot of projected-State size and identity.
2. A quick inventory of visible entity/fact/provenance/availability structures.
3. A first-pass integrity warning surface.
4. A broad entrypoint when the operator does not yet know which narrower surface to use.

The first three are supported by repository authority to varying degrees. The fourth is strongly observable as pressure but weakly authorized as State Summary responsibility.

## Alternative surface investigation

### State Summary

State Summary absorbs broad entrypoint pressure because it is compact, read-only, and combines inventory, count-level integrity, availability grouping, entity prominence, source counts, and projection metadata. Candidate-request routing also names a `state-summary read-only inspection surface`, which makes it an available answer to generic summary language.

Pressure absorbed:

- projected-State inventory;
- initial situational awareness;
- integrity warning visibility;
- entity prominence;
- availability-fact visibility;
- fallback broad summary when no narrower question has been selected.

### Current Facts

Current Facts aligns with the evidence-surface question `What does Seed currently know?` It preserves visibility and grepability and is tested as exposing raw facts that Impact later compacts or interprets.

Pressure absorbed:

- evidence inspection;
- completeness and traceability;
- low-interpretation fact lookup;
- support for debugging and reconciliation.

### Impact

Impact aligns more with interpretation around an entity. Tests show it groups local network facts, mount facts, endpoint availability roles, identity, listener endpoints, and storage topology compactly while preserving cues back to Current Facts for full evidence.

Pressure absorbed:

- entity-centered understanding;
- compact operational interpretation;
- bounded grouping of noisy evidence;
- local relevance around a named subject.

### Source Navigation

Source Navigation is explicitly read-only navigation over preserved `imports` and `defines` facts. It does not inspect files, parse source, ingest observations, or infer behavior, reachability, or ownership.

Pressure absorbed:

- repository-source lookup;
- bounded navigation from query to preserved source facts;
- symbol/module/path discovery;
- source-oriented continuation support without source authority expansion.

### Inquiry Orientation

Inquiry Orientation accepts preserved operator prose and returns deterministic lexical overlaps against projected read models and source navigation. It explicitly refuses promotion into facts, goals, decisions, commands, runtime instructions, intent, concern, recommended action, or next safe move.

Pressure absorbed:

- relating an operator question to existing material;
- preserving uncertainty;
- showing potentially related projected facts and source-navigation matches;
- orientation around a note without asserting importance or action.

### Other views

Integrity Summary, contradictions, fact conflicts, stale facts, graph issues, fact support, best fact, evidence, why, and confidence surfaces absorb narrower integrity, support, provenance, and explanation pressure. Their presence weakens any claim that State Summary alone owns all operator understanding.

## Pressure classification

| Identified pressure | Closest classification | Confidence | Notes |
| --- | --- | --- | --- |
| Need for projected-State size and identity | State | High | Compact State Summary directly supports this. |
| Need for knowledge inventory | State / View | High | Counts belong close to State; presentation is a View. |
| Need to know whether projected knowledge has integrity concerns | State / View / Integrity | High | Count-level visibility fits State Summary; drilldown belongs to integrity surfaces. |
| Need to see what entities are prominent | Lens / View / Orientation | Medium | Ranking and buckets are lens-like and attention-shaping. |
| Need to see availability quickly | View / State / unresolved | Medium | Availability facts are State-derived, but interpretation as health is outside authority. |
| Need to know where to go next | Navigation / Orientation | Medium | Repository has navigation surfaces, but no canonical entrypoint or selection mechanism. |
| Need to know what is relevant right now | Orientation / Inquiry / unresolved | Medium-low | Inquiry Orientation refuses importance and next-action claims; relevance remains bounded and uncertain. |
| Need to begin an investigation | Navigation / Continuation / unresolved | Medium | This appears to be entrypoint pressure rather than State Summary authority. |
| Need to continue recent work | Continuation / Inquiry / Orientation | Medium-low | Continuity documents discuss continuation pressure, but State Summary is not shown as its owner. |
| Need to inspect raw current knowledge | State / Evidence | High | Current Facts is a stronger match than State Summary. |
| Need to understand one entity's consequences or surrounding context | View / Lens | High | Impact is a stronger match than State Summary. |
| Need to relate operator prose to repository material | Inquiry / Orientation | High | Inquiry Orientation is purpose-built but bounded. |
| Need to navigate source definitions/imports | Navigation | High | Source Navigation is purpose-built and bounded. |

## Bounded consequence relevance

Bounded consequence discipline is a useful comparison tool. It suggests that accepting input or exposing a surface does not authorize every possible consequence of that surface.

Applied to this audit:

- State Summary can expose availability-fact counts without becoming live health authority.
- State Summary can expose top entities without becoming an attention or next-action authority.
- State Summary can expose integrity counts without becoming repair guidance.
- State Summary can expose observation-source counts without explaining which source matters now.
- Inquiry Orientation can relate note text to projected material without asserting intent, concern, importance, or next safe move.
- Source Navigation can find preserved source facts without asserting ownership, behavior, or reachability.

This comparison supports caution: some pressure repeatedly landing on State Summary may be consequence pressure beyond the surface's apparent boundary. However, it does not prove State Summary is wrong. A compact summary may intentionally provide bounded cues so long as they are not over-promoted.

## Continuity assessment

Exploratory thought exercise:

```text
If State Summary disappeared tomorrow,
what operator needs would become unmet?
```

Likely unmet needs:

1. A compact projected-State inventory.
2. Projection identity visibility in a familiar operator command.
3. Count-level integrity visibility colocated with State size.
4. One broad, low-commitment place to begin inspection.
5. Quick visibility into entity prominence and availability-fact distribution.
6. A summary-routed target for generic `summary` language.

Which of those clearly belong to State Summary?

- Compact projected-State inventory: yes, strongly.
- Projection identity visibility: yes, strongly.
- Count-level integrity visibility: yes, if framed as accounting rather than guidance.
- Broad beginning point: unclear. This appears to reveal entrypoint pressure, not necessarily State Summary authority.
- Entity prominence and availability distribution: mixed. They are State-derived but lens/view-shaped.
- Generic summary routing: observable implementation behavior, but routing availability is not architectural proof that State Summary owns every summary need.

Continuity finding: removing State Summary would expose a real operator gap, but the gap would be mixed. Some unmet needs are State Summary-shaped. Others would reveal unresolved entrypoint, orientation, navigation, and view-selection pressure already present elsewhere.

## Alternative explanations

### State Summary is functioning exactly as intended

Plausible. Repository evidence supports a compact projected-State summary plus a richer operator summary. Its broadness may be intentional and useful when bounded as read-only projected-State accounting.

### Operator workflow created the pressure

Plausible. Recent investigations repeatedly used State Summary as a primary operator surface, which can create familiarity and make it the default place to look even when a narrower surface exists.

### The repository lacks an entrypoint surface

Plausible but not established as a problem. The reviewed evidence shows many specialized surfaces and no implemented canonical view-selection mechanism. State Summary may be serving as a de facto entrypoint because it is broad and easy to invoke.

### The pressure is merely familiarity

Plausible in part. State Summary is memorable, compact, and repeatedly referenced. Familiarity could explain some usage without implying architectural overload.

### The pressure is unrelated to architecture

Possible. Some pressure may come from test habits, operator convenience, command naming, or recent task sequencing rather than surface responsibility.

### State Summary is absorbing pressure that belongs elsewhere

Plausible for orientation, next-action, relevance, source navigation, and entity-centered interpretation. Repository evidence supports separate surfaces for several of these. The audit cannot conclude a redesign from that observation.

## Uncertainties

- The audit did not measure actual operator command frequency; it inferred usage pressure from recent repository work, tests, routing, and documented investigations.
- `Lens`, `Orientation`, `Participant`, and `View selection` remain exploratory in the reviewed documents.
- State Summary's richer operator summary may intentionally include bounded lens-like cues; the audit cannot separate intended breadth from accidental overload.
- Generic `summary` language in candidate routing may reflect convenience rather than authority.
- The repository may already contain older or narrower documents that further constrain individual surfaces beyond the required review set.
- The boundary between first-pass cue, navigation cue, and orientation cue remains porous.

## Non-conclusions

This audit does not conclude that:

- State Summary should be redesigned;
- new commands should be added;
- Inquiry Orientation should change;
- command structure should change;
- Views should be implemented differently;
- Orientation should become a runtime concept;
- participant pressure should become ontology;
- State Summary is wrong;
- State Summary is the only or canonical operator entrypoint;
- operator workflows should change.

Safest audit finding:

```text
State Summary appears to be satisfying both legitimate projected-State summary
needs and broader entrypoint/orientation/navigation pressures. Repository evidence
supports the former more strongly than the latter. The latter pressures are real
enough to document, but not strong enough to authorize redesign or new concepts.
```
