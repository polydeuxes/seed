from seed_runtime.constitutional_view_composition import build_constitutional_view_composition
from seed_runtime.constitutional_view_selection import (
    ConstitutionalCapabilityProjection,
    ConstitutionalQuestionProjection,
    selected_constitutional_views_json,
    selected_constitutional_views_to_composition_request,
    select_constitutional_views,
)


def test_selection_consumes_projections_and_produces_one_immutable_artifact():
    selected = select_constitutional_views(
        question_projection=ConstitutionalQuestionProjection(
            bounded_question_id="bounded-question:compatibility",
            selection_keys=("process", "fidelity", "unowned"),
            uncertainty=("bounded question scope preserved as projected",),
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_process",
                capability_keys=("process", "stages"),
            ),
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_governance",
                capability_keys=("governance",),
            ),
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_fidelity",
                capability_keys=("fidelity",),
            ),
        ),
    )

    assert selected.bounded_question_id == "bounded-question:compatibility"
    assert selected.selected_view_names == (
        "constitutional_process",
        "constitutional_fidelity",
    )
    assert "bounded question scope preserved as projected" in selected.selection_uncertainty
    assert "unsupported selection key: unowned" in selected.selection_uncertainty
    assert selected.compatibility_answer == "No."
    assert "no raw question consumption" in selected.read_only_boundaries
    assert "no immutable constitutional view consumption" in selected.read_only_boundaries
    assert "no semantic reasoning" in selected.read_only_boundaries
    assert selected.read_only is True
    assert selected.writes_event_ledger is False
    assert selected.mutates_cluster is False


def test_selection_preserves_uncertainty_when_no_capability_supports_projection():
    selected = select_constitutional_views(
        question_projection=ConstitutionalQuestionProjection(
            bounded_question_id="bounded-question:unsupported",
            selection_keys=("missing",),
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_process",
                capability_keys=("process",),
            ),
        ),
    )

    assert selected.selected_view_names == ()
    assert "unsupported selection key: missing" in selected.selection_uncertainty
    assert (
        "no registered constitutional view matched deterministic projection keys"
        in selected.selection_uncertainty
    )
    assert selected.compatibility_answer == "Unknown."


def test_selected_views_wire_directly_into_existing_composition_contract():
    selected = select_constitutional_views(
        question_projection=ConstitutionalQuestionProjection(
            bounded_question_id="bounded-question:composition",
            selection_keys=("governance", "fidelity"),
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_governance",
                capability_keys=("governance",),
            ),
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_fidelity",
                capability_keys=("fidelity",),
            ),
        ),
    )

    request = selected_constitutional_views_to_composition_request(
        selected,
        composition_purpose="compatibility",
        output_format="json",
    )
    composition = build_constitutional_view_composition(request)

    assert request.requested_views == (
        "constitutional_governance",
        "constitutional_fidelity",
    )
    assert request.composition_purpose == "compatibility"
    assert request.bounded_question_id == "bounded-question:composition"
    assert request.selection_read_only_boundaries == selected.read_only_boundaries
    assert composition.compatibility_answer == "No."
    assert composition.preserved_selection_uncertainty == selected.selection_uncertainty
    assert composition.request is request


def test_selected_views_json_contains_only_selection_artifact_fields():
    selected = select_constitutional_views(
        question_projection=ConstitutionalQuestionProjection(
            bounded_question_id="bounded-question:json",
            selection_keys=("process",),
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_process",
                capability_keys=("process",),
            ),
        ),
    )

    payload = selected_constitutional_views_json(selected)

    assert payload["bounded_question_id"] == "bounded-question:json"
    assert payload["selected_view_names"] == ("constitutional_process",)
    assert payload["compatibility_answer"] == "No."
    assert "contributing_views" not in payload
    assert "bounded_summary" not in payload
    assert "authority_claims" not in payload


def test_selection_to_composition_handoff_preserves_uncertainty_without_strengthening():
    selected = select_constitutional_views(
        question_projection=ConstitutionalQuestionProjection(
            bounded_question_id="bounded-question:partial",
            selection_keys=("process", "missing"),
            uncertainty=("caller scope remains partial",),
        ),
        capability_projections=(
            ConstitutionalCapabilityProjection(
                registered_view_name="constitutional_process",
                capability_keys=("process",),
            ),
        ),
    )

    request = selected_constitutional_views_to_composition_request(selected)
    composition = build_constitutional_view_composition(request)

    assert request.bounded_question_id == selected.bounded_question_id
    assert request.selection_uncertainty == (
        "caller scope remains partial",
        "unsupported selection key: missing",
    )
    assert composition.preserved_selection_uncertainty == request.selection_uncertainty
    assert "caller scope remains partial" in composition.preserved_unknowns
    assert "unsupported selection key: missing" in composition.preserved_unknowns
    assert composition.compatibility_answer == "No."
    assert composition.read_only is True
    assert composition.writes_event_ledger is False
    assert composition.mutates_cluster is False
