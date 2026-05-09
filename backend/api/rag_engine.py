import os
from typing import Any, Dict
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from backend.core.logger import get_logger
from backend.core.exceptions import ModelInferenceError
from backend.core.utils import retry_with_backoff

# Import ingestion functions to simulate Graph retrieval locally
from backend.ingestion.layer1_pubmed import fetch_patent_data
from backend.ingestion.layer3_market import fetch_tracxn_data
from backend.ingestion.layer5_regulatory import fetch_ddrs_api
from backend.graph.graph_builder import generate_bkg_triplets

load_dotenv()
logger = get_logger(__name__)

HF_API_TOKEN = os.environ.get("HF_API_KEY")

def _validate_query(query: str) -> None:
    """Validates the input natural language query."""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

def _perform_vector_search(query: str) -> str:
    """
    Simulates a Vector/Cypher search against Neo4j.
    Fetches raw triplets, filters by keywords, and converts to a context string.
    """
    logger.info(f"Simulating graph vector search for query: {query}")
    
    # 1. Fetch data and generate triplets
    patents = fetch_patent_data()
    tracxn = fetch_tracxn_data()
    ddrs = fetch_ddrs_api()
    
    all_triplets = []
    all_triplets.extend(generate_bkg_triplets(patents, "layer1_patent"))
    all_triplets.extend(generate_bkg_triplets(tracxn, "layer3_tracxn"))
    all_triplets.extend(generate_bkg_triplets(ddrs, "layer5_ddrs"))
    
    # 2. Simple keyword matching (Simulating Vector Search)
    keywords = set(query.lower().split())
    relevant_context = []
    
    for t in all_triplets:
        subject = str(t.get("subject_id", "")).lower()
        obj = str(t.get("object_id", "")).lower()
        
        # If any word in the query matches the subject or object
        if any(k in subject for k in keywords) or any(k in obj for k in keywords) or "who" in keywords or "what" in keywords:
            source_url = t.get("object_props", {}).get("source_url", "No URL")
            sentence = f"{t['subject_id']} ({t['subject_label']}) {t['relation']} {t['object_id']} ({t['object_label']}). [Source: {source_url}]"
            if sentence not in relevant_context:
                relevant_context.append(sentence)
                
    if not relevant_context:
        return "No relevant context found in the Knowledge Graph."
        
    return "\n".join(relevant_context[:10]) # Limit context to top 10

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def _generate_llm_response(context: str, query: str) -> str:
    """Calls Hugging Face LLM to generate response based on context."""
    logger.info("Orchestrating LLM for final response.")
    
    if not HF_API_TOKEN:
        logger.warning("HF_API_KEY not found. Returning mocked RAG.")
        return f"Mocked RAG response based on context: {context[:50]}..."
        
    try:
        client = InferenceClient(token=HF_API_TOKEN)
        
        system_prompt = (
            "You are an AI assistant for a Healthcare Scouting Platform. "
            "Use the provided Knowledge Graph context to answer the user's query. "
            "Always include the source URLs in your answer as clickable Markdown links. "
            "Do not make up information that is not in the context."
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
        ]
        
        # Use a highly capable, fast instruct model supported by the Chat endpoint
        response = client.chat_completion(
            messages=messages, 
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=500
        )
        
        answer = response.choices[0].message.content
        logger.info("Successfully generated LLM response.")
        return answer
        
    except Exception as e:
        logger.error(f"Hugging Face LLM failed: {e}")
        return f"Mocked Fallback Response: The context shows {context[:100]}..."

def handle_rag_query(query: str) -> Dict[str, Any]:
    """
    Translates natural language query to graph query via LLM orchestration.
    Performs vector search to retrieve specific, context-aware insights.
    """
    _validate_query(query)
    
    try:
        context = _perform_vector_search(query)
        response = _generate_llm_response(context, query)
        return {"status": "success", "data": response}
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        # Return a graceful HTTP 500 equivalent structure instead of crashing
        return {"status": "error", "message": "An internal error occurred while processing your request."}
