from fastapi import APIRouter
from pydantic import BaseModel
from agent.agent import run_agent

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str

@router.post("/chat")
async def chat(req: ChatRequest):
    response = run_agent(req.user_id, req.message)
    return {"reply": response}
