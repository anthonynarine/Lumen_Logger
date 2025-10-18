"""
conftest.py — Pytest configuration for Lumen Logger
---------------------------------------------------

This file automatically loads environment variables from `.env`
and ensures test directories (like `./logs`) exist before tests run.
"""

import os
from dotenv import load_dotenv

# 🩸 Step 1: Load .env file into environment variables
load_dotenv()

# 🧱 Step 2: Ensure the log directory exists
log_dir = os.getenv("LOG_FILE_PATH", "./logs")
os.makedirs(log_dir, exist_ok=True)

# ✅ Optional: Print for confirmation (helpful for debugging)
print(f"Loaded .env and prepared log directory: {log_dir}")
