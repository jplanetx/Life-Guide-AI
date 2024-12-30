from typing import Dict, List
from datetime import datetime

class ModuleAnalyzer:
    def analyze_modules(self, data: Dict) -> Dict:
        return {
            'structure': self._analyze_module_structure(data),
            'dependencies': self._analyze_module_dependencies(data),
            'progress': self._analyze_module_progress(data),
            'recommendations': self._generate_module_recommendations(data)
        }

    def _analyze_module_structure(self, data: Dict) -> Dict:
        projects = data['projects']
        tasks = data['tasks']

        modules = {}
        for project in projects:
            module_name = project.get('Module')
            if module_name:
                if module_name not in modules:
                    modules[module_name] = {
                        'projects': [],
                        'tasks': [],
                        'completion_rate': 0,
                        'dependencies': set(),
                        'resources': []
                    }
                modules[module_name]['projects'].append(project)
                modules[module_name]['tasks'].extend(
                    [t for t in tasks if t['Project'] == project['id']]
                )

        return self._calculate_module_metrics(modules)

    def _analyze_module_dependencies(self, data: Dict) -> List:
        modules = self._analyze_module_structure(data)
        dependencies = []

        for module_name, module_data in modules.items():
            module_deps = {
                'module': module_name,
                'upstream': self._get_upstream_dependencies(module_data),
                'downstream': self._get_downstream_dependencies(module_data),
                'critical_path': self._is_on_critical_path(module_data)
            }
            dependencies.append(module_deps)

        return dependencies

    def _analyze_module_progress(self, data: Dict) -> Dict:
        modules = self._analyze_module_structure(data)
        progress = {}

        for module_name, module_data in modules.items():
            progress[module_name] = {
                'completion': self._calculate_completion_rate(module_data),
                'velocity': self._calculate_module_velocity(module_data),
                'blockers': self._identify_module_blockers(module_data),
                'next_milestones': self._identify_next_milestones(module_data)
            }

        return progress

    def _generate_module_recommendations(self, data: Dict) -> List:
        modules = self._analyze_module_structure(data)
        progress = self._analyze_module_progress(data)
        dependencies = self._analyze_module_dependencies(data)

        recommendations = []
        for module_name in modules:
            module_rec = {
                'module': module_name,
                'priority_actions': self._identify_priority_actions(
                    modules[module_name],
                    progress[module_name]
                ),
                'resource_adjustments': self._suggest_resource_adjustments(
                    modules[module_name],
                    dependencies
                ),
                'risk_mitigation': self._identify_risk_mitigation(
                    modules[module_name],
                    progress[module_name]
                )
            }
            recommendations.append(module_rec)

        return recommendations
