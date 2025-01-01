import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .core.config import validate_settings
from .api.tasks import router as tasks_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure rate limiting
limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    logger.info("Starting AI Coach API...")

    # Validate settings at startup
    try:
        settings = validate_settings()
        logger.info("Environment configuration validated successfully")
    except Exception as e:
        logger.error(f"Failed to validate environment configuration: {str(e)}")
        raise

    app = FastAPI(title="AI Coach API")
    app.state.limiter = limiter
    app.state.settings = settings  # Store settings in app state

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(tasks_router)

    @app.get("/health")
    @limiter.limit("5/minute")
    async def health_check(request: Request):
        try:
            # Test Notion connectivity
            from .services.notion_client import NotionClient
            notion = NotionClient(request.app.state.settings)
            await notion.client.users.me()
            notion_status = "connected"
        except Exception as e:
            logger.error(f"Notion health check failed: {str(e)}")
            notion_status = "disconnected"

        return {
            "status": "healthy",
            "services": {
                "notion": notion_status,
                "openai": "ready"
            },
            "environment": request.app.state.settings.environment
        }

    return app

app = create_app()
