# Examination Frontier Projection Slice 001

## 1. Recovered responsibility

This slice recovers exactly one responsibility: explicit campaign inputs -> deterministic validation and classification -> immutable read-only `ExaminationFrontier` projection. The bounded question is: for known artifacts in a bounded corpus and explicitly identified candidate examination work, what work is currently eligible, examined, blocked, unsupported, deferred, failed, or Unknown, and why?

## 2. Producer

The producer is `project_examination_frontier(...)` in `seed_runtime/examination_frontier.py`.

## 3. Input artifacts

Inputs are an existing `BoundedConstitutionalQuestion`, a caller-supplied bounded corpus inventory, and caller-supplied candidate-work visibility testimony. The corpus and work inputs are not discovery products.

## 4. Output artifact

The output is `ExaminationFrontier`, an immutable dataclass artifact with `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## 5. Direct consumers

Current direct consumers are the bounded diagnostic/operator surface `seed --examination-frontier JSON_FILE` and the supervised mixed-corpus demonstration in tests and this report. The future consumer is not implemented.

## 6. Bounded inquiry linkage

The frontier references the existing `BoundedConstitutionalQuestion` by bounded-question id, provenance, and question text. This slice does not modify the bounded inquiry owner or add corpus/campaign fields to it.

## 7. Corpus input convention

The corpus input preserves `corpus_id`, optional label, explicit member ids, substrate kind, artifact identity, artifact hash or version when known, references/provenance, location/material reference, scope status, authorization/access testimony, member unknowns, and corpus unknowns.

## 8. Candidate-work input convention

Candidate work preserves stable candidate id, corpus-member reference, work kind, capability/projection identity, convention/version, compatibility testimony, authorization status, existing result references, blocker testimony, deferral testimony, failure references, supplied status testimony, provenance, and unknowns.

## 9. Work-item identity rule

`work_item_id` is a deterministic SHA-256 identity over corpus id, member id, artifact identity, artifact hash/version, work kind, capability id, and projection/capability convention. Changed artifact hash or changed convention changes the work identity.

## 10. Frontier identity rule

`frontier_id` is deterministic over bounded-question id, corpus id, frontier convention, and the deterministic ordered work-item ids. Creation time is not used.

## 11. Classification model

Classification facets are orthogonal booleans: `eligible`, `examined`, `blocked`, `unsupported`, `deferred`, `failed`, `unknown`, and `conflict`. This intentionally permits lawful combinations such as failed-but-eligible retry evidence.

## 12. Mutually exclusive or orthogonal statuses

Statuses are orthogonal facets, not one mutually exclusive enum.

## 13. Eligibility rule

A work item is eligible only when compatibility is supplied as compatible, authorization is authorized or not applicable, no active blocker is supplied, no explicit deferral is supplied, no current matching completed result already satisfies the same bounded work identity, and no required Unknown remains.

## 14. Examined rule

A work item is examined only when an existing result reference matches the same member, artifact hash/version, work kind, capability id, convention/version, and completed state.

## 15. Blocked rule

A work item is blocked when explicit blocker testimony is supplied for a supported-in-principle candidate, such as environment access failure, dependency absence, unavailable credentials, unavailable network path, or required prior work not completed.

## 16. Unsupported rule

A work item is unsupported when supplied compatibility visibility is explicitly `unsupported`. Unsupported does not mean prohibited or permanently impossible.

## 17. Deferred rule

A work item is deferred only when explicit deferral testimony is supplied. Inactivity alone is not deferral.

## 18. Failed rule

A work item is failed when explicit failed-attempt testimony is supplied. Failure does not automatically create blockage or unsupported status.

## 19. Unknown rule

Unknown is emitted when supplied evidence is insufficient for required classification, including unknown compatibility or authorization, or when conflict is preserved.

## 20. Conflict-evidence rule

The implementation emits typed `conflict=true` and `unknown=true` for conflicting supplied status evidence that can be preserved without corrupting identity. Existing-result mismatches fail deterministically because they would otherwise substitute a result for a different bounded work item.

## 21. Newly-eligible decision

`newly_eligible` is not implemented as a transition because this slice has no previous-frontier/campaign-history owner. It is exposed as `unresolved_no_previous_frontier_input` and remains a road.

## 22. Summary-count convention

Summary counts count each orthogonal classification facet independently across emitted work items. Counts may overlap because facets are orthogonal.

## 23. Boundary notes

Human and JSON output preserve boundary notes that the frontier is read-only, discovers neither corpus members nor compatible capabilities, does not select/authorize/execute eligible work, does not equate examined with understood/admitted/complete, distinguishes blocked/unsupported/failed/Unknown, is not a scheduler/queue/priority/campaign verdict, performs no comparison/recurrence/semantic interpretation/responsibility recovery, and is not runtime Evidence or Fact.

## 24. Read-only guarantees

Projection and rendering append no events, create no pending actions, execute no tools, mutate no state/corpus/cluster, acquire no material, create no Observations/Evidence/Facts, and change no capability inventory.

## 25. Mixed-corpus demonstration

The demonstration contains Project Gutenberg website-oriented target identity, `selected_lesson_006.txt`, and bounded repository `AGENTS.md` identity. It uses only supplied testimony and existing matching result references; it performs no live network access.

## 26. Website blocker treatment

The website acquisition work is blocked by supplied environment/access testimony before confirmed live Gutenberg bytes. The demonstration does not attribute refusal to Project Gutenberg.

## 27. Book frontier results

`selected_lesson_006.txt` preserves hash `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`. Matching structural and surface-feature projection result references classify those work items as examined. Prose interpretation remains Unknown because no current canonical request-orchestration/result evidence is supplied.

## 28. Repository frontier results

Bounded `AGENTS.md` structural and surface-feature projection work uses the same neutral projection contracts and matching result references. It does not claim semantic understanding or semantic correspondence.

## 29. Codex/campaign-author supplied inputs

Campaign author supplied bounded corpus membership, candidate work identities, compatibility/capability visibility testimony, existing result references, blocker/deferral/failure testimony where applicable, and corpus/work unknowns.

## 30. Seed-owned projection responsibilities

Seed supplies input validation, stable work identity, deterministic frontier classification, immutable frontier artifact construction, and read-only human/JSON rendering.

## 31. Manual handoff eliminated

The slice eliminates manual remembering of scoped material, examined work, possible work, blockers/unsupported work, and narrative status classification. It does not choose next work.

## 32. Future immediate consumer

The future immediate consumer remains a frontier work selector or probe-request generator.

## 33. Exact next bounded question

Given an immutable examination frontier, what existing owner—or smallest missing owner—may select one eligible work item for conversion into a bounded probe request while preserving inquiry scope, selection reason, authorization boundaries, and all non-selected frontier items?

## 34. Compatibility answer

Did this slice change any existing compatibility boundary?

No.

## 35. Files changed

- `seed_runtime/examination_frontier.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `tests/test_examination_frontier.py`
- `examination_frontier_projection_slice_001.md`

## 36. LOC delta

Recorded before commit with `git diff --stat` and `git diff --numstat`.

## 37. Tests executed

- `pytest -q tests/test_examination_frontier.py`
- `pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py`
- `pytest -q tests/test_external_material_structural_projection.py tests/test_external_material_surface_feature_projection.py tests/test_external_material_testimony_binding.py`

## 38. Remaining missing roads

- bounded corpus sources -> corpus discovery and inventory expansion
- artifact identity + capability visibility -> compatible-projection enumeration
- `ExaminationFrontier` -> bounded eligible-work selection
- selected frontier work -> explicit probe request
- probe request -> policy authorization -> execution
- probe result -> frontier revision
- new capability -> previously blocked work -> newly eligible work
- frontier results -> next discriminating question
- external prose gap -> attributed grammar-provider request
- frontier exhaustion or blockage -> truthful completion or suspension
- selected feature subjects -> deterministic comparison
- comparison results -> bounded recurrence testimony

## Starting evidence verified

`deep_corpus_examination_capability_topology_audit_001.md` states that Seed has bounded inquiry and several examination tools but lacks the central campaign/frontier responsibility; that examination-frontier generation and preservation is the first missing boundary; that Codex currently acts as campaign coordinator and external grammar provider; and that deep examination needs a distinct campaign-level artifact or handoff. Existing bounded inquiry, site-rule testimony, external material projections, and shared neutral repository projection roads were preserved.
