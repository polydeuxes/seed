# What the exhausted cycle found: characterization 001

Findings only. No runtime or Book amendment. `#2394` used unchanged.

## Executive

`#2394` proved the cycle continues itself and exhausts. It never looked at what
the 809 findings contained. This looks.

**It found the closure of its own forms, not structure in the material.**

**The cycle exhausts at every scale tested**, in 16–18 passes whether the
material offers 265 or 1,386 representations. The pass count is near-constant;
the work per pass grows.

**Distributional structure is absent.** Representations whose measured
right-context sets overlap appear to emerge with more material — 0, then 3,
then 7 — and **a control destroys the result**. The same material with its
order shuffled produces 1, 8, and 9 under three seeds. Seven is inside that
band.

So the apparent classes are what sparse two-element sets produce by
coincidence. Without the control this report would have said otherwise.

## 1. The cycle exhausts at every scale

Ordinary prose, seeded with one finding on a representation the material
offered:

```text
lines   representations  recurring  findings  passes  exhausted
   40               265         62     1,761      18       yes
  120               642        136     4,366      16       yes
  300             1,386        259    10,100      17       yes
```

**[inference]** The pass count does not grow with the material. A finite set of
forms over a finite vocabulary closes, and it closes at about the same depth
regardless of how much vocabulary there is. Findings grow roughly linearly with
lines — 44, 36, 34 per line.

## 2. What the first run actually walked into

`#2394`'s 40-line run took lines 2000–2040, and the representations it measured
relative to most often were:

```text
69  'pp.'      41  'London,'   33  '12mo,'   33  'Ed.,'
29  '1st'      25  'English'   25  'M.;'     25  'the'
```

That region is a bibliography. The 809 findings map the structure of a
bibliography, which is the structure that was there.

**[inference]** The exhaustion result is about the forms closing. It is not a
claim that the material was exhausted of structure, and reading it as one would
be reading a property of the method as a property of the corpus.

## 3. Why nothing distributional could have appeared at that size

Of 141 representations with a measured right-context set in that run:

```text
  0 occupants   16 representations
  1 occupant   105 representations
  2 occupants   14
  3+             6
```

Only 26 of 146 representations occurred more than once in 40 lines. A
representation seen once has one successor, and singletons share nothing by
construction.

## 4. The control, and what it destroys

At 300 lines of prose, 211 representations have a right-context set of two or
more, and seven pairs share at least half of it. Those seven look like this:

```text
1.00  'me'       ~ 'reign,'      shared = ['and', 'the']
1.00  'phrases'  ~ 'prosperity'  shared = ['in',  'of' ]
0.67  'liberty'  ~ 'word'        shared = ['of',  'to' ]
0.67  'force'    ~ 'men'         shared = ['and', 'of' ]

and one shared left-context set:
  'Province', 'force'   both preceded by ['a', 'the']
```

A reader recognises those. That is the reason for the control.

**Same material, same measurement, order destroyed:**

```text
ORIGINAL order       reps=1386   ctx>=2: 211   overlaps = 7
SHUFFLED (seed 0)    reps=1386   ctx>=2: 239   overlaps = 1
SHUFFLED (seed 1)    reps=1386   ctx>=2: 234   overlaps = 8
SHUFFLED (seed 2)    reps=1386   ctx>=2: 234   overlaps = 9
```

Shuffling destroys every adjacency relation the material had. Whatever survives
is coincidence. It produces **1, 8, and 9**. The original produces **7**.

**[inference] The overlaps are not evidence of structure.** Two representations
each measured with two successors share both often enough that ordered and
disordered material are indistinguishable at this scale.

**What this would have become without the control.** `'Province'` and
`'force'`, both preceded by `'a'` and `'the'`, is exactly the shape a reader who
knows English wants to call a class. Reporting it would have repeated the defect
`recurrence_consumer_first_recovery_001` recorded — significance supplied by the
reader, not the measurement — with better machinery underneath it.

## 5. What was actually found

```text
found        the closure of the forms over the material, reliably,
             in 16-18 passes at every scale tested

found        that depth does not become strength: at premise depth 25 the
             recorded authority is still measurement evidence only, and
             what any representation means is still Unknown

not found    distributional structure
not found    classes, categories, or kinds
not found    anything the shuffled control does not also produce
```

## 6. What this does not establish

**That the material has no distributional structure.** §4 establishes that
**this measurement at this scale** cannot distinguish it from noise. 300 lines
gives most representations one occurrence.

**That more material would find it.** The overlap count rose 0, 3, 7 while the
control band sits around 1–9. Whether the two separate at larger scale is
untested, and the linear growth in findings makes the cost of testing knowable
but not free.

**That the four forms are the right ones.** They are four adjacency questions.
Nothing establishes that distributional class structure, if present, is visible
to them.

**That Jaccard at 0.5 is the right comparison.** It is one threshold on one
similarity, chosen for this characterization, and the control invalidates the
result at that setting rather than validating the setting.

**That the bibliography region was unrepresentative.** §2 records what it was.
§1's runs used prose and behaved the same way.

**That the exhaustion is a Stop.** `#2394` recorded this; a pass forming no new
measurement is a harness declining to repeat a finite question.

## 7. What follows

The loop works and the material is thin. The measurement that would settle §6's
first two questions is the same one run here, at a scale where most
representations recur — with the shuffled control run alongside it every time,
because at this scale the control is the only thing separating a finding from a
reader's recognition.
