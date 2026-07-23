# 04 Toolkit System


This is historical/mixed toolkit-system design testimony, not an active operation registry, executor, generated-toolkit lifecycle, or handoff architecture. Current implementation standing for toolkit/capability families remains unresolved unless separately evidenced by code.
A toolkit is a portable package of generated or hand-written observation, catalog, capability, operation, provider, and handoff metadata. In the current core path it is not an internal execution plugin. Use the canonical capability/operation vocabulary in `02-domain-model.md`: capabilities explain why Seed needs an ability, operations define what can be called, implementations define how calls are fulfilled, and providers are the external backends.

## Definition

A toolkit contains:

- manifest
- capability metadata
- named operations / callable interfaces
- input schemas
- output schemas
- policy action definitions
- observation sources and normalizers
- provider and handoff metadata
- predicate and relationship definitions when observations create knowledge
- optional read-only or metadata-only implementation code
- tests
- docs
- examples
- validation metadata

A toolkit is not just a Python file. The contract is as important as the implementation, and a provider name such as Prometheus or SSH should not be collapsed into a single tool. Providers expose implementations; operations are the callable surfaces that Seed may register and policy-check. Capability metadata can describe or suggest operations, but only `ToolRegistry` exposure plus `ToolExecutor` dispatch makes a registered operation executable in Seed.

## Directory layout

```text
toolkits/
  core/
    docker_observability/
      toolkit.yaml
      operations.py
      schemas/
        docker_storage_summary.input.json
        docker_storage_summary.output.json
      tests/
        test_docker_storage_summary.py
      docs.md
  generated/
    ssh_access/
      toolkit.yaml
      operations.py
      schemas/
      tests/
      docs.md
      validation_report.json
```

## Toolkit manifest

Current-core manifests attach `capabilities: [...]` to each operation, observation source, or handoff provider as per-tool operation metadata. Do not model a top-level `capabilities:` list as the current executable surface; top-level capability catalogs, when present in historical artifacts, are non-executable catalog metadata only.

Example `toolkit.yaml`:

```yaml
id: ssh_access
name: SSH Access Toolkit
version: 0.1.0
origin: generated
status: candidate
summary: Observation and handoff metadata for SSH access on Linux hosts.

generated_by:
  builder: seed-builder
  builder_version: 0.1.0
  tool_need_id: need_install_ssh_server

policy_actions:
  - name: ssh.verify
    risk: L1
    effect: read_only
    approval_required: false
    summary: Verify SSH service state and reachability.
  - name: ssh.install
    risk: L3
    effect: external_handoff
    approval_required: true
    summary: Prepare a non-executable handoff to install and start SSH server through an external provider.

observation_sources:
  - name: observe_ssh_access
    summary: Observe whether SSH daemon appears installed, running, and reachable from reported provider evidence.
    capabilities: [ssh_access]
    implementation: observation_sources:observe_ssh_access
    input_schema: schemas/observe_ssh_access.input.json
    output_schema: schemas/observe_ssh_access.output.json
    policy_action: ssh.verify
    visibility: model_visible
    examples:
      - input: {host: example_host}
        output: {reachable: true, service_running: true}

handoff_providers:
  - name: install_ssh_server
    summary: Prepare a non-executable external-provider handoff to install and start OpenSSH server on a Linux host.
    capabilities: [ssh_access]
    backend_types: [ansible, manual]
    target_schema: schemas/install_ssh_server.target.json
    policy_action: ssh.install
    executable: false
    visibility: handoff_only
    examples:
      - target: {host: example_host}
        output: {executable: false, provider: awx, operation: install_ssh_server}
```

## Handoff target schema example

`schemas/install_ssh_server.target.json`:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["host"],
  "properties": {
    "host": {
      "type": "string",
      "description": "Known host entity name or ID."
    },
    "provider": {
      "type": "string",
      "description": "External provider or runbook target; Seed does not execute it."
    }
  }
}
```

`handoff_providers.json` excerpt:

```json
{
  "providers": [
    {
      "name": "install_ssh_server",
      "backend_type": "ansible",
      "operation": "awx:install-ssh-server",
      "target_schema": "schemas/install_ssh_server.target.json",
      "policy_action": "ssh.install",
      "secret_boundary": "Credentials, become prompts, retries, and job lifecycle stay in AWX/Vault/ssh-agent; Seed stores no secrets.",
      "requires_external_approval": true,
      "executable": false
    }
  ]
}
```

## Integration implementation shape

Observation implementations should be small read-only adapters that emit observations for ingestion. Handoff implementations should emit metadata for a non-executable `HandoffPlan`; they should not call providers directly.

```python
def observe_ssh_access(ctx: IntegrationContext, host: str) -> list[Observation]:
    """Convert externally reported SSH status into observations."""
    host_ref = ctx.entities.require("host", host)
    provider_report = ctx.inputs.require_report()
    return ctx.observations.from_provider_report(host_ref, provider_report)
```

Generated integrations should receive a constrained context rather than importing the whole runtime.

## IntegrationContext

The runtime passes a constrained context object to read-only integration code. It deliberately excludes secret access and execution providers.

```python
@dataclass
class IntegrationContext:
    workspace_id: str
    integration_name: str
    entities: EntityAccessor
    facts: FactAccessor
    inputs: InputAccessor
    observations: ObservationWriter
    artifacts: ArtifactWriter
    logger: IntegrationLogger
```

IntegrationContext limits what generated code can access.

## Lifecycle

```text
candidate generated
  -> manifest validated
  -> schemas validated
  -> static checks passed
  -> tests passed
  -> sandbox dry run passed
  -> policy reviewed
  -> registered
  -> visible to model
```

## Toolkit status values

- `candidate` — generated but untrusted
- `validation_failed` — failed validation
- `validated` — passed automated checks
- `awaiting_review` — needs human review
- `registered` — available to runtime registry
- `disabled` — installed but not usable
- `deprecated` — retained for old events but hidden from new context

## Generated versus core toolkits

Core toolkits are hand-written and reviewed. Generated toolkits follow the same manifest format.

Runtime should not care whether a toolkit is generated or core after registration. It should only care about status, schema, policy, catalog entries, observation contracts, and handoff metadata.

## Toolkit loading

```python
def load_toolkits(paths: list[Path]) -> Registry:
    registry = Registry()
    for path in paths:
        manifest = parse_manifest(path / "toolkit.yaml")
        validation = validate_manifest(manifest)
        if not validation.ok:
            continue
        if manifest.status != "registered":
            continue
        registry.add_toolkit(manifest, base_path=path)
    return registry
```

## Context visibility

Not every registered operation should be shown to every model call.

Visibility depends on:

- workspace
- active goal
- entity kind
- policy
- risk
- user role
- environment
- operation maturity
- whether arguments are known

Example context entry:

```json
{
  "name": "install_ssh_server",
  "summary": "Prepare a non-executable handoff to install and start OpenSSH server on a Linux host.",
  "target_schema_summary": "requires host; optional external provider reference",
  "policy": {
    "action": "ssh.install",
    "risk": "L3",
    "requires_approval": true
  },
  "visibility_reason": "Relevant to current goal but Seed can only produce a handoff boundary; execution, credentials, retries, and scheduling stay external."
}
```

## Initial integration-artifact generation scope

Toolkit generation initially targets non-mutating integration artifacts:

- `InputInspector` implementations when file-backed inputs need content-based dispatch
- `ObservationSource` adapters
- `ObservationNormalizer` implementations
- PredicateCatalog entries
- RelationshipCatalog entries
- CapabilityCatalog entries
- HandoffProvider metadata
- tests

These artifacts may collect, normalize, describe, and validate integrations. Execution remains external to Seed.

`AnsibleInventoryObservationSource` is the reference example for a toolkit-generated integration in this scope. Its raw file input is inspected before parser dispatch, so extensions are hints rather than parser authority. It only parses local static inventory files and emits ordinary observations. It does not SSH, invoke Ansible, validate inventory hosts, resolve identities internally, or mutate runtime state. Its inventory hostname, IP, alias, and group observations flow through the same `ObservationNormalizer` and ingestion pipeline as every other source.

## Toolkit generation output contract

A builder must output:

```text
candidate_dir/
  toolkit.yaml
  input_inspectors/          # optional
  observation_sources/
  observation_normalizers/
  catalogs/predicates.json
  catalogs/relationships.json
  catalogs/capabilities.json
  handoff_providers.json
  schemas/*.json
  tests/test_*.py
  docs.md
  generation_notes.md
```

Optional:

```text
  rollback.md
  provider_prerequisites.md
  examples/*.json
```

## Registration event

When a toolkit is registered, append an event:

```json
{
  "kind": "toolkit.registered",
  "payload": {
    "toolkit_id": "ssh_access",
    "version": "0.1.0",
    "observation_sources": ["observe_ssh_access"],
      "handoff_providers": ["install_ssh_server"],
    "source_candidate_id": "cand_...",
    "validation_report_id": "val_..."
  }
}
```

## Versioning

Operation names should be stable. Toolkit versions can change.

Rules:

- breaking schema change requires new major version
- old events reference exact toolkit version
- deprecated operations remain resolvable for audit
- model context shows only current visible versions

## Safety constraints for generated toolkits

Generated toolkit code should not:

- import arbitrary runtime internals
- read environment variables directly
- open network sockets directly unless declared
- access filesystem outside sandbox/artifact paths
- spawn subprocesses directly
- execute host commands or mutate hosts
- manage secrets directly
- change registry or policy directly
- self-register

Use provider facades and ToolContext.
