from fastapi import FastAPI
from fastapi.testclient import TestClient
from lumen_logger.middleware import CorrelationIdMiddleware

def test_correlation_middleware_adds_header():
    """Middleware should add X-Correlation-ID header to responses."""
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/ping")
    async def ping():
        return {"msg": "pong"}

    client = TestClient(app)
    response = client.get("/ping")

    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    assert len(response.headers["X-Correlation-ID"]) > 0
