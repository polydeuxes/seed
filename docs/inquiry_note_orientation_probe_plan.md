---
title: Inquiry Note Orientation Probe Plan
status: plan
authority: planning only; not implementation, runtime change, schema migration, command addition, classifier, operator model, goal system, planning system, recommendation engine, or behavior change
created: 2026-06-16
scope: documentation-only implementation probe plan
---

# Inquiry Note Orientation Probe Plan

## 1. Purpose

This document plans the smallest useful implementation probe for this slice:

```text
operator prose
    -> preserved inquiry evidence
    -> orientation view
```

The probe should test whether Seed can preserve raw operator prose as inquiry
evidence and render a basic orientation surface from that preserved note plus
existing Seed knowledge. It must not convert prose into intent, commands,
claims, goals, work types, selected work, or execution authority.

This document is planning and functional description only. It does not implement
runtime changes, create schema migrations, add CLI commands, add tests, modify
behavior, or authorize execution.

## 2. Background / Repository Basis

The repository basis for the probe is the recent finding cluster:

```text
available knowledge != recognized work
recognized work != activated work
repository preserves responses better than activation events
same information can support different work
different work shapes need different orientation
```

The requested review set was inspected, along with adjacent runtime/read-model
surfaces. The strongest repository basis is:

- Inquiry preservation work observes that repository history often preserves the
  response to pressure better than the originating pressure or operator-facing
  inquiry note. That makes a raw note preservation probe useful, provided it is
  not treated as reconciliation, canon, runtime proposal, or intent evidence by
  itself.
- Work recognition and work-recognition reality audits distinguish information
  from recognized work. The same preserved fact, document, or State Summary row
  can support lookup, audit, reconciliation, frontier exploration, or
  continuation, so an inquiry note must remain evidence for orientation rather
  than a classifier result.
- Work-shape and orientation observations indicate that different work shapes
  need different orientation, but they do not establish a canonical taxonomy or
  authorize an intent/work-shape classifier.
- Orientation-bundle, situation, purpose/concern, relation-preservation,
  continuability, active-edge, current-work-position, and continuity documents
  repeatedly preserve relations among concern, pressure, boundary, active edge,
  support, uncertainty, and next safe movement. The probe can borrow this
  language as display vocabulary while keeping every inferred relation visibly
  tentative.
- Working-state activation and activation-failure observations show that an
  answer can exist, be found, and be read while still failing to activate the
  right work. The probe therefore should not equate related material with
  activated work.
- State Summary authority and CLI-boundary audits treat State Summary as a
  repository-level knowledge inventory/read-model surface whose semantics should
  live in runtime/read-model helpers rather than the CLI.
- Source-navigation reconciliation treats navigation as orientation over
  preserved source facts, not as new observation, stronger fact, truth,
  ownership, or implementation knowledge by itself.

Existing implementation surfaces relevant to the probe include:

- `scripts/seed_local.py`, which owns argument parsing, command dispatch,
  terminal formatting, JSON choices, and CLI misuse messages.
- `seed_runtime/state_summary_views.py`, which owns State Summary semantic
  aggregation for operator overview rather than requiring CLI code to decide
  State Summary meaning.
- `seed_runtime/context.py`, which composes compact model-decision context from
  projected state, current input, active goals, facts, tools, open tool needs,
  and recent evidence.
- `seed_runtime/context_views.py`, which provides read-only deterministic
  decision-context projections and explicitly avoids ledger reads, event
  appends, state mutation, provider calls, policy evaluation, tool execution,
  LLM calls, and separate context persistence.
- `seed_runtime/source_navigation.py`, which builds a read-only navigation view
  over preserved `imports` and `defines` facts without reading source files,
  ingesting observations, or inferring behavior, reachability, or ownership.
- `seed_runtime/explanations.py`, which builds deterministic fact explanations
  from projected state and preserved fact support.
- `seed_runtime/runtime_trace.py`, which reconstructs read-only runtime traces
  from append-only events without replaying or mutating them.
- Tests for State Summary and Context Views, especially assertions that read
  models can be built without CLI parsing and that context views do not mutate
  state.

## 3. Non-goals

This probe is not:

- a conversational UI;
- an intent classifier;
- a work-shape classifier;
- an operator model;
- a goal system;
- a planning system;
- a recommendation engine;
- a truth engine;
- an execution surface;
- an automated action trigger;
- a schema migration;
- a replacement for State Summary, Current Facts, Fact Support, Why Fact,
  Source Navigation, Runtime Trace, Context Views, or Context Composer;
- a new authority over what work is active;
- a promotion path from raw prose into claims, facts, goals, work types, or
  operator intent.

## 4. Proposed Minimal Slice

The smallest useful probe should preserve one raw inquiry note and render an
orientation view that keeps the note visible while showing bounded, supportable
related material from existing read models.

Candidate user-facing shape, with names still to be evaluated:

```bash
seed --inquiry-note "example_host keeps showing up first and that feels wrong"
seed --orient
```

Recommended probe naming:

- Use an explicit capture option such as `--inquiry-note TEXT` or
  `--record-inquiry-note TEXT` rather than `--ask`, `--intent`, `--concern`, or
  `--goal`.
- Use an explicit read-only render option such as `--orient-inquiry` or
  `--inquiry-orientation` rather than bare `--orient` if there is risk that
  `--orient` sounds like a general command dispatcher.
- If the implementation must be very small, allow capture-and-render in one CLI
  invocation with two flags, but still preserve the storage/read separation:
  capture appends the note evidence; render reads the latest selected note and
  projected knowledge.

Minimal flow:

```text
operator supplies raw note
    -> Seed stores raw note evidence with provenance metadata
    -> operator requests inquiry orientation
    -> Seed loads the raw note plus existing projected knowledge/read models
    -> Seed renders a bounded orientation view
    -> no action is selected or executed
```

## 5. Functional Behavior

### 5.1 Capturing Raw Inquiry Prose

The capture path should store the exact operator-provided prose as a string.
Normalization should be limited to transport-safe storage concerns, not semantic
rewriting. The displayed output should preserve the raw text verbatim enough that
operators can verify Seed is orienting around what was said, not around a hidden
interpretation.

Functional expectations:

- accept a non-empty text string;
- preserve the raw string as `raw_note` or equivalent;
- reject or safely render an empty string without inventing meaning;
- preserve multiline text if the CLI can receive it safely;
- never rewrite the note into a claim, goal, work type, tool request, or command.

### 5.2 Preserving The Note As Inquiry Evidence, Not Intent

The note should be stored with a type/name that encodes evidence status, for
example `inquiry.note.recorded` or a lightweight `InquiryNote` record. Avoid
names such as `intent`, `goal`, `task`, `command`, `work_type`, or
`active_concern` for the stored object.

Required distinction:

```text
raw note = preserved inquiry evidence
raw note != operator intent
raw note != command
raw note != claim
raw note != goal
raw note != recognized work
```

### 5.3 Timestamp, Source, And Optional Scope

If existing repository patterns support it, each note should retain:

- stable note id;
- raw note text;
- observed/recorded timestamp in UTC;
- workspace id;
- session id if supplied;
- source, such as `scripts.seed_local --inquiry-note`;
- optional operator-provided scope, if provided explicitly and stored as scope,
  not inferred scope;
- optional correlation id if a capture-and-render command needs to tie output to
  the just-recorded note.

The probe should not require a migration. If the existing SQLite event ledger can
store arbitrary event kinds with JSON payloads, prefer an append-only event over
a new table. If the ledger cannot support this safely without behavior changes,
use a deliberately isolated lightweight persistence file for the probe.

### 5.4 Orientation View Content

The orientation view may include:

- the raw inquiry note, always visible;
- known related facts, State Summary rows, source navigation rows, or other
  existing surfaces if supportable;
- support or a short why-this-is-related explanation;
- an active concern candidate, clearly marked as candidate;
- uncertainty;
- a next safe move, clearly marked as suggestion or bounded continuation cue.

The view must remain useful even when Seed cannot infer much. A sparse output is
valid if it includes the raw note, uncertainty, and a bounded safe cue such as
"no related material found; inspect existing knowledge surfaces before changing
behavior."

### 5.5 Avoiding Automatic Action

The probe must not:

- call tools;
- create action plans;
- create handoff plans;
- authorize proposals;
- execute providers;
- mutate facts/goals/tool needs;
- classify intent;
- promote a selected next step into execution authority.

### 5.6 Avoiding Promotion Into Claims, Goals, Work Types, Or Intent

No fact, claim, goal, work type, candidate request, or decision record should be
created from the note during this probe. If future implementations derive a
candidate concern for display, the derived value must be stored either nowhere or
as render-only output metadata, not as a durable assertion.

### 5.7 Keeping The Raw Note Visible

Every orientation rendering must include a top-level `Inquiry note` section. If
JSON output is added later, the raw note should remain in a stable top-level
field such as `inquiry_note.raw_note`.

### 5.8 Useful Failure Mode

If related material is absent or ambiguous, render:

- the raw note;
- `Potentially related: none found` or equivalent;
- uncertainty explaining that Seed cannot determine what matters from the note;
- a bounded next safe move that does not execute or imply a recommendation.

## 6. Persistence Options And Recommended Probe Choice

### Option A: Store Inquiry Notes As Observations

Pros:

- aligns with evidence preservation;
- existing projection machinery understands observation/fact ingestion.

Cons:

- high risk of turning prose into a fact-like observation;
- may invite predicate/value normalization;
- could blur `inquiry note != claim`.

Recommendation: not the first probe choice unless the observation model can
preserve raw text without fact projection.

### Option B: Store Inquiry Notes As Runtime Trace Events

Pros:

- append-only event shape already exists;
- runtime traces preserve what happened without replaying or mutating;
- event payloads can carry raw input, timestamp, workspace, session, and source.

Cons:

- runtime trace is currently run-oriented, so using it for inquiry notes may imply
  a runtime run;
- orientation notes are not necessarily part of a decision/tool runtime path.

Recommendation: viable if represented as a distinct event kind and read by a
small note reader, not by pretending it is a runtime run.

### Option C: Store Inquiry Notes As Documentation Artifacts

Pros:

- very safe for planning and human review;
- no runtime behavior risk.

Cons:

- not a useful implementation probe of operator capture;
- weak fit for CLI read/write behavior;
- difficult to orient against current projected knowledge.

Recommendation: useful for this plan only, not for the implementation probe.

### Option D: New Lightweight Persistence Surface

Pros:

- cleanly preserves `InquiryNote` as its own evidence kind;
- avoids claim/fact/goal promotion;
- can be implemented without migrations as JSONL or as a namespaced event kind if
  the existing ledger supports arbitrary events.

Cons:

- introduces a new persistence surface;
- must avoid becoming a parallel source of truth.

Recommended probe choice: use the existing append-only event ledger if it can
append a distinct `inquiry.note.recorded` event without schema changes. Add a
small read-model helper over those events, tentatively
`seed_runtime/inquiry_orientation.py`, that loads inquiry-note events and builds
a read-only orientation view. If event-ledger use would require a migration or
runtime decision-path coupling, fall back to a tightly scoped JSONL probe store
under the configured workspace path.

Minimum safe persistence shape:

```json
{
  "note_id": "inq_...",
  "raw_note": "example_host keeps showing up first and that feels wrong",
  "recorded_at": "2026-06-16T00:00:00Z",
  "workspace_id": "local",
  "session_id": "local",
  "source": "scripts.seed_local --inquiry-note",
  "operator_scope": null
}
```

## 7. Orientation Rendering Behavior

`--orient-inquiry` or equivalent should read from:

1. the latest or explicitly selected inquiry note;
2. projected State built through existing projection/cache patterns;
3. existing read-model helpers where relevant:
   - State Summary for overview/top-entity context;
   - Current Facts / fact support for raw evidence and support counts;
   - Why Fact / evidence explanations for provenance;
   - Source Navigation for source-related terms if the note references known
     source symbols, modules, or paths;
   - Context Views only as read-only projection examples, not as decision or
     provider context.

The first probe should use deterministic lexical matching and explicit support,
not LLM interpretation. For example, if the raw note contains `example_host`, the
orientation view may show State Summary rows, current facts, fact support, and
availability/source rows for `example_host`. If the note says "showing up first," the
view may mention State Summary top-entity ranking only if State Summary is one of
the rendered or inspected surfaces and the support explains that the relation is
based on wording overlap plus top-entity ordering, not on known intent.

Suggested text sections:

```text
Inquiry note:
Potentially related:
Support / why related:
Candidate active concern:
Uncertainty:
Next safe move:
Authority boundary:
```

Ambiguity display requirements:

- use `candidate`, `potentially`, `may`, and `unknown` labels;
- show when relation came from text overlap versus fact support;
- show when no supportable material exists;
- do not hide the raw note behind a summary.

If there is no related material:

```text
Potentially related:
  None found in current projected knowledge.

Uncertainty:
  Seed cannot determine whether the note names an existing entity, source
  surface, concern, or behavior.

Next safe move:
  Inspect current facts, State Summary, or source navigation manually before
  changing behavior.
```

## 8. Authority And Safety Boundaries

The implementation prompt must preserve these boundaries exactly:

```text
inquiry note != operator intent
inquiry note != command
inquiry note != claim
inquiry note != goal
orientation view != recommendation engine
orientation view != action plan
orientation view != truth
candidate active concern != recognized work
related material != selected work
next safe move != execution authority
```

Additional boundaries:

```text
raw note preservation != fact ingestion
lexical relatedness != relevance truth
support path != recommendation
State Summary prominence != importance
source navigation match != source ownership
context view != decision authorization
runtime trace/event preservation != replay
```

## 9. Example Output

The following is illustrative and non-binding. It is not a required final UI.

```text
Inquiry note:
  "example_host keeps showing up first and that feels wrong"

Potentially related:
  - State Summary top entity ranking
  - Durable fact prominence
  - Fact support for example_host
  - State Summary authority boundary

Support / why related:
  - The note mentions "example_host" and "showing up first".
  - State Summary has a top-entity surface where ordering can be visible.
  - Existing State Summary authority work says State Summary is a knowledge
    inventory surface, not impact or importance.

Candidate active concern:
  State Summary prominence may be read as significance.

Uncertainty:
  Seed cannot determine whether example_host is actually important to the operator.
  Seed also cannot determine whether the concern is ordering, fact support,
  aliasing, endpoint grouping, documentation wording, or something else.

Next safe move:
  Suggestion only: inspect fact support and ranking evidence before changing
  summary behavior.

Authority boundary:
  This orientation does not select work, infer intent, create a goal, or
  authorize execution.
```

## 10. Testing Expectations

Do not write these tests until the implementation probe is accepted. Future tests
should assert:

- inquiry note is stored raw;
- inquiry note keeps timestamp, source, workspace, session, and explicit scope
  when supplied;
- inquiry note is not promoted into fact, claim, goal, work type, candidate
  request, decision record, or tool need;
- orientation output includes the raw note;
- orientation output marks inferred concern as `candidate`;
- related material is supportable or clearly absent;
- no tools, providers, actions, action plans, handoff plans, proposals, or
  authorizations are executed;
- empty or ambiguous notes still render safely;
- State Summary/top-entity relatedness does not assert importance;
- source navigation relatedness does not assert ownership or behavior;
- read-model building does not mutate projected State;
- JSON output, if added, preserves the same authority labels as text output.

Likely test locations after acceptance:

- focused read-model tests for the new inquiry-orientation helper;
- CLI parser/dispatch tests in existing `seed_local` tests;
- regression tests ensuring event projection does not create facts/goals from
  inquiry-note events.

## 11. Open Questions

- Should note selection default to the latest note, require an explicit note id,
  or support both?
- Should capture and orientation be separate commands/flags, or should the probe
  support a capture-and-render convenience path?
- Is the existing event ledger acceptable for arbitrary `inquiry.note.recorded`
  events without migration and without accidental projection into State?
- Where should optional operator-provided scope be expressed: CLI flag, JSON
  payload, workspace/session only, or deferred?
- Should the first deterministic relatedness pass tokenize only entity-looking
  terms, or also match surface words such as `first`, `summary`, `support`, and
  `source`?
- Should JSON output be included in the first probe, or deferred until text
  behavior stabilizes?
- Should orientation read cached State Summary projection or rebuild projected
  State on demand according to existing CLI patterns?
- What retention policy, if any, applies to inquiry notes?

## 12. Implementation Risks

- The word `orientation` may invite product expectations that exceed a small
  probe.
- A bare `--orient` name may sound like a general work activation command.
- Storing notes as observations could accidentally promote prose into claims.
- Rendering a `candidate active concern` could be mistaken for recognized work if
  labels are weak.
- Showing `next safe move` could be mistaken for a recommendation or action plan
  if it is not explicitly bounded.
- Related State Summary rows may be misread as importance unless the State
  Summary authority boundary is displayed.
- Lexical matching may miss useful relations, but adding semantic inference too
- Reusing runtime trace events may blur note preservation with runtime decision
  traces unless event kind and reader boundaries are explicit.
- Adding CLI semantics in `scripts/seed_local.py` could repeat the State Summary
  CLI-boundary smell unless aggregation/orientation meaning lives in a runtime
  read-model helper.

## 13. Recommended Next Implementation Prompt If Accepted

```text
Implement the inquiry-note orientation probe described in
`docs/inquiry_note_orientation_probe_plan.md`.

Do the smallest safe slice only:
- preserve raw inquiry prose as inquiry-note evidence, not intent, command,
  claim, goal, work type, or selected work;
- use existing append-only event storage if no migration is required;
- add a small read-only runtime helper for inquiry orientation;
- add minimal CLI capture/render flags with names that preserve authority
  boundaries;
- render raw note, supportable related material, candidate concern, uncertainty,
  next safe move as suggestion only, and authority boundary;
- do not execute tools, create plans, authorize proposals, or mutate facts/goals;
- add focused tests for raw preservation, no promotion, safe rendering, and no
  action execution.
```
