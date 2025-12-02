
import warnings
warnings.filterwarnings("ignore", message="error reading bcryptversion")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import auth, obituaries  

# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="The Last Show API",
    description="AI-powered obituary generator with authentication",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(obituaries.router, prefix="/obituaries", tags=["Obituaries"])  # ← Add this

@app.get("/")
def root():
    return {
        "message": "The Last Show API v2",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}