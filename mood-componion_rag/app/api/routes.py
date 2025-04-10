from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.mood_service import get_mood_response, detect_crisis, get_crisis_resources
from pydantic import BaseModel
from typing import Optional, List
import datetime
router = APIRouter()

async def log_crisis_event(user_id: str, message: str):
    """
    Log crisis events for potential follow-up
    
    Args:
        user_id: Identifier for the user experiencing crisis
        message: The crisis message they sent
    """
    # You can implement actual logging to database or file here
    # For example:
    time_now = datetime.datetime.now().isoformat()
    log_entry = f"{time_now} - CRISIS EVENT - User: {user_id} - Message: {message}"
    
    # Simple file logging example (you might want to use a more robust solution):
    with open("crisis_logs.txt", "a") as log_file:
        log_file.write(log_entry + "\n")
    
    # If you have database logging:
    # await db.crisis_logs.insert_one({"user_id": user_id, "message": message, "timestamp": time_now})

class MoodRequest(BaseModel):
    feeling: str
    user_id: Optional[str] = None
    location: Optional[str] = None

class ResourceInfo(BaseModel):
    name: str
    contact: str
    description: Optional[str] = None

class MoodResponse(BaseModel):
    feeling: str
    response: str
    is_crisis_detected: bool = False
    crisis_resources: Optional[List[ResourceInfo]] = None

@router.post("/mood", response_model=MoodResponse)
async def mood_chat(request: MoodRequest, background_tasks: BackgroundTasks):
    # Process the mood response
    response = get_mood_response(request.feeling)
    
    # Check for crisis indicators
    is_crisis = detect_crisis(request.feeling)
    crisis_resources = None
    
    if is_crisis:
        # Get relevant crisis resources, possibly filtered by location if provided
        crisis_resources = get_crisis_resources(request.feeling, request.location)
        
        # Optional: Log crisis events for follow-up (in background)
        if request.user_id:
            background_tasks.add_task(log_crisis_event, request.user_id, request.feeling)
    
    return MoodResponse(
        feeling=request.feeling,
        response=response,
        is_crisis_detected=is_crisis,
        crisis_resources=crisis_resources
    )

# New endpoint specifically for crisis resources
@router.get("/crisis-resources/{location}")
async def get_location_resources(location: str):
    resources = get_crisis_resources("", location)
    return {"resources": resources}