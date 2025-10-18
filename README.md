# 🩸 Lumen Logger (`lumen-logger`)
**Version:** 0.3.0  
**Author:** Anthony Narine  

---

## 🧭 Overview  

`lumen-logger` is an **distributed logging system** designed to unify and simplify observability across Python-based microservices.  

Originally developed for the **Lumen Healthcare Platform** — a modern vascular ultrasound reporting system — it now serves as a **reusable, standalone package** that can be used in any FastAPI, Django, or async Python project.  

Built with scalability and consistency in mind, it provides:  
- Environment-driven configuration  
- JSON + colorized console output  
- Automatic correlation ID propagation  
- Async- and thread-safe log handling  
- Optional central collector support  

---

## ⚙️ Key Features  

| Feature | Description |
|----------|--------------|
| **Dynamic Configuration** | Controlled entirely via environment variables (LOG_LEVEL, LOG_FORMAT, etc.) |
| **Dual Output System** | Colorized console for development + rotating file or JSON output for production |
| **Correlation IDs** | Automatically traces requests across services (FastAPI and Django middleware included) |
| **Structured JSON Logging** | Ready for ingestion by ELK, Grafana Loki, or CloudWatch |
| **Async-Safe Collector** | Non-blocking HTTP-based log shipping to a central collector endpoint |
| **Zero-Touch Integration** | Each service simply imports and calls `configure_logging()` — no manual setup needed |

---

## 🧰 Installation  

### 🪄 Option 1 — Install from GitHub (Private Repo)
```bash
pip install git+https://<YOUR_GITHUB_TOKEN>@github.com/anthonynarine/Lumen_Logger.git@main
```

### 🧩 Option 2 — Install from Local Wheel
After building locally with `python -m build`:
```bash
pip install dist/lumen_logger-0.3.0-py3-none-any.whl
```

### ✅ Verification
```bash
python -c "from lumen_logger import configure_logging; print('✅ Lumen Logger imported successfully')"
```

---

## 🚀 Quick Start  

### FastAPI Integration
```python
from fastapi import FastAPI
from lumen_logger import configure_logging, CorrelationIdMiddleware

# Step 1: Initialize logging
configure_logging(service_name="lumen_media")

# Step 2: Create your FastAPI app
app = FastAPI(title="Lumen Media API")

# Step 3: Add middleware for correlation IDs
app.add_middleware(CorrelationIdMiddleware)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### Django Integration
In `settings.py`:
```python
from lumen_logger import configure_logging

configure_logging(service_name="lumen_reports")
```

In `MIDDLEWARE`:
```python
'lumen_logger.middleware.DjangoCorrelationMiddleware',
```

---

## 🧠 Configuration via Environment Variables  

| Variable | Default | Description |
|-----------|----------|--------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) |
| `LOG_FORMAT` | `text` | Log format (`text` or `json`) |
| `LOG_TO_FILE` | `true` | Enables rotating file handler |
| `LOG_FILE_PATH` | `./logs` | Directory for file-based logs |
| `LOG_MAX_SIZE_MB` | `10` | Maximum file size before rotation |
| `LOG_BACKUP_COUNT` | `5` | Number of rotated log files to retain |
| `LOG_SERVICE_NAME` | `default_service` | Service name tag used in log output |
| `LOG_COLLECTOR_URL` | *None* | Optional endpoint for central log ingestion |
| `LOG_ENABLE_CORRELATION` | `true` | Enables correlation ID propagation across requests |

---

## 🩺 Used In: The Lumen Healthcare Platform  

`lumen-logger` powers the full Lumen backend ecosystem:  

| Service | Framework | Usage |
|----------|------------|--------|
| **Lumen Media API** | FastAPI | Tracks uploads, MinIO operations, and request correlation |
| **Lumen Reports API** | Django | Logs report generation, PDF exports, and HL7 pushes |
| **Dubin RAG Agent** | FastAPI + LangChain | Provides traceable AI reasoning logs |
| **HL7 Gateway** | FastAPI | Logs message ingestion and outbound Mirth communication |

This package ensures every request in the Lumen system carries a **unique correlation ID**, providing a full trace from the frontend → backend → database → HL7 output.

---

## 🧩 Integration in Other Projects  

`lumen-logger` is designed to be **project-agnostic**.  
It can be dropped into *any* Python system needing structured, consistent logging.

Common integration targets include:
- FastAPI or Django microservices  
- Async data pipelines  
- AI or RAG-based agents (LangChain, OpenAI API integrations)  
- Financial or healthcare-grade backend systems  

---

## 🔁 Versioning & CI/CD Automation  

**Phase 2: Automated Publishing**  
Each release is automatically built and published when a tag is pushed, e.g.:

```bash
git tag v0.3.0
git push origin v0.3.0
```

The GitHub Actions workflow will:
1. Build the wheel and source distribution  
2. Upload build artifacts  
3. Optionally publish to GitHub Packages or PyPI (private or public)

---

## 🔒 License  
**Proprietary – All Rights Reserved**  
© 2025 Anthony Narine  

This software is proprietary and confidential.  
Redistribution, modification, or public disclosure without explicit written permission is strictly prohibited.  

---

## 💡 Author  
**Anthony Narine**  
Creator of the Lumen Healthcare Platform and the Lumen Logger framework.  
Focused on designing modular, reusable backend systems for healthcare and AI infrastructure.  

---

✅ **Next Phase:** Add `.github/workflows/publish.yml` to automate builds and tagging for future releases (`v0.3.1+`).
