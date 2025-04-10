from fastapi import APIRouter
from app.services.mood_service import get_mood_response
from pydantic import BaseModel

router = APIRouter()

class MoodRequest(BaseModel):
    feeling: str

@router.post("/mood")
async def mood_chat(request: MoodRequest):
    response = get_mood_response(request.feeling)
    return {"feeling": request.feeling, "response": response}
