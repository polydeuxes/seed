from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_sensing_remembering_trajectory_learning_invariants_are_canonical():
    text = _read("book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md")

    required = [
        "External provider material is not an Observation",
        "an Observation is Seed-native testimony formed after acquisition and interpretation, not environment truth",
        "sensing is not remembering",
        "Observation history is not trajectory or transition standing",
        "Retaining `up at t1`, `down at t2`, and `up at t3` does not establish outage, recovery, flapping, trajectory, trend, transition, consequence, cause",
        "Retained history is not learning",
        "changed stored data is not learning",
        "Learning establishment is not learning consumption",
        "learning is not adaptive reliance",
        "changed selection is not lawful adaptation automatically",
        "learning is not model training by identity",
        "Movement followed by outcome does not establish that the movement caused the outcome",
        "ObservationIngestor's current compressed road from Observation to evidence-linked Fact-shaped artifact does not independently establish Fact standing",
        "Activity visibility, including ExecutionStatus-style status emission, is not a sensing result, operational measurement, capability testimony, gap standing, interaction outcome, or learning",
    ]

    for invariant in required:
        assert invariant in text


def test_need_gap_and_capability_demand_invariants_are_canonical():
    text = _read("book_of_seed/03-goals-and-advancement/needs-and-opened-movement.md")

    required = [
        "A need is not a gap by identity",
        "Need established does not open movement",
        "insufficiency is not permission to act",
        "a gap is not authorization",
        "a gap does not automatically establish a capability demand",
        "current difference is not material gap automatically",
        "an unresolved question is not a failed capability",
        "There is no free-floating gap standing without that reference condition and scope",
        "Unknown capability is not absent capability",
        "one unsupported candidate is not a capability gap",
        "Capability demand is not capability",
        "not selected mechanism",
        "not authorization",
        "New observation is not gap revision automatically",
        "changed current State is not changed gap standing automatically",
        "gap revision is not movement authorization",
        "Does every gap open movement? No.",
        "Does a gap automatically establish a capability demand? No.",
        "Can passive observation revise capability or gap standing? Yes, after bounded examination and establishment.",
    ]

    for invariant in required:
        assert invariant in text


def test_capability_interaction_outcome_and_adaptation_invariants_are_canonical():
    text = _read("book_of_seed/07-operational-realization/operational-realization-and-capability.md")

    required = [
        "declared capability != verified capability",
        "capability is not mechanism, reachability, authority, reliance warrant, movement selection, or selected mechanism",
        "one successful observation does not establish general capability",
        "one successful episode does not verify a general capability",
        "one failed episode does not establish capability absence",
        "selection is not realization",
        "handoff is not realization",
        "realization report is not verified effect",
        "after-observation is not attributed result",
        "interaction episode is not causal proof or learning automatically",
        "Movement occurred is not gap reduced",
        "gap reduction is not complete need satisfaction or causal proof",
        "local outcome is not universal capability",
        "failed outcome is not capability absence automatically",
        "learned capability is not selected movement",
        "learned gap is not permission to act",
        "adaptive reliance is not automatic execution",
        "Is a capability identical to a mechanism? No.",
        "Does one successful interaction verify a general capability? No.",
        "Does one failed interaction establish that a capability is absent? No.",
        "Does gap reduction prove that the selected movement caused the result? No.",
        "Must a later selector consume raw historical episodes directly? No.",
        "Does a selector changing its answer prove learning? No.",
        "Is learning constitutionally identical to model training? No.",
        "Are trajectory, interaction-outcome, gap-revision, capability-revision, learning, adaptive-reliance, or causal-standing implementations complete today? No.",
    ]

    for invariant in required:
        assert invariant in text
