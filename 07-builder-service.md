# 07 Builder Service

The builder service turns ToolNeeds / capability gaps into generated toolkit candidates for observation, catalog, operation-contract, and handoff integration. Use the canonical capability/operation/implementation/provider/toolkit vocabulary in `02-domain-model.md`.

## Builder mission

Given a durable ToolNeed / capability gap, produce a toolkit candidate that can be validated and eventually registered.

The builder is not the runtime. It does not execute production actions, handle secrets, schedule jobs, retry work, or create a Seed-owned execution lifecycle. It creates artifacts.

## Builder inputs

```json
{
  "tool_need": {
    "name": "install_ssh_server",
    "capability": "ssh_access",
    "summary": "Install and start OpenSSH server on a Linux host.",
    "risk_hint": "mutating",
    "desired_inputs": ["host"],
    "desired_outputs": ["installed", "service_running", "summary"]
  },
  "workspace_constraints": {
    "allowed_providers": ["linux_package_provider", "service_provider"],
    "forbidden_effects": ["credential_creation"],
    "target_os_families": ["debian", "rhel"]
  },
  "existing_registry_summary": {
    "related_operations": ["verify_ssh_access"],
    "related_capabilities": ["ssh_access"]
  }
}
```

## Builder outputs

```text
candidate_dir/
  toolkit.yaml
  input_inspectors/        # only when a raw input class needs pre-dispatch inspection
  observation_sources/
  observation_normalizers/
  catalogs/
    predicates.json
    relationships.json
    capabilities.json
  handoff_providers.json
  schemas/
  tests/
  docs.md
  generation_notes.md
```


The first generated artifacts should be non-mutating integration products:

- `InputInspector` when needed
- `ObservationSource`
- `ObservationNormalizer`
- `PredicateCatalog` entries
- `RelationshipCatalog` entries
- `CapabilityCatalog` entries
- `HandoffProvider` metadata
- tests

Generated operation code, if any, must remain read-only or metadata-only unless an external provider owns the real execution path. Mutating work is represented as non-executable HandoffPlan metadata.

## Builder phases

### 1. Analyze ToolNeed / capability gap

Determine:

- capability type
- read-only versus mutating
- required providers
- inputs
- outputs
- safety risks
- related existing operations/toolkits

### 2. Draft Toolkit Plan

Produce a human-readable plan:

```yaml
toolkit_id: ssh_access
operations:
  - verify_ssh_access
  - install_ssh_server
providers:
  - package_manager
  - service_manager
risks:
  - package installation changes host state
  - service start opens network listener
```

### 3. Generate Manifest and Schemas

Generate contracts before implementation.

### 4. Generate Integration Artifacts

Generate non-mutating integration artifacts before any operation wrapper: inspectors, observation sources, normalizers, catalog entries, handoff-provider metadata, schemas, and tests. Implementation should not use raw subprocess, direct host mutation, credential prompts, or undeclared network access.

### 5. Generate Tests

Tests should cover:

- schema validation
- success path
- provider failure
- policy metadata presence
- no direct forbidden imports

### 6. Generate Docs

Docs should explain:

- purpose
- operations and provider boundaries
- inputs/outputs
- policy implications
- rollback considerations

### 7. Run Validation

Call validator and record report.

## Builder architecture

```text
Builder API
  -> ToolNeed Loader
  -> Planning Model / Template Engine
  -> Manifest Generator
  -> Schema Generator
  -> Code Generator
  -> Test Generator
  -> Documentation Generator
  -> Validator Runner
  -> Candidate Store
```

## Builder can use model tiers

Use stronger models for code generation if needed. Runtime can still use a small model.

Suggested split:

- small runtime model: detects missing capability/operation/provider path, requests ToolNeed / capability gap
- medium builder model: creates manifest and schema
- strong code model: writes implementation and tests
- deterministic validator: accepts/rejects output

## Provider facades

Generated operation wrappers and handoff metadata should target stable provider facades.

Examples:

```python
ctx.observations.ansible_inventory.parse(path)
ctx.observations.prometheus.collect(base_url, allowlisted_metrics)
ctx.handoffs.provider("awx").operation("install_ssh_server")
```

This avoids generated artifacts shelling out arbitrarily and keeps host mutation in Ansible/AWX, MCP, Temporal/Prefect, or manual provider boundaries.

## Candidate validation checklist

- manifest parses
- IDs and names are valid
- schemas are valid JSON Schema
- every operation has policy action
- every policy action has risk classification
- implementation reference resolves inside candidate
- tests exist
- tests pass
- forbidden imports absent
- no direct secret access
- no raw subprocess
- no Seed-owned host mutation or direct execution
- no network access unless declared for a read-only observation source
- no self-registration code
- docs exist

## Builder API sketch

```http
POST /tool-needs/{id}/generate
```

Response:

```json
{
  "candidate_id": "cand_...",
  "status": "generated",
  "artifact_path": "builder_out/cand_...",
  "next": "validate"
}
```

```http
POST /toolkit-candidates/{id}/validate
```

Response:

```json
{
  "validation_report_id": "val_...",
  "ok": true,
  "status": "validated"
}
```

## Builder pseudocode

```python
def generate_toolkit(tool_need_id: str) -> ToolkitCandidate:
    need = tool_need_store.require(tool_need_id)
    existing = registry.summarize_related(need)
    constraints = workspace_policy.builder_constraints(need.workspace_id)

    plan = planner.plan(need, existing, constraints)
    manifest = manifest_generator.generate(plan)
    schemas = schema_generator.generate(plan)
    code = code_generator.generate(plan, manifest, schemas)
    tests = test_generator.generate(plan, manifest, schemas, code)
    docs = docs_generator.generate(plan, manifest)

    candidate = candidate_store.write(
        manifest=manifest,
        schemas=schemas,
        code=code,
        tests=tests,
        docs=docs,
        generation_notes=plan.notes,
    )

    ledger.append("toolkit.candidate.generated", candidate.event_payload())
    return candidate
```

## Registration pseudocode

```python
def register_candidate(candidate_id: str) -> RegistrationResult:
    candidate = candidate_store.require(candidate_id)
    validation = validator.validate(candidate)

    if not validation.ok:
        ledger.append("toolkit.validation.failed", validation.payload())
        return RegistrationResult.rejected(validation)

    policy = policy_gate.evaluate("toolkit.register", scope=candidate.id)
    if policy.requires_approval:
        approval = approvals.request(policy, candidate)
        ledger.append("toolkit.registration.approval_requested", approval.payload())
        return RegistrationResult.awaiting_approval(approval)

    registry.register(candidate)
    ledger.append("toolkit.registered", candidate.registration_payload())
    return RegistrationResult.registered(candidate)
```

## Builder does not decide final trust

Even if builder says “looks good,” runtime registry decides whether to register based on validation and policy.

## MVP builder

First version can be template-only:

- accepts ToolNeed / capability gap
- generates manifest skeleton
- generates observation source/normalizer skeletons
- generates catalog-entry skeletons
- generates HandoffProvider metadata skeletons
- generates TODO tests
- records candidate

That is still valuable because it makes the growth loop explicit.

## Advanced builder

Later versions can:

- search docs
- infer OS families
- generate provider facade requests
- create rollback tools
- generate eval cases
- compare existing toolkit overlap
- propose policy actions
- run sandbox simulations
