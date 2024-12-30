from typing import Dict, List
import os
from notion_client import Client

class NotionClient:
    def __init__(self, auth_token: str):
        self.client = Client(auth=auth_token)

    async def create_database(self, parent_id: str, schema: Dict) -> str:
        """Create a new database with given schema."""
        response = self.client.databases.create(
            parent={"page_id": parent_id},
            title=[{
                "type": "text",
                "text": {"content": schema["name"]}
            }],
            properties=schema["properties"]
        )
        return response["id"]
