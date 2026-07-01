# Null to External Representation Transition Audit

## Executive answer

The smallest truthful repository-visible claim after `Null` is not `Observation`, `attachment`, `inquiry`, `grammar`, or a new receiving subsystem. The first supported claim is narrower:

```text
Null
↓
An external representation exists for one existing bounded repository responsibility
```

For the minimal representation `.` specifically, the repository-visible claim is even smaller:

```text
A non-empty raw inquiry note with text `.` can be preserved for the inquiry-orientation probe.
```

That claim does not justify observation truth, repository attachment, inquiry truth, grammar, ownership, responsibility recovery, or participation by every subsystem. It only permits the already implemented local responsibility that received the representation to act inside its declared boundary.

## Question audited

This audit asks:

```text
What is the first repository-visible fact after Null?
```

It intentionally starts one step before Observation:

```text
Null
  ↓
External Representation Exists
```

The boundary under review is:

```text
Null != External Representation Exists
External Representation Exists != Observation
```

The audit does not recover a new owner unless implementation demands one. It classifies the transition as one of:

- a constitutional transition;
- an existing owner responsibility;
- a local admission condition;
- unsupported.

## Implementation evidence reviewed

Representative implementation evidence:

- `seed_runtime/inquiry_orientation.py` preserves non-empty raw inquiry notes outside the event ledger and states that rendering is read-only and creates no facts, goals, tool needs, decisions, proposals, or plans.
- `seed_runtime/input_inspector.py` returns `InputArtifact` audit metadata for file bytes after bounded inspection without executing content or resolving embedded references.
- `seed_runtime/runtime.py` records runtime user input as `input.user_message` before state projection and answer production.
- `seed_runtime/context.py` carries that input event into `CURRENT_INPUT` for decision input composition without converting it into an observation.
- `seed_runtime/observations.py` defines `Observation` as a later canonical external observation shape with validation and ingestion into observation/evidence/fact events.
- `seed_runtime/ansible_inventory_source.py` demonstrates provider-specific intake: it first records an `InputArtifact`, then accepts only supported INI/YAML inventory shapes before emitting observations.
- `null_first_constitutional_transition_audit.md` and `external_representation_repository_attachment_audit.md` already found that existence-before-observation is distributed across existing responsibilities rather than centralized in a universal receiver.

## Smallest truthful claim

### General claim

The smallest repository-visible claim is:

```text
Some external representation has become available to a specific implemented responsibility.
```

This is a constitutional transition only in the weak sense that it distinguishes nothingness from present representation. It is not a constitutional grant to interpret, attach, observe, mutate, infer, plan, or route universally.

### For `.`

The representation `.` supports only:

```text
external representation exists
```

In the implemented inquiry-note path, it supports the more concrete local claim:

```text
preserved inquiry note exists with raw_note="."
```

It does not support:

```text
observation exists
attachment exists
inquiry truth exists
grammar exists
responsibility exists
participation is authorized
```

unless another implemented path adds that evidence.

## Which existing competency wakes up first?

The answer depends on which implemented entry path receives the representation.

### Operator prose / `.` path

First eligible competency:

```text
Inquiry Orientation, after inquiry-note preservation
```

Its participation is limited to read-only orientation over preserved prose and already projected state. Its boundary explicitly denies treating the note as a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction. Its related-material matching is deterministic lexical overlap only.

Therefore `.` wakes up preservation and read-only orientation only. It does not wake up observation, grammar, attachment, responsibility recovery, command execution, or semantic interpretation.

### File-backed path

First eligible competency:

```text
Input inspection
```

`InputInspector.inspect_file(...)` can hash bytes, classify a bounded prefix, preserve path/size/hash/extension/declared-purpose metadata, and emit warnings such as `empty_file`, `binary_or_null_bytes`, `unknown_format`, or extension mismatch.

This is a local admission condition. It permits later provider-specific translation only if another implemented owner accepts the resulting shape.

### Runtime message path

First eligible competency:

```text
Runtime input event recording / decision input composition
```

The runtime can append `input.user_message`, project state, and include the current input in the decision packet. This makes the representation visible to decision production, but still does not make it an `Observation`.

### Provider observation path

First eligible competency:

```text
Provider-local intake / source contract
```

For Ansible inventory, the provider first asks input inspection to produce an `InputArtifact`, then only accepts INI/YAML inventory shapes, then emits observations. Observation is lawful only after provider-local validation and construction of valid `Observation` records.

## Classification of the transition

### Is it a constitutional transition?

Yes, narrowly:

```text
Null -> external representation exists
```

is a repository-visible constitutional distinction because implementation can preserve or inspect representations without creating observations.

### Is it an existing owner responsibility?

Yes, but distributed. The transition is already owned locally by existing responsibilities:

- inquiry-note preservation for operator prose;
- input inspection for file bytes;
- runtime input event recording for user messages;
- provider-local intake for observation sources.

No implementation evidence demands a new universal owner.

### Is it a local admission condition?

Yes. In most reviewed paths, `External Representation Exists` is best understood as a local admission condition: the receiving competency may inspect, preserve, classify, or stop. It may not promote the representation beyond its own contract.

### Is it unsupported?

The broad claim that `External Representation Exists` is a centralized repository object or universal admission engine is unsupported. The repository has local records and events, not a global `ExternalRepresentation` abstraction.

## What `.` does and does not justify

`.' justifies:

- non-empty raw operator prose exists;
- inquiry-note preservation can record it in the isolated probe store;
- inquiry orientation can render a read-only bounded view over the note and existing projected state;
- the orientation can truthfully report no deterministic related material if no lexical support is found.

`.' does not justify:

- an observation;
- evidence or fact creation;
- repository attachment;
- semantic interpretation;
- grammar recovery;
- responsibility recovery;
- candidate participation outside an implemented local boundary;
- event-ledger or cluster mutation by diagnostic/orientation behavior.

## Supported conclusion

The first lawful transition is not a new subsystem. It is this bounded distinction:

```text
Null
↓
External representation exists for an already implemented local responsibility
↓
That responsibility may preserve, inspect, classify, orient, translate, or stop only within its own authority
```

For `.` the first lawful transition is:

```text
Null
↓
Preserved inquiry note exists: raw_note="."
↓
Inquiry Orientation may participate read-only, if asked, without creating observation truth
```

The next implementation slice, if one is ever needed, should not start by building a universal receiver. It should first identify the exact entry path and prove which existing bounded competency is allowed to act after external representation existence becomes visible.
