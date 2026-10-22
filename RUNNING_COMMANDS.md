# 🚀 AEGIS-SOC // MANUAL EXECUTION COMMAND GUIDE
> **Quick Terminal Command Reference to Run the Server, Stream Data, Inject Attacks & Run Tests**

---

## 📌 Step 1: Open PowerShell / Terminal in Project Directory
```powershell
cd "C:\Users\harsh\OneDrive\Desktop\anti gravity  soc"
```

---

## 🌐 Step 2: Start the Main FastAPI Server & Command HUD Dashboard
Start the backend server on `http://localhost:8000`:
```powershell
python server.py
```
* **Dashboard URL**: Open **`http://localhost:8000`** in your browser (Google Chrome / Edge).
* **Live API Docs**: Open **`http://localhost:8000/docs`** for interactive Swagger REST endpoints.

---

## ⚡ Step 3: Stream Real 31-Million Row Kaggle RBA Dataset
Open a **new terminal window** and run the high-speed $O(1)$ memory streamer:
```powershell
python tools/real_dataset_streamer.py
```
* Press **Enter** at the path prompt (auto-discovers `my_dataset.csv\rba-dataset.csv`).
* Select **`1`** for **High-Speed Bulk Stream** (~50–150 events/sec).
* Select **`2`** for **Real-Time Presentation Stream** (1 event/sec).

---

## 🎯 Step 4: Run Interactive SIEM CLI Attack Injector
To inject custom individual attack scenarios directly from the terminal:
```powershell
python tools/external_siem_injector.py
```
* Option `1`: Ingest Legitimate Corporate Baseline Login
* Option `2`: Ingest Adversary-in-the-Middle (AiTM) Phishing (Tokyo Geo Jump)
* Option `3`: Ingest High Entropy Token Theft Payload
* Option `4`: Ingest Automated Brute Force Scanner (Hydra / Nmap UA)

---

## 🧪 Step 5: Run Automated Integration Tests (6/6 Pass Rate)
To verify all math engines, LangGraph swarm, vector RAG, and SOAR endpoints:
```powershell
python test_system.py
```

---

## 📄 Step 6: Generate Architecture & Technical Inventory PDFs
To compile freshly styled presentation PDF documents:
```powershell
python tools/generate_pdf_docs.py
python tools/generate_inventory_pdf.py
```
* Output 1: `PROJECT_ARCHITECTURE_AND_DATAFLOW.pdf`
* Output 2: `PROJECT_TECHNICAL_INVENTORY.pdf`
