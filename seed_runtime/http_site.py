"""Serve exact bounded material over a loopback HTTP boundary."""

from __future__ import annotations

from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock, Thread
from typing import Iterable


class HttpSiteError(ValueError):
    """HTTP material or its bounded server could not be used as stated."""


@dataclass(frozen=True)
class HttpMaterial:
    path: str
    media_type: str
    body: bytes

    def __post_init__(self) -> None:
        if (
            type(self.path) is not str
            or not self.path.startswith("/")
            or self.path.startswith("//")
            or "?" in self.path
            or "#" in self.path
            or any(part in {".", ".."} for part in self.path.split("/"))
        ):
            raise HttpSiteError("HTTP material requires one exact absolute path")
        if (
            type(self.media_type) is not str
            or not self.media_type
            or "\r" in self.media_type
            or "\n" in self.media_type
        ):
            raise HttpSiteError("HTTP material requires one exact media type")
        if type(self.body) is not bytes:
            raise HttpSiteError("HTTP material body must be exact bytes")


@dataclass(frozen=True)
class HttpBoundaryObservation:
    sequence: int
    phase: str
    method: str
    request_path: str
    response_status: int | None
    material_path: str | None
    body_byte_count: int | None
    failure_type: str | None = None


class RunningHttpSite:
    """One loopback HTTP server and its bounded process-local observations."""

    def __init__(self, materials: Iterable[HttpMaterial]) -> None:
        exact_materials = tuple(materials)
        if not exact_materials:
            raise HttpSiteError("an HTTP site requires at least one exact material")
        if not all(isinstance(item, HttpMaterial) for item in exact_materials):
            raise HttpSiteError("every HTTP site entry must be exact HTTP material")
        paths = [item.path for item in exact_materials]
        if len(paths) != len(set(paths)):
            raise HttpSiteError("one HTTP path may carry only one exact material")
        self._materials = {item.path: item for item in exact_materials}
        self._observations: list[HttpBoundaryObservation] = []
        self._observation_lock = Lock()
        self._next_sequence = 1

        site = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.0"

            def log_message(self, _format: str, *_args: object) -> None:
                return

            def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
                site._record("request", "GET", self.path, None, None, None)
                material = site._materials.get(self.path)
                if material is None:
                    site._record("response_attempt", "GET", self.path, 404, None, 0)
                    try:
                        self.send_response_only(404)
                        self.send_header("Connection", "close")
                        self.end_headers()
                        self.wfile.flush()
                    except OSError as exc:
                        site._record(
                            "response_failed",
                            "GET",
                            self.path,
                            404,
                            None,
                            0,
                            type(exc).__name__,
                        )
                        return
                    site._record("response", "GET", self.path, 404, None, 0)
                    return

                site._record(
                    "response_attempt",
                    "GET",
                    self.path,
                    200,
                    material.path,
                    len(material.body),
                )
                try:
                    self.send_response_only(200)
                    self.send_header("Content-Type", material.media_type)
                    self.send_header("Connection", "close")
                    self.end_headers()
                    self.wfile.write(material.body)
                    self.wfile.flush()
                except OSError as exc:
                    site._record(
                        "response_failed",
                        "GET",
                        self.path,
                        200,
                        material.path,
                        len(material.body),
                        type(exc).__name__,
                    )
                    return
                site._record(
                    "response",
                    "GET",
                    self.path,
                    200,
                    material.path,
                    len(material.body),
                )

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = Thread(
            target=self._server.serve_forever,
            args=(0.05,),
            name="seed-http-site",
            daemon=True,
        )
        self._closed = False
        self._thread.start()

    def _record(
        self,
        phase: str,
        method: str,
        request_path: str,
        response_status: int | None,
        material_path: str | None,
        body_byte_count: int | None,
        failure_type: str | None = None,
    ) -> None:
        with self._observation_lock:
            sequence = self._next_sequence
            self._next_sequence += 1
            self._observations.append(
                HttpBoundaryObservation(
                    sequence=sequence,
                    phase=phase,
                    method=method,
                    request_path=request_path,
                    response_status=response_status,
                    material_path=material_path,
                    body_byte_count=body_byte_count,
                    failure_type=failure_type,
                )
            )

    @property
    def address(self) -> tuple[str, int]:
        host, port = self._server.server_address
        return str(host), int(port)

    @property
    def observations(self) -> tuple[HttpBoundaryObservation, ...]:
        with self._observation_lock:
            return tuple(self._observations)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=2)

    def __enter__(self) -> "RunningHttpSite":
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def host_http_material(materials: Iterable[HttpMaterial]) -> RunningHttpSite:
    """Start one loopback server for the supplied exact material."""

    return RunningHttpSite(materials)
