# Circulation Realization Pass 066 — Implementation Witness Map

Repository authority wins.

## Orientation

This pass maps R1 through R9 to implementation witnesses without changing runtime code. Classification follows concrete producer, artifact, consumer, ownership, authority boundary, tests, diagnostics/public surfaces, mutation behavior, and unsupported neighboring topology.

## Witness map

### R1 — External or operator expression to addressable pressure

- **Classification:** directly witnessed for bounded constitutional-question production.
- **Producer:** caller of `produce_bounded_constitutional_question` supplies `operator_inquiry`, `inquiry_provenance`, bounded fields, uncertainty, Unknowns, and caller fields.
- **Act:** deterministic bounded production preserves operator testimony as evidence and refuses fact, authority, capability, selection, projection, ledger, or mutation promotion.
- **Artifact crossing boundary:** frozen `BoundedConstitutionalQuestion`.
- **Consumer:** `project_constitutional_question` may consume it; formatting/JSON helpers may render it.
- **Local owner:** `seed_runtime.bounded_constitutional_question`.
- **Authority/preservation boundary:** `testimony_status` and `read_only_boundaries` preserve source testimony and negative authority.
- **Tests:** `tests/test_bounded_constitutional_question.py` proves exact provenance preservation, no promotion, immutability, deterministic identity, and no mutation.
- **Diagnostics/public surfaces:** bounded helper has JSON/human rendering helpers, but no standalone CLI diagnostic witness was selected.
- **Mutation behavior:** read-only, `writes_event_ledger=False`, `mutates_cluster=False`.
- **Unsupported neighboring topology:** no generic operator-ingress parser, no constitutional authority creation from raw wording, no automatic projection.

### R2 — Addressable pressure to translated need or possible inquiry

- **Classification:** directly witnessed for bounded constitutional-question to deterministic selection projection.
- **Producer:** `project_constitutional_question` consumes `BoundedConstitutionalQuestion`.
- **Act:** projects only bounded-question identity, exact caller-supplied selection keys, and uncertainty/Unknowns into Selection's uncertainty channel.
- **Artifact crossing boundary:** frozen `ConstitutionalQuestionProjection`.
- **Consumer:** `select_constitutional_views`.
- **Local owner:** `seed_runtime.constitutional_view_selection` owns the projection type and projection helper.
- **Authority/preservation boundary:** raw operator inquiry and provenance do not cross; uncertainty and Unknowns cross as limits; no semantic matching or downstream artifact is created.
- **Tests:** `tests/test_constitutional_question_projection.py` proves projection accepts a real bounded question, preserves identity/uncertainty, does not promote testimony, does not guess missing keys, and can be consumed by Selection.
- **Diagnostics/public surfaces:** JSON helper for selected views; no diagnostic registration changed.
- **Mutation behavior:** read-only, no ledger write, no cluster mutation.
- **Unsupported neighboring topology:** no natural-language interpretation, no admission from prompt restatement, no capability discovery.

### R3 — Possible inquiry to admitted inquiry movement

- **Classification:** partially witnessed as deterministic local Selection admission.
- **Producer:** `select_constitutional_views` consumes `ConstitutionalQuestionProjection` and `ConstitutionalCapabilityProjection` values.
- **Act:** exact-key comparison admits only registered view names supported by capability projections and preserves unsupported keys as uncertainty.
- **Artifact crossing boundary:** frozen `SelectedConstitutionalViews`.
- **Consumer:** `selected_constitutional_views_to_composition_request` and JSON helper.
- **Local owner:** Constitutional View Selection in `seed_runtime.constitutional_view_selection`.
- **Authority/preservation boundary:** selected view names are not raw views, not constitutional truth, not ranking, not planning, and not orchestration.
- **Tests:** `tests/test_constitutional_view_selection.py` proves immutable artifact production, unsupported uncertainty preservation, and no mutation.
- **Diagnostics/public surfaces:** selection JSON helper only; no CLI diagnostic path selected.
- **Mutation behavior:** read-only, no ledger write, no cluster mutation.
- **Unsupported neighboring topology:** no universal inquiry admission owner; no semantic admission; no automatic neighboring inquiry retirement.

### R4 — Admitted movement to bounded examination eligibility

- **Classification:** directly witnessed in the bounded family of constitutional view composition.
- **Producer:** `selected_constitutional_views_to_composition_request` converts selected registered view names to a `ConstitutionalViewCompositionRequest`.
- **Act:** makes explicit requested-view composition eligibility without consuming raw question text or immutable view artifacts.
- **Artifact crossing boundary:** `ConstitutionalViewCompositionRequest`.
- **Consumer:** `build_constitutional_view_composition`.
- **Local owner:** the bridge is owned by Selection; the request and composition eligibility contract are owned by Composition.
- **Authority/preservation boundary:** eligibility is explicit request only, not execution authority beyond read-only composition, not evidence discovery, and not constitutional recovery.
- **Tests:** `tests/test_constitutional_view_selection.py` proves selected views wire into the composition contract.
- **Diagnostics/public surfaces:** composition has format/JSON helper and registered read-model public surfaces indirectly through contributing views.
- **Mutation behavior:** read-only, no ledger write, no cluster mutation.
- **Unsupported neighboring topology:** no method selector across all inquiries; no universal examination-eligibility envelope.

### R5 — Examination output to scoped finding standing

- **Classification:** witnessed only for the bounded family of composition over registered constitutional read models.
- **Producer:** registered constitutional view builders called by `build_constitutional_view_composition`.
- **Act:** reads each explicitly requested registered view, extracts existing composition evidence, Unknowns, refusals, and compatibility answers.
- **Artifact crossing boundary:** `ConstitutionalContributingView` entries and correlated evidence/Unknown/refusal tuples inside `ConstitutionalViewCompositionArtifact`.
- **Consumer:** formatted/JSON composition output and downstream operator-facing report use.
- **Local owner:** `seed_runtime.constitutional_view_composition`.
- **Authority/preservation boundary:** only registered constitutional read models are consumed; evidence is correlated, not discovered; Unknowns/refusals are preserved.
- **Tests:** composition tests and selection tests exercise this handoff through `build_constitutional_view_composition`.
- **Diagnostics/public surfaces:** contributing view records include CLI flag, inventory name, and shape-audit name from read-model contracts.
- **Mutation behavior:** read-only, no ledger write, no cluster mutation.
- **Unsupported neighboring topology:** no general finding engine, no source-independent truth formation.

### R6 — Scoped finding to bounded result

- **Classification:** directly witnessed for composition artifact formation.
- **Producer:** `build_constitutional_view_composition`.
- **Act:** forms `ConstitutionalViewCompositionArtifact` with bounded summary, correlated existing evidence, preserved Unknowns/refusals, compatibility answer, and read-only boundaries.
- **Artifact crossing boundary:** `ConstitutionalViewCompositionArtifact`.
- **Consumer:** `constitutional_view_composition_json` and `format_constitutional_view_composition`.
- **Local owner:** Constitutional View Composition.
- **Authority/preservation boundary:** result is bounded explanation only; no runtime reasoning, evidence discovery, constitutional authority, implementation authority, recording, event-ledger write, or cluster mutation.
- **Tests:** composition and selection tests prove bounded artifact creation and compatibility answer preservation.
- **Diagnostics/public surfaces:** human/JSON rendering helpers.
- **Mutation behavior:** read-only, no ledger write, no cluster mutation.
- **Unsupported neighboring topology:** no global completion claim and no neighboring-inquiry closure.

### R7 — Bounded result to outward representation

- **Classification:** partially witnessed.
- **Producer:** `format_constitutional_view_composition` and `constitutional_view_composition_json`.
- **Act:** render the bounded composition artifact to human text or JSON-ready data.
- **Artifact crossing boundary:** rendered text or JSON dictionary.
- **Consumer:** CLI/API/report caller if wired by a public surface.
- **Local owner:** Composition rendering helpers.
- **Authority/preservation boundary:** rendering does not mutate and should preserve Unknown/refusal/read-only limits.
- **Tests:** formatting and JSON coverage exists for related bounded surfaces; selected path lacked full outward delivery tests before pass 068.
- **Diagnostics/public surfaces:** helper-level public surface; no new operational CLI flag.
- **Mutation behavior:** read-only helper behavior.
- **Unsupported neighboring topology:** no proof of receipt, reliance, action, or universal delivery record.

### R8 — Representation to delivered or available standing

- **Classification:** not required on the selected repository path.
- **Witness:** repository contains many CLI/diagnostic surfaces, but the selected bounded question→selection→composition path stops at renderable artifact availability rather than proof of delivery.
- **Unsupported neighboring topology:** no implementation witness proves operator receipt, understanding, reliance, or action for this path.

### R9 — Operator response to new ingress pressure

- **Classification:** unsupported on the selected repository path.
- **Witness:** no selected implementation path consumes a response to a delivered composition artifact and converts it to new bounded pressure.
- **Unsupported neighboring topology:** no correction, supersession, reopening, or response-admission owner is evidenced for this path.

## Orientation result

The strongest implementation-evidenced path is bounded constitutional-question production → question projection → view selection → composition request → composition artifact → formatting/JSON availability. The most compressed boundary is Selection-to-Composition: before pass 068 evidence, the bridge forwarded selected view names but did not carry bounded-question identity or selection uncertainty into Composition's owned request/result boundary, risking an apparent strengthening from partial selected movement into a composition result with selection limits absent.
