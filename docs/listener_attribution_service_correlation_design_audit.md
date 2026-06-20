# Listener Attribution and Service Correlation Design Audit

## Status

Exploratory design audit.

This document captures an operational boundary discovered while adding local listener and listener process attribution observations. It does not implement ownership changes, create ontology, write facts, or change diagnostic behavior.

Repository authority wins over this audit.

## Problem

Seed now observes local listeners and, where available without root, listener process attribution.

Observed current facts for `node115` include examples such as:

```text
listening_process_name = jellyfin
  address=0.0.0.0
  port=8096
  protocol=tcp
  listener_attribution_status=process_observed

listening_process_name = filebrowser
  address=::
  port=8980
  protocol=tcp
  listener_attribution_status=process_observed
```

This proves that listener process attribution can exist in the fact surface.

However, ownership discrepancies still report many service rows as:

```text
candidate_owner=node115
conflict=owner_not_observed
reason=Local listener evidence confirms a socket is present, but process/container owner attribution is unavailable.
```

This should not be treated immediately as an implementation bug.

It may be a modeling boundary:

```text
process attribution exists
but service subject correlation is missing
```

## Current distinction

There are at least three different things currently being conflated by operator intuition:

```text
listener socket visibility
listener process attribution
service subject ownership
```

These are not equivalent.

A listener row can show:

```text
port 8096 is listening
process name is jellyfin
process id is 1093163
```

But ownership diagnostics may still be evaluating service subjects such as:

```text
node116
node200
270424597b79
mini
```

Those service subjects may come from Prometheus targets, endpoint identities, host aliases, or other observed service-like surfaces.

The missing operation may not be:

```text
observe process
```

It may be:

```text
correlate this service subject to this listener/process evidence
```

## Why this matters

Without this distinction, Seed can appear to contradict itself:

```text
current facts:
  process observed

ownership:
  owner not observed
```

But both can be true if the process evidence is not correlated to the service subject being evaluated.

This is a boundary mismatch, not necessarily a parser failure or ownership bug.

## Candidate new diagnostic language

Ownership discrepancies may need to distinguish:

```text
owner_not_observed
```

from a more precise state such as:

```text
service_identity_not_correlated
```

or:

```text
process_observed_but_not_correlated
```

Exact names are intentionally undecided.

The goal is better explanation, not stronger inference.

## Candidate service correlation evidence

Future ownership logic may need to correlate service subjects to listener/process evidence using one or more of:

```text
port
protocol
address
endpoint target
Prometheus instance / target labels
process name
known service name
systemd unit
container name
host alias
node identity
```

Each correlation path has different confidence and risk.

Example:

```text
Prometheus target node116:9100
local listener 0.0.0.0:9100 process=node_exporter
```

may be stronger than:

```text
subject node116
some unrelated listener exists on node115
```

## Boundary

Observed listener process attribution is allowed.

Candidate service correlation is allowed.

Durable ownership facts are not allowed without a separate explicit boundary change.

Do not collapse:

```text
process observed
```

into:

```text
service owner proven
```

without correlation evidence and explicit confidence.

## Capability needs implication

Capability needs currently report:

```text
listener_process_inventory
container_port_mapping
container_inventory
```

If listener process attribution is present but service rows still cannot resolve, the capability need may need to change from:

```text
listener_process_inventory
```

to something like:

```text
service_endpoint_correlation
```

or:

```text
service_identity_correlation
```

This would let pressure audit distinguish:

```text
we cannot see the process
```

from:

```text
we can see the process, but cannot correlate it to the service subject
```

## Storage side observation

A related storage issue appeared:

```text
node115 | storage | user@192.168.254.100 | mount_source_conflict
```

This suggests another possible boundary:

```text
remote mount account/host string
```

is not the same as:

```text
storage owner identity
```

Remote mount evidence may need its own parsing and confidence model before it becomes ownership support.

This audit focuses on listener/service correlation, but the same principle applies:

```text
observed attribution string
```

is not automatically:

```text
owner identity
```

## Suggested next implementation direction

A narrow future implementation should not simply increase ownership confidence when process facts exist.

Instead it should:

1. Detect whether matching listener process evidence exists for the service row.
2. If process evidence exists but cannot be correlated to the service subject, report that explicitly.
3. If no process evidence exists, keep `owner_not_observed` or current attribution gap behavior.
4. Emit capability needs that reflect the actual gap:
   - process inventory missing
   - container attribution missing
   - service identity correlation missing
5. Preserve candidate-only ownership semantics.

## Non-goals

Do not use this audit to:

```text
create ownership facts
promote process names into owners
infer container ownership
require root
require Docker socket access
redefine service identity
rewrite ownership diagnostics broadly
```

## Acceptance shape for future work

A future implementation should allow ownership output to distinguish:

```text
listener process not visible
```

from:

```text
listener process visible but not correlated to service subject
```

An operator should no longer have to manually reconcile:

```text
current facts show process_observed
ownership says owner_not_observed
```

The diagnostic should explain the boundary itself.

## Current conclusion

Listener process attribution has improved observation visibility, but service ownership still requires a correlation layer.

The active pressure is shifting from:

```text
can Seed see listener processes?
```

to:

```text
can Seed correlate observed listener/process evidence to service subjects safely?
```

That is a different problem and should be treated as such.