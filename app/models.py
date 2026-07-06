# app/models.py
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


SUPPORTED_LANGUAGE_CODES = {"en", "es", "fr", "de", "pt", "ar", "hi", "zh", "ja", "ko"}


class ServiceType(str, Enum):
    """Service types available in the stadium."""

    NAVIGATION = "navigation"
    CROWD_MANAGEMENT = "crowd_management"
    ACCESSIBILITY = "accessibility"
    TRANSPORTATION = "transportation"
    SUSTAINABILITY = "sustainability"
    MULTILINGUAL = "multilingual"
    OPERATIONAL = "operational"
    FAN_EXPERIENCE = "fan_experience"


class BaseServiceRequest(BaseModel):
    """Common validation rules for service requests."""

    model_config = ConfigDict(extra="forbid")


def _normalize_text(value: str, *, field_name: str, max_length: int = 200) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} cannot be empty")
    if len(normalized) > max_length:
        raise ValueError(f"{field_name} exceeds the maximum length of {max_length}")
    if any(ord(char) < 32 and char not in {"\t", "\n"} for char in normalized):
        raise ValueError(f"{field_name} contains unsupported control characters")
    return normalized


def _normalize_language(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("language must be a string")

    normalized = value.strip().lower()
    if normalized not in SUPPORTED_LANGUAGE_CODES:
        raise ValueError(f"Unsupported language: {value}")
    return normalized


class StadiumZone(BaseModel):
    """Stadium zone information."""

    id: str = Field(..., description="Zone identifier")
    name: str = Field(..., description="Zone name")
    type: str = Field(..., description="Zone type: seating, concourse, VIP, media, etc.")
    capacity: int = Field(..., description="Zone capacity")
    facilities: List[str] = Field(default_factory=list, description="Available facilities")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features")


class NavigationRequest(BaseServiceRequest):
    """Navigation request from a fan."""

    user_id: Optional[str] = Field(None, description="User identifier")
    current_location: str = Field(..., description="Current location")
    destination: str = Field(..., description="Destination")
    language: str = Field("en", description="Preferred language")
    accessibility_needs: Optional[List[str]] = Field(None, description="Accessibility requirements")

    @field_validator("current_location", "destination")
    @classmethod
    def validate_location(cls, value: str, info) -> str:
        return _normalize_text(value, field_name=info.field_name, max_length=120)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return _normalize_language(value)

    @field_validator("accessibility_needs", mode="before")
    @classmethod
    def validate_accessibility_needs(cls, value: Optional[List[str]]) -> Optional[List[str]]:
        if value is None:
            return value
        if not isinstance(value, list):
            raise TypeError("accessibility_needs must be a list")
        return [
            _normalize_text(item, field_name="accessibility_needs item", max_length=80)
            for item in value
        ]


class NavigationResponse(BaseModel):
    """Navigation response."""

    directions: List[Dict[str, Any]] = Field(..., description="Step-by-step directions")
    estimated_time: int = Field(..., description="Estimated time in minutes")
    accessible_route: bool = Field(False, description="Is this an accessible route")
    language: str = Field("en", description="Response language")
    points_of_interest: List[str] = Field(default_factory=list, description="Points of interest along the way")


class CrowdAlert(BaseModel):
    """Crowd alert message."""

    id: str = Field(..., description="Alert identifier")
    zone: str = Field(..., description="Affected zone")
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    message: str = Field(..., description="Alert message")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    actions: List[str] = Field(default_factory=list, description="Recommended actions")


class AccessibilityInfo(BaseModel):
    """Accessibility information."""

    wheelchair_accessible: bool = Field(False, description="Is wheelchair accessible")
    hearing_loops: bool = Field(False, description="Has hearing loops")
    sign_language_available: bool = Field(False, description="Sign language available")
    accessible_restrooms: bool = Field(False, description="Accessible restrooms available")
    visual_aids: bool = Field(False, description="Visual aids available")
    service_animals_allowed: bool = Field(True, description="Service animals allowed")
    additional_services: List[str] = Field(default_factory=list, description="Additional accessibility services")


class TransportationOption(BaseModel):
    """Transportation option."""

    id: str = Field(..., description="Option identifier")
    type: str = Field(..., description="Transportation type: shuttle, train, bus, taxi, walking")
    route: str = Field(..., description="Route description")
    estimated_time: int = Field(..., description="Estimated time in minutes")
    cost: float = Field(0.0, description="Cost in USD")
    availability: str = Field("available", description="Availability status")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features")


class SustainabilityTip(BaseModel):
    """Sustainability tip."""

    id: str = Field(..., description="Tip identifier")
    category: str = Field(..., description="Category: waste, energy, water, transport, food")
    title: str = Field(..., description="Tip title")
    description: str = Field(..., description="Tip description")
    impact: str = Field(..., description="Impact level: low, medium, high")
    actions: List[str] = Field(default_factory=list, description="Actions to take")


class OperationalInsight(BaseModel):
    """Operational insight."""

    id: str = Field(..., description="Insight identifier")
    category: str = Field(..., description="Category: crowd, safety, services, logistics")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    urgency: str = Field("normal", description="Urgency: normal, high, critical")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class FanExperience(BaseModel):
    """Fan experience enhancement."""

    id: str = Field(..., description="Experience identifier")
    type: str = Field(..., description="Experience type")
    title: str = Field(..., description="Experience title")
    description: str = Field(..., description="Experience description")
    interactive_elements: List[str] = Field(default_factory=list, description="Interactive elements")
    personalization_options: List[str] = Field(default_factory=list, description="Personalization options")
    estimated_engagement: str = Field("medium", description="Engagement level: low, medium, high")


class CrowdManagementRequest(BaseServiceRequest):
    """Crowd management request."""

    zone: str = Field(..., description="Affected zone")
    crowd_level: str = Field("moderate", description="Crowd level")

    @field_validator("zone")
    @classmethod
    def validate_zone(cls, value: str) -> str:
        return _normalize_text(value, field_name="zone", max_length=120)

    @field_validator("crowd_level")
    @classmethod
    def validate_crowd_level(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"low", "moderate", "high", "critical"}:
            raise ValueError("crowd_level must be one of low, moderate, high, critical")
        return normalized


class AccessibilityRequest(BaseServiceRequest):
    """Accessibility information request."""

    service_subtype: str = Field("general", description="Accessibility request subtype")
    language: str = Field("en", description="Preferred language")

    @field_validator("service_subtype")
    @classmethod
    def validate_service_subtype(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"general", "wheelchair", "hearing", "visual", "assistance"}:
            raise ValueError("service_subtype must be one of general, wheelchair, hearing, visual, assistance")
        return normalized

    @field_validator("language")
    @classmethod
    def validate_accessibility_language(cls, value: str) -> str:
        return _normalize_language(value)


class TransportationRequest(BaseServiceRequest):
    """Transportation request."""

    origin: str = Field(..., description="Starting point")
    destination: str = Field(..., description="Destination")
    language: str = Field("en", description="Preferred language")

    @field_validator("origin", "destination")
    @classmethod
    def validate_transport_location(cls, value: str, info) -> str:
        return _normalize_text(value, field_name=info.field_name, max_length=120)

    @field_validator("language")
    @classmethod
    def validate_transport_language(cls, value: str) -> str:
        return _normalize_language(value)


class SustainabilityRequest(BaseServiceRequest):
    """Sustainability request."""

    category: str = Field("general", description="Sustainability category")
    language: str = Field("en", description="Preferred language")

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"general", "waste", "energy", "water", "transport", "food"}:
            raise ValueError("category must be one of general, waste, energy, water, transport, food")
        return normalized

    @field_validator("language")
    @classmethod
    def validate_sustainability_language(cls, value: str) -> str:
        return _normalize_language(value)


class OperationalRequest(BaseServiceRequest):
    """Operational intelligence request."""

    data: str = Field(..., description="Operational data to analyze")
    language: str = Field("en", description="Preferred language")

    @field_validator("data")
    @classmethod
    def validate_data(cls, value: str) -> str:
        return _normalize_text(value, field_name="data", max_length=800)

    @field_validator("language")
    @classmethod
    def validate_operational_language(cls, value: str) -> str:
        return _normalize_language(value)


class MultilingualRequest(BaseServiceRequest):
    """Multilingual translation request."""

    text: str = Field(..., description="Text to translate")
    target_language: str = Field("es", description="Target language")
    source_language: str = Field("en", description="Source language")

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return _normalize_text(value, field_name="text", max_length=1000)

    @field_validator("target_language", "source_language")
    @classmethod
    def validate_translation_language(cls, value: str, info) -> str:
        return _normalize_language(value)


class StadiumServiceRequest(BaseModel):
    """Complete service request."""

    request_id: str = Field(..., description="Request identifier")
    service_type: ServiceType = Field(..., description="Service type")
    user_id: Optional[str] = Field(None, description="User identifier")
    language: str = Field("en", description="Preferred language")
    query: str = Field(..., description="User query")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())