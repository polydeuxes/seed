# Reasoning Chain Visibility Investigation

## Purpose

This investigation reviews whether Seed is repeatedly able to answer questions only by manually joining implementation-backed relationships, and whether that pattern indicates a repository-wide visibility concern around reasoning chains.

This document does not propose a new ontology, workflow engine, planning system, runtime autonomy, relationship catalog, or implementation surface. It records understanding from existing repository evidence only.

## Surfaces reviewed

Implementation surfaces reviewed:

- `seed_runtime/reasoning_path_audit.py`
- `seed_runtime/selection_path_audit.py`
- `seed_runtime/reference_selection.py`
- `seed_runtime/capability_relationship.py`
- `seed_runtime/projection_shape.py`
- `seed_runtime/ownership_discrepancies.py`
- `seed_runtime/observation_domains.py`
- `seed_runtime/observation_permission.py`
- `seed_runtime/relationship_catalog.py`

Tests reviewed:

- `tests/test_reasoning_path_audit.py`
- `tests/test_selection_path_audit.py`
- `tests/test_reference_selection.py`
- `tests/test_capability_relationship.py`
- `tests/test_projection_shape.py`
- `tests/test_ownership_discrepancies.py`
- `tests/test_observation_domains.py`
- `tests/test_observation_permission.py`
- `tests/test_relationship_catalog.py`

Documentation reviewed as supporting context:

- `docs/response_caveat_characterization.md`
- `docs/projection_integrity_drilldown_characterization.md`
- `docs/knowledge_representation_reconciliation.md`
- `docs/relationship_promotion_reconciliation.md`
- `docs/architectural_status_and_next_frontier.md`

## Short answer

The strongest repository-backed answer is: Seed is not primarily missing the individual objects, and it is not primarily missing every local relationship. It is increasingly missing consistent visibility into implementation-backed reasoning chains that already exist across multiple local surfaces.

Evidence supports this conclusion because the repository already contains:

- local relationship vocabularies and projections;
- local rationale and reasoning fields;
- local support, evidence, confidence, boundary, and limitation fields;
- at least two explicit chain-preserving audit surfaces, `reasoning_path` and `selection_path`;
- several surfaces that expose only one hop of a larger path, requiring manual reconstruction across diagnostics, pressure, capability needs, operational story, projection shape, and relationship catalogs.

This is not evidence that Seed needs a new reasoning engine. Existing chain-preserving implementations are read-only visibility/audit surfaces over already-implemented behavior.

## Chain-preserving surfaces

### `reasoning_path_audit`

`ReasoningPathAudit` is the clearest chain-preserving surface. Its data shape names a domain and subject, then preserves observed evidence, intermediate conclusions, derived conclusions, consumers, story impact, unknowns, and read-only boundaries.

It explicitly builds a derivation path only from implemented diagnostic surfaces. The implementation joins ownership discrepancies, capability needs, pressure audit, privilege discovery, and operational story into one explanation path.

Representative chain preserved:

```text
ownership_discrepancies evidence
    -> ownership attribution incomplete
    -> diagnostic capability need
    -> capability_needs / pressure_audit / privilege_discovery consumers
    -> operational_story impact
```

The tests prove this chain is user-visible and read-only. They require rendered evidence, intermediate conclusions, derived conclusions, consumers, story impact, no event-ledger write, no cluster mutation, explicit unknowns for unsupported paths, and diagnostic inventory/shape-audit registration.

### `selection_path_audit`

`SelectionPathAudit` preserves a narrower chain: target, selected item, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and read-only boundaries.

Its implementation explains selection evidence without changing selection behavior, primarily by joining pressure audit ordering with operational story focus.

Representative chain preserved:

```text
pressure candidates
    -> ordered candidate set
    -> selected pressure/focus
    -> non-selected candidate reasons
    -> operational story outcome
```

The tests prove the surface exposes candidate set, selection factors, non-selected candidates, evidence, outcome stability, no event-ledger writes, no cluster mutation, and diagnostic visibility registration.

### `reference_selection`

`ReferenceSelection` preserves some chain material for historical comparison: selected reference, selection rationale, alternatives, authority boundary, and limitations. For `history`, it joins `impact_audit` and `snapshot_policy_audit` evidence into selected and alternative reference explanations.

This is chain-preserving for reference choice, but not a general reasoning-path surface. It records why a reference was selected and what alternatives were visible; it does not expose a multi-hop path from source observations through downstream consumers.

### `projection_shape`

`ProjectionShapeStage` preserves stage-level chain material: each stage consumes inputs, produces outputs, influences downstream surfaces, does not influence other surfaces, and carries an authority boundary.

This is repository-visible influence topology. It can answer many projection questions such as “what produced this?” and “what does it influence?” at a stage level. It does not preserve instance-specific evidence paths for a particular fact, relationship, conflict, or diagnostic finding.

## Chain-fragmenting surfaces

### `ownership_discrepancies`

`ownership_discrepancies` preserves local diagnostic findings: subject, ownership kind, candidate owner, confidence, evidence count, conflict, reason, and evidence references. It also exposes diagnostic-only capability-need records implied by ownership conflicts.

This surface contains important links in the observed chain:

```text
owner_not_observed
    -> listener_process_inventory
    -> container_port_mapping
    -> container_inventory
```

However, by itself it does not carry the full downstream path to observation domains, capability pressure, privilege access, or operational story impact. That full path is reconstructable but fragmented unless viewed through `reasoning_path_audit`.

### `capability_relationship`

`capability_relationship` joins capability needs with privilege guidance and exposes current access, operational benefit, pressure, attainability, expectation, reasoning, and known limitations.

It preserves rationale/influence language locally: capability pressure is visibility context, not acquisition guidance; deployment expectation and operator intent are unknown. It does not preserve the upstream diagnostic path that produced each need except through the capability need inputs it consumes.

### `observation_domains`

`observation_domains` maps capability pressure into observation domains such as `local_listeners` and `container_runtime`, and classifies domains as observed, partially observed, or unobserved with gap types and evidence.

It preserves a domain-level relationship:

```text
capability pressure
    -> observation domain
    -> classification / gap type
```

It does not preserve the whole path back to the diagnostic conflict or forward to operational story. The chain is reconstructable by joining ownership discrepancies, capability needs, observation domains, and reasoning path output.

### `observation_permission`

`observation_permission` preserves local authority reasoning for observation classes and permission states. It can explain why future autonomous invocation requires operator expression unless reusable approval exists.

This is rationale-preserving for permission boundaries, but it does not join permission state into the diagnostic/capability/domain chain. It answers “may this kind of observation be reused or invoked autonomously?” more than “which diagnostic pressure caused this observation request?”

### `relationship_catalog`

`relationship_catalog` preserves canonical relationship definitions derived from fact predicates. It answers what local relationship can be projected from a predicate, including kind, subject type, object type, and source predicates.

It is intentionally local vocabulary, not a reasoning chain. It helps with relationship visibility but does not preserve why a relationship matters, what pressure created it, or which downstream conclusion it supports.

## Rationale, causality, influence, support, and drilldown vocabulary

Existing repository vocabulary overlaps with reasoning-chain visibility but is not identical to it.

| Term | Existing repository behavior | Chain visibility status |
| --- | --- | --- |
| Rationale | Present in selection, reference selection, capability relationship, confidence/caveat documentation, and permission reasoning. | Usually local; sometimes chain-preserving in selection/reference surfaces. |
| Reasoning | Present as explicit fields in capability relationship and observation permission; explicit surface in reasoning path. | Strongest chain support in `reasoning_path_audit`; otherwise local prose. |
| Influence | Strongly present in projection shape stages. | Stage-level topology, not instance-specific chain. |
| Support | Present across evidence/fact support, claim-support docs, relationship-promotion docs, confidence, and caveats. | Usually support trails or local support quality; not always a full A->B->C reasoning chain. |
| Causality | Rarely asserted directly; repository tends to use produced-by, derived-from, influence, pressure, or support. | Causal claims should remain bounded unless implementation explicitly encodes them. |
| Contribution | Present implicitly in operational story, pressure, capability needs, and projection influence. | Reconstructable; not uniformly exposed. |
| Explanation | Present in why/caveat/integrity surfaces and documentation. | Often fact-level or caveat-level; not always cross-surface. |
| Drilldown | Present in integrity and structural drilldown investigations. | A special navigation case: moves from summary to supporting details, but not necessarily a reasoning path. |

## Representative reasoning-chain tests

### Observation / ownership chain

Question: Why does `listener_process_inventory` exist or matter?

Current repository answer: It can be explained as a diagnostic capability need derived from ownership attribution gaps. `ownership_discrepancies` records `owner_not_observed` and maps that conflict to `listener_process_inventory`. `reasoning_path_audit` then exposes evidence, intermediate conclusion, derived capability need, consumers, and story impact.

Where the chain is preserved: `reasoning_path_audit`.

Where local pieces are preserved: `ownership_discrepancies`, `capability_needs`, `observation_domains`, `capability_relationship`, `privilege_discovery`, `operational_story`.

Conclusion: This is not a missing object or missing local relationship. The local objects and relationships exist; the reusable chain visibility exists only in the dedicated reasoning-path audit and remains fragmented elsewhere.

### Observation-domain chain

Question: Why does `container_runtime` appear as an observation domain?

Current repository answer: `observation_domains` maps `container_inventory` and `container_port_mapping` capability pressure to `container_runtime`, then classifies the domain based on whether container observation predicates/families are observed.

Where the chain is preserved: Partially in `observation_domains`; more fully when joined with `reasoning_path_audit` for the upstream ownership conflict.

Conclusion: The domain object and capability-domain relationships exist. The upstream diagnostic-to-domain chain is only partially visible in one place.

### Capability reasoning chain

Question: What pressure created a capability relationship, and what outcome does it contribute to?

Current repository answer: `capability_relationship` exposes access, operational benefit, pressure, reasoning, and limitations for capability needs. `reasoning_path_audit` can show the upstream diagnostic source and downstream consumers. `selection_path_audit` and `operational_story` can show selection/focus outcomes when pressure affects current focus.

Where the chain is preserved: Fragmented across `capability_relationship`, `reasoning_path_audit`, and `selection_path_audit`.

Conclusion: Capability reasoning is repository-visible, but not uniformly chain-preserved from source diagnostic to selection outcome.

### Reference-selection chain

Question: Why was this historical comparison reference selected instead of another?

Current repository answer: `reference_selection` exposes selected reference, selection rationale, alternatives, authority boundary, and limitations. For history, it uses impact and snapshot policy audit evidence.

Where the chain is preserved: `reference_selection`.

Conclusion: Reference-selection reasoning is one of the better local rationale-preserving surfaces. It is still scoped to reference selection and should not be generalized into a global reasoning engine.

### Projection reasoning chain

Question: What produced this projection artifact and what does it influence?

Current repository answer: `projection_shape` exposes stage-level consumes, produces, influences, does-not-influence, and authority-boundary fields.

Where the chain is preserved: `projection_shape` for stage topology.

Conclusion: Projection shape has strong chain-like influence visibility at the stage level. It does not replace instance-specific support paths for particular facts, relationships, conflicts, or diagnostics.

### Relationship catalog visibility

Question: Why does this relationship exist, and what does it influence?

Current repository answer: `relationship_catalog` can say which relationship definition is derived from which predicates. `projection_shape` can say catalog relationship projection produces relationships and influences type assertions and graph issue construction. Relationship-promotion documentation discusses support, corroboration, contradiction, and confidence as relationship-support concerns.

Where the chain is preserved: Fragmented across `relationship_catalog`, `projection_shape`, state/projection code, and relationship-promotion documentation.

Conclusion: Relationship visibility exists locally. Reasoning from predicate evidence to relationship projection to graph-health influence requires manual reconstruction unless a specific audit surface composes it.

## Which questions can Seed answer today?

| Question | Answerability today | Where preserved |
| --- | --- | --- |
| Why does this exist? | Often yes for local surfaces; strongest for reasoning path, selection path, reference selection, projection shape. | Local rationale fields or chain audit surfaces. |
| Why does this matter? | Partially. Operational benefit, pressure, consumers, story impact, influence fields help. | `reasoning_path_audit`, `capability_relationship`, `projection_shape`, operational story. |
| What produced this? | Yes for projection stages and some diagnostics; partial elsewhere. | `projection_shape`, `ownership_discrepancies`, relationship catalog derived-from predicates. |
| What does it influence? | Yes at projection-stage level; partial for diagnostics/capabilities. | `projection_shape`, `reasoning_path_audit` consumers/story impact. |
| What pressure created it? | Yes for selection/capability/ownership examples; partial elsewhere. | `pressure_audit` consumers via `reasoning_path_audit`, `capability_relationship`, `selection_path_audit`. |
| What outcome does it contribute to? | Partial. Story impact and selection outcome expose some paths. | `reasoning_path_audit`, `selection_path_audit`, operational story. |

## Supported conclusions

1. **Reasoning-chain visibility is a repository-wide concern, but not yet a single repository-wide abstraction.** Evidence appears across diagnostics, selection, reference choice, projection, capability, observation, ownership, relationship, caveat, support, and drilldown surfaces.

2. **The repository is usually not missing the first-order objects.** Examples such as capability needs, observation domains, relationship definitions, projection stages, evidence references, permission domains, and ownership discrepancy rows are already represented.

3. **The repository is usually not missing every first-order relationship.** Many local relationships are explicit: predicates derive relationships; projection stages consume/produce/influence; ownership conflicts imply diagnostic capability needs; capabilities map to observation domains; pressure candidates produce selections.

4. **The recurring gap is cross-surface chain visibility.** Several questions require manually joining A->B, B->C, and C->D across different surfaces. `reasoning_path_audit` and `selection_path_audit` show that the repository already has an implementation-backed pattern for exposing such paths without adding runtime behavior.

5. **Drilldown is related but narrower.** Drilldown can navigate from summary to detail or from count to source rows. Reasoning-chain visibility asks a broader path question: what evidence produced an intermediate conclusion, what downstream surface consumed it, and what outcome or influence resulted?

6. **Rationale and support are necessary but not sufficient.** Local rationale explains a choice or boundary. Support explains evidence backing a fact or claim. A reasoning chain preserves the ordered path across intermediate conclusions and consumers.

7. **Causality should remain cautious.** Existing implementation evidence more often supports derived-from, influenced, selected-by, supported-by, consumed-by, or pressure-from language than broad causal claims.

## Unsupported conclusions

The investigation does not support these conclusions:

- Seed is missing a new ontology.
- Seed needs a workflow engine, planning system, agent framework, execution system, or runtime autonomy system.
- Every local relationship should become a chain.
- Relationship catalog visibility and reasoning-chain visibility are the same concern.
- Presentation vocabulary alone should be promoted into repository knowledge.
- Current evidence supports a universal `ReasoningEngine` or global reasoning-chain store.

## Open questions

- Which implemented surfaces beyond `reasoning_path_audit` and `selection_path_audit` should be considered chain-preserving rather than local-rationale preserving?
- Should future visibility investigations use a standard distinction among local relationship, support trail, rationale, influence path, drilldown path, and reasoning chain?
- Where should instance-specific projection paths be visible when `projection_shape` currently exposes only stage-level topology?
- Which recurring manual joins are severe enough to justify future read-only audit surfaces, and which are adequately served by existing local outputs?
- How should chain visibility avoid promoting diagnostic findings into cluster truth when `--record` or event-ledger writing is involved?

## Acceptance answer

The repository evidence supports this answer:

```text
The repository is not primarily missing objects.
The repository is not primarily missing local relationships.
The recurring missing visibility is the ability to expose implementation-backed reasoning chains that already exist across multiple surfaces.
```

Reasoning-chain visibility already exists in scoped forms (`reasoning_path_audit`, `selection_path_audit`, `reference_selection`, and `projection_shape`). It is fragmented elsewhere, especially across ownership discrepancies, capability needs, observation domains, permission boundaries, capability relationships, relationship catalog projection, and operational story/pressure outputs.

The supported concern is visibility and understanding, not new runtime behavior.
