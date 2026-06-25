---
doc_type: reconciliation
status: implementation-backed finding
scope: bounded inquiry non-answer explanation, authority-aware diagnostics, capability needs, privilege guidance
---

# Bounded Inquiry Explanation Reconciliation

## Boundary

This reconciliation asks only what current implementation already demonstrates
when a bounded inquiry cannot currently answer.

It does not propose an explanation engine, reasoning engine, conversation engine,
planner, generic inquiry framework, or capability maturity framework.
Repository authority wins.

## Central answer

Current implementation already exposes enough structured evidence for Seed to
truthfully explain parts of why a bounded inquiry cannot proceed, but the full
explanation is still composed across multiple existing subsystems.

The strongest supported statement is:

```text
For the reviewed ownership and authority diagnostics, Seed can expose what
observation is still needed, which current authority blocks or leaves that
observation uncertain, which capability would reduce the gap, and which boundary
keeps the diagnostic read-only. Humans still compose the complete inquiry-level
explanation across those surfaces.
```

The bounded non-answer explanation is therefore an emergent repository capability,
not a single owned runtime fact.

## Files inspected

Required implementation files:

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`

Required reconciliations reviewed:

- `docs/bounded_inquiry_identity_state_reconciliation.md`
- `docs/filesystem_ownership_constrained_authority_reconciliation.md`
- `docs/privilege_discovery_storage_capability_guidance_reconciliation.md`
- `docs/capability_maturity_observability_reconciliation.md`

Supporting inspection:

- `git status --short`
- `nl -ba` excerpts for the five implementation files above
- `sed -n` excerpts for required reconciliations

## 1. Recurring implementation-backed explanation components

The recurring explanation shape is not a named framework, but the same elements
repeat across the reviewed code paths.

| Component | Implementation-backed location | What it explains |
| --- | --- | --- |
| Desired observation / bounded goal | Container and service authority slice dataclasses and returns | What inquiry is being attempted. |
| Required observations | Container and service authority slices | What evidence the bounded inquiry needs. |
| Required authority | Container and service authority slices via privilege guidance | What authority class would make a needed observation possible. |
| Available authority | Container and service authority slices from supplied profile | What authority exists in the current constrained run. |
| Reachable / blocked / remaining observations | Service authority slice; container has remaining observations | Which evidence can proceed and which cannot. |
| Blocking boundary | Container and service authority slices | The concrete boundary that blocks Docker/root-dependent observation. |
| Uncertainty / remaining uncertainty | Container and service authority slices | What implementation-backed uncertainty remains after the current slice. |
| Conflict / reason / evidence count | Ownership discrepancy rows | What diagnostic condition created the gap. |
| Needed evidence / candidate capability | Ownership discrepancy capability records and capability-needs aggregation | What observation capability would reduce the gap. |
| Access level / suggested next step / notes | Privilege discovery guidance | Why a capability is or is not currently accessible and what operator-visible authority step is implied. |
| Read-only boundary / no cluster mutation | Authority slices and privilege discovery | Why explanation does not silently become operational mutation. |

Only recurring implementation-backed elements are counted here. The reviewed
repository does not expose a single `explanation` object, a normalized
`missing_subsystem` field, or a maturity stage field.

## 2. Does implementation identify what is missing, why it is missing, and what authority would reduce uncertainty?

Yes, bounded to the implemented diagnostics and authority slices.

### What is missing

`ownership_discrepancies` identifies diagnostic conflicts such as
`missing_owner`, `owner_not_observed`, `remote_export_attribution_missing`, and
`insufficient_evidence`. It also emits diagnostic capability records with
`needed_evidence` and `candidate_capability` for those conflicts.
`capability_needs` then aggregates those records by capability, subject,
diagnostic, needed evidence, and diagnostic run.

### Why it is missing

The authority slices explain current blockage by comparing required authority
with available authority. Container ownership becomes `blocked` when required
container-runtime observations require `docker_group_or_root` and both root and
Docker socket read authority are unavailable. Service ownership computes
reachable and blocked observations from required observations, required
authority, and the current profile, and marks the Docker/root boundary when that
current profile blocks container-runtime evidence.

`privilege_discovery` also explains missing guidance: unregistered capabilities
fall through to `access_level = "unknown"` with notes that no
implementation-backed privilege guidance is registered yet.

### What authority would reduce uncertainty

Where guidance is registered, `privilege_discovery` provides the authority class:
`partial_non_root` for listener-process inventory, `docker_group_or_root` for
container inventory and container port mapping, `available` for systemd
inventory, and `root` for NFS export inventory. The authority slices reuse that
guidance to populate `required_authority` for the bounded inquiry.

This is not universal. For unregistered storage capabilities such as
`mount_source_inventory`, `export_visibility_inventory`, `smb_share_inventory`,
and `remote_storage_export_inventory` in the current code, Seed can identify the
needed capability but only says privilege guidance is unknown unless a later
implementation registers guidance.

## 3. Is explanation owned by one subsystem?

No. The explanation is synthesized across existing subsystems.

- `ownership_discrepancies` owns diagnostic conflict shape, reason text,
evidence references, and capability-need emission.
- `capability_needs` owns aggregation from current projections and recorded
`diagnostic_run:*` facts.
- `privilege_discovery` owns access-level guidance, operator-facing next step,
notes, and the explicit unknown-guidance fallback.
- `container_ownership_authority` and `service_ownership_authority` own bounded
inquiry state under the constrained authority profile: required/available
authority, remaining observations, blockage, outcome, and uncertainty.

The repository-supported explanation is therefore compositional. No reviewed
file owns the whole sentence "this inquiry cannot answer because ..." as one
first-class runtime record.

## 4. Is this statement implementation-backed?

```text
Seed can explain
why an inquiry
cannot currently
answer.
```

Supported only with bounded wording:

```text
For the reviewed ownership/authority diagnostics, Seed can expose structured
implementation evidence explaining why a bounded inquiry cannot currently answer.
```

Rejected as an unqualified general statement because the implementation does not
show a generic inquiry explanation subsystem, a single explanation object, or
coverage for every possible inquiry. It does show recurring explanation
components for the reviewed authority-aware ownership surfaces.

## 5. Does current implementation distinguish lack of evidence, lack of authority, lack of implementation, and lack of guidance?

Yes, but unevenly.

| Lack type | Where distinguished | Implementation-backed meaning |
| --- | --- | --- |
| Lack of evidence | `ownership_discrepancies` conflict classes, reasons, evidence counts, and needed evidence | Existing facts do not establish the owner or attribution strongly enough. |
| Lack of authority | Container and service authority slices; privilege guidance | Required observations need root, Docker socket, or another access class that the current profile does not provide. |
| Lack of implementation | Human-synthesized from collectors/evaluators versus emitted capability names; documented in recent reconciliations | The repository may emit or consume a capability name without a corresponding collector/evaluator. No single code field records this. |
| Lack of guidance | `privilege_discovery._guidance_for()` unknown fallback | The capability lacks registered privilege guidance, even if some vocabulary or partial implementation exists elsewhere. |

The strongest distinction is between lack of evidence, lack of authority, and
lack of guidance. Lack of implementation remains a repository-supported human
conclusion rather than a first-class runtime field.

## 6. Is this repository-supported?

```text
Capability maturity
is an operator conclusion.

Inquiry explanation
is a repository fact.
```

Supported only if narrowed:

```text
Capability maturity is currently a human/operator conclusion from multiple
repository views. Inquiry explanation components are repository facts for the
reviewed diagnostics, but the complete inquiry explanation is still human-
synthesized across existing subsystems.
```

The first half is supported by the capability maturity reconciliation: current
implementation exposes signals, but not a normalized maturity stage. The second
half must be narrowed because fields such as `blocking_boundary`,
`remaining_observations`, `required_authority`, `needed_evidence`, and
`access_level` are repository facts, while the full explanation sentence is not
owned by one subsystem.

## 7. Narrowest missing subsystem responsibility

If explanation is incomplete today, the narrowest missing responsibility is not a
new framework. It is the existing capability/privilege boundary's responsibility
to preserve implementation-backed capability evidence alongside authority
guidance when turning diagnostic needs into operator-facing explanation.

That responsibility is narrow because:

1. `ownership_discrepancies` already emits the diagnostic conflict and candidate
capability.
2. `capability_needs` already aggregates the capability and needed evidence.
3. `privilege_discovery` already registers authority guidance and has an unknown
fallback.
4. The authority slices already expose blockage and remaining uncertainty.

The missing responsibility is to make the currently human-synthesized distinction
between "capability needed but collector absent", "capability needed but guidance
unknown", and "capability needed but authority unavailable" visible at that
existing seam. This is not a recommendation to add a framework; it is the
smallest existing subsystem boundary that naturally strengthens Seed's
self-explanation.

## Strongest supporting evidence

1. Container ownership exposes desired observation, required observations,
required authority, available authority, outcome, remaining observations,
uncertainty, remaining uncertainty, blocking boundary, and read-only/non-mutating
boundary fields.
2. Service ownership adds reachable and blocked observations to the same bounded
inquiry shape and computes partial reachability from current authority.
3. Ownership discrepancies encode concrete conflict classes and diagnostic reason
text, then map selected conflicts to needed evidence and candidate capabilities.
4. Capability needs aggregate diagnostic capability needs from both current
projection rows and recorded `diagnostic_run:*` facts.
5. Privilege discovery maps current capability pressure to access level,
operational benefit, suggested next step, notes, and explicit unknown guidance.
6. The reviewed reconciliations repeatedly reached the same pattern: humans can
compose a bounded explanation from repository surfaces, but repository authority
only supports the implemented fields and seams.

## Strongest contradictory evidence

1. No reviewed implementation owns a single normalized explanation record for an
inquiry non-answer.
2. No reviewed implementation records capability maturity or implementation
status as a first-class fact.
3. `privilege_discovery` unknown means missing guidance, not necessarily missing
implementation.
4. Storage capability needs can be emitted even when no collector or explicit
guidance exists for the capability.
5. Subsystem responsibility for a limitation is inferable from diagnostic and
capability names, but there is no normalized `limiting_subsystem` field.

## Acceptance answers

### When Seed cannot answer, what can it already truthfully explain?

For the reviewed surfaces, Seed can truthfully explain:

- the bounded observation being attempted;
- the observations required to answer;
- the currently available authority profile;
- the authority required by needed observations where guidance exists;
- which observations are reachable, blocked, or remaining where the slice exposes
that state;
- the diagnostic conflict and reason that created capability pressure;
- the needed evidence and candidate capability that would reduce the gap;
- whether privilege guidance is registered or unknown;
- that the diagnostic is read-only and does not mutate the cluster.

### Is explanation already an emergent repository capability, or are humans still composing it?

Both, with a boundary:

```text
Explanation components are an emergent repository capability.
The complete inquiry-level explanation is still human-composed across multiple
existing subsystems.
```

### What is the smallest existing subsystem that would naturally strengthen Seed's self-explanation?

The smallest natural subsystem boundary is the existing
`capability_needs` / `privilege_discovery` seam: it already receives diagnostic
capability pressure and turns it into operator-facing authority guidance. It is
also where missing guidance currently appears as `unknown`, which is the narrowest
place to make the difference between missing evidence, missing authority, missing
implementation evidence, and missing guidance less dependent on human synthesis.

## Report

### Files inspected

- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/privilege_discovery.py`
- `seed_runtime/capability_needs.py`
- `seed_runtime/ownership_discrepancies.py`
- `docs/bounded_inquiry_identity_state_reconciliation.md`
- `docs/filesystem_ownership_constrained_authority_reconciliation.md`
- `docs/privilege_discovery_storage_capability_guidance_reconciliation.md`
- `docs/capability_maturity_observability_reconciliation.md`

### Files changed

- `docs/bounded_inquiry_explanation_reconciliation.md`

### LOC changed

- Added 326 lines.

### Tests run

- Not run; documentation-only reconciliation.

### Recommended bounded implementation slice

Preserve implementation-backed capability evidence at the existing
`capability_needs` / `privilege_discovery` seam for capability names already
emitted by diagnostics, so operator-facing guidance can distinguish missing
evidence, missing authority, missing implementation evidence, and missing
guidance without introducing any new explanation framework.
