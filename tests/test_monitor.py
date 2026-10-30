import pytest
from unittest.mock import AsyncMock
import httpx
from app.monitor import check_target, ENDPOINT_HEALTH
from app.main import app

@pytest.mark.asyncio
async def test_check_target_success():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = httpx.Response(status_code=200, request=httpx.Request("GET", "https://example.com"))
    mock_client.get.return_value = mock_response

    target_url = "https://example.com/test-up"
    await check_target(mock_client, target_url)

    assert ENDPOINT_HEALTH.labels(endpoint=target_url)._value.get() == 1

@pytest.mark.asyncio
async def test_check_target_failure():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = httpx.Response(status_code=500, request=httpx.Request("GET", "https://example.com"))
    mock_client.get.return_value = mock_response

    target_url = "https://example.com/test-down"
    await check_target(mock_client, target_url)

    assert ENDPOINT_HEALTH.labels(endpoint=target_url)._value.get() == 0

@pytest.mark.asyncio
async def test_health_and_metrics_endpoints():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        health_resp = await client.get("/healthz")
        assert health_resp.status_code == 200
        assert health_resp.json() == {"status": "healthy"}

        ready_resp = await client.get("/ready")
        assert ready_resp.status_code == 200
        assert ready_resp.json() == {"status": "ready"}

        metrics_resp = await client.get("/metrics")
        assert metrics_resp.status_code == 200
