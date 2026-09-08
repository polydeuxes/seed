# Provider Language Translation Investigation

## Bounded answer

The implementation already exposes recurring bounded language-translation responsibilities before canonical `Observation` construction, but it exposes them unevenly. The strongest pattern is not "intermediate records" as such. The stronger recurring identity is bounded translation work that takes a provider-specific vocabulary and grammar, decodes or selects a safe subset, shapes identity, assigns Seed predicates, and then constructs canonical `Observation` records.

`Observation` is the first fully Seed-language sentence in the investigated paths: it requires `source_type`, `observed_at`, `subject`, `predicate`, `value`, `confidence`, `metadata`, `dimensions`, and optional expiry. That shape is where provider-specific samples, rows, status fields, AST nodes, git porcelain lines, local files, and platform APIs become Seed observation grammar.

## Representative providers reviewed

| Provider family | Provider language | Provider grammar | Transition boundary | Natural artifact, if any | Compression level |
| --- | --- | --- | --- | --- | --- |
| dpkg package inventory | `/var/lib/dpkg/status` package-manager fields | Paragraph records split into field maps; only `Status: install ok installed` is accepted | `parse_dpkg_status(...)` emits `PackageRecord`; `package_records_to_observations(...)` assigns package predicates | `PackageRecord` | Separated |
| Python relationship extraction | Python source syntax | Python AST nodes for imports and top-level definitions | `extract_python_*_relationship_facts(...)` emits `RelationshipFact`; `RepositorySourceObservationSource._relationship_observation(...)` constructs observations | `RelationshipFact` | Separated |
| Prometheus | Prometheus HTTP API JSON vector samples, metric labels, sample timestamp/value pairs | Allowlisted query names, success JSON object, `data.resultType == vector`, list samples with `metric` and `value` | `_query(...)` validates provider grammar; `_observations_from_query(...)` maps samples directly to observations | No durable intermediate record | Compressed translation work |
| systemd | `systemctl --output=json` unit and unit-file rows | JSON list rows with `unit`/`UNIT`, `active`/`ACTIVE`, `sub`/`SUB`, `unit_file`/`UNIT FILE`, `state`/`STATE` | `_collect_runtime_units(...)` and `_collect_unit_file_states(...)` decode row maps; `collect(...)` maps units/states to observations | Runtime dicts only | Partially separated, mostly compressed |
| filesystem / local host | Python stdlib/platform values and local files under `/proc`, `/sys`, `/etc`, and `/var/lib/dpkg/status` | API return shapes, text files, directory/file path conventions, mount/network/listener/package/systemd sub-grammars | `LocalHostObservationSource.collect(...)` orchestrates many bounded collectors; `_observation(...)` constructs local observations; dpkg and systemd are delegated | Mixed: many direct observations; package/systemd artifacts delegated | Mixed |
| repository state | Git command outputs and porcelain status lines | `rev-parse`, branch, remote, and `status --porcelain=v1` line grammar | `GitRepositoryObservationProvider.observe(...)` decodes git outputs into `RepositoryObservation` | `RepositoryObservation` | Separated, but not canonical `Observation` |

## Implementation evidence by provider

### dpkg package inventory

**Vocabulary.** The dpkg path speaks dpkg status vocabulary: package names, status strings, versions, architectures, and the dpkg manager identity.

**Grammar.** The grammar is dpkg status text split into records and parsed into fields. The implementation accepts only records whose `Status` field exactly equals `install ok installed`; malformed records and records missing `Package` or `Status` are skipped.

**Where provider language ends.** Provider language ends at `parse_dpkg_status(...)`, where dpkg field maps are converted into `PackageRecord` objects.

**Where Seed Observation language begins.** Seed Observation language begins in `package_records_to_observations(...)`, which assigns Seed predicates (`package_installed`, `package_version`, `package_architecture`, `package_manager`), subject, confidence, metadata, and dimensions.

**Bounded work.** The bounded work is split into provider decoding and observation emission. This is one of the clearest mature examples: `dpkg text -> PackageRecord -> Observation`.

### Python relationship extraction

**Vocabulary.** The Python source provider speaks import statements, `from ... import ...` statements, top-level functions, async functions, and classes.

**Grammar.** The grammar is Python syntax parsed with `ast.parse(...)`; invalid Python returns an empty list rather than observations.

**Where provider language ends.** Python language ends when AST nodes are converted into language-neutral `RelationshipFact` records containing `relationship_kind`, `subject`, `object`, `path`, and `evidence`.

**Where Seed Observation language begins.** Seed Observation language begins in `RepositorySourceObservationSource._relationship_observation(...)`, which maps `RelationshipFact.subject` to observation subject, `relationship_kind` to predicate, `object` to value, and path/evidence into metadata and dimensions.

**Bounded work.** The extraction module explicitly limits itself to static import and declaration evidence and refuses behavior, ownership, reachability, graph building, and runtime execution. This makes `RelationshipFact` a consequence of a separated bounded adapter, not proof that all providers need records.

### Prometheus

**Vocabulary.** Prometheus speaks HTTP API JSON for a fixed allowlist of metric names: `up`, `node_uname_info`, `node_filesystem_avail_bytes`, and `node_filesystem_size_bytes`.

**Grammar.** The provider grammar is a successful Prometheus JSON object with `data.resultType` equal to `vector` and a list-shaped `data.result`; each sample must be a dict with dict-shaped `metric`, list-shaped `value`, non-empty string `instance`, and parseable sample timestamp.

**Where provider language ends.** Provider language ends inside `_observations_from_query(...)`, after sample shape checks, label extraction, timestamp parsing, and metric-specific branch selection.

**Where Seed Observation language begins.** Seed Observation language begins at `_observation(...)`, which creates an `Observation` with endpoint subject, Seed predicate, numeric/derived value, confidence, metadata, and filesystem dimensions when relevant.

**Bounded work.** Prometheus has clear bounded translation work but no named intermediate provider record. The same method decodes samples, preserves label metadata, shapes identity around the `instance`, assigns predicates (`endpoint_role`, `up`, `os`, `filesystem_avail_bytes`, `filesystem_size_bytes`), and constructs observations. This is a compressed provider-language-to-Observation path rather than absence of translation.

### systemd

**Vocabulary.** systemd speaks unit identity, runtime active/sub states, and unit-file enablement state through `systemctl` JSON output.

**Grammar.** The grammar is list-shaped JSON rows. Runtime rows are keyed by `unit`/`UNIT`, `active`/`ACTIVE`, and `sub`/`SUB`; unit-file rows are keyed by `unit_file`/`UNIT FILE` and `state`/`STATE`. `_systemd_json_rows(...)` rejects invalid JSON and non-list payloads, while `_systemd_string(...)` strips valid strings and drops non-strings/empty strings.

**Where provider language ends.** Provider language mostly ends in `_collect_runtime_units(...)` and `_collect_unit_file_states(...)`, which reduce systemctl rows to Python dicts keyed by unit name. However, this boundary remains thin: those dicts are not domain records and observation assignment follows immediately in `collect(...)`.

**Where Seed Observation language begins.** Seed Observation language begins where `collect(...)` assigns `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, and `systemd_unit_file_state` predicates and calls `_observation(...)`.

**Bounded work.** systemd demonstrates partially separated decoding but compressed translation. The implementation-visible responsibility is not a mature `SystemdUnitRecord`; it is bounded decoding and predicate assignment inside `SystemdObservationSource`.

### filesystem / local host

**Vocabulary.** The local-host provider speaks multiple local languages: platform/uname values, disk usage API values, `/proc`/`/sys`/`/etc` files, network and listener structures, mount/storage data, passwd/group text, dpkg status text, and systemd unit output through delegated systemd collection.

**Grammar.** The top-level grammar is not one provider grammar. `LocalHostObservationSource` is an orchestrator over many sub-grammars. It explicitly uses Python stdlib APIs and local read-only files and does not execute shells or subprocesses for the local-host collection itself.

**Where provider language ends.** For simple stdlib/platform/disk observations, local provider language ends immediately inside `collect(...)` when values are assigned to Seed predicates. For dpkg, provider language ends in `parse_dpkg_status(...)`. For systemd, it delegates to `SystemdObservationSource`.

**Where Seed Observation language begins.** Seed Observation language begins at direct `_observation(...)` calls for local host facts and at delegated provider conversion paths for package and systemd facts.

**Bounded work.** Local host is mixed. It proves that not every provider requires a named intermediate record: direct platform/disk facts are compressed. It also proves that when a sub-language becomes substantial, the implementation already starts to split it out: dpkg parsing lives in `seed_runtime.local_packages`, and systemd is a dedicated source.

### repository state

**Vocabulary.** Repository state speaks git command outputs: work-tree checks, HEAD commit, current branch, remotes, and porcelain-v1 status lines.

**Grammar.** The provider grammar includes `git rev-parse --is-inside-work-tree`, `rev-parse HEAD`, `branch --show-current`, `remote`, and `status --porcelain=v1`; status lines use `??` for untracked and index/worktree status columns for staged and modified counts.

**Where provider language ends.** Git language ends in `GitRepositoryObservationProvider.observe(...)`, which counts porcelain lines and returns a `RepositoryObservation` dataclass with repository path, VCS, head, branch, dirty flag, counts, remote presence, status availability, and non-mutation flags.

**Where Seed Observation language begins.** In this provider, canonical Seed `Observation` language does not begin. The natural artifact is `RepositoryObservation`, a read-only diagnostic/repository-state record with `to_json_dict(...)` and formatting helpers, not a canonical observation event.

**Bounded work.** Repository state is an important counterexample to overclaiming. It exposes provider decoding and a structured artifact, but not every structured provider result is part of the canonical Observation construction path.

## Responsibility characterization

| Responsibility | Implementation-visible today | Evidence-backed characterization |
| --- | --- | --- |
| Provider vocabulary | Yes | Constants, allowlists, provider-specific field names, metric names, unit keys, package fields, AST node types, git command outputs. |
| Provider grammar | Yes, unevenly | AST parsing, dpkg record/field parsing, Prometheus JSON vector checks, systemd JSON row checks, git porcelain parsing. |
| Provider decoding | Yes | `parse_dpkg_status`, `extract_python_*_relationship_facts`, Prometheus `_query`/sample checks, systemd row collectors, git status parsing. |
| Language translation | Yes | Provider facts/samples/rows become Seed subjects, predicates, values, metadata, and dimensions. |
| Identity shaping | Yes | Package dimensions, Python module subject derivation, Prometheus endpoint instance preservation, systemd host+unit dimensions, git repository path. |
| Predicate assignment | Yes | Package predicates, relationship kinds, Prometheus metric-to-predicate branches, systemd predicates, local host predicates. |
| Observation construction | Yes where applicable | Canonical `Observation(...)` construction appears in package, repository-source, Prometheus, systemd, and local-host paths. Repository state instead constructs `RepositoryObservation`. |

## Recurring patterns

### Pattern A: separated provider decoding and generic observation emission

Mature examples:

```text
dpkg status text -> PackageRecord -> package observations
Python source text -> RelationshipFact -> relationship observations
```

The record exists because the implementation separated bounded provider decoding from observation construction. The record is not the architectural identity by itself.

### Pattern B: compressed provider decoding, translation, and observation construction

Compressed examples:

```text
Prometheus HTTP JSON vector sample -> metric-specific branch -> Observation
systemd JSON row maps -> unit/state loops -> Observation
local platform/disk values -> direct local-host Observation
```

These providers still expose translation responsibilities: they validate provider grammar, select vocabulary, shape identity, assign predicates, and construct observations. They just do so without a named intermediate record.

### Pattern C: provider decoding into a non-Observation artifact

Repository state demonstrates:

```text
git command output -> RepositoryObservation -> JSON/formatting
```

This is bounded language decoding, but it does not currently enter canonical Seed Observation grammar.

## Answers to the central questions

### 1. Do providers already expose bounded language translation responsibilities?

Yes. The evidence spans independent families: package-manager text, Python source, Prometheus metrics, systemd unit rows, local host APIs/files, and git repository state. Each implements some combination of provider vocabulary selection, grammar validation/parsing, identity shaping, predicate/value assignment, and structured output construction.

### 2. Where does provider language end?

Provider language ends at different depths:

- dpkg: at `PackageRecord` creation.
- Python relationships: at `RelationshipFact` creation.
- Prometheus: inside `_observations_from_query(...)`, just before `_observation(...)` creates Seed observations.
- systemd: after JSON rows are reduced to runtime/unit-file dicts, though predicate assignment remains in the same source class.
- local host: often at direct `_observation(...)` calls, except delegated dpkg/systemd paths.
- repository state: at `RepositoryObservation`, not at canonical `Observation`.

### 3. Where does Seed Observation language begin?

Seed Observation language begins when the implementation fills canonical fields: subject, predicate, value, source type, observed time, confidence, metadata, dimensions, and optional expiry. In the reviewed code, that is the `Observation(...)` construction point or helper wrapping it. Repository state is the counterexample: it creates `RepositoryObservation`, so canonical Observation language does not begin there.

### 4. Are intermediate records the recurring implementation identity, or consequences of separated bounded work?

Intermediate records are consequences of separated bounded work. `PackageRecord`, `RelationshipFact`, and `RepositoryObservation` prove that records appear where decoding has been separated from downstream output construction. Prometheus, systemd, and local-host direct observations prove that the recurring responsibility can exist without a named record.

### 5. What is the smallest recurring implementation-backed ownership family supported by the evidence?

The smallest supported family is **provider-language translation to bounded Seed output**. Its implementation-backed responsibilities are:

1. provider vocabulary selection;
2. provider grammar decoding or validation;
3. provider identity shaping;
4. Seed predicate/value assignment;
5. output construction as canonical `Observation` where the provider participates in the observation pipeline, or as another bounded record where it does not.

A narrower family named "intermediate records" is not supported because multiple providers perform the translation without such records. A broader family such as a generic grammar framework, generic language engine, or provider redesign is unsupported by this investigation.

## Supported conclusions

- Providers already speak bounded languages before Seed Observation language begins.
- The implementation has multiple mature separated boundaries (`PackageRecord`, `RelationshipFact`) and multiple compressed boundaries (Prometheus, systemd, local host direct facts).
- Seed Observation grammar begins at canonical `Observation(...)` construction, not at provider acquisition.
- The recurring implementation identity is bounded translation work, not intermediate records.
- Repository state proves that bounded provider decoding can produce a structured record without entering canonical Observation grammar.

## Unsupported conclusions

- Unsupported: every provider should have an intermediate record.
- Unsupported: a generic grammar framework or language engine is present or needed.
- Unsupported: Prometheus or systemd should be redesigned.
- Unsupported: repository state currently constructs canonical `Observation` records.
- Unsupported: provider labels or presentation vocabulary should be promoted to architectural knowledge without implementation evidence.
- Unsupported: changes to evidence interpretation, fact redesign, projection redesign, schema, ledger behavior, or runtime behavior.

## Confidence

High confidence that bounded language translation responsibilities recur across dpkg, Python relationship extraction, Prometheus, systemd, local host, and repository state.

High confidence that intermediate records are not the recurring identity because Prometheus, systemd, and several local-host paths perform translation without named records.

Medium confidence on the exact boundary names for local host because it contains many sub-collectors and some direct observations; its top-level source is more an orchestrator than a single provider grammar.

Medium confidence on repository state as an adjacent provider-language example because it produces `RepositoryObservation`, not canonical `Observation`.

## Recommended first ownership investigation, if justified

A first ownership investigation is justified only as characterization, not redesign: investigate **Provider Language Translation** as the smallest recurring ownership family. The investigation should start from bounded work already visible in code and compare separated and compressed examples. It should not prescribe new records, schemas, engines, or behavior changes.
