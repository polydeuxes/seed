# 05 Policy and Safety

Policy is the boundary between desire and execution.

## Core rule

A user or model can desire an action. Only policy can allow execution.

```text
desire -> decision -> validation -> policy -> execution
```

Never:

```text
desire -> execution
```

## Risk levels

Use a simple risk taxonomy first.

### L0: Local metadata

No external system access. No sensitive data.

Examples:

- list registered tools
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
  "scope": "host:node-1",
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
- tool
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

Avoid implementation-specific names in policy. Policy names describe effects.


## Plan approval vs execution authorization

Action Plan approval is plan acceptance only. It records that a user or
approver accepts the proposed plan text and lifecycle state; it does not grant
credentials, does not authorize a specific mutating tool call, and does not
permit credential reuse.

Execution authorization is separate and just in time:

- low-risk, read-only plans may satisfy readiness with `action_plan.approved`
  / `approval_present`;
- mutating or privileged plans require `execution_authorization_present`;
- each `execution_authorization.granted` is bound to one `action_plan_id`, one
  concrete proposed tool/action call, and a fingerprint of the proposed
  arguments;
- it is short-lived and secret-free; persisted state must not contain
  passwords, tokens, private keys, or raw credential/session material.

Credential/session grants are host-environment resources, not Seed state. They
are supplied just in time for the exact authorized attempt, referenced only by a
secret-free grant identifier when needed, and never persisted by Seed.

## Approval model

Approval is scoped and expiring.

Example:

```json
{
  "action": "ssh.install",
  "tool": "install_ssh_server",
  "scope": "host:node-1",
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

Generated mutating tools should start disabled or approval-only.

## Sandbox expectations

Generated code should run with:

- timeout
- memory limits
- network restrictions
- filesystem restrictions
- no raw environment access
- no direct secrets access
- controlled provider facades
- structured logging

## Forbidden shortcuts

Never allow:

- arbitrary shell as a generic model tool
- generated code self-registration
- generated code editing policy
- generated code accessing raw secrets
- model-supplied implementation references
- importing unregistered modules as tools
- policy decisions generated solely by the model

## Tool call safety sequence

```python
def safe_tool_call(tool_name, args):
    tool = registry.require_registered(tool_name)
    typed_args = schema.validate(tool.input_schema, args)
    policy = policy_gate.evaluate(tool.policy_action, typed_args.scope)

    if policy.decision == "block":
        return blocked(policy)

    if policy.decision in {"confirm", "approve"}:
        return request_approval(policy, tool, typed_args)

    return executor.invoke(tool, typed_args)
```

## Tool generation safety sequence

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
- action allowed
- action blocked
- approval requested
- approval granted
- approval denied
- tool call started
- tool call completed
- tool call failed
- toolkit generated
- toolkit validation failed
- toolkit registered

## Defense in depth

Even though policy gates execution, provider facades may still enforce low-level safety. This is acceptable if it prevents bypasses. But keep policy source-of-truth in the policy service, not scattered in provider code.

## Human-readable policy summaries

The context packet should not include giant policy tables. It should include relevant summaries:

```json
{
  "tool": "install_ssh_server",
  "policy_summary": "Requires operator approval before changing host packages or services."
}
```

## Model instructions about policy

The model should be told:

- You may propose actions.
- You may not claim an action has run unless a tool result says so.
- If policy requires approval, explain what approval is needed.
- If a tool is missing, request a Tool Need instead of inventing execution.

## Policy as product UX

Policy blocks should be useful, not dead ends.

Bad:

```text
Blocked.
```

Good:

```text
Installing SSH changes host node-1, so I need operator approval. I can create an approval request for install_ssh_server(host=node-1), or I can first run the read-only verify_ssh_access check.
```
