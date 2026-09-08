# Developer semantic injection inventory 001

## Scope

This report inventories the coordinates in the operator interaction path whose
semantic content is supplied by developers rather than established from
preserved material. It records, for each, its current source, the PR that
introduced it, its current consumers, the exact Standing it bypasses, the
machinery that survives its removal, the expected lawful stop after removal,
and the tests that encode it.

It authorizes no construction and amends no active Book law. It proposes no
replacement content; naming a substitute would relocate the injection rather
than remove it.

Verified at `bce5784`.

## 1. The finding that governs the rest

This bootstrap has been implemented **three times** and removed twice.

```text
#2071   Separate closed-choice alternatives from represented sources
        seed_runtime/operator_ingress_common_grammar_prerequisite.py
        seed_runtime/closed_choice_selection_binding.py

#2107   Delete disconnected operator ingress probe scaffold
#2151   Delete demandless closed-choice binding branch
        both modules removed

#2298   Form and record bounded role-tagged Presentations
        seed_runtime/operator_presentation.py
        _DEVELOPER_SUPPLIED_SOURCES
```

The current instance is not the first attempt and it is not novel
contamination. The same three propositions, carrying the same first-contact
role, have been introduced, deleted as disconnected or demandless, and
reintroduced 147 PRs later inside a different module.

That recurrence is the strongest evidence in this inventory. A coordinate that
returns after deletion is not an accident of one campaign; it marks a position
the implementation cannot presently leave empty while still demonstrating a
completed path.

## 2. Inventory

### 2.1 Alternative propositions (`represented_source.meaning`)

```text
current source     seed_runtime/operator_presentation.py:19
                   _DEVELOPER_SUPPLIED_SOURCES, three entries:
                     "establish richer shared grammar with the operator"
                     "navigate to the current Standing View"
                     "establish no such goal and stop locally"

first introduced   #2298 (this module); #2071 (prior implementation)

consumers          operator_source_recovery.py   — becomes proposition M
                   operator_session_standing.py  — projector reconstructs
                                                   and refuses disagreement
                   operator_presentation.py      — formation, rendering

Standing bypassed  meaning-relation establishment. M is read from formation
                   testimony rather than warranted from preserved material.
                   Seed has no access to what these sentences mean.

survives removal   source-recovery Act, meaning-relation Act, the four-way
                   Authority separation, projector reconstruction, and the
                   refusal that a forged proposition cannot enter Standing

lawful stop        source recovery never runs; no meaning relation is
                   recorded; latest_meaning_relation stays None

tests encoding it  test_operator_presentation.py, test_operator_source_recovery.py,
                   test_operator_interaction_goal.py, test_operator_response_comparison.py
                   (8, 8, 9, 1 assertions respectively)
```

### 2.2 Source identity, kind, attribution, reference

```text
current source     operator_presentation.py:19-100
                   identity  "source:developer-supplied-grammar-acquisition-candidate"
                             "source:operator-ingress-view-navigation"
                             "source:developer-supplied-local-stop-treatment"
                   reference _CANDIDATE_SOURCE_REFERENCE (a Book path)

first introduced   #2299 (identities); #2298 (kind/attribution/reference)

consumers          operator_source_recovery.py (recovers G),
                   operator_session_standing.py (validates against formation)

Standing bypassed  represented-source identity. G exists because a developer
                   wrote a stable string, not because a source was recovered
                   from anything Seed holds.

survives removal   the A-to-G lineage mechanism, recovery validation, and the
                   refusal when a recovery disagrees with recorded formation

lawful stop        no alternative, therefore no identification, therefore no
                   source to recover
```

### 2.3 Roles and response coordinates

```text
current source     operator_presentation.py:19-100 (role strings)
                   operator_presentation.py:132 (coordinate = str(position))

first introduced   #2298

consumers          operator_response_comparison.py (coordinate set, bindings),
                   operator_session_standing.py (derivation and refusal),
                   operator_interaction_goal.py (role gate)

Standing bypassed  two different things, and they should not be conflated.
                   The coordinate assignment is mechanical enumeration and is
                   arguably not injection at all -- matching "1" against a
                   recorded coordinate is grammar Seed genuinely operates.
                   The role strings are injection: potential-goal /
                   presentation-navigation / local-stop are developer
                   classifications that gate Applicability.

survives removal   response-coordinate Compare and Identification entire,
                   including the binding-absent and binding-inapplicable
                   distinctions

lawful stop        Compare refuses at "recorded presentation has no
                   alternatives" -- verified empirically
```

### 2.4 Representation purpose and boundary

```text
current source     operator_presentation.py:19-100 (representation_purpose)
                   operator_presentation.py:135-160 (scope, provenance,
                   known_loss, unknowns, conflicts per alternative)

first introduced   #2299; the coordinate name itself dates to #2071

consumers          operator_source_recovery.py, operator_session_standing.py

Standing bypassed  the purpose for which each A-to-G relation was formed.
                   Applicability compares this against the Consumer purpose,
                   so a developer wrote both sides of that comparison.

survives removal   the per-alternative preservation boundary mechanism and
                   its reconstruction at projection

lawful stop        no alternatives, no representation boundaries to preserve
```

### 2.5 Consumer treatment relation

```text
current source     operator_presentation.py:53-70, instantiated at :135
                   treatment_kind, consumer_purpose, treatment,
                   authority_boundary, provenance, consumer_authority
                   (standing / supports / evidence / scope)

first introduced   #2307; structural form #2308

consumers          operator_interaction_goal.py (Applicability derivation,
                   Admission, consumption, goal Standing),
                   operator_session_standing.py (reconstruction and refusal)

Standing bypassed  Consumer Authority. This is the sharpest case. #2307's own
                   report records that no treatment or Consumer-Authority
                   relation existed in formation testimony, and that "the
                   smallest exact developer-supplied relation is added there
                   first". The gap was found and filled rather than left open.

survives removal   Applicability determination, Admission, consumption, goal
                   Standing establishment, the determination/treatment
                   Authority separation, all four bases, projector
                   reconstruction, duplicate-identity refusal

lawful stop        determine_goal_applicability returns
                   "no-consumer-treatment-relation"; nothing proceeds to
                   Admission. This is the pre-#2307 truth restored.

tests encoding it  test_operator_interaction_goal.py (9 assertions)
```

### 2.6 Consumer purpose constant

```text
current source     operator_session_standing.py:36, CONSUMER_PURPOSE

first introduced   #2307

consumers          operator_interaction_goal.py, operator_session_standing.py

Standing bypassed  the Consumer's own purpose. Applicability requires the
                   treatment relation's consumer_purpose to equal this
                   constant; both sides are developer-written, so the
                   agreement is guaranteed rather than established.

survives removal   the Responsibility structure, purpose coordinate, and
                   agreement check -- all of which remain meaningful once a
                   purpose arrives from somewhere other than a constant

lawful stop        no treatment relation to compare a purpose against
```

### 2.7 Rendered labels and renderer frame

```text
current source     operator_presentation.py:19-100 (labels)
                   operator_presentation.py:190-235 (frame strings:
                   "Bounded Presentation", "Respond with exactly one token:",
                   "Prior exchange:", "Current bounded interaction goal:",
                   the Session Standing block labels)

first introduced   #2298 (labels and frame); extended #2300, #2302, #2307

consumers          console output only; the labels are also carried through
                   identification and recovery results

Standing bypassed  the labels are injection on the same footing as the
                   propositions. The frame is a distinct case: some outward
                   rendering must exist and developers must write it. This
                   report does not classify the frame as injection, but
                   records that no line has been drawn and that a reader will
                   otherwise find the same pattern one layer down.

survives removal   rendering entire

lawful stop        with no alternatives the current renderer emits
                   "Respond with exactly one token:" followed by nothing --
                   a real defect requiring a conditional, verified empirically
```

## 3. Verified fail-closed behavior

The load-bearing claim -- that the machinery survives removal -- was tested by
emptying `_DEVELOPER_SUPPLIED_SOURCES` and changing nothing else:

```text
C0 formed and emitted        alternatives: 0
E1 "hello" preserved         meaning Unknown, C0 lineage recorded
Compare                      refused: "recorded presentation has no alternatives"
goal path                    {"outcome": "no-validated-meaning-relation"}
projector                    1 presentation, 0 comparisons, 0 goal standings
```

Every gate refused on the first attempt without modification. The refusals were
written for integrity -- to stop forged or incomplete chains -- and serve as
dormancy unchanged.

**Consequence for any excision:** it is smaller than a description in terms of
"making the gates fail closed" implies. The gates already do. Source recovery
needs no change to require warranted Standing; it never runs. Applicability
needs no change to leave the gap open; it already returns
`no-consumer-treatment-relation`. The excision is a deletion plus a renderer
conditional.

## 4. Tests encoding the injection

```text
tests/test_operator_interaction_goal.py      9 assertions
tests/test_operator_presentation.py          8
tests/test_operator_source_recovery.py       8
tests/test_operator_response_comparison.py   1
```

These assert the literal propositions, the developer-supplied attribution, the
role names, and the treatment relation's coordinates. They are not incidental
fixtures: several exist specifically to prove the injection is *preserved
faithfully* -- that M comes only from formation testimony, that ingress text
cannot alter it, that a forged proposition is refused.

Those tests remain valuable. What they prove is that the developer's
proposition is carried without corruption, not that the proposition is Seed's.

## 5. What this inventory does not establish

```text
that the injected coordinates should be removed
that removal is presently warranted
that any replacement content exists or should be written
that the renderer frame is or is not injection
that coordinate enumeration is injection
that the prior deletions (#2107, #2151) were correct
```

The recurrence recorded in section 1 is evidence that the position resists
being left empty. It is not evidence about whether it should be.

## 6. Exact Unknowns

```text
what would put an alternative into a Presentation that Seed can read
whether role classification is separable from proposition injection
where the line falls between injected content and necessary renderer frame
whether the three propositions returning after two deletions indicates a
  requirement, a habit, or an absence of any alternative
what Standing a Presentation lawfully exposes when Standing is empty
```

## Materials inspected

```text
seed_runtime/operator_presentation.py
seed_runtime/operator_session_standing.py
seed_runtime/operator_source_recovery.py
seed_runtime/operator_response_comparison.py
seed_runtime/operator_interaction_goal.py
scripts/seed_local.py
tests/test_operator_{presentation,source_recovery,response_comparison,interaction_goal}.py

git log -S across seed_runtime/ for each injected coordinate
git log --diff-filter=D for the removed prior bootstrap modules
live fail-closed test with the source table emptied
```
