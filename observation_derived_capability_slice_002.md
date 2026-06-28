# Observation-Derived Capability Slice 002

## Selected architectural boundary

`Observed Evidence != Capability Verification`

This slice makes the candidate-observation payload and the repository-rule verification-status payload separately observable inside the private capability verification implementation.

## Implementation evidence

The transition from observed evidence to capability verification currently happens in `seed_runtime/capability_verification.py`:

- `build_capability_verification_inspection()` builds evidence-derived candidates with `build_capability_candidates()`.
- It acquires additional local verification evidence with `build_verification_evidence()`.
- It reads current capability verification inventory with `build_capability_inventory()`.
- `_verification_for_candidate()` joins the candidate evidence, acquired evidence, and inventory-derived status into the public `CapabilityVerification` inspection record.

Repository authority showed that the public behavior already distinguished candidates, verification evidence, and verification facts, but `_verification_for_candidate()` compressed observed-evidence payload construction and verification-status payload construction into one responsibility.

## Before

`_verification_for_candidate()` directly constructed `CapabilityVerification` for both branches:

- missing inventory entry: copied candidate evidence and acquired evidence while assigning `verification_status="unverified"`;
- existing inventory entry: copied candidate evidence, acquired evidence, supporting facts, supporting evidence, and inventory state in the same return expression.

That meant the implementation transition from observed evidence to capability verification was present, but not locally visible as two implementation responsibilities.

## After

The slice adds two private implementation-local value objects:

- `_ObservedCapabilityEvidence`: preserves the observed candidate evidence and acquired verification evidence for one candidate.
- `_CapabilityVerificationStatus`: carries the repository-rule interpretation of verification state, supporting verification facts/evidence, and rationale.

`_verification_for_candidate()` now composes the public `CapabilityVerification` from:

1. `_observed_evidence_for_candidate(...)`
2. `_verification_status_for_candidate(...)`

## Boundary made explicit

The explicit recovered boundary is:

```text
Observed Evidence
    !=
Capability Verification
```

Observed evidence construction now has its own private object/function. Verification-status construction now has its own private object/function. The public output remains the existing `CapabilityVerification` shape.

## Compatibility preserved

No compatibility boundary changed.

This slice did not change:

- public class names;
- CLI names;
- JSON keys;
- event names or payloads;
- ledger behavior;
- schema behavior;
- candidate derivation;
- binary evidence acquisition;
- verification status rules;
- capability inventory output;
- promotion behavior;
- runtime, tool execution, policy, or provider behavior.

## Files changed

- `seed_runtime/capability_verification.py`
- `observation_derived_capability_slice_002.md`

## LOC changed

`git diff --stat` after the implementation reported:

```text
seed_runtime/capability_verification.py | 62 ++++++++++++++++++++++++++++-----
1 file changed, 54 insertions(+), 8 deletions(-)
```

The report file was then added as this slice deliverable.

## Tests executed

```text
pytest -q tests/test_capability_verification_inspection.py tests/test_capability_inventory.py
```

Result:

```text
18 passed
```

## Remaining compressed observation-derived capability boundaries

Implementation evidence still suggests future slices may inspect these boundaries without vocabulary migration or public behavior changes:

- package-observed candidate evidence vs. package-to-capability candidate mapping;
- binary-path observation acquisition vs. sufficiency rules for capability verification;
- provider-reported capability evidence vs. repository verification status interpretation;
- projected `capability_verified` fact support vs. inventory entry presentation;
- promotion readiness evidence vs. any future creation of durable verification facts.
