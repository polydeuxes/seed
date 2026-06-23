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


def test_selection_filters_limit_top_and_summary_only(tmp_path):
    _write(tmp_path / "docs" / "complete.md", "---\na: b\n---\n# Complete\nBody\n")
    _write(tmp_path / "docs" / "missing_front.md", "# Heading\nBody")
    _write(tmp_path / "docs" / "empty_section.md", "---\na: b\n---\n# Empty\n## Child\n")

    from seed_runtime.documentation_structure import DocumentationStructureOptions

    missing_front = observe_documentation_structure(
        tmp_path, DocumentationStructureOptions(missing_front_matter=True)
    )
    assert [document.path for document in missing_front.documents] == [
        "docs/missing_front.md"
    ]

    missing_newline = observe_documentation_structure(
        tmp_path, DocumentationStructureOptions(missing_trailing_newline=True)
    )
    assert [document.path for document in missing_newline.documents] == [
        "docs/missing_front.md"
    ]

    empty_sections = observe_documentation_structure(
        tmp_path, DocumentationStructureOptions(empty_sections=True)
    )
    assert [document.path for document in empty_sections.documents] == [
        "docs/empty_section.md"
    ]

    limited = observe_documentation_structure(tmp_path, DocumentationStructureOptions(limit=1))
    assert limited.summary["selected_documents"] == 1
    assert len(limited.documents) == 1

    top = observe_documentation_structure(tmp_path, DocumentationStructureOptions(top=1))
    assert top.summary["selected_documents"] == 1
    assert top.documents[0].path in {"docs/empty_section.md", "docs/missing_front.md"}

    summary_only = observe_documentation_structure(
        tmp_path, DocumentationStructureOptions(summary_only=True)
    )
    assert summary_only.to_json_dict()["documents"] == []
    assert "Incomplete documents" not in format_documentation_structure(summary_only)


def test_document_drilldown_and_detail_expansions_do_not_emit_prose_or_code_body(tmp_path):
    _write(
        tmp_path / "docs" / "foo.md",
        "---\nstatus: secret-value\n---\n# Foo\n\n## Empty\n## Links\nSee [secret link text](docs/bar.md).\n```python\nprint('secret code')\n```\n",
    )
    _write(tmp_path / "docs" / "bar.md", "# Bar\n")

    from seed_runtime.documentation_structure import DocumentationStructureOptions

    report = observe_documentation_structure(
        tmp_path,
        DocumentationStructureOptions(
            document="docs/foo.md",
            include_sections=True,
            include_links=True,
            include_code_fences=True,
        ),
    )
    payload = report.to_json_dict()
    document = payload["documents"][0]

    assert payload["summary"]["total_documents"] == 1
    assert document["path"] == "docs/foo.md"
    assert document["sections"]
    assert document["links"] == [
        {"line": 8, "target": "docs/bar.md", "local_document": True}
    ]
    assert document["code_fences"] == [
        {
            "start_line": 9,
            "end_line": 11,
            "fence": "```",
            "info": "python",
            "closed": True,
        }
    ]
    rendered = json.dumps(payload)
    assert "secret-value" not in rendered
    assert "secret link text" not in rendered
    assert "secret code" not in rendered


def test_document_drilldown_rejects_paths_outside_top_level_docs(tmp_path):
    from seed_runtime.documentation_structure import DocumentationStructureOptions

    for document in ["../docs/foo.md", "/tmp/foo.md", "README.md", "docs/nested/foo.md"]:
        try:
            observe_documentation_structure(
                tmp_path, DocumentationStructureOptions(document=document)
            )
        except ValueError as exc:
            assert "docs/*.md" in str(exc)
        else:
            raise AssertionError(f"expected invalid document path: {document}")


def test_cli_documentation_structure_options_are_scoped_and_json(capsys, tmp_path, monkeypatch):
    _write(tmp_path / "docs" / "foo.md", "# Foo")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert seed_local.main([
        "--documentation-structure",
        "--document",
        "docs/foo.md",
        "--sections",
        "--limit",
        "1",
        "--json",
    ]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["documents"][0]["path"] == "docs/foo.md"
    assert "sections" in payload["documents"][0]

    try:
        seed_local.main(["--document", "docs/foo.md"])
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("--document should require --documentation-structure")
