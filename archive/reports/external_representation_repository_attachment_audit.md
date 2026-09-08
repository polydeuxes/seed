# External Representation / Repository Attachment Audit

## Executive answer

Yes, with an important qualification: the repository strongly supports a recurring boundary between an external/provider representation and any repository-supported attachment, but it does **not** implement one universal object named `RepositoryAttachment` or one centralized attachment engine.

The stronger supported model is:

```text
External representation
  -> bounded candidate(s), observations, translations, or matches
  -> repository-supported attachment only when implementation evidence is sufficient
  -> shared repository responsibilities
```

The weaker, rejected model is:

```text
External representation
  -> interpretation
  -> repository truth
```

The repository repeatedly preserves candidate evidence, unknowns, unsupported formats, no-match states, and non-promotion boundaries. It does not require complete semantic understanding before preserving observation or orientation. It does require bounded implementation support before an external representation can participate in shared repository responsibilities.

## Repository evidence reviewed

Representative evidence reviewed:

- `seed_runtime/input_inspector.py` for bounded file-backed input inspection and candidate format detection.
- `seed_runtime/ansible_inventory_source.py` for provider-specific translation from a file candidate into Ansible inventory observations.
- `seed_runtime/observation_sources.py` for repository-source observation, Prometheus, systemd, and JSON observation import.
- `seed_runtime/local_packages.py` for dpkg status parsing and malformed-record skipping.
- `seed_runtime/inquiry_orientation.py` for operator-prose preservation and deterministic lexical orientation.
- `seed_runtime/knowledge/observation_agreement.py` for candidate agreement without semantic or architectural promotion.
- `seed_runtime/knowledge/grammar_observation.py` for recurring relation-shape observation without grammar/truth promotion.
- `seed_runtime/selection_path_audit.py` for candidate sets, non-selected alternatives, and explicit unknown selection targets.
- Existing recovery/audit documents, especially `unknown_source_to_provider_contract_recovery_investigation.md`, `bounded_question_discipline_investigation.md`, `repository_surface_inventory_observation.md`, `responsibility_behavior_characterization.md`, `reasoning_space_translation_investigation.md`, and recent frontier/lineage documents under `docs/`.

## Implementation evidence

### 1. File bytes become a bounded candidate, not truth

`InputInspector.inspect_file(...)` hashes file bytes, reads only a bounded sample for classification, records path/size/hash/extension/declared purpose, and emits `detected_format`, `confidence`, and `warnings`. The supported detected formats are deliberately limited to `json`, `yaml`, `ini`, and `unknown`.

Important boundary evidence:

- empty files become `empty_file` warnings;
- binary/null-byte files become `binary_or_null_bytes` warnings;
- unrecognized text becomes `unknown_format`;
- extension mismatch is preserved as warning evidence;
- the inspector does not execute content or resolve embedded references.

This supports `External Representation != Repository Attachment`: raw file bytes become a bounded `InputArtifact` language/form candidate, not a provider contract and not repository truth.

### 2. Ansible translates only after provider-specific acceptance

`AnsibleInventoryObservationSource.collect()` supplies `declared_purpose="ansible_inventory"`, stores the `InputArtifact`, selects a parser from detected format or extension fallback, rejects non-INI/YAML with `unsupported Ansible inventory format`, requires UTF-8, parses only bounded static INI/YAML inventory shapes, and then emits observations.

The class docstring explicitly rejects invoking Ansible, expanding host patterns, resolving aliases, validating connectivity, or performing network access. This means Ansible inventory text is not immediately promoted into cluster truth. It becomes host/group observations only after provider-specific parsing succeeds, and even then the emitted metadata preserves input-path, detected-format, warning, hash, and source evidence.

### 3. Prometheus metrics are allowlisted and shape-validated

`PrometheusObservationSource` accepts only a fixed safe query list and rejects arbitrary PromQL. `_query(...)` validates that the HTTP response is a JSON object, has `status == "success"`, has vector-shaped data, and has a list result. Collection returns no observations and stores `last_error` when provider fetch or shape validation fails.

This is not full metric understanding. It is bounded provider translation from a known metric family into observations only after response-shape acceptance. For `node_uname_info`, stable identity labels are treated specially; other metrics remain endpoint-scoped and do not participate in endpoint alias normalization. That is direct evidence that one provider representation can have multiple possible attachment consequences depending on query family and supported label evidence.

### 4. systemd and dpkg preserve provider-local limits

The systemd helper `_systemd_json_rows(...)` returns an empty list on invalid JSON or non-list payloads and filters to dict entries. `_systemd_string(...)` accepts only non-empty strings. The dpkg parser only emits `PackageRecord` instances for installed package records and safely skips malformed records or records missing `Package`/`Status`.

These are bounded observation/translation rules. Malformed external representations do not become facts; they stop locally.

### 5. JSON observation import validates before constructing observations

`JsonObservationSource.collect()` requires a top-level object containing an `observations` array. Each entry must be an object with non-empty string `subject` and `predicate`, valid metadata shape, datetime fields, id, confidence, and `Observation(...)` construction. The implementation fails the ingest when an entry is malformed rather than partially promoting ambiguous JSON.

This is a strong counter to Model A: JSON syntax is not enough for repository attachment. Provider-specific observation shape must be validated before observations exist.

### 6. Repository-source observation extracts bounded relationships

`RepositorySourceObservationSource` scans allowlisted Python roots, reads Python source text, extracts import/definition relationship facts, and emits observations with source path, evidence, relationship family, and repository root metadata. It does not treat arbitrary source text as repository truth; only extracted relationship facts become observations.

This supports attachment without complete source understanding: the source representation can be observed for imports/definitions while leaving runtime behavior, ownership, reachability, and purpose unproven.

### 7. Operator prose is preserved as prose and oriented lexically

`Inquiry Orientation` is the clearest operator-prose evidence. It stores inquiry notes outside the event ledger, preserves raw prose, reads projected state, and never creates facts, goals, tool needs, decisions, proposals, or plans. Related material is found through deterministic lexical overlaps against projected supports and source-navigation matches. If there are no matches, the output says no deterministic related material was found and that absence does not prove unrelatedness.

The authority boundary explicitly says the note is not a fact, claim, goal, tool need, requirement, capability, decision, proposal, plan, authorization, command, or runtime instruction; lexical overlap is not semantic interpretation and does not assert importance, ownership, intent, concern, recommended action, or next safe move.

This directly answers the acceptance question: the repository can preserve candidate attachments and explicit unknowns without first understanding prose.

### 8. Observation Agreement preserves candidate agreement only

`Observation Agreement` consumes already-observed records and emits candidate agreement records only when two or more independent observation streams have exactly equal evidence text. Its boundary states that it preserves candidate agreement, provenance, and observation independence but does not promote agreement, own grammar, recover responsibility/family, own lexicon, perform semantic interpretation, assert architectural truth, write ledgers, mutate repository/runtime, or mutate clusters.

Attachment here is not interpretation. It is a justified connection between supplied observations that remains explicitly candidate-only.

### 9. Grammar Observation observes recurring shape without promotion

`Grammar Observation` consumes only `ObservationAgreementRecord` instances and emits recurring relation-shape observations such as `term != term` only after recurrence. Its record explicitly does not carry responsibility, family, lexicon, semantic meaning, or architectural truth. Its boundary rejects grammar promotion, responsibility/family recovery, semantic interpretation, and mutation.

This is strong evidence that the repository can preserve attachment-like recurrence evidence without complete understanding.

### 10. Selection Path can preserve multiple candidates and stop at unknown

`SelectionPathAudit` carries target, selected result, candidates, selection factors, non-selected candidates, evidence, outcome, unknowns, and a read-only boundary. Unsupported targets return `selected="unknown"`, `selection_factors=["unknown"]`, all available pressure candidates, and an unknown explaining that no implementation-backed selection evidence was discovered for the target.

For supported pressure selection, it preserves candidate ranking, selection factors, non-selected candidates, and evidence. This answers the multiple-candidate question: yes, one target/surface can yield multiple candidate attachments, ranked and caveated, without promoting all candidates to truth.

## Boundary analysis

### Does every provider begin with an external representation?

Supported in the broad sense, but not as one centralized abstraction. The reviewed providers begin with external representations such as file bytes, inventory text, JSON payloads, HTTP metric responses, system command JSON, dpkg status text, Python source text, Markdown/document records, and operator prose. The implementation does not expose a universal `ExternalRepresentation` type.

### Does the repository require translation before shared ownership begins?

Yes, in the reviewed implementation paths. Translation may mean candidate file classification, provider parser acceptance, response-shape validation, exact evidence equality, syntactic relation-shape recurrence, deterministic lexical overlap, or extraction of source relationships. Shared repository responsibilities begin only after bounded transformation into an implemented record: `InputArtifact`, `Observation`, `ObservationAgreementRecord`, `GrammarObservationRecord`, `RelatedMaterial`, `SelectionPathAudit`, `PackageRecord`, or similar local shape.

### Is attachment different from interpretation?

Yes. Attachment is implementation-backed connection/provenance/support. Interpretation is repeatedly rejected where evidence is insufficient. Observation Agreement can attach equal evidence across streams while rejecting semantic interpretation. Grammar Observation can attach recurring relation shape while rejecting grammar/truth promotion. Inquiry Orientation can attach lexical overlaps while rejecting intent/ownership/action interpretation.

### Can one representation produce multiple candidate attachments?

Yes. Examples:

- Inquiry Orientation can map one note to multiple related materials from fact supports and source navigation.
- Selection Path can preserve a ranked candidate set plus non-selected alternatives.
- Prometheus representations can attach differently by metric family: `node_uname_info` can support stable identity labels, while filesystem metrics remain endpoint-scoped.
- Python source can yield multiple import/definition observations from one file.

### Can every candidate legitimately conclude unsupported/unknown/no deterministic attachment and stop?

The reviewed surfaces strongly support this for their own scopes. Examples include `InputInspector` returning `unknown_format`, Ansible raising unsupported-format/parser errors, Prometheus returning `[]` and `last_error`, systemd returning no rows for invalid JSON, dpkg skipping malformed records, Inquiry Orientation returning no deterministic related material, and Selection Path returning `selected="unknown"` for unsupported targets.

This is not architectural failure; it is implemented behavior.

### Does attachment require semantic understanding?

No. The repository supports bounded attachment through exact equality, parser shape, lexical overlap, allowlisted extraction, and provenance. Semantic understanding is explicitly rejected by Observation Agreement, Grammar Observation, and Inquiry Orientation boundaries.

### Is attachment already distributed across provider responsibilities?

Yes. It is distributed, not centralized. Provider Language Translation, Repository Observation, Observation Agreement, Grammar Observation, Inquiry Orientation, Selection Path, JSON import, systemd/dpkg adapters, Prometheus translation, and Ansible inventory intake each own local portions of the boundary.

## Comparative analysis

### Model A: External representation -> Interpretation -> Repository truth

Model A is weakly supported to unsupported. The implementation repeatedly avoids direct promotion:

- file bytes become an `InputArtifact`, not truth;
- JSON must validate into observation shape;
- Prometheus query/response shape must be allowlisted and vector-shaped;
- operator prose is explicitly not a fact/goal/plan/command;
- observation agreement is candidate-only;
- grammar observation is recurrence-only;
- selection targets can remain unknown.

### Model B: External representation -> Candidate attachments -> Repository-supported attachment -> Shared responsibilities

Model B is strongly supported. It explains the recurring pattern across providers:

1. preserve external representation evidence or bounded candidate shape;
2. apply provider-local or responsibility-local validation;
3. emit local observations/candidate records only when support exists;
4. preserve provenance, caveats, unknowns, and non-promotion boundaries;
5. stop when support is insufficient.

## Counterexamples reviewed

### Immediate promotion without bounded attachment

No strong implementation counterexample was found in the reviewed paths. Some functions eventually construct `Observation(...)` records, but only after bounded extraction or validation. JSON import might look like direct promotion because it accepts user-supplied subject/predicate/value, but it still requires a provider contract: top-level object, `observations` array, entry object, required fields, metadata shape, datetime parsing, id validity, confidence/model validation, and all-entry validation before return.

### Attachment already owned by existing responsibilities

Yes. This is a counterexample to naming a new central responsibility. Attachment-like work is already distributed across existing responsibilities:

- Provider Language Translation owns provider-local parsing/validation.
- Repository Observation owns bounded source relationship extraction.
- Observation Agreement owns candidate equality across independent observation streams.
- Grammar Observation owns recurrence shape observation.
- Inquiry Orientation owns preserved prose plus lexical related-material orientation.
- Selection Path owns candidate ordering, non-selected alternatives, and unsupported-target unknowns.

Therefore the stable boundary exists, but a new named owner would be unsupported by current implementation evidence.

### Complete semantic understanding required before observation

No implementation requirement for complete semantic understanding was found. The opposite is repeatedly implemented: exact equality, lexical overlap, parser shape, allowlisted metrics, and bounded extraction are sufficient for local attachment; unsupported semantics remain unknown.

## Supported conclusions

1. **The repository distinguishes External Representation from Repository Attachment.** Supported strongly as a recurring boundary, not as a centralized type.
2. **Translation/validation precedes shared repository responsibilities.** Supported across file, Ansible, Prometheus, systemd, dpkg, JSON, Python source, operator-prose, agreement, grammar, and selection surfaces.
3. **Attachment can stop at Unknown, Unsupported, or No deterministic attachment.** Supported by implemented warnings, errors, empty results, unknown fields, and no-match uncertainty.
4. **One representation can produce multiple candidate attachments.** Supported by Inquiry Orientation related materials, Selection Path candidates/non-selected alternatives, source relationship extraction, and metric-family-specific attachment consequences.
5. **Attachment does not require semantic understanding.** Supported by explicit non-semantic boundaries and deterministic syntactic/lexical/provider-shape rules.
6. **Attachment is distributed across existing responsibilities.** Supported strongly; no universal attachment subsystem is implemented.
7. **The boundary is stable and recurring enough to recover as an architectural pattern.** Supported, if phrased as a recurring boundary/pattern rather than as a new responsibility requiring implementation changes.

## Unsupported conclusions

- A universal `RepositoryAttachment` object exists today. Unsupported.
- A centralized attachment engine exists today. Unsupported.
- Operator prose is the primary or privileged provider. Unsupported; it is one provider among many.
- The repository understands external representations semantically before observation. Rejected by implementation evidence.
- Unsupported candidates should be promoted into truth after repeated appearance. Unsupported; recurrence may create candidate agreement or grammar shape, but current boundaries reject architectural truth promotion.
- A new prose engine, semantic parser, language model, universal interpreter, or AI understanding subsystem is implied. Explicitly unsupported and not recommended.

## Confidence

High confidence that the repository already demonstrates a recurring boundary between external representation and repository-supported attachment.

Medium confidence on exact terminology, because `Repository Attachment` is not itself an implemented central object or public surface. The implementation earns the boundary, not the new owner name.

Final answer to the acceptance question:

When the repository encounters an external representation, it does **not** have to first fully understand the representation. It can constitutionally preserve candidate attachments, explicit unknowns, unsupported states, no deterministic attachment, provenance, and justified stopping until sufficient repository evidence exists. That boundary recurs across providers and responsibilities, but it is currently distributed across existing implementation surfaces rather than owned by a single architectural subsystem.
