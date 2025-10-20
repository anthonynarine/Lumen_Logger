# 🧩 Lumen Logger — System Architecture Diagram
**Version:** 0.3.6 — Dynamic Configuration + CI Workflow Update

## 🌍 Overview

Lumen Logger acts as a shared observability backbone across all Lumen microservices.
It unifies console, file, and structured JSON logging — and introduces correlation IDs
to provide distributed request tracing across FastAPI and Django services.

### 🚀 Package Source
```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.6
```

---

## 🧠 System Diagram (High-Level)

*(diagram unchanged)*

---

## 🧾 Data Flow Explanation

Each microservice calls:
```python
from lumen_logger import configure_logging
configure_logging()
```

The logger dynamically reads configuration from `.env` or environment variables.

Requests passing through `CorrelationIdMiddleware` are enriched with correlation IDs
and contextual metadata like `service_name`, `hostname`, and timestamps.

---

## ✅ Verified Reliability
- Verified via `pytest` (v0.3.6)
- CI/CD pipeline tested for build and release artifacts
- Works across FastAPI and Django microservices

---

## 🧠 Author
Anthony Narine  
Founder & Lead Engineer — Lumen Project  
Version 0.3.4 — Dynamic, reload-safe, CI-verified logging system.
