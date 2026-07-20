# Principal Identity Reconciliation

## Purpose

This audit determines whether Seed already has a first-class distinction equivalent to:

```text
claimed_principal
authenticated_principal
```

The audit is documentation-only. It does not modify runtime behavior, event storage, authentication, authorization, policy, approval handling, observation ingestion, projection behavior, tests, or local CLI behavior.

The motivating distinction is:

- A **claimed principal** is an identity asserted by content or an upstream source, for example text that says `I am John`.
- An **authenticated principal** is an identity verified by a trusted system boundary, for example an authenticated browser user, verified CLI user, trusted service account, or explicit approval grant identity.

## Existing Identity-Like Surfaces

Seed has several identity-like surfaces, but they currently answer different questions.

| Surface | Existing vocabulary | What it means today | Claimed/authenticated principal? |
| --- | --- | --- | --- |
| Event metadata | `actor`, `workspace_id`, `session_id`, `causation_id`, `correlation_id` | Event authorship and scoping metadata. | No. `actor` is coarse event-author vocabulary, and workspace/session are scopes rather than proof of identity. |
| Runtime input | `input.user_message`, `payload={"text": ...}`, `actor="user"` | Raw text from the caller in a workspace/session. | No. The payload can contain identity claims, but Seed does not parse or trust them as principal records. |
| API/CLI intake | `workspace_id`, `session_id`, local defaults such as `local` | Caller-supplied or default scopes for interaction. | No. They do not establish OS user, browser user, service account, or verified human identity. |
| Observation ingestion | `source_type`, `confidence`, evidence source, observation metadata, caller-selected ingestion `actor` | Provenance for observed facts. | Partial analogy only. It tracks source class and confidence for observations, not who is speaking through generic input. |
| Policy and approvals | `policy_action`, `risk_class`, `PolicyOutcome`, `Approval.approved_by`, pending-action status | Tool-risk and approval-gate vocabulary. | Partial analogy only. `approved_by` and `granted_by` record grant identities, but they are downstream approval/authorization metadata, not input principal classification. |
| Legacy execution authorization | `ExecutionAuthorization.granted_by` | Secret-free, short-lived grant metadata for a concrete legacy/experimental execution proposal. | Partial analogy only, and explicitly non-core. It is not a general authenticated input principal. |
| Input-envelope docs | `principal_claim`, `authenticated_principal`, `authentication_strength`, `authorization_scope` | Documentation-only vocabulary for future source envelopes. | Conceptual distinction exists in documentation, but not as current runtime data or model. |

## Actor Vocabulary

`Actor` is defined as:

```text
user
model
system
tool
builder
approver
```

This is event authorship vocabulary. It records which Seed-side category appended or caused an event, not a verified person, browser account, CLI account, service principal, device principal, or upstream identity.

Important boundaries:

- `actor="user"` does not mean the text was authenticated.
- `actor="approver"` does not name the approver; it only classifies the event author category.
- `actor="system"`, `actor="tool"`, `actor="model"`, and `actor="builder"` are operational authorship labels, not principals.
- `workspace_id` and `session_id` scope history and interaction, but they are not identity proofs.

Therefore `Actor` is not equivalent to either `claimed_principal` or `authenticated_principal`.

## Approval And Authorization Vocabulary

Seed already has approval and authorization-adjacent terms:

- `PolicyOutcome`: `allow`, `block`, `require_confirmation`, `require_approval`.
- `ToolSpec.policy_action` and `ToolSpec.risk_class`.
- `Approval`: `action`, `scope`, `approved_by`, `expires_at`, `constraints`.
- `PendingAction`: stored tool call awaiting confirmation or approval, with `scope` and status.
- `ActionPlan.approved`: plan acceptance/approval, explicitly not execution permission.
- `ExecutionAuthorization`: legacy/experimental secret-free grant metadata with `granted_by` for a concrete proposal.

These concepts are important but downstream of input identity. They answer questions such as:

- Is this registered tool call structurally valid?
- What is the action risk?
- Is there a matching approval for this action and scope?
- Has a specific pending action been approved?
- Was a legacy execution proposal granted short-lived authorization?

They do not answer:

- Who did the input claim to be?
- Who did a trusted boundary authenticate as the submitter of this input?
- How strong was that authentication?
- What request authority did that authenticated submitter have at the input boundary?

`Approval.approved_by` and `ExecutionAuthorization.granted_by` are the closest existing principal-like fields. They record grant identities, but they are not a general `authenticated_principal` attached to arbitrary input. They also do not model an untrusted identity asserted by text, so they are not `claimed_principal` either.

## Observation Source Vocabulary

Observation ingestion has richer provenance vocabulary than generic user-message intake:

- `Observation.source_type`: `user`, `discovery`, `provider`, `imported`, or `inferred`.
- `Fact.source_type`: corresponding provenance for projected facts.
- `Evidence.source`: a source string such as `observation:user` or `observation:provider`.
- `confidence`: source-provided confidence for observations and derived facts.
- CLI development paths mention `ingested_by` as metadata for seeded observations/facts.

This vocabulary is not a principal distinction.

Observation source metadata can say that an observation came from a user-class source, discovery, provider, import, or inference. It cannot say that `John` claimed the observation, that an authenticated browser session verified `John`, or that `John` had a particular input authorization scope. An observation from `source_type="user"` is still an observation-source classification, not proof of a principal.

## Claimed Identity Concepts Found

Seed has no first-class runtime model, event field, or canonical input payload field named `claimed_principal`.

Related but non-equivalent concepts found:

- `input.user_message.payload.text` can contain arbitrary identity assertions such as `I am John`, but Seed stores the text as text and does not extract a principal claim.
- `Actor` can be `user`, but this is a coarse event-author category rather than a claimed human/service identity.
- `Observation.source_type="user"` can mark user-provided observations, but it does not preserve which principal was claimed.
- `docs/input_source_authority_reconciliation.md` recommends `claimed_principal` as future vocabulary.
- `docs/input_envelope_vocabulary.md` currently defines the closely related term `principal_claim`, not runtime `claimed_principal`.

Finding: Seed has conceptual documentation for the idea of a claimed principal, but it does not have a first-class implemented `claimed_principal` surface for generic input.

## Authenticated Identity Concepts Found

Seed has no first-class runtime model, event field, or canonical input payload field that attaches `authenticated_principal` to generic input.

Related but non-equivalent concepts found:

- `Approval.approved_by` records who approved an action/scope grant, but it is approval metadata rather than authenticated input identity.
- `ExecutionAuthorization.granted_by` records who granted a legacy/experimental authorization for a concrete proposal, but that model is non-core and not generic input identity.
- `actor="approver"` records an event-author category, not the authenticated approver principal.
- `workspace_id` and `session_id` are scoping identifiers, not authentication records.
- `SeedAPI.post_user_message(...)` and local CLI paths pass workspace/session/text without authentication metadata.
- `docs/input_envelope_vocabulary.md` defines `authenticated_principal` as documentation-only future vocabulary.

Finding: Seed has documentation-only vocabulary and downstream grant identity fields, but it does not have a first-class current `authenticated_principal` attached to input.

## Missing Concepts

Seed does not currently have a first-class distinction equivalent to `claimed_principal` versus `authenticated_principal` in implemented runtime or storage surfaces.

The missing concepts are intentionally small:

- a canonical input-level field for identity asserted by content or upstream source;
- a canonical input-level field for identity verified by a trusted boundary;
- a canonical way to preserve authentication strength for that verified identity;
- a canonical input-level authorization scope that describes what the authenticated principal may request;
- an invariant that the claimed identity is untrusted by itself;
- an invariant that authenticated identity still does not bypass validation, guard, policy, approval, or pending-action boundaries.

The smallest gap is not an engine or provider framework. The smallest gap is a missing metadata distinction on input source context.

## Ownership Boundaries

This audit preserves existing owners and boundaries:

- `Runtime` owns canonical user-message intake and decision routing.
- `EventLedger` owns append-only event history.
- `ContextComposer` owns context packet construction from current input and projected state.
- `ToolExecutionPolicyService` and `PolicyGate` own registered-tool policy evaluation.
- `PendingActionService` owns pending-action lifecycle events.
- `ObservationIngestor` owns observation-to-evidence-to-fact provenance ingestion.
- `StateProjector` owns projected state reconstruction.
- Legacy `ActionPlan`, `HandoffPlan`, `ExecutionProposal`, and `ExecutionAuthorization` remain non-core compatibility/side-path artifacts.

An input principal vocabulary should remain below these boundaries. It may describe source context, but it must not become execution approval.

## Rejected Solutions

This audit rejects the following solutions:

- adding `AuthEngine`;
- adding `IdentityEngine`;
- adding `SessionEngine`;
- adding an authentication provider framework;
- rewriting `Runtime`;
- modifying tests;
- introducing new runtime models;
- treating text such as `I am admin` as authentication;
- treating `actor="user"` as authenticated identity;
- treating `workspace_id` or `session_id` as proof of identity;
- treating `source_type="user"` as a verified principal;
- treating `approved_by` or `granted_by` as a generic input principal;
- treating `authorization_scope` as execution approval;

## Recommended Vocabulary

Because Seed does not currently have a first-class implemented distinction equivalent to `claimed_principal` and `authenticated_principal`, use only the following minimal vocabulary for future input-envelope design:

### `claimed_principal`

Identity asserted by content or upstream source.

Not trusted by itself.

### `authenticated_principal`

Identity verified by a trusted boundary.

May still require authorization checks.

### `authorization_scope`

What an authenticated principal may request.

Not execution approval.

## Direct Answer

Seed does **not** currently have a first-class implemented distinction equivalent to:

```text
claimed_principal
authenticated_principal
```

Current status:

- `claimed_principal`: not implemented as a first-class runtime, event, or storage field. The idea appears in documentation as future vocabulary, and `principal_claim` appears in input-envelope documentation as a closely related documentation-only term.
- `authenticated_principal`: not implemented as a first-class runtime, event, or storage field for generic input. The term appears in input-envelope documentation only. Downstream grant fields such as `approved_by` and `granted_by` are not substitutes.

The gap is a missing input-source metadata distinction, not a missing authentication engine or runtime route.
