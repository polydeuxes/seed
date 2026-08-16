# Bounded ask routing reconciliation

## Scope

This reconciliation remains observational. It reviews the existing question-surface inventory, operational surface inventory, documentation-structure observer, existing inquiry surfaces, and CLI registration to determine whether the repository already contains enough implementation-backed knowledge to route one bounded operator question to one existing inquiry surface.

It does not recommend natural-language routing, fuzzy matching, semantic search, embeddings, planners, conversation runtime, documentation-driven execution, or a generic inquiry engine.

## Answer

Yes, for one bounded operator question, the repository already contains the pieces required to deterministically route to one existing inquiry surface when the question is represented by an existing inventory row rather than free text.

The current repository does not implement `seed ask`, does not accept a free-text question for the question-surface inventory, and does not expose a routing command. Therefore the architecture is not implemented as a user-facing ask flow. The demonstrated support is narrower: an existing static inventory row can bind a known question family and examples to exactly one current CLI surface.

## Routing evidence

### Operator-facing inquiry inventory exists

`seed_runtime/question_surface_inventory.py` defines a static `QuestionSurfaceInventoryRow` with fields for question family, example questions, surface, CLI flag, answer responsibility, authority boundary, and notes. `build_question_surface_inventory()` returns deterministic rows, including authority-constrained container ownership, service ownership, and listener endpoint reachability.

The reviewed authority rows provide the strongest routing evidence:

| Existing bounded question family | Example question evidence | Routed surface | CLI flag | Answer responsibility evidence |
| --- | --- | --- | --- | --- |
| authority-constrained container ownership | `Can Seed determine container ownership without Docker or root?` | `container_ownership_authority` | `--container-ownership-authority` | evaluates container ownership reachability under the constrained authority profile |
| authority-constrained service ownership | `Can Seed determine service ownership under current authority?` | `service_ownership_authority` | `--service-ownership-authority` | evaluates service ownership reachability under constrained authority and implementation inventory evidence |
| listener endpoint reachability | `Can Seed see local listener endpoints?` | `listener_endpoint_authority` | `--listener-endpoint-authority` | evaluates local TCP/UDP listener endpoint authority and reachability |

This is an inventory, not a router. The implementation and tests explicitly preserve that boundary: inventory row notes say it does not route questions, and the CLI rejects a free-text question argument.

### Operational surfaces exist independently

The diagnostic inventory registers the same reviewed surfaces as read-only operational diagnostics with CLI flags and declared boundaries. It also registers `documentation_structure` and `question_surface_inventory`. This proves the CLI surfaces exist as operational surfaces separate from the question-family inventory.

The CLI parser registers:

- `--documentation-structure` and exact structure-related flags such as `--recurrence`, `--where`, and `--membership`;
- `--container-ownership-authority`;
- `--service-ownership-authority`;
- `--listener-endpoint-authority`;
- `--question-surface-inventory`.

The shape audit also has a `question_surface_inventory` implementation spec pointing to `seed_runtime/question_surface_inventory.py`, its builder, formatter, JSON function, and CLI flag. That means the inventory itself is covered by the repository's diagnostic-shape machinery.

## Reviewed inquiries

### Container ownership authority

Implementation expresses all three requested pieces:

- **Question it answers:** the question inventory gives example operator questions about determining container ownership without Docker or root.
- **Desired observation:** `DESIRED_OBSERVATION = "container ownership"` in the evaluator.
- **Expected operator intent:** the inventory states the surface evaluates container ownership reachability under the constrained authority profile; the evaluator says it evaluates only the container-ownership/root-Docker authority slice.

This is sufficient for a deterministic inventory-row-to-surface mapping.

### Service ownership authority

Implementation expresses all three requested pieces:

- **Question it answers:** the question inventory gives example operator questions about determining service ownership under current authority and why it is blocked.
- **Desired observation:** `DESIRED_OBSERVATION = "service ownership"` in the evaluator.
- **Expected operator intent:** the inventory states the surface evaluates service ownership reachability under constrained authority and implementation inventory evidence; the evaluator says it evaluates only the service-ownership authority slice.

This is the strongest demonstration candidate because the user's example question, “Can you determine service ownership?”, is already represented by the question inventory's service-ownership row.

### Listener endpoint authority

Implementation expresses all three requested pieces:

- **Question it answers:** the question inventory gives example operator questions about seeing local listener endpoints and why endpoint ownership or process context is unavailable.
- **Desired observation:** `DESIRED_OBSERVATION = "local listener endpoint inventory"` in the evaluator.
- **Expected operator intent:** the inventory states the surface evaluates local TCP/UDP listener endpoint authority and reachability; the evaluator boundary explicitly excludes ownership, health, responsiveness, external accessibility, DNS validity, remote network reachability, causality, and intent.

This is deterministically routable only for the bounded endpoint-inventory question, not for service ownership or process ownership questions.

## Deterministic mapping finding

A deterministic mapping currently exists at the artifact level:

```text
QuestionSurfaceInventoryRow.question_family
+ QuestionSurfaceInventoryRow.example_questions
+ QuestionSurfaceInventoryRow.surface
+ QuestionSurfaceInventoryRow.surface_flag
```

For a bounded known question such as “Can Seed determine service ownership under current authority?”, the current inventory row maps to `service_ownership_authority` and `--service-ownership-authority` without needing fuzzy matching or natural-language interpretation.

The implementation does not currently provide a command that accepts the question and executes that route. Therefore the answer is:

```text
Can one bounded operator question already be routed to one existing inquiry?

Repository knowledge: yes, if the question is already represented as an inventory row.
Runtime CLI behavior: no, not as an implemented ask command.
```

## Documentation contribution

Documentation provides supporting evidence and prior reconciliations, but it is not the best routing authority. The reviewed implementation evidence is stronger than documentation because the question inventory directly binds question families to surfaces and CLI flags, while documentation narratives can describe, reconcile, or audit boundaries without being executable authority.

Documentation should remain supporting evidence for routing claims unless a future implementation explicitly makes it authority. Current instructions and implementation both caution against promoting presentation vocabulary or prose into repository knowledge without implementation evidence.

## Structure observer contribution

The documentation structure observer currently provides supporting evidence and validation-like audit visibility, not routing.

It observes mechanical documentation facts: front matter, heading outlines, section inventories, Markdown links, fenced code blocks, recurrence, exact section-label drilldown, exact section-label membership, skeleton signatures, and bounded output controls. Its diagnostic inventory description explicitly says it does this without interpreting prose, extracting claims, inferring authority, inferring shapes, promoting ontology, writing events, or mutating the repository.

Its tests preserve that boundary: structure filters select documents without detail expansion or semantics, rendered JSON must not include semantic prose from code blocks, and boundary fields such as `interprets_prose`, `infers_claims`, and `infers_authority` remain false.

Therefore:

| Candidate role | Finding |
| --- | --- |
| Supporting evidence | Yes. It can show where structural labels, docs, sections, links, recurrence, or membership exist. |
| Validation | Partially, for structural visibility and boundary audits only. |
| Routing | No. It does not interpret questions, infer intent, or bind questions to executable surfaces. |
| None | No, because it can still audit supporting documentation structure. |

## Would structure improve routing or audit routing?

Current structure observations would merely help audit routing. They can confirm that related documents or sections exist and can expose structural recurrence or membership around routing documentation, but they cannot decide that an operator question maps to a CLI surface because they intentionally avoid prose interpretation, claim extraction, authority inference, and ontology promotion.

## Routing authority

Best suited current artifact: **question inventory**.

Independent evaluation:

| Artifact | Routing-authority suitability | Reason |
| --- | --- | --- |
| Question inventory | Strongest | It directly records question family, example questions, answering surface, CLI flag, responsibility, boundary, and notes. |
| Operational surface inventory / diagnostic inventory | Necessary but insufficient | It proves operational surfaces and declared shape, but does not express the operator question each surface answers as directly as the question inventory. |
| Documentation | Supporting | It reconciles and explains, but prose is not implementation authority. |
| Structure observations | Audit/support only | It observes mechanical documentation structure and explicitly avoids semantic authority. |
| Existing inquiry evaluator modules | Strong for execution target, insufficient as central router | They define desired observations and bounded behavior, but each only owns its own inquiry slice. |

The initial routing authority should therefore be the question-surface inventory, with diagnostic inventory and CLI parser evidence used to prove the target surface exists and remains visible.

## Coupling of operator question, bounded inquiry, and CLI surface

Implementation partially distinguishes the three, but they are still coupled at the operational boundary.

Existing distinctions:

- **Operator question:** represented in `example_questions` in the question-surface inventory.
- **Bounded inquiry:** represented by evaluator modules and desired-observation constants such as `container ownership`, `service ownership`, and `local listener endpoint inventory`.
- **CLI surface:** represented by parser flags, diagnostic inventory entries, and question inventory `surface_flag` values.

Remaining coupling:

- There is no `ask` command or routing layer between operator question and CLI flag.
- The operator still directly invokes inquiry CLI flags.
- The question inventory rows are static documentation-like implementation data; they do not execute or dispatch.

## Smallest implementation-backed demonstration

The smallest demonstration that would prove the architecture is already present as data and execution target, but not as an ask command:

```text
Operator bounded question represented in inventory:
Can Seed determine service ownership under current authority?

Inventory row:
authority-constrained service ownership

Deterministic target:
service_ownership_authority / --service-ownership-authority

Existing inquiry:
evaluate_service_ownership_authority_slice(...)

Existing output:
service ownership authority report / JSON payload
```

The necessary pieces already exist: the inventory row, the CLI flag, the evaluator, the desired observation, the read-only boundary, diagnostic inventory registration, and shape-audit registration.

The missing piece is not knowledge; it is the absence of an implemented `seed ask` dispatch surface.

## Remaining gaps

- No implemented `seed ask` command.
- No implemented routing function that consumes a bounded question ID or inventory key and dispatches to a surface.
- `--question-surface-inventory` rejects free-text question input.
- The question inventory is explicitly not a router or recommender.
- Documentation structure is intentionally non-semantic and cannot promote routing authority.

## Strongest supporting evidence

- `QuestionSurfaceInventoryRow` binds question families and example questions to exactly one surface and CLI flag.
- The three reviewed inquiry modules expose desired-observation constants and bounded evaluators.
- The diagnostic inventory registers the reviewed inquiry surfaces as read-only operational surfaces.
- CLI parser registration exposes the surfaces as flags.
- Shape-audit implementation specs cover the question inventory and reviewed diagnostics.

## Strongest contradictory evidence

- The CLI rejects a free-text argument to `--question-surface-inventory`.
- Tests assert the question inventory is not a router or recommender.
- Documentation structure explicitly avoids interpreting prose, inferring claims, and inferring authority.
- No `seed ask` command is registered.

## Recommended bounded implementation slice

A bounded future proof slice, if implementation is later requested, would use an explicit inventory key rather than natural language:

```text
seed ask --question-family authority-constrained-service-ownership
```

The route authority would be the existing question-surface inventory row, and the target would be the existing `--service-ownership-authority` inquiry. This report does not recommend implementing it now; it identifies the smallest implementation-backed slice that current repository knowledge can support.

## Commands executed

```text
pwd && rg --files -g 'AGENTS.md' -g '!venv' -g '!node_modules' && git status --short
cat AGENTS.md && rg -n "question|diagnostic-inventory|service-ownership|container-ownership|listener-endpoint|structure|membership|coverage|recurrence|drilldown|diagnostic-shape-audit|argparse|click|Typer|--" -g '!*.pyc' -g '!venv' -g '!node_modules' .
rg --files | head -n 80 && sed -n '1,220p' seed_runtime/question_surface_inventory.py && sed -n '1,260p' seed_runtime/diagnostic_inventory.py
sed -n '220,420p' seed_runtime/question_surface_inventory.py; sed -n '1,260p' seed_runtime/service_ownership_authority.py; sed -n '1,220p' seed_runtime/container_ownership_authority.py; sed -n '1,200p' seed_runtime/listener_endpoint_authority.py
rg -n "question-surface-inventory|container-ownership-authority|service-ownership-authority|listener-endpoint-authority|documentation-structure|ask" scripts/seed_local.py seed_runtime/diagnostic_shape_audit.py tests/test_question_surface_inventory.py tests/test_documentation_structure.py | head -n 250
sed -n '1070,1230p' scripts/seed_local.py; sed -n '2360,2405p' scripts/seed_local.py; sed -n '600,630p' seed_runtime/diagnostic_shape_audit.py; sed -n '70,105p' tests/test_question_surface_inventory.py; sed -n '730,795p' tests/test_documentation_structure.py
```

## Files inspected

- `AGENTS.md`
- `seed_runtime/question_surface_inventory.py`
- `seed_runtime/diagnostic_inventory.py`
- `seed_runtime/diagnostic_shape_audit.py`
- `seed_runtime/container_ownership_authority.py`
- `seed_runtime/service_ownership_authority.py`
- `seed_runtime/listener_endpoint_authority.py`
- `seed_runtime/documentation_structure.py`
- `scripts/seed_local.py`
- `tests/test_question_surface_inventory.py`
- `tests/test_documentation_structure.py`
- `tests/test_container_ownership_authority.py`
- `tests/test_service_ownership_authority.py`
- `tests/test_listener_endpoint_authority.py`
- selected prior reconciliations under `docs/` found by targeted ripgrep

## Files changed

- `docs/bounded_ask_routing_reconciliation.md`

## LOC changed

- Added 257 lines.

## Tests run

```text
pytest -q tests/test_question_surface_inventory.py tests/test_container_ownership_authority.py tests/test_service_ownership_authority.py tests/test_listener_endpoint_authority.py tests/test_documentation_structure.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py
```
