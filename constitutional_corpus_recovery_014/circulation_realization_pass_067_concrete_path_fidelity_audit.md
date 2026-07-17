# Circulation Realization Pass 067 — Concrete-path Fidelity Audit

Repository authority wins.

## Selected path

The audited path is a lawful partial implementation path already evidenced by tests:

`produce_bounded_constitutional_question` → `project_constitutional_question` → `select_constitutional_views` → `selected_constitutional_views_to_composition_request` → `build_constitutional_view_composition` → composition JSON/human rendering.

This is not a canonical happy path. It supports unsupported keys, preserved uncertainty, bounded compatibility answers, and read-only local stop.

## Seam audit

### Seam 1 — Operator expression to bounded question

- **Standing/value entering:** operator inquiry, provenance, bounded question, intent, scope status, uncertainty, Unknowns, caller fields.
- **Local act:** `produce_bounded_constitutional_question` freezes explicit caller values and creates deterministic identity.
- **Invariants:** source wording/provenance preserved; testimony remains evidence; no fact, repository truth, capability, selection, projection, ledger write, or cluster mutation.
- **Consumer receives:** `BoundedConstitutionalQuestion`.
- **Stronger standing forbidden:** established fact, verified claim, constitutional authority, selected view, projection.
- **Test preservation:** `tests/test_bounded_constitutional_question.py` proves exact provenance, no promotion, immutability, and read-only behavior.
- **Fidelity:** faithful for this bounded family.

### Seam 2 — Bounded question to question projection

- **Standing/value entering:** bounded question identity plus caller-supplied selection fields, uncertainty, Unknowns.
- **Local act:** `project_constitutional_question` emits only exact selection keys and maps Unknowns into uncertainty.
- **Invariants:** no raw operator inquiry crosses; no semantic inference; no downstream artifacts; read-only flags preserved.
- **Consumer receives:** `ConstitutionalQuestionProjection`.
- **Stronger standing forbidden:** capability support, view selection, established answer, registered view name.
- **Test preservation:** `tests/test_constitutional_question_projection.py` proves exact-key projection, no testimony promotion, no guessing, no mutation, and Selection consumption.
- **Fidelity:** faithful for explicit caller-key projection.

### Seam 3 — Question/capability projections to selected views

- **Standing/value entering:** selection keys and uncertainty from question projection; registered capability projections.
- **Local act:** `select_constitutional_views` admits only exact key matches to registered view names and preserves unsupported keys as uncertainty.
- **Invariants:** unsupported keys remain visible; selected names do not become raw views, truth, ranking, plan, or orchestration.
- **Consumer receives:** `SelectedConstitutionalViews`.
- **Stronger standing forbidden:** full view artifact consumption, semantic reasoning, evidence discovery, neighboring inquiry closure.
- **Test preservation:** `tests/test_constitutional_view_selection.py` proves selection artifact, unsupported uncertainty, no mutation, and no raw view consumption.
- **Fidelity:** faithful as a local admission artifact.

### Seam 4 — Selected views to composition request

- **Standing/value entering:** bounded-question identity, selected registered view names, selection uncertainty, compatibility answer, and read-only boundaries.
- **Local act before pass 068:** `selected_constitutional_views_to_composition_request` forwarded selected view names, purpose, and output format into `ConstitutionalViewCompositionRequest`.
- **Consumer receives before pass 068:** a composition request without bounded-question identity or selection uncertainty.
- **Invariants that must survive:** partial/unsupported selection uncertainty, bounded-question identity, and negative authority that Selection did not resolve unsupported keys.
- **Stronger standing forbidden:** composition must not treat selected view names as all requested standing, complete support, or resolved uncertainty.
- **Test preservation before pass 068:** tests proved requested views and compatibility answer, but did not prove selection uncertainty survived into Composition.
- **Fidelity before pass 068:** unfaithful/partial. The request compressed Selection's artifact into a view-name list, so Composition owned a result without the upstream limits that selected the views.

### Seam 5 — Composition request to bounded composition result

- **Standing/value entering:** explicit requested registered views, composition purpose, output format.
- **Local act:** `build_constitutional_view_composition` reads registered constitutional views, correlates existing evidence, preserves contributing Unknowns/refusals, and forms a bounded artifact.
- **Invariants:** registered views only; no evidence discovery; no runtime reasoning; no constitutional or implementation authority; no recording; no mutation.
- **Consumer receives:** `ConstitutionalViewCompositionArtifact`.
- **Stronger standing forbidden:** global truth, completion, authority, mutation.
- **Test preservation:** composition path tests prove compatibility and request identity; after pass 068 they must also prove selection uncertainty preservation.
- **Fidelity:** faithful for registered-view composition once Seam 4 carries selection limits.

### Seam 6 — Composition artifact to outward representation

- **Standing/value entering:** bounded artifact with evidence, Unknowns, refusals, compatibility answer, boundaries.
- **Local act:** JSON/human format helpers render the artifact.
- **Consumer receives:** text or JSON-ready values.
- **Stronger standing forbidden:** receipt, reliance, action, correction, or reopening.
- **Test preservation:** bounded helper tests exist but selected path is availability-only.
- **Fidelity:** partial; no delivery/receipt path is selected or required.

## Blocking implementation-local ownership boundary

The smallest actionable boundary is the Selection-to-Composition handoff. Selection owns the admission artifact and its unresolved uncertainty; Composition owns the bounded result. The bridge compressed the handoff to `requested_views`, so Composition could not preserve Selection's upstream limits as part of its request/result artifact. Recovering this boundary requires Composition's request to accept bounded-question identity and selection uncertainty as preserved limits, and the Selection-owned bridge to populate them without granting stronger authority.
