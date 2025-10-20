"""
CorrelationIdMiddleware — Enhanced FastAPI Request Tracing Middleware
=====================================================================

Purpose:
--------
Provides end-to-end request observability by:
    • Attaching or propagating a correlation ID (cid)
    • Measuring request latency (ms)
    • Logging request start, completion, and errors
    • Appending trace headers to every response

Teaching Notes:
---------------
- Correlation IDs allow developers to trace a request through every
  Lumen microservice (Auth, Media, Dubin, HL7, etc.).
- This middleware makes it automatic — no route changes required.
- Each CID lives only for the duration of its request (context cleared after).

Headers:
    X-Correlation-ID: propagated or generated UUID
    X-Response-Time-ms: total request time (milliseconds)
"""

import uuid
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from lumen_logger.context import set_correlation_id, clear_correlation_id

# Attach logger from lumen_logger (inherits global config)
logger = logging.getLogger(__name__)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Enhanced request tracing middleware with timing and structured logs."""

    async def dispatch(self, request: Request, call_next):
        # Step 1: Retrieve or create correlation ID
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())[:8]
        set_correlation_id(cid)
        request.state.correlation_id = cid

        # Step 2: Log request start with metadata
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        method = request.method
        start_time = time.perf_counter()

        logger.info(f"➡️ {method} {path} started (cid={cid}, client={client_ip})")

        try:
            # Step 3: Process the request
            response: Response = await call_next(request)
        except Exception as e:
            # Step 4: Log and re-raise unhandled exceptions
            logger.exception(f"❌ Exception during {method} {path} (cid={cid}): {e}")
            raise
        finally:
            # Step 5: Clean up the async context
            clear_correlation_id()

        # Step 6: Measure elapsed time
        duration_ms = (time.perf_counter() - start_time) * 1000

        # Step 7: Log completion
        logger.info(
            f"⬅️ {method} {path} completed ({response.status_code}, {duration_ms:.2f} ms, cid={cid})"
        )

        # Step 8: Add trace headers
        response.headers["X-Correlation-ID"] = cid
        response.headers["X-Response-Time-ms"] = f"{duration_ms:.2f}"

        return response
