# Capability Authority And Execution Boundary Reconciliation

## Purpose

This document performs a documentation-only reconciliation of capabilities,
commands, execution, authority, providers, and runtime mutation boundaries.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify capabilities, providers,
plans, commands, actions, approvals, execution paths, tool integrations, runtime
routing, or tests.

It does not introduce new runtime semantics.

## Central Question

Recent reconciliations established projection authority, claim semantics,
assessment boundaries, recommendation boundaries, and decision boundaries. The
remaining question is:

```text
What is a capability, and how does capability differ from execution?
```

The motivating chain is:

```text
Seed knows:     endpoint unreachable
Assessment:     endpoint unavailable
Recommendation: investigate connectivity
Decision:       investigation approved
```

That chain still leaves separate boundary questions:

```text
Can Seed perform the investigation?
What capability would perform it?
What provider would supply it?
What authority is required?
What execution path would be used?
What, if anything, mutates reality?
```

## Central Finding

Seed should preserve the following conceptual chain:

```text
Projection
  -> Assessment
  -> Recommendation
  -> Decision
  -> Capability selection
  -> Command
  -> Execution
  -> Action, if execution mutates reality
```

The useful shorthand is:

```text
Assessments interpret.
Recommendations suggest.
Decisions select.
Capabilities enable.
Commands request.
Execution performs.
Actions mutate.
```

A **capability** is an evidence-backed and scope-bounded possibility: a named
kind of work Seed can reason about as potentially performable through one or
more providers, tools, adapters, handoffs, or operation implementations.
Capability is not itself permission, not itself a command, not itself execution,
and not itself an action.

A **command** is an authorized request for bounded work through a selected
capability path. A command bridges decision to execution, but it does not prove
that execution occurred.

**Execution** is the attempted realization of a command through a concrete
provider/tool/adapter path. Execution can read, observe, query, calculate, or
mutate. Only mutation-producing execution yields an **action** in the strict
architectural sense.

An **action** is the externally visible mutation or attempted mutation of
reality. Installing a package, restarting a service, writing a file, changing an
approval record, or completing a pending action are actions. Reading inventory,
querying Prometheus, collecting observations, or inspecting a filesystem are
execution, but they are not actions unless they change the environment or durable
state beyond normal audit/event recording.

The central boundary is:

```text
Capability is possibility. Execution is realization. Action is mutation.
```

## Files Considered

This reconciliation builds on existing architectural documentation and source
shape, especially:

- `docs/assessment_recommendation_and_decision_reconciliation.md`
- `docs/recommendation_selection_boundary.md`
- `docs/adoption_decision_authority_reconciliation.md`
- `docs/operation_support_boundary_reconciliation.md`
- `docs/observation_vs_mutation_reconciliation.md`
- `docs/tool_execution_ownership_audit.md`
- `docs/pending_action_lifecycle_inventory.md`
- `docs/policy_pending_action_inventory.md`
- `docs/capability_acquisition_reconciliation.md`
- `docs/capability_need_acquisition_reconciliation.md`
- `docs/capability_gap_and_operator_bridge_reconciliation.md`
- `docs/capability_verification_vocabulary.md`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/execution.py`

## Boundary Summary

| Concept | Primary verb | Primary question | Authority shape | Must not collapse into |
| --- | --- | --- | --- | --- |
| Assessment | Interprets | What does known state mean? | Evidence-backed interpretation authority | Recommendation, decision, command, execution |
| Recommendation | Suggests | What response could be considered? | Advisory authority, if any | Decision, command, authorization |
| Decision | Selects | Which option is accepted, rejected, deferred, or escalated? | Decision authority or recorded operator/policy authority | Capability, command, execution, action |
| Capability | Enables | What kind of work is possible through a supported path? | Capability metadata, support, verification, and scope; not permission by itself | Command, provider, execution, action |
| Provider | Supplies | Who or what supplies implementation or external service behavior? | Trust/adoption/verification authority for a provider | Capability or command |
| Tool | Exposes | What callable operation interface is registered? | Registration, validation, schema, and policy-gate authority | Provider or capability |
| Adapter | Translates | How is Seed's contract mapped to a provider/tool API? | Contract mapping and validation authority | Provider or command |
| Execution path | Routes | Which concrete provider/tool/adapter route will attempt work? | Selection plus policy/preflight authority | Capability or action |
| Command | Requests | What bounded work is requested now? | Execution-request authority traceable to a decision | Execution result |
| Execution | Performs | What work was attempted through the selected path? | Runtime/executor/provider authority after policy and approval | Capability or action |
| Action | Mutates | What changed or attempted to change reality? | Mutation authority, usually strongest and most auditable | Command rationale or execution mechanics |

## 1. What Is A Capability?

A capability is a stable architectural name for a **possible class of work** that
Seed can reason about and may be able to realize through one or more supported
paths.

Examples:

```text
observe local host
query Prometheus
inspect filesystem
execute package install
restart service
lookup documentation
perform web search
```

A capability communicates four separable things, depending on available support:

1. **Possibility:** the work is representable in Seed's vocabulary.
2. **Support:** there is some known path, bridge, provider, tool, handoff, or
   implementation that may perform it.
3. **Evidence:** verification or observation may support whether the path is
   available, current, stale, provider-reported, or unverified.
4. **Scope/risk:** the possible work has a visibility scope, environmental
   scope, and mutation-risk profile.

A capability does **not** by itself communicate:

- that execution is authorized;
- that a provider is trusted or adopted;
- that required evidence is sufficient;
- that a recommendation has been accepted;
- that a command exists;
- that execution has occurred;
- that an action has happened.

Therefore capability is closest to **possibility**, enriched by support and
verification metadata. It is not implementation alone, permission alone, provider
alone, or a runtime event.

### Capability Examples

| Capability statement | Meaning | Does it authorize execution? |
| --- | --- | --- |
| `can inspect filesystem` | Seed has or knows a possible filesystem inspection path. | No. |
| `can query Prometheus` | A Prometheus query path may exist. | No. |
| `can install package` | A package-install mutation path is representable or supported. | No. |
| `capability_verified(query_prometheus)` | Evidence says the capability is verified in a scope. | No; it strengthens availability, not approval. |
| `capability unavailable` | Seed cannot currently identify a supported path. | No; it may produce a gap or recommendation. |

## 2. Capability, Provider, Tool, Adapter, And Execution Path

These concepts answer different questions.

### Capability

Capability answers:

```text
What kind of work could be done?
```

It is the semantic affordance: inspect, query, install, restart, observe,
generate, look up, transform, or hand off.

### Provider

Provider answers:

```text
Who or what supplies the work?
```

A provider may be a local toolkit, host process, external API, Prometheus
server, package manager, shell-mediated service manager, generated toolkit,
human handoff, or remote service. Providers supply implementations or execution
opportunities. A provider can support multiple capabilities, and a capability can
have multiple possible providers.

Provider existence does not imply adoption, trust, current availability, policy
permission, or use. Provider adoption is a separate evidence-backed selection
authorization concern.

### Tool

Tool answers:

```text
What callable operation interface is registered or invokable?
```

A tool is a concrete operation surface with input/output contracts, validation,
registration status, policy evaluation, and implementation references or handler
binding. Tools can expose capabilities, but the tool is not the capability
itself. A `query_prometheus` tool may expose the `query Prometheus` capability;
the capability remains the semantic possibility, while the tool is the callable
interface.

### Adapter

Adapter answers:

```text
How does Seed's operation contract map to provider-specific behavior?
```

An adapter translates names, arguments, authentication context, output shapes,
errors, and provenance between Seed and a provider. It is a boundary object. It
should not own advisory recommendation, decision authority, adoption authority,
or mutation approval.

### Execution Path

Execution path answers:

```text
Which selected route will attempt this command?
```

An execution path combines a selected capability, provider, tool or handoff,
adapter, validation, policy gate, approval state, and runtime/executor dispatch
mechanism. It is more concrete than capability and less final than execution
result.

A capability can be supported by zero, one, or many execution paths. A command
should identify or resolve to one bounded execution path before work is
attempted.

## 3. Recommendation, Decision, And Capability

Recommendations, decisions, and capabilities are related but not dependent in a
single direction.

### Does A Recommendation Require A Capability?

A recommendation to perform work should eventually be checked against capability
support before it becomes a command. However, a recommendation can exist before a
capability is available.

Example:

```text
Assessment: storage pressure is high.
Recommendation: investigate storage.
Capability status: no supported storage-inspection path in this scope.
Outcome: surface capability gap or handoff recommendation, not a command.
```

The recommendation is still meaningful as advice. It simply cannot be realized
by Seed without a supported path, bridge, provider, or handoff.

### Can A Recommendation Exist Without A Capability?

Yes. Recommendations can express desired outcomes or investigation directions
that Seed cannot currently perform. Such recommendations should be labeled as
unsupported, requiring handoff, requiring acquisition, or blocked by missing
visibility/evidence/bridge.

### Can A Capability Exist Without A Recommendation?

Yes. Seed may know it can inspect the filesystem, query Prometheus, read
inventory, or restart a service without currently recommending any of those
operations. Capability availability is inventory/possibility state; it is not
advice.

### What Does A Decision Add?

A decision selects among recommendations, rejects them, defers them, escalates
them, or authorizes the next boundary crossing. A decision may approve an
investigation without yet selecting the specific execution path. A later command
must still be bounded by capability support, provider selection, policy, and
approval requirements.

## 4. What Is A Command?

A command is an authorized, bounded request for work through a selected or
resolvable capability path.

A command answers:

```text
What should be attempted now, with what arguments, scope, target, constraints,
and authority?
```

A command is not merely a recommendation restated in imperative form. It should
include or reference:

- the decision that selected the work;
- the capability required;
- the target/scope;
- the selected provider/tool/adapter path or the resolution rule for selecting
  it;
- the arguments or operation contract;
- policy and approval status;
- expected effect class, especially read-only versus mutation;
- provenance explaining why this command exists.

### Who Creates Commands?

Architecturally, commands may be created by an authorized boundary after a
decision:

- a human operator directly instructing Seed within supported scope;
- a policy-authorized service for explicitly pre-approved low-risk work;
- a runtime or orchestration component translating an accepted decision into a
  bounded execution request;
- a pending-action resume path after approval.

A model recommendation alone should not create a command. A projection alone
should not create a command. A capability catalog entry alone should not create a
command.

### What Support Is Required?

A command requires more than capability naming:

```text
decision support
capability support
provider/tool/adapter support
visibility and evidence sufficiency
policy preflight
approval or confirmation when required
traceable target and scope
```

If any of these are missing, the result should be refusal, deferral, handoff, gap
recording, or a request for more authority/evidence, not silent execution.

### What Authority Is Required?

Command authority is execution-request authority. It must be at least as strong
as the risk of the requested work. Read-only commands may be authorized by
operator request or explicit low-risk policy. Mutating commands require stronger
operator, policy, approval, or pending-action authority.

## 5. What Is Execution?

Execution is the attempted performance of a command through a concrete execution
path.

Execution answers:

```text
What work was attempted, by which provider/tool/adapter, with which inputs,
under which authority, and with what result?
```

Examples:

```text
query provider
run inventory
inspect filesystem
query Prometheus
collect observations
restart service
install package
```

Execution differs from nearby concepts:

| Concept | Difference from execution |
| --- | --- |
| Capability | Capability says work may be possible; execution attempts the work. |
| Command | Command requests work; execution performs the request. |
| Action | Action is mutation or attempted mutation; execution may be read-only. |
| Provider | Provider supplies a route; execution is the use of that route. |
| Tool | Tool is callable interface; execution is a call attempt and result. |
| Adapter | Adapter maps contracts; execution uses the mapped contract. |

Execution may append audit events, collect evidence, or produce observations.
Those durable records are not the same as the external work being performed;
they are provenance and state-recording consequences of execution.

## 6. What Is An Action?

An action is a runtime mutation of the external world or durable operational
state, including attempted mutation when the attempt itself has environmental or
audit significance.

Examples:

```text
package installed
service restarted
file written
approval recorded
pending action completed
provider preference adopted
```

An action is not every execution. The following are execution without action in
the strict mutation sense, assuming they only read/observe and record normal
audit evidence:

```text
read inventory
query Prometheus
inspect filesystem metadata
collect observations
lookup documentation
perform web search
```

Those executions may create Seed events or evidence records. That durable
recording is part of auditability. It should not cause every read-only execution
to be treated as an environmental action, or Seed would lose the important
read-versus-mutate boundary.

### Is Action The Result Of Execution?

Usually, yes: an environmental action is produced by mutating execution.
However, Seed also has durable-state actions such as approval recording,
pending-action completion, or adoption decision append. These are actions in the
state-machine sense even if no external host changed.

### Can Execution Occur Without Action?

Yes. Read-only execution is essential. Querying Prometheus, running inventory,
or collecting observations performs work but should not be described as a
mutation of reality beyond provenance capture.

## 7. Authority Transitions

Authority should increase as mutation risk increases.

```text
Assessment authority
  < Recommendation/advisory authority
  < Decision authority
  < Command authority
  < Execution authority
  < Mutation/action authority
```

### Who May Authorize Each Boundary?

| Boundary | Possible authority | Notes |
| --- | --- | --- |
| Recommendation | Advisory policy, ranking service, model output with support, documented operator intent | Recommendation is not approval. |
| Decision | Human operator, explicit policy gate, governance rule, recorded decision service | Decision selects or rejects; it does not execute. |
| Capability selection | Deterministic support resolution, capability inventory, provider selection policy, adoption state | Selection must remain explainable and scoped. |
| Command | Operator instruction, policy-authorized low-risk decision, approved pending action, orchestration translating accepted decision | Command must be traceable to decision and support. |
| Read-only execution | Command authority plus capability support, validation, and policy allow | Lower risk, but still requires scope and provenance. |
| Mutating execution/action | Strong operator approval, explicit policy authorization, pending-action approval, or equivalent authority | Strongest audit and explanation requirements. |

### What Changes As Mutation Risk Increases?

As risk increases, Seed should require stronger forms of:

- identity of the principal or authority source;
- scope and target specificity;
- evidence sufficiency;
- capability verification;
- provider adoption/trust;
- policy preflight;
- confirmation or approval;
- causation and correlation tracking;
- failure recording and rollback/handoff clarity where relevant.

Capability availability does not lower the required authority. A verified
`restart service` capability still needs mutation authority before a restart
command can be executed.

## 8. Explainability Requirements

Explainability should survive capability selection and remain available through
command, execution, and action.

### Capability Selection Provenance

Seed should be able to answer:

```text
Why was this capability selected?
```

Required provenance includes:

- assessment and recommendation context;
- decision reference;
- capability name and support status;
- known alternatives and why they were not selected, when relevant;
- provider/tool/adapter candidates considered;
- verification state, freshness, and scope;
- risk class and policy implications.

### Command Issuance Provenance

Seed should be able to answer:

```text
Why was this command issued?
```

Required provenance includes:

- decision id or decision record;
- accepted recommendation or operator instruction;
- command arguments and target scope;
- selected capability path;
- authority source;
- policy outcome;
- approval or pending-action state where applicable.

### Execution Provenance

Seed should be able to answer:

```text
Why was this execution path used, and what happened?
```

Required provenance includes:

- command reference;
- provider/tool/adapter identity;
- implementation or handler reference where applicable;
- input validation outcome;
- policy evaluation outcome;
- start/completion/failure events;
- output validation outcome;
- observations or evidence produced;
- causation and correlation ids.

### Action Provenance

Seed should be able to answer:

```text
Why was this action taken?
```

Required provenance includes all execution provenance plus:

- mutation authority;
- confirmation or approval record;
- expected mutation;
- observed or reported effect;
- failure/partial-effect semantics;
- any operator-visible risk acceptance.

The explanation chain should not stop at "the capability existed" or "the tool
was available." Those are support facts, not reasons for action.

## 9. What Should Not Be Collapsed Together?

Seed should not collapse these examples:

| Statement | Concept | Why distinct |
| --- | --- | --- |
| `can inspect filesystem` | Capability | Possibility/support only; no request. |
| `inspect filesystem` | Command | A bounded request; requires authority and scope. |
| `filesystem inventory collected` | Execution result/observation | Work occurred and produced information; not necessarily mutation. |
| `package installed` | Action | External state changed. |
| `Prometheus provider configured` | Provider/support | A supplier exists; not a recommendation or command. |
| `investigate storage` | Recommendation | Advice; may lack support or approval. |
| `investigation approved` | Decision | Selection/approval; still needs executable command path. |

Collapsing these concepts causes predictable architectural failures:

- recommendations become hidden approvals;
- capabilities become hidden permissions;
- providers become hidden trust/adoption decisions;
- commands become indistinguishable from execution results;
- read-only execution is treated like mutation or mutation is treated like
  harmless observation;
- explainability loses causation across decision, command, execution, and
  action.

## 10. What Is Capability Authority?

Capability authority is the authority to describe, verify, select, or expose
possible work. It is not automatically execution authority.

Capability records may communicate a combination of:

| Capability record communicates | Meaning | Boundary |
| --- | --- | --- |
| Available possibilities | Seed recognizes a kind of work. | Does not imply implementation. |
| Available implementations | A provider/tool/adapter path may perform the work. | Does not imply trust or approval. |
| Verification state | Evidence supports availability in a scope. | Does not imply authorization. |
| Supported execution paths | Concrete routes may exist. | Does not imply command issuance. |
| Risk/scope metadata | Work has expected blast radius and constraints. | Does not replace policy. |
| Provider recommendations | Candidate suppliers may satisfy a gap. | Does not imply adoption. |

The architectural rule is:

```text
Capability availability does not imply authorization.
Capability existence does not imply execution.
Capability verification does not imply adoption.
Capability selection does not imply action.
```

## Approved Intent To Real-World Execution

Seed should conceptually move from approved intent to real-world execution as
follows:

```text
1. Projection communicates evidence-backed state.
2. Assessment interprets the state as condition, risk, drift, or sufficiency.
3. Recommendation suggests a possible response.
4. Decision accepts, rejects, defers, escalates, or selects a response.
5. Capability selection identifies whether Seed has a supported path for the
   selected response.
6. Provider/tool/adapter selection resolves a concrete execution path.
7. Command requests bounded work with target, scope, arguments, and authority.
8. Policy and approval gates validate whether execution may proceed.
9. Execution performs the command through the selected path.
10. Result recording preserves output, failure, observations, evidence, and
    provenance.
11. If execution mutates reality, the resulting action is recorded with mutation
    authority and effect provenance.
```

In the endpoint example:

```text
Projection:     endpoint unreachable
Assessment:     endpoint unavailable
Recommendation: investigate connectivity
Decision:       investigation approved
Capability:     query Prometheus / inspect local network / inspect service logs
Provider:       Prometheus server / local host toolkit / operator handoff
Tool/adapter:   concrete query or inspection operation
Command:        query target health metrics for endpoint X in scope Y
Execution:      Prometheus query performed
Action:         none, if read-only; service restart only if later authorized
```

The investigation approval does not authorize every possible investigative or
remediation act. It authorizes movement to bounded commands only where support,
scope, policy, and approval requirements are satisfied.

## Architectural Invariants

This reconciliation supports the following invariants:

```text
Assessments interpret.
Recommendations suggest.
Decisions select.
Capabilities enable.
Providers supply.
Tools expose.
Adapters translate.
Commands request.
Execution performs.
Actions mutate.
```

Additional invariants:

- Capability is possibility; execution is realization.
- Capabilities are not commands.
- Capabilities are not actions.
- Capabilities describe what may be done, not what must or may now be executed.
- Commands request what should be done within a scope.
- Execution performs work through a selected path.
- Actions mutate reality or durable operational state.
- Capability availability does not imply authorization.
- Capability existence does not imply execution.
- Provider existence does not imply adoption.
- Verification does not imply trust, preference, or approval.
- Recommendation does not imply decision.
- Decision does not imply command unless the decision explicitly authorizes a
  bounded request.
- Every command should be traceable to a decision or direct operator instruction
  with decision-equivalent authority.
- Every execution should be traceable to a command.
- Every action should be traceable to mutation authority.
- Authority should increase as mutation risk increases.
- Explainability should survive capability selection.

## Non-Goals

This reconciliation does not propose or require:

- new runtime semantics;
- new schemas;
- new command objects;
- new capability records;
- new provider adoption machinery;
- new execution routing;
- new approval flows;
- new tests;
- changes to `ToolExecutor`, `RuntimeLoop`, capability catalog, provider
  selection, policy, pending actions, or adapters;
- treating documentation conclusions as executable requirements.

## Implementation Implications

The findings imply constraints for future work, but they do not recommend an
implementation change in this document.

Future designs that touch capabilities, commands, providers, execution, or
actions should preserve these boundaries:

- a capability model should avoid representing permission as mere availability;
- provider recommendation should remain distinct from provider adoption;
- command issuance should require decision/authority provenance;
- execution paths should preserve validation, policy, provider/tool/adapter, and
  result provenance;
- mutation-producing execution should carry stronger authority and explanation
  than read-only execution;
- read-only execution should not be mislabeled as action merely because it
  records audit evidence;
- actions should not be justified solely by capability existence.

## Conclusion

Capability is the missing enablement layer between selected intent and concrete
work. It answers whether Seed has a supported, scoped, explainable possibility
for doing something. It does not answer whether Seed should do it, whether a
provider is trusted, whether a command has been issued, whether execution has
occurred, or whether reality has changed.

The reconciled boundary is:

```text
Recommendation proposes intent.
Decision approves or selects intent.
Capability determines possible support.
Command requests bounded work.
Execution realizes the request.
Action is the mutation, if any.
```

Keeping these concepts separate preserves authority, explainability, and safety
as Seed moves from knowledge to real-world effects.
