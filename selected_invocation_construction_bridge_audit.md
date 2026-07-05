# Selected Invocation Construction Bridge Audit

## Reviewed evidence

This audit inspected the bridge from both sides without recovering a new implementation neighborhood, assigning ownership, or recommending implementation.

Construction-side evidence reviewed:

- `BoundedWorkSelectedSurfaceValue` and `bounded_work_selected_surface_value_for_eligibility(...)` in `seed_runtime/question_surface_inventory.py`.
- `BoundedWorkSelectedDispatchSurface` and `bounded_work_selected_dispatch_surface_for_eligibility(...)` in `seed_runtime/question_surface_inventory.py`.
- `BoundedWorkSelectionResult` and `bounded_work_selection_for_question_family(...)` in `seed_runtime/question_surface_inventory.py`.
- `BoundedWorkDispatchRequest` and `bounded_work_dispatch_request_for_selection(...)` in `seed_runtime/question_surface_inventory.py`.
- Selected-piece and request-construction tests in `tests/test_question_surface_inventory.py`.

Consumer-side evidence reviewed:

- `execute_bounded_work_dispatch(...)` in `seed_runtime/question_surface_inventory.py`.
- `bounded_work_dispatch_result_for_request(...)` in `seed_runtime/question_surface_inventory.py`.
- `apply_bounded_work_dispatch_result(...)` in `seed_runtime/question_surface_inventory.py`.
- `clear_bounded_ask_dispatch_message(...)` in `seed_runtime/question_surface_inventory.py`.
- `apply_bounded_ask_dispatch(...)` dispatch handoff sequence in `scripts/seed_local.py`.
- Request-consumption and downstream-boundary tests in `tests/test_question_surface_inventory.py`.

## Construction-side testimony

From the construction side, the produced bridge artifact is `BoundedWorkDispatchRequest`.

The construction neighborhood first separates selected surface value from selected dispatch surface:

- `BoundedWorkSelectedSurfaceValue` carries `question_family`, `surface_value`, `required_surface_args`, and `reason`.
- `bounded_work_selected_surface_value_for_eligibility(...)` prepares only the selected CLI surface value after permitted eligibility. It explicitly excludes exact lookup, bounded eligibility, dispatch surface identity, dispatch request construction, execution, answer composition, rendering, and semantic routing.
- `BoundedWorkSelectedDispatchSurface` carries `question_family`, `dispatch_surface`, and `reason`.
- `bounded_work_selected_dispatch_surface_for_eligibility(...)` selects only the map-backed CLI dispatch surface after permitted eligibility. It explicitly excludes exact lookup, bounded eligibility, selected surface value, dispatch request construction, execution, answer composition, rendering, and semantic routing.

`bounded_work_selection_for_question_family(...)` then consumes those two selected pieces and produces `BoundedWorkSelectionResult` with:

- `question_family`;
- `dispatch_surface`;
- `surface_value`;
- `required_surface_args`;
- `reason`.

The construction bridge endpoint is `bounded_work_dispatch_request_for_selection(...)`. It copies only the invocation-ready fields from `BoundedWorkSelectionResult` into `BoundedWorkDispatchRequest`:

- `question_family`;
- `dispatch_surface`;
- `surface_value`;
- `reason` set to `dispatch selected bounded work through existing CLI namespace`.

The construction-side tests prove the selected-piece and request-construction boundaries by asserting that selected surface values do not carry dispatch surface, bounded status, or permitted state; selected dispatch surfaces do not carry surface value, required surface args, bounded status, or permitted state; selection results do not carry permitted or bounded status; and dispatch requests do not carry required surface args, bounded status, or permitted state.

From this side, responsibilities explicitly excluded from the bridge are:

- QuestionFamily lookup;
- bounded eligibility decision;
- bounded work selection after the request is built;
- evidence interpretation;
- answer composition;
- rendering;
- semantic routing;
- dispatch execution;
- downstream compatibility handling;
- post-dispatch message clearing.

## Consumer-side testimony

From the consumer side, the received bridge artifact is `BoundedWorkDispatchRequest`.

`execute_bounded_work_dispatch(...)` receives an existing CLI namespace object and the request artifact. It consumes only:

- `dispatch_request.dispatch_surface` as the namespace attribute to set;
- `dispatch_request.surface_value` as the value assigned to that namespace attribute.

After the namespace mutation, `execute_bounded_work_dispatch(...)` hands the same request artifact to `bounded_work_dispatch_result_for_request(...)`, which produces `BoundedWorkDispatchResult` with:

- `question_family`;
- `dispatch_surface`;
- `surface_value`;
- `reason` set to `performed bounded work dispatch through existing CLI namespace`.

The neighboring call site in `apply_bounded_ask_dispatch(...)` shows the consumer sequence:

1. construct `selection`;
2. construct `dispatch_request`;
3. call `execute_bounded_work_dispatch(args, dispatch_request)`;
4. pass the resulting dispatch result to `apply_bounded_work_dispatch_result(...)`;
5. pass the same dispatch result to `clear_bounded_ask_dispatch_message(...)`.

The consumer-side tests prove that execution consumes the request and mutates the namespace, result production can produce a result from the request without mutating the namespace, dispatch-result handoff consumes the dispatch result rather than the request, and message clearing consumes only the dispatch result.

From this side, responsibilities explicitly excluded from the request-consuming bridge are:

- QuestionFamily lookup;
- eligibility decision;
- selection;
- dispatch request construction;
- dispatch result production by `execute_bounded_work_dispatch(...)` itself, because result production is delegated to `bounded_work_dispatch_result_for_request(...)`;
- answer composition;
- rendering;
- evidence interpretation;
- diagnostics;
- schema;
- event ledger;
- semantic routing;
- post-dispatch compatibility handling by the execution function itself;
- post-dispatch message clearing by the execution function itself.

## Independent constitutional translations

### Construction-side translation

- **Sender:** `bounded_work_dispatch_request_for_selection(...)`, receiving a completed `BoundedWorkSelectionResult` from the selected bounded-work construction neighborhood.
- **Receiver:** the neighboring request consumer, visible locally as `execute_bounded_work_dispatch(...)` through the call-site handoff.
- **Artifact crossing:** `BoundedWorkDispatchRequest`.
- **Fields crossing:** `question_family`, `dispatch_surface`, `surface_value`, `reason`.
- **Warrant / reason crossing:** `dispatch selected bounded work through existing CLI namespace`.
- **Explicitly non-crossing responsibilities:** exact lookup, eligibility, selection responsibility after construction, required-surface-arg metadata, bounded status, permitted state, evidence interpretation, answer composition, rendering, semantic routing, dispatch execution, downstream handoff handling, and message clearing.
- **Confidence:** High. The dataclass fields, construction function, docstring exclusions, and tests align directly.

### Consumer-side translation

- **Sender:** the call-site sequence in `apply_bounded_ask_dispatch(...)`, after request construction.
- **Receiver:** `execute_bounded_work_dispatch(...)`.
- **Artifact crossing:** `BoundedWorkDispatchRequest`.
- **Fields crossing:** `dispatch_surface` and `surface_value` are directly consumed for namespace mutation; `question_family`, `dispatch_surface`, and `surface_value` are subsequently passed through to dispatch-result production; `reason` does not appear to be consumed by execution.
- **Warrant / reason crossing:** consumer behavior is warranted by the request being an already selected bounded-work invocation for the existing CLI namespace; the produced result uses `performed bounded work dispatch through existing CLI namespace`.
- **Explicitly non-crossing responsibilities:** exact lookup, eligibility, selection, request construction, answer composition, rendering, evidence interpretation, diagnostics, schema, event ledger, semantic routing, post-dispatch compatibility handling, and message clearing. Result production is not retained inside execution; it is delegated to `bounded_work_dispatch_result_for_request(...)`.
- **Confidence:** High for `dispatch_surface` and `surface_value` consumption; medium-high for `question_family` because execution passes it through via result production rather than using it for the namespace mutation; high that `reason` is not operationally consumed by execution.

## Bridge comparison

### Matching bridge fields

- `dispatch_surface` matches on both sides and is the namespace attribute consumed by execution.
- `surface_value` matches on both sides and is the namespace value consumed by execution.
- `question_family` crosses in the request artifact and is preserved into the dispatch result.

### Mismatched assumptions

- The construction side includes `reason` in `BoundedWorkDispatchRequest` as explanatory warrant.
- The consumer side does not use request `reason` during execution. It creates a new dispatch-result reason through `bounded_work_dispatch_result_for_request(...)`.

This is a visible asymmetry, not a blocking mismatch, because no consumer-side evidence requires `reason` for namespace mutation.

### Missing fields

No required consumer field is missing from the construction artifact. The fields needed for observed execution are present: `dispatch_surface` and `surface_value`. The field needed for observed result identity preservation, `question_family`, is also present.

### Extra fields

`reason` is extra from the execution-mutation perspective. It is construction-side explanatory metadata and is not consumed by the execution mutation.

### Unsupported crossings

The following crossings are not supported by recurring implementation evidence and should remain non-crossing for this audit:

- `required_surface_args` from selection into dispatch request or execution;
- `bounded_status` into dispatch request or execution;
- `permitted` into dispatch request or execution;
- eligibility evidence into execution;
- answer-composition or rendering instructions into execution;
- semantic routing authority into execution;
- diagnostics, schema, or event-ledger mutation into execution.

## Visible seam

The local seam is visible at the handoff from `bounded_work_dispatch_request_for_selection(selection)` to `execute_bounded_work_dispatch(args, dispatch_request)`.

The seam is narrow:

- construction produces a request artifact from already selected bounded work;
- execution receives that request artifact;
- execution mutates the CLI namespace using the request's `dispatch_surface` and `surface_value`;
- execution preserves request identity fields into a dispatch result;
- downstream compatibility handling and message clearing consume the dispatch result rather than reopening request construction.

## Preserved unknowns

The audit preserves the following as unknown or out of scope:

- whether future implementation should change request shape;
- whether future implementation should add, remove, or reinterpret `reason`;
- whether any other consumer besides the visible CLI namespace mutation should receive the request;
- whether execution should ever consume `question_family` for anything beyond result identity preservation;
- whether downstream answer composition or rendering should become connected to this bridge;
- whether diagnostic or event-ledger behavior should be attached to this bridge.

## Readiness assessment

Ready for bounded implementation slice.

The bridge is visible enough for future bounded implementation work because construction and consumer evidence agree on the crossing artifact, the consumer-required fields are present, unsupported crossings are explicitly excluded by code and tests, and the local seam is directly exercised through adjacent tests.

## Confidence

High.

According to recurring
implementation evidence,

is the bridge between

Selected bounded-work
invocation construction

and its neighboring
consumer side

visible enough for a
future bounded implementation
slice?

Yes. The bridge is visible enough for a future bounded implementation slice.

Bridge audit complete.
