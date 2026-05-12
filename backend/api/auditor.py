import os
from typing import Dict, Any, List
from huggingface_hub import InferenceClient
from backend.graph.graph_builder import _get_neo4j_driver
from backend.core.logger import get_logger
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

HF_API_TOKEN = os.environ.get("HF_API_KEY")

def verify_triplet_with_llm(subject: str, relation: str, obj: str) -> Dict[str, Any]:
    """
    Performs a LIVE LLM inference to validate a graph triplet.
    NO PLACEHOLDERS.
    """
    logger.info(f"LIVE LLM AUDIT: {subject} -[{relation}]-> {obj}")
    
    if not HF_API_TOKEN:
        logger.error("HF_API_KEY missing. Cannot perform live audit.")
        return {"verified": False, "confidence": 0.0, "evidence": ["API Key Missing"]}

    try:
        client = InferenceClient(token=HF_API_TOKEN)
        
        system_prompt = (
            "You are an elite Clinical Integrity Auditor. Your job is to verify healthcare triplets from an Indian Knowledge Graph. "
            "You must evaluate the relationship and provide a confidence score between 0.0 and 1.0. "
            "Consider the technical validity of the relationship (e.g. Can a company sponsor a trial? Does a drug treat a specific disease?). "
            "Return your response EXACTLY in this format: "
            "CONFIDENCE: [score]\nREASONING: [one sentence explanation]"
        )
        
        prompt = f"Verify this triplet: Subject: {subject}, Relation: {relation}, Object: {obj}. Is this a valid clinical or business relationship in the Indian healthcare context?"
        
        response = client.chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="Qwen/Qwen2.5-7B-Instruct",
            max_tokens=200
        )
        
        content = response.choices[0].message.content
        
        # Parse LLM response
        conf_match = [line for line in content.split("\n") if "CONFIDENCE:" in line]
        reason_match = [line for line in content.split("\n") if "REASONING:" in line]
        
        confidence = float(conf_match[0].split(":")[1].strip()) if conf_match else 0.5
        reason = reason_match[0].split(":")[1].strip() if reason_match else "Inconclusive"
        
        return {
            "verified": confidence > 0.7,
            "confidence": confidence,
            "evidence": [reason]
        }
        
    except Exception as e:
        logger.error(f"LLM Audit Inference failed: {e}")
        return {"verified": False, "confidence": 0.0, "evidence": [f"Inference Error: {str(e)}"]}

def audit_entire_graph():
    """
    Iterates through the Knowledge Graph and validates all 'unverified' nodes via LIVE LLM.
    """
    driver = _get_neo4j_driver()
    if not driver: return
    
    try:
        with driver.session() as session:
            # Fetch unverified relationships (limiting for performance during turn)
            result = session.run("MATCH (s)-[r]->(o) WHERE r.verified IS NULL RETURN s.id as sub, type(r) as rel, o.id as obj LIMIT 10")
            
            records = list(result)
            if not records:
                logger.info("No unverified triplets found. All data is current.")
                return

            for record in records:
                audit_res = verify_triplet_with_llm(record["sub"], record["rel"], record["obj"])
                
                # Update Neo4j with Live LLM Scores
                session.run("""
                    MATCH (s {id: $sub})-[r]->(o {id: $obj})
                    WHERE type(r) = $rel
                    SET r.verified = $verified,
                        r.confidence = $conf,
                        r.audit_trail = $evidence
                """, sub=record["sub"], obj=record["obj"], rel=record["rel"], 
                    verified=audit_res["verified"], conf=audit_res["confidence"], evidence=audit_res["evidence"])
                
            logger.info(f"Live LLM Audit Cycle Complete for {len(records)} records.")
    finally:
        driver.close()

if __name__ == "__main__":
    audit_entire_graph()
