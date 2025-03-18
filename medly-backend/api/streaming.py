from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from database.session_manager import get_session_state
import asyncio

router = APIRouter()

@router.get("/stream-diagnosis/{session_id}")
async def stream_diagnosis(session_id: str):
    async def event_generator():
        seen_steps = set()
        while True:
            state = get_session_state(session_id)
            if state and state["reasoning_steps"]:
                for step in state["reasoning_steps"]:
                    step_str = f"{step['timestamp']}: {step['message']}"
                    if step_str not in seen_steps:
                        yield f"data: {step_str}\n\n"
                        seen_steps.add(step_str)
                if len(state["reasoning_steps"]) >= 8:  # All steps completed
                    break
            await asyncio.sleep(0.5)
    return StreamingResponse(event_generator(), media_type="text/event-stream")