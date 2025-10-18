# 🧩 Lumen Logger Package — Editable Install Guide
### Centralized Logging & Shared Utilities Setup

This guide explains how to install the **`lumen_logger`** shared package in *editable mode* across all Lumen microservices — ensuring every environment (FastAPI, Django, etc.) can import and use `configure_logging()` and other shared utilities.

---

## 📦 Overview

`lumen_logger` contains cross-service utilities used by all backends in the Lumen ecosystem, including:

- Centralized logging configuration (`configure_logging`, `reset_logging`)
- Shared constants, validators, and helpers (future)
- Standardized architecture documentation

Because each microservice (`lumen_media`, `lumen_reports`, `lumen_ai`, etc.) runs in its **own virtual environment**, the package must be installed once per venv.

---

## 🧱 Folder Structure

Your project should look like this:

```
D:\react-django\Lumen\Lumen\
├── lumen_logger/
│   ├── __init__.py
│   └── logging_conf.py
├── lumen_media/
│   └── lumen_media_venv/
├── lumen_ai/
│   └── lumen_ai_venv/
├── lumen_reports/
│   └── lumen_reports_venv/
└── setup.py
```

---

## ⚙️ Command Breakdown

### 1. `pip install -e .`

The `-e` flag means **editable mode** — Python installs a *live link* to your source code instead of copying files.

- `pip install .` → copies the files (changes require reinstall)
- `pip install -e .` → creates a symbolic link (changes apply instantly)

✅ Editable mode lets all services use your latest code automatically.

---

## 🧩 Step-by-Step Installation

### 🧠 Example: Installing for Lumen Media

#### Step 1 — Activate the venv
```bash
cd lumen_media
lumen_media_venv\Scripts\activate  # (Windows)
# or source lumen_media_venv/bin/activate (Mac/Linux)
```

#### Step 2 — Navigate to the root directory
(Where `setup.py` lives)
```bash
cd ..
```

#### Step 3 — Install in editable mode
```bash
pip install -e .
```

You should see:
```
Obtaining file:///D:/react-django/Lumen/Lumen
Installing collected packages: lumen-logger
Running setup.py develop for lumen-logger
Successfully installed lumen-logger-0.1.0
```

#### Step 4 — Verify
```bash
python -c "from lumen_logger import configure_logging; print('✅ lumen_logger import successful')"
```

If you see ✅, everything is linked correctly.

---

### 🧱 Repeat for Each Environment

Run the same steps for:
- `lumen_ai/lumen_ai_venv`
- `lumen_reports/lumen_reports_venv`

Each service will now have access to the same shared package.

---

## 🧠 Why Each venv Needs It

Virtual environments are **isolated sandboxes** — packages installed in one are invisible to others.  
Installing `lumen_logger` in editable mode inside each ensures all services can import it while keeping environments clean and independent.

---

## 🧰 Optional: Verify Installed Packages

Check that `lumen-logger` is recognized as an editable install:

```bash
pip list | find "lumen-logger"  # Windows
# or
pip list | grep lumen-logger    # Mac/Linux
```

Output:
```
lumen-logger 0.1.0  editable project location: D:\react-django\Lumen\Lumen
```

---

## 🐋 Docker / CI Usage

When containerizing services, add the same line to your Dockerfile:

```dockerfile
WORKDIR /app
COPY . /app
RUN pip install -e .
```

This ensures the container has access to the shared package automatically.

---

## ✅ Summary

| Step | Command | Description |
|------|----------|-------------|
| 1 | `activate venv` | Enter your service environment |
| 2 | `cd ..` | Return to project root |
| 3 | `pip install -e .` | Create live link to `lumen_logger` |
| 4 | `python -c "from lumen_logger import configure_logging"` | Verify import works |

---

Maintained by: **Anthony Narine**  
© 2025 — The Lumen Project
