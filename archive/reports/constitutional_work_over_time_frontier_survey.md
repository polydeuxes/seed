# Constitutional Work Over Time Frontier Survey

Repository authority wins.

## Investigation scope

This is exactly one Constitutional Frontier Survey.

It answers only this bounded question:

```text
Across recurring constitutional
recoveries,

what constitutional work,
if any,

is consistently performed by
durable work that exists
across time?
```

The phrase `work over time` is treated only as investigation pressure. This survey does not assume that work, pending work, elapsed time, queues, orchestration, scheduling, external ownership, or background execution are constitutional participants.

The investigation reviewed recurring constitutional evidence involving producer -> artifact -> consumer handoffs, event ledger behavior, pending-action and action-plan evidence, state patch behavior, repository observation, bounded lawful reliance, lawful acceptance, compatibility preservation, responsibility recovery, implementation recovery methodology, inquiry orientation, lawful stop, Unknown preservation, projection, replay, and operational timing visibility. Implementation evidence is used only where it reinforces recurring constitutional behavior.

This survey does not implement scheduling, planning, orchestration, autonomous execution, retry logic, timeout policy, workflow engines, queues, background workers, or runtime behavior.

## App authority check

The app was used as a read-only authority check, not as a source of new constitutional vocabulary.

Commands run:

```text
python scripts/seed_local.py --observe-repository . --quiet-output
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-subject pending --candidate-kind presentation_label --knowledge-reachability-audit-json
python scripts/seed_local.py --knowledge-reachability-audit --knowledge-reachability-audit-subject work --candidate-kind presentation_label --knowledge-reachability-audit-json
python scripts/seed_local.py --question-surface-inventory --summary-only
```

Repository observation reported a clean Git repository on branch `work` before this survey was written. The knowledge reachability checks returned no reachable rows for `pending` or `work` as presentation-label candidates in the current empty projected state. That result is not proof that those words lack ordinary use in documents; it is only an app-backed warning against promoting the investigation vocabulary into repository knowledge without implementation-backed reachability. The `--question-surface-inventory --summary-only` command failed because `--summary-only` belongs to the documentation-structure surface in this CLI, not question-surface inventory; the failure itself reinforces exact-surface dispatch rather than semantic acceptance of similarly plausible flags.

## Recurring constitutional evidence

### 1. Durable external work first appears constitutionally as observed or awaited material, not authority

Across the reviewed recoveries, external producers may perform work outside an instantaneous local boundary: Codex implementation, provider execution, repository investigation, human review, or asynchronous artifact production. Recurring evidence does not make the external duration authoritative. The constitutional entry point remains the same smaller pattern:

```text
source or producer condition
-> observed/source-attributed material or boundary-crossing artifact
-> local evidence evaluation
```

Observation may make the producer's returned material present. It does not make the external producer's elapsed time, effort, ownership, or intent into repository authority.

This is continuous with the recent non-collapse chain:

```text
observation
!= evidence

evidence
!= warrant

warrant
!= reliance

reliance
!= acceptance

acceptance
!= mutation
```

`Work over time` does not insert a new automatic promotion step into that chain.

### 2. Producer -> artifact -> consumer handoffs preserve delayed work as artifact availability

The strongest recurring evidence adjacent to durable work is the handoff pattern. A producer completes or preserves a bounded artifact; a consumer may later use the artifact only inside the artifact's supported role.

The constitutional work is not that the producer was busy for a while. The work is that an artifact becomes available with preserved evidence, provenance, role, authority limit, negative authority, Unknowns, confidence, compatibility, and stop conditions. That availability can make a downstream consumer eligible to evaluate, rely, render, validate, project, or accept locally.

This supports a narrow sequence:

```text
dispatch/request/producer ownership
-> no local authority gained merely by waiting
-> artifact availability
-> local observation/evidence evaluation
-> bounded warrant/reliance/admission if supported
-> mutation only where separately authorized
```

### 3. Lawful reliance remains bounded downstream use, not temporal completion

`artifact_bounded_lawful_reliance_characterization.md` recovers the movement by which a repository-supported artifact can establish a bounded lawful reliance surface for a named downstream consumer. That movement depends on preserved warrant profile, not on elapsed time.

Durable work can therefore contribute to reliance only by returning or preserving an artifact that carries enough bounded support for the consumer's role. A long-running investigation, provider call, or human review does not create reliance by duration. Reliance begins only when the returned or preserved evidence is warranted for the downstream use.

### 4. Lawful acceptance remains family-local boundary admission, not completion itself

`constitutional_lawful_acceptance_characterization.md` recovers lawful acceptance as family-local boundary admission under preserved limits. That applies directly to returned artifacts: a returned artifact may be admitted by a competent local boundary if support, authority, compatibility, negative authority, Unknowns, and stop conditions remain preserved.

This does not make `artifact returned` equal to `accepted`. Return creates availability for observation and evaluation. Acceptance is a later or adjacent local boundary decision.

### 5. Event ledger behavior preserves occurrence/order/status without silently mutating cluster truth

Event-ledger evidence repeatedly separates recording from cluster mutation. Diagnostics may write event-ledger records while preserving `mutates_cluster=false`; action-plan acceptance can append an acceptance event while not making the plan executable; repository observation and many audits remain read-only.

For durable work, this supports a smaller invariant: a ledger can preserve that some status, observation, artifact, or boundary event occurred at a point in repository history. It does not make the underlying external work authoritative, accepted, relied on, or mutative by itself.

Temporal ordering and durable record are evidence-preservation aids. They are not authority engines.

### 6. Pending-action evidence is adjacent pressure, not recovered constitutional ownership

Pending-action and runtime-loop compression recur as acknowledged adjacent work in responsibility family evidence. That evidence is important because it prevents overclaiming: the repository has not completed a broad constitutional or architectural recovery for pending-action lifecycle ownership.

Where pending appears, the recurring constitutional behavior is restraint:

- preserve the status as not-yet-complete or not-yet-admitted;
- avoid inferring completion from dispatch;
- avoid inferring acceptance from elapsed time;
- avoid inferring mutation authority from an unresolved pending condition;
- stop or preserve Unknown when the returned artifact, owner, or authority is missing.

Thus pending work is constitutionally visible as a preservation condition, not as a recovered participant.

### 7. Action-plan status separates accepted status from execution authority

Action-plan implementation evidence, as summarized by prior constitutional work, shows that accepting an action plan records an accepted status while the projected plan remains non-executable. This is highly relevant to `work over time` because an action plan can describe future or external work pressure, but accepted status does not become execution.

Supported distinction:

```text
dispatched or accepted plan/status
!= executing work
!= executable authority
!= completed artifact
!= mutation beyond separately authorized status/event recording
```

### 8. State patch behavior separates accepted operation shape from universal mutation policy

State patch evidence shows local acceptance and rejection of operation shapes. Supported patch operations may emit events; unsupported operations are rejected. Compatibility-local input shapes may be admitted, but partial application behavior prevents generalizing state patches into a universal transaction or mutation theory.

For durable work, state patch evidence supports only this: a returned or proposed change must pass a local operation boundary before event emission or state effects. The existence of prior work that produced the patch does not itself authorize the patch.

### 9. Projection and replay preserve recorded input into read surfaces; they do not validate external work

Projection and replay evidence repeatedly separates lineage, replay assessment, replay selection justification, replay selection, replay execution, projection result, diagnostics, cache status, and publication/read surfaces. The implementation may replay events and finalize projections after time has passed, and cache status may explain hit/miss/incremental replay paths.

The constitutional work is preservation and reconstruction from recorded inputs under compatibility constraints. Replay does not retroactively validate an external producer's work. Projection does not create authority for a claim. Cache visibility explains a path taken, not readiness, acceptance, or elapsed-time authority.

### 10. Timing visibility measures paths without becoming temporal authority

Time-related recoveries distinguish occurrence/source/observation/knowledge/preservation/diagnostic elapsed/progress cadence/cache visibility neighborhoods. Diagnostic elapsed timing and progress cadence can expose phase durations or decide when transient progress appears. Cache visibility can explain snapshot identity, hit/miss, incremental replay, and events applied.

Those are visibility forms. They do not support a global Time participant, scheduler, readiness gate, queue, timeout policy, or authority to continue. Durable work may be measured or displayed, but elapsed time itself does not perform constitutional promotion.

### 11. Inquiry orientation and lawful stop prevent forced continuation

Inquiry orientation and lawful-stop evidence repeatedly preserve unsupported material as Unknown, not-yet, insufficient evidence, no-pressure, unsupported, or stopped. This is central for work across time: the repository may have dispatched work, expected an artifact, or observed latency, yet still be required to stop when the artifact is absent or unsupported.

The lawful constitutional behavior is not automatic resumption. It is boundary-preserving non-inference until evidence returns and is locally evaluated.

### 12. Compatibility preservation constrains acceptance of returned artifacts

Compatibility preservation recurs in implementation recovery methodology: existing event kinds, ordering, causation, correlation, result shapes, report accessors, CLI/JSON output, diagnostic inventory, diagnostic shape audit, capability ordering, cache semantics, and answer/report surfaces are preserved unless repository evidence supports change.

For durable work, compatibility means returned artifacts and resumed processing must preserve the receiving family's existing contracts. Compatibility does not make an artifact acceptable by itself; it is one condition that may allow local admission.

## Recurring implementation evidence where applicable

### Repository observation

Repository observation exposes path, VCS, head, branch, dirty status, status availability, and remote presence while preserving read-only behavior. The app authority check used this as a present repository condition, not as mutation or acceptance authority.

### Knowledge reachability audit

The knowledge reachability checks for `pending` and `work` as presentation-label candidates returned no reachable rows in the current projected state. This supports the repository instruction not to promote presentation vocabulary into repository knowledge merely because it is useful investigation pressure.

### Exact CLI dispatch

The failed `--question-surface-inventory --summary-only` command is implementation evidence for exact dispatch discipline. A plausible flag does not become accepted by semantic fit. The implementation's actual surface grammar wins.

### Diagnostic inventory and shape-audit governance

Diagnostic surfaces carry declared record support, record scope, event-ledger behavior, diagnostic fact emission, cluster fact emission, and mutation boundaries. This reinforces that recordable outputs from durable diagnostic work must remain scoped and visible rather than silently becoming cluster truth.

### Action plans, pending actions, and tool policy

Prior implementation evidence separates validation, authorization, execution, event routing, pending-action lifecycle pressure, and action-plan acceptance. Registered operation validation and policy authorization are separate; the policy service does not execute tools, append events, create pending actions, or collapse non-allow outcomes. Action-plan acceptance records status but does not make a plan executable.

### Projection, replay, and cache status

Projection diagnostics preserve optional timing and counters; replay lineage and selection evidence preserve compatible full replay plus finalization; cache status records hit/miss/incremental replay and events applied. These implementations show durable recorded inputs can be reconstructed into current read surfaces without creating validation, scheduling, or mutation authority.

## Recovered constitutional role, if any

Recurring repository evidence does **not** support `Work Over Time`, `Pending Work`, `Durable Work`, or `Time` as standalone constitutional participants.

The shared recovered role is smaller:

```text
durable boundary preservation until artifact availability
```

More explicitly:

```text
Durable work that exists across time consistently performs constitutional work
only by preserving a boundary condition between dispatch/request/producer
ownership and later artifact availability, so that the returned or preserved
artifact can be locally observed, evaluated, warranted, relied on, accepted,
refused, or used for mutation only under separately competent authority.
```

The constitutional work is therefore not scheduling or orchestration. It is a restraint-and-handoff invariant:

```text
while work is unresolved, preserve non-promotion;
when an artifact returns, expose it as bounded material;
after return, require ordinary evidence/warrant/reliance/acceptance/mutation
boundaries again.
```

## Supported constitutional distinctions

### Observation vs dispatch

Observation makes bounded material present with provenance or evidence posture. Dispatch/request may initiate or assign external producer work, but dispatch does not itself observe the future artifact and does not authorize reliance on it.

### Dispatch vs pending work

Dispatch is a boundary event or request-like condition. Pending work is an unresolved preservation condition. Neither proves completion, artifact content, acceptance, or mutation authority.

### Pending work vs elapsed time

Pending work can persist across time. Elapsed time may be measured or displayed. Neither elapsed duration nor expected latency creates constitutional authority.

### Elapsed time vs artifact availability

Elapsed time is timing evidence or visibility. Artifact availability is the later presence of returned material that can be observed and evaluated. Time passing is not the artifact.

### Artifact availability vs acceptance

A returned artifact is available for observation and evaluation. Acceptance is family-local admission by a competent boundary under preserved limits. Return does not equal acceptance.

### Acceptance vs mutation

Acceptance may admit material for a local role. Mutation requires separate authority and implementation behavior. Accepted action-plan status, accepted diagnostic recording, and accepted state patch input do not collapse into a universal mutation right.

### Mutation vs post-mutation observation

Mutation, where authorized, changes a local event/state/cluster surface. Post-mutation observation or projection can expose the result, replay it, or render it, but that later visibility is not the mutation itself and does not retroactively expand its authority.

### Replay/projection vs validation

Replay and projection reconstruct or expose recorded state from preserved inputs. They do not validate external producer truth merely because work was previously performed or recorded.

## Recovered recurring invariants

1. **Non-promotion while unresolved.** Dispatched or pending work remains not-yet-complete and not-yet-admitted until a returned artifact or record is available.
2. **Returned artifact boundary.** Artifact return creates availability for observation/evaluation, not acceptance by itself.
3. **Producer/consumer separation.** A consumer may use only the bounded artifact role; it does not re-own producer work or infer hidden producer intent.
4. **Temporal humility.** Elapsed time, expected latency, and durable existence do not create authority, evidence sufficiency, acceptance, or mutation rights.
5. **Ledger humility.** Ledger records can preserve occurrence/order/status while remaining distinct from cluster mutation and from truth of diagnostic or external findings.
6. **Local admission only.** Acceptance, if it occurs, is family-local boundary admission under preserved limits.
7. **Compatibility preservation.** Resumed or returned work must preserve the receiving family's contracts unless repository evidence authorizes change.
8. **Unknown preservation.** Missing, late, malformed, expired, abandoned, or unsupported artifacts preserve Unknown/stop/refusal rather than inferred completion.
9. **Post-return re-evaluation.** Once an artifact returns, ordinary constitutional boundaries apply again: observation, evidence, warrant, reliance, acceptance, and mutation remain distinct.
10. **No autonomy inference.** Durable work evidence does not imply schedulers, queues, retries, workflow engines, planning authority, or autonomous execution.

## Unsupported candidate ideas

The reviewed evidence does not support:

- `Work Over Time` as a constitutional participant;
- `Pending Work` as a constitutional participant;
- Time as a scheduler, readiness gate, authority owner, or Town Clock;
- dispatch as acceptance;
- pending state as evidence sufficiency;
- expected latency as authority;
- elapsed time as warrant;
- returned artifact as automatic acceptance;
- accepted status as execution authority;
- event-ledger recording as cluster mutation;
- projection/replay as validation of external producer work;
- abandoned, expired, or resumed work as currently recovered constitutional lifecycle states;
- a workflow engine, queue, background worker, retry policy, timeout policy, or orchestration architecture.

## Preserved Unknowns

The following remain Unknown rather than promoted:

- Whether a future bounded investigation should recover a narrower pending-action lifecycle responsibility from implementation evidence.
- Whether abandoned, expired, resumed, or refused external work has recurring repository evidence beyond local status/refusal patterns.
- Whether human review and provider execution share any smaller invariant not already captured by artifact-supported bounded reliance and lawful acceptance.
- Whether event-ledger status events for operational plans deserve a dedicated constitutional characterization separate from action/mutation and lawful acceptance.
- Whether any implementation-backed surface currently records `awaiting artifact` as a stable public state rather than as investigation vocabulary.
- Whether post-completion observation has a distinct constitutional role beyond ordinary observation plus artifact availability.

## Confidence

Medium-high confidence for the negative conclusion: recurring evidence does not support a standalone constitutional participant for work, pending work, or time.

Medium confidence for the recovered smaller invariant:

```text
durable boundary preservation until artifact availability
```

Confidence is limited because pending-action lifecycle ownership remains explicitly adjacent and compressed in prior responsibility evidence, and this survey did not perform a new implementation recovery slice for pending actions.

## Recommended next bounded investigation, if any

If further work is needed, the next bounded investigation should not ask whether Seed needs scheduling or orchestration. It should ask:

```text
Across implemented pending-action and action-plan evidence,
what local status boundary, if any, separates
approved resumption, fresh authorization, recorded policy outcome,
and execution?
```

That question is narrow enough to preserve repository authority and avoid promoting durable work into autonomous architecture.

## Direct answer to the bounded question

Across recurring constitutional recoveries, durable work that exists across time consistently performs only this constitutional work:

```text
It preserves a non-promoted boundary between a dispatched/requested producer
condition and later artifact availability.
```

While unresolved, durable work preserves not-yet/Unknown/non-promotion. When an artifact returns, the artifact becomes available for ordinary local constitutional handling: observation, evidence evaluation, warrant, bounded reliance, family-local acceptance, refusal, or separately authorized mutation. Time passing, pending status, dispatch, and artifact return do not themselves create authority.
