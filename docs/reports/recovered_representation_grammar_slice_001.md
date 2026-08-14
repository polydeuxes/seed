# Bounded Representation Grammar Recovery Slice 001

## 1. Recovered responsibility
Seed now owns the bounded recovery step from caller-supplied candidate external grammar hypotheses plus explicit support material into a mechanism-neutral recovered representation grammar projection.

## 2. Producer
`recover_representation_grammars(...)` consumes an existing `CandidateExternalGrammarSet` and optional bounded source-material, claim, comparison, lexical-support, and recovery-material records.

## 3. Input artifacts
Primary input is `CandidateExternalGrammarSet`. New minimal immutable support records are `RepresentationGrammarSourceMaterialRef`, `AttributedGrammarClaim`, `RepresentationGrammarComparison`, `LexicalSupportReference`, and `CandidateRecoveryMaterial`.

## 4. Output artifact
`RepresentationGrammarRecoveryProjection` preserves recovered grammar records plus unsupported, Unknown, and conflict outcomes for every candidate.

## 5. Candidate-versus-recovered distinction
A candidate grammar remains a structural hypothesis. A recovered grammar is a Seed-owned projection that a bounded fragment is supported within an explicit applicability boundary.

## 6. Attributed-claim treatment
Attributed claims are preserved as support material references only. A claim alone produces `unknown` rather than recovery.

## 7. Structural-support treatment
Structural or behavioral support is represented through explicit `RepresentationGrammarComparison` records; mechanical projection references do not themselves prove grammar interpretation.

## 8. Comparison treatment
Comparisons preserve candidate reference, material reference, expected/observed structure, dimensions, result, reason, provenance, and Unknowns. Results distinguish `supports`, `contradicts`, `unknown`, and `conflict`.

## 9. Lexical-support treatment
Lexical support is referenced separately through `LexicalSupportReference`; recovered grammar does not own dictionaries or general semantic competency.

## 10. Recovery-state model
Candidate outcomes use `recovered`, `unsupported`, `unknown`, and `conflict`.

## 11. Recovered treatment
Recovery requires bounded positive comparison support, explicit supported structures, an applicability boundary, and no defeating contradiction or unresolved required lexical role.

## 12. Unsupported treatment
Unsupported requires bounded positive counterevidence; absence of support is not unsupported.

## 13. Unknown treatment
Unknown preserves insufficient material, missing structural comparison, unclear boundary, missing lexical support, alternatives, incomplete source material, or other Unknowns.

## 14. Conflict treatment
Conflict preserves incompatible bounded findings and is not resolved by source order, source count, candidate order, lexical ordering, prestige, or last-write-wins.

## 15. Applicability boundary
Every recovered grammar carries explicit boundary strings such as exact material class, sentence form, language/convention, supported forms, exclusions, and ambiguity limits.

## 16. Supported structures
Recovered records preserve supported structure labels from the bounded material.

## 17. Excluded structures
Recovered records preserve excluded structures as outside boundary, not automatic contradictions.

## 18. Grammar identity
Recovered grammar IDs are deterministic SHA-256 IDs over candidate identity, representation, fragment, dialect, source material identities/hashes, support/contradiction comparisons, supported/excluded structures, boundary, lexical references, Unknowns, conflicts, and recovery convention.

## 19. Projection identity
Projection IDs are deterministic SHA-256 IDs over candidate set, supplied materials, claims, comparisons, lexical references, outcomes, recovered grammars, and convention.

## 20. Candidate preservation
Every candidate receives an outcome and non-recovered candidates are not discarded.

## 21. Zero-candidate behavior
An empty candidate set produces a valid empty projection with Unknown `no candidate representation grammar`; it does not conclude material has no grammar.

## 22. Unresolved alternatives
Alternative references from candidate records are preserved on outcomes and the projection.

## 23. Grammar-refinement treatment
The implementation permits an explicit recovered `bounded_fragment` and optional `refinement_reason` only when supplied in `CandidateRecoveryMaterial`; it does not silently rewrite candidates after contradiction.

## 24. English before-support result
The English candidate with exact sentence and attributed claim but no adequate structural comparison or lexical role support remains `unknown`.

## 25. English after-support result
With explicit subject span, predicate span, sentence-order comparison, noun support for `dog`, and finite-verb support for `runs`, the simple declarative subject-predicate fragment is recovered within a narrow boundary.

## 26. English counterexample result
The overbroad candidate “every sentence begins with an explicit noun subject” is `unsupported` for `Run.` when a bounded comparison contradicts it.

## 27. Lexical-Unknown result
When required lexical roles are missing, the candidate remains `unknown`.

## 28. Bash comparison result
The Bash `echo` + one literal argument fragment can be recovered as representation grammar, with pipelines, redirection, substitution, expansion, functions, and general scripting excluded.

## 29. Mechanism-neutrality result
Recovered representation grammars contain no `mechanism_id`, provider, tool, invocation arguments, selected realization, or execution request. `/bin/bash` behavior may be referenced by comparison material without owning the grammar.

## 30. Future grammar-to-realization handoff
A narrow `FutureRepresentationGrammarBindingHandoff` exposes recovery projection ID, recovered grammar IDs, source refs, representation identities, boundaries, lexical refs, Unknowns, and conflicts only.

## 31. Legacy `RecoveredInvocationGrammar` treatment
`RecoveredInvocationGrammar` was not renamed, removed, migrated, or reinterpreted. Candidate operational realization fixtures remain unchanged.

## 32. Manual responsibility eliminated
Before, campaign authors manually read candidate hypotheses and supporting material and wrote usable fragments into invocation-named artifacts. After, Seed preserves candidate hypotheses, projects recovered/unsupported/Unknown/conflict outcomes, preserves boundaries and exclusions, and leaves mechanism binding to the next owner.

## 33. Read-only guarantees
Recovery projection and recovered grammars set `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`. The producer does not mutate State, cluster, event ledger, source artifacts, candidate sets, structural projections, lexical material, registries, catalogs, invocation contracts, operational realizations, reachability projections, observations, evidence, or facts.

## 34. Boundary notes
Boundary notes explicitly preserve candidate hypotheses, claim insufficiency, mechanism neutrality, bounded applicability, lexical separation, exclusions as outside scope, no global language competency, no mechanism/invocation/operational binding, and no capability reachability.

## 35. Compatibility answer
No. This slice did not change any existing compatibility boundary.

## 36. Files changed
- `seed_runtime/representation_grammar_recovery.py`
- `seed_runtime/__init__.py`
- `tests/test_representation_grammar_recovery.py`
- `recovered_representation_grammar_slice_001.md`

## 37. LOC delta
Recorded in `git diff --stat` before commit.

## 38. Tests executed
- `pytest -q tests/test_representation_grammar_recovery.py`
- `pytest -q tests/test_candidate_external_grammar.py tests/test_external_material_structural_projection.py tests/test_external_material_surface_feature_projection.py tests/test_candidate_operational_realization.py tests/test_capability_reachability_projection.py`
- `git diff --check`

## 39. Baseline failures
No unrelated baseline failures were observed in the executed checks.

## 40. Remaining roads
- `RecoveredRepresentationGrammar -> representation-grammar-to-mechanism applicability -> CandidateOperationalRealization`
- `CandidateOperationalRealizationSet -> CapabilityReachabilityProjection`
- `CapabilityReachabilityProjection -> OperationalRealizationSelection`
- `selected realization -> invocation request -> validation -> authorization -> execution`

## 41. Exact next bounded question
Given one mechanism-neutral `RecoveredRepresentationGrammar`, one exact `OperationalRealizationHandoff`, and one or more mechanism invocation contracts, what smallest owner may project whether a mechanism can lawfully apply that grammar to the exact demanded material without selecting the realization, projecting final capability reachability, authorizing, or executing it?
