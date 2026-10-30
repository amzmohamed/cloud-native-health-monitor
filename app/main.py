import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

try:
    from app.monitor import start_polling_loop
except ImportError:
    from monitor import start_polling_loop

TARGET_URLS = ["https://httpbin.org/status/200", "https://httpbin.org/status/500"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(start_polling_loop(TARGET_URLS, interval_seconds=15))
    yield
    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Cloud Native Health Monitor", lifespan=lifespan)

@app.get("/healthz")
async def liveness():
    return {"status": "healthy"}

@app.get("/ready")
async def readiness():
    return {"status": "ready"}

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
