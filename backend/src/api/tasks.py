from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from ..services.notion_client import NotionClient, NotionClientError
from ..services.task_intelligence import TaskIntelligenceService
from ..core.config import Settings
import logging
import json

router = APIRouter()
settings = Settings()
notion_client = NotionClient(settings)
task_service = TaskIntelligenceService(
    notion_client=notion_client,
    openai_api_key=settings.OPENAI_API_KEY
)

logger = logging.getLogger(__name__)

@router.get("/api/tasks")
async def get_tasks(request: Request) -> List[Dict[str, Any]]:
    """Fetch all tasks from Notion with their properties."""
    try:
        logger.info("Attempting to fetch tasks from Notion...")
        # Simple fetch with no filters or processing
        return await notion_client.get_tasks()
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/api/tasks/{task_id}/properties")
async def update_task_properties(task_id: str, properties: Dict[str, Any]):
    """Update task properties in Notion."""
    try:
        await notion_client.update_task(task_id, properties)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/tasks/{task_id}/analyze")
async def analyze_task(task_id: str):
    """Get AI recommendations for task properties."""
    try:
        task = await notion_client.get_task(task_id)
        task_title = task['properties']['Name']['title'][0]['text']['content']

        analysis = await task_service.analyze_task(task_title)
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing task: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
