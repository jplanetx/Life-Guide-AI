import json
from typing import Dict, List
from datetime import datetime
import os
from .ml_patterns import MLPatternAnalyzer

class InsightEngine:
    def __init__(self, notion_client, openai_client):
        self.notion = notion_client
        self.openai = openai_client
        self.ml_analyzer = MLPatternAnalyzer()

    async def generate_insights(self) -> Dict:
        data = await self._gather_data()
        base_patterns = self._analyze_patterns(data)
        ml_patterns = self.ml_analyzer.analyze_patterns(data)
        return await self._synthesize_insights({**base_patterns, 'ml_patterns': ml_patterns})

    async def _gather_data(self) -> Dict:
        goals = await self.notion.get_database(os.getenv('NOTION_GOALS_DATABASE_ID'))
        tasks = await self.notion.get_database(os.getenv('NOTION_TASKS_DATABASE_ID'))
        projects = await self.notion.get_database(os.getenv('NOTION_PROJECTS_DATABASE_ID'))
        return {'goals': goals, 'tasks': tasks, 'projects': projects}

    def _analyze_patterns(self, data: Dict) -> Dict:
        return {
            'completion_patterns': self._analyze_completion_patterns(data),
            'goal_progress': self._analyze_goal_progress(data),
            'blockers': self._identify_blockers(data),
            'productivity_patterns': self._analyze_productivity(data)
        }

    def _create_insight_prompt(self, patterns: Dict) -> str:
        ml_insights = patterns.get('ml_patterns', {})
        return f"""Analyze the following patterns and provide strategic insights:

Task Completion:
- Completion Rate: {patterns['completion_patterns']['completion_rate']}
- Peak Hours: {ml_insights.get('productivity', {}).get('peak_hours', [])}
- Task Velocity: {ml_insights.get('productivity', {}).get('task_velocity', 0)}

Goal Progress:
{json.dumps(patterns['goal_progress'], indent=2)}

Success Factors:
{json.dumps(ml_insights.get('success_factors', {}), indent=2)}

Behavior Patterns:
- Focus Periods: {ml_insights.get('behavior', {}).get('focus_periods', [])}
- Adaptability: {ml_insights.get('behavior', {}).get('adaptability_score', 0)}

Provide insights formatted as JSON with keys: summary, patterns, recommendations, priorities"""

    async def _synthesize_insights(self, patterns: Dict) -> Dict:
        prompt = self._create_insight_prompt(patterns)
        response = await self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI life coach analyzing patterns to provide actionable insights."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        content = response.get('choices', [{}])[0].get('content', '{}')
        return json.loads(content)

    # Previous methods remain unchanged
