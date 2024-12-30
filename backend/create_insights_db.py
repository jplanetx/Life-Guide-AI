from notion_client import Client
import os

# Initialize Notion client
notion = Client(auth='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')

# Database schema
properties = {
    "Title": {"title": {}},
    "Date": {"date": {}},
    "Brain Process": {
        "select": {
            "options": [
                {"name": "Pattern Recognition", "color": "blue"},
                {"name": "Decision Making", "color": "green"},
                {"name": "Learning", "color": "yellow"},
                {"name": "Memory Formation", "color": "purple"}
            ]
        }
    },
    "Type": {
        "select": {
            "options": [
                {"name": "Task Pattern", "color": "blue"},
                {"name": "Goal Progress", "color": "green"},
                {"name": "Behavior Pattern", "color": "purple"},
                {"name": "Recommendation", "color": "yellow"}
            ]
        }
    },
    "Content": {"rich_text": {}},
    "Impact Score": {"number": {"format": "number"}},
    "Action Items": {"rich_text": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Active", "color": "green"},
                {"name": "Archived", "color": "gray"}
            ]
        }
    }
}

# Create database
try:
    response = notion.databases.create(
        parent={"page_id": "0e8cefd185144f0ab7df0ba10c835542"},
        title=[{"type": "text", "text": {"content": "AI Coach Insights"}}],
        properties=properties
    )
    print(f"Database created with ID: {response['id']}")
except Exception as e:
    print(f"Error creating database: {e}")
