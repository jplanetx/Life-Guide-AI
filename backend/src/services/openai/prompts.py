from typing import Dict, List

def create_insight_prompt(data: Dict) -> str:
    return f"""Analyze the following user data and provide actionable insights:

Task Patterns:
- Completion Rate: {data['tasks']['completion_rate']}
- Peak Productivity: {data['tasks']['peak_productivity_times']}
- Blockers: {data['tasks']['common_blockers']}

Goal Progress:
- Progress Metrics: {data['goals']['goal_progress']}
- Goal Alignment: {data['goals']['goal_alignment']}

Behavioral Patterns:
- Consistency Score: {data['behavior']['consistency']}
- Adaptation Level: {data['behavior']['adaptation']}

Generate:
1. Key patterns and correlations
2. Specific, actionable recommendations
3. Areas for improvement
4. Progress acknowledgment
5. Next steps prioritized by impact

Format response as JSON with keys: summary, recommendations, action_items"""

def create_goal_alignment_prompt(goals: List[Dict], tasks: List[Dict]) -> str:
    return f"""Analyze goal-task alignment for the following:

Goals: {goals}
Tasks: {tasks}

Evaluate:
1. Task-goal alignment strength
2. Goal progress indicators
3. Missing activities for goals
4. Potential goal conflicts
5. Resource allocation efficiency

Format response as JSON with keys: alignment_score, gaps, recommendations"""
