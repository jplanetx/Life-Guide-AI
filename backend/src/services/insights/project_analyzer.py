from typing import Dict, List
from datetime import datetime

class ProjectAnalyzer:
    def analyze_projects(self, data: Dict) -> Dict:
        """Analyze project data and relationships."""
        return {
            'alignment': self._analyze_goal_project_alignment(data),
            'dependencies': self._analyze_project_dependencies(data),
            'resources': self._analyze_resource_allocation(data),
            'bottlenecks': self._identify_bottlenecks(data)
        }

    def _analyze_goal_project_alignment(self, data: Dict) -> Dict:
        goals = data['goals']
        projects = data['projects']

        alignment = {}
        for goal in goals:
            related_projects = [p for p in projects if p['Goals'] and goal['id'] in p['Goals']]
            alignment[goal['id']] = {
                'project_count': len(related_projects),
                'coverage': self._calculate_goal_coverage(goal, related_projects),
                'gaps': self._identify_coverage_gaps(goal, related_projects)
            }
        return alignment

    def _analyze_project_dependencies(self, data: Dict) -> List:
        projects = data['projects']
        dependencies = []

        for project in projects:
            if project.get('Dependencies'):
                dep_chain = self._trace_dependency_chain(project, projects)
                if self._is_critical_path(dep_chain):
                    dependencies.append({
                        'chain': dep_chain,
                        'impact': self._calculate_dependency_impact(dep_chain),
                        'risks': self._identify_dependency_risks(dep_chain)
                    })
        return dependencies

    def _analyze_resource_allocation(self, data: Dict) -> Dict:
        projects = data['projects']
        tasks = data['tasks']

        return {
            'time_allocation': self._analyze_time_distribution(projects, tasks),
            'effort_balance': self._analyze_effort_distribution(projects),
            'concurrent_load': self._calculate_concurrent_projects(),
            'optimization_opportunities': self._identify_resource_optimizations(projects)
        }

    def _identify_bottlenecks(self, data: Dict) -> List:
        projects = data['projects']
        tasks = data['tasks']

        bottlenecks = []
        for project in projects:
            project_tasks = [t for t in tasks if t['Project'] == project['id']]
            blockers = self._analyze_project_blockers(project, project_tasks)
            if blockers:
                bottlenecks.append({
                    'project_id': project['id'],
                    'blockers': blockers,
                    'impact': self._calculate_blocker_impact(blockers),
                    'suggestions': self._generate_bottleneck_solutions(blockers)
                })
        return bottlenecks

    def _calculate_goal_coverage(self, goal: Dict, projects: List) -> float:
        total_objectives = len(goal.get('Success Criteria', '').split('\n'))
        covered_objectives = 0

        for project in projects:
            project_objectives = set(obj.strip() for obj in project.get('Objectives', '').split('\n'))
            goal_objectives = set(obj.strip() for obj in goal.get('Success Criteria', '').split('\n'))
            covered_objectives += len(project_objectives.intersection(goal_objectives))

        return covered_objectives / total_objectives if total_objectives > 0 else 0

    def _identify_coverage_gaps(self, goal: Dict, projects: List) -> List:
        goal_objectives = set(obj.strip() for obj in goal.get('Success Criteria', '').split('\n'))
        covered_objectives = set()

        for project in projects:
            project_objectives = set(obj.strip() for obj in project.get('Objectives', '').split('\n'))
            covered_objectives.update(project_objectives)

        return list(goal_objectives - covered_objectives)

    def _analyze_project_blockers(self, project: Dict, tasks: List) -> List:
        return [
            {
                'task_id': task['id'],
                'blocker_type': self._categorize_blocker(task),
                'duration': self._calculate_blocker_duration(task),
                'dependencies': self._get_task_dependencies(task)
            }
            for task in tasks
            if task['Status'] == 'Blocked'
        ]
