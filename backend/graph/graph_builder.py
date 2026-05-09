import os
from typing import List, Dict, Any
from neo4j import GraphDatabase, Driver
from backend.core.logger import get_logger
from backend.core.exceptions import GraphConnectionError

logger = get_logger(__name__)

def _get_neo4j_driver() -> Driver:
    """Initializes and returns the Neo4j Python Driver."""
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    
    logger.info(f"Initializing Neo4j connection to {uri}")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        # Verify connectivity
        driver.verify_connectivity()
        return driver
    except Exception as e:
        logger.warning(f"Neo4j connection failed: {e}. Running in Cypher simulation mode.")
        return None

def generate_bkg_triplets(data: List[Dict[str, Any]], source_type: str) -> List[Dict[str, Any]]:
    """
    Translates raw JSON from ingestion layers into standardized Triplets.
    Outputs: [{"subject_label", "subject_id", "subject_props", 
               "relation", 
               "object_label", "object_id", "object_props"}]
    """
    triplets = []
    logger.info(f"Translating {len(data)} records from {source_type} into Graph Triplets.")
    
    if source_type == "layer1_patent":
        for record in data:
            patent_id = record.get("id")
            if not patent_id: continue
            
            patent_props = {
                "title": record.get("title"), 
                "status": record.get("status"),
                "source_url": record.get("source_url", "")
            }
            
            for inventor in record.get("inventors", []):
                triplets.append({
                    "subject_label": "Person", "subject_id": inventor, "subject_props": {"name": inventor},
                    "relation": "INVENTED",
                    "object_label": "Patent", "object_id": patent_id, "object_props": patent_props
                })
                
    elif source_type == "layer3_tracxn":
        for record in data:
            startup_name = record.get("startup")
            if not startup_name: continue
            
            startup_props = {
                "stage": record.get("stage"), 
                "funding_usd": record.get("total_funding_usd"),
                "source_url": record.get("source_url", "")
            }
            
            for founder in record.get("founders", []):
                triplets.append({
                    "subject_label": "Person", "subject_id": founder, "subject_props": {"name": founder},
                    "relation": "FOUNDED",
                    "object_label": "Company", "object_id": startup_name, "object_props": startup_props
                })
                
            for investor in record.get("lead_investors", []):
                triplets.append({
                    "subject_label": "Investor", "subject_id": investor, "subject_props": {"name": investor},
                    "relation": "INVESTED_IN",
                    "object_label": "Company", "object_id": startup_name, "object_props": {}
                })
                
    elif source_type == "layer5_ddrs":
        for record in data:
            device_id = record.get("entity_id")
            manufacturer = record.get("manufacturer")
            if not device_id or not manufacturer: continue
            
            device_props = {
                "status": record.get("status"), 
                "class": record.get("device_class"),
                "source_url": record.get("source_url", "")
            }
            
            triplets.append({
                "subject_label": "Company", "subject_id": manufacturer, "subject_props": {"name": manufacturer},
                "relation": "HOLDS_LICENSE",
                "object_label": "RegulatoryLicense", "object_id": device_id, "object_props": device_props
            })

    return triplets

def _format_triplets_for_cypher(triplets: List[Dict[str, Any]]) -> str:
    """Transforms raw triplets into Neo4j Cypher query parameters."""
    # This query uses APOC or dynamic labels if supported, but for strict 
    # safe parameterized queries without APOC, we execute them individually in the push_to_neo4j function
    # to handle dynamic node labels properly.
    pass

def push_to_neo4j(triplets: List[Dict[str, Any]]) -> bool:
    """
    Normalizes data into the BKG schema mapping Subject-Predicate-Object triplets
    and pushes to Neo4j.
    """
    if not triplets:
        logger.warning("No triplets provided to push_to_neo4j.")
        return False
        
    driver = _get_neo4j_driver()
    logger.info(f"Pushing {len(triplets)} triplets to Neo4j Graph DB...")
    
    if driver is None:
        logger.info("Simulation Mode: Printing first 2 Cypher queries instead of executing.")
        for i, t in enumerate(triplets[:2]):
            query = f"MERGE (s:{t['subject_label']} {{id: '{t['subject_id']}'}}) " \
                    f"MERGE (o:{t['object_label']} {{id: '{t['object_id']}'}}) " \
                    f"MERGE (s)-[:{t['relation']}]->(o)"
            logger.info(f"CYPHER: {query}")
        return True

    try:
        with driver.session() as session:
            for t in triplets:
                # To prevent Cypher injection and handle dynamic labels safely
                # MERGE constraints are based on the unique 'id' field
                query = (
                    f"MERGE (s:{t['subject_label']} {{id: $subj_id}}) "
                    f"SET s += $subj_props "
                    f"MERGE (o:{t['object_label']} {{id: $obj_id}}) "
                    f"SET o += $obj_props "
                    f"MERGE (s)-[:{t['relation']}]->(o)"
                )
                
                session.run(query, 
                            subj_id=t["subject_id"], 
                            subj_props=t["subject_props"],
                            obj_id=t["object_id"], 
                            obj_props=t["object_props"])
                
        return True
    except Exception as e:
        logger.error(f"Failed to push to Neo4j: {e}")
        raise GraphConnectionError(f"Neo4j transaction failed: {e}") from e
    finally:
        driver.close()
