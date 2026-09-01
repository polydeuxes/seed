# Bounded Ask Adjacent Terrain Survey

## Scope

This is exactly one bounded Survey after the bounded ask adjacent terrain Scout.

This Survey partitions only the newly visible adjacent implementation terrain identified in `bounded_ask_adjacent_terrain_scout.md`.
It remains immediately adjacent to Implementation Recovery Slices 001-011.

This Survey does not recover ownership, characterize responsibilities, recommend implementation slices, or propose implementation design.
Repository authority wins.

## Reviewed Scout evidence

The reviewed Scout evidence identifies the newly visible terrain as the narrow area around two bounded ask terminal paths and their neighboring construction points:

```text
presentation path:
permitted bounded work
-> presentation handoff production
-> presentation handoff consumption
-> presentation message clearing
-> stop before dispatch
```

```text
dispatch path:
permitted bounded work
-> selection result construction
-> dispatch request construction
-> dispatch execution
-> dispatch result production
-> dispatch result handoff consumption
-> dispatch message clearing
-> downstream existing surface handling
```

The reviewed Scout evidence also identifies these adjacent implementation elements:

- mirrored presentation and dispatch tail shapes;
- selection-result construction between selected-piece helpers and dispatch-request construction;
- dispatch-request construction immediately before CLI namespace mutation;
- CLI namespace mutation points surrounded by narrow handoff artifacts;
- the special `ask --question-surface-inventory` message-clearing branch adjacent to, but outside, the exact `--question-family` bounded work chain;
- compatibility-specific JSON mutation for one dispatch result path;
- repeated dataclass-backed handoff artifacts;
- repeated helper and test patterns that prove narrow seams and excluded neighboring fields;
- visible dead ends where diagnostic-only families, not-dispatchable families, and presentation handoff do not continue into a broader path.

## Recovered implementation groupings

### Grouping 1: mirrored terminal handoff-and-clearing tails

#### Membership

Presentation-side members:

- `BoundedWorkPresentationHandoff`;
- `bounded_work_presentation_handoff_for_eligibility(...)`;
- `BoundedWorkPresentationHandoffResult`;
- `apply_bounded_work_presentation_handoff(...)`;
- `BoundedAskPresentationMessageClearResult`;
- `clear_bounded_ask_presentation_message(...)`;
- presentation-tail calls inside `apply_bounded_ask_dispatch(...)`.

Dispatch-side members:

- `BoundedWorkDispatchResult`;
- `bounded_work_dispatch_result_for_request(...)`;
- `apply_bounded_work_dispatch_result(...)`;
- `BoundedAskDispatchMessageClearResult`;
- `clear_bounded_ask_dispatch_message(...)`;
- dispatch-tail calls inside `apply_bounded_ask_dispatch(...)`.

#### Boundaries

Included:

- handoff or result artifact production;
- handoff or result consumption;
- post-consumption message clearing;
- tests that check the handoff/result and clearing artifacts remain narrow.

Excluded:

- exact lookup;
- eligibility;
- refusal;
- surface-argument satisfaction;
- selection-result construction;
- dispatch-request construction;
- downstream rendering or diagnostic handling.

#### Repeated implementation shapes

- A dataclass artifact carries `question_family` plus one local payload or reason.
- A helper consumes the immediately preceding artifact.
- The CLI namespace is mutated locally at consumption or clearing time.
- Clearing `args.message` follows the handoff/result step.
- Tests use narrow assertions and excluded-field checks rather than broader behavior claims.

#### Confidence

High.

The grouping is visible in both presentation and dispatch tails, and the Scout evidence, implementation names, and adjacent tests repeat the same production-consumption-clearing pattern.

### Grouping 2: selection-to-request construction neighborhood

#### Membership

- `BoundedWorkSelectedSurfaceValue`;
- `bounded_work_selected_surface_value_for_eligibility(...)`;
- `BoundedWorkSelectedDispatchSurface`;
- `bounded_work_selected_dispatch_surface_for_eligibility(...)`;
- `BoundedWorkSelectionResult`;
- `bounded_work_selection_for_question_family(...)`;
- `BoundedWorkDispatchRequest`;
- `bounded_work_dispatch_request_for_selection(...)`;
- tests that assert selected surface value, selected dispatch surface, selection result, and dispatch request remain separate.

#### Boundaries

Included:

- selected surface value construction;
- selected dispatch surface construction;
- selection-result construction from selected pieces;
- dispatch-request construction from selection fields.

Excluded:

- eligibility decision and refusal terrain before selection;
- dispatch execution after request construction;
- presentation handoff tail;
- post-dispatch compatibility handling;
- message clearing.

#### Repeated implementation shapes

- Separate selected-piece helpers feed a compact aggregate result.
- The aggregate result is immediately copied into a request artifact.
- Dataclass artifacts carry `question_family` and narrow selected/request fields.
- Tests assert included fields and excluded neighboring fields.

#### Confidence

Medium-high.

The grouping is compact and repeatedly visible in implementation and tests. Confidence is not higher because the Survey does not expand beyond immediately adjacent terrain to prove whether this construction neighborhood has any further repeated members.

### Grouping 3: CLI namespace mutation neighborhood

#### Membership

- `setattr(args, "question_family_explanation", ...)` in presentation handoff consumption;
- `setattr(args, dispatch_request.dispatch_surface, dispatch_request.surface_value)` in dispatch execution;
- `setattr(args, "knowledge_reachability_audit_json", True)` in dispatch result handoff consumption;
- `setattr(args, "json_output", False)` in dispatch result handoff consumption;
- `setattr(args, "message", [])` in presentation message clearing;
- `setattr(args, "message", [])` in dispatch message clearing;
- the nearby `ask --question-surface-inventory` branch that clears `args.message` outside the exact `--question-family` chain.

#### Boundaries

Included:

- CLI namespace mutation points named by the Scout;
- adjacent helper artifacts that surround those mutation points;
- the nearby one-off message-clearing branch identified by the Scout.

Excluded:

- any claim that the namespace mutation points share ownership;
- any characterization of mutation responsibility;
- any downstream rendering, event-ledger, schema, or diagnostic behavior not visible in the adjacent terrain.

#### Repeated implementation shapes

- Mutation is concentrated at narrow helper consumption or clearing points.
- Mutation is surrounded by dataclass-backed handoff or result artifacts.
- Message clearing recurs in both presentation and dispatch paths.
- One compatibility mutation remains specific to a single dispatch result path.

#### Confidence

Medium.

The mutation points are explicitly visible and repeated, but the Scout preserved unknowns about whether request construction, execution mutation, compatibility mutation, or branch sequencing contain recoverable local seams.

### Grouping 4: bounded ask branch-sequence neighborhood

#### Membership

- `apply_bounded_ask_dispatch(...)` exact `--question-family` entry sequence;
- parameterized presentation branch skeleton;
- parameterized dispatch branch skeleton;
- non-parameterized presentation branch skeleton;
- non-parameterized dispatch branch skeleton;
- non-permitted refusal branch;
- adjacent special `ask --question-surface-inventory` message-clearing branch outside the exact `--question-family` sequence.

#### Boundaries

Included:

- local branch sequencing immediately adjacent to the recovered bounded ask chain;
- convergence of parameterized and non-parameterized paths on the same presentation and dispatch tail shapes;
- the nearby inventory special case only as adjacent branch terrain.

Excluded:

- unrelated CLI argument normalization;
- downstream command execution outside the bounded ask handoff/request mutations;
- implementation-family expansion beyond `question_surface_inventory.py`, `scripts/seed_local.py`, and adjacent tests unless implementation evidence requires it.

#### Repeated implementation shapes

- Parameterized and non-parameterized branches repeat a high-level shape.
- Presentation branches stop after presentation handoff and message clearing.
- Dispatch branches continue through selection, request, execution, result handling, and message clearing.
- Refusal branches remain dead ends rather than continuations.

#### Confidence

Medium-high.

The repeated branch skeletons are visible in the bounded ask orchestration point and are named by the Scout. Confidence is limited by the preserved unknown about whether branch sequencing contains any recoverable local seam.

### Grouping 5: seam-preservation test neighborhood

#### Membership

- tests for exact lookup excluding eligibility and dispatch fields;
- tests for eligibility excluding selected surface fields;
- tests for surface-argument result excluding selected surface fields;
- tests for refusal excluding permitted or dispatch fields;
- tests for selected surface value and selected dispatch surface as separate pieces;
- tests for selection result excluding eligibility fields;
- tests for presentation handoff production and consumption;
- tests for dispatch request, dispatch result production, dispatch execution, and dispatch result consumption;
- tests for presentation and dispatch message clearing;
- integrated bounded ask behavior tests for non-parameterized dispatch, parameterized dispatch, and parameterized presentation.

#### Boundaries

Included:

- adjacent tests that preserve repeated seam visibility from Slices 001-011;
- tests proving the surfaces appear as narrow implementation artifacts.

Excluded:

- tests for unrelated diagnostic inventory, shape audit, projection, documentation, or operational surfaces;
- any interpretation that test recurrence implies ownership or a future implementation plan.

#### Repeated implementation shapes

- Test names use `is_separate_from`, `consumes_*_only`, or equivalent boundary vocabulary.
- Assertions prove included local payloads.
- Assertions prove excluded neighboring fields.
- Integrated tests preserve public bounded ask behavior while helpers expose narrower artifacts.

#### Confidence

High.

The test neighborhood repeats the same seam-preservation shape across the newly visible adjacent terrain and directly supports the implementation grouping boundaries.

## Grouping boundaries across the terrain

The newly visible adjacent terrain partitions into these recurring groupings without assigning ownership or characterizing responsibilities:

1. mirrored terminal handoff-and-clearing tails;
2. selection-to-request construction neighborhood;
3. CLI namespace mutation neighborhood;
4. bounded ask branch-sequence neighborhood;
5. seam-preservation test neighborhood.

The primary boundary between the first two groupings is the presentation/dispatch split: presentation stops after handoff and clearing, while dispatch passes through selection and request construction before execution and result handling.

The primary boundary between selection-to-request construction and CLI namespace mutation is the request artifact: construction copies selection fields into an invocation artifact, while execution consumes that request and mutates the CLI namespace.

The primary boundary between terminal tails and branch sequencing is locality: the tails are repeated helper/artifact sequences, while branch sequencing is the surrounding orchestration that chooses which tail or refusal path is reached.

The primary boundary between implementation groupings and test groupings is evidentiary: tests preserve the seams but are not themselves the runtime artifact sequence.

## Preserved unknowns

- Whether any further bounded ask compression should be recovered remains unknown.
- Whether the mirrored terminal shapes indicate closure remains unknown.
- Whether the special `ask --question-surface-inventory` clearing branch is adjacent enough for future implementation work remains unknown.
- Whether selection result construction, request construction, execution mutation, JSON compatibility mutation, or branch sequencing contain any recoverable local seam remains unknown.
- Whether neighboring helpers outside `question_surface_inventory.py`, `scripts/seed_local.py`, and `tests/test_question_surface_inventory.py` are relevant remains unknown.
- Whether repeated geography implies any recurring implementation citizen remains unknown and is not inferred here.

## Confidence

Overall confidence: medium-high.

Reason: the Scout evidence, implementation artifact names, helper sequence, and adjacent tests repeatedly expose the same groupings and boundaries. Confidence is not higher because the Survey remains bounded to immediately adjacent terrain and preserves the Scout's unknowns instead of proving closure.

## Answer

According to recurring
implementation evidence,

what recurring
implementation
groupings

exist

within the newly visible
adjacent terrain?

The recurring implementation groupings are:

- mirrored terminal handoff-and-clearing tails;
- the selection-to-request construction neighborhood;
- the CLI namespace mutation neighborhood;
- the bounded ask branch-sequence neighborhood;
- the seam-preservation test neighborhood.

Survey complete.
