# app/tasks.py
from crewai import Task
import logging

logger = logging.getLogger(__name__)

def create_navigation_task(agent, current_location: str, destination: str, language: str = "en"):
    """Create the navigation task"""
    return Task(
        description=f"""
        Provide optimal wayfinding directions from {current_location} to {destination}.
        
        Requirements:
        1. Provide step-by-step directions
        2. Include estimated time
        3. Consider accessibility needs
        4. Highlight points of interest along the way
        5. Suggest alternative routes if available
        
        Language: {language}
        
        Consider:
        - Stadium zones and sections
        - Elevators and escalators
        - Restroom locations
        - Food and beverage areas
        - First aid stations
        - Information desks
        - Entrances and exits
        
        The response should be clear, concise, and easy to follow.
        """,
        expected_output="""
        A comprehensive navigation guide including:
        - Step-by-step directions
        - Estimated walking time
        - Accessibility information
        - Points of interest along the way
        - Alternative routes if applicable
        - Language-appropriate formatting
        """,
        agent=agent
    )

def create_crowd_management_task(agent, zone: str, current_crowd_level: str):
    """Create the crowd management task"""
    return Task(
        description=f"""
        Analyze crowd situation in {zone} and provide management recommendations.
        
        Current Crowd Level: {current_crowd_level}
        
        Tasks:
        1. Assess crowd density and movement patterns
        2. Identify potential congestion points
        3. Provide real-time alerts and recommendations
        4. Suggest crowd flow optimization strategies
        5. Identify safety concerns
        
        Consider:
        - Entry and exit points
        - Corridor widths
        - Bottlenecks
        - Emergency access routes
        - Staff deployment needs
        - Communication requirements
        
        Provide actionable recommendations for staff and fans.
        """,
        expected_output="""
        A detailed crowd management report including:
        - Crowd density assessment
        - Congestion point identification
        - Real-time alert recommendations
        - Flow optimization strategies
        - Safety recommendations
        - Staff deployment suggestions
        - Communication guidelines
        """,
        agent=agent
    )

def create_accessibility_task(agent, service_type: str, language: str = "en"):
    """Create the accessibility task"""
    return Task(
        description=f"""
        Provide comprehensive accessibility information for {service_type}.
        
        Language: {language}
        
        Information to include:
        1. Wheelchair accessibility details
        2. Hearing loop availability
        3. Sign language services
        4. Accessible restroom locations
        5. Visual aid information
        6. Service animal policies
        7. Special assistance services
        
        Ensure the information is accurate, helpful, and inclusive.
        """,
        expected_output="""
        A comprehensive accessibility guide including:
        - Detailed accessibility features
        - Service locations
        - Assistance availability
        - Policies and procedures
        - Contact information for support
        - Language-appropriate formatting
        """,
        agent=agent
    )

def create_transportation_task(agent, origin: str, destination: str, language: str = "en"):
    """Create the transportation task"""
    return Task(
        description=f"""
        Provide optimal transportation options from {origin} to {destination}.
        
        Language: {language}
        
        Options to consider:
        1. Shuttle services
        2. Public transit (train, bus, metro)
        3. Parking availability
        4. Ride-sharing services
        5. Walking routes
        6. Bicycle routes
        
        Include:
        - Estimated time
        - Cost information
        - Accessibility features
        - Availability status
        - Real-time updates if available
        
        Prioritize convenience, cost-effectiveness, and accessibility.
        """,
        expected_output="""
        A comprehensive transportation guide including:
        - Multiple transportation options
        - Estimated times and costs
        - Accessibility information
        - Real-time availability
        - Recommendations based on user preferences
        - Language-appropriate formatting
        """,
        agent=agent
    )

def create_sustainability_task(agent, category: str, language: str = "en"):
    """Create the sustainability task"""
    return Task(
        description=f"""
        Provide sustainability tips and information for {category}.
        
        Language: {language}
        
        Topics to cover:
        1. Waste reduction and recycling
        2. Energy conservation
        3. Water conservation
        4. Sustainable transportation
        5. Food waste reduction
        6. Carbon footprint reduction
        
        Include:
        - Actionable tips
        - Impact assessment
        - Participation opportunities
        - Educational information
        
        Make the information engaging and easy to understand.
        """,
        expected_output="""
        A comprehensive sustainability guide including:
        - Actionable tips for fans
        - Impact metrics
        - Participation opportunities
        - Educational content
        - Language-appropriate formatting
        """,
        agent=agent
    )

def create_operational_intelligence_task(agent, data: str, language: str = "en"):
    """Create the operational intelligence task"""
    return Task(
        description=f"""
        Analyze operational data and provide actionable insights.
        
        Data: {data}
        
        Language: {language}
        
        Analysis areas:
        1. Crowd flow patterns
        2. Resource utilization
        3. Service efficiency
        4. Safety metrics
        5. Fan satisfaction indicators
        6. Operational bottlenecks
        
        Provide:
        - Key insights and findings
        - Urgency assessment
        - Actionable recommendations
        - Predictive analysis
        - Risk assessment
        
        Support data-driven decision-making.
        """,
        expected_output="""
        A comprehensive operational intelligence report including:
        - Key insights and findings
        - Urgency assessment
        - Actionable recommendations
        - Predictive analysis
        - Risk assessment
        - Language-appropriate formatting
        """,
        agent=agent
    )