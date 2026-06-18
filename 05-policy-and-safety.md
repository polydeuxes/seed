# 05 Policy and Safety

Policy is the boundary between desire and an operation call or external-provider handoff.

## Core rule

A user or model can desire an action. Policy metadata determines whether Seed may call an allowed registered operation or recommend a non-executable handoff, but mutating execution remains outside Seed.

```text
desire -> decision -> validation -> policy metadata -> registered operation or HandoffPlan(executable=false) -> provider boundary
```

Never:

```text
desire -> Seed execution
```

## Risk levels

Use a simple risk taxonomy first.

### L0: Local metadata

No external system access. No sensitive data.

Examples:

- list registered capabilities
- show toolkit docs
- inspect local manifest

Default: allowed.

### L1: Read-only observation

Reads non-sensitive operational state.

Examples:

- check service status
- query storage usage
- verify port open

Default: allowed for trusted workspace users.

### L2: Sensitive read or broad discovery

Reads sensitive data, broad inventory, logs, secrets-adjacent metadata, or external APIs.

Examples:

- query production monitoring broadly
- read application logs
- enumerate cloud resources

Default: may require confirmation or role check.

### L3: Mutating action

Changes remote systems or durable external state.

Examples:

- install package
- restart service
- open firewall
- create ticket
- update config

Default: approval required.

### L4: Destructive or privilege-changing action

Can destroy data, change access, escalate privileges, or create persistent security exposure.

Examples:

- delete database
- rotate credentials
- grant admin
- disable firewall
- run arbitrary shell

Default: blocked unless specifically approved by policy and human workflow.

## Policy decision values

Policy returns one of:

- `allow`
- `confirm`
- `approve`
- `block`

```json
{
  "decision": "approve",
  "action": "ssh.install",
  "risk": "L3",
  "reason": "Installing packages changes host state and requires approval.",
  "scope": "host:example_host",
  "required_approval": {
    "role": "operator",
    "expires_in_minutes": 30
  }
}
```

## Policy inputs

Policy should evaluate:

- action
- risk
- actor
- workspace
- operation/tool name
- toolkit
- scope entity
- environment
- current approval grants
- time
- arguments
- generated/core origin

## Policy action naming

Use stable dotted names:

```text
ssh.verify
ssh.install
service.restart
package.install
file.read
file.write
toolkit.generate
toolkit.validate
toolkit.register
tool.call
```

Avoid implementation-specific names in policy. Policy names describe effects; `tool.call` remains legacy event/action vocabulary for registered operation calls.


## Legacy plan approval vs external-provider recommendations

ActionPlan approval, HandoffPlan materialization, ExecutionProposal, and ExecutionAuthorization are quarantined legacy/experimental side paths. They may be retained for historical projection and explicit CLI inspection, but they are not the current Core MVP path and must not be used to build internal workflow execution, authorization workflows, or action-plan orchestration.

The Core MVP policy path is:

```text
ToolNeed
-> capability_resolution
-> registered operation candidates
-> provider/handoff recommendations
```

Provider/handoff recommendation metadata may summarize external approval and secret boundaries, but it is not a Seed approval object and does not imply execution authorization, credential availability, provider trust, operation registration, retries, scheduling, or long-running job ownership.

Credential/session grants are external-provider resources, not Seed state. They are supplied just in time by systems such as Ansible/AWX, Vault, ssh-agent, sudo/become flows, MCP server configuration, Temporal/Prefect workers, or manual operator procedures. Seed never persists passwords, passphrases, raw tokens, private keys, raw credential/session material, or credential prompts.


## Approval model

Approval is scoped and expiring.

Example:

```json
{
  "action": "ssh.install",
  "capability": "ssh_access",
  "scope": "host:example_host",
  "approved_by": "operator@example.com",
  "expires_at": "2026-06-02T15:00:00Z",
  "constraints": {
    "package_manager": "apt",
    "start_service": true
  }
}
```

Approvals should not be broad unless intentionally designed.

## Generated toolkit safety

Generated toolkits are untrusted until validation and registration.

Policy-relevant toolkit metadata:

- origin: core/generated/imported
- validation status
- generator version
- code review status
- risk class
- required providers
- dependency list

Generated mutating capabilities should start as handoff-only and provider-controlled; generated toolkit operations are not active by default.

## Sandbox expectations

Generated capability validation should use:

- bounded validation time
- memory limits where available
- network restrictions where available
- filesystem restrictions where available
- no raw environment access
- no direct secrets access
- metadata-only provider contracts
- structured validation reports

## Forbidden shortcuts

Never allow:

- arbitrary shell as a Seed-owned operation implementation
- generated code self-registration
- generated code editing policy
- generated code or metadata accessing raw secrets
- model-supplied implementation references
- importing unregistered modules as operation implementations
- policy decisions generated solely by the model

## Handoff safety sequence

```python
def safe_handoff(action_plan, target):
    capability = capability_catalog.require(action_plan.capability)
    policy = policy_gate.summarize(capability.policy_action, target)

    if policy.decision == "block":
        return blocked(policy)

    provider = recommendation_ranker.choose_provider(capability, target)

    return HandoffPlan(
        action_plan_id=action_plan.id,
        provider=provider.name,
        backend_type=provider.backend_type,
        operation=provider.operation,
        target=target,
        policy_summary=policy.summary,
        secret_boundary=provider.secret_boundary_summary,
        requires_external_approval=policy.requires_external_approval,
        executable=False,
    )
```

## Toolkit generation safety sequence

```python
def safe_tool_generation(tool_need):
    policy = policy_gate.evaluate("toolkit.generate", scope=tool_need.id)
    if not policy.allowed:
        return blocked(policy)

    candidate = builder.generate(tool_need)
    validation = validator.validate(candidate)

    if not validation.ok:
        return rejected(validation)

    registration_policy = policy_gate.evaluate("toolkit.register", scope=candidate.id)
    if registration_policy.requires_approval:
        return awaiting_review(candidate)

    return registry.register(candidate)
```

## Audit events

Record events for:

- policy evaluated
- handoff allowed
- handoff blocked
- approval requested
- approval granted
- approval denied
- HandoffPlan created
- external provider result ingested
- external provider failure ingested
- toolkit generated
- toolkit validation failed
- toolkit registered

## Defense in depth

Even though policy gates Seed handoff recommendations, external providers must still enforce low-level safety for execution. This is acceptable and expected. Keep Seed policy metadata auditable, but do not duplicate provider credential, retry, schedule, or job lifecycle logic in Seed.

## Human-readable policy summaries

The context packet should not include giant policy tables. It should include relevant summaries:

```json
{
  "capability": "ssh_access",
  "policy_summary": "Requires operator/provider approval before changing host packages or services. This is not an approval grant.",
  "requires_external_approval": true
}
```

## Model instructions about policy

The model should be told:

- You may request ToolNeeds and summarize provider/handoff recommendation metadata; do not propose ActionPlans/HandoffPlans on the Core MVP runtime path.
- You may not claim an action has run unless external provider Evidence says so.
- If policy requires approval, explain what approval is needed in Seed or the external provider.
- If a capability/backend is missing, request a ToolNeed instead of inventing execution.
- Never ask for credentials or build retry, scheduling, or long-running job lifecycle inside Seed.

## Policy as product UX

Policy blocks should be useful, not dead ends.

Bad:

```text
Blocked.
```

Good:

```text
Installing SSH changes host example_host, so Seed can prepare a non-executable HandoffPlan for AWX with the required policy summary and secret boundary. AWX/Vault/ssh-agent handle credentials, prompts, retries, and the job lifecycle.
```
