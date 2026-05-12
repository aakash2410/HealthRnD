import os
from typing import Any, Dict
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from backend.core.logger import get_logger
from backend.core.exceptions import ModelInferenceError
from backend.core.utils import retry_with_backoff

# Import ingestion functions to simulate Graph retrieval locally
from backend.graph.graph_builder import _get_neo4j_driver

load_dotenv()
logger = get_logger(__name__)

HF_API_TOKEN = os.environ.get("HF_API_KEY")

def _validate_query(query: str) -> None:
    """Validates the input natural language query."""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

def _perform_vector_search(query: str) -> tuple[str, dict]:
    """
    Executes a Live Cypher search against the local Neo4j database.
    Returns (context_string, graph_data_dict)
    """
    logger.info(f"Executing LIVE Graph Search for query: {query}")
    
    driver = _get_neo4j_driver()
    if not driver:
        return "Error: Could not connect to Neo4j Database.", {"nodes": [], "links": []}
        
    keywords = [k.lower() for k in query.split() if len(k) > 3]
    if not keywords:
        keywords = [query.lower()]
        
    mapped_keywords = []
    for k in keywords:
        mapped_keywords.append(k)
        if "innovator" in k: mapped_keywords.append("person")
        if "grantee" in k or "startup" in k or "compan" in k: mapped_keywords.append("company")
        if "medtech" in k: mapped_keywords.append("device")
        if "patent" in k: mapped_keywords.append("patent")
        
    relevant_context = []
    graph_data = {"nodes": [], "links": []}
    node_ids = set()
    link_set = set()
    
    try:
        with driver.session() as session:
            for keyword in mapped_keywords:
                cypher_query = (
                    "MATCH (s)-[r]->(o) "
                    "WHERE toLower(s.id) CONTAINS $keyword OR toLower(o.id) CONTAINS $keyword "
                    "OR toLower(labels(s)[0]) CONTAINS $keyword OR toLower(labels(o)[0]) CONTAINS $keyword "
                    "OR toLower(s.abstract) CONTAINS $keyword OR toLower(o.abstract) CONTAINS $keyword "
                    "RETURN labels(s)[0] AS sub_label, s.id AS sub_id, type(r) AS relation, "
                    "labels(o)[0] AS obj_label, o.id AS obj_id, o.source_url AS source_url, o.abstract AS abstract "
                    "LIMIT 20"
                )
                
                result = session.run(cypher_query, keyword=keyword)
                
                for record in result:
                    source_url = record["source_url"] or "No URL"
                    abstract_text = f" Description: {record['abstract']}." if record.get('abstract') else ""
                    sentence = f"{record['sub_id']} ({record['sub_label']}) {record['relation']} {record['obj_id']} ({record['obj_label']}).{abstract_text} [Source: {source_url}]"
                    if sentence not in relevant_context:
                        relevant_context.append(sentence)
                        
                    # Build Graph Payload
                    sub_id = record['sub_id']
                    obj_id = record['obj_id']
                    
                    if sub_id not in node_ids:
                        graph_data["nodes"].append({"id": sub_id, "label": record['sub_label']})
                        node_ids.add(sub_id)
                    if obj_id not in node_ids:
                        graph_data["nodes"].append({"id": obj_id, "label": record['obj_label']})
                        node_ids.add(obj_id)
                        
                    link_key = f"{sub_id}-{record['relation']}-{obj_id}"
                    if link_key not in link_set:
                        graph_data["links"].append({"source": sub_id, "target": obj_id, "label": record['relation']})
                        link_set.add(link_key)
                        
        if not relevant_context:
            return "No relevant context found in the Knowledge Graph.", graph_data
            
        return "\n".join(relevant_context[:30]), graph_data
        
    except Exception as e:
        logger.error(f"Cypher query failed: {e}")
        return f"Error executing Cypher query: {e}", {"nodes": [], "links": []}
    finally:
        driver.close()

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def _generate_llm_response(context: str, query: str, mode: str = "orchestration") -> str:
    """Calls Hugging Face LLM to generate response based on context and mode."""
    logger.info(f"Orchestrating LLM for {mode} response.")
    
    if not HF_API_TOKEN:
        logger.warning("HF_API_KEY not found. Returning mocked RAG.")
        return f"Mocked {mode} response based on context: {context[:50]}..."
        
    try:
        client = InferenceClient(token=HF_API_TOKEN)
        
        if mode == "discovery":
            system_prompt = (
                "You are an elite Data Analyst for a Healthcare Intelligence Platform. "
                "Your job is to provide factual, precise answers based ONLY on the provided Graph Context. "
                "Avoid narrative filler. Focus on listing entities, trial phases, patent IDs, and funding amounts. "
                "Use bullet points for readability. If specific data is missing, say 'Data not found'. "
                "Always include source URLs in brackets next to the data points."
            )
        else:
            system_prompt = (
                "You are an elite Investment Analyst Agent for a Healthcare Intelligence Platform. "
                "Your job is to analyze the raw Graph Context provided and synthesize it into a formal Investment Memo. "
                "Use Markdown to structure the memo EXACTLY with the following sections: "
                "## Executive Summary\n"
                "## The Opportunity (Market & Co-Funding)\n"
                "## The Science (Patents & Trials)\n"
                "## The Therapeutic / Device (Regulatory)\n"
                "## Outstanding Risks\n"
                "## Go/No-Go Recommendation\n\n"
                "Base all your analysis strictly on the provided context. If data is missing for a section, clearly state 'Data not available in current Knowledge Graph'. "
                "Always include source URLs when referencing specific patents, startups, or grants."
            )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
        ]
        
        response = client.chat_completion(
            messages=messages, 
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=1000
        )
        
        answer = response.choices[0].message.content
        logger.info(f"Successfully generated {mode} response.")
        return answer
        
    except Exception as e:
        logger.error(f"Hugging Face LLM failed: {e}")
        return f"Mocked Fallback Response: The context shows {context[:100]}..."

def handle_rag_query(query: str, mode: str = "orchestration") -> Dict[str, Any]:
    """
    Translates natural language query to graph query via LLM orchestration.
    """
    _validate_query(query)
    
    try:
        context, graph_data = _perform_vector_search(query)
        response = _generate_llm_response(context, query, mode)
        return {"status": "success", "data": response, "graph_data": graph_data}
    except Exception as e:
        logger.error(f"RAG query failed: {e}")
        return {"status": "error", "message": f"An internal error occurred while processing your request: {e}"}
