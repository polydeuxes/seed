# Candidate Operational Realization Projection Slice 001

1. **Recovered responsibility**: for one exact `OperationalRealizationHandoff`, Seed composes supplied mechanism, claim, contract, grammar, behavior, dependency, authority, representation, and method material into bounded candidate operational realizations without selecting, authorizing, executing, or projecting final capability reachability.
2. **Producer**: `project_candidate_operational_realizations(...)`.
3. **Input artifacts**: `OperationalRealizationHandoff`, `MechanismObservation`, `AttributedMechanismClaim`, `InvocationContract`, `RecoveredInvocationGrammar`, `BehavioralObservation`, `BehaviorComparison`, and optional `OperationalRealizationBasis` records.
4. **Output artifact**: immutable `CandidateOperationalRealizationSet` with candidate partitions, no-known-realization observations, boundary notes, provenance, unknowns, conflicts, and read-only flags.
5. **Vocabulary correction**: operational material is named by responsibility. Attributed assertions are claims; observations, grammar projections, behavior comparisons, and candidate projections are not called testimony.
6. **Candidate identity**: deterministic hash over probe request, capability demand, mechanism/version, invocation contract, recovered grammar, representation binding, method reference, basis, comparison identifiers, standing, and projection convention.
7. **Candidate-set identity**: deterministic hash over probe request, capability demand, ordered candidate identifiers, and projection convention.
8. **Mechanism-observation treatment**: observations preserve mechanism identity, kind, observed value, version, provenance, and unknowns; existence alone does not establish reachability.
9. **Attributed-claim treatment**: claims preserve source, mechanism, claim reference, attribution, provenance, unknowns, and contradictions; claims are not observations.
10. **Invocation-contract treatment**: contracts preserve accepted input, produced output, argument grammar, result grammar, convention, provenance, and unknowns; declared grammar alone is only declared.
11. **Recovered-grammar treatment**: recovered grammar preserves source material, bounded fragment, supported structures, excluded structures, unknowns, and conflicts; it is not global competency.
12. **Behavioral-observation treatment**: behavioral observations preserve exact invocation input and result channels without embedding expected behavior.
13. **Behavior-comparison treatment**: comparisons preserve reference, observation, dimensions, result, reason, provenance, and unknowns without generalizing beyond the bounded comparison.
14. **Operational-realization basis**: optional immutable basis records collect source references and standings while remaining separate from candidate projection and reachability conclusion.
15. **Representation compatibility**: projected explicitly as compatible, incompatible, unknown, or conflict.
16. **Methodological compatibility**: projected explicitly as satisfies, violates, cannot establish, or conflicts with.
17. **Dependency treatment**: dependency standing is separate from mechanism availability and authority standing.
18. **Authority treatment**: authority standing is reachable, unavailable, unknown, or conflict and is not policy authorization.
19. **Candidate-standing model**: candidates are supported, unsupported, unknown, or conflict, with orthogonal reasons such as mechanism unavailable, grammar insufficient, behavior contradicted, representation incompatible, methodologically incompatible, dependency blocked, or authority blocked.
20. **Zero-candidate behavior**: an empty set records `no known realization` and does not conclude impossibility.
21. **Candidate preservation**: supported, unsupported, unknown, conflicting, incompatible, blocked, and contradicted candidates are preserved without ranking or selection.
22. **Bash before-crawl result**: `/bin/bash` existence/version plus opaque process contract can support only that narrow opaque process-invocation candidate; literal Bash expression construction remains unknown/grammar insufficient.
23. **Bash after-crawl result**: the same `/bin/bash` mechanism/version gains a candidate supported by the bounded recovered `echo hello` grammar and supporting behavior comparison.
24. **Bounded Bash competency**: only the validated literal fragment is supported; pipelines, redirection, command substitution, and general scripting remain excluded/unknown.
25. **Internal-producer result**: an internal deterministic producer is represented through the same mechanism/contract/grammar/behavior candidate shape without a registry requirement.
26. **Legacy-adapter treatment**: legacy catalog/spec material may contribute as attributed claims or contracts but does not own the projection.
27. **Future reachability handoff**: `FutureCapabilityReachabilityHandoff` exposes candidate-set identity, demand, candidate references, standings, dependency/authority observations, unknowns, and conflicts only.
28. **Caller-supplied inputs**: the producer accepts explicit immutable input tuples and does not fetch, mutate, or promote them into runtime Evidence or Fact.
29. **Seed-owned projection responsibility**: Seed now owns candidate-realization projection for an exact handoff.
30. **Manual responsibility eliminated**: campaign authors no longer manually correlate observations, claims, contracts, grammar, behavior, dependencies, authority, representations, and method constraints to decide possible realizations.
31. **Read-only guarantees**: projection and rendering are read-only, write no event ledger, do not mutate cluster/state, do not create invocation requests or arguments, do not authorize, do not execute, and do not mark work complete.
32. **Boundary notes**: the artifact states that it is not overall reachability, mechanism existence is insufficient, declared grammar is not validated competency, behavioral support is bounded, authority differs from policy authorization, candidates are unranked/unselected, no known realization is not impossibility, and no tool/provider/toolkit/registered-operation concept is required.
33. **Compatibility answer**: No. This slice did not change an existing compatibility boundary.
34. **Files changed**: `seed_runtime/candidate_operational_realization.py`, `seed_runtime/__init__.py`, `tests/test_candidate_operational_realization.py`, and this report.
35. **LOC delta**: recorded by `git diff --stat` and `git diff --numstat` before commit.
36. **Tests executed**: focused candidate-operational-realization tests and requested compatibility test groups listed in the final response.
37. **Baseline failures**: none observed in the executed test groups unless noted in final response.
38. **Remaining roads**: `CandidateOperationalRealizationSet → CapabilityReachabilityProjection`; `CapabilityReachabilityProjection → OperationalRealizationSelection`; selected realization to invocation request; invocation request to validation, authorization, execution.
39. **Exact next bounded question**: Given one `CandidateOperationalRealizationSet` for an exact capability demand, what smallest owner may project whether that bounded transformation is reachable, partially reachable, blocked, unsupported, conflicting, or Unknown without selecting a realization or authorizing execution?
