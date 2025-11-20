import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.core.database import Base, engine

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# API Routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Setup Template Engine
# Detect path works for both local run and frozen exe
if getattr(os, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

templates_dir = os.path.join(base_dir, "app", "templates")
static_dir = os.path.join(base_dir, "app", "static")

# Ensure directories exist to prevent crash on first run
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

# --- Frontend Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/accounts", response_class=HTMLResponse)
async def page_accounts(request: Request):
    return templates.TemplateResponse("accounts.html", {"request": request})

@app.get("/statements", response_class=HTMLResponse)
async def page_statements(request: Request):
    return templates.TemplateResponse("statements.html", {"request": request})

@app.get("/categories", response_class=HTMLResponse)
async def page_categories(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})