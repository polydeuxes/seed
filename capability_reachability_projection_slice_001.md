# Capability Reachability Projection Slice 001

1. **Recovered responsibility**: Seed now projects demand-level reachability for one exact bounded transformation from an already-produced candidate-realization set, without selecting, authorizing, invoking, executing, or reopening raw operational material.
2. **Producer**: `project_capability_reachability(...)`.
3. **Input artifacts**: `CandidateOperationalRealizationSet` and its matching `FutureCapabilityReachabilityHandoff`.
4. **Output artifact**: immutable `CapabilityReachabilityProjection` plus a narrow read-only `FutureOperationalRealizationSelectionHandoff` only for reachable or blocked downstream explanation/selection paths.
5. **Reachability identity**: deterministic over probe request identity, capability demand identity, candidate-set identity, future handoff content, candidate records and standings, blockers, Unknowns, conflicts, state, reason, and projection convention.
6. **Reachability-state model**: `reachable`, `blocked`, `unsupported`, `unknown`, and `conflict`.
7. **Capability-demand binding**: the producer validates that candidate set and handoff preserve the same exact probe request and capability-demand identity.
8. **Candidate aggregation**: the producer partitions supporting, blocked, unsupported, Unknown, and conflicting candidate references without ranking or selecting them.
9. **Reachable treatment**: `reachable` requires at least one full-demand supported candidate with available mechanism/dependencies and reachable authority.
10. **Blocked treatment**: `blocked` preserves otherwise sufficient candidates blocked by dependency, authority, or mechanism availability.
11. **Unsupported treatment**: `unsupported` requires known bounded candidates to positively fail required demand dimensions.
12. **Unknown treatment**: `unknown` covers no known realization, incomplete candidate space, insufficient grammar/behavior evidence, representation Unknown, method cannot-establish, dependency Unknown, authority Unknown, and other insufficiency.
13. **Conflict treatment**: `conflict` preserves unresolved candidate or set conflicts and does not resolve by ordering, count, or apparent strength.
14. **Candidate-space completeness**: the producer does not invent completeness; explicit `candidate_space_incomplete` or `candidate_space_unknown` Unknowns prevent unsupported overclaiming.
15. **Mechanical reachability**: aggregated separately as a typed orthogonal dimension.
16. **Dependency reachability**: aggregated separately and preserved through dependency blocker references.
17. **Authority reachability**: aggregated separately and preserved through authority blocker references.
18. **Policy-authorization exclusion**: policy authorization is not evaluated, and authority unavailable is not rendered as unauthorized or denied.
19. **Representation treatment**: incompatible representation contributes positive unsupported evidence; Unknown representation remains Unknown.
20. **Methodological treatment**: method violations contribute positive unsupported evidence; cannot-establish remains Unknown.
21. **Grammar treatment**: sufficient behaviorally supported grammar may contribute to reachability; unknown/declared-only/recovered-only/insufficient grammar remains insufficient for full reachability where behavior is required.
22. **Behavioral treatment**: supported behavior can contribute to reachability; contradicted behavior contributes positive unsupported evidence; missing behavior remains Unknown where required.
23. **No-known-realization behavior**: zero candidates produce `unknown` with `no known realization`, not unsupported or impossible.
24. **Multiple-supported-candidate behavior**: multiple supported candidates establish reachability while preserving all supporting references and no preference.
25. **Bash before-crawl result**: literal-output demand remains `unknown` when the candidate set only shows mechanism existence and insufficient literal-command evidence.
26. **Bash after-crawl result**: bounded literal-output demand becomes `reachable` when candidate evidence includes bounded grammar, behavior, representation, method, dependency, and authority support.
27. **Bounded Bash competency**: unexamined Bash grammar such as pipelines, redirection, command substitution, and general scripting remains outside the projection.
28. **Internal-producer result**: an internal deterministic producer candidate can support reachability without tool-registry or provider membership.
29. **Future selection handoff**: the handoff preserves projection/candidate-set/demand identity, state, candidate partitions, and reason; it does not select, authorize, construct arguments, or execute.
30. **Caller-supplied inputs**: callers supply candidate set and matching future handoff only; raw observations, claims, contracts, recovered grammar, and behavior records are not re-supplied.
31. **Seed-owned projection responsibility**: Seed owns deterministic validation and aggregation from candidate standings to demand-level reachability.
32. **Manual responsibility eliminated**: campaign authors no longer manually inspect every projected candidate to decide reachability, blocked, unsupported, Unknown, or conflict for this bounded question.
33. **Read-only guarantees**: projection and rendering preserve `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.
34. **Boundary notes**: the artifact records capability-as-reachability, candidate-consumption only, no selection, mechanical/dependency/authority/policy separation, no-known-realization semantics, unsupported evidence requirements, no preference among multiple candidates, no pending/execution side effects, and no required tool/provider/registry concept.
35. **Compatibility answer**: No. This slice did not change any existing compatibility boundary.
36. **Files changed**: `seed_runtime/capability_reachability_projection.py`, `seed_runtime/__init__.py`, `tests/test_capability_reachability_projection.py`, and this report.
37. **LOC delta**: see `git diff --stat` and `git diff --numstat` from the slice verification.
38. **Tests executed**: focused capability-reachability tests, candidate-operational-realization compatibility tests, probe-request tests, capability inventory/single-capability projection tests, and authority/policy/pending/execution-adjacent tests listed below.
39. **Baseline failures**: none observed in the executed checks.
40. **Remaining roads**: `CapabilityReachabilityProjection -> OperationalRealizationSelection`; selected realization to bounded invocation request; invocation request to validation, authorization, and execution; execution result to attributed result artifact, examination, and admission.
41. **Exact next bounded question**: Given one `CapabilityReachabilityProjection` establishing that an exact bounded transformation is reachable through one or more supported candidates, what smallest owner may select zero or one operational realization under an explicit selection policy without constructing an invocation request, authorizing, or executing it?
