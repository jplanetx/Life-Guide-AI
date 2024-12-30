from typing import Dict, Any
from openai import OpenAI

class TaskIntelligenceService:
    def __init__(self, notion_client, openai_api_key: str):
        self.notion = notion_client
        self.client = OpenAI(api_key=openai_api_key, max_retries=2)

    async def analyze_task(self, task_title: str) -> Dict[str, Any]:
        """Analyze task and suggest properties."""
        prompt = f"""Analyze this task and suggest appropriate properties:
Task: {task_title}

Provide suggestions for:
1. Priority level (High/Medium/Low)
2. Estimated time required (in hours)
3. Energy level needed (High/Medium/Low)
4. Best time of day to work on it
5. Related project categories

Format as JSON with explanations.
"""
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a task analysis expert helping prioritize and organize work."},
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                'task_title': task_title,
                'analysis': completion.choices[0].message.content
            }
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return {
                'task_title': task_title,
                'error': str(e)
            }
