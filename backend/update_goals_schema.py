from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv('NOTION_API_KEY'))
GOALS_DB_ID = os.getenv('NOTION_GOALS_DATABASE_ID')

updates = {
    "Status": {
        "select": {
            "options": [
                {"name": "Not Started", "color": "gray"},
                {"name": "In Progress", "color": "yellow"},
                {"name": "Completed", "color": "green"},
                {"name": "Blocked", "color": "red"},
                {"name": "Deferred", "color": "purple"}
            ]
        }
    },
    "Category": {
        "select": {
            "options": [
                {"name": "Career", "color": "blue"},
                {"name": "Personal", "color": "green"},
                {"name": "Health", "color": "red"},
                {"name": "Learning", "color": "yellow"},
                {"name": "Financial", "color": "orange"},
                {"name": "Relationships", "color": "pink"}
            ]
        }
    },
    "Progress": {"number": {"format": "percent"}},
    "Effort": {
        "select": {
            "options": [
                {"name": "Small", "color": "green"},
                {"name": "Medium", "color": "yellow"},
                {"name": "Large", "color": "red"}
            ]
        }
    }
}

try:
    response = notion.databases.update(
        database_id=GOALS_DB_ID,
        properties=updates
    )
    print("Goals database updated successfully")
except Exception as e:
    print(f"Error updating database: {e}")
