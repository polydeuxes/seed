# Cross-Seed Provenance And Federation Reconciliation

## Purpose

This document performs a documentation-only reconciliation of cross-Seed
knowledge sharing, provenance preservation, foreign evidence, shared events,
mirrored state, imported claims, federation boundaries, and authority.

It is an architectural boundary audit.

It does not implement code, modify schemas, modify runtime behavior, modify
observations, modify evidence handling, modify claims, modify events, modify
projections, modify identity models, modify trust models, modify authority
systems, modify synchronization mechanisms, or add tests.

## Central Question

Seed currently reasons about observations, evidence, claims, events,
projections, trust, authority, identity, and provenance. A new architectural
frontier appears when more than one Seed instance exists:

```text
Seed A observes something.
Seed B receives knowledge from Seed A.
```

The central question is not only whether Seed B should believe the knowledge.
The central question is:

```text
What exactly did Seed B receive?
```

Possible answers include:

```text
the same event
an event report
foreign evidence
foreign testimony
an imported claim
a projection export
a mirrored state fragment
a shared-state update
```

Those answers are not interchangeable.

## Central Finding

```text
Seed-to-Seed sharing is evidence transfer, not truth transfer.
```

A receiving Seed should preserve the distinction between:

```text
what happened locally
what another Seed observed
what another Seed claimed
what another Seed projected
what another Seed was authorized to declare
what the local Seed verified independently
```

Cross-Seed import must not collapse provenance, trust, authority, identity, or
verification into a single notion of accepted truth.

## Current Architectural Baseline

Seed's existing architecture already separates knowledge layers:

```text
Observation
    -> Evidence
    -> Fact / Claim
    -> Projection / Read View
```

Existing reconciliation work also distinguishes evidence support, source trust,
source authority, and truth. This document extends that separation across Seed
instance boundaries.

A cross-Seed boundary adds another layer:

```text
Foreign Seed source
    -> transfer path
    -> local import record
    -> local interpretation
    -> optional local promotion
    -> local projection
```

Importing knowledge from another Seed should therefore be treated as a new
local act with preserved foreign provenance, not as if the receiving Seed had
performed the originating observation itself.

## Definitions

### Seed Instance

A Seed instance is a bounded reasoning installation with its own operational
context, append-only history, projection state, import/export boundaries, and
operator governance.

Architecturally, a Seed instance has:

| Dimension | Meaning |
| --- | --- |
| Instance identity | The identity by which other systems can refer to this Seed installation. |
| Authority scope | The domains in which this Seed is permitted to declare, promote, synchronize, or override knowledge. |
| Trust scope | The local assessment of which sources, adapters, operators, paths, and foreign Seeds are reliable for which domains. |
| Provenance scope | The evidence, observations, events, claims, imports, transformations, and projections whose history this instance can explain. |
| Operator context | The human or organizational context that configures, operates, authorizes, and interprets the instance. |

A Seed instance is not merely a database replica or API endpoint. It is a
reasoning boundary.

A Seed instance can be a source for another Seed. It can also be treated as a
foreign authority, but only within explicit scope.

### Local Observation

A local observation is an observation produced inside the receiving Seed's own
observation boundary by a local source path.

Examples:

```text
Seed B's local host adapter observes port 443 listening.
Seed B's local operator states that service nginx should be present.
Seed B's local repository scanner observes a file.
```

A local observation means:

```text
This Seed received this from one of its own source paths.
```

It does not mean the observation is true.

### Foreign Observation

A foreign observation is an observation produced by another Seed instance.

When Seed B receives Seed A's observation, Seed B should not treat it as a
local observation. Seed B possesses local evidence that Seed A reported an
observation.

The safest default interpretation is:

```text
foreign observation
    -> imported report of another Seed's observation
    -> local evidence about foreign testimony
```

A foreign observation may support local reasoning, but its foreign origin must
survive import.

### Local Evidence

Local evidence is preserved support produced or captured inside the local Seed's
own provenance scope.

It answers:

```text
What did this Seed observe, receive, derive, or preserve locally?
```

Local evidence may include imported material, but imported material remains
locally preserved evidence about a foreign source path unless independently
verified or explicitly promoted under local authority.

### Foreign Evidence

Foreign evidence is evidence preserved by another Seed instance.

Foreign evidence can be transferred, but transfer changes the receiving Seed's
relationship to it. Seed B usually receives:

```text
evidence that Seed A had evidence
```

rather than the same evidentiary position Seed A had.

Foreign evidence remains useful when the import preserves enough information to
support audit and reinterpretation:

```text
originating Seed identity
foreign evidence identity
foreign observation identity, when applicable
foreign source identity or source class
foreign event or claim identity, when applicable
payload or digest
observation time
foreign record time
import time
transfer path
integrity metadata, when available
trust context
claimed authority context
known transformations or redactions
```

If the foreign evidence includes raw source payloads, signatures, stable source
identifiers, and verifiable transfer integrity, the receiving Seed may reason
more directly about the evidence. Even then, the receiving Seed should preserve
both support paths:

```text
foreign source produced evidence
Seed A preserved or transmitted it
Seed B imported it
```

### Event

An event is a historical record within a Seed's event boundary. It may describe
an observation, state transition, import, export, tool result, claim creation,
or other architectural occurrence depending on the owning subsystem.

An event identity is scoped unless explicitly designed otherwise. The same
identifier string in two Seeds is not sufficient to prove the same event.

### Shared Event

A shared event is an event whose identity is intentionally recognized by more
than one Seed under a shared identity scheme and sufficient provenance.

Two Seeds may refer to the same real-world occurrence without possessing the
same architectural event.

The distinction is:

| Situation | Interpretation |
| --- | --- |
| Seed A has event `E_A`; Seed B imports A's report | Seed B has an imported event report about `E_A`. |
| Seed A and Seed B independently observe similar content | Similar event content, not necessarily same event. |
| Seed A and Seed B use a shared event namespace, integrity proof, and agreed authority | Candidate shared event identity. |
| Seed B independently verifies the same external occurrence | Corroborated occurrence, still with separate local and foreign support paths unless identity is explicitly unified. |

Shared event identity requires stronger evidence than similar event content.
Identity collapse becomes unsafe when it hides disagreement, erases source
paths, merges incompatible clocks, or makes a foreign report appear local.

### Imported Event Report

An imported event report is Seed B's local record that Seed A reported event
`E_A`.

It is not automatically the same event as `E_A`.

It should preserve:

```text
reporting Seed
reported event identity
reported event payload or digest
reported event time
foreign append or observation time
local import time
transfer path
supporting evidence references
authority asserted by the reporter
local trust assessment, if any
```

### Claim

A claim is a knowledge assertion that can be supported, contradicted, promoted,
projected, questioned, or explained.

Claims are not self-authenticating truth. They depend on support, scope,
authority, and interpretation.

### Imported Claim

An imported claim is a claim received from another Seed.

Example:

```text
Seed A claims host115 has nginx installed.
Seed B imports that claim.
```

Seed B should treat this as:

```text
Seed A testified that host115 has nginx installed.
```

not automatically as:

```text
Seed B locally knows host115 has nginx installed.
```

An imported claim may become:

```text
corroborating evidence for a local claim
foreign testimony displayed in an explanation
a candidate for local promotion under local authority
a disagreement participant
a scoped assertion accepted for a limited federation domain
```

But it should remain distinguishable from a local claim unless explicit local
authority promotes it.

Every imported claim should be able to answer:

```text
Who said this?
From which Seed?
From which source?
With what evidence?
Under what authority?
When was it imported?
```

### Projection Export

A projection export is a communication surface derived from a Seed projection.

It may be a summary, view, report, snapshot, API response, handoff document, or
state surface. It is not automatically evidence, authority, or truth.

Projection export is not evidence export unless provenance and support survive
with enough fidelity for the receiver to audit the support path.

Projection export is also not authority. A projection may report what the
exporting Seed currently believes, selected, or rendered. It does not by itself
establish that the exporting Seed had authority to define the receiving Seed's
truth.

### Mirrored State

Mirrored state is a copied or synchronized representation of another Seed's
state or projection.

Mirroring answers:

```text
What does the mirror currently reflect from the source Seed?
```

It does not answer:

```text
Is the mirrored content true?
Is the mirrored content locally observed?
Is the mirrored content locally authoritative?
Do the two Seeds share one identity?
```

Mirrored state differs from shared truth, shared events, shared claims, shared
projections, and foreign evidence:

| Concept | Boundary |
| --- | --- |
| Mirrored state | Copy of another state surface or selected records. |
| Shared truth | Not established by copying; requires authority and reconciliation. |
| Shared event | Requires shared identity and provenance, not just matching state. |
| Shared claim | Requires explicit claim identity and scope, not just projection equality. |
| Shared projection | Multiple Seeds may expose compatible views without sharing authority. |
| Foreign evidence | Support material, not the current mirrored result itself. |

Mirroring is not identity.

### Shared State

Shared state is state intentionally maintained by multiple Seeds under an
explicit coordination model.

Shared state requires more than replication. It requires:

```text
shared identity rules
explicit authority allocation
conflict handling rules
write ownership rules
provenance preservation
operator or organizational agreement
clock, ordering, or causality assumptions
recovery behavior
explanation behavior
```

Shared state may be valid for narrow domains. For example, multiple Seeds may
share an allowlist, a federation registry, a task board, or a replicated claim
index. That does not imply all facts, events, evidence, or projections are
shared truth.

The strongest invariant is:

```text
Shared state requires explicit authority.
```

### Federation

Federation is an intentional relationship among Seed instances that allows
knowledge, projections, claims, evidence, events, or state surfaces to cross
instance boundaries under explicit rules.

Federation may include any of the following, but none are implied by default:

```text
sharing observations
sharing evidence
sharing claims
sharing projections
sharing selected state
sharing event reports
shared identity namespaces
shared authority for specific domains
shared conflict handling policies
```

Federation does not automatically mean:

```text
shared authority
shared truth
shared identity
shared event identity
universal trust
local verification
operator equivalence
```

Federation is a communication and governance boundary, not a magical collapse
of instance boundaries.

## Cross-Seed Provenance

Cross-Seed provenance is the preserved explanation of how knowledge moved from
one Seed instance to another and what support survived that transfer.

It should include, when available:

| Provenance element | Reason it matters |
| --- | --- |
| Originating Seed identity | Identifies the foreign reasoning boundary. |
| Originating operator identity or context | Separates Seed identity from human or organizational control. |
| Source observation identity | Preserves the original observation path. |
| Source evidence identity | Allows support path audit. |
| Source event identity | Distinguishes event report from local event. |
| Source claim identity | Allows imported claim tracking and contradiction review. |
| Evidence chain | Shows what supported the foreign assertion. |
| Transfer path | Identifies the mechanism and intermediaries by which knowledge arrived. |
| Export time | Captures when the foreign Seed emitted the knowledge. |
| Import time | Captures when the local Seed received it. |
| Transformation history | Records summarization, redaction, filtering, normalization, or projection. |
| Trust context | Captures local assessment of reliability, where modeled. |
| Authority context | Captures claimed and locally accepted authority scope. |
| Integrity context | Captures signatures, digests, transport guarantees, or tamper evidence. |

Provenance is not trust. Trust is an assessment of a source or path.
Provenance is the record needed to make, explain, revise, or dispute such an
assessment.

Import is not verification. Import records receipt and preservation. Verification
requires a separate local basis.

## Reasoning Rules By Boundary

### Local Observation vs Foreign Observation

Seed B should not rewrite Seed A's observation as Seed B's observation.

Recommended conceptual treatment:

```text
Seed A observation
    -> Seed B import record
    -> foreign testimony evidence in Seed B
```

Seed B may use that testimony to support local conclusions, but explanations
should remain able to show that the path passed through Seed A.

### Local Evidence vs Foreign Evidence

Evidence can cross boundaries as material, metadata, payload, digest, or report.
However, the receiving Seed's evidentiary relationship changes unless the
original source is directly verifiable by the receiver.

The local question becomes:

```text
What does this imported material prove to Seed B?
```

Often it proves:

```text
Seed A reported support for claim C.
```

It may also support:

```text
Claim C is plausible.
Claim C is corroborated by a foreign source.
Claim C deserves local investigation.
Claim C can be accepted under scoped foreign authority.
```

It should not silently prove:

```text
Seed B observed C directly.
```

### Imported Claim vs Local Claim

An imported claim remains foreign testimony until local authority promotes,
accepts, or derives a local claim from it.

Possible statuses include:

```text
preserved foreign claim
candidate local claim
corroborating support
accepted scoped federation claim
rejected foreign claim
contradicting foreign claim
superseded foreign claim
```

Promotion should preserve the foreign path rather than replacing it.

### Projection Export vs Evidence Export

A projection is a read surface over selected state. It may omit caveats,
contradictions, stale support, alternative claims, raw evidence, or authority
context.

Therefore:

```text
projection export != evidence export
projection export != claim authority
projection export != local observation
```

Projection export can be useful as an alert, summary, handoff, or discovery
surface. It should not be treated as evidence export unless the support and
provenance required for audit are included or reachable.

### Mirrored State vs Shared Truth

Mirrored state may help Seed B display or query Seed A's current projection, but
it does not make the mirrored content local truth.

Mirrors should preserve at least:

```text
source Seed
source projection identity
source projection version or time
mirror import time
known filtering or transformation
support availability
authority scope, if any
```

A mirror that lacks provenance should be treated as a weak communication surface,
not as a foundation for strong local claims.

### Shared State vs Federation

Federation is the relationship. Shared state is one possible product of that
relationship.

A federation can exist without shared state:

```text
Seeds exchange signed event reports but keep separate state.
```

Shared state can exist only within an explicit domain:

```text
Seeds jointly maintain a federation membership registry.
```

Shared state should never imply unlimited shared authority.

## Shared Event Identity

An event can be canonical across Seeds only when the architecture deliberately
provides a cross-instance identity basis.

Candidate requirements include:

```text
shared event namespace or globally stable event identifier
originating Seed identity
immutable event payload or digest
identity derivation rules
integrity proof or equivalent audit basis
agreement about whether the event is authored, observed, imported, or shared
conflict policy for duplicate or divergent reports
```

Without those conditions, Seed B should model Seed A's event as an imported
event report.

Unsafe collapse examples:

| Collapse | Why unsafe |
| --- | --- |
| Same timestamp and payload means same event | Independent observers may produce similar records. |
| Same foreign event ID means same local event | IDs may be scoped to the originating Seed. |
| Imported event is appended as local observation | Erases foreign source and transfer path. |
| Projection match means event match | Projection can summarize, filter, or select over many event histories. |
| Shared event means shared authority | Event identity does not define who can interpret or override it. |

## Authority Boundaries

Authority is scoped. A foreign Seed can be an authority only for the domains in
which local governance recognizes it.

Examples:

| Foreign Seed role | Possible authority scope |
| --- | --- |
| Site-local Seed | May be authoritative for hosts it directly manages or observes. |
| Security Seed | May be authoritative for vulnerability attestations but not service ownership. |
| Inventory Seed | May be authoritative for asset registration but not live process state. |
| Operator-operated Seed | May carry operator testimony but not universal truth. |
| Federation registry Seed | May be authoritative for federation membership but not member facts. |

Authority does not remove provenance. If Seed B accepts Seed A as authoritative
for a domain, Seed B should still remember that the accepted declaration came
from Seed A.

Trust also does not create authority. A trusted Seed may be reliable without
being allowed to decide a domain. An authoritative Seed may be allowed to decide
a domain while still requiring audit and provenance.

## Disagreement Handling

When Seeds disagree, disagreement should be preserved before it is resolved.

Examples:

```text
Seed A claims service nginx is running.
Seed B claims service nginx is stopped.

Seed A reports event E.
Seed B reports conflicting event F.
```

The receiving Seed should preserve:

```text
both claims or reports
both source Seeds
both support paths
both observation or report times
both import times
both authority scopes
known transformations
local selection or resolution rationale, if any
```

Contradiction behavior should distinguish:

| Case | Treatment |
| --- | --- |
| Foreign claim contradicts local observation | Preserve both; local projection may prefer local observation while exposing foreign disagreement. |
| Two foreign Seeds disagree | Preserve both; compare authority, trust, freshness, and evidence without erasing either. |
| Foreign authority conflicts with non-authoritative local source | Preserve both; selection may follow scoped authority but explanation should show conflict. |
| Shared-state writes conflict | Apply explicit shared-state conflict policy; preserve losing, superseded, or rejected support. |
| Projection exports disagree | Treat as disagreement between exported views until underlying evidence is available. |

Reconciliation may select, rank, promote, reject, defer, or request more
evidence. It should not rewrite history to make disagreement disappear.

## What Should Not Be Collapsed Together

The following boundaries should remain explicit:

```text
foreign claim != local claim
foreign observation != local observation
shared event != imported event report
projection export != evidence export
mirrored state != shared truth
federation != authority
Seed identity != operator identity
trust != provenance
import != verification
mirroring != identity
claim support != claim truth
shared state != unlimited shared authority
same content != same event
foreign evidence != local observation
local acceptance != foreign authorship erasure
```

## Architectural Invariants

This reconciliation supports the following invariants:

1. Seed-to-Seed sharing is evidence transfer, not truth transfer.
2. A foreign Seed's claim is testimony unless promoted or accepted under local
   authority.
3. Provenance must survive federation.
4. Import is not verification.
5. Mirroring is not identity.
6. Mirrored state is not shared truth.
7. Shared state requires explicit authority.
8. Projection export is not evidence export unless support and provenance
   survive.
9. Federation does not automatically create authority.
10. Cross-Seed reconciliation should preserve local and foreign support paths.
11. Disagreement between Seeds should be preserved before it is resolved.
12. Shared event identity requires stronger evidence than similar event content.
13. Seed identity and operator identity are related but distinct.
14. Trust and authority are related but distinct.
15. Local promotion should add a local decision path without deleting the
    foreign path.

## Implementation Implications

This document does not recommend implementation work as an immediate task.
However, the findings imply constraints for any future implementation:

- Future import mechanisms should preserve originating Seed identity, source
  identity, support chain, transfer path, import time, trust context, and
  authority context where available.
- Future projection exports should declare whether they include provenance and
  whether support is complete, partial, summarized, redacted, or unavailable.
- Future federation designs should define authority scope explicitly rather than
  assuming that connectivity implies authority.
- Future shared-state designs should define identity, write authority, conflict
  handling, ordering, and provenance rules before synchronizing state.
- Future reconciliation views should show local and foreign support paths rather
  than flattening them into a single anonymous support count.
- Future event-sharing designs should distinguish shared event identity from
  imported event reports.

These are architectural guardrails, not runtime requirements introduced by this
document.

## Non-Goals

This reconciliation does not:

- define a network protocol;
- define a federation API;
- define a schema migration;
- define event serialization;
- define cryptographic signing requirements;
- define trust scores;
- define authority policy syntax;
- define projection export formats;
- define conflict-resolution algorithms;
- change observation ingestion;
- change evidence handling;
- change claim promotion;
- change event projection;
- change identity models;
- change runtime behavior;
- add tests.

## Summary

The safest architectural stance is:

```text
A Seed instance is a reasoning boundary.
Crossing that boundary creates imported knowledge with foreign provenance.
Imported knowledge can support local reasoning without becoming local truth.
Federation connects reasoning boundaries; it does not erase them.
```

A receiving Seed should be able to explain not only what it currently believes,
but also whether that belief came from local observation, foreign testimony,
mirrored state, projection export, scoped authority, shared state, or explicit
local verification.
