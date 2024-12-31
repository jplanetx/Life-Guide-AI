import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from .core.config import Settings
from .api.tasks import router as tasks_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure rate limiting
limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    logger.info("Starting AI Coach API...")

    app = FastAPI(title="AI Coach API")
    app.state.limiter = limiter

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
        return {
            "status": "healthy",
            "services": {
                "notion": "connected",
                "openai": "ready"
            }
        }

    return app

app = create_app()