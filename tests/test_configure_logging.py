import os
import logging
import importlib
import time
import lumen_logger.logging_conf as logging_conf
from lumen_logger import configure_logging


def test_log_includes_correlation_id(tmp_path, capsys):
    """
    Ensure correlation ID is automatically injected into log records.

    This test verifies that:
        • correlation_id appears in formatted console output.
        • File logs contain correlation_id.
        • No manual get_correlation_id() call required.
    """
    log_dir = tmp_path / "logs"
    log_dir.mkdir()

    os.environ["LOG_SERVICE_NAME"] = "test_service"
    os.environ["LOG_FILE_PATH"] = str(log_dir)
    os.environ["LOG_TO_FILE"] = "true"

    importlib.reload(logging_conf)
    configure_logging()

    logger = logging.getLogger("cid_test_logger")

    # Emit a log and capture formatted console output
    logger.info("CID injection test message")

    captured = capsys.readouterr().err + capsys.readouterr().out
    assert "correlation_id" in captured, "Correlation ID missing from console output."

    # Wait to ensure log flush
    time.sleep(0.2)

    log_files = list(log_dir.glob("*.log"))
    assert log_files, "No log file created."
    log_file = log_files[0]
    contents = log_file.read_text()

    assert "correlation_id=" in contents, "Log record missing correlation_id."
    assert "CID injection test message" in contents, "Expected log message not found."
