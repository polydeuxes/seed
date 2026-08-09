# The d1 battery across sixteen sources: experiment 010

Findings only. No runtime or Book amendment. No explanation offered.

## Summary

d1 only, twenty fresh permutations per source, the same 300-line window and the
same one-half overlap criterion used since `#2396`. A baseline taken **before**
any composition destroys source isolation.

```text
source           words  recur  cand   ordered   shuffled min..max  mean   >= ordered
  euclid          3646    328   256      157         9..38        18.4      0/20
  emerson         3417    308   268       78         4..27        10.4      0/20
  algebra         1295    161    95       67         3..23         9.7      0/20
  franklin        2939    316   269       23         5..14         8.6      0/20
  austen          2774    306   271       20         0.. 9         4.5      0/20
  latin_vulgate   2466    277   218       20         7..19        11.9      0/20
  cookbook        1387    210   146       12         1.. 9         4.1      0/20
  roget           2445    277   206        5         0.. 2         0.1      0/20
  boole           1997    265   186       27         3..28        11.2      1/20
  ---------------------------------------------------------------------------
  grammar_brown   2801    259   211        7         1..21         5.9      5/20
  webster         1267    129    87        2         0.. 7         1.2      5/20
  grammar_kittr   1494    161   137        2         0.. 4         1.4      7/20
  dickens         2659    289   250        6         1..10         4.5      7/20
  bash_guide      1096    152   108        2         0.. 7         1.9     10/20
  hume            1616    216   146        3         0.. 6         2.9     10/20
  french_hugo     2324    217   189        2         0.. 5         2.0     11/20
```

**Eight of sixteen sources separate cleanly. Brown is among the worst.**

The whole arc from `#2395` to `#2407` treated Brown as the normal case and
Roget as the exception, and asked why Roget separates. **That question was
backwards.** Separation is the common outcome across this battery, and Brown is
one of seven sources that fail it.

## 1. The groupings a reader expected are not there

**[measured]** Both grammar books fail. `grammar_brown` at 5/20 and
`grammar_kittr` at 7/20. Whatever the physiology responds to, it is not
"a book about English grammar".

**[measured]** Ordinary prose falls on both sides. Austen, Franklin and Emerson
separate at 0/20; Dickens at 7/20 and Hume at 10/20 do not. Genre does not
sort this.

**[measured]** The two non-English adversaries split. `latin_vulgate`
separates at 0/20; `french_hugo` fails at 11/20. The physiology is **not**
English-only, and it is also not uniform outside English.

**[measured]** Webster fails at 5/20 while Roget separates at 0/20. Both are
reference works organised by entry.

## 2. One thing the outcomes do line up with

**[measured]** Every source that fails to separate produced an ordered count of
7 or below. Every source that separates produced 12 or above, except Roget at 5.

```text
  fails to separate    ordered counts   2, 2, 2, 3, 6, 7
  separates            ordered counts   5, 12, 20, 20, 23, 27, 67, 78, 157
```

**[Unknown]** Whether that is a property of the sources, of the measurement, or
of a comparison too small to resolve when the counts are small. Nothing here
distinguishes those, and this report offers no account of it.

**[inference]** A source producing two overlaps cannot separate from a
permutation population reaching seven, whatever the material holds. In that
region the outcome may be reporting the size of the numbers rather than the
arrangement behind them. That is the operator's flatness observation from
`#2406` appearing as a pattern across sources rather than within one.

## 3. Internal check

**[measured]** The battery reproduces `#2406`'s two d1 rows exactly:

```text
  grammar_brown   ordered 7   1..21   mean 5.9   5/20      as #2406
  roget           ordered 5   0.. 2   mean 0.1   0/20      as #2406
```

The sweep is doing what the earlier runs did.

## 4. Disclosures

**300 lines is not a matched quantity of material.** The windows range from
1,096 words (`bash_guide`) to 3,646 (`euclid`). Recurring representations range
from 129 to 328. `#2401` established that recurrence, not volume, is the match
that matters, and this battery **is not matched on it**. Both numbers are
printed above so a reader can see what was compared.

**Two of the strongest separators are not the books they name.** `boole` is
LaTeX source and `euclid` is tag-stripped HTML, as `corpus/SOURCES.md` records.
Regular markup is exactly the kind of repeated arrangement this measurement
finds, and neither result should be read as being about Boole or Euclid until
that is ruled out.

**`algebra` used a different window.** It has 3,956 lines and cannot supply
`[6000:6300]`. It was measured at `[1800:2100]`.

**The one-half overlap criterion is still unvaried**, as disclosed in `#2406`
and `#2407`.

**These are pair findings, not relations**, per `#2408`.

## 5. What this does not establish

**Any account of why sources differ.** Curator asked for a baseline with no
explanation, and none is offered. The section 2 co-occurrence is recorded
because it is visible in the table, not because it explains anything.

**That the separating sources hold more structure.** `#2395` holds: a
measurement family failing to distinguish ordered from shuffled material
establishes nothing about the material, and this report relies on that in seven
rows.

**That any source is ranked.** The table is grouped by outcome and ordered
within groups for reading. Neither is a ranking, and the ordered counts are not
comparable across sources that were never matched on recurrence.

**That the battery is complete.** Sixteen sources, one window each, one
displacement, one criterion, twenty permutations.
