# Constitutional Pipeline Real Inquiry Campaign 001

Repository authority wins. This campaign is read-only with respect to implementation and tests and commits only this report.

## Orientation verification

- Branch: `work`.
- Starting commit: `4b6fa9093e37e4ab62776fc7111716461d0e554a`.
- `constitutional_pipeline_operations.md` exists.
- The implemented and documented public surfaces are present:
  - `seed --constitutional-pipeline` / `python scripts/seed_local.py --constitutional-pipeline`.
  - `seed --constitutional-pipeline-diagnostic` / `python scripts/seed_local.py --constitutional-pipeline-diagnostic`.
  - `seed ask --question-family "constitutional pipeline" --surface-args ...` / `python scripts/seed_local.py ask --question-family "constitutional pipeline" --surface-args ...`.
- The latest documentation report concludes: `Constitutional pipeline operationally complete and documented`.
- The supported exact keys remain exactly:
  - `process` -> `constitutional_process`.
  - `governance` -> `constitutional_governance`.
  - `fidelity` -> `constitutional_fidelity`.
- No newer repository evidence inspected during the campaign contradicted the completed/documented pipeline state.

## Repository evidence used for orientation and inquiry selection

- `constitutional_pipeline_operations.md` documents the deterministic topology from operator inquiry through provenance explanation and states that operator testimony is preserved rather than verified as fact.
- `constitutional_pipeline_operations.md` documents the direct pipeline, diagnostic, and bounded ask surfaces.
- `constitutional_pipeline_operations.md` documents that bounded ask accepts one exact `selection_key`, that an empty string supplies no key, and that matching is exact rather than semantic or fuzzy.
- `constitutional_pipeline_operational_documentation_001.md` records the operational documentation completion classification.
- `constitutional_pipeline_self_consumption_demonstration_001.md` records prior bounded ask behavior for process, governance, unsupported/absent keys, Unknown preservation, and diagnostic comparison.
- `constitutional_pipeline_implementation_scout_001.md`, `constitutional_pipeline_integration_wiring_001.md`, and `constitutional_pipeline_diagnostic_implementation_001.md` supplied current implementation-pressure context without overriding the completed-pipeline orientation.
- Current implementation-pressure neighborhoods were sampled from repository reports about constitutional process, governance, fidelity, pipeline completion/lawful stopping, and current implementation pressure around Question Grammar / Inquiry Navigation.

## Commands run

Orientation and source inspection:

```bash
pwd && rg --files -g 'AGENTS.md' -g '!**/.git/**' .. /workspace 2>/dev/null | head -50 && git status --short --branch
cat AGENTS.md && git rev-parse --abbrev-ref HEAD && git rev-parse HEAD && rg -n "constitutional-pipeline|constitutional pipeline|constitutional_pipeline_operations|operationally complete|process|governance|fidelity" -S .
rg -n "constitutional_pipeline_operations|Constitutional pipeline operationally complete|constitutional-pipeline|question-family \"constitutional pipeline\"|supported.*process|supported.*governance|supported.*fidelity" -S --glob '!docs/**' --glob '!*.pyc' .
python scripts/seed_local.py --help | sed -n '2200,2260p'; python scripts/seed_local.py ask --help | head -120
sed -n '1,120p' constitutional_pipeline_operations.md; sed -n '270,286p' constitutional_pipeline_operational_documentation_001.md; sed -n '2200,2255p' scripts/seed_local.py; sed -n '312,330p' seed_runtime/question_surface_inventory.py
```

Inquiry execution:

```bash
python scripts/seed_local.py --db /tmp/cp001.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator asks whether lawful stopping still applies after pipeline completion; testimony only." "operator:campaign-001" "Does current constitutional process evidence support lawful stopping after pipeline completion?" "caller supplied bounded constitutional inquiry" "bounded" "process" --json > /tmp/q1.json
python scripts/seed_local.py --db /tmp/cp001.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator asks whether governance view creates a governor or hierarchy; testimony only." "operator:campaign-001" "Does constitutional governance evidence support a governance hierarchy or only connective governance?" "caller supplied bounded constitutional inquiry" "bounded" "governance" --json > /tmp/q2.json
python scripts/seed_local.py --db /tmp/cp001.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator asks whether fidelity can enforce runtime evaluation; testimony only." "operator:campaign-001" "Does constitutional fidelity evidence support runtime enforcement or only read-only preservation assessment?" "caller supplied bounded constitutional inquiry" "bounded" "fidelity" --json > /tmp/q3.json
python scripts/seed_local.py --db /tmp/cp001.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator asks which current implementation pressure should become next architecture; testimony only." "operator:campaign-001" "Does current constitutional pipeline evidence justify recovering Question Grammar or Inquiry Navigation from implementation pressure?" "caller supplied bounded constitutional inquiry" "bounded" "process" --pipeline-unknown "current implementation pressure may be outside the process view evidence" --json > /tmp/q4.json
python scripts/seed_local.py --db /tmp/cp001.sqlite ask --question-family "constitutional pipeline" --surface-args "Operator prose mentions governance but intentionally supplies no exact key; testimony only." "operator:campaign-001" "Which constitutional view should be inferred from prose when no exact key is supplied?" "caller supplied bounded constitutional inquiry" "bounded" "" --json > /tmp/q5.json
```

Supplemental human and diagnostic execution:

```bash
python scripts/seed_local.py --db /tmp/cp001.sqlite --constitutional-pipeline --operator-inquiry "Operator asks whether lawful stopping still applies after pipeline completion; testimony only." --inquiry-provenance operator:campaign-001 --bounded-question "Does current constitutional process evidence support lawful stopping after pipeline completion?" --constitutional-intent "caller supplied bounded constitutional inquiry" --scope-status bounded --selection-key process > /tmp/q1.txt
python scripts/seed_local.py --db /tmp/cp001.sqlite --constitutional-pipeline-diagnostic --operator-inquiry "Operator prose mentions governance but intentionally supplies no exact key; testimony only." --inquiry-provenance operator:campaign-001 --bounded-question "Which constitutional view should be inferred from prose when no exact key is supplied?" --constitutional-intent "caller supplied bounded constitutional inquiry" --scope-status bounded --json > /tmp/q5diag.json
python scripts/seed_local.py --db /tmp/cp001.sqlite --constitutional-pipeline-diagnostic --operator-inquiry "Operator asks whether fidelity can enforce runtime evaluation; testimony only." --inquiry-provenance operator:campaign-001 --bounded-question "Does constitutional fidelity evidence support runtime enforcement or only read-only preservation assessment?" --constitutional-intent "caller supplied bounded constitutional inquiry" --scope-status bounded --selection-key fidelity --json > /tmp/q3diag.json
python - <<'PY'
import json, glob
for f in glob.glob('/tmp/q*.json')+glob.glob('/tmp/q*diag.json'):
    data=json.load(open(f)); print('\n',f)
    print('keys', data.get('selection',{}).get('requested_keys'), data.get('selection',{}).get('unsupported_question_keys'), data.get('selection',{}).get('selected_view_names'))
    print('unknowns', data.get('composition',{}).get('preserved_unknowns'))
    print('refusals', data.get('composition',{}).get('preserved_refusals'))
    print('diag status', data.get('status'), 'first', data.get('first_insufficiency'))
    if 'stages' in data:
        print([(s.get('name'),s.get('status'),s.get('unsupported_keys'),s.get('selected_view_names')) for s in data['stages']])
PY
python - <<'PY'
import json
for n in range(1,6):
    data=json.load(open(f'/tmp/q{n}.json'))
    sel=data.get('selection',{})
    comp=data['composition']
    b=data['bounded_question']
    print(n, b['operator_inquiry'], b.get('caller_supplied_fields'), sel.get('selected_view_names'), sel.get('unsupported_question_keys'), len(comp.get('preserved_unknowns',[])), len(comp.get('preserved_refusals',[])), comp.get('writes_event_ledger'), comp.get('mutates_cluster'))
PY
```

## Inquiry 1: constitutional process / lawful stopping

### Source repository pressure

Pipeline completion and lawful stopping pressure: the operator asks whether a completed, documented constitutional pipeline still supports stopping rather than ownership recovery.

### Inquiry formation record

- Operator communicative act: `Operator asks whether lawful stopping still applies after pipeline completion; testimony only.`
- Preserved operator testimony: same text, preserved as operator testimony and not established fact.
- Bounded constitutional question: `Does current constitutional process evidence support lawful stopping after pipeline completion?`
- Explicit constitutional intent: `caller supplied bounded constitutional inquiry`.
- Scope status: `bounded`.
- Exact selection key: `process`.
- Uncertainty: none.
- Unknowns: none supplied by the campaign.
- Inquiry provenance: `operator:campaign-001`.
- Campaign-supplied bounded fields: bounded question, intent, scope, and exact selection key.

### Findings

- Human-output findings: human output preserved the testimony, displayed the bounded question, selected `constitutional_process`, explained exact key matching, and showed process Unknowns.
- JSON findings: selected view was `constitutional_process`; preserved Unknown count was 5; preserved refusal count was 0; `writes_event_ledger=false`; `mutates_cluster=false`.
- Diagnostic findings: no insufficiency required investigation for this successful process-selection case.
- Selected views: `constitutional_process`.
- Provenance explanation findings: `process` matched `constitutional_process` by exact key; no unsupported keys were reported.
- Unknown and refusal findings: process Unknowns were preserved; no refusals were produced.

### Evaluation answers

1. Operator testimony preserved correctly: Yes.
2. Bounded question useful and faithful: Yes.
3. Explicit key obvious: Yes for an operator already reading the operations guide; it maps directly to the process neighborhood.
4. Selected view matched intended neighborhood: Yes.
5. Provenance explained exact match: Yes.
6. Composition answered bounded question: Yes, by rendering process evidence and lawful read-only boundaries rather than creating recovery work.
7. Unknowns preserved: Yes.
8. Refusals useful/scoped: Not applicable; none surfaced.
9. Diagnostic made first insufficiency visible: Not applicable; none observed.
10. Internal vocabulary required: Low; `process` is documented, but the operator still needs the exact key.
11. Meaning lost: No material loss.
12. Required unsupported semantic inference: No.

### Friction classification

No issue.

## Inquiry 2: constitutional governance / hierarchy refusal

### Source repository pressure

Governance pressure: repository reports distinguish connective governance from governance ownership, hierarchy, runtime governance, and repository mutation.

### Inquiry formation record

- Operator communicative act: `Operator asks whether governance view creates a governor or hierarchy; testimony only.`
- Preserved operator testimony: same text, preserved as operator testimony and not established fact.
- Bounded constitutional question: `Does constitutional governance evidence support a governance hierarchy or only connective governance?`
- Explicit constitutional intent: `caller supplied bounded constitutional inquiry`.
- Scope status: `bounded`.
- Exact selection key: `governance`.
- Uncertainty: none.
- Unknowns: none supplied by the campaign.
- Inquiry provenance: `operator:campaign-001`.
- Campaign-supplied bounded fields: bounded question, intent, scope, and exact selection key.

### Findings

- Human-output findings: JSON was primary for this comparison; the selected view and refusal lists were typed and directly inspectable.
- JSON findings: selected view was `constitutional_governance`; preserved Unknown count was 7; preserved refusal count was 7; refusals included hierarchy, governance execution, governance ownership, runtime governance, and repository mutation.
- Diagnostic findings: no compatibility defect; a governance request can select successfully while composition preserves refusals.
- Selected views: `constitutional_governance`.
- Provenance explanation findings: `governance` matched `constitutional_governance` by exact key.
- Unknown and refusal findings: Unknowns and refusals were preserved rather than resolved.

### Evaluation answers

1. Operator testimony preserved correctly: Yes.
2. Bounded question useful and faithful: Yes.
3. Explicit key obvious: Yes for documented use.
4. Selected view matched intended neighborhood: Yes.
5. Provenance explained exact match: Yes.
6. Composition answered bounded question: Yes, especially by preserving hierarchy and runtime-governance refusals.
7. Unknowns preserved: Yes.
8. Refusals useful/scoped: Yes.
9. Diagnostic made first insufficiency visible: Not applicable; refusal is lawful output, not a defect.
10. Internal vocabulary required: Moderate; `governance` is documented, but interpreting refusal status benefits from reading the operations guide.
11. Meaning lost: No material loss.
12. Required unsupported semantic inference: No.

### Friction classification

No issue.

## Inquiry 3: constitutional fidelity / runtime enforcement refusal

### Source repository pressure

Fidelity pressure: repository reports preserve fidelity as read-only preservation assessment and explicitly refuse runtime evaluation, fidelity enforcement, implementation mutation, repository mutation, and redesign.

### Inquiry formation record

- Operator communicative act: `Operator asks whether fidelity can enforce runtime evaluation; testimony only.`
- Preserved operator testimony: same text, preserved as operator testimony and not established fact.
- Bounded constitutional question: `Does constitutional fidelity evidence support runtime enforcement or only read-only preservation assessment?`
- Explicit constitutional intent: `caller supplied bounded constitutional inquiry`.
- Scope status: `bounded`.
- Exact selection key: `fidelity`.
- Uncertainty: none.
- Unknowns: none supplied by the campaign.
- Inquiry provenance: `operator:campaign-001`.
- Campaign-supplied bounded fields: bounded question, intent, scope, and exact selection key.

### Findings

- Human-output findings: JSON was primary for refusal comparison; the fidelity refusal list is operator-useful because it names exactly what is refused.
- JSON findings: selected view was `constitutional_fidelity`; preserved Unknown count was 9; preserved refusal count was 9; refusals included runtime evaluation, fidelity enforcement, implementation mutation, repository mutation, architectural redesign, and projection recovery.
- Diagnostic findings: diagnostic stages completed through selection/composition and reported the final stage as `refused`, making the lawful refusal visible rather than hiding it as a crash.
- Selected views: `constitutional_fidelity`.
- Provenance explanation findings: `fidelity` matched `constitutional_fidelity` by exact key.
- Unknown and refusal findings: Unknowns and refusals were preserved.

### Evaluation answers

1. Operator testimony preserved correctly: Yes.
2. Bounded question useful and faithful: Yes.
3. Explicit key obvious: Yes for documented use.
4. Selected view matched intended neighborhood: Yes.
5. Provenance explained exact match: Yes.
6. Composition answered bounded question: Yes, by preserving fidelity refusals.
7. Unknowns preserved: Yes.
8. Refusals useful/scoped: Yes.
9. Diagnostic made first insufficiency visible: Yes; final composition/refusal status was visible.
10. Internal vocabulary required: Moderate; `fidelity` is documented but repository-specific.
11. Meaning lost: No material loss.
12. Required unsupported semantic inference: No.

### Friction classification

No issue.

## Inquiry 4: current implementation pressure / Question Grammar and Inquiry Navigation

### Source repository pressure

Current implementation pressure: prior reports mention Question Grammar, Inquiry Navigation, exact bounded fields, and pipeline operation. The campaign tests whether a real operator pressure should recover new architecture merely because explicit bounded fields are cumbersome.

### Inquiry formation record

- Operator communicative act: `Operator asks which current implementation pressure should become next architecture; testimony only.`
- Preserved operator testimony: same text, preserved as operator testimony and not established fact.
- Bounded constitutional question: `Does current constitutional pipeline evidence justify recovering Question Grammar or Inquiry Navigation from implementation pressure?`
- Explicit constitutional intent: `caller supplied bounded constitutional inquiry`.
- Scope status: `bounded`.
- Exact selection key: `process`.
- Uncertainty: none.
- Unknowns: `current implementation pressure may be outside the process view evidence`.
- Inquiry provenance: `operator:campaign-001`.
- Campaign-supplied bounded fields: bounded question, intent, scope, exact selection key, and explicit Unknown.

### Findings

- Human-output findings: the pipeline preserved the campaign-supplied Unknown and did not transform it into a conclusion.
- JSON findings: selected view was `constitutional_process`; campaign-supplied Unknown remained on the bounded question; composition preserved 5 process Unknowns; refusal count was 0; `writes_event_ledger=false`; `mutates_cluster=false`.
- Diagnostic findings: no compatibility defect; the diagnostic pattern remained read-only.
- Selected views: `constitutional_process`.
- Provenance explanation findings: `process` matched `constitutional_process` by exact key.
- Unknown and refusal findings: explicit Unknown was preserved at the bounded-question level; composition did not resolve it without evidence.

### Evaluation answers

1. Operator testimony preserved correctly: Yes.
2. Bounded question useful and faithful: Partly. It faithfully represents the pressure, but the selected process view alone cannot decide all future implementation-pressure questions.
3. Explicit key obvious: Somewhat; `process` was lawful but not uniquely obvious for Question Grammar / Inquiry Navigation pressure.
4. Selected view matched intended neighborhood: Partly; process was the closest existing exact key, but this question spans implementation pressure beyond one view.
5. Provenance explained exact match: Yes.
6. Composition answered bounded question: Partly; it preserved process evidence and Unknowns but did not fully adjudicate whether Question Grammar or Inquiry Navigation should be investigated.
7. Unknowns preserved: Yes.
8. Refusals useful/scoped: Not applicable; none surfaced.
9. Diagnostic made first insufficiency visible: Not strongly; because the insufficiency was about question/view fit rather than pipeline stage failure.
10. Internal vocabulary required: Moderate; the operator needed repository vocabulary and the exact key contract.
11. Meaning lost: Some nuance about current implementation pressure was compressed into the process key.
12. Required unsupported semantic inference: No stage performed it; the operator/campaign supplied the bounding.

### Friction classification

Capability.

Rationale: no current single selected constitutional view exposed enough existing knowledge to fully answer this implementation-pressure question. This was not architecture compression; it was a bounded capability gap for this one inquiry.

## Inquiry 5: absent exact key / no natural-language inference

### Source repository pressure

Input contract pressure: the operations guide documents that bounded ask accepts one exact selection key and that an empty string supplies no key. This inquiry tests whether prose mentioning a neighborhood causes unsupported inference.

### Inquiry formation record

- Operator communicative act: `Operator prose mentions governance but intentionally supplies no exact key; testimony only.`
- Preserved operator testimony: same text, preserved as operator testimony and not established fact.
- Bounded constitutional question: `Which constitutional view should be inferred from prose when no exact key is supplied?`
- Explicit constitutional intent: `caller supplied bounded constitutional inquiry`.
- Scope status: `bounded`.
- Exact selection key: absent / empty string.
- Uncertainty: none.
- Unknowns: none supplied by the campaign.
- Inquiry provenance: `operator:campaign-001`.
- Campaign-supplied bounded fields: bounded question, intent, scope, and absent key.

### Findings

- Human-output findings: no selected view was produced, as documented.
- JSON findings: caller-supplied fields contained no `selection_key`; selected views were empty; composition had no contributors; Unknown/refusal counts were 0; `writes_event_ledger=false`; `mutates_cluster=false`.
- Diagnostic findings: diagnostic stages showed empty selection-related statuses, making absence visible.
- Selected views: none.
- Provenance explanation findings: there was no exact key to match; prose was not used as a selector.
- Unknown and refusal findings: none surfaced.

### Evaluation answers

1. Operator testimony preserved correctly: Yes.
2. Bounded question useful and faithful: Yes as a negative-control inquiry.
3. Explicit key obvious: The absence was intentional; for ordinary use, this demonstrates that exact key input remains required.
4. Selected view matched intended neighborhood: No view selected, lawfully.
5. Provenance explained exact match: Yes by absence/no match behavior.
6. Composition answered bounded question: Yes, negatively: no inference occurs from prose alone.
7. Unknowns preserved: Not applicable.
8. Refusals useful/scoped: Not applicable.
9. Diagnostic made first insufficiency visible: Yes; empty selection status was visible.
10. Internal vocabulary required: Low-to-moderate; an operator must know the exact key contract.
11. Meaning lost: No, because the purpose was to test absent-key behavior.
12. Required unsupported semantic inference: No; the system refused to infer.

### Friction classification

No issue.

## Cross-inquiry results matrix

| Inquiry | Required case coverage | Selected view(s) | Unknowns | Refusals | Event ledger | Cluster mutation | Friction |
| --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | process selection | `constitutional_process` | 5 preserved | 0 | false | false | No issue |
| 2 | governance selection; lawful refusals | `constitutional_governance` | 7 preserved | 7 preserved | false | false | No issue |
| 3 | fidelity selection; lawful refusals | `constitutional_fidelity` | 9 preserved | 9 preserved | false | false | No issue |
| 4 | explicit Unknown; current implementation pressure | `constitutional_process` | explicit bounded Unknown plus 5 process Unknowns | 0 | false | false | Capability |
| 5 | absent key / no matching key | none | 0 | 0 | false | false | No issue |

## Event-ledger behavior

All five JSON results reported `writes_event_ledger=false` for the composed result. The bounded-question records also reported `writes_event_ledger=false`. The campaign used `/tmp/cp001.sqlite` as a neutral temporary database path, but the constitutional pipeline outputs remained read-only and did not require event-ledger writes.

## Cluster-mutation behavior

All five JSON results reported `mutates_cluster=false` for the composed result. The bounded-question records also reported `mutates_cluster=false`. No command intentionally mutated cluster truth, implementation state, tests, views, registrations, or capabilities.

## Recurrence analysis

- No issue: inquiries 1, 2, 3, and 5 were handled lawfully and usefully.
- Capability: inquiry 4 exposed that a broad current-implementation-pressure question can exceed the explanatory reach of one selected constitutional view.
- The capability friction appeared in only one inquiry and did not satisfy the recurrence standard.
- No concrete correctness or compatibility defect appeared.
- No implementation evidence directly proved a missing contract.

Did real usage expose a repeated limitation?

No.

## Question Grammar determination

Does current evidence justify Question Grammar investigation?

No.

Reason: explicit bounded fields were cumbersome but faithful. The campaign did not show repeated evidence that the communicative act cannot be faithfully represented without a missing deterministic question-forming responsibility.

## Inquiry Navigation determination

Does current evidence justify Inquiry Navigation investigation?

No.

Reason: exact keys were documented and worked. One broad implementation-pressure question made key choice less obvious, but this single case did not show repeated evidence that an operator cannot navigate to the correct registered constitutional capability without repository-internal knowledge.

## Compatibility determination

Compatibility defect?

No.

Documented behavior worked as implemented: exact keys selected exact registered views, empty key selected no view, Unknowns were preserved, refusals were preserved, diagnostic output made empty/refused cases visible, and read-only/event-ledger/mutation boundaries stayed false.

## Lawful Architectural Stopping

Does Lawful Architectural Stopping still apply?

Yes, with direct evidence: the pipeline accepted explicit bounded input, selected only exact registered keys, preserved Unknowns and refusals, did not infer from prose, did not write the event ledger, did not mutate the cluster, and produced no repeated limitation or compatibility defect requiring ownership recovery.

Did this campaign recover new architecture?

No.

## Completion classification

Operationally sufficient: Current real inquiries are handled lawfully and usefully.

## Recommended next pressure

No architectural or implementation follow-up. Recommended next pressure: continue ordinary real-use monitoring of exact-key operator ergonomics and broad implementation-pressure inquiries; only open a new pressure if two materially different future inquiries show the same capability/key-navigation limitation or one inquiry exposes a concrete compatibility defect.

## Read-only implementation/test statement

No implementation files changed. No test files changed. No capabilities, selection keys, views, registrations, bounded ask behavior, diagnostics, event-ledger behavior, persistence behavior, mutation behavior, planning behavior, recovery behavior, or architecture were changed.

## Completion answers

```text
Did this campaign recover new architecture?

No.
```

```text
Did real usage expose a repeated limitation?

No.
```

```text
Does current evidence justify Question Grammar investigation?

No.
```

```text
Does current evidence justify Inquiry Navigation investigation?

No.
```

```text
Does Lawful Architectural Stopping still apply?

Yes, with direct evidence: exact-key pipeline operation worked, absent-key behavior stayed non-inferential, Unknowns/refusals were preserved, event-ledger writes stayed false, cluster mutation stayed false, and no repeated limitation or compatibility defect appeared.
```

## Report accounting

- Implementation diff: `+0 / -0`.
- Test diff: `+0 / -0`.
- Report diff: `+432 / -0`.
- Report LOC: `432`.
- Commit hash: recorded by the final git commit containing this report; exact hash reported in campaign completion summary.
