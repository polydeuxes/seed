from __future__ import annotations

import json
import os
from pathlib import Path
import sys

import pytest

from seed_runtime.grammar_change import (
    GrammarChangeError,
    apply_grammar_creation,
    apply_grammar_change,
    observe_grammar,
    propose_grammar_change,
    propose_grammar_creation,
    run_grammar_check,
)


def _repository(tmp_path: Path) -> Path:
    root = tmp_path / "seed-repository"
    grammar = root / "book_of_seed" / "grammar.json"
    grammar.parent.mkdir(parents=True)
    grammar.write_text(
        json.dumps({"structural_edges": {"locality": {"from": "a", "to": "b"}}})
        + "\n",
        encoding="utf-8",
    )
    (root / "check.py").write_text(
        "import json\n"
        "g=json.load(open('book_of_seed/grammar.json', encoding='utf-8'))\n"
        "raise SystemExit(0 if 'yield' in g['structural_edges'] else 9)\n",
        encoding="utf-8",
    )
    return root


def test_current_and_proposed_grammar_remain_distinct_until_exact_replacement(tmp_path):
    root = _repository(tmp_path)
    current = observe_grammar(root)
    proposed = (
        json.dumps(
            {
                "structural_edges": {
                    "locality": {"from": "a", "to": "b"},
                    "yield": {"from": "occurrence", "to": "result"},
                }
            },
            indent=2,
        )
        + "\n"
    ).encode()

    change = propose_grammar_change(current, proposed)
    assert current.material != proposed
    assert (root / current.relative_path).read_bytes() == current.material
    assert "yield" in change.difference

    applied = apply_grammar_change(root, change)
    checked = run_grammar_check(root, (sys.executable, "check.py"))
    assert applied.before == current.identity
    assert (root / current.relative_path).read_bytes() == proposed
    assert checked.returncode == 0


def test_stale_current_grammar_cannot_replace_newer_material(tmp_path):
    root = _repository(tmp_path)
    current = observe_grammar(root)
    change = propose_grammar_change(current, b'{"structural_edges": {}}\n')
    grammar_path = root / current.relative_path
    grammar_path.write_text('{"structural_edges": {"participation": {}}}\n')

    with pytest.raises(GrammarChangeError, match="changed after observation"):
        apply_grammar_change(root, change)


@pytest.mark.parametrize(
    "material",
    [b"not json", b"[]", b'"text"', b"\xff"],
)
def test_malformed_proposed_grammar_is_refused_before_source_changes(tmp_path, material):
    root = _repository(tmp_path)
    current = observe_grammar(root)

    with pytest.raises(GrammarChangeError, match="UTF-8 JSON object"):
        propose_grammar_change(current, material)
    assert (root / current.relative_path).read_bytes() == current.material


def test_an_external_repository_can_acquire_its_first_machine_grammar(tmp_path):
    root = tmp_path / "other-repository"
    (root / "machine").mkdir(parents=True)
    (root / "check.py").write_text(
        "import json\n"
        "g=json.load(open('machine/grammar.json', encoding='utf-8'))\n"
        "raise SystemExit(0 if g.get('checks') == [['python', '-m', 'pytest']] else 8)\n",
        encoding="utf-8",
    )
    proposed = b'{"checks": [["python", "-m", "pytest"]]}\n'

    creation = propose_grammar_creation(
        root,
        proposed,
        relative_path="machine/grammar.json",
    )
    assert not (root / "machine/grammar.json").exists()
    assert creation.difference.startswith("--- /dev/null\n+++ b/machine/grammar.json\n")

    observed = apply_grammar_creation(root, creation)
    checked = run_grammar_check(root, (sys.executable, "check.py"))
    assert observed.material == proposed
    assert checked.returncode == 0


def test_grammar_creation_never_overwrites_a_path_that_appeared_later(tmp_path):
    root = tmp_path / "other-repository"
    (root / "machine").mkdir(parents=True)
    creation = propose_grammar_creation(
        root,
        b'{"checks": []}\n',
        relative_path="machine/grammar.json",
    )
    destination = root / "machine/grammar.json"
    destination.write_bytes(b'{"newer": true}\n')

    with pytest.raises(GrammarChangeError, match="already exists"):
        apply_grammar_creation(root, creation)
    assert destination.read_bytes() == b'{"newer": true}\n'


def test_grammar_creation_closes_the_last_moment_overwrite_race(
    tmp_path, monkeypatch
):
    root = tmp_path / "other-repository"
    (root / "machine").mkdir(parents=True)
    creation = propose_grammar_creation(
        root,
        b'{"checks": []}\n',
        relative_path="machine/grammar.json",
    )
    destination = root / "machine/grammar.json"
    real_link = os.link

    def competing_creation(source, target, **kwargs):
        destination.write_bytes(b'{"competing": true}\n')
        return real_link(source, target, **kwargs)

    monkeypatch.setattr("seed_runtime.grammar_change.os.link", competing_creation)
    with pytest.raises(GrammarChangeError, match="appeared after observation"):
        apply_grammar_creation(root, creation)
    assert destination.read_bytes() == b'{"competing": true}\n'


def test_grammar_creation_refuses_a_symbolic_link_parent(tmp_path):
    root = tmp_path / "other-repository"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "machine").symlink_to(outside, target_is_directory=True)

    with pytest.raises(GrammarChangeError, match="symbolic link"):
        propose_grammar_creation(
            root,
            b'{"checks": []}\n',
            relative_path="machine/grammar.json",
        )
