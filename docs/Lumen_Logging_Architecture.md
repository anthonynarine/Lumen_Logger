# 🧩 Lumen Logger — System Architecture Diagram

## 🌍 Overview

Lumen Logger acts as a shared observability backbone across all Lumen microservices.
It unifies console, file, and structured JSON logging — and introduces correlation IDs
to provide distributed request tracing across FastAPI and Django services.

---

## 🧠 System Diagram (High-Level)

```mermaid
flowchart LR
    subgraph Frontend["Lumen Frontend (React)"]
    end

    Frontend -->|REST / WebSocket| Reports
    Reports["Lumen Reports (Django)"] -->|HTTP + X-Correlation-ID| Media["Lumen Media (FastAPI)"]
    Media -->|AI Request| Dubin["Dubin RAG (FastAPI)"]
    Media -->|HL7 ORU| HL7["HL7 Listener (FastAPI)"]

    Reports -->|Structured Logs| Collector["Lumen Log Collector (FastAPI)"]
    Media -->|Structured Logs| Collector
    Dubin -->|Structured Logs| Collector
    HL7 -->|Structured Logs| Collector
    Collector -->|Forward JSON| Grafana[(Grafana Loki / Prometheus)]

    classDef service fill:#151515,stroke:#4fa3ff,stroke-width:1px,color:#fff;
    class Reports,Media,Dubin,HL7,Collector service;
🧾 Data Flow Explanation
Service Startup
Each microservice calls:

python
Copy code
from lumen_logger import configure_logging
configure_logging(service_name="lumen_media")
→ Environment variables define output behavior (console, file, JSON).

Incoming Request
CorrelationIdMiddleware intercepts the request.

If header X-Correlation-ID exists → reuse it.

Otherwise → generate a new UUIDv4.
The ID is stored in a per-request context via contextvars.

Logging Event
When a log is emitted:

logging_conf.py injects contextual data:

service_name

hostname

correlation_id

timestamp

The record is formatted as text (dev) or JSON (prod).

Output Routing

Destination	Handler Type	Purpose
Developer Console	ColorFormatter	Real-time feedback
/logs/<service>.log	RotatingFileHandler	Persistent logs
LOG_COLLECTOR_URL	Async JSON Client	Central aggregation

Central Collector (Optional)

Receives POST batches of logs.

Stores to PostgreSQL or forwards to Grafana Loki.

Enables querying by correlation ID.

🧩 Example Trace (Cross-Service)
java
Copy code
Request: X-Correlation-ID = 9e1a47e1-33c8-4b7b-9f55-d61a04cf2eab

Frontend ─▶ Lumen Reports (Django)
                │
                ├── Logs: "Exam created" (cid=9e1a47e1…)
                │
                ▼
            Lumen Media (FastAPI)
                │
                ├── Logs: "Image upload complete" (cid=9e1a47e1…)
                │
                ▼
            Dubin RAG (FastAPI)
                ├── Logs: "Criteria query resolved" (cid=9e1a47e1…)
                │
                ▼
            Collector → Grafana
📊 Integration Summary
Component	Role	Key Logger Feature
Lumen Reports	Django-based structured reporting	Thread-safe correlation IDs
Lumen Media	Handles uploads, MinIO, metadata	Async logging + correlation
Lumen Dubin	AI microservice (LangChain RAG)	JSON structured logs
Lumen HL7	Outbound ORU/ADT messages	Service-level audit trails
Collector	Optional centralized endpoint	Aggregates + visualizes logs

🔒 Security
PHI and patient identifiers are automatically redacted before output.

HTTPS-only collector connections.

Service-level isolation: each log includes a service_name tag.

Compatible with HIPAA and internal audit requirements.

🧱 Future Roadmap
Feature	Description
Collector Microservice	Async endpoint to receive JSON logs
Prometheus Metrics	Real-time error/warning counters
ElasticSearch Adapter	Long-term storage and full-text search
AI Log Insights (Dubin)	NLP summarization of log patterns

🧠 Author
Anthony Narine
Founder & Lead Engineer — Lumen Project
https://github.com/anthonynarine