import os
import logging
import importlib
import lumen_logger.logging_conf as logging_conf
from lumen_logger import configure_logging

def test_configure_logging_creates_log_file(tmp_path):
    """Test that configure_logging initializes and writes to a log file."""
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    # Set environment variables before reloading the module
    os.environ["LOG_SERVICE_NAME"] = "test_service"
    os.environ["LOG_FILE_PATH"] = str(log_dir)
    os.environ["LOG_TO_FILE"] = "true"

    # Reload to ensure logger sees updated env vars
    importlib.reload(logging_conf)

    configure_logging()
    logger = logging.getLogger("test_logger")

    logger.info("Hello from lumen_logger!")

    log_files = list(log_dir.glob("*.log"))
    assert len(log_files) > 0, "No log file was created."
    assert log_files[0].stat().st_size > 0, "Log file is empty."
