from contextlib import asynccontextmanager
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging

from app.core.config import settings
from app.db.session import SessionLocal, engine, get_db
from app.domain.models import Base, Cafe
from app.api.routers import cafes, employees
from app.core.exception_handlers import register_handlers

logger = logging.getLogger(__name__)

# Import the seed function
from seed import seed_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events for the FastAPI app."""
    
    # Startup event
    print("[Startup] Checking if database needs seeding...")
    db = SessionLocal()
    try:
        cafe_count = db.query(Cafe).count()
        if cafe_count == 0:
            print("[Startup] Database is empty. Seeding with sample data...")
            seed_database()  # Seed function opens its own session
            print("[Startup] Seeding complete!")
        else:
            print(f"[Startup] Database already has {cafe_count} cafes. Skipping seed.")
    except Exception as e:
        logger.error(f"[Startup] Error during seeding check: {e}")
    finally:
        db.close()
    
    yield  # Run the app
    
    # Shutdown event
    print("[Shutdown] Application shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="GIC Cafe/Employee API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,  # Attach lifespan here
    )
    
    # CORS
    allow_origins = settings.CORS_ORIGINS or ["https://deploy-cafe-manager.onrender.com"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Error handlers
    register_handlers(app)

    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
        print("[Startup] Database tables created or verified.")
    except Exception as e:
        print(f"[Startup] Skipped metadata.create_all: {e}")

    # Routers
    app.include_router(cafes.router, prefix=settings.API_PREFIX)
    app.include_router(employees.router, prefix=settings.API_PREFIX)
    
    # Mount static files for uploads (if exists)
    uploads_path = Path("uploads")
    if uploads_path.exists() and uploads_path.is_dir():
        app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    
    # Health endpoint
    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
