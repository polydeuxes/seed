# Evidence Graph → Fact-confidence consumer Uptake movement recovery 001

## 1. Scope and negative authority

This is one bounded, Book-first, report-only constitutional recovery against merged `main` after PR 1973. It examines one consumer only: `seed_runtime.confidence.build_fact_confidence(...)` / `_fact_confidence(...)`, reached through projected `State` and `build_evidence_graph(...)`. PRs 1799, 1805–1809, 1820–1826, 1901, 1971–1973, earlier reports, names, tests, and docstrings are locator testimony, never law or occurrence proof. Claims below are checked against the active Book and implementation.

The report does **not** recover or authorize a universal evidence router, universal admission engine, global current-standing object, global goal topology, workflow, schema, selector, registry, pipeline, refactor, deletion, or implementation proposal. It stops at the first confidence-consumer-local use and first compressed movement. `FactConfidence` is not truth, current truth, verification, authority to act, or universal promotion.

Classification vocabulary is **evidenced**, **partially evidenced**, **compressed**, **compatibility-only**, **absent**, and **Unknown**. Occurrence vocabulary is stated separately.

## 2. Active Book clauses used as constitutional expectation

| Active clause | Governing expectation used here |
|---|---|
| `01.External.A–D` | Programming, JSON, database, event, graph, confidence, and View shapes remain external/realization grammar. Fidelity is a bounded comparison preserving subject, witness, limits, erasure, invention, mutation, relocation, conflict, Unknowns, and stop; it is not global certification. |
| Lenses, Views, and Constitutional Roads | Availability, consumer-local applicability, admission, and responsible consumption are separate. Uptake is a consumer-side relation family; a road is its assertion-preserving subfamily. Visibility, adjacency, transport, a noun, or field reading does not establish Uptake. |
| Acts and Act Artifacts | A responsible validated production boundary evidences an act; construction of an act-shaped artifact does not. Consumer validation does not prove producer occurrence unless the consumer assertion requires it. |
| Orientation and Movement, including correction 001 | Movement is a warranted transition in lawful position or standing, not mutation, changed record, projection, method call, or object construction by identity. |
| Testimony and Established Fact | A constitutional Fact is an established, evidence-backed, normalized, scoped claim limited by source authority; a `Fact` artifact is not proof of that standing, currentness, verification, or fully resolved support. The repository explicitly compresses Observation intake, Evidence construction, normalization, optional Fact construction, and event emission. |
| Evidence A–F | Evidence support binding must distinguish identity, source, kind/context, subject/claim, authority, preservation, confidence, and provenance. A reference or row does not establish truth, applicability, admission, verified provenance, producer occurrence, or independent support. Bounded absence must not become falsehood. |
| Events, Facts, and State | Event records, Fact standing, projected material, current lawful condition, and current standing differ. Replay may expose supporting material; current standing requires a responsible bounded consumer preserving evidence, authority, freshness, conflict, expiry, and Unknowns. |
| Projection A–C | Visibility is not Uptake. Purpose-relative losslessness depends on distinctions required by that consumer. Derived material may be rebuildable from retained evidence/rules, but rerunning does not reconstruct a prior invocation. |

Thus the governing consumer grammar is:

```text
available material
→ consumer-local applicability
→ consumer-local admission
→ responsible consumption / Uptake
→ possible consumer-local assertion or standing
```

None of the arrows follows merely from representation adjacency.

## 3. Highest-order external grammar ↔ Fidelity ↔ constitutional grammar orientation

```text
external grammar
↕ bounded Fidelity comparison
constitutional grammar
```

| Crossing | Constitutional subject and expectation | Implementation witness | Preserved distinctions | Erasure / invention / mutation / authority relocation | Conflict, Unknown, stop |
|---|---|---|---|---|---|
| Observation → `Evidence` | Source-relative observed claim becomes bounded support material without becoming truth. | `ObservationIngestor.observation_to_evidence` copies subject, predicate, value, metadata, dimensions, expiry, time, source type, confidence into canonical `Evidence`. | Evidence id, workspace, `observation:<source_type>`, kind, observation id, claim coordinates, temporal testimony, confidence. | Receipt/recording time and producer authority are not invented. Construction alone does not prove occurrence. | Producer occurrence remains Unknown outside an invoked/recorded road. Stop at Evidence standing. |
| Evidence → `Fact` | Claim-appropriate support may warrant a weak source-relative Fact; otherwise refuse. | `ingest_many` suppresses one exact Prometheus OS shape; otherwise `observation_to_fact` links the evidence id and copies claim/time/scope coordinates. | Exact evidence reference, source type, confidence, dimensions, expiry, inferred marker. | No explicit generic provenance, conflict, authority, or admission object is invented. The method must not be read as universal establishment law. | Broader producer-specific Fact warrant remains Unknown. Stop at bounded Fact or suppression. |
| Ledger → projected `State` | Retained occurrence assertions replay into recoverable projected material. | `StateProjector.project` lists events and applies Observation/Evidence/Fact kinds; derived indexes are rebuilt. | Workspace, ledger order/as-of id, serialized claims and ids, projection rules. | Replay does not prove event claims, historical invocation, currentness, or Uptake. Measurement pruning can remove older projected provenance while ledger history remains. | Projection completeness relative to retained history/rules is evidenced; prior invocation reconstruction is absent. |
| Projected material → Evidence Graph | Resolve Fact evidence references and represent graph-local support visibility honestly. | `_evidence_graph_material_for_fact`, `_node_from_evidence`, `EvidenceLink`, `_fact_view`. | Evidence identity/type/summary, selected source event/run ids, confidence/time, fact identity/content, unresolved/derivation references. | Payload is summarized; source string, workspace, full payload, dimensions, expiry, authority, known loss and conflict are erased from nodes. A `supports` link is invented from membership/resolution, but only as graph-local representation. | Unresolved reference is represented, not a typed constitutional Unknown. Stop at consumer-ready graph material. |
| Graph → confidence result | This exact consumer may form a bounded support-count/contradiction estimate. | `_fact_confidence` reads only `len(view.evidence)`, `view.supporting_event_ids`, Fact explicit confidence, and supplied contradictions. | Fact identity/content, count, event ids, explicit Fact confidence, contradiction count/reasons. | Evidence assertion/content/source/provenance/time/confidence/scope/authority/expiry/Unknowns are not examined. Count is mapped to 0/.50/.75. | Admission/currentness/authority sufficiency remain Unknown. Stop at `FactConfidence`, never truth/currentness. |

## 4. Constrained-movement orientation

The investigation is movement-first, not object-first:

```text
projected Fact standing presently exists
→ confidence-estimation responsibility is burdened
→ graph-resolved reference material is available
→ _fact_confidence performs a consumer-local count/contradiction examination
→ a bounded confidence-shaped estimate is constructed
```

The warranted movements recovered are: (1) source-relative Observation material receives Evidence standing through responsible conversion and recording; (2) that Evidence is either linked into a bounded Fact artifact or promotion is suppressed; (3) replay makes retained material recoverable; (4) the graph changes a reference's graph-local position from unresolved/absent to resolved node plus support link; (5) the confidence consumer changes its estimate from unsupported/0 (absent explicit confidence) to support-count-backed `.50`, or to `.75` at two nodes, subject to explicit confidence and contradiction rules. These movements do not require dedicated constitutional objects and none makes projected visibility current standing.

## 5. Control-road recovery

```text
Observation → Evidence → Fact or bounded suppression
```

1. **Evidence production — evidenced, runtime-active when ingestion is invoked.** `ingest_many` invokes `observation_to_evidence`. The exact implementation act canonicalizes one Observation into `Evidence`: a new `evd_obs` identity plus preserved source-relative payload, time, expiry, dimensions, and confidence. `ingest_many` then creates `observation.observed` and `evidence.observed` events and appends the batch. Construction is the conversion witness; the appended `evidence.observed` event is preservation evidence, not proof the observation's proposition is true.
2. **Fact admission/refusal — partially evidenced and compressed.** The only explicit local gate is `_should_suppress_fact_promotion`: exactly metadata `fact_promotion_suppressed is True`, `source_name == prometheus`, `prometheus_metric == node_uname_info`, and predicate `os`. Matching material returns `None`; all other material is mechanically passed to `observation_to_fact`. There is no separate examination of Evidence kind, payload agreement, source authority, provenance completeness, scope, conflict, currentness, or Unknowns. “Admitted” is therefore safe only as **implementation-local promotion accepted**, not a general constitutional admission finding.
3. **Fact standing — partially evidenced.** The produced artifact asserts the Observation's exact subject/predicate/value/dimensions at `observed_at`, with source type, confidence, expiry, inference marker, and one exact Evidence id. Under the Book this can warrant weak source-relative established Fact standing when claim strength does not exceed that testimony. Broader, current, verified, authority-heavy, or producer-specific standing is Unknown.
4. **Occurrence/preservation — evidenced.** Non-suppressed ingestion emits Observation, Evidence, then Fact event; suppressed ingestion emits Observation and Evidence only. The event sequence preserves the producer output assertion, but Event != Evidence truth and Event != Fact standing by identity.

### Control-road suppression case

The current Prometheus `node_uname_info` OS adapter marks the endpoint-scoped raw OS Observation with `fact_promotion_suppressed=True`; `ingest_many` still constructs and records its Evidence and returns `None` for its Fact position. Current tests prove the metadata shape and ingestion behavior. This establishes:

```text
Observation preserved
→ Evidence produced and evidence.observed recorded
→ Fact production suppressed; no fact event for that item
```

Therefore **Evidence preserved != Evidence admitted for Fact establishment**. No `TypedUnknownRecord` is produced by this refusal; absence of a Fact remains bounded absence, not Typed Unknown standing.

## 6. Target-road recovery

```text
projected State
→ build_evidence_graph
→ FactEvidenceView for one Fact
→ build_fact_confidence / _fact_confidence
→ FactConfidence
```

The target road is read-only and deterministically constructible. It is runtime-active when CLI confidence surfaces or callers invoke it, and test-active in focused tests. `build_fact_confidence` selects a `Fact` by exact id, builds/reuses an `EvidenceGraph`, builds/reuses contradiction results, maps graph views by exact `fact_id`, and invokes `_fact_confidence`.

The first exact consumer-local use occurs at:

```python
support_count = len(evidence_view.evidence)
evidence_confidence = _evidence_confidence(support_count)
```

This is not canonical-Evidence assertion adoption. It is **reference-level, partial/compressed Uptake** of the graph's resolved-membership assertion: the output confidence and unsupported flag materially depend on how many resolved nodes the exact Fact view contains. The exact Evidence assertion could be replaced by different content while retaining one resolved node and the non-contradiction inputs, and this consumer would return the same support contribution.

## 7. Exact Fact/Evidence trace

The exact non-fabricated repository scenario is the test-active fixture in `tests/test_evidence_graph.py`:

| Coordinate | Exact trace |
|---|---|
| Fact identity/content | `fact_supported`: `service runs_on example_host_b`, discovery source, explicit confidence `0.91`, observed `2026-01-01T00:00:00Z`. |
| Exact evidence reference | `fact_supported.evidence_ids == ["evd_obs_1"]`. |
| Canonical Evidence | `evd_obs_1`, `source="observation:discovery"`, `kind="observation"`, payload source event `evt_123`, Observation `obs_1`, matching subject/predicate/value, run `run_1`, confidence `.91`. |
| Graph resolution | One `EvidenceNode(evidence_id="evd_obs_1", evidence_type="observation", source_event_id="evt_123", source_run_id="run_1", confidence=.91, created_at=...)`; one `supports` link to `fact_supported`; one exact Fact view. |
| Confidence input | View identity/content, `len(evidence)==1`, supporting ids `evd_obs_1` and `evt_123`; Fact explicit confidence `.91`; contradiction list if any. |
| Output assertion | For the same shape under `_fact_confidence`, support contribution is `.50`; because `.91` is explicit relative to discovery default `.95`, max preserves `.91`; output is not unsupported, support count 1, with count and explicit-confidence reasons, before any contradiction penalty. |

That fixture is **test-active direct construction**, not proof that these literal ids occurred in a runtime ledger. Separately, the CLI test invokes `--observe service runs_on example_host_b`, then the Evidence and confidence CLI surfaces read replayed SQLite state without appending events; that proves the road is runtime/CLI-triggered but uses generated ids. The report deliberately does not fabricate a runtime instance to merge these two evidentiary standings.

**Compressed/unresolved comparison.** The exact `fact_missing_evidence → evd_missing` test has no canonical Evidence in `State`. The graph produces no node/link, retains `EvidenceGraphReference(standing="unresolved_evidence_reference")`, and supplies zero evidence/supporting ids. The confidence test's exact `fact-missing → evd-missing` produces support count `0`, confidence `0.0`, and `unsupported=True` where no explicit confidence is supplied. This is represented unresolved reference plus bounded unsupported result—not a `TypedUnknownRecord`, not falsehood, and not proof that Evidence never existed historically.

## 8. Producer-occurrence analysis

The three burdens remain independent:

| Burden | Finding |
|---|---|
| Evidence producer occurrence | **Evidenced only for invoked ingestion paths** by `ingest_many` conversion plus event batch append; `Evidence` existence, graph resolution, fixture construction, or replay alone does not establish the historical producer invocation or truth of its source claim. |
| Consumer Uptake occurrence | **Evidenced for an invocation of `_fact_confidence`** only as count-level use: its returned fields materially vary with resolved node cardinality. Rebuildability proves a fresh invocation can reproduce current output, not that a prior consumer ran. |
| Authority scope | **Partially evidenced/Unknown.** The function contract authorizes a deterministic estimate over projected facts, graph membership, explicit Fact confidence, and contradictions. Nothing authorizes truth, current applicability, verification, operational reliance, or source-authority expansion. |

## 9. Evidence Graph responsibility

`build_evidence_graph` performs a deterministic read-only representation/projection act:

* orders projected Facts;
* resolves their `evidence_ids` against `state.evidence`;
* incorporates Evidence attached through matching `FactSupport`/supporting Facts;
* creates deduplicated `EvidenceNode`s and graph-local `supports` links;
* preserves missing ids as `EvidenceGraphReference` values rather than nodes;
* creates exact `FactEvidenceView`s and compact explanations/supporting ids.

Its standing is **graph visibility + graph membership + support-reference resolution + consumer-ready compressed Evidence material**. It is not admitted canonical Evidence for every consumer and not a Typed Unknown producer.

| Dimension | Graph output standing |
|---|---|
| Subject/identity | Exact Evidence id and exact target Fact id are preserved; node deduplication is global to the graph. |
| Assertion/content | Evidence payload is reduced to a summary; link asserts graph-local “supports” based on resolved reference/support membership, not independently examined semantic support. |
| Standing | Read-only represented support visibility; unresolved reference representation where resolution fails. |
| Source/provenance | Type, selected event/run id, created time and confidence survive; full source string/payload/workspace/lineage do not. |
| Responsibility | Graph builder owns deterministic resolution/representation, not producer validation or universal relevance. |
| Authority/warrant | Projected State membership plus exact Fact/reference/support matching warrants the graph representation only. |
| Scope/locality | Workspace State and each Fact view; no cross-consumer applicability. |
| Occurrence/preservation | Constructed per call; not separately persisted; rebuildable from State, but prior invocation is not reconstructable. |

## 10. Applicability analysis

Question: why is this exact Evidence relevant to this exact Fact's confidence under this consumer purpose?

* The graph uses exact `Fact.evidence_ids`, or evidence on `FactSupport`-associated supporting Facts, to place a node in the exact view. This evidences **reference/membership applicability for graph formation**.
* The confidence consumer selects the view by exact `fact.id`. This implicitly treats every resolved node in that view as eligible to count.
* Neither boundary compares the Evidence payload's subject/predicate/value/dimensions with the target Fact, applies source-type or temporal/expiry rules, tests the consumer purpose, or emits `applicable | inapplicable | Unknown | conflicting` standing.

Therefore explicit confidence-consumer applicability standing is **absent**. An implicit count-eligibility assumption is **compressed into exact-reference/FactSupport membership and graph adjacency**. This is not “applicability Unknown”: the implementation simply does not produce an applicability determination. Whether the canonical assertion is constitutionally applicable to current confidence purpose remains **Unknown to this recovery** where that purpose requires semantic, temporal, source, or authority matching.

## 11. Admission analysis

No separate confidence-consumer admission responsibility exists. The consumer does not validate producer occurrence, Evidence kind/standing, source authority, provenance completeness, scope match, currentness/expiry, conflict within Evidence, negative authority, Fidelity limits, known loss, or Typed Unknowns. Resolved-node presence is assumed countable; unresolved references are invisible to `_fact_confidence` except indirectly as no nodes.

Admission is therefore **absent as explicit standing and compressed/assumed from resolved graph membership for counting**. It is not inherited lawfully from Fact establishment in any disclosed contract: although the Fact reference is upstream testimony, the consumer does not establish that the assertion and reliance authority required for confidence use survived. The graph test name “not admitted support” accurately describes its local behavior but is test testimony, not a constitutional admission artifact.

## 12. Uptake analysis

| Question | Finding |
|---|---|
| What depends materially on Evidence? | `support_count`, count reason, support-derived `.50/.75`, `unsupported`, and transported `supporting_event_ids`; contradiction computation also receives the graph but is a neighboring producer. |
| What changes if absent/unresolved? | Resolved count falls; without explicit Fact confidence output becomes `0.0` and unsupported. With explicit confidence, that value may remain while reason/unsupported semantics differ. |
| What if content/source/time/confidence/scope/authority changes but node count does not? | This consumer's Evidence-derived confidence contribution does not change. |
| What if conflicting? | Only separately produced `Contradiction` count/reasons cause a `.75` multiplier; canonical Evidence conflict coordinates are not locally inspected. |
| New local standing | A deterministic `FactConfidence` estimate over projected Fact explicit confidence, resolved support cardinality, and contradiction results, with bounded reasons/ids. |

Classification: **partial or compressed, reference-level Uptake only**. It is real consumer-local movement because the resolved-membership assertion is materially used to produce different estimate standing; it is not faithful full Evidence-assertion Uptake, universal promotion, producer occurrence, currentness, or authority expansion. A field read alone would not suffice; the output dependence supplies the movement evidence.

## 13. Typed Unknown matrix

| Candidate Unknown subject | Producer / locality | Explicit typed standing? | Representation, downstream use, resolution |
|---|---|---:|---|
| Evidence producer occurrence unavailable | None on target road | **Absent** | Graph node does not carry occurrence proof. Remains report-level Unknown; resolve with responsible producer/recording evidence. |
| Exact Evidence reference unresolved | Evidence Graph / exact Fact view | **No** | `EvidenceGraphReference("unresolved_evidence_reference")`; confidence drops it to zero count. Resolve by projecting canonical Evidence with matching id, subject to retained history/rules. |
| Evidence content unavailable to confidence | No producer | **No** | Node summary exists, but consumer never reads even it. This is compression/ignored input, not Typed Unknown. |
| Source role/provenance | Graph partially transports type/event/run; confidence ignores them | **No** | Unknown where omitted; not persisted as unknown standing. Resolve by reopening canonical Evidence/producer evidence, where retained. |
| Applicability | No target-road producer | **Absent, not an Unknown result** | Count eligibility is assumed. A constitutional answer remains Unknown when semantic/temporal applicability is required. |
| Admission | No target-road producer | **Absent, not an Unknown result** | Resolved membership substitutes operationally for countability. |
| Conflict unresolved | Contradiction producer represents contradictions; confidence counts/penalizes | **No Typed Unknown** | Conflict is represented, not resolved. Evidence-level conflicts unavailable. |
| Currentness/expiry | No graph/confidence producer | **Absent** | Fact/Evidence time is available upstream; node time is ignored; expiry omitted. Current reliance remains Unknown. |
| Authority | No graph/confidence producer | **Absent** | Function negative authority is clear; positive reliance beyond estimate is Unknown. |
| Confidence sufficiency | No producer | **Absent** | Threshold labels/count mapping are rules, not sufficiency adjudication. |
| Consumer result | Confidence producer | **No Unknown alternative** | Always returns a record for an existing Fact; missing Fact returns `None`, which is not Typed Unknown. |
| Repository `TypedUnknownRecord` | `preserve_typed_unknown` used by other audits | **Evidenced elsewhere, absent here** | It preserves type/area/reason and public projection erases `unknown_type`; neither Evidence Graph nor confidence imports/produces/consumes it. |

## 14. Capability matrix

| Boundary capability | Availability | Applicability / selection | Authority | Execution / observed result / verification / standing |
|---|---|---|---|---|
| Produce canonical Evidence from Observation | `observation_to_evidence` available | Selected for each `ingest_many` item | Bounded conversion and record authority | Runtime-active when ingestion runs; tests verify shape/events. Result is source-relative Evidence, not truth. |
| Preserve Observation/Evidence occurrence assertions | Event ledger append available | Selected by ingestion | Record assertions only | Runtime-active; replayable. Does not verify source proposition. |
| Establish or suppress Fact promotion | conversion plus exact suppression predicate available | All nonmatching items selected mechanically | Weak source-relative Fact only | Runtime-active; suppression verified. No universal admission capability recovered. |
| Replay projected Evidence/Fact material | `StateProjector` available | Workspace/event-scope selected | Projection only | Projection-replay-active; rebuilds current recoverable material under rules. |
| Resolve references/form graph visibility | graph builder available | Exact Fact id/reference and support matching | Representation only | Runtime/CLI/test-active; deterministic and read-only. |
| Judge Fact-local applicability | No responsible boundary | Not selected | None | **Absent**. Reference matching is not this capability by identity. |
| Admit Evidence for confidence use | No responsible boundary | Resolved nodes implicitly countable | Count-only assumption | **Absent as constitutional capability**; implementation can count. |
| Consume Evidence to produce confidence standing | `_fact_confidence` available | One/all projected Facts | Estimate-only | Runtime/CLI/test-active; **compressed reference-level Uptake**, not assertion adoption. |
| Preserve conflict | contradiction results available | Selected per Fact id | Penalize estimate, not resolve | Partially evidenced; contradictions retained as reasons/count. |
| Preserve Typed Unknown | generic helper available elsewhere | Not selected here | None here | Absent on target road. Helper existence does not create capability occurrence here. |
| Rebuild target material | ledger replay + graph/confidence builders | Workspace and current invocation | Recompute only | Current output reconstructable if history/rules retained; historical invocation not. |

At every row: availability != applicability != selection != authority != execution != result != verification != current standing.

## 15. Gap matrix

| Required standing | Present standing | Exact consumer/consequence | Material incompatibility / finding |
|---|---|---|---|
| Honest differentiation of resolved vs unresolved references | Resolved nodes and represented missing references | `_fact_confidence` receives nodes but not reference list | **Evidenced Gap:** unresolved-reference reason/identity is compressed to zero support, so output cannot distinguish missing reference from no reference. Material to explanation/Unknown honesty; numeric behavior is deliberate. |
| Consumer-local applicability for semantic/current confidence reliance | Exact-reference graph membership only | Fact-confidence consumer | **Partially evidenced Gap:** no payload/scope/time/source comparison. Material only if output is relied on as more than count-based estimate; current contract refuses stronger standing. |
| Admission preserving source/authority/currentness limits | No admission finding; node count | Fact-confidence consumer | **Evidenced Gap for Evidence-assertion Uptake**, but not necessarily a defect in a declared count estimator. It blocks lawful strengthening beyond count-level output. |
| Reconstruct why confidence changed | count reason + ids, but no admitted assertions/rules snapshot | Later reader of `FactConfidence` | **Compressed Gap:** current reason is reconstructable with current State/rules; historical reason/rule invocation is not persisted. |
| Typed Unknown for unresolved support | Reference representation only | Confidence consumer | **Evidenced representation gap**, but the Book does not require every bounded absence to become Typed Unknown. Material only for a purpose requiring Unknown standing. |
| Preserve conflict | Separate contradiction count/reasons | Confidence consumer | No evidenced Gap at coarse contradiction purpose; Evidence-level conflict basis remains compressed. |

Not every compression is a Gap: omitting full payload from a count-only estimator is compatible with its negative authority. The first exact material Gap relative to honest confidence explanation is loss of the distinction **no evidence reference vs unresolved evidence reference** at the confidence boundary.

## 16. Demand matrix

Demand requires applicable requirement + current standing + warranted comparison + incompatibility + consumer-local consequence.

| Candidate Demand | Requirement and comparison | Finding |
|---|---|---|
| Evidence resolution | Distinguish supported from unsupported and do not strengthen unresolved ids; nodes vs represented references | **Evidenced and satisfied** numerically: unresolved ids do not increase support/confidence. No new Demand. |
| Applicability | Produce a bounded count-based confidence estimate; graph membership supplies count eligibility | **No evidenced current Demand** under the narrow contract. A Demand would arise only for semantic/current/source-aware confidence, which is not claimed. |
| Admission/authority | Avoid reliance beyond estimate authority | Negative authority is documented; no local admission standing | **Partially evidenced Demand at the reliance boundary**, not an implementation proposal: any consumer claiming Evidence-supported current truth would require admission/authority that is absent. No such current downstream consumer is established here. |
| Provenance | Expose supporting ids and count reasons | Ids are transported; full provenance is reopenable from State in current invocation | No evidenced Demand for current count estimate; historical self-contained explanation remains compressed. |
| Conflict treatment | Reduce but do not resolve contradicted facts | Separate contradictions are counted and reasons preserved | **Satisfied at coarse contract**; no evidenced Demand for resolution. |
| Currentness | Current-facing reliance would require expiry/freshness | Confidence output does not claim currentness | **No current Demand**; currentness remains outside authority. |
| Typed Unknown | Preserve unresolved reason as typed standing | No declared target contract requires it | **No evidenced Demand**, despite an evidenced Gap for consumers requiring the distinction. |

The responsible conclusion is not “richer Evidence exists, therefore Demand.” The only immediate requirement actually evidenced is a bounded confidence estimate distinguishing resolved support count and contradictions; it is satisfied within its deliberately weak authority.

## 17. Eight-dimensional matrices

Abbreviations: S=subject/identity, A=assertion/content, St=standing, P=source/provenance, R=responsibility, W=authority/warrant, L=scope/locality, O=occurrence/preservation.

### 17.1 Observation, canonical Evidence, Fact establishment/refusal

| Subject | S | A | St | P | R | W | L | O |
|---|---|---|---|---|---|---|---|---|
| Observation | `Observation.id` + claim subject | source reports predicate/value | attributed observation testimony | source type, time, metadata, dimensions, expiry | observation producer; ingestor records | source-relative only | workspace/subject/dimensions/time | runtime occurrence only when produced; event preserves assertion |
| canonical Evidence | new `evd_obs` + observation id | payload restates exact claim/context | applicable support material for bounded examination; not Fact | `observation:<type>`, time, payload, confidence | conversion owner; ledger preservation owner | bounded provenance representation | workspace and preserved claim scope | conversion+event evidenced when ingestion runs; replayable |
| Fact established | `fact_obs` + subject | normalized predicate/value | weak source-relative Fact when claim strength is warranted; otherwise artifact standing only | evidence id, source type, time/confidence/expiry | `observation_to_fact` compressed establishment | copied testimony; no stronger authority | claim/dimensions/time | optional fact event preserves assertion |
| Fact refused/suppressed | Observation/Evidence remain subjects; no Fact subject | promotion not performed for exact OS shape | bounded suppression result `None`; no Unknown | suppression metadata/provenance retained in Evidence | exact predicate in ingestor | narrow compatibility/safety rule | Prometheus `node_uname_info` endpoint OS | runtime/test-active; Observation/Evidence events only |

### 17.2 Projected material and Evidence Graph

| Subject | S | A | St | P | R | W | L | O |
|---|---|---|---|---|---|---|---|---|
| Projected Evidence | Evidence id retained in State | replayed Evidence payload | currently recoverable projected material, not current standing | ledger event/payload; ordering/as-of State | `StateProjector` | retained event + replay rules | workspace/projection rule | projection-replay-active; rebuildable, not prior invocation |
| EvidenceNode | Evidence id | compact type/summary/confidence/time | resolved graph-visible material | selected event/run ids | graph builder | State id resolution | graph / exact views containing node | per-call, unpersisted |
| EvidenceLink | evidence id → Fact id | graph-local `supports` | support-membership representation | inherited ids only | graph builder | exact reference/support association | exact graph | per-call, unpersisted |
| FactEvidenceView | exact Fact id/content | Fact plus resolved nodes/references/count explanation | consumer-ready graph representation | ids and selected node coordinates | graph builder | projected State + graph method | one Fact | per-call, rebuildable |

### 17.3 Applicability, admission, Uptake, result

| Subject | S | A | St | P | R | W | L | O |
|---|---|---|---|---|---|---|---|---|
| confidence applicability | No dedicated subject produced | implicit “resolved nodes in this exact view may count” | **compressed; no explicit constitutional standing** | exact ids/membership only | no separate owner | adjacency/reference rule | exact Fact consumer | no independently evidenced act |
| confidence admission | No dedicated subject produced | implicit “present node is countable” | **absent/assumed**, not admitted Evidence standing | not validated | no separate owner | none beyond graph presence | exact Fact consumer | no independently evidenced act |
| confidence Uptake | exact Fact + view count | count contributes `.50/.75` | **partial/reference-level Uptake** | supporting ids transported | `_fact_confidence` | deterministic count contract only | exact Fact estimate | occurs per invocation; not persisted |
| resulting standing | `FactConfidence.fact_id` | estimated confidence/support/contradiction/unsupported/reasons | bounded confidence-shaped projection assertion, or `None` for missing Fact—not Typed Unknown | ids/reasons; source limits omitted | confidence builder | projected Fact + count + contradictions + explicit confidence rule | current invocation/workspace State | constructible/runtime/CLI/test-active; rebuildable under retained inputs/rules |

## 18. Event-to-projection recurrence

For a new relevant ingestion event batch:

| Arrow | Producer → consumer | Constitutional act / witness | Lineage, Fidelity burden, Unknown |
|---|---|---|---|
| new Event → new Evidence material | Ingestor/ledger → `StateProjector` | `evidence.observed` records converted Evidence; projector applies it | Exact payload/id retained. Event truth and producer proposition remain unverified. |
| Evidence material → changed projected State | Projector → State readers | Replay incorporates Evidence; Fact event separately incorporates reference | Workspace/order/rules preserved. Incremental equivalence depends on same inputs/rules; current code's normal `project` is full replay. |
| State → changed graph | graph builder | Matching id changes unresolved reference to node+link, or adds a node | Identity and selected provenance preserved; semantic applicability/admission remain absent. |
| graph → changed confidence input | `build_fact_confidence` | exact view now has a different node count/supporting ids | No evidence that every consumer reran. A call is required. |
| input → changed local standing | `_fact_confidence` | count rule changes support contribution 0→.50 or .50→.75, subject to explicit max and contradiction penalty | Output reason/count changes; canonical assertion is not adopted. Why beyond count/id/rule is compressed. |

A newly appended Evidence event **without a corresponding projected Fact reference** changes State evidence availability but not this Fact's graph or confidence. A Fact event referencing an unresolved Evidence id can create represented reference/zero count; later matching Evidence can resolve it on replay even if append order is unusual, because the completed projected dictionaries are read after replay. New Event appended != consumer reran; State/graph change != Uptake; support-count change != lawful truth change.

## 19. Projection/rebuildability analysis

* `StateProjector.project` performs full workspace ledger replay into a new `State`; this is **projection-replay-active**.
* `project_from_state`/snapshot paths support projection from a supplied state and later events, so incremental/cached projection mechanisms exist, but full replay is not constitutionally superior by identity. Fidelity depends on retained evidence, identical applicable rules/limits, and declared purpose.
* Graph and confidence outputs are not separately persisted and are deterministically rebuildable from projected State plus graph/contradiction/confidence rules.
* SQLite ledger supplies cross-restart retained history; process-local `EventLedger` does not by itself.
* Measurement-history projection can prune Evidence/Observations from projected State while the ledger remains the replay source. Thus graph resolution is a function of the declared projection, not historical existence by identity.
* Current output can be reconstructed from retained history/rules; a historical confidence invocation, its caller purpose, exact supplied alternate graph/contradictions, and the fact that any consumer relied are not reconstructed.
* Projection visibility becomes current constitutional standing **nowhere by identity**.

## 20. Object-bias audit

| Term | External/object meaning | Constitutional correction |
|---|---|---|
| `EvidenceNode` | dataclass representation of selected Evidence coordinates | Neither Evidence producer occurrence nor admitted support; graph-visible material only. |
| `EvidenceLink` | generated id relation | Graph-local support-membership assertion, not universal applicability or authority. |
| `FactEvidenceView` | compact per-Fact representation | Lens/consumer-ready material; not Fact establishment, applicability, or Uptake by identity. |
| `FactConfidence` | output dataclass | Bounded estimate standing only when responsibly produced; object construction alone proves nothing. |
| `EvidenceGraph` | container of nodes/links/views | Projection representation, not router, admission engine, knowledge graph truth, or constitutional subject. |
| `State` | mutable projection object | Currently recoverable material; constitutional current standing is not this object. |
| projection | replay/derived representation shorthand | A responsible act may expose material; update is not movement/currentness by identity. |
| support count | integer cardinality | Compressed coordinate that drives local estimate; not Evidence sufficiency or corroboration automatically. |
| unknown record | `TypedUnknownRecord` elsewhere | Artifact can preserve typed standing; absence, `None`, empty tuple, zero, or missing key is not Unknown by identity. |
| consumer | function/caller shorthand | Constitutional responsibility is the bounded examination and warranted use, not the class/function name. |
| pipeline / handoff | adjacency/order shorthand | Neither a constitutional road nor Uptake unless assertions, limits, validation, occurrence, and local warrant are preserved. |

The main object bias would be to infer that because a canonical `Evidence` becomes an `EvidenceNode` in an `EvidenceGraph`, an admission act occurred. The actual movement recovered is weaker: reference resolution changes graph-local visibility, then the consumer counts that membership.

## 21. Control-road versus target-road comparison

| Concern | Control road | Target road |
|---|---|---|
| Producer occurrence | Ingestor conversion plus append is runtime-active and record-evidenced | Graph/confidence occurrence only per call; reconstruction does not prove prior call |
| Subject | Observation claim → Evidence → optional Fact | projected Fact + graph-visible reference material → estimate |
| Input assertion | source reported exact claim/context | graph resolved N references for exact Fact; contradictions supplied |
| Applicability | exact Observation conversion; promotion except narrow suppression | implicit exact reference/FactSupport membership only |
| Admission | compressed mechanical promotion or explicit narrow suppression | absent/assumed from resolved node for counting |
| Consumption | Fact copies Evidence id and claim coordinates | consumer counts nodes; does not examine assertion |
| Output standing | weak source-relative Fact or bounded suppression | confidence-shaped projection estimate / `None` for missing Fact |
| Authority | claim may not exceed source testimony | count/explicit-confidence/contradiction estimate only |
| Scope | workspace, claim/dimensions/time | exact Fact in supplied State/current invocation |
| Conflict | no generic admission conflict examination | separate contradiction count/penalty, no resolution |
| Unknown | no Typed Unknown on suppression | no Typed Unknown; absences compressed |
| Occurrence/preservation | events appended and replayable | output unpersisted; supporting ids/reasons only in returned object |
| Rebuildability | recorded artifacts replayable, truth not | current output rebuildable; prior invocation/reliance not |

The distinction that recurs is responsibility-local warrant: upstream construction/preservation cannot substitute for later applicability, admission, and use. The control road need not be structurally copied into the target road.

## 22. Producer → standing → consumer matrix

| Producer | Produced standing | Consumer | Consumer act and limit |
|---|---|---|---|
| Observation source | attributed observation testimony | `ObservationIngestor` | converts/records; source truth not verified |
| `observation_to_evidence` within invoked ingestion | canonical source-relative Evidence material | Fact promotion and State replay | exact claim/provenance payload preserved; occurrence tied to invocation/recording |
| `observation_to_fact` or suppression predicate | weak Fact assertion or bounded refusal | ledger/projector | event preserves assertion; no current standing |
| Event ledger | immutable ordered occurrence assertions | `StateProjector` | replay under rules, not truth adoption |
| `StateProjector` | currently recoverable projected material | Evidence Graph | resolves ids/forms visibility, not current standing |
| Evidence Graph | node/link/view or unresolved reference representation | Fact-confidence consumer | consumes cardinality and supporting ids only |
| contradiction builder | per-Fact contradiction representation | Fact-confidence consumer | counts and applies fixed penalty, does not resolve |
| `_fact_confidence` | bounded `FactConfidence` estimate | unspecified callers/CLI | any reliance beyond disclosed estimate authority remains unestablished |

## 23. Active / constructible / test / historical classification

| Road or act | Classification |
|---|---|
| Observation ingestion/conversion/event append | **runtime-active**, CLI-triggered in tests, test-active |
| exact Prometheus OS suppression | **runtime-active** when matching adapter output is ingested; test-active |
| in-memory/SQLite event preservation | **runtime-active**; only SQLite is cross-restart persistent |
| `StateProjector.project` full replay | **projection-replay-active**, runtime/CLI/test-active |
| snapshot/incremental projection paths | runtime-active where selected; test-active; not proof of a specific prior invocation |
| `build_evidence_graph` | runtime/CLI-triggered and test-active; also constructible-only absent a caller invocation; formatting surfaces are separate |
| compatibility alias `find_evidence_for_fact` | **compatibility-only** alias over canonical finder; test-active |
| `build_fact_confidence(s)` | runtime/CLI-triggered and test-active; returned record unpersisted |
| exact `fact_supported` / `evd_obs_1` trace | **test-active direct construction**, not runtime occurrence evidence |
| exact unresolved traces | **test-active direct construction** |
| graph applicability/admission standing | **absent** |
| graph/confidence Typed Unknown production | **absent**; generic helper active elsewhere only |
| a prior confidence invocation reconstructed from ledger | **absent/Unknown** |
| PR and earlier-report descriptions | **historical locator testimony** only |

## 24. Strongest contradictions

1. Graph explanation says “Seed believes this fact because” while the implementation establishes only resolved reference cardinality and the Book refuses graph membership as truth, belief, currentness, or admission. This is an external presentation phrase, not constitutional standing.
2. `EvidenceLink.relationship="supports"` and `strength=min(fact.confidence,node.confidence)` appear semantically rich, but `_fact_confidence` ignores link relation/strength and node confidence; it counts nodes. Graph richness therefore does not become confidence Uptake.
3. `EvidenceNode` preserves summary, type, event/run id, confidence, and time, yet the consumer examines none. Consumer-ready availability is not consumer applicability/admission/use of those coordinates.
4. An unresolved reference is expressly represented by the graph, but the confidence boundary makes it indistinguishable from no reference in count, ids, unsupported flag, and reason.
5. The Fact can carry explicit confidence high enough that adding/removing resolved Evidence does not change the numeric confidence, although count/reasons/unsupported characterization can change. Numeric stability is not absence of consumer movement.
6. Full projection replay can faithfully rebuild present material but neither proves the source occurrence was true nor that the confidence consumer previously ran or relied.

## 25. Strongest Unknowns

* Whether the exact source producer behind a replayed canonical Evidence actually occurred, beyond the bounded ingestion/record assertions available.
* Whether broader-than-source-relative Fact standing was ever lawfully established for a given producer/predicate.
* Whether the Evidence assertion—not merely its resolved id—is applicable to the exact confidence purpose now.
* Whether any responsible boundary admitted that assertion while preserving source authority, provenance, scope, freshness/expiry, conflict, known loss, and Unknowns.
* Whether `.50/.75` cardinality constitutes sufficient confidence for any external consumer purpose.
* What positive authority, if any, permits a later consumer to rely on `FactConfidence` beyond a deterministic projected estimate.
* Whether unresolved Evidence was absent historically, pruned by projection, unavailable in the retained corpus, malformed, or simply not yet appended.
* Whether every target consumer reran after an Event; no invocation ledger exists for graph/confidence calls.
* Historical invocation inputs (including alternate supplied graph/contradictions), caller purpose, rules/version, and reliance are not preserved by the returned object.

## 26. Smallest next honest connection

The recovery stops here. The **first exact current consumer-local Uptake crossing** is the conversion of the exact Fact view's resolved-node cardinality into `support_count`, a `.50/.75` support contribution, reasons, supporting ids, and `unsupported` standing in `FactConfidence`. The result is a bounded confidence-shaped estimate over projected material, not Evidence-assertion adoption, truth, currentness, verification, or authority to act.

The **smallest missing or compressed constitutional movement** is between graph resolution and counting:

```text
resolved canonical Evidence available in exact FactEvidenceView
→ [no explicit consumer-local applicability standing]
→ [no explicit consumer-local admission standing]
→ resolved membership counted
```

The earliest material compression is applicability: exact reference/FactSupport membership substitutes for a purpose-, claim-, scope-, source-, and time-aware determination. Admission is the next absent movement. This report does not propose artifacts or implementation for either. The lawful stopping point is the count-level Uptake and its estimate standing; goals, horizons, Questions, Answers, presentation, execution, and universal routing remain outside scope.

### Direct answers to the twenty governing findings

1. Canonical Evidence is produced by invoked `ObservationIngestor.observation_to_evidence`, with occurrence/preservation evidenced when `ingest_many` appends `evidence.observed`.
2. `_should_suppress_fact_promotion` explicitly refuses one exact Prometheus OS shape; otherwise `observation_to_fact` mechanically promotes, a compressed—not universal—admission boundary.
3. The Fact carries at most weak source-relative, evidence-linked, normalized, scoped standing; stronger/current/verified standing remains absent or Unknown.
4. The graph resolves projected ids, represents unresolved references, and forms deterministic node/link/view visibility.
5. It does not establish confidence-consumer applicability; exact membership is an implicit proxy.
6. It does not establish confidence-consumer admission; resolved presence is assumed countable.
7. The consumer directly receives the Fact, `FactEvidenceView` object, resolved node list, represented references, ids and explanation, but directly examines only node cardinality and supporting ids from the view.
8. Canonical identity becomes count membership; content/source/provenance/time/confidence/scope/authority/expiry are ignored or unavailable; event ids are transported.
9. Yes, but only partial/reference-level Uptake: resolved membership materially changes output.
10. The result is bounded `FactConfidence` estimate standing: confidence, support/contradiction counts, flags, reasons, and ids.
11. No Typed Unknowns are explicitly produced on either inspected road; the generic type/helper is used elsewhere.
12. Unresolved Evidence, missing Fact, applicability, admission, currentness, authority, and sufficiency are absence/compression, not Typed Unknown standing.
13. Capabilities exist for conversion, recording, suppression/promotion, replay, resolution, graph formation, count estimation, contradiction penalty, and rebuild; no constitutional applicability/admission capability is recovered here.
14. The first exact Gap is the confidence boundary's collapse of no reference and unresolved reference; richer semantic applicability/admission gaps matter only to stronger reliance.
15. No new current Demand is evidenced for the narrow estimator. Stronger current/truth reliance would face admission/authority Demand, but no such consumer is established.
16. Authority permits only deterministic confidence estimation over supplied projected inputs; no authority for truth/currentness/action is recovered.
17. A relevant appended batch can add/resolve Evidence and its Fact link; on a later replay/build/call the graph count and estimate may change. Append alone does not rerun consumers.
18. Present output is reconstructable from retained history and the same rules/limits; a prior invocation or reliance is not.
19. No: projection visibility becomes current standing nowhere by identity.
20. The first missing/compressed movement is explicit consumer-local applicability between resolved graph material and count eligibility; admission immediately remains absent behind it.
