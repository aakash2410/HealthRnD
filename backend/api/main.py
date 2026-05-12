from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.api.rag_engine import handle_rag_query
from backend.graph.graph_queries import get_dashboard_metrics, get_scouting_signals, get_all_entities
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Nexus Health Intelligence API")

# Configure CORS to allow our React Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    mode: str = "orchestration"

@app.post("/api/rag")
async def rag_endpoint(request: QueryRequest):
    logger.info(f"Received {request.mode} query from frontend: {request.query}")
    try:
        result = handle_rag_query(request.query, mode=request.mode)
        if result.get("status") == "success":
            return {"status": "success", "response": result["data"], "graph_data": result.get("graph_data")}
        else:
            return {"status": "error", "response": result.get("message", "Unknown error")}
    except Exception as e:
        logger.error(f"RAG Engine failed: {e}")
        return {"status": "error", "response": f"System Error: {str(e)}"}

@app.get("/api/dashboard/metrics")
async def dashboard_metrics():
    return get_dashboard_metrics()

@app.get("/api/dashboard/signals")
async def dashboard_signals():
    return get_scouting_signals()

@app.get("/api/discovery/entities")
async def discovery_entities():
    return get_all_entities()

@app.get("/api/health")
async def health_check():
    return {"status": "online", "database": "Live Neo4j"}
