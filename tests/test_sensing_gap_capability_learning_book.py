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


def test_book_vii_capability_chapter_remains_absent():
    assert not (ROOT / "book_of_seed/07-operational-realization/operational-realization-and-capability.md").exists()
    assert not (ROOT / "book_of_seed/07-operational-realization").exists()


def test_constrained_movement_grammar_invariants_are_canonical():
    text = _read("book_of_seed/03-goals-and-advancement/orientation-and-movement.md")

    required = [
        "Constitutional movement is a warranted transition in lawful position, standing, or advancement posture",
        "Movement is not mutation by identity",
        "Standing is not a durable object by identity",
        "a named constitutional subject does not require a dedicated artifact",
        "changed standing does not automatically open later movement",
        "Does constitutional movement require runtime mutation? No.",
    ]

    for invariant in required:
        assert invariant in text


def test_constrained_constraint_invariants_are_canonical():
    text = _read("book_of_seed/02-acts-and-constraints/constraints-policy-and-preconditions.md")

    required = [
        "A constraint is not the governed movement",
        "a constraint result is not performance of the governed movement",
        "a constraint is not a sequential pipeline stage",
        "which movement remains admissible",
        "which standing may be relied upon",
        "A constraint result can lawfully admit, block, narrow, redirect, defer, or leave unchanged a later movement",
        "Does a constraint result perform the movement it governs? No.",
    ]

    stale_anchors = [
        "ToolExecutionPolicyService",
        "ToolExecutor.execute",
        "seed_runtime/tool_execution_policy.py",
        "seed_runtime/execution.py",
    ]

    for invariant in required:
        assert invariant in text

    for stale_anchor in stale_anchors:
        assert stale_anchor not in text


def test_constrained_movement_correction_records_stale_anchor_follow_up():
    text = _read("book_of_seed/constrained_movement_sensing_gap_capability_learning_correction_001.md")

    required = [
        "PR 1901 initially reported that no false current-repository anchors were encountered",
        "A subsequent direct repository check established that `ToolExecutionPolicyService` and `ToolExecutor.execute` were still listed as representative anchors despite their modules being absent from current main",
        "The stale anchors were removed in this bounded follow-up",
        "Historical report mistake != constitutional grammar invalid",
        "Stale implementation witness != constitutional responsibility invalid",
        "Deleted executor != constraint grammar deleted",
    ]

    for invariant in required:
        assert invariant in text


def test_constrained_evidence_learning_and_causation_invariants_are_canonical():
    text = _read("book_of_seed/05-evidence-and-knowledge/testimony-and-established-fact.md")

    required = [
        "Sensing produces testimony that may support later evidentiary movement",
        "it is not advancement",
        "Observation produced is not testimony admitted",
        "Remembering preserves recoverability across time",
        "Remembering does not perform later reliance",
        "Trajectory establishment may be understood, where warranted, as constrained movement from occurrence history to bounded temporal understanding",
        "Retained history is not trajectory establishment",
        "Learning establishment may be understood as constrained constitutional movement in retained understanding",
        "Learning establishment is not storage mutation",
        "or adaptive reliance",
        "Adaptive reliance is later movement constrained by the result of earlier movement in understanding",
        "adaptive reliance is not automatic execution",
        "Association standing is not causal standing",
    ]

    for invariant in required:
        assert invariant in text


def test_constrained_need_gap_and_demand_invariants_are_canonical():
    text = _read("book_of_seed/03-goals-and-advancement/needs-and-opened-movement.md")

    required = [
        "Need and gap are disciplines governing possible advancement, not permission to advance",
        "Gap established does not perform movement",
        "Gap family names are not a subclass hierarchy",
        "Evidence gap constrains establishment movement",
        "Knowledge gap constrains answer or explanation movement",
        "Capability demand is a constraint on candidate formation and realization inquiry",
        "capability demand established is not capability exists",
        "Gap revision may be understood as constrained movement in insufficiency standing",
        "Gap revision is not movement authorization",
        "Is gap primarily one universal object family? Not by default",
        "Does an established gap itself perform movement? No.",
    ]

    for invariant in required:
        assert invariant in text


def test_constrained_book_vii_capability_chapter_remains_absent():
    assert not (ROOT / "book_of_seed/07-operational-realization/operational-realization-and-capability.md").exists()
    assert not (ROOT / "book_of_seed/07-operational-realization").exists()


def test_constrained_stopping_invariants_are_canonical():
    text = _read("book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md")

    required = [
        "Stopping may be constrained by evidence gap, capability Unknown, authority gap, resource insufficiency, unresolved causation, preservation failure",
        "may require stop, defer, narrow, return to inquiry, expose insufficiency, or refuse reliance",
        "Stopping is not failure",
        "Unknown is not permission to invent movement",
    ]

    for invariant in required:
        assert invariant in text
