# Unknown Structure Grammar Recovery Topology Audit 001

## 1. Bounded question

What existing artifacts, responsibilities, and roads allow Seed to project structural questions over an attributed unknown representation, preserve competing candidate grammars, test them against evidence, and recover a verified translation capability?

This audit is read-only and implementation-backed. It does not implement grammar recovery, parser synthesis, probe types, translator validation, capability promotion, or observer refactoring.

## 2. Governing orientation

Operator testimony under test:

```text
unknown external representation
→ attributed sample preservation
→ structural projection
→ candidate external grammar
→ discriminating probe
→ revised candidate grammar
→ candidate translator or parser realization
→ translation validation
→ Seed-native observation
→ capability evidence
→ sufficient understanding or another probe
```

Existing provider-specific observers are treated as reverse evidence and possible scaffolding/reference implementations, not as proof that canonical Seed must permanently contain one observer per external substrate.

## 3. Constitutional guardrail

Seed may ask structural questions over unfamiliar material: repetition, variation, co-occurrence, stable fields, temporal-looking values, categorical-looking values, changed/disappeared elements under controlled probes, explanatory candidates, contradictions, and remaining Unknowns.

Seed must not impose internal semantics on an external representation without evidence. Structural regularity is not semantic truth.

## 4. Composition-depth rule

This audit descends only to the highest stable boundary sufficient for the bounded inquiry. It does not inspect Git object storage, packfiles, compression, transport internals, parser internals, runtime internals, or machine internals unless repository evidence makes them independently meaningful for recovering the observed structure contract.

## 5. Methodology

Executed focused read-only searches requested by the audit prompt, then inspected implementation bodies and consumers in the relevant neighborhoods. Search matches were not treated as classifications by themselves. Existing tests were inspected as repository testimony where they stated boundaries.

No providers, observers, event-ledger commands, tool execution commands, or mutation-oriented runtime surfaces were executed. The only repository mutation is this Markdown audit artifact.

## 6. Inspected neighborhoods

Primary implementation neighborhoods inspected:

- `seed_runtime/structure_observation.py`
- `seed_runtime/knowledge/repository_observation.py`
- `seed_runtime/repository_observation.py`
- `seed_runtime/observations.py`
- `seed_runtime/observation_sources.py`
- `seed_runtime/inquiry_artifacts.py`
- `seed_runtime/inquiry_orientation.py`
- `seed_runtime/candidate_requests.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/capability_promotion_readiness.py`
- `seed_runtime/tool_validation.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_runtime/evidence.py`
- `seed_runtime/state.py`
- `seed_builder/generator.py`
- `seed_builder/validator.py`
- `seed_builder/registration.py`
- focused tests for observation sources, repository observation, candidate requests, capability verification, toolkit generation, toolkit registration, inquiry orientation, and observation agreement.

## 7. Terminology

Preserved distinctions for this audit:

- raw representation != attributed sample
- structural regularity != candidate grammar
- candidate grammar != verified grammar
- grammar != semantics
- candidate translator != verified translator
- successful translation != truth
- translation capability != current realization
- tool construction != tool registration != capability verification
- sufficiency for one inquiry != universal grammar mastery

## 8. Unknown-representation intake topology

### Existing evidence

`Observation` is the canonical external observation and can carry source type, observed time, subject, predicate, value, confidence, metadata, dimensions, and expiry. `ObservationIngestor` preserves each observation as an `observation.observed` event and also converts it to provenance `Evidence` with the observation payload copied into evidence. `Evidence` can carry arbitrary payload dictionaries with observed time, source, kind, and confidence.

Prometheus intake decodes provider JSON samples into `PrometheusDecodedSample` and then maps them into provider-local `PrometheusObservationShape` before canonical `Observation` emission. That is not opaque intake; it is provider-shaped decoding before observation.

Inquiry notes preserve raw operator prose in an isolated JSONL probe store with source and time, but this is for operator inquiry prose, not arbitrary external representations or grammar recovery samples.

Repository observation preserves a normalized repository-state contract derived from Git commands. It does not preserve the raw command result payloads as attributed samples.

### Current capability against required fields

| Required preservation | Current state |
| --- | --- |
| raw bytes or text | Partial: `Evidence.payload` and `Observation.value/metadata` could carry text-like payloads, and inquiry notes preserve raw prose. No explicit opaque external sample artifact exists. |
| parsed generic data | Partial: arbitrary `dict` payloads and Prometheus JSON-derived data exist, but parsed generic data is not modeled as unknown grammar material. |
| source attribution | Present in `Observation.source_type`, `Evidence.source`, provider metadata, and inquiry-note source. |
| collection time | Present in `Observation.observed_at`, `Evidence.observed_at`, inquiry-note `recorded_at`, and Prometheus metadata. |
| endpoint or path | Partial: provider metadata/repository fields carry endpoint/path, but there is no general unknown-sample endpoint/path field. |
| operation used | Partial: Prometheus query metadata and Git provider commands are implicit/implementation-local; no general unknown-sample operation field. |
| sample boundaries | Partial: Prometheus samples are individual decoded samples; inquiry notes are JSONL records. No general sample boundary artifact. |
| negative or failed samples | Partial: repository unavailable observations preserve reasons; Python artifact adapter emits parse-failed module fact. No general failed unknown sample model. |
| correlation across repeated samples | Partial: ledger correlation IDs and provider metadata exist, but no grammar-recovery sample series/correlation owner. |
| explicit grammar unknown | Absent as an unknown external grammar attribute. `unknown` appears in diagnostics/inquiry visibility, but not as a grammar state for preserved samples. |

### Producer, artifact, consumer

Current producers include provider observers, repository observers, and inquiry-note recording. Current artifacts include canonical `Observation`, `Evidence`, `RepositoryObservation`, `InquiryNoteRecord`, and provider-local decoded records. Current consumers include `ObservationIngestor`, state projection, inquiry orientation, repository-state renderers, and provider-specific normalizers. No current producer/artifact/consumer trio owns opaque unknown external sample preservation for grammar recovery.

## 9. Structural-projection topology

### Existing evidence

`StructureObservationBoundary` explicitly owns read-only structural extraction and evidence preservation while denying content interpretation, substrate parsing, grammar ownership, responsibility recovery, lexicon ownership, event-ledger writes, repository mutation, and cluster mutation.

The Python repository artifact adapter is a concrete substrate adapter under that parent owner. It observes caller-provided Python source text, uses Python parsing, emits module/class/function/method/import artifact facts, preserves parse failure as a module/file fact, and explicitly denies content interpretation, responsibility recovery, lexicon ownership, ledger writes, and mutations.

Prometheus provider-local decoding recognizes provider envelope/vector sample shape, metric labels, timestamp/value position, and emits provider-local observation shapes. This is structural and semantic provider mapping combined in a known substrate, not a general unknown-structure projector.

Repository observation projects Git command outputs into counts/status fields; it is a known repository-state observer, not generic structural comparison.

### Required structural questions

| Structural support | Current state |
| --- | --- |
| shape/type/nesting | Partial for known substrates. Python AST and Prometheus decoded samples inspect known shapes. No generic unknown-shape artifact. |
| repetition/ordering/cardinality | Partial in provider code and tests, but no generic comparison over multiple samples. |
| stable versus variable fields | Absent as a general implementation-backed responsibility. |
| relationships | Partial for Python artifacts and Seed state relationships, not unknown external structure. |
| line/source position | Mostly absent from inspected structure observation; Python AST source positions are not preserved in emitted artifact facts. |
| comparison across samples | Absent for unknown grammar recovery; comparison surfaces exist elsewhere but not structural sample comparison. |
| typed Unknowns | Partial vocabulary exists in diagnostics and candidate-request Unknown handling; absent as typed unknown grammar/sample fields. |

`StructureObservationBoundary` is a reusable parent boundary, but its implementation evidence says it does not own substrate parsing or grammar. Adjacent adapters currently work only for known substrates.

## 10. Candidate-grammar topology

### Existing evidence

Seed has several candidate-preservation surfaces:

- `candidate_requests` preserves language-derived candidate requests and routes without command/capability/execution promotion.
- `capability_candidates` preserves capability candidates derived from observed package evidence, with supporting evidence and explicit non-promotion notes.
- capability verification and promotion-readiness surfaces preserve candidate evidence separately from verification, selection, permission, and execution.
- observation agreement tests assert candidate agreement remains separate from grammar and architectural truth.

### Gap

No inspected artifact is a grammar candidate. Capability candidates are scoped to package/capability evidence, not external grammar hypotheses. Candidate requests are scoped to operator language routing, not structural explanations. They demonstrate a reusable non-promotion pattern but not a reusable grammar-candidate owner.

Current candidate artifacts can preserve identity, confidence, rationale, supporting evidence, target boundary, and ambiguity in their own domains. They do not preserve grammar scope, candidate grammar statements, contradicting sample testimony, unresolved grammar alternatives, or revision history for external grammar recovery.

## 11. Probe-formation topology

### Existing evidence

Inquiry orientation records notes in an isolated probe store and composes related material by deterministic lexical overlap. Candidate request routing preserves routes without execution. Tool validation distinguishes selected operation names from capability recommendation. Execution requires registered tools, validation, and policy.

### Gap

No bounded responsibility was found that transforms competing grammar candidates into an unresolved distinction, then into a discriminating evidence need, then into a bounded probe. Existing `Decision`, candidate route, inquiry note, and execution-plan surfaces should not be assumed as owners of this road. Seed can preserve some operator-provided probe-like notes, but cannot form a discriminating structural probe without selecting/executing a tool as a distinct artifact.

## 12. Testimony/comparison topology

### Existing evidence

Capability candidates preserve supporting evidence. Verification-evidence and verification-inspection surfaces distinguish observed candidate evidence, acquired evidence, existing `capability_verified` facts, and verification status. Promotion-readiness can state supportability without promotion. Observation agreement preserves candidate agreement and explicitly does not own grammar.

### Gap

There is no grammar-testimony owner that can say: sample X supports candidate grammar A, sample Y contradicts candidate grammar B, probe Z was non-discriminating, or field F remains Unknown. Support counts are not grammar truth, and no warrant boundary for grammar truth was found.

## 13. Translator-recovery topology

### Existing evidence

`seed_builder` can generate untrusted toolkit candidates from `ToolNeed`, write a manifest, operation stub, tests, docs, and generation notes. `ToolkitValidator` validates candidate manifests, schemas, implementation references, forbidden imports, and candidate tests. `ToolkitRegistrationService` registers only validated candidates and emits `tool.registered` events. `ToolRegistry` loads manifests and registers operation specs; `ToolExecutor` executes only registered tools after validation and policy checks.

Prometheus and repository observers are hand-coded provider realizations. Prometheus has provider-local decoded sample and observation shape layers. Repository observation has a hand-coded Git command-to-contract mapping.

### Gap

No road exists from a supported grammar candidate to a translation specification, generated parser, deterministic transform, provider adapter, or executable translator. Builder generation is from `ToolNeed`, not from grammar candidates or translation specs, and the generated operation is a stub requiring review. Tool registration accepts validated toolkit artifacts, but registration does not prove translation correctness or capability.

## 14. Translation-validation topology

### Existing evidence

Tool validation can check registered operation existence/status and input/output schema. Toolkit validation can check manifests, schemas, implementation references, forbidden imports, and run candidate tests. Prometheus and repository observer tests provide fixture-like expected outputs for known provider mappings. Observation ingestion preserves provenance when translating canonical observations into evidence/facts.

### Current state by validation dimension

| Validation dimension | Current state |
| --- | --- |
| parser executes | Partial through candidate tests/tool execution, not grammar-specific. |
| output shape is valid | Present for registered tool schemas and toolkit schemas. |
| translation is deterministic | Not generally represented; deterministic code paths exist but no translator determinism evidence artifact. |
| known fixtures are preserved | Present in observer tests for known providers; absent as recovered-translator validation owner. |
| new samples are explained | Absent. |
| provenance survives | Present for `Observation` to `Evidence`; partial for provider metadata. |
| Unknowns survive | Absent for grammar translation outputs. |
| authority limits survive | Present in many boundaries; absent as translator-validation criterion. |
| translated observations are useful | Partial through observations/facts and capability evidence, but not translator-specific. |

## 15. Capability-projection topology

### Existing evidence

Capability-candidate, verification-evidence, capability-verification, and promotion-readiness surfaces strongly preserve the separation between candidate evidence, verification evidence, verification facts, capability selection, execution authority, and tool invocation. A successful translator validation could conceptually become evidence, but no current artifact admits translator-validation evidence as capability evidence for a bounded translation capability.

### Gap

No current road prevents `JSON parser installed` or `one successful sample parsed` from being incorrectly treated as universal capability proof because no road exists at all from recovered translator validation into bounded capability projection. Existing capability evidence machinery is reusable as a boundary pattern, not as a grammar-recovery implementation.

## 16. Sufficiency/stopping topology

### Existing evidence

Inquiry artifact visibility recognizes supported and unsupported conclusions as document-visible, not runtime-modeled artifacts. Capability verification inspection can state unverified/stale/verified based on existing facts. Promotion-readiness can state supported/unsupported for future promotion without promoting.

### Gap

No implementation-backed grammar sufficiency artifact was found that can say: this grammar/translator is sufficient for this bounded inquiry but incomplete generally. Lawful stopping is present as a recurring boundary style in read-only inspections, but not as a grammar-recovery stop condition.

## 17. Retention/specialization topology

### Existing evidence

Toolkit candidate generation writes candidate artifacts to a candidate store. Toolkit registration can retain validated toolkit operations in registry/state/ledger. ToolRegistry can list and require registered operations. Generated candidates can be validated before registration.

### Gap

No lifecycle owner was found for recovered translators as retained/cached/replaced/compiled/delegated/discarded realizations. Current candidate storage and toolkit registration could accept artifacts after validation, but they do not encode translator recovery, replacement, specialization, or discard semantics.

## 18. Prometheus reverse reconstruction

| Recovery stage | Existing implementation evidence | Existing owner | Missing road or artifact |
| --- | --- | --- | --- |
| attributed samples | Prometheus provider decodes provider JSON samples; metadata includes source name, query, labels, sample/source times, and Seed collection time. | `PrometheusObservationSource` / provider-local code | No opaque attributed Prometheus payload sample artifact before decoding. |
| structural distinctions | Provider-local `PrometheusDecodedSample` recognizes `metric`, `instance`, timestamp, and value; observation-shape mapper distinguishes known query names. | `seed_runtime/observation_sources.py` | No generic structural projector that could recover vector/envelope distinctions from samples. |
| candidate grammar | Absent. Current code directly maps known Prometheus shapes. | None | Grammar hypothesis artifact absent. |
| discriminating probe | Absent for grammar recovery. Query set is provider implementation, not candidate-discriminating probe formation. | None | Evidence-need/probe artifact absent. |
| comparison testimony | Provider tests can assert expected mappings; no sample-support/contradiction testimony. | Tests / provider code | Grammar testimony owner absent. |
| translator candidate | Hand-coded `_prometheus_observation_shapes` is an implemented provider translator, not a recovered candidate. | Prometheus provider | Road from grammar candidate to translator spec/code absent. |
| validation evidence | Existing tests validate selected mappings and decoded samples; schemas/provenance via Observation. | Tests / Observation pipeline | Translator-validation evidence artifact absent. |
| capability projection | Capability machinery can represent candidates/verification in other domains. | Capability candidate/verification modules | No bounded Prometheus-payload-translation capability projection road. |
| sufficient stopping | Not represented for recovered Prometheus grammar. | None | Bounded sufficiency stop absent. |

## 19. Git reverse reconstruction

| Recovery stage | Existing implementation evidence | Existing owner | Missing road or artifact |
| --- | --- | --- | --- |
| attributed samples | Git provider runs `rev-parse`, `branch`, `remote`, and `status --porcelain=v1` internally; unavailable reasons are preserved. | `GitRepositoryObservationProvider` | Raw command results are not preserved as attributed samples. |
| structural distinctions | Status lines are interpreted by fixed positions and `??`; counts are produced. | `GitRepositoryObservationProvider` | No generic recovery of line grammar from repeated command samples. |
| candidate grammar | Absent. Status grammar is hand-coded. | None | Candidate grammar artifact absent. |
| discriminating probe | Absent. No road asks for a repository-state perturbation to distinguish grammar hypotheses. | None | Probe/evidence-need artifact absent. |
| comparison testimony | Tests can validate repository observation results; no support/contradiction record for candidate grammars. | Tests | Grammar testimony owner absent. |
| translator candidate | Hand-coded Git command-to-`RepositoryObservation` mapping. | `GitRepositoryObservationProvider` | Translation spec/candidate realization road absent. |
| validation evidence | Repository observation tests and status fields validate known mapping. | Tests / provider | Recovered-translator validation artifact absent. |
| capability projection | Git client can appear as a capability candidate from package evidence, separate from repository-state translation. | Capability candidate modules | No bounded repository-state translation capability projection. |
| sufficient stopping | Not represented for recovered Git grammar. | None | Bounded sufficiency stop absent. |

## 20. Python structure reverse reconstruction

| Recovery stage | Existing implementation evidence | Existing owner | Missing road or artifact |
| --- | --- | --- | --- |
| attributed samples | Adapter consumes caller-provided `source_path` and text. | `RepositoryArtifactObservationAdapter` | Text is input, but no opaque sample record with collection/provenance series. |
| structural distinctions | AST parse emits module/class/function/async function/method/import facts; parse failure emits module fact only. | Repository Artifact Observation Adapter under Structure Observation | General unknown grammar structural projection absent. |
| candidate grammar | Absent; Python AST grammar is prebuilt in Python parser. | None | Candidate grammar artifact absent. |
| discriminating probe | Absent. | None | Probe formation from structural ambiguity absent. |
| comparison testimony | Self-model tests use emitted artifact facts; observation agreement preserves candidate agreement separate from grammar. | Tests / observation-agreement code | Grammar support/contradiction testimony absent. |
| translator candidate | Adapter is a deterministic known-substrate extractor, not recovered translator. | Repository Artifact Observation Adapter | Road from grammar candidate to extractor spec/code absent. |
| validation evidence | Tests validate artifact facts and parse-failure behavior. | Tests | Recovered-translator validation artifact absent. |
| capability projection | Not directly connected to capability verification. | None | No structure-translation capability evidence road. |
| sufficient stopping | Adapter stops at structural artifact extraction and avoids ownership/lexicon inference. | Adapter boundary | No grammar sufficiency artifact. |

## 21. Reusable owners

- `StructureObservationBoundary`: reusable parent boundary for read-only structural extraction with non-interpretation and no grammar ownership.
- `RepositoryArtifactObservationAdapter`: reusable example of substrate adapter over caller-provided text, parse failure handling, and structural extraction without responsibility/lexicon inference.
- `Observation` / `ObservationIngestor` / `Evidence`: reusable provenance and observation-to-evidence preservation road, though not currently opaque-sample-specific.
- `candidate_requests`: reusable non-promotion and ambiguity-preservation pattern.
- `capability_candidates`, `verification_evidence`, `capability_verification`, `capability_promotion_readiness`: reusable candidate/evidence/verification boundary pattern.
- `seed_builder` generator/validator/registration: reusable candidate-realization lifecycle pattern, but currently not grammar-specific.
- `ToolRegistry`, `ToolValidationService`, `ToolExecutor`: reusable registered-operation validation/execution boundaries.

## 22. Scaffolding classification

| Observer/surface | Classification | Can provide |
| --- | --- | --- |
| Prometheus provider observer | reference implementation; bootstrap capability; fixture; optimized realization for known Prometheus mapping; insufficient evidence as canonical grammar-recovery owner | Training fixtures, expected translation outputs, validation testimony, reverse-engineering examples, fallback realization. |
| Git repository observer | reference implementation; bootstrap capability; compatibility surface; fixture; insufficient evidence as canonical grammar-recovery owner | Expected repository-state contract, validation testimony, reverse-engineering example, fallback realization. |
| Python repository artifact adapter | canonical owner for known Python repository artifact structural extraction under Structure Observation; reference implementation; fixture; not canonical unknown-grammar owner | Structural extraction boundary example, parse-failure testimony, validation fixtures. |
| Structure Observation boundary | canonical parent boundary for substrate-independent structural observation; scaffolding for unknown grammar only because it denies substrate parsing and grammar ownership | Boundary vocabulary and non-interpretation guardrail. |
| Candidate request/route inspection | scaffolding/reference pattern for candidate preservation and ambiguity, not grammar candidates | Candidate/non-promotion pattern. |
| Capability candidate/verification surfaces | canonical owners for capability candidate/verification inspection; scaffolding/reference pattern for grammar candidate verification | Evidence/verification separation pattern. |
| Toolkit generator/validator/registration | canonical owners for toolkit candidate generation, validation, and registration; scaffolding for translator realization | Candidate artifact lifecycle, validation-before-registration pattern. |

“Scaffolding” here does not mean disposable. It means the implementation can inform or support future recovery work but is not itself evidence that the recovery responsibility is implemented.

## 23. Existing roads

- Known provider payload/sample → provider-local decoded shape → provider-local observation shape → canonical `Observation` → `Evidence`/Fact.
- Caller-provided Python source text → AST-backed repository artifact facts, with parse failure retained as limited evidence.
- Operator prose → candidate request(s) and route(s), preserving ambiguity without command/capability/execution promotion.
- Observed package facts → capability candidates → verification evidence → verification inspection/promotion-readiness inspection.
- ToolNeed → untrusted toolkit candidate files → validation report → registration if valid → registered operation → validation/policy-gated execution.
- Canonical observation → evidence event and optional fact event with provenance.

## 24. Missing roads

- Opaque external representation → attributed unknown sample artifact.
- Attributed unknown samples → generic structural projection/comparison.
- Structural regularities → candidate grammar hypotheses.
- Competing grammar candidates → unresolved distinction → bounded evidence need.
- Evidence need → discriminating probe artifact without selecting/executing a tool.
- Probe result → support/contradiction/inconclusive testimony tied to candidate grammar distinction.
- Supported grammar candidate → translation specification.
- Translation specification → generated parser/deterministic transform/provider adapter candidate.
- Translator candidate → grammar-aware validation evidence.
- Translator validation evidence → bounded translation capability candidate/verification support.
- Bounded inquiry support → lawful stop without claiming universal grammar mastery.
- Recovered realization → retained/cached/replaced/compiled/delegated/discarded lifecycle.

## 25. Missing owners

- Opaque unknown external sample owner.
- Generic structural sample comparison owner.
- Candidate external grammar owner.
- Grammar testimony/support/contradiction owner.
- Discriminating probe/evidence-need owner for structural ambiguity.
- Translation specification owner separate from executable parser code.
- Recovered translator validation owner.
- Grammar-recovery sufficiency/stopping owner.
- Recovered translator retention/specialization lifecycle owner.

## 26. Dominant gap

The dominant gap is candidate grammar preservation. Intake and structural projection are partial/scaffolded for known substrates, and downstream tool/capability validation patterns exist, but no artifact preserves competing grammar hypotheses with support, contradiction, scope, provenance, unresolved alternatives, and revision history. Without that owner, discriminating probes, translator realization, validation, capability projection, and stopping have no typed handoff.

## 27. Strongest counterevidence

- Structure Observation explicitly denies owning substrate parsing and grammar, which argues that current structure observation only works through known substrate adapters.
- Prometheus translation is hand-coded around known query names and sample fields; it does not preserve unknown payloads before mapping.
- Git repository observation directly runs and interprets Git commands; raw command outputs are not preserved as first-class attributed samples.
- Python structure observation relies on Python AST parsing and emits known artifact facts; it does not generalize automatically to unknown grammars.
- Capability candidates are explicitly capability candidates, not capabilities or grammar candidates.
- Toolkit generation starts from `ToolNeed`, not grammar evidence; generated operations are untrusted stubs and must validate before registration.
- Execution requires registered tools, validation, and policy, preserving bootstrap safety and arguing against arbitrary recovered parser execution.
- Inquiry artifact visibility states supported/unsupported conclusions are document-visible, not implementation-modeled runtime inquiry conclusions.
- No evidence shows lawful stopping can currently be separated from complete grammar recovery for grammar-recovery inquiries, because no grammar-recovery sufficiency owner exists.

## 28. Preserved Unknowns

- Whether Seed should use existing `Observation`/`Evidence` or a separate artifact for opaque sample preservation is Unknown.
- Whether grammar candidates should reuse any existing candidate surface or require a new artifact is Unknown.
- Whether recovered translators should enter `seed_builder`, a provider-adapter path, or another realization path is Unknown.
- Whether discriminating probes should be modeled near inquiry, observation request, operation request, or execution planning is Unknown.
- Whether provider-specific observers are long-term canonical owners, fallback realizations, or bootstrap examples for every substrate is Unknown.
- Whether raw payload preservation would require new secrecy/redaction boundaries is Unknown from inspected evidence.

## 29. Supported conclusions

1. Seed does not currently implement an end-to-end unknown-structure grammar recovery loop.
2. Seed has strong boundary patterns for non-promotion, evidence preservation, capability candidate verification, and validation-before-registration.
3. Seed can inspect known structures through substrate-specific observers/adapters.
4. Seed lacks an implementation-backed grammar-candidate artifact and road.
5. Seed lacks a discriminating structural probe formation artifact.
6. Seed lacks a road from supported grammar candidates to translation specifications or recovered translator realizations.
7. Existing provider observers can serve as reverse-engineering examples and validation fixtures without becoming canonical architecture.
8. The smallest next bounded implementation slice is not parser synthesis; it is preserving candidate grammar hypotheses and testimony boundaries, because downstream roads require that typed handoff.

## 30. Unsupported conclusions

- Unsupported: Seed can recover arbitrary external grammars today.
- Unsupported: Prometheus/Git/Python observers prove generic grammar recovery exists.
- Unsupported: Installing or observing a parser proves a bounded translation capability.
- Unsupported: One successful sample translation proves grammar truth.
- Unsupported: Capability candidates can be reused as grammar candidates without new evidence.
- Unsupported: Tool registration proves translator correctness.
- Unsupported: Structure Observation owns grammar recovery.
- Unsupported: Provider-specific observers should be removed or renamed.

## 31. Primary classification

C. Seed can inspect known structures, but candidate grammar recovery is a genuinely missing responsibility.

## 32. Dominant-gap classification

3. Candidate grammar preservation.

## 33. Exact next bounded boundary

Responsibility boundary: candidate external grammar preservation and testimony boundary.

Producer: a future read-only structural projection/comparison surface over already attributed samples.

Artifact or handoff: candidate grammar hypothesis records that preserve candidate identity, scope, provenance, supporting testimony, contradicting testimony, unresolved alternatives, confidence/warrant status, and explicit Unknowns without verification or semantic promotion.

Consumer: future discriminating evidence-need/probe formation and translator-specification validation surfaces.

Exact bounded question: can Seed preserve competing structural explanations for an attributed unknown representation, including support, contradiction, unresolved alternatives, and Unknowns, without claiming grammar truth or semantics?

Explicit exclusions: no opaque sample type, no parser synthesis, no translator generation, no tool registration, no capability promotion, no event-ledger mutation, no LLM recovery loop, no provider refactor, no canonical `Observation` change.

## 34. Implementation-warrant decision

One bounded implementation slice is warranted.

## 35. Files changed

- Added `unknown_structure_grammar_recovery_topology_audit_001.md`.

## 36. Probes/tests executed

Read-only searches executed:

```bash
rg -n "StructureObservation|structure observation|grammar|candidate|hypothesis|testimony|comparison|probe" seed_runtime scripts tests
```

```bash
rg -n "sufficiency|warrant|admission|reliance|Unknown|conflict|support" seed_runtime scripts tests
```

```bash
rg -n "ToolNeed|ToolSpec|register|implementation|verification|promotion|execution" seed_runtime scripts tests
```

```bash
rg -n "PrometheusDecodedSample|PrometheusObservationShape|RepositoryObservation|RepositoryArtifactFact" seed_runtime tests
```

Implementation inspections used `sed -n` on the relevant files listed in section 6 and `find seed_builder -maxdepth 2 -type f` to enumerate and inspect builder files. No runtime providers, observers, event-ledger commands, or mutating tests were executed.

Diff guardrail commands executed before commit:

```bash
git diff --stat
git diff --numstat
git status --short
```

## 37. Confidence statement

Confidence is moderate-high for the topology classification because the inspected implementation bodies consistently show known-substrate observers/adapters, strong non-promotion patterns, and validation/registration boundaries, while no grammar-candidate owner or grammar-recovery handoff appears in the requested neighborhoods or focused tests. Confidence is not absolute because the repository is large and this audit intentionally avoided reopening complete Eye, capability, and observation-translation audits.

## Required questions answered

1. Can Seed currently preserve an opaque external representation without first understanding its grammar? Partial/mostly no: generic payload containers exist, but no explicit opaque unknown external sample artifact.
2. Can it explicitly represent that the grammar is unknown? No, not as grammar state on samples/candidates.
3. Can it compare multiple attributed samples structurally? No for unknown grammar recovery.
4. Can it distinguish stable and variable structure? No as a generic structural comparison responsibility.
5. Can it preserve candidate structural interpretations? Partially in other domains as candidate/non-promotion patterns, not for structural interpretations.
6. Can it preserve competing candidate grammars? No.
7. Can it attach supporting and contradicting testimony to a grammar candidate? No.
8. Can it derive a bounded evidence need from an unresolved structural distinction? No.
9. Can it form a discriminating probe without selecting or executing a tool? No implementation-backed grammar probe artifact found.
10. Can it correlate probe results back to the candidate distinction? No.
11. Can it represent that a probe was inconclusive? No for grammar probes.
12. Can it distinguish decoding from semantic translation? Partially in provider code and boundaries, but not as a general recovery model.
13. Can it represent a translation mapping independently from executable parser code? No generic translation-spec artifact found.
14. Can it construct or register a candidate translator realization? It can construct/register toolkit candidates generally after validation, but not translator realizations from grammar candidates.
15. Can that realization be tested without becoming automatically trusted? Yes for toolkit candidates generally; not translator-specific.
16. Can translator success become capability evidence? Not currently as a bounded translation capability road.
17. Can translator failure weaken or revise a candidate grammar? No.
18. Can Seed preserve raw samples after translation for future reinterpretation? Partial through evidence payload/provenance if stored, but no explicit raw-sample retention boundary.
19. Can it state that a grammar is sufficient for one inquiry but incomplete generally? No implementation-backed grammar sufficiency artifact found.
20. Can it lawfully stop once the current inquiry is supported? Not for grammar recovery; lawful-stop patterns exist elsewhere.
21. Which current artifacts are reusable? Structure Observation boundary, Python adapter pattern, Observation/Evidence, candidate request routes, capability candidate/verification/promotion-readiness, builder validation/registration, registry/validation/execution.
22. Which current artifacts are scaffolding only? Prometheus and Git observers as reverse examples for grammar recovery; candidate request/capability candidate surfaces as patterns only; builder as realization lifecycle pattern only.
23. Which responsibilities are genuinely missing? Opaque sample owner, structural comparison owner, grammar candidate owner, grammar testimony owner, discriminating probe owner, translation spec owner, recovered translator validation owner, grammar sufficiency owner, retention/specialization owner.
24. Which roads are missing between mature owners? Evidence/sample to Structure Observation, Structure Observation to candidate grammar, candidate grammar to evidence need/probe, probe result to testimony, grammar candidate to translation spec, translation validation to capability projection, bounded support to lawful stop.
25. Is the largest gap intake, structural projection, candidate grammar, probe formation, translator realization, validation, capability projection, or stopping? Candidate grammar preservation.
26. What is the smallest next bounded implementation slice? Candidate external grammar preservation and testimony boundary, with explicit exclusions listed in section 33.
