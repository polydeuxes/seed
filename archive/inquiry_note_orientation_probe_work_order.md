---
title: Inquiry Note Orientation Probe Work Order
status: work order
authority: implementation guidance only; minimized V1 probe; not an implementation, runtime behavior change, schema migration, command execution authorization, classifier, planning system, recommendation engine, or truth surface
created: 2026-06-16
scope: documentation-only plan-lint and implementation work-order refinement
source_plan: docs/inquiry_note_orientation_probe_plan.md
---

# Inquiry Note Orientation Probe Work Order

## 1. Purpose

Create the smallest safe implementation slice for this hypothesis:

```text
operator prose
    -> preserved inquiry evidence
    -> bounded orientation read model
```

V1 exists only to preserve raw operator inquiry prose and render a read-only
orientation view over that preserved note plus already-available knowledge. It
must not decide what the operator means, what work is active, what is true, what
should happen next, or which material is selected for work.

This work order intentionally narrows the existing probe plan. The original plan
allowed candidate concern and next-safe-move display as clearly marked tentative
output. V1 removes those from default output because they are easy to read as
intent inference, recommendation, or action planning.

## 2. Scope

In scope for V1:

- capture one raw inquiry note supplied by an operator;
- preserve the note as inquiry-note evidence, not intent;
- preserve minimal provenance that can be obtained without migrations or runtime
  decision-path coupling;
- build a small read-only orientation helper, likely
  `seed_runtime/inquiry_orientation.py`;
- render a bounded orientation view from the preserved note and deterministic
  related-material lookup;
- keep CLI behavior thin: argument parsing, dispatch, and formatting only;
- add implementation tests only after this work order is accepted by a separate
  implementation task.

Out of scope for this work order itself:

- runtime behavior changes;
- tests;
- schema migrations;
- implementation code;
- new facts, goals, tool needs, plans, proposals, or provider calls.

## 3. V1 Minimized Behavior

### 3.1 Capture

V1 should accept a non-empty raw text note and store it verbatim enough that the
operator can verify the preserved text. Transport-safe escaping is acceptable;
semantic rewriting is not.

Minimum record fields:

```json
{
  "note_id": "inq_...",
  "raw_note": "operator text exactly as received",
  "recorded_at": "2026-06-16T00:00:00Z",
  "source": "scripts.seed_local --record-inquiry-note",
  "workspace_id": "existing workspace value if safely available",
  "session_id": "existing session value if safely available"
}
```

`workspace_id` and `session_id` are optional in V1 unless existing local CLI or
runtime patterns already make them available without inference, migration, or
coupling to a decision run.

### 3.2 Evidence Status

The stored object should be named and typed as inquiry-note evidence, for example
`inquiry.note.recorded` or an `InquiryNote` record. Avoid names containing
`intent`, `goal`, `task`, `command`, `work_type`, `active_concern`,
`recommendation`, or `plan`.

### 3.3 Orientation

V1 orientation should:

- always render the raw inquiry note;
- render potentially related material only when deterministic support exists;
- explain why each related item was included;
- render uncertainty even when related material exists;
- render an authority boundary every time;
- remain useful when no related material is found.

V1 orientation must not by default render:

- candidate active concern;
- next safe move;
- recommendation;
- action plan;
- work-shape classification;

## 4. Explicit Deferrals From Original Plan

Defer these original-plan possibilities to V2+ candidates:

- candidate active concern display;
- next safe move display;
- capture-and-render convenience flows that might feel like command handling;
- JSON output, unless the implementer can add it without increasing authority or
  parser scope;
- operator-provided scope flags;
- retention policy;
- LLM-assisted interpretation;
- semantic relatedness;
- intent, concern, work-shape, task, or goal classification;
- recommendation, planning, proposal, provider, or tool-execution integration;
- durable storage of render-only derived metadata;
- treating State Summary ordering as importance;
- treating source-navigation matches as ownership or behavior evidence.

## 5. Storage Recommendation

Prefer append-only event storage only if all of the following are true:

- a distinct event kind such as `inquiry.note.recorded` can be appended without a
  migration;
- the event is not projected into facts, goals, requirements, capabilities, tool
  needs, decisions, proposals, plans, or runtime traces used for execution;
- reading inquiry notes does not require pretending a note is part of a provider,
  tool, or decision run;
- the implementation can test that projection remains unchanged by an inquiry
  note event.

If any of those conditions fail, use a smaller isolated JSONL probe store under
an existing workspace/local-state path. The JSONL store should be explicitly
probe-scoped and should not become a parallel truth store. Its only durable
object is the inquiry note record.

Do not create a database table or schema migration for V1.

## 6. Read-Model / Helper Recommendation

Add a small read-only helper, likely `seed_runtime/inquiry_orientation.py`, that
owns inquiry-orientation semantics. The helper should expose narrow functions
similar in spirit to existing read-model helpers:

- record loading or note selection from the chosen storage adapter;
- deterministic token extraction from the raw note;
- deterministic related-material matching over already-projected State and
  existing read-model outputs;
- construction of an immutable or plain-data orientation view;
- text rendering support, if existing project style places rendering beside the
  view.

The helper must not:

- mutate State;
- append events while rendering;
- read source files directly;
- call providers or LLMs;
- execute tools;
- evaluate policy;
- create facts, goals, requirements, capabilities, tool needs, decisions,
  proposals, or plans.

Related-material matching should be deterministic only. Acceptable V1 matching:

- exact or case-normalized entity/source/token overlap;
- source surface lexical matches using existing source-navigation read models;
- State Summary or fact-support rows when a note token matches their preserved
  subjects, aliases, paths, or displayed surface terms.

Not acceptable in V1:

- semantic intent inference;
- guessing the operator's concern;
- ranking by importance;
- unsupported relation claims;
- LLM interpretation.

## 7. CLI Recommendation

The CLI should remain thin and should not own inquiry semantics. It may own:

- flag parsing;
- local storage adapter selection;
- dispatch to the helper;
- terminal text formatting, if formatting is not in the helper;
- JSON/text choice only if JSON is included later.

Recommended names:

- capture: `--record-inquiry-note TEXT`;
- orientation render: `--inquiry-orientation [NOTE_ID]`.

Acceptable shorter alternatives:

- `--inquiry-note TEXT` for capture;
- `--orient-inquiry [NOTE_ID]` for rendering.

Avoid bare `--orient` in V1. It sounds broad and product-like, and it may imply a
general orientation, planning, or recommendation command rather than a bounded
read-only inquiry-note view.

If both capture and render are supplied in one invocation, implementation must
still preserve the internal boundary:

```text
capture appends note evidence
render reads note evidence and projected knowledge
```

The render step must not treat the just-captured note as a command.

## 8. Output Format

Default V1 text output should use these sections:

```text
Inquiry note:
Potentially related material:
Support / why related:
Uncertainty:
Authority boundary:
```

Required behavior:

- `Inquiry note` shows the raw note visibly and verbatim enough for operator
  verification.
- `Potentially related material` lists only supportable deterministic matches or
  explicitly states that none were found.
- `Support / why related` explains token/source/entity overlap and cites the
  read-model surface or preserved support path used by the helper.
- `Uncertainty` states what Seed cannot determine from the note.
- `Authority boundary` states the V1 boundaries in plain language.

Useful no-match output shape:

```text
Inquiry note:
  "...raw note..."

Potentially related material:
  None found in current projected knowledge.

Support / why related:
  No deterministic entity, source, or surface lexical match was found.

Uncertainty:
  Seed cannot determine whether the note names an existing entity, source
  surface, concern, behavior, or desired work.

Authority boundary:
  This view preserves an inquiry note and does not infer intent, select work,
  make a recommendation, create a plan, or assert truth.
```

## 9. Authority Boundaries

V1 implementation and output must preserve these boundaries:

```text
inquiry note != operator intent
inquiry note != command
inquiry note != claim
inquiry note != goal
inquiry note != work type
orientation view != recommendation engine
orientation view != action plan
orientation view != truth
related material != selected work
lexical relatedness != relevance truth
State Summary prominence != importance
source navigation match != source ownership
```

Additional implementation boundary:

```text
stored inquiry-note evidence != fact ingestion
read-model construction != state mutation
CLI dispatch != semantic authority
support path != recommendation
runtime/event preservation != replay
```

## 10. Test Expectations

Do not add tests as part of this documentation-only refinement. A later
implementation task should include focused tests asserting:

- raw note is preserved verbatim;
- note id, raw note, recorded timestamp, source, and safely available
  workspace/session provenance are preserved;
- note is not promoted into fact, claim, goal, work type, tool need,
  requirement, capability, decision, proposal, or plan;
- orientation output includes the raw note;
- related material is supportable or explicitly absent;
- support / why-related text is rendered for every related item;
- uncertainty is rendered;
- authority boundary is rendered;
- no actions, tools, providers, plans, proposals, or authorizations execute;
- CLI remains formatting/dispatch only;
- read-model helper does not mutate state;
- source-navigation matches do not assert source ownership;
- State Summary matches do not assert importance;
- empty or whitespace-only notes are rejected or rendered safely without
  invented meaning.

## 11. Implementation Risks

- Storing notes in an existing event ledger may accidentally couple inquiry
  notes to runtime traces, decision paths, or projection behavior.
- Naming flags too broadly may make a read-only probe look like a general
  orientation or recommendation feature.
- Showing candidate concern or next safe move in V1 may imply intent inference or
  action guidance even with labels.
- Related-material matching may be mistaken for relevance truth.
- State Summary ordering may be mistaken for importance.
- Source-navigation matches may be mistaken for ownership, behavior, or call
  evidence.
- CLI-local rendering may accumulate semantic policy if the helper is too thin.
- Persisting derived render metadata may turn tentative interpretation into a
  durable claim.

## 12. Out-of-Scope

V1 must not include:

- schema migrations;
- runtime behavior changes beyond bounded capture/render plumbing;
- facts, claims, goals, requirements, capabilities, tool needs, plans,
  proposals, or decision records derived from notes;
- provider, LLM, or tool execution;
- recommendation or action planning;
- intent, work-shape, concern, or task classification;
- candidate active concern by default;
- next safe move by default;
- semantic search or embedding-based matching;
- source-file scanning outside existing preserved source facts;
- changes to State Summary authority;
- changes to Source Navigation authority;
- retention, sync, or multi-user policy.

## 13. Final Implementation Checklist

Before implementing V1, confirm:

- [ ] Storage choice requires no migration.
- [ ] Inquiry-note records are named as evidence, not intent or work.
- [ ] Minimum provenance fields are available or explicitly omitted as unsafe.
- [ ] Capture preserves raw note text verbatim.
- [ ] Render path is read-only after note selection.
- [ ] Helper owns deterministic related-material semantics.
- [ ] CLI owns only parsing, dispatch, and formatting.
- [ ] Output includes raw note, potentially related material, support / why
      related, uncertainty, and authority boundary.
- [ ] Output excludes candidate active concern, next safe move, recommendation,
      default.
- [ ] Related-material matching is deterministic and supportable.
- [ ] No LLM, provider, tool, plan, proposal, or action path is invoked.
- [ ] Tests prove notes are not projected into facts/goals/tool needs or other
      runtime decision artifacts.
- [ ] Tests prove read-model construction does not mutate State.
