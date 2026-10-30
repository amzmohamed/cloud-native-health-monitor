import asyncio
import logging
import httpx
from prometheus_client import Counter, Gauge, Histogram

logger = logging.getLogger("health-monitor")

ENDPOINT_HEALTH = Gauge(
    "endpoint_up", 
    "Health status of monitored endpoint (1 = UP, 0 = DOWN)", 
    ["endpoint"]
)
ENDPOINT_RESPONSE_TIME = Histogram(
    "endpoint_response_time_seconds", 
    "Response latency for monitored endpoint", 
    ["endpoint"]
)
ENDPOINT_CHECKS_TOTAL = Counter(
    "endpoint_checks_total", 
    "Total check iterations executed", 
    ["endpoint", "status"]
)

async def check_target(client: httpx.AsyncClient, url: str, timeout: float = 5.0) -> None:
    try:
        with ENDPOINT_RESPONSE_TIME.labels(endpoint=url).time():
            response = await client.get(url, timeout=timeout)
            
        if response.status_code == 200:
            ENDPOINT_HEALTH.labels(endpoint=url).set(1)
            ENDPOINT_CHECKS_TOTAL.labels(endpoint=url, status="success").inc()
        else:
            ENDPOINT_HEALTH.labels(endpoint=url).set(0)
            ENDPOINT_CHECKS_TOTAL.labels(endpoint=url, status=f"http_{response.status_code}").inc()
    except httpx.RequestError as exc:
        logger.warning(f"Connection failed for {url}: {exc}")
        ENDPOINT_HEALTH.labels(endpoint=url).set(0)
        ENDPOINT_CHECKS_TOTAL.labels(endpoint=url, status="connection_error").inc()

async def start_polling_loop(endpoints: list[str], interval_seconds: int = 15):
    """Asynchronous background loop keeping the FastAPI event loop unblocked."""
    async with httpx.AsyncClient() as client:
        while True:
            tasks = [check_target(client, url) for url in endpoints]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(interval_seconds)
