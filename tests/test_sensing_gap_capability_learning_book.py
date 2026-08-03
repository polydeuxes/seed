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


def test_demand_gap_and_capability_demand_invariants_are_canonical():
    text = _read("book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md")

    required = [
        "The canonical goal-advancement Demand families are clarification, inquiry, authority, and operational realization",
        "Demand established does not open movement",
        "Demand standing must remain recoverable",
        "Establishment establishes bounded required-result standing",
        "there is no Need -> Demand transition",
        "They are not an exhaustive constitutional Demand taxonomy",
        "Demand is not Gap, Capability, capability candidate, mechanism candidate, selection, authorization, execution, or movement",
        "“Capability demand” is not evidenced as an independent constitutional kind between Demand and Capability",
        "Demand established != candidate producer exists",
        "Gap evidence may support Demand establishment",
        "Gap does not automatically establish Demand",
        "Unknown capability is not absent capability",
        "One unsupported candidate is not a capability Gap",
        "Candidate-, reachability-, selection-, or warrant-shaped testimony",
        "New observation is not automatic Gap revision",
        "Gap revision is a separate evidence-supported revision of scoped incompatibility; it is not authorization",
        "A Gap resolved within scope does not mean all advancement is complete",
    ]

    for invariant in required:
        assert invariant in text


def test_canonical_navigation_uses_demand_and_bounds_former_need_vocabulary():
    concordance = _read("book_of_seed/concordance.md")

    required = [
        "| goal-advancement Demand |",
        "[Demands and opened movement](03-goals-and-advancement/demands-and-opened-movement.md)",
        "former advancement-need vocabulary",
        "former `NeedFamily` implementation vocabulary",
        "Demand != Gap",
        "Gap != Demand by identity",
        "Demand != Capability",
        "Demand established != movement opened",
        "“Capability demand”**: noncanonical shorthand for Demand content",
        "It is not an independent constitutional kind, Capability, mechanism, selected mechanism, authorization, or execution",
    ]
    stale = [
        "| advancement need |",
        "[Needs and opened movement]",
        "claim standing, evidence, need",
        "addressing a declared need or gap",
    ]

    for invariant in required:
        assert invariant in concordance

    for residue in stale:
        assert residue not in concordance

    assert "orientation, Demand, selection" in _read("book_of_seed/03-goals-and-advancement/README.md")
    assert "no selected movement != no remaining Demand" in _read(
        "book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md"
    )


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


def test_constrained_demand_gap_invariants_are_canonical():
    text = _read("book_of_seed/03-goals-and-advancement/demands-and-opened-movement.md")

    required = [
        "A **Demand** states what result, relation, clarification, inquiry, authority, transformation, competency, or other bounded condition is required under an exact responsibility and scope",
        "A family label is not an exact Demand",
        "A projection container is not an established Demand",
        "An absent projection does not mean Demand absent",
        "Unknown is not unsupported",
        "A **Gap** is an evidence-supported scoped incompatibility relative to a declared reference condition and responsibility",
        "Demand can exist without an established Gap, and Gap can exist without an established Demand",
        "common-grammar standing required by the exact consumer",
        "bounded relational Demand",
        "exact family:\n    Unknown",
        "Recurrence supplies measurement evidence only",
        "it is not a global language state or a competency by identity",
    ]

    for invariant in required:
        assert invariant in text


def test_operator_ingress_common_grammar_clause_has_no_unsupported_examination_assignment():
    text = _read(
        "book_of_seed/03-goals-and-advancement/operator-ingress-common-grammar-prerequisite.md"
    )

    required = [
        "Common-grammar standing remains relative to the consumer, material, act, purpose, participants, and scope",
        "Exact token binding is not free-form interpretation",
    ]

    for invariant in required:
        assert invariant in text

    unsupported = [
        "## Bounded common-grammar interpretation examination",
        "communicative interpretation-examination responsibility",
        "first interpretation-examination responsibility",
        "Seed owns this constitutional act generally",
        "whose declared communicative examination requires",
    ]

    for claim in unsupported:
        assert claim not in text


def test_constrained_book_vii_capability_chapter_remains_absent():
    assert not (ROOT / "book_of_seed/07-operational-realization/operational-realization-and-capability.md").exists()
    assert not (ROOT / "book_of_seed/07-operational-realization").exists()


def test_constrained_stopping_invariants_are_canonical():
    text = _read("book_of_seed/08-authority-communication-and-stopping/stopping-and-completion.md")

    required = [
        "Stopping may be constrained by evidence gap, capability Unknown, authority gap, resource limits, unresolved causation, preservation failure",
        "may require stop, defer, narrow, return to inquiry, expose unmet requirements, or refuse reliance",
        "Stopping is not failure",
        "Unknown is not permission to invent movement",
    ]

    for invariant in required:
        assert invariant in text

    assert "resource insufficiency" not in text
    assert "expose insufficiency" not in text
