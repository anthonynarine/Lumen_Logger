## Overview

`lumen_logger` is the centralized, environment-aware, correlation-driven logging framework
used across the **Lumen** ecosystem — a modular suite of Python microservices powering
modern vascular ultrasound reporting and AI-assisted diagnostics.

It replaces per-service log setups with one unified, production-grade system that
supports **FastAPI**, **Django**, and **async workloads** with zero code duplication.

---

## 🎯 Goals

- Provide consistent, structured logs across all Lumen microservices.
- Enable end-to-end request tracing via correlation IDs.
- Support colorized console output (for developers) and JSON output (for collectors).
- Be environment-configurable via `.env` variables.
- Offer automatic resilience and graceful fallback when collectors are offline.
- Require **zero modification** to existing service code beyond `configure_logging()`.

---

## 🧠 Architectural Overview

### 1️⃣ System Context

┌──────────────────────┐ ┌────────────────────┐
│ Lumen Media (FastAPI)│──────▶│ Lumen Log Collector│
│ lumen_logger active │ │ (optional FastAPI) │
└──────────────────────┘ └────────────────────┘
│ ▲
▼ │
┌──────────────────────┐ ┌────────────────────┐
│ Lumen Reports (Django)│────▶│ Grafana / Loki / S3│
│ lumen_logger active │ │ Central Observability│
└──────────────────────┘ └────────────────────┘

pgsql
Copy code

Every microservice (Media, Reports, Dubin, HL7, etc.) uses the same logger package.
Each emits logs locally **and optionally forwards them** to a central collector service
for unified visualization.

---

### 2️⃣ Internal Modules

| Module | Responsibility |
|---------|----------------|
| **`logging_conf.py`** | Reads environment variables, builds handlers (console, file, JSON), injects metadata (service_name, hostname, correlation_id). |
| **`context.py`** | Manages per-request context using `contextvars` (async-safe). Stores and retrieves correlation IDs. |
| **`middleware.py`** | Adds FastAPI/Django middleware to generate and propagate correlation IDs through request headers. |
| **`collector_client.py`** *(future)* | Asynchronously pushes structured JSON logs to a central log collector API endpoint. |

---

## ⚙️ Configuration via Environment Variables

| Variable | Description | Example |
|-----------|-------------|----------|
| `LOG_LEVEL` | Logging level | `INFO`, `DEBUG`, `WARNING` |
| `LOG_FORMAT` | `text` for colorized output or `json` for structured output | `text` |
| `LOG_TO_FILE` | Enable rotating file handler | `true` |
| `LOG_FILE_PATH` | Directory for file logs | `/logs` |
| `LOG_MAX_SIZE_MB` | Max file size before rotation | `10` |
| `LOG_BACKUP_COUNT` | Number of backup files | `5` |
| `LOG_SERVICE_NAME` | Service identifier | `lumen_media` |
| `LOG_COLLECTOR_URL` | Optional remote collector endpoint | `http://central-logger:9000/ingest` |
| `LOG_ENABLE_CORRELATION` | Enable correlation tracking | `true` |

All variables are optional — sensible defaults are used if not set.

---

## 🧾 Usage Examples

### 🟦 FastAPI Example

```python
from fastapi import FastAPI
from lumen_logger import configure_logging, CorrelationIdMiddleware

# Step 1: Configure logging system (reads env vars automatically)
configure_logging(service_name="lumen_media")

# Step 2: Create FastAPI app
app = FastAPI(title="Lumen Media API")

# Step 3: Attach correlation middleware
app.add_middleware(CorrelationIdMiddleware)

@app.get("/health")
async def health_check():
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Health check endpoint invoked.")
    return {"status": "ok", "service": "lumen_media"}
✅ Console output:

css
Copy code
[2025-10-17 19:32:11] [lumen_media] [INFO] app.main:47 → Health check endpoint invoked.
    (correlation_id=cfb178ea-ccda-4ccf-9a2e-9fa21b1a5122)
🟨 Django Example
python
Copy code
# settings.py
INSTALLED_APPS = [
    ...
    "lumen_logger",
]

MIDDLEWARE = [
    ...
    "lumen_logger.middleware.CorrelationIdMiddleware",
]

# Initialize logging
from lumen_logger import configure_logging
configure_logging(service_name="lumen_reports")
✅ Every request and DRF view will automatically include a correlation ID
and log with the configured format.

🧩 How Correlation Works
Each request passes through CorrelationIdMiddleware.

If the header X-Correlation-ID exists, it’s reused.

Otherwise, a new UUID is generated.

The ID is stored in a ContextVar (FastAPI) or thread.local (Django).

logging_conf.py injects this value into every log record.

The same ID propagates downstream (e.g., Reports → Media → Dubin).

Example:

markdown
Copy code
Frontend → Lumen Reports → Lumen Media → Lumen HL7
             │                 │
             ▼                 ▼
        correlation_id=abc123  correlation_id=abc123
Result: a complete distributed trace visible across all logs.

📦 Installation
Option 1: From GitHub (private subdirectory)
bash
Copy code
pip install git+https://<TOKEN>@github.com/anthonynarine/Lumen.git#subdirectory=lumen_logger
Option 2: From GitHub Package Registry (future)
bash
Copy code
pip install lumen-logger \
  --extra-index-url https://__token__:<YOUR_TOKEN>@pypi.github.com/anthonynarine/simple
Option 3: Local wheel install (for offline Docker)
bash
Copy code
pip install dist/lumen_logger-0.2.0-py3-none-any.whl
🩺 Features Summary
Feature	Description
Environment-driven	Configures dynamically from .env vars.
Colorized Console	Developer-friendly during local runs.
Rotating File Logs	Docker-safe persistent log output.
JSON Formatter	Machine-readable structured logs for ELK/Loki.
Correlation ID	End-to-end tracing across microservices.
Resilient Fallbacks	Logs still go to console/file if collector is down.
Zero-touch Integration	One call: configure_logging() — no refactoring needed.

🧠 Example Log Record (JSON Mode)
json
Copy code
{
  "timestamp": "2025-10-17T19:32:11.923Z",
  "level": "INFO",
  "service": "lumen_media",
  "hostname": "docker-02",
  "module": "app.routes.image_routes",
  "line": 47,
  "message": "Upload succeeded",
  "correlation_id": "cfb178ea-ccda-4ccf-9a2e-9fa21b1a5122"
}
🚀 Integration Flow Inside Lumen
Phase	Component	Description
1️⃣	lumen_logger	Shared package for logging + correlation logic
2️⃣	lumen_media	FastAPI microservice (uploads, MinIO integration)
3️⃣	lumen_reports	Django/DRF microservice (exam data + PDFs)
4️⃣	lumen_dubin	AI/RAG microservice (criteria + calculations)
5️⃣	lumen_hl7	FastAPI microservice (HL7 → EMR)
6️⃣	lumen_log_collector (optional)	Central endpoint for collecting JSON logs

Each service imports and initializes the same logger.
All logs contain correlation IDs, service names, and consistent formatting.

🧩 Future Expansion
Module	Planned Feature
collector_client.py	Async batching + HTTP log shipping
metrics.py	Prometheus metrics integration
filters.py	PHI-safe log redaction
decorators.py	@traceable() decorator for async tasks (Celery, RQ)

🧰 Developer Notes
The package uses Python’s standard logging library — no custom handlers or dependencies.

ContextVars ensures async safety in FastAPI (each request gets its own log context).

Works seamlessly with uvicorn and gunicorn reloads — duplicate handlers are prevented.

🧱 Example Docker Integration
Mount a /logs volume for persistent logs:

yaml
Copy code
services:
  lumen_media:
    build: .
    env_file: .env
    volumes:
      - ./logs:/logs
    environment:
      LOG_TO_FILE: "true"
      LOG_FILE_PATH: "/logs"
      LOG_SERVICE_NAME: "lumen_media"
✅ Logs appear in both console and /logs/lumen_media.log.

📜 License
pgsql
Copy code
Lumen License – All Rights Reserved
Copyright (c) 2025 Anthony Narine.

This software is proprietary and confidential.
Redistribution, modification, or public disclosure without explicit written permission is strictly prohibited.
💬 Author
Anthony Narine
Founder & Lead Engineer — Lumen Project
https://github.com/anthonynarine

“Every log tells a story — we just made them readable.”
— Lumen Logging Philosophy