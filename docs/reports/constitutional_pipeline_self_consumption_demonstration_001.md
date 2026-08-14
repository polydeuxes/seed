# Constitutional Pipeline Self-Consumption Demonstration 001

## Orientation verification

Repository authority was inspected before running the demonstration. The required implementation reports all exist:

- `bounded_constitutional_question_implementation_001.md`
- `constitutional_question_projection_implementation_001.md`
- `constitutional_capability_projection_implementation_001.md`
- `constitutional_pipeline_invocation_implementation_001.md`
- `constitutional_pipeline_public_surface_implementation_001.md`
- `constitutional_pipeline_diagnostic_implementation_001.md`
- `constitutional_pipeline_provenance_explanation_implementation_001.md`
- `constitutional_pipeline_integration_wiring_001.md`

Current code supports this integrated path:

```text
ask --question-family "constitutional pipeline" --surface-args ...
  -> bounded ask admission / eligibility / dispatch
  -> --constitutional-pipeline
  -> ConstitutionalPipelineRequest
  -> invoke_constitutional_pipeline(...)
  -> ConstitutionalPipelineResult
  -> provenance explanation
```

Implementation evidence reviewed: `seed_runtime/question_surface_inventory.py` registers `constitutional pipeline` as `constitutional_pipeline`, declares the bounded args `operator_inquiry`, `inquiry_source`, `bounded_question`, `constitutional_intent`, `scope_status`, `selection_key`, and maps them to the existing surface. `scripts/seed_local.py` builds `ConstitutionalPipelineRequest` and calls `invoke_constitutional_pipeline(...)`. `seed_runtime/constitutional_pipeline.py` executes bounded question, question projection, capability projection, selection, composition, and provenance explanation.

No newer repository evidence contradicted the reported topology. Existing bounded ask ownership remains distinct from constitutional pipeline ownership: bounded ask admits exact question-family invocation and prepares surface args; the constitutional pipeline owns typed stage execution.

## Branch and starting commit

- Branch: `work`
- Starting commit: `66e1f3fff4422449a0a7ff7648b7eaeabeb470fa`

## Help / dispatch evidence

Commands inspected:

```bash
python scripts/seed_local.py --help
python scripts/seed_local.py ask --help
rg -n "constitutional pipeline|constitutional_pipeline|selection_key|BOUNDED_ASK_REQUIRED_SURFACE_ARGS|BOUNDED_ASK_DISPATCH_SURFACES" seed_runtime scripts tests -S
```

Help exposes `ask --question-family`, `--surface-args`, `--constitutional-pipeline`, `--constitutional-pipeline-diagnostic`, typed pipeline fields, direct repeated `--selection-key`, `--pipeline-unknown`, and JSON rendering. The bounded ask path for this family accepts one exact `selection_key` through `--surface-args`; repeated direct `--selection-key` flags are a public pipeline-surface capability but are not part of the current bounded-ask adapter contract.

## Event-ledger and cluster baseline

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --events-only
sqlite3 /tmp/seed-cp-demo/events.sqlite 'select count(*) as count from events;'
```

Before demonstration:

```text
no events
event_count=0
```

## A. Exact supported key

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator says process should be visible; testimony only." "operator:self-consumption-demo-001" "Which constitutional process surface is available?" "caller supplied bounded constitutional inquiry" "bounded" "process" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:ee510285134b4e6770c194ef80a3a6376a570a523fae515a5786d4398cd5079a",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [
    "process"
  ],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [
    "process"
  ],
  "unsupported_keys": [],
  "selected_views": [
    "constitutional_process"
  ],
  "selection_uncertainty": [],
  "composition_contributors": [
    "constitutional_process"
  ],
  "composition_unknowns": [
    "constitutional_process: Whether every constitutional inquiry starts only as Pressure remains unknown.",
    "constitutional_process: Whether every Recovery requires a separate Cross-Examination artifact remains unknown.",
    "constitutional_process: Whether every Cross-Examination requires a separate Completion Audit remains unknown.",
    "constitutional_process: Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains unknown.",
    "constitutional_process: Whether a single named constitutional process owner exists remains unknown."
  ],
  "composition_refusals": [],
  "empty_selection_explanation": "",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: Exact key `process` projected exactly, matched capability key `process`, selected `constitutional_process`, contributed `Constitutional Process View`, and emitted provenance. Human output was also inspected.

## B. Multiple supported keys

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator supplies three exact keys; testimony only." "operator:self-consumption-demo-001" "Which constitutional views are available?" "caller supplied bounded constitutional inquiry" "bounded" "process governance fidelity" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:0b8fb4940ec1f3f451f15530f0c8c2d0bb6e78b9fc97552cf8e4bd76bd7b9bb3",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [
    "process governance fidelity"
  ],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [],
  "unsupported_keys": [
    "process governance fidelity"
  ],
  "selected_views": [],
  "selection_uncertainty": [
    "unsupported selection key: process governance fidelity",
    "no registered constitutional view matched deterministic projection keys"
  ],
  "composition_contributors": [],
  "composition_unknowns": [],
  "composition_refusals": [],
  "empty_selection_explanation": "No selected view was produced because explicit keys did not match projected capability keys; this is not verified irrelevance.",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: Current bounded-ask repository authority exposes one `selection_key` surface argument. The phrase `process governance fidelity` is preserved as one exact unsupported key; no fuzzy splitting occurs. This is a documentation/usage gap, not a stage failure.

## C. No selection key

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator prose mentions process but key intentionally absent; testimony only." "operator:self-consumption-demo-001" "Which constitutional view should be inferred from prose?" "caller supplied bounded constitutional inquiry" "bounded" "" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:387315ce953dbbc5b36ca4321679f1c6f108bfc358868027f08cbc4cab990a1e",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [],
  "unsupported_keys": [],
  "selected_views": [],
  "selection_uncertainty": [
    "no registered constitutional view matched deterministic projection keys"
  ],
  "composition_contributors": [],
  "composition_unknowns": [],
  "composition_refusals": [],
  "empty_selection_explanation": "No explicit selection key was supplied; empty selection is not verified irrelevance.",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: No key was inferred from prose. Question projection keys are empty, selection is empty, composition has no contributors, and explanation says absence is not verified irrelevance.

## D. Unsupported exact key

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator supplies unsupported exact key; testimony only." "operator:self-consumption-demo-001" "Which unsupported constitutional view matches?" "caller supplied bounded constitutional inquiry" "bounded" "unsupported-explicit-key" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:3fd089bf7d6fa7fdf9fb346e0eca070530176d4e178f6d212dbd812c522ff445",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [
    "unsupported-explicit-key"
  ],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [],
  "unsupported_keys": [
    "unsupported-explicit-key"
  ],
  "selected_views": [],
  "selection_uncertainty": [
    "unsupported selection key: unsupported-explicit-key",
    "no registered constitutional view matched deterministic projection keys"
  ],
  "composition_contributors": [],
  "composition_unknowns": [],
  "composition_refusals": [],
  "empty_selection_explanation": "No selected view was produced because explicit keys did not match projected capability keys; this is not verified irrelevance.",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: Unsupported key remains observable, no semantic/fuzzy match is attempted, unsupported uncertainty remains visible, and no view is invented.

## E. Unknown input

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator supplies Unknown evidence; testimony only." "operator:self-consumption-demo-001" "Which process surface is available with Unknown preserved?" "caller supplied bounded constitutional inquiry" "bounded" "process" --pipeline-unknown "operator assertion not verified" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:cda0a64906baa30b4e923762b98428acd943ba210062e50df9381f0eb0c207a9",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [
    "process"
  ],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [
    "process"
  ],
  "unsupported_keys": [],
  "selected_views": [
    "constitutional_process"
  ],
  "selection_uncertainty": [
    "unknown: operator assertion not verified"
  ],
  "composition_contributors": [
    "constitutional_process"
  ],
  "composition_unknowns": [
    "constitutional_process: Whether every constitutional inquiry starts only as Pressure remains unknown.",
    "constitutional_process: Whether every Recovery requires a separate Cross-Examination artifact remains unknown.",
    "constitutional_process: Whether every Cross-Examination requires a separate Completion Audit remains unknown.",
    "constitutional_process: Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains unknown.",
    "constitutional_process: Whether a single named constitutional process owner exists remains unknown."
  ],
  "composition_refusals": [],
  "empty_selection_explanation": "",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: Unknown survives bounded-question production, question projection as typed uncertainty, and provenance/composition channels. It is not converted into a negative fact.

## F. Refusal contribution

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator asks governance; testimony only." "operator:self-consumption-demo-001" "Which constitutional governance surface contributes?" "caller supplied bounded constitutional inquiry" "bounded" "governance" --json
```

Evidence:

```json
{
  "status": "0",
  "bounded_question_id": "bounded-constitutional-question:3d8dea72dffb585ebd191217b39883e80236ad0f11e5717ed34aa223ce3a1733",
  "inquiry_provenance": "operator:self-consumption-demo-001",
  "question_selection_keys": [
    "governance"
  ],
  "capability_keys": [
    [
      "constitutional_process",
      [
        "process"
      ]
    ],
    [
      "constitutional_governance",
      [
        "governance"
      ]
    ],
    [
      "constitutional_fidelity",
      [
        "fidelity"
      ]
    ]
  ],
  "matched_keys": [
    "governance"
  ],
  "unsupported_keys": [],
  "selected_views": [
    "constitutional_governance"
  ],
  "selection_uncertainty": [],
  "composition_contributors": [
    "constitutional_governance"
  ],
  "composition_unknowns": [
    "constitutional_governance: Whether there is a distinct constitutional governance owner remains Unknown.",
    "constitutional_governance: Whether every recovery requires a separate cross-examination artifact remains Unknown.",
    "constitutional_governance: Whether every cross-examination requires a separate completion audit remains Unknown.",
    "constitutional_governance: Whether the Orientation-to-Recovery handoff has a recoverable constitutional interface remains Unknown.",
    "constitutional_governance: Whether Question Grammar and Inquiry Navigation are distinct competencies remains Unknown.",
    "constitutional_governance: Whether a common owner exists for external-representation recovery families remains Unknown and currently unsupported.",
    "constitutional_governance: Whether governance relationships require any implementation topology remains Unknown because implementation was not inspected."
  ],
  "composition_refusals": [
    "constitutional_governance: governance execution",
    "constitutional_governance: governance ownership",
    "constitutional_governance: constitutional recovery",
    "constitutional_governance: implementation recovery",
    "constitutional_governance: hierarchy",
    "constitutional_governance: runtime governance",
    "constitutional_governance: repository mutation"
  ],
  "empty_selection_explanation": "",
  "testimony": "operator testimony preserved as evidence, not established fact",
  "writes_event_ledger": false,
  "mutates_cluster": false
}
```

Finding: Selected view `constitutional_governance` remains distinguishable from explicit refusals. Composition preserves refusals and provenance reports them without converting the result into full pipeline failure.

## Human-output evidence

Exact-key human output excerpt:

```text
Constitutional Pipeline

Operator input testimony

Operator inquiry supplied: Operator says process should be visible; testimony only.
Inquiry provenance: operator:self-consumption-demo-001
Testimony status: operator testimony preserved as evidence, not established fact

Bounded question

ID: bounded-constitutional-question:ee510285134b4e6770c194ef80a3a6376a570a523fae515a5786d4398cd5079a
Question: Which constitutional process surface is available?
Constitutional intent: caller supplied bounded constitutional inquiry
Scope status: bounded
Uncertainty: none
Unknowns: none

Question projection

Selection keys: process
Read-only: true
Writes event ledger: false
Mutates cluster: false

Capability projection

* constitutional_process: keys=process; compatibility=No.; read_only=true; writes_event_ledger=false; mutates_cluster=false
* constitutional_governance: keys=governance; compatibility=No.; read_only=true; writes_event_ledger=false; mutates_cluster=false
* constitutional_fidelity: keys=fidelity; compatibility=No.; read_only=true; writes_event_ledger=false; mutates_cluster=false

Selected constitutional views

Selected views: constitutional_process
Selection uncertainty: none
Compatibility answer: No.
Read-only: true
Writes event ledger: false
Mutates cluster: false

Composition result

Requested views: constitutional_process
Purpose: bounded_explanation
Compatibility answer: No.
Read-only: true
Writes event ledger: false
Mutates cluster: false

Provenance explanation

Why these views were selected
Question selection keys: process
Available capability keys: constitutional_process=[process]; constitutional_governance=[governance]; constitutional_fidelity=[fidelity]
Matched keys: process
Selected views explained by exact matches: constitutional_process

Why requested keys we
```

Diagnostic human output excerpt:

```text
Constitutional Pipeline Diagnostic

Boundary
- recordability: read-only non-recording diagnostic; record_scope=none
- event ledger: no event-ledger writes
- cluster mutation: no cluster mutation
- testimony: operator testimony is preserved as evidence, not established fact
- diagnostic: observes typed pipeline artifacts only; does not own stage algorithms or constitutional authority

Stages
Pipeline stage | Status | Artifact / counts | Uncertainty / Unknown / refusal summary | Read-only / ledger / mutation
bounded_question | complete | bounded-constitutional-question:3d8dea72dffb585ebd191217b39883e80236ad0f11e5717ed34aa223ce3a1733; selected_views=0, unknowns=0, refusals=0 | none | read_only=true writes_event_ledger=false mutates_cluster=false
question_projection | complete | bounded-constitutional-question:3d8dea72dffb585ebd191217b39883e80236ad0f11e5717ed34aa223ce3a1733; keys=1, selected_views=0, unknowns=0, refusals=0 | none | read_only=true writes_event_ledger=false mutates_cluster=false
capability_projection | complete | capability_projections:3; keys=3, selected_views=0, unknowns=0, refusals=0 | none | read_only=true writes_event_ledger=false mutates_cluster=false
selection | complete | bounded-constitutional-question:3d8dea72dffb585ebd191217b39883e80236ad0f11e5717ed34aa223ce3a1733; selected_views=1, unknowns=0, refusals=0 | none | read_only=true writes_event_ledger=false mutates_cluster=false
composition_request | complete | purpose:bounded_explanation; selected_views=1, unknowns=0, refusals=0 | none | read_only=true writes_event_ledger=false mutates_cluster=false
comp
```

## Diagnostic evidence

Command:

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --constitutional-pipeline-diagnostic --operator-inquiry "Operator asks governance; testimony only." --inquiry-provenance operator:self-consumption-demo-001 --bounded-question "Which constitutional governance surface contributes?" --constitutional-intent "caller supplied bounded constitutional inquiry" --scope-status bounded --selection-key governance --json
```

Evidence:

```text
status=0; stages=[('bounded_question', 'complete', 0, 0, 0, 0, []), ('question_projection', 'complete', 1, 0, 0, 0, []), ('capability_projection', 'complete', 3, 0, 0, 0, []), ('selection', 'complete', 0, 1, 0, 0, []), ('composition_request', 'complete', 0, 1, 0, 0, []), ('composition', 'refused', 0, 1, 7, 7, [])]; writes_event_ledger=False; mutates_cluster=False; event_ledger_status=no event-ledger writes; cluster_mutation_status=no cluster mutation
```

Finding: bounded ask admits and dispatches inquiry; the public pipeline executes and renders the pipeline result; the diagnostic classifies stage conditions; provenance explains typed handoffs and exact matches. These surfaces remain distinct.

## Determinism comparison

Equivalent successful JSON request was run twice and compared:

```bash
cmp -s /tmp/seed-cp-demo/determinism1.out /tmp/seed-cp-demo/determinism2.out
```

- `cmp` exit status: `0`
- Finding: outputs are byte-identical. Bounded-question identity and ordering are deterministic for equivalent inputs and capability sources.

## Event-ledger after state

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --events-only
sqlite3 /tmp/seed-cp-demo/events.sqlite 'select count(*) as count from events;'
```

After demonstration:

```text
no events
event_count=0
```

Finding: direct ledger count stayed `0 -> 0`; bounded ask constitutional pipeline execution did not write the event ledger. Rendered payloads also report `writes_event_ledger=false`.

## Cluster-mutation evidence

```bash
python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --integrity-summary
```

Excerpt:

```text
Integrity Summary

Unsupported facts: 0
See: --unsupported-facts

Fact conflicts: 0
See: --fact-conflicts

Contradictions: 0
See: --contradictions

Graph issues: 0
See: --graph-issues

Stale facts: 0
See: --stale-facts

Refresh recommendations: 0
See: --stale-fact-refreshes

Capabilities

Verified: 0
Unverified: 0
Stale: 0
Unknown: 0
Provider reported: 0

See: --capability-status

Caveats

* Integrity signals are projection-backed counts, not truth or correctness judgments.
* Unsupported, unverified, stale, contradicted, or missing evidence does not mean false.
* Refresh recommendations are inventory signals only; no refresh or verification is executed.

Projection Version: v1
Last Event: none
```

Finding: integrity summary reports `Last Event: none`, and pipeline/provenance/diagnostic payloads report `mutates_cluster=false`. No repository-supported evidence showed cluster mutation.

## Testimony / evidence / fact boundary

Observed output preserves operator text in `operator_inquiry` and provenance fields and marks it as `operator testimony preserved as evidence, not established fact`. Read-only boundaries explicitly reject established fact, verified claim, repository truth, constitutional authority, and authoritative capability promotion. The output uses those phrases as boundary refusals, not as fields that promote testimony into fact.

## Compatibility finding

No implementation or test files were changed. The only operational limitation found is that bounded ask currently exposes a single `selection_key` surface argument for `constitutional pipeline`. Multiple direct `--selection-key` flags are supported by the public pipeline surface but are not represented by the bounded-ask surface-arg contract. Because repository authority documents the bounded contract as singular and the task says multiple keys only where lawful, this report treats that as a documentation/usage gap rather than a compatibility defect.

## Implementation changes

None.

## Test changes

None.

## Commands/tests executed

- `cat AGENTS.md`
- `git status --short`
- `git rev-parse --abbrev-ref HEAD`
- `git rev-parse HEAD`
- `python scripts/seed_local.py --help`
- `python scripts/seed_local.py ask --help`
- `rg -n "constitutional pipeline|constitutional_pipeline|selection_key|BOUNDED_ASK_REQUIRED_SURFACE_ARGS|BOUNDED_ASK_DISPATCH_SURFACES" seed_runtime scripts tests -S`
- demonstration commands listed above
- `cmp -s /tmp/seed-cp-demo/determinism1.out /tmp/seed-cp-demo/determinism2.out`
- `python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --events-only`
- `sqlite3 /tmp/seed-cp-demo/events.sqlite 'select count(*) as count from events;'`
- `python scripts/seed_local.py --db /tmp/seed-cp-demo/events.sqlite --integrity-summary`

## LOC delta

- Implementation diff: `+0 / -0`
- Test diff: `+0 / -0`
- Report diff: this file only.

## Explicit answers

Did this task recover new architecture?

No.

Did Seed consume the constitutional pipeline through bounded ask?

Yes.

Did any stage infer selection keys from unrestricted operator language?

No.

Was operator testimony promoted into fact?

No.

Were Unknown, unsupported, empty, and refused outcomes preserved distinctly?

Yes. Unknown appears as typed unknown/uncertainty; unsupported exact keys remain unsupported; empty key selection remains absence; governance refusals remain preserved refusals.

Did execution write the event ledger or mutate cluster state?

No.

## Completion classification

Operationally complete with documentation gap: execution is correct, but operator usage is not sufficiently documented for the distinction between bounded ask's current single `selection_key` surface argument and the public pipeline surface's repeated `--selection-key` flags.

## Remaining next pressure

Constitutional pipeline operational documentation.

## Commit hash

Final commit hash is reported in the completion response; embedding the final hash in this committed file would change the commit hash.
