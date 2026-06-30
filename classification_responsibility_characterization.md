# Classification Responsibility Characterization

## Executive answer

Completed responsibility-family audits keep pointing to **Classification** because, after they finish their local answer, selection, reasoning, evidence, rendering, or navigation separations, the remaining work is often the same bounded act: assign an already-collected object to an explicit status bucket and expose the boundary of that assignment.

The recurring bounded work is **categorization of existing implementation evidence**, not interpretation, authority ownership, evidence ownership, rendering, navigation, dispatch, or schema redesign.

The repository already contains several implementation-backed classification surfaces:

- entity type / unknown coverage classification from projected `State`;
- operational CLI surface classification from argparse and diagnostic inventory evidence;
- inquiry artifact visibility classification from repository-visible artifact evidence;
- question-family bounded status / eligibility classification from static inventory and dispatch maps.

However, current evidence is **not sufficient to recommend a Classification ownership recovery**. The pattern is recurring and implementation-backed as a *destination*, but no single compressed implementation owner or lifecycle has been shown. Classification is implemented locally by multiple surfaces with different inputs, outputs, and authority boundaries.

Required recovery answer:

```text
Insufficient implementation evidence.
```

## Implementation reviewed

Primary implementation reviewed:

- `seed_runtime/classification_coverage.py`
- `seed_runtime/operational_surface_inventory.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/question_surface_inventory.py`
- `scripts/seed_local.py`
- `tests/test_classification_coverage.py`
- `tests/test_operational_surface_inventory.py`
- `tests/test_inquiry_artifacts.py`
- `tests/test_question_surface_inventory.py`

Primary investigation and audit artifacts reviewed:

- `answer_composition_projection_navigation_audit.md`
- `reasoning_path_answer_composition_completion_audit.md`
- `question_bounded_work_invocation_investigation.md`
- `question_family_registration_boundary_audit.md`
- `docs/question_family_artifact_reconciliation.md`
- related pressure, capability, selection, reasoning, evidence, and inquiry artifact references found by repository search.

Commands used during this investigation:

```bash
rg -n "Classification|classification|Answer Composition|InquiryArtifactVisibility|Pressure Visibility|Capability Verification|Selection Path|Reasoning Path|Evidence Interpretation|question_surface_inventory" .
rg -n "belongs to Classification|Classification ownership|Classification family|remaining.*Classification|assign.*Classification|reassign.*Classification|not Classification|Classification should|classification/evaluation" *.md docs/*.md
sed -n '1,220p' reasoning_path_answer_composition_completion_audit.md
sed -n '1,260p' answer_composition_projection_navigation_audit.md
sed -n '1,220p' question_bounded_work_invocation_investigation.md
sed -n '1,210p' question_family_registration_boundary_audit.md
sed -n '1,140p' seed_runtime/question_surface_inventory.py
sed -n '140,260p' seed_runtime/operational_surface_inventory.py
sed -n '1,140p' seed_runtime/classification_coverage.py
sed -n '1,160p' seed_runtime/inquiry_artifacts.py
sed -n '1,120p' tests/test_classification_coverage.py
sed -n '1,120p' tests/test_operational_surface_inventory.py
sed -n '1,90p' tests/test_inquiry_artifacts.py
```

## Completed families reviewed

### Answer Composition

Answer Composition completion evidence repeatedly shows completed local composition work stopping when the remaining concern is not answer grammar. In `ReasoningPathAudit`, the remaining grouped payload after answer-composition separations is `_DerivationLineagePayload(consumers, story_impact, unknowns)`, and the audit assigns that residue to derivation lineage, consumer explanation, operational-story impact, and reasoning-specific unknowns rather than Answer Composition.

The projection navigation audit is the strongest direct evidence for the Classification handoff. It says `InquiryArtifactVisibility` still has classification adjacent to evidence and limitations; it characterizes the stronger remaining work as classification/evaluation of repository visibility, not bounded answer composition. It also lists inquiry artifact residual work as classification/evaluation and states that the artifact surface explicitly refuses inquiry graph creation, pressure transformation inference, workflow, and planning.

### Selection Path

Selection Path is a counterexample to over-broad Classification. The Answer Composition navigation audit says `SelectionPathAudit` reached local Answer Composition completion and that candidate ordering, non-selected candidate reasoning, factor derivation, and unknown target handling are selection algorithm explanation and lineage concerns. That means completed Answer Composition does **not** assign selection mechanics to Classification.

### Reasoning Path

Reasoning Path is also a counterexample to over-broad Classification. The Reasoning Path Answer Composition completion audit stops at derivation lineage, consumer lineage, operational-story impact, and reasoning-specific unknowns. It does not assign derivation construction or evidence interpretation to Classification.

### InquiryArtifactVisibility

`InquiryArtifactVisibility` is the clearest recurring destination. Its public record is `artifact`, `classification`, `evidence`, and `limitations`; private payloads separate supporting evidence and limitations for some rows; the boundary explicitly refuses recording, ledger writes, cluster mutation, inquiry movement inference, inquiry graph creation, pressure transformation inference, and workflow/planning behavior. The implementation therefore has a narrow classification role: assign artifact visibility status based on listed evidence while refusing adjacent responsibilities.

### Question-family / bounded work investigations

Question-family work shows classification-like status assignment without natural-language interpretation. `question_surface_inventory.py` derives bounded ask status from static maps: required-argument families are `eligible_with_parameters`, dispatch-mapped families are `eligible_now`, diagnostic-only families are `diagnostic_only`, and everything else is `not_dispatchable`. The bounded dispatch request docstring explicitly says it does not decide QuestionFamily lookup, eligibility, bounded work selection, evidence interpretation, answer composition, rendering, or semantic routing. This is status categorization and invocation description, not a generic classifier.

## Recurring reassignment evidence

| Completed or bounded family | Work it refuses to own | Destination it names or exposes | Evidence-backed characterization |
| --- | --- | --- | --- |
| Answer Composition / `InquiryArtifactVisibility` | Artifact visibility result assignment after evidence and limitations are present | classification/evaluation | Assign artifact to visibility category; do not create inquiry graph, infer movement, infer pressure transformation, plan, or mutate. |
| Answer Composition / `SelectionPathAudit` | Candidate ordering, non-selected alternatives, factor derivation | Selection Path | Not Classification; these remain selection lineage and algorithm explanation. |
| Answer Composition / `ReasoningPathAudit` | Consumers, story impact, derivation unknowns | Reasoning Path | Not Classification; these remain derivation lineage and reasoning-specific unknowns. |
| Question bounded work | Free-text question meaning, answer composition, rendering, evidence interpretation | exact status / eligibility maps | Categorize exact registered family as eligible, parameterized, diagnostic-only, or not dispatchable. |
| Operational visibility | CLI option semantics beyond registered/parser evidence | operational surface classification audit | Categorize parser-discovered surfaces as primary/filter/modifier/debug/manual/legacy/unknown using deterministic implementation evidence. |
| Entity type coverage | Evidence truth, graph authority, cluster mutation | classification coverage diagnostic | Count projected current entity types and unknown-type impacts; diagnostic is non-mutating. |

## Classification responsibilities

Implementation-backed Classification responsibilities are bounded and local:

1. **Status assignment for known subjects.** Classification begins when an implementation already has a bounded subject: an entity in projected state, a CLI flag from argparse, an inquiry artifact row, or an exact question-family string.

2. **Deterministic categorization from existing evidence.** Classification assigns categories from implementation evidence already produced elsewhere. For entity coverage, the diagnostic reads `state.current_entity_types`, counts known and unknown entities, and reports distributions and unknown impacts. For operational surfaces, the audit iterates parser options, calls `_classification_for`, and stores the resulting category and reason. For question families, status is derived from static dispatch, required-argument, and diagnostic-only maps.

3. **Boundary exposure.** Classification surfaces preserve what their status means and does not mean. `InquiryArtifactVisibility` exposes a boundary denying recording, event-ledger writes, cluster mutation, inquiry movement inference, inquiry graph creation, pressure transformation inference, workflow, and planning. `classification_coverage` calls itself a non-mutating diagnostic.

4. **Conservative unknown handling.** Unknown is treated as a valid output category, not as permission to infer. Entity classification coverage counts unknown entities; inquiry artifacts include `unknown` as `repository_visible` only because specific repository evidence supports that artifact row; question-family eligibility returns `not_dispatchable` when no current map supports dispatch.

## Classification non-responsibilities

The implementation evidence rejects the following as Classification responsibilities:

1. **Interpretation.** Classification does not interpret free-text operator intent or semantic meaning in the bounded ask path. Exact registered family strings are required, and dispatch consumes inventory/map data rather than recovered family objects or prose meaning.

2. **Authority.** Classification does not own authority. Question-family rows carry authority-boundary text, but bounded status is map-derived; authority evaluators and diagnostic inventories remain separate surfaces.

3. **Evidence.** Classification does not own evidence production. Entity coverage consumes projected state; operational surface classification consumes argparse and diagnostic inventory; inquiry artifact classification lists evidence strings; reasoning and selection surfaces produce their own evidence and lineage.

4. **Rendering.** Classification does not own rendering. Formatter and JSON functions render already-built audits or diagnostics.

5. **Navigation.** Classification does not own inquiry navigation, source navigation, lexical matching, or continuation. Completed Answer Composition audits assign those residues to inquiry navigation/evidence collection or to their native family, not Classification.

6. **Selection.** Classification does not own candidate ordering, non-selected candidate reasoning, selection factors, or unknown target handling. These remain Selection Path responsibilities.

7. **Reasoning / evidence interpretation.** Classification does not own derivation construction, consumer lineage, operational-story impact, or reasoning-specific unknowns. These remain Reasoning Path responsibilities.

8. **Mutation or truth promotion.** Classification diagnostics are read-only unless a specific record path exists; even recordable diagnostic output is diagnostic self-observation, not cluster mutation or authoritative truth promotion.

## Where Classification begins

Classification begins after the subject and source evidence are already established:

```text
bounded subject + existing implementation evidence -> category/status assignment
```

Examples:

- `State.current_entity_types` already exists before `build_classification_coverage_diagnostic` counts host/service/unknown distribution.
- argparse actions already exist before `build_operational_surface_classification_audit` assigns surface categories.
- `QuestionSurfaceInventoryRow` and dispatch maps already exist before bounded status is derived.
- Inquiry artifact evidence and limitations are already enumerated before the artifact receives a visibility classification.

## Where Classification stops

Classification stops at the category/status result plus reason/boundary. It does not proceed into:

- collecting new evidence;
- interpreting meaning;
- selecting candidates;
- navigating source material;
- authorizing truth;
- composing answers;
- rendering output;
- mutating event ledger or cluster state;
- recovering new ownership.

## Counterexamples

### Classification absorbing Evidence Interpretation

No implementation evidence found. `ReasoningPathAudit` retains derivation evidence and conclusions as reasoning-path material, and its completion audit assigns the remaining residue to derivation lineage, consumer lineage, story impact, and reasoning unknowns rather than Classification. `InquiryArtifactVisibility` lists evidence beside classification, but the boundary is visibility categorization; it does not interpret findings into cluster truth or inquiry movement.

### Classification absorbing Selection

Counterexample found. Selection residual work is explicitly Selection Path ownership: candidate ordering, non-selected candidate reasoning, factor derivation, and unknown target handling are selection algorithm explanation and lineage concerns, not Answer Composition and not Classification.

### Classification absorbing Navigation

Counterexample found. Inquiry orientation residual work is described as lexical matching, source navigation, inquiry-note preservation, and presentation; those are evidence collection, inquiry navigation, or rendering concerns rather than Answer Composition. They are also not recovered as Classification.

### Classification absorbing Authority

No evidence found. Question-family inventory rows expose authority boundaries, but bounded ask status comes from dispatch maps. Classification coverage consumes projected type state; it does not declare authority over entity truth. Inquiry artifact boundaries explicitly deny mutation and inference.

### Completed families that do not reassign remaining work to Classification

Counterexamples found:

- `ReasoningPathAudit` Answer Composition completion assigns remainder to Reasoning Path.
- `SelectionPathAudit` Answer Composition completion assigns remainder to Selection Path.
- Operational story residual work remains upstream operational visibility, pressure, capability, privilege, correlation, impact, or rendering work.

These counterexamples prevent claiming that every completed family terminates at Classification.

## Supported conclusions

1. **Completed families point to Classification when the leftover work is category/status assignment over already-collected evidence.** The clearest case is `InquiryArtifactVisibility`, where classification/evaluation of repository visibility remains after answer-composition concerns are bounded.

2. **The recurring bounded work is categorization, not interpretation.** The repeated pattern is: subject is known, evidence exists, implementation assigns a conservative category/status and exposes boundary.

3. **Classification begins after evidence and subject selection.** It requires an already-bounded object such as an entity, CLI flag, artifact row, or exact question family.

4. **Classification stops before authority, evidence production, rendering, navigation, selection, and reasoning.** Multiple counterexamples keep those concerns in their native families.

5. **Classification is emerging as recurring vocabulary backed by multiple local implementations, but not yet as one recovered responsibility family.** There are local deterministic classifiers/status assigners, but no shared owner, lifecycle, compressed implementation object, or cross-surface recovery target.

6. **There is not sufficient implementation evidence to justify Classification ownership recovery now.** Recurrence is visible, but recurrence alone is not enough under the repository's non-promotion rules.

## Unsupported conclusions

The following conclusions are unsupported by current implementation evidence:

- Classification should become a framework.
- Classification should become a shared classifier.
- Classification owns semantic interpretation.
- Classification owns authority.
- Classification owns evidence.
- Classification owns rendering.
- Classification owns navigation.
- Classification owns selection.
- Classification owns reasoning-path derivation.
- Classification should recover ownership now.
- Similar uses of the word `classification` prove a single responsibility family.

## Direct answers to requested questions

### 1. Why do completed families repeatedly terminate at Classification?

Because once a completed family has separated its own local responsibilities, the residue is sometimes only the act of assigning a status to already-bounded material. Answer Composition can compose answer, reason, support, boundary, and limitations; it should not decide artifact visibility categories. Selection Path can explain selection; it should not be recast as answer composition. Reasoning Path can explain derivation; it should not be recast as classification.

### 2. What recurring bounded work is being reassigned?

The recurring bounded work is conservative category/status assignment over existing implementation evidence: artifact visibility categories, entity known/unknown type coverage, operational surface categories, and question-family bounded eligibility statuses.

### 3. What implementation responsibilities belong to Classification?

Classification owns local deterministic categorization, reason/status recording, unknown handling, and boundary visibility for the categorized subject.

### 4. Which responsibilities explicitly do not belong to Classification?

Interpretation, authority, evidence production, rendering, navigation, selection, reasoning derivation, truth promotion, workflow/planning, event-ledger mutation, and cluster mutation do not belong to Classification under current evidence.

### 5. Is Classification emerging as a recurring responsibility family, or are completed families merely using similar vocabulary?

It is more than merely similar vocabulary because the repository has multiple deterministic category/status implementations. But it is not yet a recovered responsibility family because those implementations are local, heterogeneous, and not shown to share one compressed owner.

### 6. Is there sufficient implementation evidence to justify a Classification ownership recovery?

```text
Insufficient implementation evidence.
```

The repository demonstrates recurring classification-like work, but not recurring compressed implementation ownership that should be recovered as a bounded Classification family.

## Confidence

- **High confidence** that current classification work is categorization/status assignment over existing evidence.
- **High confidence** that Classification does not own selection, reasoning derivation, rendering, navigation, authority, or evidence production.
- **Medium confidence** that Classification is an emerging recurring responsibility destination, because the pattern appears in multiple independent surfaces but remains locally implemented.
- **High confidence** that ownership recovery is not justified by current implementation evidence.

## Recommendation

Do not recover Classification ownership now.

The bounded recommendation is characterization only: preserve the current local classification boundaries and require future recovery, if ever requested, to demonstrate recurring compressed implementation ownership rather than repeated use of the word `classification`.
