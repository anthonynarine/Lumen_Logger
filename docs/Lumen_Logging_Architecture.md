# 🧩 Lumen Logger — System Architecture Diagram
**Version:** 0.3.3 — Dynamic Configuration + Full Test Integration

## 🌍 Overview

Lumen Logger acts as a shared observability backbone across all Lumen microservices.
It unifies console, file, and structured JSON logging — and introduces correlation IDs
to provide distributed request tracing across FastAPI and Django services.

### 🚀 Package Source
Lumen Logger is now distributed as a standalone public package:
```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.3
```

---

## 🧠 System Diagram (High-Level)

*(diagram remains unchanged)*

---

## 🧾 Data Flow Explanation

### Service Startup
Each microservice simply calls:
```python
from lumen_logger import configure_logging
configure_logging()
```
→ The logger dynamically reads configuration from `.env` or environment variables.

### Incoming Request
`CorrelationIdMiddleware` intercepts the request:
- If header `X-Correlation-ID` exists → reused.
- Else → a new UUIDv4 is generated and stored in `contextvars`.

### Logging Event
When a log is emitted:
- `logging_conf.py` injects contextual data:
  - `service_name`
  - `hostname`
  - `correlation_id`
  - `timestamp`

### Output Routing

| Destination | Handler Type | Purpose |
|--------------|--------------|----------|
| Developer Console | ColorFormatter | Real-time feedback |
| `/logs/<service>.log` | RotatingFileHandler | Persistent logs |
| *(Collector-ready)* | JSONFormatter | Future central aggregation |

### Central Collector (Future-Ready)
Logs can optionally be sent to a central FastAPI collector via `LOG_COLLECTOR_URL`.
If unavailable, all logs gracefully fall back to file and console output.

---

## 🧩 Testing and Reliability
- ✅ Verified via `pytest` suite:
  - Log file creation and rotation.
  - Correlation ID propagation via FastAPI middleware.
- 🧪 100% green across all test cases (v0.3.3).

---

## 🧱 Future Roadmap (Unchanged)

---

## 🧠 Author
Anthony Narine  
Founder & Lead Engineer — Lumen Project  
Version 0.3.3 — Dynamic, reload-safe, test-verified logging system.
