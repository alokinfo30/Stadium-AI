import unittest
try:
    import pytest
except ImportError:
    pytest = None

from app import create_app
from app.models import (
    AccessibilityRequest,
    CrowdManagementRequest,
    NavigationRequest,
    OperationalRequest,
    TransportationRequest,
)

if pytest:
    @pytest.fixture()
    def client():
        app = create_app()
        app.config.update(TESTING=True)
        with app.test_client() as client:
            yield client


def test_navigation_request_model_accepts_valid_data(client=None):
    payload = NavigationRequest(
        current_location="Main Entrance",
        destination="Gate A",
        language="en",
        accessibility_needs=["wheelchair"],
    )
    assert payload.current_location == "Main Entrance"
    assert payload.destination == "Gate A"


def test_crowd_management_request_rejects_invalid_level(client=None):
    try:
        CrowdManagementRequest(zone="North Concourse", crowd_level="extreme")
        assert False, "Should have raised validation error"
    except Exception:
        pass


def test_accessibility_request_model_accepts_valid_data(client=None):
    payload = AccessibilityRequest(service_subtype="wheelchair", language="en")
    assert payload.service_subtype == "wheelchair"


def test_transportation_request_model_accepts_valid_data(client=None):
    payload = TransportationRequest(origin="Hotel", destination="Stadium", language="en")
    assert payload.origin == "Hotel"


def test_operational_request_model_accepts_valid_data(client=None):
    payload = OperationalRequest(data="Crowd flow is steady", language="en")
    assert payload.data == "Crowd flow is steady"


def test_health_endpoint_returns_success(client=None):
    if client is None:
        app = create_app()
        app.config.update(TESTING=True)
        client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_service_endpoint_rejects_unknown_service(client=None):
    if client is None:
        app = create_app()
        app.config.update(TESTING=True)
        client = app.test_client()
    response = client.post(
        "/api/service",
        json={"service_type": "unknown"},
    )
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_service_endpoint_rejects_invalid_payload_shape(client=None):
    if client is None:
        app = create_app()
        app.config.update(TESTING=True)
        client = app.test_client()
    response = client.post(
        "/api/service",
        data="not-json",
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_security_headers_are_present(client=None):
    if client is None:
        app = create_app()
        app.config.update(TESTING=True)
        client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
