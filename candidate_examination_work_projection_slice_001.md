# Candidate Examination Work Projection Slice 001

## 1. Recovered responsibility

This slice recovers exactly one responsibility: mechanically enumerate bounded candidate examination work from explicit corpus members, known representation visibility, and visible capability/projection contracts. It does not select, prioritize, authorize, schedule, execute, compare, or semantically interpret work.

## 2. Producer

The producer is `project_candidate_examination_work` in `seed_runtime/candidate_examination_work.py`.

## 3. Input artifacts

Inputs are explicit `BoundedCorpusMember` records with `RepresentationVisibility` records and explicit `ExaminationWorkContract` records. The structural and surface-feature roads are implementation-backed by existing external-material projection modules. The website acquisition/orientation road remains caller-supplied contract visibility for this slice.

## 4. Output artifact

The output artifact is immutable `CandidateExaminationWorkSet`, carrying deterministic candidate records, bounded exclusions, set unknowns, boundary notes, `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`.

## 5. Direct consumer

The direct consumer is the existing `ExaminationFrontier` through the narrow `CandidateExaminationWorkSet.to_frontier_candidate_work()` adapter. The adapter supplies candidate identities and compatibility testimony without moving classification ownership.

## 6. Corpus-input boundary

The producer consumes only caller-supplied corpus members. It does not discover members, crawl websites, read repository files, acquire material, or inspect arbitrary files.

## 7. Representation-visibility boundary

Representation visibility is explicit and typed. The producer checks representation kind and evidence status only; it does not derive new text, structure, features, facts, observations, or evidence.

## 8. Contract-visibility boundary

Every emitted candidate is grounded in an explicit `ExaminationWorkContract`. Free-form work names are ignored and cannot create candidate work. No universal capability ontology was introduced.

## 9. Candidate identity rule

`candidate_work_id` is a SHA-256 identity over `corpus_id`, `corpus_member_id`, artifact identity/hash, contract identity, capability identity, accepted input representation, produced output representation, and contract convention/version.

## 10. Compatibility observations

The producer preserves candidate-generation observations: `compatible`, `missing_required_representation`, `capability_unavailable`, `contract_unknown`, and `representation_unknown`. These are not frontier classifications.

## 11. Missing-prerequisite behavior

A missing required input representation is emitted as candidate work with `compatibility_observation=missing_required_representation` and the unmet representation in `missing_prerequisites`. It is not called blocked.

## 12. Unavailable-versus-incompatible distinction

Unavailable capability is preserved as `capability_unavailable`. Incompatible representation is not conflated with unavailable capability. Missing representation remains distinct from unsupported capability.

## 13. Exclusion/non-emission rule

The implementation emits only records grounded in visible contracts. Bounded exclusions are available for non-emitted incompatible pairs; arbitrary caller work names do not emit records.

## 14. Deterministic ordering

Contracts are processed by contract identity; output records are sorted by corpus member, contract, and candidate identity.

## 15. Frontier adapter/handoff

`CandidateExaminationWorkRecord.to_frontier_candidate_work()` constructs existing `CandidateWork` inputs. Non-compatible candidate-generation observations become frontier unknown testimony; the frontier remains the only classifier.

## 16. Mixed-corpus proving results

The mixed-corpus test uses one Project Gutenberg target member, one selected lesson member, and one `AGENTS.md` repository member with explicit representations and visible contracts.

## 17. Website-oriented candidate result

Seed derives one website target candidate only from caller-supplied acquisition/orientation contract visibility and an explicit `acquisition_target` representation. It does not claim live Project Gutenberg bytes exist and does not classify environment failure as blocked.

## 18. Selected lesson candidate results

Seed derives selected lesson structural work from exact text representation plus the structural projection contract, and selected lesson surface-feature work from structural projection representation plus the surface-feature projection contract. The selected lesson hash used by the test is `01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963`.

## 19. Repository candidate results

Seed derives `AGENTS.md` structural and surface-feature candidates through the same neutral representation/contract matching used for the selected lesson. It does not infer Markdown, instruction, module, class, semantic role, or authority.

## 20. Prose interpretation decision

No prose-interpretation candidate is invented. No canonical visible prose-interpretation contract was introduced by this slice.

## 21. Comparison decision

No comparison candidate is invented. A future comparator report is not treated as a registered artifact-to-capability contract.

## 22. Campaign-author supplied inputs

The campaign author now supplies bounded corpus membership, known representation visibility, and narrow contract visibility not already canonical. For the mixed-corpus proof, website acquisition/orientation contract visibility remains caller-supplied.

## 23. Seed-derived candidates

Seed derives candidate identity, representation matching, missing-prerequisite visibility, availability observations, deterministic ordering, the immutable work set, and the frontier-compatible handoff.

## 24. Manual handoff eliminated

The campaign author no longer writes structural, surface-feature, website acquisition, prose, or comparison work items manually for this slice. Seed emits only the candidates grounded in visible contracts, and omits prose/comparison candidates absent canonical contracts.

## 25. Boundary notes

Human and JSON renderers preserve the boundary notes: candidate work is derived from explicit corpus membership, known representations, and visible contracts; a candidate is not selected, eligible, authorized, scheduled, or executed; contract compatibility is not capability sufficiency; missing prerequisites are not blockers; unavailable capability is distinct from incompatible representation; no semantic interpretation, comparison, recurrence, priority, or campaign planning occurs; and the artifact is not runtime Evidence or Fact.

## 26. Read-only guarantees

The producer and renderer are read-only: `read_only=true`, `writes_event_ledger=false`, and `mutates_cluster=false`. Tests check that projection/rendering do not alter repository status and do not create event-ledger, pending-action, runtime fact, evidence, or observation identifiers.

## 27. Compatibility answer

Did this slice change any existing compatibility boundary?

No.

## 28. Files changed

- `seed_runtime/candidate_examination_work.py`
- `tests/test_candidate_examination_work.py`
- `candidate_examination_work_projection_slice_001.md`

## 29. LOC delta

The final LOC delta is reported by `git diff --stat` and `git diff --numstat` before commit.

## 30. Tests executed

- `pytest -q tests/test_candidate_examination_work.py`
- `pytest -q tests/test_candidate_examination_work.py tests/test_examination_frontier.py tests/test_external_material_structural_projection.py tests/test_external_material_surface_feature_projection.py`

## 31. Exact next bounded question

Given an immutable `ExaminationFrontier` whose candidate work was derived by Seed rather than manually written by the campaign author, what smallest existing or missing owner may select one eligible item for a bounded probe request while preserving the inquiry, selection reason, authorization boundary, and all non-selected alternatives?

## 32. Remaining missing roads

Remaining missing roads are canonical prose-interpretation contract visibility, canonical structural-comparison contract visibility, and any future selector owner for one eligible frontier item. None are implemented in this slice.
