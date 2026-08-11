# Signature-count layer over the recovered population: run 001

Roadmap items 1, 2 and 4. `#2476`'s equality-signature count Measurement, run
against the Test Seed's whole recorded signature population rather than a
fixture, profiled, and re-run after one change to prove the findings unmoved.

Store: `test_seed_assertion_comparison_layers_20260811.db`, 8.39 GB, 1,164,280
occurrences, 21 sessions. Read from a copy; the store was never written.

## Item 1 — the act produced the numbers

```text
  findings                 3
  counts                   12,228   3,447   481
  sum                      16,156
  population in session    16,156 positional_equality_signature_recorded
```

**[measured]** Complete: the three counts sum to the population exactly, so no
signature fell outside a group and none was counted twice.

**[measured]** The counts equal the roadmap's stated expectation
`12,228 / 3,447 / 481`.

**That agreement is worth less than it looks.** The expectation was a reader's
tally. If it was computed by grouping in Python rather than by running the
Measurement, then this run is the *first* production of the number and the tally
was a prediction of it — which makes the match a check on the reader's
arithmetic, not corroboration of the finding. `05.Testimony.E:29` is the reason
to say so: repetition of one derivation is not independent corroboration. The
finding stands on the recorded act. It does not stand on the agreement.

## Item 2 — where the time went

```text
  elapsed                    299 s
  peak RSS                  < 0.05 GB          the layer streams
  ledger.get                48,468   distinct 28,388   1.7x repeat
  integrity_of             113,092   distinct 44,544   2.5x repeat
  iter_session_kind         32,313   of which 32,312 were ingress reads
  reads per signature            3.0
```

**[measured]** Cost per warm call, and what the whole run spends on each:

```text
  iter_session_kind, 300 ingress occurrences   7.093 ms   x32,312 = 229.2 s
  integrity_of                                 0.037 ms  x113,092 =   4.2 s
  get                                          0.046 ms   x48,468 =   2.2 s
```

**229 of the 299 seconds — 77% — is one read, repeated 32,312 times.**

### The repetition, and why it is not a caching problem

Each signature replays its source Compare, and that Compare recovers two
positional-result Assertions. Recovering one calls
`_validate_result_assertion_ingress`, which re-reads the producing session's
complete ingress population to check the carried support equals it. Two per
signature, 16,156 signatures, 32,312 reads — the counted number exactly.

The population re-read is **300 occurrences**, and there are at most sixteen
distinct (session, boundary) pairs behind 32,312 reads. So a cache is available,
and two already exist in the codebase for exactly this
(`adjacent_pair_measurement.py:387`, `assertion_comparison.py:833`). Neither
covers this path, because `compare_positional_result_assertions` is a fresh
invocation per Compare and an invocation-local cache spanning two inputs holds
nothing across signatures.

**A cache is not the first thing warranted, because the read is 31x more
expensive than what the caller consumes.**

```text
  ids only, one column                          0.251 ms
  every column, no decode                       0.600 ms
  every column + JSON decode                    2.308 ms
  full ledger read as Events                    7.093 ms
```

**[measured]** The caller keeps `tuple(item.id for item in ...)`. It decodes 300
payloads — 264 KB, 902 bytes each — to read 300 identity strings and discards
the rest.

## Item 3 — an identity read, which is not a cache

`iter_session_kind_ids` on both ledgers: the same bounded rows in the same order,
selecting one column.

**Nothing is skipped by reading less.** `iter_session_kind` verifies no digest —
`#2416` deliberately kept verification off ordinary reads and left it with
`integrity_of`, which is a separate act and is unchanged here. So an identity
read forgoes no check the occurrence read performs.

**This is why it was preferable to the cache.** A cache raises a question an
identity read does not: whether the second read it elides would have detected
something the first could not. Here the answer would probably have been no —
the existing caches key on the boundary commitment, and a bounded read through a
committed boundary is meant to be repeatable — but the identity read never has
to be argued, because both reads still happen.

Held by test on both ledgers, at every boundary, including an absent kind and a
boundary that excludes later occurrences: `identities == occurrences`, always.

## Item 4 — the same findings, re-run

```text
                          before       after
  findings                     3           3
  counts              12,228/3,447/481    same
  elapsed                  299 s        64 s      4.7x
  get                     48,468      48,468
  integrity_of           113,092     113,092
```

**[measured]** Not just the counts. Every finding's assertion identity, subject,
content, scope and production-reference digest were serialised both times and
compared byte for byte.

**One instrument reading needs its caveat.** `iter_session_kind` fell from 32,313
to 1 — but the ingress reads did not stop happening; they moved to
`iter_session_kind_ids`, which the counter did not wrap. **The same number of
reads occur over the same rows.** Each one is cheaper. Anyone reading that line
as reads being eliminated is reading it wrong.

## What this establishes, and what it does not

**Establishes:** the count layer runs on a real population, is complete against
it, streams rather than accumulating, and produces findings independent of how
the ingress support is read.

**Does not establish** that 12,228 signatures sharing a canonical identity means
anything. `01.External:28` bounds a count to the counting assertion, and the
layer's own refusal — *"establishes no Equivalence, similarity, relation,
profile, meaning, significance, or Standing movement"* — is the disposition.
The largest group is the largest group.

**Does not close the cost question.** 64 s is still 32,312 reads of a population
that changed at most sixteen times, and `integrity_of` still repeats 2.5x over
44,544 distinct occurrences. Both remain available and neither was taken, because
one measured change is worth more than two unmeasured ones.

**Does not scale.** This is 16,156 signatures from 120 body-pairs at 16 bodies.
The pairs go as n squared and the reads go with them; 4.7x on a quadratic buys
one doubling of the corpus, not a corpus.
