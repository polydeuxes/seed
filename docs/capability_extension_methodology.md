# Capability Extension Methodology

## Purpose

Seed should grow capabilities without weakening the architectural boundaries that
make its reasoning model inspectable. Capability growth is safest when every
extension starts by naming the gap, reducing the gap to the narrowest fact Seed
needs, and choosing the least-privileged source of truth that can support that
fact.

Capability growth should be constrained because a new capability can otherwise
quietly become a bundle of unrelated powers: observation, inference, execution,
network access, privilege escalation, and state mutation. When those powers are
introduced together, reviewers can no longer tell which part of the system is
learning something, which part is interpreting it, and which part is acting on
it.

Architecture drift often begins when observation, inference, and execution become
mixed. An observation that says more than it directly saw becomes an inference.
An inference that triggers work becomes execution. Execution that is hidden
inside observation makes facts look more authoritative than their evidence
supports. Seed extensions should therefore separate:

- **Observation**: a narrow, direct, read-only statement about what was seen.
- **Evidence**: the support that records where the observation came from.
- **Fact**: the projected knowledge claim Seed can reason over.
- **Inference**: an optional reasoning step over facts, explicitly separate from
  observation.
- **Execution**: an explicitly authorized operation, never implied by observing.

This methodology keeps capability growth reviewable, testable, and aligned with
Seed's Core MVP boundaries.

## Extension Flow

Use this canonical flow for capability extensions:

```text
Capability Gap
↓
Required Question
↓
Narrowest Fact
↓
Least-Privileged Source
↓
Read-Only Observation
↓
Observation
↓
Evidence
↓
Fact
↓
Inference (optional)
↓
User Query
```

### Capability Gap

Name what Seed cannot currently answer or represent. The gap should be stated as
a missing reasoning capability, not as a desired tool, provider, command, or
execution path.

### Required Question

Translate the gap into the smallest question Seed needs answered. Avoid broad
questions such as "is this available?" when the real question is narrower, such
as "is an interface configured?" or "does projected state contain support for
this capability?"

### Narrowest Fact

Define the narrowest fact that can answer the required question. Prefer facts
that describe directly observed configuration, registrations, or projected state.
Do not encode inferred health, availability, reachability, or success into an
observation fact.

### Least-Privileged Source

Choose the least-privileged source of truth that can support the narrowest fact.
Prefer existing projected facts, existing observations, and local read-only data
before considering external providers, operator input, elevated privilege, or
execution.

### Read-Only Observation

If a new observation is required, it should read only the selected source. It
should not mutate state, contact unnecessary systems, perform probes that imply
network activity, request write access, or execute registered operations.

### Observation

Record only what was directly observed. Observation vocabulary should be precise
enough to prevent accidental promotion into broader claims.

### Evidence

Attach evidence that identifies the source and boundary of the observation. The
evidence should make the fact auditable without overstating what the source can
prove.

### Fact

Project observations into facts with explicit predicates and values. Facts should
remain scoped to what the observation and evidence support.

### Inference (optional)

Inference may combine facts to answer broader questions, but it must remain
separate from observation. Inferred conclusions should preserve uncertainty,
staleness, contradictions, and source limitations.

### User Query

User-facing answers should distinguish observed facts from inferred conclusions
and should avoid presenting candidates, recommendations, or configured resources
as verified capabilities unless a verification model supports that claim.

## Observation Rules

Observe narrowly. Infer broadly.

Observation must not claim more than was directly observed. A narrow observation
can support later reasoning, but the observation itself should stay within the
source boundary.

Acceptable observation-style facts include:

- `interface configured`
- `DNS configured`
- `route configured`
- `default_gateway configured`
- `local_observation_status observed`
- `registered operation candidate`
- `provider recommendation`

These must not imply:

- `reachable`
- `available`
- `working`
- `verified capability`
- `operation executed`
- `provider contacted`
- `host accessible from another environment`

Examples:

- Observing a configured network interface does not prove that another host can
  reach it.
- Observing a configured DNS resolver does not prove that DNS queries work.
- Observing a configured route does not prove that packets can traverse the
  route.
- Observing a local status marker does not prove service availability.
- Discovering a registered operation candidate does not prove that the operation
  satisfies a requested capability.

## Privilege Rules

Capability extensions should prefer sources in this order:

1. Existing projected facts
2. Existing observations
3. Local read-only sources
4. External read-only providers
5. Explicit operator input

Only after all of the above fail should elevated privilege even be considered.
If elevated privilege is proposed, the proposal must explain why every lower
privilege source is insufficient and must keep the elevated scope as narrow as
possible.

Read access and write access are different capabilities. Write access includes
the ability to alter, replace, or delete information, so it must not be treated as
a harmless extension of read access.

Write implies delete.

Observation should never request write access. If a workflow needs write access,
that workflow is no longer observation; it is execution or mutation and must be
modeled, authorized, and tested under execution rules instead of observation
rules.

## Source Selection Rules

For every new capability, ask these questions before adding behavior or new
surfaces:

- Can this be answered from existing facts?
- Can this be answered from existing observations?
- Can this be answered from local read-only data?
- Can this be answered without network access?
- Can this be answered without privilege escalation?
- Can this be answered without execution?

A capability extension should stop at the first source that can answer the
narrowest fact. If a broader source is selected, the design should document why
narrower and less-privileged sources are insufficient.

## Non-Inference Rules

Observation vocabulary must preserve the difference between a direct statement
and a derived conclusion.

Use these non-equivalences as guardrails:

```text
default_gateway configured
!= gateway reachable

dns_resolver configured
!= DNS working

local_observation_status observed
!= host available

provider recommendation
!= verified capability

registered operation candidate
!= verified capability
```

Additional non-equivalences:

- `interface configured` != `network reachable`
- `route configured` != `route works`
- `capability requested` != `capability verified`
- `known capability` != `verified capability`
- `operation name begins with verify_` != `verification performed`
- `read-only provider metadata` != `provider executed`

## Capability Extension Checklist

Future contributors should use this checklist before implementing a capability
extension:

- [ ] State the capability gap without naming a preferred tool or execution
      mechanism.
- [ ] Translate the gap into the required question Seed must answer.
- [ ] Define the narrowest fact that answers that question.
- [ ] Confirm whether existing projected facts already answer the question.
- [ ] Confirm whether existing observations already answer the question.
- [ ] Identify the least-privileged source of truth for any missing fact.
- [ ] Prefer local read-only data before external providers.
- [ ] Avoid network access unless the narrowest fact truly requires it.
- [ ] Avoid privilege escalation unless all lower-privilege sources fail.
- [ ] Avoid execution unless the extension is explicitly an execution capability.
- [ ] Keep observation vocabulary narrower than inference vocabulary.
- [ ] Attach evidence that records source, scope, and time boundary.
- [ ] Project observations into facts without adding unsupported conclusions.
- [ ] Keep inference optional and separate from observation.
- [ ] Preserve contradiction and temporal semantics for conflicting or stale
      facts.
- [ ] Do not treat recommendations, candidates, or registrations as verified
      capabilities.
- [ ] Add tests or documentation checks that prevent future overreach.
- [ ] Confirm the extension does not add Runtime behavior unless explicitly
      required and reviewed as runtime work.
- [ ] Confirm the extension does not add ToolExecutor behavior unless explicitly
      required and reviewed as execution work.
- [ ] Confirm the extension does not add prompt generation or hidden execution
      capabilities.

## Relationship To Seed Architecture

This methodology aligns with Seed's architecture by keeping each reasoning layer
within its intended boundary.

### Observation

Observation is the narrow, read-only act of recording what a source directly
shows. Observation should not perform execution, infer availability, or claim
verification. Local observation is especially constrained: it may describe local
configuration, but not remote reachability or service health unless those were
separately and explicitly observed by an appropriate source.

### Evidence

Evidence records why Seed can trust a fact enough to reason about it. Evidence
should identify the source, scope, and temporal boundary of an observation
without expanding the claim. Evidence for "configured" does not become evidence
for "working" unless a separate observation supports that stronger claim.

### Fact

Facts are the durable reasoning vocabulary produced from observations and their
evidence. Facts should be narrow enough to remain true within their evidence
scope and expressive enough for later inference. Fact predicates should avoid
collapsing requested, candidate, recommended, provider-reported, and verified
capabilities into one meaning.

### FactSupport

FactSupport connects facts to their supporting evidence. Capability extensions
should use support links to make claims auditable instead of inventing new
implicit authorities. A fact without appropriate support should not be promoted
into a stronger capability status.

### Contradiction handling

Narrow observations make contradictions explicit and manageable. If two sources
disagree, Seed should preserve the competing facts, evidence, and support rather
than allowing an observation path to resolve the conflict by overclaiming.
Contradiction handling depends on observations remaining scoped and comparable.

### Temporal reasoning

Capability facts can become stale. A fact that was true at one observation time
may not answer a current query. Extensions should preserve observation time,
freshness, expiry, and event boundaries so temporal reasoning can distinguish
current support from historical support.

### Capability verification

Capability verification is a scoped status supported by acceptable evidence; it
is not implied by a request, catalog entry, provider recommendation, registered
operation candidate, or operation name. Extensions should keep capability
resolution read-only and should not introduce implicit verification behavior.

### Architecture invariants

The methodology reinforces Seed's invariants: observation must not imply
execution, observation must not imply availability, capability resolution must
not imply verification, write access must not be required for observation, and
least-privileged observation sources should be preferred. These rules prevent
new capabilities from drifting into Runtime behavior, ToolExecutor behavior,
prompt generation, or unreviewed execution capabilities.
