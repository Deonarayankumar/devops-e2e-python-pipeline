"""API tests."""

from __future__ import annotations

import fakeredis.aioredis
import pytest
from httpx import ASGITransport, AsyncClient

from order_api.main import app


@pytest.fixture
async def client():
    fake = fakeredis.aioredis.FakeRedis(decode_responses=True)
    app.state.redis = fake
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_and_get_order(client: AsyncClient) -> None:
    create = await client.post("/orders", json={"sku": "WIDGET-01", "quantity": 3})
    assert create.status_code == 201
    body = create.json()
    assert body["status"] == "pending"

    fetched = await client.get(f"/orders/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["sku"] == "WIDGET-01"
