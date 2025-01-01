from typing import Dict, Any, Tuple, Optional
import openai
from .notion_client import NotionClient
import logging
import re

logger = logging.getLogger(__name__)

class TaskIntelligenceService:
    def __init__(self, notion_client: NotionClient, openai_api_key: str):
        self.notion_client = notion_client
        openai.api_key = openai_api_key

    async def analyze_task(self, task_title: str) -> Dict[str, Any]:
        """Analyze a task and suggest properties."""
        try:
            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": """You are an AI task analyst.
                    Analyze tasks and suggest appropriate importance, urgency,
                    and other relevant properties."""},
                    {"role": "user", "content": f"Analyze this task: {task_title}"}
                ],
                temperature=0.7,
            )

            return {
                "analysis": response.choices[0].message.content,
                "suggested_properties": self._extract_properties(
                    response.choices[0].message.content
                )
            }
        except Exception as e:
            logger.error(f"Error analyzing task: {str(e)}", exc_info=True)
            raise

    async def process_chat(
        self,
        conversation: str,
        task_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[str, Optional[Dict[str, Any]]]:
        """Process chat messages and return response with potential task updates."""
        try:
            system_prompt = """You are an AI task management assistant with access
            to the user's Notion tasks. You can provide insights, suggestions,
            and help optimize task properties. When discussing tasks:
            1. Provide clear, actionable advice
            2. Consider context and priorities
            3. Suggest property updates when appropriate
            4. Explain your reasoning

            If suggesting task property updates, format them as:
            [TASK_UPDATE]
            importance: High/Medium/Low
            urgency: High/Medium/Low
            status: Not Started/In Progress/Completed
            [/TASK_UPDATE]
            """

            response = await openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation}
                ],
                temperature=0.7,
            )

            ai_response = response.choices[0].message.content
            task_updates = self._extract_task_updates(ai_response)

            # Clean the response by removing the task update block
            clean_response = ai_response.replace(
                self._find_task_update_block(ai_response),
                ""
            ).strip()

            return clean_response, task_updates

        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}", exc_info=True)
            raise

    def _extract_properties(self, analysis: str) -> Dict[str, str]:
        """Extract suggested properties from analysis text."""
        properties = {}

        # Look for importance
        importance_match = re.search(
            r'importance:?\s*(high|medium|low)',
            analysis.lower()
        )
        if importance_match:
            properties['importance'] = importance_match.group(1).capitalize()

        # Look for urgency
        urgency_match = re.search(
            r'urgency:?\s*(high|medium|low)',
            analysis.lower()
        )
        if urgency_match:
            properties['urgency'] = urgency_match.group(1).capitalize()

        # Look for status
        status_match = re.search(
            r'status:?\s*(not started|in progress|completed)',
            analysis.lower()
        )
        if status_match:
            properties['status'] = status_match.group(1).capitalize()

        return properties

    def _find_task_update_block(self, text: str) -> str:
        """Find the task update block in the text."""
        match = re.search(
            r'\[TASK_UPDATE\].*?\[/TASK_UPDATE\]',
            text,
            re.DOTALL
        )
        return match.group(0) if match else ""

    def _extract_task_updates(self, text: str) -> Optional[Dict[str, str]]:
        """Extract task updates from the formatted block in the text."""
        update_block = self._find_task_update_block(text)
        if not update_block:
            return None

        updates = {}

        # Extract properties
        for line in update_block.split('\n'):
            line = line.strip().lower()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key in ['importance', 'urgency', 'status']:
                    updates[key] = value.capitalize()

        return updates if updates else None
