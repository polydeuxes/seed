# Question graph pass 090 — evidence fidelity correction

## Correction boundary

This pass corrects archival overreach from pass 089 without changing graph nodes, graph edges, classifications, Book doctrine, runtime code, or tests. The correction is evidentiary naming only: current-facing Book language remains non-canonical, while repository and report names are restored when they identify the evidence supporting a standing.

## Restored evidence names

- `QuestionFamily` is restored where the graph identifies the implementation artifact realizing the constitutional standing “public answer family.” The constitutional standing is still “public answer family”; the implementation/report evidence name is `QuestionFamily`.
- `Question Shape` is restored where the graph identifies historical reports or recovered testimony about recurring bounded forms of asking. The Book-facing standing remains “question form.”
- `Survey Warrant Family` is restored where the graph identifies historical reports or recovered testimony about methodological warrant families. The Book-facing standing remains “methodological warrant.”

## Preserved distinction

Constitutional standing is not implementation or report evidence name. Therefore:

```text
constitutional standing != implementation or report evidence name
```

The present-facing Book vocabulary remains non-canonical and unchanged:

```text
question form
methodological warrant
public answer family
```

The archival/current-state artifact may cite literal evidence names only to identify the supporting implementation or report testimony:

```text
public answer family <- evidenced by `QuestionFamily` where exact inventory evidence exists
question form <- evidenced by `Question Shape` where historical report testimony is being named
methodological warrant <- evidenced by `Survey Warrant Family` where recovered testimony is being named
```

## Pass 089 correction

`question_graph_pass_089_current_state.md` remains the current-state artifact. Its graph structure is unchanged. The pass now restores literal evidence names at the evidence-identification points and its final line is restored to the recovery-completion line required for the current-state artifact.

## Book and implementation status

No Book clause changes are made. No runtime code changes are made. No tests are changed. No diagnostic, audit, probe, view, operational CLI flag, or recordable output is added or modified.

Question graph evidence fidelity correction complete.
