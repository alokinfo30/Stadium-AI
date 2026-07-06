# app/main.py
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging
import json
import uuid
from datetime import datetime

load_dotenv()
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

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
        "description": "Find your way around the stadium"
    },
    "crowd_management": {
        "name": "Crowd Management",
        "icon": "👥",
        "description": "Real-time crowd insights and alerts"
    },
    "accessibility": {
        "name": "Accessibility",
        "icon": "♿",
        "description": "Inclusive access information"
    },
    "transportation": {
        "name": "Transportation",
        "icon": "🚌",
        "description": "Transportation options to and from the stadium"
    },
    "sustainability": {
        "name": "Sustainability",
        "icon": "🌱",
        "description": "Eco-friendly tips and practices"
    },
    "multilingual": {
        "name": "Multilingual",
        "icon": "🌐",
        "description": "Translate to your preferred language"
    },
    "operational": {
        "name": "Operational Intelligence",
        "icon": "📊",
        "description": "Real-time operational insights"
    }
}

SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,es,fr,de,pt,ar,hi,zh,ja,ko').split(',')

@main_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html', services=SERVICES, languages=SUPPORTED_LANGUAGES)

@main_bp.route('/api/service', methods=['POST'])
def handle_service():
    """Handle a service request"""
    try:
        data = request.json
        service_type = data.get('service_type')
        
        if not service_type:
            return jsonify({
                'error': 'Missing service type',
                'status': 'error'
            }), 400
        
        if service_type not in SERVICES:
            return jsonify({
                'error': f'Invalid service type: {service_type}',
                'status': 'error'
            }), 400
        
        if not CREW_AVAILABLE:
            return jsonify({
                'error': 'CrewAI not available. Please check installation.',
                'status': 'error'
            }), 500
        
        language = data.get('language', 'en')
        crew = StadiumAICrew()
        
        # Route to appropriate handler
        if service_type == 'navigation':
            current_location = data.get('current_location', 'Main Entrance')
            destination = data.get('destination', 'Section A')
            result = crew.handle_navigation(current_location, destination, language)
            
        elif service_type == 'crowd_management':
            zone = data.get('zone', 'Main Concourse')
            crowd_level = data.get('crowd_level', 'moderate')
            result = crew.handle_crowd_management(zone, crowd_level)
            
        elif service_type == 'accessibility':
            service_subtype = data.get('service_subtype', 'general')
            result = crew.handle_accessibility(service_subtype, language)
            
        elif service_type == 'transportation':
            origin = data.get('origin', 'Stadium')
            destination = data.get('destination', 'City Center')
            result = crew.handle_transportation(origin, destination, language)
            
        elif service_type == 'sustainability':
            category = data.get('category', 'general')
            result = crew.handle_sustainability(category, language)
            
        elif service_type == 'operational':
            operational_data = data.get('data', 'Crowd flow analysis')
            result = crew.handle_operational_intelligence(operational_data, language)
            
        elif service_type == 'multilingual':
            text = data.get('text', '')
            target_lang = data.get('target_language', 'es')
            source_lang = data.get('source_language', 'en')
            result = crew.multilingual_translate(text, target_lang, source_lang)
            
        else:
            return jsonify({
                'error': f'Unhandled service type: {service_type}',
                'status': 'error'
            }), 400
        
        if result['status'] == 'error':
            return jsonify({
                'error': result.get('error', 'Unknown error'),
                'status': 'error'
            }), 500
        
        return jsonify({
            'status': 'success',
            'service': service_type,
            'result': result,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error handling service: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main_bp.route('/api/services', methods=['GET'])
def get_services():
    """Get all available services"""
    return jsonify({
        'status': 'success',
        'services': SERVICES,
        'languages': SUPPORTED_LANGUAGES
    })

@main_bp.route('/api/models', methods=['GET'])
def get_models():
    """Get available models"""
    try:
        from app.model_manager import model_manager
        results = model_manager.test_providers()
        available = [m for m, v in results.items() if v]
        
        return jsonify({
            'status': 'success',
            'models': {
                'primary': os.getenv('OPENROUTER_PRIMARY_MODEL', 'openai/gpt-4o-mini'),
                'fallbacks': os.getenv('OPENROUTER_FALLBACK_MODELS', '').split(','),
                'available': available,
                'all_tested': results
            }
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'crew_available': CREW_AVAILABLE,
        'version': '1.0.0',
        'features': list(SERVICES.keys()),
        'languages_supported': len(SUPPORTED_LANGUAGES)
    })