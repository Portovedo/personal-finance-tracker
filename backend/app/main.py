import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.database import Base, engine

# Ensure database tables exist on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Configure CORS to allow the local GUI wrapper to communicate freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# Logic to locate the bundled React frontend files
if getattr(sys, 'frozen', False):
    # In the frozen exe, files are extracted to sys._MEIPASS
    base_dir = sys._MEIPASS
else:
    # In development, files are relative to this script
    base_dir = os.path.dirname(os.path.abspath(__file__))

static_dir = os.path.join(base_dir, "static")
assets_dir = os.path.join(static_dir, "assets")

# Mount static files if they exist (i.e., after the build process)
if os.path.exists(static_dir):
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    # SPA Catch-all route: Return index.html for any unknown path
    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        index_path = os.path.join(static_dir, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"error": "Frontend index.html not found."}
else:
    @app.get("/")
    def read_root():
        return {"message": "API Running. Frontend build not found in static folder."}