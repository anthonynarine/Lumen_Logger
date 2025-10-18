"""
CorrelationIdMiddleware — FastAPI Request Tracing Middleware
------------------------------------------------------------

Purpose:
    Automatically attaches a unique correlation ID to every incoming HTTP request.
    This enables distributed tracing across all Lumen microservices.

Key Features:
    • Reads `X-Correlation-ID` header if provided (propagation between services).
    • Generates a new UUID if missing.
    • Stores the ID in an async-safe ContextVar (see context.py).
    • Adds the ID to all logs created during that request.
    • Appends the ID to the outgoing response headers.

Teaching Notes:
    - ContextVars are thread- and async-safe: each coroutine has its own context.
    - This design is inspired by OpenTelemetry trace propagation, simplified for Python logging.
"""

import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response

from .context import set_correlation_id, get_correlation_id


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware that ensures every request has a correlation ID.

    If a request includes an `X-Correlation-ID` header, it reuses that value.
    Otherwise, it generates a new UUIDv4 and attaches it to:
        - The request context (for logs)
        - The response headers (for downstream propagation)
    """

    def __init__(self, app: ASGIApp, header_name: str = "X-Correlation-ID") -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next):
        # Step 1: Retrieve or generate correlation ID
        correlation_id = request.headers.get(self.header_name)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Step 2: Store in async context
        set_correlation_id(correlation_id)

        # Step 3: Continue request lifecycle
        response: Response = await call_next(request)

        # Step 4: Add correlation ID to outgoing response headers
        response.headers[self.header_name] = correlation_id

        return response
