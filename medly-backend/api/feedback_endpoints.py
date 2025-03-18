from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    session_id: str
    action: str
    feedback: str

@router.post("/submit-feedback")
async def submit_feedback(request: FeedbackRequest):
    # Log feedback or save to database
    print(f"Feedback: Session {request.session_id}, Action: {request.action}, Comment: {request.feedback}")
    return {"status": "submitted"}