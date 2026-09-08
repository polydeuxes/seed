# Unknown Source to Provider Contract Recovery Investigation

## Executive answer

Seed currently has **one implementation-backed unknown-source-to-language-candidate path**: file-backed Ansible inventory intake through `InputInspector`. A source first becomes identifiable when `InputInspector.inspect_file(...)` hashes bounded file bytes, records audit metadata, classifies a bounded text prefix as `json`, `yaml`, `ini`, or `unknown`, and preserves warnings such as `empty_file`, `binary_or_null_bytes`, `unknown_format`, and extension mismatch evidence. That produces an `InputArtifact`, which is a language-candidate record, not a verified provider contract.

A provider language candidate becomes a usable provider contract only inside a provider-specific source that already knows the provider purpose. The Ansible source passes `declared_purpose="ansible_inventory"`, chooses an INI/YAML parser from `InputArtifact.detected_format` or extension fallback, rejects unsupported formats, reads UTF-8 text, and then runs Ansible-specific INI/YAML membership parsers before emitting observations. Prometheus, systemd, dpkg, and JSON observation import do not start from unknown external sources in the same way; their classes/functions are constructed or called only after a human/runtime-selected provider path has already established the provider contract.

The repository distinguishes a **failed language hypothesis** from a **provider contract violation** only partially:

- Before provider selection, `InputInspector` treats unknown/binary/empty/mismatched file evidence as candidate-format warnings.
- After provider selection, provider-specific validators raise or suppress provider-contract failures: Ansible raises `unsupported Ansible ...`, Prometheus returns no observations and stores `last_error` on response/API shape failures, JsonObservationSource raises `invalid JSON observation file` or per-entry validation failures, systemd silently returns no rows for malformed JSON output, and dpkg skips malformed records.

Provider Language Translation becomes permitted at provider-specific translation entry points after those provider-specific checks have accepted enough shape to proceed. Examples include Ansible parser membership records turning into identity observations, Prometheus `_query(...)` returning a success vector payload and `_prometheus_decoded_sample(...)` returning valid sample records, systemd row maps being accepted by `_systemd_json_rows(...)` and `_systemd_string(...)`, dpkg `PackageRecord` creation, and JsonObservationSource entry validation immediately before `Observation(...)` construction.

**Ownership-family recommendation:** Insufficient implementation evidence. The repository has recurring provider-language verification inside provider translation/adapters, and one local file-format candidate path through `InputInspector`; it does not yet show a recurring bounded responsibility that acquires or verifies provider language contracts independently of Provider Language Translation.

## Implementation evidence reviewed

- `seed_runtime/input_inspector.py`: `DetectedInputFormat`, `InputArtifact`, `InputInspector.inspect_file(...)`, text-format heuristics, extension mismatch warnings.
- `seed_runtime/ansible_inventory_source.py`: Ansible inventory provider bootstrap from `InputInspector`, parser selection, unsupported-format errors, UTF-8 validation, INI/YAML parser errors, observation metadata preservation.
- `seed_runtime/observation_sources.py`: `PrometheusObservationSource`, `PrometheusDecodedSample`, `PrometheusObservationShape`, `SystemdObservationSource`, `_systemd_json_rows(...)`, `JsonObservationSource`, observation collection behavior.
- `seed_runtime/local_packages.py`: dpkg status parsing, `PackageRecord`, malformed-record skip behavior, package observation emission.
- Tests reviewed: `tests/test_input_inspector.py`, `tests/test_ansible_inventory_source.py`, `tests/test_observation_sources.py`, and prior provider-language investigations (`provider_representation_to_observation_investigation.md`, `provider_language_translation_investigation.md`, `provider_language_translation_responsibility_characterization.md`, provider-language translation slices).

## Current contract acquisition paths

| Path | Contract acquisition evidence | Result |
| --- | --- | --- |
| Unknown file -> Ansible inventory | `InputInspector.inspect_file(...)` creates `InputArtifact`; `AnsibleInventoryObservationSource.collect()` passes declared purpose, selects parser format, rejects non-INI/YAML, reads UTF-8, and parses Ansible group/host structure. | This is the only reviewed path that begins from unknown file bytes and produces a provider-language candidate before provider-specific parsing. |
| Prometheus | `PrometheusObservationSource` is constructed with a Prometheus base URL and fixed `SAFE_QUERIES`; `_query(...)` verifies allowlist, HTTP JSON object, success status, vector result type, and list result. | Provider contract is human/runtime-established by constructing the Prometheus source; verification is response-shape validation inside the provider. |
| systemd | `SystemdObservationSource` calls fixed `systemctl ... --output=json` commands; `_systemd_json_rows(...)` JSON-decodes stdout to list-shaped dict rows. | Provider contract is established by the dedicated source and command path; malformed JSON becomes no rows, not a separate candidate failure. |
| dpkg | `LocalHostObservationSource` reads the configured dpkg status file and calls `parse_dpkg_status(...)`; the parser accepts only installed records with required fields. | Provider contract is established by the configured dpkg status path and parser call; malformed records are skipped. |
| JSON observation import | `JsonObservationSource` is constructed for a JSON observation file; `collect()` requires top-level object, `observations` array, entry object, required fields, non-empty strings, metadata object, timestamps, and `Observation` model validity. | Provider contract is established by choosing JsonObservationSource; malformed JSON/schema is a provider contract violation for that source. |

## Language-candidate evidence

`InputArtifact` is the clearest language-candidate representation. It preserves file path, size, SHA-256, extension, optional declared purpose, detected format, confidence, and warnings. `DetectedInputFormat` is intentionally small: `json`, `yaml`, `ini`, or `unknown`.

`InputInspector.inspect_file(...)` reads bytes in bounded chunks, hashes the whole file, keeps only a bounded sample for classification, detects null bytes, classifies text based on content rather than extension, and records extension mismatch warnings when content and suffix disagree. This establishes evidence about a language hypothesis while avoiding execution and embedded-reference resolution.

Ansible inventory is the only provider reviewed that consumes that language-candidate record before parser selection. It explicitly records the resulting `InputArtifact` and propagates the detected format, warnings, input path, and SHA-256 into observation metadata, which proves the source preserves the candidate evidence even after successful provider-specific parsing.

## Contract-verification evidence

### Ansible inventory

`AnsibleInventoryObservationSource.collect()` converts the language candidate into a provider-specific parsing contract. It:

1. calls `InputInspector.inspect_file(..., declared_purpose="ansible_inventory")`;
2. selects `parser_format` from the detected format;
3. falls back to extension only if the detector returned `unknown`;
4. rejects parser formats outside `ini`/`yaml`;
5. requires UTF-8 text;
6. runs Ansible-specific INI/YAML parsers;
7. emits observations only after group/host membership parsing succeeds.

This is evidence of a bounded progression from source bytes to candidate to provider-specific parser acceptance.

### Prometheus

`PrometheusObservationSource` is not an unknown-source path. The contract is assumed when the class is instantiated with a base URL and safe Prometheus query vocabulary. Verification occurs inside `_query(...)`, which rejects non-allowlisted queries, decodes JSON, requires an object, requires `status == "success"`, requires `data.resultType == "vector"`, and requires list-shaped `data.result`. Sample-level verification then happens in `_prometheus_decoded_sample(...)`, which accepts only dict samples with dict `metric`, list `value`, non-empty string `instance`, and parseable timestamps.

### systemd

`SystemdObservationSource` assumes the systemd contract by executing fixed `systemctl` commands with `--output=json`. `_systemd_json_rows(...)` treats stdout as JSON rows: invalid JSON or non-list payload returns an empty list; non-dict entries are filtered out. `_systemd_string(...)` accepts only non-empty strings. Translation then proceeds over provider-shaped runtime/unit-file dictionaries.

### dpkg

`parse_dpkg_status(...)` assumes dpkg status text and verifies records by field grammar. `_parse_dpkg_record(...)` returns `None` for malformed continuation lines, missing colons, or empty field names. `parse_dpkg_status(...)` skips malformed/incomplete records and only emits `PackageRecord` when `Package` exists and `Status` is exactly `install ok installed`.

### JSON observation import

`JsonObservationSource.collect()` assumes the JSON observation import contract once this source has been selected. It turns malformed JSON into `ValueError("invalid JSON observation file ...")`, then validates top-level object and `observations` array. `_observation_from_entry(...)` validates each entry before constructing `Observation`, causing the whole collect to fail before ingestion when any entry is malformed.

## Contract-violation evidence

The same payload condition is treated differently depending on whether a provider source has already been selected:

- **Malformed/unknown text before provider selection:** `InputInspector` records `unknown_format`, `empty_file`, or `binary_or_null_bytes`. This is failed candidate evidence, not a provider contract violation.
- **Unsupported detected format after Ansible provider selection:** `AnsibleInventoryObservationSource` raises `unsupported Ansible inventory format: <format>`. At that point the provider purpose is known, so the same format evidence becomes provider-specific rejection.
- **Malformed JSON after JsonObservationSource selection:** JSON decoding failure raises `invalid JSON observation file ...`; malformed entries raise `observations[index] ...` errors.
- **Malformed Prometheus HTTP response:** `_query(...)` raises `ValueError`, but `collect()` catches it with transport errors, records `last_error`, and returns no observations. That is a provider contract/availability failure inside a known Prometheus source, not language discovery.
- **Malformed systemd JSON:** `_systemd_json_rows(...)` returns `[]`; the provider source continues and emits no rows for malformed output. This is a contract failure handled as empty provider evidence rather than an exception.
- **Malformed dpkg records:** malformed records are skipped safely. This is contract filtering within an already selected dpkg parser, not a failed hypothesis about some other language.

## Provider translation entry point

Provider Language Translation first assumes a verified-enough provider contract at these implementation points:

- **Ansible:** after parser selection and successful `_parse_ini(...)` or `_parse_yaml(...)`; observation construction begins in the loop over parsed memberships.
- **Prometheus:** after `_query(...)` returns a validated vector payload and `_prometheus_decoded_sample(...)` returns a valid sample. `_prometheus_observation_shapes(...)` maps decoded samples to provider-local observation shapes; `_observation(...)` builds `Observation` objects.
- **systemd:** after `_systemd_json_rows(...)` and `_systemd_string(...)` produce usable unit/state values; `collect()` maps them to `systemd_unit`, `systemd_active_state`, `systemd_sub_state`, and `systemd_unit_file_state` observations.
- **dpkg:** at `PackageRecord` creation for installed packages; generic package observation emission begins in `package_records_to_observations(...)`.
- **JSON observation import:** after `_observation_from_entry(...)` validates the entry shape and constructs an `Observation`; there is little separate translation because the provider language is already Seed observation-shaped JSON.

## Answers to recovery questions

### 1. How does an unknown source become a provider language candidate?

Only file-backed intake through `InputInspector` currently demonstrates this. Unknown file bytes become a candidate when the inspector records an `InputArtifact` with content-derived `detected_format`, confidence, extension, hash, size, declared purpose if supplied, and warnings. The candidate is a language/form hypothesis (`json`, `yaml`, `ini`, `unknown`), not a provider contract.

### 2. How does a provider language candidate become a verified provider contract?

Only Ansible demonstrates candidate-to-provider progression. The candidate becomes usable when an Ansible-specific source has already supplied the provider purpose, selected an INI/YAML parser from the candidate (or extension fallback for unknown), accepted UTF-8 text, and parsed Ansible-specific inventory structure. Other reviewed providers do not acquire contracts from unknown candidates; they begin from already selected provider sources and verify provider response/file shape internally.

### 3. Where does the repository distinguish failed language hypothesis from provider contract violation?

The distinction exists at the boundary between `InputInspector` and provider-specific sources. `InputInspector` warning output is failed language-hypothesis evidence. Ansible unsupported-format/parser errors, JsonObservationSource JSON/schema errors, Prometheus `_query(...)` validation failures, systemd malformed-output empty rows, and dpkg malformed-record skips are provider contract handling after the provider source/path has been selected. There is no generic cross-provider type or framework that names this distinction.

### 4. Where does Provider Language Translation first assume a verified contract?

Translation begins at provider-local boundaries after enough shape validation has succeeded: Ansible parsed memberships; Prometheus validated vector payload plus decoded sample; systemd decoded row maps/strings; dpkg `PackageRecord`; JsonObservationSource validated entry-to-Observation construction. These are provider-specific implementation points, not a shared contract-verification layer.

### 5. Is there sufficient implementation evidence to justify a new ownership family?

Insufficient implementation evidence.

The repository demonstrates recurring Provider Language Translation and provider-local validation. It does not demonstrate a recurring bounded responsibility for acquiring or verifying provider language contracts independently of translation. `InputInspector` is a reusable local file-format candidate mechanism, but reviewed use shows it as Ansible intake support rather than a general provider-contract acquisition owner.

## Supported conclusions

1. A language candidate is implementation-backed for file-backed inputs through `InputArtifact` and `DetectedInputFormat`.
2. Ansible inventory is the only reviewed path that starts from content-based language detection before provider-specific parser selection.
3. Prometheus, systemd, dpkg, and JsonObservationSource begin from selected provider paths; their validation is provider-internal contract checking, not unknown-source discovery.
4. Malformed JSON is a failed language hypothesis only before a JSON/provider contract is selected; inside `JsonObservationSource`, Prometheus `_query(...)`, or systemd JSON-output handling, malformed JSON is provider-specific contract failure/empty evidence.
5. Provider Language Translation begins only after provider-local validation has accepted sufficient shape for provider-specific interpretation.

## Unsupported conclusions

- Unsupported: Seed has a general provider contract discovery framework.
- Unsupported: every future source can progress from unknown external source to verified provider contract without human/runtime provider selection.
- Unsupported: `InputInspector` verifies provider contracts by itself.
- Unsupported: Prometheus/systemd/dpkg contracts are acquired from unknown sources in current implementation.
- Unsupported: malformed provider payloads are uniformly represented as errors; behavior differs by provider.
- Unsupported: a new ownership family for contract acquisition is justified by existing recurring implementation evidence.

## Confidence

High confidence that `InputInspector` is the current language-candidate mechanism for file-backed raw input and that Ansible is the only reviewed provider using it before parser selection.

High confidence that Prometheus, systemd, dpkg, and JSON observation import rely on already selected provider/source paths and perform provider-local validation there.

Medium confidence on exhaustive coverage of every provider-like path because the repository contains many diagnostic and architectural documents; the investigation focused on the requested implementation areas and prior provider-language investigations.

## Recommendation

Do not recover a new ownership family at this time. Preserve the current characterization:

```text
Unknown Source
  -> InputArtifact / DetectedInputFormat language candidate (file-backed only)
  -> provider-specific parser/source selection when a provider purpose is known
  -> provider-local contract validation
  -> Provider Language Translation
```

If future implementation adds multiple providers that independently acquire and verify contracts from unknown sources before translation, then a new ownership investigation may be justified. Current evidence says Seed is still mostly relying on human- or runtime-established provider contracts, with Ansible file intake as the bounded exception.
