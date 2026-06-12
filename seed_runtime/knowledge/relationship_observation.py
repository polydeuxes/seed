"""Deterministic Relationship Observation v0 Python import adapter.

``RelationshipFact`` is the language-neutral relationship evidence record.
Python import extraction is the first adapter that emits that record. This v0
adapter supports only static Python ``import`` and ``from ... import ...``
syntax from caller-provided source text.

Import relationships are dependency/name-availability evidence only. They do
not prove behavior, calls, routes, boundaries, or ownership. This module never
reads files, scans repositories, imports repository modules, uses LLMs,
reconciles claims, builds graphs, or integrates with runtime/tool execution.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import posixpath


IMPORTS = "imports"
DEPENDS_ON = "depends_on"
RELATED_TO = "related_to"
BELONGS_TO_DOMAIN = "belongs_to_domain"
DEFINES = "defines"

_DOCUMENT_RELATIONSHIP_KINDS = frozenset({DEPENDS_ON, RELATED_TO})


@dataclass(frozen=True)
class RelationshipFact:
    relationship_kind: str
    subject: str
    object: str
    path: str
    evidence: str


def documentation_navigation_relationship_facts(
    source_path: str,
    *,
    domain: str | None = None,
    defines: tuple[str, ...] = (),
    depends_on: tuple[str, ...] = (),
    related: tuple[str, ...] = (),
) -> list[RelationshipFact]:
    """Build relationship facts from authored documentation navigation metadata.

    The caller supplies metadata already observed from YAML front matter. This
    helper does not read files, inspect prose, infer concepts, or reconcile the
    documentation graph with repository relationships. It only maps explicit
    metadata fields to relationship facts using stable document, domain, and
    concept identities.
    """

    subject = _document_identity(source_path)
    facts: list[RelationshipFact] = []

    for target in depends_on:
        facts.append(
            _documentation_relationship_fact(
                source_path, subject, DEPENDS_ON, target, object_kind="document"
            )
        )
    for target in related:
        facts.append(
            _documentation_relationship_fact(
                source_path, subject, RELATED_TO, target, object_kind="document"
            )
        )
    if domain:
        facts.append(
            _documentation_relationship_fact(
                source_path, subject, BELONGS_TO_DOMAIN, domain, object_kind="domain"
            )
        )
    for concept in defines:
        facts.append(
            _documentation_relationship_fact(
                source_path, subject, DEFINES, concept, object_kind="concept"
            )
        )

    return facts


def _documentation_relationship_fact(
    source_path: str,
    subject: str,
    relationship_kind: str,
    value: str,
    *,
    object_kind: str,
) -> RelationshipFact:
    relationship_object = (
        _document_reference_identity(source_path, value)
        if relationship_kind in _DOCUMENT_RELATIONSHIP_KINDS
        else value
    )
    return RelationshipFact(
        relationship_kind=relationship_kind,
        subject=subject,
        object=relationship_object,
        path=source_path,
        evidence=(
            f"{subject} {relationship_kind} {object_kind} "
            f"{relationship_object}."
        ),
    )


def _document_identity(source_path: str) -> str:
    return posixpath.normpath(source_path.replace("\\", "/")).lstrip("./")


def _document_reference_identity(source_path: str, reference: str) -> str:
    reference = reference.replace("\\", "/").strip()
    if _is_absolute_or_uri_reference(reference):
        return posixpath.normpath(reference).lstrip("/")
    source_dir = posixpath.dirname(_document_identity(source_path))
    if not source_dir:
        return posixpath.normpath(reference).lstrip("./")
    return posixpath.normpath(posixpath.join(source_dir, reference)).lstrip("./")


def _is_absolute_or_uri_reference(reference: str) -> bool:
    return reference.startswith("/") or "://" in reference


def extract_python_import_relationship_facts(
    source_path: str,
    text: str,
) -> list[RelationshipFact]:
    """Extract v0 static Python import relationships from supplied source text.

    This is the first Relationship Observation adapter. It emits only
    ``imports`` relationships observed from Python ``import`` and ``from ...
    import ...`` syntax. Invalid Python returns an empty relationship list.
    """

    try:
        tree = ast.parse(text, filename=source_path)
    except SyntaxError:
        return []

    subject = _subject_from_path(source_path)
    facts: list[RelationshipFact] = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            facts.extend(_import_relationships(source_path, subject, node))
        elif isinstance(node, ast.ImportFrom):
            facts.extend(_import_from_relationships(source_path, subject, node))
    return facts


def extract_relationship_facts(source_path: str, text: str) -> list[RelationshipFact]:
    """Compatibility wrapper for the v0 Python import relationship adapter.

    This name is not a general relationship extractor. It delegates to
    ``extract_python_import_relationship_facts`` and therefore supports only
    static Python import relationships.
    """

    return extract_python_import_relationship_facts(source_path, text)


def _import_relationships(
    source_path: str,
    subject: str,
    node: ast.Import,
) -> list[RelationshipFact]:
    return [
        RelationshipFact(
            relationship_kind=IMPORTS,
            subject=subject,
            object=alias.name,
            path=source_path,
            evidence=f"{subject} imports {alias.name}.",
        )
        for alias in node.names
    ]


def _import_from_relationships(
    source_path: str,
    subject: str,
    node: ast.ImportFrom,
) -> list[RelationshipFact]:
    module = _import_from_module(node)
    return [
        RelationshipFact(
            relationship_kind=IMPORTS,
            subject=subject,
            object=alias.name,
            path=source_path,
            evidence=_import_from_evidence(subject, module, alias.name),
        )
        for alias in node.names
    ]


def _import_from_module(node: ast.ImportFrom) -> str:
    relative_prefix = "." * node.level
    return f"{relative_prefix}{node.module or ''}"


def _import_from_evidence(subject: str, module: str, name: str) -> str:
    if not module:
        return f"{subject} imports {name}."
    return f"{subject} imports {name} from {module}."


def _subject_from_path(source_path: str) -> str:
    subject = source_path.removesuffix(".py")
    subject = subject.replace("\\", "/").strip("/")
    while subject.startswith("./"):
        subject = subject[2:]
    subject = subject.replace("/", ".")
    if subject.endswith(".__init__"):
        subject = subject[: -len(".__init__")]
    return subject or source_path
