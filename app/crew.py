# app/crew.py
from crewai import Crew
import os
import logging
from typing import Dict
from app.model_manager import model_manager

logger = logging.getLogger(__name__)

class StadiumAICrew:
    """Orchestrate the stadium AI services"""
    
    def __init__(self):
        try:
            from app.agents import (
                create_navigation_agent,
                create_crowd_management_agent,
                create_accessibility_agent,
                create_transportation_agent,
                create_sustainability_agent,
                create_multilingual_agent,
                create_operational_intelligence_agent
            )
            from app.tasks import (
                create_navigation_task,
                create_crowd_management_task,
                create_accessibility_task,
                create_transportation_task,
                create_sustainability_task,
                create_operational_intelligence_task,
                create_multilingual_task
            )
            
            self.create_navigation_agent = create_navigation_agent
            self.create_crowd_management_agent = create_crowd_management_agent
            self.create_accessibility_agent = create_accessibility_agent
            self.create_transportation_agent = create_transportation_agent
            self.create_sustainability_agent = create_sustainability_agent
            self.create_multilingual_agent = create_multilingual_agent
            self.create_operational_intelligence_agent = create_operational_intelligence_agent
            
            self.create_navigation_task = create_navigation_task
            self.create_crowd_management_task = create_crowd_management_task
            self.create_accessibility_task = create_accessibility_task
            self.create_transportation_task = create_transportation_task
            self.create_sustainability_task = create_sustainability_task
            self.create_operational_intelligence_task = create_operational_intelligence_task
            self.create_multilingual_task = create_multilingual_task
            
            self.verbose = os.getenv('DEBUG', 'False').lower() == 'true'
            self.model_manager = model_manager
            
            logger.info("✅ StadiumAICrew initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize StadiumAICrew: {str(e)}")
            raise
    
    def handle_navigation(self, current_location: str, destination: str, language: str = "en") -> Dict:
        """Handle navigation request"""
        try:
            logger.info(f"🧭 Navigation: {current_location} → {destination}")
            
            agent = self.create_navigation_agent()
            task = self.create_navigation_task(agent, current_location, destination, language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "current_location": current_location,
                "destination": destination,
                "language": language
            })
            
            return {
                "status": "success",
                "service": "navigation",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Navigation failed: {str(e)}")
            return {
                "status": "error",
                "service": "navigation",
                "error": str(e)
            }
    
    def handle_crowd_management(self, zone: str, crowd_level: str) -> Dict:
        """Handle crowd management request"""
        try:
            logger.info(f"👥 Crowd Management: {zone} - {crowd_level}")
            
            agent = self.create_crowd_management_agent()
            task = self.create_crowd_management_task(agent, zone, crowd_level)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "zone": zone,
                "current_crowd_level": crowd_level
            })
            
            return {
                "status": "success",
                "service": "crowd_management",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Crowd management failed: {str(e)}")
            return {
                "status": "error",
                "service": "crowd_management",
                "error": str(e)
            }
    
    def handle_accessibility(self, service_type: str, language: str = "en") -> Dict:
        """Handle accessibility request"""
        try:
            logger.info(f"♿ Accessibility: {service_type}")
            
            agent = self.create_accessibility_agent()
            task = self.create_accessibility_task(agent, service_type, language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "service_type": service_type,
                "language": language
            })
            
            return {
                "status": "success",
                "service": "accessibility",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Accessibility failed: {str(e)}")
            return {
                "status": "error",
                "service": "accessibility",
                "error": str(e)
            }
    
    def handle_transportation(self, origin: str, destination: str, language: str = "en") -> Dict:
        """Handle transportation request"""
        try:
            logger.info(f"🚌 Transportation: {origin} → {destination}")
            
            agent = self.create_transportation_agent()
            task = self.create_transportation_task(agent, origin, destination, language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "origin": origin,
                "destination": destination,
                "language": language
            })
            
            return {
                "status": "success",
                "service": "transportation",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Transportation failed: {str(e)}")
            return {
                "status": "error",
                "service": "transportation",
                "error": str(e)
            }
    
    def handle_sustainability(self, category: str, language: str = "en") -> Dict:
        """Handle sustainability request"""
        try:
            logger.info(f"🌱 Sustainability: {category}")
            
            agent = self.create_sustainability_agent()
            task = self.create_sustainability_task(agent, category, language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "category": category,
                "language": language
            })
            
            return {
                "status": "success",
                "service": "sustainability",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Sustainability failed: {str(e)}")
            return {
                "status": "error",
                "service": "sustainability",
                "error": str(e)
            }
    
    def handle_operational_intelligence(self, data: str, language: str = "en") -> Dict:
        """Handle operational intelligence request"""
        try:
            logger.info("📊 Operational Intelligence")
            
            agent = self.create_operational_intelligence_agent()
            task = self.create_operational_intelligence_task(agent, data, language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            result = crew.kickoff(inputs={
                "data": data,
                "language": language
            })
            
            return {
                "status": "success",
                "service": "operational_intelligence",
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Operational intelligence failed: {str(e)}")
            return {
                "status": "error",
                "service": "operational_intelligence",
                "error": str(e)
            }
    
    def multilingual_translate(self, text: str, target_language: str, source_language: str = "en") -> Dict:
        """Handle multilingual translation"""
        try:
            logger.info(f"🌐 Translation: {source_language} → {target_language}")
            
            agent = self.create_multilingual_agent()
            task = self.create_multilingual_task(agent, text, target_language, source_language)
            
            crew = Crew(agents=[agent], tasks=[task], verbose=self.verbose)
            # The inputs are now part of the task definition, 
            # but kickoff can still accept them to override if needed.
            # For clarity, we can pass them here as well.
            result = crew.kickoff(inputs={ 
                "text": text,
                "source_language": source_language,
                "target_language": target_language
            })
            
            return {
                "status": "success",
                "service": "translation",
                "source_language": source_language,
                "target_language": target_language,
                "result": str(result)
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return {
                "status": "error",
                "service": "translation",
                "error": str(e)
            }