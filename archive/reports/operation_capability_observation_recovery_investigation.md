# Operation capability observation recovery investigation

## Scope and method

This is a recovery report only. It does not propose a new runtime, automatic tool generation, plugin framework, operation synthesis, dynamic execution system, agent framework, or new registry. The question is whether the current implementation already makes operational capability observable before it is registered or executed.

Commands used during this investigation:

```bash
pwd && rg --files -g 'AGENTS.md' -g '*.md' | head -100
cat AGENTS.md && rg --files | rg 'capability|tool|observation|execution|manual|provider' | head -200
sed -n '1,220p' seed_runtime/capability_catalog.py; sed -n '1,220p' seed_runtime/capability_inventory.py; sed -n '1,220p' seed_runtime/tool_needs.py; sed -n '1,220p' seed_runtime/execution.py
sed -n '220,520p' seed_runtime/execution.py; sed -n '1,240p' seed_runtime/registry.py; sed -n '1,220p' seed_runtime/toolkit_loader.py 2>/dev/null || true; rg "class ToolRegistry|register|ToolSpec|CapabilityCatalog|Provider" seed_runtime toolkits tests -n | head -200
sed -n '1,260p' seed_runtime/toolkit_registration.py 2>/dev/null; sed -n '1,260p' seed_runtime/capability_candidates.py; sed -n '1,260p' seed_runtime/capability_verification.py; sed -n '1,220p' seed_runtime/observation_sources.py
rg "class .*ObservationSource|executable|manual|provider|binary|which|shutil|tool.registered|ToolkitRegistration" -n seed_runtime toolkits tests docs | head -300
sed -n '1,240p' seed_builder/registration.py; sed -n '1,260p' seed_builder/generator.py; sed -n '1,220p' seed_runtime/verification_evidence.py; sed -n '1,120p' tests/test_verification_evidence.py
for f in implementation_execution_grammar_recovery_investigation.md tool_vocabulary_orientation_recovery_investigation.md docs/execution_concepts_implementation_investigation.md docs/observation_execution_transition_investigation.md docs/current_implementation_audit_execution_observation_projection_cache_capability.md docs/capability_operation_execution_reconciliation.md docs/tool_execution_ownership_audit.md docs/tool_vocabulary_reconciliation.md; do [ -f "$f" ] && echo '---' $f && sed -n '1,80p' "$f"; done
```

Primary implementation evidence reviewed:

- `seed_runtime/observation_sources.py`
- `seed_runtime/capability_candidates.py`
- `seed_runtime/verification_evidence.py`
- `seed_runtime/capability_verification.py`
- `seed_runtime/capability_inventory.py`
- `seed_runtime/capability_catalog.py`
- `seed_runtime/tool_needs.py`
- `seed_runtime/registry.py`
- `seed_runtime/execution.py`
- `seed_builder/generator.py`
- `seed_builder/registration.py`
- `tests/test_verification_evidence.py`
- prior execution/tool-vocabulary/capability reconciliation reports listed in the prompt

## Executive answer

Operational capability enters the repository through more than one path. The strongest current paths are:

```text
manual/static capability metadata
  -> CapabilityCatalog YAML entries
  -> provider/handoff recommendations
  -> no operation registration and no execution

validated toolkit artifact
  -> load toolkit manifest
  -> ToolRegistry.register_toolkit
  -> tool.registered event
  -> ToolExecutor may execute the registered implementation after validation and policy

projected observation evidence
  -> package_installed fact
  -> capability candidate
  -> local PATH binary evidence
  -> verification inspection
  -> still no registration, selection, permission, policy approval, or execution
```

Therefore the implementation **partially supports** an observation-first operational architecture, but only up to candidate and verification-evidence inspection. Current executable operations are still manually or builder-registered from reviewed toolkit manifests. The repository already contains pieces for `observe evidence -> recover capability candidate -> inspect verification evidence`, and separately contains pieces for `registered operation -> bounded execution`. It does **not** currently contain an implementation-backed transition that promotes observed executable/manual/provider evidence into a registered `ToolSpec` operation contract.

The answer to whether `tool` is currently a promoted artifact rather than an observed one is: **yes for executable `ToolSpec`/`ToolRegistry` entries**. Registered tools are promotion/registration artifacts loaded from manifests or emitted as `tool.registered` events. Observed binaries and packages are preserved as evidence or candidates, not promoted into registered tools.

## 1. Where operational capability currently enters

| Entry path | Implementation owner | What enters | Observation-backed? | Registered operation? | Evidence |
| --- | --- | --- | ---: | ---: | --- |
| Static capability catalog | `CapabilityCatalog.load()` | Capability-to-provider/handoff metadata from `capability_catalog/*.yml` | No, manually maintained files | No | Loader reads sorted YAML files and constructs `CapabilityCatalogEntry`/`CapabilityRecommendation`; class says it is read-only metadata and does not execute tools. |
| Runtime missing capability request | `ToolNeedService.create_from_decision()` | A normalized `ToolNeed` with capability, summary, desired IO, risk hint | Indirectly from a runtime decision, not observation evidence | No | Service appends `tool_need.created`; `resolve_capability()` is read-only and returns catalog, provider, handoff, and registry candidates. |
| Toolkit manifest registration | `ToolRegistry.load_manifest()` / `register_toolkit()` and `ToolkitRegistrationService.register()` | `ToolSpec` registered operations | No direct observation requirement; validation report plus manifest | Yes | Registry stores manifest `tools`; registration service loads `toolkit.yaml`, registers toolkit, then appends `tool.registered`. |
| Generated candidate artifact | `ToolkitGenerator.generate()` | Untrusted candidate manifest, operation stub, tests, docs | Derived from a `ToolNeed`, not observation of an executable/manual | Not until validated and registered | Generator writes manifest with implementation string and stubs, with notes to validate before registration. |
| Projected package evidence | `build_capability_candidates()` | Capability candidates such as `ssh_client`, `python_runtime`, `docker_client` | Yes, from projected `package_installed` facts | No | Candidate module explicitly says a candidate is not capability proof, permission, decision, policy, or tool invocation. |
| PATH executable evidence | `build_verification_evidence()` | Verification evidence such as `binary_path_observed` | Yes, filesystem metadata inspection only | No | Function checks executable files in PATH, never invokes them, and never promotes evidence into `capability_verified` facts. |
| Existing verification facts | `build_capability_inventory()` / `build_capability_verification_inspection()` | Verification state derived from projected `capability_verified` facts | Yes if facts have observed support; can include provider-reported facts | No by itself | Inventory derives states from projected facts; candidate verification joins candidate universe to capability inventory and remains read-only. |

## 2. Observation -> capability -> registered operation: supported or bypassed?

The current implementation supports this sequence only through the **capability-candidate inspection boundary**:

```text
fact.observed(package_installed)
  -> projected Fact
  -> build_capability_candidates
  -> CapabilityCandidate
  -> build_verification_evidence checks PATH binary metadata
  -> build_capability_verification_inspection reports unverified/verified status
```

It does not support this full executable-registration sequence:

```text
observed executable/manual/provider metadata
  -> recovered operation contract
  -> ToolSpec
  -> ToolRegistry registration
  -> ToolExecutor execution
```

The registration path currently bypasses observation in the sense that `ToolRegistry.register_toolkit()` accepts an already-formed `Toolkit`/manifest, and `ToolkitRegistrationService.register()` accepts a validated artifact path and validation report. Neither implementation requires an observation source, package fact, PATH binary evidence, manual text, provider metadata observation, or capability candidate before registering.

## 3. What binaries, manuals, provider metadata, and contracts expose today

### Binaries

Binaries are observable as metadata only. `build_verification_evidence()` maps known capability candidates to repository-known binary names (`ssh`, `python3`, `docker`, `git`, `curl`), checks whether those names are executable files on PATH, records `binary_path_observed`, and marks support notes including `filesystem_metadata_only` and `binary_not_invoked`. This is sufficient to recover **verification evidence**, not a registered operation contract.

### Manuals and documentation

There is checked-in evidence that manual/help text may be relevant to capability-shape investigation, but current runtime code reviewed here does not parse manuals into `ToolSpec` contracts. Generated toolkit artifacts can include `docs.md`, and catalog recommendations can include summaries, but those are manual/static descriptions rather than observed manuals converted into operations.

### Provider metadata

Provider metadata currently enters through `CapabilityCatalog` recommendations and through provider-reported `capability_verified` facts. Catalog metadata can include provider, backend type, and operation text, but `ToolNeedService.resolve_capability()` treats those as provider recommendations or handoff candidates. Tests and invariants assert recommendation metadata does not become a registered operation merely because it has an operation string.

### Implementation contracts

Toolkit manifests expose enough implementation contract information for registration: name, summary, input schema, output schema, policy action, implementation import path, risk, visibility, and capabilities. This is the strongest existing operation-contract format. It is not recovered from binary/manual observation; it is declared in a manifest and loaded into `ToolSpec`.

## 4. Observed, derived, registered, and promoted concepts

| Concept | Classification | Owner | Boundary |
| --- | --- | --- | --- |
| `Observation` from source adapters | Observed | `ObservationSource` implementations and `ObservationCollectionService` | Source adapters collect observations; ingestion/projection are separate. |
| `Fact` / `FactSupport` in projected state | Promoted from events/evidence into projection | `ObservationIngestor`, `StateProjector`, fact support aggregation | Facts can support inventory and verification; they are not executable authority. |
| `package_installed` | Observed/projected | Local package observation and fact projection | Used as evidence for candidates, not proof of permission or operation. |
| `CapabilityCandidate` | Derived | `build_capability_candidates()` | Preserves possible capability from package facts only; explicitly not capability proof or execution authority. |
| `VerificationEvidence` | Observed support evidence | `build_verification_evidence()` | PATH metadata only; not verification, permission, selection, or invocation. |
| `CapabilityInventoryEntry` | Derived read model | `build_capability_inventory()` | Derived from projected tools, needs, and `capability_verified` facts. |
| `CapabilityCatalogEntry` / `CapabilityRecommendation` | Manual/static metadata | `CapabilityCatalog` | Provider/handoff suggestions; read-only and non-executing. |
| `ToolNeed` | Registered/recorded capability gap | `ToolNeedService` and event ledger | Runtime need record; not executable operation. |
| `ToolSpec` | Registered operation contract | Toolkit manifest loader and `ToolRegistry` | Callable operation metadata; can be executed only through validation/policy path. |
| `ToolRegistry` entry | Registered/promoted operation artifact | `ToolRegistry` / `ToolkitRegistrationService` | Model-visible/registered operation catalog; not observation source. |
| `ToolExecutor` invocation | Bounded execution | `ToolExecutor` | Requires registered spec, validation, policy, and importable implementation. |

## 5. Manual registration boundaries and counterexamples

Manual registration is clearly the current architectural owner for executable operation contracts when the operation is a Seed toolkit operation. The manifest loader requires explicit schema and implementation metadata. The executor imports the implementation string from the registered spec and validates output against the registered schema. Observation of a binary path cannot provide those Seed-specific boundaries by itself.

Counterexamples to a universal observation-first model:

- `CapabilityCatalog` is intentionally static/read-only provider metadata. It can recommend providers or handoffs without observing a local executable.
- `ToolRegistry.register_toolkit()` registers already-declared tools from a toolkit manifest; it is not a discovery mechanism.
- `ToolkitRegistrationService.register()` depends on a validation report and artifact path, not observation facts.
- `ToolExecutor.execute()` requires a registered operation and policy result before invocation; it is not a capability discovery path.
- Provider recommendation `operation` strings are handoff metadata unless separately represented as a registered `ToolSpec`.

These counterexamples do not reject observation-first inquiry. They reject the stronger unsupported claim that current executable operations are recovered from observation.

## 6. Recurring implementation that infers capability from observed evidence

The recurring pattern that does exist is conservative:

1. Preserve observed evidence as facts or observations.
2. Derive candidates from recurring evidence (`package_installed` -> candidate labels).
3. Acquire additional read-only verification evidence (`PATH` executable metadata).
4. Keep verification, permission, selection, policy, and execution separate.

The capability-candidate and verification-evidence modules repeat the same boundary vocabulary: candidate evidence is not capability proof, binary evidence is not permission, and neither path selects, evaluates policy, invokes tools, plans, or writes the ledger during inspection.

This is observation-first, but it is not operation-registration-first. The implementation recovers **candidate capability evidence** from observation; it does not recover **registered operation contracts** from observation.

## 7. Does the repository already support the proposed architecture pieces?

For the shape:

```text
observe executable
↓
observe supporting manual or implementation description
↓
recover capability
↓
promote operation contract
↓
execute bounded operation
```

Current support is split:

| Step | Current support | Implementation-backed conclusion |
| --- | --- | --- |
| Observe executable | Partial | PATH executable metadata can be observed for known candidates without invoking binaries. |
| Observe supporting manual or implementation description | Weak/manual only | Docs and manifest summaries exist; no reviewed code recovers operation contracts from observed manuals/help text. |
| Recover capability | Partial | Candidates are derived from package facts and supported by binary evidence; verification status derives from `capability_verified` facts. |
| Promote operation contract | Manual/registration only | `ToolSpec` is promoted from toolkit manifests through registration, not from observed evidence. |
| Execute bounded operation | Supported for registered tools | `ToolExecutor` executes only registered specs after validation and policy. |

So the repository already contains important architectural pieces, but the current implementation does not connect them into automatic observation-to-operation promotion. That unsupported connection should not be claimed as existing behavior.

## 8. Supported conclusions

- Operational capability currently originates from both manual/static metadata and observation-derived evidence, depending on the concept.
- Executable operations originate from registered toolkit manifests and `tool.registered` events, not from observed binaries or manuals.
- Capability candidates can be recovered from observed projected package facts.
- Verification evidence can be recovered from observed PATH executable metadata without invoking binaries.
- Capability verification state is derived from projected `capability_verified` facts and fact support, not from candidate evidence alone.
- Provider/handoff recommendations are catalog metadata; they do not register or execute operations.
- Current implementation already preserves the boundary between observation, candidate derivation, verification evidence, registration, policy, and execution.
- The tool vocabulary hides this separation because registered operations, missing capability needs, recommendations, and execution all share `tool` names in some APIs/events.

## 9. Unsupported conclusions

- Unsupported: Seed currently recovers `ToolSpec` contracts from observed binaries.
- Unsupported: Seed currently parses manuals/help text into operation schemas.
- Unsupported: provider metadata with an `operation` string is a registered operation.
- Unsupported: capability candidates are verified capabilities.
- Unsupported: observed binary presence grants permission, policy approval, operation selection, or execution authority.
- Unsupported: `ToolExecutor` owns capability discovery or registration.
- Unsupported: registration currently requires observation evidence.
- Unsupported: the repository has a complete implementation-backed `observe executable -> recover operation contract -> execute` pipeline.

## 10. Recommended next investigation

The next recovery-only investigation should inspect **operation contract provenance**:

```text
For each current ToolSpec, where did its contract come from?
```

That investigation should trace checked-in toolkit manifests, generated toolkit artifacts, validation reports, `tool.registered` events, tests, and any documentation/manifests that act as authority for input/output schemas and policy actions. The goal would not be to design automatic operation synthesis, but to distinguish which registered operation contracts are hand-authored, generated stubs, validated candidates, or projected ledger artifacts.
