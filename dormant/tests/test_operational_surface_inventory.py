import json

from scripts import seed_local
from seed_runtime.diagnostic_inventory import DIAGNOSTIC_INVENTORY
from seed_runtime.operational_surface_inventory import (
    build_operational_surface_inventory,
    build_visibility_coverage_audit,
    format_operational_surface_inventory,
    format_visibility_coverage_audit,
)


def _surface(surfaces, name):
    return next(surface for surface in surfaces if surface.name == name)


def test_operational_surfaces_are_discovered_from_argparse_evidence():
    surfaces = build_operational_surface_inventory(seed_local.build_parser())

    debug = _surface(surfaces, "--current-facts-cache-debug")
    assert debug.category == "debug"
    assert debug.evidence == "argparse"


def test_operational_surface_inventory_renders(capsys):
    assert seed_local.main(["--operational-surface-inventory"]) == 0

    output = capsys.readouterr().out
    assert "Operational Surface Inventory" in output
    assert "--current-facts-cache-debug" in output
    assert "Registered:" in output


def test_operational_surface_inventory_json_is_valid(capsys):
    assert seed_local.main(["--operational-surface-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload["surfaces"], list)
    assert any(
        surface["name"] == "--operational-surface-inventory"
        and surface["registered"] is True
        for surface in payload["surfaces"]
    )


def test_visibility_coverage_audit_renders(capsys):
    assert seed_local.main(["--visibility-coverage-audit"]) == 0

    output = capsys.readouterr().out
    assert "Visibility Coverage Audit" in output
    assert "Discovered surfaces:" in output
    assert "Unregistered surfaces:" in output


def test_visibility_coverage_audit_json_is_valid(capsys):
    assert seed_local.main(["--visibility-coverage-audit", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["discovered"] >= payload["registered"]
    assert isinstance(payload["unregistered"], list)


def test_unregistered_surfaces_are_reported_with_custom_registry():
    parser = seed_local.build_parser()
    entries = tuple(
        entry
        for entry in DIAGNOSTIC_INVENTORY
        if "--current-facts-cache-debug" not in entry.cli_flags
    )

    audit = build_visibility_coverage_audit(parser, diagnostic_entries=entries)

    assert "--current-facts-cache-debug" in [
        surface.name for surface in audit.unregistered
    ]
    assert "invisible to diagnostic inventory" in format_visibility_coverage_audit(
        audit
    )


def test_registered_surfaces_are_not_falsely_reported():
    audit = build_visibility_coverage_audit(seed_local.build_parser())

    assert "--current-facts-cache-debug" not in [
        surface.name for surface in audit.unregistered
    ]
    assert _surface(audit.surfaces, "--visibility-coverage-audit").registered is True


def test_empty_state_behavior_is_sane():
    assert "No operational surfaces discovered" in format_operational_surface_inventory(
        ()
    )
    audit = build_visibility_coverage_audit(
        seed_local.build_parser(), diagnostic_entries=()
    )
    assert audit.discovered > 0


def test_operational_surface_inventory_does_not_write_event_ledger_or_mutate_cluster(
    tmp_path,
):
    db_path = tmp_path / "seed.sqlite"

    assert (
        seed_local.main(["--db", str(db_path), "--operational-surface-inventory"]) == 0
    )
    assert not db_path.exists()


def test_visibility_coverage_audit_does_not_write_event_ledger_or_mutate_cluster(
    tmp_path,
):
    db_path = tmp_path / "seed.sqlite"

    assert seed_local.main(["--db", str(db_path), "--visibility-coverage-audit"]) == 0
    assert not db_path.exists()


def _classification(items, name):
    return next(item for item in items if item.surface == name)


def test_operational_surface_classification_audit_classifies_primary_surfaces():
    from seed_runtime.operational_surface_inventory import build_operational_surface_classification_audit

    audit = build_operational_surface_classification_audit(seed_local.build_parser())

    assert _classification(audit.items, "--operational-surface-inventory").classification == "primary_surface"
    assert _classification(audit.items, "--ownership-discrepancies").classification == "primary_surface"
    assert _classification(audit.items, "--pressure-audit").classification == "primary_surface"


def test_cli_surface_classification_input_prepares_parser_material_only():
    from seed_runtime.operational_surface_inventory import (
        OperationalSurfaceClassification,
        _CliSurfaceClassificationInput,
        _prepare_cli_surface_classification_inputs,
    )

    prepared = _prepare_cli_surface_classification_inputs(
        seed_local.build_parser(), diagnostic_entries=DIAGNOSTIC_INVENTORY
    )
    observe = next(item for item in prepared if item.flag == "--operational-surface-inventory")

    assert isinstance(observe, _CliSurfaceClassificationInput)
    assert observe.flag == "--operational-surface-inventory"
    assert "--operational-surface-inventory" in observe.flags
    assert observe.help_text
    assert observe.action_type == "_StoreTrueAction"
    assert observe.category == "inventory"
    assert observe.registered is True
    assert not isinstance(observe, OperationalSurfaceClassification)
    assert not hasattr(observe, "classification")
    assert not hasattr(observe, "reason")
    assert not hasattr(observe, "to_json_dict")


def test_classification_consumes_prepared_cli_surface_input():
    from seed_runtime.operational_surface_inventory import (
        _CliSurfaceClassificationInput,
        _classification_for,
    )

    classification, reason = _classification_for(
        _CliSurfaceClassificationInput(
            flag="--example-debug",
            flags=("--example-debug",),
            help_text="Debug an example surface.",
            action_type="_StoreTrueAction",
            nargs=0,
            registered=False,
            category="debug",
        )
    )

    assert classification == "debug_surface"
    assert "argparse help" in reason


def test_filters_are_not_classified_as_primary_surfaces():
    from seed_runtime.operational_surface_inventory import build_operational_surface_classification_audit

    audit = build_operational_surface_classification_audit(seed_local.build_parser())

    assert _classification(audit.items, "--candidate-kind").classification == "filter"
    assert _classification(audit.items, "--provider").classification == "filter"
    assert _classification(audit.items, "--predicate").classification == "filter"


def test_modifiers_are_not_classified_as_primary_surfaces():
    from seed_runtime.operational_surface_inventory import build_operational_surface_classification_audit

    audit = build_operational_surface_classification_audit(seed_local.build_parser())

    assert _classification(audit.items, "--json").classification == "modifier"


def test_debug_surfaces_are_recognized():
    from seed_runtime.operational_surface_inventory import build_operational_surface_classification_audit

    audit = build_operational_surface_classification_audit(seed_local.build_parser())

    assert _classification(audit.items, "--current-facts-cache-debug").classification == "debug_surface"


def test_manual_input_paths_are_recognized():
    from seed_runtime.operational_surface_inventory import build_operational_surface_classification_audit

    audit = build_operational_surface_classification_audit(seed_local.build_parser())

    alias = _classification(audit.items, "--alias")
    assert alias.classification == "manual_input"
    assert "operator-provided" in alias.reason


def test_operational_surface_classification_audit_renders_and_json_is_valid(capsys):
    assert seed_local.main(["--operational-surface-classification-audit"]) == 0
    output = capsys.readouterr().out
    assert "Operational Surface Classification Audit" in output
    assert "Primary Surfaces:" in output
    assert "Filters:" in output

    assert seed_local.main(["--operational-surface-classification-audit", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload["items"], list)
    assert any(
        item["surface"] == "--alias" and item["classification"] == "manual_input"
        for item in payload["items"]
    )


def test_classification_empty_state_behavior_is_sane():
    import argparse
    from seed_runtime.operational_surface_inventory import (
        build_operational_surface_classification_audit,
        format_operational_surface_classification_audit,
    )

    audit = build_operational_surface_classification_audit(argparse.ArgumentParser())

    assert audit.items == ()
    assert "No CLI elements discovered" in format_operational_surface_classification_audit(audit)


def test_visibility_coverage_differentiates_primary_filters_and_modifiers():
    parser = seed_local.build_parser()
    entries = tuple(
        entry
        for entry in DIAGNOSTIC_INVENTORY
        if "--visibility-coverage-audit" not in entry.cli_flags
    )

    audit = build_visibility_coverage_audit(parser, diagnostic_entries=entries)
    output = format_visibility_coverage_audit(audit)

    assert "Unregistered primary surfaces:" in output
    assert "Unregistered filters:" in output
    assert "Unregistered modifiers:" in output
    assert audit.unregistered_classification_counts["primary_surface"] > 0
    assert audit.unregistered_classification_counts["filter"] > 0
    assert audit.unregistered_classification_counts["modifier"] > 0
