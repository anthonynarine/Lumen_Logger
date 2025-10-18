# ⚙️ Lumen Logger — Public Package Build & Installation Guide (v0.3.4)

## 🧠 Overview

`lumen_logger` is a **public, standalone package** for the Lumen platform.
It provides unified, environment-driven logging and correlation ID tracing
across all Lumen microservices (Media, Reports, Dubin, HL7, etc.).

This guide explains how to:
- Build and version the package
- Run automated tests
- Install it from GitHub
- Use it inside any Lumen service

---

## 🧩 1️⃣ Folder Structure

Lumen_Logger/
├── lumen_logger/
│   ├── logging_conf.py
│   ├── context.py
│   ├── middleware.py
│   └── ...
├── tests/
│   ├── conftest.py
│   ├── test_configure_logging.py
│   ├── test_context.py
│   └── test_middleware.py
├── pyproject.toml
├── requirements.txt
├── README.md
├── LICENSE
└── dist/

---

## 🧱 2️⃣ Installation (Public GitHub)
You can now install it **directly from the public repo**:

```bash
pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.4
```

✅ No tokens or private access required.

---

## 🧪 3️⃣ Running Tests
Ensure `pytest` and `python-dotenv` are installed:
```bash
pip install -r requirements.txt
pytest -v
```

All tests should pass:
```
tests/test_configure_logging.py::test_configure_logging_creates_log_file PASSED
tests/test_middleware.py::test_correlation_middleware_adds_header PASSED
```

---

## ⚙️ 4️⃣ Configure .env for Local Development
Create a `.env` file in your project root:
```bash
LOG_LEVEL=INFO
LOG_TO_FILE=true
LOG_FILE_PATH=./logs
LOG_SERVICE_NAME=test_logger_service
```

---

## 🧾 5️⃣ Using It in a Service
Example (FastAPI):

```python
from lumen_logger import configure_logging, CorrelationIdMiddleware
from fastapi import FastAPI

configure_logging()
app = FastAPI()
app.add_middleware(CorrelationIdMiddleware)
```

---

## 🧱 6️⃣ Automated Builds (CI/CD)
Two workflows now handle automation:

| File | Purpose |
|------|----------|
| `.github/workflows/publish.yml` | Builds and uploads artifacts on version tag |
| `.github/workflows/release.yml` | Creates GitHub Release with `.whl` and `.tar.gz` |

Tag and push:
```bash
git tag v0.3.4
git push origin v0.3.4
```

GitHub Actions will automatically build and publish the release.

---

## 🧠 Summary
| Task | Command |
|------|----------|
| Build package | `python -m build` |
| Run tests | `pytest -v` |
| Install | `pip install git+https://github.com/anthonynarine/Lumen_Logger.git@v0.3.4` |
| Tag new version | `git tag v0.3.4 && git push origin v0.3.4` |

---

**Author:** Anthony Narine  
Founder & Lead Engineer — Lumen Project  
> “A unified log is the heartbeat of a unified system.”  
> — Lumen Engineering Philosophy
