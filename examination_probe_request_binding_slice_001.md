# Examination Probe Request Binding Slice 001

1. **Recovered responsibility**: bind exactly one selected examination-work item to its exact material, candidate-work record, work contract, requested representation change, method constraints, selection reason, provenance, Unknowns, and read-only boundary notes as an immutable requested probe.
2. **Producer**: `bind_examination_probe_request(...)`.
3. **Input artifacts**: `ExaminationWorkSelection`, `FutureProbeRequestHandoff`, `ExaminationFrontier`, `CandidateExaminationWorkSet`, and `ExaminationMethodApplicabilityProjection`.
4. **Output artifact**: `ExaminationProbeRequest`, plus a narrow `OperationalRealizationHandoff` emitted only from a bound request.
5. **Request identity**: deterministic over inquiry identity, selection identity, selected work identity, candidate-work identity, work-contract identity, artifact identity/hash, method-applicability projection identity, and `examination_probe_request_v1`.
6. **Request-state model**: implementation constructs only `bound`; absent, incompatible, Unknown, inapplicable, or conflicting upstream material fails deterministically with `ExaminationProbeRequestError` rather than silently repairing. The typed vocabulary is documented as `bound`, `unknown`, `conflict`, and `invalid`.
7. **Artifact and version binding**: candidate, frontier, and method records must preserve the same artifact identity and hash/version.
8. **Candidate-work binding**: the selected frontier work must reference an existing candidate-work record, and identities must match.
9. **Work-contract binding**: contract identity, capability, work kind, input representation, output representation, and convention remain candidate-work owned and are copied into the request.
10. **Requested outcome**: derived from the contract as producing the contract-declared output representation from the contract-declared input representation for the exact artifact version.
11. **Representation binding**: input and output representations are preserved from the selected candidate work contract, not inferred from tools.
12. **Selection-reason preservation**: the `FutureProbeRequestHandoff.selection_reason` is copied unchanged.
13. **Fidelity treatment**: fidelity constraints are preserved exactly from the applicable method record.
14. **Attribution treatment**: attribution constraints are preserved exactly from the applicable method record, including provider-attribution requirements without provider selection.
15. **Claim-treatment constraints**: claim-treatment constraints are preserved exactly and remain request constraints, including no Evidence/Fact promotion when present.
16. **Method-applicability relationship**: the request requires one applicable method record for the selected candidate and rejects Unknown, inapplicable, conflict, or mismatched method records.
17. **No-realization behavior**: no provider, registered operation, operation arguments, credentials, authorization, schedule, execution proposal, or pending action are selected or required.
18. **Operational-realization handoff**: `to_operational_realization_handoff()` exposes only request id, inquiry, artifact identity/hash, work contract, capability, representations, method-constraint reference, and read-only flags.
19. **Mechanical structural proving result**: focused tests bind structural projection work and preserve exact artifact version, structural contract, exact-text input, structural output, fidelity constraints, and selection reason.
20. **Surface-feature proving result**: focused tests bind a surface-feature work item and preserve structural-projection input with surface-feature output.
21. **External-method decision**: no external-grammar candidate was invented; the slice only preserves external-style attribution/claim constraints when attached to canonical method records.
22. **Mismatch behavior**: mismatched selection, handoff, frontier, candidate, artifact version, contract/capability/convention, or method record fails deterministically.
23. **No-selection behavior**: zero selected work and multi/conflict-like selected states cannot produce a request or handoff.
24. **Caller-supplied inputs**: callers provide existing upstream artifacts; they do not restate already preserved material.
25. **Seed-owned binding responsibility**: Seed now validates upstream identities and binds selected work to exact material and constraints.
26. **Manual handoff eliminated**: campaign authors no longer manually chase selected work, artifact/version, contract, requested representation change, method constraints, selection reason, and provenance.
27. **Read-only guarantees**: `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`; binding/rendering do not mutate upstream artifacts, state, registry, ledger, or cluster.
28. **Boundary notes**: human and JSON output preserve notes that the artifact is a requested probe, not an operational realization, registered operation, authorization, pending action, Evidence, or Fact.
29. **Compatibility answer**: No.
30. **Files changed**: `seed_runtime/examination_probe_request.py`, `tests/test_examination_probe_request.py`, and `examination_probe_request_binding_slice_001.md`.
31. **LOC delta**: see `git diff --stat` / `git diff --numstat` before commit.
32. **Tests executed**: focused probe-request tests and adjacent compatibility tests listed in the final response.
33. **Remaining missing roads**: `ExaminationProbeRequest -> candidate operational realizations`; candidate realizations -> selected realization or insufficiency; selected realization -> `ExecutionProposal`; proposal -> validation -> policy authorization -> execution; execution result -> recording -> frontier revision.
34. **Exact next bounded question**: Given one bound `ExaminationProbeRequest`, what existing owner—or smallest missing owner—may project zero or more candidate operational realizations by matching its capability, representations, and constraints to available providers and registered operations without selecting, authorizing, or executing one?
