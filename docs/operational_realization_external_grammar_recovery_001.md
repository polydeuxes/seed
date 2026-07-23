# Operational Realization External Grammar Recovery 001

## Scope

This is one bounded, report-only Fidelity recovery of the active operational-realization family on current merged `main` after PR 1933.  The inspected boundary was determined by symbol search over `seed_runtime`, `tests`, and `docs`, then by focused file inspection and history search.  No production code, tests, fixtures, package exports, CLI behavior, API behavior, events, the Book, or repository structure are changed by this report.

Primary files inspected:

- `seed_runtime/examination_probe_request.py`
- `seed_runtime/candidate_operational_realization.py`
- `seed_runtime/capability_reachability_projection.py`
- `seed_runtime/operational_realization_selection.py`
- `seed_runtime/operational_realization_warrant.py`
- `seed_runtime/representation_grammar_applicability.py`
- `seed_runtime/__init__.py`
- `tests/test_candidate_operational_realization.py`
- `tests/test_capability_reachability_projection.py`
- `tests/test_operational_realization_selection.py`
- `tests/test_operational_realization_warrant.py`
- related tests found by repository search: `tests/test_examination_probe_request.py`, `tests/test_representation_grammar_applicability.py`, `tests/test_operator_expression_interpretation.py`, and operational-realization need tests.

## Governing Distinction

The active distinction recovered here is:

- **External grammar**: what a foreign mechanism accepts, how it is invoked, what representations it consumes, what material it returns, and how returned material is conventionally interpreted.
- **Seed internal grammar**: how testimony is preserved, how sources are attributed, how candidates are compared, how support or contradiction changes standing, how scope and exclusions are retained, and how Unknown remains visible.

An external grammar can be evidence-backed.  That does not make it Seed's internal constitutional grammar.  The operational-realization family mostly models evidence-backed claims about mechanisms, invocation contracts, recovered bounded fragments, process-style observations, compatibility, reachability, selection, and warranting.  Its internal-looking fields are standing disciplines embedded inside a staged external-grammar pipeline, not independent constitutional primitives.

## Current Artifact Inventory

| Artifact | Definition/export evidence | Producer | Consumer | Production occurrence outside tests | Classification |
| --- | --- | --- | --- | --- | --- |
| `OperationalRealizationHandoff` | Defined in `examination_probe_request.py`; exported from `seed_runtime.__init__`. | `ExaminationProbeRequest.to_operational_realization_handoff()` when a probe request is `bound`; tests construct it directly. | `project_candidate_operational_realizations()` and representation-grammar applicability. | A method can create it, but repository search found no non-test road invoking candidate projection from that method. | C. staged_handoff_scaffolding |
| `InvocationContract` | Defined/exported in candidate module. | Tests and callers can construct; auto-fallback creates unknown contract. | Candidate projection; representation-grammar applicability tests. | No non-test occurrence of concrete contracts found. | A. external_grammar_representation |
| `RecoveredInvocationGrammar` | Defined/exported in candidate module. | Tests construct; representation grammar recovery has separate `RecoveredRepresentationGrammar`. | Candidate projection. | No non-test occurrence as this class found. | D. external_grammar_evidence |
| `BehavioralObservation` | Defined/exported in candidate module. | Tests construct. | Candidate projection and behavior comparisons. | No non-test occurrence found. | D. external_grammar_evidence |
| `BehaviorComparison` | Defined/exported in candidate module. | Tests construct. | Candidate projection maps support/contradiction/unknown/conflict into behavior standing. | No non-test occurrence found. | E. mixed_compression |
| `OperationalRealizationBasis` | Defined/exported in candidate module; can be auto-created from observations/claims/contracts/grammars. | Candidate projection when explicit bases are absent; tests construct explicit bases. | Candidate projection. | Auto-production is inside projection only; no non-test road reaches that projection. | E. mixed_compression |
| `CandidateOperationalRealization` | Defined/exported in candidate module. | `project_candidate_operational_realizations()`. | Candidate set, reachability projection, selection, warrant. | No non-test road found. | E. mixed_compression |
| `CandidateOperationalRealizationSet` | Defined/exported in candidate module. | `project_candidate_operational_realizations()`. | `to_future_capability_reachability_handoff()`, reachability projection, format/json helpers. | No non-test road found. | E. mixed_compression |
| `FutureCapabilityReachabilityHandoff` | Defined/exported in candidate module. | `CandidateOperationalRealizationSet.to_future_capability_reachability_handoff()`. | `project_capability_reachability()`. | No non-test road found. | C. staged_handoff_scaffolding |
| `CapabilityReachabilityProjection` | Defined/exported in reachability module. | `project_capability_reachability()`. | Selection, json/format helpers, warrant validation. | No non-test road found. | E. mixed_compression |
| `FutureOperationalRealizationSelectionHandoff` | Defined/exported in reachability module. | `project_capability_reachability()` only for reachable/blocked state. | `select_operational_realization()`. | No non-test road found. | C. staged_handoff_scaffolding |
| `OperationalRealizationSelection` | Defined/exported in selection module. | `select_operational_realization()`. | Warrant projection and json/format helpers. | No non-test road found. | E. mixed_compression |
| `FutureOperationalRealizationWarrantHandoff` | Defined/exported in selection module. | `select_operational_realization()` only when selected. | `project_operational_realization_warrant()`. | No non-test road found. | C. staged_handoff_scaffolding |
| `OperationalRealizationWarrant` | Defined/exported in warrant module. | `project_operational_realization_warrant()`. | json/format helpers; emits future egress handoff when warranted. | No non-test road found. | E. mixed_compression |
| `FutureBoundedEgressTranslationHandoff` | Defined/exported in warrant module. | `project_operational_realization_warrant()` only when warrant is `warranted`. | No current implementation consumer found by symbol search. | None found. | F. compatibility_or_historical_residue |

## Producer → Artifact → Consumer Roads

### Runtime-constructible road

The only constructible full road in current code is:

`ExaminationProbeRequest.to_operational_realization_handoff()` → `OperationalRealizationHandoff` → `project_candidate_operational_realizations()` → `CandidateOperationalRealizationSet.to_future_capability_reachability_handoff()` → `FutureCapabilityReachabilityHandoff` → `project_capability_reachability()` → `CapabilityReachabilityProjection.future_selection_handoff` → `select_operational_realization()` → `OperationalRealizationSelection.future_warrant_handoff` → `project_operational_realization_warrant()` → `OperationalRealizationWarrant.future_egress_translation_handoff`.

This is a constructible road, not an observed production occurrence.  Current search found the projection calls only in tests, while the modules export constructors, projectors, json helpers, and formatters.  The handoffs are mostly identity-and-partition transfer seams into the next predetermined stage.

### Fixture road

The active fixture road appears in the candidate, reachability, selection, warrant, representation-grammar-applicability, examination-probe-request, and operator-expression tests.  Tests directly construct `/bin/bash`, `echo hello`, `stdout`, `stderr`, `exit_status`, compatibility, method, dependency, authority, and policy fixture material.  Those tests prove behavior of the staged objects and their validators.  They do not prove a production path that invokes Bash, preserves observations from an actual runtime probe, writes events, mutates state, establishes knowledge, projects a response, or reaches an egress implementation.

### Package export road

`seed_runtime.__init__` exports the named artifacts and helper functions.  Package export is compatibility/API surface evidence.  It is not current consumer evidence.

### CLI/rendered surface road

Each stage has `format_*` and `*_json` helpers for candidate set, reachability projection, selection, and warrant.  Repository search did not find CLI flags or argparse roads exposing these helpers.  Formatting is read-only rendering, not constitutional necessity.

### Event/persistence road

The primary artifacts default to `read_only=True`, `writes_event_ledger=False`, and `mutates_cluster=False`.  No repository evidence was found that these artifacts write the event ledger, persist cluster truth, mutate state, establish facts, or authorize execution.

## Production Occurrence Findings

For each stage:

- **Handoff from examination request**: producer exists as a method on `ExaminationProbeRequest`; no non-test consumer chain found.
- **Candidate projection**: producer function exists; current call sites found by search are tests and one representation-grammar-applicability test bridge.  No operator-visible or state-changing consequence found.
- **Capability reachability**: producer function exists; current call sites found by search are tests.  It may format/read-only render but does not select or execute.
- **Selection**: producer function exists; current call sites found by search are tests.  It creates the warrant handoff only because the next stage expects it.
- **Warrant**: producer function exists; current call sites found by search are tests.  It creates a future egress handoff, but no consumer for that handoff was found.
- **Egress translation handoff**: producer exists; no current consumer found.  It does not reach egress, external invocation, preservation, examination establishment, projection response, or any event-writing path.

Current finding: **no production occurrence of the staged operational-realization family was found after deletion of the operational-realization Book district**.  The family is constructible and exported; current runtime roads are not evidenced beyond the examination request's ability to make an unused handoff.

## External Grammar Classification

- `InvocationContract`: external grammar representation.  Its fields are accepted input representation, produced output representation, argument grammar, result grammar, mechanism, convention, provenance, and unknowns.
- `RecoveredInvocationGrammar`: external grammar evidence.  It preserves a bounded fragment, supported structures, excluded structures, source material refs, provenance, unknowns, and conflicts.
- `BehavioralObservation`: external grammar evidence.  It preserves exact invocation input plus process-return conventions: stdout, stderr, exit status, and version.
- `BehaviorComparison`: mixed compression.  It compares returned material to a reference and assigns support/contradiction/unknown/conflict, an internal standing discipline applied to external process observations.
- `OperationalRealizationBasis`: mixed compression.  It collects mechanism, contract, grammar, observation references, availability, dependency, authority, representation compatibility, method compatibility, Unknown, and conflicts.
- `CandidateOperationalRealization`: mixed compression.  It turns external mechanism grammar plus internal standing into a candidate standing.
- `CandidateOperationalRealizationSet`: mixed compression.  It partitions candidates into supported, unsupported, unknown, and conflict while retaining no-known-realization observations.
- `CapabilityReachabilityProjection`: mixed compression.  It interprets candidate standings into reachability, blockedness, unsupportedness, Unknown, or conflict for an exact bounded transformation.
- `OperationalRealizationSelection`: mixed compression.  It is internally meaningful as zero-or-one choice discipline, but it remains bound to operational-realization candidates and policy constraints over mechanism, representation, authority, and dependency.
- `OperationalRealizationWarrant`: mixed compression.  It is internally meaningful as bounded reliance discipline, but it warrants a mechanism-specific selected realization with invocation contract and grammar references.

## Staged Handoff Classification

- `OperationalRealizationHandoff`: staged handoff from examination request to candidate-realization projection.  It contains probe, artifact, work-contract, capability, representation, and method references, but no mechanism or observation.
- `FutureCapabilityReachabilityHandoff`: staged handoff from candidate set to reachability.  It repeats candidate IDs, standings, dependency observations, authority observations, unknowns, and conflicts so reachability can validate the transfer.
- `FutureOperationalRealizationSelectionHandoff`: staged handoff from reachability to selection.  It exists only when reachability is reachable or blocked, and says whether selection is lawful now.
- `FutureOperationalRealizationWarrantHandoff`: staged handoff from selection to warrant.  It exists only when selection selected a candidate.
- `FutureBoundedEgressTranslationHandoff`: residue.  It is produced only by warranted warrant projection and no current consumer was found.

These Future* objects are software-stage plumbing.  They should not be treated as independent constitutional responsibilities.

## Protected Distinction Ledger

### Mechanism existence

- **Current representation**: `MechanismObservation` and `availability_evidence`/`mechanism_availability_standing`.
- **Evidence**: candidate projection maps availability evidence to mechanism standing.
- **Standing**: real distinction; testimony about an external grammar/mechanism.
- **Dependency on staged subsystem**: currently represented here for operational-realization candidates, but mechanism observation as attributed testimony can exist without the pipeline.
- **Remaining Unknown**: no canonical non-operational mechanism-observation vocabulary was recovered in this bounded pass.

### Mechanism availability

- **Current representation**: availability evidence values `available`, `unavailable`, `unknown`, `conflict`.
- **Evidence**: candidate projection and reachability partition available/unavailable/conflict/unknown.
- **Standing**: real distinction; external mechanism standing, not Seed constitution.
- **Dependency**: not logically dependent on staged subsystem; currently tested here.
- **Remaining Unknown**: whether any active operational surface records availability elsewhere was not established.

### Declared invocation form

- **Current representation**: `InvocationContract.argument_grammar` and `result_grammar`; grammar standing can be `declared_only`.
- **Evidence**: tests use `opaque bounded process invocation`, `echo literal`, and direct internal producer contracts.
- **Standing**: external grammar representation.
- **Dependency**: currently protected through this subsystem.
- **Remaining Unknown**: whether a smaller testimony model already holds declared foreign invocation forms outside this family.

### Behavior-tested invocation form

- **Current representation**: `RecoveredInvocationGrammar` plus `BehavioralObservation` and `BehaviorComparison`.
- **Evidence**: tests use `echo hello`, returned stdout/stderr/exit status, and comparison dimensions.
- **Standing**: evidence about external grammar; internal only in the support/contradiction discipline.
- **Dependency**: the exact Bash/process shape is currently represented here.
- **Remaining Unknown**: no active producer of these observations outside tests was found.

### Behavioral support

- **Current representation**: `BehaviorComparison.result == supported`, mapped to `behavior_standing == supported` and possibly `grammar_standing == behaviorally_supported`.
- **Evidence**: candidate and warrant tests assert supported candidates and warranted state.
- **Standing**: mixed; support as a standing act is internal, but the observed dimensions are external.
- **Dependency**: support/contradiction can exist without staged operational realization; the Bash-specific support fixture currently lives here.
- **Remaining Unknown**: canonical general support/contradiction vocabulary outside this family was not exhaustively recovered.

### Behavioral contradiction

- **Current representation**: `BehaviorComparison.result == contradicted`; reachability lists behavioral contradictions; warrant rejects contradicted behavior.
- **Evidence**: candidate and warrant tests mutate behavior to contradiction/conflict.
- **Standing**: mixed; contradiction is internal standing discipline over external observations.
- **Dependency**: not logically dependent on staged subsystem.
- **Remaining Unknown**: current non-operational contradiction ledger was not fully mapped in this pass.

### Representation compatibility

- **Current representation**: accepted/produced representations on contracts compared to required/requested representations; basis can force compatible/incompatible/unknown/conflict.
- **Evidence**: tests use `text/plain`, `json`, `bytes`, and incompatible pairs.
- **Standing**: external grammar compatibility relation with an internal compatibility standing.
- **Dependency**: currently represented in this subsystem and also adjacent representation-grammar-applicability, but not proven as a production road here.
- **Remaining Unknown**: whether representation compatibility has one canonical non-operational form elsewhere.

### Methodological compatibility

- **Current representation**: `methodological_compatibility` values `satisfies`, `violates`, `cannot_establish`, `conflicts_with`.
- **Evidence**: tests assert satisfy/violate cases; examination request carries method-applicability constraints.
- **Standing**: internal-ish standing discipline but compressed into mechanism-candidate evaluation.
- **Dependency**: method applicability exists earlier in examination request machinery, so this distinction does not depend exclusively on operational realization.
- **Remaining Unknown**: whether the later candidate-level method compatibility duplicate is necessary.

### Dependency availability

- **Current representation**: basis/candidate dependency evidence and reachability blockers.
- **Evidence**: tests create unavailable dependencies and expect blocked/non-selected/warrant rejection behavior.
- **Standing**: external or environmental availability testimony, not internal constitutional grammar.
- **Dependency**: not logically dependent on the staged family.
- **Remaining Unknown**: current production dependency-check source not found.

### Authority availability

- **Current representation**: `authority_evidence`, `authority_standing`, authority blockers; boundary notes distinguish authority reachability from constitutional authorization.
- **Evidence**: tests create unavailable authority and reachability blocked cases.
- **Standing**: mixed; authority reachability is an operational precondition, not authorization.
- **Dependency**: the distinction is real and should remain distinct from authorization, but does not require this staged subsystem.
- **Remaining Unknown**: active authorization road not examined beyond confirming this family does not authorize.

### Bounded grammar support

- **Current representation**: recovered bounded fragment, supported structures, excluded structures, behaviorally supported grammar standing, and boundary notes.
- **Evidence**: `echo hello` is supported while pipelines, redirection, command substitution, and general scripting are excluded in tests.
- **Standing**: external grammar evidence plus internal scoping discipline.
- **Dependency**: bounded scope/exclusions can be represented without preserving operational-realization classes.
- **Remaining Unknown**: exact successor home is out of scope and not designed here.

### Excluded grammar structures

- **Current representation**: `RecoveredInvocationGrammar.excluded_structures` and warrant limitations/loss.
- **Evidence**: tests explicitly retain excluded pipelines and prevent one literal fragment from becoming global competency.
- **Standing**: real external grammar testimony with internal scope-retention discipline.
- **Dependency**: not inherently dependent on staged subsystem.
- **Remaining Unknown**: whether exclusions are already canonically held in representation-grammar recovery for this exact mechanism family.

### One successful fragment != global competency

- **Current representation**: boundary notes, recovered grammar bounded fragment, excluded structures, reachability exact bounded transformation validation.
- **Evidence**: tests compare before/after widening demand and assert one literal does not prove wider demand.
- **Standing**: internal standing discipline applied to external grammar evidence.
- **Dependency**: no; the principle can operate over arbitrary testimony.
- **Remaining Unknown**: no single canonical general class identified in this pass.

## Test-Family Findings

The tests protect real distinctions, but mostly as fixture roads:

- `/bin/bash exists`: preserved as mechanism observation/availability testimony.
- `echo hello is an accepted bounded fragment`: candidate translation from a recovered external bounded fragment.
- `stdout contains hello`, `stderr is empty`, `exit status is zero`: preserved returned material using external process conventions.
- `representation is compatible or incompatible`: external representation relation plus standing.
- `method satisfies or violates a proposed requirement`: internal-ish method discipline, duplicated at candidate stage.
- `dependency/authority unavailable`: environmental and authority-precondition testimony, not authorization.
- `pipelines remain excluded`: retained limitation preventing global competency.

The tests are useful as recovery witnesses.  They do not by themselves validate the current subsystem or prove production standing.

## Historical Standing

Focused history commands found the following supporting testimony:

- `git log --all -S'CandidateOperationalRealization'` shows the family entered at `b098883 Recover constitutional view composition consumer (#1832)` and was later touched by reports/corrections including `1a6533d Correct operational realization compression (#1927)`.
- `git log --all -G'Book VII|Operational Realization' -- docs tests seed_runtime` shows `fd0adf3 Excise Book VII operational topic collection (#1929)` and `eb5cda7 Correct Fidelity production ownership (#1930)`, with PR 1933 adding a contamination/failure recovery report.
- The existing contamination report records Book VII excision and identifies the candidate operational realization/future-handoff chain as passing-test contamination risk rather than confirmed production standing.

History supports that the operational-realization family once had adjacent Book standing and has since been narrowed, questioned, or preserved through reports/tests.  History is not current authority; current code search is the authority for production occurrence.

## Small Internal Acts Recovered

The smallest internal acts supported by the family's evidence are:

1. **Preserve attributed testimony**
   - Evidence: provenance fields on contracts, grammars, observations, bases, sets, selections, and warrants.
   - Canonical elsewhere: likely yes as a general Seed discipline, but not fully mapped here.
   - Can exist without terminology: yes.
   - Kind: responsibility/standing discipline, not a mechanism-specific artifact.

2. **Preserve returned material**
   - Evidence: behavioral observations retain invocation input, stdout, stderr, exit status, version, provenance, Unknown.
   - Canonical elsewhere: unknown in this bounded pass.
   - Can exist without terminology: yes, over arbitrary observations.
   - Kind: preservation responsibility.

3. **Compare expectation with observation**
   - Evidence: behavior comparison records compared dimensions and result.
   - Canonical elsewhere: unknown.
   - Can exist without terminology: yes.
   - Kind: act.

4. **Record support and contradiction**
   - Evidence: behavior comparison result and candidate/warrant mappings.
   - Canonical elsewhere: likely as general standing discipline, but not proven here.
   - Can exist without terminology: yes.
   - Kind: standing discipline.

5. **Bound scope and retain exclusions**
   - Evidence: bounded fragment, supported structures, excluded structures, exact demand validation, and limitations/loss.
   - Canonical elsewhere: representation grammar recovery/applicability appears adjacent, but this pass does not promote it.
   - Can exist without terminology: yes.
   - Kind: standing discipline.

6. **Retain Unknown and conflicts**
   - Evidence: unknowns/conflicts fields and partitioning across all stages.
   - Canonical elsewhere: yes as broad Seed vocabulary, though exact references were not fully mapped here.
   - Can exist without terminology: yes.
   - Kind: standing discipline.

7. **Change candidate standing from bounded evidence**
   - Evidence: candidate projection maps availability, grammar, behavior, representation, method, dependency, and authority into supported/unsupported/unknown/conflict.
   - Canonical elsewhere: uncertain.
   - Can exist without terminology: yes over arbitrary candidates, but this implementation is mechanism-specific.
   - Kind: act plus artifact-level policy.

No successor classes are designed or recommended here.

## What Is Not Recovered

- `InvocationContract` is not recovered as a constitutional primitive.  It is a representation of a foreign invocation form.
- `RecoveredInvocationGrammar` is not recovered as Seed's internal grammar.  It is evidence about a bounded external grammar fragment.
- `OperationalRealizationBasis` is not recovered as a constitutional primitive.  It compresses testimony, compatibility, support, environmental availability, authority reachability, Unknown, and conflicts for a mechanism candidate.
- The Future* handoffs are not recovered as constitutional acts.  They are stage-transfer scaffolding.
- The warrant's egress handoff is not recovered as an active egress road.  No consumer was found.
- Behavior support is not treated as truth.
- One successful invocation is not treated as global competency.

## Unknowns

- Whether a non-operational canonical testimony/comparison/standing vocabulary already covers every small internal act was not exhaustively mapped.
- Whether package consumers outside this repository import the exported classes is unknown; repository current authority shows only exports, not external use.
- Whether PR 1934 should delete, quarantine, or rewrite tests is intentionally not answered by this report.
- Whether representation-grammar recovery/applicability should absorb any recovered internal act is out of scope.

## Fidelity Finding

The current operational-realization family does **not** primarily implement Seed's internal constitutional grammar.  It primarily encodes an evidence-backed grammar for interpreting and invoking foreign mechanisms, then threads that evidence through staged handoffs into reachability, selection, warrant, and an unconsumed future egress handoff.

The family is **mixed but decomposable**:

- **Internal**: preserving attributed testimony, preserving returned material, comparing expectations with observations, recording support/contradiction, retaining Unknown/conflict, bounding scope, retaining exclusions, and preventing one successful fragment from becoming global competency.
- **External**: mechanism identity/existence/availability, invocation contract, accepted/produced representations, bounded fragments such as `echo hello`, stdout/stderr/exit-status conventions, representation compatibility, dependency availability, authority reachability as operational precondition, and grammar exclusions such as pipelines.
- **Staged plumbing**: `OperationalRealizationHandoff`, `FutureCapabilityReachabilityHandoff`, `FutureOperationalRealizationSelectionHandoff`, `FutureOperationalRealizationWarrantHandoff`, and `FutureBoundedEgressTranslationHandoff`.

Required bounded answer: `mixed_but_decomposable`.

## Recommended Next Inquiry

Perform a separate deletion-readiness inquiry that compares the recovered small internal acts against current general testimony, evidence, comparison, candidate-standing, Unknown/conflict, and representation-grammar machinery.  The next inquiry should ask which tests preserve unique constitutional behavior and which tests merely preserve staged operational-realization scaffolding.  It should not design a replacement framework.
