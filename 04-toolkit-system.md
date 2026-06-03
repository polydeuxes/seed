# 04 Toolkit System

A toolkit is a portable package of generated or hand-written operational capability.

## Definition

A toolkit contains:

- manifest
- tools
- capability definitions
- policy action definitions
- input schemas
- output schemas
- implementation code
- tests
- docs
- examples
- validation metadata

A toolkit is not just a Python file. The contract is as important as the implementation.

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

Example `toolkit.yaml`:

```yaml
id: ssh_access
name: SSH Access Toolkit
version: 0.1.0
origin: generated
status: candidate
summary: Tools for verifying and managing SSH access on Linux hosts.

generated_by:
  builder: seed-builder
  builder_version: 0.1.0
  tool_need_id: need_install_ssh_server

capabilities:
  - name: ssh_access
    summary: Host accepts SSH login with approved credentials.
    entity_kinds: [host]
    verification_tool: verify_ssh_access

policy_actions:
  - name: ssh.verify
    risk: L1
    effect: read_only
    approval_required: false
    summary: Verify SSH service state and reachability.
  - name: ssh.install
    risk: L3
    effect: mutating
    approval_required: true
    summary: Install and start SSH server.

tools:
  - name: verify_ssh_access
    summary: Verify SSH daemon is installed, running, and reachable.
    implementation: operations:verify_ssh_access
    input_schema: schemas/verify_ssh_access.input.json
    output_schema: schemas/verify_ssh_access.output.json
    policy_action: ssh.verify
    visibility: model_visible
    examples:
      - input: {host: node-1}
        output: {reachable: true, service_running: true}

  - name: install_ssh_server
    summary: Install and start OpenSSH server on a Linux host.
    implementation: operations:install_ssh_server
    input_schema: schemas/install_ssh_server.input.json
    output_schema: schemas/install_ssh_server.output.json
    policy_action: ssh.install
    visibility: approval_required
    examples:
      - input: {host: node-1, package_manager: apt}
        output: {installed: true, service_running: true}
```

## Tool schema example

`schemas/install_ssh_server.input.json`:

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
    "package_manager": {
      "type": "string",
      "enum": ["apt", "dnf", "yum", "apk", "auto"],
      "default": "auto"
    },
    "start_service": {
      "type": "boolean",
      "default": true
    }
  }
}
```

`schemas/install_ssh_server.output.json`:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["ok", "host", "installed", "service_running", "summary"],
  "properties": {
    "ok": {"type": "boolean"},
    "host": {"type": "string"},
    "installed": {"type": "boolean"},
    "service_running": {"type": "boolean"},
    "changed": {"type": "boolean"},
    "summary": {"type": "string"},
    "evidence": {
      "type": "object",
      "additionalProperties": true
    }
  }
}
```

## Operation implementation shape

Operations should be small adapters around provider primitives.

```python
def verify_ssh_access(ctx: ToolContext, host: str) -> dict:
    """Verify SSH service status and port reachability."""
    host_ref = ctx.entities.require("host", host)
    result = ctx.providers.ssh.check(host_ref)
    return {
        "ok": result.reachable and result.service_running,
        "host": host_ref.name,
        "reachable": result.reachable,
        "service_running": result.service_running,
        "summary": result.summary,
        "evidence": result.evidence,
    }
```

Generated operations should receive a `ToolContext` rather than importing the whole runtime.

## ToolContext

The runtime passes a constrained context object to tools.

```python
@dataclass
class ToolContext:
    workspace_id: str
    tool_name: str
    call_id: str
    entities: EntityAccessor
    facts: FactAccessor
    providers: ProviderFacade
    secrets: SecretAccessor
    artifacts: ArtifactWriter
    logger: ToolLogger
```

ToolContext limits what tool code can access.

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

Runtime should not care whether a toolkit is generated or core after registration. It should only care about status, schema, policy, and implementation reference.

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

Not every registered tool should be shown to every model call.

Visibility depends on:

- workspace
- active goal
- entity kind
- policy
- risk
- user role
- environment
- tool maturity
- whether arguments are known

Example context entry:

```json
{
  "name": "install_ssh_server",
  "summary": "Install and start OpenSSH server on a Linux host.",
  "input_schema_summary": "requires host; optional package_manager",
  "policy": {
    "action": "ssh.install",
    "risk": "L3",
    "requires_approval": true
  },
  "visibility_reason": "Relevant to current goal but cannot execute without approval."
}
```

## Initial integration-artifact generation scope

Toolkit generation initially targets non-mutating integration artifacts:

- `InputInspector` implementations when file-backed inputs need content-based dispatch
- `ObservationSource` adapters
- `ObservationNormalizer` implementations
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
  operations.py
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
    "tools": ["verify_ssh_access", "install_ssh_server"],
    "source_candidate_id": "cand_...",
    "validation_report_id": "val_..."
  }
}
```

## Versioning

Tool names should be stable. Toolkit versions can change.

Rules:

- breaking schema change requires new major version
- old events reference exact toolkit version
- deprecated tools remain resolvable for audit
- model context shows only current visible versions

## Safety constraints for generated toolkits

Generated toolkit code should not:

- import arbitrary runtime internals
- read environment variables directly
- open network sockets directly unless declared
- access filesystem outside sandbox/artifact paths
- spawn subprocesses directly unless provider allows it
- manage secrets directly
- change registry or policy directly
- self-register

Use provider facades and ToolContext.
