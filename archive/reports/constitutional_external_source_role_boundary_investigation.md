# Constitutional External Source Role Boundary Investigation

## Boundary

This document performs exactly one bounded constitutional investigation:

```text
source role != source truth
```

It investigates the constitutional boundary around external source roles for a possible future in which a human provides public-world evidence packets.

This is not world ingestion. It is not legal research. It is not a source-scoring system. It does not rank publishers, create reliability weights, assign legal authority, define a public-world ontology, implement evidence ingestion, add diagnostics, mutate the event ledger, or promote external vocabulary into repository knowledge.

Repository authority wins.

## Bounded question

When future Seed receives human-provided public-world evidence packets, what constitutional work, if any, distinguishes external source roles such as:

```text
reported claim / primary account / official statement / secondary analysis / contextual background / corroborating source / contradictory source
```

without treating role labels as truth, volume as authority, visibility as fact, repetition as proof, confidence as certainty, or narrative as history?

## App-visible evidence used

The app was used as a read-only authority check, not as a public-world source and not as a source-role oracle.

Reviewed command:

```text
python -m scripts.seed_local --documentation-structure --recurrence --limit 10 --top 10
```

App-visible finding:

- The app reported 577 Markdown documents and recurring review section labels including `Purpose`, `Non-Goals`, `Conclusion`, `Files inspected`, `Supported conclusions`, `Unsupported conclusions`, `Scope`, and `Central Finding`.
- The app boundary stated that this mode is read-only, observes structural recurrence only, performs no prose interpretation, no claim extraction, no authority inference, no shape inference, no ontology promotion, no event-ledger writes, and no repository mutation.

This app evidence is useful only for discipline: it confirms that a visible structure or repeated label can be observed without becoming interpreted truth, authority, ontology, or mutation.

## Repository evidence reviewed

Review was limited to already present repository artifacts that bear on evidence, warrant, source-local authority, observation, narrative/history separation, temporal authority, and bounded lawful relation:

- `constitutional_warrant_characterization.md`
- `constitutional_sentence_investigation.md`
- `constitutional_narrative_history_boundary_investigation.md`
- `constitutional_repetition_proof_boundary_investigation.md`
- `constitutional_boundary_confusion_competency_audit_review.md`
- `constitutional_lawful_acceptance_characterization.md`
- `constitutional_reliance_characterization.md`
- `constitutional_observation_characterization.md`
- `constitutional_local_grammar_recovery_characterization.md`
- `constitutional_temporal_topology_survey.md`
- `constitutional_district_purpose_cross_examination.md`
- `constitutional_work_over_time_frontier_survey.md`
- implementation-adjacent source/evidence surfaces where relevant, especially `seed_runtime/observations.py`, `seed_runtime/evidence_graph.py`, and `seed_runtime/source_navigation.py`

## Central finding

External source roles are constitutionally useful only as **warrant-bounding provenance roles**.

A source role may tell future Seed how a human-provided evidence packet is allowed to be considered:

```text
what kind of support this packet claims to be
what claim form it can support
which authority boundary must remain attached
which negative authority blocks overuse
what unknowns and confidence limits must survive
where later reliance must stop
```

A source role does **not** itself tell Seed that the packet is true, current, authoritative for Seed, legally controlling, historically complete, implementation-relevant, or sufficient for ingestion.

The constitutional distinction is therefore not a score and not a hierarchy. It is a boundary-preserving role declaration that constrains later evidence binding, warrant, reliance, contradiction handling, and lawful stop.

## Source-role distinctions that survive repository authority

### 1. Reported claim

A reported claim is material asserted by the source or by someone represented in the packet.

Constitutional work:

- preserve the assertion as source-attributed;
- preserve speaker/source, subject-as-reported, time/preservation context where available, scope, and confidence limits;
- keep the asserted content below truth, fact, history, and implementation authority unless a competent repository boundary later admits it for a narrower role.

Negative authority:

- reported claim != verified fact;
- reported claim != world truth;
- reported claim != Seed-local history;
- reported claim != permission to project or mutate.

### 2. Primary account

A primary account is closer to the event, decision, artifact, or actor being described, but closeness is not proof.

Constitutional work:

- preserve vantage point and claimed proximity;
- distinguish firsthand/source-local authority from repository authority;
- allow later review to ask whether the account is admissible for a bounded claim form;
- preserve limitations such as partial perspective, self-interest, missing context, or uncertain timestamp.

Negative authority:

- primary account != complete history;
- primary account != automatic authority for all claims inside it;
- primary account != contradiction resolution by proximity alone.

### 3. Official statement

An official statement is a source-local authority claim: it may show what an institution, office, project, or actor publicly said or published under its own authority.

Constitutional work:

- preserve the asserted official capacity and source-local scope;
- distinguish authority to speak for the source from authority to establish external truth;
- allow bounded reliance on the existence/content of the statement when provenance is preserved;
- keep legal, regulatory, operational, or implementation effect outside scope unless separately supported.

Negative authority:

- official statement != truth oracle;
- official statement != legal conclusion;
- official statement != Seed acceptance;
- official statement != authority outside the issuing source's bounded role.

### 4. Secondary analysis

Secondary analysis interprets, summarizes, evaluates, or narrates other material.

Constitutional work:

- preserve it as interpretation or analysis rather than event evidence;
- capture the dependency on cited or unstated underlying sources where visible;
- use it, if at all, for possible framing, candidate questions, or bounded explanation support;
- refuse to let fluent narrative replace source evidence or temporal provenance.

Negative authority:

- secondary analysis != primary evidence;
- narrative coherence != history;
- expert confidence != certainty;
- summary != underlying record.

### 5. Contextual background

Contextual background may help interpret terms, chronology, institutions, or prior conditions, but it does not prove the target claim merely by being useful.

Constitutional work:

- preserve background as scope-setting or orientation material;
- keep it separate from direct support for the target claim;
- require explicit movement before background can become evidence for a specific bounded claim;
- preserve unknowns when context is incomplete, stale, jurisdiction-limited, domain-limited, or only broadly similar.

Negative authority:

- context != support for every adjacent claim;
- relevance != proof;
- useful orientation != repository knowledge;
- background narrative != event history.

### 6. Corroborating source

A corroborating source independently supports some bounded part of a claim, but corroboration depends on what overlaps and whether independence survives review.

Constitutional work:

- preserve the exact overlap being corroborated;
- preserve whether the sources appear independent, derivative, common-sourced, or unknown;
- distinguish agreement evidence from truth promotion;
- refuse volume-based authority when many packets repeat the same unsupported source or phrase.

Negative authority:

- corroboration != proof;
- repetition != proof;
- volume != authority;
- agreement on one detail != validation of all details.

### 7. Contradictory source

A contradictory source challenges, limits, or conflicts with a claim, but contradiction does not automatically prove the opposite.

Constitutional work:

- preserve the exact conflicting assertion, scope, timing, and source role;
- mark the affected claim as disputed, limited, stale, ambiguous, or unknown where warranted;
- force lawful stop when evidence is insufficient to resolve the conflict;
- keep contradiction visible to downstream reliance.

Negative authority:

- contradiction != automatic disproof;
- later source != automatically better source;
- conflict visibility != resolution;
- unresolved conflict != permission to pick the preferred narrative.

## What source roles are not

Source roles are not:

- a source-scoring system;
- a hierarchy where `official` always beats `secondary` or `primary` always beats `contextual`;
- legal research or public-world truth adjudication;
- ingestion permission;
- fact promotion;
- event-ledger history;
- current-world freshness;
- certainty calibration by label alone;
- a substitute for provenance, support path, contradiction handling, or local authority.

## Relationship to recovered boundary-confusion constraints

The recent boundary-confusion constraints are preserved as follows:

- **Evidence != Vibes.** A source role must attach to a concrete packet and support path, not a feeling that a source seems credible.
- **Authority != Volume.** More packets do not expand authority unless their provenance and independent support warrant a bounded movement.
- **Visibility != Truth.** A visible public-world packet remains visible material until a competent boundary admits it for a role.
- **Repetition != Proof.** Repeated claims may show recurrence, syndication, or common sourcing; they do not prove the target claim by repetition alone.
- **Confidence != Certainty.** Confidence is a calibrated limit on reliance, not a conversion into truth.
- **Narrative != History.** A coherent account over packets is not the event history or temporal provenance it describes.

## Lawful use pattern for future evidence packets

A future Seed should treat a human-provided public-world evidence packet as constitutionally usable only through a pattern like:

```text
packet preserved with provenance
-> source role declared or recovered as candidate role
-> bounded claim form identified
-> support/authority/negative-authority/unknowns preserved
-> contradictions and dependencies checked where available
-> warrant, limited reliance, or lawful stop emitted by a competent boundary
```

The source role participates in this pattern by narrowing what kind of support may be considered. It does not perform the movement by itself.

## Supported conclusions

1. External source roles are constitutionally meaningful as role-bound provenance and warrant constraints.
2. The same packet may carry multiple roles for different bounded claims: for example, an official statement can be primary evidence of what an office said while remaining weak evidence of whether the statement is true.
3. Role labels must preserve negative authority: no source role automatically creates truth, fact, ingestion, projection, mutation, legal conclusion, or implementation pressure.
4. Corroboration and contradiction are relation roles, not source ranks. They require exact overlap, scope, dependency, and conflict preservation.
5. Context and secondary analysis may lawfully orient review, but they must not silently become direct proof of the target claim.
6. The useful constitutional distinction is claim-form-specific lawful reliance, not source scoring.

## Unsupported conclusions

1. Unsupported: Seed should rank public-world sources by source role.
2. Unsupported: official statements are always controlling for truth.
3. Unsupported: primary accounts always outrank secondary analysis.
4. Unsupported: many reports make a claim authoritative.
5. Unsupported: future Seed should ingest public-world packets into facts merely because a role is present.
6. Unsupported: public-world source roles create legal, historical, or implementation authority without separate repository-supported movement.

## Unknowns preserved

- What concrete packet schema, if any, future Seed may implement.
- Whether source roles should be user-declared, locally recovered, or both.
- Which future boundary, if any, would admit public-world packets into observations, evidence, facts, diagnostics, or review-only artifacts.
- How independence among public-world sources would be represented if implementation ever exists.
- How freshness, jurisdiction, publication revision, archival capture, and retraction would be preserved.
- Whether any public-world source role vocabulary should become stable repository vocabulary.

## Confidence

Confidence is **medium-high** that repository evidence supports source roles as warrant-bounding provenance roles and rejects source roles as truth, rank, scoring, ingestion, legal, or implementation authority.

Confidence is **medium** in the candidate role list because the exact vocabulary is task-local and not recovered as stable repository ontology.

## Lawful stop

Stop here. The investigation clarifies the constitutional boundary only. It does not ingest world evidence, perform legal research, define a scoring model, add an implementation surface, or require future Seed to adopt these labels as canonical vocabulary.
