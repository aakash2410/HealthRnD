# BioScout AI: Human-in-the-Loop Intelligence Engine

BioScout AI is an advanced, production-ready Intelligence Platform designed for healthcare and agritech investment scouting. It bridges the gap between massive, fragmented global health datasets and actionable strategic insights using a **Human-in-the-Loop (HITL) AI Agent architecture**.

Instead of relying on fragile LLM hallucinations, BioScout AI strictly grounds its analysis on a live **Neo4j Knowledge Graph**, dynamically built by directly querying institutional global APIs.

---

## 🏗️ System Architecture

### 1. The React UI (HITL Studio)
A multi-page, high-fidelity Material Design 3 React application.
*   **Intelligence:** A command center for high-level metrics and funding momentum graphs.
*   **Discovery:** A deep-dive search interface with entity-resolution ontology filters.
*   **Orchestration Studio:** A split-canvas editor where analysts watch the AI draft an Investment Memo in real-time on the left, while verifying the raw Neo4j "Evidence Graph" nodes on the right. 

### 2. The RAG Analyst Agent (FastAPI)
The central intelligence node (`backend/api/rag_engine.py`). When a user queries the platform, the backend translates the query into a multi-hop Cypher query against Neo4j, retrieves the ground-truth nodes (startups, clinical trials, patents), and uses a Large Language Model to synthesize a highly structured, compliance-ready Investment Memo.

### 3. Live Data Ingestion Engine
To showcase the true power of the platform, the backend (`backend/ingestion/`) utilizes a 100% real-world ETL pipeline. It queries four massive, open-access databases, transforming their JSON payloads into Subject-Predicate-Object triplets:
*   **Scientific (Layer 1):** NCBI E-utilities (PubMed) for live research abstracts and researcher affiliations.
*   **Market/Institutional (Layer 3):** OpenAlex API for institutional momentum and geographic mapping (bypassing expensive Tracxn keys).
*   **Regulatory (Layer 5):** ClinicalTrials.gov (v2) for live, global clinical trial phases and sponsors.
*   **Co-Funding (Layer 6):** NIH RePORTER API to scrape millions of dollars in live, verified government grant disbursements.

---

## 🚀 Quickstart

**1. Start the Graph Database**
Ensure Docker is running, then spin up the local Neo4j instance:
```bash
docker-compose up -d
```

**2. Populate the Knowledge Graph**
Fetch live data from the global APIs and push it into Neo4j:
```bash
python3 ingest_data.py
```

**3. Run the AI Backend**
Start the FastAPI server:
```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

**4. Run the React Frontend**
Launch the multi-page Material Design interface:
```bash
cd frontend
npm run dev
```

---

## 🔮 Next Steps & Scaling Roadmap

While the prototype currently hits global databases to prove its structural integrity, transitioning it into a hyper-localized Indian context requires specific engineering pushes:

**1. Build the Indian Web Scrapers (Data Layer)**
*   *The Problem:* Global APIs (like NIH and ClinicalTrials.gov) miss hyper-local Indian funding (BIRAC/SERB) and Phase 1 AYUSH clinical trials.
*   *The Solution:* We must build raw Python `BeautifulSoup` web scrapers to extract HTML tables directly from the CTRI (Clinical Trials Registry India) and BIRAC portals, bypassing their lack of REST APIs.

**2. Automate the Pipeline (Orchestration Layer)**
*   *The Problem:* Running `ingest_data.py` manually is not scalable.
*   *The Solution:* Deploy **Apache Airflow** or **Prefect** to automatically schedule the ingestion scripts to run every Sunday night, fetching only the *delta* (new trials/patents) since the last run.

**3. Entity Resolution Engine (NLP Layer)**
*   *The Problem:* Messy data means "Serum Institute" and "Serum Institute of India" might be treated as two separate nodes.
*   *The Solution:* Reintroduce the **SciSpacy / BioBERT** NLP pipeline to mathematically merge and deduplicate entities before they hit the Neo4j database.

**4. Cloud Deployment (Infra Layer)**
*   *The Problem:* The Neo4j database is currently running locally on Docker.
*   *The Solution:* Migrate the graph to **Neo4j AuraDB Enterprise** so the entire platform can be securely accessed via the web by the wider Foundation team.
