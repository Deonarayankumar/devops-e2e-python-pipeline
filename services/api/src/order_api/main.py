"""FastAPI order service."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "orders:pending"


class OrderCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=1, le=10_000)


class OrderResponse(BaseModel):
    id: str
    sku: str
    quantity: int
    status: str


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.redis = redis.from_url(REDIS_URL, decode_responses=True)
    try:
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(title="Order API", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    r: redis.Redis = app.state.redis
    await r.ping()
    return {"status": "ok"}


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(payload: OrderCreate) -> OrderResponse:
    r: redis.Redis = app.state.redis
    order_id = await r.incr("orders:seq")
    key = f"order:{order_id}"
    await r.hset(
        key,
        mapping={"sku": payload.sku, "quantity": str(payload.quantity), "status": "pending"},
    )
    await r.lpush(QUEUE_KEY, str(order_id))
    return OrderResponse(id=str(order_id), sku=payload.sku, quantity=payload.quantity, status="pending")


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str) -> OrderResponse:
    r: redis.Redis = app.state.redis
    data = await r.hgetall(f"order:{order_id}")
    if not data:
        raise HTTPException(status_code=404, detail="order not found")
    return OrderResponse(
        id=order_id,
        sku=data["sku"],
        quantity=int(data["quantity"]),
        status=data.get("status", "unknown"),
    )
