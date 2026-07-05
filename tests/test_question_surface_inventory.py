import json

import pytest

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import (
    IMPLEMENTATION_SPECS,
    build_diagnostic_shape_audit,
)
from seed_runtime.question_surface_inventory import (
    BOUNDED_ASK_DISPATCH_SURFACES,
    _bounded_work_eligibility_for_prepared_question_family,
    _lookup_exact_question_family,
    _prepare_question_family_eligibility_input,
    apply_bounded_work_dispatch_result,
    apply_bounded_work_presentation_handoff,
    bounded_work_dispatch_request_for_selection,
    bounded_work_eligibility_for_question_family,
    bounded_work_presentation_handoff_for_eligibility,
    bounded_work_refusal_for_eligibility,
    bounded_work_selected_dispatch_surface_for_eligibility,
    bounded_work_selected_surface_value_for_eligibility,
    bounded_work_selection_for_question_family,
    bounded_work_surface_args_for_eligibility,
    bounded_ask_inventory_findings,
    execute_bounded_work_dispatch,
    build_question_surface_inventory,
    question_surface_inventory_json,
)


def test_cli_human_output_lists_known_question_families_and_flags(capsys):
    assert seed_local.main(["--question-surface-inventory"]) == 0
    output = capsys.readouterr().out

    assert "Known question families and answering Seed surfaces" in output
    for expected in (
        "operational pressure",
        "--ops-brief",
        "current operational explanation",
        "--operational-story",
        "derivation explanation",
        "--reasoning-path",
        "selection explanation",
        "--selection-path",
        "authority-constrained container ownership",
        "--container-ownership-authority",
    ):
        assert expected in output


def test_cli_json_output_includes_required_row_fields(capsys):
    assert seed_local.main(["--question-surface-inventory", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload
    required = {
        "question_family",
        "example_questions",
        "surface",
        "surface_flag",
        "answer_responsibility",
        "authority_boundary",
        "notes",
        "bounded_status",
        "dispatch_surface",
        "required_surface_args",
        "json_support",
        "human_formatter",
        "implementation_reason",
        "canonical_diagnostic_surface",
        "diagnostic_inventory_name",
        "diagnostic_shape_spec_name",
        "relationship_status",
    }
    assert required <= set(payload[0])
    assert isinstance(payload[0]["example_questions"], list)


def test_bounded_ask_question_families_alias_exposes_implementation_inventory(capsys):
    assert seed_local.main(["ask", "--question-families"]) == 0
    output = capsys.readouterr().out

    assert "bounded_status: eligible_now" in output
    assert "bounded_status: eligible_with_parameters" in output
    assert "bounded_status: diagnostic_only" in output
    assert "bounded_status: not_dispatchable" in output
    assert "dispatch_surface: service_ownership_authority" in output
    assert "required_surface_args: domain, subject" in output
    assert "Implementation findings: none" in output


def test_bounded_ask_inventory_json_answers_required_operator_questions(capsys):
    assert seed_local.main(["ask", "--question-families", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    by_family = {row["question_family"]: row for row in payload}
    assert (
        by_family["authority-constrained service ownership"]["bounded_status"]
        == "eligible_now"
    )
    assert (
        by_family["authority-constrained service ownership"]["required_surface_args"]
        == []
    )
    assert (
        by_family["authority-constrained service ownership"]["dispatch_surface"]
        == "service_ownership_authority"
    )
    assert (
        by_family["authority-constrained service ownership"][
            "canonical_diagnostic_surface"
        ]
        == "service_ownership_authority"
    )
    assert (
        by_family["authority-constrained service ownership"][
            "diagnostic_inventory_name"
        ]
        == "service_ownership_authority"
    )
    assert (
        by_family["authority-constrained service ownership"][
            "diagnostic_shape_spec_name"
        ]
        == "service_ownership_authority"
    )
    assert (
        by_family["authority-constrained service ownership"]["relationship_status"]
        == "connected"
    )
    assert (
        by_family["derivation explanation"]["bounded_status"]
        == "eligible_with_parameters"
    )
    assert by_family["derivation explanation"]["required_surface_args"] == [
        "domain",
        "subject",
    ]
    assert (
        by_family["source definition/import lookup"]["implementation_reason"]
        == "no bounded ask dispatch mapping in current implementation"
    )


def test_exact_question_family_lookup_is_separate_from_eligibility_and_dispatch():
    lookup = _lookup_exact_question_family("selection explanation")

    assert lookup.question_family == "selection explanation"
    assert tuple(lookup.__dataclass_fields__) == ("question_family",)
    assert "bounded_status" not in lookup.__dataclass_fields__
    assert "dispatch_surface" not in lookup.__dataclass_fields__
    assert "required_surface_args" not in lookup.__dataclass_fields__


def test_exact_question_family_lookup_rejects_unknown_text_before_eligibility():
    with pytest.raises(ValueError, match="unknown Question Family: made up"):
        _lookup_exact_question_family("made up")


def test_question_family_eligibility_input_preparation_is_separate_from_eligibility():
    prepared_input = _prepare_question_family_eligibility_input(
        "authority-constrained service ownership"
    )

    assert prepared_input.question_family == "authority-constrained service ownership"
    assert tuple(prepared_input.__dataclass_fields__) == ("question_family",)
    assert "dispatch_surface" not in prepared_input.__dataclass_fields__
    assert "surface_value" not in prepared_input.__dataclass_fields__
    assert "bounded_status" not in prepared_input.__dataclass_fields__
    assert "permitted" not in prepared_input.__dataclass_fields__

    eligibility = _bounded_work_eligibility_for_prepared_question_family(
        prepared_input
    )

    assert eligibility.question_family == prepared_input.question_family
    assert eligibility.bounded_status == "eligible_now"
    assert eligibility.permitted is True


def test_question_family_eligibility_input_preparation_rejects_unknown_text():
    with pytest.raises(ValueError, match="unknown Question Family: made up"):
        _prepare_question_family_eligibility_input("made up")


def test_bounded_work_eligibility_result_is_separate_from_surface_selection():
    with pytest.raises(ValueError, match="unknown Question Family: made up"):
        bounded_work_eligibility_for_question_family("made up")

    eligible_now = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )
    assert eligible_now.question_family == "authority-constrained service ownership"
    assert eligible_now.bounded_status == "eligible_now"
    assert eligible_now.permitted is True
    assert eligible_now.required_surface_args == ()
    assert "dispatch_surface" not in eligible_now.__dataclass_fields__

    eligible_with_parameters = bounded_work_eligibility_for_question_family(
        "derivation explanation"
    )
    assert eligible_with_parameters.bounded_status == "eligible_with_parameters"
    assert eligible_with_parameters.permitted is True
    assert eligible_with_parameters.required_surface_args == ("domain", "subject")

    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    assert diagnostic_only.bounded_status == "diagnostic_only"
    assert diagnostic_only.permitted is False

    not_dispatchable = bounded_work_eligibility_for_question_family(
        "source definition/import lookup"
    )
    assert not_dispatchable.bounded_status == "not_dispatchable"
    assert not_dispatchable.permitted is False



def test_bounded_work_surface_args_result_is_separate_from_selection():
    eligibility = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )
    no_args = bounded_work_surface_args_for_eligibility(
        "authority-constrained service ownership", eligibility
    )

    assert no_args.question_family == "authority-constrained service ownership"
    assert no_args.surface_args == ()
    assert no_args.required_surface_args == ()
    assert "dispatch_surface" not in no_args.__dataclass_fields__
    assert "surface_value" not in no_args.__dataclass_fields__
    assert "permitted" not in no_args.__dataclass_fields__

    with pytest.raises(ValueError, match="does not accept --surface-args"):
        bounded_work_surface_args_for_eligibility(
            "authority-constrained service ownership", eligibility, ("extra",)
        )

    parameterized_eligibility = bounded_work_eligibility_for_question_family(
        "selection explanation"
    )
    with pytest.raises(ValueError, match="requires --surface-args"):
        bounded_work_surface_args_for_eligibility(
            "selection explanation", parameterized_eligibility
        )
    with pytest.raises(ValueError, match="requires exactly 1 --surface-args value"):
        bounded_work_surface_args_for_eligibility(
            "selection explanation", parameterized_eligibility, ("one", "two")
        )

    provided_args = bounded_work_surface_args_for_eligibility(
        "selection explanation", parameterized_eligibility, ("target:one",)
    )

    assert provided_args.surface_args == ("target:one",)
    assert provided_args.required_surface_args == ("target",)

def test_bounded_work_refusal_result_is_separate_from_eligibility_and_selection():
    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    refusal = bounded_work_refusal_for_eligibility(diagnostic_only)

    assert refusal.question_family == "surface inventory"
    assert refusal.bounded_status == "diagnostic_only"
    assert refusal.message == (
        "Question Family 'surface inventory' is diagnostic_only and is not an "
        "inquiry-answer surface for bounded ask"
    )
    assert "permitted" not in refusal.__dataclass_fields__
    assert "dispatch_surface" not in refusal.__dataclass_fields__

    not_dispatchable = bounded_work_eligibility_for_question_family(
        "source definition/import lookup"
    )
    not_dispatchable_refusal = bounded_work_refusal_for_eligibility(not_dispatchable)

    assert not_dispatchable_refusal.bounded_status == "not_dispatchable"
    assert not_dispatchable_refusal.message == (
        "Question Family 'source definition/import lookup' is not_dispatchable by current "
        "implementation-backed eligibility"
    )

    permitted = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )
    with pytest.raises(ValueError, match="requires non-permitted eligibility"):
        bounded_work_refusal_for_eligibility(permitted)


def test_bounded_work_selected_surface_value_is_separate_from_selection():
    eligibility = bounded_work_eligibility_for_question_family(
        "observation domain coverage"
    )
    selected_value = bounded_work_selected_surface_value_for_eligibility(
        "observation domain coverage", eligibility
    )

    assert selected_value.question_family == "observation domain coverage"
    assert selected_value.surface_value == "__all__"
    assert selected_value.required_surface_args == ()
    assert "dispatch_surface" not in selected_value.__dataclass_fields__
    assert "bounded_status" not in selected_value.__dataclass_fields__
    assert "permitted" not in selected_value.__dataclass_fields__

    parameterized_eligibility = bounded_work_eligibility_for_question_family(
        "selection explanation"
    )
    parameterized_surface_args = bounded_work_surface_args_for_eligibility(
        "selection explanation", parameterized_eligibility, ("target:one",)
    )
    parameterized_value = bounded_work_selected_surface_value_for_eligibility(
        "selection explanation",
        parameterized_eligibility,
        parameterized_surface_args,
    )

    assert parameterized_value.surface_value == "target:one"
    assert parameterized_value.required_surface_args == ("target",)

    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    with pytest.raises(ValueError, match="requires permitted eligibility"):
        bounded_work_selected_surface_value_for_eligibility(
            "surface inventory", diagnostic_only
        )


def test_bounded_work_selected_dispatch_surface_is_separate_from_value_and_selection():
    eligibility = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )

    selected_dispatch_surface = bounded_work_selected_dispatch_surface_for_eligibility(
        "authority-constrained service ownership", eligibility
    )

    assert selected_dispatch_surface.question_family == (
        "authority-constrained service ownership"
    )
    assert selected_dispatch_surface.dispatch_surface == "service_ownership_authority"
    assert "surface_value" not in selected_dispatch_surface.__dataclass_fields__
    assert "required_surface_args" not in selected_dispatch_surface.__dataclass_fields__
    assert "bounded_status" not in selected_dispatch_surface.__dataclass_fields__
    assert "permitted" not in selected_dispatch_surface.__dataclass_fields__

    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    with pytest.raises(ValueError, match="requires permitted eligibility"):
        bounded_work_selected_dispatch_surface_for_eligibility(
            "surface inventory", diagnostic_only
        )

def test_bounded_work_selection_result_is_separate_from_eligibility_and_dispatch():
    eligibility = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )
    selection = bounded_work_selection_for_question_family(
        "authority-constrained service ownership", eligibility
    )

    assert selection.question_family == "authority-constrained service ownership"
    assert selection.dispatch_surface == "service_ownership_authority"
    assert selection.surface_value is True
    assert selection.required_surface_args == ()
    assert "permitted" not in selection.__dataclass_fields__
    assert "bounded_status" not in selection.__dataclass_fields__

    parameterized_eligibility = bounded_work_eligibility_for_question_family(
        "derivation explanation"
    )
    parameterized_surface_args = bounded_work_surface_args_for_eligibility(
        "derivation explanation",
        parameterized_eligibility,
        ("runtime", "service:web"),
    )
    parameterized_selection = bounded_work_selection_for_question_family(
        "derivation explanation",
        parameterized_eligibility,
        parameterized_surface_args,
    )

    assert parameterized_selection.dispatch_surface == "reasoning_path"
    assert parameterized_selection.surface_value == ("runtime", "service:web")
    assert parameterized_selection.required_surface_args == ("domain", "subject")

    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    with pytest.raises(ValueError, match="requires permitted eligibility"):
        bounded_work_selection_for_question_family("surface inventory", diagnostic_only)


def test_bounded_work_presentation_handoff_is_separate_from_dispatch_request():
    eligibility = bounded_work_eligibility_for_question_family(
        "selection explanation"
    )

    presentation_handoff = bounded_work_presentation_handoff_for_eligibility(
        "selection explanation", eligibility
    )

    assert presentation_handoff.question_family == "selection explanation"
    assert presentation_handoff.question_family_explanation == "selection explanation"
    assert "dispatch_surface" not in presentation_handoff.__dataclass_fields__
    assert "surface_value" not in presentation_handoff.__dataclass_fields__
    assert "required_surface_args" not in presentation_handoff.__dataclass_fields__

    diagnostic_only = bounded_work_eligibility_for_question_family("surface inventory")
    with pytest.raises(ValueError, match="requires permitted eligibility"):
        bounded_work_presentation_handoff_for_eligibility(
            "surface inventory", diagnostic_only
        )


def test_apply_bounded_work_presentation_handoff_consumes_handoff_only():
    parser = seed_local.build_parser()
    args = parser.parse_args([
        "ask",
        "--question-family",
        "selection explanation",
        "--surface-args",
        "target:one",
        "--presentation",
    ])
    eligibility = bounded_work_eligibility_for_question_family(
        "selection explanation"
    )
    presentation_handoff = bounded_work_presentation_handoff_for_eligibility(
        "selection explanation", eligibility
    )

    result = apply_bounded_work_presentation_handoff(args, presentation_handoff)

    assert args.question_family_explanation == "selection explanation"
    assert args.selection_path is None
    assert result.question_family == "selection explanation"
    assert result.question_family_explanation == "selection explanation"
    assert "dispatch_surface" not in result.__dataclass_fields__
    assert "surface_value" not in result.__dataclass_fields__
    assert "required_surface_args" not in result.__dataclass_fields__


def test_bounded_work_dispatch_request_is_separate_from_selection():
    eligibility = bounded_work_eligibility_for_question_family(
        "authority-constrained service ownership"
    )
    selection = bounded_work_selection_for_question_family(
        "authority-constrained service ownership", eligibility
    )

    dispatch_request = bounded_work_dispatch_request_for_selection(selection)

    assert dispatch_request.question_family == "authority-constrained service ownership"
    assert dispatch_request.dispatch_surface == "service_ownership_authority"
    assert dispatch_request.surface_value is True
    assert "required_surface_args" not in dispatch_request.__dataclass_fields__
    assert "bounded_status" not in dispatch_request.__dataclass_fields__
    assert "permitted" not in dispatch_request.__dataclass_fields__


def test_execute_bounded_work_dispatch_consumes_request_and_mutates_namespace():
    parser = seed_local.build_parser()
    args = parser.parse_args([
        "ask",
        "--question-family",
        "observation permission state",
    ])
    eligibility = bounded_work_eligibility_for_question_family(
        "observation permission state"
    )
    selection = bounded_work_selection_for_question_family(
        "observation permission state", eligibility
    )
    dispatch_request = bounded_work_dispatch_request_for_selection(selection)

    result = execute_bounded_work_dispatch(args, dispatch_request)

    assert args.observation_permission == "__all__"
    assert result.question_family == "observation permission state"
    assert result.dispatch_surface == "observation_permission"
    assert result.surface_value == "__all__"


def test_apply_bounded_work_dispatch_result_consumes_dispatch_result_only():
    parser = seed_local.build_parser()
    args = parser.parse_args([
        "ask",
        "--question-family",
        "knowledge reachability",
        "--json",
    ])
    eligibility = bounded_work_eligibility_for_question_family("knowledge reachability")
    selection = bounded_work_selection_for_question_family(
        "knowledge reachability", eligibility
    )
    dispatch_request = bounded_work_dispatch_request_for_selection(selection)
    dispatch_result = execute_bounded_work_dispatch(args, dispatch_request)

    result = apply_bounded_work_dispatch_result(args, dispatch_result)

    assert result is dispatch_result
    assert args.knowledge_reachability_audit_json is True
    assert args.json_output is False
    assert "required_surface_args" not in dispatch_result.__dataclass_fields__
    assert "bounded_status" not in dispatch_result.__dataclass_fields__
    assert "permitted" not in dispatch_result.__dataclass_fields__


def test_apply_bounded_work_dispatch_result_preserves_non_compatibility_json():
    parser = seed_local.build_parser()
    args = parser.parse_args([
        "ask",
        "--question-family",
        "observation domain coverage",
        "--json",
    ])
    eligibility = bounded_work_eligibility_for_question_family(
        "observation domain coverage"
    )
    selection = bounded_work_selection_for_question_family(
        "observation domain coverage", eligibility
    )
    dispatch_request = bounded_work_dispatch_request_for_selection(selection)
    dispatch_result = execute_bounded_work_dispatch(args, dispatch_request)

    apply_bounded_work_dispatch_result(args, dispatch_result)

    assert args.observation_domains == "__all__"
    assert args.json_output is True


def test_bounded_ask_dispatch_consumes_bounded_work_dispatch_request():
    parser = seed_local.build_parser()
    args = parser.parse_args([
        "ask",
        "--question-family",
        "observation domain coverage",
    ])

    seed_local.apply_bounded_ask_dispatch(args, parser)

    assert args.observation_domains == "__all__"
    assert args.message == []

    parameterized_args = parser.parse_args([
        "ask",
        "--question-family",
        "selection explanation",
        "--surface-args",
        "target:one",
    ])

    seed_local.apply_bounded_ask_dispatch(parameterized_args, parser)

    assert parameterized_args.selection_path == "target:one"
    assert parameterized_args.message == []

    presentation_args = parser.parse_args([
        "ask",
        "--question-family",
        "selection explanation",
        "--surface-args",
        "target:one",
        "--presentation",
    ])

    seed_local.apply_bounded_ask_dispatch(presentation_args, parser)

    assert presentation_args.question_family_explanation == "selection explanation"
    assert presentation_args.selection_path is None
    assert presentation_args.message == []


def test_bounded_ask_inventory_validates_question_families_and_dispatch_maps():
    rows = build_question_surface_inventory()
    families = [row.question_family for row in rows]

    assert len(families) == len(set(families))
    assert bounded_ask_inventory_findings(rows) == ()
    assert set(BOUNDED_ASK_DISPATCH_SURFACES) <= set(families)
    assert (
        sum(1 for row in rows if row.dispatch_surface == "service_ownership_authority")
        == 1
    )


def test_question_surface_inventory_registration_is_read_only_and_static():
    entry = next(
        item
        for item in DIAGNOSTIC_INVENTORY
        if item.name == "question_surface_inventory"
    )

    assert entry.cli_flags == (
        "--question-surface-inventory",
        "ask --question-families",
        "--question-family-definition",
        "--question-family-explanation",
    )
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.emits_diagnostic_facts is False
    assert entry.writes_event_ledger is False
    assert entry.reads_diagnostic_facts is False
    assert entry.uses_repo_files is False
    assert entry.uses_projected_state is False
    assert entry.mutates_cluster is False


def test_question_surface_rows_connect_to_diagnostic_inventory_and_shape_specs():
    diagnostic_names = {entry.name for entry in DIAGNOSTIC_INVENTORY}
    spec_names = set(IMPLEMENTATION_SPECS)
    rows = build_question_surface_inventory()
    dispatchable_rows = [
        row
        for row in rows
        if row.bounded_status
        in {"eligible_now", "eligible_with_parameters", "diagnostic_only"}
    ]

    assert dispatchable_rows
    for row in dispatchable_rows:
        assert row.relationship_status == "connected"
        assert row.diagnostic_inventory_name in diagnostic_names
        assert row.diagnostic_shape_spec_name in spec_names
        assert row.diagnostic_inventory_name == row.diagnostic_shape_spec_name


def test_canonical_surface_aliases_are_exposed_without_inference():
    rows = {row.question_family: row for row in build_question_surface_inventory()}
    row = rows["knowledge reachability"]

    assert row.dispatch_surface == "knowledge_reachability_audit"
    assert row.canonical_diagnostic_surface == "knowledge_reachability"
    assert row.diagnostic_inventory_name == "knowledge_reachability"
    assert row.diagnostic_shape_spec_name == "knowledge_reachability"
    assert (
        "canonical diagnostic surface alias: "
        "knowledge_reachability_audit -> knowledge_reachability"
        in row.implementation_reason
    )


def test_representative_relationship_surfaces_validate_successfully():
    rows = {row.question_family: row for row in build_question_surface_inventory()}

    for question_family, expected_surface in (
        ("authority-constrained service ownership", "service_ownership_authority"),
        ("operational pressure", "ops_brief"),
        ("knowledge reachability", "knowledge_reachability"),
    ):
        row = rows[question_family]
        assert row.relationship_status == "connected"
        assert row.canonical_diagnostic_surface == expected_surface
        assert row.diagnostic_inventory_name == expected_surface
        assert row.diagnostic_shape_spec_name == expected_surface


def test_relationship_visibility_does_not_traverse_answer_payloads():
    payload = json.dumps(
        [
            row.to_json_dict()
            for row in build_question_surface_inventory()
            if row.relationship_status == "connected"
        ],
        sort_keys=True,
    )

    assert "answer_payload" not in payload
    assert "evidence_chain" not in payload
    assert "provenance" not in payload
    assert "intermediate_conclusions" not in payload


def test_question_surface_inventory_shape_audit_is_consistent():
    rows = [
        row
        for row in build_diagnostic_shape_audit()
        if row.diagnostic == "question_surface_inventory"
    ]

    assert rows
    assert {row.status for row in rows} == {"consistent"}


def test_question_surface_inventory_is_not_a_router_or_recommender():
    rows = build_question_surface_inventory()
    rendered = "\n".join(
        [
            row.question_family
            + row.answer_responsibility
            + row.authority_boundary
            + row.notes
            for row in rows
        ]
    ).lower()

    assert "recommend" not in rendered
    assert "best command" not in rendered
    assert "infer intent" not in rendered
    assert all(row.example_questions for row in rows)


def test_question_surface_inventory_rejects_free_text_question_argument(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(["--question-surface-inventory", "what should I run?"])

    assert exc.value.code == 2


def test_bounded_ask_service_ownership_matches_direct_human(capsys):
    assert seed_local.main(["--service-ownership-authority"]) == 0
    direct = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "authority-constrained service ownership",
            ]
        )
        == 0
    )
    bounded = capsys.readouterr().out

    assert bounded == direct


def test_bounded_ask_listener_endpoint_matches_direct_json(capsys):
    assert seed_local.main(["--listener-endpoint-authority", "--json"]) == 0
    direct = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "listener endpoint reachability",
                "--json",
            ]
        )
        == 0
    )
    bounded = json.loads(capsys.readouterr().out)

    assert bounded == direct


def test_bounded_ask_observation_domains_matches_direct_human_and_json(capsys):
    assert seed_local.main(["--observation-domains"]) == 0
    direct_human = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "observation domain coverage",
            ]
        )
        == 0
    )
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--observation-domains", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "observation domain coverage",
                "--json",
            ]
        )
        == 0
    )
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_observation_permission_matches_direct_human_and_json(capsys):
    assert seed_local.main(["--observation-permission"]) == 0
    direct_human = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "observation permission state",
            ]
        )
        == 0
    )
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--observation-permission", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "observation permission state",
                "--json",
            ]
        )
        == 0
    )
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_projection_shape_json_preserves_raw_answer(capsys):
    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "projection shape visibility",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert "composed_question_family_explanation" not in payload
    assert "stages" in payload
    assert payload["boundary"] == {
        "mutates_cluster": False,
        "read_only": True,
        "writes_event_ledger": False,
    }


def test_bounded_ask_question_family_presentation_json_uses_composed_explanation(capsys):
    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "projection shape visibility",
                "--presentation",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert payload["question_family"] == "projection shape visibility"
    assert "composed_question_family_explanation" in payload
    assert "stages" not in payload
    explanation = payload["composed_question_family_explanation"]
    assert explanation["question_family"] == "projection shape visibility"
    sections = {section["field"]: section for section in explanation["sections"]}
    assert set(sections) >= {
        "question_family_definition",
        "question_family_answer_responsibility",
        "question_family_boundary",
        "question_family_diagnostic_relationship",
    }
    assert (
        sections["question_family_definition"]["value"]["dispatch_surface"]
        == "projection_shape"
    )


def test_bounded_ask_presentation_unknown_family_remains_bounded(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(
            [
                "ask",
                "--question-family",
                "not a family",
                "--presentation",
                "--json",
            ]
        )

    assert exc.value.code == 2
    assert "unknown Question Family: not a family" in capsys.readouterr().err


def test_bounded_ask_presentation_rejects_free_text_routing(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(
            [
                "ask",
                "what answers this?",
                "--question-family",
                "projection shape visibility",
                "--presentation",
            ]
        )

    assert exc.value.code == 2
    assert "--question-family can only be used" in capsys.readouterr().err


def test_bounded_ask_presentation_parameterized_family_still_requires_surface_args(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(
            [
                "ask",
                "--question-family",
                "derivation explanation",
                "--presentation",
                "--json",
            ]
        )

    assert exc.value.code == 2
    assert "requires --surface-args" in capsys.readouterr().err


def test_bounded_ask_presentation_does_not_select_other_subject_compositions(capsys):
    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "projection shape visibility",
                "--presentation",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    assert "composed_question_family_explanation" in payload
    assert "composed_diagnostic_surface_explanation" not in payload
    assert "composed_projection_stage_explanation" not in payload
    assert (
        payload["composed_question_family_explanation"]["question_family"]
        == "projection shape visibility"
    )


def test_bounded_ask_knowledge_reachability_matches_direct_json(capsys):
    assert (
        seed_local.main(
            [
                "--knowledge-reachability-audit",
                "--knowledge-reachability-audit-json",
            ]
        )
        == 0
    )
    direct = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "knowledge reachability",
                "--json",
            ]
        )
        == 0
    )
    bounded = json.loads(capsys.readouterr().out)

    for payload in (direct, bounded):
        payload["metadata"].pop("indexes", None)
        payload["metadata"].pop("timing", None)
        payload["metadata"].pop("timings", None)
    assert bounded == direct


def test_bounded_ask_rejects_parameter_required_family_without_surface_args(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(["ask", "--question-family", "derivation explanation"])

    assert exc.value.code == 2
    assert "requires --surface-args" in capsys.readouterr().err


def test_bounded_ask_derivation_explanation_forwards_surface_args_human_and_json(
    capsys,
):
    assert seed_local.main(["--reasoning-path", "runtime", "web_service"]) == 0
    direct_human = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "derivation explanation",
                "--surface-args",
                "runtime",
                "web_service",
            ]
        )
        == 0
    )
    bounded_human = capsys.readouterr().out

    assert (
        seed_local.main(["--reasoning-path", "runtime", "web_service", "--json"]) == 0
    )
    direct_json = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "derivation explanation",
                "--surface-args",
                "runtime",
                "web_service",
                "--json",
            ]
        )
        == 0
    )
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_selection_explanation_forwards_surface_args_human_and_json(capsys):
    assert seed_local.main(["--selection-path", "container_ownership"]) == 0
    direct_human = capsys.readouterr().out

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "selection explanation",
                "--surface-args",
                "container_ownership",
            ]
        )
        == 0
    )
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--selection-path", "container_ownership", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert (
        seed_local.main(
            [
                "ask",
                "--question-family",
                "selection explanation",
                "--surface-args",
                "container_ownership",
                "--json",
            ]
        )
        == 0
    )
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_parameterized_family_requires_exact_surface_arg_count(capsys):
    with pytest.raises(SystemExit) as too_few:
        seed_local.main(
            [
                "ask",
                "--question-family",
                "derivation explanation",
                "--surface-args",
                "runtime",
            ]
        )
    assert too_few.value.code == 2
    assert "requires exactly 2 --surface-args" in capsys.readouterr().err

    with pytest.raises(SystemExit) as too_many:
        seed_local.main(
            [
                "ask",
                "--question-family",
                "selection explanation",
                "--surface-args",
                "container_ownership",
                "extra",
            ]
        )
    assert too_many.value.code == 2
    assert "requires exactly 1 --surface-args" in capsys.readouterr().err


def test_bounded_ask_rejects_surface_args_outside_parameterized_family(capsys):
    with pytest.raises(SystemExit) as without_question_family:
        seed_local.main(["ask", "--surface-args", "runtime"])
    assert without_question_family.value.code == 2
    assert "--surface-args can only be used" in capsys.readouterr().err

    with pytest.raises(SystemExit) as zero_arg_family:
        seed_local.main(
            [
                "ask",
                "--question-family",
                "authority-constrained service ownership",
                "--surface-args",
                "runtime",
            ]
        )
    assert zero_arg_family.value.code == 2
    assert "does not accept --surface-args" in capsys.readouterr().err


def test_bounded_ask_rejects_diagnostic_only_family(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(["ask", "--question-family", "surface inventory"])

    assert exc.value.code == 2
    assert "diagnostic_only" in capsys.readouterr().err


def test_bounded_ask_rejects_not_dispatchable_family(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(["ask", "--question-family", "source definition/import lookup"])

    assert exc.value.code == 2
    assert "not_dispatchable" in capsys.readouterr().err


def test_question_family_definition_json_includes_identity_explanation(capsys):
    assert (
        seed_local.main(
            [
                "--question-family-definition",
                "authority-constrained service ownership",
                "--json",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)

    definition = payload["question_family_definition"]
    assert payload["question_family"] == "authority-constrained service ownership"
    assert definition == {
        "answer_responsibility": "evaluates service ownership reachability under constrained authority and implementation inventory evidence",
        "bounded": True,
        "bounded_status": "eligible_now",
        "dispatch_surface": "service_ownership_authority",
        "display_name": "authority-constrained service ownership",
        "evidence_source": "question_surface_inventory",
        "implementation_reason": "present in bounded ask dispatch map",
        "question_family_answer_responsibility": {
            "answer_responsibility": "evaluates service ownership reachability under constrained authority and implementation inventory evidence",
            "dispatch_surface": "service_ownership_authority",
            "evidence_source": "question_surface_inventory",
            "implementation_reason": "present in bounded ask dispatch map",
            "relationship_status": "connected",
            "responsible_answering_surface": "service_ownership_authority",
            "status": "known",
            "surface_flag": "--service-ownership-authority",
        },
        "question_family_boundary": "read-only evaluator; no provider acquisition; no execution; no event-ledger writes; no mutation",
        "question_family_diagnostic_relationship": {
            "canonical_diagnostic_surface": "service_ownership_authority",
            "diagnostic_inventory_name": "service_ownership_authority",
            "diagnostic_shape_spec_name": "service_ownership_authority",
            "dispatch_surface": "service_ownership_authority",
            "evidence_source": "question_surface_inventory",
            "implementation_reason": "present in bounded ask dispatch map",
            "relationship_status": "connected",
            "status": "known",
        },
        "question_family": "authority-constrained service ownership",
        "relationship_status": "connected",
        "status": "known",
        "surface": "service_ownership_authority",
        "surface_flag": "--service-ownership-authority",
    }


def test_question_family_definition_human_renders_identity_explanation(capsys):
    assert (
        seed_local.main(
            ["--question-family-definition", "source definition/import lookup"]
        )
        == 0
    )
    output = capsys.readouterr().out

    assert "QuestionFamily definition: source definition/import lookup" in output
    assert "bounded_status: not_dispatchable" in output
    assert "dispatch_surface: none" in output
    assert (
        "answer_responsibility: looks up preserved imports and definitions from projected facts"
        in output
    )
    assert (
        "question_family_boundary: read-only projected-fact view; does not inspect repository files, parse source, or append events"
        in output
    )
    assert "question_family_answer_responsibility:" in output
    assert (
        "responsible_answering_surface: source_navigation"
        in output
    )
    assert (
        "implementation_reason: no bounded ask dispatch mapping in current implementation"
        in output
    )
    assert "question_family_diagnostic_relationship:" in output
    assert "canonical_diagnostic_surface: source_navigation" in output
    assert "diagnostic_inventory_name: none" in output
    assert "diagnostic_shape_spec_name: none" in output
    assert "relationship_status: missing_diagnostic_inventory" in output


def test_question_family_definition_unknown_is_bounded_and_does_not_infer(capsys):
    assert seed_local.main(["--question-family-definition", "made up", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["question_family"] == "made up"
    assert payload["question_family_definition"] == {
        "answer_responsibility": "unknown",
        "bounded": "unknown",
        "bounded_status": "unknown",
        "dispatch_surface": "unknown",
        "display_name": "made up",
        "evidence_source": "question_surface_inventory",
        "implementation_reason": "unknown question family; no question-surface inventory row exists",
        "question_family_answer_responsibility": {
            "answer_responsibility": "unknown",
            "dispatch_surface": "unknown",
            "evidence_source": "question_surface_inventory",
            "implementation_reason": "unknown question family; no question-surface inventory row exists",
            "relationship_status": "unknown",
            "responsible_answering_surface": "unknown",
            "status": "unknown",
        },
        "question_family_boundary": "unknown question family; no implementation-backed authority boundary exists",
        "question_family_diagnostic_relationship": {
            "canonical_diagnostic_surface": "unknown",
            "diagnostic_inventory_name": "unknown",
            "diagnostic_shape_spec_name": "unknown",
            "dispatch_surface": "unknown",
            "evidence_source": "question_surface_inventory",
            "implementation_reason": "unknown question family; no question-surface inventory row exists",
            "relationship_status": "unknown",
            "status": "unknown",
        },
        "question_family": "made up",
        "status": "unknown",
    }


def test_question_family_definition_does_not_change_inventory_output(capsys):
    assert seed_local.main(["--question-surface-inventory", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload == question_surface_inventory_json(
        build_question_surface_inventory()
    )
    assert "question_family_definition" not in payload[0]


def test_question_family_definition_guardrails_exclude_behavior_and_inference(capsys):
    assert (
        seed_local.main(
            ["--question-family-definition", "operational pressure", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    serialized = json.dumps(payload, sort_keys=True).lower()
    answer_responsibility = payload["question_family_definition"][
        "question_family_answer_responsibility"
    ]
    diagnostic_relationship = payload["question_family_definition"][
        "question_family_diagnostic_relationship"
    ]
    boundary = payload["question_family_definition"]["question_family_boundary"].lower()

    assert answer_responsibility == {
        "answer_responsibility": "compact operational pressure and visibility summary",
        "dispatch_surface": "ops_brief",
        "evidence_source": "question_surface_inventory",
        "implementation_reason": "present in bounded ask dispatch map",
        "relationship_status": "connected",
        "responsible_answering_surface": "ops_brief",
        "status": "known",
        "surface_flag": "--ops-brief",
    }
    assert boundary == (
        "read-only summary assembled from existing audits; no recording; no mutation"
    )
    assert diagnostic_relationship == {
        "canonical_diagnostic_surface": "ops_brief",
        "diagnostic_inventory_name": "ops_brief",
        "diagnostic_shape_spec_name": "ops_brief",
        "dispatch_surface": "ops_brief",
        "evidence_source": "question_surface_inventory",
        "implementation_reason": "present in bounded ask dispatch map",
        "relationship_status": "connected",
        "status": "known",
    }
    for forbidden in (
        "runtime execution",
        "planner behavior",
        "routing behavior",
        "semantic interpretation",
        "implementation inference",
        "relationship inference",
        "relationship engine",
        "semantic matching",
        "new authority",
        "future routing",
        "llm reasoning",
        "execute",
    ):
        assert forbidden not in serialized


def test_composed_question_family_explanation_json_uses_existing_fields_only(capsys):
    assert (
        seed_local.main(
            ["--question-family-explanation", "operational pressure", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    definition = seed_local.question_family_definition_json(
        "operational pressure", build_question_surface_inventory()
    )["question_family_definition"]
    composed = payload["composed_question_family_explanation"]

    assert payload["question_family"] == "operational pressure"
    assert composed["composition_source"] == "question_family_definition"
    assert [section["field"] for section in composed["sections"]] == [
        "question_family_definition",
        "question_family_answer_responsibility",
        "question_family_boundary",
        "question_family_diagnostic_relationship",
    ]
    assert composed["sections"][0]["value"] == {
        "question_family": definition["question_family"],
        "display_name": definition["display_name"],
        "status": definition["status"],
        "bounded_status": definition["bounded_status"],
        "dispatch_surface": definition["dispatch_surface"],
    }
    assert composed["sections"][1]["value"] == definition[
        "question_family_answer_responsibility"
    ]
    assert composed["sections"][2]["value"] == definition[
        "question_family_boundary"
    ]
    assert composed["sections"][3]["value"] == definition[
        "question_family_diagnostic_relationship"
    ]


def test_composed_question_family_explanation_human_orders_existing_fields(capsys):
    assert seed_local.main(["--question-family-explanation", "source definition/import lookup"]) == 0
    output = capsys.readouterr().out

    assert "QuestionFamily explanation: source definition/import lookup" in output
    assert "Definition:" in output
    assert "Answer responsibility:" in output
    assert "Boundary:" in output
    assert "Diagnostic relationship:" in output
    assert "bounded_status: not_dispatchable" in output
    assert "dispatch_surface: none" in output
    assert "answer_responsibility: looks up preserved imports and definitions from projected facts" in output
    assert "read-only projected-fact view; does not inspect repository files, parse source, or append events" in output
    assert "relationship_status: missing_diagnostic_inventory" in output


def test_composed_question_family_explanation_unknown_remains_bounded(capsys):
    assert seed_local.main(["--question-family-explanation", "made up", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    definition = seed_local.question_family_definition_json(
        "made up", build_question_surface_inventory()
    )["question_family_definition"]
    composed = payload["composed_question_family_explanation"]

    assert composed["status"] == "unknown"
    assert composed["sections"][0]["value"]["bounded_status"] == "unknown"
    assert composed["sections"][1]["value"] == definition[
        "question_family_answer_responsibility"
    ]
    assert composed["sections"][2]["value"] == definition[
        "question_family_boundary"
    ]
    assert composed["sections"][3]["value"] == definition[
        "question_family_diagnostic_relationship"
    ]


def test_composed_question_family_explanation_does_not_change_existing_surfaces(capsys):
    assert seed_local.main(["--question-family-definition", "operational pressure", "--json"]) == 0
    before_definition = json.loads(capsys.readouterr().out)
    assert seed_local.main(["--question-surface-inventory", "--json"]) == 0
    before_inventory = json.loads(capsys.readouterr().out)

    assert seed_local.main(["--question-family-explanation", "operational pressure", "--json"]) == 0
    capsys.readouterr()

    assert seed_local.main(["--question-family-definition", "operational pressure", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == before_definition
    assert seed_local.main(["--question-surface-inventory", "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == before_inventory


def test_composed_question_family_explanation_guardrails_do_not_introduce_semantics(capsys):
    assert seed_local.main(["--question-family-explanation", "operational pressure", "--json"]) == 0
    serialized = json.dumps(json.loads(capsys.readouterr().out), sort_keys=True).lower()

    for forbidden in (
        "presentation inference",
        "presentation reasoning",
        "presentation interpretation",
        "presentation normalization",
        "presentation recommendation",
        "semantic meaning",
        "semantic",
        "implementation not already present",
        "discover",
        "rank",
        "relationship engine",
        "explainablesubject",
        "ontology",
    ):
        assert forbidden not in serialized
