# Free-Form Operator Interface / Dynamic View Topology Audit 001

## 1. Bounded question

Is the free-form `seed` session the canonical bidirectional constitutional interface, with operator prose translated inward and bounded constitutional views translated outward, while CLI argument commands and fixed diagnostic surfaces remain temporary serialized grammar, compatibility entry points, or implementation scaffolding?

## 2. Fixed distinctions preserved

This audit preserves the requested distinctions: interactive session is not operator ingress; operator input is not terminal output; operator prose is not a bounded constitutional question; CLI arguments are not constitutional inquiry; CLI parsing is not constitutional interpretation; question family is not operator meaning; diagnostic command is not canonical capability; fixed view is not dynamic composition; view selection, view composition, presentation translation, terminal egress, and rendered text are separate responsibilities.

## 3. Methodology

Read-only implementation audit. I inspected the CLI entry point, shell loop, runtime refusal path, bounded question producer, selection/composition pipeline, question-family dispatch, diagnostic inventory, read-model registrations, and renderer/printing paths. I ran focused probes and a small baseline test set. No source, tests, diagnostics, views, renderers, registry entries, or CLI behavior were changed.

## 4. Inspected entry points

- `scripts/seed_local.py` is the executable implementation inspected. Its `main()` builds the parser, parses argv, applies bounded ask dispatch, handles many one-shot diagnostic/read-model flags, then either runs HTTP, one-shot message handling, or `run_shell()`.
- `run_shell()` implements the no-argument interactive prompt: it prints a shell banner to stderr, reads `input("seed> ").strip()`, exits on `exit`/`quit`/EOF, and otherwise calls `app.run(text)` and prints `format_cli_output(...)`.
- `LocalSeedApp.run()` passes text to `Runtime.handle_user_message(workspace_id, session_id, text)` and returns the response plus ledger events.
- `Runtime.handle_user_message()` appends `input.user_message` with `{"text": text}`, appends `runtime.decision_authority_unsupported`, and returns an unsupported response.

## 5. Current interactive prompt topology

Current actual topology for `seed` with no args:

```text
process entry
→ argparse parse empty argv
→ build LocalSeedApp
→ run_shell
→ terminal input read (`input("seed> ")`)
→ string strip
→ LocalSeedApp.run
→ Runtime.handle_user_message
→ event-ledger input.user_message
→ event-ledger runtime.decision_authority_unsupported
→ RuntimeResponse(kind="unsupported")
→ format_response_summary / format_cli_output
→ print to stdout
```

The session is an interactive loop, but not a constitutional free-form ingress. It records raw-ish stripped text as user-message event payload, preserves workspace/session ids and actor `user`, but does not produce `BoundedConstitutionalQuestion`, does not project selection keys, does not select constitutional views, and does not compose a bounded constitutional explanation.

## 6. Free-form warning analysis

The emitted warning is:

```text
No Seed-owned runtime decision authority is configured for free-text input.
```

Implementation evidence says the unsupported boundary is not merely lexical parsing. The runtime explicitly refuses model-shaped/free-text decision authority because model-produced Decisions are external grammar and cannot route Seed runtime movement. Missing producers include prose-to-bounded-inquiry interpretation and authority/scope binding, but the first implementation-blocking producer is the operator-expression-to-bounded-inquiry interpreter: no owner converts free-form text into explicit bounded fields such as bounded question, constitutional intent, scope status, and selection keys.

## 7. CLI grammar inventory

| CLI element | Parsed meaning | Canonical artifact produced | View/result selected | Presentation selected | Compatibility/scaffolding role |
|---|---|---|---|---|---|
| positional `message` | free-text one-shot runtime input | `RuntimeResponse(kind=unsupported)` plus input event | none | `format_cli_output` summary | legacy/convenience input path; not constitutional inquiry |
| no args / shell | repeated free-text runtime input | same unsupported runtime response | none | CLI summary to stdout | interactive convenience wrapper today |
| `ask --question-family FAMILY` | exact inventory-backed question-family text | bounded-work eligibility/selection/dispatch handoffs, not `BoundedConstitutionalQuestion` except constitutional-pipeline family through surface args | mapped existing surface | raw answer surface unless `--presentation` | temporary structured operator grammar and compatibility dispatcher |
| `--surface-args` | explicit surface parameters forwarded unchanged | surface-arg result / argparse namespace mutation | command-specific | inherited | parameter escape hatch; implementation-specific |
| `--presentation` with `ask` | return composed QuestionFamily explanation | presentation handoff/result | question-family explanation | human/json via surrounding flags | compatibility presentation path |
| `--current-facts [SUBJECT PREDICATE]` | read current facts or all current facts | formatted fact view from projected state/fact index | current-facts read model | human only in inspected path | fixed read-model surface |
| `--state-build` | state summary read model | state summary view | state build | human/json depending flags in nearby code | fixed read-model surface |
| `--ownership-discrepancies` + `--alias` | discrepancy diagnostic over projected state | discrepancy rows | ownership discrepancy diagnostic | human or JSON | fixed diagnostic/prebuilt composition |
| `--knowledge-reachability-audit` family/subject/kind/limit/all/json/debug | reachability audit parameters | reachability audit result | knowledge reachability diagnostic | human table or JSON | fixed diagnostic with audit-specific grammar |
| `--diagnostic-inventory` | registry-backed diagnostic inventory | inventory entries | diagnostic inventory | human or JSON | visibility registry surface |
| `--classification-coverage` | classification coverage diagnostic | diagnostic artifact, optional record | classification coverage | human; records when requested | fixed diagnostic, can write diagnostic_run ledger facts |
| `--constitutional-pipeline` | explicit bounded constitutional pipeline fields | `ConstitutionalPipelineResult` containing bounded question, projections, selection, composition | selected by explicit selection keys | human or JSON | closest current canonical structured inquiry path |
| `--operator-inquiry` | operator testimony string | field in `ConstitutionalPipelineRequest`/`BoundedConstitutionalQuestion` | none alone | none | serialized testimony field |
| `--inquiry-provenance` | provenance string | bounded-question provenance | none alone | none | serialized provenance field |
| `--bounded-question` | explicit bounded question | bounded-question field | none alone | none | manual interpretation field |
| `--constitutional-intent` | explicit intent | bounded-question field | none alone | none | manual interpretation field |
| `--scope-status` | explicit scope status | bounded-question field | none alone | none | manual scope field |
| `--selection-key` | exact selection key | caller-supplied field consumed by question projection | deterministic view match | none alone | manual view-demand encoding |
| `--constitutional-view-composition VIEWS...` | explicit registered view names | `ConstitutionalViewCompositionArtifact` | views named directly | human or JSON | explicit composition adapter; bypasses inquiry interpretation |
| `--constitutional-process/governance/fidelity` | direct view flag | individual constitutional view artifact | fixed view | human or JSON | prebuilt constitutional read-model surface |
| `--json` | representation request for supported diagnostics/views | JSON-ready dict rendered through `json.dumps` | no | JSON | presentation/rendering switch, often CLI-owned |

## 8. Arguments-as-external-grammar analysis

The hypothesis is supported for most current structured roads. Example:

```bash
seed ask --question-family "ownership ambiguity" --surface-args node115
```

Semantics encoded by flags: exact family identity, use of bounded ask machinery, and surface-argument forwarding. Semantics manually supplied by the operator: the family label and node/surface parameter. Semantics inferred by Seed: only exact inventory admission, eligibility, required-argument satisfaction, mapped surface dispatch, and renderer selection. The flags bypass free-form constitutional interpretation and often compress inquiry, selection, composition, and presentation into one command-specific path.

For the constitutional pipeline command, flags manually supply the already-interpreted bounded inquiry. That is lawful for automation and tests, but it proves the free-form translator is absent.

## 9. Canonical-ingress convergence

Current roads can converge conceptually on `BoundedConstitutionalQuestion`, because that artifact already preserves operator inquiry, provenance, bounded question, intent, scope status, uncertainty, Unknowns, caller-supplied fields, and read-only boundaries. Today only `--constitutional-pipeline` produces it. `ask --question-family` and fixed diagnostics mostly bypass it.

After external syntax is decoded, `BoundedConstitutionalQuestion` or an equivalent repository-established bounded inquiry artifact should own inquiry semantics regardless of prose, CLI args, JSON, or machine representation.

## 10. Operator-authority treatment

- Information requests: CLI diagnostics/read models are read-only unless diagnostic recording is explicitly supported.
- Internal examination: fixed diagnostics perform bounded internal projections/audits.
- Passive observation: `--observe`/related ingestion paths append observations and are separate from free-form prompt.
- Active external movement: current runtime refuses free-text movement authority; action plans are described as experimental/legacy safe text paths.
- Presentation choice: `--json`, `--presentation`, and pipeline `output_format` encode presentation preferences.
- Risk acceptance: no free-form authority/risk binding was found in the prompt path.

Current CLI flags carry authority implicitly by selecting command families: read-only flags remain read-only by implementation; observation flags ingest; diagnostic record flags can write diagnostic facts; runtime free text cannot authorize movement.

## 11. Constitutional inquiry pipeline

Implemented stages:

| Stage | Producer | Artifact | Consumer | Responsibility | Used by prompt? | Used by CLI? | Status |
|---|---|---|---|---|---|---|---|
| explicit request | argparse/main | `ConstitutionalPipelineRequest` | `invoke_constitutional_pipeline` | collect explicit already-bounded fields | no | `--constitutional-pipeline` | established structured road |
| bounded inquiry | `produce_bounded_constitutional_question` | `BoundedConstitutionalQuestion` | question projection | preserve explicit testimony/fields, no NL classification | no | pipeline only | established but manual |
| question projection | `project_constitutional_question` | `ConstitutionalQuestionProjection` | selection | exact selection keys from caller fields | no | pipeline only | established narrow |
| capability projection | `project_constitutional_capabilities` | tuple projections | selection | registered view capability keys | no | pipeline only | established narrow |
| view selection | `select_constitutional_views` | `SelectedConstitutionalViews` | composition adapter | exact-key deterministic matching | no | pipeline only | established narrow |
| composition request | `selected_constitutional_views_to_composition_request` | `ConstitutionalViewCompositionRequest` | composition | pass selected view names and output format | no | pipeline only | established |
| composition | `build_constitutional_view_composition` | `ConstitutionalViewCompositionArtifact` | renderer/json | compose requested registered constitutional views | no | pipeline/direct composition | established but limited |
| explanation rendering | `format_constitutional_pipeline_result` / JSON function | text/dict | print | human/JSON presentation | no | pipeline only | partial/compressed |

## 12. Fixed diagnostic surface analysis

Fixed diagnostics are not the constitutional view system itself. They are registered CLI/report surfaces that often combine projection, result assembly, and human/JSON rendering. Diagnostic inventory and shape audit register and check those surfaces. The constitutional view system exists separately and currently covers three registered constitutional read-model views plus explicit composition. Examples such as ownership discrepancies, classification coverage, knowledge reachability, source navigation/selection path, and diagnostic inventory are prebuilt diagnostics or visibility views, not dynamic selectors over arbitrary micro-projections.

## 13. Dynamic view hypothesis

The repository can compose several selected registered constitutional views into one artifact only when requested views are already registered and selected by explicit keys or names. It cannot currently satisfy `What owns storage on node115, what evidence supports that conclusion, and what prevents stronger attribution?` without a named diagnostic/surface or new projection because ownership/storage/evidence/limitations/Unknowns are not exposed as selectable constitutional view components in the implemented constitutional selection/composition registry.

## 14. Dynamic-view boundaries

`ConstitutionalViewCompositionArtifact` preserves boundedness: request, contributing views, existing evidence, Unknowns, explicit refusals, compatibility answer, read-only boundaries, no ledger writes, no cluster mutation. Missing boundary: inquiry decomposition/capability projection over domain-specific operational views. The current composition artifact is lawful but too small and registered-view-only.

## 15. Micro-projection composition analysis

Many diagnostics own their own builders, predicates, filtering, sorting, explanation assembly, JSON functions, and formatters. Some reusable read-model registrations and diagnostic inventories exist, but dynamic composition over small reusable constitutional projections is not generally implemented. Pressure points: command-specific grammar in argparse, direct `print(json.dumps(...))` in CLI branches, diagnostic-specific formatters, and fixed dispatch maps.

## 16. View creation versus composition

- Possibility A, select and compose existing view artifacts: supported for registered constitutional process/governance/fidelity views; partially supported for fixed diagnostics through CLI, but not general.
- Possibility B, project a new bounded view shape from existing constitutional grammar: not generally implemented; would need a lawful projection owner and registry contract.
- Possibility C, generate arbitrary new query/rendering code: not supported and not constitutionally warranted.

Dynamic does not require runtime code generation. It can mean composing known producers selected by a bounded inquiry.

## 17. Internal result versus presentation

For ownership discrepancies and many diagnostics, builders produce typed rows/artifacts and separate JSON/human functions exist. However CLI branches often select the diagnostic, call the builder, choose JSON/human, and print. Human and JSON usually derive from the same result, but presentation selection, rendering, and terminal emission are frequently owned by CLI branches. For constitutional pipeline, `ConstitutionalPipelineResult` is canonical stage-preserving result, with separate JSON and human formatter functions.

## 18. Operator-presentation translation

A distinct universal `project_operator_presentation(...)` owner was not found. Existing renderers are per-surface presentation translators. They are lawful in many cases, but scattered. The missing distinction is not the first blocker for free-form ingress; the first blocker occurs before bounded inquiry production.

## 19. Terminal egress

Terminal egress is mostly direct `print(...)` in `main()` branches and `run_shell()`. There is no clean reusable terminal adapter that only writes a completed presentation artifact, flushes, handles encoding/order/failures, and avoids semantic work. Today CLI branches often select view/result, render, and emit.

## 20. Operator-facing versus operational egress

Operator-facing stdout is separate from operational shell/process execution in the implementation. The runtime refuses free-text movement authority. Some modules discuss external mechanisms/operational realization, but writing an answer to stdout does not authorize arbitrary shell movement. A shared abstract family could be constitutionally bounded egress, but implementation ownership is distinct.

## 21. Bidirectional session topology

Actual session:

```text
Local shell loop
├── terminal input read and strip
├── Runtime unsupported input recording/refusal
└── terminal output print
```

It is bidirectional at the terminal I/O level only. It does not own constitutional conversation state, inquiry lineage, reference resolution, presentation preference, authority scope beyond workspace/session actor fields, or previous result references.

## 22. Multi-turn inquiry analysis

A second prompt cannot refer to the prior bounded result because no bounded result is produced by the first prompt and no discourse/reference-resolution owner exists. Missing owners would include session context, discourse binding, reference resolution, inquiry-family continuation, and view-composition continuation. This is not required for the first free-form slice.

## 23. Prose grammar requirements

A minimal useful grammar would need to separate lexical/domain binding (`node115`, ownership/storage/service), question/request forms (`show`, `what`, `why`, `supports`, `unknown`, `prevents`), scope expression, authority expression, reference resolution for follow-ups, presentation preference (`as JSON`), and domain vocabulary. Full English is unnecessary for an initial bounded slice.

## 24. Inquiry-versus-presentation distinction

`Show me ownership on node115 as JSON` contains inquiry meaning (`ownership` scoped to `node115`) and presentation preference (`JSON`). Current CLI sometimes preserves this (`--json` separate from diagnostic flag), but dispatcher branches still combine result selection, rendering, and terminal emission. `--presentation` in bounded ask selects a question-family explanation rather than merely changing representation, so it mixes presentation-like naming with a different result surface.

## 25. Surface-argument analysis

`surface_args` are temporary CLI syntax and diagnostic-specific implementation parameters. For constitutional pipeline family they include serialized bounded inquiry fields. After free-form ingress exists, a bounded parameter artifact should survive inside the bounded inquiry/projection request. The ad hoc `--surface-args VALUE...` syntax should become only an adapter that decodes into that artifact, not a canonical implementation seam.

## 26. Automation and machine-caller analysis

CLI arguments remain lawful for scripts, tests, cron, remote calls, reproducible inquiries, and compatibility. Strong counterargument: exact structured inputs avoid ambiguity and preserve machine reproducibility. The canonical machine road should likely be a serialized `BoundedConstitutionalQuestion`/pipeline request rather than many bespoke historical flags, but no removal is warranted.

## 27. Error and Unknown handling

Current owners preserve several non-fabrication outcomes:

- unsupported prose: runtime returns `kind="unsupported"` with reason and input event id.
- unknown question family: exact lookup raises parser error.
- missing surface args: parser/eligibility errors.
- unsupported selection key: selection uncertainty records unsupported key.
- unavailable view: composition rejects unsupported registered view names.
- Unknowns/refusals: composition preserves contributing view Unknowns and explicit refusals.
- terminal emission failure: only BrokenPipeError is handled at top level; no presentation-emission artifact.

## 28. Repository proving inquiries

- Existing fixed-view inquiry, `Show the current facts for node115.`: interactive road cannot reach current-facts; fixed CLI `--current-facts node115 <predicate>` can, depending exact args.
- Composed inquiry, ownership/support/Unknowns: no current free-form route; existing diagnostics may cover pieces, but no dynamic selection/composition over ownership evidence and Unknowns.
- Explanation inquiry, stronger service ownership: service ownership authority diagnostic exists as fixed surface; free-form cannot select limitations/authority/dependency/evidence views dynamically.
- Presentation request, `Show that as JSON.`: no multi-turn result binding; CLI `--json` changes many one-shot outputs, but recomputation commonly occurs per command.
- Unsupported prediction: runtime properly refuses free text rather than fabricating prediction.

## 29. CLI equivalence proving case

Proved for constitutional pipeline only in one direction:

```text
CLI --constitutional-pipeline + explicit fields
→ ConstitutionalPipelineRequest
→ BoundedConstitutionalQuestion
→ projection/selection/composition
→ result
```

Disproved for free-form equivalence today:

```text
free-form expression
→ RuntimeResponse(kind="unsupported")
```

The two cannot yet converge at runtime because prose is never interpreted into the bounded inquiry artifact.

## 30. Dynamic-view proving case

Inquiry: `What owns storage on node115, why does Seed believe that, and what blocks stronger confidence?`

Smallest conceptual component set: current ownership projection, storage/host scope projection, supporting observations/evidence, provenance, discrepancies/conflicts, authority limitations, dependency limitations, Unknowns, next lawful examination. Existing source fragments likely include current facts, ownership discrepancies, service/container ownership authority, observation permission/domain coverage, knowledge reachability, and selection/reasoning path audits. Selection reasons and composition roles are currently embedded in named diagnostics rather than exposed as selectable constitutional micro-views. Missing responsibilities: inquiry decomposition, capability projection over operational/domain projections, dynamic view selection, and broader bounded composition. Presentation is later.

## 31. Ownership matrix

| Responsibility | Current producer | Current artifact | Current consumer | Status | Canonical or scaffolding | Missing/compressed owner |
|---|---|---|---|---|---|---|
| raw interactive expression | `run_shell`/terminal | stripped string | `LocalSeedApp.run` | partial | scaffolding | raw unstripped preservation |
| operator attribution | `Runtime.handle_user_message` | event actor `user`, workspace/session | ledger/readers | partial | established for events | operator identity beyond actor string |
| authority/scope binding | CLI flags/runtime refusal | command semantics/refusal event | dispatch/runtime | compressed | mixed | explicit operator authority ingress |
| prose grammar application | none | none | none | missing | missing | free-form grammar owner |
| inquiry interpretation | manual CLI fields | `ConstitutionalPipelineRequest` fields | bounded question producer | partial | canonical structured slice | expression-to-bounded-inquiry producer |
| structured CLI decoding | argparse/main | argparse namespace/handoffs | command branches | established | compatibility/mixed | canonical structured request decoder |
| bounded constitutional inquiry | bounded question module | `BoundedConstitutionalQuestion` | question projection | established | canonical candidate | free-form producer missing |
| inquiry decomposition | exact selection key extraction | `ConstitutionalQuestionProjection` | selection | partial | narrow canonical | semantic decomposition owner |
| capability projection | constitutional selection module | capability projections | selection | partial | narrow canonical | operational/domain capability projections |
| view candidate enumeration | read-model contracts/builders | registered names/keys | capability projection | partial | canonical for three views | general inventory of constitutional views |
| constitutional view selection | selection module | `SelectedConstitutionalViews` | composition adapter | established narrow | canonical slice | dynamic selector over broader views |
| selected-view preservation | selection artifact | selected names/uncertainty | composition | established | canonical slice | richer selection rationale |
| view composition | composition module | composition artifact | renderer/json | established narrow | canonical slice | broader composition owner |
| dynamic view projection | none general | none | none | missing | missing | bounded custom projection owner |
| bounded explanation | composition/pipeline | composition artifact/pipeline result | formatters | partial | canonical slice | domain explanation composition |
| presentation selection | argparse `--json`, `--presentation`, output_format | booleans/fields | CLI branches/renderers | compressed | mixed | presentation request artifact |
| human presentation translation | per-surface formatters | strings | `print` | partial | established per surface | universal presentation translator absent |
| JSON presentation translation | `*_json`, `to_plain`, `json.dumps` | dict/text JSON | `print` | partial | established per surface | JSON artifact vs emission boundary |
| terminal emission | `print` in CLI/shell | stdout bytes/text | terminal | compressed | scaffolding | terminal adapter |
| interactive session state | `run_shell`, workspace/session ids | none durable except events | runtime/ledger | partial | convenience wrapper | session context owner |
| multi-turn reference binding | none | none | none | missing | missing | discourse/reference owner |
| machine-readable inquiry | pipeline flags/JSON-ready result | request fields | pipeline | partial | canonical candidate | serialized bounded inquiry endpoint |
| CLI compatibility | argparse maps | namespace/handoffs | command branches | established | compatibility | none |

## 32. Complete current trace

For `seed`, then entered prompt `What owns storage on node115?`:

1. `scripts/seed_local.py:main()` builds and parses empty args.
2. No diagnostic/read-model branch matches.
3. `build_local_app(...)` constructs runtime/ledger/projector.
4. `run_shell(app, ...)` prints banner to stderr.
5. Prompt loop calls `input("seed> ").strip()`.
6. Text is not `exit`, `quit`, or empty.
7. `app.run(text)` calls `runtime.handle_user_message(workspace, session, text)`.
8. Runtime appends `input.user_message` with payload `text` and actor `user`.
9. Runtime appends `runtime.decision_authority_unsupported` with reason and removed boundary.
10. Runtime returns unsupported response.
11. `format_cli_output` calls `format_response_summary`; no constitutional artifact is produced.
12. `run_shell` prints the formatted response to stdout.

Missing arrows: prose grammar application; authority/scope binding; bounded constitutional question production; question projection; capability projection; view selection; view composition; presentation artifact production; clean terminal egress adapter.

## 33. Target-neutral trace

```text
external operator representation
→ decoded operator expression with provenance and authority/scope claims
→ canonical bounded inquiry
→ inquiry decomposition and capability projection
→ selected bounded views
→ constitutional result/composition preserving evidence, provenance, Unknowns, refusals
→ requested presentation representation
→ operator-facing boundary emission
```

Required responsibilities: decode representation, bind provenance/authority/scope, produce bounded inquiry, decompose inquiry into lawful view demands, enumerate/project capabilities, select views, compose result, translate presentation, emit without semantic mutation.

## 34. Strongest supporting evidence

- The runtime refuses free-text authority and records unsupported response instead of routing prose.
- `BoundedConstitutionalQuestion` explicitly owns only explicit caller inputs and says it performs no natural-language classification or view selection.
- Question projection extracts only exact caller-declared selection keys.
- Selection performs deterministic exact-key comparison only.
- Composition accepts explicitly requested registered constitutional views only.
- `ask --question-family` maps exact family text to existing inquiry surfaces and forwards surface args unchanged.

## 35. Strongest counterevidence

- Structured CLI is heavily implemented, tested, and inventory-backed; it may intentionally be the stable public interface for exactness and automation.
- The constitutional pipeline already exists as a fully structured command requiring explicit bounded fields, suggesting structured inquiry can be canonical.
- The free-form prompt may be only a legacy convenience wrapper after model decision authority was excised.
- Fixed diagnostics have registries and shape audits, so they are not merely accidental scaffolding.
- Exact CLI flags preserve reproducibility and ambiguity control that prose cannot provide alone.
- Current composition explicitly refuses unsupported view names, which is lawful boundedness, not deficiency by itself.

## 36. Supported conclusions

- Today `seed` without args is an interactive unsupported free-text shell, not a constitutional bidirectional interface.
- Raw operator text is preserved after `.strip()` in the event ledger payload; input provenance is workspace/session/actor/event based, not rich operator identity.
- Authority and scope are not inferred from prose; free-text movement authority is refused.
- CLI arguments frequently bypass constitutional interpretation by supplying exact family, command, surface args, selection keys, or already-bounded fields.
- CLI and prose can converge on `BoundedConstitutionalQuestion`, but only CLI pipeline does so today.
- Fixed diagnostics are prebuilt surfaces/compositions, not the complete dynamic constitutional view system.
- Dynamic bounded composition is partially possible only for registered constitutional views; domain-specific arbitrary inquiry composition is not currently possible.
- Human/JSON rendering is usually separate from typed result construction, but CLI branches compress selection, rendering choice, and print emission.
- Terminal emission is not a distinct clean boundary.

## 37. Unsupported conclusions

- It is unsupported to claim free-form session is currently canonical.
- It is unsupported to claim CLI commands should be removed.
- It is unsupported to claim arbitrary English parsing or runtime code generation is required.
- It is unsupported to claim JSON is the canonical constitutional artifact.
- It is unsupported to claim fixed diagnostics are useless scaffolding.
- It is unsupported to claim dynamic composition is fully implemented.

## 38. Interface classification

D. The repository does not yet contain enough ownership to identify a canonical interface.

## 39. CLI classification

4. CLI commands mix canonical structured inquiry with historical diagnostic dispatch.

## 40. View classification

III. Fixed diagnostics mix projection, composition, and presentation, preventing dynamic view construction.

## 41. Presentation classification

β. Rendering currently mixes constitutional composition with presentation translation.

## 42. First-missing-boundary classification

b. Operator-expression-to-bounded-inquiry interpretation is first missing.

## 43. Exact next bounded boundary

Responsibility to recover: translate an already-read operator expression into explicit bounded inquiry fields or a refusal/clarification outcome.

Current missing/compressed owner: no owner between `run_shell`/`Runtime.handle_user_message` and `produce_bounded_constitutional_question`.

Producer: future operator-expression interpretation boundary.

Input artifacts: operator expression text, event/provenance fields, workspace/session/operator attribution, allowed authority/scope context, minimal bounded grammar result.

Output artifact or handoff: `BoundedConstitutionalQuestion` inputs or a typed unsupported/ambiguous/clarification-required refusal.

Immediate consumer: `produce_bounded_constitutional_question` / constitutional pipeline request construction.

Manual responsibility eliminated: operator no longer has to supply `--bounded-question`, `--constitutional-intent`, `--scope-status`, and `--selection-key` for simple bounded inquiries.

Compatibility treatment: existing CLI flags remain adapters that can still supply explicit structured fields.

Explicit exclusions: no full English parser, no arbitrary query generation, no general chatbot, no dynamic code generation, no CLI/diagnostic removal, no renderer redesign, no multi-turn discourse, no predicate cleanup, no shell/process changes.

## 44. Implementation-warrant decision

One bounded implementation slice is warranted.

## 45. Files changed

- `free_form_operator_interface_dynamic_view_topology_audit_001.md` only.

## 46. Probes executed

- `find .. -name AGENTS.md -print`
- `git status --short`
- `rg -n "prose.*support|free.form|interactive|repl|prompt>|input\(|readline|while.*input|seed>" scripts seed_runtime tests || true`
- `rg -n "argparse|add_argument|add_subparsers|question.family|surface.args|presentation|ask|current.facts|ownership.discrepancies" scripts seed_runtime tests || true`
- `rg -n "BoundedConstitutionalQuestion|QuestionProjection|CapabilityProjection|ConstitutionalViewSelection|SelectedConstitutionalViews|ConstitutionalViewComposition|BoundedConstitutionalExplanation" seed_runtime tests scripts || true`
- `rg -n "def main|if __name__|add_argument|subparsers|def interactive|input\(" scripts seed_runtime | head -300`
- `rg -n "class LocalSeedApp|def run\(|free-text|runtime decision authority|format_cli_output|def raw" scripts/seed_local.py seed_runtime -n`
- `printf 'What owns storage on node115?\nexit\n' | python scripts/seed_local.py 2>&1 | sed -n '1,120p'`

## 47. Tests executed

- `pytest -q tests/test_constitutional_pipeline.py tests/test_bounded_constitutional_question.py tests/test_constitutional_view_selection.py tests/test_diagnostic_inventory.py tests/test_diagnostic_shape_audit.py` — passed, 130 tests.

## 48. Confidence statement

High confidence for current interactive behavior, bounded question pipeline ownership, exact-key selection, registered-view-only composition, and CLI dispatch compression. Medium confidence for broad diagnostic micro-projection duplication because the repository has many diagnostic modules and this audit used focused representative inspection rather than exhaustive body-by-body review.
