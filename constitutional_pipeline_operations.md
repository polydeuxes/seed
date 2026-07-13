# Constitutional Pipeline Operations

This is an operator guide for the implemented constitutional pipeline surfaces. It explains how to invoke, inspect, and interpret the current behavior without recovering architecture or changing pipeline behavior.

## Implemented topology

```text
Operator Inquiry
        ↓
BoundedConstitutionalQuestion
        ↓
QuestionProjection
        +
CapabilityProjection
        ↓
ConstitutionalViewSelection
        ↓
SelectedConstitutionalViews
        ↓
ConstitutionalViewComposition
        ↓
ConstitutionalPipelineResult
        ↓
Provenance Explanation
```

The topology is deterministic over explicit operator-supplied fields. Operator testimony is preserved as evidence and provenance; it is not verified as fact.

## Which surface should I use?

### Direct pipeline: `seed --constitutional-pipeline`

Use the direct pipeline when you need:

- the complete pipeline result;
- human or JSON output;
- repeated exact `--selection-key` arguments;
- explicit uncertainty or Unknown inputs;
- the provenance explanation in the public result.

Invocation convention in this repository is `python scripts/seed_local.py ...`. Use `--db` when you want a neutral temporary event-ledger path for verification, even though the pipeline itself does not write events.

### Pipeline diagnostic: `seed --constitutional-pipeline-diagnostic`

Use the diagnostic when you need:

- per-stage status;
- empty versus unsupported distinction;
- Unknown and refusal counts;
- read-only, event-ledger, and mutation boundaries.

The diagnostic is distinct from the public pipeline result. It reports stage status and counts; it is not a replacement for the composed operator-facing answer.

### Bounded ask integration: `seed ask --question-family "constitutional pipeline" --surface-args ...`

Use bounded ask when you are invoking the pipeline through existing bounded ask admission and dispatch.

Prominent current limitation:

```text
The current bounded-ask surface-arg contract accepts one exact
selection_key value.

It does not split a space-separated value into multiple keys.

For multiple keys, use the direct --constitutional-pipeline surface
with repeated --selection-key arguments.
```

## Required arguments

Direct pipeline and diagnostic examples should provide these explicit bounded inputs:

- `--operator-inquiry <text>`
- `--inquiry-provenance <text>`
- `--bounded-question <text>`
- `--constitutional-intent <text>`
- `--scope-status <text>`
- zero or more `--selection-key <exact-key>` arguments
- optional repeated `--pipeline-uncertainty <text>` entries
- optional repeated `--pipeline-unknown <text>` entries
- optional `--json` for JSON output

Bounded ask for the constitutional pipeline forwards positional surface args in this order:

```text
operator_inquiry inquiry_provenance bounded_question constitutional_intent scope_status selection_key
```

The final `selection_key` is one exact value. An empty string supplies no key. A string such as `"process governance fidelity"` is one unsupported exact key, not three keys.

## Exact selection keys

Current demonstrated exact keys are:

| Exact key | Selected view |
| --- | --- |
| `process` | `constitutional_process` |
| `governance` | `constitutional_governance` |
| `fidelity` | `constitutional_fidelity` |

Matching is exact. Do not assume synonyms, semantic matching, fuzzy matching, natural-language inference, or capability discovery.

## Copyable command examples

Use a neutral temporary database path when verifying ledger behavior:

```bash
DB=/tmp/seed-cp-ops/events.sqlite
mkdir -p /tmp/seed-cp-ops
```

### 1. Direct pipeline with one exact key

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator says process should be visible; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which constitutional process surface is available?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key process
```

### 2. Direct pipeline with multiple repeated exact keys

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator asks for process and fidelity; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which constitutional views are available?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key process \
  --selection-key fidelity
```

### 3. Direct pipeline JSON output

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator says process should be visible; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which constitutional process surface is available?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key process \
  --json
```

### 4. Bounded ask with one exact key

```bash
python scripts/seed_local.py --db "$DB" ask \
  --question-family "constitutional pipeline" \
  --surface-args \
  "Operator says process should be visible; testimony only." \
  operator:docs \
  "Which constitutional process surface is available?" \
  "caller supplied bounded constitutional inquiry" \
  bounded \
  process \
  --json
```

### 5. Bounded ask with no key

```bash
python scripts/seed_local.py --db "$DB" ask \
  --question-family "constitutional pipeline" \
  --surface-args \
  "Operator prose mentions process but key intentionally absent; testimony only." \
  operator:docs \
  "Which constitutional view should be inferred from prose?" \
  "caller supplied bounded constitutional inquiry" \
  bounded \
  "" \
  --json
```

### 6. Unsupported exact key

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator supplies unsupported exact key; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which unsupported constitutional view matches?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key unsupported-explicit-key \
  --json
```

### 7. Explicit Unknown input

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator supplies Unknown evidence; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which process surface is available with Unknown preserved?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key process \
  --pipeline-unknown "operator assertion not verified" \
  --json
```

### 8. Pipeline diagnostic

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline-diagnostic \
  --operator-inquiry "Operator says process should be visible; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which constitutional process surface is available?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key process \
  --json
```

### 9. Governance selection demonstrating preserved refusals

```bash
python scripts/seed_local.py --db "$DB" \
  --constitutional-pipeline \
  --operator-inquiry "Operator asks governance; testimony only." \
  --inquiry-provenance operator:docs \
  --bounded-question "Which constitutional governance surface contributes?" \
  --constitutional-intent "caller supplied bounded constitutional inquiry" \
  --scope-status bounded \
  --selection-key governance \
  --json
```

### Bounded ask multi-key pitfall

This is valid syntax, but it supplies one unsupported exact key:

```bash
python scripts/seed_local.py --db "$DB" ask \
  --question-family "constitutional pipeline" \
  --surface-args \
  "Operator supplies three exact keys; testimony only." \
  operator:docs \
  "Which constitutional views are available?" \
  "caller supplied bounded constitutional inquiry" \
  bounded \
  "process governance fidelity" \
  --json
```

Use the repeated direct `--selection-key` form when you intend multiple keys.

## Outcome interpretation

### Empty

```text
No explicit selection key was supplied.
```

Meaning:

- no key was inferred from prose;
- no view was selected;
- this is not verified irrelevance.

### Unsupported

```text
An explicit key did not match any projected capability key.
```

Meaning:

- the key remains visible;
- no fuzzy match occurs;
- no view is invented.

### Unknown

```text
Typed uncertainty remains unresolved.
```

Meaning:

- Unknown is preserved;
- Unknown is not false;
- Unknown is not a negative constitutional conclusion.

### Refused

```text
A selected view contributed explicit refusals.
```

Meaning:

- the view may still be selected and composed;
- refusal is not full pipeline failure;
- the refused responsibility remains outside the view's authority.

## Provenance explanation

The public pipeline result includes a provenance explanation. Use JSON output when you need to inspect exact fields for:

- supplied question keys;
- projected capability keys;
- exact matched keys;
- unsupported keys;
- selected views;
- composition contributors;
- remaining uncertainty;
- Unknowns;
- refusals.

```text
The provenance explanation reports why the deterministic pipeline
selected a view.

It does not explain why the operator chose a key and does not verify
the operator inquiry.
```

## Diagnostic interpretation

The diagnostic stage statuses are:

```text
complete
empty
unsupported
unknown
refused
```

A function returning successfully does not necessarily mean the constitutional inquiry produced a complete answer. For example, a governance request can have Selection `complete` because `governance` exactly selected `constitutional_governance`, while Composition is `refused` because the selected view preserves explicit refusals. That refusal is surfaced as stage status and counts; it is not a crash and not a full pipeline failure.

The diagnostic output also reports:

- `event_ledger_status`, currently `no event-ledger writes` for these surfaces;
- `cluster_mutation_status`, currently `no cluster mutation`;
- per-stage `read_only`, `writes_event_ledger`, and `mutates_cluster` booleans.

## Testimony and mutation boundary

```text
Operator testimony is evidence, not fact.
```

Pipeline execution:

- preserves operator inquiry and provenance;
- does not verify the inquiry;
- does not create established facts;
- does not create constitutional authority;
- does not create authoritative capabilities;
- does not write the event ledger;
- does not mutate cluster state.

## Compatibility and scope

These are outside the current operator contract:

- natural-language selection-key inference;
- Question Grammar competency;
- Inquiry Navigation competency;
- semantic or fuzzy matching;
- autonomous constitutional routing;
- capability discovery;
- pipeline mutation;
- event-ledger recording.

Do not describe future research or architectural vocabulary as current functionality unless implementation evidence supports it.
