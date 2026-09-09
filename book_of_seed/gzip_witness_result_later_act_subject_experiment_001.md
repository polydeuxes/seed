# Gzip Witness result later-Act subject experiment 001

## Question

If an exact Witness result names the gzip executable path, does Seed use that
result in later Acts over newly supplied gzip material? If it does, how far
does the existing physiology proceed?

This is a live experiment under `seed_behavior_experiment_protocol_001.md`.
It adds no runtime road, Book clause, Witness Grammar, or admission. Gzip,
executable, filesystem, path, and decompression are ordinary report-local
terms.

## Exact first reading

The operator supplies:

```text
!ls /usr/bin/gzip
```

The existing invocation road records:

```text
operator material occurrence Q
        ↓
operator-to-destination Locality relation L
        ↓
Witness source Act and result R
```

The live result is:

```text
R.exact_material = b"/usr/bin/gzip\n"
R.source_occurrence_references = [Q, L]
R.Locality = L.destination Locality
```

The invocation also records exact empty error and completion results in the
same Locality. Existing Measurement physiology addresses the current material
results. The latest byte-pair Measurement through the selected boundary `B`
is retained as the exact first premise for a later pair Compare.

## Exact later material

The operator then supplies a deterministic 21-byte gzip representation of
`b"A"` in the same Locality. The expected expanded byte is known only to the
test control; it is not supplied to Seed.

The existing runtime records the compressed bytes as a separate operator
material result `G`, advances the current reading, and produces a later
byte-pair Measurement.

The recorded-pair Compare exactly addresses:

```text
first Measurement through B
second Measurement after G
```

The active pipeline then records its existing shared-position Measurement,
Applicability, governed Compare, and Distinction Measurement occurrences.

This is a positive result-to-later-Act control:

```text
R current through B
→ Measurement result derived from the current material
→ exact subject of later Compare
```

The path-shaped Witness result is not merely stored beside `G`. Its measured
coordinates participate in later Acts under the existing grammar.

## Exact stopping point

The exact material results after the later pipeline are:

```text
b"/usr/bin/gzip\n"
b""
b""
the 21-byte gzip representation
```

No exact `b"A"` material result occurs.

The positive composition establishes none of these additional coordinates:

```text
path bytes as an executable-file coordinate
the gzip executable as a subject of an Act
the compressed material as input to that executable
an exact destination for expanded material
decompression
```

Seed measures and compares the exact bytes it has. It does not turn the path
text into the behavior of the filesystem object named by that text.

## Distinctions recovered

```text
Witness source provenance of R                          present
R current through exact B                               present
R-derived Measurement used by later Acts                present
G current after B                                       present
exact comparison of first and second Measurements       present

filesystem object addressed through the path bytes      absent
gzip behavior applied to G                               absent
expanded material result                                absent
```

Thus the missing boundary is narrower than generic result use:

```text
exact result content naming a filesystem object
!=
that filesystem object becoming an exact Act subject
```

## Scale adversary

A neighboring diagnostic replaced the 14-byte path result with the complete
98,136-byte gzip executable acquired through ordinary `!cat`, then supplied
the same 21-byte compressed material in that Locality.

The executable acquisition completed in about two seconds. Its pair
Measurement contained 19,834 result positions. The later pipeline spent more
than ninety seconds in the existing shared-position Applicability road while
repeatedly reconstructing the large recorded-pair comparison.

When that downstream diagnostic call was omitted outside Seed, the preceding
acquisition, Measurement, and recorded-pair Compare completed in under five
seconds. This isolates a scale boundary; it supplies no alternate physiology
and no decompression result.

The 14-byte path specimen is therefore the semantic control. The complete
binary adds scale but no new distinction to this question.

## Disposition

The existing Source, Measurement, Compare, Applicability, and Distinction
physiology remains unchanged.

The next question is not whether Seed can use an earlier result at all. It
can. The next question is whether an existing exact relation can carry:

```text
result content naming a filesystem object
→ that exact filesystem object as a later-Act subject
```

Until that relation occurs, Seed has exact path bytes and exact compressed
bytes, but not gzip behavior addressed to those bytes.
