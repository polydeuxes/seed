# Typed Projection Handoff Reconciliation

## 1. Purpose and scope

This document audits Seed's semantic boundary between alignment/reconciliation
outputs and projected self-model state.

The audit question is:

```text
Does Seed currently define a clear semantic handoff between alignment / reconciliation outputs and projected self-model state?
```

This is a documentation-only reconciliation. It does not modify production code,
tests, event schemas, projection schemas, projection stores, runtime behavior,
provider logic, policy behavior, or acquisition pipelines.

The boundary under review is intentionally narrow:

```text
DocumentationClaim
        ↘
          AlignmentRecord
        ↗
RepositoryArtifactFact
        ↓
Projection / Inventory / Self Model
```

The questions are:

- What leaves alignment?
- What enters projection?
- What becomes projected knowledge?
- What remains acquisition or reconciliation metadata?

This document does not design a projection engine, projection store, response
formatter, repository scanner, truth arbiter, or new alignment-record schema.

## 2. Existing concepts found

### DocumentationObservation

Documentation Observation is the documentation-side acquisition slice. It asks
what the repository says, not whether the repository is correct. Current
self-model documentation describes it as reading bounded documentation input and
extracting explicit documentation-backed claims with provenance such as source
path, heading, line or text span, extraction kind, and claim text.

A DocumentationObservation must not infer repository behavior, architecture,
truth, implementation completeness, provider capability, policy authority, or
runtime permission.

### DocumentationClaim

A `DocumentationClaim` is a documentation-backed statement capable of receiving
support. It records that documentation says something. It is not a repository
fact and not proof that the statement is true.

Current fixture-level fields are:

```text
claim
claim_family
source_path
source_heading
```

Documentation claims can be ownership claims, rejected-concept claims, frontier
claims, existence claims, structure claims, or future explicitly supported claim
families. Claims outside supported patterns should be absent from reconciliation
or become `not_evaluable` if manually supplied as claims.

### RepositoryObservation

Repository Observation is the repository-side acquisition slice. It asks what
repository artifacts exist. Current v0 behavior is deterministic extraction from
bounded, caller-provided source text rather than repository-wide proof.

A RepositoryObservation must not infer architecture, ownership, behavior,
provider capability, policy authority, documentation alignment, or truth.

### RepositoryArtifactFact

A `RepositoryArtifactFact` is a structural fact about an observed repository
artifact. It records that an artifact exists or has an observed structural shape.
It is not a documentation claim and not an architectural conclusion.

Current fixture-level fields are:

```text
fact
artifact_kind
path
symbol
parent_symbol
```

Examples include module/file existence, class existence, function existence,
method containment, and imports where observation rules emit them.

### Repository observation reconciliation

Repository reconciliation compares documentation claims with supplied repository
artifact facts under explicit deterministic rules. It is read-only. It produces
alignment knowledge; it does not append facts, project state, execute tools,
call providers, correct documentation, or modify repository code.

A crucial scope rule is that missing support means missing from the supplied
artifact fact set, not repository-wide absence, unless a future acquisition scope
explicitly establishes repository-wide negative-evidence semantics.

### Existence reconciliation

Existence reconciliation is the sharpest structural claim family. It supports
explicit forms such as:

```text
X exists.
X defines Y.
```

`X exists.` can be supported by a direct artifact fact whose symbol is `X`.
`X defines Y.` is currently same-path existence support, not full structural
containment, behavior, ownership, or call-flow evidence.

### Structure reconciliation

Structure reconciliation is stronger than existence but weaker than behavior,
boundary, or ownership. The currently documented implemented structure form is:

```text
X defines method Y.
```

It requires both a class artifact for `X` and a method artifact for `Y` with
`parent_symbol == X`. Same-path evidence alone is insufficient.

### AlignmentRecord

An `AlignmentRecord` is the deterministic comparison result between one
`DocumentationClaim` and supplied `RepositoryArtifactFact` records under an
explicit rule. It is reconciliation state, not raw observation, not evidence,
not a repository artifact fact, and not proof of truth.

Current fixture-level fields are:

```text
claim
artifact_facts
outcome
rule_id
reason
```

Current implemented/documented outcomes are:

```text
supported
missing_support
potential_conflict
not_evaluable
```

The user's vocabulary `unsupported` and `contradicted` maps imperfectly onto the
current alignment vocabulary:

- `unsupported` is closest to `missing_support` for recognized claims whose
  expected support is absent from the supplied fact set.
- `contradicted` is stronger than current `potential_conflict`; current v0/v1
  alignment usually has potential-conflict semantics, not definite contradiction.
- `not_evaluable` is already a first-class outcome.

### Alignment status

Alignment status is a reconciliation outcome for a supplied claim, supplied fact
set, and explicit rule. It is not a truth value, confidence score, execution
permission, policy decision, human review result, or repository-wide search
result.

### Self-model acquisition architecture

The current self-model acquisition architecture is coherent at conceptual and
fixture level:

```text
DocumentationObservation
        ↓
DocumentationClaim

RepositoryObservation
        ↓
RepositoryArtifactFact

DocumentationClaim + RepositoryArtifactFact set
        ↓
AlignmentRecord
        ↓
Projected self-model / inventory view
```

The acquisition audit identifies a remaining seam: the exact durable handoff
from typed self-model records into projected inventory state is conceptually
named but not operationally specified as one canonical contract.

### Projection state

Seed's general projection architecture turns append-only event-ledger data into
latest-current state and derived read-only views. Projection state answers what
Seed currently knows, along with support, conflicts, stale status, evidence, and
other integrity metadata.

ProjectionStore ownership is narrow: it caches latest-current projection
snapshots and does not own events, historical truth, as-of queries, provider
execution, or projection mutation beyond cache behavior.

### Projection inventories and inventory views

Inventory views are read-only views over projected knowledge. Existing inventory
patterns expose facts, observations, requirements, capabilities, issues,
unsupported facts, contradictions, confidence summaries, integrity summaries,
and capability status without creating new knowledge.

For the self-model domain, the conceptual inventory view is expected to expose
claims, repository artifact facts, alignment outcomes, unsupported or missing
support claims, potential conflicts, non-evaluable claims, source provenance,
rule provenance, and acquisition scope. The shape of that self-model inventory
is not yet canonically specified.

### Projection snapshots

Projection snapshots are latest-current cache artifacts. They should cache the
current projected self-model when such a projection exists, but they should not
be treated as historical truth stores, as-of APIs, reconciliation engines, or
sources of new claims.

### State projection

State projection is the latest-current derivation mechanism. It can retain
durable facts, choose current measurement samples, expose conflicts, expose
stale facts at read time, and build read-only views. It does not decide truth,
rewrite old facts because a newer fact exists, or resolve contradictions by
itself.

### Projection integrity summaries

Projection integrity summaries show that Seed already has a pattern for joining
read-only integrity signals such as unsupported facts, contradictions, graph
issues, stale facts, confidence summaries, and capability inventory counts.
These summaries are views; they do not mutate projection state or resolve truth.

For self-model projection, analogous integrity summaries could count supported,
missing-support, potential-conflict, contradicted-if-added, and non-evaluable
claims, but the current documentation does not require a specific summary object.

### Knowledge projection patterns

The broader representation pattern is:

```text
Observation -> Evidence -> Fact -> Projected Knowledge Structures
```

with a claim-support branch:

```text
Fact -> Support Relationship -> Claim
```

The self-model typed records are compatible with this pattern if interpreted as:

- a `DocumentationClaim` is the claim surface, backed by evidence that a
  document stated the claim;
- a `RepositoryArtifactFact` is the repository-artifact fact surface, backed by
  repository observation evidence;
- an `AlignmentRecord` is the reconciliation result linking a claim, the
  artifact facts considered by a rule, an outcome, and explanatory provenance.

### Response composition paths

Response is a distributed read-only/selective concern. It answers from selected
projected knowledge and explanations. Response must not create facts, mutate
projections, execute operations, silently verify claims, or treat selection as
truth.

For the self-model domain, response-visible information should be selected from
projected claims, artifact facts, alignment outcomes, evidence/provenance, and
inventory summaries. It should preserve caveats about unsupported,
potential-conflict, contradicted-if-defined, not-evaluable, stale, or scope-limited
status.

## 3. Current alignment outputs

Alignment currently produces one `AlignmentRecord` per reconciled
`DocumentationClaim`.

An alignment output includes:

| Field | Semantic role | Authoritative? | Projection treatment |
| --- | --- | --- | --- |
| `claim` | The documentation claim being evaluated. | Yes, as the claim identity and claim text for this alignment. | Project as the claim side of the self-model record, with documentation provenance. |
| `artifact_facts` | The exact repository artifact facts the rule used as support or conflict evidence. | Yes, for support/conflict membership in this alignment. | Project as links/references to already-projected artifact facts; do not turn them into broader behavior. |
| `outcome` | The rule outcome. | Yes, as the alignment status. | Project as alignment status and use for inventory grouping. |
| `rule_id` | The deterministic rule that produced the outcome. | Yes, as rule provenance and eligibility boundary. | Project as provenance/trace metadata. |
| `reason` | Human-readable explanation of why the rule returned the outcome. | Explanatory only. | Preserve for explanation/response, but do not parse as a contract or derive new facts from it. |

Alignment also implicitly carries important negative information:

- no `artifact_facts` for a supported-by-absence rule can be meaningful only
  inside that rule's documented absence semantics;
- no `artifact_facts` for `missing_support` means the recognized rule found no
  matching support in the supplied fact set;
- no `artifact_facts` for `not_evaluable` means the rule did not know how to
  evaluate the claim, not that support was absent.

Alignment does not produce:

- truth;
- current-belief victory;
- verified behavior;
- execution authority;
- provider capability;
- policy approval;
- repository-wide negative facts;
- documentation correction instructions;
- code-change instructions;
- projection-store schema decisions.

## 4. Current projection inputs

The current documentation implies, but does not fully specify, that self-model
projection should consume durable records or typed views corresponding to:

1. documentation claims and their evidence/provenance;
2. repository artifact facts and their evidence/provenance;
3. support relationships from artifact facts to claims;
4. alignment records and outcomes;
5. acquisition scope and freshness/staleness metadata when available;
6. rule identifiers and explanatory reasons sufficient for inventory and
   response surfaces.

This is an implicit projection-input set, not a fully specified schema.

The minimal safe projection input for the alignment handoff is the
`AlignmentRecord`, plus stable references to the claim, artifact facts, and
evidence/provenance records it names. Projection should not consume free-form
`reason` text as a source of additional semantic assertions.

## 5. Candidate handoff contract

No new vocabulary is strictly necessary. The existing `AlignmentRecord` can be
the canonical handoff object if a small semantic contract is made explicit.

A sufficient handoff contract would be:

```text
An AlignmentRecord is projectable self-model reconciliation state.
Projection may project its claim identity, artifact-fact references, outcome,
rule_id, evidence/provenance references, and acquisition scope into current
self-model and inventory views. Projection must not project its outcome as truth,
must not parse its reason as facts, and must not infer behavior, ownership,
absence, contradiction, stale state, or supersession beyond explicit rule and
scope metadata.
```

### Authoritative fields

The authoritative handoff fields are:

1. `claim` — identifies the documentation-backed claim that is being reconciled.
2. `artifact_facts` — identifies the repository facts considered relevant by the
   rule for support or conflict; empty means only what the outcome and rule say
   it means.
3. `outcome` — identifies the alignment status.
4. `rule_id` — identifies the deterministic rule and therefore the semantic
   eligibility boundary.

These fields are authoritative only within their documented scope. For example,
`outcome = supported` is authoritative that the rule reported support, not that
the claim is globally true.

### Explanatory-only fields

`reason` is explanatory only. It is suitable for inventory drilldown,
operator-facing explanation, and response caveats. It should never be parsed or
upgraded into a projected fact, rule, claim, or repository artifact.

Documentation source heading, source path, artifact path, artifact kind, symbol,
parent symbol, line spans, extraction kind, evidence IDs, timestamps, and
acquisition scope are provenance and eligibility metadata. They can be projected
for traceability and filtering, but they do not themselves prove the claim unless
an explicit rule says they are part of support.

### Candidate vocabulary evaluation

| Candidate term | Needed? | Evaluation |
| --- | --- | --- |
| `ProjectionCandidate` | Not necessary now. | Could name an intermediate queue item, but the semantic boundary can be expressed directly on `AlignmentRecord`. |
| `ProjectedKnowledge` | Already broadly present. | Useful as general vocabulary, but too broad for the alignment handoff. |
| `ProjectableAlignment` | Not necessary now. | Would duplicate `AlignmentRecord` unless projection eligibility becomes conditional by schema or policy. |
| `AlignmentOutcome` | Useful but already implicit. | Could be a clean name for the outcome enum/status, including future `unsupported` or `contradicted` aliases. |
| `ProjectionContract` | Useful as documentation title, not a record. | This document effectively defines the missing semantic contract. |
| `ProjectionView` | Already compatible. | Appropriate for inventory or response read views, not for the handoff object itself. |
| `ProjectionEligibility` | Possibly useful later. | Only needed if future projection excludes some alignment records by scope, freshness, authority, or canonicality. |

The smallest vocabulary change is no vocabulary change: treat
`AlignmentRecord` as the handoff object and document which fields are
projectable, authoritative, explanatory, and prohibited from projection.

## 6. Supported / unsupported / contradicted / not_evaluable behavior

### `supported`

`supported` behavior should be:

- project the documentation claim as a claim that exists;
- project the repository artifact facts as artifact facts that exist in the
  observed scope;
- project the alignment status as `supported`;
- project links from the alignment to the supporting artifact facts;
- make the claim inventory-visible as supported-by-rule;
- make it response-visible as supported with caveats about rule scope;
- never project it as globally true, fully verified, behaviorally proven, safe to
  execute, or immune to later contradiction.

### `unsupported` / current `missing_support`

Seed's current alignment vocabulary uses `missing_support`, not `unsupported`,
for recognized claims where expected support is absent from the supplied fact
set.

`missing_support` behavior should be:

- project the documentation claim as a claim that exists;
- project the alignment status as missing support / unsupported within the rule
  and acquisition scope;
- preserve the rule that knew what support should have looked like;
- make the claim inventory-visible in unsupported or missing-support views;
- make it response-visible only with explicit caveats, such as "no matching
  support in the observed scope";
- not project the claim as a durable accepted fact;
- not project repository-wide absence unless acquisition scope explicitly
  supports negative evidence;
- not treat the claim as false.

### `contradicted` / current `potential_conflict`

Seed's current fixture-level vocabulary usually has `potential_conflict`, not a
definite `contradicted` outcome. `potential_conflict` behavior should be:

- project the documentation claim as a claim that exists;
- project the conflict signal as potential conflict, not definite
  contradiction;
- link the artifact facts that triggered the conflict signal;
- make the claim inventory-visible in conflict/review views;
- make it response-visible with careful wording such as "artifact facts may
  conflict with this claim";
- never project the claim as false solely from `potential_conflict`;
- never project the artifact fact as a policy violation or architecture error
  unless a stronger rule defines that outcome.

If future alignment adds `contradicted`, behavior should be stronger but still
not truth arbitration:

- project the claim as contradicted-by-rule within scope;
- link the contradicting artifact facts and rule;
- exclude it from accepted projected self-model assertions unless the assertion
  is phrased as "documentation claim exists but is contradicted";
- make it highly visible in inventory and response caveats;
- do not delete the claim, delete artifact facts, choose a winner, or rewrite
  history.

### `not_evaluable`

`not_evaluable` behavior should be:

- project the documentation claim as a claim that exists if the claim itself was
  acquired;
- project the alignment status as not evaluable;
- preserve the rule family or unsupported-pattern reason;
- make it inventory-visible as a non-evaluable claim;
- make it response-visible only as a limitation, not as unsupported or false;
- not count it as missing support;
- not infer repository absence;
- not infer future support or contradiction.

## 7. Worked examples

### Example A: supported ToolExecutor execution claim

Input records:

```text
RepositoryArtifactFact:
    Class ToolExecutor exists.

DocumentationClaim:
    ToolExecutor executes registered operations.

Alignment:
    supported
```

Current documentation caveat: the canonical recognized ownership wording is
closer to:

```text
ToolExecutor owns registered-operation execution.
```

The wording "executes registered operations" should be projected as supported
only if documentation extraction or reconciliation explicitly normalizes it into
a recognized claim family/rule. Without that explicit rule, it should be absent
from reconciliation or `not_evaluable`.

If an explicit rule returns `supported`, projection should project:

- the documentation claim record: documentation says ToolExecutor executes or
  owns registered-operation execution;
- the repository artifact fact: ToolExecutor exists in the observed repository
  scope;
- the alignment status: the claim is supported by the ToolExecutor rule;
- the link from the alignment to the ToolExecutor artifact fact;
- the rule id and source/provenance metadata;
- inventory grouping as supported-by-rule.

Projection should not project:

- "ToolExecutor executes registered operations" as a verified behavioral fact;
- approval authority;
- runtime call-flow proof;
- policy permission;
- repository-wide completeness;
- truth beyond the explicit alignment rule.

What remains alignment metadata:

- `rule_id` as rule provenance;
- `reason` as human-readable explanation;
- the fact that support was decided by a narrow rule over supplied facts;
- caveats about behavior not being proven by class existence alone.

### Example B: unsupported ToolExecutor approval-management claim

Input records:

```text
DocumentationClaim:
    ToolExecutor manages approvals.

Repository support:
    none

Alignment:
    unsupported
```

Current vocabulary caveat: with current rules, this exact claim is more likely
`not_evaluable` unless a future approval-management rule recognizes it. It would
be `missing_support` only if a rule explicitly defines expected approval
management support and then finds none.

If a future explicit rule returns `missing_support` / `unsupported`, projection
should project:

- the documentation claim exists;
- the alignment status is unsupported / missing support within the supplied
  scope;
- the rule that expected support;
- source/provenance and acquisition scope;
- inventory grouping under unsupported or missing-support claims.

Projection should not project:

- ToolExecutor manages approvals as accepted projected knowledge;
- ToolExecutor does not manage approvals as a repository-wide negative fact;
- a policy boundary violation;
- a runtime behavior claim;
- a recommendation to change code or documentation.

Inventory-only implications:

- The claim should be visible in unsupported/missing-support inventory.
- It may be visible in claim inventory with claim text, source, family, rule,
  outcome, and absence scope.
- It should not appear in a supported capability/ownership inventory as an
  accepted responsibility.

Response-only implications:

- A response may say: documentation contains an approval-management claim, but
  Seed has no matching repository support in the observed scope under the
  relevant rule.
- A response must not say the claim is false unless a future contradiction rule
  and evidence support that exact wording.

If current rules return `not_evaluable`, then the inventory and response should
say not evaluable rather than unsupported.

### Example C: repository artifact removed while existing claim remains

Input condition:

```text
Repository artifact removed.
Existing claim remains.
Alignment:
    contradicted or unsupported
```

Current vocabulary caveat: current alignment would normally report
`missing_support` for a recognized existence, ownership, or structure claim when
no matching artifact fact is supplied. It would report `potential_conflict` only
for claim families whose rule treats a matching artifact as conflicting, such as
rejected-concept or frontier claims. A definite `contradicted` outcome is not yet
part of the fixture-level alignment vocabulary.

Projected state behavior should be:

- keep the documentation claim visible as a documentation claim until
  documentation acquisition removes or supersedes it;
- project the absence of a matching artifact only as missing support within the
  observed acquisition scope;
- if a future explicit negative-evidence or contradiction rule exists, project
  contradicted-by-rule rather than deleting the claim;
- never silently turn artifact removal into documentation deletion;
- never silently turn missing support into repository-wide non-existence;
- retain provenance and scope so readers can distinguish "not observed in this
  fixture" from "removed from a repository-wide observed scope."

Inventory behavior should be:

- show the claim in unsupported/missing-support or contradicted inventory;
- show the previous artifact fact as stale, absent from latest projection, or
  superseded only if the event/projection model explicitly represents that
  lifecycle;
- avoid using `superseded` for facts or alignments unless a future self-model
  lifecycle contract defines it, because current state docs reserve explicit
  supersession language narrowly in other domains;
- show acquisition scope and latest observation metadata where available.

Stale/supersession behavior should be:

- stale is appropriate only when evidence/fact expiry or freshness metadata says
  the record is stale;
- supersession is not currently a general fact/support/alignment lifecycle;
- removal from current repository observation should affect current support, not
  rewrite historical claims or facts;
- future implementations need explicit lifecycle semantics if they want to mark
  claims, artifact facts, or alignment records as superseded.

## 8. Inventory and response implications

### What becomes durable projected state?

Durable projected self-model state should include current read-model records for:

- documentation claims that were acquired;
- repository artifact facts that were acquired;
- evidence/provenance for those claims and facts;
- alignment records or equivalent alignment views;
- rule/outcome metadata;
- links from alignment records to claim and artifact-fact records;
- acquisition scope and freshness metadata where available.

The durable projected state should phrase supported claims as supported claims,
not as unqualified implementation truth.

### What remains reconciliation metadata?

The following remain reconciliation metadata, even when projected for
traceability:

- `rule_id`;
- `reason`;
- rule-family eligibility;
- supplied fact-set scope;
- matching details;
- unsupported-pattern explanations;
- caveats that support is narrow, fixture-scoped, or absence-based.

Metadata can be inventory-visible and response-visible, but it should not be
promoted into independent facts unless a future event/schema explicitly stores it
as such.

### What becomes inventory-visible?

Inventory views should be able to show:

- all acquired claims;
- all observed repository artifact facts;
- alignment status per claim;
- supporting or conflicting artifact facts per alignment;
- unsupported / missing-support claims;
- potential-conflict or contradicted-if-added claims;
- not-evaluable claims;
- rule id;
- source path, heading, artifact path, symbol, artifact kind, parent symbol;
- acquisition scope;
- stale or freshness caveats if the underlying records carry them.

Inventory views should not show unsupported or contradicted claims as accepted
self-model truths.

### What becomes response-visible?

Response surfaces may use selected inventory/projected records to answer:

- What does Seed claim about itself?
- What repository artifacts did Seed observe?
- Which claims are supported by observed artifacts?
- Which claims lack support in the observed scope?
- Which claims may conflict with observed artifacts?
- Which claims are not evaluable under current rules?
- Why did this alignment outcome occur?

Response wording must preserve the difference between:

- documentation claim;
- repository artifact fact;
- support relationship;
- alignment outcome;
- projected current state;
- truth;
- behavior;
- policy authority;
- provider capability;
- runtime execution.

### What should never be projected?

Projection should never project these as self-model knowledge from alignment
alone:

- documentation claims as implementation truth;
- class/module existence as behavioral execution proof;
- missing support as falsehood;
- fixture-level absence as repository-wide absence;
- `potential_conflict` as definite contradiction;
- `supported` as verified truth;
- `reason` text as parsable facts;
- rule names as architecture requirements;
- response wording as knowledge creation;
- policy approvals or provider capabilities;
- automatic code/documentation change recommendations;
- hidden inferences that collapse acquisition, reconciliation, and projection.

## 9. Remaining ambiguities

The current documentation already implies the handoff, but it leaves several
semantic details under-specified for consistent future projection implementation:

1. **Projectable status vocabulary.** Current alignment uses `missing_support`
   and `potential_conflict`; the audit vocabulary uses `unsupported` and
   `contradicted`. A future contract should either retain current terms or define
   explicit aliases/mappings without changing semantics accidentally.

2. **DocumentationClaim as fact or view.** The architecture says facts enter
   projection and claims receive support, but self-model docs often expose
   `DocumentationClaim` directly. Future projection needs to say whether a
   `DocumentationClaim` is itself the durable projected record, a typed view over
   a documentation-claim fact, or both.

3. **RepositoryArtifactFact as canonical fact or view.** Current fixture records
   treat it as the fact. The broad architecture could also treat it as a typed
   view over ordinary fact predicates. Future projection should choose one
   representation boundary.

4. **AlignmentRecord as fact, relationship, issue, or read view.** Existing docs
   describe it as reconciliation state and self-model input, but not whether the
   projected form is stored as a fact, specialized relationship, issue-like
   integrity record, or self-model alignment view.

5. **Acquisition scope and negative evidence.** Missing support and
   absence-based support require scope. The exact durable scope fields needed for
   projection and inventory are not yet specified.

6. **Freshness, removal, stale, and supersession lifecycle.** Current state docs
   are careful about expiry and latest-current semantics, but self-model-specific
   claim/artifact/alignment lifecycle terms are not fully specified.

7. **Contradiction semantics.** Current alignment has `potential_conflict`, not a
   strong contradicted outcome. If future docs introduce `contradicted`, they
   must define stronger evidence requirements and projection behavior.

8. **Accepted projected knowledge wording.** The docs need a compact rule for
   how a supported claim may be worded in inventory/response without implying
   verified truth.

9. **Inventory schema.** Inventory concepts are clear, but the self-model
   inventory row fields and grouping rules are not canonical.

10. **Response caveat policy.** Response should preserve caveats, but the exact
    wording policy for supported, missing-support, potential-conflict,
    contradicted, and not-evaluable self-model claims is not centralized.

## 10. Non-goals

This reconciliation does not:

- implement a projection engine;
- implement a projection store;
- modify projection schemas;
- modify event schemas;
- redesign `AlignmentRecord`;
- add new status values;
- rename current status values;
- implement repository-wide observation;
- implement negative-evidence semantics;
- implement response composition;
- add inventory routes or CLI commands;
- modify runtime behavior;
- modify ToolExecutor behavior;
- call providers;
- change policy behavior;
- decide truth;
- adjudicate documentation versus code;
- create a `SelfModelEngine`, `ProjectionEngine`, `TruthEngine`, `ClaimStore`, or
  `SupportStore`.

## 11. Rejected solutions

### Collapse alignment into projection truth

Rejected. Alignment outcomes are rule-bound reconciliation records. Projection
may expose them, but must not convert `supported` into global truth or convert
`missing_support` into falsehood.

### Treat `AlignmentRecord.reason` as data

Rejected. `reason` is human-readable explanation. Parsing it would create a
hidden schema and invite projection to infer facts that rules did not produce.

### Add a new handoff object before documenting semantics

Rejected. Names such as `ProjectionCandidate`, `ProjectableAlignment`, or
`ProjectionEligibility` may be useful later, but they do not solve the current
semantic ambiguity by themselves. The smallest needed step is a semantic contract
for existing `AlignmentRecord` fields.

### Collapse acquisition, reconciliation, and projection

Rejected. Documentation Observation, Repository Observation, Reconciliation, and
Projection answer different questions. Collapsing them would allow documentation
claims, repository facts, and alignment outcomes to masquerade as one another.

### Use response as projection

Rejected. Response can report selected projected knowledge, caveats, and
limitations. It must not create knowledge, mutate projection, or become the place
where unsupported claims are silently accepted or rejected.

### Use inventory as truth arbitration

Rejected. Inventory views group and expose projected records. They do not decide
which claim wins, whether code is wrong, or whether documentation is authoritative.

### Introduce definite contradiction without stronger rules

Rejected. Current `potential_conflict` intentionally avoids definite
contradiction. A `contradicted` state requires explicit stronger evidence and
rule semantics.

### Treat missing artifact as repository-wide removal

Rejected. Missing support is scoped to supplied facts unless acquisition scope
establishes repository-wide observation and negative-evidence semantics.

## 12. Direct answer

Seed partially defines a semantic handoff between alignment/reconciliation
outputs and projected self-model state.

The implicit contract is already visible:

```text
DocumentationClaim + RepositoryArtifactFact set
        ↓ explicit reconciliation rule
AlignmentRecord(claim, artifact_facts, outcome, rule_id, reason)
        ↓ projection / inventory / response selection
self-model view of claims, artifacts, support, alignment, and caveats
```

That is sufficient to understand the fixture-level architecture and to avoid the
most dangerous collapses:

- documentation claims are not repository facts;
- repository artifact facts are not architectural truth;
- alignment outcomes are not truth values;
- projection should expose current self-model read views, not create claims;
- inventory and response should preserve support, uncertainty, scope, and
  limitation metadata.

However, Seed's projection handoff is not yet sufficiently specified for future
projection implementations to be built consistently without one more small
semantic contract.

The smallest remaining semantic contract required between `AlignmentRecord` and
projected self-model state is:

```text
AlignmentRecord is the canonical typed handoff from reconciliation to self-model
projection. Projection may persist or derive read views from its claim,
artifact_facts, outcome, rule_id, and provenance/scope references. The claim,
artifact_facts, outcome, and rule_id are authoritative only as reconciliation
state within the explicit rule and acquisition scope. The reason is explanatory
only. Projection must represent supported, missing-support/unsupported,
potential-conflict/contradicted-if-added, and not-evaluable outcomes as alignment
status, not as truth, behavior, policy authority, repository-wide absence, or
automatic correction.
```

No new engine, store, or vocabulary is required to state that contract. Future
implementation work can then choose concrete projection schemas and inventory
views while preserving the existing acquisition/reconciliation/projection
separation.
