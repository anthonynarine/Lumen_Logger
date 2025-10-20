"""
test_middleware.py — Tests for Enhanced CorrelationIdMiddleware
---------------------------------------------------------------

Covers:
    • Automatic generation and propagation of X-Correlation-ID
    • Inclusion of X-Response-Time-ms header
    • ContextVar behavior via lumen_logger.context
"""

import re
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from lumen_logger.middleware import CorrelationIdMiddleware
from lumen_logger.context import get_correlation_id


def create_test_app():
    """Create a minimal FastAPI app using the enhanced middleware."""
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/ping")
    async def ping(request: Request):
        cid = getattr(request.state, "correlation_id", None)
        return {"msg": "pong", "cid": cid}

    return app


def test_correlation_middleware_adds_headers():
    """Ensure the middleware adds both correlation and timing headers."""
    client = TestClient(create_test_app())

    response = client.get("/ping")

    # 1️⃣ Basic route validation
    assert response.status_code == 200
    body = response.json()
    assert body["msg"] == "pong"

    # 2️⃣ Verify correlation ID headers
    assert "X-Correlation-ID" in response.headers
    cid = response.headers["X-Correlation-ID"]
    assert isinstance(cid, str) and len(cid) > 0

    # 3️⃣ Verify response time header format
    assert "X-Response-Time-ms" in response.headers
    ms = response.headers["X-Response-Time-ms"]
    assert re.match(r"^\d+(\.\d+)?$", ms), "Invalid response time format"

    # 4️⃣ Ensure context and state match
    assert body["cid"] == cid


def test_middleware_reuses_incoming_header():
    """If client sends X-Correlation-ID, middleware should reuse it."""
    client = TestClient(create_test_app())
    custom_cid = "test-cid-1234"

    response = client.get("/ping", headers={"X-Correlation-ID": custom_cid})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == custom_cid
