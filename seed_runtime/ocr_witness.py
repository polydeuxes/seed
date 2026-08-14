"""Interrogate an OCR program with exact image bytes and preserve raw answers.

The OCR program is a witness.  Its exit status, stdout bytes, and stderr bytes
are the complete answer observed here.  No decoder is inserted after it, and
no returned byte is treated as a character, word, sentence, story, or accurate
reading of the image.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
import subprocess
from typing import Iterable


class OcrWitnessError(ValueError):
    """The exact image material or witness invocation is malformed."""


@dataclass(frozen=True)
class ExactImageMaterial:
    """One exact image byte source supplied to an OCR witness."""

    source_id: str
    exact_bytes: bytes
    media_type: str

    def __post_init__(self) -> None:
        if (
            type(self.source_id) is not str
            or not self.source_id
            or type(self.exact_bytes) is not bytes
            or not self.exact_bytes
            or type(self.media_type) is not str
            or not self.media_type
        ):
            raise OcrWitnessError("malformed exact image material")

    @property
    def commitment(self) -> str:
        return sha256(self.exact_bytes).hexdigest()


@dataclass(frozen=True)
class OcrWitnessAnswer:
    """The exact raw answer from one OCR invocation over one image source."""

    source_id: str
    image_commitment: str
    witness: str
    arguments: tuple[str, ...]
    returncode: int
    stdout_bytes: bytes
    stderr_bytes: bytes
    timed_out: bool
    establishes_reading_accuracy: bool = False
    establishes_image_content: bool = False

    @property
    def answer_commitment(self) -> str:
        material = (
            self.returncode.to_bytes(8, "big", signed=True)
            + len(self.stdout_bytes).to_bytes(8, "big")
            + self.stdout_bytes
            + self.stderr_bytes
        )
        return sha256(material).hexdigest()


@dataclass(frozen=True)
class OcrAnswerChange:
    """Two adjacent supplied coordinates at which the raw witness answer differs."""

    left_coordinate: int
    right_coordinate: int
    left_source_id: str
    right_source_id: str
    left_answer_commitment: str
    right_answer_commitment: str


@dataclass(frozen=True)
class OcrLadderStep:
    """One exact supplied coordinate, image material, and raw witness answer."""

    coordinate: int
    image: ExactImageMaterial
    answer: OcrWitnessAnswer


def render_text_image(
    *,
    source_id: str,
    supplied_text: str,
    point_size: int,
    width: int = 240,
    height: int = 96,
    ink_value: int = 0,
    renderer: str = "convert",
) -> ExactImageMaterial:
    """Render one exact PNG specimen; the supplied text is construction input."""

    if (
        type(supplied_text) is not str
        or not supplied_text
        or type(point_size) is not int
        or point_size <= 0
        or type(width) is not int
        or width <= 0
        or type(height) is not int
        or height <= 0
        or type(ink_value) is not int
        or not 0 <= ink_value <= 255
    ):
        raise OcrWitnessError("image rendering requires exact positive coordinates")
    command = (
        renderer,
        "-size",
        f"{width}x{height}",
        "xc:white",
        "-fill",
        f"#{ink_value:02x}{ink_value:02x}{ink_value:02x}",
        "-font",
        "DejaVu-Sans",
        "-pointsize",
        str(point_size),
        "-gravity",
        "center",
        "-annotate",
        "+0+0",
        supplied_text,
        "png:-",
    )
    completed = subprocess.run(command, capture_output=True, check=False)
    if completed.returncode != 0 or not completed.stdout:
        raise OcrWitnessError(
            f"image renderer refused the supplied coordinates: {completed.stderr!r}"
        )
    return ExactImageMaterial(source_id, completed.stdout, "image/png")


def invoke_ocr_witness(
    image: ExactImageMaterial,
    *,
    witness: str = "tesseract",
    page_segmentation_mode: int = 10,
    language: str = "eng",
    timeout_seconds: float = 30.0,
) -> OcrWitnessAnswer:
    """Hand exact image bytes to one OCR process and preserve its raw answer."""

    if (
        type(page_segmentation_mode) is not int
        or page_segmentation_mode < 0
        or type(language) is not str
        or not language
        or type(timeout_seconds) not in (int, float)
        or timeout_seconds <= 0
    ):
        raise OcrWitnessError("OCR invocation requires exact bounded coordinates")
    arguments = (
        witness,
        "stdin",
        "stdout",
        "--psm",
        str(page_segmentation_mode),
        "-l",
        language,
    )
    try:
        completed = subprocess.run(
            arguments,
            input=image.exact_bytes,
            capture_output=True,
            check=False,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return OcrWitnessAnswer(
            source_id=image.source_id,
            image_commitment=image.commitment,
            witness=witness,
            arguments=arguments,
            returncode=-1,
            stdout_bytes=exc.stdout or b"",
            stderr_bytes=exc.stderr or b"",
            timed_out=True,
        )
    except FileNotFoundError as exc:
        raise OcrWitnessError(f"OCR witness is unavailable: {witness}") from exc
    return OcrWitnessAnswer(
        source_id=image.source_id,
        image_commitment=image.commitment,
        witness=witness,
        arguments=arguments,
        returncode=completed.returncode,
        stdout_bytes=completed.stdout,
        stderr_bytes=completed.stderr,
        timed_out=False,
    )


def observe_point_size_ladder(
    supplied_text: str,
    point_sizes: Iterable[int],
    *,
    renderer: str = "convert",
    witness: str = "tesseract",
) -> tuple[OcrLadderStep, ...]:
    """Vary only supplied point size and retain each exact raw OCR answer."""

    sizes = tuple(point_sizes)
    if (
        not sizes
        or any(type(size) is not int or size <= 0 for size in sizes)
        or tuple(sorted(set(sizes))) != sizes
    ):
        raise OcrWitnessError("point sizes must be distinct positive ascending values")
    steps = []
    for size in sizes:
        image = render_text_image(
            source_id=f"point_size_{size}",
            supplied_text=supplied_text,
            point_size=size,
            renderer=renderer,
        )
        steps.append(
            OcrLadderStep(
                coordinate=size,
                image=image,
                answer=invoke_ocr_witness(image, witness=witness),
            )
        )
    return tuple(steps)


def observe_ink_value_ladder(
    supplied_text: str,
    ink_values: Iterable[int],
    *,
    point_size: int = 32,
    renderer: str = "convert",
    witness: str = "tesseract",
) -> tuple[OcrLadderStep, ...]:
    """Vary only supplied foreground pixel value and retain raw OCR answers."""

    values = tuple(ink_values)
    if (
        not values
        or any(type(value) is not int or not 0 <= value <= 255 for value in values)
        or tuple(sorted(set(values))) != values
    ):
        raise OcrWitnessError("ink values must be distinct ascending bytes")
    steps = []
    for value in values:
        image = render_text_image(
            source_id=f"ink_value_{value}",
            supplied_text=supplied_text,
            point_size=point_size,
            ink_value=value,
            renderer=renderer,
        )
        steps.append(
            OcrLadderStep(
                coordinate=value,
                image=image,
                answer=invoke_ocr_witness(image, witness=witness),
            )
        )
    return tuple(steps)


def exact_answer_changes(steps: Iterable[OcrLadderStep]) -> tuple[OcrAnswerChange, ...]:
    """Return only adjacent supplied coordinates carrying different raw answers."""

    exact_steps = tuple(steps)
    changes = []
    for left, right in zip(exact_steps, exact_steps[1:]):
        if left.answer.answer_commitment == right.answer.answer_commitment:
            continue
        changes.append(
            OcrAnswerChange(
                left_coordinate=left.coordinate,
                right_coordinate=right.coordinate,
                left_source_id=left.image.source_id,
                right_source_id=right.image.source_id,
                left_answer_commitment=left.answer.answer_commitment,
                right_answer_commitment=right.answer.answer_commitment,
            )
        )
    return tuple(changes)


def exact_answer_classes(
    steps: Iterable[OcrLadderStep],
) -> tuple[tuple[int, ...], ...]:
    """Group supplied coordinates only where the raw witness answers are equal."""

    grouped: dict[str, list[int]] = {}
    for step in steps:
        grouped.setdefault(step.answer.answer_commitment, []).append(step.coordinate)
    return tuple(tuple(coordinates) for coordinates in grouped.values())


def output_byte_counts(answer: OcrWitnessAnswer) -> dict[int, int]:
    """Count raw stdout byte values without interpreting them."""

    return dict(sorted(Counter(answer.stdout_bytes).items()))


def output_adjacent_byte_counts(answer: OcrWitnessAnswer) -> dict[tuple[int, int], int]:
    """Count exact ordered adjacent stdout byte pairs without decoding."""

    return dict(sorted(Counter(zip(answer.stdout_bytes, answer.stdout_bytes[1:])).items()))
