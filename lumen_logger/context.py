"""
context.py — Async-Safe Context Management for Lumen Logger
-----------------------------------------------------------

Provides utilities to store and retrieve request-specific context
(e.g., correlation IDs) using Python's `contextvars` module.

Teaching Notes:
    - ContextVars provide isolated context per coroutine.
    - Perfect for FastAPI / async environments.
    - This data is automatically included in logs.
"""

import contextvars

# Define ContextVar to store the correlation ID for each request
correlation_id_ctx = contextvars.ContextVar("correlation_id", default=None)


def set_correlation_id(value: str) -> None:
    """
    Sets the correlation ID in the current request context.

    Args:
        value (str): Correlation ID string (UUID or propagated header value)
    """
    correlation_id_ctx.set(value)


def get_correlation_id() -> str | None:
    """
    Retrieves the correlation ID for the current request context.

    Returns:
        str | None: The correlation ID if available, else None.
    """
    return correlation_id_ctx.get()
