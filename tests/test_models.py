try:
    import pytest
except ImportError:
    pytest = None

from app.models import (
    AccessibilityRequest,
    CrowdManagementRequest,
    MultilingualRequest,
    NavigationRequest,
    OperationalRequest,
    SustainabilityRequest,
    TransportationRequest,
)


def test_navigation_model_validation():
    req = NavigationRequest(
        current_location="Gate 4 East",
        destination="Section 118, Row 12",
        language="en",
        accessibility_needs=["wheelchair", "step_free"],
    )
    assert req.current_location == "Gate 4 East"
    assert req.destination == "Section 118, Row 12"
    assert req.language == "en"
    assert len(req.accessibility_needs) == 2


def test_crowd_management_valid_levels():
    for level in ["low", "moderate", "high", "critical"]:
        req = CrowdManagementRequest(zone="East Concourse", crowd_level=level)
        assert req.crowd_level == level


def test_crowd_management_invalid_level_raises():
    try:
        CrowdManagementRequest(zone="East Concourse", crowd_level="danger_overload")
        assert False, "Should raise validation error"
    except Exception:
        pass


def test_accessibility_valid_subtypes():
    for subtype in ["general", "wheelchair", "hearing", "visual", "assistance"]:
        req = AccessibilityRequest(service_subtype=subtype, language="es")
        assert req.service_subtype == subtype
        assert req.language == "es"


def test_transportation_model_validation():
    req = TransportationRequest(origin="Stadium North Exit", destination="Metro Hub", transit_mode="metro")
    assert req.origin == "Stadium North Exit"
    assert req.destination == "Metro Hub"
    assert req.transit_mode == "metro"


def test_sustainability_valid_categories():
    for cat in ["general", "waste", "energy", "water", "transport", "food"]:
        req = SustainabilityRequest(category=cat, language="fr")
        assert req.category == cat


def test_multilingual_model_validation():
    req = MultilingualRequest(
        text="Welcome to the FIFA World Cup Quarter Final",
        target_language="es",
        source_language="en",
    )
    assert req.text.startswith("Welcome")
    assert req.target_language == "es"
    assert req.source_language == "en"


def test_operational_model_validation():
    req = OperationalRequest(data="Gate 4 throughput: 180 fans/min. Concourse B wait: 2.5m.", language="en")
    assert "throughput" in req.data
