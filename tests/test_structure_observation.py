from seed_runtime.documentation_structure import BOUNDARY
from seed_runtime.knowledge.repository_observation import (
    REPOSITORY_ARTIFACT_OBSERVATION_ADAPTER_BOUNDARY,
    RepositoryArtifactObservationAdapter,
    extract_repository_artifact_facts,
)
from seed_runtime.structure_observation import (
    STRUCTURE_OBSERVATION_BOUNDARY,
    STRUCTURE_OBSERVATION_BOUNDARY_TEXT,
    STRUCTURE_OBSERVATION_OWNER,
)


def test_structure_observation_owner_is_substrate_independent_boundary():
    boundary = STRUCTURE_OBSERVATION_BOUNDARY

    assert STRUCTURE_OBSERVATION_OWNER == "Structure Observation"
    assert boundary.read_only is True
    assert boundary.structural_extraction is True
    assert boundary.preserves_evidence is True
    assert boundary.interprets_content is False
    assert boundary.owns_substrate_parsing is False
    assert boundary.owns_grammar is False
    assert boundary.owns_responsibility_recovery is False
    assert boundary.owns_lexicon is False
    assert boundary.writes_event_ledger is False
    assert boundary.mutates_repository is False
    assert boundary.mutates_cluster is False


def test_structure_observation_does_not_change_documentation_boundary_shape():
    assert BOUNDARY == {
        "read_only": True,
        "interprets_prose": False,
        "infers_claims": False,
        "infers_authority": False,
        "infers_shapes": False,
        "writes_event_ledger": False,
        "mutates_repository": False,
    }


def test_structure_observation_boundary_text_excludes_forbidden_ownership():
    assert "substrate adapter boundary" in STRUCTURE_OBSERVATION_BOUNDARY_TEXT
    assert "no substrate parsing" in STRUCTURE_OBSERVATION_BOUNDARY_TEXT
    assert "no grammar interpretation" in STRUCTURE_OBSERVATION_BOUNDARY_TEXT
    assert "no responsibility recovery" in STRUCTURE_OBSERVATION_BOUNDARY_TEXT
    assert "no lexicon stabilization" in STRUCTURE_OBSERVATION_BOUNDARY_TEXT


def test_repository_artifact_observation_is_structure_observation_adapter():
    boundary = REPOSITORY_ARTIFACT_OBSERVATION_ADAPTER_BOUNDARY

    assert boundary.parent_owner == STRUCTURE_OBSERVATION_OWNER
    assert boundary.adapter_owner == "Repository Artifact Observation Adapter"
    assert boundary.read_only is True
    assert boundary.structural_extraction is True
    assert boundary.preserves_evidence is True
    assert boundary.python_parsing is True
    assert boundary.module_observation is True
    assert boundary.class_observation is True
    assert boundary.function_observation is True
    assert boundary.method_observation is True
    assert boundary.repository_artifact_record_construction is True
    assert boundary.interprets_content is False
    assert boundary.owns_responsibility_recovery is False
    assert boundary.owns_lexicon is False
    assert boundary.writes_event_ledger is False
    assert boundary.mutates_repository is False
    assert boundary.mutates_cluster is False


def test_repository_artifact_public_extractor_delegates_without_shape_change():
    source = """import os

class ExampleComponent:
    def inspect(self):
        pass

async def observe():
    pass
"""

    facts = extract_repository_artifact_facts("fixtures/self_model_source.py", source)
    adapter_facts = RepositoryArtifactObservationAdapter().extract(
        "fixtures/self_model_source.py", source
    )

    assert facts == adapter_facts
    assert [(fact.artifact_kind, fact.symbol, fact.parent_symbol) for fact in facts] == [
        ("module", None, None),
        ("import", "os", None),
        ("class", "ExampleComponent", None),
        ("method", "inspect", "ExampleComponent"),
        ("function", "observe", None),
    ]
