from typing import Dict, List, Optional, Union
from notion_client import Client as SyncClient
from notion_client import AsyncClient
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class NotionClientError(Exception):
    """Custom exception for Notion client errors"""
    pass

class NotionClient:
    def __init__(self, settings):
        try:
            if not settings.NOTION_API_KEY:
                raise NotionClientError("Notion API key is missing")
            if not settings.NOTION_TASKS_DATABASE_ID:
                raise NotionClientError("Notion tasks database ID is missing")

            logger.info(f"Initializing Notion client with database ID: {settings.NOTION_TASKS_DATABASE_ID}")
            self.client = AsyncClient(auth=settings.NOTION_API_KEY)
            self.sync_client = SyncClient(auth=settings.NOTION_API_KEY)
            self.tasks_db_id = settings.NOTION_TASKS_DATABASE_ID
            self.projects_db_id = settings.NOTION_PROJECTS_DATABASE_ID

            logger.info("NotionClient initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize NotionClient: {str(e)}", exc_info=True)
            raise NotionClientError(f"Initialization failed: {str(e)}")

    async def get_tasks(self) -> List[Dict]:
        """Get tasks with extra debugging."""
        try:
            # 1. Verify database access and get schema
            logger.info(f"Attempting to retrieve database info for ID: {self.tasks_db_id}")
            db_info = await self.client.databases.retrieve(self.tasks_db_id)

            # 2. Log database properties
            logger.info("Database properties:")
            properties = db_info.get('properties', {})
            for prop_name, prop_info in properties.items():
                logger.info(f"Property '{prop_name}': type={prop_info.get('type')}")

            # 3. Attempt the simplest possible query
            logger.info("Attempting to query database with no filters...")
            try:
                response = await self.client.databases.query(
                    database_id=self.tasks_db_id
                )
                logger.info(f"Successfully retrieved {len(response.get('results', []))} results")

                # 4. Log first result if available
                if response.get('results'):
                    first_result = response['results'][0]
                    logger.info("First result structure:")
                    logger.info(json.dumps({
                        'id': first_result.get('id'),
                        'properties': first_result.get('properties')
                    }, indent=2))

                return response.get('results', [])

            except Exception as query_error:
                logger.error("Error during database query:", exc_info=True)
                logger.error(f"Query error details: {str(query_error)}")
                raise NotionClientError(f"Database query failed: {str(query_error)}")

        except Exception as e:
            logger.error(f"Error in get_tasks: {str(e)}", exc_info=True)
            raise NotionClientError(f"Failed to fetch tasks: {str(e)}")

    async def get_task(self, task_id: str) -> Dict:
        """Get a single task by ID."""
        try:
            if not task_id:
                raise NotionClientError("Task ID is required")

            logger.info(f"Retrieving task with ID: {task_id}")
            result = await self.client.pages.retrieve(page_id=task_id)

            if result:
                logger.info("Successfully retrieved task")
                logger.debug(f"Task data: {json.dumps(result, indent=2)}")
            return result

        except Exception as e:
            logger.error(f"Error fetching task {task_id}: {str(e)}", exc_info=True)
            raise NotionClientError(f"Failed to fetch task: {str(e)}")

    async def get_projects(self) -> List[Dict]:
        """Get projects with error handling."""
        try:
            logger.info(f"Querying projects database: {self.projects_db_id}")
            response = await self.client.databases.query(
                database_id=self.projects_db_id
            )
            return response.get("results", [])
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
            raise NotionClientError(f"Failed to fetch projects: {str(e)}")

    async def update_task(self, task_id: str, properties: Dict) -> Dict:
        """Update task with validation."""
        try:
            if not task_id:
                raise NotionClientError("Task ID is required")
            logger.info(f"Updating task {task_id} with properties: {json.dumps(properties, indent=2)}")
            return await self.client.pages.update(
                page_id=task_id,
                properties=properties
            )
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {str(e)}", exc_info=True)
            raise NotionClientError(f"Failed to update task: {str(e)}")

    async def create_task(self, properties: Dict) -> Dict:
        """Create task with validation."""
        try:
            if not properties:
                raise NotionClientError("Properties are required")
            logger.info(f"Creating task with properties: {json.dumps(properties, indent=2)}")
            return await self.client.pages.create(
                parent={"database_id": self.tasks_db_id},
                properties=properties
            )
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}", exc_info=True)
            raise NotionClientError(f"Failed to create task: {str(e)}")
