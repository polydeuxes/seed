---
scope: capability maturity observability reconciliation
status: investigation-only
---

# Capability Maturity Observability Reconciliation

## Boundary

This reconciliation asks only whether Seed currently has implementation-backed
knowledge of the maturity stage of its own capabilities while answering the
active constrained-observation mission:

```text
What can Seed learn without root?
What can Seed learn without Docker?
What can Seed learn without network probing?
What should Seed do when additional observation requires operator authorization?
```

It does not propose a maturity framework, scoring system, implementation roadmap,
planner, generic capability model, or knowledge graph redesign. Repository
authority wins.

## Central answer

Seed currently exposes several implementation-backed signals that humans can use
to infer capability maturity, but Seed does **not** currently know a normalized
maturity stage for its own capabilities.

The strongest supported statement is:

```text
Subsystem maturity is an emergent repository property today.
Humans infer it from multiple repository views.
It is not yet a first-class implementation-backed capability fact.
```

This is not a new architectural concept. The implemented/partial/placeholder
language emerged from existing subsystem seams: observation collectors,
ownership diagnostics, capability-need aggregation, privilege guidance, and
predicate vocabulary. The missing responsibility is narrow: the existing
capability/privilege boundary can say that a capability is needed and what
authority guidance is registered, but no existing subsystem records whether the
capability is implemented, partially implemented, placeholder-only, or unknown.

## Files inspected

Required implementation files:

- `seed_runtime/capability_needs.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_sources.py`
- `predicate_catalog/core.json`

Relevant reconciliations reviewed:

- `docs/filesystem_ownership_constrained_authority_reconciliation.md`
- `docs/privilege_discovery_storage_capability_guidance_reconciliation.md`
- `docs/service_ownership_authority_reuse_findings.md`
- `docs/inquiry_shapes_emerged_reconciliation.md`

App surfaces inspected:

- `python scripts/seed_local.py --capability-needs --json`
- `python scripts/seed_local.py --privilege-discovery --json`

## 1. Does implementation already distinguish implemented, partial, placeholder, and unknown capabilities?

Partially, but not as a single implementation-backed maturity distinction.

### Implemented capability signals

Implementation-backed evidence exists when a capability can be traced to an
actual observation source or evaluator. For example, `LocalHostObservationSource`
collects local facts through read-only local paths, emits metadata that denies
privilege escalation and network probing, and includes concrete mount, storage,
listener, user, package, and systemd collection calls. This is implemented
behavior, not prose-only vocabulary.

`ownership_discrepancies` also implements concrete diagnostic behavior. It has
storage and service subject discovery, conflict classes, discrepancy rows, and
capability-need emission for unresolved conflicts.

### Partial capability signals

Partiality is visible when one subsystem implements part of a capability while
another required subsystem remains absent or only generic. The clearest example
is storage export visibility. `ownership_discrepancies` consumes storage/export
vocabulary and emits storage capability needs, and `capability_needs` aggregates
those needs. However, `privilege_discovery` only has specific registered guidance
for `nfs_export_inventory`; several related storage capabilities fall through to
unknown guidance.

This supports a human conclusion of partial implementation, but there is no
runtime field named `implementation_status`, `maturity`, or equivalent.

### Placeholder capability signals

Placeholder-like signals exist when a capability name or predicate appears as
vocabulary consumed or emitted by diagnostics, but no collector or guidance exists
for it. Examples from the reviewed storage reconciliation include
`smb_share_inventory` and `remote_storage_export_inventory`: they are emitted as
capability needs for unresolved remote export attribution, but repository review
found no implementation that collects those observations.

Again, this is a human-derived classification from multiple files. The code does
not label these as placeholders.

### Unknown capability signals

Unknown is implementation-backed in one narrow place: `privilege_discovery`
returns `access_level = "unknown"` for capability names without registered
privilege guidance and instructs operators to inspect implementation evidence
before requesting additional privileges.

That unknown value means unknown **privilege guidance**, not unknown
implementation maturity. It is the closest current machine-readable fallback,
but it does not distinguish partially implemented from placeholder-only.

## 2. Are these distinctions implementation-backed or human interpretation?

They are mixed.

| Distinction | Current status | Evidence |
| --- | --- | --- |
| Implemented | Implementation-backed when a collector/evaluator emits observations or diagnostics. | Local host observation source and ownership discrepancy diagnostics contain executable collection/diagnostic code. |
| Partially implemented | Human interpretation from cross-subsystem evidence. | Some capability needs are emitted/aggregated while guidance or collectors are absent or incomplete. |
| Placeholder capability | Human interpretation from vocabulary without an implementation path. | Predicate/capability names can exist in diagnostics or catalog without a concrete source/guidance implementation. |
| Unknown capability | Implementation-backed only for privilege guidance fallback. | `_guidance_for()` returns `unknown` for unregistered capability names. |

The repository therefore supports maturity inference, but the inference is not
owned by a runtime maturity subsystem.

## 3. When Seed cannot answer a bounded inquiry, can implementation identify which subsystem, capability, and authority is limiting the answer?

Yes, but only for the boundaries currently wired into diagnostics and authority
slices.

### Capability

`ownership_discrepancies` maps unresolved conflict classes to
`candidate_capability` names and `needed_evidence` records. `capability_needs`
then groups those records by capability, subject, diagnostic, needed evidence,
and diagnostic run. This is implementation-backed capability pressure.

### Authority

`privilege_discovery` maps registered capability names to access guidance such as
`partial_non_root`, `docker_group_or_root`, `available`, and `root`. For
unregistered capabilities, it returns `unknown`. This is implementation-backed
authority guidance where registered and explicit uncertainty where not
registered.

### Subsystem

Subsystem identification is weaker. It can be inferred from the diagnostic name
and capability name: for example, `ownership_discrepancies` is the subsystem that
emits ownership pressure, `capability_needs` aggregates that pressure, and
`privilege_discovery` supplies authority guidance. But there is no normalized
field that says `limiting_subsystem = observation_sources` or
`limiting_subsystem = privilege_discovery`.

Therefore, Seed can identify limiting capability and registered authority better
than it can identify limiting subsystem.

## 4. Does Seed expose enough evidence to reason about its own observational maturity?

Yes, enough evidence is exposed for humans to reason about it.

No, Seed does not yet expose enough implementation-backed structure for Seed
itself to assert the stage of implementation for each capability.

The current evidence is distributed:

- observation sources prove what can be collected locally and read-only;
- ownership diagnostics prove which evidence gaps block an ownership answer;
- capability needs aggregate unresolved diagnostic pressure;
- privilege discovery proves which authority guidance is registered;
- the predicate catalog proves durable vocabulary and mappings;
- reconciliation documents synthesize maturity conclusions across those views.

That distribution is sufficient for investigation prose. It is not sufficient for
an implementation-backed statement that a capability is `implemented`,
`partially_implemented`, `placeholder`, or `unknown`.

## 5. Is this statement implementation-backed?

```text
Seed can know
not only what it knows,

but also

what stage of implementation
its own capabilities occupy.
```

Rejected.

Supported replacement:

```text
Seed can expose what it observed, which diagnostic evidence is missing, which
capabilities would help resolve the gap, and what authority guidance is
registered for some of those capabilities. Humans currently synthesize capability
implementation stage from those repository views.
```

The contradiction is strongest in `privilege_discovery`: unknown guidance is an
implemented fallback, but it only means no guidance registration exists. It does
not prove whether the capability implementation is absent, placeholder-only,
partially implemented, or merely missing a guidance mapping.

## 6. Narrowest missing implementation responsibility

The narrowest missing responsibility is not a framework. It is a capability
implementation-evidence registration boundary adjacent to the existing
capability/privilege seam.

The smallest natural owner is the existing capability-needs / privilege-discovery
boundary:

```text
record, for capability names already emitted by diagnostics, whether repository
implementation evidence exists for the observation capability before converting
that need into operator-facing authority guidance.
```

That boundary is narrow because:

- `ownership_discrepancies` already emits capability names;
- `capability_needs` already aggregates capability names;
- `privilege_discovery` already registers per-capability guidance and has an
  unknown fallback;
- no new planner, maturity framework, or generic capability model is required to
  expose the missing implementation-evidence responsibility.

## Implementation-backed maturity signals

- Concrete observation collection exists in `LocalHostObservationSource`, with
  explicit read-only, local-only, no-subprocess, no-privilege-escalation, and
  no-network-probe metadata.
- Ownership discrepancy diagnostics produce concrete conflict rows and
  diagnostic capability need records.
- Capability needs are aggregated from current projection rows and recorded
  `diagnostic_run:*` facts.
- Privilege discovery emits read-only audit metadata with `mutates_cluster=false`
  and `writes_event_ledger=false`.
- Registered privilege guidance distinguishes authority boundaries for some
  capabilities.
- The predicate catalog records canonical vocabulary, value types, allowed
  values, cardinality, and source mappings.

## Human-derived maturity signals

- `implemented` is inferred by tracing a capability name to executable collector
  or evaluator behavior.
- `partially implemented` is inferred when diagnostic vocabulary and aggregation
  exist but collector/guidance coverage is incomplete.
- `placeholder` is inferred when vocabulary is emitted or consumed without a
  concrete collector or guidance implementation.
- `unknown capability maturity` is inferred when a capability falls through
  privilege guidance and no implementation evidence is found elsewhere.

## Existing subsystem responsibilities

| Subsystem | Existing responsibility | Maturity relevance |
| --- | --- | --- |
| `observation_sources` | Collect local/repository/system observations and attach boundary metadata. | Proves implemented observation capability where concrete collection exists. |
| `ownership_discrepancies` | Diagnose ownership conflicts and emit capability needs for missing evidence. | Proves bounded inquiry pressure and needed evidence. |
| `capability_needs` | Aggregate diagnostic capability needs from current and recorded diagnostics. | Proves capability demand, not implementation stage. |
| `privilege_discovery` | Map needed capabilities to operator-facing authority guidance. | Proves authority guidance status, not implementation stage. |
| `predicate_catalog` | Define predicate vocabulary and mappings. | Proves vocabulary, not collector existence. |

## Strongest supporting evidence

1. Current app output shows no current capability pressure in this repository
   state: `--capability-needs --json` returned `[]`.
2. Current app output shows privilege discovery is read-only and currently has no
   capabilities to report: `--privilege-discovery --json` returned boundary
   metadata with empty `capabilities`, `mutates_cluster=false`, and
   `writes_event_ledger=false`.
3. `ownership_discrepancies` contains the implementation-backed mapping from
   conflict classes to needed evidence, candidate capabilities, and privilege
   levels.
4. `capability_needs` turns those records into grouped capability pressure.
5. `privilege_discovery` has specific guidance for a limited set of capabilities
   and an explicit `unknown` fallback for the rest.

## Strongest contradictory evidence

1. No inspected implementation file contains a maturity-stage field for
   capabilities.
2. The predicate catalog contains vocabulary but no proof that a collector or
   diagnostic implements every predicate or capability implied by that
   vocabulary.
3. Unknown privilege guidance is not the same as unknown implementation maturity.
4. Recent reconciliations contain the strongest implemented/partial/placeholder
   distinctions, but those distinctions are written as investigation prose rather
   than emitted by an app surface.

## Acceptance answer

Seed does not currently know the maturity of its own capabilities as an
implementation-backed fact. Humans infer that maturity from multiple repository
views: observation code, diagnostic code, capability need aggregation, privilege
guidance, predicate vocabulary, tests, app output, and reconciliation prose.

If maturity is not yet implementation-backed, the smallest existing subsystem
boundary that would naturally own it is the capability-needs / privilege-discovery
boundary, because that is where diagnostic capability names become
operator-facing authorization guidance.

Subsystem maturity is therefore an emergent repository property, not a new
architectural concept.

## Files changed

- `docs/capability_maturity_observability_reconciliation.md`

## LOC changed

- One documentation file added, 344 lines.

## Tests and checks run

- `python scripts/seed_local.py --capability-needs --json`
- `python scripts/seed_local.py --privilege-discovery --json`
- `pytest -q tests/test_privilege_discovery.py tests/test_ownership_discrepancies.py`

## Recommended bounded implementation slice

If implementation is requested later, keep the slice bounded to the existing
capability-needs / privilege-discovery seam:

```text
For capability names already emitted by diagnostics, expose whether registered
implementation evidence exists before presenting authority guidance.
```

This is the narrow missing responsibility identified by the investigation, not a
maturity framework or scoring system.
