import openai
from typing import Dict
from .prompts import create_insight_prompt, create_goal_alignment_prompt

class OpenAIClient:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    async def generate_insights(self, data: Dict) -> Dict:
        """Generate insights using OpenAI's GPT model."""
        prompt = create_insight_prompt(data)

        response = await openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are an AI life coach analyzing user data to provide actionable insights."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    async def analyze_goal_alignment(self, goals: Dict, tasks: Dict) -> Dict:
        """Analyze alignment between goals and tasks."""
        prompt = create_goal_alignment_prompt(goals, tasks)

        response = await openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": "You are an AI coach analyzing goal-task alignment and providing optimization recommendations."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content
