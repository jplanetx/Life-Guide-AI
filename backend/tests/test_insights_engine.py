import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock
from src.services.insights.engine import InsightEngine

@pytest.fixture
def mock_data():
    return {
        'goals': [{'id': 'goal1', 'Status': 'In Progress', 'Progress': 60}],
        'tasks': [{'id': 'task1', 'Status': 'Completed', 'Related Goals': ['goal1']}],
        'projects': []
    }

@pytest.fixture
def mock_response():
    return {
        'choices': [{
            'content': '{"summary": "test", "patterns": [], "recommendations": [], "priorities": []}'
        }]
    }

@pytest.fixture
def insight_engine():
    notion_client = AsyncMock()
    openai_client = AsyncMock()
    return InsightEngine(notion_client, openai_client)

@pytest.mark.asyncio
async def test_synthesize_insights(insight_engine, mock_data, mock_response):
    patterns = insight_engine._analyze_patterns(mock_data)
    insight_engine.openai.chat.completions.create.return_value = mock_response
    insights = await insight_engine._synthesize_insights(patterns)
    assert isinstance(insights, dict)

@pytest.mark.asyncio
async def test_generate_insights_integration(insight_engine, mock_data, mock_response):
    async def mock_get_database(id):
        return mock_data['goals']

    insight_engine.notion.get_database = AsyncMock(side_effect=mock_get_database)
    insight_engine.openai.chat.completions.create.return_value = mock_response
    insights = await insight_engine.generate_insights()
    assert isinstance(insights, dict)
