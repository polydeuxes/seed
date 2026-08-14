# External Grammar Structural Recovery Characterization

## Evidence reviewed

This characterization reviews implementation-backed evidence only. Existing prose investigations were used as pointers to code paths, not as architectural authority.

Primary implementation evidence reviewed:

- `seed_runtime/inquiry_orientation.py`: preserves raw operator prose as an inquiry note, relates it to projected read models through deterministic lexical overlap, and refuses fact, intent, ownership, command, recommendation, or next-safe-move authority.
- `seed_runtime/local_packages.py`: parses dpkg status text into `PackageRecord` objects and then maps those normalized records into canonical package observations.
- `seed_runtime/observation_sources.py`: translates repository source relationships and Prometheus JSON/vector samples into Seed observation shapes and then canonical `Observation` objects.
- `seed_runtime/knowledge/relationship_observation.py`: parses Python source/AST and documentation navigation metadata into bounded `RelationshipFact` records while refusing behavior, reachability, capability, and ownership claims.
- `seed_runtime/knowledge/repository_observation.py`: extracts Python module/class/function/method/import artifacts from caller-provided source text and records explicit negative boundaries against content interpretation, responsibility recovery, event-ledger writes, repository mutation, and cluster mutation.
- Prior implementation-backed characterizations on provider translation, intermediate structural evidence, constitutional transitions, artifact deltas, representation boundaries, and competency interrogation were reviewed only where they pointed back to these implementation surfaces.

## Answer

The repository has already recovered a recurring distinction between external representation and recovered constitutional structure, but only in bounded implementation families.

The answer is not that Seed has a universal representation-independent grammar. It does not.

The answer is also not that current recovery work is merely interpreting English prose. It is broader than prose because dpkg status text, Prometheus provider JSON, Python source/AST structure, documentation navigation metadata, and operator prose all show implementation-local translation from representation into Seed-owned bounded structures.

The smallest truthful answer is:

```text
Current implementation repeatedly treats external representations as input material,
then emits bounded Seed-owned structures with explicit authority limits.

That pattern recurs across operator prose, provider-native data, and source structure.

It is constitutionally recurring as a discipline of boundary-preserving recovery,
not as a universal grammar engine.
```

## Representation review

| Family | External representation | Recovered constitutional structure | Representation-specific details that disappear | Recovered structures that recur when representations differ |
|---|---|---|---|---|
| Operator prose to inquiry orientation | Raw inquiry-note text supplied by an operator. | `InquiryNoteRecord`, `InquiryOrientationView`, related-material rows, uncertainty text, and authority boundary. | Prose does not become fact, goal, requirement, command, authorization, intent, ownership, recommendation, or next safe move. Only token overlap survives as related-material support. | Preserved evidence, bounded view, explicit negative authority, read-only/non-mutating posture. |
| dpkg status to package observations | dpkg status database records and fields such as `Package`, `Status`, `Version`, and `Architecture`. | `PackageRecord` objects, then canonical package observations such as `package_installed`, `package_version`, `package_architecture`, and `package_manager`. | dpkg record syntax, paragraph shape, malformed records, non-installed records, and raw field layout disappear. | Provider-local normalized record before canonical observation; provenance metadata; read-only/non-execution boundary. |
| Prometheus provider JSON to observations | Prometheus HTTP API JSON vector payloads, metric labels, sample timestamps, sample values, and safe query names. | `PrometheusDecodedSample`, `PrometheusObservationShape`, then canonical observations with Seed predicates such as `up`, `endpoint_role`, `os`, `filesystem_avail_bytes`, and `filesystem_size_bytes`. | Raw JSON envelope, Prometheus API response shape, sample-list positions, provider metric names as sole structure, and some endpoint identity ambiguity disappear or are demoted into metadata/suppression. | Decode first, provider-local interpreted shape second, canonical observation last; source time/provenance is retained without making provider syntax canonical. |
| Python source / AST to relationship facts | Python text parsed as AST nodes for imports, import-from statements, top-level definitions, classes, functions, and async functions. | `RelationshipFact` records such as `imports` and `defines`, later mapped by repository source observation into canonical observations. | AST node object identity, Python syntax trivia, indentation, comments, import statement formatting, and source-language mechanics disappear. | Caller-provided source text is structurally parsed into bounded evidence; negative boundaries prevent behavior, reachability, capability, and ownership promotion. |
| Documentation navigation metadata to relationship facts | Authored front-matter/navigation metadata supplied by caller: domain, defines, depends_on, related. | `RelationshipFact` records with stable document/domain/concept identities. | YAML/front-matter representation details and prose content disappear; relative references are normalized into document identities. | Explicit metadata becomes bounded relationship evidence without prose inference or documentation graph reconciliation. |
| Python source to repository artifacts | Caller-provided Python source text and AST. | `RepositoryArtifactFact` records for module/file, class, function, method, and import artifacts. | Source formatting, AST internals, statement ordering beyond top-level extraction, and executable semantics disappear. | Structural extraction, evidence preservation, read-only boundary, no content interpretation, no responsibility recovery, no event-ledger or cluster mutation. |
| Transition-family and artifact-delta characterization | Existing observations, pressure, inquiry notes, candidates, facts, diagnostics, and surface outputs. | Family-local transition descriptions: what artifact appears, what remains unchanged, what gains support, visibility, or authority. | Prose labels such as transition vocabulary do not themselves become architecture. | Repeated artifact-delta discipline: ask what changed, what did not change, and whether authority changed. |
| Competency interrogation methodology | Questions, failing/available commands, evidence surfaces, implementation behavior, tests, and stop conditions. | Earned competency boundaries: what can be answered, what evidence is sufficient, what must stop, and what remains unknown. | Methodological prose is not treated as capability proof; vocabulary does not become operational authority. | Implementation-backed interrogation over labels; negative authority boundaries and typed unknowns recur. |

## Translation review

### Operator prose -> inquiry orientation

This is a constitutional recovery pattern, but a weak one. The external representation is operator language. The recovered structure is not the meaning of that prose as architecture. The implementation preserves the note, tokenizes it, relates tokens to already projected material, renders uncertainty, and states the authority boundary.

This supports the distinction:

```text
operator prose
↓
preserved inquiry evidence plus bounded orientation
```

It does not support:

```text
operator prose
↓
operator intent, requirement, command, ownership, or architecture
```

### Provider-native language -> canonical observations

This is a stronger non-prose case. dpkg and Prometheus provider representations are not English-prose recovery. They show provider-local translation into Seed-owned records or shapes before canonical observation emission.

The recurring shape is:

```text
provider-native representation
↓
provider-local normalized/interpreted structure
↓
canonical Observation
```

This is not identical to inquiry orientation because provider translation can produce canonical observations and later facts, while inquiry orientation is read-only and non-promotional. The shared constitutional pattern is only the separation of external representation from recovered bounded structure.

### Source structure -> recovered artifacts

Repository source recovery is another non-prose case. Python source text is parsed as Python/AST, but the recovered structures are repository artifacts or relationship facts, not raw Python syntax and not architecture ownership.

The recurring shape is:

```text
source representation
↓
structural evidence record
↓
observation, artifact fact, or navigation/support surface
```

This is related to provider translation because both use representation-specific parsing to produce Seed-owned structural records. It differs because source recovery often stops at structural evidence or repository artifact facts and explicitly refuses behavior, reachability, capability authority, and ownership.

### Same constitutional pattern or unrelated families?

They are not one implementation family and should not be assigned a common owner.

They are, however, the same recurring constitutional discipline at a smaller level:

1. accept external representation as evidence-bearing material;
2. perform family-local parsing/translation;
3. emit a bounded Seed-owned structure;
4. preserve provenance or support;
5. explicitly prevent representation details from becoming constitutional authority.

That commonality is boundary discipline, not a universal grammar engine.

## Distinction analysis

### External grammar != recovered structure

Independently recurring and implementation-backed.

- Operator prose remains an inquiry note and lexical-overlap input; the recovered orientation view is not the prose itself.
- dpkg status text becomes normalized package records and package observations; raw dpkg wire format is not the canonical structure.
- Prometheus JSON becomes decoded samples, observation shapes, and observations; JSON/vector syntax is not canonical structure.
- Python syntax/AST becomes relationship facts and artifact facts; AST nodes are not the recovered constitutional participant.

### Representation != constitutional participant

Independently recurring and implementation-backed.

- A sentence does not become an operator intent, command, or architectural boundary.
- A Prometheus sample label does not automatically become stable host identity; the implementation suppresses some endpoint-subject promotions for `node_uname_info` OS observations.
- Python import syntax does not become dependency behavior, route behavior, capability authority, or runtime ownership.
- Documentation navigation metadata becomes relationship evidence, not documentation prose authority over repository truth.

### Language != architecture

Independently recurring, but mostly in language/operator/documentation families.

Natural-language inputs can be preserved and oriented, and documentation metadata can create relationship facts. But language content does not by itself become architecture, authority, or executable work. This distinction is well supported for operator prose and documentation prose, and indirectly supported by non-language provider/source families because they also require translation before admission.

### Vocabulary != boundary

Independently recurring and strongly supported.

The repository repeatedly refuses to promote presentation vocabulary into architecture. Inquiry orientation refuses intent/ownership/recommendation; relationship extraction refuses behavior/reachability/ownership; repository artifact extraction refuses responsibility recovery and lexicon ownership; transition characterizations ask what artifact changed rather than accepting transition labels as authority.

## Negative analysis

Separating representation from recovered structure prevents these implementation failures:

1. **Prose becoming architecture.** Inquiry orientation stores and displays operator prose but refuses to treat it as fact, claim, goal, requirement, command, authorization, ownership, intent, recommended action, or next safe move.
2. **Provider syntax becoming canonical structure.** dpkg status paragraphs do not flow downstream as dpkg paragraphs; they become `PackageRecord` and then canonical observations. Prometheus JSON vectors do not become canonical observations directly; samples are decoded and mapped to observation shapes first.
3. **Vocabulary becoming constitutional ownership.** Python import/definition vocabulary creates bounded relationship evidence only. It does not prove behavior, reachability, capability authority, or runtime ownership.
4. **Representation becoming authority.** Documentation navigation metadata can create relationship facts, but the helper does not inspect prose, infer concepts, or reconcile documentation graph authority. Repository artifact extraction similarly refuses interpretation, responsibility recovery, event-ledger writes, and mutation.
5. **Observation support becoming mutation.** Several reviewed boundaries preserve read-only metadata and negative mutation flags. Structural recovery can make evidence visible without mutating repository, cluster, event ledger, or operational authority.
6. **Transition labels becoming lifecycle truth.** Artifact-delta characterizations prevent the label `transition` from hiding whether anything durable changed, whether support increased, whether authority changed, or whether only visibility changed.

## Locality

Structural recovery is not merely language-local.

- It is **language-local** in inquiry orientation and natural-language/documentation boundaries: language is preserved as communicative or artifact-situated material and then bounded.
- It is **provider-local** in dpkg and Prometheus translation: provider-native representations require provider-specific decoding before Seed observations.
- It is **family-local** in source/artifact recovery and relationship extraction: Python source and documentation metadata have different adapters and different negative authority boundaries.
- It is **constitutionally recurring** only at the level of discipline: representation is not authority; recovered structures are bounded; support/provenance is preserved; negative boundaries prevent over-promotion.

The repository does not support calling this universal, representation-independent, or grammar-engine-owned.

## Typed unknowns

The following remain typed unknowns because current implementation evidence does not recover them:

- `multimodal_recovery`: no implementation-backed recovery from multimodal representations was reviewed.
- `diagram_recovery`: no diagram parser or diagram-to-constitutional-structure boundary was found in the reviewed implementation evidence.
- `audio_recovery`: no audio representation recovery is supported by the reviewed implementation.
- `vision_recovery`: no vision/image representation recovery is supported by the reviewed implementation.
- `representation_independent_recovery`: current evidence supports multiple representation-specific adapters, not representation-independent recovery.
- `universal_structural_grammar`: current evidence supports bounded family-local translation, not a universal structural grammar.
- `common_owner`: no single implementation owner currently owns operator prose orientation, provider translation, source artifact extraction, and competency methodology as one subsystem.

## Smallest truthful answer

The smallest recurring implementation-backed evidence is not prose interpretation. It is this repeated sequence:

```text
external representation is accepted
↓
family-local parsing or matching occurs
↓
a Seed-owned bounded structure is emitted
↓
representation-specific details are discarded, normalized, or retained only as metadata/support
↓
negative authority boundaries prevent the representation from becoming architecture
```

The smallest concrete cross-family examples are:

- operator prose becomes a preserved inquiry note plus read-only lexical orientation, not intent or command;
- dpkg status text becomes `PackageRecord` and package observations, not dpkg paragraphs as canonical truth;
- Prometheus JSON becomes decoded samples, provider-local observation shapes, and canonical observations, not provider JSON as Seed grammar;
- Python source/AST becomes relationship facts or artifact facts, not behavior, reachability, ownership, or architecture.

Therefore the repository has already been recovering constitutional structure from external representations in several bounded families. It has not merely been recovering English prose.

But the recovered truth is smaller than a universal theory:

```text
Seed currently demonstrates recurring boundary-preserving structural recovery
from multiple external representations.

Seed does not demonstrate universal representation-independent recovery.
```

## Lawful termination

This investigation terminates at characterization.

It does not introduce a universal grammar engine, redesign Seed grammar, speculate about future AI capabilities, recommend implementation, or stabilize representation-independent recovery as architecture.

Repository authority wins: current implementation supports bounded family-local recovery with recurring constitutional boundary discipline.

## Remaining questions

- Are there additional provider adapters whose translation path is compressed directly from provider-native material to canonical `Observation`, and do they weaken or refine the recurrence?
- Which downstream consumers depend on intermediate structures such as `PackageRecord`, `PrometheusDecodedSample`, `PrometheusObservationShape`, `RelationshipFact`, and `RepositoryArtifactFact` independently of canonical observation ingestion?
- Should future investigations compare test coverage for these boundaries, without changing the boundaries themselves?
- Are there operational surfaces where presentation vocabulary is still insufficiently separated from recovered structure?

## Confidence

Confidence is high that the repository distinguishes external representation from recovered bounded structure in operator prose, dpkg, Prometheus, Python relationship extraction, documentation metadata relationships, and repository artifact extraction.

Confidence is medium that this is best called constitutionally recurring, because the recurrence is a shared boundary discipline across unrelated families rather than a single implemented abstraction.

Confidence is low for any stronger claim that Seed has a representation-independent grammar or universal structural recovery engine.
