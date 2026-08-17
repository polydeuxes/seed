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
| terminal keystroke | `dfcfcac0` | Does one exact DEL byte change the raw result of one fixed opaque PTY/readline invocation while source bytes and process coordinates remain exact? | Not crossed.  Seed has no terminal-editing competency or durable finding over the two results. |
| Surf | `8e8a2557` | How do equal exact inputs partition across four fixed Surf argv forms? | Not crossed.  Process results establish neither display access nor presentation. |
| Piper | `8f071e92` | How do exact supplied prose occurrences partition under one fixed voice implementation, with stdout, stderr, limits, and return result preserved? | Not crossed.  PCM formation coordinates and an admitted audio destination boundary remain absent. |
| FFmpeg stream | `66f80309` | How do exact Book pair subjects partition across fixed stream-decoder invocation forms? | Not crossed.  The observed partitions remain external implementation results. |
| Bash syntax and bounded shell | `87d93140` | How does the same exact material partition under syntax-only Bash and a bounded isolated Bash invocation? | Not crossed.  Neither invocation is a Seed competency. |
| PCM/photo matrix | `27ad8129` | How do controlled raw and encoded media specimens partition across fixed media implementation functions? | Not crossed.  The source format coordinates were operator testimony, not live Seed findings. |
| visual ladder | `df0ef6b2` | What changes when one operator-declared visual construction coordinate changes at a time? | Not crossed.  The rendered files are material; the construction coordinates remain operator testimony. |
| audio ladder | `dbfd8d03` | What changes when occurrence count or frequency changes while the other construction coordinates hold? | Not crossed.  The exact samples remain external specimens. |
| pixel ladder | `f57b58ce` | What changes when one raw channel position or value changes? | Not crossed.  Channel roles and extent remain external testimony. |

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
