# Declaration Competency Interrogation

## Bounded question

```text
Declaration,

what kind of competency
are you?
```

This interrogation uses recurring implementation evidence only. It does not recover implementation, recover ownership, recommend a slice, or authorize a campaign.

## Competency identity

Declaration is the competency that makes operational claims explicit as inspectable repository objects before other surfaces rely on them.

Its constitutional work is to name a surface or candidate, attach bounded claims about its shape or authority, and preserve those claims in data structures, registries, result objects, JSON payloads, rendered output, and tests. In the reviewed evidence, Declaration does not by itself execute, mutate, promote, acquire capability, select work, evaluate policy, or establish ownership. It gives other implementation paths explicit material to inspect, compare, render, and test.

## Implementation evidence

Declaration has already appeared independently in these representative implementation families:

| Implementation family | Declaration evidence observed |
| --- | --- |
| Operational Visibility | Operational CLI surfaces are discovered from argparse declarations, then compared with diagnostic registry entries to classify registered, JSON-capable, operational visibility surfaces. |
| Diagnostic Visibility | Diagnostic inventory entries declare diagnostic names, CLI flags, projected-state use, repository-file use, JSON support, record support, record scope, diagnostic fact emission, cluster fact emission, event-ledger writes, cluster mutation, diagnostic-fact reads, and descriptions. |
| Diagnostic inventory | `DiagnosticInventoryEntry` is an explicit operational shape declaration for one diagnostic/test-like CLI surface. The registry is a tuple of such entries. |
| Diagnostic shape audit | `DiagnosticImplementationSpec` declares implementation expectations for each diagnostic name, including module path, build/format/JSON/record functions, CLI flags, JSON flags, repository-file markers, diagnostic-fact read markers, and mutation markers. The audit compares declared fields to observed implementation evidence. |
| CLI operational surfaces | `scripts/seed_local.py` declares CLI flags for diagnostic, capability, inventory, audit, and operational visibility surfaces; operational surface inventory consumes parser actions as declared public options. |
| Capability verification | Candidate verification inspection declares a read-only inspection boundary and negative boundary notes separating candidates, verification facts, selection, execution authority, execution decisions, tool invocation, permission, policy evaluation, and execution. |
| Responsibility evaluation / authority surfaces | Container, service, and listener authority diagnostics declare read-only boundaries, event-ledger behavior, mutation behavior, and diagnostic-fact usage through inventory entries, shape specs, outputs, and tests. |
| Compatibility declarations | Several tests and implementation paths preserve compatibility handoffs by proving result/lineage payloads, compatibility wrappers, response shapes, or public JSON/CLI surfaces remain unchanged. |
| Negative authority declarations | Capability verification, promotion readiness, capability relationship, and authority diagnostics declare what they do not do: no promotion, no capability-verified fact creation, no capability selection, no policy evaluation, no tool execution, no acquisition, no event-ledger write, and no cluster mutation. |

## Physiology

Observable activity of Declaration:

1. Names a thing: a diagnostic, operational CLI surface, capability candidate, verification status, boundary, record scope, JSON surface, or authority diagnostic.
2. Attaches explicit fields to the named thing: flags, booleans, scope labels, implementation paths, function names, markers, boundary strings, notes, limitations, and unknown values.
3. Preserves those fields as stable data: dataclasses, registry rows, audit rows, inspection result objects, JSON dictionaries, and rendered reports.
4. Allows comparison: diagnostic shape audit compares declared inventory fields with observed implementation markers; tests compare declarations against CLI output, JSON output, and expected boundaries.
5. Separates positive claims from negative authority: a declaration can say a surface supports JSON, writes the event ledger, or records diagnostic facts; it can also say a surface does not mutate the cluster, does not select capabilities, does not evaluate policy, and does not execute tools.
6. Leaves operational action to adjacent competencies. Declaration itself is descriptive and inspectable in the observed evidence.

## Inputs

Inputs observed entering Declaration:

- Surface identity: diagnostic names, operational surface names, CLI flags, and question/diagnostic identifiers.
- Implementation references: module paths, build functions, format functions, JSON functions, record functions, parser actions, and implementation markers.
- Boundary facts: record support, record scope, event-ledger behavior, cluster mutation behavior, diagnostic-fact reads/writes, projected-state use, repository-file use, read-only status, and JSON support.
- Evidence summaries: capability candidates, candidate support, verification support, current access, operational benefit, pressure counts, reasoning strings, known limitations, and unknown attainability/expectation values.
- Negative authority vocabulary already backed by implementation: no acquisition, no promotion, no inventory modification, no capability selection, no policy evaluation, no tool execution, no permission creation, no recording, no event-ledger writes, and no cluster mutation.

## Outputs

Outputs observed leaving Declaration:

- Registry rows such as diagnostic inventory entries.
- Implementation specs for diagnostic shape audit.
- Audit rows with declared, observed, and status fields.
- CLI visibility inventories and classifications.
- Read-only inspection objects for capability verification and promotion readiness.
- JSON dictionaries containing declared boundary and shape fields.
- Human-readable reports rendering declared boundaries, limitations, and unknowns.
- Tests that assert the declared surface appears, keeps expected scope, preserves JSON/record behavior, avoids cluster mutation, and avoids event-ledger writes when declared read-only.

## Locality

### Observed

Declaration has been observed in:

- `seed_runtime/diagnostic_inventory.py` diagnostic registry rows.
- `seed_runtime/diagnostic_shape_audit.py` implementation specs and shape-audit comparison rows.
- `seed_runtime/operational_surface_inventory.py` CLI surface discovery and classification using parser declarations and registry declarations.
- `scripts/seed_local.py` argparse CLI flags and command dispatch surfaces.
- Capability verification and promotion readiness inspection objects and boundary notes.
- Capability relationship visibility output boundaries and unknown fields.
- Authority diagnostics and tests that assert read-only, ledger, mutation, and diagnostic-fact behavior.
- Compatibility-preservation tests and reports where output shape or wrapper behavior is explicitly preserved.

### Not observed / not established

- Not observed as a single shared Declaration framework.
- Not observed as ownership recovery.
- Not observed as implementation recovery.
- Not observed as a planner, selector, executor, capability acquisition path, policy evaluator, permission creator, or cluster mutator.
- Not established across all repository code; current evidence is strongest around operational visibility, diagnostic visibility, capability inspection, authority diagnostics, and compatibility/negative-authority surfaces.
- Not established as city-, district-, or neighborhood-level architecture beyond the recurring implementation-backed competency described here.

## Adjacency

Recurring citizens immediately adjacent to Declaration include:

- Operational Visibility
- Diagnostic Visibility
- Diagnostic Inventory
- Diagnostic Shape Audit
- CLI Surface
- Capability Candidate
- Capability Verification
- Verification Evidence
- Promotion Readiness
- Record Scope
- Event Ledger
- Mutation Boundary
- Read-only Boundary
- Compatibility Handoff
- Negative Authority
- Responsibility Evaluation
- Authority Boundary
- JSON Surface
- Rendered Report
- Test Assertion
- Unknown / Limitation

No relationship characterization is asserted here beyond adjacency.

## Survey resolution

```text
Citizen
```

Declaration is currently visible at citizen resolution. The reviewed evidence supports a recurring competency across multiple implementation families, but does not support treating Declaration as a house, neighborhood, district, or city.

## Maturity

Supported maturity labels:

- Implementation-backed: Declaration appears in executable code, dataclasses, registries, parser declarations, JSON functions, formatters, and tests.
- Shared: Declaration recurs independently across diagnostic inventory, diagnostic shape audit, operational CLI surfaces, capability verification, capability relationship, authority diagnostics, compatibility checks, and negative authority boundaries.
- Local: Each observed declaration remains local to its surface, registry, audit, or inspection object; no shared Declaration framework is recovered.
- Methodological: The repository repeatedly uses declarations to make boundaries inspectable and testable before allowing visibility surfaces to stand.

Unsupported / unknown maturity labels:

- Unknown for repository-wide completeness outside the reviewed implementation families.
- Unknown for any future framework status.

## Preserved unknowns

- Whether Declaration exists uniformly outside operational visibility, diagnostics, capability inspection, responsibility/authority diagnostics, compatibility surfaces, and negative-authority surfaces.
- Whether Declaration should ever become a shared abstraction.
- Whether there are undiscovered declaration forms not represented by the reviewed evidence.
- Whether Declaration has house-, neighborhood-, district-, or city-level structure.
- Whether all compatibility declarations share the same internal mechanism.
- Whether all negative authority declarations share the same internal mechanism.
- Whether Declaration can be separated from adjacent citizens without changing implementation.
- Whether Declaration has a stable lifecycle beyond being created, compared, rendered, and asserted in tests.
- Whether Declaration has any role in runtime behavior outside visibility, inspection, and boundary reporting.
- Whether Declaration can evaluate truth; current evidence only supports explicit claims being made inspectable and checked against implementation evidence in bounded places.

## Confidence

Confidence is high that Declaration is an implementation-backed recurring competency for making operational, diagnostic, capability, compatibility, record-scope, event-ledger, mutation, and negative-authority claims explicit and inspectable.

Confidence is medium that the same competency accounts for all reviewed compatibility declarations, because compatibility preservation appears in multiple tests and reports but is not always centralized in the same declaration mechanism.

Confidence is low for any broader architectural status, shared framework, ownership claim, or repository-wide coverage beyond the reviewed recurring evidence.

Competency interrogation complete.
