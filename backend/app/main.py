from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import SessionLocal
from app.domain.models import Cafe
from app.api.routers import cafes, employees

# Import the seed function
from seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("[Startup] Checking if database needs seeding...")
    db = SessionLocal()
    try:
        cafe_count = db.query(Cafe).count()
        if cafe_count == 0:
            print("[Startup] Database is empty. Seeding with sample data...")
            seed_database()
            print("[Startup] Seeding complete!")
        else:
            print(f"[Startup] Database already has {cafe_count} cafes. Skipping seed.")
    finally:
        db.close()
    
    yield  # Run the app
    
    # Shutdown event (optional cleanup)
    print("[Shutdown] Application shutting down...")

def create_app() -> FastAPI:
    app = FastAPI(
        title="GIC Cafe/Employee API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
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

    # Routers
    app.include_router(cafes.router, prefix=settings.API_PREFIX)
    app.include_router(employees.router, prefix=settings.API_PREFIX)
    uploads_path = Path("uploads")
    if uploads_path.exists() and uploads_path.is_dir():
        app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
    
    # Seed database immediately when app loads
    try:
        db = next(get_db())
        seed_database(db)
    except Exception as e:
        logger.error(f"Seeding failed: {e}")

    # Health endpoint
    @app.get("/health", tags=["system"])
    def health():
        return {"status": "ok"}

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        # Avoid crashing if migrations manage the schema
        print(f"[startup] Skipped metadata.create_all: {e}")

    return app

app = create_app()
