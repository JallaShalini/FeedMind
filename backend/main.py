from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from backend.api.routes import feedmind_ws, router
from backend.config import settings
from backend.database.redis_client import close_redis_client, get_redis_client
from backend.database.session import dispose_engine, init_db
from backend.services.streaming import ensure_consumer_group


app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Also bind websocket routes at the root level without /api prefix
app.websocket("/ws/feedmind")(feedmind_ws)
app.websocket("/ws/sentiment")(feedmind_ws)


@app.on_event("startup")
async def startup_event() -> None:
    await init_db()
    redis_client = get_redis_client()
    await ensure_consumer_group(redis_client, settings.redis_stream_name, settings.redis_consumer_group)


@app.on_event("shutdown")
async def shutdown_event() -> None:
    await close_redis_client()
    await dispose_engine()


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "FeedMind API", "status": "running"}
