# Input Envelope Vocabulary

## Purpose

This document defines first-class vocabulary for describing the source context of input before Seed classifies the utterance as an `InputAct` or chooses a downstream `DecisionKind`.

It is documentation-only. It does not modify runtime behavior, event storage, authentication, authorization, policy, tool execution, projection behavior, package exports, or local CLI behavior.

The motivation comes from `docs/input_source_authority_reconciliation.md`: Seed can already preserve raw text, workspace id, session id, and a coarse event actor, but it does not yet preserve where generic input came from, who or what submitted it, how that identity was established, or what authority context surrounds it.

## Central Distinction

`InputEnvelope` answers:

> Where did this input come from, who or what submitted it, and what source context surrounds it?

`InputAct` answers:

> What kind of thing did the user say?

`DecisionKind` answers:

> What should Seed do next?

These are related, but they are not the same thing.

```text
InputEnvelope != InputAct
InputAct != DecisionKind
InputEnvelope != Authorization
```

An input envelope preserves source metadata. It must not authenticate a user by itself, authorize execution, bypass validation, or grant trust merely because the payload text claims authority.

## Layer Model

The intended conceptual stack is:

```text
InputEnvelope
        ↓
InputInspection / InputAct
        ↓
DecisionKind
        ↓
Validation / guard / policy / capability boundaries
        ↓
Runtime route
```

Each layer answers a different question:

| Layer | Question |
| --- | --- |
| `InputEnvelope` | Where did the input come from and what source context surrounds it? |
| `InputAct` | What kind of utterance was received? |
| `DecisionKind` | What route should Seed take next? |
| Validation / guard / policy | Is that route structurally valid and allowed? |
| Runtime route | Which owner service handles the valid decision? |

## Initial Vocabulary

### `channel`

`channel` describes the broad interface through which input entered Seed.

Example values:

```text
cli
browser
api
voice
webcam
home_assistant
webhook
automation
file_import
connector
unknown
```

It is not identity, proof of authentication, authorization, or execution permission.

### `transport`

`transport` describes the lower-level delivery mechanism or integration path.

Example values:

```text
local_process
stdin
http_session
websocket
rest_api
mqtt
home_assistant_event
microphone_transcript
camera_ocr
scheduled_job
connector_callback
unknown
```

It is not the same as `channel`, proof of human identity, or a policy decision.

### `modality`

`modality` describes the form of the payload before semantic classification.

Example values:

```text
text
audio_transcript
image_ocr
video_derived
event_payload
json
file
mixed
unknown
```

It is not `InputAct` and does not say whether the payload is a command, query, observation, correction, or casual answer.

### `payload_kind`

`payload_kind` describes the immediate representation handed to Seed.

Example values:

```text
user_text
transcribed_text
ocr_text
structured_event
uploaded_document
imported_observation_batch
connector_result
unknown
```

It is not semantic classification, source trust, or a durable observation/fact by default.

### `principal_claim`

`principal_claim` is the identity the source, payload, or upstream system claims is responsible for the input.

Example values:

```text
operator
admin
service:home_assistant
unknown
```

It is not authenticated identity. It must not be trusted merely because input text claims authority.

### `authenticated_principal`

`authenticated_principal` is the identity established by an external authentication boundary, if any.

Example values:

```text
operator:john
service:home_assistant
device:kitchen_tablet
none
unknown
```

It is not a role by itself and is not sufficient for execution authority without policy and authorization scope.

### `authentication_strength`

`authentication_strength` describes how strongly the source identity was established.

Suggested vocabulary:

```text
none
claimed
weak
session
strong
service_account
unknown
```

It is not authorization, approval, or a bypass around tool policy.

### `authorization_scope`

`authorization_scope` describes what the authenticated principal is allowed to request or influence at the input boundary.

Suggested vocabulary:

```text
none
read_only
conversation
observation_submitter
claim_submitter
low_risk_actions
operator
admin
service_limited
unknown
```


### `source_trust`

`source_trust` describes Seed's coarse trust posture toward the input source.

Suggested vocabulary:

```text
untrusted
low
medium
high
system
unknown
```

It is not truth, correctness, or execution approval.

### `source_risk`

`source_risk` describes the risk introduced by the input source itself, separate from the requested action's risk class.

Suggested vocabulary:

```text
unknown_source
unauthenticated_remote
transcription_uncertain
ocr_uncertain
third_party_payload
automation_generated
trusted_local_operator
trusted_service
unknown
```

This is not a replacement for `ToolSpec.risk_class`. It describes the source, not the operation.

### `device_id`

`device_id` identifies the device or integration endpoint that submitted the input when available.

Example values:

```text
local_cli
browser_session
kitchen_tablet
home_assistant
webhook
unknown
```

It is not a human identity, proof of trust, or authorization scope.

### `origin`

`origin` captures optional origin metadata such as host, connector, service, or process label when safe to store.

Example values:

```text
localhost
ssh_session
browser
home_assistant
connector:github
unknown
```

Origin metadata must remain secret-safe and should not store credentials, tokens, cookies, or sensitive identifiers unless explicitly modeled as safe metadata.

## Example Envelopes

### Local CLI typed by trusted operator

```text
channel: cli
transport: local_process
modality: text
payload_kind: user_text
principal_claim: operator
authenticated_principal: operator:john
authentication_strength: weak | strong depending on host/session boundary
authorization_scope: operator
source_trust: high
source_risk: trusted_local_operator
device_id: local_cli
origin: localhost
```

This may support operator workflows, but it still does not bypass validation, guard, or policy.

### Browser session authenticated as operator

```text
channel: browser
transport: http_session
modality: text
payload_kind: user_text
principal_claim: operator
authenticated_principal: operator:john
authentication_strength: session
authorization_scope: operator
source_trust: high
source_risk: trusted_local_operator
device_id: browser_session
origin: browser
```

This establishes a stronger principal than text alone, but execution remains gated.

### Browser session with read-only scope

```text
channel: browser
transport: http_session
modality: text
payload_kind: user_text
principal_claim: viewer
authenticated_principal: viewer
authentication_strength: session
authorization_scope: read_only
source_trust: medium
source_risk: unknown
```

This may allow questions or read-only interactions, but should not allow privileged side effects.

### Unknown voice transcript

```text
channel: voice
transport: microphone_transcript
modality: audio_transcript
payload_kind: transcribed_text
principal_claim: unknown
authenticated_principal: none
authentication_strength: none
authorization_scope: none
source_trust: low
source_risk: transcription_uncertain
```

This should not authorize side effects merely because the transcript contains a command.

### Webcam/OCR-derived input

```text
channel: webcam
transport: camera_ocr
modality: image_ocr
payload_kind: ocr_text
principal_claim: unknown
authenticated_principal: none
authentication_strength: none
authorization_scope: none
source_trust: untrusted
source_risk: ocr_uncertain
```

This should be treated as untrusted input unless a separate trusted process establishes authority.

### Home Assistant automation event

```text
channel: home_assistant
transport: home_assistant_event
modality: event_payload
payload_kind: structured_event
principal_claim: service:home_assistant
authenticated_principal: service:home_assistant
authentication_strength: service_account
authorization_scope: service_limited
source_trust: medium
source_risk: automation_generated
```

This can be useful for observations or low-risk automation paths, but it is not a human operator command.

### Unauthenticated webhook

```text
channel: webhook
transport: rest_api
modality: json
payload_kind: structured_event
principal_claim: unknown
authenticated_principal: none
authentication_strength: none
authorization_scope: none
source_trust: untrusted
source_risk: unauthenticated_remote
```

This should never be trusted as command authority.

## Relationship To InputAct

An envelope should be created or supplied before input-act classification.

Example:

```text
InputEnvelope(channel=voice, authenticated_principal=none, source_trust=low)
        ↓
InputAct(command_request)
        ↓
DecisionKind(refuse or ask_question)
```

The same text through a different envelope may have a different safe downstream route:

```text
InputEnvelope(channel=cli, authenticated_principal=operator:john, source_trust=high)
        ↓
InputAct(command_request)
        ↓
DecisionKind(request_tool, propose_action_plan, call_tool, ask_question, or refuse)
```

The input act is the same. The authority context is different.

## Relationship To DecisionKind

`InputEnvelope` should not choose `DecisionKind` directly. It should constrain or inform later decisions.

Examples:

- Unknown voice plus `command_request` should bias away from side effects.
- Authenticated operator browser plus `operator_query` may answer normally.
- Home Assistant event plus `user_observation` may support observation intake if an owner exists.
- OCR text plus `command_request` should not become `call_tool` merely because the text is imperative.

## Relationship To Policy And Approval

An input envelope can provide metadata to policy, but it must not replace policy.

Policy still needs to evaluate:

- requested action;
- tool risk class;
- registered operation visibility;
- authenticated principal;
- authorization scope;
- approval status;
- pending-action status;
- source trust;
- context-specific constraints.

An envelope may help policy decide that an action requires confirmation, approval, refusal, or read-only handling. It must not itself grant approval.

## Relationship To Observations

Observation ingestion already has source metadata such as `source_type`, `confidence`, and `ingested_by` in development CLI paths.

That metadata is not the same as a general input envelope.

A future implementation may map an input envelope into observation metadata when user input becomes a user-provided observation, but the mapping must remain explicit.

```text
InputEnvelope
        ↓
InputAct(user_observation)
        ↓
future observation intake owner
        ↓
Observation metadata
```

The envelope does not make the observation true.

## Relationship To Event Metadata

Current events already carry `actor`, `workspace_id`, `session_id`, `causation_id`, and `correlation_id`.

A future implementation could preserve envelope metadata in an event payload or add a narrow model referenced by the input event. This document does not require either approach.

Any future storage must remain secret-safe.

## Future Implementation Boundary

A later implementation may add a narrow immutable record such as:

```text
InputEnvelope:
  channel: str
  transport: str
  modality: str
  payload_kind: str
  principal_claim: str | None
  authenticated_principal: str | None
  authentication_strength: str
  authorization_scope: str
  source_trust: str
  source_risk: str | None
  device_id: str | None
  origin: str | None
```

If implemented, it should be metadata-only at first.

It should not:

- rewrite `Runtime`;
- replace `InputInspection`;
- replace `InputAct`;
- choose final `DecisionKind`;
- execute tools;
- authorize side effects;
- bypass `ToolIntentGuard`;
- bypass policy, approval, pending-action, or registered-tool boundaries;
- make `request_tool` executable;
- store secrets.

## Rejected Solutions

This vocabulary rejects:

- treating text like `I am admin` as authentication;
- inferring authority from tone, confidence, or imperative wording;
- treating CLI input as unlimited authority;
- treating local network input as trusted by default;
- treating voice input as authenticated by default;
- treating webcam/OCR input as command authority;
- treating Home Assistant automation as a human operator;
- treating browser input as trusted without a verified session/principal;
- treating `InputAct` as authorization;
- treating `DecisionKind` as authentication;
- adding `AuthEngine`, `IdentityEngine`, `ChannelEngine`, or a new `RuntimeLoop`;
- bypassing validation, guard, policy, approval, pending-action, or registered-tool boundaries;
- using source metadata as implicit approval for side effects.

## Documentation-Only Status

This document defines vocabulary only. It does not modify runtime behavior, classifier behavior, source handling, authentication, authorization, policy, event ledger behavior, projection behavior, tool execution, package exports, or local CLI behavior.
