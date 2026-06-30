# External Artifact Intake vs Provider Language Translation Investigation

## Executive answer

External Artifact Intake already exists as bounded implementation work, but only as a recurring local responsibility pattern, not as a single shared framework or globally named ownership family.

The strongest implementation evidence is `InputInspector.inspect_file(...)`: it accepts a raw file path, reads bytes, hashes the whole file, samples a bounded prefix, detects null/binary content, determines a likely text format from content, compares that result to the file extension, and returns `InputArtifact` metadata without parsing provider semantics. `AnsibleInventoryObservationSource.collect()` then uses that `InputArtifact.detected_format` to choose the INI or YAML inventory parser before translating inventory grammar into `Observation` records.

The boundary is not universal. Several providers make parser choice by provider identity or fixed contract rather than independent format detection: Prometheus always performs HTTP GET and JSON-loads the Prometheus API response; systemd always invokes `systemctl --output=json` and JSON-loads rows; `JsonObservationSource` is a fixed JSON observation-file provider; toolkit manifests are JSON despite commonly using `.yaml` filenames in tests/CLI paths; capability catalog loading is fixed to checked-in `*.yml` files and invokes YAML loading by catalog path convention.

Therefore:

- **External Artifact Intake exists** where raw artifact acceptance and format/language determination happen before provider grammar interpretation.
- **Its authority terminates** when it has produced bounded artifact metadata and/or chosen the concrete parser/format for the provider.
- **Provider Language Translation begins** when provider-specific grammar is interpreted into provider-local records/shapes or Seed observations.
- **Parser selection is split in current implementation**: content/extension parser selection is External Artifact Intake in the Ansible inventory path; fixed parser choice by provider identity or declared source contract belongs to provider bootstrap/translation, not to a separate intake owner.
- **A new ownership family is weakly justified only if named narrowly** around recurring raw-artifact acceptance and language/parser selection. There is not enough evidence for a broad shared ingestion framework, parser abstraction, or universal upstream stage.

## Implementation evidence reviewed

### File-backed format inspection

`seed_runtime.input_inspector` defines `DetectedInputFormat = Literal["json", "yaml", "ini", "unknown"]`, a bounded sample size, extension-to-format expectations, and an `InputArtifact` record containing the path, size, SHA-256, extension, declared purpose, detected format, confidence, and warnings.

`InputInspector.inspect_file(...)` accepts a raw path, reads file bytes in chunks, hashes the full file, samples only a bounded prefix, detects empty and null-byte files, decodes text with replacement, calls `_detect_text_format(...)`, and warns when the extension disagrees with the detected format.

`_detect_text_format(...)` chooses JSON, INI, YAML, or unknown using content signals such as first non-whitespace character, INI section syntax, YAML mapping syntax, and Ansible inventory keys. It does not parse provider semantics.

### Ansible inventory provider

`AnsibleInventoryObservationSource.collect()` calls `InputInspector.inspect_file(..., declared_purpose="ansible_inventory")`, stores the resulting `InputArtifact`, chooses `parser_format` from `artifact.detected_format`, falls back to extension only when detection is unknown, rejects unsupported formats, then reads UTF-8 text and invokes `_parse_ini(...)` or `_parse_yaml(...)`.

The INI/YAML parser methods are provider-specific. `_parse_ini(...)` interprets Ansible group sections, ignores `:vars`/`:children`, uses `shlex.split(...)`, filters secret fields, and records host/group/alias membership. `_parse_yaml(...)` parses the repository's simple YAML subset and walks Ansible `hosts`/`children` mappings. Observation emission adds `input_path`, `input_sha256`, `input_detected_format`, and `input_warnings` to metadata.

Tests preserve this split. `tests/test_input_inspector.py` proves content can override an `.ini` extension for YAML content and records an extension mismatch warning. `tests/test_ansible_inventory_source.py` proves a `.ini` file containing YAML uses the YAML parser, and a `.yml` file containing INI uses the INI parser.

### Prometheus HTTP provider

`PrometheusObservationSource` accepts a base URL and timeout, restricts queries to `SAFE_QUERIES`, performs HTTP GET with `Accept: application/json`, `json.loads(...)` the response body, validates the Prometheus response envelope (`dict`, status `success`, vector `data`, list `result`), and then passes result samples through `_prometheus_decoded_sample(...)` and `_prometheus_observation_shapes(...)` before constructing `Observation` objects.

This path has raw external artifact intake in the sense that HTTP response bytes enter the repository and are JSON-decoded. However, it does not contain independent language detection. The parser is fixed by the provider contract: Prometheus HTTP API JSON. The recently recovered local completion point remains implementation-backed: Prometheus JSON -> `PrometheusDecodedSample` -> `PrometheusObservationShape` -> `Observation`.

### systemd provider

`SystemdObservationSource` invokes `systemctl list-units --output=json` and `systemctl list-unit-files --output=json`, then `_systemd_json_rows(...)` `json.loads(...)` the command output and filters to dictionary rows. Parser choice is fixed by command construction and provider identity, not by content sniffing or extension handling. Provider grammar begins when rows are interpreted as unit names, active/sub states, and unit-file states.

### JSON observation file provider

`JsonObservationSource.collect()` reads a local file as UTF-8, `json.loads(...)` it, requires a top-level object with an `observations` array, and validates each entry into `Observation`. This is a fixed JSON import provider. It accepts a raw artifact but does not decide among possible artifact languages.

### dpkg status provider

`LocalHostObservationSource._collect_local_package_observations(...)` reads `/var/lib/dpkg/status` through `_read_text(...)`, passes text to `parse_dpkg_status(...)`, and converts resulting `PackageRecord` instances to observations. `seed_runtime.local_packages` explicitly describes dpkg status parsing as the first narrow package adapter. No content sniffing occurs; parser selection is by fixed dpkg-status source identity.

### Documentation and Python source adapters

Documentation claim extraction intentionally accepts caller-provided text, parses simple Markdown headings/lines, and parses YAML front matter for navigation metadata without reading files or integrating with runtime/tool execution. Relationship observation for Python imports/definitions likewise parses caller-provided Python source text with `ast.parse(...)` and explicitly does not read files or scan repositories. These modules are provider-language adapters, not external artifact intake owners, because callers already provide text.

The broader documentation structure diagnostic does perform repository-relative `.md` path validation and Markdown structural observation, but its public contract is an operational diagnostic surface, not a provider ingestion path for observations. It reinforces that extension/path validation exists, but it should not be promoted automatically into the provider intake boundary.

### Catalog and manifest loading

`CapabilityCatalog.load(...)` scans checked-in `*.yml` files and `_load_yaml_mapping(...)` uses PyYAML when present or a small fallback YAML parser. This is fixed catalog bootstrap by path convention, not content-detected external artifact intake.

`ToolRegistry.load_manifest(...)` delegates to `load_toolkit_manifest(...)`, which reads the manifest and `json.loads(...)` it, then validates toolkit fields. Tests and CLI code pass paths ending in `toolkit.yaml`, which is an important counterexample: extension names are not authoritative across the repository, and the registry parser is fixed to JSON by implementation.

## Current ingestion pipeline

The implementation-backed pipeline is not a single global chain. Current paths look like this:

```text
Ansible inventory file path
  -> InputInspector raw-byte read/hash/sample
  -> detected_format + warnings
  -> parser selection: INI or YAML
  -> Ansible provider grammar interpretation
  -> Observation

Prometheus base URL
  -> allowlisted HTTP GET
  -> JSON decode + Prometheus envelope validation
  -> PrometheusDecodedSample
  -> PrometheusObservationShape
  -> Observation

systemctl provider
  -> fixed systemctl --output=json command
  -> JSON row loading/filtering
  -> systemd unit/state interpretation
  -> Observation

dpkg status path
  -> fixed status file text read
  -> dpkg status grammar parsing
  -> PackageRecord
  -> Observation

JSON observation file
  -> fixed JSON file read/decode
  -> observation-array validation
  -> Observation
```

## Artifact intake responsibilities

Implementation evidence supports these responsibilities as External Artifact Intake where they occur before provider grammar interpretation:

1. **Accept raw external artifact handles**: file paths, command output, or HTTP response bodies.
2. **Perform safe bounded acquisition**: read bytes/text with limits where implemented, decode without execution, handle missing/unreadable artifacts conservatively.
3. **Preserve artifact audit metadata**: path, size, hash, extension, declared purpose, detected format, confidence, and warnings in the `InputArtifact` path.
4. **Determine artifact language when content sniffing exists**: JSON/YAML/INI/unknown in `InputInspector`.
5. **Compare declared/extension language to detected language**: warning on mismatches.
6. **Choose parser when the provider permits multiple artifact languages**: Ansible inventory chooses INI vs YAML from `InputArtifact.detected_format`, falling back to extension only if detection is unknown.

## Provider translation responsibilities

Implementation evidence supports these responsibilities as Provider Language Translation:

1. Interpret provider-specific grammar after a parser/format has been selected.
2. Map provider fields into provider-local normalized records or shapes, such as Ansible host/group membership, `PrometheusDecodedSample`, `PrometheusObservationShape`, systemd row fields, or `PackageRecord`.
3. Apply provider-specific safety exclusions and unsupported-shape decisions, such as Ansible secret field filtering, unsupported host patterns, Prometheus safe query allowlisting, malformed Prometheus sample skipping, systemd row filtering, and dpkg skipping non-installed or malformed records.
4. Construct `Observation` objects or normalized intermediate records that later become observations.

## Boundary between the two

The cleanest implementation boundary appears in the Ansible inventory path:

```text
External Artifact Intake:
  path -> InputInspector.inspect_file(...) -> InputArtifact(detected_format, warnings, hash, size, extension)
  parser_format selection from detected format / fallback extension

Provider Language Translation:
  _parse_ini(text) / _parse_yaml(text)
  Ansible inventory host/group/alias interpretation
  Observation emission
```

For fixed-contract providers, the boundary is compressed or absent:

```text
Prometheus Provider Language Translation begins at provider HTTP JSON contract:
  _query(...) JSON-loads and validates Prometheus envelope
  _prometheus_decoded_sample(...) starts provider-shaped sample decoding

systemd Provider Language Translation begins at fixed systemctl JSON output:
  _systemd_json_rows(...) JSON-loads command output
  row fields are interpreted as units/states

dpkg Provider Language Translation begins at fixed dpkg status text:
  parse_dpkg_status(...) parses status records

JSON Observation import begins at fixed JSON observation-file contract:
  JsonObservationSource.collect() JSON-loads and validates observation entries
```

## Answers to recovery questions

### 1. Who accepts raw external artifacts?

- `InputInspector.inspect_file(...)` accepts raw file paths for inspectable file-backed inputs.
- `AnsibleInventoryObservationSource.collect()` accepts an inventory file path and delegates initial inspection to `InputInspector`.
- `PrometheusObservationSource._query(...)` accepts HTTP response bytes from a Prometheus API endpoint.
- `SystemdObservationSource` accepts command stdout from `systemctl --output=json`.
- `LocalHostObservationSource._collect_local_package_observations(...)` accepts `/var/lib/dpkg/status` text.
- `JsonObservationSource.collect()` accepts a JSON observation file path.
- Catalog and registry loaders accept catalog/manifest paths for bootstrap metadata.

### 2. Who determines what language an artifact speaks?

- `InputInspector._detect_text_format(...)` determines JSON/YAML/INI/unknown from content for file-backed inputs that use it.
- `AnsibleInventoryObservationSource.collect()` chooses the actual parser format for inventories from `InputArtifact.detected_format` with extension fallback.
- Prometheus, systemd, dpkg status, JSON observation import, capability catalog, and registry manifest paths do **not** independently determine language from content; their language is fixed by provider/source identity or loader contract.

### 3. Who chooses which parser or grammar to invoke?

- Ansible inventory parser selection is chosen by `AnsibleInventoryObservationSource.collect()` using `InputInspector` output.
- Prometheus uses JSON because `_query(...)` is a Prometheus HTTP JSON API client.
- systemd uses JSON because the provider itself constructs `systemctl --output=json` commands.
- dpkg uses `parse_dpkg_status(...)` because the source is the fixed dpkg status database.
- capability catalog uses YAML because it loads `*.yml` catalog entries.
- toolkit registry uses JSON because `load_toolkit_manifest(...)` unconditionally calls `json.loads(...)`.

### 4. Where does provider-specific grammar actually begin?

- Ansible: `_parse_ini(...)` / `_parse_yaml(...)` after parser format selection.
- Prometheus: Prometheus envelope validation and `_prometheus_decoded_sample(...)`, then `_prometheus_observation_shapes(...)`.
- systemd: `_systemd_json_rows(...)` plus field interpretation in `_collect_runtime_units(...)` and `_collect_unit_file_states(...)`.
- dpkg: `parse_dpkg_status(...)` and `_parse_dpkg_record(...)`.
- JSON observation import: validation of `observations` entries into `Observation` objects.
- Documentation/Python adapters: caller-provided Markdown/YAML-front-matter/Python text parsing functions, because external file intake is explicitly outside those helpers.

### 5. Where does Provider Language Translation first become responsible?

Provider Language Translation begins when the implementation stops asking “what artifact language is this?” and starts interpreting provider-specific meanings within that language. In the Ansible path, that is the call to `_parse_ini(...)` or `_parse_yaml(...)`. In fixed-contract providers, it begins immediately at the provider-specific JSON/text loading boundary because there is no separate content-language decision.

## Counterexamples and disconfirming evidence

1. **Typed/caller-provided source text**: documentation claim extraction and relationship observation explicitly do not read files; they parse text already supplied by a caller.
2. **No format detection**: Prometheus, systemd, dpkg, JSON observation files, registry manifests, and capability catalog files all use fixed parser contracts.
3. **Extension names ignored or misleading**: toolkit manifests are JSON-loaded even when paths such as `toolkit.yaml` are passed by tests/CLI code.
4. **Parser selection by provider identity**: Prometheus JSON, systemctl JSON, and dpkg status parsing are selected by the provider source, not by an independent artifact-language detector.
5. **Parsing can be provider translation**: `parse_dpkg_status(...)` is both parsing and the first provider adapter; no upstream language determination appears before it.

## Supported conclusions

1. External Artifact Intake is present as implementation-backed bounded work in the file-backed Ansible/input-inspection path.
2. Its strongest responsibilities are raw file acceptance, safe read/hash/sample, content format detection, extension mismatch warnings, and parser selection for multi-format file-backed providers.
3. Its authority terminates at `InputArtifact` metadata and parser-format selection; it does not own provider grammar semantics or observation construction.
4. Provider Language Translation begins with provider grammar interpretation: Ansible INI/YAML inventory parsing, Prometheus decoded samples/shapes, systemd row interpretation, dpkg status records, and observation-file entry validation.
5. Parser selection is not uniformly owned. Content-driven parser selection is External Artifact Intake; fixed parser choice by provider identity/source contract is Provider Language Translation or provider bootstrap.
6. Implementation evidence justifies recognizing a narrow recurring upstream responsibility, but not a redesign, generic parser framework, shared ingestion layer, or broad ownership family without further slices.

## Unsupported conclusions

- Unsupported: all providers have a separate External Artifact Intake phase.
- Unsupported: all JSON/YAML/INI/TOML/Markdown/Python parsing should move under one owner.
- Unsupported: extension names are authoritative.
- Unsupported: content sniffing is already a general framework.
- Unsupported: Prometheus requires a new upstream boundary before Provider Language Translation beyond HTTP JSON acquisition and envelope validation.
- Unsupported: documentation/Python relationship parsers own external artifact intake; they explicitly operate on caller-provided text.
- Unsupported: a new ownership recovery should be performed now. This report characterizes existing implementation only.

## Confidence

Moderate-high for the Ansible/InputInspector boundary because code and tests directly prove content-based format detection and parser selection before provider semantics.

Moderate for the broader recurring-responsibility claim because multiple providers accept raw artifacts, but most fixed-contract providers compress acquisition, decoding, and provider translation into provider-specific code rather than a separate intake owner.

Low for any claim that External Artifact Intake is already a complete ownership family across the repository.

## Recommendation on ownership family justification

A new ownership family is **not yet strongly justified** as a repository-wide family.

A narrow family candidate may be justified only if future work needs a name for the already recurring, implementation-backed work of:

```text
raw artifact acceptance -> safe bounded acquisition -> artifact language detection -> parser selection handoff
```

However, current implementation evidence shows this most clearly in the Ansible/input-inspection path and only partially in fixed-contract providers. The safer recommendation is:

```text
Insufficient implementation evidence for a broad ownership family.
```

If named at all, it should be treated as a narrow upstream boundary candidate, not as a mandate to redesign ingestion or centralize parsers.
