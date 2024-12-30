from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from datetime import datetime

from ..services.insights.engine import InsightEngine
from ..core.dependencies import get_notion_client, get_openai_client

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/generate")
async def generate_insights(
    insight_engine: InsightEngine = Depends(lambda: InsightEngine(
        get_notion_client(),
        get_openai_client()
    ))
) -> Dict:
    """Generate comprehensive insights across goals, tasks, and projects."""
    try:
        return await insight_engine.generate_insights()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_insight_history(
    insight_engine: InsightEngine = Depends(lambda: InsightEngine(
        get_notion_client(),
        get_openai_client()
    ))
) -> Dict:
    """Retrieve historical insights and track changes over time."""
    try:
        return await insight_engine.get_insight_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
