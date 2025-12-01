"""
Main application file for the Closet Management Application.
This file sets up the FastAPI application with all routes and configurations.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1 import auth, items
from backend.config.database import Base, engine

# Create FastAPI application
app = FastAPI(
    title="Closet Management App",
    version="1.0.0",
    description="API for managing clothing items in a virtual closet",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(items.router, prefix="/api/v1/items", tags=["items"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Closet Management App API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


Base.metadata.create_all(bind=engine)
