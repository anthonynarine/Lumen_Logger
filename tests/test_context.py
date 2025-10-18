import contextvars
import uuid

# Context variable that stores the correlation ID
_correlation_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("correlation_id", default=None)

def get_correlation_id() -> str | None:
    """Retrieve the current correlation ID from context."""
    return _correlation_id.get()

def set_correlation_id(value: str | None = None) -> str:
    """Set or generate a correlation ID and store it in context."""
    if value is None:
        value = str(uuid.uuid4())
    _correlation_id.set(value)
    return value

def clear_correlation_id() -> None:
    """Clear the correlation ID from context."""
    _correlation_id.set(None)
