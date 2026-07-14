"""Campaign-local scaffold for Graded Lessons supervised grammar apprenticeship 001.

This module preserves bounded external material and caller-supplied testimony. It
intentionally performs no English interpretation.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
from typing import Any

from seed_runtime.candidate_external_grammar import (
    CandidateExternalGrammarInput,
    assemble_candidate_external_grammar_set,
    candidate_external_grammar_json,
    format_candidate_external_grammar,
)

CAMPAIGN_DIR = Path(__file__).parent
SELECTED_LESSON = CAMPAIGN_DIR / "selected_lesson_006.txt"
EXPECTED_SHA256 = "01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"
EXPECTED_BYTE_LENGTH = 1628


@dataclass(frozen=True)
class SourceArtifactIdentity:
    reported_title: str
    reported_creator: str
    source_url_or_archive_identity: str
    acquisition_method: str
    acquired_at: str
    content_type: str
    encoding: str
    byte_length: int
    sha256: str
    reported_edition_or_transcription: str
    edition_relationship_unknowns: tuple[str, ...]
    raw_artifact_location: str


@dataclass(frozen=True)
class LessonSelection:
    parent_source_sha256: str
    selection_method: str
    exact_bounds: str
    heading_context: str
    selected_text: str
    selector_attribution: str
    selection_unknowns: tuple[str, ...]


@dataclass(frozen=True)
class MaterialAnnotation:
    annotation_id: str
    material_reference: str
    annotation_kind: str
    bounded_annotation: str
    supplied_by: str
    unknowns: tuple[str, ...]


@dataclass(frozen=True)
class SupervisionStep:
    step_id: str
    material_reference: str
    operation: str
    supplied_by: str
    bounded_output: str
    uncertainty: str
    explicitly_refused_claims: tuple[str, ...]


def selected_lesson_bytes() -> bytes:
    return SELECTED_LESSON.read_bytes()


def source_identity() -> SourceArtifactIdentity:
    data = selected_lesson_bytes()
    digest = sha256(data).hexdigest()
    return SourceArtifactIdentity(
        reported_title="Graded Lessons in English",
        reported_creator="Alonzo Reed and Brainerd Kellogg",
        source_url_or_archive_identity="Project Gutenberg eBook #7010 plain text; https://www.gutenberg.org/ebooks/7010.txt.utf-8 redirected to http://www.gutenberg.org/cache/epub/7010/pg7010.txt",
        acquisition_method="operator used the repository environment's web retrieval surface to inspect Project Gutenberg metadata and copied one bounded lesson excerpt without alteration into the campaign artifact",
        acquired_at="2026-07-14T00:00:00Z",
        content_type="text/plain selected excerpt from Project Gutenberg plain-text transcription",
        encoding="UTF-8",
        byte_length=len(data),
        sha256=digest,
        reported_edition_or_transcription="Project Gutenberg eBook #7010; produced by Karl Hagen, Charles Franks, and the Online Distributed Proofreading Team; release date December 1, 2004; most recently updated December 30, 2020; revised edition, 1896 reported in text",
        edition_relationship_unknowns=(
            "The full parent plain-text artifact was not committed.",
            "The campaign preserves the selected excerpt hash, not a full-book byte hash.",
        ),
        raw_artifact_location=str(SELECTED_LESSON),
    )


def validate_source_identity() -> SourceArtifactIdentity:
    identity = source_identity()
    if identity.sha256 != EXPECTED_SHA256:
        raise AssertionError(identity.sha256)
    if identity.byte_length != EXPECTED_BYTE_LENGTH:
        raise AssertionError(identity.byte_length)
    return identity


def lesson_selection() -> LessonSelection:
    text = selected_lesson_bytes().decode("utf-8")
    return LessonSelection(
        parent_source_sha256=EXPECTED_SHA256,
        selection_method="campaign author selected Project Gutenberg rendered plain-text lines corresponding to LESSON 6 from the externally supplied transcription",
        exact_bounds="selected_lesson_006.txt lines 1-4; Project Gutenberg web-rendered text lines 59-62 in the retrieval view",
        heading_context="LESSON 6. ANALYSIS.",
        selected_text=text,
        selector_attribution="campaign author supplied",
        selection_unknowns=(
            "Full parent-artifact byte offsets were not available in the repository environment.",
            "The line numbers are retrieval-view line numbers, not canonical Project Gutenberg file line numbers.",
        ),
    )


def annotations() -> tuple[MaterialAnnotation, ...]:
    return (
        MaterialAnnotation("ann_rule_subject", "selected_lesson_006.txt:L2:sentences 13-15", "candidate_rule_statement", "campaign author reports that the span appears to define Subject.", "campaign author supplied", ("Correctness of the interpretation is not established.",)),
        MaterialAnnotation("ann_rule_predicate_analysis", "selected_lesson_006.txt:L3:sentences 1-2", "candidate_rule_statement", "campaign author reports that the span appears to define Predicate and Analysis.", "campaign author supplied", ("Correctness of the interpretation is not established.",)),
        MaterialAnnotation("ann_model_intemperance", "selected_lesson_006.txt:L1-L2:Model Intemperance degrades exchange", "candidate_example", "campaign author reports that the span appears to present a labeled model example.", "campaign author supplied", ("Seed does not decide whether the model is grammatically correct.",)),
        MaterialAnnotation("ann_model_stars", "selected_lesson_006.txt:L3:Model Stars twinkle explanation", "candidate_example", "campaign author reports that the span appears to present a second labeled model example.", "campaign author supplied", ("Seed does not compare it autonomously with the first model.",)),
        MaterialAnnotation("ann_exercise_numbered", "selected_lesson_006.txt:L2:numbered items 1-12 and L4:numbered items 1-12", "candidate_exercise_instruction", "campaign author reports that the numbered sentence lists appear to request analysis by the model.", "campaign author supplied", ("The exercise purpose is human testimony, not Seed inference.",)),
        MaterialAnnotation("ann_label_subject_predicate", "selected_lesson_006.txt:L2:terms _+Subject+_ and _+Predicate+_", "candidate_label", "campaign author reports that the highlighted terms appear to label grammatical categories.", "campaign author supplied", ("Label/category relationship remains Unknown.",)),
        MaterialAnnotation("ann_ambiguous_models", "selected_lesson_006.txt:L1-L3:two +Model+ spans", "unknown", "campaign author reports uncertainty whether the two model spans are complementary examples or a repeated teaching pattern.", "campaign author supplied", ("Seed preserves the ambiguity without resolving it.",)),
    )


def candidate_input() -> CandidateExternalGrammarInput:
    return CandidateExternalGrammarInput.from_json_dict({
        "representation_scope": "Supervised structural candidates over Graded Lessons campaign 001 selected lesson; caller-supplied testimony only.",
        "set_unknowns": [
            "Seed has not read, understood, or verified English grammar from the lesson.",
            "String testimony references are not schema-bound to source offsets.",
        ],
        "candidates": [
            {
                "candidate_id": "gl001_pair_label_example",
                "structural_claim": "The lesson may pair highlighted category labels with model sentences and explanations.",
                "claim_scope": "selected_lesson_006 only",
                "provenance": ["source:gl001:selected_lesson_006@sha256:01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"],
                "supporting_testimony": ["source:gl001:selected_lesson_006:L1-L3#ann_model_intemperance", "source:gl001:selected_lesson_006:L2#ann_label_subject_predicate", "source:gl001:selected_lesson_006:L3#ann_model_stars"],
                "contradicting_testimony": [],
                "unresolved_alternatives": ["The highlighted terms may be presentation emphasis rather than structural category labels."],
                "explicit_unknowns": ["Seed does not know whether the labels are correct grammar categories."],
            },
            {
                "candidate_id": "gl001_repeated_two_part_structure",
                "structural_claim": "The lesson may present sentences as divisible into two named parts before asking for repeated analysis.",
                "claim_scope": "selected_lesson_006 only",
                "provenance": ["source:gl001:selected_lesson_006@sha256:01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"],
                "supporting_testimony": ["source:gl001:selected_lesson_006:L2#ann_rule_subject", "source:gl001:selected_lesson_006:L3#ann_rule_predicate_analysis", "source:gl001:selected_lesson_006:L4#ann_exercise_numbered"],
                "contradicting_testimony": ["source:gl001:selected_lesson_006:L1-L3#ann_ambiguous_models"],
                "unresolved_alternatives": ["The lesson may be a classroom script rather than a formal structural grammar candidate."],
                "explicit_unknowns": ["Relationship between printed labels and sentence roles remains Unknown."],
            },
            {
                "candidate_id": "gl001_model_then_exercise",
                "structural_claim": "The lesson may use a model-then-exercise pattern: labeled model explanation followed by numbered items.",
                "claim_scope": "selected_lesson_006 only",
                "provenance": ["source:gl001:selected_lesson_006@sha256:01af0782acb7d945a2c97e5916168790ccf204a99cbc96eca6c5b2a3e6d7b963"],
                "supporting_testimony": ["source:gl001:selected_lesson_006:L1-L2#ann_model_intemperance", "source:gl001:selected_lesson_006:L3#ann_model_stars", "source:gl001:selected_lesson_006:L2,L4#ann_exercise_numbered"],
                "contradicting_testimony": [],
                "unresolved_alternatives": ["The numbered lists may be examples, exercises, or both."],
                "explicit_unknowns": ["Seed does not infer instructional intent."],
            },
        ],
    })


def candidate_outputs() -> dict[str, Any]:
    artifact = assemble_candidate_external_grammar_set(candidate_input())
    return {"human": format_candidate_external_grammar(artifact), "json": candidate_external_grammar_json(artifact)}


def supervision_trace() -> tuple[SupervisionStep, ...]:
    return (
        SupervisionStep("preserve_hash", "selected_lesson_006.txt", "hash source bytes", "observer or import scaffold supplied", EXPECTED_SHA256, "none for selected artifact bytes", ("Seed interpreted the prose",)),
        SupervisionStep("preserve_bounds", "selected_lesson_006.txt:L1-L4", "preserve line boundaries", "observer or import scaffold supplied", "four UTF-8 text lines retained", "parent byte offsets Unknown", ("Seed selected the pedagogically relevant lesson",)),
        SupervisionStep("annotate_rule", "selected_lesson_006.txt:L2-L3", "this span appears to state a rule", "campaign author supplied", "ann_rule_subject; ann_rule_predicate_analysis", "human interpretation", ("Seed verified the rule",)),
        SupervisionStep("annotate_examples", "selected_lesson_006.txt:L1-L3", "this span appears to be an example", "campaign author supplied", "ann_model_intemperance; ann_model_stars", "human interpretation", ("Seed classified examples autonomously",)),
        SupervisionStep("render_candidates", "CandidateExternalGrammarInput", "render caller-supplied structures", "Seed supplied", "deterministic human and JSON candidate output", "strings preserved but not bound by schema", ("Seed ranked, verified, or promoted a candidate",)),
    )


def campaign_record() -> dict[str, Any]:
    validate_source_identity()
    return {
        "source_identity": asdict(source_identity()),
        "lesson_selection": asdict(lesson_selection()),
        "annotations": [asdict(a) for a in annotations()],
        "supervision_trace": [asdict(s) for s in supervision_trace()],
        "candidate_input": {
            "representation_scope": candidate_input().representation_scope,
            "set_unknowns": list(candidate_input().set_unknowns),
            "candidates": [c.to_json_dict() for c in candidate_input().candidates],
        },
        "candidate_output": candidate_outputs(),
    }
