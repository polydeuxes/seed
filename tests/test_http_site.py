from __future__ import annotations

from http.client import HTTPConnection

import pytest

from seed_runtime.http_site import HttpMaterial, HttpSiteError, host_http_material


def _request(site, path: str):
    connection = HTTPConnection(*site.address, timeout=2)
    try:
        connection.request("GET", path)
        response = connection.getresponse()
        return response.status, dict(response.getheaders()), response.read()
    finally:
        connection.close()


def test_seed_hosts_exact_html_and_image_material_at_distinct_paths():
    html = b'<!doctype html><img src="/pixel.rgb">\n'
    pixel = bytes((255, 0, 0))
    with host_http_material(
        (
            HttpMaterial("/", "text/html; charset=utf-8", html),
            HttpMaterial("/pixel.rgb", "application/octet-stream", pixel),
        )
    ) as site:
        html_status, html_headers, html_body = _request(site, "/")
        pixel_status, pixel_headers, pixel_body = _request(site, "/pixel.rgb")

        assert (html_status, html_body) == (200, html)
        assert html_headers["Content-Type"] == "text/html; charset=utf-8"
        assert (pixel_status, pixel_body) == (200, pixel)
        assert pixel_headers["Content-Type"] == "application/octet-stream"

        responses = [item for item in site.observations if item.phase == "response"]
        assert [(item.material_path, item.body_length) for item in responses] == [
            ("/", len(html)),
            ("/pixel.rgb", len(pixel)),
        ]


def test_response_attempt_precedes_response_boundary_observation():
    with host_http_material((HttpMaterial("/", "text/plain", b"seed\n"),)) as site:
        assert _request(site, "/") == (
            200,
            {
                "Content-Type": "text/plain",
                "Content-Length": "5",
                "Connection": "close",
            },
            b"seed\n",
        )
        phases = [item.phase for item in site.observations]
        assert phases == ["request", "response_attempt", "response"]
        assert [item.sequence for item in site.observations] == [1, 2, 3]


def test_unknown_or_path_like_request_does_not_read_the_filesystem(tmp_path, monkeypatch):
    secret = tmp_path / "secret.txt"
    secret.write_text("do not serve", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with host_http_material((HttpMaterial("/", "text/plain", b"home"),)) as site:
        status, _headers, body = _request(site, "/secret.txt")
        assert (status, body) == (404, b"")
        status, _headers, body = _request(site, "/../secret.txt")
        assert (status, body) == (404, b"")


@pytest.mark.parametrize(
    "material",
    [
        ("relative", "text/plain", b"x"),
        ("/../x", "text/plain", b"x"),
        ("/x?y", "text/plain", b"x"),
        ("/x", "text/plain\r\nBad: yes", b"x"),
        ("/x", "text/plain", "not bytes"),
    ],
)
def test_http_material_refuses_ambiguous_or_nonbyte_coordinates(material):
    with pytest.raises(HttpSiteError):
        HttpMaterial(*material)


def test_duplicate_paths_are_refused_before_the_server_starts():
    with pytest.raises(HttpSiteError, match="one HTTP path"):
        host_http_material(
            (
                HttpMaterial("/", "text/plain", b"first"),
                HttpMaterial("/", "text/plain", b"second"),
            )
        )
