# 06 Context Engine

The context engine is the core product component.

## Purpose

The context engine turns durable state into a compact, useful model-facing packet.

It answers:

- What is the user asking now?
- What goal is active?
- What facts matter?
- What is missing?
- What tools are available?
- What tools are blocked?
- What tools do not exist yet?
- What decisions may the model make?

## Context packet shape

```json
{
  "packet_id": "ctx_...",
  "workspace": {
    "id": "ws_...",
    "name": "default"
  },
  "trigger": {
    "event_id": "evt_...",
    "text": "can you install ssh on node-1?"
  },
  "active_goal": {
    "id": "goal_...",
    "summary": "Make node-1 accessible over SSH",
    "status": "active"
  },
  "entities": [
    {
      "id": "ent_node_1",
      "kind": "host",
      "name": "node-1",
      "confidence": 0.98
    }
  ],
  "facts": [
    {
      "subject": "node-1",
      "predicate": "ssh.service.running",
      "value": false,
      "freshness": "stale",
      "observed_at": "2026-06-01T12:00:00Z"
    }
  ],
  "available_tools": [],
  "relevant_blocked_tools": [],
  "open_tool_needs": [],
  "missing_capabilities": [
    {
      "capability": "ssh_access",
      "reason": "No registered tool can install SSH."
    }
  ],
  "policy_notes": [],
  "decision_schema": "DecisionV1"
}
```

## Context sources

Context composer pulls from:

- current input event
- recent session events
- active goal
- relevant entities
- facts about entities
- available capabilities and handoff backends
- open tool needs
- approval state
- toolkit registry
- policy summaries
- previous failed decisions

The context engine should stay focused on selecting and composing relevant state for the model. Knowledge acquisition, evidence capture, fact extraction, and fact validation belong to the knowledge and evidence system.

## Knowledge classes

Not all knowledge should be treated equally. Seed should distinguish between:

1. Operational knowledge
2. Structured knowledge
3. Retrieved knowledge
4. Derived knowledge
5. User-supplied knowledge

### Operational knowledge

Produced by tools observing real systems.

Examples:

- Prometheus metrics
- SSH inspection
- Docker status
- Home Assistant state
- Cloud APIs

Operational knowledge has the highest priority for infrastructure decisions because it reflects the current environment.

Examples:

- node210 disk usage
- container health
- service status

### Structured knowledge

Produced by curated knowledge systems.

Examples:

- Wikidata
- local knowledge graphs
- internal inventories
- CMDB records

Structured knowledge is useful for stable or curated facts such as:

- capital cities
- chemical properties
- astronomical values
- historical dates

### Retrieved knowledge

Information retrieved from documents.

Examples:

- documentation
- wiki pages
- RFCs
- README files

Retrieved knowledge should be treated as evidence rather than direct fact.

### Derived knowledge

Generated from reasoning over facts.

Examples:

- root-cause hypotheses
- capacity forecasts
- risk assessments

Derived knowledge should always record supporting evidence.

### User-supplied knowledge

Claims made by users.

Examples:

- "My server is down."
- "Node210 is the registry."

User statements are evidence until supported or disputed by additional observed Facts; Seed preserves provenance rather than stamping them `verified`.

## Context budget

Design for small models first. Keep context short and structured.

Suggested budget:

```text
system rules:        500-1000 tokens
current input:       100-500 tokens
state summary:       500-1500 tokens
facts:               500-1500 tokens
available capabilities:     500-2000 tokens
decision schema:     500-1000 tokens
```

Target: under 6k tokens for normal interactions.

## Context sections

### 1. Role and rules

Tell the model what it can do.

```text
You are Seed's decision model. You do not execute actions directly, ask for credentials, or manage retries/schedules/jobs. You produce one structured decision: answer, ask_question, request_tool, propose_action_plan, propose_handoff_plan, propose_state_patch, or refuse. HandoffPlans must include requires_external_approval and executable=false, and must not imply approval or credentials.
```

### 2. Current input

Include exact text or payload.

### 3. Current state summary

Short summary of active goal and relevant prior state.

### 4. Relevant entities

Only include entities likely relevant to the current input.

### 5. Facts

Include facts with freshness.

Use labels:

- `fresh`
- `recent`
- `stale`
- `expired`
- `conflicting`

### 6. Tools

Show only relevant tools, not entire registry.

Include:

- name
- summary
- required args
- risk/approval summary
- when to use

### 7. Open Tool Needs

Show existing Tool Needs so the model does not duplicate them.

### 8. Decision schema

Provide exact output format.

## Tool visibility selection

```python
def visible_tools(state, goal, entities, user):
    candidates = registry.tools_for_entity_kinds(entity.kind for entity in entities)
    candidates += registry.tools_for_capabilities(goal.missing_capabilities)
    candidates = relevance_ranker.rank(candidates, goal, state.current_input)
    return [summarize_tool(tool, user, state) for tool in candidates[:MAX_TOOLS]]
```

## Fact selection

```python
def relevant_facts(state, entities, goal):
    facts = []
    for entity in entities:
        facts.extend(state.facts.for_entity(entity.id))
    facts.extend(state.facts.for_goal(goal.id))
    facts = rank_by_relevance_and_freshness(facts)
    return facts[:MAX_FACTS]
```

## Missing capability detection

This can be deterministic, model-assisted, or both.

Examples:

```text
Input: "install ssh on node-1"
Known capability: ssh_access
Available tools: verify_ssh_access
Missing tool: install_ssh_server
```

The context packet should say:

```json
{
  "missing_capabilities": [
    {
      "capability": "ssh_access",
      "missing_tool_kind": "installer",
      "suggested_tool_need": "install_ssh_server"
    }
  ]
}
```

## Context packet should be stored

Record the context packet or a hash plus reproducible references.

Why:

- debug model decisions
- reproduce failures
- evaluate prompts
- compare model versions

## Prompt template

```text
You are Seed's decision model.

Rules:
- Produce exactly one JSON decision.
- Do not claim external work has run unless provider Evidence is in context.
- If a required capability/backend is missing, request_tool.
- If arguments are missing for a risky action, ask_question.
- If a backend requires approval, propose a HandoffPlan with requires_external_approval=true; do not imply approval has been granted.
- Never invent provider/backend names outside available capabilities unless using request_tool.

Current input:
{{trigger.text}}

Active goal:
{{goal.summary}}

Relevant state:
{{state_summary}}

Entities:
{{entities}}

Facts:
{{facts}}

Available tools:
{{available_tools}}

Open tool needs:
{{open_tool_needs}}

Allowed decision schema:
{{decision_schema}}
```

## Decision schema in context

Short form for model:

```json
{
  "kind": "answer|ask_question|request_tool|propose_action_plan|propose_handoff_plan|propose_state_patch|refuse",
  "reason": "string",
  "message": "string for answer",
  "question": "string for ask_question",
  "tool_need": "object for request_tool",
  "action_plan": "non-executable object for propose_action_plan",
  "handoff_plan": "provider handoff object with requires_external_approval and executable=false",
  "patches": "array for propose_state_patch",
  "safe_alternative": "string for refuse"
}
```

Use strict schema validation outside the model.

## Evaluation cases

Create golden cases:

1. User asks to check known host with fresh fact -> answer.
2. User asks to check known host with stale fact and provider exists -> propose_handoff_plan.
3. User asks to install SSH and install backend missing -> request_tool.
4. User asks to install SSH and backend exists but needs approval -> propose_handoff_plan with policy summary.
5. User asks vague action without host -> ask_question.
6. User asks arbitrary shell -> refuse or request_tool, not internal execution.

## Context engine anti-patterns

Avoid:

- dumping raw event history
- showing every registered tool
- hiding policy requirements
- omitting freshness
- letting prompt text be the only schema
- treating model memory as durable memory
- allowing model to invent facts
