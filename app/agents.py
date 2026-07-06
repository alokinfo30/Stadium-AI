# app/agents.py
import logging
from crewai import Agent
from app.model_manager import model_manager

logger = logging.getLogger(__name__)

try:
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    TOOLS_AVAILABLE = True
except ImportError:
    logger.warning("⚠️ crewai_tools not available. Using fallback.")
    TOOLS_AVAILABLE = False
    
    class SerperDevTool:
        def __init__(self):
            self.name = "SerperDevTool"
            self.description = "Search tool (fallback)"
        def run(self, query):
            return f"Search results for: {query} (fallback)"
    
    class ScrapeWebsiteTool:
        def __init__(self):
            self.name = "ScrapeWebsiteTool"
            self.description = "Web scraping tool (fallback)"
        def run(self, url):
            return f"Scraped content from: {url} (fallback)"

def create_navigation_agent():
    """Create the navigation agent for wayfinding"""
    config = model_manager.get_model_config('navigation')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.3))
    
    return Agent(
        role="Stadium Navigation Expert",
        goal="Provide optimal wayfinding solutions for fans and staff",
        backstory=(
            "You are a navigation expert with deep knowledge of stadium layout. "
            "You help fans find their seats, facilities, and points of interest. "
            "You consider accessibility needs and provide clear, step-by-step directions. "
            "You understand crowd flow patterns and can suggest the best routes."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm,
        tools=[SerperDevTool(), ScrapeWebsiteTool()]
    )

def create_crowd_management_agent():
    """Create the crowd management agent"""
    config = model_manager.get_model_config('crowd_management')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.2))
    
    return Agent(
        role="Crowd Management Specialist",
        goal="Ensure safe and efficient crowd movement throughout the stadium",
        backstory=(
            "You are a crowd management expert with experience in large-scale events. "
            "You analyze crowd patterns, predict congestion, and provide real-time "
            "alerts and recommendations. You prioritize safety and fan experience."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_accessibility_agent():
    """Create the accessibility agent"""
    config = model_manager.get_model_config('accessibility')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.4))
    
    return Agent(
        role="Accessibility Specialist",
        goal="Ensure inclusive access for all fans regardless of abilities",
        backstory=(
            "You are an accessibility expert who ensures every fan can enjoy the "
            "match experience. You provide information on wheelchair access, "
            "hearing loops, visual aids, and other accessibility services. "
            "You advocate for inclusive design and barrier-free access."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_transportation_agent():
    """Create the transportation agent"""
    config = model_manager.get_model_config('transportation')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.3))
    
    return Agent(
        role="Transportation Logistics Expert",
        goal="Optimize transportation options for fans to and from the stadium",
        backstory=(
            "You are a transportation logistics expert who coordinates shuttle services, "
            "public transit, parking, and ride-sharing options. You provide real-time "
            "updates and suggest the best transportation modes based on fan location "
            "and preferences."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_sustainability_agent():
    """Create the sustainability agent"""
    config = model_manager.get_model_config('sustainability')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.4))
    
    return Agent(
        role="Sustainability Champion",
        goal="Promote eco-friendly practices and reduce environmental impact",
        backstory=(
            "You are a sustainability expert who educates fans on eco-friendly practices. "
            "You provide tips on waste reduction, energy conservation, and sustainable "
            "transportation. You help the stadium achieve its green goals."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_multilingual_agent():
    """Create the multilingual agent"""
    config = model_manager.get_model_config('multilingual')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.5))
    
    return Agent(
        role="Multilingual Communications Expert",
        goal="Provide seamless multilingual support for international fans",
        backstory=(
            "You are a multilingual communications expert fluent in multiple languages. "
            "You translate information and assist fans in their preferred language. "
            "You ensure that language is never a barrier to enjoying the match experience."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

def create_operational_intelligence_agent():
    """Create the operational intelligence agent"""
    config = model_manager.get_model_config('operational')
    llm = model_manager.get_llm(config['model'], config.get('temperature', 0.2))
    
    return Agent(
        role="Operational Intelligence Analyst",
        goal="Provide real-time insights for stadium operations and decision-making",
        backstory=(
            "You are an operational intelligence expert who analyzes data from "
            "multiple sources to provide actionable insights. You help staff make "
            "informed decisions about crowd management, resource allocation, and "
            "emergency response."
        ),
        allow_delegation=False,
        verbose=True,
        llm=llm
    )