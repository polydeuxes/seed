# Prometheus `sysname` to `os` semantic-competency recovery 001

## 1. Scope and negative authority

This is one bounded, Book-first, report-only constitutional recovery on the current merged implementation after PR 1975. Its sole external witness is one accepted Prometheus instant-vector item returned for the configured query `node_uname_info`. PR 1975, earlier Prometheus reports, implementation names, tests, comments, catalogs, and familiar operator vocabulary are locator testimony or evidence of their own bounded kind; none is constitutional authority by identity.

The governing comparison is:

```text
external grammar
↕ bounded Fidelity
constitutional grammar
```

This report does not establish that `node_uname_info` describes a node; that `instance` identifies a subject, endpoint, process, or host; that `nodename` names a host; that `sysname` means operating system; that `Linux` is an OS-family value; that co-presence creates a relation; or that `os`, `prometheus_instance`, or `alias` is the right constitutional predicate. It does not recommend implementation or deletion and does not continue into general observer architecture, Fact implementation, the Evidence Graph, confidence, goals, horizons, Questions, Answers, execution, or presentation.

Occurrence is classified independently below. Runtime code may execute and tests may witness execution even where semantic standing is **Unknown**. Exactly one report is changed; no production behavior or canonical Book clause is changed.

## 2. Active Book clauses

The following clauses govern this recovery.

* **01.External.A–D:** provider vocabulary remains attributed external grammar. A bounded translation must state source, scope, external context, translated claim, uncertainty, and authority limit. Addressability is not assimilation. Cross-seam use must preserve provenance, limits, Unknowns, and refusal conditions. A Fidelity finding requires an actual bounded comparison of constitutional expectation and implementation witness; an artifact or copy is not such a finding.
* **Lenses, Views, and Constitutional Roads:** constructibility, adjacency, repeated co-occurrence, and mechanical compatibility do not establish a constitutional road. Availability, applicability, admission, and consumption are separate. A lawful Observation view carries source-attributed testimony, not automatic Fact or current standing.
* **Acts and Act Artifacts:** invocation, successful return, result construction, external effect, assertion truth, and a responsible act occurrence are distinct. A class or artifact does not prove the act its name suggests.
* **03.Movement.A:** mutation or a changed runtime value is not constitutional movement unless subject, warrant, authority, evidence, scope, and limits travel with the transition.
* **Testimony and Established Fact:** claim expression, interpretation, normalization, support, and establishment differ. A `Fact` object is fact-shaped implementation vocabulary; constitutional Fact standing must not exceed producing evidence, source authority, or the production boundary. Testimony is not established fact, and carried `observed_at` is not an independent establishment time.
* **05.Evidence.A–F:** an evidence identifier or row does not prove truth, independence, currentness, or universal admission. Co-occurrence does not prove a semantic relation. Attribution is not responsibility. Missing provenance remains a bounded Unknown rather than a global negative.
* **05.Recording.A–D:** recording preserves an attributed assertion within a horizon; it does not produce the external occurrence, semantic competency, truth, or renewed standing. Retrieval and projection cannot recreate dimensions never preserved.

These clauses require the dimensions used at every crossing here: subject; assertion; standing; source/provenance; responsible producer; authority/warrant; scope/locality; occurrence/preservation; conflict; known loss; Typed Unknown; and lawful stopping point.

## 3. Raw external witness

The smallest available testimony is represented without adopting its vocabulary:

```text
configured query token: node_uname_info
accepted envelope: status="success", data.resultType="vector"
one data.result item:
  metric:
    instance: "192.0.2.115:9100"
    nodename: "example_host"
    sysname: "Linux"
  value: [T, "1"]
```

The strongest pre-semantic claim is only:

> At the preserved provider/configuration boundary, Prometheus returned one accepted vector item containing the query-context token `node_uname_info`, provider tokens `instance`, `nodename`, and `sysname` with the shown values, and a two-position sample value containing `T` and `"1"`.

Its subject is **this returned item occurrence**, not a host. Its assertion is about returned syntax. Its standing is **structurally decoded, source-relative testimony**. Its source is the configured Prometheus HTTP response as represented by current code/test testimony. The acquiring adapter is the implementation producer; external semantic responsibility and authority are **Unknown**. Scope is one item, one response, one query invocation. Successful receipt/acceptance is runtime-possible and compatibility-tested; preservation of the original bytes, complete response, request authority, and invocation identity is absent. Conflicting responses are not reconciled. The lawful stop is before field-role, subject, predicate, relation, currentness, or truth interpretation.

## 4. Central finding

The repository contains a **compiled realization** that structurally accepts Prometheus vector JSON, decodes a sample, then applies a **frozen semantic bundle**: `instance` becomes the assertion subject, `sysname` (or fallback `system`) becomes predicate `os`, its text becomes stripped lowercase `linux`, provider sample time becomes `observed_at`, confidence becomes `0.95`, expiry is absent, and endpoint-shaped OS material is marked against Fact promotion. Separately, co-present `nodename` and `instance` metadata are translated by `EndpointAliasNormalizer` into `example_host prometheus_instance 192.0.2.115:9100`.

Code and focused tests evidence executable behavior and compatibility. They do not preserve constitutive provider-contract evidence, predicate or relation meanings, candidate comparison, a bounded Fidelity finding, semantic competency identity/version/scope, conditions of use/refusal, or authority for applying that competency to this occurrence. Thus the implementation ability is **evidenced and compatibility-tested**, but constitutional semantic competency standing is **absent/Unknown**. `sysname="Linux"` does not presently warrant constitutional `os=linux`.

The smallest source-relative semantic claim candidate is: **“For this occurrence, the provider record returned the token/value `sysname="Linux"` in the series-label dictionary associated with query token `node_uname_info`.”** It needs only structural recognition plus attribution, not a claim that `sysname` means uname system name. The first missing semantic movement is a bounded, evidenced comparison establishing the role and meaning of `sysname` in the applicable provider metric contract (including scope, authority, version, alternatives, loss, Unknowns, and refusal conditions). Predicate `os` remains a later, independent competency crossing.

## 5. Structural decoding topology

```text
HTTP bytes
→ JSON object
→ status == "success"
→ data object
→ resultType == "vector"
→ result list
→ item object
→ metric object + value list(len >= 2)
→ nonempty string metric.instance
→ value[0] convertible to UTC datetime
→ PrometheusDecodedSample(
     metric copy,
     instance,
     converted timestamp,
     raw timestamp,
     arbitrary value[1])
```

Provider-record recognition is classified as follows.

| Candidate recognition | Current standing | Evidence and limit |
|---|---|---|
| “this is a Prometheus vector result” | **structurally decoded; compatibility-tested; frozen realization** | `_query` requires exact envelope fields and tests exercise them. This recognizes configured Prometheus-shaped syntax; it does not semantically establish what a vector represents. |
| “this item belongs to `node_uname_info`” | **mixed: structurally associated and frozen assumption** | The adapter itself sent that query then passes its loop variable into translation. No returned `__name__` label is required and response/query correspondence beyond this call path is not independently evidenced. |
| “metric is a label dictionary” | **structurally decoded; compatibility-tested; semantic role Unknown** | A Python dictionary is required and copied. Calling its members metric labels is provider vocabulary preserved in metadata, not constitutional label semantics. |
| “value is a sample tuple” | **structurally decoded; compatibility-tested; semantic role partially evidenced/Unknown** | A list of length at least two is required; positions zero and one are assigned timestamp/value roles. Extra members are ignored. No preserved provider contract establishes tuple semantics. |

Structural decoding establishes accepted shape, copied tokens, a nonempty string at `metric.instance`, timestamp convertibility, and preservation of `value[1]`. It does **not** establish metric meaning, field roles, represented subject, sample-value meaning, source authority, currentness, truth, independence, `os`, any identity/relation, or lawful semantic competency invocation.

## 6. Hidden semantic stack

The apparently short `sysname → os` step hides independent competencies:

| Layer | Current classification | Hidden decision |
|---|---|---|
| Envelope/sample grammar | **compiled realization; compatibility-tested** | Which response/item forms count as acceptable. |
| Metric-contract recognition | **frozen assumption** | Query context is treated as the item’s `node_uname_info` contract. |
| Label-role interpretation | **frozen assumption** | `instance`, `nodename`, and `sysname/system` receive special roles. |
| Subject formation | **frozen assumption** | `instance` is assertion subject; `nodename` later becomes relation subject. |
| Predicate competency | **frozen assumption** | `sysname/system` warrants `os`. |
| Value grammar | **compressed** | strip/lowercase accepts every nonempty string; `Linux` becomes `linux` without preserving a typed value meaning. |
| Temporal convention | **mixed** | convertible `value[0]` becomes provider-authoritative sample time and Observation time; freshness/currentness is not established. |
| Authority convention | **frozen assumption** | constructor default supplies `source_type=provider`; metadata calls Prometheus time authoritative. |
| Confidence convention | **frozen assumption** | every emitted Prometheus Observation receives `0.95`. |
| Relation competency | **frozen assumption** | nodename plus instance becomes source-specific `_instance` predicate. |
| Compatibility/refusal | **evidenced frozen realization** | endpoint-shaped uname OS is suppressed from Fact promotion. |
| Fidelity examination | **absent** | No preserved comparison warrants any semantic crossing. |

The stack is not one translation: it contains a structural decoder, semantic translator, implicit ontology, predicate competency, relation competency, authority/temporal/confidence conventions, compatibility rules, and frozen realizations.

## 7. Semantic competency establishment history

The required establishment history and current recovery are:

| Establishment movement | What would establish it | Current standing/occurrence |
|---|---|---|
| External tokens/structures encountered | Attributed raw examples and provider/configuration boundary | One bounded witness is **evidenced** in tests/report; production original-byte preservation is **absent**. |
| Candidate grammar | Multiple accepted/refused forms, contract/version evidence, alternatives and limits | Executable grammar is **compiled realization**; constitutive evidence is **absent**. |
| Candidate field roles | Provider HELP/TYPE/docs or authoritative probe evidence tied to version and context | Roles are **semantic candidates frozen into code**; standing **Unknown**. |
| Candidate subjects | Explicit model of series, target, exporter, endpoint, environment, and name with discriminating evidence | Alternatives are **absent** from the adapter; endpoint subject is a **frozen assumption**. |
| Candidate predicates/relations | Defined constitutional meanings, allowed subjects/value grammar, authority and conflict rules | `os`/`prometheus_instance` are executable vocabulary; semantic competency is **absent/Unknown**. |
| Evidence/probes/recurrence/comparison | Provider-contract evidence, HELP/TYPE, repeated and contrasting samples, cross-source probes, negative cases | Tests provide **compatibility evidence** only; semantic corpus is **absent**. |
| Fidelity examination | Bounded comparison preserving subject, expectation, witness, loss, invention, authority, conflict, Unknown, stop | **Absent**. |
| Bounded semantic competency standing | Identified/versioned competency with scope, warrant, applicability and refusal conditions | **Absent**. |
| Optional compiled realization | Code implementing the established grammar with traceable competency/version | Executable code is **evidenced**, but linkage to establishment is **absent**. |

The adapter could be a cached realization of competency learned elsewhere; compiled form is not inherently invalid. The repository simply cannot recover that history, so it cannot distinguish learned grammar from developer-baked grammar.

## 8. Competency invocation history

Invocation is independent of establishment:

| Invocation movement | Required standing | Current witness |
|---|---|---|
| Bounded observation requirement | Why this occurrence/material is needed | **absent** on this road. |
| Applicable competency | Match between requirement, provider/version, query and established scope | **absent**; configured class availability substitutes. |
| Selection | Responsible choice among applicable competencies | **compressed/absent**; fixed `SAFE_QUERIES` loop selects the token. |
| Authority | Authority to contact this source and rely on bounded output | URL/configuration and GET occur; constitutional authority is **Unknown**. |
| Acquisition | Request/receipt under declared boundary | Runtime implementation exists and tests fake successful receipt: **compatibility-tested occurrence**, real witness occurrence only as stipulated. |
| Decoding | Apply identified structural grammar/version | Decoder executes; identity/version and refusal testimony are **absent**. |
| Established-semantics application | Apply only established roles/predicates within scope | Code executes frozen rules; constitutional occurrence is **Unknown** because standing is absent. |
| Source-relative testimony | Preserve source, claim strength, scope, time, authority limits, loss and Unknowns | Metadata preserves many tokens but assertion shape strengthens them; standing is **partial/mixed**. |

Evidence that the rules might have been learned does not explain why they were selected here; configuration and successful execution do not establish the rules’ semantics.

## 9. Token-role matrix

| Token | Current assigned role and translation | Supporting evidence | Alternative roles | Authority/scope | Translation loss |
|---|---|---|---|---|---|
| `instance` | Mandatory nonempty string; `PrometheusDecodedSample.instance`; subject of `os`; copied to metadata; lexically tested as endpoint | Code and tests: **structurally decoded, compatibility-tested, frozen realization** | series discriminator, scrape target label, exporter endpoint, arbitrary relabelled value, provider instance, unresolved token | Provider-relative one item; semantic authority **Unknown** | Label-name provenance remains in metadata, but subject selection strengthens it; relabeling/config origin, scheme and target role absent. |
| `nodename` | Optional trimmed metadata; treated as `stable_name` by `EndpointAliasNormalizer`; relation subject | Code comment and behavior tests only: **compatibility-tested frozen assumption** | uname field, container/namespace name, exporter environment name, provider-reported token, arbitrary relabelled text | One record; authority and stability **Unknown** | “label reported” becomes subject/name-like identity; exact whitespace is erased; field origin/version absent. |
| `sysname` | Preferred over fallback `system`; stripped/lowercased; becomes value of `os` | Code/tests prove behavior: **compatibility-tested frozen assumption** | uname field, kernel identifier, provider taxonomy, arbitrary relabelled text, opaque token | One record/sample; source authority **Unknown** | Original case/whitespace and distinction from fallback `system` are compressed in assertion, though original labels remain metadata; meaning is strengthened. |
| sample timestamp `T` | Must convert; UTC datetime becomes shape and Observation `observed_at`; metadata calls it Prometheus sample time/authority | Conversion tests: **structurally decoded, compatibility-tested** | evaluation timestamp, scrape timestamp, explicit series timestamp, server-assigned time | One sample; “current instant” is configured intent, not currentness warrant | Raw value is preserved in metadata, but clock origin, skew, scrape/evaluation relation and freshness are absent. |
| sample value `"1"` | Preserved in decoded sample but ignored for uname shape | Decode tests: **structurally decoded**; semantic meaning **Unknown** | information-metric presence marker, gauge value, truth flag, count, arbitrary numeric sample | One sample; no semantic authority | Completely erased from emitted OS assertion except original response is not preserved; its role in validating the labels is silently assumed/ignored. |

## 10. Subject-candidate matrix

| Candidate subject | Current relative standing | Evidence needed to distinguish it | Remaining Unknown |
|---|---|---|---|
| Prometheus series S | **semantic candidate; strongest minimally interpretable subject** | Series identity rules, complete label set/query/time boundary, response provenance | Whether query/labels uniquely identify S; series identity/version. |
| Scrape target | **semantic candidate** | Prometheus target/relabel configuration and provider contract tying `instance` to target | Whether `instance` is overwritten or denotes target address. |
| Exporter process | **semantic candidate** | Scrape configuration plus process identity/probe evidence | Whether endpoint terminates at exporter, proxy, or another component. |
| Network endpoint X | **partially evidenced candidate / frozen subject** | Address grammar and configuration showing X is an endpoint in this scope | Protocol, namespace, routing, endpoint ownership, and semantic applicability. |
| Environment observed by exporter | **semantic candidate** | Exporter metric contract and deployment/namespace evidence | Host vs container vs VM vs kernel namespace. |
| Provider-reported nodename Y | **structurally present candidate** | Contract for `nodename`, naming scope, identity and comparison evidence | What it names and whether it is stable/unique. |
| Unresolved external subject | **evidenced lawful stop** | Retain record/series attribution until discriminating evidence arrives | All real-world correspondence remains typed Unknown. |

No candidate is selected constitutionally. The current implementation selects endpoint-shaped `instance`; that is executable behavior, not subject-standing evidence.

## 11. Assertion-candidate matrix

| Candidate | Subject / claim strength / modality | Required evidence and competency | Authority, scope, time, conflict and Unknowns | Standing |
|---|---|---|---|---|
| **A.** Prometheus returned `sysname="Linux"` on series S | Returned record/series; lexical, source-relative report | Structural grammar, response/query association, bounded series addressability | Provider/config boundary; one item at T; conflicting items coexist; real-world meaning Unknown | **evidenced at record level; series identity partially evidenced** |
| **B.** Provider reported `uname.sysname="Linux"` for environment represented by S | Represented environment; interprets field role but retains provider modality | Versioned metric contract establishing metric and field role; evidence identifying represented environment; Fidelity finding | Provider authority only; metric/version/deployment scope; sample-time semantics; conflicts retained; environment correspondence Unknown | **semantic candidate; not earned** |
| **C.** Scrape target reported system-name Linux | Scrape target; stronger subject and reporter attribution | Target/relabel/exporter identity, field-role and reporter competencies | Target/config scope and T; conflicts with target discovery/other samples; process/environment Unknown | **frozen-adjacent candidate; not earned** |
| **D.** Environment behind endpoint X has uname sysname Linux | Environment; direct property claim, loses report modality | Endpoint-role/attachment evidence, uname contract, environment boundary, temporal and authority warrant | Endpoint/deployment at T; conflicts require source/time treatment; namespace/currentness Unknown | **semantic candidate; not earned** |
| **E.** Host Y uses operating-system family Linux | Host; strongest normalized constitutional claim | Host identity, `nodename↔host`, `instance↔environment`, `sysname↔OS-family`, `Linux` value grammar, `os` predicate competency, corroboration/Fidelity and establishment authority | Host/config/version/time scope; defined conflict policy; distribution/kernel/family/currentness Unknown | **foreign to raw syntax and absent** |

These are alternatives, not a mandatory progression. Selection requires claim-specific evidence, an applicable established competency, responsible selection and authority, Fidelity findings at every changed subject/meaning, and preservation of conflict/Unknowns.

## 12. Predicate-competency analysis

Current code and broader repository usage show that the token `os` exists and is treated as host-classifying vocabulary in some consumers. The required files do not provide a constitutive definition answering all of the following:

| Predicate dimension | Required standing | Current recovery |
|---|---|---|
| Meaning | A bounded proposition such as uname sysname, kernel family, OS family, distribution family, or installed OS | **Unknown; compressed across usages**. |
| Eligible subjects | Defined subject kinds and correspondence rules | State code often treats `os` as host-related, while Prometheus emits it on endpoint text; **mixed/contradictory**. |
| Value grammar | Canonical domains, equivalence and preservation rules | Any nonempty `sysname/system` string is lowercase; special set has no different behavior; **frozen normalization**. |
| `Linux` denotation | Kernel identity vs uname token vs OS/distribution family | **Unknown**. Lowercasing proves only string transformation. |
| Source warrant | Which provider contracts, probes, operator claims, or corroboration can support it | **absent** for Prometheus sysname. |
| Temporal standing | Observation/effective/current interval and expiry | T is copied; no expiry; currentness **Unknown**. |
| Authority strength | Source report vs established property | `source_type=provider` and `0.95` are conventions, not examined authority. |
| Conflict | Incompatible values by subject/source/time/semantic layer | No semantic-layer conflict rule is preserved at translation. |
| Weaker predicate | `prometheus_label_sysname`, `provider_reported_uname_sysname`, or an attributed record claim could preserve less interpretation | Candidates only; no constitutional predicate is established here. |

Therefore `sysname="Linux"` does **not** currently warrant constitutional `os=linux`. Required competency is an identified, evidenced, scoped and Fidelity-examined `os` predicate competency defining eligible subjects, value grammar, source authority, temporal/conflict behavior, translation loss, Unknowns, and refusal conditions, plus an independently established `sysname` role/value correspondence. It is not recoverably established. Catalog membership or code recurrence is compatibility vocabulary, not meaning, applicability, or assertion warrant.

## 13. Relation-candidate analysis

The direct structural finding is only: **X and Y appeared as values of `instance` and `nodename` on the same returned record occurrence.** Co-presence warrants that bounded association, not identity or attachment.

| Relation candidate | Required distinguishing evidence | Current standing |
|---|---|---|
| Y names X | Naming contract and proof X is the named subject | **not warranted; frozen implication**. |
| Y is the host behind X | Host/endpoint topology, exporter placement and identity evidence | **absent**. |
| X is a scrape endpoint for Y | Target/relabel configuration plus Y subject semantics | **semantic candidate; absent**. |
| Y has Prometheus instance X | Defined `prometheus_instance` relation and provider/config warrant | Emitted by normalizer; **compiled realization/frozen vocabulary**, not earned relation competency. |
| Y aliases X | Both sides must be same identity under an alias grammar | This record alone does not establish it; **not warranted**. |
| X and Y merely co-occurred | Same item and labels | **evidenced** within one occurrence. |
| Relation Unknown | Preserve co-occurrence while refusing stronger meaning | **strongest lawful semantic standing**. |

`EndpointIdentityNormalizer` does not derive `alias` from this sample alone. It needs a separate identity-valued `ip_address`, `alias`, or `ansible_host` whose value matches the lexical endpoint base. Even then, code/test evidence proves the derivation rule, not constitutional alias semantics. `prometheus_instance` is frozen provider-specific vocabulary synthesized from `source_name`, not an earned predicate in this examined corpus.

## 14. Frozen semantic bundle inventory

| Baked answer | Symbol(s) | Correct classification | Occurrence / limit |
|---|---|---|---|
| Fixed metric availability and query meaning | `PrometheusObservationSource.SAFE_QUERIES`, `collect` | compatibility rule + frozen realization | Runtime-active when invoked; allowlisting does not establish metric semantics. |
| Prometheus response/vector grammar | `_query` | structural decoder + compatibility rule | Executed and tested; provider-version contract unpreserved. |
| Item grammar and mandatory `instance` | `_prometheus_decoded_sample`, `PrometheusDecodedSample` | structural decoder + frozen realization | Executed/tested; rejected item details are not preserved. |
| `node_uname_info` branch has OS meaning | `_prometheus_observation_shapes` | semantic translator + implicit ontology + frozen assumption | Executed/tested; semantic warrant absent. |
| `instance` is subject | `_prometheus_observation_shapes` | subject-formation ontology + frozen assumption | Endpoint-shaped X is selected; alternatives erased. |
| `sysname`/`system` has OS role | `_prometheus_os_from_uname` | predicate competency substitute + frozen assumption | Preferred/fallback lookup, strip/lowercase; origin distinction compressed. |
| `Linux→linux` is canonical value | `_prometheus_os_from_uname` | value-normalization convention + frozen realization | Tested; denotation Unknown. |
| sample value is irrelevant | uname branch | metric-contract assumption | Decoded then erased; meaning Unknown. |
| sample timestamp is Observation time and Prometheus-authoritative | decoder, metadata, shape | temporal + authority convention | Raw and converted forms preserved; currentness/clock warrant absent. |
| confidence `0.95` | `_observation` | confidence convention | Always assigned; warrant absent. |
| no expiry | `Observation` construction | temporal convention by omission | `expires_at=None`; does not establish timelessness/currentness. |
| endpoint scope | `instance` subject plus `is_endpoint_subject` | lexical ontology + frozen assumption | Used to suppress; endpoint semantics not established. |
| nodename is stable host identity | comment and `EndpointAliasNormalizer` | ontology/relation competency substitute + frozen assumption | Comment says authoritative/stable; no constitutive evidence. |
| relation is `<source>_instance` | `EndpointAliasNormalizer` | relation translator + frozen vocabulary | For source `prometheus`, produces `prometheus_instance`. |
| conditional identity relation is `alias` | `EndpointIdentityNormalizer` | relation competency + compatibility rule | Not produced by raw witness alone; semantics still unestablished. |
| OS Fact eligibility is refused only for endpoint-shaped Prometheus uname | shape metadata, `_should_suppress_fact_promotion` | negative compatibility rule + frozen realization | Tested; suppresses Fact artifact, not a general semantic adjudication. |
| Predicate catalog normalization | `PredicateNormalizer` | mapping executor / compiled realization | No additional mapping for this already-`os` row; catalog presence never supplies warrant. |

## 15. Compiled realization versus recoverable competency

`PrometheusObservationSource`, its dataclasses/helpers, and its normalizers are a coherent executable candidate for a cached or compiled semantic realization. Compilation can lawfully follow competency establishment; it need not repeat all evidence during every invocation. The constitutional problem is recoverability, not the mere existence of code.

| Constitutive dimension | Preserved? |
|---|---|
| Competency identity and version | **absent** beyond implementation symbol names. |
| Constitutive/provider-contract evidence | **absent**. |
| Predicate and relation meanings | **absent/fragmentary vocabulary use**. |
| Bounded Fidelity findings | **absent**. |
| Scope/applicability | **compressed** into fixed branches and lexical checks. |
| Authority/warrant | **absent**; metadata conventions substitute. |
| Conflicts and alternatives | **absent**. |
| Typed Unknowns | **mostly erased/silently resolved**. |
| Conditions of use | **partly compiled** as accept/reject checks. |
| Conditions of refusal | Malformed samples and missing sysname are refused, and endpoint OS Fact promotion is suppressed; semantic refusal reasons/evidence are **absent**. |

Thus **compiled semantic realization exists != constitutive competency standing is recoverable**. Tests prove the compiled behavior, not that it was lawfully learned.

## 16. Semantic evidence inventory

| Potential source | Found evidence | Classification and semantic force |
|---|---|---|
| Provider documentation references | No reference/version adjacent to the adapter or focused tests | **absent**; no provider-contract warrant. |
| HELP/TYPE metadata | Not queried or preserved | **absent**. |
| Tests | Exact vector shapes, decode acceptance/refusal, lowercase OS output, metadata, suppression, and relation output | **compatibility evidence**; establishes current behavior, not external semantics. |
| Comments/docstrings | “authoritative for stable host identity”; provider-local interpretation wording | **external/developer testimony**, internally contradictory with endpoint subject; insufficient as constitutive evidence. |
| Configuration | base URL, optional name/type, timeout, fixed query list | **authority/configuration evidence only in a weak operational sense**; no semantic applicability or access warrant. |
| Operator testimony | None preserved for this witness | **absent**. |
| Recurrence across samples | Tests contain examples, but no evaluated recurrence corpus or independence | **behavioral recurrence/compatibility**, semantically insufficient. |
| Comparison with other sources | Local source also emits `os`; consumers use `os` | **vocabulary recurrence**, not shared meaning or correspondence evidence. |
| Probe results | No provider-semantic or subject-identity probe preserved | **absent**. |
| Historical reports/PRs | Earlier reports locate symbols and concerns | **historical locator testimony** only. |
| Predicate definitions | Catalog and consumers recognize tokens/cardinality/mappings | **compatibility/ontology fragments**; no sufficient `os` definition or applicability warrant. |
| Normalizer mappings | Code derives `prometheus_instance`; PredicateNormalizer maps catalog entries | **compiled behavior**, not semantic evidence. |

No examined evidence source establishes the needed provider metric contract or the `os`/relation competencies.

## 17. Typed Unknown matrix

| Typed Unknown: exact subject | Responsible producer / consumer locality | Evidence and resolution condition | Current treatment |
|---|---|---|---|
| What subject `instance` represents | Metric producer/configurator; shape translator | Relabel/target contract and deployment evidence | **silently resolved** to Observation subject; alternative erased. |
| Role of `nodename` | Metric producer/exporter; alias normalizer | Versioned metric-field contract and naming scope | **silently resolved** as stable name; original token retained in metadata. |
| Role of `sysname` | Metric producer/exporter; OS translator | Contract/HELP/docs/probe tied to version | **silently resolved** as OS input. |
| Meaning of `node_uname_info` | Metric producer; query branch | Metric contract, HELP/TYPE, version | **silently resolved** by branch name. |
| Relation X↔Y | Producer/configurator; alias normalizer | Target/relabel/deployment/naming evidence | **silently resolved** to `prometheus_instance`; co-occurrence is all evidenced. |
| Correspondence `sysname↔os` | Predicate competency producer; translator/consumers | Defined predicate plus bounded Fidelity examination | **erased/silently resolved**. |
| Scope/denotation of `Linux` | Metric and predicate competency producers | Value grammar and system/environment evidence | **compressed** to lowercase. |
| Authority of labels | Provider/configuration authority owner; testimony consumer | Provenance and authority grant | **absent**, disguised by `source_type=provider`. |
| Currentness | Metric/time producer; current-state consumer | Timestamp semantics, clock/freshness/expiry policy | **silently non-expiring**, currentness still Unknown. |
| Confidence warrant | Adapter/semantic competency producer; ranking consumers | Calibrated rule and evidence | **silently resolved** to `0.95`. |
| Meaning of sample value `"1"` | Metric producer; shape translator | Metric contract/HELP and negative samples | **erased** after decode. |
| Independence from other samples | Collection/provider; evidence consumer | Acquisition IDs, scrape/evaluation provenance, recurrence design | **absent**. |
| Translation loss | Semantic translator/Fidelity examiner; testimony consumer | Preserved mapping/version/loss finding | **partly visible** via raw labels, otherwise absent. |

These are consumer-local semantic Unknowns, not a demand for one persistent artifact per row.

## 18. Capability matrix

| Candidate competency/capability | Implementation ability | Constitutional Capability standing | Availability → applicability → selection → authority → execution → verified result |
|---|---|---|---|
| Prometheus structure decoding | **evidenced/compatibility-tested** | **Unknown/absent** as versioned competency | available and executed in tests; applicability/authority absent; structural result verified in scope. |
| Metric-contract interpretation | Branch exists | **absent** | available as code; applicability/selection/authority and verified semantics absent. |
| Label-role interpretation | Special lookups exist | **absent** | executed; no standing or semantic verification. |
| Subject formation | `instance` selection exists | **absent** | mechanically selected/executed; no authority or candidate comparison. |
| Predicate interpretation | `os` selection/lowercase exists | **absent** | mechanically executed; verified output shape only. |
| Relation interpretation | source-specific `_instance` and conditional alias rules exist | **absent** | normalizer availability/execution tested; semantics unverified. |
| Temporal interpretation | Timestamp conversion/metadata exists | **partial structural ability** | conversion verified; time authority/currentness applicability absent. |
| Source-relative testimony production | Observation/Evidence metadata exists | **partially evidenced/mixed** | executes and records attribution, but assertion shape strengthens meaning and omits limits. |
| Fidelity examination | No responsible comparison found | **absent** | unavailable; therefore no selection/execution/result. |

## 19. Gap matrix

A Gap is stated only where the current consumer actually requires missing standing.

| Current consumer requirement | Present standing | Consumer-local incompatibility/consequence | Gap |
|---|---|---|---|
| `_prometheus_observation_shapes` must choose subject/predicate/value to emit an `Observation` | Structurally decoded tokens only | Code emits `instance os linux` without recoverable semantic competency | **Gap: label-role, subject, predicate/value competency and Fidelity standing**. |
| `EndpointAliasNormalizer` must form a relation | Co-present X/Y plus provider source token | Code emits `prometheus_instance` without relation competency | **Gap: relation meaning/applicability/warrant**. |
| Metadata asserts source-time authority and Observation carries T/no expiry | Convertible timestamp only | Consumers can read authoritative/nonexpiring shape without time-semantic warrant | **Gap: bounded temporal competency**. |
| Source-relative testimony consumer must distinguish reported syntax from normalized property | Metadata retains labels but SPV assertion says `os=linux` | Claim strength is ambiguous/strengthened | **Gap: bounded source-relative modality and Fidelity limits**. |

No Gap is asserted merely because there is hardcoded code. Structure decoding itself is locally satisfied for the accepted witness. Fact establishment and later consumers are outside this report’s stopping boundary.

## 20. Demand matrix

Demand requires an applicable requirement, present standing, warranted comparison, incompatibility, and consumer-local consequence. No current path preserves that complete derivation.

| Candidate demand | Required derivation status | Finding |
|---|---|---|
| Establish metric-contract competency | Requirement and missing standing are visible, but no responsible warranted comparison/selection is preserved | **Demand absent/Unknown**; only Gap is recoverable. |
| Establish `os` predicate competency | Translator requires it, but no examined applicability/comparison authority exists | **Demand absent/Unknown**. |
| Establish subject/relation competency | Normalizers consume candidate tokens, but no warranted candidate comparison exists | **Demand absent/Unknown**. |
| Establish temporal/Fidelity competency | Assertion shape needs limits, but no demand-producing act is preserved | **Demand absent/Unknown**. |

Hardcoded semantics are evidence of implementation need and incompatibility pressure, not evidence that constitutional Demand occurred.

## 21. Fidelity crossing matrix

| Crossing | Preserved | Erased / invented / strengthened | Scope, authority, source, time, conflict, Unknown | Fidelity finding |
|---|---|---|---|---|
| Raw JSON → accepted Prometheus result | Accepted envelope fields and result list in process | Original bytes/headers/extras may be erased; “Prometheus result” source role relies on configured route | Scope narrows to accepted response; authority and conflicts Unknown | **structural compatibility-tested; semantic Fidelity Unknown**. |
| Accepted result → decoded sample | Metric dict, instance, raw+UTC timestamp, value[1] | Container/extras and rejection coordinates erased; positional roles invented semantically | One item; source retained indirectly; time converted; conflicts absent | **mixed structural preservation; no bounded finding**. |
| Decoded sample → field-role candidates | Raw metric retained in metadata; instance/time named | Candidates collapse to assigned roles; sample value erased for uname | Item→assertion scope; authority labels added; Unknowns erased | **unexamined/Unknown**. |
| Field-role candidates → subject candidates | X retained | `instance` strengthened to sole assertion subject; endpoint scope inferred lexically | Series/environment alternatives erased; authority unchanged in code but apparent claim authority rises | **unfaithful or mixed candidate; no produced finding**. |
| `sysname` token → predicate candidates | Original labels plus selected text | `os` invented; uname/kernel/opaque alternatives erased | Source-relative token becomes constitutional-looking predicate; meaning/conflict Unknown | **unexamined strengthening**. |
| `Linux` token → value candidates | Original case in metadata; lowercase in value | Canonical equivalence and semantic layer implied; whitespace/case erased | Provider token becomes normalized-looking value; scope/authority strengthened | **lossy mixed crossing, Fidelity Unknown**. |
| Co-present labels → relation candidates | X/Y and derivation source id(s) retained | `stable_name` and `prometheus_instance` invented; mere co-occurrence strengthened | Record-local association becomes subject relation; authority borrowed from provider metadata; conflict not examined | **unexamined strengthening**. |
| Candidate assertion → source-relative testimony | Provider/query/base URL/labels/times retained in metadata | SPV surface lacks explicit “reported token” modality; 0.95 and no expiry invented/conventional | Source partly preserved; assertion authority/currentness can be overread; Unknowns not first-class | **mixed/compressed**. |
| Testimony → Fact-establishment eligibility | Exact OS metadata and evidence record retained | Endpoint OS is negatively suppressed; relation is otherwise mechanically eligible | No positive admission/support/conflict/Fidelity examination; time copied | **OS ineligible by compatibility rule; constitutional Fact eligibility Unknown**. |

No row has a stored bounded Fidelity finding. The matrix itself is this report’s bounded examination finding, not runtime certification and not authority to translate.

## 22. Object-bias and vocabulary-bias audit

| Vocabulary/object | Bias refused | Recoverable classification |
|---|---|---|
| `PrometheusObservationSource` | Class name proves observer/competency/source authority | Implementation owner compressing request, decode, translation and construction: **compiled realization**. |
| `PrometheusDecodedSample` | Dataclass field names prove provider semantics | Structurally useful representation with semantically loaded names. |
| `PrometheusObservationShape` | “Observation” proves constitutional observation standing | Provider-local translated shape; source-relative standing partial. |
| `node_uname_info` | English/metric name proves node/uname/information meaning | External query token plus frozen branch. |
| `instance`, `nodename`, `sysname` | Familiar names define roles | Provider tokens; roles **Unknown** until established. |
| `endpoint`, `host`, `node`, `stable_name` | Implementation/operator vocabulary resolves subject kind | Semantic candidates or frozen ontology, not authority. |
| `os` | Predicate exists/catalog recurrence proves meaning/applicability | Frozen vocabulary and unestablished predicate competency. |
| `prometheus_instance` | Source-specific spelling proves relation | Synthesized compatibility vocabulary; unearned semantic relation. |
| `alias` | Normalizer output proves identity equivalence | Conditional compiled derivation; relation warrant independently required. |
| `confidence=0.95`, `authoritative`, `current_instant` | Labels prove calibrated authority/currentness | Conventions/tested fields; warrants **Unknown**. |
| `Observation`, `Evidence`, `Fact` | Programming artifact implies constitutional standing | Implementation grammar; standing needs independent responsible movement. |

## 23. Strongest contradictions

1. The comment says only `node_uname_info` is “authoritative for stable host identity,” yet the direct OS assertion remains on `instance`, and the only Y→X result is a separately synthesized `prometheus_instance` relation. Authority, stability, and host identity are asserted lexically but not evidenced.
2. The adapter labels its temporal intent `current_instant` and assigns no expiry, while the only structural basis is a convertible provider timestamp of Unknown clock/freshness semantics. Preserved occurrence time and current applicability conflict conceptually.
3. `sysname` is treated as `os`, while no definition distinguishes uname system name, kernel identity, OS family, or distribution family. Predicate specificity is stronger than preserved semantic evidence.
4. The raw sample value is structurally required and decoded, then ignored for uname. If `"1"` gates whether label information is asserted, its semantic contribution is erased; if it does not, that irrelevance is also unproven.
5. Endpoint-shaped `os` is deemed unsafe for Fact promotion, but the same occurrence’s stronger-looking Y→X `prometheus_instance` relation remains mechanically promotable. Negative compatibility is predicate-specific, not a general semantic warrant.
6. Original labels preserve some external grammar, while the primary SPV assertion silently presents normalized constitutional-looking vocabulary. Attribution survives, but claim modality and translation loss are compressed.

## 24. Strongest Unknowns

* Which metric contract/version produced the record and what `node_uname_info`, its labels, and sample value mean.
* What real or external subject, if any, is represented by the series and by `instance`.
* Whether `nodename` names an environment, host, namespace, exporter context, or only reports opaque text.
* Whether `sysname` is uname `sysname`, who observed it, and the boundary of that observation.
* Whether `Linux` denotes a returned token, kernel, uname value, OS family, distribution family, or another taxonomy.
* What `os` constitutionally means, which subjects may bear it, and what source/time/conflict authority it implies.
* Whether any semantic relation beyond co-occurrence holds between X and Y.
* Why this competency was applicable/selected/authorized for this occurrence.
* What warrants Prometheus’s asserted time authority, confidence `0.95`, and no expiry.
* Whether the compiled realization derives from previously earned competency or developer-baked grammar.
* What translation loss, alternatives, conflicts, and refusal conditions were known when the rules were compiled.

## 25. Smallest next honest semantic crossing

The lawful path stops here:

```text
one accepted returned item
→ structurally preserved provider tokens and positions
→ bounded source-relative claim candidate:
   “for this occurrence, the provider record returned
    sysname=Linux in the label dictionary associated with
    configured query token node_uname_info”
→ STOP
```

The first exact missing semantic movement is **not** `Linux→linux` and not `sysname→os`. It is establishment of the applicable metric-field-role competency: an identified responsible boundary must compare attributed, version/scoped provider-contract evidence and implementation witness to determine whether the token `sysname` denotes a provider-reported uname field, for which represented subject/environment, with what authority, time, alternatives, losses, conflicts, Unknowns, and refusal conditions. Only after that independent standing exists could a later predicate-competency examination ask whether the bounded provider report maps to any constitutional `os` claim.

## Direct answers

1. **Strongest claim before semantic interpretation:** Prometheus returned one accepted vector item containing the specified provider/configuration tokens, values, and two-position sample at this occurrence.
2. **What structural decoding establishes:** Accepted envelope/list/item shapes; a metric dictionary; a nonempty string under token `instance`; a convertible first sample position; preservation of the raw/converted timestamp and second position in `PrometheusDecodedSample`.
3. **What it does not establish:** Metric/label meaning, subject correspondence, reporter, truth, authority, currentness, sample-value meaning, identity/relation, `os`, value taxonomy, semantic competency, or Fact standing.
4. **Current meanings assigned to `node_uname_info`:** Allowlisted safe query; source of “authoritative stable host identity” metadata treatment; metric whose `sysname/system` yields OS; trigger for endpoint OS Fact suppression. These are frozen implementation meanings.
5. **Meanings assigned to tokens:** `instance` is mandatory sample coordinate, assertion subject and endpoint candidate; `nodename` is optional stable-name/relation subject; `sysname` is preferred OS input; timestamp is authoritative Observation time; `"1"` is decoded but ignored for uname.
6. **Evidence supporting each:** Current code and focused tests support exact assignment and compatibility behavior. They do not supply provider-semantic evidence. The timestamp’s numeric convertibility is structurally supported; semantic time authority is not.
7. **Only frozen meanings:** Metric meaning, label roles beyond structure, endpoint/host ontology, `sysname↔os`, `Linux↔linux` semantic equivalence, stable-name role, relation meaning, `0.95`, no expiry, and Fact eligibility convention.
8. **Candidate subjects:** Series, scrape target, exporter process, network endpoint, exporter-observed environment, provider-reported nodename, and unresolved external subject.
9. **Candidate assertions:** A–E in section 11, ranging from returned-token testimony to host OS-family property; they are alternatives, not compulsory stages.
10. **What warrants selection:** Claim-specific provider/config/deployment evidence; established applicable field-role/subject/predicate/relation competencies; responsible selection and authority; bounded Fidelity comparisons; conflict, temporal, loss and Unknown preservation.
11. **Does `sysname="Linux"` warrant `os=linux`?** No. The code performs that mapping, but constitutional warrant is not recoverable.
12. **Weaker supported assertion:** For this occurrence, the provider record returned token/value `sysname="Linux"` in the series-label dictionary associated with configured query token `node_uname_info`.
13. **Competency required for predicate `os`:** A scoped predicate competency defining meaning, eligible subjects, value grammar, source authority, temporal/conflict behavior, translation loss, Unknowns and refusal conditions, plus an established source-field correspondence.
14. **Is it established?** No; executable vocabulary and compatibility tests exist, but constitutive standing is absent/Unknown.
15. **Warranted `nodename`/`instance` relation:** Only co-occurrence on the same provider record occurrence. All stronger relations are candidates.
16. **Is `prometheus_instance` earned?** It is a compiled, compatibility-tested, frozen vocabulary synthesis; no earned semantic predicate standing was found.
17. **Is `alias` warranted?** Not by this record. The raw witness does not trigger `EndpointIdentityNormalizer`; even conditional execution would prove rule behavior, not semantic alias warrant.
18. **Silently resolved Unknowns:** Subject of `instance`; roles of metric/nodename/sysname/value; X↔Y relation; `sysname↔os`; `Linux` scope; provider/time/confidence authority; currentness; independence; and translation loss.
19. **Can the adapter distinguish learned from developer-baked grammar?** No. It may be compiled learned competency, but preserves no competency identity/version, constitutive evidence, Fidelity findings, or linkage.
20. **First exact missing semantic movement:** Bounded establishment and Fidelity examination of the applicable `node_uname_info.sysname` field role and represented subject/environment, before any `os` predicate crossing.
