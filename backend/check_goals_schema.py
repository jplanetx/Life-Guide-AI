from notion_client import Client

notion = Client(auth='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')

response = notion.databases.retrieve(database_id="629eb59275a44d19ac656fe1fe4fb052")
print("Current properties:", list(response['properties'].keys()))
