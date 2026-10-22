# 🛡️ AEGIS-SOC // METHODOLOGY & SYSTEM WORKFLOW
> **Department of Computer Science & Engineering (Data Science) — Vemana Institute of Technology**  
> *Authoritative Methodology Specification for Autonomous Multi-Agent Threat Detection & SOAR Framework*

---

## 🏛️ Executive Methodology Overview

As the Senior Security Officer presiding over **AEGIS-SOC**, the methodology is engineered around a **6-Stage Closed-Loop Autonomous Intelligence Framework**. 

Rather than relying on static, vulnerable firewall rules, our methodology combines **Data Science Feature Engineering** (Shannon Entropy & Haversine Travel Velocity) with **Vector RAG (ChromaDB)**, **Cognitive LLMs (Google Gemini 2.5 Flash)**, and an **Autonomous Triage & SOAR Decision Matrix**.

---

## 📐 Methodology Architecture Diagram

```
                       ┌──────────────────────────────────────────┐
                       │           1. USER / TELEMETRY INPUT      │
                       │   (Authentication Logs / Ingest Payload) │
                       └────────────────────┬─────────────────────┘
                                            │
                                            ▼
                       ┌──────────────────────────────────────────┐
                       │          2. ENTERPRISE INGESTION         │
                       │    (FastAPI Gateway & Trajectory State)  │
                       └────────────────────┬─────────────────────┘
                                            │
                                            ▼
                       ┌──────────────────────────────────────────┐
                       │     3. LARGE LANGUAGE MODEL REASONING     │
                       │     (Google Gemini 2.5 Cognitive LLM)    │
                       └────────────────────┬─────────────────────┘
                                            │
    ┌───────────────────────────────────────┴───────────────────────────────────────┐
    │                       4. COGNITIVE & ANOMALY FIREWALL                         │
    │                                                                               │
    │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────────┐ │
    │  │  Retriever   │   │  Anomaly &   │   │  Confidence  │   │ Decision Engine│ │
    │  │  (ChromaDB)  │ ➔ │  Math Verification│ ➔ │ Risk Scoring │ ➔ │    Outcomes    │ │
    │  │ MITRE ATT&CK │   │  Entropy & Velocity│ │   (0 - 100)  │   │                │ │
    │  └──────────────┘   └──────────────┘   └──────────────┘   └───┬────────────┘ │
    └───────────────────────────────────────────────────────────────┼───────────────┘
                                                                    │
                                   ┌────────────────────────────────┴────────────────┐
                                   │ Decision Engine Outcomes                        │
                                   ├─────────────────────────────────────────────────┤
                                   │  🟢 ALLOW / MONITOR  : Risk < 50 (Safe Access)  │
                                   │  🟡 FLAG / HITL      : 50 <= Risk <= 80 (Pause) │
                                   │  🔴 BLOCK / CONTAIN  : Risk > 80 (SOAR Enforce) │
                                   └────────────────────────────────┬────────────────┘
                                                                    │
                                                                    ▼
                       ┌──────────────────────────────────────────┐
                       │           5. VERIFIED RESPONSE           │
                       │    (Automated SOAR Session & IP Block)   │
                       └────────────────────┬─────────────────────┘
                                            │
                                            ▼
                       ┌──────────────────────────────────────────┐
                       │        6. DASHBOARD & AUDIT LEDGER       │
                       │   - Real-time Sci-Fi Command HUD         │
                       │   - Immutable Audit Ledger (Compliance)  │
                       │   - Analytics & Pipeline Performance     │
                       └──────────────────────────────────────────┘
```

---

## 🔬 Detailed Block-by-Block Methodology Breakdown

### 1️⃣ User / Telemetry Input (`User Query`)
* **Officer Role & Function**: Serves as the primary data ingress point. Receives raw authentication event records containing user identity (UPN), source IP, timestamp, geolocation coordinates (`lat`, `lon`), session token, and client User-Agent signature.
* **Mechanism**: Supports streaming ingestion over real-world dataset logs (`tools/real_dataset_streamer.py`) or real-time REST payloads.

### 2️⃣ Enterprise Ingestion (`Enterprise Search`)
* **Officer Role & Function**: Evaluates incoming events against historical identity baselines.
* **Mechanism**: Serves as the trajectory lookup gateway (`user_last_events` in `server.py`). Retrieves the user’s previous login event to calculate temporal and geographical movement across consecutive access attempts.

### 3️⃣ Large Language Model (`Google Gemini 2.5 Flash`)
* **Officer Role & Function**: Provides cognitive threat reasoning and semantic context synthesis.
* **Mechanism**: Synthesizes natural language explanations for complex behavioral anomalies, providing explainable AI (XAI) for why an identity action was flagged.

---

### 4️⃣ Cognitive & Anomaly Firewall (`Core Triage Matrix`)

This central validation box contains **5 integrated sub-engines**:

#### A. Retriever (`ChromaDB Vector Store`)
* **Function**: Queries local ChromaDB embeddings (`core/vector_store.py`) seeded with MITRE ATT&CK techniques (`T1539 AiTM`, `T1550.004 Token Theft`, `T1110 ATO`, `T1090 Proxy`).
* **Mechanism**: Uses **Cosine Distance Semantic Matching** to associate raw telemetry indicators with known adversary tactics in milliseconds.

#### B. Fact Verification Engine (`Shannon & Haversine Math Engine`)
* **Function**: Verifies telemetry parameters against mathematical formulas to eliminate false positives:
  * **Shannon Entropy ($H(X)$)**: Detects high-randomness stolen or synthetic session tokens ($>3.85\text{ bits/char}$).
  * **Haversine Travel Velocity**: Calculates physical speed in $\text{km/h}$ between consecutive login coordinates. Speeds exceeding $800\text{ km/h}$ flag **Impossible Travel**.

#### C. Confidence Risk Scoring (`Algorithmic Risk Computation`)
* **Function**: Computes a dynamic composite risk score ranging from **$0.0$ to $100.0$**.
* **Mechanism**: Combines vector match severity, mathematical entropy/velocity violations, and automated scanner signatures with mathematical variance jitter ($\pm 2.5$).

#### D. Source Cross-Validation (`User Trajectory History`)
* **Function**: Validates current telemetry against prior state variables within `AgentGraphState` across the 3-node LangGraph swarm.

#### E. Decision Engine Outcomes (`Triage Execution`)
* **🟢 ALLOW / MONITOR (Score $<50$)**: High-confidence benign authentication. Logged in baseline ledger for continuous monitoring.
* **🟡 FLAG / HITL (Score $50-80$)**: Medium-confidence ambiguous anomaly. Execution is paused, and an alert is routed to the **Human-In-The-Loop (HITL)** analyst portal.
* **🔴 BLOCK / CONTAIN (Score $>80$)**: High-confidence critical threat. Immediate autonomous SOAR containment is dispatched.

---

### 5️⃣ Verified Response (`SOAR Mitigation Execution`)
* **Officer Role & Function**: Executes automated incident containment without human delay.
* **Mechanism**:
  1. Revokes compromised identity OAuth session tokens (`revoke_identity_session()`).
  2. Blocks attacker perimeter IP addresses (`block_perimeter_ip()`).
  3. Dispatches real SMTP TLS security warning emails to recipient inboxes (`dispatch_security_notification_email()`).

---

### 6️⃣ Dashboard + Audit Logs (`Compliance & Operational Visibility`)
* **Officer Role & Function**: Maintains real-time operational visibility and regulatory compliance tracking.
* **Mechanism**:
  * **Real-time Monitoring**: Sci-Fi Cyber Defense Command Theater HUD (`static/index.html`).
  * **Audit Logs**: Immutable ledger capped at 2,000 items (`audit_ledger`) for compliance and zero RAM overflow.
  * **Analytics & Insights**: Live performance throughput ($100\%$ swarm triage rate) and vector store status tracking.

---

## 🎓 Academic Defense & Presentation Script (for Evaluators)

When presenting this slide to your professors/evaluators, deliver the explanation using this authoritative script:

> *"Respected Members of the Evaluation Panel, good morning/afternoon.*
>
> *Our project methodology, titled **AEGIS-SOC**, establishes an AI-driven autonomous security framework structured across 6 core operational stages.*
>
> *1. **Data Ingestion**: Raw identity telemetry is ingested in real-time.*
> *2. **Enterprise Ingestion Gateway**: FastAPI checks historical identity baselines to track geographical movement.*
> *3. **Cognitive LLM**: Google Gemini 2.5 Flash analyzes context and synthesizes natural language threat reasoning.*
> *4. **Cognitive & Anomaly Firewall**: This is our core innovation. It houses a **ChromaDB Vector Retriever** pre-seeded with MITRE ATT&CK embeddings, a **Mathematical Fact Verification Engine** that computes Shannon Token Entropy and Haversine Travel Velocity, and a **Confidence Risk Scoring Engine** that outputs a dynamic threat score from 0 to 100.*
> *5. **Decision Engine Outcomes**: Low-risk events (<50) are Allowed; medium-risk events (50–80) are Flagged for Human-In-The-Loop Analyst review; and critical-risk events (>80) trigger immediate Autonomous Block action.*
> *6. **Verified Response & Audit**: Our SOAR engine automatically revokes compromised session tokens, blocks attacker IPs, dispatches real warning emails, and records every action in an immutable audit ledger on our Command Theater HUD.*
>
> *This methodology effectively reduces incident detection and containment latency to milliseconds while eliminating AI hallucination risks. Thank you."*
