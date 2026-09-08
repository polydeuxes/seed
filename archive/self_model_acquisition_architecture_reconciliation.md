# Self-Model Acquisition Architecture Reconciliation

## 1. Purpose and Scope

This document audits Seed's current self-model acquisition architecture end to
end.

The audit question is:

```text
Can a reader clearly explain how Seed learns about itself from repository
contents and documentation?
```

This is a documentation-only reconciliation. It does not modify production code,
tests, event schemas, projections, storage, runtime routing, provider execution,
capability acquisition logic, or policy behavior.

The scope is the existing self-model vocabulary and fixture-level architecture:

- `RepositoryObservation`
- `DocumentationObservation`
- `RepositoryArtifactFact`
- `DocumentationClaim`
- `AlignmentRecord`
- existence claim reconciliation
- structure claim reconciliation
- repository observation reconciliation
- repository artifact ontology reconciliation
- self-model acquisition fixture tests
- knowledge acquisition architecture
- observation ingestion
- evidence and fact support
- projection state and inventory views
- acquisition ownership boundaries

The audit intentionally does not introduce a new acquisition engine, ontology
system, projection store, claim store, or truth arbitration layer.

## 2. Existing Concepts Found

### Knowledge acquisition spine

Seed's general knowledge acquisition model is already documented as:

```text
Observation -> Evidence -> Fact -> Projection
```

That spine answers:

```text
What was observed?
Why is the resulting fact believed?
What fact entered the model?
What projected state or view can now expose it?
```

Self-model acquisition reuses this spine rather than defining an independent
self-understanding subsystem.

### Self-model reconciliation spine

The self-model and alignment documents define a narrower reconciliation spine:

```text
Documentation
        ↓
Documentation Claims

Repository
        ↓
Repository Artifact Facts

Documentation Claims + Repository Artifact Facts
        ↓
Alignment Records

Alignment Records
        ↓
Self Model
```

This spine answers:

```text
What does Seed claim about itself?
What does Seed's repository contain?
How do those two sets of records align?
```

It is explicitly not a reasoning engine and not a truth engine.

### DocumentationObservation

Documentation Observation is the documentation-side acquisition slice. It asks:

```text
What does the repository say?
```

Its safe v0 behavior is deterministic extraction from supplied documentation
text. It extracts narrow explicit claims from headings, bullet lines, explicit
boundary phrases, rejected-concept statements, frontier statements, existence
statements, and structure statements.

It must not decide whether the documentation is true, whether the code matches,
or which claim wins.

### DocumentationClaim

A `DocumentationClaim` is a documentation-backed statement capable of receiving
support from facts. It carries at least:

```text
claim
claim_family
source_path
source_heading
```

Examples:

```text
ToolExecutor owns registered-operation execution.
ToolExecutor exists.
Runtime defines method handle_user_message.
InputEngine is rejected.
```

A DocumentationClaim is not an implementation fact. It records that a document
claims something.

### RepositoryObservation

Repository Observation is the repository-side acquisition slice. It asks:

```text
What repository artifacts exist?
```

Its safe v0 behavior is deterministic extraction from caller-provided Python
source text. It emits module/file facts and, when parsing succeeds, top-level
classes, top-level functions, top-level async functions, direct class methods,
and top-level imports.

It must not infer architecture, ownership, behavior, authority, runtime usage,
or documentation alignment.

### RepositoryArtifactFact

A `RepositoryArtifactFact` is a structural fact about an observed repository
artifact. It carries at least:

```text
fact
artifact_kind
path
symbol
parent_symbol
```

Examples:

```text
Module/file seed_runtime/execution.py exists.
Class ToolExecutor exists in seed_runtime/execution.py.
Class Runtime defines method handle_user_message in seed_runtime/runtime.py.
Import seed_runtime.events.Event exists in seed_runtime/runtime.py.
```

A RepositoryArtifactFact is not a documentation claim and not an architectural
conclusion.

### Claim support and fact support

The representation reconciliation keeps two support questions separate:

```text
Evidence supports facts.
Facts support claims.
```

Fact support answers:

```text
Why does Seed believe this fact exists?
```

Claim support answers:

```text
Why does this claim have backing?
```

These are complementary, not interchangeable.

### AlignmentRecord

An `AlignmentRecord` is the deterministic comparison result between one
DocumentationClaim and supplied RepositoryArtifactFacts. It carries at least:

```text
claim
artifact_facts
outcome
rule_id
reason
```

Current outcomes are:

```text
supported
missing_support
potential_conflict
not_evaluable
```

An AlignmentRecord is not raw observation, not evidence, not a repository fact,
and not proof of truth. It is reconciliation state.

### Existence claims

Existence claim reconciliation defines a narrow claim family for explicit claims
such as:

```text
ToolExecutor exists.
Runtime defines handle_user_message.
```

The key boundary is that existence support can come from direct artifact facts,
but it must not be upgraded into ownership support.

### Structure claims

Structure claim reconciliation narrows method-containment semantics. The
supported form is:

```text
X defines method Y.
```

This requires a class fact for `X` and a method fact for `Y` with
`parent_symbol == X`. It is stronger than the broader existence form `X defines
Y.` because it encodes direct class-method containment rather than same-path
co-occurrence.

### Repository artifact ontology

The repository artifact ontology work clarifies that artifact kinds matter.
Modules, classes, functions, methods, imports, tests, documentation files,
configuration, generated artifacts, and scripts should not all be treated as the
same kind of support.

This is important because a class definition, an import mention, a documentation
paragraph, and a test fixture can all mention `ToolExecutor` while supporting
very different conclusions.

### Projection state and inventory views

The general architecture projects evidence-backed facts into current knowledge
structures and inventory views. The self-model documents describe the self model
as a derived view over claims, artifacts, support relationships, and alignment
records.

The implemented self-model slice is still fixture-level. It demonstrates that
claims, artifact facts, and alignment records compose end to end, but it does
not yet fully specify how those typed records are appended, projected, and
inventoried as durable canonical runtime state.

## 3. Canonical Acquisition Flow

The clearest current canonical flow is a two-lane acquisition flow followed by
reconciliation:

```text
Documentation lane:
Documentation source text
        ↓
DocumentationObservation
        ↓
Documentation evidence
        ↓
Documentation-derived fact that a claim exists
        ↓
DocumentationClaim

Repository lane:
Repository source text / artifact listing
        ↓
RepositoryObservation
        ↓
Repository evidence
        ↓
RepositoryArtifactFact

Reconciliation lane:
DocumentationClaim
+
RepositoryArtifactFact set
        ↓
Explicit reconciliation rule
        ↓
AlignmentRecord
        ↓
Projected self-model / inventory view
```

This is the canonical explanation a reader can assemble today.

The flow is coherent at the conceptual and fixture level, but there is an
important seam: the documents sometimes describe `DocumentationClaim` and
`RepositoryArtifactFact` directly as acquisition products, while the broader
knowledge architecture expects ordinary `Observation -> Evidence -> Fact ->
Projection` transitions. The architecture is compatible, but the exact durable
handoff from observations/evidence/facts into typed claim/fact/alignment read
models is not described in one canonical operational sequence.

## 4. Where Acquisition Begins

Self-model acquisition begins at bounded, read-only inputs:

1. documentation text supplied to Documentation Observation; and
2. repository source or artifact text supplied to Repository Observation.

For the current implementation slice, this is caller-provided text rather than a
repository-wide scanner. That boundary matters: missing support means missing
from the supplied artifact facts, not proof of repository-wide absence, unless a
future acquisition scope explicitly says the whole relevant repository has been
observed.

## 5. What Is Observed Directly

Direct observations include:

- documentation source path, nearest heading, line/text span, extraction kind,
  and explicit claim text;
- repository source path, module/file presence, parse outcome, class names,
  function names, async function names, direct class-method names, import names,
  and parent/containment metadata available from parsing.

Direct observations do not include:

- architectural ownership;
- behavioral execution authority;
- correctness;
- documentation truth;
- implementation completeness;
- user intent;
- provider capability;
- policy approval.

## 6. What Is Inferred

Only narrow deterministic inferences are currently allowed:

- a line matching an explicit documentation pattern becomes a
  DocumentationClaim with a claim family;
- a Python AST node becomes a RepositoryArtifactFact with an artifact kind;
- a recognized claim family and matching artifact facts become an
  AlignmentRecord outcome;
- a missing matching artifact fact becomes `missing_support` only within the
  supplied fact set;
- unknown claim families or unsupported text patterns become `not_evaluable`.

The current architecture does not infer broad semantics such as:

- `class ToolExecutor` proves `ToolExecutor executes registered operations`;
- an import proves local definition;
- a documentation sentence proves implementation behavior;
- absence from a fixture proves repository-wide absence;
- alignment support proves truth.

## 7. What Becomes Evidence

Evidence is the provenance-preserving support payload derived from an
observation. For this domain, evidence should preserve:

- source path;
- source heading when applicable;
- line range or text span when available;
- extraction kind;
- observed artifact kind;
- parse source or AST source when applicable;
- acquisition scope.

Evidence answers:

```text
Why does Seed believe this observed record exists?
```

For example, evidence for `Class ToolExecutor exists in seed_runtime/execution.py`
should point to the source path and class definition span, not to a documentation
claim saying `ToolExecutor owns execution`.

## 8. What Becomes Fact

Facts are evidence-backed records that can enter projection.

In the self-model domain, two fact-like surfaces must remain distinct:

1. documentation-derived fact: a document made a claim; and
2. repository artifact fact: a repository artifact exists or has a structural
   relationship.

The current fixture types name the second directly as `RepositoryArtifactFact`.
For the first, the current documents usually expose `DocumentationClaim`
directly rather than naming an intermediate `DocumentationClaimFact`. This is
understandable, but it is the main remaining operational seam between the broad
knowledge spine and the self-model spine.

## 9. What Becomes Claim

A claim is a documentation-backed statement that can receive support.

A claim can be extracted only from documentation-side observation, not from
repository artifact observation. Repository artifacts may support a claim, fail
to support it, or potentially conflict with it, but they do not become the claim
itself.

Examples:

```text
ToolExecutor exists.
ToolExecutor owns registered-operation execution.
ToolExecutor manages approvals.
Runtime defines method handle_user_message.
```

Each example is a claim only if documentation states it in a supported explicit
form or future rules define a supported extraction form.

## 10. What Becomes Alignment

An AlignmentRecord is produced when a DocumentationClaim is reconciled against a
set of RepositoryArtifactFacts through an explicit rule.

Current alignment is claim-family specific:

- ownership rules are narrow and hard-coded for known symbols;
- rejected-concept rules look for mentions of rejected concepts;
- frontier rules look for implementation-like mentions of a frontier name;
- existence rules evaluate explicit `X exists.` and `X defines Y.` patterns;
- structure rules evaluate explicit `X defines method Y.` patterns.

Alignment answers:

```text
Does the supplied repository-artifact fact set support this documentation claim
under this explicit rule?
```

It does not answer:

```text
Is the claim true?
Should code be changed?
Should documentation be changed?
What should Seed do next?
```

## 11. What Becomes Projected Knowledge

Projected self-model knowledge should be the durable read view over:

- observed documentation claims;
- observed repository artifact facts;
- evidence support for those records;
- support relationships from artifact facts to claims;
- alignment records and outcomes;
- inventory views summarizing claims, artifacts, unsupported claims,
  potentially conflicting claims, and non-evaluable claims.

Conceptually, the projection answers:

```text
What does Seed know about itself, and why does it believe it?
```

Today, the answer is clearly modeled conceptually and through fixture tests, but
not fully specified as one durable operational projection contract for claims,
artifact facts, alignments, and inventory views.

## 12. Ownership Boundaries

| Stage | Owner | Owns | Must not own |
| --- | --- | --- | --- |
| Documentation Observation | Knowledge Acquisition | Extract explicit documentation claims from bounded documentation input | Truth, implementation validation, repository scanning, claim victory |
| Repository Observation | Knowledge Acquisition | Extract structural artifact facts from bounded repository input | Architectural intent, behavior, documentation alignment |
| Evidence ingestion | Knowledge Acquisition / evidence support | Preserve provenance and support payloads | Claim truth or alignment outcome |
| Fact creation | Knowledge Acquisition | Convert supported observations into evidence-backed facts | Context selection, response shaping, policy decisions |
| Claim support | Claim Support / reconciliation | Relate facts to claims through explicit rules | Fact creation, evidence creation, truth arbitration |
| Alignment records | Repository Reconciliation / Knowledge Integrity-adjacent reconciliation | Record deterministic comparison outcomes | Runtime behavior, implementation planning, automatic correction |
| Projection state | Projection ownership | Build current self-model and inventory read views from durable records | New acquisition, hidden inference, provider execution |
| Inventory / response views | Knowledge Selection / Response surfaces | Select, summarize, and explain projected records | Create facts, overwrite claims, adjudicate undocumented truth |

The broad ownership boundaries are explicit. The remaining ambiguity is not who
should own each stage; it is the exact typed handoff between the general
`Observation -> Evidence -> Fact -> Projection` pipeline and the self-model
specific `DocumentationClaim + RepositoryArtifactFact -> AlignmentRecord`
pipeline.

## 13. Observation, Claim, Fact, and Alignment Distinctions

### Observation vs conclusion

Observations are bounded source readings. They do not decide architecture.

Examples:

```text
The file text contains a heading named Ownership Boundaries.
The Python AST contains a class named ToolExecutor.
```

Conclusions are later records such as facts, support relationships, alignment
outcomes, and projected inventory state.

### Claim vs fact

A claim says what documentation states. A fact says what evidence supports as an
observed record.

Correct separation:

```text
DocumentationClaim: ToolExecutor owns registered-operation execution.
RepositoryArtifactFact: Class ToolExecutor exists in seed_runtime/execution.py.
```

Incorrect collapse:

```text
Class ToolExecutor exists, therefore ToolExecutor owns execution.
```

### Artifact fact vs alignment record

An artifact fact records an observed repository structure. An alignment record
records how that fact set relates to a documentation claim.

Correct separation:

```text
RepositoryArtifactFact: Class ToolExecutor exists.
AlignmentRecord: The ToolExecutor ownership claim is supported by a narrow v0
rule because a ToolExecutor artifact fact exists.
```

Even when the v0 ownership rule says `supported`, that support is a rule outcome
with known weakness, not a broad behavioral proof.

### Fact support vs claim support

Fact support links evidence to facts. Claim support links facts to claims.

Correct separation:

```text
Evidence -> RepositoryArtifactFact
RepositoryArtifactFact -> DocumentationClaim
```

Incorrect collapse:

```text
Evidence directly proves the architectural claim.
```

## 14. Repository and Documentation Separation

The separation is mostly clear.

Repository Observation asks:

```text
What does the repository contain?
```

Documentation Observation asks:

```text
What does the repository say?
```

Repository facts and documentation claims are clearly different in the fixture
model and in the reconciliation documents. The architecture repeatedly warns not
to treat documentation as proof of implementation and not to treat repository
symbols as architectural intent.

The remaining risk is terminology drift: some documentation describes
documentation-derived records as facts, while other documents emphasize
`DocumentationClaim`. The concepts are compatible if interpreted as
"evidence-backed fact that a claim exists" plus "claim text that can be
reconciled," but that interpretation should be made explicit wherever future
implementation work touches durable projection.

## 15. Existence and Structure Separation

Existence and structure are now clearly separated enough for future work.

Existence claims:

```text
X exists.
X defines Y.
```

Structure claims:

```text
X defines method Y.
```

The difference is important:

- `X exists.` needs a matching artifact symbol;
- `X defines Y.` needs same-path co-occurrence under the existence rule;
- `X defines method Y.` needs a class fact plus a method fact whose parent is the
  class.

This separation prevents same-path existence support from masquerading as direct
class-member structure support.

## 16. Worked Examples

### Example A: repository source contains `class ToolExecutor`

Input:

```python
class ToolExecutor:
    pass
```

Observation:

```text
RepositoryObservation sees Python source text for the supplied source path and
an AST ClassDef named ToolExecutor.
```

Evidence:

```text
Repository evidence records the source path, extraction kind `python_ast_class`,
and the class definition span when available.
```

Claim:

```text
No DocumentationClaim is created from this repository source alone.
```

Fact:

```text
RepositoryArtifactFact: Class ToolExecutor exists in the supplied source path.
```

Reconciliation:

```text
None unless there is a DocumentationClaim to compare against the fact set.
```

Alignment result:

```text
No AlignmentRecord from this input alone.
```

Projected state:

```text
The repository artifact inventory can project that ToolExecutor exists as a
class in the observed scope. The self-model should not project that ToolExecutor
owns, executes, or approves anything from this source alone.
```

### Example B: documentation states `ToolExecutor executes registered operations`

Input:

```text
ToolExecutor executes registered operations.
```

Observation:

```text
DocumentationObservation sees documentation text containing a sentence about
ToolExecutor.
```

Evidence:

```text
Documentation evidence records source path, heading, line/text span, extraction
kind, and claim text when the sentence is extracted.
```

Claim:

```text
A DocumentationClaim can exist only if the extraction rules classify this text.
Today, the canonical supported ownership example is `ToolExecutor owns
registered-operation execution.` The wording `executes registered operations` is
semantically close, but if no explicit extraction rule recognizes it, it should
remain unextracted or become `not_evaluable` after explicit claim creation.
```

Fact:

```text
The documentation-side fact is only that the document made this claim. It is not
a repository artifact fact and not proof of runtime behavior.
```

Reconciliation:

```text
If normalized into a supported ownership claim and a ToolExecutor artifact fact
is supplied, the current narrow ownership rule may produce support. If not
normalized, no canonical rule should infer ownership or behavior from this
sentence.
```

Alignment result:

```text
Supported only under an explicit recognized ownership rule; otherwise
not_evaluable or absent from reconciliation.
```

Projected state:

```text
The projected self-model may show a documentation claim about ToolExecutor and,
if reconciled, an alignment outcome. It should not project proven execution
behavior unless behavioral evidence rules are later defined.
```

### Example C: documentation states `ToolExecutor manages approvals`

Input:

```text
ToolExecutor manages approvals.
```

Observation:

```text
DocumentationObservation can see the sentence as documentation text.
```

Evidence:

```text
Documentation evidence can preserve where the sentence appeared if extracted.
```

Claim:

```text
Under current documented rules, this is not a canonical supported ownership,
existence, structure, rejected-concept, or frontier pattern. If represented as a
DocumentationClaim anyway, it should be `not_evaluable` unless a future explicit
approval-management claim family is defined.
```

Fact:

```text
The only safe documentation-side fact is that documentation states this claim.
No RepositoryArtifactFact is created by this documentation sentence.
```

Reconciliation:

```text
A ToolExecutor class fact is insufficient to prove approval management. The
architecture forbids upgrading symbol existence into behavioral ownership or
approval authority.
```

Alignment result:

```text
not_evaluable, or missing support if a future explicit approval-management rule
requires artifact evidence that is not present.
```

Projected state:

```text
The projected self-model should show an unsupported or non-evaluable
documentation claim, not an accepted fact that ToolExecutor manages approvals.
```

### Example D: repository no longer contains `ToolExecutor`

Input:

```text
The supplied repository artifact scope contains no class, function, module, or
import fact with symbol ToolExecutor.
```

Observation:

```text
RepositoryObservation observes whatever artifacts are in scope. It does not
observe `ToolExecutor`.
```

Evidence:

```text
Evidence exists for the artifacts that were observed and for the acquisition
scope. Absence is meaningful only if that scope is explicit.
```

Claim:

```text
Any existing DocumentationClaim such as `ToolExecutor exists.` or
`ToolExecutor owns registered-operation execution.` remains a documentation
claim until superseded or removed by documentation acquisition.
```

Fact:

```text
No positive RepositoryArtifactFact for ToolExecutor exists in the supplied fact
set. This is not automatically a repository-wide negative fact.
```

Reconciliation:

```text
`ToolExecutor exists.` -> missing_support when reconciled against the supplied
fact set.

`ToolExecutor owns registered-operation execution.` -> missing_support under the
current narrow ownership rule when no ToolExecutor artifact fact is supplied.
```

Alignment result:

```text
missing_support within the observed acquisition scope.
```

Projected state:

```text
The projected self-model should show the documentation claim as lacking
repository artifact support in the observed scope. It should not state
repository-wide non-existence unless acquisition scope and negative-evidence
semantics explicitly allow that conclusion.
```

## 17. Answers to the Audit Questions

1. **What is the canonical self-model acquisition pipeline today?**
   Documentation Observation produces DocumentationClaims; Repository
   Observation produces RepositoryArtifactFacts; explicit reconciliation rules
   compare them into AlignmentRecords; projection/inventory views should expose
   claims, facts, evidence, and alignment.

2. **Where does acquisition begin?**
   It begins with bounded read-only documentation text and repository artifact
   text/source supplied to the observation slices.

3. **What is observed directly?**
   Documentation text, headings, explicit claim strings, source paths, Python
   modules/files, class definitions, functions, direct class methods, imports,
   and parse outcomes.

4. **What is inferred?**
   Claim family classification, artifact fact construction from parsed source,
   and rule-bound alignment outcomes.

5. **What becomes evidence?**
   Provenance payloads for documentation and repository observations: source
   path, heading, span, extraction kind, artifact kind, and scope.

6. **What becomes fact?**
   Repository artifact facts and documentation-derived facts that a claim was
   stated. RepositoryArtifactFact is explicit; the documentation-claim-as-fact
   handoff remains less explicit.

7. **What becomes claim?**
   Documentation-backed statements extracted from documentation inputs.
   Repository observations do not become claims.

8. **What becomes alignment?**
   Reconciliation outputs comparing one claim to supplied artifact facts under
   an explicit rule.

9. **What becomes projected knowledge?**
   The self-model read view: claims, repository artifact facts, support
   relationships, alignment outcomes, provenance, and inventory summaries.

10. **Are repository observations and documentation observations clearly
    separated?**
    Yes at the conceptual and fixture levels.

11. **Are repository facts and documentation claims clearly separated?**
    Mostly yes. The key residual ambiguity is how documentation claims are
    represented as evidence-backed facts in durable projection without collapsing
    claim and fact semantics.

12. **Are existence claims and structure claims clearly separated?**
    Yes. Existence covers `X exists.` and same-path `X defines Y.`; structure
    covers direct `X defines method Y.` containment.

13. **Are artifact facts and alignment records clearly separated?**
    Yes. Artifact facts describe repository structure; alignment records
    describe rule outcomes comparing claims to facts.

14. **Is ownership of each stage explicit?**
    Mostly yes. Acquisition, evidence support, claim support, reconciliation,
    projection, and response/selection responsibilities are separated.

15. **Is there a single canonical acquisition flow?**
    There is a single conceptual flow, but not yet a single fully specified
    durable operational flow that names every transition from observations and
    evidence into typed claims, artifact facts, alignments, projection state, and
    inventory views.

16. **What ambiguities remain?**
    The smallest ambiguity is the durable handoff between the general knowledge
    spine and the self-model typed records: exactly when a
    DocumentationObservation becomes evidence, when it becomes a fact that a
    claim exists, when it becomes a DocumentationClaim, and how that claim and
    later AlignmentRecord are projected into canonical inventory state.

## 18. Remaining Ambiguities

### Smallest unresolved boundary

The smallest remaining unresolved boundary is:

```text
DocumentationObservation / RepositoryObservation
        ↓
Evidence-backed Fact
        ↓
Typed self-model record
        ↓
Projected self-model inventory
```

The architecture says all of these concepts should exist and remain compatible,
but it does not yet provide one canonical operational contract for the handoff.

More specifically:

- Is a `DocumentationClaim` itself a projected fact, a typed view over a fact, or
  both?
- Is a `RepositoryArtifactFact` the canonical fact record, or a typed view over
  an ordinary Fact with repository-artifact predicates?
- Is an `AlignmentRecord` projected as a fact, relationship, issue, inventory
  row, or specialized reconciliation view?
- Which projection owns the current self-model inventory of unsupported,
  supported, conflicting, and non-evaluable claims?
- How should evidence spans and acquisition scope be carried into that inventory
  so that absence and missing support are not overclaimed?

### Other ambiguities

- Ownership claims still have deliberately weak v0 support semantics for known
  symbols; existence and structure are sharper than ownership.
- Behavioral evidence is named as a future evidence level but not implemented as
  a reconciliation family.
- Negative evidence remains scope-sensitive and is not a general absence proof.
- Documentation authority, freshness, canonicality, and supersession metadata are
  recognized but not fully operationalized for self-model projection.
- Repository-wide acquisition scope is not established by fixture-level supplied
  source text.
- Inventory view schemas for the self model are conceptually described but not
  canonically specified.

## 19. Non-Goals

This reconciliation does not propose or require:

- a new acquisition engine;
- a new ontology system;
- a new architecture engine;
- a new truth engine;
- a new claim store;
- a new support store;
- provider calls;
- runtime execution;
- tool execution;
- policy behavior changes;
- broad LLM interpretation of documentation;
- repository-wide semantic analysis;
- automatic documentation correction;
- automatic code generation;
- collapsing documentation claims into repository facts;
- collapsing observations into conclusions.

## 20. Rejected Solutions

### Add a SelfModelEngine

Rejected. The existing knowledge acquisition, evidence, fact, projection, claim
support, and reconciliation concepts are sufficient. A new engine would obscure
ownership and create a parallel truth path.

### Treat documentation as truth

Rejected. Documentation Observation records what documentation claims. It does
not prove implementation behavior.

### Treat repository symbols as architecture

Rejected. A class or import can support existence and narrow structural claims,
but it cannot by itself prove ownership, execution behavior, approval authority,
or architectural intent.

### Collapse claims and facts

Rejected. A claim needs support; a fact needs evidence. They answer different
questions and must remain separate.

### Collapse alignment into projection truth

Rejected. Alignment outcomes are reconciliation records. `supported` means
supported by a rule and supplied fact set, not globally true.

### Add a new ontology layer now

Rejected. The repository artifact ontology can be sharpened within existing
artifact kinds, evidence metadata, facts, relationships, and projected views.

## 21. Direct Answer

Seed's self-model acquisition architecture is coherent enough to explain the
current fixture-level model and to guide near-term self-model acquisition work.
A reader can explain the core answer:

```text
Seed learns what it says about itself from DocumentationObservation, learns what
its repository contains from RepositoryObservation, preserves evidence for both,
turns observed repository structure into RepositoryArtifactFacts, turns observed
documentation statements into DocumentationClaims, reconciles claims and facts
through explicit rules into AlignmentRecords, and should project those records
into self-model inventory views.
```

However, it is not yet complete enough to serve as the fully canonical durable
model for all future acquisition work.

The smallest remaining unresolved boundary is the typed projection handoff:

```text
How exactly do ordinary observations, evidence, and facts become durable
DocumentationClaim, RepositoryArtifactFact, AlignmentRecord, and inventory-view
records without collapsing documentation claims, repository facts, evidence
support, claim support, and alignment outcomes together?
```

Once that handoff is specified, no new architectural layer appears necessary.
The existing append/project/inventory pattern and the existing
Observation/Evidence/Fact/Projection spine are sufficient.
