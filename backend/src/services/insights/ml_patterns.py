from typing import Dict, List
import numpy as np
from datetime import datetime, time
from collections import defaultdict

class MLPatternAnalyzer:
    def analyze_patterns(self, historical_data: Dict) -> Dict:
        productivity_patterns = self._analyze_productivity_cycles(historical_data)
        success_patterns = self._analyze_success_factors(historical_data)
        behavior_patterns = self._analyze_behavior_patterns(historical_data)

        return {
            'productivity': productivity_patterns,
            'success_factors': success_patterns,
            'behavior': behavior_patterns
        }

    def _analyze_productivity_cycles(self, data: Dict) -> Dict:
        tasks = data.get('tasks', [])
        completed_tasks = [t for t in tasks if t.get('Status') == 'Completed']

        time_patterns = defaultdict(list)
        for task in completed_tasks:
            completion_time = task.get('CompletionDate')
            if completion_time:
                hour = completion_time.hour
                time_patterns[hour].append(task)

        peak_hours = sorted(
            time_patterns.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:3]

        return {
            'peak_hours': [hour for hour, _ in peak_hours],
            'task_velocity': self._calculate_task_velocity(completed_tasks),
            'optimal_duration': self._calculate_optimal_duration(completed_tasks)
        }

    def _analyze_success_factors(self, data: Dict) -> Dict:
        tasks = data.get('tasks', [])
        goals = data.get('goals', [])

        successful_tasks = [t for t in tasks if t.get('Status') == 'Completed']
        successful_goals = [g for g in goals if g.get('Status') == 'Completed']

        task_factors = {
            'categories': self._extract_common_categories(successful_tasks),
            'completion_times': self._extract_completion_patterns(successful_tasks),
            'quality_factors': self._extract_quality_factors(successful_tasks)
        }

        goal_factors = {
            'categories': self._extract_common_categories(successful_goals),
            'success_rate': len(successful_goals) / len(goals) if goals else 0
        }

        return {
            'task_success_patterns': task_factors,
            'goal_success_patterns': goal_factors
        }

    def _extract_common_categories(self, items: List) -> Dict:
        categories = defaultdict(int)
        for item in items:
            if cat := item.get('Category'):
                categories[cat] += 1
        return dict(categories)

    def _extract_completion_patterns(self, tasks: List) -> Dict:
        patterns = defaultdict(int)
        for task in tasks:
            if start := task.get('StartDate'):
                hour = start.hour
                patterns[hour] += 1
        return dict(patterns)

    def _extract_quality_factors(self, tasks: List) -> Dict:
        quality_scores = [t.get('Quality', 0) for t in tasks]
        return {
            'average': np.mean(quality_scores) if quality_scores else 0,
            'high_quality_count': sum(1 for score in quality_scores if score > 0.8)
        }

    def _analyze_behavior_patterns(self, data: Dict) -> Dict:
        tasks = data.get('tasks', [])
        focus_periods = self._identify_focus_periods(tasks)
        procrastination_patterns = self._identify_procrastination_triggers(tasks)

        return {
            'focus_periods': focus_periods,
            'procrastination_triggers': procrastination_patterns,
            'adaptability_score': self._calculate_adaptability(tasks)
        }

    def _identify_focus_periods(self, tasks: List) -> List[Dict]:
        focus_periods = []
        for task in tasks:
            if (start := task.get('StartDate')) and (end := task.get('CompletionDate')):
                focus_periods.append({
                    'start': start,
                    'end': end,
                    'focus_score': self._calculate_focus_score([task])
                })
        return focus_periods

    def _identify_procrastination_triggers(self, tasks: List) -> List[str]:
        delayed_tasks = [t for t in tasks if t.get('Status') == 'Delayed']
        triggers = defaultdict(int)
        for task in delayed_tasks:
            if category := task.get('Category'):
                triggers[category] += 1
        return [k for k, v in sorted(triggers.items(), key=lambda x: x[1], reverse=True)]

    def _calculate_adaptability(self, tasks: List) -> float:
        if not tasks:
            return 0.0
        completed_on_time = sum(1 for t in tasks if t.get('Status') == 'Completed' and not t.get('Delayed', False))
        return completed_on_time / len(tasks)

    def _calculate_task_velocity(self, tasks: List) -> float:
        if not tasks:
            return 0.0
        time_diffs = []
        for i in range(1, len(tasks)):
            if (cur := tasks[i].get('CompletionDate')) and (prev := tasks[i-1].get('CompletionDate')):
                time_diffs.append((cur - prev).total_seconds() / 3600)
        return np.mean(time_diffs) if time_diffs else 0.0

    def _calculate_optimal_duration(self, tasks: List) -> Dict:
        durations = defaultdict(list)
        for task in tasks:
            if (start := task.get('StartDate')) and (end := task.get('CompletionDate')):
                duration = (end - start).total_seconds() / 3600
                if category := task.get('Category'):
                    durations[category].append(duration)
        return {k: float(np.median(v)) for k, v in durations.items()}

    def _calculate_focus_score(self, tasks: List) -> float:
        if not tasks:
            return 0.0
        completed = len([t for t in tasks if t.get('Status') == 'Completed'])
        quality_scores = [float(t.get('Quality', 0)) for t in tasks if t.get('Quality') is not None]

        completion_rate = completed / len(tasks)
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

        return (completion_rate * 0.6) + (avg_quality * 0.4)
