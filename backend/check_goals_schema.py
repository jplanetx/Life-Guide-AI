from notion_client import Client
import os
from dotenv import load_dotenv

# Load .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Initialize Notion client
notion = Client(auth=os.getenv('NOTION_API_KEY'))

# Retrieve goals database schema
try:
    response = notion.databases.retrieve(database_id=os.getenv('NOTION_GOALS_DATABASE_ID'))
    print("Current properties:", list(response['properties'].keys()))
except Exception as e:
    print(f"Error retrieving database schema: {e}")
