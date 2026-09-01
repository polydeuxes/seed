# Grammar Observation Evidence Contract Audit

## selected architectural question

What is the smallest implementation-backed evidence contract that `Grammar Observation` should consume from `Observation Agreement` if Observation Agreement later changes its internal matching algorithm?

Bounded answer: `Grammar Observation` should consume only the durable candidate-agreement evidence interface: candidate agreement text or pattern, participating independent streams, provenance-preserving supporting evidence references, and the non-promotion boundary. It should not consume the current exact-evidence-text matching rule as an architectural dependency.

This audit does not implement Grammar Observation, change agreement matching, change CLI/JSON/schema/event/ledger/runtime behavior, or add observers.

## implementation evidence

### Observation Agreement implementation boundary

`seed_runtime/knowledge/observation_agreement.py` defines Observation Agreement as read-only over already-observed records. Its module docstring says it consumes supplied observation records, emits candidate agreement records with provenance, and does not parse substrates, infer semantics, own grammar or lexicon, promote architectural truth, write ledgers, or mutate state.

The explicit boundary map preserves five positive responsibilities:

- consume supplied observation records;
- preserve candidate agreement;
- preserve provenance;
- preserve observation independence;
- emit candidate agreement records.

The same boundary rejects promotion, grammar ownership, responsibility recovery, family recovery, lexicon ownership, semantic interpretation, architectural truth, runtime mutation, event/ledger writes, repository mutation, and cluster mutation.

### Record shapes currently crossing the boundary

`ObservationAgreementEvidence` is a provenance-preserving reference to one supplied observation record. Its fields are:

- `stream`;
- `provenance`;
- `evidence`.

`ObservationAgreementRecord` is the emitted candidate agreement record. Its fields are:

- `participating_observation_streams`;
- `supporting_evidence`;
- `provenance`;
- `candidate_agreement`;
- `non_promotion_boundary`.

The implementation constructs agreement records only after grouping supplied evidence and finding at least two independent streams.

### Current algorithm is intentionally small

The current `observe_observation_agreements(...)` rule groups supplied observations by evidence text after trimming surrounding whitespace. The docstring calls this rule intentionally small and says exact evidence equality preserves candidate agreement and provenance without parsing substrates, canonicalizing terms, interpreting semantics, or promoting truth.

That makes exact text equality an implementation-local recovery strategy, not the durable contract Grammar Observation should depend on.

### Current supplied observation record families

Observation Agreement currently consumes three already-observed record families:

- `DocumentationArchitecturalRelationRecord` from documentation structure;
- `RepositoryArtifactFact` from self-model/repository artifact observation;
- `RelationshipFact` from relationship observation.

For each family, Observation Agreement converts existing record evidence into `ObservationAgreementEvidence` with a stream label, provenance string, and evidence text. It does not inspect raw Markdown, raw Python, repository files, runtime state, or events.

### Producer boundaries remain narrower than grammar

Documentation structure is explicitly read-only and rejects prose interpretation, grammar interpretation, responsibility recovery, lexicon stabilization, claim extraction, authority inference, shape inference, event-ledger writes, and repository mutation.

`RelationshipFact` is a language-neutral relationship evidence record. Relationship Observation states that import relationships are dependency/name-availability evidence only and do not prove behavior, calls, routes, boundaries, or ownership; definition relationships are syntactic declaration evidence only and do not prove invocation, behavior, reachability, capability authority, or runtime ownership.

`RepositoryArtifactFact` is an observed artifact fact record with artifact fact text, artifact kind, path, symbol, and optional parent symbol. Its surrounding module reconciles only supplied fixture records and does not inspect the repository, parse documentation, project state, or integrate with runtime execution.

### Prior audits place agreement before grammar without making agreement grammar

The classification audit defines Observation Agreement as read-only preservation of candidate agreement between independent observation streams, where each stream already produced bounded evidence for the same structural pattern, without promoting that agreement to truth, grammar, responsibility, lexicon, semantics, or mutation.

The architectural-position audit says Grammar Observation consumes recurring implementation relation shape and needs evidence of recurring relation shape while avoiding unsupported promotion. It also says independent agreements are stronger input than raw observations because they preserve convergence and provenance while refusing truth, responsibility, and lexicon authority.

The grammar visibility audit supports observing grammar only as recurring implementation relation shape, not as a new engine, observer, registry, or vocabulary authority. It also warns that attractive prose distinctions are insufficient without implementation evidence.

## durable evidence contract

The smallest implementation-backed contract from Observation Agreement to Grammar Observation is:

1. **Candidate agreement** — the bounded candidate shape that multiple observations support. Today this is `candidate_agreement` and is populated with evidence text. A future matcher may produce the same field from normalized, tokenized, structural, or heuristic comparison, but Grammar Observation should treat it as candidate input, not truth.
2. **Participating independent streams** — `participating_observation_streams` proves the candidate is supported by at least two observation streams rather than one repeated observation source.
3. **Supporting evidence references** — `supporting_evidence` preserves each participating record's `stream`, `provenance`, and `evidence`, allowing downstream auditability without re-running the matching algorithm.
4. **Provenance summary** — `provenance` provides the compact provenance tuple currently asserted by tests and record construction. It is redundant with `supporting_evidence.provenance`, but implemented as part of the record and therefore part of the current durable surface.
5. **Non-promotion boundary** — `non_promotion_boundary` preserves that the record is candidate-only and not architectural truth.

In short, Grammar Observation can consume:

```text
candidate_agreement
participating_observation_streams
supporting_evidence(stream, provenance, evidence)
provenance
non_promotion_boundary
```

It should consume these as evidence input for recurring relation-shape visibility, not as grammar truth.

## algorithm-specific details

The following are implementation details of the current exact-match algorithm and should not become Grammar Observation requirements:

- evidence text equality as the agreement criterion;
- trimming surrounding whitespace before comparison;
- grouping by a dictionary keyed by stripped evidence text;
- sorted iteration over evidence text keys;
- preserving first-seen stream order with `dict.fromkeys(...)`;
- the current stream label constants as an exhaustive stream universe;
- the assumption that `candidate_agreement` must equal a raw supplied evidence string;
- the absence of an explicit confidence score;
- the absence of an explicit `agreement_criterion` field.

These details explain how this implementation recovers an owner today. They should not define the evidence contract for Grammar Observation.

## recommended boundary

### Information that belongs to Observation Agreement

Observation Agreement should own:

- consuming supplied observation records only;
- preserving stream independence;
- preserving candidate agreement;
- preserving per-record supporting evidence and provenance;
- preserving non-promotion;
- deciding internally whether supplied observations agree enough to emit a candidate record.

Observation Agreement may change its internal agreement algorithm without requiring Grammar Observation changes if it continues to emit the durable fields above.

### Information reserved for Grammar Observation

Grammar Observation should own:

- deciding whether candidate agreements participate in recurring implementation relation shape;
- comparing candidate agreement records across slices/modules/audits for recurrence;
- distinguishing grammar visibility from grammar authority;
- refusing vocabulary, responsibility, lexicon, semantic, or architectural truth promotion unless separate implementation evidence supports it.

Grammar Observation should not own:

- parsing raw Markdown/Python/runtime/evidence substrates;
- reconstructing Observation Agreement's matching algorithm;
- deciding whether two raw observations agree;
- treating agreement criterion as grammar meaning.

### Required subset for Grammar Observation

Grammar Observation requires a subset of the available information:

| Information | Required by Grammar Observation? | Reason |
| --- | --- | --- |
| Candidate agreement | Yes | It is the candidate relation-shape input. |
| Participating streams | Yes | It proves independent observation support and prevents single-stream recurrence from masquerading as agreement. |
| Supporting evidence | Yes | It preserves auditability and lets grammar visibility remain implementation-evidence-backed. |
| Provenance | Yes | It lets downstream audits trace the candidate back to implementation/documentation/relationship records. |
| Agreement criterion | No | It would couple Grammar Observation to the current or future matching algorithm. |
| Agreement confidence | Not currently | No implemented field exists; adding it would be a schema/JSON/record change outside this audit. |

## counterexamples

### Coupling to exact text matching would weaken the boundary

If Grammar Observation required `candidate_agreement` to be exactly equal to all supporting evidence strings, it would depend on the current grouping strategy rather than the durable candidate-agreement surface. A future Observation Agreement implementation using normalized relation tokens, structured relation records, fuzzy evidence comparison, or multiple corroborating heuristics would then break Grammar Observation unnecessarily.

### Coupling to normalization rules would weaken the boundary

The current implementation only strips surrounding whitespace. If Grammar Observation treated that as the official normalization contract, any future change to case-folding, punctuation normalization, relation-token parsing, or source-specific extraction would become a Grammar Observation compatibility issue. The implementation evidence supports the opposite boundary: agreement decides whether observations agree; grammar consumes emitted candidate agreements.

### Exposing matching criterion would weaken the boundary

An `agreement_criterion` field might be useful for debugging an agreement implementation, but making it a Grammar Observation input would encourage downstream grammar logic to reason about how agreement was produced rather than what evidence was preserved. That would blur the boundary between agreement production and grammar visibility.

### Grammar can remain independent of how agreement was produced

The architectural-position audit already says Grammar Observation is interested in recurring implementation relation shape and that independent agreements are stronger input because they preserve convergence and provenance while still refusing truth and lexicon authority. None of that requires Grammar Observation to know whether the agreement was exact text equality, structural matching, normalized token matching, or another future heuristic.

## compatibility considerations

If Observation Agreement completely changes its internal matching algorithm, Grammar Observation can remain compatible if these invariants hold:

1. emitted records still identify the candidate agreement;
2. emitted records still identify at least two independent participating streams;
3. emitted records still preserve supporting evidence with stream, provenance, and evidence;
4. emitted records still preserve non-promotion as candidate-only evidence;
5. emitted records do not require Grammar Observation to parse raw substrates or reconstruct matcher-specific criteria.

A future implementation may add fields such as `agreement_criterion`, `agreement_confidence`, `normalized_candidate`, or `match_explanation`, but the current implementation evidence does not justify making those required inputs for Grammar Observation. Such fields should remain optional diagnostic/explanatory material unless a later slice explicitly changes the boundary and updates diagnostics/tests as required by repository instructions.

## recommended next slice

Do not implement Grammar Observation next by adding a parser or grammar engine. The next smallest implementation-backed slice would be a contract test or adapter characterization that asserts Observation Agreement records remain consumable through the durable evidence subset while leaving the matching algorithm private.

A safe future slice could:

- add tests documenting that downstream consumers use only candidate agreement, streams, supporting evidence/provenance, and non-promotion;
- avoid adding CLI/JSON/schema/event/ledger surfaces;
- avoid adding confidence or criterion fields until a concrete consumer proves they are necessary;
- keep Grammar Observation as visibility over recurring relation shape, not as authority or vocabulary promotion.

## confidence

High confidence that the durable contract is candidate agreement plus independent streams, supporting evidence, provenance, and non-promotion. This is directly implemented in `ObservationAgreementRecord`, `ObservationAgreementEvidence`, boundary constants, and tests.

Medium confidence that `provenance` should remain separate from `supporting_evidence`: the current implementation and tests include both, but the data is duplicative. Treat it as stable for compatibility now, not as proof that future record design should duplicate it forever.

High confidence that exact evidence text equality, whitespace trimming, grouping order, current stream labels as an exhaustive universe, matching criterion, and confidence are not required Grammar Observation inputs. They are either current algorithm details or unimplemented fields.
