import json
from pathlib import Path

import scripts.seed_local as seed_local
from seed_runtime.documentation_structure import (
    BOUNDARY_TEXT,
    DocumentationStructureDetailExpansions,
    DocumentationStructureOptions,
    documentation_structure_json,
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


def test_document_metrics_for_empty_document(tmp_path):
    _write(tmp_path / "docs" / "empty.md", "")

    document = observe_documentation_structure(tmp_path).documents[0]
    payload = document.to_json_dict()

    assert payload["line_count"] == 0
    assert payload["byte_count"] == 0
    assert payload["blank_line_count"] == 0
    assert payload["nonblank_line_count"] == 0
    assert payload["empty_document"] is True
    assert payload["has_trailing_newline"] is False


def test_document_metrics_for_document_without_trailing_newline(tmp_path):
    _write(tmp_path / "docs" / "no_newline.md", "# Title\nBody")

    document = observe_documentation_structure(tmp_path).documents[0]

    assert document.line_count == 2
    assert document.byte_count == len(b"# Title\nBody")
    assert document.blank_line_count == 0
    assert document.nonblank_line_count == 2
    assert document.empty_document is False
    assert document.has_trailing_newline is False


def test_document_metrics_count_blank_lines_mechanically(tmp_path):
    _write(tmp_path / "docs" / "blank_lines.md", "# Title\n\n   \nBody\n")

    document = observe_documentation_structure(tmp_path).documents[0]

    assert document.line_count == 4
    assert document.blank_line_count == 2
    assert document.nonblank_line_count == 2
    assert document.has_trailing_newline is True


def test_document_metrics_report_byte_and_line_count_summary(tmp_path):
    _write(tmp_path / "docs" / "alpha.md", "# A\nBody\n")
    _write(tmp_path / "docs" / "beta.md", "# B\n\n")

    report = observe_documentation_structure(tmp_path)
    metrics_by_path = {document.path: document for document in report.documents}

    assert metrics_by_path["docs/alpha.md"].line_count == 2
    assert metrics_by_path["docs/alpha.md"].byte_count == len(b"# A\nBody\n")
    assert metrics_by_path["docs/beta.md"].line_count == 2
    assert metrics_by_path["docs/beta.md"].byte_count == len(b"# B\n\n")
    assert report.summary["total_lines"] == 4
    assert report.summary["total_bytes"] == len(b"# A\nBody\n") + len(b"# B\n\n")
    assert report.summary["blank_line_count"] == 1
    assert report.summary["nonblank_line_count"] == 3
    assert report.summary["empty_document_count"] == 0
    assert report.summary["documents_without_trailing_newline"] == 0


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


def test_section_inventory_uses_heading_hierarchy_without_prose_output(tmp_path):
    _write(
        tmp_path / "docs" / "sections.md",
        "\n".join(
            [
                "# Root",
                "Intro prose says authority and shape should stay hidden.",
                "## Child",
                "### Grandchild",
                "Grandchild body claim should stay hidden.",
                "## Empty Child",
                "",
            ]
        ),
    )

    report = observe_documentation_structure(tmp_path)
    document = report.documents[0]
    payload = document.to_json_dict()

    assert payload["sections"] == [
        {
            "heading_text": "Root",
            "heading_level": 1,
            "start_line": 1,
            "end_line": 6,
            "child_section_count": 2,
            "parent_heading_path": [],
        },
        {
            "heading_text": "Child",
            "heading_level": 2,
            "start_line": 3,
            "end_line": 5,
            "child_section_count": 1,
            "parent_heading_path": ["Root"],
        },
        {
            "heading_text": "Grandchild",
            "heading_level": 3,
            "start_line": 4,
            "end_line": 5,
            "child_section_count": 0,
            "parent_heading_path": ["Root", "Child"],
        },
        {
            "heading_text": "Empty Child",
            "heading_level": 2,
            "start_line": 6,
            "end_line": 6,
            "child_section_count": 0,
            "parent_heading_path": ["Root"],
        },
    ]
    assert document.section_count == 4
    assert document.max_section_depth == 3
    assert document.empty_section_count == 1
    assert report.summary["section_count"] == 4
    assert report.summary["max_section_depth"] == 3
    assert report.summary["empty_section_count"] == 1

    rendered_payload = json.dumps(payload)
    assert "Intro prose" not in rendered_payload
    assert "authority" not in rendered_payload
    assert "shape" not in rendered_payload
    assert "body claim" not in rendered_payload


def test_section_boundaries_ignore_heading_like_text_inside_code_blocks(tmp_path):
    _write(
        tmp_path / "docs" / "section_code.md",
        "\n".join(
            [
                "# Root",
                "```",
                "## Not a Section",
                "```",
                "## Next",
            ]
        ),
    )

    document = observe_documentation_structure(tmp_path).documents[0]
    payload = document.to_json_dict()

    assert payload["sections"] == [
        {
            "heading_text": "Root",
            "heading_level": 1,
            "start_line": 1,
            "end_line": 5,
            "child_section_count": 1,
            "parent_heading_path": [],
        },
        {
            "heading_text": "Next",
            "heading_level": 2,
            "start_line": 5,
            "end_line": 5,
            "child_section_count": 0,
            "parent_heading_path": ["Root"],
        },
    ]
    assert "Not a Section" not in json.dumps(payload)


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
    assert "Total lines: 5" in output
    assert "Total bytes: 29" in output
    assert "Blank lines: 0" in output
    assert "Nonblank lines: 5" in output
    assert "Empty documents: 0" in output
    assert "Documents without trailing newline: 0" in output
    assert "With YAML front matter: 1" in output
    assert "Missing YAML front matter: 1" in output
    assert "With H1 heading: 1" in output
    assert "Missing H1 heading: 1" in output
    assert BOUNDARY_TEXT in output
    assert "docs/missing.md: missing_front_matter_and_heading" in output


def test_cli_json_is_valid_and_does_not_write_event_ledger_or_mutate_repo(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "example.md",
        "---\nstatus: hidden\n---\n# Example\nBody claim.\n",
    )
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


def test_documentation_structure_filter_flags_are_rejected_without_surface():
    filter_flags = [
        "--missing-front-matter",
        "--missing-trailing-newline",
        "--empty-sections",
        "--links",
        "--code-fences",
        "--sections",
    ]
    for flag in filter_flags:
        try:
            seed_local.main([flag])
        except SystemExit as exc:
            assert exc.code == 2
        else:  # pragma: no cover - defensive assertion
            raise AssertionError(
                f"{flag} should be rejected without --documentation-structure"
            )


def test_documentation_structure_filter_flags_are_accepted_and_read_only(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "complete.md",
        "---\nstatus: ok\n---\n# Complete\n\n[Target](target.md)\n",
    )
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    _write(tmp_path / "docs" / "missing_front.md", "# Missing Front\n\n")
    _write(
        tmp_path / "docs" / "missing_newline.md",
        "---\nstatus: ok\n---\n# Missing Newline",
    )
    _write(
        tmp_path / "docs" / "empty_sections.md",
        "# Empty Sections\n\n## Empty\n## Next\nBody\n",
    )
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    cases = [
        (["--missing-front-matter"], "docs/missing_front.md"),
        (["--missing-trailing-newline"], "docs/missing_newline.md"),
        (["--empty-sections"], "docs/empty_sections.md"),
        (["--links"], "Links:"),
        (["--code-fences"], "Code fences:"),
        (["--sections"], "Sections:"),
    ]
    for flags, expected in cases:
        before = {
            p.relative_to(tmp_path).as_posix(): p.read_bytes()
            for p in tmp_path.rglob("*")
            if p.is_file()
        }
        assert seed_local.main(["--documentation-structure", *flags]) == 0
        output = capsys.readouterr().out
        after = {
            p.relative_to(tmp_path).as_posix(): p.read_bytes()
            for p in tmp_path.rglob("*")
            if p.is_file()
        }
        assert before == after
        assert expected in output
        assert BOUNDARY_TEXT in output
        assert "event ledger writes" in output


def test_documentation_structure_detail_flags_are_accepted_in_json_and_read_only(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "details.md",
        "# Details\n\n## Empty\n\n[Target](target.md)\n\n```python\nprint('hidden')\n```\n",
    )
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)
    before = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--links",
                "--code-fences",
                "--sections",
                "--json",
            ]
        )
        == 0
    )

    after = sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*"))
    payload = json.loads(capsys.readouterr().out)
    document = next(d for d in payload["documents"] if d["path"] == "docs/details.md")
    assert before == after
    assert document["link_observations"]
    assert document["code_block_observations"]
    assert document["sections"]
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_repository"] is False


def test_documentation_structure_document_selects_single_doc_in_human_output(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "selected.md",
        "# Selected\n\nVisible prose must stay hidden.\n",
    )
    _write(tmp_path / "docs" / "other.md", "# Other\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(["--documentation-structure", "--document", "docs/selected.md"])
        == 0
    )

    output = capsys.readouterr().out
    assert "Selected document: docs/selected.md" in output
    assert "Total documents: 1" in output
    assert "docs/other.md" not in output
    assert "Visible prose" not in output
    assert BOUNDARY_TEXT in output


def test_documentation_structure_document_missing_is_rejected(tmp_path, monkeypatch):
    _write(tmp_path / "docs" / "present.md", "# Present\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    try:
        seed_local.main(["--documentation-structure", "--document", "docs/missing.md"])
    except SystemExit as exc:
        assert exc.code == 2
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("missing document should be rejected")


def test_documentation_structure_document_rejects_traversal(tmp_path, monkeypatch):
    _write(tmp_path / "docs" / "present.md", "# Present\n")
    _write(tmp_path / "outside.md", "# Outside\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    for path in ["docs/../outside.md", "../seed/docs/present.md"]:
        try:
            seed_local.main(["--documentation-structure", "--document", path])
        except SystemExit as exc:
            assert exc.code == 2
        else:  # pragma: no cover - defensive assertion
            raise AssertionError(f"{path} should be rejected")


def test_documentation_structure_document_rejects_non_doc_paths(tmp_path, monkeypatch):
    _write(tmp_path / "docs" / "notes.txt", "# Notes\n")
    _write(tmp_path / "README.md", "# Readme\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    for path in ["docs/notes.txt", "README.md", str(tmp_path / "docs" / "notes.md")]:
        try:
            seed_local.main(["--documentation-structure", "--document", path])
        except SystemExit as exc:
            assert exc.code == 2
        else:  # pragma: no cover - defensive assertion
            raise AssertionError(f"{path} should be rejected")


def test_documentation_structure_document_json_shape_is_stable(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "selected.md",
        "---\nsecret: hidden\n---\n# Selected\n\nClaim text.\n",
    )
    _write(tmp_path / "docs" / "other.md", "# Other\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--document",
                "docs/selected.md",
                "--json",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert set(payload) == {"documents", "summary", "boundary"}
    assert [document["path"] for document in payload["documents"]] == [
        "docs/selected.md"
    ]
    assert payload["summary"]["total_documents"] == 1
    assert payload["summary"]["selected_document"] == "docs/selected.md"
    assert payload["boundary"]["interprets_prose"] is False
    rendered_payload = json.dumps(payload)
    assert "hidden" not in rendered_payload
    assert "Claim text" not in rendered_payload


def test_documentation_structure_document_flag_is_rejected_without_surface():
    try:
        seed_local.main(["--document", "docs/example.md"])
    except SystemExit as exc:
        assert exc.code == 2
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("--document should require --documentation-structure")


def test_documentation_structure_filters_select_without_detail_expansion_or_semantics(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "missing_front.md",
        "# Operational Truth\n\n[Hidden](target.md)\n\n```python\nprint('semantic claim')\n```\n",
    )
    _write(tmp_path / "docs" / "target.md", "---\nstatus: ok\n---\n# Target\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--missing-front-matter", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert [document["path"] for document in payload["documents"]] == [
        "docs/missing_front.md"
    ]
    assert payload["summary"]["total_documents"] == 1
    assert payload["summary"]["selected_documents"] == 1
    assert payload["summary"]["total_available_documents"] == 2
    document = payload["documents"][0]
    assert "sections" not in document
    assert "link_observations" not in document
    assert "code_block_observations" not in document
    rendered_payload = json.dumps(payload)
    assert "semantic claim" not in rendered_payload
    assert "document_purpose" not in rendered_payload
    assert payload["boundary"]["interprets_prose"] is False
    assert payload["boundary"]["infers_claims"] is False
    assert payload["boundary"]["infers_authority"] is False


def test_documentation_structure_detail_expansions_do_not_select_documents(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "plain.md", "# Plain\n")
    _write(
        tmp_path / "docs" / "details.md",
        "# Details\n\n## Child\n\n[Target](target.md)\n\n```text\nnot interpreted\n```\n",
    )
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--sections",
                "--links",
                "--code-fences",
                "--json",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    assert [document["path"] for document in payload["documents"]] == [
        "docs/details.md",
        "docs/plain.md",
        "docs/target.md",
    ]
    details = next(d for d in payload["documents"] if d["path"] == "docs/details.md")
    assert details["sections"]
    assert details["link_observations"]
    assert details["code_block_observations"]
    assert payload["boundary"]["interprets_prose"] is False


def test_documentation_structure_limit_bounds_document_output(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "a.md", "# A\n")
    _write(tmp_path / "docs" / "b.md", "# B\n")
    _write(tmp_path / "docs" / "c.md", "# C\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert seed_local.main(["--documentation-structure", "--limit", "2", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert [document["path"] for document in payload["documents"]] == [
        "docs/a.md",
        "docs/b.md",
    ]
    assert payload["summary"]["matching_documents"] == 3
    assert payload["summary"]["output_documents"] == 2
    assert payload["summary"]["limit"] == 2


def test_documentation_structure_top_prioritizes_structural_offenders(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "ok.md", "---\nstatus: ok\n---\n# OK\n")
    _write(
        tmp_path / "docs" / "broken.md",
        "# Broken\n\n[Missing](missing.md)\n```python\n",
    )
    _write(tmp_path / "docs" / "missing_front.md", "# Missing Front\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert seed_local.main(["--documentation-structure", "--top", "1", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert [document["path"] for document in payload["documents"]] == ["docs/broken.md"]
    assert payload["summary"]["matching_documents"] == 3
    assert payload["summary"]["output_documents"] == 1
    assert payload["summary"]["top"] == 1


def test_documentation_structure_summary_only_suppresses_rows_and_details(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "details.md",
        "# Details\n\n## Child\n\n[Target](target.md)\n",
    )
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--sections", "--links", "--summary-only"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Matching documents: 2" in output
    assert "Output documents: 0" in output
    assert "\nSections:\n" not in output
    assert "\nLinks:\n" not in output
    assert "docs/details.md" not in output
    assert BOUNDARY_TEXT in output


def test_documentation_structure_output_bounds_require_surface():
    for flag in ["--limit", "--top", "--summary-only"]:
        args = [flag]
        if flag != "--summary-only":
            args.append("1")
        try:
            seed_local.main(args)
        except SystemExit as exc:
            assert exc.code == 2
        else:  # pragma: no cover - defensive assertion
            raise AssertionError(f"{flag} should require --documentation-structure")


def test_recurrence_counts_are_structural_raw_and_json_boundary(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    _write(
        tmp_path / "docs" / "alpha.md",
        "---\nstatus: draft\nscope: secret meaning\n---\n# Alpha\n\n## Findings\nProse claims authority and ontology promotion.\n\n```bash\necho hi\n```\n\n[doc](target.md) [external](https://example.test)\n",
    )
    _write(
        tmp_path / "docs" / "beta.md",
        "---\nstatus: final\ncreated: 2026-01-01\n---\n# Beta\n\n## Findings\nNo claim should be extracted.\n\n```yaml\na: b\n```\n\n[missing](missing.md)\n",
    )
    before = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--recurrence", "--min-count", "1", "--json"]
        )
        == 0
    )

    after = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    payload = json.loads(capsys.readouterr().out)
    assert before == after
    assert payload["documents"] == 3
    recurrence = payload["recurrence"]
    assert recurrence["applied_min_count"] == {
        "section_labels": 1,
        "front_matter_keys": 1,
        "heading_depths": 1,
        "code_fence_languages": 1,
    }
    assert recurrence["itemized_summaries"]["section_labels"] == {
        "total_distinct_entries": 4,
        "entries_at_or_above_min_count": 4,
    }
    assert {row["label"]: row["count"] for row in recurrence["section_labels"]}[
        "Findings"
    ] == 2
    assert {row["key"]: row["count"] for row in recurrence["front_matter_keys"]} == {
        "status": 2,
        "scope": 1,
        "created": 1,
    }
    assert {row["depth"]: row["count"] for row in recurrence["heading_depths"]} == {
        1: 3,
        2: 2,
    }
    assert {
        row["language"]: row["count"] for row in recurrence["code_fence_languages"]
    } == {"bash": 1, "yaml": 1}
    assert recurrence["link_target_classes"] == {
        "internal_docs_links": 2,
        "external_links": 1,
        "broken_local_docs_links": 1,
    }
    rendered = json.dumps(payload)
    assert "secret meaning" not in rendered
    assert "claims authority" not in rendered
    assert "No claim" not in rendered
    assert payload["boundary"] == {
        "read_only": True,
        "prose_interpretation": False,
        "claim_extraction": False,
        "authority_inference": False,
        "shape_inference": False,
        "ontology_promotion": False,
        "writes_event_ledger": False,
        "mutates_repository": False,
    }


def test_recurrence_min_count_filters_itemized_groups_not_link_totals(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "target.md", "# Target\n")
    _write(
        tmp_path / "docs" / "one.md",
        "---\nstatus: draft\nsolo: yes\n---\n# One\n## Repeat\n```text\nx\n```\n[ok](target.md) [external](https://example.test)\n",
    )
    _write(
        tmp_path / "docs" / "two.md",
        "---\nstatus: final\n---\n# Two\n## Repeat\n## Solo\n```bash\nx\n```\n[missing](missing.md)\n",
    )
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--recurrence", "--min-count", "2", "--json"]
        )
        == 0
    )

    recurrence = json.loads(capsys.readouterr().out)["recurrence"]
    assert {row["label"] for row in recurrence["section_labels"]} == {"Repeat"}
    assert {row["key"] for row in recurrence["front_matter_keys"]} == {"status"}
    assert {row["depth"] for row in recurrence["heading_depths"]} == {1, 2}
    assert recurrence["code_fence_languages"] == []
    assert recurrence["link_target_classes"] == {
        "internal_docs_links": 2,
        "external_links": 1,
        "broken_local_docs_links": 1,
    }


def test_recurrence_text_top_and_summary_only_controls(tmp_path, monkeypatch, capsys):
    _write(
        tmp_path / "docs" / "one.md",
        "---\na: 1\n---\n# One\n## Repeat\n```text\nx\n```\n",
    )
    _write(
        tmp_path / "docs" / "two.md",
        "---\nb: 2\n---\n# Two\n## Repeat\n## Other\n```bash\nx\n```\n",
    )
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(["--documentation-structure", "--recurrence", "--top", "1"])
        == 0
    )
    output = capsys.readouterr().out
    assert "Documentation Structure Recurrence" in output
    assert "- Repeat: 2" in output
    assert "- Other: 1" not in output
    assert "Boundary: read only; observes structural recurrence only" in output
    assert "Section skeleton signatures:" not in output

    assert (
        seed_local.main(["--documentation-structure", "--recurrence", "--summary-only"])
        == 0
    )
    summary_output = capsys.readouterr().out
    assert "total distinct entries:" in summary_output
    assert "entries at or above min_count 2:" in summary_output
    assert "entries at or above min_count 1:" in summary_output
    assert "- Repeat: 2" not in summary_output
    assert "- depth 1:" not in summary_output


def test_recurrence_distribution_rare_skeleton_missing_common_and_outlier_json(
    tmp_path, monkeypatch, capsys
):
    for index in range(25):
        extra = "## Shared\n" if index < 24 else ""
        _write(
            tmp_path / "docs" / f"common_{index:02}.md",
            f"---\nstatus: draft\n---\n# Doc {index}\n## Purpose\n{extra}",
        )
    _write(
        tmp_path / "docs" / "outlier.md",
        "# Outlier\n## UniqueA\n## UniqueB\n##### Deep\n```text\nx\n```\n```text\nx\n```\n```text\nx\n```\n```text\nx\n```\n```text\nx\n```\n",
    )
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--recurrence",
                "--rare",
                "--missing-common-sections",
                "--outliers",
                "--limit",
                "2",
                "--top",
                "2",
                "--json",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    recurrence = payload["recurrence"]
    section_buckets = {
        row["bucket"]: row["distinct_entries"]
        for row in recurrence["recurrence_distributions"]["section_labels"]
    }
    assert section_buckets["1"] >= 3
    assert section_buckets["25-99"] == 1
    rare_labels = [
        row["label"] for row in recurrence["rare_structures"]["section_labels"]
    ]
    assert len(rare_labels) == 2
    assert "Deep" in rare_labels
    assert recurrence["section_skeleton_signatures"][0]["document_count"] == 24
    assert recurrence["common_section_labels"] == [
        {"label": "Purpose", "present": 25, "missing": 1}
    ]
    assert recurrence["documents_missing_common_sections"] == [
        {
            "path": "docs/outlier.md",
            "missing_section_labels": ["Purpose"],
            "missing_count": 1,
        }
    ]
    assert recurrence["structural_outliers"][0]["path"] == "docs/outlier.md"
    signals = {
        signal["signal"] for signal in recurrence["structural_outliers"][0]["signals"]
    }
    assert "missing_front_matter" in signals
    assert "deep_heading_depth" in signals
    rendered = json.dumps(payload)
    assert "meaning" not in rendered
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_repository"] is False


def test_recurrence_summary_only_keeps_buckets_and_suppresses_items(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "one.md", "# One\n## Solo\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--recurrence",
                "--rare",
                "--outliers",
                "--summary-only",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Section label recurrence distribution:" in output
    assert "Rare structures:" in output
    assert "entries:" in output
    assert "Structural outliers:" in output
    assert "documents with structural signals:" in output
    assert "- Solo: 1" not in output


def test_recurrence_human_skeleton_signatures_are_compact_structural_visibility(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "h1_a.md", "# Repeat\n# Repeat\n# Repeat\n")
    _write(tmp_path / "docs" / "h1_b.md", "# Repeat\n# Repeat\n")
    _write(
        tmp_path / "docs" / "sections.md",
        "# Title\n## Raw Start\n## Raw Start\n### Raw Detail\n### Raw Detail\n## Raw End\n",
    )
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--recurrence", "--skeletons", "--top", "10"]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert (
        "- no H2/H3 sections: 2 docs; sections=0; max_depth=1; h1=5; h2=0; h3=0"
        in output
    )
    assert "    - h1=3: 1 docs; sections=0; max_depth=1; h2=0; h3=0" in output
    assert "    - h1=2: 1 docs; sections=0; max_depth=1; h2=0; h3=0" in output
    assert "H1|H1|H1" not in output
    assert "H2:Raw Start|H3:Raw Detail|H2:Raw End" in output
    assert "Raw Beginning" not in output
    signature_lines = output.split("Section skeleton signatures:", 1)[1].split(
        "Link target classes:", 1
    )[0]
    assert "meaning" not in signature_lines
    assert "claim" not in signature_lines
    assert "authority" not in signature_lines
    assert "ontology" not in signature_lines


def test_recurrence_human_skeleton_signatures_truncate_but_json_keeps_raw_signature(
    tmp_path, monkeypatch, capsys
):
    headings = "".join(f"## Raw {index}\n" for index in range(12))
    _write(tmp_path / "docs" / "long.md", f"# Title\n{headings}")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(["--documentation-structure", "--recurrence", "--skeletons"])
        == 0
    )

    output = capsys.readouterr().out
    assert "... +9 more" in output
    assert "H2:Raw 11" not in output

    assert (
        seed_local.main(
            ["--documentation-structure", "--recurrence", "--skeletons", "--json"]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    row = payload["recurrence"]["section_skeleton_signatures"][0]
    assert row["signature"].endswith("H2:Raw 11")
    assert "... +4 more" not in row["signature"]
    assert row["rendered_signature"].endswith("... +9 more")
    assert row["document_count"] == 1
    assert row["docs_count"] == 1
    assert row["section_count"] == 12
    assert row["max_depth"] == 2
    assert row["h1_count"] == 1
    assert row["h2_count"] == 12
    assert row["h3_count"] == 0
    assert payload["boundary"]["mutates_repository"] is False


def test_recurrence_long_skeletons_truncate_human_but_json_preserves_raw(
    tmp_path, monkeypatch, capsys
):
    headings = "\n".join(f"## Section {index}" for index in range(1, 8))
    _write(tmp_path / "docs" / "long.md", f"# Long\n{headings}\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(["--documentation-structure", "--recurrence", "--skeletons"])
        == 0
    )
    output = capsys.readouterr().out
    assert "H2:Section 1|H2:Section 2|H2:Section 3|... +4 more" in output
    assert "H2:Section 7" not in output

    assert (
        seed_local.main(
            ["--documentation-structure", "--recurrence", "--skeletons", "--json"]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    signatures = payload["recurrence"]["section_skeleton_signatures"]
    assert signatures[0]["signature"].endswith("H2:Section 7")


def test_recurrence_summary_only_skeletons_shows_totals_not_rows(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "one.md", "# One\n## Visible\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--recurrence",
                "--skeletons",
                "--summary-only",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out
    assert "Section skeleton signatures:" in output
    assert "total distinct signatures:" in output
    assert "H2:Visible" not in output


def test_section_label_drilldown_text_exact_matches_limit_summary_and_boundaries(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "alpha.md",
        "# Alpha\n\n## Purpose\nClaims recommendation similarity classification.\n\n## Purposeful\nNot exact.\n\n### Purpose\nNo claim extraction here.\n",
    )
    _write(tmp_path / "docs" / "beta.md", "# Beta\n\n## Purpose\nOntology promotion prose.\n")
    before = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--where",
                "section-label:Purpose",
                "--limit",
                "2",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    after = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    assert before == after
    assert "Documentation Structure Drilldown" in output
    assert "Category: section-label" in output
    assert "Key: Purpose" in output
    assert "Occurrences: 3" in output
    assert "Documents: 2" in output
    assert "docs/alpha.md:3 depth=2" in output
    assert "docs/alpha.md:9 depth=3" in output
    assert "docs/beta.md:3 depth=2" not in output
    assert "... +1 more" in output
    assert "Purposeful" not in output
    assert "Claims recommendation" not in output
    assert "No claim extraction" not in output
    assert "Boundary: read only; observes structural recurrence only" in output
    assert "no prose interpretation" in output
    assert "no claim extraction" in output
    assert "no authority inference" in output
    assert "no shape inference" in output
    assert "no ontology promotion" in output
    assert "no event ledger writes" in output
    assert "no repository mutation" in output

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--where",
                "section-label:Purpose",
                "--summary-only",
            ]
        )
        == 0
    )
    summary_output = capsys.readouterr().out
    assert "Occurrences: 3" in summary_output
    assert "Documents: 2" in summary_output
    assert "docs/alpha.md:3 depth=2" not in summary_output


def test_section_label_drilldown_json_exact_structural_observation_and_boundary(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "alpha.md",
        "# Alpha\n\n## Purpose\nProse says authority inference.\n\n## Purposeful\nNot exact.\n\n### Purpose\nShape inference prose.\n",
    )
    _write(tmp_path / "docs" / "beta.md", "# Beta\n\n## Purpose\nRecommend similar docs.\n")
    before = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            ["--documentation-structure", "--where", "section-label:Purpose", "--json"]
        )
        == 0
    )

    after = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    payload = json.loads(capsys.readouterr().out)
    assert before == after
    assert payload == {
        "category": "section-label",
        "key": "Purpose",
        "occurrences": 3,
        "documents": 2,
        "matches": [
            {"path": "docs/alpha.md", "line": 3, "depth": 2},
            {"path": "docs/alpha.md", "line": 9, "depth": 3},
            {"path": "docs/beta.md", "line": 3, "depth": 2},
        ],
        "boundary": {
            "read_only": True,
            "prose_interpretation": False,
            "claim_extraction": False,
            "authority_inference": False,
            "shape_inference": False,
            "ontology_promotion": False,
            "writes_event_ledger": False,
            "mutates_repository": False,
        },
    }
    rendered = json.dumps(payload)
    assert "Purposeful" not in rendered
    assert "authority inference" not in rendered
    assert "Shape inference" not in rendered
    assert "Recommend similar" not in rendered


def test_section_label_membership_exact_members_json_boundary_and_read_only(
    tmp_path, monkeypatch, capsys
):
    _write(
        tmp_path / "docs" / "alpha.md",
        "# Alpha\n\n## Purpose\nClaims recommendation similarity classification.\n\n## Purposeful\nNot exact.\n\n### Purpose\nOntology prose.\n",
    )
    _write(tmp_path / "docs" / "beta.md", "# Beta\n\n## Purpose\nShape inference prose.\n")
    _write(tmp_path / "docs" / "gamma.md", "# Gamma\n\n## Purposeful\nNot exact.\n")
    before = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--membership",
                "section-label:Purpose",
                "--json",
            ]
        )
        == 0
    )

    after = {
        p.relative_to(tmp_path).as_posix(): p.read_text(encoding="utf-8")
        for p in tmp_path.rglob("*")
        if p.is_file()
    }
    payload = json.loads(capsys.readouterr().out)
    assert before == after
    assert set(payload) == {"category", "key", "member_count", "members", "boundary"}
    assert payload["category"] == "section-label"
    assert payload["key"] == "Purpose"
    assert payload["member_count"] == 2
    assert payload["members"] == [
        {"path": "docs/alpha.md"},
        {"path": "docs/beta.md"},
    ]
    assert payload["boundary"]["exact_observed_structural_inclusion"] is True
    assert payload["boundary"]["similarity"] is False
    assert payload["boundary"]["classification"] is False
    assert payload["boundary"]["ontology_promotion"] is False
    assert payload["boundary"]["shape_inference"] is False
    assert payload["boundary"]["recommendation"] is False
    assert payload["boundary"]["prose_interpretation"] is False
    assert payload["boundary"]["writes_event_ledger"] is False
    assert payload["boundary"]["mutates_repository"] is False
    rendered = json.dumps(payload)
    assert "Purposeful" not in rendered
    assert "Claims recommendation" not in rendered
    assert "classification" in rendered.lower()
    assert "ontology" in rendered.lower()


def test_section_label_membership_human_limit_summary_and_boundary_language(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path / "docs" / "alpha.md", "# Alpha\n\n## Purpose\n")
    _write(tmp_path / "docs" / "beta.md", "# Beta\n\n## Purpose\n")
    _write(tmp_path / "docs" / "gamma.md", "# Gamma\n\n## Purposeful\n")
    monkeypatch.setattr(seed_local, "REPO_ROOT", tmp_path)

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--membership",
                "section-label:Purpose",
                "--limit",
                "1",
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "Structural Membership" in output
    assert "Category: section-label" in output
    assert "Key: Purpose" in output
    assert "Members:\n    2" in output
    assert "docs/alpha.md" in output
    assert "docs/beta.md" not in output
    assert "... +1 more" in output
    assert "Purposeful" not in output
    assert "exact observed structural inclusion" in output
    assert "no similarity" in output
    assert "no classification" in output
    assert "no ontology promotion" in output
    assert "no shape inference" in output
    assert "no recommendation" in output
    assert "no prose interpretation" in output

    assert (
        seed_local.main(
            [
                "--documentation-structure",
                "--membership",
                "section-label:Purpose",
                "--summary-only",
            ]
        )
        == 0
    )
    summary_output = capsys.readouterr().out
    assert "Members:\n    2" in summary_output
    assert "docs/alpha.md" not in summary_output
    assert "Documents:" not in summary_output


def test_documentation_structure_observes_explicit_architectural_relation_forms(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    forms = [
        ("A", "!=", "B"),
        ("A", "owns", "B"),
        ("A", "produces", "B"),
        ("A", "consumes", "B"),
        ("A", "hands off to", "B"),
        ("A", "preserves", "B"),
        ("A", "bounds", "B"),
        ("A", "derives", "B"),
        ("A", "selects", "B"),
        ("A", "explains", "B"),
        ("A", "observes", "B"),
        ("A", "does not own", "B"),
    ]
    lines = ["---", "title: Relations", "---", "# Relations"]
    lines.extend(f"{left} {relation} {right}" for left, relation, right in forms)
    (docs / "relations.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    options = DocumentationStructureOptions(
        detail_expansions=DocumentationStructureDetailExpansions(
            include_architectural_relations=True
        )
    )
    document = observe_documentation_structure(tmp_path, options).documents[0]

    observed = tuple(
        (row.left_term, row.relation, row.right_term, row.source_path, row.evidence)
        for row in document.architectural_relation_observations
    )
    assert observed == tuple(
        (left, relation, right, "docs/relations.md", f"{left} {relation} {right}")
        for left, relation, right in forms
    )
    assert document.architectural_relation_observations[0].line_number == 5


def test_documentation_structure_architectural_relations_json_and_human_output(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "relations.md").write_text(
        "---\ntitle: Relations\n---\n# Relations\nAlpha owns Beta\n",
        encoding="utf-8",
    )
    options = DocumentationStructureOptions(
        detail_expansions=DocumentationStructureDetailExpansions(
            include_architectural_relations=True
        )
    )
    report = observe_documentation_structure(tmp_path, options)

    data = documentation_structure_json(report)
    rows = data["documents"][0]["architectural_relation_observations"]
    assert rows == [
        {
            "left_term": "Alpha",
            "relation": "owns",
            "right_term": "Beta",
            "source_path": "docs/relations.md",
            "line_number": 5,
            "evidence": "Alpha owns Beta",
        }
    ]
    output = format_documentation_structure(report, options)
    assert "Architectural relations:" in output
    assert "left='Alpha' relation='owns' right='Beta'" in output


def test_documentation_structure_architectural_relation_counterexamples(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "relations.md").write_text(
        "\n".join(
            [
                "---",
                "title: Relations",
                "---",
                "# Relations",
                "In general, Alpha owns Beta when configured.",
                "Alpha might produce Beta",
                "- Alpha consumes Beta",
                "```",
                "Alpha owns Beta",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    options = DocumentationStructureOptions(
        detail_expansions=DocumentationStructureDetailExpansions(
            include_architectural_relations=True
        )
    )

    document = observe_documentation_structure(tmp_path, options).documents[0]

    assert document.architectural_relation_observations == ()
