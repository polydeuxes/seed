import json
from pathlib import Path

import scripts.seed_local as seed_local
from seed_runtime.documentation_structure import (
    BOUNDARY_TEXT,
    format_documentation_structure,
    observe_documentation_structure,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_observes_yaml_front_matter_keys_and_h1_without_values_or_prose(tmp_path):
    _write(
        tmp_path / "docs" / "example.md",
        "---\nstatus: draft\nscope: repository docs\n---\n# Example\n\nThis claims authority and shape meaning.\n",
    )

    report = observe_documentation_structure(tmp_path)
    document = report.documents[0]

    assert document.path == "docs/example.md"
    assert document.front_matter_present is True
    assert document.front_matter_keys == ("status", "scope")
    assert "draft" not in json.dumps(document.to_json_dict())
    assert "repository docs" not in json.dumps(document.to_json_dict())
    assert document.heading_present is True
    assert document.title_heading == "Example"
    assert document.structure_status == "complete"
    payload = report.to_json_dict()
    assert payload["boundary"] == {
        "read_only": True,
        "interprets_prose": False,
        "infers_claims": False,
        "infers_authority": False,
        "infers_shapes": False,
        "writes_event_ledger": False,
        "mutates_repository": False,
    }
    rendered_payload = json.dumps(payload)
    assert "claims authority" not in rendered_payload
    assert "shape meaning" not in rendered_payload


def test_front_matter_must_start_file_and_missing_heading_status(tmp_path):
    _write(
        tmp_path / "docs" / "later_delimiter.md",
        "Intro prose\n---\nstatus: hidden\n---\nNot a heading\n",
    )

    document = observe_documentation_structure(tmp_path).documents[0]

    assert document.front_matter_present is False
    assert document.front_matter_keys == ()
    assert document.heading_present is False
    assert document.title_heading is None
    assert document.structure_status == "missing_front_matter_and_heading"


def test_structure_status_values_for_partial_documents(tmp_path):
    _write(tmp_path / "docs" / "complete.md", "---\na: b\n---\n# Complete\n")
    _write(tmp_path / "docs" / "missing_front.md", "# Heading\n\nBody\n")
    _write(tmp_path / "docs" / "missing_heading.md", "---\na: b\n---\nBody\n")
    _write(tmp_path / "docs" / "missing_both.md", "Body\n")

    statuses = {
        document.path: document.structure_status
        for document in observe_documentation_structure(tmp_path).documents
    }

    assert statuses == {
        "docs/complete.md": "complete",
        "docs/missing_front.md": "missing_front_matter",
        "docs/missing_heading.md": "missing_heading",
        "docs/missing_both.md": "missing_front_matter_and_heading",
    }


def test_human_output_renders_summary_incomplete_documents_and_boundary(tmp_path):
    _write(tmp_path / "docs" / "complete.md", "---\na: b\n---\n# Complete\n")
    _write(tmp_path / "docs" / "missing.md", "Body\n")

    output = format_documentation_structure(observe_documentation_structure(tmp_path))

    assert "Documentation Structure" in output
    assert "Total documents: 2" in output
    assert "With YAML front matter: 1" in output
    assert "Missing YAML front matter: 1" in output
    assert "With H1 heading: 1" in output
    assert "Missing H1 heading: 1" in output
    assert BOUNDARY_TEXT in output
    assert "docs/missing.md: missing_front_matter_and_heading" in output


def test_cli_json_is_valid_and_does_not_write_event_ledger_or_mutate_repo(tmp_path, monkeypatch, capsys):
    _write(tmp_path / "docs" / "example.md", "---\nstatus: hidden\n---\n# Example\nBody claim.\n")
    before = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert seed_local.main(["--documentation-structure", "--json"]) == 0

    after = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))
    payload = json.loads(capsys.readouterr().out)
    assert before == after
    assert payload["documents"][0]["path"] == "docs/example.md"
    assert payload["documents"][0]["front_matter_keys"] == ["status"]
    assert "hidden" not in json.dumps(payload)
    assert "Body claim" not in json.dumps(payload)
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_repository"] is False
    assert payload["boundary"]["interprets_prose"] is False
    assert payload["boundary"]["infers_claims"] is False
    assert payload["boundary"]["infers_authority"] is False
    assert payload["boundary"]["infers_shapes"] is False
