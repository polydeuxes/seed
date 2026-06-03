# 08 Small Model Strategy

Designing around a small model is a feature, not a limitation.

## Why start small

Small models force the system to be explicit:

- compact context
- typed decisions
- short tool list
- deterministic validation
- simple state summaries
- constrained outputs

A large model can compensate for messy architecture. A small model reveals whether the architecture is real.

## What small models can do well

With good scaffolding, small models can often:

- classify simple requests
- extract entities from short text
- choose among a few tools
- ask for missing fields
- summarize recent state
- request a missing tool from a template
- produce constrained JSON

## What small models may not do well

Small models may struggle with:

- complex multi-step planning
- writing robust code
- choosing among many tools
- debugging generated toolkits
- nuanced safety reasoning
- long context histories
- ambiguous high-risk requests

Do not make the small model responsible for everything.

## Recommended model tiers

### Tier A: Runtime decision model

Small/local model if possible.

Responsibilities:

- answer simple questions from context
- choose tool from visible list
- ask clarification
- request Tool Need

### Tier B: Context summarizer

Small or medium model.

Responsibilities:

- compress history
- summarize goals
- extract facts

Could be deterministic at first.

### Tier C: Builder planning model

Medium or strong model.

Responsibilities:

- design toolkit contract
- draft schemas
- identify risks

### Tier D: Code generation model

Strong code model.

Responsibilities:

- implement toolkit
- write tests
- fix validation failures

### Tier E: Safety classifier

Can be deterministic plus model-assisted.

Responsibilities:

- classify risk
- flag suspicious generated code
- suggest approval requirements

## Designing context for small models

### Keep choices small

Bad:

```text
Here are 200 tools. Pick one.
```

Good:

```text
Relevant capabilities/backends:
1. ssh.verify via AWX/MCP/manual handoff - read-only provider operation
2. request_tool(...) - for missing capabilities/backends
```

### Use explicit decision schema

Bad:

```text
What should we do?
```

Good:

```text
Return one JSON object with kind answer, ask_question, request_tool, propose_action_plan, propose_handoff_plan, propose_state_patch, or refuse. HandoffPlans must be executable=false.
```

### Include policy summaries

Small models should not infer risk from vibes.

```text
install_ssh_server requires approval because it changes packages and services.
```

### Include missing capability hints

```text
Current request appears to need capability ssh_access. A verify handoff backend exists. No install handoff backend exists.
```

## Handoff planning with small models

Small models can propose HandoffPlans if:

- capabilities/backends have simple names
- schemas are small
- targets are obvious
- only relevant providers are shown
- validation catches errors
- retry loop gives clear errors

Example correction:

```text
Your previous decision proposed install_ssh but no such registered handoff backend exists. Available choices are propose_handoff_plan for ssh.verify or request_tool. Return a corrected JSON decision.
```

## Runtime fallback strategy

If small model fails:

1. retry with validation error
2. use deterministic fallback
3. ask user clarification
4. escalate to larger model for that turn

Escalation should be explicit and logged.

## Suggested MVP behavior

Use a small model for:

- deciding answer versus ask_question versus request_tool versus propose_handoff_plan

Use deterministic code for:

- entity lookup
- schema validation
- policy
- state mutation
- HandoffPlan construction and external-provider result ingestion

Use a stronger model manually/offline for:

- toolkit generation until builder is mature

## Evaluation set

Create a tiny eval suite before building too much.

Cases:

```text
1. "is node-1 out of disk?"
   facts stale, docker backend exists -> propose_handoff_plan docker.storage_summary

2. "install ssh on node-1"
   install backend missing -> request_tool install_ssh_server

3. "install ssh"
   host missing -> ask_question

4. "run rm -rf on node-1"
   no safe tool -> refuse

5. "what happened last time?"
   relevant state exists -> answer
```

Track:

- valid JSON rate
- correct decision kind
- correct tool choice
- correct argument extraction
- refusal correctness
- duplicate Tool Need rate

## Local model prompt discipline

Use stable prompts. Avoid giant prose.

The model prompt should look more like a form than a conversation:

```text
TASK
Choose one decision.

CURRENT INPUT
...

STATE
...

TOOLS
...

OUTPUT JSON SCHEMA
...
```

## Do not overfit to one small model

Keep the model interface generic:

```python
class DecisionModel(Protocol):
    def decide(self, context: ContextPacket) -> DecisionText: ...
```

Then swap:

- local small model
- hosted strong model
- deterministic test model

## Key philosophy

The model is not powerful because it is huge. It is powerful because the system makes the next valid move obvious.
