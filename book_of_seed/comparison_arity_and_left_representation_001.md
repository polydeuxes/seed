# Correcting #2420's arity leak and its missing coordinate

Runtime amended narrowly. No Book amendment.

## 1. The runtime implemented what its report disclaimed

`#2420`'s report said:

> **That the comparison is complete.** It compares two findings. Comparing more
> than two, comparing across workspaces, and consuming comparison findings are
> all unbuilt.

**[measured]** `compare_preserved_findings` refused fewer than two and duplicate
ids, then ran `set.intersection(*occupant_sets)` over however many were
supplied. **Three-body comparison existed and worked.**

**[inference]** This is the worse of the two defects here, and not because of
its size. A report disclaiming a capability the code has is how accidental
competence is discovered later through use rather than through review — and the
sentence would have been cited as evidence the capability was absent.

**Repaired.** Exactly two, and the refusal says why:

```text
a bounded comparison consumes exactly two preserved findings; 3 supplied.
Comparing more than two is unbuilt
```

**[inference]** Two is not a convenience. What more than two inputs *jointly*
establish is not recovered anywhere, and an intersection over n findings is not
that recovery — it is one operation standing in for an unasked question. When
the n-ary case is wanted it needs its own recovery, and this refusal is where
that will be noticed.

## 2. Pair identity was reconstructable only from prose

**[measured]** The comparison distinguished `representation_measured`,
`equivalence_rule`, `counting_scope`, `measured_position`, `measurement_form`
and `bounded_exchange` — but not `measured_left_representation`, which every
measurement finding already carries structurally.

**[measured]** `representation_measured` is a sentence, not a coordinate. In
`#2420`'s layer C the anchor was fixed to `'the'` for every body, so nothing
needed to ask which anchor a finding measured from.

**[inference]** The question layer C actually exists to answer needs it:

```text
  ('because', 'therefore') at d1        left   same
  ('because', 'therefore') at d7        right  same
                                        displacement  different
```

Establishing that without the coordinate means parsing prose, or knowing the
anchor because a reader fixed it. Both put the reader back inside the
comparison, which is what `#2420` was built to remove.

**Repaired.** `measured_left_representation` is a compared coordinate, and the
subject-sameness that gates `agreement` now requires it to match. Two findings
that measured from different anchors are `Unknown` even when everything else
agrees.

## 3. What this does not change

**The relation disposition.** Cross-exchange comparisons still produce
`Unknown`, on the same basis. Nothing here loosens that.

**Layer C's result.** `#2420`'s run compared occupants after `'the'` and its
numbers stand. This report does not rerun it.

**What layer C still is not.** `#2420` ran one representation per body.
The full-range pair findings of `#2413`–`#2417` were computed in experiment code
and never recorded, so Seed still cannot consume them, and the real layer C —
every available displacement, exact left and right — has not been run.

## 4. What this does not establish

**That the remaining coordinates are complete.** Two were found missing or
unbounded by review. The comparison distinguishes seven coordinates now, and
nothing establishes that seven is the right number.

**That refusing three inputs is constitutionally required.** `05.Testimony.E`
says "multiple", which does not mean two. The refusal reflects what is
*recovered*, not what the clause forbids, and the report now matches the code in
saying so.
