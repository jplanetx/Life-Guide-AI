from ..services.notion.client import NotionClient
from ..services.openai.client import OpenAIClient
import os

def get_notion_client() -> NotionClient:
    return NotionClient(os.getenv('NOTION_API_KEY'))

def get_openai_client() -> OpenAIClient:
    return OpenAIClient(os.getenv('OPENAI_API_KEY'))
