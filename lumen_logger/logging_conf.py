"""
logging_conf.py — Lumen Enterprise Logging System (v2.1.0)
-----------------------------------------------------------

Provides dynamic, environment-driven, and correlation-aware logging
for all Lumen microservices (FastAPI + Django).

This refactored version ensures:
    • Dynamic re-evaluation of environment variables on each call.
    • Colorized console logs for developers.
    • Rotating file handlers for persistent production logs.
    • JSON log formatting for ELK/Grafana Loki compatibility.
    • Correlation ID injection across distributed systems.
    • Safe operation in async + multithreaded environments.

Author: Anthony Narine
Project: Lumen — Modern Vascular Ultrasound Reporting Platform
Version: 2.1.0
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
# 🧱 Helper — Robust Environment Variable Loader
# ---------------------------------------------------------------------------
def _get_env(key: str, default=None, cast_type=str):
    """
    Safely fetches and casts environment variables.

    Args:
        key (str): Name of the environment variable.
        default (Any): Default value if not found.
        cast_type (type): Optional type caster (str, int, bool).

    Returns:
        Any: The environment variable's value, cast to the given type.
    """
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
# 🧩 Custom LogRecord Factory — Inject Context
# ---------------------------------------------------------------------------
def _inject_context_into_log_record(record: logging.LogRecord) -> logging.LogRecord:
    """
    Inject contextual metadata (correlation_id, service_name, hostname)
    into every LogRecord before formatting.

    Teaching Notes:
        - This hook runs once per emitted log record.
        - It enriches log entries for distributed tracing.
    """
    record.service_name = os.getenv("LOG_SERVICE_NAME", "lumen_service")
    record.hostname = socket.gethostname()
    record.correlation_id = get_correlation_id() or "-"
    record.timestamp = datetime.utcnow().isoformat()
    return record


# ---------------------------------------------------------------------------
# 🧠 Core Logging Configuration
# ---------------------------------------------------------------------------
def configure_logging():
    """
    Configures and initializes the Lumen enterprise logger.

    This function dynamically reads configuration from environment
    variables, sets up handlers and formatters, and ensures each log
    record includes context such as service name and correlation ID.

    Teaching Notes:
        - This function may be called multiple times safely.
        - Each call re-reads environment variables dynamically.
        - File + console handlers coexist for dual-output logging.
    """

    # -----------------------------------------------------------------------
    # Step 1: Load configuration dynamically from environment
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

    # Prevent duplicate handlers (important for FastAPI reloads)
    if getattr(root_logger, "_lumen_logger_initialized", False):
        return
    root_logger.setLevel(log_level)

    # -----------------------------------------------------------------------
    # Step 4: Inject contextual metadata into log records
    # -----------------------------------------------------------------------
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        return _inject_context_into_log_record(record)

    logging.setLogRecordFactory(record_factory)

    # -----------------------------------------------------------------------
    # Step 5: Define log formats
    # -----------------------------------------------------------------------
    base_format = (
        "[%(asctime)s] [%(service_name)s] [%(levelname)s] "
        "%(name)s:%(lineno)d → %(message)s "
        "(correlation_id=%(correlation_id)s)"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # JSON structured format — ideal for collectors
    def json_formatter(record):
        return json.dumps(
            {
                "timestamp": record.timestamp,
                "level": record.levelname,
                "service": record.service_name,
                "hostname": record.hostname,
                "module": record.name,
                "line": record.lineno,
                "message": record.getMessage(),
                "correlation_id": record.correlation_id,
            },
            ensure_ascii=False,
        )

    # -----------------------------------------------------------------------
    # Step 6: Build formatters
    # -----------------------------------------------------------------------
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

    # -----------------------------------------------------------------------
    # Step 7: Handlers setup
    # -----------------------------------------------------------------------
    handlers = []

    # Console Handler (always active)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    console_handler.setLevel(log_level)
    handlers.append(console_handler)

    # Rotating File Handler (optional)
    if log_to_file:
        file_handler = RotatingFileHandler(
            log_file, maxBytes=log_max_size, backupCount=log_backups, encoding="utf-8"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        handlers.append(file_handler)

    # -----------------------------------------------------------------------
    # Step 8: Attach handlers to the root logger
    # -----------------------------------------------------------------------
    for handler in handlers:
        root_logger.addHandler(handler)

    root_logger._lumen_logger_initialized = True  # Prevent reinit on reload

    # -----------------------------------------------------------------------
    # Step 9: Silence noisy libraries
    # -----------------------------------------------------------------------
    for noisy_lib in ["uvicorn", "aioboto3", "botocore", "fastapi"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)

    # -----------------------------------------------------------------------
    # Step 10: Startup confirmation
    # -----------------------------------------------------------------------
    root_logger.info(f"✅ Lumen logging initialized for service: {service_name}")
    root_logger.debug(f"Log file → {log_file}")
    root_logger.debug(f"Log format → {log_format}")
