from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from ..services.notion_client import NotionClient
from ..services.task_intelligence import TaskIntelligenceService
from ..core.config import Settings
from pydantic import BaseModel
import logging

router = APIRouter()
settings = Settings()
notion_client = NotionClient(settings)
task_service = TaskIntelligenceService(
    notion_client=notion_client,
    openai_api_key=settings.OPENAI_API_KEY
)

logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    taskId: str = None
    context: str = ""

@router.post("/api/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Process chat messages and return AI response with potential task updates."""
    try:
        # Get task context if taskId is provided
        task_context = ""
        task_data = None
        if request.taskId:
            task_data = await notion_client.get_task(request.taskId)
            task_context = f"\nTask Context: {task_data}"

        # Prepare the conversation history
        conversation = request.context + "\n" if request.context else ""
        for msg in request.messages:
            conversation += f"{msg.role}: {msg.content}\n"

        # Get AI response and potential task updates
        response, task_updates = await task_service.process_chat(
            conversation=conversation,
            task_data=task_data
        )

        return {
            "response": response,
            "taskUpdates": task_updates
        }

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
