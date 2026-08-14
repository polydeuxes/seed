from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import shutil

import pytest

from seed_runtime.ocr_witness import (
    ExactImageMaterial,
    OcrLadderStep,
    OcrWitnessAnswer,
    OcrWitnessError,
    exact_answer_classes,
    exact_answer_changes,
    invoke_ocr_witness,
    observe_ink_value_ladder,
    observe_point_size_ladder,
    output_adjacent_byte_counts,
    output_byte_counts,
    render_text_image,
)


def _answer(source: str, image: bytes, stdout: bytes) -> OcrWitnessAnswer:
    return OcrWitnessAnswer(
        source_id=source,
        image_commitment=ExactImageMaterial(source, image, "image/png").commitment,
        witness="bounded-test-witness",
        arguments=("bounded-test-witness",),
        returncode=0,
        stdout_bytes=stdout,
        stderr_bytes=b"",
        timed_out=False,
    )


def test_raw_ocr_output_is_measured_as_bytes_without_decoder_vocabulary():
    answer = _answer("image_1", b"image one", b"seed\n")

    assert output_byte_counts(answer) == {
        0x0A: 1,
        0x64: 1,
        0x65: 2,
        0x73: 1,
    }
    assert output_adjacent_byte_counts(answer) == {
        (0x64, 0x0A): 1,
        (0x65, 0x64): 1,
        (0x65, 0x65): 1,
        (0x73, 0x65): 1,
    }


def test_equal_raw_answers_do_not_identify_equal_image_sources():
    first = _answer("image_1", b"image one", b"same\n")
    second = _answer("image_2", b"image two", b"same\n")

    assert first.stdout_bytes == second.stdout_bytes
    assert first.image_commitment != second.image_commitment
    assert first.source_id != second.source_id
    assert first.establishes_reading_accuracy is False
    assert second.establishes_image_content is False


def test_adjacent_answer_changes_are_recovered_without_naming_what_changed():
    images = (
        ExactImageMaterial("size_1", b"image one", "image/png"),
        ExactImageMaterial("size_2", b"image two", "image/png"),
        ExactImageMaterial("size_3", b"image three", "image/png"),
    )
    steps = tuple(
        OcrLadderStep(size, image, _answer(image.source_id, image.exact_bytes, stdout))
        for size, image, stdout in zip((1, 2, 3), images, (b"", b"", b"x\n"))
    )

    changes = exact_answer_changes(steps)

    assert [(item.left_coordinate, item.right_coordinate) for item in changes] == [
        (2, 3)
    ]
    assert exact_answer_classes(steps) == ((1, 2), (3,))


def test_answer_commitment_changes_when_stderr_or_status_changes():
    exact = _answer("image", b"image", b"x\n")

    assert replace(exact, stderr_bytes=b"warning").answer_commitment != exact.answer_commitment
    assert replace(exact, returncode=1).answer_commitment != exact.answer_commitment


def test_point_size_coordinates_must_be_positive_distinct_and_ascending():
    for values in ((), (0,), (2, 1), (1, 1), (1, "2")):
        with pytest.raises(OcrWitnessError, match="point sizes"):
            observe_point_size_ladder("seed", values)


def test_ink_values_must_be_distinct_ascending_bytes():
    for values in ((), (-1,), (256,), (2, 1), (1, 1), (1, "2")):
        with pytest.raises(OcrWitnessError, match="ink values"):
            observe_ink_value_ladder("seed", values)


def test_ocr_witness_source_contains_no_text_decoder(tmp_path):
    source = Path(__file__).resolve().parents[1] / "seed_runtime/ocr_witness.py"
    material = source.read_text(encoding="utf-8")

    assert ".decode(" not in material
    assert "represented_text" not in material
    assert "closing_punctuation" not in material


@pytest.mark.skipif(
    shutil.which("convert") is None or shutil.which("tesseract") is None,
    reason="live image renderer and OCR witness are unavailable",
)
def test_live_witness_receives_exact_images_and_returns_only_raw_answers():
    image = render_text_image(source_id="seed_32", supplied_text="seed", point_size=32)
    answer = invoke_ocr_witness(image)

    assert image.exact_bytes.startswith(b"\x89PNG\r\n\x1a\n")
    assert answer.image_commitment == image.commitment
    assert answer.returncode == 0
    assert answer.stdout_bytes
    assert type(answer.stdout_bytes) is bytes
    assert type(answer.stderr_bytes) is bytes
    assert answer.establishes_reading_accuracy is False
    assert answer.establishes_image_content is False


@pytest.mark.skipif(
    shutil.which("convert") is None or shutil.which("tesseract") is None,
    reason="live image renderer and OCR witness are unavailable",
)
def test_live_point_size_ladder_exposes_raw_answer_changes():
    steps = observe_point_size_ladder("seed", (4, 6, 8, 12, 18, 24, 32, 48))

    assert len({step.image.commitment for step in steps}) == len(steps)
    assert all(step.answer.image_commitment == step.image.commitment for step in steps)
    assert exact_answer_changes(steps)


@pytest.mark.skipif(
    shutil.which("convert") is None or shutil.which("tesseract") is None,
    reason="live image renderer and OCR witness are unavailable",
)
def test_live_ink_value_ladder_exposes_raw_answer_changes():
    steps = observe_ink_value_ladder("seed", (0, 64, 128, 192, 224, 240, 248, 252, 255))

    assert len({step.image.commitment for step in steps}) == len(steps)
    assert exact_answer_changes(steps)
