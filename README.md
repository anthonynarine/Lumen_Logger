# 🩸 Lumen Logger (`lumen-logger`)
**Version:** 0.3.4  
**Author:** Anthony Narine  

---

## 🧭 Overview  

`lumen-logger` is a **distributed, enterprise-grade logging system** designed to unify observability and structured logging across Python-based microservices.

Originally built for the **Lumen Healthcare Platform**, it now serves as a reusable, standalone package for **FastAPI**, **Django**, and **async Python** applications.

Features include:
- Dynamic `.env`-driven configuration  
- Colorized + structured JSON output  
- Automatic correlation ID injection  
- Thread- and async-safe initialization  
- Zero-touch setup (`configure_logging()` just works)  
- Collector-ready for centralized log aggregation  

---

## ⚙️ Key Features  

| Feature | Description |
|----------|--------------|
| **Dynamic Config** | Reads settings from `.env` and environment vars at runtime |
| **Dual Output System** | Color console (dev) + rotating file logs (prod) |
| **Correlation IDs** | Distributed tracing for microservice observability |
| **Structured JSON Logs** | ELK / Grafana Loki compatible |
| **Async Collector Ready** | Non-blocking HTTP log shipping (future-ready) |
| **Zero-Touch Setup** | Works in FastAPI or Django without custom config |

---

## 🧰 Installation  

### 🪄 From GitHub (Public Repo)
```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.4
```

✅ No tokens required — this is a public, CI-built package.

### 🧱 From Local Build
After running `python -m build`:
```bash
pip install dist/lumen_logger-0.3.4-py3-none-any.whl
```

---

## 🚀 Quick Start  

### FastAPI Example
```python
from fastapi import FastAPI
from lumen_logger import configure_logging, CorrelationIdMiddleware

configure_logging()

app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

### Django Example
```python
# settings.py
from lumen_logger import configure_logging
configure_logging()

MIDDLEWARE = [
    'lumen_logger.middleware.DjangoCorrelationMiddleware',
    ...
]
```

---

## ⚙️ Environment Variables  

| Variable | Default | Description |
|-----------|----------|--------------|
| `LOG_LEVEL` | `INFO` | Log verbosity level |
| `LOG_FORMAT` | `text` | Output type (`text` or `json`) |
| `LOG_TO_FILE` | `true` | Enables rotating file logs |
| `LOG_FILE_PATH` | `./logs` | Directory for log files |
| `LOG_MAX_SIZE_MB` | `10` | Max file size before rotation |
| `LOG_BACKUP_COUNT` | `5` | Number of rotated logs to keep |
| `LOG_SERVICE_NAME` | `lumen_service` | Service identifier |
| `LOG_COLLECTOR_URL` | *None* | Optional async collector endpoint |
| `LOG_ENABLE_CORRELATION` | `true` | Enables correlation ID tracing |

### Example `.env`
```bash
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_FILE_PATH=./logs
LOG_SERVICE_NAME=lumen_media
```

---

## 🧪 Testing

Lumen Logger includes a full test suite.

Run locally:
```bash
pip install -r requirements.txt
pytest -v
```

Expected output:
```
tests/test_configure_logging.py::test_configure_logging_creates_log_file PASSED
tests/test_middleware.py::test_correlation_middleware_adds_header PASSED
```

---

## 🔁 CI/CD & Releases  

`lumen-logger` builds and publishes new releases automatically via **GitHub Actions** when a tag is pushed:

```bash
git tag v0.3.4
git push origin v0.3.4
```

✅ Actions perform:
- Package build  
- Artifact upload  
- GitHub Release creation with `.whl` and `.tar.gz`

---

## 📘 Documentation  

Full documentation is available in `/docs`:

- [`Lumen_Logging_Architecture.md`](docs/Lumen_Logging_Architecture.md)
- [`Lumen_Logger_Package_Guide_v2.md`](docs/Lumen_Logger_Package_Guide.md)

---

## 🧩 Reuse Across Projects  

`lumen-logger` powers the following Lumen microservices:
- **Lumen Media API**
- **Lumen Reports API**
- **Dubin (RAG Agent)**
- **HL7 Gateway**
- **Billing API**
- and any future FastAPI or Django projects

---

## 🔒 License  

**MIT License**  
© 2025 Anthony Narine  

This public package may be used in open-source or commercial applications with attribution.

---

## 💡 Author  

**Anthony Narine**  
Founder & Lead Engineer — Lumen Project  
Designing modular, reusable, AI-integrated backend systems for healthcare and enterprise observability.

---

⭐ **Star the repo** if you find it useful — every star supports the Lumen open-source ecosystem.
