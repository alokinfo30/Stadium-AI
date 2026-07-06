# app/utils.py
import json
import logging
from typing import Dict, Any
import re

logger = logging.getLogger(__name__)

def parse_ai_response(response: str) -> Dict[str, Any]:
    """Parse AI response to extract structured data"""
    try:
        if response.strip().startswith('{'):
            return json.loads(response)
        
        json_match = re.search(r'```json\s*(\{.*\})\s*```', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        
        return {"raw_response": response}
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error: {str(e)}")
        return {"raw_response": response}
    except Exception as e:
        logger.error(f"Error parsing AI response: {str(e)}")
        return {"raw_response": response}

def get_service_icon(service_type: str) -> str:
    """Get icon for service type"""
    icons = {
        "navigation": "🧭",
        "crowd_management": "👥",
        "accessibility": "♿",
        "transportation": "🚌",
        "sustainability": "🌱",
        "multilingual": "🌐",
        "operational": "📊"
    }
    return icons.get(service_type, "🤖")