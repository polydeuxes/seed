"""Generic relation observation over preserved external material.

The observer is never given a candidate to look for. It enumerates which
representations recur, which share a leading form, and which occur next to
which, and whatever the source put there appears in the answer.

**The material below is developer-written.** Any regularity in it -- a
recurring marker, a recurring blank line -- is a property of strings typed in
this file, not a discovery about any real corpus. These tests therefore assert
the *mechanism*, never that a particular form was found. `corpus/` is
gitignored, so no test here can run against real acquired material.
"""

from __future__ import annotations

import hashlib

import pytest

from seed_runtime.external_material_relation_observation import (
    ExternalMaterialRelationObservationError,
    external_material_relation_observation_json,
    format_external_material_relation_observation,
    observe_external_material_relations,
)
from seed_runtime.external_material_structural_projection import (
    ExternalMaterialStructuralProjectionRequest,
    project_external_material_structure,
)
from seed_runtime.external_material_testimony_binding import (
    ExternalMaterialManifest,
    ExternalMaterialSelectedArtifactRecord,
    ExternalMaterialSourceRecord,
)

MATERIAL = (
    "MARK 1.--alpha\n"
    "\n"
    "MARK 2.--beta\n"
    "\n"
    "MARK 3.--alpha\n"
    "plain line\n"
)


def _projection(text: str = MATERIAL):
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    manifest = ExternalMaterialManifest(
        manifest_id="m:test",
        sources=(
            ExternalMaterialSourceRecord(
                source_id="s:test",
                source_identity="developer-written fixture",
                source_kind="external_text",
                provenance="written in this test module",
            ),
        ),
        selected_artifacts=(
            ExternalMaterialSelectedArtifactRecord(
                artifact_id="a:test",
                parent_source_id="s:test",
                artifact_hash=digest,
                line_count=len(text.splitlines(keepends=True)),
                character_count=len(text),
                selection_bounds="whole fixture",
            ),
        ),
    )
    request = ExternalMaterialStructuralProjectionRequest(
        manifest_id="m:test",
        source_id="s:test",
        artifact_id="a:test",
        expected_artifact_hash=digest,
        encoding="utf-8",
        exact_text=text,
    )
    return project_external_material_structure(manifest, request)


@pytest.fixture(scope="module")
def observation():
    return observe_external_material_relations(_projection())


# --------------------------------------------------------------------------
# 01.External:28 requires three disclosures on any recurrence assertion.
# --------------------------------------------------------------------------


def test_the_three_mandatory_disclosures_are_carried(observation):
    """`01.External:28`: the representation measured, the sameness rule, the scope."""
    assert "exact line text" in observation.representation_measured
    assert "byte-for-byte equality" in observation.equivalence_rule
    assert "no case, whitespace, punctuation, or unicode normalization" in (
        observation.equivalence_rule.lower()
    )
    assert "one selected artifact within one manifest" in observation.counting_scope


def test_the_scope_disclaims_the_wider_source(observation):
    """Counting inside one artifact says nothing about material outside it."""
    assert "not counted and not claimed absent" in observation.counting_scope


# --------------------------------------------------------------------------
# Findings are enumerated from the material, never tested against candidates.
# --------------------------------------------------------------------------


def test_the_observer_accepts_no_candidate_to_look_for():
    """The signature admits a projection and nothing else.

    This is the whole safeguard. An observer that accepted a pattern would let
    the caller choose the measurement to match material the caller already
    understood.
    """
    import inspect

    parameters = inspect.signature(observe_external_material_relations).parameters
    assert list(parameters) == ["structural_projection"]


def test_recurrence_is_counted_not_asserted(observation):
    """Every distinct representation is reported with its own occurrence count."""
    counts = {f.representation: f.occurrence_count for f in observation.equality_findings}
    assert counts["MARK 1.--alpha\n"] == 1
    assert counts["\n"] == 2
    assert observation.recurring_representation_count == 1
    assert observation.distinct_representation_count == len(counts)


def test_equal_representations_carry_every_line_that_holds_them(observation):
    blank = next(f for f in observation.equality_findings if f.is_blank)
    assert blank.occurrence_count == len(blank.line_ids) == len(blank.line_numbers)
    assert blank.line_numbers == (2, 4)


def test_shared_leading_forms_come_out_of_the_material(observation):
    """A prefix appears only because two representations share it."""
    prefixes = {f.prefix for f in observation.prefix_findings}
    assert "MARK " in prefixes
    for finding in observation.prefix_findings:
        holders = [
            f
            for f in observation.equality_findings
            if f.representation.startswith(finding.prefix)
        ]
        assert len(holders) >= 2


def test_no_prefix_is_reported_when_nothing_is_shared():
    observation = observe_external_material_relations(_projection("aaa\nbbb\nccc\n"))
    assert observation.prefix_findings == ()


def test_adjacency_is_positional_only(observation):
    """Reported pairs are consecutive lines, and only recurring pairs are kept."""
    for finding in observation.adjacency_findings:
        assert finding.occurrence_count > 1


# --------------------------------------------------------------------------
# What the observation refuses to be.
# --------------------------------------------------------------------------


def test_the_observation_writes_nothing(observation):
    assert observation.read_only is True
    assert observation.writes_event_ledger is False
    assert observation.mutates_cluster is False


def test_the_observation_disclaims_meaning_and_evidence(observation):
    notes = " ".join(observation.boundary_notes)
    assert "not tested against supplied candidates" in notes
    assert "not a marker, label, heading, or kind" in notes
    assert "not sequence, cause, or relation of meaning" in notes
    assert "does not identify headings, citations, definitions" in notes
    assert "not runtime Evidence, Fact, candidate verification" in notes


def test_recurrence_does_not_claim_the_representations_are_one_subject(observation):
    """`01.Kinds:28`: equal content does not make occurrences identical."""
    notes = " ".join(observation.boundary_notes)
    assert "not thereby the same subject, occurrence, or assertion" in notes


# --------------------------------------------------------------------------
# Determinism and integrity.
# --------------------------------------------------------------------------


def test_observation_is_deterministic(observation):
    again = observe_external_material_relations(_projection())
    assert external_material_relation_observation_json(
        again
    ) == external_material_relation_observation_json(observation)


def test_ordering_is_a_property_of_the_material(observation):
    counts = [f.occurrence_count for f in observation.equality_findings]
    assert counts == sorted(counts, reverse=True)


def test_observation_binds_to_the_projected_artifact(observation):
    projection = _projection()
    assert observation.artifact_hash == projection.artifact_hash
    assert observation.manifest_id == projection.manifest_id
    assert observation.projected_line_count == len(projection.lines)


def test_a_foreign_projection_convention_is_refused():
    projection = _projection()
    foreign = type(projection)(
        **{
            **{k: getattr(projection, k) for k in projection.__dataclass_fields__},
            "projection_convention": "something_else_v1",
        }
    )
    with pytest.raises(ExternalMaterialRelationObservationError):
        observe_external_material_relations(foreign)


def test_rendering_states_the_disclosures(observation):
    rendered = format_external_material_relation_observation(observation)
    assert "equivalence rule:" in rendered
    assert "counting scope:" in rendered
    assert "representation measured:" in rendered
