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
  "observed_at": "...",
  "expires_at": "...",
  "confidence": 0.8
}
```

Facts should be explicit about staleness. The context engine should prefer fresh facts and label stale ones.

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
    "preferred_tool": "verify_ssh_access"
  }
}
```

### Tool

A registered executable operation visible to the runtime.

A tool has a typed contract and an implementation reference.

Fields:

```json
{
  "name": "verify_ssh_access",
  "summary": "Verify whether SSH is reachable on a host.",
  "toolkit_id": "tk_ssh_access",
  "input_schema": {},
  "output_schema": {},
  "policy_action": "ssh.verify",
  "implementation": "toolkits.ssh_access.operations:verify_ssh_access",
  "status": "registered",
  "visibility": "model_visible"
}
```

### Toolkit

A package containing related tools, schemas, policy metadata, tests, and docs.

Examples:

- `ssh_access`
- `linux_packages`
- `docker_observability`
- `git_repository`
- `ticketing_jira`

A toolkit can be hand-written or generated.

### Tool Need

A durable request for a missing tool or capability.

This is one of the most important objects in Seed.

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


### Execution Authorization

`action_plan.approved` means the human accepted the durable text plan. It is
not credential approval and it is not permission to run an arbitrary future
tool call. Privileged or mutating work needs a separate
`execution_authorization.granted` event for each concrete execution attempt.

Execution authorizations are short-lived and bind all of the following:

- the `action_plan_id` that was accepted;
- the proposed concrete tool/action name;
- a deterministic fingerprint of the exact proposed arguments;
- secret-free grant metadata for any just-in-time external prompt, agent, sudo
  timestamp, or vault reference.

Example:

```json
{
  "id": "auth_...",
  "action_plan_id": "plan_...",
  "tool_name": "restart_container",
  "arguments_fingerprint": "sha256:...",
  "granted_by": "operator@example.com",
  "expires_at": "2026-06-03T15:05:00Z",
  "interactive_prompt": true,
  "ssh_agent": "SSH_AUTH_SOCK",
  "sudo_timestamp": "host-sudo-cache",
  "external_vault_token_ref": "vault://seed/jit/session-ref",
  "secret_seen_by_seed": false
}
```

Passwords, passphrases, raw tokens, private keys, and other secrets are never
stored in Action Plans, durable Approvals, Execution Authorizations, event
payloads, CLI arguments, models, or the database. Execution Authorization may
store only these secret-free grant metadata fields: `interactive_prompt`,
`ssh_agent`, `sudo_timestamp`, and `external_vault_token_ref`; it must also
record `secret_seen_by_seed: false`. Any credential material must be supplied
just in time by the host environment for the exact authorized attempt and
discarded outside Seed's persistent state. The preferred privileged execution
path is an external prompt or agent such as Ansible's `become` prompt, an
SSH agent, sudo's host-managed timestamp cache, or an external vault reference.

### Decision

Structured output from a model.

Possible kinds:

- `answer`
- `ask_question`
- `call_tool`
- `request_tool`
- `propose_state_patch`
- `refuse`

Example:

```json
{
  "kind": "request_tool",
  "reason": "No registered tool can install SSH on the host.",
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
  has many Tools
  has many Tool Needs

Event
  may create Goal
  may update Fact
  may request Tool Call
  may request Tool Need
  may record Tool Result

Tool Need
  may create Toolkit Candidate
  may become Toolkit
  may register Tools

Tool
  belongs to Toolkit
  has Policy Action
  has Implementation
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

### Tool lifecycle

```text
draft
  -> generated
  -> validated
  -> registered
  -> visible
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
- **Tools** are registered.
- **Tool Needs** are missing tools.
- **Toolkits** package tools.
- **Policy** gates action.
