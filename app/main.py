from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import auth, chat, user, feedback, subjects, dashboard, files

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="STEAMX API",
    description="Backend API for STEAMX - AI-powered learning assistant",
    version="1.0.0"
)

# CORS middleware
allowed_origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",

    "https://steamx-v1-frontend.vercel.app",
    "https://steamx-v1-frontend.onrender.com",
    "https://steamx-v1-backend.onrender.com",

    "https://steamx.it.com",
    "https://www.steamx.it.com",
    "https://steamx.pk",
    "https://www.steamx.pk",
]

# Add FRONTEND_URL from environment only if it exists
if settings.FRONTEND_URL and settings.FRONTEND_URL not in allowed_origins:
    allowed_origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*steamx.*|http://localhost:.*|http://127\.0\.0\.1:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(subjects.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(files.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "STEAMX API",
        "version": "1.0.0",
        "status": "running"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}