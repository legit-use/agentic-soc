# 🎓 AEGIS-SOC // 3-SPEAKER UNIVERSITY PANEL PRESENTATION SCRIPT
> **Project Title**: AEGIS-SOC: AI-Powered Autonomous Multi-Agent Framework for Enterprise Cyber Defense  
> **Target Duration**: ~30 Minutes Total (Approx. 8–10 Minutes per Speaker)  
> **Department**: Department of Computer Science & Engineering (Data Science) — Vemana Institute of Technology

---

## 👥 Speaker Allocation Summary

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│  SPEAKER 1 (00:00 – 10:00) : Introduction, Problem Statement, Objectives & Data   │
│  SPEAKER 2 (10:00 – 20:00) : Multi-Agent Swarm, Math Engines & Vector RAG        │
│  SPEAKER 3 (20:00 – 30:00) : SOAR Mitigation, Live HUD Demo, Outcomes & Viva QA  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

# 🎙️ SPEAKER 1: Introduction, Problem Statement, Objectives & Data Architecture (00:00 – 10:00)

### 📌 Slide 1: Title & Introduction (2 Mins)
> *"Good morning respected internal guide, external examiners, and members of the evaluation panel. My name is [Speaker 1 Name], and along with my team members [Speaker 2 Name] and [Speaker 3 Name], we are proud to present our final year project titled **'AEGIS-SOC: An AI-Powered Autonomous Multi-Agent Framework for Enterprise Cyber Defense'**.*
>
> *In today's digital landscape, modern enterprises face an unprecedented volume of sophisticated cyberattacks. Traditional Security Operations Centers (SOCs) are overwhelmed by thousands of daily alerts, leading to severe analyst fatigue and critical detection delays that take human teams an average of 200 days to identify a breach. Our project addresses this critical challenge by engineering an autonomous, multi-agent AI framework that ingests, analyzes, and mitigates advanced cyber threats in milliseconds without human latency."*

---

### 📌 Slide 2: Problem Statement & Existing Limitations (2.5 Mins)
> *"Let us examine why existing enterprise cybersecurity defenses fail against modern attack vectors:*
>
> 1. *First, **Static Rule-Based Limitations**: Traditional firewalls and SIEM systems rely on fixed threshold rules that attackers easily evade using rotating proxies and dynamic IP addresses.*
> 2. *Second, **Advanced Identity Attacks**: Attacks such as **Adversary-in-the-Middle (AiTM) Phishing** steal active session tokens directly from memory, completely bypassing Multi-Factor Authentication (MFA).*
> 3. *Third, **Token Theft & Replay**: Pass-the-cookie attacks allow attackers to hijack legitimate user sessions without triggering standard password alerts.*
> 4. *And fourth, **Alert Fatigue & Response Latency**: Human security analysts spend hours manually correlating log data, allowing adversaries sufficient dwell time to move laterally.*
>
> *Therefore, there is an urgent industry need for an autonomous system that uses mathematical anomaly verification, vector threat intelligence, and multi-agent reasoning to contain breaches instantly."*

---

### 📌 Slide 3: Project Objectives (2.5 Mins)
> *"To solve these industry challenges, we established six concrete technical objectives:*
>
> 1. *To develop a real-time, AI-based autonomous security framework for detecting and preventing identity cyber threats.*
> 2. *To design a 3-node stateful multi-agent swarm architecture consisting of Ingestion, Analysis, and Response agents.*
> 3. *To mathematically detect advanced attacks including AiTM phishing, session token theft, and automated account takeovers.*
> 4. *To integrate Large Language Models (Google Gemini 2.5 Flash) and ChromaDB Vector RAG for explainable cognitive threat reasoning.*
> 5. *To achieve sub-second incident mitigation through an automated SOAR engine that revokes sessions, blocks perimeter IPs, and dispatches real security alert emails.*
> 6. *And to provide full enterprise transparency through an immutable audit ledger and an interactive Human-In-The-Loop analyst dashboard."*

---

### 📌 Slide 4: Data Ingestion & Large-Scale Streaming Architecture (3 Mins)
> *"Now, let us examine how our system ingests and processes large-scale enterprise data.*
>
> *Instead of relying on synthetic toy data, we evaluated our system on a real-world **31-Million Row Risk-Based Authentication (RBA) Dataset** from Kaggle, comprising 462 MB of dense authentication logs.*
>
> *Processing a file of this scale traditionally crashes server memory. We solved this by engineering an **$O(1)$ Memory Generator Streamer** in `tools/real_dataset_streamer.py`. Using Python iterators, our pipeline reads CSV records row-by-row, keeping system RAM consumption at an ultra-low **35 megabytes** while maintaining high throughput of **50 to 150 events per second**.*
>
> *Each record is dynamically normalized into our standardized `TelemetryEvent` schema, extracting seven critical attributes: User Principal Name (UPN), Source IP, Geolocation Coordinates (`lat`, `lon`), User-Agent string, Session Cookie, and Timestamp.*
>
> *I will now hand over to [Speaker 2 Name] to explain our mathematical anomaly engines, vector threat memory, and multi-agent swarm architecture. Thank you."*

---

# 🎙️ SPEAKER 2: Multi-Agent Swarm, Math Engines & Vector RAG (10:00 – 20:00)

### 📌 Slide 5: Mathematical Anomaly Detection Engines (3 Mins)
> *"Thank you, [Speaker 1 Name]. Good morning respected examiners. My name is [Speaker 2 Name], and I will walk you through the core mathematical engines and multi-agent reasoning intelligence of AEGIS-SOC.*
>
> *To eliminate AI hallucinations and false alarms, we do not rely solely on LLMs for detection. Instead, we developed a deterministic **Mathematical Anomaly Engine** in `core/math_engine.py` featuring two foundational algorithms:*
>
> 1. *First is **Shannon Token Entropy ($H(X)$)**:*
>    $$\text{Entropy } H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
>    *This formula measures character randomness in session tokens. Legitimate session cookies follow structured patterns, whereas stolen, randomized, or synthetic session tokens exhibit high randomness. If calculated entropy exceeds **3.85 bits per character**, the system immediately flags **Session Token Theft (MITRE T1550.004)**.*
>
> 2. *Second is the **Haversine Travel Velocity Formula**:*
>    *When a user logs in from two consecutive locations, our system calculates the great-circle geographic distance across the Earth's sphere. Dividing distance by elapsed time produces physical travel speed in km/h. If velocity exceeds **800 km/h** (e.g., logging in from London and then Tokyo 5 minutes later at 19,000 km/h), it mathematically proves **Impossible Travel / AiTM Phishing (MITRE T1539)**.*"

---

### 📌 Slide 6: ChromaDB Vector Threat Memory & Retrieval-Augmented Generation (RAG) (3.5 Mins)
> *"Next is our **Vector Threat Intelligence Memory** implemented in `core/vector_store.py`.*
>
> *We deployed a local **ChromaDB Vector Database** pre-seeded with mathematical vector embeddings of the global **MITRE ATT&CK Enterprise Matrix**.*
>
> *When an anomaly is detected, Node 2 converts the telemetry indicators into semantic text and performs a **Cosine Distance Vector Search** in milliseconds. This maps the active event to standardized tactics:*
> * `T1539`: Adversary-in-the-Middle (AiTM) Phishing
> * `T1550.004`: Pass-the-Cookie / Web Session Token Theft
> * `T1110`: Brute Force / Automated Account Takeover (ATO)
> * `T1090`: Suspicious Proxy / Anonymizer VPN Anomaly
>
> *This vector retrieval grounds our **Google Gemini 2.5 Flash LLM**, providing the model with exact MITRE context so it synthesizes natural language, explainable threat narratives without hallucinations."*

---

### 📌 Slide 7: LangGraph 3-Node Stateful Swarm & Triage Matrix (3.5 Mins)
> *"To orchestrate autonomous reasoning, we built a 3-node stateful swarm using **LangGraph** (`agents/graph_pipeline.py`):*
>
> * **Node 1: Ingestion Agent**: Extracts mathematical features (Entropy & Velocity) and attaches user trajectory history to `AgentGraphState`.
> * **Node 2: Threat Analysis Agent**: Queries ChromaDB RAG, invokes Gemini 2.5 LLM, and calculates a dynamic composite risk score from **$0.0$ to $100.0$** with mathematical variance jitter ($\pm 2.5$).
> * **Node 3: Response Agent**: Evaluates our **3-Tier Triage Decision Matrix**:
>   1. **Score $< 50.0$ (AUTONOMOUS MONITOR)**: Verified safe corporate access recorded in the baseline ledger.
>   2. **Score $50.0 - 80.0$ (HUMAN-IN-THE-LOOP REVIEW)**: Ambiguous anomaly (e.g., unusual VPN location). Automated containment is paused, routing the case to the analyst portal.
>   3. **Score $> 80.0$ (AUTONOMOUS CRITICAL BLOCK)**: High-severity breach triggering immediate automated SOAR response.
>
> *I now invite [Speaker 3 Name] to demonstrate our SOAR mitigation enforcer, Command HUD, and achieved project outcomes."*

---

# 🎙️ SPEAKER 3: SOAR Mitigation, Command HUD Demo, Outcomes & Viva QA (20:00 – 30:00)

### 📌 Slide 8: Enterprise SOAR Mitigation Engine (2.5 Mins)
> *"Thank you, [Speaker 2 Name]. Respected members of the panel, my name is [Speaker 3 Name], and I will present our automated mitigation engine, Command Theater HUD, and verified project outcomes.*
>
> *Detection without response is meaningless. In `core/mitigation_engine.py`, we developed an **Enterprise SOAR Enforcer** that executes sub-second containment across three automated layers:*
> 1. *First, **OAuth Identity Session Revocation**: Instantly invalidates compromised session cookies and forces token expiration in the Identity Provider.*
> 2. *Second, **Perimeter IP Firewall Blocking**: Automatically pushes the attacker's IP address to the firewall blacklist.*
> 3. *Third, **Real SMTP Security Email Dispatch**: Using Python `smtplib` over secure TLS (Port 587), our engine automatically generates and delivers HTML warning emails directly to the victim employee's inbox and SOC team.*
>
> *This reduces incident containment time from hours to under **50 milliseconds**."*

---

### 📌 Slide 9: Tactical Cyber Defense Command Theater HUD & Memory Safety (3 Mins)
> *"To give security teams real-time operational control, we developed the **Cyber Defense Command Theater HUD** (`static/index.html`):*
>
> * **Central Lock Status Theater**: Dynamically displays lock state (*SYSTEM SECURE* in Green, *HITL REVIEW* in Amber, and *CRITICAL BREACH CONTAINED* in Red) with live risk score readouts.
> * **Dynamic Target Scanner**: Changes color and animation dynamically based on real-time perimeter threat level.
> * **Shannon Entropy Waveform Spectrum**: Visualizes real-time token randomness ($H(X)$) across live data streams.
> * **Human-In-The-Loop (HITL) Review Portal**: Allows analysts to open ambiguous alerts, inspect telemetry evidence, add justification notes, and click **[AUTHORIZE BLOCK]** or **[DISMISS FALSE POSITIVE]**.
> * **Memory-Bounded Audit Ledger**: To guarantee backend stability during 31-million row streams, our server enforces a **2,000-item sliding window array cap**, keeping server memory bounded under 50 MB RAM forever."*

---

### 📌 Slide 10: Achieved Outcomes & Verification (2 Mins)
> *"We rigorously verified our system against automated integration tests in `test_system.py`, achieving a **100% pass rate** across all subsystems:*
>
> * ✔ **Mathematical Accuracy**: Verified Shannon Entropy at 4.98 bits/char and Haversine velocity at 19,117 km/h.
> * ✔ **Vector RAG Matching**: Verified cosine distance retrieval against MITRE T1539 and T1090.
> * ✔ **SOAR Execution**: Verified autonomous token revocation, IP blocking, and TLS email dispatch.
> * ✔ **HITL API Lifecycle**: Verified both APPROVED and DISMISSED analyst routes.
> * ✔ **Dataset Scalability**: Successfully ingested 31 million log entries with zero memory leaks."*

---

### 📌 Slide 11: Applications, Future Scope & Conclusion (2.5 Mins)
> *"**Applications**: AEGIS-SOC is directly deployable across **Banking & FinTech** to stop account takeovers, **Cloud Identity Providers (Azure AD/Okta)** to stop AiTM MFA bypass, **Healthcare Networks** for HIPAA protection, and **MSSPs** for multi-tenant monitoring.
>
> **Future Scope**: Our roadmap includes integrating local offline LLMs (Llama 3.3 / DeepSeek-R1) for zero cloud latency, deploying dynamic **canary honeypot tokens** to trap adversaries, and using **Graph Neural Networks (GNNs)** to predict lateral movement.
>
> In conclusion, **AEGIS-SOC** proves that combining deterministic mathematics, vector threat memory, and LangGraph multi-agent AI delivers true autonomous, explainable, and sub-second cyber defense.
>
> Thank you, respected panel. We are now open for your questions."*

---

## 🎯 Quick-Reference Viva Q&A Cheat Sheet (For All 3 Speakers)

| Likely Question from Examiners | Who Answers | Key Answer Points |
| :--- | :---: | :--- |
| **Q1: How do you prevent LLM Hallucinations?** | **Speaker 2** | *"We do not rely solely on LLMs. Detection is driven by deterministic mathematics (Shannon Entropy & Haversine formula) and ChromaDB MITRE ATT&CK embeddings. Gemini LLM is only used for narrative explanation, not raw decision thresholds."* |
| **Q2: How did you handle 31 Million rows (462 MB) without crashing RAM?** | **Speaker 1** | *"We implemented an $O(1)$ memory generator streamer in Python using `csv.DictReader` iterators and a 2,000-item sliding window cap on the audit ledger. RAM usage remains constant at ~35 MB."* |
| **Q3: What happens when an ambiguous risk score (50–80) occurs?** | **Speaker 3** | *"The system enters Human-In-The-Loop (HITL) mode. Automated blocking is paused, the Command HUD displays an amber lock alert, and an analyst reviews the evidence to either authorize containment or dismiss false positives."* |
| **Q4: How does AiTM Phishing bypass MFA, and how do you stop it?** | **Speaker 1 / 2** | *"AiTM uses reverse proxies to steal post-authentication session cookies. We detect it because the stolen cookie is replayed from a new IP/location within minutes, violating our Haversine velocity threshold (>800 km/h)."* |
| **Q5: What is the purpose of ChromaDB Vector Database here?** | **Speaker 2** | *"ChromaDB provides sub-millisecond semantic retrieval using cosine distance. It maps observed attack indicators to standardized MITRE ATT&CK technique vectors (T1539, T1550.004, T1110, T1090)."* |
