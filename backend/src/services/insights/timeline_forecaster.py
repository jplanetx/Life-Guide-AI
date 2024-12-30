from typing import Dict, List, Union
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

class TimelineForecaster:
    def __init__(self):
        self.reliability_threshold = 0.6

    def _analyze_completion_patterns(self, data: Dict) -> Dict:
        tasks = data.get('tasks', [])
        by_category = defaultdict(list)

        for task in tasks:
            if (category := task.get('Category')) and task.get('StartDate') and task.get('CompletionDate'):
                duration = (task['CompletionDate'] - task['StartDate']).total_seconds() / 3600
                by_category[category].append(duration)

        return {
            category: {
                'mean_duration': float(np.mean(durations)),
                'std_duration': float(np.std(durations)) if len(durations) > 1 else 0,
                'reliability': len(durations) / len(tasks) if tasks else 0
            }
            for category, durations in by_category.items() if durations
        }

    def _calculate_critical_path(self, project: Dict, durations: Dict) -> List[Dict]:
        tasks = project.get('tasks', [])
        if not tasks:
            return []

        graph = self._build_dependency_graph(tasks)
        path = []
        current_task = next((t for t in tasks if not t.get('Dependencies')), None)

        while current_task:
            duration = durations.get(current_task.get('Category', ''), {}).get('mean_duration', 0)
            path.append({
                'task_id': current_task['id'],
                'duration': duration
            })

            # Find next task in chain
            next_tasks = [t for t in tasks if current_task['id'] in t.get('Dependencies', [])]
            current_task = next_tasks[0] if next_tasks else None

        return path

    def _forecast_milestones(self, project: Dict, durations: Dict) -> List[Dict]:
        tasks = project.get('tasks', [])
        if not tasks:
            return []

        milestones = []
        for task in tasks:
            if task.get('Type') == 'Milestone':
                deps = [t for t in tasks if t['id'] in task.get('Dependencies', [])]
                completion_date = self._estimate_milestone_completion(task, deps, durations)
                confidence = self._calculate_confidence_score(task, deps)

                milestones.append({
                    'id': task['id'],
                    'name': task.get('Title', ''),
                    'estimated_completion': completion_date,
                    'confidence': confidence
                })
        return milestones

    def _calculate_confidence_score(self, task: Dict, dependencies: List[Dict]) -> float:
        if not task:
            return 0.0

        base_score = 0.7
        if not task.get('StartDate'):
            base_score *= 0.8
        if not task.get('PlannedCompletionDate'):
            base_score *= 0.8

        blocked_deps = sum(1 for d in dependencies if d.get('Status') == 'Blocked')
        if blocked_deps:
            base_score *= (1 - (0.1 * blocked_deps))

        return max(min(base_score, 1.0), 0.0)

    def _build_dependency_graph(self, tasks: Union[List[Dict], List[str]]) -> Dict:
        graph = defaultdict(list)
        if not tasks or not isinstance(tasks[0], dict):
            return {}

        for task in tasks:
            for dep_id in task.get('Dependencies', []):
                graph[dep_id].append(task['id'])
        return dict(graph)

    def _estimate_milestone_completion(self, task: Dict, dependencies: List[Dict], durations: Dict) -> datetime:
        total_duration = sum(
            durations.get(dep.get('Category', ''), {}).get('mean_duration', 0)
            for dep in dependencies
        )
        return datetime.now() + timedelta(hours=total_duration)
