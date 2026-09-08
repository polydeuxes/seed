# Material witnesses

This directory is for operator-owned implementation interrogations whose
observations have not yet become Seed competencies.

A material witness supplies exact material to an external implementation
function and preserves the bounded result that function returned.  The
external result is testimony about that invocation.  It is not, by identity,
a Seed Measurement, Candidate, Admission, Applicability determination,
Standing movement, Representation, or emission.

These witnesses are deliberately outside both `seed_runtime/` and `scripts/`.
They do not participate in the implementation-function Fidelity catalog, and
their tests are not collected by the default `tests/` suite.  Run a witness
test explicitly while interrogating that witness.

```text
.venv/bin/pytest -q material_witnesses
```

## Why this boundary exists

The first versions were honest external probes.  Later work added script-local
objects named `Admission`, result references, and occurrence identities so the
observations could be compared exactly.  Those names resembled live Seed
physiology closely enough that later readers treated the probes as internal
competencies.  A cleanup pass then made the opposite mistake and deleted probes
whose observed distinctions had not crossed into Seed.

The location of a relation decides which claim it can support:

```text
external invocation + external result
    -> material-witness observation

durable Seed assignment + Act Evidence + exact input relation
    + Yield + result + Standing reader
    -> Seed competency
```

Moving a witness result into the ledger through ordinary Ingest preserves its
material and provenance.  It does not turn the external invocation or its
partition into a Seed Act or finding.

## Original interrogations

| Material witness | Introduction | Original bounded question | Current crossing |
| --- | --- | --- | --- |
| system material | `3f2ab483` | Can host-returned bytes arrive separately from the operator instruction and from the invocation declaration? | Replaced.  Exact system-attributed Ingest and supplied-invocation occurrences now preserve the distinction.  The original commit explicitly called its harness provisional. |
| calculator relation material | `c5438305` | Can one uninterpreted relation-bearing claim and one calculator result each traverse their exact Seed roads without the calculator becoming mathematical Authority? | The claim's addressed `0x3d` byte yields one exact two-Assertion path.  That path reaches the conflicting and later-result-only findings of an earlier-to-claim pair comparison while the relation of those distinctions remains Unknown.  Current Standing exposes those exact finding branches as three read-only pins, recording nothing and authorizing no later Act.  Calculator stdout enters a distinct invocation Locality with command provenance and its own pair-position Measurement; no current Responsibility compares it with the path finding. |
| terminal keystroke | `dfcfcac0` | Does one exact DEL byte change the exact result of one fixed opaque PTY/readline invocation while source bytes and process coordinates remain exact? | Crossed through bounded comparison.  The external function reference, each source, and each stdout result traverse the supplied-invocation console road in one fresh invocation Locality.  Each stdout Ingest preserves both the exact prior function-reference occurrence and source occurrence as provenance.  Every supplied occurrence receives its own append-tip byte and occurrence-position Measurements before any exact boundary emission.  Where stdout provenance carries the exact immediately prior supplied source occurrence reference, this Seed records pair Measurements for the exact earlier and later byte boundaries, determines Applicability, records their Participation in one Compare, and Yields full-content equal findings, conflicting findings, findings of the earlier result, findings of the later result, and Unknown findings into Standing.  The comparison establishes no source relation or represented relation.  The external function reference remains opaque material rather than a Seed Act or Authority. |
| terminal style | `4880e4aa` | Can two exact materials produce equal visible terminal cells while only one carries presentation controls? | Crossed through bounded byte comparison only.  An isolated tmux invocation preserves both its plain cell capture and its style-preserving capture as exact result material with source and external-function provenance.  The two views enter one invocation Locality, their full pair findings enter a responsible Compare, and the exact style-preserving result can be admitted and emitted.  No Seed Measurement establishes presentation controls, and no Representation rule applies recovered style to new material. |
| game protocol | `bb351082` | Does one fixed stateful game implementation distinguish two exact command streams whose position material differs at one turn boundary? | Not crossed.  The bounded external invocation preserves each input boundary's accepted byte count and each distinct stdout result enters ordinary Ingest with its exact source occurrence as provenance.  The witness establishes neither a framing relation, strategy, causation, Admission, nor a Seed competency. |
| material-reference comparison | `45a80b8d` | How do exact operator, session, and lineage materials differ from sixteen exact Book occurrences under external implementation functions and recurrent-pair probes? | Not crossed.  The external invocation and script-local comparison objects are material-witness testimony.  Their Admission-shaped names establish no Seed Admission, Applicability, Fidelity, or competency.  The live byte-pair Measurement within the experiment remains a Seed finding, but the script comparison consuming it is external. |
| Surf | `8e8a2557` | How do equal exact inputs partition across four fixed Surf argv forms? | Not crossed.  Process results establish neither display access nor presentation. |
| Piper | `8f071e92` | How do exact supplied prose occurrences partition under one fixed voice implementation, with stdout, stderr, limits, and return result preserved? | Partly crossed.  Each opaque stdout result now enters through exact system Ingest with its source occurrence as provenance.  PCM formation coordinates and an admitted audio destination boundary remain absent. |
| FFmpeg stream | `66f80309` | How do exact Book pair subjects partition across fixed stream-decoder invocation forms? | Not crossed.  The observed partitions remain external implementation results. |
| Bash syntax and bounded shell | `87d93140` | How does the same exact material partition under syntax-only Bash and a bounded isolated Bash invocation? | Not crossed.  Neither invocation is a Seed competency. |
| PCM/photo matrix | `27ad8129` | How do controlled media specimens before and after encoding partition across fixed media implementation functions? | Not crossed.  The source format coordinates were operator testimony, not live Seed findings. |
| visual ladder | `df0ef6b2` | What changes when one operator-declared visual construction coordinate changes at a time? | Not crossed.  The rendered files are material; the construction coordinates remain operator testimony. |
| audio ladder | `dbfd8d03` | What changes when occurrence count or frequency changes while the other construction coordinates hold? | Not crossed.  The exact samples remain external specimens. |
| pixel ladder | `f57b58ce` | What changes when one exact channel position or value changes? | Not crossed.  Channel roles and extent remain external testimony. |

## Retirement boundary

A material witness is ready to retire only after one live Seed road can:

1. address the exact source and result occurrences;
2. preserve the implementation function and invocation boundary without
   turning the function into Seed authority;
3. perform a responsible bounded Measurement or Compare;
4. record its Evidence of Yield and result;
5. recover the same distinction after restart from Standing; and
6. apply that distinction prospectively to held-out material.

Until that crossing exists, a witness is an unfinished competency experiment,
not contamination and not Seed knowledge.
