# Event And Change Reconciliation

## Purpose

This document performs a documentation-only reconciliation of events, changes,
state transitions, historical occurrences, consequences, claims, and temporal
reasoning.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify observations, facts,
relationships, projections, recommendations, decisions, commands, actions,
timelines, storage models, event systems, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established claim strength and assertion semantics,
historical versus current claims, freshness and knowledge quality,
recommendation relevance and consequences, and operator intent and goals. A
recurring architectural question remains:

```text
What is an event?
```

Examples include:

```text
package installed
package removed
service started
service stopped
host rebooted
filesystem detached
configuration changed
```

These do not behave like simple current-state claims. They describe things that
happened, may explain current conditions, and may remain historically true after
the current state changes again.

## Central Finding

The safest architectural answer is:

```text
Events describe occurrences.
Claims describe propositions about knowledge.
State describes selected conditions at a time.
Changes describe transitions between states or values.
Consequences describe outcomes that may follow from conditions or occurrences.
Projections describe selected interpretations for a purpose, commonly current.
```

Therefore:

```text
Event
  ≠ current state
  ≠ normalized fact by itself
  ≠ contradiction by itself
  ≠ consequence by itself
  ≠ recommendation by itself
```

An event can be represented by claims, supported by observations and evidence,
used by projections, connected to consequences, and cited by recommendations.
But the event itself is the occurrence being described, not every object that may
record, support, interpret, or respond to that occurrence.

## Files Considered

This reconciliation builds on existing architectural documentation, especially:

- `docs/claim_strength_and_assertion_semantics_reconciliation.md`
- `docs/evidence_strength_and_claim_strength_reconciliation.md`
- `docs/observation_refresh_and_knowledge_freshness_reconciliation.md`
- `docs/goal_relevance_and_recommendation_generation_reconciliation.md`
- `docs/knowledge_lifecycle_reconciliation.md`
- `docs/temporal_reasoning_audit.md`
- `docs/state.md`
- `docs/invariants.md`

## Boundary Summary

| Concept | Primary role | Answers | Must not become |
| --- | --- | --- | --- |
| Observation | Source-attributed report | What did a source report from a vantage point at a time? | Event, fact, current truth, action result |
| Evidence | Provenance and support material | Why may Seed consider a claim? | Claim, event, truth arbitration |
| Claim | Scoped proposition represented or interpreted by Seed | What proposition is available for reasoning? | Occurrence, current state, universal truth |
| Fact | Normalized provenance-backed claim | What proposition has Seed normalized? | Raw event, selected current state, verified reality |
| Event | Occurrence in the world or operational domain | What happened, when, and in what scope? | Current state, consequence, recommendation |
| State | Condition or value at a time or interval | What was, is, or is projected to be true in a scope? | Event history, contradiction, transition |
| Change | Transition between distinguishable states or values | What became different between before and after? | Mere disagreement, current state, replacement record |
| Consequence | Outcome, impact, or risk arising from a condition or occurrence | What did, could, or may result? | Event, goal, decision, command |
| Projection | Selected interpretation over preserved knowledge | What view should be used for a purpose? | Source of historical truth, action, observation |
| Recommendation | Advisory relevance path from condition/consequence to goal | What should be considered and why? | Decision, command, event, consequence |

## 1. What Is an Event?

An event is an occurrence with temporal and contextual identity.

It answers:

```text
What happened, in what scope, according to what support, at what event time or
reported time?
```

Examples:

```text
package nginx was installed on host H at time T
package nginx was removed from host H at time T2
service nginx stopped on host H at time T3
host node115 rebooted at time T4
filesystem /data detached from host H at time T5
configuration file C changed from version A to version B at time T6
```

An event is not necessarily a current-state claim. `nginx installed on date X`
can remain true after `nginx removed on date Y`. `host rebooted yesterday` can
remain true even if the host is now stable. `filesystem detached at 10:00` can
remain true after the filesystem is reattached at 10:15.

Architecturally, an event should be understood as the occurrence being reasoned
about. Seed may preserve event knowledge through observations, evidence,
ledger entries, facts, relationships, or narrative explanations, but none of
those storage or read-model objects should be treated as identical to the
occurrence in all contexts.

### Are events claims, observations, facts, relationships, consequences, or something else?

Events are something else conceptually: they are occurrences.

They may be expressed through claims:

```text
Claim: host node115 rebooted at 2026-06-09T12:00:00Z
```

They may be reported by observations:

```text
Observation: system log source reported reboot marker at T
```

They may be normalized as facts:

```text
Fact: node115 had reboot occurrence at T, supported by log evidence
```

They may participate in relationships:

```text
Event E affected service S
Event E occurred_on host H
```

They may produce or explain consequences:

```text
Event: filesystem detached
Consequence: service became unavailable
```

But the event is still the occurrence. The claim asserts or represents it; the
observation reports it; the fact normalizes it; the relationship links it; the
consequence describes an outcome of it.

## 2. What Is a Change?

A change is a transition between distinguishable states, values, or conditions
across time or version scope.

It answers:

```text
What was different after a transition compared with before it?
```

Examples:

```text
Before: service nginx running
After:  service nginx stopped
Change: service nginx transitioned from running to stopped

Before: package nginx installed
After:  package nginx absent
Change: package nginx transitioned from installed to absent

Before: config checksum abc
After:  config checksum def
Change: configuration content changed from abc to def
```

A change differs from state because state describes a condition at a time or
interval, while change describes the transition between conditions.

A change differs from an event because an event is an occurrence and a change is
the transition described or implied by one or more occurrences. Some events are
change events (`service stopped`), while others may be occurrences without a
modeled before/after pair (`backup failed`, `host rebooted`, `operator approved
plan`).

A change differs from contradiction because contradiction is disagreement among
claims or selected values within a scope. A valid state transition can produce
claims that look different without being contradictory:

```text
At T1: service running
At T2: service stopped
```

Those two propositions conflict only if they are asserted for the same temporal
scope and incompatible state model. With explicit times, they describe history.
Without times or scope, they may be ambiguous, stale, or over-strong, but not
necessarily a logical contradiction.

A change differs from replacement because replacement is often a storage or
projection behavior: one selected value takes the place of another in a current
view. The historical change is the transition itself; the replacement is a view
or data-management consequence of selecting a current value.

## 3. Relationship Between Events and Claims

Events and claims are related but not identical.

A claim is a scoped proposition. An event is an occurrence that a claim may
assert, deny, qualify, or interpret.

Example:

```text
Claim: nginx is installed on host H as of projection time Q
Event: nginx was installed on host H at time X
Event: nginx was removed from host H at time Y
```

The install event may support a historical claim that nginx was installed at X.
It may also support a current-state claim only if no stronger or more relevant
later knowledge indicates removal, expiry, uncertainty, or narrower scope. The
remove event may support a current projection that nginx is absent while leaving
the historical install event true.

Events may therefore:

- support claims about occurrences;
- support claims about prior state;
- contribute to current-state selection;
- explain why a current state is believed;
- qualify claim strength by adding temporal scope; and
- conflict with overbroad claims that omit required time or scope.

Events should not be treated as automatically creating timeless claims. The
claim form matters:

```text
Event-supported historical claim: nginx was installed at X.
Over-strong current claim: nginx is installed now.
Projection claim: nginx is currently selected installed as of Q under rules R.
```

A single event may justify the first, may be insufficient for the second, and may
contribute to the third only through projection rules and freshness expectations.

## 4. Relationship Between Events and State

State describes a condition, value, or selected interpretation at a time or over
an interval. Events describe occurrences that may establish, modify, terminate,
or explain state.

Example:

```text
Event: service nginx stopped at T
Current state: service nginx unavailable as of Q
```

The event may be evidence for the current state, but it is not the current state
itself. Additional evidence may show the service restarted after T. The stopped
event remains historically true, while the current-state projection may select
`available` after a later start event or successful health check.

Useful distinctions:

| Statement | Boundary |
| --- | --- |
| `service stopped at T` | Event or historical event claim |
| `service was stopped during interval I` | Historical state claim |
| `service is stopped now` | Current-state claim |
| `projection selects service stopped as of Q` | Projection claim |
| `service unavailable because it stopped at T` | Explanation connecting event to current state |

Events can explain state without being state. State can be selected without
explicit event modeling when observations directly report current conditions.
Changes connect prior and later state, but projections decide what current
interpretation is selected for a given read purpose.

## 5. Relationship Between Events and Historical Knowledge

Historical knowledge is knowledge whose truth or usefulness is scoped to a past
time, interval, sequence, or occurrence. Events are a central form of historical
knowledge because they preserve that something happened.

History can remain true while current state changes:

```text
George Washington was President of the United States.
node115 rebooted yesterday.
package nginx was installed last year.
filesystem /data detached at 10:00 and reattached at 10:15.
```

None of these statements requires the corresponding current state to still hold.
George Washington is not currently president; the node may now be healthy; the
package may now be removed; the filesystem may now be attached. The historical
occurrence remains true if the evidence and scope support it.

Events can remain useful after current state changes because they may support:

- audit trails;
- incident timelines;
- causal explanations;
- recurrence detection;
- baseline comparison;
- compliance or accountability reasoning;
- recommendation relevance; and
- operator trust in explanations.

Historical preservation should not require current-state relevance. If history
is retained only when it remains currently selected, Seed loses the ability to
explain change, diagnose regressions, learn patterns, or answer temporal
questions.

## 6. Relationship Between Events and Consequences

Consequences describe outcomes, impacts, or risks that did, could, or may result
from a condition or occurrence. They may arise from events, state claims,
changes, or combinations of these.

Examples:

```text
Event: filesystem detached
Consequence: service became unavailable

State: filesystem remains detached
Consequence: service remains unavailable and data writes fail

Change: configuration changed from valid to invalid
Consequence: service reload failed

Claim: backup failed last night
Consequence: increased data-loss exposure until successful backup is confirmed
```

A consequence is not the event itself. The event says what happened; the
consequence says what resulted, may result, or matters because of what happened.

Consequences may be observed, inferred, projected, or hypothetical. They should
retain their own evidentiary and modal character:

```text
Observed consequence: service outage began after detach event.
Inferred consequence: detach likely caused service unavailability.
Projected consequence: continued detachment may prevent recovery.
Hypothetical consequence: if detachment recurs, failover may be required.
```

This preserves the boundary established by recommendation relevance: the
condition or occurrence matters to a goal through possible or observed
consequences, not by becoming the goal or recommendation.

## 7. Relationship Between Events and Recommendations

Event knowledge participates in recommendation relevance by supplying the
condition, trigger, explanation, or history that connects a possible consequence
to an operator-owned goal.

Example:

```text
Event: backup failed at T
Consequence: recovery point objective may be at risk
Goal: preserve recoverability
Recommendation: investigate backup pipeline
```

The recommendation is not justified merely because an event exists. It is
justified when Seed can explain both:

```text
Evidence path: why believe or consider the event or condition?
Goal relevance path: why does the event's consequence matter to the goal?
```

Events may make recommendations relevant even after the direct current state has
changed. For example, a failed backup event may remain relevant until a later
successful backup, integrity verification, or policy-specific recovery objective
is satisfied. A reboot event may remain relevant to reliability investigation if
it is part of a repeated pattern, even if the host is currently healthy.

Recommendations should not collapse event history into action authority. An
event can justify considering an investigation; it does not approve commands,
select a decision, or prove that an action is safe.

## 8. Relationship Between Events and Freshness

Freshness evaluates how recent support is relative to the question and expected
rate of change. Event knowledge interacts with freshness differently from
current-state knowledge.

An event can be historical but not stale when the question is historical:

```text
Question: Did node115 reboot yesterday?
Event evidence: reboot marker from yesterday with stable log provenance
Freshness interpretation: not stale for that historical question
```

The same event may be stale or insufficient for a current-state question:

```text
Question: Is node115 healthy now?
Event evidence: reboot marker from yesterday
Freshness interpretation: insufficient for current health without newer support
```

Some event knowledge may be permanently useful for historical, audit, or causal
purposes if the occurrence itself is not expected to change. The fact that an
event happened does not become false merely because time passes. However, event
knowledge can degrade in other ways:

- source trust may be questioned;
- timestamp precision may be inadequate;
- event identity may be ambiguous;
- causal interpretation may be weakened by later evidence;
- relevance to a current goal may expire;
- retention or provenance may be incomplete; and
- newer events may change current-state implications.

Thus, event freshness depends on the question:

| Question | Freshness implication |
| --- | --- |
| Did event E happen at T? | Historical support may remain fresh if provenance is stable. |
| Is the effect of E still present? | Requires current or interval evidence. |
| Is E part of an ongoing pattern? | Requires sequence and recurrence evidence. |
| Does E matter to the current goal? | Requires consequence and goal relevance context. |

## 9. What Should Not Be Collapsed Together?

The following should remain distinct:

```text
Current State:       nginx installed
Historical Event:    nginx installed on date X
Change:              nginx removed on date Y
Current Projection:  nginx absent as of projection time Q
```

They are distinct because they answer different questions:

| Object | Question answered |
| --- | --- |
| Current state | What condition is selected or believed now? |
| Historical event | What happened at a past time? |
| Change | What transition occurred between before and after? |
| Current projection | What interpretation is selected by view rules at projection time? |

Collapsing them causes architectural errors:

- treating old install events as proof of current installation;
- treating removal as contradiction rather than transition;
- deleting history when current projection changes;
- losing explanations for why the current state changed;
- overstating claim strength by omitting time scope;
- making recommendation relevance depend only on current state; and
- confusing evidence age with historical falsity.

A current projection may select `nginx absent` while Seed also preserves that
`nginx was installed on date X`. Both can be true under their scopes.

## 10. Role of Time

Time is not owned by a single layer. It appears in several different contexts
and should not be flattened into one timestamp concept.

| Time role | Meaning | Example |
| --- | --- | --- |
| Evidence context | When support was observed, reported, collected, or valid for a source | log line collected at T, metric sample interval I |
| Event context | When the occurrence happened or was reported to have happened | service stopped at T |
| Claim context | The temporal scope of the proposition | package was installed during interval I |
| State context | The time or interval for the condition | service running at T1, stopped at T2 |
| Change context | The before/after ordering or transition interval | config changed between version A and B |
| Projection context | When and under what replay/selection rules a view was produced | current projection as of event id N and projection time Q |
| Freshness context | How recent the support is relative to the question | package inventory from 30 days ago |
| Consequence context | When an outcome occurred, may occur, or remains possible | outage began after detach event |
| Recommendation context | Why the occurrence or consequence matters now or for a goal horizon | investigate repeated backup failures this week |

Time therefore provides evidence context, event context, claim context, state
context, projection context, freshness context, consequence context, and
recommendation context. Each role should be explicit enough to avoid promoting a
historical statement into a current one or demoting a durable historical event
into stale noise.

## Historical Truth Versus Current Truth

Historical truth and current truth are different scopes, not different quality
levels.

```text
Historical truth: package P was installed at T.
Current truth: package P is installed now.
```

A historical truth can be high quality even when it has no current-state effect.
A current truth can be weak if it depends on stale evidence. Current truth may
change; historical truth about an occurrence remains scoped to what happened.

This distinction supports several invariants:

- an occurrence may remain true after state changes;
- an event may explain current state without being current state;
- a later state transition does not erase an earlier event;
- a change is not automatically a contradiction; and
- historical preservation should not require current-state relevance.

## Architectural Invariants

The findings support the following architectural invariants:

```text
Claims describe knowledge propositions.
Events describe occurrences.
States describe conditions or values at a time or interval.
Changes describe transitions between states or values.
Consequences describe outcomes, impacts, or risks.
Projections describe selected interpretations for a purpose.
Recommendations describe advisory relevance paths, not decisions or commands.
History should survive state change.
An event may remain true after its effects disappear.
Current state and historical occurrence are different concepts.
Consequences may connect events to goals.
Freshness is question-relative and does not make historical events false.
Contradictions require incompatible claims in the same relevant scope.
```

## Non-Goals

This reconciliation does not propose or require:

- a new event schema;
- a new change schema;
- a new historical database;
- a new timeline implementation;
- new projection behavior;
- new fact cardinality behavior;
- new contradiction behavior;
- new recommendation generation behavior;
- new freshness scoring behavior;
- changes to observations, facts, relationships, actions, commands, or tests;
- automatic causal inference from event order;
- automatic conversion of events into current-state claims; or
- automatic deletion of history when current projections change.

## Implementation Implications

Because this is a documentation-only boundary audit, implementation implications
are limited to interpretive constraints for future design and review:

1. Future designs should preserve the distinction between occurrence knowledge
   and current-state selection.
2. Event-supported claims should carry enough temporal and scope context to avoid
   over-strong current assertions.
3. Change reasoning should distinguish transitions from contradictions.
4. Consequence reasoning may use events, states, changes, and claims as inputs,
   but consequences should remain separate from those inputs.
5. Recommendation explanations should be able to cite event history when it
   provides the evidence path or goal relevance path.
6. Freshness review should ask which question is being answered before labeling
   event knowledge stale.
7. Historical preservation should be evaluated independently from current-state
   relevance.

These are boundary constraints, not requests to modify runtime behavior.

## Example Reconciliations

### Package installed, then removed

```text
T1 Event: package nginx installed
T2 Event: package nginx removed
Q Projection: package nginx absent
```

Valid interpretations:

- `nginx was installed at T1` may remain historically true.
- `nginx was removed at T2` may explain current absence.
- `nginx is absent as of Q` may be the current projection.
- `nginx installed now` is not supported by T1 alone after T2.

### Service stopped, then restarted

```text
T1 State: service running
T2 Event: service stopped
T3 Event: service started
Q State: service available
```

The stopped event remains useful for incident analysis even if the current state
is healthy. The transition from running to stopped is a change. The later start
event may change the current projection without deleting the stop event.

### Filesystem detached with service impact

```text
Event: filesystem /data detached
Consequence: dependent service unavailable
Goal: maintain service availability
Recommendation: investigate detach cause and restore stable storage attachment
```

The event explains the condition. The consequence connects the event to the
goal. The recommendation is relevant through that consequence but does not own
the event, consequence, decision, or action.

### Historical public office example

```text
Historical claim: George Washington was President of the United States.
Current claim: George Washington is President of the United States.
```

The historical claim can be true while the current claim is false. Treating both
as one timeless predicate would erase the temporal boundary that makes each
statement meaningful.

## Conclusion

Seed should reason about things that happened by preserving the conceptual
boundary between occurrences, propositions, conditions, transitions, outcomes,
and selected interpretations.

The key reconciliation is:

```text
An event is an occurrence.
A change is a transition.
A claim is a proposition about knowledge.
A state is a condition at a time or interval.
A consequence is an outcome or risk.
A recommendation is an advisory relevance path.
A projection is a selected interpretation.
```

Events can support claims, explain states, participate in changes, cause or
suggest consequences, and make recommendations relevant. They should not be
collapsed into current state, contradiction, consequence, or recommendation.
History should survive state change, and freshness should be evaluated relative
to the question being asked.
