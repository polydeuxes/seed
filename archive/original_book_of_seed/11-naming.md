# 11 Naming


This is historical/mixed naming testimony. It is not an active domain model and does not preserve HandoffPlan, Toolkit Candidate, policy route, or provider handoff architecture as current.
Names shape the architecture. Use names that describe the new system, not the legacy one.

## Candidate product/system names

### Seed

Pros:

- implies growth
- small start, larger capability over time
- fits generated toolkits
- short

### Loom

Pros:

- context threads woven into action
- good metaphor for event/state/context

Cons:

- less explicit about capability/toolkit growth

### Forge

Pros:

- strong builder metaphor

Cons:

- overemphasizes toolkit creation over context engine

### Sprout

Pros:

- playful version of Seed

Cons:

- maybe too cute

### Cortex

Pros:

- context/reasoning feel

Cons:

- generic and overloaded

Recommendation: use **Seed** for the new repo unless a better name emerges.

## Recommended component names

| Concept | Recommended name | Avoid |
|---|---|---|
| Append-only history | Event Ledger | log if ambiguous |
| Current derived view | State Projector | chain manager |
| Model-facing state | Context Composer | prompt builder only |
| Model output | Decision | intent |
| Missing capability/backend | ToolNeed | requirement |
| Capability inventory | CapabilityCatalog | registered operation list |
| External provider handoff | HandoffPlan | provider execution job |
| Capability package | Toolkit | plugin if too broad |
| Permission metadata/check | Policy Gate | guardrails only |
| Action runner | External provider | internal executor |
| Toolkit builder | Builder | self-modifier |
| Generated untrusted output | Toolkit Candidate | tool/implementation |
| External thing | Entity | resource if ambiguous |
| Claim about entity | Fact | metadata only |
| User objective | Goal | chain |

## Terms to avoid from the old repo

### Gateway

Suggests API proxy rather than context engine.

### Provider operation as product language

Too implementation-centered when it hides the capability and provider boundary. Use Capability for the abstract ability, Tool/Operation for the callable interface, Implementation for the adapter, and Provider for the external backend.

### CapabilitySpec

Okay internally, but for product language use Capability.

### Chain

Implies fixed workflow. Use Goal or Session.

### Requirement

Use Requirement for what the user or system needs accomplished. Do not use it for missing callable surfaces; use ToolNeed for durable capability gaps or missing provider handoff targets, and Capability for abstract abilities.

### Remediation

Too ops-specific. Use Plan or Action.

### Intent

Fine as a transient parse concept, but avoid as durable core object. Use Decision for model output and Goal for user objective.

## Naming conventions

### Operation/tool names

Use verbs and objects:

```text
verify_ssh_access
install_ssh_server
summarize_docker_storage
list_host_notes
create_ticket
```

### Capability names

Use nouns or states:

```text
ssh_access
docker_storage_observable
host_notes_available
repository_readable
```

### Policy actions

Use dotted effect names:

```text
ssh.verify
ssh.install
docker.storage.read
service.restart
toolkit.register
```

### Event kinds

Use dotted past-tense or domain-event names:

```text
input.user_message
model.decision.proposed
tool.call.started
tool.call.completed
tool_need.created
toolkit.candidate.generated
toolkit.registered
policy.evaluated
approval.requested
approval.granted
```

## Naming test

A name is good if a new contributor can answer:

1. Is this durable or transient?
2. Is this model-facing or internal?
3. Is this a desire, policy metadata, or external-provider handoff?
4. Is this generated or registered?
5. Does this mutate the world?

## Example language

Use:

```text
The user created a Goal. The context composer selected relevant Facts and CapabilityCatalog entries. The model produced a Decision to request a ToolNeed. The builder generated a Toolkit Candidate. Validation passed. Seed emitted a non-executable HandoffPlan for AWX with policy metadata.
```

Avoid:

```text
The gateway parsed intent into a chain and invoked a provider operation directly to satisfy a requirement.
```
