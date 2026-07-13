# Constitutional Pipeline Implementation Scout 001

Repository authority wins. This scout is read-only with respect to implementation and tests. It inspects the current constitutional-pipeline implementation pressure around producing `BoundedConstitutionalQuestion` and commits only this report.

## Current branch and repository state

- Branch: `work`.
- Starting HEAD inspected before this scout report: `84adc25`.
- Working tree before report creation was clean relative to tracked files.
- Active AGENTS instructions require operational visibility updates for new diagnostics, but this scout adds no diagnostic, operational surface, implementation code, or tests.

## Commands and evidence paths inspected

Commands used for orientation and evidence discovery:

```bash
pwd
rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules'
git status --short --branch
cat AGENTS.md
rg -n "BoundedConstitutionalQuestion|QuestionProjection|CapabilityProjection|ConstitutionalViewSelection|ConstitutionalViewComposition|SelectedConstitutionalViews|BoundedConstitutionalExplanation|constitutional" .
rg -n "BoundedConstitutionalQuestion|QuestionProjection|CapabilityProjection|ConstitutionalViewSelection|ConstitutionalViewComposition|SelectedConstitutionalViews|BoundedConstitutionalExplanation" src tests *.md -g '!*.pyc'
rg --files | sed -n '1,120p'
rg -n "class Constitutional|@dataclass|def .*constitutional|constitutional_view" seed.py tests/test_constitutional_view_selection.py tests/test_constitutional_view_composition.py 2>/dev/null
sed -n '1,260p' seed_runtime/constitutional_view_selection.py
sed -n '1,220p' seed_runtime/constitutional_view_composition.py
sed -n '1,180p' tests/test_constitutional_view_selection.py
rg -n "operator inquiry|operator.*inquiry|bounded question|QuestionFamily|bounded_ask|question_family|provenance|testimony|evidence" seed_runtime tests | head -n 240
rg -n "constitutional_view_composition|constitutional_process|constitutional_governance|constitutional_fidelity|diagnostic" seed.py seed_runtime/diagnostic_inventory.py seed_runtime/diagnostic_shape_audit.py tests/test_constitutional_view_composition.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py | head -n 220
rg -n "constitutional-view-composition|constitutional_view_composition|constitutional-process|constitutional-governance|constitutional-fidelity|bounded-ask|QuestionFamily" scripts seed_runtime tests | head -n 260
git branch --show-current
git rev-parse --short HEAD
sed -n '1,140p' constitutional_pipeline_readiness_audit.md
sed -n '1,130p' lawful_architectural_stopping_characterization.md
```

Primary implementation files inspected:

- `seed_runtime/constitutional_view_selection.py`
- `seed_runtime/constitutional_view_composition.py`
- `seed_runtime/read_model_ownership.py`
- `seed_runtime/constitutional_process_view.py`
- `seed_runtime/constitutional_governance_view.py`
- `seed_runtime/constitutional_fidelity_view.py`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `scripts/seed_local.py`

Primary test files inspected:

- `tests/test_constitutional_view_selection.py`
- `tests/test_constitutional_view_composition.py`
- `tests/test_constitutional_process_view.py`
- `tests/test_constitutional_governance_view.py`
- `tests/test_constitutional_fidelity_view.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_diagnostic_inventory.py`
- `tests/test_diagnostic_shape_audit.py`

Primary repository-authority reports inspected for the active constitutional pipeline, and only insofar as they directly concern this pipeline:

- `constitutional_pipeline_readiness_audit.md`
- `lawful_architectural_stopping_characterization.md`
- `bounded_constitutional_question_slice_001.md`
- `constitutional_question_projection_characterization.md`
- `constitutional_capability_projection_characterization.md`
- `constitutional_view_selection_slice_001.md`
- `constitutional_view_selection_slice_002.md`
- `constitutional_view_selection_characterization.md`
- `constitutional_view_composition_slice_001.md`
- `constitutional_view_composition_slice_002.md`

## Constitutional pipeline consistency verification

The current branch supports the active work as the constitutional pipeline:

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
QuestionProjection
        +
CapabilityProjection
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
BoundedConstitutionalExplanation
```

Repository evidence supporting the gate:

- `constitutional_pipeline_readiness_audit.md` explicitly states that implementation evidence supports this topology as architecturally complete.
- `seed_runtime/constitutional_view_selection.py` implements `ConstitutionalQuestionProjection`, `ConstitutionalCapabilityProjection`, `SelectedConstitutionalViews`, `select_constitutional_views(...)`, and `selected_constitutional_views_to_composition_request(...)`.
- `seed_runtime/constitutional_view_selection.py` consumes projections only, performs deterministic exact-key matching, refuses raw question consumption, refuses immutable constitutional view consumption, and preserves read-only / no-ledger / no-cluster-mutation boundaries.
- `seed_runtime/constitutional_view_composition.py` implements `ConstitutionalViewCompositionRequest`, `ConstitutionalViewCompositionArtifact`, `constitutional_view_composition_request(...)`, `build_constitutional_view_composition(...)`, JSON rendering, and human formatting.
- `tests/test_constitutional_view_selection.py` proves projection consumption, immutable selected-view output, uncertainty preservation, and direct wiring into Composition.
- `tests/test_constitutional_view_composition.py` proves explicit request shape, registered-view composition, Unknown/refusal preservation, unregistered-view refusal, rendering, CLI exposure, diagnostic inventory registration, and shape-audit visibility.
- `constitutional_question_projection_characterization.md` characterizes Question Projection as a deterministic read-only projection regenerated from the bounded-question fields.
- `constitutional_capability_projection_characterization.md` characterizes Capability Projection as a deterministic read-only projection regenerated from read-model contracts, registration, and immutable constitutional view artifacts.
- `constitutional_view_selection_characterization.md` supports `ConstitutionalViewSelection` as an irreducible implementation-local ownership boundary.
- `lawful_architectural_stopping_characterization.md` supports Lawful Architectural Stopping as the current condition where remaining work is implementation realization, deterministic projection, public/diagnostic exposure, integration wiring, tests, or documentation.

No inspected implementation evidence establishes a different active district or invalidates the listed topology.

## Symbols and call paths inspected

### Downstream implemented path

Current implemented downstream path is:

```text
ConstitutionalQuestionProjection
+
ConstitutionalCapabilityProjection
        ↓
select_constitutional_views(...)
        ↓
SelectedConstitutionalViews
        ↓
selected_constitutional_views_to_composition_request(...)
        ↓
ConstitutionalViewCompositionRequest
        ↓
build_constitutional_view_composition(...)
        ↓
ConstitutionalViewCompositionArtifact
```

`ConstitutionalViewCompositionArtifact` is the implemented bounded constitutional explanation artifact for the current topology. It is not named `BoundedConstitutionalExplanation` in code, but the readiness audit treats it as the implemented bounded explanation surface.

### CLI and diagnostic path

The public implemented constitutional path is currently view/composition-oriented, not full-pipeline-oriented:

```text
scripts/seed_local.py --constitutional-view-composition VIEW...
        ↓
constitutional_view_composition_request(requested_views=...)
        ↓
build_constitutional_view_composition(...)
        ↓
format_constitutional_view_composition(...) or constitutional_view_composition_json(...)
```

Diagnostic inventory and shape-audit registration exists for `constitutional_view_composition`, `constitutional_process`, `constitutional_governance`, and `constitutional_fidelity`. No diagnostic or CLI evidence exposes a full operator-inquiry-to-bounded-question-to-selection pipeline.

### QuestionFamily adjacency

`seed_runtime/question_surface_inventory.py` contains exact `QuestionFamily` lookup, eligibility, selection, dispatch, definition, and explanation machinery. That machinery admits exact registered question-family text for bounded work and presentation, but the bounded-question slice already found that it does not translate an operator constitutional inquiry into the `BoundedConstitutionalQuestion` artifact consumed by Selection. Current inspection agrees: it is adjacent admission/dispatch machinery, not the constitutional pipeline producer.

## Current `BoundedConstitutionalQuestion` construction evidence

No implementation symbol named `BoundedConstitutionalQuestion` currently exists in `seed_runtime` or `tests`.

The closest construction evidence is test-only inline construction of `ConstitutionalQuestionProjection` with synthetic `bounded_question_id` values in `tests/test_constitutional_view_selection.py`, for example:

- `bounded-question:compatibility`
- `bounded-question:unsupported`
- `bounded-question:composition`
- `bounded-question:json`

Those are not `BoundedConstitutionalQuestion` producers. They are test-only projection fixtures used to exercise Selection. They skip operator inquiry intake and bounded-question construction.

The current implementation therefore has no deterministic `BoundedConstitutionalQuestion` producer, no named owner implemented in code, no compatibility adapter implementing that producer, and no public path that produces the artifact from an operator inquiry.

## Producer questions

1. **Does a deterministic `BoundedConstitutionalQuestion` producer already exist?**  
   No. The ownership boundary is recovered in `bounded_constitutional_question_slice_001.md`, but implementation code does not define a `BoundedConstitutionalQuestion` artifact or producer.

2. **If it exists, where is its ownership currently located?**  
   It does not exist in implementation. Architectural ownership is already recovered as `BoundedConstitutionalQuestion`; implementation ownership is absent, not compressed inside Selection or Composition.

3. **Is it a named owner, an inline construction, a test-only constructor, a compatibility adapter, or a compressed responsibility?**  
   Current code has only test-only inline `ConstitutionalQuestionProjection` fixture construction. There is no named bounded-question owner implemented. There is no compatibility adapter for operator inquiry to bounded question. There is no evidence that Selection or Composition compresses this producer because Selection explicitly refuses raw question consumption and Composition consumes explicit registered view names only.

4. **What exact inputs does it consume?**  
   No implemented producer consumes inputs. The recovered boundary and projection characterization imply the future producer should consume an operator constitutional inquiry plus explicit bounded fields sufficient to preserve inquiry provenance, bounded question text or identity, constitutional intent, scope status, uncertainty notes, and read-only / non-mutating flags. Current repository evidence does not justify natural-language grammar interpretation or authority creation as inputs.

5. **What exact artifact does it produce?**  
   No implemented artifact is produced today. The expected artifact is an immutable `BoundedConstitutionalQuestion` carrying the already-recovered question fields needed by deterministic Question Projection.

6. **Does it preserve operator inquiry provenance?**  
   No implemented producer exists. Existing characterization requires provenance preservation; current test-only projection fixtures preserve only a synthetic bounded question id and selection keys, not operator inquiry provenance.

7. **Does it preserve the distinction between testimony, evidence, and fact?**  
   No implemented producer exists. Existing Selection and Composition do preserve non-authority boundaries by refusing evidence discovery, constitutional recovery, mutation, and raw question consumption. A future producer must preserve operator inquiry as testimony/evidence rather than fact.

8. **Does it mutate repository state, persist authority, or promote claims?**  
   No implemented producer exists. Existing downstream Selection and Composition are read-only, do not write the event ledger, and do not mutate cluster state.

9. **Does it depend on authored constitutional knowledge that belongs elsewhere?**  
   No implemented producer exists. The lawful future producer should not depend on authored constitutional knowledge beyond explicit inputs and already-recovered bounded fields; Selection and Capability Projection consume registered capability keys elsewhere.

10. **Is its behavior deterministic from its explicit inputs?**  
    Not applicable in current implementation. The required next implementation is expected to be deterministic from explicit inputs.

11. **Are bounding, normalization, grammar interpretation, admission, projection, and authority currently compressed together?**  
    Not inside the current constitutional pipeline implementation. Projection fixture construction in tests compresses fixture setup only. QuestionFamily exact lookup/eligibility/dispatch is a separate surface, but it is not a `BoundedConstitutionalQuestion` producer. There is no evidence of production responsibility compressed with Selection or Composition.

12. **Is any such compression a genuine implementation-local ownership boundary?**  
    No. The only genuine boundary already recovered for this pressure is `BoundedConstitutionalQuestion`; implementation is missing rather than compressed in another owner. Test fixture shortcuts are not ownership boundaries.

13. **Can the producer be implemented directly without recovering new topology?**  
    Yes. Current evidence supports direct implementation realization inside the already recovered `BoundedConstitutionalQuestion` boundary.

14. **What existing consumer first requires the produced question?**  
    Deterministic Question Projection first requires it. Selection then consumes `ConstitutionalQuestionProjection`, not the raw bounded question. The implemented first downstream code consumer after projection is `select_constitutional_views(...)`.

15. **What is the narrowest compatibility-preserving implementation step?**  
    Add an immutable `BoundedConstitutionalQuestion` artifact and a deterministic producer/helper that preserves operator inquiry provenance and explicit bounded fields without changing Selection, Composition, CLI behavior, diagnostics, event ledger behavior, cluster mutation behavior, or existing tests.

## Producer inputs, output, and ownership location

### Current producer inputs

None in implementation.

### Expected lawful producer inputs for the next implementation step

The narrow input set supported by existing evidence is:

- operator inquiry as received;
- explicit bounded question text or identity;
- explicit constitutional intent or selection-key intent, if already supplied by the caller rather than inferred as fact;
- explicit scope/admission status;
- explicit uncertainty notes;
- explicit provenance/source label for the inquiry;
- read-only, event-ledger, and cluster-mutation boundary flags defaulting to non-mutating values.

Any grammar interpretation, semantic inference, autonomous question generation, evidence discovery, authority assertion, durable knowledge update, or projection-key derivation beyond explicit deterministic inputs would exceed current evidence.

### Current producer output

None in implementation.

### Expected lawful producer output

One immutable `BoundedConstitutionalQuestion` artifact. It should be a preservation artifact, not an authority artifact: it preserves the operator inquiry and bounded fields as evidence/provenance for downstream deterministic projection.

### Current producer ownership location

Architectural ownership is recovered in `bounded_constitutional_question_slice_001.md`; implementation ownership has not been realized. The responsibility is not owned by Selection, Composition, QuestionFamily lookup, CLI parsing, diagnostic inventory, or read-model registration.

## Provenance and testimony handling

Current downstream code provides strong negative evidence for authority promotion:

- Selection consumes only `ConstitutionalQuestionProjection` and `ConstitutionalCapabilityProjection`.
- Selection explicitly refuses raw question consumption, immutable constitutional view consumption, semantic reasoning, heuristics, planning, orchestration, evidence discovery, constitutional recovery, repository mutation, event-ledger writes, and cluster mutation.
- Composition consumes explicit registered view names only and refuses heuristic selection, evidence discovery, runtime reasoning, authority recovery, planning, orchestration, and repository mutation.

However, no current implementation preserves operator inquiry provenance before projection. Test-only `bounded_question_id` strings are not sufficient provenance. The next producer must carry the operator inquiry as received and preserve its evidentiary/testimonial status. It must not convert that inquiry into established fact, constitutional authority, repository truth, durable knowledge, authoritative capability claims, or selected view claims.

## Mutation, persistence, and authority findings

- `select_constitutional_views(...)` returns `SelectedConstitutionalViews` with `read_only=True`, `mutates_cluster=False`, and `writes_event_ledger=False` when inputs preserve those boundaries.
- `build_constitutional_view_composition(...)` returns `ConstitutionalViewCompositionArtifact` with `read_only=True`, `mutates_cluster=False`, and `writes_event_ledger=False`.
- Existing constitutional view/composition CLI surfaces render output but do not record a producer artifact or mutate cluster state.
- Diagnostic inventory and shape-audit surfaces exist for current public constitutional views/composition, but no full constitutional pipeline diagnostic exists.
- No inspected path persists `BoundedConstitutionalQuestion`, writes it to the event ledger, mutates repository state, or promotes operator testimony to fact.

## Compressed responsibilities found

No valid implementation-local ownership compression was found around `BoundedConstitutionalQuestion` production.

Rejected apparent compressions:

- **Test-only `ConstitutionalQuestionProjection` fixture construction**: invalid candidate. It is fixture setup, not production responsibility.
- **`QuestionFamily` exact lookup/eligibility/dispatch**: invalid candidate. It is existing bounded work admission/dispatch for registered public question-family rows, not a producer of the bounded constitutional question consumed by Selection.
- **CLI `--constitutional-view-composition` requested-view parsing**: invalid candidate. It is public composition plumbing for explicit view names, not operator inquiry intake or bounded-question construction.
- **Selection exact-key comparison**: invalid candidate. It is already implemented and characterized as irreducible Selection ownership; it refuses raw question consumption and does not own question construction.
- **Composition request creation**: invalid candidate. It preserves explicit registered-view composition and does not own selection or bounded-question construction.
- **Question Projection**: invalid ownership candidate. Repository evidence characterizes it as deterministic projection from `BoundedConstitutionalQuestion`, not a separate owner.
- **Capability Projection**: invalid ownership candidate. Repository evidence characterizes it as deterministic projection from registered contracts/views, not a separate owner.

## Classification under the four lawful outcomes

Selected lawful outcome: **Implementation Realization**.

Reasons:

- The missing work is a deterministic `BoundedConstitutionalQuestion` producer inside an already recovered boundary.
- The producer is not currently implemented under another name.
- The downstream Selection and Composition boundaries are implemented and preserve their boundaries.
- Question Projection and Capability Projection are characterized as deterministic projections, not ownership recovery work.
- No evidence exposes a new implementation-local ownership boundary satisfying the Candidate Standard.

Not selected:

- **Ownership Recovery**: rejected because no new compressed implementation-local responsibility is visible.
- **Projection Characterization**: rejected for the current pressure because Question Projection and Capability Projection are already characterized; the immediate missing artifact is the pre-projection bounded question producer.
- **Irreducible Boundary**: rejected for the producer itself because irreducibility applies to Selection; `BoundedConstitutionalQuestion` has already been recovered and now needs implementation.

## Adjacent pressure classifications

| Adjacent item | Classification | Basis |
| --- | --- | --- |
| `QuestionProjection` | Ready after producer | Already characterized as deterministic derivation from `BoundedConstitutionalQuestion`; implementation can follow after the artifact exists. |
| `CapabilityProjection` | Partially implemented | Projection record type exists as `ConstitutionalCapabilityProjection`, but deterministic production from contracts/registrations/views is not implemented. |
| End-to-end constitutional pipeline invocation | Ready after producer | Selection-to-Composition handoff exists; upstream bounded-question and projection producers are missing. |
| Public constitutional pipeline surface | Ready after producer | Current public surface composes explicit views only; a full pipeline surface should wait for producer/projection implementation. |
| Diagnostic exposure | Ready after producer | Any new operational surface must update diagnostic inventory and shape audit; no diagnostic surface should be added during this scout. |
| Integration wiring | Ready after producer | Existing adapter from `SelectedConstitutionalViews` to `ConstitutionalViewCompositionRequest` can be reused once upstream producers exist. |
| End-to-end provenance explanation | Ready after producer | Requires preserved operator inquiry provenance in the bounded-question artifact before explanation can lawfully surface it. |

## Candidate Standard evaluation

No valid new ownership recovery candidate exists.

- No candidate is independent: all apparent candidates are missing code, deterministic projection, public rendering/CLI plumbing, integration wiring, already-separated Selection/Composition responsibility, or test fixture setup.
- No candidate is sequential: after producer implementation, likely adjacent work remains deterministic projection, public/diagnostic exposure, integration wiring, tests, or documentation.
- All inspected candidates are invalid under the Candidate Standard because they either re-describe the already recovered `BoundedConstitutionalQuestion`, duplicate existing Selection/Composition ownership, or speculate beyond implementation evidence.

## Lawful Architectural Stopping determination

The Lawful Stopping Test passes.

Remaining pressure consists only of:

- deterministic producer implementation for `BoundedConstitutionalQuestion`;
- deterministic Question Projection implementation;
- deterministic Capability Projection implementation;
- compatibility-preserving integration wiring;
- public surface work after producers exist;
- diagnostic surface work if new operational visibility is exposed;
- tests;
- documentation/reporting.

No inspected evidence breaks the stopping condition. The fact that the full pipeline cannot yet run end to end does not prove architectural incompleteness.

Conclusion:

```text
Lawful Architectural Stopping still applies.
Remain in implementation mode.
```

## Exact recommended next command

Recommendation category: **Implementation realization**.

Recommended exact target:

```text
Implement the deterministic BoundedConstitutionalQuestion producer.
```

Narrow command shape for the next implementation session:

```text
Implement an immutable BoundedConstitutionalQuestion artifact and deterministic producer/helper from explicit operator-inquiry inputs, preserving inquiry provenance, testimony/evidence boundaries, uncertainty, read-only status, writes_event_ledger=false, and mutates_cluster=false, without changing Selection or Composition.
```

## Expected implementation files likely affected by next command

Likely new or modified files:

- `seed_runtime/constitutional_bounded_question.py` or a similarly narrow module name under `seed_runtime/`.
- `seed_runtime/constitutional_view_selection.py` only if type-level compatibility needs imports or a projection helper in a later step; this scout recommends not modifying Selection for the producer itself.
- Possibly `seed_runtime/__init__.py` if repository packaging conventions require export; current evidence does not require it.

Files not expected to change for the producer-only step:

- `seed_runtime/constitutional_view_composition.py`
- `scripts/seed_local.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`

Those should wait until projection, public surface, or diagnostic exposure work.

## Expected test neighborhoods

Likely new or modified tests:

- A new `tests/test_constitutional_bounded_question.py`, or equivalent narrow producer test file.
- Later, `tests/test_constitutional_view_selection.py` when Question Projection production is implemented and Selection can be exercised from real bounded-question artifacts.
- Later, `tests/test_constitutional_view_composition.py` only if end-to-end wiring changes composition consumption.
- Later, `tests/test_diagnostic_inventory.py` and `tests/test_diagnostic_shape_audit.py` only if a new diagnostic, CLI, probe, view, recordable output, or operational surface is added.

Producer-only tests should prove:

- immutable artifact shape;
- deterministic output from explicit inputs;
- operator inquiry preserved as received;
- provenance/source preserved;
- uncertainty preserved;
- no authority/fact/capability promotion fields;
- `read_only=True`;
- `writes_event_ledger=False`;
- `mutates_cluster=False`.

## Compatibility risks

- Adding a producer should not change existing Selection fixture behavior or Composition CLI behavior.
- Introducing automatic selection-key derivation from natural language would create compatibility and authority risk; it should be avoided unless a later deterministic projection contract authorizes it.
- Reusing `QuestionFamily` admission machinery as if it were the constitutional bounded-question producer would risk conflating registered public question-family dispatch with constitutional inquiry preservation.

## Schema risks

- The bounded-question artifact schema must preserve enough fields for deterministic Question Projection without embedding projection ownership prematurely.
- Avoid adding durable persistence schema, event-ledger event schema, diagnostic fact schema, or cluster-state schema for producer-only implementation.
- Avoid fields that imply truth, authority, verified capability, established fact, or repository knowledge.

## Provenance risks

- Highest risk: silently promoting operator inquiry text into fact or constitutional authority.
- The producer should label operator input as inquiry/testimony/evidence/provenance, not as repository truth.
- If caller-supplied bounded fields include intent or scope, the artifact should preserve their supplied/provenance character and uncertainty, not infer validity beyond explicit inputs.
- Do not derive constitutional knowledge from presentation vocabulary without implementation evidence.

## Read-only scout confirmation

No implementation files were changed.

No test files were changed.

No slice report was created.

No PR metadata was created during scout authoring.

Only `constitutional_pipeline_implementation_scout_001.md` is intended for commit.

## Commit hash for scout report commit

Scout report creation commit: `9022aa5`.

Current pressure classification:

Implementation Realization — deterministic `BoundedConstitutionalQuestion` producer.

Lawful Architectural Stopping:

Still applies. Remain in implementation mode.

Recoverable ownership candidates:

None. Apparent candidates are missing code, deterministic projections, public/diagnostic surfaces, integration wiring, test fixtures, or already-separated Selection/Composition responsibilities.

Recommended next mode:

Implementation realization.

Recommended exact target:

Implement the deterministic `BoundedConstitutionalQuestion` producer as an immutable provenance-preserving, read-only, non-mutating artifact/helper from explicit operator-inquiry inputs.

Reason:

Repository evidence supports the constitutional pipeline as architecturally complete; Selection and Composition are implemented; Question Projection and Capability Projection are deterministic projections; the missing bounded-question producer is not implemented and does not require new ownership recovery.
