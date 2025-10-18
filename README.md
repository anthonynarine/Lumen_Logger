# 🩸 Lumen Logger (`lumen-logger`)
**Version:** 0.3.1  
**Author:** Anthony Narine  

---

## 🧭 Overview  

`lumen-logger` is a **distributed logging system** built to unify observability and structured logging across Python-based microservices.

Originally developed for the **Lumen Healthcare Platform**, it now serves as a reusable, standalone package for **FastAPI**, **Django**, or **async Python** applications.

Features include:
- Environment-driven configuration  
- JSON + colorized console output  
- Automatic correlation ID propagation  
- Async + thread-safe handling  
- Optional log collector integration  

---

## ⚙️ Key Features  

| Feature | Description |
|----------|--------------|
| **Dynamic Config** | Configure entirely via environment variables |
| **Dual Output System** | Color console for dev + rotating file/JSON for production |
| **Correlation IDs** | Trace requests across distributed services |
| **Structured JSON Logs** | Ready for ELK, Grafana Loki, or CloudWatch |
| **Async Collector Support** | Non-blocking HTTP log shipping |
| **Zero-Touch Setup** | Just `configure_logging()` — works everywhere |

---

## 🧰 Installation  

### 🪄 From GitHub (Public Repo)
```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@main
```

### 🧩 From Tagged Release
```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.1
```

### 🧱 From Local Build
After running `python -m build`:
```bash
pip install dist/lumen_logger-0.3.1-py3-none-any.whl
```

✅ Verify:
```bash
python -c "from lumen_logger import configure_logging; print('✅ Lumen Logger imported successfully')"
```

---

## 🚀 Quick Start  

### FastAPI Example
```python
from fastapi import FastAPI
from lumen_logger import configure_logging, CorrelationIdMiddleware

configure_logging(service_name="lumen_media")

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
configure_logging(service_name="lumen_reports")

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
| `LOG_FILE_PATH` | `./logs` | Directory for file logs |
| `LOG_MAX_SIZE_MB` | `10` | Max log file size before rotation |
| `LOG_BACKUP_COUNT` | `5` | Number of rotated logs to keep |
| `LOG_SERVICE_NAME` | `default_service` | Used as log prefix |
| `LOG_COLLECTOR_URL` | *None* | Optional async collector endpoint |
| `LOG_ENABLE_CORRELATION` | `true` | Adds correlation IDs automatically |

---

## 🧠 Integration Targets  

| Framework | Use Case |
|------------|-----------|
| **FastAPI** | API & microservice logs with correlation IDs |
| **Django** | App-wide logs, request tracing |
| **LangChain / AI Agents** | Logging token usage & chains |
| **Healthcare Systems** | HIPAA-safe observability and audit trails |
| **Financial Backends** | JSON logs for compliance pipelines |

---

## 🔁 CI/CD & Releases  

`lumen-logger` automatically builds and publishes new releases via **GitHub Actions** whenever a tag is pushed.

```bash
git tag v0.3.1
git push origin v0.3.1
```

✅ This triggers:
- Package build  
- Artifact upload  
- Automatic GitHub Release creation with `.whl` + `.tar.gz`

---

## 🧩 Reuse Across Projects  

`lumen-logger` was engineered as a **universal, enterprise-grade logger**.  
You can integrate it with:
- Lumen Healthcare microservices  
- AI agents like Dubin (LangChain)  
- Future APIs like StockMind or Auth API  
- Any project requiring reliable, structured logging  

---

## 🔒 License  

**MIT License** (Open-Source Release)  
© 2025 Anthony Narine  

This public version of `lumen-logger` may be reused in open-source or commercial projects, provided attribution remains.

---

## 💡 Author  

**Anthony Narine**  
Designing modular, reusable, AI-integrated backend systems for healthcare and enterprise applications.

---

⭐ **If you like this project**, consider starring the repo to support future releases.
