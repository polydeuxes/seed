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
    assert document.heading_outline[0].level == 1
    assert document.heading_outline[0].text == "Example"
    assert document.heading_outline[0].line_number == 5
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


def test_heading_outline_records_only_structural_heading_metadata(tmp_path):
    _write(
        tmp_path / "docs" / "outline.md",
        "\n".join(
            [
                "---",
                "status: draft",
                "---",
                "# Guide",
                "",
                "This paragraph mentions # Not a Heading and claims production purpose.",
                "### Deep Section",
                "## Repeated",
                "###### Leaf",
                "## Repeated",
                "#### Skipped Again",
                "",
            ]
        ),
    )

    document = observe_documentation_structure(tmp_path).documents[0]
    payload = document.to_json_dict()

    assert payload["heading_outline"] == [
        {"level": 1, "text": "Guide", "line_number": 4},
        {"level": 3, "text": "Deep Section", "line_number": 7},
        {"level": 2, "text": "Repeated", "line_number": 8},
        {"level": 6, "text": "Leaf", "line_number": 9},
        {"level": 2, "text": "Repeated", "line_number": 10},
        {"level": 4, "text": "Skipped Again", "line_number": 11},
    ]
    assert document.has_section_headings is True
    assert document.max_heading_depth == 6
    assert document.skipped_heading_level_present is True
    assert document.duplicate_heading_texts == ("Repeated",)

    rendered_payload = json.dumps(payload)
    assert "Not a Heading" not in rendered_payload
    assert "production purpose" not in rendered_payload


def test_heading_text_is_not_used_to_infer_document_purpose(tmp_path):
    _write(
        tmp_path / "docs" / "purpose_words.md",
        "# Operational Runbook\n\nThis prose says the document governs cluster truth.\n",
    )

    document = observe_documentation_structure(tmp_path).documents[0]
    payload = document.to_json_dict()

    assert payload["heading_outline"] == [
        {"level": 1, "text": "Operational Runbook", "line_number": 1},
    ]
    assert "purpose" not in payload
    assert "document_purpose" not in payload
    assert "governs cluster truth" not in json.dumps(payload)


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


def test_link_observation_records_targets_without_interpreting_text_or_prose(tmp_path):
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    _write(
        tmp_path / "docs" / "links.md",
        "\n".join(
            [
                "# Links",
                "",
                "[Authoritative relationship type](target.md) and [External ontology](https://example.test/schema).",
                "[claim-id]: missing.md",
                "This prose says target.md is cluster truth and should not appear.",
                "",
            ]
        ),
    )

    report = observe_documentation_structure(tmp_path)
    document = next(d for d in report.documents if d.path == "docs/links.md")
    payload = document.to_json_dict()

    assert payload["link_observations"] == [
        {
            "source_path": "docs/links.md",
            "raw_target": "target.md",
            "is_relative": True,
            "points_under_docs": True,
        },
        {
            "source_path": "docs/links.md",
            "raw_target": "https://example.test/schema",
            "is_relative": False,
            "points_under_docs": False,
        },
        {
            "source_path": "docs/links.md",
            "raw_target": "missing.md",
            "is_relative": True,
            "points_under_docs": True,
        },
    ]
    assert report.summary["internal_doc_link_count"] == 2
    assert report.summary["external_link_count"] == 1
    assert report.summary["broken_local_doc_link_count"] == 1

    rendered_payload = json.dumps(payload)
    assert "Authoritative relationship type" not in rendered_payload
    assert "External ontology" not in rendered_payload
    assert "claim-id" not in rendered_payload
    assert "cluster truth" not in rendered_payload
    assert "relationship" not in rendered_payload
    assert "ontology" not in rendered_payload


def test_link_observation_is_read_only_and_does_not_mutate_files(tmp_path):
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    _write(tmp_path / "docs" / "links.md", "# Links\n\n[Read only](target.md)\n")
    before = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }

    report = observe_documentation_structure(tmp_path)

    after = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    assert before == after
    assert report.boundary["mutates_repository"] is False
    assert report.boundary["writes_event_ledger"] is False


def test_code_block_observation_records_closed_fences_without_contents(tmp_path):
    _write(
        tmp_path / "docs" / "code.md",
        "\n".join(
            [
                "# Code",
                "",
                "```Python title=example",
                "print('secret runtime behavior')",
                "# Not a Markdown Heading",
                "```",
                "",
            ]
        ),
    )

    report = observe_documentation_structure(tmp_path)
    document = report.documents[0]
    payload = document.to_json_dict()

    assert payload["code_block_observations"] == [
        {
            "fence_type": "backtick",
            "info_string": "Python title=example",
            "language": "python",
            "start_line": 3,
            "end_line": 6,
            "closed": True,
        }
    ]
    assert report.summary["code_block_count"] == 1
    assert report.summary["unclosed_code_block_count"] == 0
    assert report.summary["code_block_languages"] == ["python"]
    assert payload["heading_outline"] == [
        {"level": 1, "text": "Code", "line_number": 1}
    ]
    rendered_payload = json.dumps(payload)
    assert "secret runtime behavior" not in rendered_payload
    assert "Not a Markdown Heading" not in rendered_payload


def test_code_block_observation_records_tilde_fences_and_unclosed_fences(tmp_path):
    _write(
        tmp_path / "docs" / "fences.md",
        "\n".join(
            [
                "# Fences",
                "",
                "~~~",
                "[hidden link](missing.md)",
                "~~~",
                "",
                "```Shell",
                "seed --should-not-be-inferred",
                "# Hidden Heading",
            ]
        ),
    )

    report = observe_documentation_structure(tmp_path)
    document = report.documents[0]
    payload = document.to_json_dict()

    assert payload["code_block_observations"] == [
        {
            "fence_type": "tilde",
            "info_string": None,
            "language": None,
            "start_line": 3,
            "end_line": 5,
            "closed": True,
        },
        {
            "fence_type": "backtick",
            "info_string": "Shell",
            "language": "shell",
            "start_line": 7,
            "end_line": None,
            "closed": False,
        },
    ]
    assert report.summary["code_block_count"] == 2
    assert report.summary["unclosed_code_block_count"] == 1
    assert report.summary["code_block_languages"] == ["shell"]
    assert payload["link_observations"] == []
    assert payload["heading_outline"] == [
        {"level": 1, "text": "Fences", "line_number": 1}
    ]
    rendered_payload = json.dumps(payload)
    assert "hidden link" not in rendered_payload
    assert "missing.md" not in rendered_payload
    assert "should-not-be-inferred" not in rendered_payload
    assert "Hidden Heading" not in rendered_payload
