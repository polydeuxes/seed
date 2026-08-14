# Observation-Derived Capability Slice 003

## selected architectural boundary

`Capability Verification != Capability Promotion`.

This slice makes the transition from verification payload construction to promotion-readiness/admission decision directly observable inside the existing capability promotion-readiness implementation.

## implementation evidence

- `build_capability_promotion_readiness_inspection()` still constructs the same candidate universe from evidence-derived capability candidates.
- It still gathers verification evidence through `build_verification_evidence()`.
- The transition point remains local to `_readiness_for_candidate()`.
- The implementation now routes that transition through an implementation-local `_CapabilityVerificationPayload` before applying the promotion-readiness decision.
- `_promotion_readiness_from_verification_payload()` is the only place in this slice that decides whether the verified evidence payload is promotion-ready.

## before

`_readiness_for_candidate()` directly combined two responsibilities:

1. copying the candidate evidence and verification evidence into the verification-side payload; and
2. deciding whether those verified inputs support future capability verification promotion.

That made verification construction and promotion/admission readiness appear as one implementation responsibility even though the public behavior already preserved the boundary by not creating `capability_verified` facts or mutating repository state.

## after

The code now separates the local responsibilities:

1. `_verification_payload_for_candidate()` constructs an implementation-local verification payload from candidate support and verification support.
2. `_promotion_readiness_from_verification_payload()` consumes that payload and decides whether promotion readiness is `supported` or `unsupported`.
3. `_readiness_for_candidate()` remains the compatibility-preserving adapter that composes the two private steps and returns the existing public `CapabilityPromotionReadiness` shape.

## boundary made explicit

The recovered boundary made explicit is:

```text
Capability Verification Payload
        !=
Capability Promotion Readiness Decision
```

This is the smallest observable implementation boundary that reflects the recovered distinction:

```text
Capability Verification
        !=
Capability Promotion
```

## compatibility preserved

No compatibility boundary changed.

Specifically, this slice did not change:

- public class names;
- CLI flags;
- JSON shape;
- event ledger behavior;
- schema;
- verification rules;
- promotion-readiness rules;
- capability inventory output;
- repository mutation behavior.

## files changed

- `seed_runtime/capability_promotion_readiness.py`
- `observation_derived_capability_slice_003.md`

## LOC changed

Implementation diff before this report:

```text
36 insertions, 8 deletions in seed_runtime/capability_promotion_readiness.py
```

## tests executed

```text
pytest -q tests/test_capability_promotion_readiness.py tests/test_capability_verification_inspection.py
```

Result:

```text
21 passed
```

## remaining compressed observation-derived capability boundaries

Potential remaining compressed boundaries to investigate in future slices, without changing them in this slice:

- promotion-readiness inspection vs. any future durable `capability_verified` fact creation;
- verification evidence acquisition vs. verification fact authority;
- capability inventory construction vs. current operational capability state;
- capability admission vs. capability selection, authorization, policy evaluation, or execution;
- read-only capability catalog metadata vs. observed capability evidence.
