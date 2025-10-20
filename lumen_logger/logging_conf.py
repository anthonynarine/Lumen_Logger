"""
logging_conf.py — Lumen Enterprise Logging System (v2.2.0)
-----------------------------------------------------------

Provides dynamic, environment-driven, and correlation-aware logging
for all Lumen microservices (FastAPI + Django).

Enhancements in v2.2.0:
    • Correlation ID injection is automatic via a global filter.
    • Middleware sets ContextVar; logger fetches it transparently.
    • Eliminates need to call get_correlation_id() in modules or factory.
    • Cleaner code, consistent tracing across all modules.

Author: Anthony Narine
Project: Lumen — Modern Vascular Ultrasound Reporting Platform
Version: 2.2.0
"""

import json
import logging
import os
import socket
from logging.handlers import RotatingFileHandler
from datetime import datetime
from colorlog import ColoredFormatter

from .context import get_correlation_id

# ---------------------------------------------------------------------------
# 🧩 Correlation Filter — Injects CID Automatically
# ---------------------------------------------------------------------------
class CorrelationIdFilter(logging.Filter):
    """
    Logging filter that injects the active correlation ID and metadata
    into each LogRecord automatically.

    Teaching Notes:
        - Executed once per record emission.
        - Prevents duplication of CID logic across modules or formatters.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.service_name = os.getenv("LOG_SERVICE_NAME", "lumen_service")
        record.hostname = socket.gethostname()
        record.correlation_id = get_correlation_id() or "-"
        record.timestamp = datetime.utcnow().isoformat()
        return True


# ---------------------------------------------------------------------------
# 🧱 Helper — Robust Environment Variable Loader
# ---------------------------------------------------------------------------
def _get_env(key: str, default=None, cast_type=str):
    value = os.getenv(key, default)
    if value is None:
        return default
    try:
        if cast_type is bool:
            return str(value).lower() in {"1", "true", "yes"}
        if cast_type is int:
            return int(value)
        return cast_type(value)
    except Exception:
        return default


# ---------------------------------------------------------------------------
# 🧠 Core Logging Configuration
# ---------------------------------------------------------------------------
def configure_logging():
    """
    Initializes the enterprise logger with automatic correlation context.

    Teaching Notes:
        - Safe to call multiple times (idempotent).
        - Each log record now includes service name, hostname, and CID.
        - Supports JSON or colorized console output.
    """

    # -----------------------------------------------------------------------
    # Step 1: Load environment-driven configuration
    # -----------------------------------------------------------------------
    log_level = _get_env("LOG_LEVEL", "INFO").upper()
    log_format = _get_env("LOG_FORMAT", "text")
    log_to_file = _get_env("LOG_TO_FILE", True, bool)
    log_file_path = _get_env("LOG_FILE_PATH", "./logs")
    log_max_size = _get_env("LOG_MAX_SIZE_MB", 10, int) * 1024 * 1024
    log_backups = _get_env("LOG_BACKUP_COUNT", 5, int)
    service_name = _get_env("LOG_SERVICE_NAME", "lumen_service")

    # -----------------------------------------------------------------------
    # Step 2: Ensure log directory exists
    # -----------------------------------------------------------------------
    os.makedirs(log_file_path, exist_ok=True)
    log_file = os.path.join(log_file_path, f"{service_name}.log")

    # -----------------------------------------------------------------------
    # Step 3: Configure root logger
    # -----------------------------------------------------------------------
    root_logger = logging.getLogger()

    if getattr(root_logger, "_lumen_logger_initialized", False):
        return
    root_logger.setLevel(log_level)

    # -----------------------------------------------------------------------
    # Step 4: Define log formatters
    # -----------------------------------------------------------------------
    base_format = (
        "[%(asctime)s] [%(service_name)s] [%(levelname)s] "
        "%(name)s:%(lineno)d → %(message)s "
        "(correlation_id=%(correlation_id)s)"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    color_formatter = ColoredFormatter(
        "%(log_color)s" + base_format,
        datefmt=date_format,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )

    file_formatter = logging.Formatter(base_format, datefmt=date_format)

    # Optional JSON format for ELK/Grafana
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            return json.dumps(
                {
                    "timestamp": getattr(record, "timestamp", datetime.utcnow().isoformat()),
                    "level": record.levelname,
                    "service": getattr(record, "service_name", service_name),
                    "hostname": getattr(record, "hostname", socket.gethostname()),
                    "module": record.name,
                    "line": record.lineno,
                    "message": record.getMessage(),
                    "correlation_id": getattr(record, "correlation_id", "-"),
                },
                ensure_ascii=False,
            )

    # -----------------------------------------------------------------------
    # Step 5: Build handlers
    # -----------------------------------------------------------------------
    handlers = []

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    console_handler.setLevel(log_level)
    console_handler.addFilter(CorrelationIdFilter())
    handlers.append(console_handler)

    if log_to_file:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=log_max_size, backupCount=log_backups, encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter if log_format == "text" else JSONFormatter())
        file_handler.setLevel(log_level)
        file_handler.addFilter(CorrelationIdFilter())
        handlers.append(file_handler)

    # -----------------------------------------------------------------------
    # Step 6: Attach handlers to root logger
    # -----------------------------------------------------------------------
    for handler in handlers:
        root_logger.addHandler(handler)

    root_logger._lumen_logger_initialized = True

    # -----------------------------------------------------------------------
    # Step 7: Silence noisy dependencies
    # -----------------------------------------------------------------------
    for noisy_lib in ["uvicorn", "aioboto3", "botocore", "fastapi"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)

    # -----------------------------------------------------------------------
    # Step 8: Startup confirmation
    # -----------------------------------------------------------------------
    root_logger.info(f"✅ Lumen logging initialized for service: {service_name}")
    root_logger.debug(f"Log file → {log_file}")
    root_logger.debug(f"Log format → {log_format}")
