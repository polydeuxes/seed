# Operational Vocabulary Responsibility Audit

## Scope and method

This audit recovers implementation responsibility only. It does not rename concepts, propose replacement names, or redesign lifecycle boundaries. The evidence set is the current repository implementation plus the recent recovery investigations named in the task.

The recurring implementation rule is that names are weaker than ownership boundaries. The implementation frequently carries historical terms such as `tool`, `runtime`, `execution`, or `presentation`, but the authoritative responsibility is the code path, owned data, input contract, output/termination, and explicit boundary text.

## Concise audit table

| Current Name | Recovered Responsibility | Current Orientation | Responsibility Alignment |
| ------------ | ------------------------ | ------------------- | ------------------------ |
| `ToolNeed` | Preserves a requested or missing capability with desired inputs/outputs and reason. | Tool/historical implementation vocabulary. | Partial: responsibility is capability gap/request, not tool execution. |
| `ToolSpec` | Defines a registered executable operation contract: schema, implementation, policy action, visibility, status, risk, capabilities. | Tool and registry mechanism. | Partial-to-strong: `Tool` is historical, but `Spec` accurately signals contract. |
| `ToolRegistry` | Owns registered operation catalog lookup, duplicate protection, manifest loading, and model-visible filtering. | Tool-centric catalog vocabulary. | Partial: implementation center is registered-operation catalog. |
| `ToolExecutor` | Executes only registered operations after validation, policy evaluation, pending-action handling, and event recording. | Tool/execution vocabulary. | Strong when bounded to registered operations; weak if read as universal executor. |
| `CapabilityCatalog` | Read-only capability metadata and provider/handoff recommendation catalog. | Responsibility vocabulary. | Strong: catalog is recommendation metadata, not proof or authority. |
| `CapabilityCandidate` | Read-only preservation of possible capabilities inferred from projected package evidence, with explicit non-authority boundary. | Responsibility vocabulary with candidate boundary. | Strong. |
| `CapabilityVerification` | Read-only inspection joining capability candidates to projected `capability_verified` fact support. | Responsibility vocabulary. | Strong. |
| `Runtime` | Orchestrates validated decisions, records input/model/response events, delegates request-tool and call-tool branches to owner services. | Runtime/historical orchestration vocabulary. | Partial: not a universal lifecycle owner. |
| `Execution` / `ExecutionProposal` / `ExecutionStatus` | Split responsibilities: registered operation execution, experimental non-executable concrete-call proposal, and transient activity visibility. | Implementation/runtime/operator vocabulary. | Mixed: no single execution lifecycle exists. |
| `StateProjector` | Replays event history and finalizes derived indexes into inspectable projected state/read model. | Mechanism vocabulary. | Strong: projection is the responsibility and boundary. |
| `ObservationIngestor` | Converts observations into observation/evidence events and optional fact events while preserving provenance. | Responsibility vocabulary. | Strong. |
| `RelationshipCatalog` | Read-only vocabulary mapping fact predicates to bounded relationship definitions consumed by projection. | Responsibility vocabulary. | Strong. |
| `ExplanationBuilder` | Builds deterministic explanations from projected fact support, current beliefs, ambiguity, and conflicts. | Responsibility vocabulary. | Strong. |
| `Presentation` | Renders or surfaces human/JSON/operator views from projected or repository evidence without promoting vocabulary to knowledge. | Operator-facing vocabulary. | Partial: accurate for rendering, unsafe if read as authority. |
| `QuestionSurfaceInventory` | Static inventory mapping question families to answer surfaces, responsibilities, flags, diagnostics, and boundaries; not routing natural language. | Surface/operator vocabulary. | Strong as inventory; weak as question understanding. |
| `DiagnosticInventory` | Registry-backed operational shape declarations for diagnostic CLI surfaces, record scope, ledger writes, and mutation boundaries. | Responsibility vocabulary. | Strong. |
| `DocumentationStructure` | Read-only structural observation of Markdown documents and recurrence/membership/drilldown without prose or authority inference. | Responsibility vocabulary. | Strong. |

## Concept recovery

### `ToolNeed`

- **Current name:** `ToolNeed`.
- **Implementation owner:** `seed_runtime.models.ToolNeed` stores the record shape; `ToolNeedService` creates and resolves need records through ledger events.
- **Actual responsibility:** preserve a missing/requested capability and the reason it was requested. Its fields center `capability`, `reason`, `desired_inputs`, `desired_outputs`, `risk_hint`, and status. It does not execute, verify, register, adopt, or select a provider.
- **Input:** model/runtime request-tool decision data or service calls that describe a capability gap.
- **Termination:** a proposed or resolved need record in projected state and related recommendation metadata; not a tool call.
- **Architectural orientation:** capability-gap preservation.
- **Name orientation:** historical tool vocabulary. The implementation responsibility has shifted toward capability need/request ownership.
- **Alignment:** partial. `Need` is accurate; `Tool` carries historical/tool-oriented residue.

### `ToolSpec`

- **Current name:** `ToolSpec`.
- **Implementation owner:** toolkit manifest loader and registry.
- **Actual responsibility:** declare the executable operation contract: name, summary, toolkit id, input/output schema, policy action, implementation, status, visibility, risk class, capabilities, and examples.
- **Input:** toolkit manifests or code-created toolkit specs.
- **Termination:** registry-stored operation contract available to validation, model-visible lists, and execution.
- **Architectural orientation:** registered operation contract.
- **Name orientation:** tool/implementation mechanism plus accurate specification vocabulary.
- **Alignment:** partial-to-strong. `Spec` is accurate; `Tool` reflects historical runtime/tool language.

### `ToolRegistry`

- **Current name:** `ToolRegistry`.
- **Implementation owner:** `seed_runtime.registry.ToolRegistry`.
- **Actual responsibility:** maintain registered toolkit and operation entries; reject duplicates; return required entries; list model-visible registered operations; map normalized capabilities to registered operations.
- **Input:** `Toolkit`/`ToolSpec` objects loaded from manifests.
- **Termination:** deterministic registered-operation catalog lookup/listing.
- **Architectural orientation:** registered operation catalog authority.
- **Name orientation:** tool-centric historical vocabulary.
- **Alignment:** partial. Registry is accurate; current center is registered operation, not generic tool interaction.

### `ToolExecutor`

- **Current name:** `ToolExecutor`.
- **Implementation owner:** `seed_runtime.execution.ToolExecutor`.
- **Actual responsibility:** execute registered operation calls only after registry-backed validation, state-aware policy evaluation, pending-action handling, and event recording.
- **Input:** `Runtime.call_tool` branch or approved pending action, plus workspace/session/tool name/arguments.
- **Termination:** completed, failed, denied, or pending tool-call result and ledger events such as started/completed/failed.
- **Architectural orientation:** registered-operation execution boundary.
- **Name orientation:** tool/execution vocabulary.
- **Alignment:** strong only inside the registered-operation boundary. It is misaligned if interpreted as owner of discovery, recommendations, capability verification, runtime responses, diagnostics, projection, or observation.

### `CapabilityCatalog`

- **Current name:** `CapabilityCatalog`.
- **Implementation owner:** `seed_runtime.capability_catalog.CapabilityCatalog` and checked-in catalog entries.
- **Actual responsibility:** load and serve read-only capability metadata and provider or handoff recommendations for a `ToolNeed` capability.
- **Input:** YAML catalog entries and a need capability.
- **Termination:** recommendation rows or no recommendation.
- **Architectural orientation:** capability recommendation metadata.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong. The code explicitly says the catalog does not execute tools.

### `CapabilityCandidate`

- **Current name:** `CapabilityCandidate`.
- **Implementation owner:** `seed_runtime.capability_candidates`.
- **Actual responsibility:** preserve possible capability candidates derived from projected observed package facts while retaining evidence support and boundary notes that reject proof, permission, selection, policy evaluation, invocation, and execution.
- **Input:** projected `State`, package-installed facts, optional filter.
- **Termination:** read-only `CapabilityCandidateInspection`.
- **Architectural orientation:** evidence-derived candidate preservation.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong. Candidate vocabulary matches weaker-than-verification responsibility.

### `CapabilityVerification`

- **Current name:** `CapabilityVerification`.
- **Implementation owner:** `seed_runtime.capability_verification` plus capability inventory and verification evidence helpers.
- **Actual responsibility:** inspect verification status by joining candidate universe to projected `capability_verified` facts and verification evidence. It does not choose, authorize, invoke, or execute capability use.
- **Input:** projected `State`, capability candidates, capability inventory, verification evidence, optional filter/time.
- **Termination:** read-only `CapabilityVerificationInspection`.
- **Architectural orientation:** verification-status inspection.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong.

### `Runtime`

- **Current name:** `Runtime`.
- **Implementation owner:** `seed_runtime.runtime.Runtime`.
- **Actual responsibility:** orchestrate user-message handling, project current state, compose decision input, obtain and validate model decisions, guard tool intent, record model/response events, route decisions to owner services, and return a `RuntimeResponse`.
- **Input:** workspace id, session id, user text.
- **Termination:** answer, question, refusal, invalid-decision response, tool-need response, tool-call response, or delegated state-patch behavior depending on decision branch.
- **Architectural orientation:** decision routing/orchestration, not universal lifecycle ownership.
- **Name orientation:** historical runtime implementation vocabulary.
- **Alignment:** partial. It accurately identifies a runtime orchestration locus, but repository evidence rejects reading it as the owner of execution, capability discovery, projection authority, or presentation knowledge.

### `Execution`

- **Current name:** `Execution`, appearing as `ToolExecutor`, `ExecutionProposal`, and `ExecutionStatus` surfaces.
- **Implementation owner:** split across `ToolExecutor`, `ExecutionProposalService`, `ExecutionStatusConsumer`, policy/pending-action services, and CLI status consumers.
- **Actual responsibility:** no universal execution lifecycle. Registered operation execution is one bounded branch; execution proposals are legacy/experimental non-executable concrete-call shapes; execution status is renderer-independent, non-authoritative progress visibility.
- **Input:** varies by branch: registered tool call, action plan plus state, or status emissions from long-running projection/ingestion/persistence work.
- **Termination:** completed/failed/pending tool call, optional non-executable proposal, or transient status rendering/recording.
- **Architectural orientation:** split implementation detail and operator visibility.
- **Name orientation:** implementation-centric and operator-centric.
- **Alignment:** mixed. `Execution` remains correct only where code actually invokes registered operations. It is inaccurate as a universal lifecycle label.

### `StateProjector`

- **Current name:** `StateProjector`.
- **Implementation owner:** `seed_runtime.state.StateProjector`.
- **Actual responsibility:** rebuild current inspectable state by replaying ledger events, applying event handlers, and finalizing derived indexes, relationships, entity types, graph issues, supports, conflicts, and inference.
- **Input:** append-only ledger events and catalogs.
- **Termination:** projected `State` read model, diagnostics, or cache-adjacent reports from other helpers.
- **Architectural orientation:** projection/read-model construction from event authority.
- **Name orientation:** responsibility/mechanism vocabulary.
- **Alignment:** strong. It is named after projection responsibility and does not claim event-authority ownership.

### `ObservationIngestor`

- **Current name:** `ObservationIngestor`.
- **Implementation owner:** `seed_runtime.observations.ObservationIngestor`.
- **Actual responsibility:** accept observations, derive provenance evidence, optionally derive facts, and append ordered observation/evidence/fact events in batches.
- **Input:** `Observation` objects and event context.
- **Termination:** persisted observation/evidence events and optional fact events; returns fact or `None` when fact promotion is suppressed.
- **Architectural orientation:** observation-to-ledger intake with provenance preservation.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong.

### `RelationshipCatalog`

- **Current name:** `RelationshipCatalog`.
- **Implementation owner:** `seed_runtime.relationship_catalog.RelationshipCatalog` and built-in relationship catalog JSON.
- **Actual responsibility:** load and provide read-only relationship definitions and predicate-to-relationship mapping for projection.
- **Input:** catalog JSON or injected relationship definitions.
- **Termination:** canonical relationship definitions returned by name, predicate, or list.
- **Architectural orientation:** bounded relationship vocabulary consumed by projection.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong. It does not claim relationship evidence proves behavior, calls, reachability, or ownership.

### `ExplanationBuilder`

- **Current name:** `ExplanationBuilder`.
- **Implementation owner:** `seed_runtime.explanations.ExplanationBuilder`.
- **Actual responsibility:** build deterministic explanations from projected state supports, current beliefs, competing beliefs, and conflicts.
- **Input:** projected `State`, query subject, query predicate.
- **Termination:** explanation model with current, ambiguous, or no-current-belief status.
- **Architectural orientation:** projected-support explanation rendering.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong. It builds explanations; it does not create facts or resolve authority.

### `Presentation`

- **Current name:** `Presentation` as a broad operational concept rather than one class.
- **Implementation owner:** CLI renderers, formatter functions, question-surface inventory, diagnostic reports, explanation rendering, and view builders.
- **Actual responsibility:** expose bounded views for humans or JSON consumers using projected state, repository structure, or diagnostic inputs.
- **Input:** projected state, report objects, inventory rows, CLI arguments, and repository files depending on surface.
- **Termination:** rendered human text or JSON output.
- **Architectural orientation:** operator-facing visibility, not knowledge authority.
- **Name orientation:** operator interaction.
- **Alignment:** partial. It is accurate for rendering and view surfaces, but presentation labels do not become repository knowledge without implementation evidence.

### `QuestionSurfaceInventory`

- **Current name:** `QuestionSurfaceInventory`.
- **Implementation owner:** `seed_runtime.question_surface_inventory`.
- **Actual responsibility:** statically map question families to surfaces, flags, examples, answer responsibilities, authority boundaries, diagnostic names, shape specs, and implementation reasons. It explicitly does not infer natural-language intent by itself.
- **Input:** no runtime inference input; deterministic construction of rows.
- **Termination:** read-only inventory rows rendered by CLI/JSON.
- **Architectural orientation:** operator question-to-surface documentation and visibility.
- **Name orientation:** responsibility-oriented surface inventory.
- **Alignment:** strong as inventory. It would be misread if treated as classifier, router, or ontology.

### `DiagnosticInventory`

- **Current name:** `DiagnosticInventory`.
- **Implementation owner:** `seed_runtime.diagnostic_inventory`.
- **Actual responsibility:** registry-backed declarations of diagnostic surfaces, including flags, projected-state/file usage, JSON support, record support, diagnostic record scope, fact emission, ledger writes, mutation boundary, and descriptions.
- **Input:** static inventory definitions.
- **Termination:** deterministic inventory output and shape-audit evidence.
- **Architectural orientation:** operational visibility contract and diagnostic boundary registry.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong.

### `DocumentationStructure`

- **Current name:** `DocumentationStructure`.
- **Implementation owner:** `seed_runtime.documentation_structure`.
- **Actual responsibility:** read Markdown files and report mechanical structural metadata, recurrence, exact section drilldown, and exact membership without prose interpretation, claim extraction, authority inference, shape inference, ontology promotion, event-ledger writes, or repository mutation.
- **Input:** repository root, selected document, and structural options.
- **Termination:** `DocumentationStructureReport` and related recurrence/drilldown/membership reports.
- **Architectural orientation:** read-only repository document structure observation.
- **Name orientation:** responsibility-oriented.
- **Alignment:** strong.

## Well-aligned vocabulary

The following concepts are already named close to implementation responsibility:

- `CapabilityCatalog`, because it is a read-only catalog of capability metadata and recommendations rather than capability proof or execution authority.
- `CapabilityCandidate`, because candidate status is explicitly weaker than verified capability, selection, policy, invocation, or execution.
- `CapabilityVerification`, because it inspects verification status from projected verification facts.
- `StateProjector`, because it projects state from ledger events and derived indexes without owning original event authority.
- `ObservationIngestor`, because it ingests observations into ordered ledger events while preserving provenance.
- `RelationshipCatalog`, because it is a catalog of relationship vocabulary and predicate mapping, not a behavioral proof engine.
- `ExplanationBuilder`, because it builds explanations from projected support and conflicts.
- `QuestionSurfaceInventory`, when read as inventory rather than natural-language routing.
- `DiagnosticInventory`, because it inventories diagnostic shapes, flags, recording, ledger, and mutation boundaries.
- `DocumentationStructure`, because it observes document structure and explicitly refuses semantic promotion.

## Substantially drifted or partially drifted vocabulary

### Tool-oriented drift

`ToolNeed`, `ToolRegistry`, `ToolExecutor`, and parts of `ToolSpec` preserve historical tool vocabulary. Implementation evidence narrows these concepts:

- `ToolNeed` centers capability gap/request responsibility.
- `ToolRegistry` centers registered operation catalog authority.
- `ToolExecutor` centers registered-operation execution only.
- `ToolSpec` centers registered operation contract fields.

The mismatch is not uniform: `ToolExecutor` remains acceptable when the operation is actually a registered executable tool call, while `ToolNeed` is more strongly drifted because need records are capability-gap records rather than tools.

### Runtime-oriented drift

`Runtime` is implementation-centered vocabulary that can overstate responsibility. The code owns orchestration and routing, but delegates core behavior to projection, tool need, recommendation, state patch, validation, and execution services. Current vocabulary is acceptable only if read narrowly as orchestration runtime.

### Execution-oriented drift

`Execution` is not one lifecycle. Evidence splits it into registered-operation execution, experimental non-executable execution proposals, and transient operator-visible execution status. Any audit or future vocabulary work must avoid promoting `execution` into a universal architectural center.

### Operator/presentation drift

`Presentation` and question-facing surfaces are operator interaction terms. They accurately describe output surfaces, but do not create repository knowledge. Presentation vocabulary requires implementation evidence before it can become preserved or projected knowledge.

## Historical vocabulary that should explicitly remain where responsibility still matches

- `ToolExecutor` should retain its historical vocabulary for the bounded branch that actually executes registered operations. The responsibility still matches registered tool-call execution.
- `ToolSpec` can retain `Spec` because the implementation is genuinely a contract/specification. The `Tool` portion remains historical but is still locally meaningful where manifests define executable operation entries.
- `ExecutionStatus` can retain its name because it describes transient activity status, but only with the non-authoritative visibility boundary intact.
- `Runtime` can remain accurate as an implementation locus for decision orchestration, provided it is not treated as the owner of all lifecycle semantics.

## Direction of mismatch

### Tool-centric: accepted, but bounded

Accepted for `ToolNeed`, `ToolSpec`, `ToolRegistry`, and `ToolExecutor`. The strongest evidence is that their implementation centers capabilities, registered operation contracts, registry authority, and execution boundaries rather than open-ended model/tool interaction.

### LLM-centric: partly accepted

Accepted primarily around `Runtime` and decision production/validation paths. However, most recovered concepts do not center LLM interaction. Capability candidates, verification, projection, observation ingestion, relationships, diagnostics, and documentation structure are implementation/read-model responsibilities independent of model invocation.

### Implementation-centric: accepted

Accepted for `Runtime`, `Execution`, `StateProjector`, and `Tool*` surfaces. Some implementation-centered names are accurate (`StateProjector`); others overgeneralize responsibility (`Execution`, `Runtime`) unless bounded.

### Operator-centric: accepted for surfaces only

Accepted for `Presentation`, `QuestionSurfaceInventory`, `DiagnosticInventory`, `DocumentationStructure`, and `ExecutionStatus` as visibility surfaces. Rejected as knowledge authority: operator-facing labels do not prove repository knowledge or architectural ownership.

## Unsupported conclusions

This recovery does not support any of the following conclusions:

- That all operational concepts should be renamed now.
- That there is one universal promotion pipeline.
- That there is one universal execution lifecycle.
- That `ToolExecutor` owns discovery, provider adoption, capability verification, diagnostics, observation, or projection.
- That `Runtime` owns every lifecycle under Seed.
- That presentation labels such as navigation, continuation, topology, state build, or current work position are automatically preserved knowledge.
- That capability candidates are verified capabilities.
- That documentation structure observation extracts claims or authority.

## Implementation-backed conclusions

1. The repository has recovered enough responsibility evidence to identify which vocabulary is well aligned and which vocabulary is historical.
2. The most stable responsibility centers are observation ingestion, state projection, capability candidate preservation, capability verification inspection, relationship cataloging, explanation building, diagnostic inventory, question surface inventory, and documentation structure observation.
3. The least stable vocabulary centers are `ToolNeed`, `ToolRegistry`, broad `Execution`, broad `Runtime`, and broad `Presentation` if read without their implementation boundaries.
4. Future renaming work is technically plausible for the most drifted concepts, but this audit does not propose names.
5. The concepts most ready for future renaming investigation are `ToolNeed`, `ToolRegistry`, and broad `Execution`, because their recovered responsibilities are already repeatedly bounded by implementation and prior recovery reports.
6. `Runtime` requires more caution before any renaming effort because its orchestration responsibility is real but broad, and multiple services cross through it.
7. `ToolExecutor` is not a simple rename candidate because its bounded responsibility still includes actual registered operation execution.

## Recommended next investigation

Run a narrower future investigation on readiness for vocabulary change, not on replacement names. The next investigation should ask:

- Which public CLI surfaces, tests, docs, manifests, and JSON keys currently depend on `ToolNeed`, `ToolRegistry`, `ToolSpec`, `ToolExecutor`, `Runtime`, and `Execution` vocabulary?
- Which of those names are stable API contracts versus internal implementation labels?
- Which historical names are only documentation vocabulary, and which are serialized or user-visible compatibility surfaces?
- Which concepts have enough implementation-backed responsibility recovery to support a compatibility-preserving rename plan later?

That next investigation should still avoid proposing replacement names until compatibility boundaries are recovered.
