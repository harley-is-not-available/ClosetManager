from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import auth, items, upload
from .config.database import Base, engine
from .config.settings import settings

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Closet Manager API",
    description="API for managing clothing items in a closet",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["upload"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Closet Manager API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
