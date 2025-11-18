from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(
    title="ClosetManager Backend",
    description="API for managing closet inventory and user authentication",
    version="0.1.0",
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 setup for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Include routers for different API modules
# (These will be defined in separate files within the 'routers' directory)
# Example: from .routers import auth, closet, user
# app.include_router(auth.router)
# app.include_router(closet.router)
# app.include_router(user.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to ClosetManager Backend API"}
