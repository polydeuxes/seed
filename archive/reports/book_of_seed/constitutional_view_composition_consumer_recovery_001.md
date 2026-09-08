# Constitutional View Composition Consumer Recovery 001

## Scope and method

This recovery is consumer-only. It uses `SelectedConstitutionalViews` only as the artifact name under examination and does not inspect upstream selection mechanics to infer consumer requirements.

Method used:

```text
constitutional grammar
→ consumer expectation
→ consumer witness
→ faithful within consumer scope / unfaithful crossing / Unknown
```

## Book grammar consumed

The grammar consumed for this pass is limited to the requested consumer distinctions:

- producer output is not automatically a consumer requirement;
- selected identity is not selection occurrence proof;
- consumer acceptance is not upstream admission renewal;
- consumer-local validation is not producer validation;
- consumer use is not producer standing reproduction;
- composition request is not composed explanation;
- representation selection is not consideration selection;
- selected representation is not sufficient explanation;
- consumer-local assertion is not reusable upstream warrant;
- available, applicable, admitted, consumed, sufficient, warranted, and authorized are separate standings.

The grammar expectation for a faithful consumer is therefore narrow: the consumer may assert only what it independently consumes, validates, constructs, preserves, or refuses within its own boundary.

## Consumer implementation inspected

Implementation witness inspected:

- `seed_runtime/constitutional_view_composition.py`
- `tests/test_constitutional_view_composition.py`
- CLI dispatch only where it directly creates and renders the composition request in `scripts/seed_local.py`

No upstream selection implementation was inspected for this recovery.

## Responsible consumer question

The consumer answers this bounded implementation question:

```text
Given an explicit ConstitutionalViewCompositionRequest naming registered constitutional views, a purpose label, an output format intent, optional bounded-question identity, and optional upstream selection limits, can this boundary build only those requested registered read-only constitutional view artifacts and return one immutable bounded explanation artifact that correlates existing evidence while preserving selection uncertainty, Unknowns, refusals, and read-only / non-authority boundaries?
```

This question is about composition from an explicit request, not about whether a lawful selection occurrence happened upstream.

## Consumer-local subject

Composition acts first on the **composition request**, then on **requested view names**, then on **registered view instances built locally**.

Distinctions recovered:

| Identity | Consumer witness | Standing |
| --- | --- | --- |
| Request identity | The `ConstitutionalViewCompositionRequest` object is embedded unchanged in the output artifact. | Preserved request testimony, not selection proof. |
| Selected representation identity | The `requested_views` tuple names requested registered views. | Validated as registered/buildable identity before construction. |
| Built view identity | Each requested name indexes a read-model contract and local builder, then becomes a `ConstitutionalContributingView.name`. | Consumed representation identity. |
| Composition result identity | Output artifact name is fixed as `Constitutional View Composition`. | Consumer-local artifact identity only. |
| Bounded question identity | Optional `bounded_question_id` is preserved when supplied and rendered as `none` when absent. | Passed-through identity only, not validated as true or sufficient. |

## Inputs actually required

| Input | Classification | Consumer witness |
| --- | --- | --- |
| `requested_views` | Required by request shape; validated and consumed by builder. | Converted to tuple by request helper; each name is checked against contracts and local builders. |
| `composition_purpose` | Defaulted and passed through; rendered. | Defaults to `bounded_explanation`; no bounded-purpose validation beyond being stored/rendered is evidenced. |
| `output_format` | Defaulted and passed through; used by CLI dispatch, not by composition builder. | Defaults to `human`; CLI passes `json` or `human`; builder stores it in request. Unsupported literal is type-level only, not runtime-refused by builder. |
| `bounded_question_id` | Optional, passed through. | Stored in request and rendered/json-emitted; no independent lookup or validation is evidenced. |
| `selection_uncertainty` | Optional, passed through and consumed for preservation. | Stored in request; copied to `preserved_selection_uncertainty` and prepended into `preserved_unknowns`. |
| `selection_read_only_boundaries` | Optional, accepted but ignored by current builder output. | Stored in request; no read from this field is evidenced in `build_constitutional_view_composition`. |
| Registered read-model contracts | Looked up and validated. | Name-to-contract map is reconstructed from `CONSTITUTIONAL_READ_MODEL_CONTRACTS`; requested names must appear. |
| Local builder / JSON renderer map | Looked up and validated. | Requested names must appear in `_BUILDERS`; builder and JSON renderer are used to construct payloads. |
| View contents | Constructed locally and consumed selectively. | Builders create view objects; JSON renderers produce payloads; composition reads only specific payload keys. |
| Compatibility answers | Consumed selectively. | `compatibility_answer` is read from each payload to produce a combined `No.` only when all are `No.`, otherwise `Unknown.` |
| Read-only constraints | Produced locally, not validated from request. | Artifact hard-codes read-only flags and read-only boundary statements. |
| Selection keys | Not consumed. | No field or read path in the consumer uses selection keys. |
| Capability keys | Not consumed. | No field or read path in the consumer uses capability keys. |
| Candidate-set identity | Not consumed. | No field or read path in the consumer uses candidate-set identity. |
| Matched-key basis | Not consumed. | No field or read path in the consumer uses matched-key basis. |
| Non-selected candidates | Not consumed. | No field or read path in the consumer uses non-selected candidates. |
| Producer occurrence proof | Not consumed. | No field or read path in the consumer uses proof that selection occurred. |
| Producer provenance | Unknown / not consumed in composition boundary. | No provenance field is part of the request shape; no producer provenance read is evidenced. |

## Fields read, validated, forwarded, ignored, or Unknown

### Request fields

| Field | Present | Read | Validated | Forwarded | Affects composition | Rendered | Ignored / Unknown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `requested_views` | Yes | Yes | Yes, against contracts and `_BUILDERS`. | Yes, inside `artifact.request`. | Yes, determines build loop and contributing views. | Yes. | Not ignored. |
| `composition_purpose` | Yes | No builder decision read evidenced beyond request embedding. | No. | Yes. | No composition logic effect evidenced. | Yes. | Runtime purpose boundedness validation is Unknown/not evidenced. |
| `output_format` | Yes | No builder decision read evidenced beyond request embedding. | Type-level literal only; no runtime check evidenced. | Yes. | No builder logic effect evidenced. | Not directly rendered except via JSON request. | Unsupported runtime value behavior is Unknown if dataclass constructed directly. |
| `bounded_question_id` | Yes | No builder decision read evidenced beyond request embedding. | No. | Yes. | No composition logic effect evidenced. | Yes. | Identity correctness is Unknown. |
| `selection_uncertainty` | Yes | Yes. | No truth validation. | Yes. | Yes, copied into preserved fields. | Yes. | Not ignored. |
| `selection_read_only_boundaries` | Yes | No. | No. | Yes through embedded request only. | No artifact boundary merge evidenced. | JSON request only. | Ignored for local `read_only_boundaries`. |

### Built view payload fields

| Payload field | Present in possible payload | Read | Validated | Forwarded | Affects composition | Rendered | Ignored / Unknown |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `composition` | Yes | Yes. | No semantic validation. | Yes as contributing evidence and correlated evidence. | Yes, builds `correlated_existing_evidence`. | Yes. | Not ignored. |
| `unknowns` | Yes | Yes. | No semantic validation. | Yes as per-view and preserved Unknowns. | Yes. | Yes. | Not ignored. |
| `explicit_refusals` | Some views. | Yes through default empty tuple. | No semantic validation. | Yes as per-view and preserved refusals. | Yes. | Yes. | Not ignored. |
| `compatibility_answer` | Yes. | Yes through default `Unknown.`. | No semantic validation. | Not directly per-view except inside full payload. | Yes, determines combined compatibility answer. | Combined answer rendered. | Stronger compatibility meaning is not established. |
| Contract `cli_flag`, `inventory_name`, `shape_audit_name` | Yes. | Yes. | Name lookup only. | Yes in contributing view. | Affects contribution metadata. | CLI flag rendered. | Diagnostic standing is not re-audited. |
| Other payload fields | Unknown / adjacent. | Not evidenced. | Not evidenced. | Full `artifact` payload is forwarded inside each contributing view. | No direct composition effect evidenced. | JSON only via full artifact. | Field-level consumption remains Unknown unless one of the keys above. |

## Applicability, admission, and consumption findings

- Applicability: not independently established as a constitutional participation standing. The consumer validates requested names against registered contracts and builder availability, then constructs those views.
- Admission: not established. Registered identity validation and successful construction are not treated as admitted, unadmitted, conflicting, or Unknown participation standing by this implementation.
- Consumption: every requested view that passes validation is built and represented as a `ConstitutionalContributingView`. The consumer then actually consumes selected payload fields from each built view.
- Requested material can remain unconsumed at field granularity: the full payload is embedded, but only `composition`, `unknowns`, `explicit_refusals`, and `compatibility_answer` are evidenced as affecting composition logic.
- Refusal is supported for unsupported requested view names through `ValueError`.
- Omission / partial composition for invalid requested names is not evidenced; invalid names stop the composition before artifact production.
- Unknown is preserved from upstream `selection_uncertainty` and from view-local `unknowns`; it is not resolved.

## Consumer-local validation

Validated:

- each requested view name must be present in registered constitutional read-model contracts;
- each requested view name must be present in the local builder / JSON renderer map.

Not validated or not evidenced:

- view identity after builder return is not compared to the requested name except by using the requested name in the contributing view record;
- output format is not runtime-validated by the builder;
- composition purpose boundedness is not runtime-validated;
- bounded question identity is not looked up or verified;
- selection uncertainty is preserved but not checked for truth;
- `selection_read_only_boundaries` are accepted and embedded in the request but not merged into local boundary assertions;
- per-view semantic correctness is not checked;
- producer occurrence, candidate-set identity, selection keys, capability keys, matched-key basis, and non-selected candidates are not checked.

Validation failure witnessed:

- unknown or unsupported requested view name raises `ValueError` saying composition only accepts registered constitutional views and listing unsupported and supported names.

## Actual representation consumption

For each requested registered/buildable view, composition:

1. looks up the read-model contract by requested name;
2. looks up the builder and JSON renderer by requested name;
3. builds the view object locally;
4. renders it to a JSON-ready payload;
5. creates a contributing-view record with requested name, contract metadata, full payload, and selected per-view contribution fields;
6. appends payload `composition` entries to correlated existing evidence;
7. prefixes payload `unknowns` with the view name and preserves them;
8. prefixes payload `explicit_refusals` with the view name and preserves them;
9. reads payload `compatibility_answer` to compute the artifact-level compatibility answer.

The consumer does not evidence consumption of selection occurrence proof, candidate-set identity, selection keys, capability keys, matched-key basis, non-selected candidates, or producer provenance.

## Failure and partial outcomes

| Outcome | Witnessed result |
| --- | --- |
| Zero requested views | Supported by implementation path: no unknown requested names, empty loop, empty contributing views/evidence/unknowns/refusals, combined compatibility becomes `No.` because `all([])` is true. Whether this is constitutionally intended is Unknown. |
| Unknown requested view | Refusal by `ValueError`; no artifact. |
| Missing builder for registered view | Refusal by same unsupported-name path because names must be in both contracts and `_BUILDERS`. |
| Partially available views | No partial artifact evidenced; any unknown/missing name raises before building. |
| Unsupported output format | No builder-level refusal evidenced; behavior is Unknown if direct dataclass construction bypasses typing. |
| Upstream selection uncertainty | Preserved in `preserved_selection_uncertainty` and also in `preserved_unknowns`. |
| View-local Unknown | Preserved with view-name prefix. |
| Conflicting view material | No explicit conflict taxonomy evidenced; compatibility aggregation can yield `Unknown.` unless all answers are `No.`. |
| Composition refusal | Witnessed for unsupported registered/buildable identity. |
| Producer proof absent | No refusal evidenced because consumer does not require producer proof. |

## Artifact produced

The produced artifact is `ConstitutionalViewCompositionArtifact` with:

- fixed name: `Constitutional View Composition`;
- embedded request;
- tuple of `ConstitutionalContributingView` records;
- bounded summary;
- deduplicated correlated existing evidence;
- preserved selection uncertainty;
- preserved Unknowns;
- preserved refusals;
- aggregate compatibility answer;
- local read-only boundaries;
- `read_only=True`;
- `mutates_cluster=False`;
- `writes_event_ledger=False`.

This artifact is a consumer-local composition artifact, not proof of selection occurrence, not a sufficient answer, not authority, not constitutional movement, and not a reusable upstream warrant.

## Standing produced

The consumer-local standing produced is:

```text
these explicitly requested names were accepted as registered/buildable constitutional read-model identities, built locally as read-only views, and composed into one bounded explanation artifact that correlates existing evidence and preserves supplied uncertainty, view Unknowns, refusals, and non-authority boundaries.
```

Standing not produced:

- no upstream selection occurrence proof;
- no candidate-set completeness;
- no selection-key match;
- no capability-key match;
- no admission standing;
- no evidence sufficiency;
- no truth determination;
- no goal binding;
- no inquiry movement;
- no authorization;
- no execution;
- no recording;
- no event-ledger mutation;
- no cluster mutation.

## Negative authority

The consumer explicitly refuses or does not establish stronger authority through its request docstring, bounded summary, flags, and read-only boundary text.

| Stronger claim | Consumer-side finding |
| --- | --- |
| Producer occurrence | Not established; not consumed. |
| Candidate-set completeness | Not established; not consumed. |
| Selection-key match | Not established; not consumed. |
| Capability-key match | Not established; not consumed. |
| Semantic correctness | Not established. |
| Evidence sufficiency | Not established. |
| Truth | Not established. |
| Goal binding | Not established. |
| Inquiry movement | Not established. |
| Authorization | Explicitly refused as no constitutional authority / no implementation authority. |
| Execution | Not established. |
| Recording | Explicitly refused. |
| Event-ledger mutation | Explicitly false. |
| Cluster mutation | Explicitly false. |

## Consumer-side Fidelity finding

Finding: **faithful within consumer scope, with preserved Unknowns**.

No consumer-side Fidelity crossing is established in this pass because the inspected consumer does not claim producer occurrence, does not treat selected names as proof of lawful selection, does not establish admission from registration, does not claim explanation sufficiency, preserves supplied selection uncertainty, does not strengthen compatibility beyond its local aggregation rule, and keeps representation separate from authority or movement.

Caveats preserved as Unknown rather than crossings:

- zero requested views yields an artifact with aggregate compatibility `No.` due to empty `all(...)`; no implementation evidence states the constitutional meaning of that case;
- output-format support is not builder-validated when a malformed request object is constructed directly;
- `selection_read_only_boundaries` are accepted but not incorporated into artifact-level `read_only_boundaries` except through embedded request serialization;
- full per-view payloads are forwarded even though only some fields affect composition logic.

## Realization-invariant expectation

A realization-invariant Constitutional View Composition consumer requires:

1. a bounded composition request or equivalent testimony containing requested representation identities, purpose/output intent, optional bounded-question identity, and optional uncertainty/boundary notes;
2. a way to validate requested representation identities against locally recognized registered view contracts or equivalent registry evidence;
3. a way to obtain or construct the requested read-only view representations locally;
4. a way to preserve sufficient identity linkage between requested identity, built representation, and composition result;
5. selective consumption of representation contribution material, Unknowns, refusals, and compatibility testimony sufficient for the consumer-local assertion;
6. refusal or Unknown preservation when a requested representation cannot be validated or constructed;
7. explicit negative authority preserving that composition is not selection proof, admission, sufficiency, truth, authorization, recording, execution, or mutation.

This expectation does not require the current Python dataclasses specifically. Equivalent objects, rows, serialized references, query results, or distributed representation testimony could satisfy the consumer if they preserve identity, scope, uncertainty, local validation, consumed material, bounded assertion, and negative authority.

## Preserved Unknowns

- Whether zero requested views should be treated as a meaningful composed explanation, a refusal, or an empty artifact is Unknown.
- Whether output formats outside `human` and `json` can occur through all call paths is Unknown; type hints constrain ordinary construction but no runtime builder refusal is evidenced.
- Whether `selection_read_only_boundaries` should affect artifact-level boundary text is Unknown; current consumer embeds but does not otherwise consume them.
- Whether forwarded full view payload fields beyond the explicitly consumed keys have downstream meaning is Unknown.
- Whether conflicting per-view material should produce a dedicated conflict standing is Unknown.
- Whether the consumer should validate view identity inside the built payload is Unknown.
- Whether a bounded question identity, when supplied, is true or belongs to the request is Unknown.
- Whether selection uncertainty is complete is Unknown; the consumer only preserves what it receives.

## Closing questions

### What does Constitutional View Composition independently require?

It independently requires an explicit bounded composition request naming requested views, plus local registered read-model contracts and local builders / JSON renderers for those names. It requires enough view payload material to correlate existing evidence, preserve Unknowns and refusals, and aggregate compatibility testimony.

### What does it actually consume from the selection artifact?

From the selection-side handoff as represented at the composition boundary, it actually consumes requested view names, optional bounded-question identity, and selection uncertainty. It accepts selection read-only boundary notes in the request but no builder consumption of that field is evidenced. It does not consume selection occurrence proof, candidate-set identity, selection keys, capability keys, matched-key basis, non-selected candidates, or producer provenance.

### What additional material does it obtain or construct locally?

It reconstructs a contract lookup from registered constitutional read-model contracts, looks up local builders and JSON renderers, builds each requested view locally, renders each view to payload form, extracts contribution evidence / Unknowns / refusals / compatibility answers, and constructs one immutable composition artifact with local read-only and non-mutating boundaries.

### What bounded assertion does it produce?

It asserts that explicitly requested registered/buildable constitutional read-model views were composed read-only into one bounded explanation artifact that correlates existing evidence and preserves supplied selection uncertainty, view-local Unknowns, explicit refusals, and non-authority / non-mutation boundaries.

### Does it require proof of selection occurrence, candidate-set identity, or matched-key basis?

No consumer witness shows that it requires any of those. They are not consumed by the composition boundary.

### What uncertainty or refusal survives?

Supplied selection uncertainty survives in `preserved_selection_uncertainty` and `preserved_unknowns`. View-local Unknowns survive with view-name prefixes. View-local explicit refusals survive with view-name prefixes. Unsupported requested view identity refuses composition with `ValueError`. Other failure or conflict standings remain Unknown unless evidenced above.

### Is any consumer-side Fidelity crossing established?

No. The consumer is faithful within its bounded scope on the inspected evidence, with preserved Unknowns and caveats rather than an established crossing.

### What exact consumer witness is now ready for a later producer-consumer cross-examination?

The witness is: `ConstitutionalViewCompositionRequest` supplies requested view names, purpose/output intent, optional bounded-question identity, selection uncertainty, and boundary notes; `build_constitutional_view_composition(...)` validates requested names only against registered contracts and local builders, builds and renders each requested view, consumes payload `composition`, `unknowns`, `explicit_refusals`, and `compatibility_answer`, preserves request identity and uncertainty, produces `ConstitutionalViewCompositionArtifact`, refuses unsupported requested names, and does not consume or establish producer occurrence, candidate-set identity, selection-key match, capability-key match, matched-key basis, non-selected candidates, admission, sufficiency, truth, authorization, recording, event-ledger writes, or cluster mutation.
