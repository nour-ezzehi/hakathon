# app/services/mood_service.py
from app.core.mood_chain import get_bot_response
from app.data.crisis_resources import get_resources_by_crisis_type, get_emergency_resources

# Crisis detection function
def detect_crisis(message: str) -> bool:
    crisis_keywords = ["suicide", "kill myself", "end my life", "don't want to live", 
                     "better off dead", "no reason to live", "can't go on"]
    
    message_lower = message.lower()
    for keyword in crisis_keywords:
        if keyword in message_lower:
            return True
    return False

# Get relevant crisis resources
def get_crisis_resources(message: str, location: str = None):
    # Get resources based on crisis type and location
    resources = get_resources_by_crisis_type(message, location)
    
    # Always include emergency resources
    emergency = get_emergency_resources()
    
    # Combine and return (emergency resources first)
    return emergency + resources

# Function for mood responses
def get_mood_response(feeling: str):
    # Check for crisis indicators
    is_crisis = detect_crisis(feeling)
    
    # Get response from bot
    return get_bot_response(feeling, is_crisis=is_crisis)