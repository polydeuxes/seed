# Representation Grammar / Invocation Grammar Topology Audit 001

## 1. Bounded question

Does the current candidate-operational-realization road preserve the grammar governing examined or produced material separately from the grammar used to invoke the mechanism applying it?

Audited road:

```text
ExaminationProbeRequest
→ OperationalRealizationHandoff
→ CandidateOperationalRealizationSet
→ CapabilityReachabilityProjection
```

Primary discriminating case: English prose subject/predicate projection. Comparison case: Bash literal-output projection.

## 2. Fixed distinctions

- **Representation grammar**: structure governing the material being interpreted, transformed, compared, or produced.
- **Invocation grammar**: bounded structure by which one realization mechanism is requested and returns a result.
- `representation grammar != invocation grammar`.
- `language competency != mechanism availability`.
- `recovered grammar != invocation contract`.
- `grammar application != grammar recovery`.
- `internal producer != grammar owner`.
- `mechanism accepts a grammar reference != mechanism owns that grammar`.
- `capability reachability != global language competency`.

## 3. Methodology

This was a read-only implementation-backed audit except for this report file. I used focused `rg` probes, then inspected implementation bodies and direct tests for the scoped artifacts. Classification is based on fields, construction logic, test fixtures, and consumers rather than symbol names alone.

Executed probes are listed in section 28.

## 4. Inspected owners

Scoped implementation artifacts inspected:

- `ExaminationProbeRequest` and `OperationalRealizationHandoff` in `seed_runtime/examination_probe_request.py`.
- `InvocationContract`, `RecoveredInvocationGrammar`, `OperationalRealizationBasis`, `CandidateOperationalRealization`, `CandidateOperationalRealizationSet`, and candidate projection logic in `seed_runtime/candidate_operational_realization.py`.
- `CapabilityReachabilityProjection` and its producer in `seed_runtime/capability_reachability_projection.py`.
- Candidate external grammar preservation in `seed_runtime/candidate_external_grammar.py`.
- External-material structural and surface-feature projection in `seed_runtime/external_material_structural_projection.py` and `seed_runtime/external_material_surface_feature_projection.py`.
- Candidate examination work contracts and records in `seed_runtime/candidate_examination_work.py`.
- Direct tests in `tests/test_candidate_operational_realization.py`, `tests/test_capability_reachability_projection.py`, `tests/test_candidate_external_grammar.py`, `tests/test_external_material_structural_projection.py`, `tests/test_external_material_surface_feature_projection.py`, and `tests/test_examination_probe_request.py`.
- Campaign fixtures for English grammar source material in `campaigns/graded_lessons_supervised_grammar_apprenticeship_campaign_001/campaign.py` and `selected_lesson_006.txt`.

## 5. Current grammar topology

### Current artifacts and what they describe

| Artifact / field | Preserved content | Material, invocation, or both? | Evidence |
|---|---|---|---|
| `CandidateExternalGrammarInputCandidate.structural_claim` | Caller-supplied structural grammar hypothesis | Material | Candidate external grammar boundary notes say candidate grammars are caller-supplied structural hypotheses and are not verified. |
| `CandidateExternalGrammarInputCandidate.supporting_testimony`, `contradicting_testimony` | Source-material references for claims | Material support | They preserve testimony relationships without evaluation. |
| `ExternalMaterialStructuralProjection` | Exact-text line and nonblank-region coordinates | Material projection | Boundary notes explicitly reject prose comprehension and grammar inference. |
| `ExternalMaterialSurfaceFeatureProjection` | Raw line/region length features | Material surface only | Boundary notes reject identifying prose, code, or grammar. |
| `ExaminationWorkContract.accepted_input_representation`, `produced_output_representation` | Work input/output representation names | Examination work contract; not mechanism invocation | Candidate work compatibility matches corpus representation kind to accepted input representation. |
| `ExaminationProbeRequest.required_input_representation`, `requested_output_representation` | Exact demand representation pair | Demand | Request binds selected examination meaning and contains no provider/tool/operation args. |
| `OperationalRealizationHandoff.required_input_representation`, `requested_output_representation` | Demand representation pair handed to realization projection | Demand | It is created from the bound probe request. |
| `InvocationContract.accepted_input_representation`, `produced_output_representation` | Mechanism contract input/output representation names | Mechanism invocation plus representation compatibility bridge | Candidate projection compares them to handoff representations. |
| `InvocationContract.argument_grammar`, `result_grammar` | Declared argument/result grammar for a mechanism contract | Both in current use | Bash tests put `echo literal` here, which is Bash material grammar, while `opaque bounded process invocation` is closer to process invocation. |
| `RecoveredInvocationGrammar.bounded_fragment`, `supported_structures`, `excluded_structures`, `source_material_refs` | Recovered bounded grammar fragment with source references | Material in fixtures; named as invocation | Bash fixture stores `echo hello`, `simple literal command`, exclusions, and source material refs here. |
| `OperationalRealizationBasis.invocation_contract_ref` | Contract reference | Invocation | It links basis to `InvocationContract`. |
| `OperationalRealizationBasis.recovered_grammar_ref` | Grammar reference | Ambiguous by type name; materially representation grammar in fixtures | It points to `RecoveredInvocationGrammar`, then candidate stores that reference. |
| `BehavioralObservation.exact_invocation_input` | Exact input to mechanism | Invocation sample carrying material | Bash fixture uses `echo hello`; internal producer fixture uses `hello`. |
| `BehaviorComparison.reference_id` | Comparison target | Either grammar or contract depending caller convention | Projection defaults to grammar id if present, otherwise contract id. |
| `CandidateOperationalRealization.recovered_grammar_reference` | Grammar reference on candidate | Ambiguous but separable from invocation contract reference | Candidate has both `invocation_contract_reference` and `recovered_grammar_reference`. |
| `CapabilityReachabilityProjection.grammar_sufficiency` | Summary from candidate grammar standing | Candidate standing only | Reachability consumes candidate projection, not raw grammar. |

## 6. `RecoveredInvocationGrammar` analysis

### Fields

`RecoveredInvocationGrammar` has:

- `grammar_id`
- `mechanism_id`
- `bounded_fragment`
- `convention`
- `supported_structures`
- `excluded_structures`
- `source_material_refs`
- provenance, unknowns, conflicts

The fields look like a recovered bounded grammar of material: fragment, supported structures, excluded structures, and source-material references. The `mechanism_id` field binds it to a mechanism, but does not prove that the grammar governs the mechanism-call boundary.

### Producer and inputs

There is no standalone producer that recovers this artifact from external grammar material. The candidate projection accepts `recovered_grammars` as caller-supplied input and groups them by `mechanism_id`.

### Consumers

`project_candidate_operational_realizations` consumes it by:

- grouping by `mechanism_id`;
- pairing every contract for a mechanism with every recovered grammar for that mechanism when explicit bases are absent;
- assigning `recovered_grammar_ref` into `OperationalRealizationBasis` and then into `CandidateOperationalRealization`;
- deriving `grammar_standing` from grammar presence and behavior comparison result.

`CapabilityReachabilityProjection` consumes only candidate standings and grammar standing summaries, not raw grammar contents.

### Classification

`RecoveredInvocationGrammar` currently represents:

```text
D. compressed ownership of both
```

with stronger concrete fixture evidence that it often preserves:

```text
B. recovered grammar of the material supplied to the mechanism
```

The first proving fixture is the Bash fixture in `tests/test_candidate_operational_realization.py`, where `RecoveredInvocationGrammar("grammar-echo-literal", "/bin/bash", "echo hello", supported_structures=("simple literal command",), excluded_structures=("pipelines", "redirection", "command substitution", "general scripting"), source_material_refs=("dungeon-artifact-1",))` describes the Bash program fragment, not the argv/stdin/environment/cwd contract used to invoke `/bin/bash`.

## 7. `InvocationContract` analysis

### Fields

`InvocationContract` has:

- `contract_id`
- `mechanism_id`
- `accepted_input_representation`
- `produced_output_representation`
- `argument_grammar`
- `result_grammar`
- `convention`
- provenance and unknowns

### What it owns today

`InvocationContract` owns a mechanism-bound contract identifier and accepted/produced representation compatibility. It also owns `argument_grammar` and `result_grammar`; those fields are currently capable of absorbing embedded material grammar.

In tests, two `/bin/bash` contracts are passed:

- `contract-process` with `argument_grammar="opaque bounded process invocation"`, closer to mechanism-call structure.
- `contract-bash-literal` with `argument_grammar="echo literal"`, a Bash language fragment carried in an invocation field.

### Answer

`InvocationContract` is not currently a pure mechanism-call contract. It partly owns mechanism-call structure, but the `argument_grammar` field currently absorbs grammar that can belong to the supplied material. This is most visible in the Bash fixture, where Bash program grammar is placed in the contract argument grammar.

## 8. External-grammar road trace

Trace observed:

```text
external grammar material
→ structural projection
→ candidate grammar
→ recovered bounded grammar
→ examination capability demand
→ candidate operational realization
```

### Preserved correctly

- External exact text is mechanically projected by `ExternalMaterialStructuralProjection`; line IDs, character ranges, artifact identity, artifact hash, encoding, and projection conventions are preserved. The artifact explicitly does not infer grammar.
- `CandidateExternalGrammarSet` preserves caller-supplied structural grammar hypotheses, testimony references, unresolved alternatives, and explicit unknowns without verifying them.

### Left unconnected

- There is no implementation-backed adapter from `CandidateExternalGrammarSet` or English lesson material to `RecoveredInvocationGrammar` or to a neutral recovered representation grammar artifact.
- There is no distinct `RecoveredRepresentationGrammar` artifact found in the scoped road.

### Renamed as invocation grammar

- The only recovered grammar input accepted by candidate operational realization is named `RecoveredInvocationGrammar`.
- If recovered English grammar were fed into the current road, the nearest available field would be `RecoveredInvocationGrammar.bounded_fragment` plus `supported_structures`, `excluded_structures`, and `source_material_refs`, thereby renaming representation grammar as invocation grammar.

### Copied into a mechanism-owned contract

- A second compression path exists through `InvocationContract.argument_grammar`, as shown by the Bash `echo literal` fixture.

### Exact first mismatch

The first missing/misplaced owner is the boundary between candidate external/recovered representation grammar and candidate operational realization: candidate realization has a separate `recovered_grammar_reference`, but the only concrete grammar artifact type it can reference is `RecoveredInvocationGrammar`, which is mechanism-bound and named/treated as invocation grammar.

## 9. English prose trace

### Before grammar recovery

Material:

```text
English sentence S
```

Mechanism:

```text
internal structural producer exists
```

Invocation contract:

```text
producer accepts exact text and projection inputs
```

Representation grammar:

```text
Unknown
```

Supported projection before recovery:

- Invoking an internal producer opaquely is possibly reachable if a mechanism contract and behavior observations exist.
- Correctly identifying subject/predicate is Unknown, because the road has no recovered bounded English grammar support for the exact sentence.
- Mechanism availability alone does not establish capability reachability.

### After bounded grammar recovery

Recovered grammar:

```text
simple declarative sentence fragment G
```

Support:

```text
examples, comparisons, lexical bindings, contradictions, limitations, Unknowns
```

Current road can preserve a candidate that says:

```text
producer M + contract C + recovered grammar reference R + behavior comparisons → candidate standing
```

But it cannot do so without distortion unless `R` is understood despite its type name as representation grammar. There is no explicit candidate-level statement that `M applies representation grammar G to sentence S`; there is only `recovered_grammar_reference`, linked to `RecoveredInvocationGrammar` and paired by `mechanism_id`.

Expected bounded reachability after recovery:

```text
subject/predicate projection within G → supportable/reachable if behavior comparison supports it
```

Everything outside G remains Unknown: idioms, ambiguous attachment, unexamined clause structures, unsupported lexical meanings, pragmatic implication, and general prose understanding.

## 10. Bash trace

Correct separation should be:

```text
mechanism: /bin/bash version V
invocation contract: bounded process invocation contract P
representation grammar: validated Bash literal-command grammar G
behavior: observations supporting G under V
demand: bounded literal-output transformation D
```

Current implementation partially supports this separation because a candidate has both `invocation_contract_reference` and `recovered_grammar_reference`. However, the Bash fixtures also merge the distinction in two places:

1. `InvocationContract.argument_grammar="echo literal"` stores Bash language grammar in a contract field.
2. `RecoveredInvocationGrammar` stores `echo hello` and Bash program structures under an invocation-grammar artifact name.

The Bash language grammar itself should not be classified as invocation grammar merely because the Bash program is carried through an invocation field. The current fixture can still express before/after Bash after correcting the distinction: keep `/bin/bash` and process contract as invocation, and carry `echo hello` / simple literal command grammar as representation grammar referenced by the candidate.

## 11. Internal-producer trace

Existing deterministic producer fixture:

```text
mechanism: internal:deterministic_literal_producer
contract: direct-producer-call-v1
representation grammar: grammar-direct-literal / literal input to literal output
```

Answers:

- Mechanism identity: `internal:deterministic_literal_producer`.
- Invocation contract: `InvocationContract("direct-producer-call-v1", "internal:deterministic_literal_producer", "text/plain", "text/plain", "direct producer-call contract")`.
- Representation grammar applied: literal input to literal output, stored as `RecoveredInvocationGrammar("grammar-direct-literal", ...)`.
- Can that grammar be replaced without replacing the producer? Shape permits multiple grammars per mechanism because grammars are grouped by mechanism and cross-paired with contracts when bases are absent.
- Can the same producer apply several grammar fragments? Shape permits it, but no semantic role field distinguishes grammar fragments as representation grammars.
- Does the producer require a registry entry? No; tests assert no registry/tool/provider fields are required.
- Does calling the producer directly erase the invocation-contract distinction? No; direct call is represented as a contract, but the grammar reference remains compressed/misnamed.
- Does the word `tool` appear anywhere necessarily? No. Boundary notes and tests explicitly exclude tool/provider/toolkit/registered-operation requirements.

## 12. Lexical-knowledge analysis

Dictionary and thesaurus material belongs to representation knowledge and grammar support when it is needed to apply a bounded English grammar fragment. It may also be an invocation input to an internal producer, but passing it to a producer does not make it invocation grammar.

Recommended ownership distinction for the audited topology:

- Lexical material as source/reference: representation knowledge.
- Lexical material as evidence supporting grammar recovery/application: grammar support.
- Lexical material as candidate-realization basis: basis reference proving the mechanism had the bounded inputs needed.
- Lexical material as function/process argument: invocation input, not invocation grammar.

Preserved distinctions:

```text
lexical knowledge != invocation grammar
grammar fragment != dictionary contents
lexical support != general semantic competency
```

Current implementation has no first-class lexical support reference in candidate realization. Lexical support could only be compressed into provenance, source material refs, unknowns, behavior comparison reason, or method constraints.

## 13. Behavioral-support analysis

Behavioral support for an internal English producer can include:

- expected structural projection from a bounded sentence;
- comparison with grammar-book examples;
- contradiction against counterexamples;
- stable deterministic producer output;
- exact source-span preservation;
- failure on material outside recovered grammar.

Current behavior artifacts:

- `BehavioralObservation` records exact invocation input, stdout, stderr, exit status, mechanism id, and version.
- `BehaviorComparison` compares an observation to either a grammar or contract reference and records dimensions, result, reason, provenance, and unknowns.
- Candidate grammar standing becomes `behaviorally_supported` only when grammar exists and comparison result is supported.

This evidence can support both producer implementation behavior and representation grammar application, but the responsibilities are distinct:

- Producer validation: stable deterministic output, exit status, exact spans, failure behavior.
- Grammar validation: examples, counterexamples, recovered grammar-book support, excluded structures, lexical bindings.
- Current `BehaviorComparison.reference_id` can point at grammar id or contract id, but does not type the comparison responsibility.

## 14. Candidate-realization analysis

Candidate realization binds:

```text
mechanism
contract
recovered grammar
accepted representation
produced representation
behavioral support
candidate standing
```

Evidence:

- `CandidateOperationalRealization` has separate `mechanism_reference`, `invocation_contract_reference`, `recovered_grammar_reference`, `accepted_input_representation`, and `produced_output_representation` fields.
- Automatic basis construction groups contracts and grammars by mechanism and cross-pairs them.
- Explicit `OperationalRealizationBasis` can bind one mechanism, one contract, one recovered grammar, behavioral observations/comparisons, availability/dependency/authority evidence, representation compatibility, and methodological compatibility.

Can it express one mechanism → several representation grammars? Structurally yes, because multiple recovered grammars for the same `mechanism_id` produce multiple candidate pairings. Semantically compressed, because the grammar artifact is named invocation grammar.

Can it express one representation grammar → several mechanisms? Structurally weak. The grammar type requires `mechanism_id`, so the same grammar must be duplicated per mechanism or manually referenced through bases with mechanism-specific artifacts. That suggests representation grammar ownership is not neutral.

Does current shape preserve both dimensions? Partially. It preserves separate references at the candidate level, but current grammar artifact ownership and contract fields compress representation grammar and invocation grammar.

## 15. Capability-reachability analysis

The reachability producer need not understand raw grammar material. It validates the future handoff against the candidate set, then consumes candidate standings and summary dimensions. It projects reachability from candidate support/block/unknown/conflict states.

Candidate standing has enough information to mean:

```text
this mechanism + this contract + this recovered grammar reference + behavior/support standings
```

It does not have enough explicit information to mean, without convention:

```text
this mechanism can apply this representation grammar to this exact material for this exact demand
```

Missing candidate-level handoff: an explicit representation-grammar reference or typed grammar-role binding from recovered representation grammar to candidate realization, separate from mechanism invocation contract.

## 16. Ownership matrix

| Responsibility | Current producer | Current artifact | Current consumer | Current status | Missing or compressed handoff |
|---|---|---|---|---|---|
| representation-grammar material | Campaign/manual caller | External material, `CandidateExternalGrammarInputCandidate.structural_claim` | Candidate external grammar formatting/tests | established upstream | Not connected to candidate realization |
| recovered representation grammar | No distinct producer found | `RecoveredInvocationGrammar` in practice | Candidate operational realization | compressed / misnamed | Neutral `RecoveredRepresentationGrammar` or typed role reference |
| lexical support | Campaign/manual caller if any | No first-class artifact in scoped road | Could only be provenance/source refs/behavior reason | missing handoff | Lexical support references distinct from invocation input |
| mechanism identity | Mechanism observations, claims, contracts, bases | `mechanism_id`, `mechanism_reference` | Candidate projection and reachability | established | None for identity |
| mechanism invocation contract | Caller-supplied contracts | `InvocationContract` | Candidate projection | partial | Keep material grammar out of `argument_grammar` or type embedded grammar reference |
| grammar-to-mechanism applicability | Caller/manual basis and behavior comparison | `OperationalRealizationBasis.recovered_grammar_ref`, `BehaviorComparison` | Candidate projection | partial / compressed | Typed applicability binding: mechanism contract applies representation grammar G |
| behavior of mechanism | Caller-supplied observations | `BehavioralObservation` | Candidate projection | established | Could type producer-behavior comparisons separately |
| behavior supporting grammar | Caller-supplied comparisons | `BehaviorComparison.reference_id` | Candidate projection | partial | Comparison role not explicit; can compare grammar or contract |
| candidate realization projection | `project_candidate_operational_realizations` | `CandidateOperationalRealizationSet` | Reachability producer | established with compressed grammar role | Separate representation-grammar and invocation-contract references |
| capability reachability | `project_capability_reachability` | `CapabilityReachabilityProjection` | Future selection handoff/rendering | established | No raw grammar schema needed if candidate standing is fixed upstream |

## 17. Exact first mismatch

The exact first mismatch is at candidate realization input ownership: `project_candidate_operational_realizations` accepts only `recovered_grammars: tuple[RecoveredInvocationGrammar, ...]` and indexes them by `mechanism_id`. A recovered English grammar from external material has no neutral representation-grammar owner or typed handoff into candidate realization. Feeding it directly requires renaming/compressing it as `RecoveredInvocationGrammar` or placing fragments into `InvocationContract.argument_grammar`.

## 18. Strongest supporting evidence

- `CandidateOperationalRealization` separates `invocation_contract_reference` from `recovered_grammar_reference`, proving the candidate shape recognizes two dimensions at least by reference.
- `OperationalRealizationBasis` also separates `invocation_contract_ref` and `recovered_grammar_ref`.
- Bash tests show the same `/bin/bash` mechanism before and after recovered grammar support, and avoid global Bash competency conclusions.
- Internal producer tests prove no tool/provider/registry concept is required.
- Reachability consumes candidate standing only and does not reinterpret raw grammar material.

## 19. Strongest counterevidence

Counterevidence actively preserved:

- Boundary notes say “Declared invocation grammar does not establish behaviorally validated competency” and “Behavioral support is bounded to the observed mechanism, version, invocation grammar, and probe conditions,” which may indicate the implementation intentionally uses “invocation grammar” broadly.
- The candidate has separate `invocation_contract_reference` and `recovered_grammar_reference`, so complete schema collapse has not occurred at the candidate level.
- `RecoveredInvocationGrammar` has a generic `bounded_fragment` and source refs, so it could be treated as a neutral recovered bounded grammar by caller convention despite its name.
- `InvocationContract` preserves accepted/produced representations separately from argument/result grammar, so it is not only a material grammar owner.
- Bash and English do not require entirely different roads; both can fit the existing candidate shape if grammar role is corrected or explicitly typed.
- Reachability likely does not require schema changes because it consumes candidate standing only.

## 20. Supported conclusions

1. Representation grammar is the structure governing material being interpreted, transformed, compared, or produced.
2. Invocation grammar is the structure governing how a realization mechanism is requested and returns a result.
3. `RecoveredInvocationGrammar` does not reliably describe the mechanism invocation boundary; fixtures use it for material grammar.
4. `InvocationContract` is partly a mechanism-call contract but currently can absorb material grammar via `argument_grammar`.
5. Candidate realization has separate contract and grammar references, but grammar ownership is compressed/misnamed.
6. One mechanism can structurally have several grammar fragments in the current road.
7. One representation grammar can conceptually have several mechanisms, but current artifact shape makes this awkward because `RecoveredInvocationGrammar` is mechanism-bound.
8. English grammar is preserved upstream as external/candidate grammar material, but not directly connected to candidate realization without renaming or compression.
9. Bash currently obscures and partially merges process invocation and Bash language grammar.
10. Capability reachability does not need to understand raw grammar material if candidate standing accurately carries the grammar-to-mechanism applicability conclusion.

## 21. Unsupported conclusions

- Unsupported: English is globally understood.
- Unsupported: Bash is globally acquired.
- Unsupported: internal producers own English grammar.
- Unsupported: passing grammar into a producer makes it invocation grammar.
- Unsupported: lexical material is general semantic competency.
- Unsupported: mechanism availability alone establishes capability reachability.
- Unsupported: the existing English external grammar road already reaches capability projection without distortion.
- Unsupported: no ownership change is required; counterevidence supports partial separation but not complete correctness.

## 22. Primary classification

```text
D. Current artifacts compress representation grammar and invocation grammar into one owner.
```

## 23. English-road classification

```text
4. The road does not yet connect recovered English grammar to operational realization.
```

The road is conceptually close because candidate realization has a grammar reference, but the English external-grammar road lacks an explicit recovered-representation-grammar to candidate-realization handoff.

## 24. First-missing-boundary classification

```text
II. Representation-grammar-to-candidate-realization binding is missing.
```

Recovered representation-grammar ownership exists upstream as candidate external grammar material but not as a direct candidate-realization input. The first missing boundary is the typed binding from that recovered representation grammar to the mechanism/contract candidate.

## 25. Exact next bounded boundary

Responsibility to recover:

```text
representation-grammar-to-candidate-realization applicability binding
```

Current missing/compressed owner:

```text
RecoveredInvocationGrammar plus OperationalRealizationBasis.recovered_grammar_ref
```

Producer:

```text
narrow adapter from recovered/candidate external grammar artifact to candidate operational realization grammar-role binding
```

Input artifacts:

```text
CandidateExternalGrammarSet or future recovered representation grammar artifact,
ExaminationProbeRequest / OperationalRealizationHandoff,
InvocationContract,
MechanismObservation / BehavioralObservation / BehaviorComparison as available
```

Output artifact or changed handoff:

```text
typed representation grammar reference on candidate realization basis or an adapter output that binds representation grammar G to mechanism M under invocation contract C
```

Immediate consumer:

```text
project_candidate_operational_realizations
```

Manual responsibility eliminated:

```text
manual renaming of representation grammar as RecoveredInvocationGrammar or embedding material grammar in InvocationContract.argument_grammar
```

Compatibility treatment:

```text
legacy RecoveredInvocationGrammar remains accepted as an adapter/compatibility input, but new role should be explicit and not require broad migration
```

Explicit exclusions:

```text
no provider selection, no realization selection, no invocation-request construction, no authorization, no execution, no reachability-topology rewrite, no broad grammar migration
```

## 26. Implementation-warrant decision

```text
One bounded implementation slice is warranted.
```

- Responsibility to recover: representation-grammar-to-candidate-realization binding.
- Current missing or compressed owner: `RecoveredInvocationGrammar`/`InvocationContract.argument_grammar` compressed ownership.
- Producer: narrow adapter or explicit role-binding producer.
- Input artifacts: recovered/candidate external grammar material, handoff, mechanism contract, behavior/support references.
- Output artifact or changed handoff: typed representation grammar reference or candidate basis binding.
- Immediate consumer: candidate operational realization projection.
- Manual responsibility eliminated: treating representation grammar as invocation grammar by convention.
- Compatibility treatment: keep existing fields as legacy/adapter inputs.
- Explicit exclusions: no broad grammar migration; no reachability or realization-selection changes.

## 27. Files changed

- `representation_invocation_grammar_topology_audit_001.md` only.

## 28. Probes executed

Read-only search/inspection probes:

```bash
rg -n "RecoveredInvocationGrammar|InvocationContract|OperationalRealizationBasis|CandidateOperationalRealization" seed_runtime tests
rg -n "CandidateExternalGrammar|external grammar|structural projection|surface feature|grammar fragment|source_material" seed_runtime tests campaigns
rg -n "dictionary|thesaurus|lexical|subject|predicate|sentence|English" seed_runtime tests campaigns
rg -n "accepted_input_representation|produced_output_representation|required_input_representation|requested_output_representation" seed_runtime tests
rg -n "grammar_reference|grammar_id|contract_reference|mechanism_reference|behavior" seed_runtime tests
sed -n '1,230p' seed_runtime/candidate_operational_realization.py
sed -n '1,130p' seed_runtime/examination_probe_request.py
sed -n '1,140p' seed_runtime/candidate_external_grammar.py
sed -n '1,160p' tests/test_candidate_operational_realization.py
```

Baseline tests:

```bash
pytest -q tests/test_candidate_external_grammar.py tests/test_external_material_structural_projection.py tests/test_external_material_surface_feature_projection.py tests/test_candidate_operational_realization.py tests/test_capability_reachability_projection.py tests/test_examination_probe_request.py
```

Diff guardrail:

```bash
git diff --stat
git diff --numstat
git diff --check
git status --short
```

## 29. Confidence statement

Confidence: moderate-high for the scoped implementation topology. The strongest evidence is direct field shape plus Bash/internal-producer fixtures. Remaining uncertainty: the term `RecoveredInvocationGrammar` may have been intended as a broad umbrella by prior convention, but current fixtures and the English proving case show that this convention compresses ownership in a way that obscures the representation/invocation boundary.

## Required questions answered

1. Representation grammar is structure governing material being interpreted, transformed, compared, or produced.
2. Invocation grammar is bounded structure by which a realization mechanism is requested and returns a result.
3. Current owners are listed in sections 5 and 16.
4. `RecoveredInvocationGrammar` does not reliably describe invocation grammar.
5. Yes, it sometimes preserves representation grammar instead.
6. That usage is implicit/accidental by fixture convention, not explicit by role field.
7. Yes, one mechanism can structurally apply several grammar fragments.
8. Conceptually yes, one representation grammar can have several realizations; current shape makes neutral sharing awkward.
9. Partially; candidate references are separate, but ownership is compressed/misnamed.
10. Not directly without distortion.
11. The nearest field is `RecoveredInvocationGrammar.bounded_fragment` with supporting/excluded/source fields; upstream candidate English grammar is in `CandidateExternalGrammarInputCandidate.structural_claim`.
12. It is lost/unconnected between candidate external grammar and candidate realization, or renamed as `RecoveredInvocationGrammar`.
13. No, the internal producer does not own English grammar.
14. No, passing grammar into a producer does not make it invocation grammar.
15. Dictionary and thesaurus material belong to lexical representation knowledge and grammar support, possibly passed as invocation input but not invocation grammar.
16. Lexical knowledge can be part of capability demand and realization basis through distinct references.
17. Grammar-validating evidence includes grammar-book examples, counterexamples, lexical bindings, limitations, and source-span preservation under G.
18. Producer-validating evidence includes stable deterministic outputs, exact invocation observations, exit status, and failure behavior.
19. Yes, those comparison responsibilities are distinct.
20. Yes, Bash can be represented without merging process invocation and Bash language grammar.
21. Yes, the before/after Bash fixture can still be expressed after correcting the distinction.
22. Capability reachability likely does not require schema changes.
23. Candidate realization needs either schema changes or a narrow typed adapter/reference.
24. A narrow adapter or additional typed reference appears sufficient.
25. No distinct `RecoveredRepresentationGrammar` artifact was found in the scoped road.
26. Adding another grammar artifact would not duplicate an existing neutral owner; it would separate compressed ownership.
27. `RecoveredInvocationGrammar` is partly misnamed.
28. It is also compressed ownership requiring separation.
29. The first missing/misplaced owner is the representation-grammar-to-candidate-realization binding.
30. Yes, one bounded implementation slice is warranted.
