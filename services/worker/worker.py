"""Background worker consuming order queue from Redis."""

from __future__ import annotations

import logging
import os
import signal
import sys
import time

import redis

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("worker")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_KEY = "orders:pending"
POLL_TIMEOUT = int(os.getenv("POLL_TIMEOUT", "5"))
_running = True


def _shutdown(signum: int, frame: object) -> None:
    global _running
    log.info("received signal %s, shutting down", signum)
    _running = False


def process_order(r: redis.Redis, order_id: str) -> None:
    key = f"order:{order_id}"
    if not r.exists(key):
        log.warning("order %s missing, skipping", order_id)
        return
    r.hset(key, "status", "processed")
    log.info("processed order %s", order_id)


def run() -> int:
    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)
    r = redis.from_url(REDIS_URL, decode_responses=True)
    log.info("worker started, listening on %s", QUEUE_KEY)
    while _running:
        item = r.brpop(QUEUE_KEY, timeout=POLL_TIMEOUT)
        if item is None:
            continue
        _, order_id = item
        process_order(r, order_id)
    log.info("worker stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
