# Null State Transition Discipline Investigation

## Executive answer

Implementation evidence supports a recurring, bounded **Null State Transition Discipline** across several mature read-only visibility, diagnostic, verification, and inquiry-adjacent surfaces.

The repository does not support recovering this as a new shared architectural ownership family.

```text
Insufficient implementation evidence.
```

The supported characterization is narrower:

```text
Null / unknown / candidate / unsupported

-> observation
-> preserved evidence
-> repository-rule interpretation
-> bounded supported status
-> explicit authority boundary or stop condition
```

This discipline is real as an implementation-backed epistemic methodology, but it remains uneven outside the strongest visibility and diagnostic competencies.

## Evidence standard

This investigation treats implementation and tests as primary authority. Prior recovery reports are secondary evidence only where they summarize implementation-backed behavior.

The relevant implementation question is not whether the vocabulary "Null State Transition Discipline" already exists. The question is whether repository behavior repeatedly prevents unsupported transition from unknown or candidate state into trusted knowledge, ownership, authority, execution, or mutation.

## Question 1: Does implementation consistently begin from an uncommitted state?

Yes, in the reviewed mature surfaces, but not as a universal framework.

Capability verification begins from evidence-derived candidates and does not treat candidate evidence as verified capability knowledge. A candidate without an existing projected `capability_verified` fact remains `unverified`.

Selection-path audit begins from an implemented selection target check. If no implementation-backed selection surface exists for the requested target, it returns `selected="unknown"` and records an explicit unknown reason.

Diagnostic inventory begins from declared operational shape rather than assumed authority. A diagnostic surface must declare record support, record scope, event-ledger behavior, diagnostic fact emission, cluster fact emission, and cluster mutation behavior.

## Question 2: What observable transitions are permitted away from Null?

Permitted transitions are evidence-gated and authority-bounded:

1. Candidate capability evidence may become a displayed capability candidate.
2. Candidate capability evidence may become `verified` only through existing projected `capability_verified` semantics.
3. Missing verification evidence remains `unverified`.
4. Unknown selection targets remain `unknown` unless implemented selection evidence exists.
5. Diagnostic output may be recorded only under declared diagnostic scope.
6. Event-ledger writes do not imply cluster mutation.
7. Diagnostic facts do not silently become cluster facts.
8. Executable operation contract metadata may widen presentation, but does not verify capability existence or grant execution authority.

## Question 3: Which competencies currently preserve this discipline?

The strongest implementation-backed preservation appears in:

- Capability Verification.
- Capability Inventory.
- Selection Path Visibility.
- Diagnostic Inventory.
- Diagnostic Shape Audit, through tests that compare declared diagnostic shape against implementation behavior.
- Read-only operational authority surfaces that declare `mutates_cluster=false`.
- Negative and unsupported inquiry methodology, as summarized by prior implementation-backed recovery reports.

These competencies preserve separate concepts for observation, evidence, classification or status, authority, and stop condition.

## Question 4: Are any competencies permitted to bypass Null?

No reviewed mature visibility, diagnostic, or verification competency is permitted to bypass Null in the strong sense of converting observation directly into trusted knowledge, execution authority, cluster mutation, or ownership.

The repository does contain uneven implementation areas. Provider language translation is a known partial case: some providers preserve intermediate evidence explicitly, while compressed provider paths place observation, classification, and observation construction close together. That unevenness prevents a universal-family conclusion, but it does not provide positive evidence that bypassing Null is allowed.

## Question 5: Does implementation evidence support this as recurring epistemic discipline rather than merely architectural recovery?

Yes, boundedly.

The discipline appears in capability verification, diagnostic shape declaration, selection explanation, operation/capability boundary handling, and negative unsupported inquiry behavior. Those domains are broader than architectural recovery alone.

The repository already contains a closely related recovered pattern:

```text
Observation -> Evidence -> Classification -> Authority -> Stop
```

That report concludes the pattern is real but bounded, strongest in read-only visibility and diagnostic/evaluation surfaces, and not a shared ownership implementation.

The Null framing is therefore supported as a generalization of recurring epistemic discipline:

```text
Do not transition from candidate/unknown/unsupported into accepted knowledge or authority without evidence and an explicit boundary.
```

## Question 6: Is there sufficient implementation evidence to justify a new architectural family?

```text
Insufficient implementation evidence.
```

There is enough implementation evidence to name a recurring discipline or methodology pattern. There is not enough implementation evidence to create a new architectural family, shared base class, runtime pipeline, schema layer, or ownership recovery.

## Supported conclusion

The repository already operates under a general bounded discipline:

```text
Null persists until evidence justifies transition.
```

This is supported across multiple competencies, especially read-only visibility, diagnostic, and verification surfaces.

## Unsupported conclusions

The evidence does not support:

- a universal Null-state runtime pipeline;
- a new architectural ownership family;
- schema changes for a universal transition model;
- a shared base class for all competencies;
- a claim that every provider path preserves the same intermediate evidence structure;
- a claim that every implementation surface begins from an explicit public `Null` object;
- a claim that observation alone can become truth, ownership, permission, execution, or mutation.

## Final classification

```text
Real recurring epistemic methodology: supported.
Recurring competency expression in mature visibility/diagnostic/verification surfaces: supported.
Universal implementation pattern: unsupported.
New architectural family: insufficient implementation evidence.
```
