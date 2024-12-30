from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from ..services.life_coach.service import LifeCoachService
from ..core.dependencies import get_notion_client, get_openai_client

router = APIRouter(prefix="/life-coach", tags=["life-coach"])

@router.get("/insights/{user_id}")
async def get_insights(
    user_id: str,
    life_coach: LifeCoachService = Depends(lambda: LifeCoachService(
        get_notion_client(),
        get_openai_client()
    ))
) -> Dict:
    """Get personalized insights and recommendations."""
    try:
        return await life_coach.gather_insights(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/goals/{user_id}")
async def set_goal(
    user_id: str,
    goal: Dict,
    life_coach: LifeCoachService = Depends(lambda: LifeCoachService(
        get_notion_client(),
        get_openai_client()
    ))
):
    """Set a new goal for tracking."""
    try:
        return await life_coach.set_goal(user_id, goal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
