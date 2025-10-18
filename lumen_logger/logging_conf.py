"""
logging_conf.py — Lumen Enterprise Logging System
-------------------------------------------------

Provides environment-driven, correlation-aware, and distributed logging
for all Lumen microservices (FastAPI + Django).

Key Capabilities:
    • Reads configuration dynamically from environment variables.
    • Colorized console logs for local/staging.
    • Rotating file logs for production persistence.
    • JSON formatting for structured ingestion (ELK, Grafana Loki).
    • Correlation ID auto-injection from context.py.
    • Async-safe, thread-safe, and reload-safe.

Author: Anthony Narine
Version: 2.0.0
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
# 🧱 Helper — Load Environment Variables Safely
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
# 🧩 Custom LogRecord Factory
# ---------------------------------------------------------------------------
def _inject_context_into_log_record(record: logging.LogRecord) -> logging.LogRecord:
    """
    Injects contextual data (correlation_id, service_name, hostname)
    into every LogRecord before formatting.

    Teaching Notes:
        - This function hooks into Python's logging system globally.
        - It runs once for every log emitted, adding our custom metadata.
    """
    record.service_name = os.getenv("LOG_SERVICE_NAME", "lumen_service")
    record.hostname = socket.gethostname()
    record.correlation_id = get_correlation_id() or "-"
    record.timestamp = datetime.utcnow().isoformat()
    return record


# ---------------------------------------------------------------------------
# 🧠 Core Configuration Function
# ---------------------------------------------------------------------------
def configure_logging():
    """
    Configures the unified Lumen logging system.

    Reads environment variables to determine handlers, formats, and levels.
    Prevents duplicate handlers during reloads and ensures safe async behavior.
    """
    # Step 1: Environment variables
    log_level = _get_env("LOG_LEVEL", "INFO").upper()
    log_format = _get_env("LOG_FORMAT", "text")
    log_to_file = _get_env("LOG_TO_FILE", True, bool)
    log_file_path = _get_env("LOG_FILE_PATH", "./logs")
    log_max_size = _get_env("LOG_MAX_SIZE_MB", 10, int) * 1024 * 1024
    log_backups = _get_env("LOG_BACKUP_COUNT", 5, int)
    service_name = _get_env("LOG_SERVICE_NAME", "lumen_service")

    # Step 2: Prepare log directory
    os.makedirs(log_file_path, exist_ok=True)
    log_file = os.path.join(log_file_path, f"{service_name}.log")

    # Step 3: Create root logger
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # Avoid reconfiguring on reload
    root_logger.setLevel(log_level)

    # Step 4: Attach our custom record factory
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        return _inject_context_into_log_record(record)

    logging.setLogRecordFactory(record_factory)

    # Step 5: Define formats
    base_format = (
        "[%(asctime)s] [%(service_name)s] [%(levelname)s] "
        "%(name)s:%(lineno)d → %(message)s "
        "(correlation_id=%(correlation_id)s)"
    )
    date_format = "%Y-%m-%d %H:%M:%S"

    # JSON structured format for collectors
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

    # Step 6: Formatters
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

    # Step 7: Handlers
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

    # Step 8: Attach handlers
    for handler in handlers:
        root_logger.addHandler(handler)

    # Step 9: Mute noisy dependencies
    for noisy_lib in ["uvicorn", "aioboto3", "botocore", "fastapi"]:
        logging.getLogger(noisy_lib).setLevel(logging.WARNING)

    root_logger.info(f"✅ Lumen logging initialized for service: {service_name}")
    root_logger.debug(f"Log file → {log_file}")
    root_logger.debug(f"Log format → {log_format}")
