try:
    import pytest
except ImportError:
    pytest = None

from app import create_app


def get_client(client=None):
    if client is not None:
        return client
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def test_enterprise_security_headers_enforcement(client=None):
    """Verify all 7 enterprise security headers are present on all responses."""
    c = get_client(client)
    response = c.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert response.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"
    assert "microphone=(self)" in response.headers.get("Permissions-Policy", "")
    assert "max-age=31536000" in response.headers.get("Strict-Transport-Security", "")
    assert "default-src 'self'" in response.headers.get("Content-Security-Policy", "")


def test_xss_injection_payload_sanitization(client=None):
    """Verify that raw malicious script tags are rejected or safely sanitized."""
    c = get_client(client)
    malicious_payload = {
        "service_type": "multilingual",
        "text": "<script>alert('XSS_ATTACK')</script> Hello Match",
        "target_language": "es",
        "source_language": "en",
    }
    response = c.post("/api/service", json=malicious_payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.get_json()
        assert "<script>" not in str(data)


def test_payload_size_limit_rejection(client=None):
    """Verify that oversized payloads exceeding 2MB are rejected with HTTP 413."""
    c = get_client(client)
    huge_payload = "A" * (3 * 1024 * 1024)  # 3MB
    response = c.post(
        "/api/service",
        data=huge_payload,
        content_type="application/json",
    )
    assert response.status_code in [413, 400]


def test_invalid_http_methods_rejected(client=None):
    """Verify that non-supported HTTP verbs on endpoints return appropriate status codes."""
    c = get_client(client)
    response = c.put("/api/service", json={"service_type": "navigation"})
    assert response.status_code == 405
    response = c.delete("/api/models")
    assert response.status_code == 405


def test_sql_injection_attempt_handled_safely(client=None):
    """Verify that SQL injection strings in parameters are safely processed without database corruption."""
    c = get_client(client)
    sql_inj_payload = {
        "service_type": "navigation",
        "current_location": "' OR '1'='1' --",
        "destination": "'; DROP TABLE users; --",
        "language": "en",
    }
    response = c.post("/api/service", json=sql_inj_payload)
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        assert response.get_json()["status"] == "success"
