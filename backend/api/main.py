from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.api.rag_engine import handle_rag_query
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

@app.post("/api/rag")
async def rag_endpoint(request: QueryRequest):
    logger.info(f"Received query from frontend: {request.query}")
    try:
        result = handle_rag_query(request.query)
        # handle_rag_query returns a dict like {"status": "success", "data": "string", "graph_data": {...}}
        if result.get("status") == "success":
            return {"status": "success", "response": result["data"], "graph_data": result.get("graph_data")}
        else:
            return {"status": "error", "response": result.get("message", "Unknown error")}
    except Exception as e:
        logger.error(f"RAG Engine failed: {e}")
        return {"status": "error", "response": f"System Error: {str(e)}"}

@app.get("/api/health")
async def health_check():
    return {"status": "online", "database": "Live Neo4j"}
