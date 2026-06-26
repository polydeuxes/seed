import json

import pytest

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.diagnostic_shape_audit import build_diagnostic_shape_audit
from seed_runtime.question_surface_inventory import build_question_surface_inventory


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
    }
    assert required <= set(payload[0])
    assert isinstance(payload[0]["example_questions"], list)


def test_question_surface_inventory_registration_is_read_only_and_static():
    entry = next(
        item for item in DIAGNOSTIC_INVENTORY if item.name == "question_surface_inventory"
    )

    assert entry.cli_flags == ("--question-surface-inventory",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.emits_diagnostic_facts is False
    assert entry.writes_event_ledger is False
    assert entry.reads_diagnostic_facts is False
    assert entry.uses_repo_files is False
    assert entry.uses_projected_state is False
    assert entry.mutates_cluster is False


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

    assert seed_local.main([
        "ask",
        "--question-family",
        "authority-constrained service ownership",
    ]) == 0
    bounded = capsys.readouterr().out

    assert bounded == direct


def test_bounded_ask_listener_endpoint_matches_direct_json(capsys):
    assert seed_local.main(["--listener-endpoint-authority", "--json"]) == 0
    direct = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "listener endpoint reachability",
        "--json",
    ]) == 0
    bounded = json.loads(capsys.readouterr().out)

    assert bounded == direct


def test_bounded_ask_observation_domains_matches_direct_human_and_json(capsys):
    assert seed_local.main(["--observation-domains"]) == 0
    direct_human = capsys.readouterr().out

    assert seed_local.main([
        "ask",
        "--question-family",
        "observation domain coverage",
    ]) == 0
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--observation-domains", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "observation domain coverage",
        "--json",
    ]) == 0
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_observation_permission_matches_direct_human_and_json(capsys):
    assert seed_local.main(["--observation-permission"]) == 0
    direct_human = capsys.readouterr().out

    assert seed_local.main([
        "ask",
        "--question-family",
        "observation permission state",
    ]) == 0
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--observation-permission", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "observation permission state",
        "--json",
    ]) == 0
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_knowledge_reachability_matches_direct_json(capsys):
    assert seed_local.main([
        "--knowledge-reachability-audit",
        "--knowledge-reachability-audit-json",
    ]) == 0
    direct = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "knowledge reachability",
        "--json",
    ]) == 0
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


def test_bounded_ask_derivation_explanation_forwards_surface_args_human_and_json(capsys):
    assert seed_local.main(["--reasoning-path", "runtime", "web_service"]) == 0
    direct_human = capsys.readouterr().out

    assert seed_local.main([
        "ask",
        "--question-family",
        "derivation explanation",
        "--surface-args",
        "runtime",
        "web_service",
    ]) == 0
    bounded_human = capsys.readouterr().out

    assert seed_local.main([
        "--reasoning-path", "runtime", "web_service", "--json"
    ]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "derivation explanation",
        "--surface-args",
        "runtime",
        "web_service",
        "--json",
    ]) == 0
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_selection_explanation_forwards_surface_args_human_and_json(capsys):
    assert seed_local.main(["--selection-path", "container_ownership"]) == 0
    direct_human = capsys.readouterr().out

    assert seed_local.main([
        "ask",
        "--question-family",
        "selection explanation",
        "--surface-args",
        "container_ownership",
    ]) == 0
    bounded_human = capsys.readouterr().out

    assert seed_local.main(["--selection-path", "container_ownership", "--json"]) == 0
    direct_json = json.loads(capsys.readouterr().out)

    assert seed_local.main([
        "ask",
        "--question-family",
        "selection explanation",
        "--surface-args",
        "container_ownership",
        "--json",
    ]) == 0
    bounded_json = json.loads(capsys.readouterr().out)

    assert bounded_human == direct_human
    assert bounded_json == direct_json


def test_bounded_ask_parameterized_family_requires_exact_surface_arg_count(capsys):
    with pytest.raises(SystemExit) as too_few:
        seed_local.main([
            "ask",
            "--question-family",
            "derivation explanation",
            "--surface-args",
            "runtime",
        ])
    assert too_few.value.code == 2
    assert "requires exactly 2 --surface-args" in capsys.readouterr().err

    with pytest.raises(SystemExit) as too_many:
        seed_local.main([
            "ask",
            "--question-family",
            "selection explanation",
            "--surface-args",
            "container_ownership",
            "extra",
        ])
    assert too_many.value.code == 2
    assert "requires exactly 1 --surface-args" in capsys.readouterr().err


def test_bounded_ask_rejects_surface_args_outside_parameterized_family(capsys):
    with pytest.raises(SystemExit) as without_question_family:
        seed_local.main(["ask", "--surface-args", "runtime"])
    assert without_question_family.value.code == 2
    assert "--surface-args can only be used" in capsys.readouterr().err

    with pytest.raises(SystemExit) as zero_arg_family:
        seed_local.main([
            "ask",
            "--question-family",
            "authority-constrained service ownership",
            "--surface-args",
            "runtime",
        ])
    assert zero_arg_family.value.code == 2
    assert "does not accept --surface-args" in capsys.readouterr().err


def test_bounded_ask_rejects_diagnostic_only_family(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main(["ask", "--question-family", "surface inventory"])

    assert exc.value.code == 2
    assert "diagnostic_only" in capsys.readouterr().err


def test_bounded_ask_rejects_not_dispatchable_family(capsys):
    with pytest.raises(SystemExit) as exc:
        seed_local.main([
            "ask", "--question-family", "source definition/import lookup"
        ])

    assert exc.value.code == 2
    assert "not_dispatchable" in capsys.readouterr().err
