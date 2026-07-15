# Representation Grammar Applicability Slice 001

1. **Recovered responsibility:** Seed now owns a bounded representation-grammar applicability projection that answers whether one recovered, mechanism-neutral representation grammar can lawfully apply through one mechanism and invocation contract for one exact operational demand.
2. **Producer:** `project_representation_grammar_applicability(...)` produces an immutable `RepresentationGrammarApplicabilityProjection`.
3. **Input artifacts:** The producer consumes a `RepresentationGrammarRecoveryProjection`, one `RecoveredRepresentationGrammar`, one `OperationalRealizationHandoff`, one mechanism reference, one `InvocationContract`, and one caller-supplied `ApplicabilityDemandMaterial` record preserving exact material, boundaries, lexical references, fidelity, attribution, claim treatment, known loss, provenance, Unknowns, and conflicts.
4. **Output artifact:** `RepresentationGrammarApplicabilityProjection` preserves deterministic identity, exact demand binding, grammar, mechanism, contract, compatibility dimensions, state, reason, support references, provenance, Unknowns, conflicts, boundary notes, and read-only guarantees.
5. **Future candidate-realization handoff:** `FutureCandidateOperationalRealizationHandoff` is emitted only when `applicability_state == applicable` and carries only references needed by future candidate realization.
6. **Applicability-state model:** The state model is `applicable`, `not_applicable`, `unknown`, and `conflict`.
7. **Exact demand binding:** The projection binds probe request, operational-realization handoff, capability demand, source representation, target representation, material class, grammar, mechanism, contract, and convention.
8. **Grammar ownership:** The recovered representation grammar remains mechanism-neutral; the mechanism may apply it but does not own it.
9. **Mechanism treatment:** Mechanism identity is a reference for this exact applicability question and does not prove existence, availability, reachability, authority, selection, warrant, or execution.
10. **Invocation-contract treatment:** The invocation contract contributes accepted and produced representation compatibility but does not become the representation grammar and does not prove full grammar application by itself.
11. **Source-representation treatment:** Source representation compatibility is checked between the recovered grammar, exact demand material, handoff, and contract.
12. **Target-representation treatment:** Required target/result representation compatibility is checked between demand, handoff, and produced contract representation.
13. **Lexical-support treatment:** Lexical support remains separate from grammar structure; unresolved required lexical bindings project `unknown` rather than structural contradiction.
14. **Applicability-boundary treatment:** The exact demand must remain inside the recovered grammar applicability boundary; explicitly excluded structures project `not_applicable`.
15. **Fidelity treatment:** Known loss that defeats required fidelity projects non-applicability for this application, not invalid grammar recovery.
16. **Attribution treatment:** Attribution constraints are preserved as applicability dimensions and references.
17. **Claim-treatment treatment:** Claim-treatment constraints are preserved as applicability dimensions and references.
18. **Known-loss treatment:** Known limitations and demand known-loss references remain traceable and participate in deterministic identity.
19. **Applicable treatment:** Applicable means only the grammar/demand/mechanism/contract relationship is bounded-compatible and emits a narrow future candidate-realization handoff.
20. **Not-applicable treatment:** Not applicable is used only for positive incompatibility, such as excluded structures or representation/contract mismatch.
21. **Unknown treatment:** Unknown is used for missing or unresolved applicability support, including unsupported but not excluded structures or unresolved lexical bindings.
22. **Conflict treatment:** Conflict preserves incompatible evidence without resolving it by source order, count, registry precedence, familiarity, or latest write.
23. **Deterministic identity:** Projection identity hashes stable semantic inputs, sorted references, state, reason, Unknowns, conflicts, convention, grammar, recovery, demand, handoff, mechanism, and contract.
24. **Candidate-grammar rejection:** Candidate grammar hypotheses cannot enter the positive realization road; only recovered grammars belonging to the recovery projection are accepted.
25. **English simple-declarative result:** The simple declarative English fixture projects `applicable` for explicit subject and simple predicate.
26. **English boundary-failure result:** Subordinate-clause/imperative boundaries remain `not_applicable` or `unknown` without broadening the grammar.
27. **English lexical-unknown result:** A structurally applicable sentence with unresolved lexical binding projects `unknown`.
28. **English counterexample result:** `Run.` remains outside the explicit-subject declarative grammar; the projection does not universalize all English sentences.
29. **Bash literal result:** A bounded literal Bash representation fixture projects `applicable` without constructing command text or invoking `/bin/bash`.
30. **Bash excluded-structure result:** Pipelines remain excluded and project `not_applicable` even though Bash may generally execute them.
31. **Bash unknown-structure result:** Unrecovered, non-excluded Bash structures project `unknown` rather than impossibility.
32. **One-grammar/multiple-mechanisms result:** One recovered grammar can produce independent applicable projections for multiple mechanisms/contracts without ranking or selecting.
33. **One-mechanism/multiple-grammars result:** One mechanism can participate in multiple independently identified grammar applicability projections without owning either grammar.
34. **Contract-mismatch result:** Contract representation mismatch blocks this grammar/mechanism/contract application without invalidating grammar recovery.
35. **Mechanism-availability distinction:** Current availability remains outside representation-grammar applicability and is preserved for candidate realization/reachability.
36. **Internal-producer result:** Internal deterministic producers use the same applicability artifact and need no registry, shell, process, provider, or tool boundary.
37. **Candidate-realization integration:** `project_candidate_operational_realizations(...)` now accepts `representation_grammar_applicability_handoffs` additively and preserves separate grammar, mechanism, and contract references.
38. **Legacy grammar compatibility:** `RecoveredInvocationGrammar` remains present and accepted; existing legacy fixtures remain green.
39. **Caller-supplied inputs:** Callers supply immutable recovered grammar, demand material, mechanism, and contract references; they do not reconstruct grammar from raw external material.
40. **Seed-owned applicability responsibility:** Seed now owns the bounded applicability decision rather than requiring campaign authors to manually bridge recovery and realization.
41. **Manual responsibility eliminated:** Manual transfer of recovered grammar into candidate realization and manual mechanism-ownership assumptions are eliminated for the new road.
42. **Read-only guarantees:** The projection and rendering are read-only, write no event ledger entries, mutate no cluster state, construct no material, invoke no mechanism, create no pending action, and execute nothing.
43. **Boundary notes:** Boundary notes explicitly preserve mechanism-neutral grammar, no broadening, no material construction, no reachability, no selection, no warrant, no authorization, no execution, and no registry requirement.
44. **Compatibility answer:** No. This slice did not change any existing compatibility boundary; the integration is additive and legacy inputs remain supported.
45. **Files changed:** `seed_runtime/representation_grammar_applicability.py`, `seed_runtime/candidate_operational_realization.py`, `tests/test_representation_grammar_applicability.py`, and this report.
46. **LOC delta:** Recorded by `git diff --stat` before commit.
47. **Tests executed:** Focused applicability tests, compatibility tests for recovery/candidate/reachability/selection/warrant, and full-suite baseline run were executed.
48. **Baseline failures:** Full suite still has 57 unrelated baseline failures concentrated in runtime decision routing, generated architecture stability, observation inventory/utilization, consumer dependency audit, Seed-local CLI, State patches, tool intent/recommendations/validation.
49. **Remaining roads:** `RepresentationGrammarApplicabilityProjection -> CandidateOperationalRealizationSet` remains narrow and incomplete beyond handoff consumption; warrant-to-translation, authorization, execution, result ingress, behavioral comparison, recording, and knowledge admission remain unresolved.
50. **Exact next bounded question:** Given one warranted selected realization for an exact bounded demand whose recovered representation grammar has been explicitly projected as applicable through the selected mechanism and invocation contract, what smallest owner may translate the Seed-native demanded meaning into the exact external representation accepted by that contract while preserving the applicability boundary, effect constraints, provenance, known loss, Unknowns, and conflicts without authorizing, emitting, or executing it?
