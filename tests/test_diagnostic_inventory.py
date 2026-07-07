import json

import scripts.seed_local as seed_local
from seed_runtime.diagnostic_inventory import (
    DIAGNOSTIC_INVENTORY,
    DiagnosticInventoryEntry,
    _DiagnosticInventoryCompositionInput,
    _DiagnosticSurfaceBoundaryStatementSequence,
    _DiagnosticSurfaceBoundaryText,
    _DiagnosticSurfaceBoundaryFieldLabel,
    _DiagnosticSurfaceBoundaryLine,
    _DiagnosticSurfaceCliFlagDisplay,
    _DiagnosticSurfaceCliFlagsFieldLabel,
    _DiagnosticSurfaceCliFlagsLine,
    _DiagnosticSurfaceExplanationComposition,
    _KnownDiagnosticSurfaceDefinition,
    _UnknownDiagnosticSurfaceDefinition,
    _DiagnosticSurfaceHeadingLine,
    _DiagnosticSurfaceBoundaryIdentification,
    _DiagnosticSurfaceBoundaryStatementSet,
    _DiagnosticSurfaceReadOnlyEvaluation,
    _DiagnosticSurfaceConsumptionDeclarationSequence,
    _DiagnosticSurfaceConsumptionDeclarationSet,
    _DiagnosticSurfaceConsumptionLine,
    _DiagnosticSurfaceConsumptionIdentification,
    _DiagnosticSurfaceConsumptionText,
    _DiagnosticSurfaceConsumptionFieldLabel,
    _DiagnosticSurfaceDefinitionLineSet,
    _DiagnosticSurfaceDefinitionSectionLine,
    _DiagnosticSurfaceDefinitionSectionLabel,
    _DiagnosticSurfaceDefinitionSectionIndent,
    _DiagnosticSurfaceDescriptionLine,
    _DiagnosticSurfaceDescriptionFieldLabel,
    _DiagnosticSurfaceDescriptionText,
    _DiagnosticSurfaceEvidenceSourceLine,
    _DiagnosticSurfaceExplanationConsumption,
    _DiagnosticSurfaceExplanationLineSet,
    _DiagnosticSurfaceImplementationReasonLine,
    _DiagnosticSurfaceInventoryRegistrationLine,
    _DiagnosticSurfaceJsonSupportFieldLabel,
    _DiagnosticSurfaceJsonSupportLine,
    _DiagnosticSurfaceJsonSupportValue,
    _DiagnosticSurfaceNameValue,
    _DiagnosticSurfaceRecordSupportFieldLabel,
    _DiagnosticSurfaceRecordSupportLine,
    _DiagnosticSurfaceRecordSupportValue,
    _DiagnosticSurfaceRecordScopeFieldLabel,
    _DiagnosticSurfaceRecordScopeLine,
    _DiagnosticSurfaceRecordScopeValue,
    _DiagnosticSurfaceShapeRegistrationIdentification,
    _DiagnosticSurfaceShapeRegistrationLookup,
    _DiagnosticSurfaceShapeRegistrationStatusLine,
    _DiagnosticSurfaceStatusLine,
    _DiagnosticSurfaceStatusValue,
    _DiagnosticSurfaceStatusFieldLabel,
    _compose_diagnostic_inventory,
    _assemble_diagnostic_surface_boundary_statement_set,
    _assemble_diagnostic_surface_definition_line_set,
    _assemble_diagnostic_surface_explanation_line_set,
    _assemble_diagnostic_surface_consumption_declaration_set,
    _compose_diagnostic_inventory_json,
    _compose_diagnostic_surface_explanation,
    _diagnostic_surface_boundary,
    _diagnostic_surface_consumption,
    _diagnostic_surface_shape_registration_status,
    _evaluate_diagnostic_surface_read_only_boundary,
    _extract_diagnostic_surface_boundary_statement_sequence,
    _extract_diagnostic_surface_consumption_declaration_sequence,
    _extract_diagnostic_surface_explanation_boundary,
    _extract_diagnostic_surface_explanation_consumption,
    _extract_diagnostic_surface_explanation_definition,
    _format_diagnostic_surface_consumption,
    _identify_diagnostic_surface_boundary,
    _identify_diagnostic_surface_consumption,
    _identify_diagnostic_surface_shape_registration,
    _lookup_diagnostic_surface_shape_registration,
    _prepare_diagnostic_inventory_composition,
    _prepare_diagnostic_surface_boundary_text,
    _render_diagnostic_surface_boundary_line,
    _prepare_diagnostic_surface_cli_flag_display,
    _prepare_diagnostic_surface_definition_description_text,
    _prepare_diagnostic_surface_definition_json_support_value,
    _prepare_diagnostic_surface_definition_record_support_value,
    _prepare_diagnostic_surface_definition_record_scope_value,
    _prepare_diagnostic_surface_explanation_cli_flag_display,
    _prepare_diagnostic_surface_explanation_cli_flags_field_label,
    _prepare_diagnostic_surface_explanation_description_text,
    _prepare_diagnostic_surface_explanation_description_field_label,
    _prepare_diagnostic_surface_explanation_json_support_field_label,
    _prepare_diagnostic_surface_explanation_json_support_value,
    _prepare_diagnostic_surface_explanation_name_value,
    _prepare_diagnostic_surface_explanation_record_support_field_label,
    _prepare_diagnostic_surface_explanation_record_support_value,
    _prepare_diagnostic_surface_explanation_record_scope_field_label,
    _prepare_diagnostic_surface_explanation_record_scope_value,
    _prepare_diagnostic_surface_explanation_definition_section_label,
    _select_diagnostic_surface_explanation_definition_section_indent,
    _prepare_diagnostic_surface_explanation_status_value,
    _prepare_diagnostic_surface_explanation_status_field_label,
    _prepare_diagnostic_surface_explanation_boundary_text,
    _prepare_diagnostic_surface_explanation_boundary_field_label,
    _prepare_diagnostic_surface_explanation_consumption_text,
    _prepare_diagnostic_surface_explanation_consumption_field_label,
    _render_diagnostic_surface_explanation_description_line,
    _render_diagnostic_surface_explanation_json_support_line,
    _render_diagnostic_surface_explanation_record_support_line,
    _render_diagnostic_surface_explanation_record_scope_line,
    _render_diagnostic_surface_explanation_boundary_line,
    _render_diagnostic_surface_explanation_consumption_line,
    _render_diagnostic_surface_explanation_definition_heading_line,
    _render_diagnostic_surface_explanation_definition_section_line,
    _render_diagnostic_surface_explanation_cli_flags_line,
    _render_diagnostic_surface_definition_identity_heading_line,
    _render_diagnostic_surface_definition_cli_flags_line,
    _render_diagnostic_surface_explanation_status_line,
    _render_diagnostic_surface_cli_flags_line,
    _prepare_diagnostic_surface_consumption_text,
    _render_diagnostic_surface_consumption_line,
    _render_diagnostic_surface_evidence_source_line,
    _render_diagnostic_surface_definition_status_line,
    _render_diagnostic_surface_definition_description_line,
    _render_diagnostic_surface_definition_json_support_line,
    _render_diagnostic_surface_definition_record_support_line,
    _render_diagnostic_surface_definition_record_scope_line,
    _render_diagnostic_surface_definition_boundary_line,
    _render_diagnostic_surface_definition_consumption_line,
    _render_diagnostic_surface_definition_inventory_registration_line,
    _render_diagnostic_surface_definition_shape_registration_status_line,
    _render_diagnostic_surface_definition_implementation_reason_line,
    _render_diagnostic_surface_definition_evidence_source_line,
    _render_diagnostic_surface_implementation_reason_line,
    _render_diagnostic_surface_inventory_registration_line,
    _render_diagnostic_surface_shape_registration_status_line,
    _render_diagnostic_surface_status_line,
    _produce_known_diagnostic_surface_definition,
    _produce_unknown_diagnostic_surface_definition,
    _diagnostic_surface_definition_wrapper,
    _diagnostic_surface_explanation_wrapper,
    diagnostic_surface_definition_json,
    diagnostic_surface_explanation_json,
    format_diagnostic_surface_definition,
    format_diagnostic_surface_explanation,
    format_diagnostic_inventory,
)


def _entry(name: str) -> DiagnosticInventoryEntry:
    return next(entry for entry in DIAGNOSTIC_INVENTORY if entry.name == name)


def test_cli_diagnostic_inventory_lists_known_diagnostics(capsys):
    assert seed_local.main(["--diagnostic-inventory"]) == 0

    output = capsys.readouterr().out

    assert "Diagnostic" in output
    for name in [
        "classification_coverage",
        "graph_issue_summary",
        "knowledge_reachability",
        "documentation_structure",
        "ownership_discrepancies",
        "capability_needs",
        "observation_utilization",
        "architecture_conformance_audit",
        "operational_graph",
        "operational_graph_confidence",
        "operational_graph_taxonomy",
        "consumer_audit",
        "emitter_attribution_audit",
        "current_facts_cache_debug",
        "investigation_path",
    ]:
        assert name in output


def test_cli_diagnostic_inventory_json_emits_valid_json(capsys):
    assert seed_local.main(["--diagnostic-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert isinstance(payload, list)
    assert {entry["name"] for entry in payload} >= {
        "classification_coverage",
        "graph_issue_summary",
        "knowledge_reachability",
        "documentation_structure",
        "ownership_discrepancies",
        "capability_needs",
        "observation_utilization",
        "architecture_conformance_audit",
        "operational_graph",
        "operational_graph_confidence",
        "operational_graph_taxonomy",
        "consumer_audit",
        "emitter_attribution_audit",
        "current_facts_cache_debug",
        "investigation_path",
    }
    assert payload[0]["cli_flags"]


def test_recording_diagnostics_declare_diagnostic_run_scope_and_ledger_writes():
    recording_entries = [
        entry for entry in DIAGNOSTIC_INVENTORY if entry.supports_record
    ]

    assert recording_entries
    assert all(entry.record_scope == "diagnostic_run" for entry in recording_entries)
    assert all(entry.writes_event_ledger for entry in recording_entries)


def test_current_diagnostics_do_not_mutate_cluster():
    assert all(not entry.mutates_cluster for entry in DIAGNOSTIC_INVENTORY)


def test_current_diagnostic_shapes_match_implementation_authority():
    assert _entry("documentation_structure").cli_flags == (
        "--documentation-structure",
        "--document",
        "--missing-front-matter",
        "--missing-trailing-newline",
        "--empty-sections",
        "--sections",
        "--links",
        "--code-fences",
        "--architectural-relations",
        "--recurrence",
        "--rare",
        "--missing-common-sections",
        "--outliers",
        "--skeletons",
        "--where",
        "--membership",
        "--limit",
        "--top",
        "--summary-only",
        "--min-count",
        "--max-count",
    )
    assert _entry("documentation_structure").uses_repo_files
    assert (
        "exact section-label structural membership"
        in _entry("documentation_structure").description
    )
    assert (
        "without parsing code contents" in _entry("documentation_structure").description
    )
    assert _entry("documentation_structure").supports_json
    assert not _entry("documentation_structure").supports_record
    assert _entry("documentation_structure").record_scope == "none"
    assert not _entry("documentation_structure").writes_event_ledger
    assert not _entry("documentation_structure").mutates_cluster
    assert _entry("ownership_discrepancies").supports_record
    assert _entry("knowledge_reachability").uses_repo_files
    assert _entry("capability_needs").reads_diagnostic_facts
    assert _entry("current_facts_cache_debug").cli_flags == (
        "--current-facts-cache-debug",
    )
    assert not _entry("current_facts_cache_debug").writes_event_ledger
    assert not _entry("current_facts_cache_debug").mutates_cluster
    assert _entry("investigation_path").cli_flags == ("--investigation-path",)
    assert _entry("investigation_path").supports_json
    assert not _entry("investigation_path").writes_event_ledger
    assert not _entry("investigation_path").mutates_cluster
    assert _entry("architecture_conformance_audit").cli_flags == (
        "--architecture-conformance-audit",
    )
    assert _entry("architecture_conformance_audit").supports_json
    assert not _entry("architecture_conformance_audit").supports_record
    assert _entry("architecture_conformance_audit").record_scope == "none"
    assert not _entry("architecture_conformance_audit").writes_event_ledger
    assert not _entry("architecture_conformance_audit").mutates_cluster
    assert _entry("operational_graph").cli_flags == ("--operational-graph",)
    assert _entry("operational_graph").supports_json
    assert not _entry("operational_graph").supports_record
    assert _entry("operational_graph").record_scope == "none"
    assert not _entry("operational_graph").writes_event_ledger
    assert not _entry("operational_graph").mutates_cluster
    assert _entry("operational_graph_confidence").cli_flags == (
        "--operational-graph-confidence",
        "--exclude-aggregate",
    )
    assert _entry("operational_graph_taxonomy").cli_flags == (
        "--operational-graph-taxonomy",
    )
    assert _entry("operational_graph_taxonomy").supports_json
    assert not _entry("operational_graph_taxonomy").supports_record
    assert _entry("operational_graph_taxonomy").record_scope == "none"
    assert not _entry("operational_graph_taxonomy").writes_event_ledger
    assert not _entry("operational_graph_taxonomy").mutates_cluster
    assert _entry("operational_graph_confidence").supports_json
    assert not _entry("operational_graph_confidence").supports_record
    assert _entry("operational_graph_confidence").record_scope == "none"
    assert not _entry("operational_graph_confidence").writes_event_ledger
    assert not _entry("operational_graph_confidence").mutates_cluster


def test_inventory_rendering_is_generated_from_registry_data():
    rendered = format_diagnostic_inventory(
        (
            DiagnosticInventoryEntry(
                name="synthetic_probe",
                cli_flags=("--synthetic-probe",),
                uses_projected_state=False,
                uses_repo_files=True,
                supports_json=True,
                supports_record=True,
                record_scope="diagnostic_run",
                emits_diagnostic_facts=True,
                emits_cluster_facts=False,
                writes_event_ledger=True,
                mutates_cluster=False,
                reads_diagnostic_facts=True,
                description="Synthetic registry entry used to prove generated rendering.",
            ),
        )
    )

    assert "synthetic_probe" in rendered
    assert "--synthetic-probe" in rendered
    assert "diagnostic_run" in rendered
    assert "writes_event_ledger=true" in rendered
    assert "reads_diagnostic_facts=true" in rendered


def test_diagnostic_inventory_preparation_carries_only_inventory_entries():
    entries = (
        DiagnosticInventoryEntry(
            name="synthetic_probe",
            cli_flags=("--synthetic-probe",),
            uses_projected_state=False,
            uses_repo_files=True,
            supports_json=True,
            supports_record=False,
            record_scope="none",
            emits_diagnostic_facts=False,
            emits_cluster_facts=False,
            writes_event_ledger=False,
            mutates_cluster=False,
            reads_diagnostic_facts=True,
            description="Synthetic declaration proving preparation is bounded.",
        ),
    )

    prepared = _prepare_diagnostic_inventory_composition(entries)

    assert isinstance(prepared, _DiagnosticInventoryCompositionInput)
    assert prepared.entries == entries
    assert set(prepared.__dataclass_fields__) == {"entries"}


def test_diagnostic_inventory_composition_consumes_prepared_input_without_shape_changes():
    entry = DiagnosticInventoryEntry(
        name="synthetic_probe",
        cli_flags=("--synthetic-probe",),
        uses_projected_state=False,
        uses_repo_files=True,
        supports_json=True,
        supports_record=True,
        record_scope="diagnostic_run",
        emits_diagnostic_facts=True,
        emits_cluster_facts=False,
        writes_event_ledger=True,
        mutates_cluster=False,
        reads_diagnostic_facts=True,
        description="Synthetic declaration proving composition stays inventory-bounded.",
    )
    prepared = _DiagnosticInventoryCompositionInput(entries=(entry,))

    rendered = _compose_diagnostic_inventory(prepared)
    payload = _compose_diagnostic_inventory_json(prepared)

    assert "synthetic_probe" in rendered
    assert "--synthetic-probe" in rendered
    assert payload == [entry.to_json_dict()]
    assert "diagnostic_surface_boundary" not in payload[0]
    assert "shape_registration_status" not in payload[0]


def test_container_ownership_authority_inventory_entry_declares_boundary():
    entry = _entry("container_ownership_authority")

    assert entry.cli_flags == ("--container-ownership-authority",)
    assert entry.supports_json is True
    assert entry.supports_record is False
    assert entry.record_scope == "none"
    assert entry.uses_projected_state is True
    assert entry.uses_repo_files is False
    assert entry.reads_diagnostic_facts is True
    assert entry.writes_event_ledger is False
    assert entry.mutates_cluster is False


def test_projected_state_consumers_registered_in_diagnostic_inventory():
    entry = _entry("projected_state_consumers")

    assert entry.cli_flags == ("--projected-state-consumers",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.uses_projected_state
    assert not entry.uses_repo_files
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster


def test_implementation_trait_characterization_registered_in_diagnostic_inventory():
    entry = _entry("implementation_trait_characterization")

    assert entry.cli_flags == ("--implementation-trait-characterization",)
    assert entry.supports_json
    assert not entry.supports_record
    assert entry.record_scope == "none"
    assert not entry.uses_projected_state
    assert not entry.uses_repo_files
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster
    assert not entry.emits_diagnostic_facts
    assert not entry.emits_cluster_facts


def test_diagnostic_surface_definition_json_includes_identity_explanation(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    definition = payload["diagnostic_surface_definition"]

    assert definition["status"] == "known"
    assert definition["diagnostic_name"] == "diagnostic_shape_audit"
    assert definition["cli_flags"] == ["--diagnostic-shape-audit"]
    assert definition["description"] == _entry("diagnostic_shape_audit").description
    assert definition["supports_json"] is True
    assert definition["supports_record"] is False
    assert definition["record_scope"] == "none"
    assert definition["diagnostic_surface_boundary"] == {
        "status": "known",
        "statements": [
            "read-only",
            "does not record",
            "record_scope=none",
            "does not write event ledger",
            "does not mutate cluster",
            "does not use projected state",
            "does not use repository files",
            "does not emit diagnostic facts",
            "does not emit cluster facts",
            "does not read diagnostic facts",
        ],
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "boundary recovered from declared diagnostic inventory fields",
    }
    assert definition["diagnostic_surface_consumption"] == {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": False,
            "uses_repo_files": False,
            "reads_diagnostic_facts": False,
        },
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "consumption recovered from declared diagnostic inventory fields",
    }
    assert definition["diagnostic_inventory_registration"] == "present"
    assert definition["shape_registration_status"] == "present"


def test_diagnostic_surface_read_only_evaluation_precedes_boundary_identification():
    evaluation = _evaluate_diagnostic_surface_read_only_boundary(
        _entry("diagnostic_shape_audit")
    )

    assert isinstance(evaluation, _DiagnosticSurfaceReadOnlyEvaluation)
    assert evaluation.read_only is True
    assert set(evaluation.__dataclass_fields__) == {"read_only"}

    recording_evaluation = _evaluate_diagnostic_surface_read_only_boundary(
        _entry("classification_coverage")
    )

    assert isinstance(recording_evaluation, _DiagnosticSurfaceReadOnlyEvaluation)
    assert recording_evaluation.read_only is False


def test_diagnostic_surface_boundary_statement_set_precedes_identification():
    statement_set = _assemble_diagnostic_surface_boundary_statement_set(
        _entry("diagnostic_shape_audit")
    )

    assert isinstance(statement_set, _DiagnosticSurfaceBoundaryStatementSet)
    assert statement_set.statements == (
        "does not record",
        "record_scope=none",
        "does not write event ledger",
        "does not mutate cluster",
        "does not use projected state",
        "does not use repository files",
        "does not emit diagnostic facts",
        "does not emit cluster facts",
        "does not read diagnostic facts",
    )
    assert set(statement_set.__dataclass_fields__) == {"statements"}


def test_diagnostic_surface_boundary_identification_precedes_presentation():
    identification = _identify_diagnostic_surface_boundary(
        _entry("diagnostic_shape_audit")
    )

    assert isinstance(identification, _DiagnosticSurfaceBoundaryIdentification)
    assert identification.statements == (
        "read-only",
        "does not record",
        "record_scope=none",
        "does not write event ledger",
        "does not mutate cluster",
        "does not use projected state",
        "does not use repository files",
        "does not emit diagnostic facts",
        "does not emit cluster facts",
        "does not read diagnostic facts",
    )
    assert _diagnostic_surface_boundary(identification) == {
        "status": "known",
        "statements": list(identification.statements),
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "boundary recovered from declared diagnostic inventory fields",
    }


def test_diagnostic_surface_consumption_declaration_set_precedes_identification():
    declaration_set = _assemble_diagnostic_surface_consumption_declaration_set(
        _entry("diagnostic_shape_audit")
    )

    assert isinstance(declaration_set, _DiagnosticSurfaceConsumptionDeclarationSet)
    assert declaration_set.uses_projected_state is False
    assert declaration_set.uses_repo_files is False
    assert declaration_set.reads_diagnostic_facts is False
    assert set(declaration_set.__dataclass_fields__) == {
        "uses_projected_state",
        "uses_repo_files",
        "reads_diagnostic_facts",
    }


def test_diagnostic_surface_consumption_identification_precedes_presentation():
    identification = _identify_diagnostic_surface_consumption(
        _entry("diagnostic_shape_audit")
    )

    assert isinstance(identification, _DiagnosticSurfaceConsumptionIdentification)
    assert identification.uses_projected_state is False
    assert identification.uses_repo_files is False
    assert identification.reads_diagnostic_facts is False
    assert _diagnostic_surface_consumption(identification) == {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": False,
            "uses_repo_files": False,
            "reads_diagnostic_facts": False,
        },
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "consumption recovered from declared diagnostic inventory fields",
    }


def test_diagnostic_surface_shape_registration_lookup_precedes_status_identification():
    lookup = _lookup_diagnostic_surface_shape_registration("diagnostic_shape_audit")

    assert isinstance(lookup, _DiagnosticSurfaceShapeRegistrationLookup)
    assert lookup.present is True
    assert set(lookup.__dataclass_fields__) == {"present"}

    missing = _lookup_diagnostic_surface_shape_registration("synthetic_missing")

    assert isinstance(missing, _DiagnosticSurfaceShapeRegistrationLookup)
    assert missing.present is False


def test_diagnostic_surface_shape_registration_identification_precedes_definition_composition():
    identification = _identify_diagnostic_surface_shape_registration(
        "diagnostic_shape_audit"
    )

    assert isinstance(identification, _DiagnosticSurfaceShapeRegistrationIdentification)
    assert identification.status == "present"
    assert _diagnostic_surface_shape_registration_status(identification) == "present"

    missing = _identify_diagnostic_surface_shape_registration("synthetic_missing")

    assert isinstance(missing, _DiagnosticSurfaceShapeRegistrationIdentification)
    assert missing.status == "absent"
    assert _diagnostic_surface_shape_registration_status(missing) == "absent"


def test_diagnostic_surface_inventory_registration_line_rendering_precedes_line_set_assembly():
    registration_line = _render_diagnostic_surface_inventory_registration_line(
        "present", indent="    "
    )

    assert isinstance(registration_line, _DiagnosticSurfaceInventoryRegistrationLine)
    assert registration_line.line == "    diagnostic_inventory_registration: present"
    assert set(registration_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_shape_registration_status_line_rendering_follows_status_identification():
    status_line = _render_diagnostic_surface_shape_registration_status_line(
        "present", indent="    "
    )

    assert isinstance(status_line, _DiagnosticSurfaceShapeRegistrationStatusLine)
    assert status_line.line == "    shape_registration_status: present"
    assert set(status_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_implementation_reason_line_rendering_precedes_line_set_assembly():
    reason_line = _render_diagnostic_surface_implementation_reason_line(
        "known diagnostic surface recovered from diagnostic inventory",
        indent="    ",
    )

    assert isinstance(reason_line, _DiagnosticSurfaceImplementationReasonLine)
    assert (
        reason_line.line
        == "    implementation_reason: known diagnostic surface recovered from diagnostic inventory"
    )
    assert set(reason_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_evidence_source_line_rendering_precedes_line_set_assembly():
    evidence_source_line = _render_diagnostic_surface_evidence_source_line(
        "diagnostic_inventory + diagnostic_shape_audit",
        indent="    ",
    )

    assert isinstance(evidence_source_line, _DiagnosticSurfaceEvidenceSourceLine)
    assert (
        evidence_source_line.line
        == "    evidence_source: diagnostic_inventory + diagnostic_shape_audit"
    )
    assert set(evidence_source_line.__dataclass_fields__) == {"line"}


def test_known_diagnostic_surface_definition_production_precedes_wrapper_composition():
    entry = _entry("diagnostic_shape_audit")

    definition = _produce_known_diagnostic_surface_definition(entry)

    assert isinstance(definition, _KnownDiagnosticSurfaceDefinition)
    assert definition.entry == entry
    assert isinstance(definition.boundary, _DiagnosticSurfaceBoundaryIdentification)
    assert isinstance(
        definition.consumption, _DiagnosticSurfaceConsumptionIdentification
    )
    assert isinstance(
        definition.shape_registration, _DiagnosticSurfaceShapeRegistrationIdentification
    )
    assert _diagnostic_surface_definition_wrapper(definition) == {
        "diagnostic_surface_definition": diagnostic_surface_definition_json(
            "diagnostic_shape_audit"
        )["diagnostic_surface_definition"]
    }


def test_unknown_diagnostic_surface_definition_production_precedes_wrapper_composition():
    definition = _produce_unknown_diagnostic_surface_definition("synthetic_missing")

    assert isinstance(definition, _UnknownDiagnosticSurfaceDefinition)
    assert definition.diagnostic_name == "synthetic_missing"
    assert _diagnostic_surface_definition_wrapper(definition) == {
        "diagnostic_surface_definition": {
            "status": "unknown",
            "diagnostic_name": "synthetic_missing",
            "cli_flags": [],
            "description": "unknown",
            "supports_json": "unknown",
            "supports_record": "unknown",
            "record_scope": "unknown",
            "diagnostic_surface_boundary": {
                "status": "unknown",
                "statements": [],
                "evidence_source": "diagnostic_inventory",
                "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
            },
            "diagnostic_surface_consumption": {
                "status": "unknown",
                "declared_consumption": {},
                "evidence_source": "diagnostic_inventory",
                "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
            },
            "diagnostic_inventory_registration": "absent",
            "shape_registration_status": "unknown",
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        }
    }


def test_diagnostic_surface_definition_identity_heading_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    heading_line = _render_diagnostic_surface_definition_identity_heading_line(
        definition
    )

    assert isinstance(heading_line, _DiagnosticSurfaceHeadingLine)
    assert heading_line.line == "DiagnosticSurface definition: diagnostic_shape_audit"
    assert set(heading_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_status_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    status_line = _render_diagnostic_surface_definition_status_line(
        definition, indent="    "
    )

    assert isinstance(status_line, _DiagnosticSurfaceStatusLine)
    assert status_line.line == "    status: known"
    assert set(status_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_cli_flags_line_rendering_precedes_line_set_assembly():
    display = _prepare_diagnostic_surface_cli_flag_display(["--diagnostic-shape-audit"])

    cli_flags_line = _render_diagnostic_surface_definition_cli_flags_line(
        display, indent="    "
    )

    assert isinstance(cli_flags_line, _DiagnosticSurfaceCliFlagsLine)
    assert cli_flags_line.line == "    cli_flags: --diagnostic-shape-audit"
    assert set(cli_flags_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_description_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]
    description_text = _prepare_diagnostic_surface_definition_description_text(
        definition
    )

    description_line = _render_diagnostic_surface_definition_description_line(
        description_text, indent="    "
    )

    assert isinstance(description_text, _DiagnosticSurfaceDescriptionText)
    assert (
        description_text.text
        == "Compares diagnostic registry declarations with static "
        "implementation shape without recording or mutation."
    )
    assert set(description_text.__dataclass_fields__) == {"text"}
    assert isinstance(description_line, _DiagnosticSurfaceDescriptionLine)
    assert (
        description_line.line
        == "    description: Compares diagnostic registry declarations with static "
        "implementation shape without recording or mutation."
    )
    assert set(description_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_json_support_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]
    json_support_value = _prepare_diagnostic_surface_definition_json_support_value(
        definition
    )

    json_support_line = _render_diagnostic_surface_definition_json_support_line(
        json_support_value, indent="    "
    )

    assert isinstance(json_support_value, _DiagnosticSurfaceJsonSupportValue)
    assert json_support_value.value is True
    assert set(json_support_value.__dataclass_fields__) == {"value"}
    assert isinstance(json_support_line, _DiagnosticSurfaceJsonSupportLine)
    assert json_support_line.line == "    supports_json: true"
    assert set(json_support_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_record_support_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    record_support_value = _prepare_diagnostic_surface_definition_record_support_value(
        definition
    )

    record_support_line = _render_diagnostic_surface_definition_record_support_line(
        record_support_value, indent="    "
    )

    assert isinstance(record_support_value, _DiagnosticSurfaceRecordSupportValue)
    assert record_support_value.value is False
    assert set(record_support_value.__dataclass_fields__) == {"value"}
    assert isinstance(record_support_line, _DiagnosticSurfaceRecordSupportLine)
    assert record_support_line.line == "    supports_record: false"
    assert set(record_support_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_record_scope_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    record_scope_value = _prepare_diagnostic_surface_definition_record_scope_value(
        definition
    )

    record_scope_line = _render_diagnostic_surface_definition_record_scope_line(
        record_scope_value, indent="    "
    )

    assert isinstance(record_scope_value, _DiagnosticSurfaceRecordScopeValue)
    assert record_scope_value.value == "none"
    assert set(record_scope_value.__dataclass_fields__) == {"value"}
    assert isinstance(record_scope_line, _DiagnosticSurfaceRecordScopeLine)
    assert record_scope_line.line == "    record_scope: none"
    assert set(record_scope_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_boundary_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    boundary_line = _render_diagnostic_surface_definition_boundary_line(
        definition, indent="    "
    )

    assert isinstance(boundary_line, _DiagnosticSurfaceBoundaryLine)
    assert (
        boundary_line.line
        == "    diagnostic_surface_boundary: read-only; does not record; "
        "record_scope=none; does not write event ledger; does not mutate cluster; "
        "does not use projected state; does not use repository files; "
        "does not emit diagnostic facts; does not emit cluster facts; "
        "does not read diagnostic facts"
    )
    assert set(boundary_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_consumption_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    consumption_line = _render_diagnostic_surface_definition_consumption_line(
        definition, indent="    "
    )

    assert isinstance(consumption_line, _DiagnosticSurfaceConsumptionLine)
    assert (
        consumption_line.line
        == "    diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    )
    assert set(consumption_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_inventory_registration_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    registration_line = (
        _render_diagnostic_surface_definition_inventory_registration_line(
            definition, indent="    "
        )
    )

    assert isinstance(registration_line, _DiagnosticSurfaceInventoryRegistrationLine)
    assert registration_line.line == "    diagnostic_inventory_registration: present"
    assert set(registration_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_shape_registration_status_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    status_line = _render_diagnostic_surface_definition_shape_registration_status_line(
        definition, indent="    "
    )

    assert isinstance(status_line, _DiagnosticSurfaceShapeRegistrationStatusLine)
    assert status_line.line == "    shape_registration_status: present"
    assert set(status_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_implementation_reason_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    reason_line = _render_diagnostic_surface_definition_implementation_reason_line(
        definition, indent="    "
    )

    assert isinstance(reason_line, _DiagnosticSurfaceImplementationReasonLine)
    assert (
        reason_line.line
        == "    implementation_reason: identity recovered from the diagnostic inventory "
        "entry and static shape-audit registration"
    )
    assert set(reason_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_evidence_source_line_rendering_precedes_line_set_assembly():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    evidence_source_line = _render_diagnostic_surface_definition_evidence_source_line(
        definition, indent="    "
    )

    assert isinstance(evidence_source_line, _DiagnosticSurfaceEvidenceSourceLine)
    assert (
        evidence_source_line.line
        == "    evidence_source: diagnostic_inventory + diagnostic_shape_audit"
    )
    assert set(evidence_source_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_definition_line_set_assembly_precedes_human_rendering():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    line_set = _assemble_diagnostic_surface_definition_line_set(definition)

    assert isinstance(line_set, _DiagnosticSurfaceDefinitionLineSet)
    assert line_set.lines[0] == "DiagnosticSurface definition: diagnostic_shape_audit"
    assert "  cli_flags: --diagnostic-shape-audit" in line_set.lines
    assert (
        "  diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    ) in line_set.lines
    assert set(line_set.__dataclass_fields__) == {"lines"}
    assert format_diagnostic_surface_definition("diagnostic_shape_audit") == "\n".join(
        line_set.lines
    )


def test_diagnostic_surface_status_line_rendering_precedes_line_set_assembly():
    status_line = _render_diagnostic_surface_status_line("known", indent="    ")

    assert isinstance(status_line, _DiagnosticSurfaceStatusLine)
    assert status_line.line == "    status: known"
    assert set(status_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_cli_flag_display_preparation_precedes_human_rendering():
    display = _prepare_diagnostic_surface_cli_flag_display(["--alpha", "--beta"])

    assert isinstance(display, _DiagnosticSurfaceCliFlagDisplay)
    assert display.text == "--alpha, --beta"

    empty_display = _prepare_diagnostic_surface_cli_flag_display([])

    assert isinstance(empty_display, _DiagnosticSurfaceCliFlagDisplay)
    assert empty_display.text == "none"

    unknown_display = _prepare_diagnostic_surface_cli_flag_display("unknown")

    assert isinstance(unknown_display, _DiagnosticSurfaceCliFlagDisplay)
    assert unknown_display.text == "none"


def test_diagnostic_surface_cli_flags_line_rendering_follows_display_preparation():
    flag_display = _DiagnosticSurfaceCliFlagDisplay(text="--alpha, --beta")

    cli_flags_line = _render_diagnostic_surface_cli_flags_line(
        flag_display, indent="    "
    )

    assert isinstance(cli_flags_line, _DiagnosticSurfaceCliFlagsLine)
    assert cli_flags_line.line == "    cli_flags: --alpha, --beta"
    assert set(cli_flags_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_boundary_statement_sequence_extraction_precedes_text_rendering():
    boundary = {
        "status": "known",
        "statements": ["read-only", "does not record", "record_scope=none"],
    }

    sequence = _extract_diagnostic_surface_boundary_statement_sequence(boundary)

    assert isinstance(sequence, _DiagnosticSurfaceBoundaryStatementSequence)
    assert sequence.statements == (
        "read-only",
        "does not record",
        "record_scope=none",
    )
    assert set(sequence.__dataclass_fields__) == {"statements"}
    assert _prepare_diagnostic_surface_boundary_text(boundary).text == (
        "read-only; does not record; record_scope=none"
    )

    assert (
        _extract_diagnostic_surface_boundary_statement_sequence("unknown").statements
        == ()
    )
    assert (
        _extract_diagnostic_surface_boundary_statement_sequence(
            {"statements": []}
        ).statements
        == ()
    )


def test_diagnostic_surface_boundary_text_preparation_precedes_line_rendering():
    boundary = {
        "status": "known",
        "statements": ["read-only", "does not record", "record_scope=none"],
    }

    boundary_text = _prepare_diagnostic_surface_boundary_text(boundary)

    assert isinstance(boundary_text, _DiagnosticSurfaceBoundaryText)
    assert boundary_text.text == "read-only; does not record; record_scope=none"
    assert set(boundary_text.__dataclass_fields__) == {"text"}

    empty_boundary_text = _prepare_diagnostic_surface_boundary_text(
        {"status": "unknown", "statements": []}
    )

    assert isinstance(empty_boundary_text, _DiagnosticSurfaceBoundaryText)
    assert empty_boundary_text.text == "unknown"

    unknown_boundary_text = _prepare_diagnostic_surface_boundary_text("unknown")

    assert isinstance(unknown_boundary_text, _DiagnosticSurfaceBoundaryText)
    assert unknown_boundary_text.text == "unknown"


def test_diagnostic_surface_boundary_line_rendering_follows_text_preparation():
    boundary_text = _DiagnosticSurfaceBoundaryText(
        text="read-only; does not record; record_scope=none"
    )

    boundary_line = _render_diagnostic_surface_boundary_line(
        boundary_text, indent="    "
    )

    assert isinstance(boundary_line, _DiagnosticSurfaceBoundaryLine)
    assert (
        boundary_line.line
        == "    diagnostic_surface_boundary: read-only; does not record; record_scope=none"
    )
    assert set(boundary_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_consumption_declaration_sequence_extraction_precedes_text_rendering():
    consumption = {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": True,
            "uses_repo_files": False,
            "reads_diagnostic_facts": True,
        },
    }

    sequence = _extract_diagnostic_surface_consumption_declaration_sequence(consumption)

    assert isinstance(sequence, _DiagnosticSurfaceConsumptionDeclarationSequence)
    assert sequence.declarations == (
        ("uses_projected_state", True),
        ("uses_repo_files", False),
        ("reads_diagnostic_facts", True),
    )
    assert set(sequence.__dataclass_fields__) == {"declarations"}
    assert _prepare_diagnostic_surface_consumption_text(consumption).text == (
        "uses_projected_state=true; uses_repo_files=false; reads_diagnostic_facts=true"
    )

    assert (
        _extract_diagnostic_surface_consumption_declaration_sequence(
            "unknown"
        ).declarations
        == ()
    )
    assert (
        _extract_diagnostic_surface_consumption_declaration_sequence(
            {"declared_consumption": {}}
        ).declarations
        == ()
    )


def test_diagnostic_surface_consumption_text_preparation_precedes_line_rendering():
    consumption = {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": True,
            "uses_repo_files": False,
            "reads_diagnostic_facts": True,
        },
    }

    consumption_text = _prepare_diagnostic_surface_consumption_text(consumption)

    assert isinstance(consumption_text, _DiagnosticSurfaceConsumptionText)
    assert (
        consumption_text.text
        == "uses_projected_state=true; uses_repo_files=false; reads_diagnostic_facts=true"
    )
    assert set(consumption_text.__dataclass_fields__) == {"text"}

    empty_consumption_text = _prepare_diagnostic_surface_consumption_text(
        {"status": "unknown", "declared_consumption": {}}
    )

    assert isinstance(empty_consumption_text, _DiagnosticSurfaceConsumptionText)
    assert empty_consumption_text.text == "unknown"

    unknown_consumption_text = _prepare_diagnostic_surface_consumption_text("unknown")

    assert isinstance(unknown_consumption_text, _DiagnosticSurfaceConsumptionText)
    assert unknown_consumption_text.text == "unknown"


def test_diagnostic_surface_consumption_line_rendering_follows_text_preparation():
    consumption_text = _DiagnosticSurfaceConsumptionText(
        text="uses_projected_state=true; uses_repo_files=false"
    )

    consumption_line = _render_diagnostic_surface_consumption_line(
        consumption_text, indent="    "
    )

    assert isinstance(consumption_line, _DiagnosticSurfaceConsumptionLine)
    assert (
        consumption_line.line
        == "    diagnostic_surface_consumption: uses_projected_state=true; uses_repo_files=false"
    )
    assert set(consumption_line.__dataclass_fields__) == {"line"}
    assert (
        _format_diagnostic_surface_consumption(
            {
                "declared_consumption": {
                    "uses_projected_state": True,
                    "uses_repo_files": False,
                }
            },
            indent="    ",
        )
        == consumption_line.line
    )


def test_diagnostic_surface_definition_human_renders_identity_explanation(capsys):
    assert (
        seed_local.main(["--diagnostic-surface-definition", "diagnostic_shape_audit"])
        == 0
    )

    output = capsys.readouterr().out

    assert "DiagnosticSurface definition: diagnostic_shape_audit" in output
    assert "  status: known" in output
    assert "  cli_flags: --diagnostic-shape-audit" in output
    assert f"  description: {_entry('diagnostic_shape_audit').description}" in output
    assert "  supports_json: true" in output
    assert "  supports_record: false" in output
    assert "  record_scope: none" in output
    assert (
        "  diagnostic_surface_boundary: read-only; does not record; "
        "record_scope=none; does not write event ledger; does not mutate cluster; "
        "does not use projected state; does not use repository files; "
        "does not emit diagnostic facts; does not emit cluster facts; "
        "does not read diagnostic facts"
    ) in output
    assert (
        "  diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    ) in output
    assert "  diagnostic_inventory_registration: present" in output
    assert "  shape_registration_status: present" in output


def test_diagnostic_surface_definition_unknown_is_bounded(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "missing_surface", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)

    assert payload["diagnostic_surface_definition"] == {
        "status": "unknown",
        "diagnostic_name": "missing_surface",
        "cli_flags": [],
        "description": "unknown",
        "supports_json": "unknown",
        "supports_record": "unknown",
        "record_scope": "unknown",
        "diagnostic_surface_boundary": {
            "status": "unknown",
            "statements": [],
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        },
        "diagnostic_surface_consumption": {
            "status": "unknown",
            "declared_consumption": {},
            "evidence_source": "diagnostic_inventory",
            "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
        },
        "diagnostic_inventory_registration": "absent",
        "shape_registration_status": "unknown",
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
    }


def test_diagnostic_surface_definition_does_not_change_inventory_output(capsys):
    assert seed_local.main(["--diagnostic-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert isinstance(payload, list)
    assert "diagnostic_surface_definition" not in payload[0]
    assert _entry("diagnostic_surface_definition").supports_json is True
    assert _entry("diagnostic_surface_definition").record_scope == "none"
    assert not _entry("diagnostic_surface_definition").mutates_cluster
    assert "diagnostic_surface_boundary" not in payload[0]
    assert "diagnostic_surface_consumption" not in payload[0]


def test_diagnostic_surface_consumption_json_uses_inventory_declarations(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "privilege_discovery", "--json"]
        )
        == 0
    )

    definition = json.loads(capsys.readouterr().out)["diagnostic_surface_definition"]

    assert definition["diagnostic_surface_consumption"] == {
        "status": "known",
        "declared_consumption": {
            "uses_projected_state": True,
            "uses_repo_files": False,
            "reads_diagnostic_facts": True,
        },
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "consumption recovered from declared diagnostic inventory fields",
    }


def test_diagnostic_surface_definition_guardrails_exclude_runtime_planning_and_inference(
    capsys,
):
    assert (
        seed_local.main(
            ["--diagnostic-surface-definition", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    rendered = json.dumps(json.loads(capsys.readouterr().out)).lower()

    for forbidden in [
        "runtime execution",
        "diagnostic execution",
        "planner behavior",
        "semantic interpretation",
        "implementation inference",
        "consumption inference",
        "future execution",
        "new relationship concepts",
    ]:
        assert forbidden not in rendered


def test_diagnostic_surface_explanation_json_composes_only_existing_fields(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-explanation", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    explanation = payload["diagnostic_surface_explanation"]
    definition = explanation["diagnostic_surface_definition"]

    assert set(explanation) == {
        "diagnostic_surface_definition",
        "diagnostic_surface_boundary",
        "diagnostic_surface_consumption",
    }
    assert (
        explanation["diagnostic_surface_boundary"]
        == definition["diagnostic_surface_boundary"]
    )
    assert (
        explanation["diagnostic_surface_consumption"]
        == definition["diagnostic_surface_consumption"]
    )
    assert (
        definition
        == diagnostic_surface_definition_json("diagnostic_shape_audit")[
            "diagnostic_surface_definition"
        ]
    )


def test_diagnostic_surface_explanation_composition_precedes_wrapper():
    definition = diagnostic_surface_definition_json("diagnostic_shape_audit")[
        "diagnostic_surface_definition"
    ]

    explanation = _compose_diagnostic_surface_explanation(definition)

    assert isinstance(explanation, _DiagnosticSurfaceExplanationComposition)
    assert explanation.definition == definition
    assert set(explanation.__dataclass_fields__) == {"definition"}
    assert _diagnostic_surface_explanation_wrapper(explanation) == {
        "diagnostic_surface_explanation": {
            "diagnostic_surface_definition": definition,
            "diagnostic_surface_boundary": definition["diagnostic_surface_boundary"],
            "diagnostic_surface_consumption": definition[
                "diagnostic_surface_consumption"
            ],
        }
    }


def test_diagnostic_surface_explanation_line_set_assembly_precedes_human_rendering():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]

    line_set = _assemble_diagnostic_surface_explanation_line_set(explanation)

    assert isinstance(line_set, _DiagnosticSurfaceExplanationLineSet)
    assert line_set.lines[0] == "DiagnosticSurface explanation: diagnostic_shape_audit"
    assert "  definition:" in line_set.lines
    assert "    cli_flags: --diagnostic-shape-audit" in line_set.lines
    assert (
        "    diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    ) in line_set.lines
    assert set(line_set.__dataclass_fields__) == {"lines"}
    assert format_diagnostic_surface_explanation("diagnostic_shape_audit") == "\n".join(
        line_set.lines
    )


def test_diagnostic_surface_explanation_consumption_extraction_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]

    explanation_consumption = _extract_diagnostic_surface_explanation_consumption(
        explanation
    )

    assert isinstance(explanation_consumption, _DiagnosticSurfaceExplanationConsumption)
    assert (
        explanation_consumption.consumption
        == explanation["diagnostic_surface_consumption"]
    )
    assert set(explanation_consumption.__dataclass_fields__) == {"consumption"}


def test_diagnostic_surface_explanation_status_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    status_value = _prepare_diagnostic_surface_explanation_status_value(
        explanation_definition
    )
    status_field_label = _prepare_diagnostic_surface_explanation_status_field_label()
    status_line = _render_diagnostic_surface_explanation_status_line(
        status_value, field_label=status_field_label.text, indent="    "
    )

    assert isinstance(status_value, _DiagnosticSurfaceStatusValue)
    assert status_value.value == "known"
    assert set(status_value.__dataclass_fields__) == {"value"}
    assert isinstance(status_field_label, _DiagnosticSurfaceStatusFieldLabel)
    assert status_field_label.text == "status"
    assert set(status_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(status_line, _DiagnosticSurfaceStatusLine)
    assert status_line.line == "    status: known"
    assert set(status_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_description_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    description_text = _prepare_diagnostic_surface_explanation_description_text(
        explanation_definition
    )
    description_field_label = (
        _prepare_diagnostic_surface_explanation_description_field_label()
    )
    description_line = _render_diagnostic_surface_explanation_description_line(
        description_text, field_label=description_field_label.text, indent="    "
    )

    assert isinstance(description_text, _DiagnosticSurfaceDescriptionText)
    assert (
        description_text.text
        == "Compares diagnostic registry declarations with static "
        "implementation shape without recording or mutation."
    )
    assert set(description_text.__dataclass_fields__) == {"text"}
    assert isinstance(description_field_label, _DiagnosticSurfaceDescriptionFieldLabel)
    assert description_field_label.text == "description"
    assert set(description_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(description_line, _DiagnosticSurfaceDescriptionLine)
    assert (
        description_line.line
        == "    description: Compares diagnostic registry declarations with static "
        "implementation shape without recording or mutation."
    )
    assert set(description_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_json_support_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    json_support_value = _prepare_diagnostic_surface_explanation_json_support_value(
        explanation_definition
    )
    json_support_field_label = (
        _prepare_diagnostic_surface_explanation_json_support_field_label()
    )
    json_support_line = _render_diagnostic_surface_explanation_json_support_line(
        json_support_value, field_label=json_support_field_label.text, indent="    "
    )

    assert isinstance(json_support_value, _DiagnosticSurfaceJsonSupportValue)
    assert json_support_value.value is True
    assert set(json_support_value.__dataclass_fields__) == {"value"}
    assert isinstance(json_support_field_label, _DiagnosticSurfaceJsonSupportFieldLabel)
    assert json_support_field_label.text == "supports_json"
    assert set(json_support_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(json_support_line, _DiagnosticSurfaceJsonSupportLine)
    assert json_support_line.line == "    supports_json: true"
    assert set(json_support_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_record_support_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    record_support_value = _prepare_diagnostic_surface_explanation_record_support_value(
        explanation_definition
    )
    record_support_field_label = (
        _prepare_diagnostic_surface_explanation_record_support_field_label()
    )
    record_support_line = _render_diagnostic_surface_explanation_record_support_line(
        record_support_value, field_label=record_support_field_label.text, indent="    "
    )

    assert isinstance(record_support_value, _DiagnosticSurfaceRecordSupportValue)
    assert record_support_value.value is False
    assert set(record_support_value.__dataclass_fields__) == {"value"}
    assert isinstance(
        record_support_field_label, _DiagnosticSurfaceRecordSupportFieldLabel
    )
    assert record_support_field_label.text == "supports_record"
    assert set(record_support_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(record_support_line, _DiagnosticSurfaceRecordSupportLine)
    assert record_support_line.line == "    supports_record: false"
    assert set(record_support_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_record_scope_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    record_scope_value = _prepare_diagnostic_surface_explanation_record_scope_value(
        explanation_definition
    )
    record_scope_field_label = (
        _prepare_diagnostic_surface_explanation_record_scope_field_label()
    )
    record_scope_line = _render_diagnostic_surface_explanation_record_scope_line(
        record_scope_value, field_label=record_scope_field_label.text, indent="    "
    )

    assert isinstance(record_scope_value, _DiagnosticSurfaceRecordScopeValue)
    assert record_scope_value.value == "none"
    assert set(record_scope_value.__dataclass_fields__) == {"value"}
    assert isinstance(record_scope_field_label, _DiagnosticSurfaceRecordScopeFieldLabel)
    assert record_scope_field_label.text == "record_scope"
    assert set(record_scope_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(record_scope_line, _DiagnosticSurfaceRecordScopeLine)
    assert record_scope_line.line == "    record_scope: none"
    assert set(record_scope_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_boundary_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_boundary = _extract_diagnostic_surface_explanation_boundary(explanation)

    boundary_text = _prepare_diagnostic_surface_explanation_boundary_text(
        explanation_boundary
    )
    boundary_field_label = (
        _prepare_diagnostic_surface_explanation_boundary_field_label()
    )
    boundary_line = _render_diagnostic_surface_explanation_boundary_line(
        boundary_text, field_label=boundary_field_label.text, indent="    "
    )

    assert isinstance(boundary_text, _DiagnosticSurfaceBoundaryText)
    assert boundary_text.text == (
        "read-only; does not record; record_scope=none; does not write event "
        "ledger; does not mutate cluster; does not use projected state; does not "
        "use repository files; does not emit diagnostic facts; does not emit "
        "cluster facts; does not read diagnostic facts"
    )
    assert set(boundary_text.__dataclass_fields__) == {"text"}
    assert isinstance(boundary_field_label, _DiagnosticSurfaceBoundaryFieldLabel)
    assert boundary_field_label.text == "diagnostic_surface_boundary"
    assert set(boundary_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(boundary_line, _DiagnosticSurfaceBoundaryLine)
    assert boundary_line.line == (
        "    diagnostic_surface_boundary: read-only; does not record; "
        "record_scope=none; does not write event ledger; does not mutate cluster; "
        "does not use projected state; does not use repository files; does not emit "
        "diagnostic facts; does not emit cluster facts; does not read diagnostic facts"
    )
    assert set(boundary_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_consumption_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_consumption = _extract_diagnostic_surface_explanation_consumption(
        explanation
    )

    consumption_text = _prepare_diagnostic_surface_explanation_consumption_text(
        explanation_consumption
    )
    consumption_field_label = (
        _prepare_diagnostic_surface_explanation_consumption_field_label()
    )
    consumption_line = _render_diagnostic_surface_explanation_consumption_line(
        consumption_text, field_label=consumption_field_label.text, indent="    "
    )

    assert isinstance(consumption_text, _DiagnosticSurfaceConsumptionText)
    assert consumption_text.text == (
        "uses_projected_state=false; uses_repo_files=false; reads_diagnostic_facts=false"
    )
    assert set(consumption_text.__dataclass_fields__) == {"text"}
    assert isinstance(consumption_field_label, _DiagnosticSurfaceConsumptionFieldLabel)
    assert consumption_field_label.text == "diagnostic_surface_consumption"
    assert set(consumption_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(consumption_line, _DiagnosticSurfaceConsumptionLine)
    assert consumption_line.line == (
        "    diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    )
    assert set(consumption_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_definition_heading_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    name_value = _prepare_diagnostic_surface_explanation_name_value(
        explanation_definition
    )
    heading_line = _render_diagnostic_surface_explanation_definition_heading_line(
        name_value
    )

    assert isinstance(name_value, _DiagnosticSurfaceNameValue)
    assert name_value.value == "diagnostic_shape_audit"
    assert set(name_value.__dataclass_fields__) == {"value"}
    assert isinstance(heading_line, _DiagnosticSurfaceHeadingLine)
    assert heading_line.line == "DiagnosticSurface explanation: diagnostic_shape_audit"
    assert set(heading_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_definition_section_line_rendering_precedes_line_set_assembly():
    section_label = _prepare_diagnostic_surface_explanation_definition_section_label()
    section_indent = _select_diagnostic_surface_explanation_definition_section_indent()
    section_line = _render_diagnostic_surface_explanation_definition_section_line(
        section_label, indent=section_indent.text
    )

    assert isinstance(section_label, _DiagnosticSurfaceDefinitionSectionLabel)
    assert section_label.text == "definition"
    assert set(section_label.__dataclass_fields__) == {"text"}
    assert isinstance(section_indent, _DiagnosticSurfaceDefinitionSectionIndent)
    assert section_indent.text == "  "
    assert set(section_indent.__dataclass_fields__) == {"text"}
    assert isinstance(section_line, _DiagnosticSurfaceDefinitionSectionLine)
    assert section_line.line == "  definition:"
    assert set(section_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_cli_flag_display_preparation_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )

    flag_display = _prepare_diagnostic_surface_explanation_cli_flag_display(
        explanation_definition
    )

    assert isinstance(flag_display, _DiagnosticSurfaceCliFlagDisplay)
    assert flag_display.text == "--diagnostic-shape-audit"
    assert set(flag_display.__dataclass_fields__) == {"text"}


def test_diagnostic_surface_explanation_cli_flags_line_rendering_precedes_line_set_assembly():
    explanation = diagnostic_surface_explanation_json("diagnostic_shape_audit")[
        "diagnostic_surface_explanation"
    ]
    explanation_definition = _extract_diagnostic_surface_explanation_definition(
        explanation
    )
    flag_display = _prepare_diagnostic_surface_explanation_cli_flag_display(
        explanation_definition
    )

    cli_flags_field_label = (
        _prepare_diagnostic_surface_explanation_cli_flags_field_label()
    )
    cli_flags_line = _render_diagnostic_surface_explanation_cli_flags_line(
        flag_display, field_label=cli_flags_field_label.text, indent="    "
    )

    assert isinstance(cli_flags_field_label, _DiagnosticSurfaceCliFlagsFieldLabel)
    assert cli_flags_field_label.text == "cli_flags"
    assert set(cli_flags_field_label.__dataclass_fields__) == {"text"}
    assert isinstance(cli_flags_line, _DiagnosticSurfaceCliFlagsLine)
    assert cli_flags_line.line == "    cli_flags: --diagnostic-shape-audit"
    assert set(cli_flags_line.__dataclass_fields__) == {"line"}


def test_diagnostic_surface_explanation_human_renders_coherent_composition(capsys):
    assert (
        seed_local.main(["--diagnostic-surface-explanation", "diagnostic_shape_audit"])
        == 0
    )

    output = capsys.readouterr().out

    assert "DiagnosticSurface explanation: diagnostic_shape_audit" in output
    assert "  definition:" in output
    assert "    status: known" in output
    assert "    cli_flags: --diagnostic-shape-audit" in output
    assert "    diagnostic_surface_boundary: read-only; does not record;" in output
    assert (
        "    diagnostic_surface_consumption: uses_projected_state=false; "
        "uses_repo_files=false; reads_diagnostic_facts=false"
    ) in output
    assert "implementation_reason" not in output
    assert "evidence_source" not in output


def test_diagnostic_surface_explanation_unknown_is_bounded(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-explanation", "missing_surface", "--json"]
        )
        == 0
    )

    explanation = json.loads(capsys.readouterr().out)["diagnostic_surface_explanation"]

    assert explanation["diagnostic_surface_definition"]["status"] == "unknown"
    assert (
        explanation["diagnostic_surface_definition"]["diagnostic_name"]
        == "missing_surface"
    )
    assert explanation["diagnostic_surface_boundary"] == {
        "status": "unknown",
        "statements": [],
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
    }
    assert explanation["diagnostic_surface_consumption"] == {
        "status": "unknown",
        "declared_consumption": {},
        "evidence_source": "diagnostic_inventory",
        "implementation_reason": "unknown diagnostic surface; no diagnostic inventory entry exists",
    }


def test_diagnostic_surface_explanation_preserves_existing_field_behaviors(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-explanation", "privilege_discovery", "--json"]
        )
        == 0
    )

    composed = json.loads(capsys.readouterr().out)["diagnostic_surface_explanation"]
    existing = diagnostic_surface_definition_json("privilege_discovery")[
        "diagnostic_surface_definition"
    ]

    assert composed["diagnostic_surface_definition"] == existing
    assert (
        composed["diagnostic_surface_boundary"]
        == existing["diagnostic_surface_boundary"]
    )
    assert (
        composed["diagnostic_surface_consumption"]
        == existing["diagnostic_surface_consumption"]
    )


def test_diagnostic_surface_explanation_does_not_change_inventory_output(capsys):
    assert seed_local.main(["--diagnostic-inventory", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)

    assert "diagnostic_surface_explanation" not in payload[0]
    entry = _entry("diagnostic_surface_explanation")
    assert entry.cli_flags == ("--diagnostic-surface-explanation",)
    assert entry.supports_json is True
    assert entry.record_scope == "none"
    assert not entry.writes_event_ledger
    assert not entry.mutates_cluster


def test_diagnostic_surface_explanation_guardrails_are_presentation_only(capsys):
    assert (
        seed_local.main(
            ["--diagnostic-surface-explanation", "diagnostic_shape_audit", "--json"]
        )
        == 0
    )

    rendered = json.dumps(json.loads(capsys.readouterr().out)).lower()

    for forbidden in [
        "runtime inference",
        "presentation reasoning",
        "normalize",
        "reinterpret",
        "recommend",
        "semantic meaning",
        "implementation not already present",
        "presentation framework",
        "explainablesubject",
        "ontology",
        "generic composition",
    ]:
        assert forbidden not in rendered
