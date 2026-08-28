# Nested result content address census 001

## Question

Recorded pair Compare findings are exact content inside one recorded Compare
result. A later Compare result formerly referenced each finding with:

```text
recorded comparison occurrence
finding category
finding position
copied finding subject
```

This census asks whether the copied subject establishes any distinction beyond
the parent result occurrence and its exact local coordinates.

## Exact parent content

The recorded pair Compare result already records a complete findings structure:

```text
findings
├── same_content_findings[position]
├── conflicting_findings[position]
├── findings_of_earlier_result[position]
└── findings_of_later_result[position]
```

Each addressed entry contains its exact subject and comparison content. The
category is part of the local coordinate because one integer position can occur
in more than one category. The position is local to one exact parent Compare
result occurrence.

Therefore the exact address is:

```text
recorded comparison result occurrence
+ finding category
+ finding position
```

A bare category and position do not address content in another result
occurrence.

## Subtraction

The copied `subject` field was removed from every live comparison-finding
reference. A reader now follows the parent occurrence, selects the exact
category, selects the exact position, and validates the addressed finding's
subject there.

The subtraction preserves:

```text
complete recorded Compare findings
exact pair selection
ordered-path Compare Applicability
ordered-path Compare results
Distinction Measurement
current-coordinate reads
durable replay
mutation refusal
```

Changing the category or position makes the reference address different or
absent parent content and is refused. Equal local positions in separate parent
result occurrences remain separate exact addresses.

## Result

```text
copied finding subject in later reference       not established
parent recorded result occurrence               exact
finding category                                exact local coordinate
finding position                                exact local coordinate
subject inside addressed parent content         exact
new generic address object                      not introduced
```

This is the same recovered physiology already established for ordinary result
content:

```text
exact parent occurrence
+ exact result-local coordinate
→ exact addressed content
```

The local coordinate may be one `result_position`, or it may be the structured
pair `finding_category + finding_position`. The containing occurrence remains
part of the exact coordinate in both cases.
