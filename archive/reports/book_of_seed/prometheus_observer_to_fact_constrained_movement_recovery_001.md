# Prometheus observer-to-Fact constrained-movement recovery 001

## 1. Scope and negative authority

This is one bounded, Book-first, report-only recovery of the current merged implementation, using one `node_uname_info` vector sample as the primary witness. PRs 1624, 1822, 1886, 1973, and 1974 were treated only as locator testimony; no proposition below rests on their wording. The active Book, implementation, and current tests are the authorities examined.

This report does **not** establish an architecture, bless current names, or recommend a refactor, observer, schema, pipeline, deletion, migration, or durable Prometheus design. It does not continue into the Evidence Graph, confidence consumers, goals, horizons, Questions, Answers, execution, or presentation. A class, method, artifact, event name, and projection row are never treated as constitutional standing by identity.

The bounded witness is a successful vector result whose sample has `instance=192.0.2.115:9100`, `nodename=example_host`, `sysname=Linux`, and `[timestamp, "1"]`. Results for the other three allowlisted queries are mentioned only where they cause normalizers to emit additional rows.

## 2. Active Book clauses

The controlling clauses are:

* **01.External.A–D:** provider grammar remains attributed external grammar; translation must preserve source, scope, uncertainty, and authority limits; Fidelity is a bounded comparison, not certification.
* **Lenses, Views, and Roads:** availability, applicability, admission, and consumption are distinct. Call adjacency and typed carriage prove no constitutional road.
* **Acts and Act Artifacts:** construction of an act-shaped artifact does not prove the responsible act occurred; consumer validation is not producer occurrence.
* **Orientation and Movement:** movement begins from standing, burdens a responsibility, and may change standing only under warrant and constraints; implementation order is not constitutional order.
* **Testimony and Established Fact:** attributed testimony is not the testified proposition; Evidence is not Fact; a Fact artifact is not constitutional Fact standing.
* **Recording and Knowledge Extraction:** recording preserves an assertion but does not make it true, establish knowledge, renew occurrence, or mutate cluster truth.
* **05.Evidence.A–F:** an evidence identifier is distinct from support existence, applicability, verified provenance, producer occurrence, and independent corroboration.
* **06.State.A and the temporal amendment:** event order is not causation; projection selects and reconstructs material but neither establishes upstream standing nor current standing.
* **06.Projection.A–C:** projected visibility is not authority; losslessness is consumer-purpose-relative; rebuildability is not reconstruction of a prior invocation.

Therefore the constitutional comparison is always `external grammar ↕ bounded Fidelity ↕ constitutional grammar`, never Python/JSON/Prometheus vocabulary by identity.

## 3. Central finding

The current road evidences a **working, tested, frozen Prometheus realization** and several real occurrences (HTTP I/O, decoding attempts, artifact construction, ledger append, replay). It does **not** evidence formation or selection of a constitutionally standing Prometheus observer competency. The first missing/compressed crossing is before acquisition: no responsible movement establishes a bounded observation requirement, the applicability of this competency, selection of `node_uname_info`, and access authority. Hardcoded compatibility rules then decode and interpret provider material into source-attributed but boundary-weak `Observation` artifacts.

Downstream, every retained Observation is mechanically packaged as an `Evidence` artifact, and every nonsuppressed Observation is mechanically copied into a `Fact` artifact. Neither conversion examines applicability, admission, source authority, conflict, translation Fidelity, or sufficient support. Thus current Fact artifacts on this road are **fact-shaped projected material; constitutional Fact standing is Unknown**, not positively established. The OS row is the narrow exception: endpoint-scoped `node_uname_info` OS testimony is preserved as Observation and Evidence but refused Fact promotion by provider-specific negative compatibility metadata. Absence of that suppressor is the only positive gate for all other rows; it is not a positive constitutional warrant.

## 4. Current exact implementation topology

```text
configuration(base_url, timeout, source_type)
→ PrometheusObservationSource.collect()
  → for SAFE_QUERIES in fixed order
  → _query(query)
     → allowlist check
     → GET {base}/api/v1/query?query={query}
     → urlopen/read/UTF-8/JSON
     → object/status=success/data/resultType=vector/result=list checks
  → _observations_from_query(query, payload, seed_collected_at)
     → _prometheus_decoded_sample(sample) or skip
     → metadata construction
     → _prometheus_observation_shapes(query, decoded, metadata)
     → PrometheusObservationSource._observation(...), confidence=0.95
→ ObservationCollectionService.collect()
  → source.collect()
  → _normalize_observation(): type/source_type validation + observation_source metadata
  → StateProjector(ledger).project(workspace)
  → DEFAULT_OBSERVATION_NORMALIZATION_PIPELINE.normalize(new, state=current)
     → EndpointAliasNormalizer
     → EndpointIdentityNormalizer
     → PredicateNormalizer
     → originals retained + deduplicated derived Observations
  → ObservationIngestor.ingest_many()
     → observation_to_evidence()
     → _should_suppress_fact_promotion()
     → observation_to_fact() unless suppressed
     → observation.observed, evidence.observed, fact.observed/fact.inferred Events
     → EventLedger.append_many()
→ StateProjector.project()
  → replay apply(): reconstruct Observation/Evidence/Fact dictionaries
  → finalize(): aliases, retention, supports, relationships, conflicts, indexes
  → projected State material
```

For the primary sample itself, `_prometheus_observation_shapes` emits only endpoint-scoped `os=linux`. Because `nodename` and `instance` are copied into metadata, `EndpointAliasNormalizer` also emits `example_host --prometheus_instance→ 192.0.2.115:9100`. Predicate normalization can add canonical rows for other query samples (`up→availability_status`, filesystem names), but does not create an extra OS row. `EndpointIdentityNormalizer` can additionally derive `alias` only when an identity claim (`ip_address`, `alias`, or `ansible_host`) from the current batch or projected facts matches the endpoint base; that claim is not produced by this uname sample.

## 5. Constitutional movement topology

The evidenced topology is not an eight-stage pipeline:

```text
[requirement/applicability/selection/authority: absent or Unknown]
→ external request execution occurrence (evidenced only at live invocation)
→ bounded structural decoding (evidenced)
→ provider-local interpretation/translation (frozen realization; compatibility tested)
→ Observation artifact production (evidenced)
→ source-relative testimony preservation (partial: rich metadata, weak assertion boundary)
→ internally derived relation artifact production (evidenced; warrant mixed/absent)
→ Evidence representation conversion and recording (evidenced artifacts; admission absent)
→ Fact artifact construction or narrow refusal (evidenced implementation)
→ event-record preservation (evidenced when append succeeds)
→ replay/material projection (evidenced)
[constitutional Fact establishment/current standing: absent or Unknown]
```

Real constitutional movements here are acquisition occurrence, attributed testimony production/preservation, derivation of a relation assertion, explicit refusal of one promotion, recording, and bounded projection. Structural decode, field shaping, copying, ID allocation, and object construction are transformations unless a separate responsible boundary supplies standing.

## 6. Candidate movement inventory without forced cardinality

| Candidate | Classification | Occurrence | Finding |
|---|---|---|---|
| observation need establishment | absent | absent | no need subject or requirement reaches the source |
| competency applicability | absent | absent | configuration/invocation substitutes for examination |
| competency selection | absent | absent | service receives an already-selected object |
| acquisition authorization | Unknown | Unknown | read-only/GET/allowlist constrain method, not network authority |
| external acquisition | evidenced | runtime-active | `urlopen` context proves code performs I/O when run; tests fake it |
| provider grammar decoding | evidenced / compatibility-only | runtime-active, test-active | bounded envelope/sample structural checks |
| translation/interpretation | evidenced / frozen realization | runtime-active | query branches choose subject, predicate, value, time, metadata |
| Observation testimony production | partially evidenced | runtime-active | artifact produced; source-relative assertion is implicit rather than typed |
| normalization | mixed | runtime-active | lexical predicate mapping plus relational derivation |
| derivation | evidenced but warrant compressed | runtime-active | alias rows are internally produced |
| Evidence production | mixed | runtime-active | preservation-shaped packaging without admission/support examination |
| Evidence preservation | evidenced | runtime-active, projection-replay-active | event payload and projected dictionary retain artifact |
| Fact support examination | absent | absent | no applicability, admission, conflict, independence, or authority check |
| Fact establishment/refusal | mixed | runtime-active | mechanical construction for most; one narrow negative refusal |
| event recording | evidenced | runtime-active | append after complete collection/normalization |
| projection | evidenced | projection-replay-active | material reconstruction and derived indexes |

## 7. Observer competency formation analysis

No current road accepts evidence about an external representation and produces bounded observer competency standing after Fidelity examination.

| Formation responsibility | Current basis | Classification |
|---|---|---|
| endpoint reachability | base URL configuration; I/O success/failure | configuration; runtime result, not standing |
| permitted request method | hardcoded GET | frozen implementation assumption |
| allowed query identity | `SAFE_QUERIES` | frozen realization / compatibility-only |
| response-envelope grammar | `_query` checks | tested compatibility |
| sample grammar | `_prometheus_decoded_sample` | tested compatibility |
| metric semantics | query-name branches | frozen implementation assumption |
| label semantics | `instance`, `nodename`, `sysname/system`, filesystem labels | frozen realization |
| time interpretation | sample tuple first element → UTC `observed_at` | tested compatibility; provider authority asserted in metadata only |
| subject formation | `instance` endpoint, later nodename relation | frozen realization |
| predicate formation | hardcoded strings + predicate catalog normalizer | mixed frozen realization/compatibility |
| confidence rule | constant `0.95`, minimum for derivations | unsupported implementation convention |
| authority limits | read-only and provider metadata | partially represented; not established |
| failure interpretation | exception→`last_error`+`[]`; malformed sample→skip | frozen realization; not Typed Unknown |

Tests are evidence of intended compatibility and current behavior, not evidence that provider semantics, access authority, or constitutional competency was established. No candidate method/decoder/translator evidence set, competency identity, applicability boundary, or Fidelity finding is preserved.

## 8. Observer competency invocation analysis

Invocation starts with an already-constructed source and a call. It establishes neither why observation is required nor why Prometheus is applicable. The exact query is selected because the class iterates its fixed tuple, not because a bounded requirement selected it. Network authority is unrepresented. Successful I/O makes response material available in-process; it does not prove the provider proposition.

What is recoverable: configured endpoint/name/type/timeout; fixed query; GET URL and Accept header in the running call; receipt sufficient to read bytes; decode/shape rules in the current code; sample and collection times in emitted metadata; broad failure text in `last_error`; translated artifacts and recorded payloads after success. What is not recoverable: requirement, selection act, access grant, original response bytes after translation, refused sample coordinates, translator version/identity, competency standing, or historical invocation after process exit (apart from translated event material).

## 9. Frozen scaffolding versus recoverable grammar matrix

| Responsibility | Present character | Constitutional standing |
|---|---|---|
| HTTP route/query/request/JSON/vector knowledge | provider-specific frozen realization, runtime necessity | foreign grammar; no competency standing |
| structural boundary checks | provider-specific compatibility support | bounded decode occurrence when invoked |
| source-relative testimony principle | shared constitutional movement | partially realized by metadata and Evidence payload |
| subject/predicate/value interpretation | provider-specific frozen realization | translation artifact; warrant Unknown |
| Observation representation | general implementation grammar | artifact, not testimony standing by identity |
| source validation/metadata augmentation/orchestration | shared runtime scaffolding | mixed orchestration, not one act |
| endpoint relation derivation | general-ish normalizer realization | internal relational assertion; derivation warrant compressed |
| Evidence/Fact conversion | shared runtime implementation | representation conversion, not establishment automatically |
| event append and replay | shared runtime necessity | recording/projection acts within their narrow claims |
| prior Prometheus implementations/PRs | locator testimony | historical; no active authority |

The operator's “frozen scaffolding competency” is consistent with the implementation evidence only if “competency” means executable ability. The repository has that ability; it does not preserve constitutional Capability or observer-competency standing. Whether provider code should survive is outside authority.

## 10. Prometheus acquisition analysis

| Act | Owner | Input/output standing | Authority and failure | Occurrence/preservation |
|---|---|---|---|---|
| query selection | `collect` fixed iteration | config → query string | allowlist constrains; applicability absent | selection reason not recorded |
| request formation | `_query` | base URL/query → Request | GET/read-only convention; network authority Unknown | Request transient |
| network request | `urlopen` | Request → response context | configured timeout; HTTP/URL/OS errors | occurred only if call executes; no request event |
| response receipt | response context/read | response stream → bytes | HTTP success alone not truth | bytes transient and erased |
| response decoding | UTF-8 + `json.loads` | bytes → Python material | shape exceptions collapse collection | decoded envelope transient |
| response validation | `_query` | material → accepted vector envelope | validates object/success/vector/list only | rule in code; outcome not separately preserved |
| sample extraction | decoder loop | result item → decoded sample or skip | malformed item silently skipped | accepted coordinates partially copied; refusal absent |

Configured URL is not reachability; allowlisting is not applicability; Request construction is not occurrence; HTTP success is not proposition truth.

## 11. External grammar decoding analysis

Recognized envelope grammar is exactly: top-level dictionary; `status == "success"`; `data` dictionary; `resultType == "vector"`; `result` list. Recognized sample grammar is: sample dictionary; `metric` dictionary; `value` list of at least two entries; nonempty string `metric.instance`; finite/representable numeric timestamp in `value[0]`; arbitrary `value[1]`. Extra tuple entries and fields are accepted. Metric and label value types are mostly checked only when interpreted.

This establishes **shape acceptance**, not provider meaning, metric semantics, source authority, currentness, completeness, or truth. `status=success` is external provider grammar accepted for compatibility. A recognized metric name merely selects a hardcoded translator. The original JSON bytes, envelope extras, and skipped samples are not preserved.

## 12. Translation analysis

For the uname witness:

| Coordinate/decision | Result | Character |
|---|---|---|
| external coordinates | query, complete metric-label dict, raw/parsed sample timestamp, sample value | translation input; sample value is semantically ignored |
| subject | `metric.instance` | interpretation; endpoint-scoped |
| predicate | `os` | implementation convention / translation |
| value | lowercased stripped `sysname` or `system` | interpretation; unknown names accepted, missing name refuses row |
| dimensions | `{}` | implementation convention; labels remain metadata |
| source | `source_type` (default provider), source_name prometheus, base URL | partial attribution |
| observed time | provider sample timestamp | translation; collection time separately metadata |
| confidence | `0.95` | invented coordinate without recovered warrant |
| expiry | `None` | invented/open-ended coordinate; no currentness warrant |
| authority limit | read_only, GET, provider time authority | descriptive metadata, not an admitted authority boundary |
| known loss | no explicit field | bytes/envelope/query outcome/ignored sample value/translator version lost |

Endpoint versus stable host is decided twice: source translation emits endpoint OS and attaches nodename metadata; alias normalization makes the identity-relative relation. Labels become filesystem dimensions only for three allowlisted labels and two filesystem predicates; otherwise the label dictionary stays metadata. `source_type=provider` comes from constructor default, not a finding that this source role was examined. The class sets confidence and temporal intent without evidence of the rule.

## 13. Observation standing matrix

| Produced claim | Subject/assertion | Standing | Scope/authority/time | Loss/conflict/stop |
|---|---|---|---|---|
| uname OS | endpoint says translated uname OS is linux | partially evidenced source testimony | provider endpoint; sample time; read-only acquisition; confidence label 0.95 unwarranted | source-relative boundary only in metadata; no conflict handling; stop at testimony |
| uname alias | nodename has `prometheus_instance` endpoint | internally derived relational testimony | nodename/endpoint pair; max input time; min confidence | derivation disguised under provider source type; stop before establishment |
| endpoint identity alias (conditional) | prior identity subject aliases endpoint | internally derived relational material | current batch + nonexpired projected fact-shaped material | prior applicability/admission Unknown; mixed lineage |
| predicate canonical row (other samples) | same endpoint has canonical predicate/value | internally derived translated material | copied source scope/time; rule-defined | translator/normalizer is producer but source_type stays provider |

Canonical Observation eight dimensions: **subject** endpoint; **assertion** `os=linux`; **standing** source-attributed translated testimony at best; **source/provenance** provider name/base/query/labels and Observation id; **responsibility** source decoder/translator; **authority/warrant** read-only compatibility, semantic warrant Unknown; **scope/locality** one endpoint/sample; **occurrence/preservation** produced in memory then event-preserved. Known loss, conflict, Typed Unknown, and expiry authority are not first-class. The representation can be read as “X is true of S” because `subject/predicate/value` carry no typed “Prometheus reported” modality; metadata is required to recover the weaker boundary.

## 14. Collection-service decomposition

`ObservationCollectionService.collect` is **several compressed acts behind an orchestration boundary**, not one constitutional act. It coordinates source invocation; materializes all results before writes; validates returned class and `source_type`; augments metadata; projects current State; invokes normalization; ingests; and emits transient lifecycle/timing diagnostics. It performs no observation-requirement, competency-applicability, selection, or authority examination. Its projected-State construction is a consumer preparation step, not Fact establishment. `ObservationProducerLifecycle`/`ExecutionStatus` records transient progress messages; it proves neither external acquisition nor constitutional production and is not ledger testimony.

## 15. State-aware normalization decomposition

| Normalizer | Inputs/comparison | Output/warrant | Time/confidence/source | Admission/conflict/Unknown |
|---|---|---|---|---|
| `EndpointAliasNormalizer` | all growing batch Observations; hostname/nodename + instance/endpoint metadata | stable-name relation; lexical/provider convention | latest input time, earliest expiry, minimum confidence, first metadata/source type | no applicability/admission/conflict; groups same tuple |
| `EndpointIdentityNormalizer` | endpoint base vs `ip_address`/`alias`/`ansible_host` from batch and nonexpired `state.facts` | `identity.subject alias endpoint`; equality match is implicit warrant | max identity/endpoint time, earliest expiry, min confidence, endpoint source type | expiry only; no establishment/applicability/admission/conflict check |
| `PredicateNormalizer` | configured mapping/value rules over all accumulated observations | canonical predicate/value Observation | implementation rule; inherited coordinates/derived metadata | compatibility mapping, not semantic support examination |
| pipeline | originals + sequential derivations | retains originals, deduplicates derived keys | deterministic derived ids | duplicate suppression is not corroboration/conflict adjudication |

These are mixed translation and derivation, not merely lexical normalization. The state-aware input is `State.facts.values()`: Fact artifacts reconstructed from events and filtered only for expiry, not constitutional Facts or currently admitted standing.

## 16. Critical projected-Fact → derived-Observation → Evidence → Fact cycle

1. Previous standing consumed: a projected `Fact` artifact; constitutional standing is Unknown.
2. Applicability: only predicate membership, parseable identity value, endpoint-base equality, and non-expiry.
3. Admission: none.
4. Assertion: identity subject `alias` endpoint.
5. Owner: `EndpointIdentityNormalizer`, though output retains the endpoint Observation's `source_type`.
6. Representation as Observation: required by pipeline protocol; no constitutional reason is recovered.
7. Attribution: mixed—metadata names normalizer and antecedent ids, while source type and most metadata come from the endpoint's external source.
8. It becomes Evidence exactly like source output and, absent suppressor, a Fact artifact exactly like source output.
9. Fact preserves only evidence id/source type/inferred boolean, not derivation metadata directly; metadata remains reachable through Evidence.
10. Deterministic derived Observation id can prevent a duplicate event id only indirectly? No: ledgers reject duplicate event ids, not duplicate Observation ids; separate collections can append events carrying the same derived Observation id and create fresh Evidence/Fact ids.
11. Repeated collection therefore creates new Evidence and Fact identities for materially dependent testimony, which can appear as recurrence or corroboration to ID-counting consumers, although derivation metadata may expose shared antecedents.
12. `source_type` is collapsed to the endpoint source; `inferred` is false unless source_type literally equals `inferred`.

The resulting standing is **mixed observational/inferential/relational/projected**. It is not newly sensed. It should not be granted external testimony standing merely because its Python representation is `Observation`; whether the artifact remains properly classified constitutionally is Unknown/unsupported. No naming recommendation follows.

## 17. Evidence production analysis

`observation_to_evidence` is a **representation conversion plus provenance packaging**, and event append subsequently preserves it. It allocates a fresh id, labels source `observation:{source_type}`, copies observed time, subject/predicate/value/metadata/dimensions/expiry, and copies confidence. It does not examine producer occurrence, authority, translation Fidelity, scope applicability, conflicts, known loss, uncertainty, derivation dependence, consumer purpose, or admission.

Thus every raw and derived Observation receives an Evidence artifact and `evidence.observed` record, including the suppressed OS claim. That is evidenced preservation-shaped standing, not stronger Evidence standing, truth, or independent support. A new Evidence identity can obscure shared dependence; lineage remains only inside copied metadata and observation id.

## 18. Fact establishment/refusal analysis

The transition is mechanical:

```text
Observation + newly allocated Evidence
→ if exact Prometheus/uname/os suppression metadata: None
→ else Fact(copy coordinates, evidence_ids=[new id])
```

`observation_to_fact` performs no interpretation, normalization, applicability, admission, source-authority comparison, conflict examination, or support-sufficiency examination. It sets `inferred` only when `source_type == "inferred"`. That boolean is insufficient to preserve normalizer derivation because normalizers retain the provider source type. Fact does not directly preserve producer, query, translator, or normalizer; navigation through Evidence is required and cannot restore unrecorded warrant.

The exact suppressed claim is `subject=<endpoint>, predicate=os, value=<translated sysname>`, when shape metadata says suppression is true and ingestion verifies source_name prometheus plus metric node_uname_info. The implementation comment says uname alone is authoritative for stable host identity, yet it suppresses OS because the subject is endpoint-shaped; it does not translate OS onto nodename. This is **provider-specific negative compatibility logic**, not a general constitutional admission decision. Nonsuppressed claims are accepted solely because the predicate returns false. There is no positive warrant.

Accordingly: OS gets Observation and Evidence artifacts but no Fact artifact. The nodename→endpoint derived relation and other raw/canonical Prometheus claims get Fact artifacts. **No claim on this road has recoverable constitutional Fact standing solely from this producer.** Reconstructing a Fact artifact proves a recorded fact-shaped assertion, not establishment occurrence.

## 19. Event-recording analysis

| Kind | What it actually preserves | Lineage/authority limit |
|---|---|---|
| `observation.observed` | serialized Observation artifact and event recording occurrence | caller causation only; does not prove external producer occurrence or truth |
| `evidence.observed` | serialized Evidence package + Observation id/source type | causation defaults to Observation id (not an Event); represented linkage, not verified causation/admission |
| `fact.observed` | serialized nonsuppressed Fact artifact + Observation id/source type | causation defaults to Evidence event id; does not prove Fact establishment or external observation |
| `fact.inferred` | same Fact shape forced inferred on replay | chosen only from source_type; does not make inference lawful or preserve normalizer derivation automatically |

Batch order is Observation, Evidence, optional Fact per input. It is implementation sequence, not constitutional causation. `append_many` validates duplicate event ids and stores/copies events; SQLite uses one transaction. Recording proves those event records were appended if the call succeeds, not that acquisition, translation Fidelity, support, or establishment occurred lawfully.

## 20. Projection/rebuildability analysis

`StateProjector.apply` reconstructs serialized Observations, Evidence, and Facts into dictionaries; `finalize` builds alias resolution, measurement retention, observed/inferred partitions, FactSupport, relationships, conflicts, and other indexes. Replay can reconstruct retained artifact coordinates, event order, event metadata/link fields, and whatever provenance survived payloads. It can rerun current projection rules over those records.

Replay cannot reconstruct original bytes, complete response envelopes, skipped samples, request/response occurrence evidence, decoder or translator version/rules at historical invocation, normalizer rules at historical invocation, requirement, competency selection/standing, network authority, translation Fidelity, admission, Fact-establishment warrant, consumer purpose, or the historical in-memory invocation. Successful full replay validates only current material reconstruction under current code, not the observer chain or current standing.

## 21. Typed Unknown matrix

| Candidate | Actual representation | Classification |
|---|---|---|
| endpoint unreachable / request unauthorized / provider unavailable | caught exception → `last_error` and `[]` | failure/absence; not Typed Unknown |
| envelope grammar unrecognized | `ValueError` caught → `last_error` and `[]` | failure; not Typed Unknown |
| sample malformed/timestamp unavailable | silent skip | absence; not Typed Unknown |
| metric semantics unavailable | no recognized branch or missing sysname → `[]` shape | compression/absence |
| subject identity unresolved | endpoint remains subject; no derived alias | absence, not explicit Unknown |
| provider timestamp unavailable | sample skipped | absence |
| translation loss | unrepresented | Unknown to recovery |
| normalization ambiguity/conflicting identities | may emit multiple aliases; no Typed Unknown | mixed/conflict unexamined |
| prior Fact standing unavailable | projected artifact consumed anyway | Unknown erased at boundary |
| Evidence applicability unresolved | never represented | absent |
| Fact support insufficient | only narrow suppression; otherwise promotion | absent |
| producer occurrence unavailable | never typed | Unknown/compressed |

**Explicit Typed Unknowns on this road: none.** `last_error`, empty list, skip, `None`, and suppressed Fact are distinct failure/refusal/absence representations and are not Typed Unknown by identity.

## 22. Capability matrix

| Capability | Availability/applicability/selection | Authority/execution/result/verification/standing |
|---|---|---|
| external acquisition | executable source available; applicability/selection absent | access authority Unknown; execution runtime-active; response not independently verified; frozen ability |
| provider decoding | callable rules selected by collector | structural result tested; semantic verification absent; compatibility-only |
| sample translation | callable branch selected by query | execution active; rules tested, warrant absent; frozen realization |
| Observation production | available/automatic | artifact result evidenced; testimony boundary partial |
| source attribution | available/automatic | rich metadata, no competency/authority verification; partial |
| state-aware comparison | default pipeline active | nonexpiry/equality only; prior standing Unknown; mixed |
| identity relation derivation | available when coordinates match | derivation executed; warrant/admission absent |
| Evidence preservation | automatic for every Observation | ledger occurrence evidenced; support standing not verified |
| Fact support examination | no capability boundary | absent |
| Fact establishment | constructor available/automatic | artifact generated; constitutional capability standing absent |
| Fact refusal | exact suppressor available | runtime-active narrow compatibility refusal |
| event recording | ledger available | append execution verifiable in-process/persistence; no truth authority |
| projection rebuild | projector available | replay-active and tested; reconstructs material, not upstream standing |

Capability identity, availability, applicability, selection, authority, execution, observed result, verification, and current standing are nowhere unified. Most are implementation abilities without constitutional Capability standing.

## 23. Gap matrix

| Required standing | Present standing | Exact consumer and local consequence | Materiality |
|---|---|---|---|
| bounded observation requirement + applicable selected competency + access authority | configured callable source | collector executes all fixed queries without recoverable reason/authority | first, material Gap |
| warranted provider grammar/semantic translation | tested hardcoded compatibility | translator produces constitutional-looking coordinates without recoverable semantic warrant | material |
| source-relative Observation with disclosed loss | metadata-rich artifact | ingestor treats it as direct claim; loss/authority limits are not examined | material |
| applicable/admitted prior Fact | nonexpired projected Fact artifact | identity normalizer derives a relation | material recursive Gap |
| internally derived standing and dependency | provider-typed Observation + metadata | Evidence/Fact converters treat it like ordinary testimony | material |
| independent support examination | fresh Evidence id | Fact constructor binds one id, allowing dependence to look new | material for later support counting; downstream not pursued |
| positive Fact-establishment warrant | absence of exact suppressor | ingestor constructs Fact artifact | material |
| recoverable establishing occurrence | ordered event records | projector rebuilds artifact but not act/warrant | material explanatory Gap |

Not every compression is a Gap: a combined HTTP decode function is merely implementation compression where the consumer only needs accepted decoded material; deterministic ID/dedup is implementation behavior; one orchestration method is not itself unconstitutional. Gaps are claimed only at consumers that strengthen or rely on standing.

## 24. Demand matrix

Demand is narrower than Gap and requires an applicable requirement plus comparison and consequence.

| Requirement | Comparison | Consumer-local consequence | Demand finding |
|---|---|---|---|
| preserve source-relative testimony | Book 01.External.C vs metadata-dependent modality and mechanical promotion | ingestor can read provider testimony as subject truth | evidenced bounded Demand at ingestion |
| preserve provider provenance | payload retains base/query/labels/times but not bytes/rules/version/loss | replay cannot explain exact translation | partially evidenced Demand; exact required retention remains Unknown |
| derive identity relations | equality/nonexpiry inputs vs no applicability/admission | relation artifact can be promoted | evidenced bounded Demand for standing examination, not for implementation change |
| establish a Fact | Book Fact distinction vs mechanical copy | projected fact-shaped material can be relied upon as Fact | evidenced Demand at promotion boundary |
| avoid false corroboration | fresh IDs vs shared source/derivation | ID-counting consumer may overcount | evidenced consumer-local Demand to preserve dependence; no downstream continuation |
| rebuild current understanding | retained artifacts vs lost production/warrant | replay rebuilds material but not lawful standing | partially evidenced; “current” requirement itself needs consumer scope |
| explain why a Fact exists | event/Evidence navigation vs no positive warrant | can explain mechanics, not establishment | evidenced Demand at explanation boundary |

No Demand follows merely from provider-specific scaffolding existing, nor from a speculative permanent architecture.

## 25. Fidelity crossing matrix

| Crossing | Preserved | Erased/invented/changed | Standing/authority finding |
|---|---|---|---|
| bytes → decoded response | recognized JSON fields | raw bytes/encoding/envelope extras erased; Python types introduced | structural acceptance only |
| response → decoded sample | metric dict, instance, raw+UTC time, value | sample container/extras/index lost; malformed silently erased | decoded external material only |
| sample → Observation shape | endpoint, OS mapping, sample time, metadata | sample value ignored; `os`, lowercase, suppression invented; scope chosen | translation; no semantic Fidelity finding |
| shape → Observation | coordinates/metadata | id and 0.95 invented; dimensions `{}`; source type assigned; expiry omitted | artifact testimony, authority not strengthened lawfully |
| Observation → derived Observation | antecedent ids in metadata, min confidence, bounded expiry | subject/predicate/value/time/source attribution may change; derivation producer mixed | inferential relation, not new sensing |
| Observation → Evidence | most fields copied | new identity, source string/kind invented; no loss/conflict/admission | preservation packaging, no strengthening |
| Observation + Evidence → Fact artifact | claim, dimension, time, confidence, expiry, evidence id | Observation metadata/producer method indirect; inferred often false; establishment time absent | artifact construction, not Fact standing |
| artifacts/events → State | serialized coordinates/order | original bytes/rules/warrants/invocation absent; projection indexes introduced | projected material, not current standing |

No examined crossing has a stored bounded Fidelity finding. Field copying is not Fidelity; no crossing receives global certification.

## 26. Eight-dimensional matrices for every distinct produced standing

| Produced standing | Subject | Assertion | Standing | Provenance | Responsibility | Authority/scope | Occurrence/preservation + Unknown/stop |
|---|---|---|---|---|---|---|---|
| decoded sample | endpoint-labelled provider sample | metric labels/value existed in accepted vector item | decoded external material | configured endpoint/query and response item, transient | decoder | structural grammar only, one sample | runtime decode; not separately preserved; semantics Unknown; stop before testimony |
| endpoint OS Observation | endpoint | provider uname interpreted as OS | partial attributed testimony | base/query/labels/sample+collection times | source translator | read-only external sample, endpoint-local | artifact/event; confidence/warrant/loss Unknown; stop before Fact |
| nodename Prometheus-instance Observation | nodename + endpoint | relation between stable label and scrape endpoint | internally derived relation | source Observation id(s), normalizer metadata | alias normalizer | equality of supplied labels, local batch | artifact/event; derivation admission Unknown; stop before external testimony claim |
| conditional identity alias Observation | prior identity subject + endpoint | alias relation | mixed projected/inferential relation | projected Fact id + endpoint Observation ids | identity normalizer | nonexpiry/base equality only | artifact/event; prior Fact standing Unknown |
| canonical predicate Observation | endpoint | mapped predicate/value | internal translation/normalization | original id + mapping metadata | predicate normalizer | configured rule | artifact/event; semantic warrant Unknown |
| Evidence artifact (each above) | copied claim | this Observation package exists | represented provenance/support candidate | fresh id + copied payload | ingestor converter | no admission or authority exam | evidence event; independence Unknown; stop before support acceptance |
| nonsuppressed Fact artifact | copied claim subject | claim represented as Fact | fact-shaped material; constitutional standing Unknown | Evidence id, indirectly Observation | ingestor constructor | absence of suppressor only | fact event/projection; establishment absent |
| suppression/refusal result | endpoint OS promotion | no Fact artifact emitted | narrow implementation refusal | suppression metadata/reason | shape translator + ingestor gate | exact provider/metric/predicate scope | Observation/Evidence retained; no explicit refusal event/Typed Unknown |
| event record | workspace/event id | named artifact was recorded | immutable record assertion | payload/link fields/order/time | ledger caller/ledger | workspace + storage boundary | append occurrence; upstream truth/causation Unknown |
| projected material | workspace dictionary/index member | retained artifacts exposed under replay rules | projected representation | events and current projector rules | projector | replay/finalization scope | rebuild active; current/constitutional standing Unknown |

## 27. Object-bias audit

| Noun | What it actually is/hides |
|---|---|
| `PrometheusObservationSource` | implementation owner compressing config, fixed selection, request, decode, interpretation, attribution, and artifact construction; not constitutional observer by identity |
| `ObservationCollectionService` | orchestration/compatibility boundary across invocation, validation, metadata, projection, normalization, ingestion, diagnostics; not one act |
| `ObservationNormalizationPipeline` | sequencing/dedup representation plus relational and lexical movements |
| `EndpointAliasNormalizer` | implementation owner of a derivation act; “normalization” hides relation assertion |
| `EndpointIdentityNormalizer` | state-consuming comparison/derivation owner; consumes fact-shaped material |
| `Observation` | representation that may contain external testimony or internal derivation; not one standing |
| `Evidence` | representation/provenance package; not admitted support by identity |
| `Fact` | representation; may be fact-shaped without establishment standing |
| `Event` | record artifact/assertion; not occurrence/truth automatically |
| `State` | projected container/material, not constitutional current State standing |
| observer | external shorthand unless competency, requirement, authority, and invocation stand |
| normalizer | external shorthand spanning translation and derivation |
| ingestor | implementation owner spanning packaging, artifact construction/refusal, event formation, recording coordination |
| projector | implementation owner of replay/material reconstruction, not truth or current-standing owner |

## 28. Active/runtime/test/constructible/historical classification

| Surface | Standing classification | Occurrence classification |
|---|---|---|
| Prometheus source, HTTP/decode/translate | frozen realization / compatibility-only | runtime-active when configured; test-active |
| default normalization | mixed | runtime-active by collection default; test-active |
| collection service | compressed orchestration | runtime-active, constructible-only where no caller configures it |
| ingestor + in-memory ledger | mixed conversion/recording | runtime-active, test-active |
| SQLite ledger | compatibility support/persistence | runtime-active when selected; test-active |
| State projection | evidenced representation act | projection-replay-active, runtime-active, test-active |
| ExecutionStatus | transient implementation visibility | formatting/progress-only; runtime-active |
| PR locator testimony | foreign to active authority | historical |
| observer competency formation | absent | absent |
| constitutional Fact establishment on this road | absent/Unknown | absent/Unknown |

## 29. Strongest contradictions

1. The implementation calls artifacts `Observation`, `Evidence`, and `Fact` in a mechanical sequence, while the Book requires testimony, applicable represented support, and established Fact to remain distinct standings.
2. `node_uname_info` is described in code as authoritative for stable host identity, yet its direct OS claim remains endpoint-scoped and is suppressed; the stable-host output is an internally derived endpoint relation, not stable-host OS testimony.
3. Derived normalizer output declares `derived=true` but retains provider `source_type`, so the artifact simultaneously exposes internal derivation and ordinary provider testimony grammar.
4. A projected Fact artifact is used to derive a new Observation without proving Fact standing, applicability, or admission.
5. A narrow negative suppression rule is treated as the entire promotion boundary; nonsuppression supplies no positive establishment warrant.
6. Fresh Evidence/Fact ids are produced per ingestion while source dependence can remain shared, conflicting with the Book's warning that identifiers and sequence are not independent support or causation.
7. Replay is complete for retained artifacts but incomplete for the acts and warrants their names imply.

## 30. Strongest Unknowns

* Why an observation is needed, why Prometheus is applicable, why each fixed query is selected, and who authorizes network access.
* What evidence established Prometheus envelope, sample, metric, label, timestamp, subject, predicate, and confidence semantics.
* Whether the endpoint is the constitutionally correct subject for OS, and what authority the nodename label has.
* What `0.95`, no expiry, and “current_instant” lawfully mean.
* What malformed/skipped/unavailable material existed and what loss translation introduced.
* Whether projected Fact artifacts consumed by normalization ever possessed Fact standing or are applicable/admitted for identity derivation.
* Whether derived Observations are intended as testimony, inference, relationship proposals, or compatibility rows.
* Whether any nonsuppressed claim has sufficient, independent, conflict-examined support.
* Whether a historical request, decode, translation, derivation, or establishment occurred after only its final payload remains.

## 31. Smallest next honest decomposition

The recovery stops at the first compressed crossing:

```text
bounded observation requirement
+ candidate Prometheus implementation ability
+ evidence of endpoint/query/grammar/semantics
+ applicability and access authority
→ (currently absent) bounded observer competency selection/invocation standing
→ acquisition
```

The smallest honest decomposition is descriptive, not prescriptive: keep **competency formation**, **competency invocation**, **external acquisition occurrence**, **structural decoding**, **source-relative translation/testimony**, **internal derivation**, **Evidence applicability/admission**, **Fact establishment/refusal**, **recording**, and **projection** distinguishable. The implementation currently compresses or omits several of these. This report makes no implementation recommendation.

## Direct answers

1. **How are Facts produced?** Fixed queries are fetched, vector samples decoded, query branches emit Observations, default normalizers retain originals/add derivations, the ingestor allocates Evidence, and—unless the exact OS suppressor matches—copies each Observation into a Fact and records all artifacts.
2. **Standing at each step?** Configuration; transient external material; structurally decoded provider material; partially attributed testimony artifacts; mixed internal derivations; provenance/Evidence artifacts; fact-shaped artifacts; recorded assertions; projected material. Constitutional Fact/current standing is Unknown.
3. **Only implementation transformations?** URL/Request formation, JSON/Python conversion, structural field extraction, object/id construction, copying, batching, and dictionary reconstruction.
4. **Constitutional movements?** Actual acquisition, bounded testimony production/preservation, relation derivation, narrow refusal, recording, and projection—only within evidenced limits.
5. **Inside `PrometheusObservationSource`?** Configuration, fixed query choice, request formation/execution, response decode/validation, sample decode, provider semantic interpretation, subject/predicate/value/time/confidence formation, attribution, suppression marking, and Observation construction.
6. **Inside collection service?** Invocation, return validation, attribution augmentation, projected-State construction, normalizer orchestration, ingestion, status, and diagnostics.
7. **Inside ingestor?** Evidence packaging, suppression decision, Fact construction, event/link construction, batch append coordination, and returned Fact filtering semantics.
8. **Observer competency standing?** No.
9. **Frozen implementation competency?** Yes: executable, tested provider-specific ability, without constitutional competency standing.
10. **Decoder/translator evidence?** Active code and compatibility tests establish current behavior; no preserved provider-semantic evidence or Fidelity warrant was found.
11. **One uname sample becomes?** One endpoint OS Observation; one nodename→endpoint derived Observation when nodename exists; Evidence for each; no OS Fact; a relation Fact artifact for the derived row. Conditional identity normalizers can add another alias only with separate identity material.
12. **Endpoint-relative?** Raw OS; all other raw query claims; canonical predicate variants remain endpoint-scoped.
13. **Identity-relative?** `nodename prometheus_instance endpoint`, plus conditional alias relations.
14. **Internally derived?** Alias/identity relations and predicate-normalized variants.
15. **Evidence?** Every raw and derived Observation, including suppressed OS.
16. **Fact artifacts?** Every nonsuppressed raw/derived Observation; not the exact suppressed OS row.
17. **Constitutional Fact standing?** None is recoverably established by this road; Unknown.
18. **Suppressed OS?** Endpoint-scoped translated uname `os`; suppressed by explicit metadata/reason to avoid endpoint-subject promotion.
19. **Positive nonsuppression warrant?** None; only failure to match the negative rule.
20. **Normalizer input?** Fact-shaped projected material, not proven constitutional Facts.
21. **Applicability/admission?** Only lexical/equality/nonexpiry filters; no constitutional applicability/admission act.
22. **Derived Observations properly classified?** As Python objects yes; constitutional Observation testimony standing is mixed/Unknown and not established.
23. **Misleading new Evidence identity?** It can: fresh id packages dependent derivation without independent-support examination.
24. **Repeated collection independent corroboration?** It can appear so to ID-counting consumers; it does not constitutionally become corroboration.
25. **Events preserve?** Serialized artifact assertions, workspace, actor/time/order, and weak implementation linkage—not truth, lawful production, or establishment.
26. **Replay reconstructs?** Retained Observation/Evidence/Fact artifacts and projection indexes under current rules.
27. **Replay cannot reconstruct?** Bytes, skipped material, historical rules/invocation, requirements, authority, competency, Fidelity, admission, establishment warrant, or current standing.
28. **Explicit Typed Unknowns?** None on this road.
29. **Absence/failure/compression Unknowns?** Reachability/authorization/envelope failures, malformed samples, semantics, subject identity, time, translation loss, conflicts, prior Fact standing, Evidence applicability, support sufficiency, and producer occurrence.
30. **First missing/compressed movement?** Establishing a bounded observation requirement and applicable, selected, authorized observer competency before acquisition.

The lawful stopping point is the observer-to-Fact boundary just recovered: no conclusion is drawn about downstream confidence or action.
