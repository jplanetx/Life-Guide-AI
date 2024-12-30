import pytest
from datetime import datetime, timedelta
from src.services.insights.timeline_forecaster import TimelineForecaster

@pytest.fixture
def test_data():
    now = datetime.now()
    month_ago = now - timedelta(days=30)
    task_data = [
        {
            'id': 'task1',
            'Title': 'Test Task 1',
            'Category': 'Development',
            'Status': 'Completed',
            'StartDate': month_ago,
            'CompletionDate': now,
            'PlannedCompletionDate': month_ago + timedelta(days=2),
            'Dependencies': []
        },
        {
            'id': 'task2',
            'Title': 'Test Task 2',
            'Category': 'Development',
            'Status': 'Completed',
            'StartDate': None,
            'CompletionDate': now,
            'Type': 'Milestone',
            'Dependencies': ['task1']
        }
    ]
    return {'tasks': task_data, 'project': {'id': 'proj1', 'tasks': task_data}}

@pytest.fixture
def forecaster():
    return TimelineForecaster()

def test_completion_patterns_with_missing_data(forecaster, test_data):
    patterns = forecaster._analyze_completion_patterns(test_data)
    assert 'Development' in patterns
    assert patterns['Development']['mean_duration'] > 0

def test_milestone_forecasts_handles_missing_dates(forecaster, test_data):
    milestones = forecaster._forecast_milestones(test_data['project'], {
        'Development': {'mean_duration': 48}
    })
    assert len(milestones) > 0
    assert isinstance(milestones[0]['estimated_completion'], datetime)

def test_confidence_scoring_with_incomplete_data(forecaster, test_data):
    task = test_data['tasks'][0]
    dependencies = test_data['tasks'][1:]
    score = forecaster._calculate_confidence_score(task, dependencies)
    assert 0 <= score <= 1

def test_critical_path_with_sparse_data(forecaster, test_data):
    path = forecaster._calculate_critical_path(test_data['project'], {
        'Development': {'mean_duration': 48}
    })
    assert len(path) > 0
    assert 'duration' in path[0]
