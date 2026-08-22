# Competency Interrogation Slice 003

## Selected implementation boundary

Granted Authority Assessment != Observation Permission / Eligibility Report Composition

The selected boundary is local to the observation-permission diagnostic. The implementation already used existing approval evidence to decide whether a reusable authority grant was observed, and then composed public observation-domain permission and future-invocation visibility from that result. This slice recovers the authority-grant assessment as a private implementation-local artifact without changing the public report shape.

This does not implement a Competency Interrogation Engine, runtime grammar, constitutional framework, authority framework, permission framework, global evaluator, planner, scheduler, routing redesign, campaign logic, methodology owner, or any new diagnostic surface.

## Implementation evidence

`seed_runtime/observation_permission.py` already concentrated the pressure in `_domain_entry(...)`:

1. It identified the observation class for a domain.
2. It searched the existing `State.approvals` model for reusable approval evidence through `_approval_for_domain(...)`.
3. It converted that evidence into authority-evidence text plus reusable and future-autonomous-invocation states.
4. It composed the public `ObservationPermissionDomain` report fields, including `permission_state`, `reasoning`, `known_limitations`, and compatibility JSON fields.

The existing tests already proved this surface is read-only, uses the existing approval model, preserves manual invocation boundaries, exposes diagnostic inventory visibility, and remains shape-audit consistent. That implementation evidence supported a neighboring constitutional safeguard: observed reusable authority is not the same responsibility as permission/eligibility/report composition.

## Before

`_domain_entry(...)` directly mixed:

- granted-authority assessment:
  - locating reusable approval evidence for an observation domain;
  - deriving authority evidence;
  - deriving reusable permission from that authority evidence;
  - deriving future autonomous invocation from that authority evidence;
- permission / eligibility / consumer report composition:
  - deriving `permission_state` for the public domain row;
  - assembling public reasoning;
  - attaching known limitations;
  - constructing `ObservationPermissionDomain`.

The behavior was compatible, but the implementation-local boundary between a reusable authority grant and public observation-permission visibility was only implicit.

## After

A private implementation-local assessment owner now exists:

- `_GrantedAuthorityAssessment`
- `_assess_granted_authority(...)`

`_domain_entry(...)` now consumes `_GrantedAuthorityAssessment` and remains the owner of public `ObservationPermissionDomain` composition.

## Recovered producer

`_assess_granted_authority(...)` is the recovered producer. It consumes the current `State`, the observation domain, and the implementation-known observation class, then produces only the local reusable-authority assessment needed by the observation-permission row composer.

## Recovered artifact/helper

`_GrantedAuthorityAssessment` is the recovered private artifact. It carries only:

- `domain`
- `approval_observed`
- `authority_evidence`
- `reusable_permission`
- `future_autonomous_invocation`

It intentionally does not carry public report-composition fields such as `permission_state`, `reasoning`, `known_limitations`, public report boundary flags, JSON output, or human-readable rendering.

## Recovered consumer

`_domain_entry(...)` consumes `_GrantedAuthorityAssessment` to compose the unchanged public `ObservationPermissionDomain` compatibility shape.

## Compatibility preserved

No compatibility boundary changed.

The CLI flag, JSON keys, diagnostic inventory entry, shape-audit expectations, record behavior, event-ledger behavior, runtime behavior, schema, and cluster-mutation boundary remain unchanged.

## Answers to required questions

### 1. Where were granted-authority assessment and permission/eligibility/report composition previously mixed?

They were mixed inside `_domain_entry(...)` in `seed_runtime/observation_permission.py`. That function both assessed existing reusable approval authority and composed the public observation-permission domain row.

### 2. Which implementation-local boundary became directly observable?

```text
Granted Authority Assessment
        !=
Observation Permission / Eligibility Report Composition
```

### 3. What private artifact or helper now carries the recovered assessment?

`_GrantedAuthorityAssessment`, produced by `_assess_granted_authority(...)`.

### 4. Who consumes it?

`_domain_entry(...)` consumes `_GrantedAuthorityAssessment` and composes `ObservationPermissionDomain`.

### 5. Did any compatibility boundary change?

No.

## Files changed

- `seed_runtime/observation_permission.py`
- `tests/test_observation_permission.py`
- `competency_interrogation_slice_003.md`

## LOC changed

Implementation/test diff before this report:

```text
seed_runtime/observation_permission.py | 59 +++++++++++++++++++++++++---------
tests/test_observation_permission.py   | 50 +++++++++++++++++++++++++++-
2 files changed, 92 insertions(+), 17 deletions(-)
```

This report adds the requested repository artifact.

## Tests executed

```text
pytest -q tests/test_observation_permission.py
pytest -q tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
python -m compileall -q seed_runtime/observation_permission.py
```

## Remaining compressed competency-interrogation responsibilities

The observation-permission diagnostic still intentionally keeps these responsibilities inside the existing local report producer unless future implementation evidence independently supports another slice:

- observation-domain class lookup and unsupported-domain handling;
- public `permission_state` derivation;
- public reasoning text assembly;
- known-limitation attachment;
- report-level diagnostic boundary projection;
- public JSON compatibility projection;
- human-readable formatting.

No framework, global authority system, permission framework, runtime grammar, routing redesign, planner, scheduler, or campaign logic was introduced.
