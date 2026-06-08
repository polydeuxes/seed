import hashlib

from seed_runtime.input_inspector import InputAct, InputInspector, classify_input_act


def test_ini_extension_containing_yaml_is_detected_from_content(tmp_path):
    path = tmp_path / "inventory.ini"
    content = """all:
  children:
    servers:
"""
    path.write_text(content, encoding="utf-8")

    artifact = InputInspector.inspect_file(path, declared_purpose="ansible_inventory")

    assert artifact.detected_format == "yaml"
    assert "extension_mismatch:.ini!=yaml" in artifact.warnings
    assert artifact.declared_purpose == "ansible_inventory"
    assert artifact.size_bytes == len(content.encode("utf-8"))
    assert artifact.sha256 == hashlib.sha256(content.encode("utf-8")).hexdigest()


def test_real_ini_is_detected_from_section(tmp_path):
    path = tmp_path / "inventory.ini"
    path.write_text(
        "[servers]\nnode115 ansible_host=192.168.254.115\n", encoding="utf-8"
    )

    artifact = InputInspector.inspect_file(path)

    assert artifact.detected_format == "ini"
    assert artifact.warnings == []


def test_json_is_detected_from_first_non_whitespace_character(tmp_path):
    path = tmp_path / "observations.json"
    path.write_text('{"observations":[]}', encoding="utf-8")

    artifact = InputInspector.inspect_file(path)

    assert artifact.detected_format == "json"


def test_empty_file_is_unknown_with_warning(tmp_path):
    path = tmp_path / "empty.yml"
    path.write_bytes(b"")

    artifact = InputInspector.inspect_file(path)

    assert artifact.detected_format == "unknown"
    assert "empty_file" in artifact.warnings


def test_null_byte_file_is_unknown_with_binary_warning(tmp_path):
    path = tmp_path / "inventory.ini"
    path.write_bytes(b"[servers]\x00node115")

    artifact = InputInspector.inspect_file(path)

    assert artifact.detected_format == "unknown"
    assert "binary_or_null_bytes" in artifact.warnings


def test_unknown_text_is_unknown_with_warning(tmp_path):
    path = tmp_path / "inventory.txt"
    path.write_text("not a supported structured format\n", encoding="utf-8")

    artifact = InputInspector.inspect_file(path)

    assert artifact.detected_format == "unknown"
    assert "unknown_format" in artifact.warnings


def test_classify_input_act_fixture_examples():
    examples = (
        ("What does Seed know about ProjectionStore?", InputAct.OPERATOR_QUERY),
        ("Install Docker on node116.", InputAct.COMMAND_REQUEST),
        ("Jellyfin is running on node116.", InputAct.USER_OBSERVATION),
        ("README says ToolExecutor owns execution.", InputAct.DOCUMENTATION_CLAIM),
        ("No, node116 is not the Jellyfin host anymore.", InputAct.CORRECTION),
        ("Thanks, that makes sense.", InputAct.CASUAL_ANSWER),
    )

    for raw_text, input_act in examples:
        inspection = classify_input_act(raw_text)

        assert inspection.raw_text == raw_text
        assert inspection.input_act == input_act
        assert inspection.input_act.value == input_act.value
        assert inspection.reason.startswith("deterministic_")


def test_input_inspection_record_is_immutable():
    inspection = classify_input_act("What does Seed know about ProjectionStore?")

    try:
        inspection.input_act = InputAct.CASUAL_ANSWER
    except (TypeError, ValueError):
        pass
    else:  # pragma: no cover - defensive across pydantic implementations
        raise AssertionError("InputInspection should be immutable")
