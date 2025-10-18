# ⚙️ Lumen Logger — Private Package Build & Installation Guide

## 🧠 Overview

`lumen_logger` is designed as a **standalone internal Python package** for the Lumen platform.
It provides unified, environment-driven logging and correlation ID tracing across all Lumen
microservices (Media, Reports, Dubin, HL7, etc.).

This guide explains **how to build, version, and install** the package privately from GitHub
so that every service can consume it using `pip`.

---

## 🧩 1️⃣ Folder Structure

Lumen/
├── lumen_logger/
│ ├── lumen_logger/
│ │ ├── init.py
│ │ ├── logging_conf.py
│ │ ├── context.py
│ │ ├── middleware.py
│ │ └── ...
│ ├── pyproject.toml
│ ├── README.md
│ ├── LICENSE
│ └── dist/ (auto-generated after build)

---

## 🧱 2️⃣ Build the Package

### Step 1 — Install Build Tools
```bash
cd lumen_logger
pip install build
```

### Step 2 — Build the Wheel & Source Distribution
```bash
python -m build
```
✅ Output:
```
Building wheel for lumen-logger (pyproject.toml)
Successfully built lumen_logger-0.2.0-py3-none-any.whl
```

### Step 3 — Verify the Build
```bash
ls dist/
# lumen_logger-0.2.0-py3-none-any.whl
# lumen_logger-0.2.0.tar.gz
```

---

## 🧰 3️⃣ Test Local Installation
From any other Lumen service (e.g., lumen_media):

```bash
pip install ../lumen_logger/dist/lumen_logger-0.2.0-py3-none-any.whl
```
Then verify:

```bash
python -c "from lumen_logger import configure_logging; print('✅ lumen_logger works!')"
```

---

## 🔒 4️⃣ Install from Private GitHub Repo
Since the main Lumen repo is private, you can install directly from it without publishing publicly.

### Method 1 — Subdirectory Install (Recommended)
Add this to your service’s `requirements.txt`:
```
git+https://<TOKEN>@github.com/anthonynarine/Lumen.git#subdirectory=lumen_logger
```
Then run:
```bash
pip install -r requirements.txt
```

✅ Pip will clone the private repo (authenticated) and install only the `lumen_logger` subdirectory.

### Method 2 — Environment Variable for Token
To avoid hardcoding your token:

#### `.env`
```ini
GITHUB_TOKEN=ghp_your_github_token_here
```

#### PowerShell
```powershell
$env:GITHUB_TOKEN="ghp_your_github_token_here"
pip install git+https://$env:GITHUB_TOKEN@github.com/anthonynarine/Lumen.git#subdirectory=lumen_logger
```

#### Linux/Mac
```bash
export GITHUB_TOKEN=ghp_your_github_token_here
pip install git+https://$GITHUB_TOKEN@github.com/anthonynarine/Lumen.git#subdirectory=lumen_logger
```

---

## 🩸 5️⃣ Version Tagging for Releases
To create versioned builds:
```bash
cd lumen_logger
git add .
git commit -m "lumen-logger v0.2.0"
git tag v0.2.0
git push origin main --tags
```

You can now install specific versions:
```bash
pip install git+https://<TOKEN>@github.com/anthonynarine/Lumen.git@v0.2.0#subdirectory=lumen_logger
```

---

## 🌍 6️⃣ Optional — GitHub Packages (Private PyPI Registry)
You can also publish `lumen_logger` to GitHub Packages for internal pip installs.

### Step 1 — Create Token
Go to: https://github.com/settings/tokens

Click **Generate new token (classic)** and give it:

- `repo`
- `read:packages`
- `write:packages`

### Step 2 — Upload Package
```bash
pip install twine
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

### Step 3 — Install via Packages
```bash
pip install lumen-logger   --extra-index-url https://__token__:<YOUR_GITHUB_TOKEN>@pypi.github.com/anthonynarine/simple
```

---

## 🧱 7️⃣ CI/CD (Automatic Builds via GitHub Actions)
You can automate builds with this workflow:

`.github/workflows/publish.yml`
```yaml
name: Publish Lumen Logger

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install build tools
        run: pip install build twine
      - name: Build package
        run: python -m build ./lumen_logger
      - name: Publish to GitHub Packages
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.GITHUB_TOKEN }}
        run: |
          twine upload --repository-url https://upload.pypi.org/legacy/ lumen_logger/dist/*
```
✅ Every time you tag a version (`v0.3.0`), GitHub builds and uploads it automatically.

---

## 🧩 8️⃣ Verification Commands

| Purpose | Command | Notes |
|----------|----------|-------|
| Check installed version | `pip show lumen-logger` | Shows current version |
| List installed files | `pip show -f lumen-logger` | File paths |
| Verify imports | `python -c "import lumen_logger; print(lumen_logger.__file__)"` | Confirms import |
| Uninstall | `pip uninstall lumen-logger` | Clean removal |

---

## 🔐 Security Notes
- Tokens are scoped and revocable — never commit them to Git.
- All installs occur over HTTPS.
- Logs generated by `lumen_logger` never contain PHI by design.
- Suitable for HIPAA-compliant environments when collector uses TLS.

---

## 🧱 Summary

| Task | Command | Notes |
|------|----------|-------|
| Build package | `python -m build` | Generates .whl + .tar.gz |
| Local test install | `pip install ../lumen_logger/dist/...` | Verify imports |
| Private install (subdir) | `pip install git+https://<TOKEN>@github.com/anthonynarine/Lumen.git#subdirectory=lumen_logger` | Recommended |
| Tag new version | `git tag v0.3.0 && git push origin main --tags` | Versioned releases |
| GitHub Actions build | Automatic | On tag push |

---

## 💬 Author
**Anthony Narine**  
Founder & Lead Engineer — Lumen Project  
https://github.com/anthonynarine  

> “A unified log is the heartbeat of a unified system.”  
> — Lumen Engineering Philosophy
