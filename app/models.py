# app/models.py
from pydantic import BaseModel, Field
from typing import Dict, Optional, List, Any
from datetime import datetime
from enum import Enum

class ServiceType(str, Enum):
    """Service types available in the stadium"""
    NAVIGATION = "navigation"
    CROWD_MANAGEMENT = "crowd_management"
    ACCESSIBILITY = "accessibility"
    TRANSPORTATION = "transportation"
    SUSTAINABILITY = "sustainability"
    MULTILINGUAL = "multilingual"
    OPERATIONAL = "operational"
    FAN_EXPERIENCE = "fan_experience"

class StadiumZone(BaseModel):
    """Stadium zone information"""
    id: str = Field(..., description="Zone identifier")
    name: str = Field(..., description="Zone name")
    type: str = Field(..., description="Zone type: seating, concourse, VIP, media, etc.")
    capacity: int = Field(..., description="Zone capacity")
    facilities: List[str] = Field(default_factory=list, description="Available facilities")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features")

class NavigationRequest(BaseModel):
    """Navigation request from fan"""
    user_id: Optional[str] = Field(None, description="User identifier")
    current_location: str = Field(..., description="Current location")
    destination: str = Field(..., description="Destination")
    language: str = Field("en", description="Preferred language")
    accessibility_needs: Optional[List[str]] = Field(None, description="Accessibility requirements")

class NavigationResponse(BaseModel):
    """Navigation response"""
    directions: List[Dict] = Field(..., description="Step-by-step directions")
    estimated_time: int = Field(..., description="Estimated time in minutes")
    accessible_route: bool = Field(False, description="Is this an accessible route")
    language: str = Field("en", description="Response language")
    points_of_interest: List[str] = Field(default_factory=list, description="Points of interest along the way")

class CrowdAlert(BaseModel):
    """Crowd alert message"""
    id: str = Field(..., description="Alert identifier")
    zone: str = Field(..., description="Affected zone")
    severity: str = Field(..., description="Severity: low, medium, high, critical")
    message: str = Field(..., description="Alert message")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    actions: List[str] = Field(default_factory=list, description="Recommended actions")

class AccessibilityInfo(BaseModel):
    """Accessibility information"""
    wheelchair_accessible: bool = Field(False, description="Is wheelchair accessible")
    hearing_loops: bool = Field(False, description="Has hearing loops")
    sign_language_available: bool = Field(False, description="Sign language available")
    accessible_restrooms: bool = Field(False, description="Accessible restrooms available")
    visual_aids: bool = Field(False, description="Visual aids available")
    service_animals_allowed: bool = Field(True, description="Service animals allowed")
    additional_services: List[str] = Field(default_factory=list, description="Additional accessibility services")

class TransportationOption(BaseModel):
    """Transportation option"""
    id: str = Field(..., description="Option identifier")
    type: str = Field(..., description="Transportation type: shuttle, train, bus, taxi, walking")
    route: str = Field(..., description="Route description")
    estimated_time: int = Field(..., description="Estimated time in minutes")
    cost: float = Field(0.0, description="Cost in USD")
    availability: str = Field("available", description="Availability status")
    accessibility_features: List[str] = Field(default_factory=list, description="Accessibility features")

class SustainabilityTip(BaseModel):
    """Sustainability tip"""
    id: str = Field(..., description="Tip identifier")
    category: str = Field(..., description="Category: waste, energy, water, transport, food")
    title: str = Field(..., description="Tip title")
    description: str = Field(..., description="Tip description")
    impact: str = Field(..., description="Impact level: low, medium, high")
    actions: List[str] = Field(default_factory=list, description="Actions to take")

class OperationalInsight(BaseModel):
    """Operational insight"""
    id: str = Field(..., description="Insight identifier")
    category: str = Field(..., description="Category: crowd, safety, services, logistics")
    title: str = Field(..., description="Insight title")
    description: str = Field(..., description="Insight description")
    urgency: str = Field("normal", description="Urgency: normal, high, critical")
    recommendations: List[str] = Field(default_factory=list, description="Recommended actions")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())

class FanExperience(BaseModel):
    """Fan experience enhancement"""
    id: str = Field(..., description="Experience identifier")
    type: str = Field(..., description="Experience type")
    title: str = Field(..., description="Experience title")
    description: str = Field(..., description="Experience description")
    interactive_elements: List[str] = Field(default_factory=list, description="Interactive elements")
    personalization_options: List[str] = Field(default_factory=list, description="Personalization options")
    estimated_engagement: str = Field("medium", description="Engagement level: low, medium, high")

class StadiumServiceRequest(BaseModel):
    """Complete service request"""
    request_id: str = Field(..., description="Request identifier")
    service_type: ServiceType = Field(..., description="Service type")
    user_id: Optional[str] = Field(None, description="User identifier")
    language: str = Field("en", description="Preferred language")
    query: str = Field(..., description="User query")
    context: Optional[Dict] = Field(None, description="Additional context")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())