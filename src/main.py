from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.database import DATABASE_URL, create_connection, init_db
from src.routers.todos import router as todos_router

STATIC_DIR = Path(__file__).parent.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = create_connection(DATABASE_URL)
    init_db(conn)
    conn.close()
    yield


app = FastAPI(title="Todo Demo — Claude Code × Superpowers", version="0.1.0", lifespan=lifespan)
app.include_router(todos_router)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(str(STATIC_DIR / "index.html"))
