"""
context.py — Async-Safe Context Management for Lumen Logger
-----------------------------------------------------------

Purpose:
    Provides utilities to store and retrieve request-specific context
    (e.g., correlation IDs) using Python's `contextvars` module.

Teaching Notes:
    - ContextVars provide isolated context per coroutine.
    - Perfect for FastAPI / async environments.
    - This data is automatically included in logs.
"""

import contextvars
import uuid

# -------------------------------------------------------------------------
# Global Context Variable
# -------------------------------------------------------------------------
# Holds the correlation ID per async context (one per request/task)
correlation_id_ctx: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "correlation_id", default=None
)

# -------------------------------------------------------------------------
# Context Management Utilities
# -------------------------------------------------------------------------
def set_correlation_id(value: str | None = None) -> str:
    """
    Sets or generates a correlation ID in the current request context.

    Args:
        value (str | None): Correlation ID string (UUID or propagated header value).
                            If None, a new UUID will be generated.

    Returns:
        str: The correlation ID assigned to this context.
    """
    if value is None:
        value = str(uuid.uuid4())
    correlation_id_ctx.set(value)
    return value


def get_correlation_id() -> str | None:
    """
    Retrieves the correlation ID for the current async context.

    Returns:
        str | None: The correlation ID if available, else None.
    """
    return correlation_id_ctx.get()


def clear_correlation_id() -> None:
    """
    Clears the correlation ID from the current context.

    Teaching Notes:
        - Prevents async context leakage between concurrent requests.
        - Called at the end of each request by CorrelationIdMiddleware.
    """
    correlation_id_ctx.set(None)
