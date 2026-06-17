# BioScout AI: Sovereign Healthcare Intelligence Hub

BioScout AI is a production-grade, hyper-localized Intelligence Platform designed for India's healthcare and agritech sectors. It tracks clinical trials, patent landscapes, and sovereign capital flows by ingesting real-world, verified data from official Government of India portals (CTRI, BIRAC, IP India). 

The platform operates on a strict **Zero Dummy Data Policy**—every node, relationship, and metric is backed by live, verifiable institutional data stored in a native Neo4j Knowledge Graph.

---

## 🏗️ What Works Perfectly (End-to-End)

The core technical pipeline is robust and fully functional:

1. **The React UI (HITL Studio):** 
   - A multi-page, high-fidelity React/Vite dashboard featuring live Recharts and 10-second auto-polling. 
   - Dashboard queries have been optimized to dynamically read all graph nodes (e.g., tracking $45.3M across 757+ active entities).
   - Entity visualization automatically falls back to full, human-readable study/innovation titles instead of technical IDs.
2. **The RAG Analyst Agent (FastAPI):** 
   - Translates frontend API requests into Cypher queries seamlessly.
   - Endpoint routing is perfectly synced (`/api/dashboard/metrics`), delivering real-time graph state to the frontend UI.
3. **The Auditor (Fact-Checking Agent):** 
   - A live Qwen-2.5 7B LLM integration that cross-references ingested nodes in real-time. 
   - Assigns `confidence_scores` and generates `audit_trails` to ensure strict clinical and business validity against hallucinations.
4. **Graph Persistence (Neo4j):** 
   - High-speed batch commit architectures (`UNWIND`) comfortably process hundreds of triplets simultaneously without database degradation.

---

## 🗄️ Current Data Ingestion State

The ingestion engine has transitioned from global generic sources to targeted Indian sovereign registries, though structural challenges remain.

- **Patents (Layer 1):** Actively extracting real patent titles from the **IP India Public Search**.
- **Regulatory (Layer 5):** Pulling live, human-readable clinical trials. Bypassed the heavily guarded main CTRI portal by utilizing the **WHO-ICTRP Sovereign Mirror**. Currently ingesting samples of 50+ high-fidelity trials at a time.
- **Co-Funding (Layer 6):** Successfully captured 549 verified grant records (BIG, SBIRI, BIPP) representing $45.3M in Sovereign Capital Flow. Achieved via a **Live Data Bridge** (browser subagent) that bypasses BIRAC's JavaScript-rendered tables.

---

## 🚧 Gaps in Ingestion & Logical Issues

Due to the inherent architecture of Indian government servers, several structural blockers exist:

1. **CTRI Captcha Blocker:** The main `ctri.nic.in` advanced search form is protected by a mandatory text-in-image CAPTCHA (`T9` field). Pure REST-based scrapers are blocked, forcing reliance on mirror registries.
2. **DNS & Connection Latency:** Portals like `main.icmr.nic.in` frequently suffer from DNS resolution errors (`NameResolutionError`) and severe server timeouts, making synchronous programmatic ingestion highly unstable.
3. **BIRAC Dynamic Rendering:** `birac.nic.in` utilizes hidden JSON/AJAX endpoints with strict session/token requirements and JavaScript-rendered tables. Traditional `requests`/`BeautifulSoup` pipelines return 404s or empty tables, necessitating heavy browser automation (Live Data Bridges).
4. **ICTRP Export Limits:** The WHO-ICTRP mirror limits direct programmatic search exports to 10,000 records per session, capping the speed of total corpus ingestion.

---

## 🚀 Pending System Improvements

To graduate the platform from a "Live Mirror" into a complete "National Archive", the following initiatives are pending:

**1. The 126k Bulk Archive Ingestion**
- *Goal:* Ingest the *entire* national history of Indian clinical trials (126,819 records).
- *Solution:* Procure the full comprehensive CSV/XML dataset directly from the WHO SharePoint facility and process it using a dedicated, high-speed Python `UNWIND` batch loader.

**2. Persistent Task Scheduling**
- *Goal:* Move from manual browser bridges and `ingest_data.py` triggers to autonomous background syncs.
- *Solution:* Deploy **Celery** or **Apache Airflow / Cron** to fetch deltas on a weekly basis, maintaining high availability despite government server downtime.

**3. Automated Entity Resolution (Deduplication)**
- *Goal:* Clean up messy organizational inputs (e.g., merging "Serum Institute" and "Serum Institute of India").
- *Solution:* Integrate a mathematical NLP pipeline (SciSpacy/BioBERT) before node creation to deduplicate graph entities.

**4. Error & Latency Monitoring**
- *Goal:* Provide visibility when sovereign portals are down.
- *Solution:* Implement a dashboard warning system (e.g., "Source Currently Unavailable") to explain temporary lags in ingestion or 0-record pulls.
