# 02 Domain Model

This document defines clean names for the new system. Avoid legacy terms that imply the old architecture.

## Core objects

### Event

An immutable record of something that happened.

Examples:

- user message
- model decision
- tool call requested
- tool call completed
- policy blocked action
- tool need created
- toolkit generated
- validation failed
- approval granted

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
- SSH command output
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

Evidence is immutable. Facts may be extracted, validated, revised, expired, or superseded as interpretations of one or more Evidence records.

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
  "verification": {
    "preferred_operation": "ssh.verify"
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
  "desired_outputs": ["installed", "service_status", "next_verification"]
}
```

### Action Plan

A durable, text-only, non-executable plan for satisfying a ToolNeed or user goal.

ActionPlans are not runbooks that Seed executes. They are auditable planning artifacts that can later be accepted, rejected, superseded, or used as the source for a non-executable HandoffPlan.

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


### HandoffPlan

A non-executable provider handoff derived from an accepted Action Plan or other validated planning path. HandoffPlans are the core execution-adjacent object: they tell a user or external provider what Seed recommends handing off, while making the boundary explicit.

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

`ExecutionProposal` is experimental and is not part of Seed's core path yet. It may be useful as a research object for concrete-call shaping, but the architecture should not depend on it for execution lifecycle, credentials, retries, scheduling, or long-running jobs. Prefer `HandoffPlan` for the current architecture.

### Execution Authorization (experimental)

`ExecutionAuthorization` is experimental and is not part of Seed's core path yet. It does not grant credentials and should not be treated as permission for Seed to execute anything. The core path is Action Plan acceptance followed by a non-executable HandoffPlan to an external provider.

Passwords, passphrases, raw tokens, private keys, and other secrets are never stored in Action Plans, HandoffPlans, durable Approvals, experimental Execution Authorizations, event payloads, CLI arguments, models, or the database. Credential material belongs to external systems such as Ansible/AWX prompts, Vault, ssh-agent, sudo/become flows, MCP server configuration, Temporal/Prefect workers, or manual operator procedures.


### Decision

Structured output from a model.

Possible kinds:

- `answer`
- `ask_question`
- `request_tool`
- `propose_action_plan`
- `propose_handoff_plan`
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
  has many ActionPlans
  has many HandoffPlans

Event
  may create Goal
  may update Fact
  may request ToolNeed
  may record ActionPlan or HandoffPlan
  may record external provider Evidence

ToolNeed
  may create Toolkit Candidate
  may become CapabilityCatalog metadata
  may produce non-executable ActionPlans

HandoffPlan
  references ActionPlan
  references provider/backend type
  records whether external approval is still required
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
  -> visible for handoff planning
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
- Action Plan
- HandoffPlan
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
- **ActionPlans** are non-executable plans.
- **HandoffPlans** describe external provider handoff with `executable: false`.
- **Toolkits** package capability metadata and integration contracts.
- **Policy** supplies auditable metadata and constraints for handoff.
