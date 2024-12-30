from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    notion_api_key: str
    notion_tasks_database_id: str
    notion_areas_database_id: str
    notion_projects_database_id: str
    notion_insights_database_id: str
    notion_goals_database_id: str
    openai_api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False
