# Candidate Attachment / Repository Participation Audit

## Executive answer

Yes, boundedly: repository evidence already distinguishes **Candidate Attachment** from **Repository Participation**.

The strongest supported model is:

```text
External representation
  -> candidate attachment / local record / bounded observation evidence
  -> admission by an existing bounded owner
  -> only then shared repository participation
```

Attachment itself does not always imply participation in shared repository responsibilities. Participation is admitted by existing implementation boundaries such as observation ingestion, state projection/current-fact selection, provider-specific extraction, exact agreement rules, grammar recurrence rules, read-only audit builders, or explicit promotion-readiness checks. Those owners can also stop locally, preserve unknown/unsupported states, or expose candidate-only output without promotion.

The repository does **not** support a new centralized participation engine, admission service, repository gateway, semantic engine, or implementation recommendation. The evidence supports a recurring boundary, distributed across existing responsibilities.

## Repository evidence reviewed

Reviewed evidence includes:

- `external_representation_repository_attachment_audit.md` as the prior recovery of the external-representation-to-attachment boundary.
- `seed_runtime/observations.py` for canonical `Observation`, observation-to-evidence conversion, optional observation-to-fact promotion, and suppression behavior.
- `seed_runtime/capability_candidates.py` for candidate capability preservation that explicitly is not capability, authority, selection, policy, or execution.
- `seed_runtime/capability_promotion_readiness.py` for a later supported/unsupported readiness inspection that still does not promote or create `capability_verified` facts.
- `tests/test_capability_candidates.py` and `tests/test_capability_promotion_readiness.py` for executable negative evidence that candidates/readiness do not write events, create facts, select capabilities, evaluate policy, or execute tools.
- `seed_runtime/inquiry_orientation.py` and `inquiry_note_artifact_characterization.md` for operator prose preserved outside the event ledger and used only by a read-only lexical orientation surface.
- `seed_runtime/knowledge/observation_agreement.py` for candidate agreement between independent observation streams without semantic interpretation or truth promotion.
- `seed_runtime/knowledge/grammar_observation.py` for recurring relation-shape observation without grammar, lexicon, responsibility, family, semantic, or architectural truth promotion.
- `seed_runtime/selection_path_audit.py` for read-only selection visibility with candidate sets, non-selected alternatives, unknowns, and no ledger/fact/cluster mutation.
- Existing recovery documents around current facts, read models, provider language translation, repository observation, observation agreement, grammar observation, inquiry orientation, selection path, reasoning path, answer composition, observation transition, and repository attachment.

## Implementation evidence

### 1. Canonical observation participates only through ingestion, and fact participation can be suppressed

`Observation` is a canonical external observation that can be converted into a `Fact`. The wording is important: it can be converted, not that every upstream candidate already is a fact or shared truth. `ObservationIngestor.ingest_many(...)` explicitly creates an `observation.observed` event and an `evidence.observed` event for each observation, then creates a `fact.observed` or `fact.inferred` event only when `_should_suppress_fact_promotion(...)` does not return true.

This is direct implementation evidence for a participation boundary:

```text
Observation
  -> observation event / evidence event
  -> optional fact event
```

The special suppression rule for Prometheus `node_uname_info` `os` observations demonstrates that even a canonical observation may participate as observed/evidence material without becoming a fact. That rejects the claim that every attachment immediately becomes full shared repository fact participation.

### 2. Capability candidates are preserved as candidates and explicitly barred from execution participation

`seed_runtime/capability_candidates.py` is unusually explicit. Its module docstring says it preserves evidence-derived capability candidates only, and that a candidate is not a capability, execution authority, execution decision, policy evaluation, or tool invocation. Its boundary notes include:

- `capability_candidate_not_capability`
- `capability_candidate_not_execution_authority`
- `capability_candidate_not_execution_decision`
- `capability_candidate_not_tool_invocation`
- `observed_evidence_not_capability_proof`
- `capability_presence_not_capability_permission`
- `no_capability_selection`
- `no_policy_evaluation`
- `no_tool_execution`
- `read_only_inspection`

`build_capability_candidates(...)` consumes current projected `package_installed` facts and returns a `CapabilityCandidateInspection`. It does not create events, facts, execution proposals, pending actions, or action plans. Tests assert that candidate output is read-only and does not become execution decisions, tool execution, or policy evaluation.

This is one of the strongest counterexamples to Model A. A projected package fact can attach to a possible capability candidate, but the candidate is not admitted into capability, policy, planning, or execution participation.

### 3. Promotion readiness is separate from promotion

`seed_runtime/capability_promotion_readiness.py` adds another step after capability candidate preservation. It joins capability candidates with read-only verification evidence and labels readiness as `supported` only when both candidate support and verification support exist. The module and dataclasses repeatedly state that this remains an inspection only and does not create `capability_verified` facts, select capabilities, evaluate policy, invoke tools, plan, execute, or modify inventory.

The executable test `test_promotion_readiness_does_not_create_capability_verified_facts_or_write_events(...)` proves that even `promotion_readiness == "supported"` does not write new events, mutate facts, or create a `capability_verified` fact. This demonstrates at least three distinct states:

```text
candidate capability
  != readiness supported
  != promoted capability_verified fact / execution participation
```

Therefore participation is separately earned and may still stop before promotion.

### 4. Inquiry notes remain provider-local/read-model-local forever unless another implemented path consumes them

`seed_runtime/inquiry_orientation.py` says inquiry notes are stored outside the event ledger. Rendering reads projected state but never mutates it, appends events, calls providers, executes tools, or creates facts, goals, tool needs, decisions, proposals, or plans. The `AUTHORITY_BOUNDARY` says the inquiry note is preserved operator prose and not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction; matches are deterministic lexical overlaps only and do not assert importance, ownership, intent, concern, recommended action, or next safe move.

This means operator prose may be attached to related material for orientation, but that attachment is provider-local/read-model-local. It is not repository participation as observation, fact, current fact, selection, answer truth, execution, or policy. Existing characterization documents also found no path by which inquiry notes become observations, facts, event-ledger events, claim support, projections, or current facts.

This supports the conclusion that candidate attachments can legitimately remain local forever without architectural failure.

### 5. Observation Agreement admits only candidate agreement, not architectural truth

`observe_observation_agreements(...)` consumes already-observed inputs and emits `ObservationAgreementRecord` only when two or more independent observation streams have exactly equal evidence text after trimming. Its boundary explicitly says it preserves candidate agreement, provenance, and observation independence, while rejecting agreement promotion, grammar ownership, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, runtime mutation, event writes, ledger writes, repository mutation, and cluster mutation.

This is a precise boundary between attachment and participation. The agreement participates only in the Observation Agreement surface as candidate agreement. It is not admitted to shared architectural truth or mutation responsibilities.

### 6. Grammar Observation requires recurrence and still remains non-promotional

`observe_grammar_observations(...)` consumes only `ObservationAgreementRecord` instances. A candidate agreement contributes only when it has one known relation operator and non-empty text on both sides; at least two agreements must share the same shape before a `GrammarObservationRecord` is emitted. Even after that recurrence admission, the record carries a non-promotion boundary and explicitly does not carry responsibility, family, lexicon, semantic meaning, or architectural truth.

This shows that participation can be locally admitted after another criterion, recurrence, while still stopping before broader repository promotion.

### 7. Selection Path preserves candidates, non-selected alternatives, and unknowns without mutation

`SelectionPathAudit` includes `selected`, `candidates`, `selection_factors`, `non_selected`, `evidence`, `outcome`, `unknowns`, and a boundary whose defaults are read-only: `records_facts=False`, `writes_event_ledger=False`, and `mutates_cluster=False`. Unsupported targets return `selected="unknown"`, preserve available candidates, and include an unknown explaining that no implementation-backed selection evidence was discovered for the target.

Selection Path is evidence that a surface can consume candidate material for visibility and explanation without admitting it to facts, event writes, or cluster mutation. It also shows that participation can stop at `unknown` rather than forcing promotion.

### 8. Current Facts and read-model evidence reject a single universal participation owner

Read-model recovery documents describe `State.get_current_facts(...)` as current projected fact selection over projected `State` and `FactSupport`, while `DerivedFactIndex` is a reusable cache/index over those current-fact semantics rather than the owner of current facts. Current Facts formatting can use the fact index or fall back to `State.get_current_facts(...)` directly. Capability Candidates can also optionally use `DerivedFactIndex.current_facts(...)` or scan state facts directly.

This rejects the counterclaim that participation is already fully owned by Current Facts, Fact Index, Observation, or another single recurring owner. Participation exists, but the implementation distributes admission across projection, facts, read models, diagnostics, inquiry views, and provider-local surfaces.

## Boundary analysis

### Does every attachment immediately participate in repository reasoning?

No. Capability candidates are preserved but are not execution decisions, policy evaluations, tool invocations, or capability permissions. Inquiry notes are preserved and can be oriented lexically but do not become facts, goals, plans, observations, event-ledger entries, or current facts. Observation Agreement emits candidate-only agreement records and rejects semantic/architectural truth. Grammar Observation emits recurrence records and still rejects grammar/truth promotion. Selection Path surfaces candidates and unknowns without fact or ledger mutation.

### Must participation be separately earned?

Yes, in the reviewed paths. Admission is performed by existing owners:

- `ObservationIngestor` admits canonical observations into event/evidence participation and optionally fact participation.
- Provider-specific translators admit external forms only after parser/shape/extraction support.
- `State` projection/current-fact selection admits facts into current projected read-model visibility.
- Capability candidate inspection admits package facts into candidate capability visibility only.
- Promotion readiness admits candidates into supported/unsupported readiness only when candidate support and verification support are both present.
- Observation Agreement admits exact-equality agreement only across independent supplied streams.
- Grammar Observation admits recurring relation-shape observations only after recurrence over agreement records.
- Inquiry Orientation admits lexical related-material orientation only as read-only orientation.
- Selection Path admits selection visibility only for implemented targets, otherwise stops at unknown.

### Can candidate attachments remain permanently outside shared participation?

Yes. Inquiry notes can remain in isolated JSONL storage and never enter the event ledger. Capability candidates can remain read-only candidates and never become verified capabilities or execution decisions. Observation agreements can remain candidate-only records. Grammar observations can remain implementation-local recurrence observations. Selection candidates can remain non-selected or unknown.

The repository treats these as legitimate outputs, not failures.

### What implementation admits an attached artifact into shared responsibilities?

No single implementation admits all artifacts. Admission is distributed:

| Artifact / candidate | Admission implementation | Participation admitted | Explicit non-admission |
| --- | --- | --- | --- |
| `Observation` | `ObservationIngestor.ingest_many(...)` | `observation.observed`, `evidence.observed`, optional `fact.observed` / `fact.inferred` | fact promotion can be suppressed |
| Package-derived capability candidate | `build_capability_candidates(...)` | read-only candidate visibility | capability, permission, policy, execution, selection |
| Capability readiness | `build_capability_promotion_readiness_inspection(...)` | supported/unsupported readiness inspection | `capability_verified` fact, policy, execution, inventory mutation |
| Inquiry note | `record_inquiry_note(...)`, `build_inquiry_orientation(...)` | preserved prose and lexical orientation | event ledger, facts, observations, goals, plans, commands |
| Observation agreement | `observe_observation_agreements(...)` | candidate agreement with provenance | architectural truth, semantic interpretation, ledger writes |
| Grammar observation | `observe_grammar_observations(...)` | recurring shape observation | grammar/truth/responsibility/family promotion |
| Selection path material | `build_selection_path_audit(...)` | read-only selection explanation | facts, ledger writes, cluster mutation |

### Can participation legitimately stop without promotion?

Yes. The best direct proof is capability promotion readiness: even a `supported` readiness result is not promotion and does not create `capability_verified` facts or write events. Observation ingestion also proves partial stop: observation/evidence can be recorded while fact promotion is suppressed for a bounded Prometheus case. Inquiry Orientation, Observation Agreement, Grammar Observation, and Selection Path all explicitly stop before broader promotion.

### Can participation remain provider-local?

Yes. Inquiry notes remain local to the inquiry-note store and orientation surface. Provider translation records and candidate surfaces can remain local/read-only. Observation Agreement and Grammar Observation are read-only internal knowledge surfaces without ledger writes. Capability Candidates and Promotion Readiness are read-only inspections. Provider-local participation is legitimate where the implementation boundary says it is local, read-only, or candidate-only.

### Does repository evidence already distinguish attachment from participation?

Yes. The evidence is stronger than terminology. The implementation repeatedly preserves candidate/local/provenance records while explicitly denying broader participation in facts, truth, policy, execution, mutation, current facts, or architectural recovery unless a bounded owner admits it.

## Comparative analysis

### Model A

```text
Representation
  -> Attachment
  -> Participation
```

Model A is too strong. It incorrectly predicts that attached candidates immediately participate in shared repository responsibilities. Counterevidence includes:

- capability candidates are not capabilities, permissions, selections, policy decisions, or tool invocations;
- supported promotion readiness is still not promotion;
- inquiry-note orientation does not create observations, facts, plans, or event-ledger entries;
- observation agreement is candidate-only;
- grammar observation is recurrence-only and non-promotional;
- selection path can stop at unknown;
- observation ingestion can suppress fact promotion.

### Model B

```text
Representation
  -> Candidate Attachment
  -> Participation eligibility
  -> Shared repository participation
```

Model B is more strongly supported, with one refinement: the repository does not expose one universal `ParticipationEligibility` object. Eligibility is implemented by local owner-specific admission checks:

- parser/shape/extraction checks for provider language translation;
- `ObservationIngestor` for observation/evidence/fact participation;
- state projection/current-fact selection for current fact visibility;
- candidate support plus verification support for promotion readiness;
- exact equality across independent streams for Observation Agreement;
- recurrence over agreement records for Grammar Observation;
- deterministic lexical overlap for Inquiry Orientation;
- implemented target matching for Selection Path.

Therefore the recovered architecture is distributed Model B, not a centralized gateway.

## Counterexamples

### Candidate attachment always becoming repository participation

No strong implementation counterexample was found. The closest candidate is canonical `Observation`: after `ObservationIngestor.ingest_many(...)`, an observation normally writes observation/evidence events and may write a fact. But this is not proof that all candidate attachments become participation because:

1. the object is already a canonical `Observation`, not arbitrary candidate attachment;
2. fact promotion is optional and can be suppressed;
3. many candidate surfaces never enter `ObservationIngestor` at all.

### Participation fully owned by Observation, Fact, Current Facts, or another recurring owner

Rejected. Observations/facts/current facts own important participation boundaries, but not all of them. Inquiry Orientation, Observation Agreement, Grammar Observation, Capability Candidates, Promotion Readiness, Selection Path, diagnostic/read-only views, and provider-local translators each own local participation or non-participation boundaries.

### Candidate attachment remaining permanently local without architectural failure

Supported. Inquiry notes, capability candidates, observation agreements, grammar observations, selection candidates/non-selected alternatives, unsupported selection targets, and promotion-readiness inspections can remain local/read-only/candidate-only. Tests and module boundaries make this an expected behavior.

### Participation stopping before promotion

Supported. Capability Promotion Readiness can return `supported` while writing no events and creating no `capability_verified` fact. Observation ingestion can stop at observation/evidence without fact promotion in the bounded suppression case. Observation Agreement and Grammar Observation stop before truth promotion by design.

## Answers to recovery questions

### 1. Does the repository distinguish Candidate Attachment from Repository Participation?

Yes, boundedly and repeatedly. The distinction is not implemented as a universal type, but it is implemented as a recurring boundary across observation ingestion, capability candidates, promotion readiness, inquiry orientation, observation agreement, grammar observation, and selection path.

### 2. What implementation evidence supports or rejects that distinction?

Supporting evidence:

- `ObservationIngestor` separates observation/evidence events from optional fact promotion.
- Capability Candidates preserve candidates while rejecting capability, authority, selection, policy, and execution.
- Promotion Readiness separates readiness support from actual promotion and fact creation.
- Inquiry Orientation preserves prose and lexical related material outside the event ledger.
- Observation Agreement emits candidate-only agreements and rejects truth/semantic promotion.
- Grammar Observation requires recurrence and still rejects grammar/truth/responsibility promotion.
- Selection Path preserves candidates, non-selected alternatives, and unknowns under read-only boundaries.

Rejecting evidence:

- No strong evidence was found that candidate attachments always become shared repository participation.
- No strong evidence was found that one existing owner fully owns all participation.

### 3. What admits an artifact into shared repository participation?

An artifact is admitted by the bounded implementation that owns the relevant downstream responsibility. Examples include `ObservationIngestor` for observation/evidence/fact event participation, `State` projection/current fact selection for current fact visibility, provider-specific extraction for provider observations, exact-equality agreement rules for Observation Agreement, recurrence rules for Grammar Observation, and candidate-plus-verification support for readiness inspection. There is no single universal admission service.

### 4. Can candidate attachments legitimately remain local forever?

Yes. Inquiry notes, capability candidates, observation agreements, grammar observations, selection candidates, and readiness inspections can remain local/read-only/candidate-only without repository failure.

### 5. Can participation stop before promotion?

Yes. Promotion readiness is explicitly not promotion, even when supported. Observation/evidence ingestion can stop before fact promotion in a bounded suppression case. Observation Agreement, Grammar Observation, Inquiry Orientation, and Selection Path all stop before truth/fact/mutation promotion.

### 6. Is participation already distributed across existing responsibilities?

Yes. The repository evidence rejects a centralized owner. Participation and non-participation are distributed across provider translation, observation ingestion, state projection/current facts, read-model surfaces, capability inspection, readiness inspection, inquiry orientation, selection path, observation agreement, and grammar observation.

### 7. Is there sufficient implementation evidence to recover this as a stable recurring boundary?

Yes, with bounded wording. The stable boundary is:

```text
Candidate Attachment != Repository Participation
```

The boundary is earned as a recurring implementation pattern, not as a new component, service, engine, or framework.

## Supported conclusions

1. **Candidate Attachment and Repository Participation are distinct in current repository evidence.**
2. **Attachment does not automatically imply participation in facts, truth, current facts, policy, execution, mutation, or answer authority.**
3. **Participation is separately admitted by existing bounded owners.**
4. **Admission is distributed, not centralized.**
5. **Candidate attachments can remain local forever.**
6. **Participation can stop before promotion.**
7. **Provider-local/read-model-local participation is legitimate when the implementation boundary says so.**
8. **Model B is more strongly supported than Model A, provided Model B is understood as distributed and owner-specific.**

## Unsupported conclusions

- A centralized participation engine exists.
- A repository admission service exists.
- A repository gateway should be implemented.
- A semantic engine is required.
- Candidate attachments always become facts, current facts, answers, observations, pressures, selections, or execution decisions.
- Observation, Fact, Current Facts, or Answer Composition fully owns all participation boundaries.
- Observation Agreement becomes architectural truth.
- Grammar Observation becomes repository grammar or lexicon authority.
- Inquiry Orientation turns operator prose into repository facts, goals, plans, commands, or truth.
- Supported promotion readiness is already promotion.

## Confidence

High confidence that the repository already distinguishes candidate attachment from repository participation as a recurring boundary.

Medium confidence on naming. `Candidate Attachment` and `Repository Participation` are architectural characterizations, not universal public types in the implementation.

Final recovered answer:

```text
After an external representation produces candidate attachments,
those attachments participate inside shared repository responsibilities
only when an existing bounded owner admits them for a specific responsibility.
Attachment alone does not imply shared participation.
Participation can remain local, stop at unknown/unsupported/candidate-only,
or stop before promotion without architectural failure.
```
