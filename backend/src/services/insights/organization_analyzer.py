from typing import Dict, List
from datetime import datetime

class OrganizationAnalyzer:
    def analyze_structure(self, data: Dict) -> Dict:
        return {
            'clusters': self._identify_task_clusters(data),
            'dependencies': self._analyze_dependencies(data),
            'suggested_modules': self._suggest_modules(data)
        }

    def _identify_task_clusters(self, data: Dict) -> List:
        """Identify natural groupings of tasks based on relationships and metadata."""
        tasks = data['tasks']
        projects = data['projects']

        clusters = []
        for project in projects:
            project_tasks = [t for t in tasks if t.get('Project') == project['id']]

            # Group by common properties, dependencies, and objectives
            task_groups = self._group_related_tasks(project_tasks)
            if len(task_groups) > 1:  # Multiple distinct groups suggest potential module
                clusters.append({
                    'project_id': project['id'],
                    'task_groups': task_groups,
                    'common_traits': self._identify_common_traits(task_groups)
                })

        return clusters

    def _suggest_modules(self, data: Dict) -> List[Dict]:
        """Generate module suggestions based on task clusters and project structure."""
        clusters = self._identify_task_clusters(data)

        suggested_modules = []
        for cluster in clusters:
            if len(cluster['task_groups']) >= 2:  # Minimum complexity for module
                suggested_modules.append({
                    'name': self._generate_module_name(cluster),
                    'description': self._generate_module_description(cluster),
                    'tasks': [task['id'] for group in cluster['task_groups'] for task in group],
                    'rationale': self._generate_module_rationale(cluster)
                })

        return suggested_modules

    def _group_related_tasks(self, tasks: List) -> List:
        """Group tasks based on shared attributes and relationships."""
        groups = {}
        for task in tasks:
            key = self._generate_grouping_key(task)
            if key not in groups:
                groups[key] = []
            groups[key].append(task)

        return list(groups.values())

    def _generate_grouping_key(self, task: Dict) -> str:
        """Create a grouping key based on task attributes."""
        components = [
            task.get('Category', ''),
            task.get('Status', ''),
            str(task.get('Priority', '')),
            str(task.get('Dependencies', []))
        ]
        return '|'.join(components)

    def _identify_common_traits(self, task_groups: List) -> Dict:
        """Identify common characteristics within task groups."""
        all_tasks = [task for group in task_groups for task in group]

        return {
            'categories': self._get_common_values(all_tasks, 'Category'),
            'dependencies': self._get_common_dependencies(all_tasks),
            'priorities': self._get_common_values(all_tasks, 'Priority')
        }

    def _generate_module_name(self, cluster: Dict) -> str:
        """Generate a descriptive name for the suggested module."""
        common_traits = cluster['common_traits']
        primary_category = common_traits['categories'][0] if common_traits['categories'] else 'Misc'
        return f"{primary_category} Module"

    def _generate_module_description(self, cluster: Dict) -> str:
        """Generate a description explaining the module's purpose."""
        traits = cluster['common_traits']
        return f"Module focusing on {traits['categories'][0]} tasks with {len(cluster['task_groups'])} distinct task groups"

    def _generate_module_rationale(self, cluster: Dict) -> str:
        """Generate explanation for why these tasks should be a module."""
        return f"Tasks share common {', '.join(cluster['common_traits'].keys())} and natural grouping patterns"
