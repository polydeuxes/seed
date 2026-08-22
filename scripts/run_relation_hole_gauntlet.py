"""Run every pytest source independently through the relation-hole observer.

Each file has its own time boundary and artifact.  One slow population therefore
cannot erase completed observations or prevent later populations from running.
This runner does not load implementation-measurement admission: it records
ordinary implementation testimony and does not classify pytest occurrences as
Seed occurrences.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
import os
from pathlib import Path
import signal
import subprocess
import time


OUTPUT_ENVIRONMENT_COORDINATE = "SEED_RELATION_HOLE_OBSERVATION"


def _slug(path: Path) -> str:
    return path.as_posix().replace("/", "__").removesuffix(".py")


def _digest(path: Path) -> str | None:
    if not path.exists():
        return None
    return sha256(path.read_bytes()).hexdigest()


def _run_one(
    repository: Path,
    source: Path,
    output_directory: Path,
    time_limit_seconds: float,
) -> dict[str, object]:
    slug = _slug(source)
    artifact = output_directory / f"{slug}.json"
    log = output_directory / f"{slug}.log"
    environment = os.environ.copy()
    environment[OUTPUT_ENVIRONMENT_COORDINATE] = str(artifact)
    command = (
        str(repository / ".venv/bin/pytest"),
        "-q",
        "-p",
        "scripts.observe_relation_holes",
        source.as_posix(),
    )
    started = time.monotonic()
    with log.open("wb") as output:
        process = subprocess.Popen(
            command,
            cwd=repository,
            env=environment,
            stdout=output,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        status = "completed"
        try:
            returncode = process.wait(timeout=time_limit_seconds)
        except subprocess.TimeoutExpired:
            status = "time_limit_reached"
            os.killpg(process.pid, signal.SIGINT)
            try:
                returncode = process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                returncode = process.wait()
    elapsed = time.monotonic() - started
    return {
        "source": source.as_posix(),
        "status": status,
        "returncode": returncode,
        "wall_time_seconds": round(elapsed, 6),
        "artifact": artifact.as_posix() if artifact.exists() else None,
        "artifact_byte_count": artifact.stat().st_size if artifact.exists() else 0,
        "artifact_digest": _digest(artifact),
        "log": log.as_posix(),
        "log_byte_count": log.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--time-limit-seconds", type=float, default=60.0)
    parser.add_argument("sources", nargs="*", type=Path)
    arguments = parser.parse_args()
    if arguments.workers < 1:
        parser.error("workers must be positive")
    if arguments.time_limit_seconds <= 0:
        parser.error("time limit must be positive")

    repository = Path(__file__).resolve().parents[1]
    if arguments.sources:
        relative_sources = sorted(arguments.sources)
    else:
        sources = sorted((repository / "tests").glob("test_*.py"))
        relative_sources = [source.relative_to(repository) for source in sources]
    output_directory = arguments.output.resolve()
    output_directory.mkdir(parents=True, exist_ok=True)

    results = []
    with ThreadPoolExecutor(max_workers=arguments.workers) as executor:
        futures = {
            executor.submit(
                _run_one,
                repository,
                source,
                output_directory,
                arguments.time_limit_seconds,
            ): source
            for source in relative_sources
        }
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"{result['status']:>18} {result['wall_time_seconds']:>9.3f}s "
                f"{result['source']}",
                flush=True,
            )

    results.sort(key=lambda item: str(item["source"]))
    manifest = {
        "observer": "independently bounded pytest relation-hole populations",
        "source_count": len(results),
        "completed_count": sum(
            result["status"] == "completed" for result in results
        ),
        "time_limit_reached_count": sum(
            result["status"] == "time_limit_reached" for result in results
        ),
        "nonzero_return_count": sum(
            result["returncode"] != 0 for result in results
        ),
        "workers": arguments.workers,
        "time_limit_seconds": arguments.time_limit_seconds,
        "results": results,
    }
    structural = json.dumps(
        manifest, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    manifest["structural_digest"] = sha256(structural).hexdigest()
    manifest_path = output_directory / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"manifest {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
