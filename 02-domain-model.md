# 02 Domain Model

This document defines clean names for the new system. Avoid legacy terms that imply the old architecture.


## Raw IN and semantic catalogs

Raw inputs enter Seed through a non-executing pipeline:

```text
raw input
  -> InputInspector
  -> ObservationSource
  -> ObservationNormalizer
  -> ObservationIngestor
  -> Evidence / Facts
```

The domain vocabulary is split into catalogs so current state remains explainable:

- `PredicateCatalog` defines what can be known, including canonical predicate names, value types, units, provider mappings, and cardinality.
- `RelationshipCatalog` defines how entities connect and which relationship kinds control graph traversal.
- `EntityTypeCatalog` defines the classes of entities and validates which predicates/relationships fit those classes.
- `CapabilityCatalog` defines what can be recommended or handed off to external providers.
- `InferenceCatalog` defines deterministic rules that produce inferred facts from unambiguous observed facts. It is not LLM projection logic.

## Canonical capability/tool vocabulary

Use this vocabulary when describing how Seed moves from user/system needs to safe recommendations, handoffs, and registered calls. Some current code and docs still use “tool” broadly; until names are cleaned up, read the terms through these boundaries.

| Term | Meaning | Examples | Boundary |
| --- | --- | --- | --- |
| Requirement | What a user or system needs accomplished. | “Find why Docker storage is full”; “make this host reachable over SSH.” | Explains the desired outcome; it is not a callable interface. |
| Capability | Abstract ability Seed needs or can recommend. | `observe_metrics`, `inspect_filesystem`, `remote_access`, `hear_human`, `speak_human`, `observe_video`. | Explains **why** Seed needs an ability; conceptual and not necessarily executable. |
| Tool / Operation | Named callable interface satisfying a capability. | `prometheus_query`, `read_file`, `list_dir`, `stat_file`, `grep_file`, `ssh_exec`, `sftp_read`, `sftp_write`, `sshfs_mount`, `piper_tts`. | Defines **what** can be called, subject to registry, visibility, schema, and policy. |
| Implementation | Concrete backend adapter fulfilling an operation. | Prometheus HTTP API adapter, local filesystem adapter, OpenSSH adapter, Paramiko adapter, Piper adapter, Whisper adapter. | Defines **how** a registered operation is fulfilled. |
| Provider | External system or backend exposing one or more implementations. | Prometheus, SSH, local OS, Frigate, Piper, AWX. | Owns backend behavior, credentials, side effects, and provider-specific limits outside Seed’s conceptual model. |
| Toolkit | Package of capability metadata, operations, schemas, policies, observation adapters, handoff metadata, tests, and docs. | SSH access toolkit, Docker observability toolkit, file inspection toolkit. | Packages and validates contracts; existence does not grant execution. |
| ToolNeed | Durable request for a missing capability or provider handoff target. | “Need metric observation through Prometheus”; “need remote file inspection over SSH/SFTP.” | Records the gap; often means “CapabilityNeed” in practice and does not invent execution. |

Architecture rule: capabilities explain why Seed needs an ability; tools/operations define what can be called; implementations define how the call is fulfilled; providers are external backends or systems; toolkits package and validate those contracts. Seed should reason about capabilities first, then choose visible tools/operations and implementations through registry, policy, and provider boundaries.

Clarifying examples:

- Prometheus is not one tool; it is a provider/backend that can expose metric observation operations such as `prometheus_query`.
- SSH is not one tool; it is a provider/backend family that can expose operations such as `ssh_exec`, `sftp_read`, `sftp_write`, `sshfs_mount`, and remote file inspection.
- Filesystem access is a capability area with operations such as `list_dir`, `read_file`, `stat_file`, and `grep_file`, plus parsers such as `parse_json`, `parse_yaml`, and `parse_logs`.
- STT, TTS, video, and sensor input are operations under broader capabilities such as `hear_human`, `speak_human`, and `observe_video`.

Current naming mismatch to interpret carefully:

- `ToolNeed` often means “CapabilityNeed” in practice.
- `ToolRegistry` is closer to a registered callable operation inventory.
- `CapabilityCatalog` is the cognitive recommendation and handoff layer.
- `ToolExecutor` executes registered operation implementations.
- `RuntimeTool` is an in-memory `RuntimeLoop` handler shape, not the entire tool model.

## Core objects

### Event

An immutable record of something that happened.

Examples:

- user message
- model decision
- observation ingested
- handoff plan proposed
- policy blocked action
- tool need created
- toolkit generated
- validation failed
- generated toolkit artifacts

Fields:

```json
{
  "id": "evt_...",
  "kind": "user_message",
  "workspace_id": "ws_...",
  "session_id": "ses_...",
  "actor": "user|model|system|tool|builder|approver",
  "timestamp": "...",
  "payload": {},
  "causation_id": "evt_...",
  "correlation_id": "goal_..."
}
```

### Workspace

A durable boundary for state, tools, policies, and users.

Use workspaces instead of global state.

### Session

A conversation or interaction thread. Sessions are not the source of truth; they are a lens over events.

### Goal

A user or system objective that may span multiple events.

Examples:

- “make node-1 accessible over SSH”
- “figure out why Docker storage is full”
- “prepare a deployment checklist”

Fields:

```json
{
  "id": "goal_...",
  "summary": "Make node-1 accessible over SSH",
  "status": "active|blocked|complete|abandoned",
  "workspace_id": "ws_...",
  "created_from_event_id": "evt_...",
  "facts": {},
  "open_questions": [],
  "related_entities": []
}
```

### Entity

A thing the system knows about.

Examples:

- host
- service
- repository
- database
- user
- environment
- cloud account
- ticket

Fields:

```json
{
  "id": "ent_...",
  "kind": "host",
  "name": "node-1",
  "aliases": ["node1"],
  "attributes": {},
  "confidence": 0.95
}
```

### Fact

A claim about an entity or goal, with freshness and provenance.

```json
{
  "id": "fact_...",
  "subject_id": "ent_node_1",
  "predicate": "ssh.service.running",
  "value": false,
  "source_event_id": "evt_...",
  "evidence_ids": ["evid_..."],
  "source_type": "provider",
  "observed_at": "...",
  "expires_at": "...",
  "confidence": 0.8
}
```

Facts should be explicit about staleness and provenance. The context engine should prefer fresh, high-confidence facts and label stale ones.

Fact `source_type` values are `user`, `discovery`, `provider`, `inferred`, or `imported`, with default confidence scores of 0.90, 0.95, 0.85, 0.60, and 0.70 respectively. Inferred facts are marked with `source_type: "inferred"` and their confidence cannot exceed the confidence of the source fact.

Facts may be derived from one or more Evidence records. Facts are projected interpretations of Evidence, not raw observations.

### Evidence

Raw observations that may support Facts.

Examples:

- Prometheus query result
- Prometheus read result
- Ansible inventory parse result
- local host observation
- API response
- User statement
- Documentation excerpt
- Wikidata record

Fields:

```json
{
  "id": "evid_...",
  "source": "prometheus",
  "observed_at": "...",
  "payload": {},
  "confidence": 0.95
}
```

Evidence is immutable. Facts may be extracted, aggregated, revised, expired, or superseded as interpretations of one or more Evidence records. Validation-like checks are represented as additional evidence-backed Facts, not as a separate verified flag.


### Fact Support

A projected aggregate for one claim value. FactSupport is not appended as authoritative truth; it is rebuilt from Facts.

```json
{
  "subject": "host:node-1",
  "predicate": "ssh.running",
  "value": true,
  "supporting_fact_ids": ["fact_provider_1", "fact_discovery_2"],
  "source_types": ["provider", "discovery"],
  "confidence": 0.94,
  "observed_at": "2026-06-03T10:00:00Z",
  "latest_observed_at": "2026-06-03T10:05:00Z"
}
```

Terminology:

- **Observed fact**: extracted from direct input, provider output, discovery, or imported records.
- **Inferred fact**: deterministically derived from other Facts and treated as weaker support.
- **Supporting fact**: same subject, predicate, and value.
- **Conflicting fact**: same subject and predicate with a different value.
- **Best fact/current belief**: the representative Fact for the value with the strongest aggregate support, confidence, provenance, and recency.

Seed preserves provenance through `supporting_fact_ids` and Evidence IDs. It should not collapse provenance into `verified: true`.


### ProjectionStore

A deterministic cache of current projected state. `EventLedger` owns append-only events; `ProjectionStore` owns rebuildable projections such as current facts, FactSupport aggregates, measurement samples, identity/alias indexes, entity types, relationships/topology, graph validation issues, and explanation inputs. It is cache, not source of truth. The current SQLite backing should stay portable to Postgres by keeping projection rebuilds deterministic and avoiding SQLite-only semantics in domain logic.

### Capability

Something an entity can have or satisfy.

Examples:

- `ssh_access`
- `docker_storage_observable`
- `package_install_allowed`
- `repository_readable`

Capabilities are conceptual. They are not necessarily executable.

Fields:

```json
{
  "name": "ssh_access",
  "summary": "Host accepts SSH login with approved credentials.",
  "entity_kinds": ["host"],
  "support_observation": {
    "preferred_operation": "ssh.observe"
  }
}
```

### CapabilityCatalog Entry

A registered capability and provider handoff description visible to the runtime.

A catalog entry has a typed contract, policy metadata, and provider/backend references. It is not an instruction for Seed to execute.

Fields:

```json
{
  "name": "ssh_access",
  "summary": "Host accepts SSH login with approved credentials.",
  "toolkit_id": "tk_ssh_access",
  "backend_types": ["ansible", "manual"],
  "operations": ["ssh.verify", "ssh.install"],
  "target_schema": {},
  "policy_action": "ssh.install",
  "provider_refs": ["awx:ssh-access-template", "runbook:ssh-access"],
  "status": "registered",
  "visibility": "model_visible"
}
```

### Toolkit

A package containing related capability metadata, schemas, policy metadata, tests, docs, and optional integration contracts.

Examples:

- `ssh_access`
- `linux_packages`
- `docker_observability`
- `git_repository`
- `ticketing_jira`

A toolkit can be hand-written or generated.

### Tool Need

A durable request for a missing capability or provider handoff target.

This is one of the most important objects in Seed. It records what capability is missing without inventing internal execution.

```json
{
  "id": "need_...",
  "name": "install_ssh_server",
  "summary": "Install and start OpenSSH server on a host.",
  "capability": "ssh_access",
  "reason": "User asked to make node-1 accessible over SSH, but no install tool exists.",
  "requested_by_event_id": "evt_...",
  "risk_hint": "mutating",
  "status": "proposed|accepted|generating|generated|validating|validated|registered|rejected",
  "desired_inputs": ["host"],
  "desired_outputs": ["installed", "service_status", "supporting_evidence"]
}
```

### Action Plan (legacy/experimental; quarantined from Core MVP)

A durable, text-only, non-executable plan for satisfying a ToolNeed or user goal.

ActionPlans are legacy/experimental planning artifacts retained for historical projection and explicit CLI side paths. They are not part of the current Core MVP runtime path, are not routed by canonical Runtime decisions, and are not runbooks that Seed executes.

Fields:

```json
{
  "id": "plan_...",
  "tool_need_id": "need_...",
  "provider": "awx-prod",
  "capability": "ssh_access",
  "summary": "Use AWX to install and start OpenSSH on node-1.",
  "steps": ["Confirm host target", "Launch AWX job template", "Review provider result"],
  "risk_class": "L3",
  "requires_approval": true,
  "status": "proposed",
  "executable": false
}
```

### Toolkit Candidate

An untrusted generated toolkit awaiting validation.

Fields:

```json
{
  "id": "cand_...",
  "tool_need_id": "need_...",
  "artifact_path": "builder_out/cand_...",
  "generator": "seed-builder-v1",
  "status": "generated|validation_failed|validated|rejected",
  "validation_report_id": "val_..."
}
```

### Policy Action

A named action evaluated by policy.

Examples:

- `ssh.verify`
- `ssh.install`
- `package.install`
- `file.read`
- `service.restart`
- `toolkit.register`

Policy actions should be stable and boring.

### Approval

A durable permission decision for a specific action, scope, and actor.

```json
{
  "id": "appr_...",
  "action": "ssh.install",
  "scope": "ent_node_1",
  "approved_by": "user_...",
  "expires_at": "...",
  "constraints": {
    "tool": "install_ssh_server",
    "host": "node-1"
  }
}
```


### HandoffPlan (legacy/experimental; quarantined from Core MVP)

A non-executable provider handoff derived from an accepted legacy Action Plan or other validated planning path. HandoffPlans are retained for historical projection and explicit CLI side paths, but they are quarantined from the current Core MVP. The Core MVP stops at ToolNeed, capability_resolution, registered operation candidates, and provider/handoff recommendations.

Seed does not run a HandoffPlan. It does not prompt for credentials, hold secrets, retry, schedule, or monitor long-running work. External systems own those responsibilities.

A HandoffPlan is explicitly **not** an approval. It does not imply user approval, execution authorization, credential availability, provider trust, or tool registration. `requires_external_approval` records that the external backend or operator must still approve the handoff before execution; it is not an approval grant.

Fields:

```json
{
  "id": "handoff_...",
  "action_plan_id": "plan_...",
  "provider": "awx-prod",
  "backend_type": "ansible",
  "operation": "ssh.install",
  "target": "host:node-1",
  "policy_summary": "Requires operator approval in AWX before host package/service changes. This is not a Seed approval grant.",
  "secret_boundary": "Credentials, become prompts, retries, and job lifecycle stay in AWX/Vault/ssh-agent; Seed stores no secrets.",
  "requires_external_approval": true,
  "executable": false
}
```

`backend_type` is one of:

- `ansible` — host automation through Ansible/AWX.
- `mcp` — tool integration through an MCP server.
- `temporal` — workflow handoff through Temporal or Prefect-style orchestration.
- `manual` — human/operator runbook handoff.

Required fields:

- `action_plan_id`
- `provider`
- `backend_type`
- `operation`
- `target`
- `policy_summary`
- `secret_boundary`
- `requires_external_approval`
- `executable: false`

### ExecutionProposal (experimental)

`ExecutionProposal` is experimental/legacy and is not part of Seed's core path. It may be useful as a research object for concrete-call shaping or historical compatibility, but the architecture must not depend on it for execution lifecycle, credentials, retries, scheduling, long-running jobs, ToolNeed, capability_resolution, or Runtime routing.

### Execution Authorization (experimental)

`ExecutionAuthorization` is experimental/legacy and is not part of Seed's core path. It does not grant credentials and should not be treated as permission for Seed to execute anything. The Core MVP path is ToolNeed -> capability_resolution -> registered operation candidates -> provider/handoff recommendations.

Passwords, passphrases, raw tokens, private keys, and other secrets are never stored in Action Plans, HandoffPlans, durable Approvals, experimental Execution Authorizations, event payloads, CLI arguments, models, or the database. Credential material belongs to external systems such as Ansible/AWX prompts, Vault, ssh-agent, sudo/become flows, MCP server configuration, Temporal/Prefect workers, or manual operator procedures.


### Decision

Structured output from a model.

Possible kinds:

- `answer`
- `ask_question`
- `request_tool`
- `propose_state_patch`
- `refuse`

Example:

```json
{
  "kind": "request_tool",
  "reason": "No registered capability/backend handoff can install SSH on the host.",
  "tool_need": {
    "name": "install_ssh_server",
    "capability": "ssh_access",
    "summary": "Install and start SSH server on a Linux host.",
    "risk_hint": "mutating"
  }
}
```

## Object relationships

```text
Workspace
  has many Sessions
  has many Events
  has many Goals
  has many Entities
  has many Facts
  has many Toolkits
  has many ToolNeeds
  has one or more CapabilityCatalog views
  may project legacy ActionPlans/HandoffPlans for historical compatibility

Event
  may create Goal
  may update Fact
  may request ToolNeed
  may record external provider Evidence
  may project legacy planning/handoff events for historical compatibility

ToolNeed
  may create Toolkit Candidate
  may become CapabilityCatalog metadata
  may produce capability_resolution and provider/handoff recommendations

Legacy HandoffPlan
  references legacy ActionPlan
  remains projection/CLI compatibility only
  never implies approval, execution authorization, credentials, provider trust, or tool registration
  is always executable: false
```

## Lifecycle summaries

### Tool Need lifecycle

```text
proposed
  -> accepted
  -> generating
  -> generated
  -> validating
  -> validated
  -> registered
```

Failure paths:

```text
proposed -> rejected
generated -> validation_failed
validated -> rejected
registered -> deprecated
```

### Capability metadata lifecycle

```text
draft
  -> generated
  -> validated
  -> registered in CapabilityCatalog
  -> visible for provider/handoff recommendations
  -> deprecated
```

### Goal lifecycle

```text
active
  -> waiting_for_user
  -> waiting_for_tool
  -> waiting_for_approval
  -> complete
  -> abandoned
```

## Naming rules

Use:

- Event
- Goal
- Entity
- Fact
- Capability
- Tool
- Toolkit
- Tool Need
- Policy Action
- Approval
- Action Plan (legacy/experimental only)
- HandoffPlan (legacy/experimental only)
- Decision
- Context Packet

Avoid in the new repo:

- gateway
- provider operation
- chain
- requirement, unless describing an external business requirement
- remediation as a core abstraction
- intent as the durable object; use Decision for model output and Goal for user objective

## Why these names

The old system mixed execution implementation, provider metadata, and user intent. These new names keep the mental model simple:

- **Events** happened.
- **State** is projected.
- **Context** is composed.
- **Decisions** are proposed.
- **Capabilities** are registered in the CapabilityCatalog.
- **ToolNeeds** are missing capabilities.
- **ActionPlans** are legacy/experimental non-executable plans retained outside Core MVP routing.
- **HandoffPlans** are legacy/experimental provider handoff records retained outside Core MVP routing with `executable: false`.
- **Toolkits** package capability metadata and integration contracts.
- **Policy** supplies auditable metadata and constraints for registered operation candidates and provider/handoff recommendations.

## Entity relationships

An `EntityRelationship` is a deterministic, directed semantic edge derived from a
fact through `RelationshipCatalog`. It records its subject, relationship, object,
source fact ID, source type, confidence, observation time, metadata, and a
`relationship_kind` (`identity`, `topology`, `dependency`, `hosting`, or `grouping`).
The kind controls graph traversal semantics: dependency queries traverse dependency
and hosting edges, but not identity or grouping edges. It is preserved during
projection so future reasoning can distinguish the meaning of otherwise similar
edges. Facts remain the source of truth; relationship projection does not replace
fact retention, support aggregation, or alias resolution.
