import pytest
from datetime import datetime, timedelta
from src.services.insights.ml_patterns import MLPatternAnalyzer

@pytest.fixture
def test_data():
    now = datetime.now()
    return {
        'tasks': [
            {
                'id': 'task1',
                'Status': 'Completed',
                'StartDate': now - timedelta(hours=2),
                'CompletionDate': now,
                'Category': 'Development',
                'Quality': 0.8
            },
            {
                'id': 'task2',
                'Status': 'Completed',
                'StartDate': now - timedelta(hours=4),
                'CompletionDate': now - timedelta(hours=2),
                'Category': 'Development',
                'Quality': 0.9
            }
        ],
        'goals': [
            {
                'id': 'goal1',
                'Status': 'Completed',
                'Category': 'Development'
            }
        ]
    }

@pytest.fixture
def ml_analyzer():
    return MLPatternAnalyzer()

def test_productivity_cycles(ml_analyzer, test_data):
    patterns = ml_analyzer.analyze_patterns(test_data)
    assert 'productivity' in patterns
    assert 'peak_hours' in patterns['productivity']
    assert 'task_velocity' in patterns['productivity']

def test_success_factors(ml_analyzer, test_data):
    patterns = ml_analyzer.analyze_patterns(test_data)
    assert 'success_factors' in patterns
    assert 'task_success_patterns' in patterns['success_factors']

def test_behavior_patterns(ml_analyzer, test_data):
    patterns = ml_analyzer.analyze_patterns(test_data)
    assert 'behavior' in patterns
    assert 'focus_periods' in patterns['behavior']
    assert 'adaptability_score' in patterns['behavior']

def test_focus_score_calculation(ml_analyzer):
    tasks = [
        {'Status': 'Completed', 'Quality': 0.8},
        {'Status': 'Completed', 'Quality': 0.9}
    ]
    score = ml_analyzer._calculate_focus_score(tasks)
    assert 0 <= score <= 1
