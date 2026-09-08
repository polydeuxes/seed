# Constitutional Inquiry Admissibility Record Investigation

Repository authority wins. This document performs one bounded constitutional investigation only. It does not implement an admissibility record, inquiry navigation, a question engine, planning, a registry, an ontology, runtime behavior, or a new diagnostic surface.

## Investigation scope

Bounded question:

> Across exact question-surface inventory, inquiry orientation, source navigation, reasoning path audit, selection path audit, fact support, explanation, diagnostic inventory, and diagnostic shape audit, what fields or statuses, if any, consistently constitute an admissibility record for a next evidence-bearing question?

The phrase `admissibility record` is treated only as investigation pressure. The investigation asks whether recurring repository evidence already preserves common anatomy around a next evidence-bearing question. It does not assume the record exists.

## Recurring constitutional evidence

1. **Exact question-family evidence supports bounded public inquiry identity, not prose-derived questions.** `constitutional_question_family_reconciliation_investigation.md` reports that Question Families are exact static inventory rows, not inferred prose categories. The recurring fields named there include family name, example questions, answering surface, CLI flag, answer responsibility, authority boundary, notes, bounded status, dispatch surface, required arguments, formatter metadata, implementation reason, diagnostic relationship fields, and relationship status. It also reports that unknown families are unknown or rejected rather than inferred.

2. **Bounded inquiry discipline recurs as evidence, boundary, unknown, confidence, and stop.** `competency_interrogation_grammar_investigation.md` recovers recurring interrogation discipline around subject identity, evidence binding, preconditions or inputs, outputs or handoff, boundaries, granted and negative authority, unknowns, lawful stop, reliance, termination, and confidence. This supports a constitutional anatomy for deciding whether a bounded inquiry may answer, but it does not prove a single shared implemented record.

3. **Presentation vocabulary remains non-authoritative unless implementation evidence supports it.** The repository instructions explicitly warn that terms such as source navigation may be visibility or presentation labels only. This weakens any attempt to promote a shared admissibility vocabulary from labels alone.

4. **Diagnostic visibility contract recurs as an authority boundary.** The repository instructions require diagnostic inventory and diagnostic shape-audit coverage when new diagnostic or recordable surfaces are added, and require diagnostic recording to preserve `record_scope=diagnostic_run` and `mutates_cluster=false` unless intentionally different. This is recurring admissibility evidence for diagnostic surfaces, but only inside the diagnostic-surface boundary.

5. **Unknown preservation and stop discipline recur as refusal mechanisms.** Existing constitutional investigations repeatedly preserve unknowns, unsupported answers, remaining questions, lawful termination, and confidence limits. That recurrence supports an admissibility result that can lawfully say unknown, ineligible, unsupported, blocked, or stop rather than generating the next question autonomously.

## Recurring implementation evidence

1. **Question-surface inventory already exposes the strongest exact inquiry gate.** `seed_runtime/question_surface_inventory.py` builds deterministic read-only rows with `question_family`, `surface`, `surface_flag`, `answer_responsibility`, `authority_boundary`, `notes`, `required_surface_args`, `bounded_status`, `dispatch_surface`, formatter metadata, diagnostic relationship fields, and `relationship_status`. Running `python scripts/seed_local.py --question-surface-inventory --json` returned 17 rows with these keys. This is direct implementation evidence for exact public inquiry identity, eligibility status, required arguments, authority boundary, and diagnostic relationship.

2. **Inquiry orientation preserves operator prose without converting it into fact or instruction.** `seed_runtime/inquiry_orientation.py` defines an authority boundary stating that an inquiry note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. It exposes note identity, related material, surface family, support, uncertainty, and boundary. This reinforces admissibility as bounded orientation only; it does not create a next-question engine.

3. **Source navigation admits only explicit query lookup over preserved facts.** `seed_runtime/source_navigation.py` requires a query and builds source-navigation rows from projected fact supports. Its boundary says it uses existing projected source fact/support evidence only and does not inspect repository files during lookup or infer beyond source-navigation matches. This contributes target/query identity, evidence source, source/support relationship, and unknown status, but only for lookup.

4. **Reasoning path audit exposes required domain and subject plus read-only derivation boundary.** `seed_runtime/reasoning_path_audit.py` defines `ReasoningPathAudit` with `domain`, `subject`, evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and a boundary with `records_facts=false`, `writes_event_ledger=false`, and `mutates_cluster=false`. This supports target identity, evidence path, consumers, Unknown preservation, and mutation boundary.

5. **Selection path audit exposes target, candidates, selected result, evidence, unknowns, and read-only boundary.** `seed_runtime/selection_path_audit.py` defines `SelectionPathAudit` with `target`, `selected`, candidates, selection factors, non-selected alternatives, evidence, outcome, unknowns, and the same no-record/no-ledger/no-mutation boundary. This supports selection eligibility and refusal anatomy without general planning.

6. **Fact support and explanation preserve support status rather than question generation.** `seed_runtime/explanations.py` answers `why(subject, predicate)` using projected fact support and returns statuses `current`, `ambiguous`, or `no_current_belief`, with support confidence, supporting fact ids, evidence ids, source types, observed timestamps, competing beliefs, and conflict when present. This supports evidence source, support status, confidence, and unknown/no-current-belief boundaries for a claim.

7. **Diagnostic inventory declares operational surface shape.** `seed_runtime/diagnostic_inventory.py` defines `DiagnosticInventoryEntry` fields: name, CLI flags, projected-state use, repo-file use, JSON support, record support, record scope, diagnostic/cluster fact emission, event-ledger writes, cluster mutation, diagnostic fact reads, and description. Running `python scripts/seed_local.py --diagnostic-inventory --json` returned 52 rows with these keys. This is strong implementation evidence for surface identity, recordability, event-ledger boundary, mutation boundary, and evidence-source class for diagnostics.

8. **Diagnostic shape audit checks declared implementation shape.** `seed_runtime/diagnostic_shape_audit.py` compares diagnostic inventory declarations with static implementation specs and emits rows with diagnostic, field, declared, observed, and status. Running `python scripts/seed_local.py --diagnostic-shape-audit --json` returned 468 rows with these keys. This supports diagnostic relationship and shape consistency, not domain truth.

## Recovered recurring admissibility fields, if any

No single repository-wide `admissibility record` is implemented or constitutionally recovered as a named artifact.

However, recurring evidence does recover a **smaller common admissibility anatomy** for a next evidence-bearing question. The fields/statuses that recur across enough surfaces to be stable are:

| Recovered field or status | Evidence strength | Constitutional meaning |
| --- | --- | --- |
| **Question or surface identity** | Strong | A bounded inquiry must name an exact question family, diagnostic surface, note, query, domain/subject, target, or subject/predicate. The identity is not inferred from prose when the implementation requires exact input. |
| **Answering or evidence surface** | Strong | The repository repeatedly identifies the surface that can answer or expose evidence: question inventory rows, source navigation, reasoning path, selection path, explanation, or diagnostic inventory/audit. |
| **Required arguments / target identity** | Strong | Several surfaces require explicit parameters: source-navigation query, reasoning domain and subject, selection target, explanation subject and predicate, inquiry note id/latest note, or question-family required surface args. Missing or unknown targets stop or bound the answer. |
| **Authority boundary** | Strong | Read-only, no-routing, no-execution, no-recording, no-ledger, and no-mutation boundaries recur. Inquiry orientation especially refuses to convert prose into facts or commands. Diagnostic inventory and audits declare event-ledger and mutation boundaries explicitly. |
| **Evidence source / support relation** | Strong | Fact supports, source-navigation rows, reasoning evidence, selection evidence, explanation support, diagnostic declarations, and shape-audit declared/observed pairs all preserve where the answer comes from. |
| **Eligibility / bounded status** | Medium-high | Question-surface inventory has explicit bounded status; diagnostics have known/unknown and shape status; explanations have current/ambiguous/no-current-belief; authority slices use blocked/unknown-like outcomes. These are not one enum, but they recur as local admissibility statuses. |
| **Unknown or refusal status** | Strong | Unknown-family refusal, typed unknowns, source-navigation unknowns, diagnostic unknowns, no-current-belief, unsupported conclusions, and lawful stop recur as preservation rather than failure to be hidden. |
| **Diagnostic relationship** | Medium-high | For public question surfaces and diagnostics, diagnostic inventory name, shape spec name, relationship status, declared/observed/status, and registry-vs-implementation checks recur. This is strong only for diagnostic-adjacent surfaces. |
| **Recordability and mutation boundary** | Strong for diagnostics, medium elsewhere | Diagnostic inventory explicitly records support for `supports_record`, `record_scope`, event-ledger writes, and `mutates_cluster`. Reasoning and selection audits expose no-record/no-ledger/no-mutation boundaries. This is not universal for every inquiry surface but recurs strongly where operational visibility is involved. |
| **Stop reason / limitation** | Medium | Stop discipline recurs constitutionally and appears in local limitations, unknowns, no-current-belief, missing arguments, diagnostic-only status, and no-match uncertainty. The exact field name `stop_reason` is not shared. |

### Smallest recovered answer

The repository already preserves the following admissibility anatomy, but not a formal record:

```text
exact inquiry/surface identity
+ required target or arguments
+ answering/evidence surface
+ authority boundary
+ evidence/support source
+ local eligibility/status, including Unknown/refusal when applicable
+ diagnostic/record/mutation boundary where the surface is diagnostic or recordable
+ local limitation or stop condition
```

This anatomy is sufficient to answer whether a next evidence-bearing question is bounded and evidence-bearing in the current repository. It is not sufficient to generate, rank, or navigate to the next question.

## Unsupported candidate fields

The following candidates are not recovered as common fields across the reviewed surfaces:

- **A named `admissibility_record` type.** No such implemented or constitutional artifact was found.
- **Autonomous next-question generation.** Evidence supports bounded inquiry admissibility and refusal, not generation.
- **A universal inquiry identity separate from exact family/surface/target identity.** Current evidence is local: question family, diagnostic name, note id, query, domain/subject, target, or subject/predicate.
- **A shared eligibility enum.** `eligible_now`, `eligible_with_parameters`, `diagnostic_only`, `unknown`, `current`, `ambiguous`, `no_current_belief`, `consistent`, `warning`, `mismatch`, and `blocked`-like statuses are local, not one global enum.
- **A shared `stop_reason` field.** Stop discipline recurs, but field names vary or are implicit in status, limitation, unknowns, missing arguments, or boundary text.
- **A shared confidence field.** Explanation and constitutional investigations preserve confidence, but diagnostic inventory and shape audit use declared/observed/status rather than confidence.
- **A shared diagnostic relationship for non-diagnostic surfaces.** Diagnostic relationship is strongly implemented for diagnostic/question-surface boundaries, but source navigation, explanation, and fact support do not become diagnostic surfaces by that fact.
- **A planning or navigation handoff.** Inquiry orientation, source navigation, reasoning path, and selection path expose bounded evidence and related material; they do not plan or route future work.

## Preserved Unknowns

- Whether future implementation should introduce an admissibility record remains unknown and outside this investigation.
- Whether the recurring anatomy should be named remains unknown.
- Whether `stop reason` should become a field rather than local limitation/status remains unknown.
- Whether eligibility statuses should be reconciled across question-family, diagnostic, explanation, authority, and audit surfaces remains unknown.
- Whether diagnostic relationship should remain diagnostic-only or become visible for other inquiry surfaces remains unknown.
- Whether confidence belongs in admissibility, evidence support, or final explanation remains unresolved.

## Confidence

**Medium-high confidence** that recurring repository evidence already preserves common admissibility anatomy around exact identity, required target/arguments, answering or evidence surface, authority boundary, evidence/support source, local eligibility/status, Unknown/refusal, diagnostic/record/mutation boundary where applicable, and limitation/stop.

**Low confidence** that the repository already has a stable, shared, named admissibility record. The evidence is local and recurring, not unified.

## Recommended next bounded investigation, if any

If another investigation is needed, keep it bounded to this question:

```text
Do the local eligibility/status vocabularies across question-surface inventory,
diagnostic shape audit, explanation, reasoning path audit, and selection path audit
share a recoverable status lattice, or must they remain local statuses?
```

That investigation should remain read-only and should not implement a status enum, registry, question engine, planner, or navigation surface.
