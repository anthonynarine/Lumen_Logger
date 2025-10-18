"""
Lumen Logger — Centralized Observability Package
------------------------------------------------

Shared cross-service utilities for the Lumen ecosystem:
    • Enterprise logging configuration (environment-aware + correlation ID)
    • Request-level context management (ContextVars)
    • FastAPI/Django correlation middleware
    • Future: async log collector client (central ingestion)

Teaching Notes:
    - This package unifies observability across all Lumen services.
    - Designed for zero-touch integration:
        from lumen_logger import configure_logging
        configure_logging()
    - Avoid running logic on import to prevent circular dependencies.
    - All modules are safe for async + threaded execution.
"""

# ---------------------------------------------------------------------------
# 📦 Public Imports
# ---------------------------------------------------------------------------
from .logging_conf import configure_logging
from .context import get_correlation_id, set_correlation_id
from .middleware import CorrelationIdMiddleware

# ---------------------------------------------------------------------------
# 🧾 Public API Surface
# ---------------------------------------------------------------------------
__all__ = [
    "configure_logging",
    "get_correlation_id",
    "set_correlation_id",
    "CorrelationIdMiddleware",
]

__version__ = "2.0.0"
__author__ = "Anthony Narine"
