# Contradiction Discovery and Visibility Reconciliation

## Purpose

This document performs a documentation-only reconciliation of contradiction
existence, contradiction discovery, contradiction visibility, contradiction
projection, contradiction explanation, and contradiction resolution boundaries.
It is an architectural boundary audit.

It does not implement code, modify schemas, change runtime behavior, alter
observations or evidence handling, change claim/event/projection/integrity
systems, change trust or authority behavior, alter reconciliation behavior, or
add tests.

## Summary Finding

Contradiction existence, discovery, visibility, projection, explanation, and
resolution are distinct architectural concepts.

A contradiction may exist in preserved knowledge before any projection,
assessment, operator, integrity process, relationship analysis, identity
clarification, or reconciliation workflow becomes aware of it. Discovery exposes
that already-present incompatibility. Projection may then choose whether and how
to show it. Explanation accounts for the incompatible support paths. Resolution
selects, qualifies, retires, supersedes, or otherwise handles the contradiction
without erasing the preserved history that made the contradiction explainable.

The core boundary is:

```text
Contradiction Exists
        ↓
Later Discovery
        ↓
Later Projection / Visibility
        ↓
Optional Explanation
        ↓
Optional Resolution
```

Discovery is not creation. Projection is not existence. Visibility is not truth.
Resolution is not erasure.

## Files Considered

This reconciliation builds on the existing architecture and adjacent
reconciliations, especially:

- `docs/contradiction_handling_audit.md`
- `docs/learning_and_knowledge_change_reconciliation.md`
- `docs/causality_and_explanation_reconciliation.md`
- `docs/operator_interface_and_projection_authority_reconciliation.md`
- `docs/read_model_inventory_and_authority_reconciliation.md`
- `docs/evidence_trust_and_source_authority_reconciliation.md`
- `docs/event_and_change_reconciliation.md`
- `docs/relationship_fact_reconciliation.md`
- `docs/why_not_explanation_characterization.md`
- `docs/why_not_vocabulary.md`
- `docs/state.md`

## Boundary Summary

| Concept | Architectural definition | What owns it? | What it is not |
| --- | --- | --- | --- |
| Contradiction | Coexistence of preserved claims that cannot all be accepted together within a relevant identity, predicate, value, dimension, time, scope, or authority boundary. | Preserved knowledge plus the semantics needed to compare claims. | Not automatically an error, winner selection, operator-visible warning, or resolution. |
| Contradiction existence | The latent or explicit property that incompatible preserved claims are present in Seed's knowledge. | Knowledge representation, claim preservation, identity/scope semantics, and predicate semantics. | Not a projection artifact and not dependent on current visibility. |
| Contradiction discovery | The act of recognizing that preserved claims are incompatible under some comparison boundary. | Assessment, interpretation, integrity analysis, projection logic, relationship analysis, identity clarification, or reconciliation review. | Not necessarily a new observation and not creation of the contradiction. |
| Contradiction visibility | Whether a discovered or discoverable contradiction is exposed to an operator, API, explanation, audit, projection, handoff, or response. | View, surface, projection, response, and operator-interface policy. | Not truth, not existence, and not resolution. |
| Contradiction projection | A read-model or view decision to compute, select, format, summarize, suppress, caveat, or expose contradiction information from preserved knowledge. | Projection and view layers. | Not mutation of claims and not creation of the underlying contradiction. |
| Contradiction explanation | An account of why claims are in tension, including preserved support paths, evidence, provenance, authority, scope, and selection rationale. | Explanation layer over preserved knowledge and projections. | Not causality itself and not automatic resolution. |
| Contradiction resolution | A later handling decision that selects, qualifies, supersedes, retracts, scopes, or otherwise reconciles incompatible claims for a purpose while preserving provenance. | Reconciliation, authority, lifecycle, or explicit resolution policy. | Not discovery, visibility, projection, or deletion of history. |

## 1. What Is a Contradiction?

A contradiction is the coexistence of two or more preserved claims that cannot
all be accepted together under the same relevant comparison boundary.

The comparison boundary may include:

- identity: whether two claims are about the same subject after identity or alias
  interpretation;
- predicate: whether the claims assert the same or mutually exclusive property;
- value: whether the asserted values are incompatible;
- dimensions: whether dimensions such as environment, namespace, region,
  interface, or source scope make the claims comparable;
- time: whether the claims are simultaneous current-state assertions,
  historical assertions, measurements, or superseded states;
- authority: whether a claim is asserted as local evidence, foreign testimony,
  operator input, inference, import, or policy-backed selection;
- cardinality: whether the predicate permits multiple coexisting values;
- lifecycle state: whether a claim is active, expired, retracted, superseded, or
  preserved only as history.

For example:

```text
Claim A: host115 owner = TeamA
Claim B: host115 owner = TeamB
```

These claims are contradictory if all of the following are true for the relevant
architectural comparison:

1. `host115` resolves to the same subject;
2. `owner` is treated as single-cardinality or otherwise mutually exclusive in
   the relevant scope;
3. `TeamA` and `TeamB` are distinct incompatible values;
4. the dimensions do not separate the claims into different scopes;
5. the time and lifecycle treatment make both claims relevant to the same
   comparison;
6. neither claim is merely quoted, historical, withdrawn, or otherwise scoped so
   that it no longer competes with the other for that comparison.

The contradiction is not created by an operator seeing it, by a read model
surfacing it, or by an explanation describing it. Those actions may discover,
project, or explain the contradiction, but the incompatibility arises from the
preserved claims and the semantics that make them comparable.

## 2. What Is Contradiction Existence?

Contradiction existence is the presence of incompatible preserved claims within a
relevant semantic boundary.

It is primarily a property of preserved knowledge, not a projection artifact. The
claims and their support paths may already be present before any contradiction
view or audit identifies them. Existence depends on claim preservation plus the
semantic rules needed to compare claims, such as identity, predicate cardinality,
dimensions, authority, and time.

Existence can be latent. Seed may preserve two claims whose incompatibility is
not yet known because:

- identity has not yet been clarified;
- an alias has not yet been resolved;
- a predicate has not yet been classified as exclusive;
- support has not yet been reclassified;
- an imported claim has not yet been interpreted in local scope;
- a relationship analysis has not yet connected relevant entities;
- a projection has not yet computed that comparison;
- the contradiction is outside the currently selected view.

Latent existence does not mean the architecture has failed. It means preserved
knowledge can contain incompatibility before the system has selected, examined,
or exposed the comparison that reveals it.

## 3. What Is Contradiction Discovery?

Contradiction discovery is the recognition that preserved claims are
incompatible under a comparison boundary.

Discovery may be performed by:

- projection logic that groups comparable claims;
- integrity analysis that audits preserved facts, evidence, and support;
- relationship analysis that connects claims across related entities;
- identity clarification that determines two subjects are the same subject;
- support reclassification that changes whether a claim is treated as evidence,
  testimony, inference, import, or current support;
- predicate or dimension interpretation that makes claims comparable;
- operator investigation that notices incompatible preserved claims;
- explanation generation that assembles competing support paths;
- reconciliation review that evaluates current-state selection against history.

Discovery is not necessarily observation. A new observation may discover a
contradiction, but discovery can also occur entirely over existing preserved
claims. If Seed already contains `host115 owner = TeamA` and `host115 owner =
TeamB`, a later projection redesign or identity clarification can discover the
contradiction without observing anything new about `host115`.

Discovery is also not creation. Discovery changes what Seed or an operator knows
about the preserved knowledge; it does not necessarily add the incompatible
claims that made the contradiction possible.

## 4. What Is Contradiction Visibility?

Contradiction visibility is whether a contradiction is exposed through a
particular surface, view, projection, explanation, audit, handoff, or response.

Visibility is distinct from discovery:

```text
Contradiction exists.
Contradiction has been discovered by an integrity audit.
The current operator view does not show that audit result.
```

In that example, the contradiction exists and has been discovered, but it is not
currently visible to the operator. Conversely, a contradiction may be visible in
an audit report but omitted from a compact operational summary because the
summary is scoped to selected current state.

Visibility depends on audience and surface responsibilities, such as:

- whether the view is current-state, historical, integrity-oriented, or
  explanation-oriented;
- whether the operator requested conflicts, caveats, or support details;
- whether the projection is compact or diagnostic;
- whether the response boundary permits uncertainty disclosure;
- whether the handoff format includes unresolved contradictions;
- whether privilege, safety, or relevance rules constrain what is shown.

Visibility is not truth. A visible contradiction is not proof that one claim is
false. A hidden contradiction is not proof that no contradiction exists.
Visibility is a presentation and selection property, not an ontological or truth
property.

## 5. What Is Contradiction Projection?

Contradiction projection is the act of deriving, selecting, shaping, or exposing
contradiction information in a read model or view.

Projection may:

- group comparable claims;
- select the comparison boundary;
- exclude expired or historical claims for a current-state view;
- include historical claims for an audit view;
- attach competing fact identifiers;
- summarize values and reasons;
- include or omit evidence details;
- compute severity or caveats for the view;
- choose a winning current value for one purpose while still showing conflict;
- suppress contradiction details in a surface that is not responsible for them.

Projection differs from existence because projection is derived from preserved
knowledge. If the incompatible claims already exist, a projection that exposes
them reveals the contradiction rather than creating it.

Projection also differs from resolution. A projection may show a selected current
value, best-supported value, or current belief while retaining competing claims
and support. Selection for display or operational use is not elimination of the
unselected claims, and it is not a final truth decision unless an explicit
resolution policy says so.

## 6. What Is Contradiction Explanation?

Contradiction explanation is an account of why claims are incompatible and why a
particular surface is reporting, selecting, caveating, or not selecting them.

A contradiction explanation should preserve and expose, as appropriate for the
surface:

- the competing claims;
- the subject identity or relationship path that made the claims comparable;
- the predicate and dimension boundary;
- the incompatible values;
- the source and authority classification of each claim;
- the evidence records or observations supporting each claim;
- fact/support identifiers needed to trace the support path;
- event or import provenance where available;
- confidence, freshness, or expiry caveats if relevant;
- lifecycle state such as retracted, superseded, expired, current, or historical;
- the projection or view rule that made the contradiction visible;
- any selection rationale if a current value is shown.

The explanation should be able to distinguish:

```text
why TeamA was previously selected
why TeamB is now selected
why both support paths still exist
why the earlier support is not erased
why the disagreement is reported as contradiction, ambiguity, stale support,
foreign testimony, or historical disagreement
```

Explanation is distinct from causality. An explanation may include causal
context, but its architectural responsibility is to make the represented support
and selection path intelligible. It should not invent causal claims merely
because two claims conflict.

## 7. What Is Contradiction Resolution?

Contradiction resolution is the handling of incompatible claims for a purpose.
It may select, qualify, scope, supersede, retract, reject, archive, or otherwise
reconcile claims while preserving the provenance and history required to explain
what happened.

Resolution differs from existence because existence only means incompatible
claims are present. Resolution differs from discovery because discovery only
recognizes the incompatibility. Resolution differs from projection because
projection may expose or select from the contradiction without authoritatively
settling it.

Resolution may take several forms:

- selecting a current owner while preserving prior ownership claims;
- scoping one claim to `staging` and another to `production`;
- clarifying that two host identifiers were different subjects;
- marking one imported claim as foreign testimony rather than local evidence;
- treating an older claim as superseded but historically valid;
- recording a source retraction;
- preserving both claims as unresolved if no authority can decide;
- escalating the contradiction to an operator or integrity workflow.

Resolution should not erase contradiction history. If Seed once preserved
competing support for `host115 owner = TeamA` and `host115 owner = TeamB`, later
resolution should retain enough provenance to explain the prior contradiction,
the basis for resolution, and why any unselected claim is no longer current for
the relevant purpose.

## 8. Can Contradiction Exist Without Discovery?

Yes. The architecture supports contradiction existence without discovery.

```text
Contradiction Exists
        ↓
Later Discovery
        ↓
Later Projection
```

This follows from preserved knowledge being richer than any single current view.
Seed may preserve claims before running the comparison that would identify them
as incompatible. The contradiction exists as a latent property once the
incompatible claims and relevant semantics are present, even if no surface has
reported it.

Examples:

- two claims about the same host owner exist before aliases reveal that the host
  identifiers refer to the same machine;
- a predicate is later classified as single-cardinality;
- two imported claims are later interpreted as local current-state claims rather
  than quoted foreign assertions;
- relationship analysis later determines that two claims affect the same
  dependent entity;
- an integrity audit is introduced that checks a comparison no prior projection
  computed.

## 9. Can Discovery Occur Without New Observations?

Yes. Discovery can occur without new observations.

Discovery can result from reinterpretation, selection, or analysis over already
preserved knowledge. Examples include:

- projection redesign that groups claims differently;
- identity clarification that merges two subjects;
- support reclassification that changes how claims compete;
- relationship analysis that exposes incompatible implications;
- imported claim reinterpretation that changes local scope;
- predicate cardinality clarification;
- dimension normalization;
- authority reassessment;
- explanation generation that assembles support paths not previously shown
  together;
- integrity analysis that runs a new audit over existing claims.

This kind of discovery may still count as learning. Seed learns something about
its represented knowledge even though it did not observe a new external fact.
The learning is the recognition of incompatibility, not the creation of the
underlying claims.

## 10. What Should Not Be Collapsed Together?

The following distinctions should be preserved.

### Contradiction != Discovery

A contradiction is the incompatible coexistence of claims. Discovery is the
recognition of that incompatibility. Collapsing them would imply contradictions
do not exist until noticed, which would make preserved knowledge dependent on
operator or projection awareness.

### Discovery != Resolution

Discovery identifies a problem or tension. Resolution handles it. Collapsing them
would make every detected contradiction appear solved merely because it was
found.

### Existence != Projection

Existence belongs to preserved knowledge and semantic comparability. Projection
is a derived view. Collapsing them would imply contradictions can be created or
destroyed by changing a surface.

### Projection != Resolution

Projection may select, summarize, or expose a contradiction for a purpose.
Resolution changes the handling status of the contradiction or claims under an
explicit policy. Collapsing them would turn ordinary read-model selection into
truth arbitration.

### Visibility != Truth

Visibility means a surface shows or hides something. Truth concerns whether a
claim is correct. A hidden contradiction may still exist, and a visible
contradiction may still be unresolved.

### Selection != Elimination

Selecting a current value does not delete or invalidate unselected support.
Selection is a view or use decision. Elimination would remove or make knowledge
unavailable.

### Historical Disagreement != Current Contradiction

Two historical claims may disagree without creating a current contradiction if
they refer to different times, scopes, authorities, or lifecycle states. Current
contradiction requires that claims compete within the relevant current comparison
boundary.

### Explanation != Causality

Explanation shows the support, selection, and reasoning path. Causality asserts
that one thing caused another. Contradiction explanations should not imply causal
relationships unless causal support exists.

### Confidence Penalty != Resolution

A confidence projection may lower confidence or flag risk because contradiction
exists, but that does not decide which claim is true or erase the competing
support.

## Support Preservation

Support preservation is required for contradiction explanation, later discovery,
and responsible resolution.

Seed should preserve enough information to reconstruct:

- which claims competed;
- which observations, evidence records, imports, inferences, or events supported
  each claim;
- which authority or source supplied each support path;
- which identity, dimension, predicate, or relationship interpretation made the
  claims comparable;
- which projection or audit surfaced the contradiction;
- which resolution, if any, later changed current-state selection;
- why unselected or superseded claims remain part of history.

Without support preservation, resolution becomes indistinguishable from erasure,
and explanation cannot distinguish stale history, rejected testimony, corrected
identity, supersession, and unresolved contradiction.

## Non-Goals

This reconciliation does not define or require:

- new contradiction schemas;
- new event types;
- new projection stores;
- new runtime behavior;
- automatic contradiction detection beyond existing behavior;
- automatic truth arbitration;
- automatic claim mutation;
- automatic evidence mutation;
- new observation handling;
- new trust or authority semantics;
- new reconciliation workflows;
- new tests;
- a universal contradiction ontology for all possible domains;
- a requirement that every operator surface show every contradiction;
- a requirement that every contradiction be resolved.

## Implementation Implications

Because this is a boundary audit, the primary implication is conceptual rather
than prescriptive: implementation work should preserve the distinction between
existence, discovery, visibility, projection, explanation, and resolution.

If future implementation work is proposed, it should avoid:

- treating projected conflict rows as the only possible existence of
  contradiction;
- treating absence from a view as absence from preserved knowledge;
- treating discovery as a new observation unless a new observation actually
  occurred;
- treating selected current state as deletion of historical alternatives;
- treating explanation output as the authority that resolves contradiction;
- treating resolution as permission to erase provenance;
- merging contradiction, ambiguity, stale support, graph validation issues,
  historical disagreement, and foreign testimony into one undifferentiated
  status.

No implementation work is required by this document unless a future change would
otherwise collapse these boundaries.

## Architectural Invariants

The findings support the following invariants:

1. **Contradiction existence is independent of projection.** A contradiction may
   exist in preserved knowledge before a projection exposes it.
2. **Discovery is not creation.** Discovering incompatibility does not create the
   incompatible claims.
3. **Projection is not resolution.** A projected view may expose or select among
   contradictions without settling them.
4. **Visibility is not truth.** Showing or hiding a contradiction does not decide
   whether any claim is true.
5. **Selection is not elimination.** Choosing a current value does not erase
   competing support.
6. **Resolution should preserve provenance.** Resolution must retain enough
   support history to explain the contradiction and the handling decision.
7. **Contradiction history should survive resolution.** Prior disagreement
   remains part of the knowledge lifecycle even after current state is settled.
8. **Learning may result from contradiction discovery.** Seed can learn from
   recognizing incompatibility in existing preserved knowledge without a new
   external observation.
9. **Support paths should survive projection changes.** A projection redesign may
   expose a contradiction, but support paths should remain traceable to the
   underlying preserved knowledge.
10. **Historical disagreement is not automatically current contradiction.** Time,
    dimensions, lifecycle state, and authority determine whether claims still
    compete.

## Final Reconciliation

Contradiction is an incompatibility among preserved claims within a relevant
semantic boundary. Contradiction existence is the presence of that
incompatibility in preserved knowledge. Contradiction discovery is the later
recognition of the incompatibility. Contradiction visibility is whether a surface
shows it. Contradiction projection is the derived read-model behavior that may
compute or expose it. Contradiction explanation is the support-preserving account
of why the incompatibility is present and how it is selected or caveated.
Contradiction resolution is a later handling decision that may settle current use
without erasing history.

Therefore, Seed's architecture should preserve this chain:

```text
preserved claims
  may contain latent contradiction
    before discovery
      before projection
        before visibility
          before explanation
            before optional resolution
```

The distinctions matter because Seed's knowledge model is historical,
provenance-aware, projection-backed, and explanation-oriented. If existence,
discovery, visibility, projection, and resolution are collapsed, Seed would lose
the ability to explain how it learned, why it selected one view, what support was
preserved, and why current-state selection does not erase history.
