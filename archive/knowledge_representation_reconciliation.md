# Knowledge Representation Reconciliation

## Purpose

This document reconciles Seed's existing representation language with the newer Claim Support model.

It prevents a second vocabulary drift problem by clarifying how these representations fit together:

```text
Observation
→ Evidence
→ Fact
→ Relationships
→ Entity Types
→ Contradictions
→ Projection
→ Explanation
```

and:

```text
Observation
→ Evidence
→ Fact
→ Support Relationship
→ Claim
```

## Finding

These models are compatible.

They describe different parts of the representation layer.

The first model describes projected knowledge structures.

The second model describes claim justification structure.

## Existing Projected Knowledge Structure

Seed already projects more than facts.

Current projected knowledge can include:

```text
Facts
Relationships
Entity Types
Contradictions
Issues
Requirements
Capabilities
Evidence Graph
State Views
Explanation surfaces
```

This remains true.

Claim Support does not replace these structures.

## Claim Justification Structure

Claim Support adds a narrower representation concern:

```text
Fact
        ↓
Support Relationship
        ↓
Claim
```

This describes how projected facts can support claims.

It does not replace existing FactSupport or Evidence Graph behavior.

## Evidence Support Versus Claim Support

The key distinction is:

```text
Evidence supports facts.

Facts support claims.
```

Evidence support answers:

```text
Why does Seed believe this fact exists?
```

Claim support answers:

```text
Why does this claim have backing?
```

These are different questions.

## Relationship To FactSupport

Existing `FactSupport` language remains valid.

`FactSupport` links facts to evidence.

Claim Support links facts to claims.

Therefore:

```text
FactSupport is evidence support.
Claim Support is claim justification support.
```

They should not be collapsed into one concept.

## Relationship To Relationships

Support Relationship may be represented as a specialized relationship type in future work.

However, it should retain distinct semantics:

```text
relationship: entity A depends_on entity B
support relationship: fact A supports claim B
```

Both are relationships.

They do not mean the same thing.

## Relationship To Projection

Projection remains the current-state derivation mechanism.

Claim Support may produce projected support relationships in future work, but it should do so through existing projection ownership.

It should not create a separate SupportStore or ClaimStore.

## Relationship To Explanation

Explanation surfaces already answer why projected facts are believed.

Claim Support can later allow explanation surfaces to answer why claims are supported.

Example:

```text
Why does Seed say ToolExecutor owns execution?
```

A support-aware answer can cite:

```text
documentation claim
repository facts
support relationship
support strength
```

## Reconciled Representation Map

The reconciled representation model is:

```text
Observation
        ↓
Evidence
        ↓
Fact
        ↓
Projected Knowledge Structures
        ↓
Explanation / Query / Response
```

with an additional claim-justification branch:

```text
Fact
        ↓
Support Relationship
        ↓
Claim
```

These are not competing models.

They are complementary branches of the representation layer.

## Non-Goals

This reconciliation does not justify:

```text
ReasoningEngine
InferenceEngine
TruthEngine
ClaimStore
SupportStore
ArchitectureEngine
```

It does not require runtime behavior.

It does not require implementation.

## Documentation Impact

Front-door documentation should describe:

```text
Process Layer:
Knowledge Acquisition → Knowledge Integrity → Knowledge Selection → Response

Representation Layer:
Observation → Evidence → Fact → projected structures
Claim Support Branch:
Fact → Support Relationship → Claim
```

## Conclusion

Seed's representation language is now reconciled.

Existing projected knowledge structures remain valid.

Claim Support adds an explicit claim-justification branch.

The canonical distinction is:

```text
Evidence supports facts.
Facts support claims.
```
