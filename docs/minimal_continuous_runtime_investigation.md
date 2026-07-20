# Minimal Continuous Runtime Investigation

## Purpose and scope

This document investigates the smallest useful continuous runtime for Seed. It is
architectural exploration only. It does not implement runtime behavior, agent
behavior, chat, active-edge detection, lens selection, orientation inference,
task management, memory systems, or LLM integration.

The operational distinction tested here is:

```text
continuous runtime != chat interface
```

A continuous runtime, at its smallest useful scale, appears to preserve selected
participant context across otherwise separate command invocations. A chat
interface is only one possible interaction surface over such context and is not
required by the evidence reviewed here.

## Files inspected

Core architecture and implementation-facing surfaces inspected:

- `02-domain-model.md`
- `03-runtime-loop.md`
- `seed_runtime/runtime.py`
- `seed_runtime/events.py`
- `seed_runtime/state.py`
- `seed_runtime/projection_store.py`
- `seed_runtime/state_views.py`
- `seed_runtime/state_summary_views.py`
- `seed_runtime/source_navigation.py`
- `seed_runtime/inquiry_orientation.py`

Continuity, orientation, activation, inquiry, active-edge, and lens documents
inspected:

- `docs/continuation_context_and_working_state_reconciliation.md`
- `docs/current_work_position_frontier.md`
- `docs/active_edge_frontier.md`
- `docs/working_state_activation_observation.md`
- `docs/working_state_activation_artifact_audit.md`
- `docs/working_state_activation_failure_observation.md`
- `docs/orientation_bundle_load_bearing_observation.md`
- `docs/orientation_non_convergence_audit.md`
- `docs/orientation_object_observation.md`
- `docs/work_shape_and_orientation_observation.md`
- `docs/work_recognition_observation.md`
- `docs/inquiry_preservation_observation.md`
- `docs/inquiry_note_orientation_surface_reachability_observation.md`
- `docs/inquiry_orientation_surface_family_observation.md`
- `docs/inquiry_as_bridge_observation.md`
- `docs/inquiry_as_movement_observation.md`
- `docs/inquiry_connectivity_and_staleness_audit.md`
- `docs/lens_as_observation_and_compression_pattern.md`
- `docs/lens_catalog_observation.md`
- `docs/lens_implementation_frontier_observation.md`
- `docs/lens_orientation_and_dashboard_observation.md`
- `docs/lens_view_architecture_audit.md`
- `docs/lens_view_reconciliation.md`
- `docs/lens_vs_orientation_observation.md`
- `docs/operator_understanding_surface_observation.md`
- `docs/operator_surface_family_observation.md`
- `docs/operator_navigation_reconciliation.md`
- `docs/source_navigation_surface_reconciliation.md`
- `docs/source_navigation_without_grep_audit.md`

## 1. What information currently survives across commands?

Seed already preserves several durable or rebuildable surfaces across command
boundaries:

1. **Append-only events.** `EventLedger` records runtime events and can list them
   by workspace. `SQLiteEventLedger` persists the same event shape to SQLite.
2. **Projected State.** `StateProjector` rebuilds `State` from workspace events.
   The domain model treats State as projected rather than authoritative.
3. **Facts, evidence, goals, tool needs, entities, relationships, and graph
   validation issues.** These survive when represented as ledger-backed state or
   deterministic projections.
4. **Projection snapshots.** `ProjectionStore` can cache rebuildable current
   projections when the snapshot last event matches the current ledger tip.
5. **Decision and runtime trace events.** Runtime input, proposed decisions,
   answers, questions, refusals, and related events survive as event history.
6. **Documentation artifacts.** Inquiry notes, frontiers, reconciliations,
   observations, maps, and audits preserve architectural findings and current
   inquiry pressure outside the runtime database.
7. **Sessions as event lenses.** Sessions exist, but the domain model explicitly
   says they are not the source of truth.

## 2. What information currently resets between commands?

The recurring reset is not primarily factual state. It is participant-position
state. The following appear to reset unless captured in a document or event:

- the immediate investigation question;
- why this question mattered now;
- the current object of attention;
- the active pressure or tension;
- the selected boundary being tested;
- what was just completed;
- the live reasoning branch;
- what remained unresolved;
- the next safe move;
- which adjacent paths were intentionally out of scope;
- which notes or findings were already consumed and activated;
- why a lens, orientation bundle, or active edge was selected rather than merely
  visible.

This explains why repository inquiries repeatedly ask: "What was I
investigating?", "Why was I looking at this?", "What changed since last time?",
"What remains unresolved?", and "What work is still active?" The stored state can
answer many "what exists" questions, but it does not by itself answer the
participant-context question: "where was the work standing?"

## 3. What architectural concepts appear to require continuity?

The strongest continuity-requiring concepts are:

- **Continuation context.** It is explicitly about safe, coherent resumption
  after interruption and includes working-state information that is neither full
  history nor authority.
- **Working state / current work position.** These concern the current work
  location relative to known artifacts, unresolved questions, constraints, and
  safe movement.
- **Activation.** Activation distinguishes available or read information from
  information that becomes live in working state.
- **Active edge.** Active edge concerns the selected unresolved boundary pulling
  work forward; it is hard to recognize from durable facts alone.
- **Orientation.** Orientation bundles appear to combine current concern,
  pressure, boundary, active edge, continuation, next safe move, selection
  rationale, and validation state.
- **Inquiry preservation.** Inquiry notes preserve more than outcomes; they
  preserve movement through unresolved understanding.
- **Lens discovery.** Lens work appears related to repeated observation and
  compression patterns, not just a single static view.

## 4. What concepts appear fully compatible with one-shot execution?

The repository already supports many one-shot commands and read models well:

- state summary;
- current facts;
- stale facts;
- unsupported facts;
- graph issues;
- contradictions;
- relationships;
- source navigation;
- runtime trace / why-run rendering;
- capability inventory and verification inspection;
- projection-cache rebuild or reuse;
- deterministic context packet composition for one input event.

These surfaces can project, summarize, audit, or explain durable state without
remembering the participant's active reasoning branch across command invocations.
They may support continuity, but they do not themselves preserve continuity.

## 5. Current continuity inventory

| Mechanism | What survives | What does not survive | Primary consumers |
| --- | --- | --- | --- |
| Event ledger | Ordered events, workspace scope, actors, payloads, session IDs, causation/correlation links. | Participant attention, active concern, consumed/activated status unless encoded as events. | State projection, runtime trace, explanations, audits, owner services. |
| SQLite event ledger | Durable version of ledger events. | Same as event ledger; persistence does not imply currentness or activation. | CLI/API/local runtime state across processes. |
| State | Projected entities, facts, goals, tool needs, evidence, relationships, issues, pending/action-like records. | Why a participant is looking at one part of state now; active inquiry movement. | Context composer, state views, source navigation, summaries, inspections. |
| Facts | Claims with provenance, freshness, confidence, subject, predicate, value. | Inquiry rationale, selected tension, active edge, participant concern. | State views, context packets, fact index, integrity and contradiction views. |
| Evidence | Raw immutable observations supporting facts. | Interpretation movement after evidence is noticed; why evidence is currently relevant. | Fact extraction, support, verification, audit/explain surfaces. |
| Claims / fact support | Aggregated support and conflicts around claim values. | Which conflict matters now and what question it is serving. | Current-fact views, contradiction/support/integrity views. |
| Relationships / topology | Deterministic edges, aliases, validation issues, relationship-derived navigation. | Active relationship of use, selection rationale, or pressure. | Relationship views, graph issues, source navigation, explanations. |
| Goals | Durable objectives with status and open questions when represented. | Fine-grained current work position inside an active investigation. | Context composer, runtime decisions, summaries. |
| Tool needs / capability gaps | Needed capability, risk hints, desired inputs/outputs, recommendations. | Operator's current investigation path around the gap unless explicitly recorded. | Runtime request_tool path, capability recommendation/inventory views. |
| Decision journal / runtime events | Input, proposed decision, validation result, outcome, context hash/traceable event path where used. | Ongoing participant understanding outside the single run. | Trace, why-run, explain/audit surfaces. |
| ProjectionStore / cached projections | Rebuildable current state snapshots keyed by last event and version. | Authority, participant context, activation, or active inquiry state. | CLI/API performance paths, state-view commands. |
| ContextPacket | Current input, selected active goal, entities, facts, tools, open tool needs, evidence, schema. | Continuity across commands unless the selected context already exists in State/events; post-command participant movement. | Decision providers and runtime validation. |
| State views / summaries | Read-only projections for operator understanding. | Active concern and next safe move unless provided by surrounding inquiry context. | CLI/API/operator surfaces. |
| Source navigation | Routes to evidence and source support. | Why this route is the currently active route. | Operator/source audit and navigation surfaces. |
| Inquiry notes / docs | Findings, questions, boundaries, search paths, inspected files, open tensions, lineage. | Automatic activation in a future participant's working state; canonical runtime state. | Human and model participants, future investigations, docs navigation. |
| Continuation / handoff artifacts | Current work-position, next safe move, constraints, unresolved questions when authored. | Runtime enforcement; proof that a consumer activated them. | Future participants and handoff readers. |

## 6. Is inquiry-note preservation the first example of participant-context preservation?

It is a strong early example, but not the only continuity mechanism. The event
ledger preserves system history; State preserves projected domain knowledge;
handoff and continuation documents preserve work-position context. Inquiry-note
preservation is distinctive because it preserves **participant-context movement**:
what was being investigated, why it mattered, what path was taken, what remained
unresolved, and which surrounding documents or concepts were active.

So the answer is:

```text
inquiry-note preservation is not the first persistence mechanism;
it may be the clearest current example of participant-context preservation.
```

## 7. Minimum runtime capable of preserving continuity

The smallest useful continuous runtime suggested by the evidence is not a chat
interface and not an autonomous agent. It is a thin participant-context runtime
that can preserve and retrieve a bounded continuation record across invocations.

Architectural characteristics only:

- accepts discrete command invocations;
- records a compact participant-context artifact for the current work episode;
- binds that artifact to workspace, session or work stream, triggering input,
  inspected artifacts, current concern, active pressure, unresolved questions,
  constraints, and next safe move;
- can present that artifact back to later commands as context;
- keeps event ledger and State authority boundaries intact;
- treats cached projections as cache, not memory authority;
- does not converse, plan autonomously, infer active edge, select lenses, or
  execute tasks by itself.

In other words, minimum useful continuity is:

```text
one-shot command execution
+ durable participant-context record
+ retrieval/presentation of that record at the next relevant invocation
```

## Runtime-level comparison

| Level | Name | Architectural characteristic | Compatible with current evidence? | Not included |
| --- | --- | --- | --- | --- |
| 0 | One-shot commands only | Each command projects state, runs, renders, exits. Durable facts/events/docs may exist, but no participant context is actively carried. | Already present and useful for state/read-model commands. | Continuation, activation, active work-position. |
| 1 | Persistent inquiry context | Preserves inquiry notes, inspected files, open questions, path, and unresolved tension across invocations. | Strongly supported by recent inquiry-preservation work. | General participant profile, chat, autonomy. |
| 2 | Persistent participant context | Preserves current concern, active pressure, selected boundary, constraints, recent movement, activated references, and next safe move for a participant/session/work stream. | Appears to be the smallest useful continuous runtime for Seed. | Natural language conversation, active-edge detection, lens inference, task management. |
| 3 | Conversational runtime | Adds multi-turn natural-language interaction over participant context. | Possible surface, but not required by the architectural pressure. | Autonomy by default. |
| 4 | Autonomous runtime | Initiates, selects, plans, detects active edges/lenses, and manages tasks. | Explicitly outside this investigation and not required for minimal continuity. | N/A. |

A Level 1 runtime may be enough if the scope is only inquiry-note preservation. A
Level 2 runtime is the smallest general answer to the recurring questions about
what was active, why it mattered, and what remained unresolved. Level 3 is a UI
choice. Level 4 is a different product category.

## Relationship to inquiry notes

Inquiry notes are already doing much of the work that a minimum runtime would
need to preserve: inspected files, purpose, scope boundaries, search terms,
findings, unresolved questions, and current pressure. Their limitation is that
they are passive artifacts. A future participant can find and read them, but the
repository's activation documents show that availability and consumption do not
guarantee that the content becomes active in working state.

Therefore inquiry notes are evidence for continuity need, not proof that a
conversational interface is needed.

## Relationship to orientation

Orientation appears to require continuity when the relevant question is not
"what exists?" but "how should this participant enter the current work?" The
orientation bundle evidence suggests that current concern, pressure, boundary,
active edge, continuation posture, next safe move, selection rationale, and
validation state often need to remain related. One-shot commands can display
some of these pieces, but the relation among them is often reconstructed from
surrounding documents.

Continuity is therefore necessary for orientation when orientation means
resumption into active work. It is less necessary when orientation only means a
static map or inventory.

## Relationship to active edge

Active edge is not just another fact about the repository. It is the selected
unresolved boundary that explains why work is pulled in a particular direction.
Because selection, unresolvedness, pressure, and safe movement can change over
time, active-edge concepts appear continuity-dependent. A one-shot command can
surface candidates or evidence, but preserving which edge was active and why is
participant-context preservation.

This does not imply implementation of active-edge detection. The investigation
only observes that active-edge meaning is temporal and selection-dependent.

## Relationship to lens discovery

Lens discovery may sometimes begin in a single inquiry: one investigation can
notice that a repeated compression pattern makes scattered evidence legible.
However, repository lens work appears stronger when a pattern recurs across
inquiries, documents, and operator surfaces. A lens differs from a one-time view
when it survives as a reusable way to compress or re-orient future understanding.

Continuity appears helpful for lens discovery because repeated inquiry over time
is what distinguishes durable lens pressure from a local observation. Continuity
also appears helpful for orientation because a lens is useful only when the
participant can understand why that lens is relevant now. Continuity appears
helpful for active-edge concepts because active edge supplies the temporal pull
that may make one lens useful and another merely available.

## What survives today

Today, Seed can preserve events, projected facts/state, evidence, relationships,
tool needs, runtime traces, cached projections, source-navigation routes, and
written inquiry artifacts. It can also preserve sessions as lenses over events.

## What resets today

Today, unless a participant writes it into an inquiry note, handoff, event, or
other artifact, the following reset between isolated command invocations:
current concern, active pressure, work-position, activated references, current
reasoning branch, selected boundary, unresolved question, and next safe move.

## Minimum useful runtime analysis

The smallest useful continuous runtime is a continuity carrier, not a chat loop.
Its architectural purpose would be to keep a bounded participant-context record
alive across commands so future invocations can resume from the current work
position without rebuilding it from scratch. This runtime would be continuous
because it preserves selected context over time, not because it is always running
or conversational.

## Recommended next investigation

Investigate the boundary of a **participant-context artifact** without proposing
implementation. The next investigation should ask:

```text
What fields are necessary and sufficient to preserve current work position
without turning Seed into a planner, chat agent, memory system, or active-edge
inference engine?
```

That investigation should compare inquiry notes, handoff templates, runtime
trace summaries, and ContextPacket content to determine what is already present,
what is missing, and what must remain documentation-only.

## Files changed

- `docs/minimal_continuous_runtime_investigation.md`

## LOC changed

- Added approximately 275 documentation lines.
