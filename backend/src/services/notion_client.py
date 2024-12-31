from typing import Dict, List, Optional, Union
from notion_client import Client as SyncClient
from notion_client import AsyncClient
from datetime import datetime

class NotionClient:
    def __init__(self, settings):
        self.client = AsyncClient(auth=settings.NOTION_API_KEY)
        self.sync_client = SyncClient(auth=settings.NOTION_API_KEY)
        self.tasks_db_id = settings.NOTION_TASKS_DATABASE_ID
        self.projects_db_id = settings.NOTION_PROJECTS_DATABASE_ID

    async def get_tasks(self, status: Optional[str] = None) -> List[Dict]:
        query = {}
        if status:
            query["filter"] = {
                "property": "Status",
                "status": {
                    "equals": status
                }
            }

        response = await self.client.databases.query(
            database_id=self.tasks_db_id,
            **query
        )
        return response["results"]

    async def get_projects(self) -> List[Dict]:
        response = await self.client.databases.query(
            database_id=self.projects_db_id
        )
        return response["results"]

    async def update_task(self, task_id: str, properties: Dict) -> Dict:
        return await self.client.pages.update(
            page_id=task_id,
            properties=properties
        )

    async def create_task(self, properties: Dict) -> Dict:
        return await self.client.pages.create(
            parent={"database_id": self.tasks_db_id},
            properties=properties
        )