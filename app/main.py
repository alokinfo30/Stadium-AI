# app/main.py
import logging
import os
from datetime import datetime

import bleach
from dotenv import load_dotenv
from flask import Blueprint, jsonify, render_template, request
from pydantic import ValidationError

from app.models import (
    AccessibilityRequest,
    CrowdManagementRequest,
    MultilingualRequest,
    NavigationRequest,
    OperationalRequest,
    SustainabilityRequest,
    TransportationRequest,
)

load_dotenv()
logger = logging.getLogger(__name__)

main_bp = Blueprint("main", __name__)

# Import crew
try:
    from app.crew import StadiumAICrew

    CREW_AVAILABLE = True
    logger.info("✅ StadiumAICrew imported successfully")
except ImportError as e:
    logger.warning(f"⚠️ Crew not available: {e}")
    CREW_AVAILABLE = False

# Service mapping
SERVICES = {
    "navigation": {
        "name": "Navigation",
        "icon": "🧭",
        "description": "Find your way around the stadium",
    },
    "crowd_management": {
        "name": "Crowd Management",
        "icon": "👥",
        "description": "Real-time crowd insights and alerts",
    },
    "accessibility": {
        "name": "Accessibility",
        "icon": "♿",
        "description": "Inclusive access information",
    },
    "transportation": {
        "name": "Transportation",
        "icon": "🚌",
        "description": "Transportation options to and from the stadium",
    },
    "sustainability": {
        "name": "Sustainability",
        "icon": "🌱",
        "description": "Eco-friendly tips and practices",
    },
    "multilingual": {
        "name": "Multilingual",
        "icon": "🌐",
        "description": "Translate to your preferred language",
    },
    "operational": {
        "name": "Operational Intelligence",
        "icon": "📊",
        "description": "Real-time operational insights",
    },
}

SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "en,es,fr,de,pt,ar,hi,zh,ja,ko").split(",")
REQUEST_MODELS = {
    "navigation": NavigationRequest,
    "crowd_management": CrowdManagementRequest,
    "accessibility": AccessibilityRequest,
    "transportation": TransportationRequest,
    "sustainability": SustainabilityRequest,
    "operational": OperationalRequest,
    "multilingual": MultilingualRequest,
}


def _error_response(message: str, status_code: int = 400):
    return jsonify({"error": message, "status": "error"}), status_code


def _sanitize_result_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value)
    return bleach.clean(text, tags=[], strip=True)


@main_bp.route("/")
def index():
    """Render the main page."""
    return render_template("index.html", services=SERVICES, languages=SUPPORTED_LANGUAGES)


@main_bp.route("/api/service", methods=["POST"])
def handle_service():
    """Handle a service request with strict validation."""
    if not request.is_json:
        return _error_response("Request body must be valid JSON")

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return _error_response("Request body must be a JSON object")

    service_type = payload.get("service_type")
    if not service_type:
        return _error_response("Missing service type")

    if service_type not in SERVICES:
        return _error_response(f"Invalid service type: {service_type}")

    if not CREW_AVAILABLE:
        return _error_response("CrewAI not available. Please check installation."), 500

    request_payload = {key: value for key, value in payload.items() if key != "service_type"}
    request_model = REQUEST_MODELS.get(service_type)
    if request_model is None:
        return _error_response(f"Unhandled service type: {service_type}")

    try:
        validated_request = request_model(**request_payload)
    except ValidationError as exc:
        logger.warning("Validation failed for %s: %s", service_type, exc)
        return _error_response(f"Invalid request data: {exc}")

    try:
        crew = StadiumAICrew()

        if service_type == "navigation":
            result = crew.handle_navigation(
                validated_request.current_location,
                validated_request.destination,
                validated_request.language,
            )
        elif service_type == "crowd_management":
            result = crew.handle_crowd_management(
                validated_request.zone,
                validated_request.crowd_level,
            )
        elif service_type == "accessibility":
            result = crew.handle_accessibility(
                validated_request.service_subtype,
                validated_request.language,
            )
        elif service_type == "transportation":
            result = crew.handle_transportation(
                validated_request.origin,
                validated_request.destination,
                validated_request.language,
            )
        elif service_type == "sustainability":
            result = crew.handle_sustainability(
                validated_request.category,
                validated_request.language,
            )
        elif service_type == "operational":
            result = crew.handle_operational_intelligence(
                validated_request.data,
                validated_request.language,
            )
        elif service_type == "multilingual":
            result = crew.multilingual_translate(
                validated_request.text,
                validated_request.target_language,
                validated_request.source_language,
            )
        else:
            return _error_response(f"Unhandled service type: {service_type}")

        if result.get("status") == "error":
            return jsonify({
                "error": result.get("error", "Unknown error"),
                "status": "error",
            }), 500

        return jsonify({
            "status": "success",
            "service": service_type,
            "result": {
                **result,
                "result": _sanitize_result_text(result.get("result", "")),
            },
            "timestamp": datetime.utcnow().isoformat(),
        })
    except Exception as exc:
        logger.error("Error handling service: %s", exc)
        return _error_response(str(exc), 500)


@main_bp.route("/api/services", methods=["GET"])
def get_services():
    """Get all available services."""
    return jsonify({
        "status": "success",
        "services": SERVICES,
        "languages": SUPPORTED_LANGUAGES,
    })


@main_bp.route("/api/models", methods=["GET"])
def get_models():
    """Get available models."""
    try:
        from app.model_manager import model_manager

        results = model_manager.test_providers()
        available = [model for model, is_available in results.items() if is_available]

        return jsonify({
            "status": "success",
            "models": {
                "primary": os.getenv("OPENROUTER_PRIMARY_MODEL", "openai/gpt-4o-mini"),
                "fallbacks": os.getenv("OPENROUTER_FALLBACK_MODELS", "").split(","),
                "available": available,
                "all_tested": results,
            },
        })
    except Exception as exc:
        return _error_response(str(exc), 500)


@main_bp.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "crew_available": CREW_AVAILABLE,
        "version": "1.0.0",
        "features": list(SERVICES.keys()),
        "languages_supported": len(SUPPORTED_LANGUAGES),
    })