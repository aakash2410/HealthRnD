import os
import re
from typing import List, Dict, Any, Set
from neo4j import GraphDatabase, Driver
from backend.core.logger import get_logger
from backend.core.exceptions import GraphConnectionError

logger = get_logger(__name__)

def _get_neo4j_driver() -> Driver:
    """Initializes and returns the Neo4j Python Driver."""
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        return driver
    except Exception as e:
        logger.error(f"Failed to connect to Neo4j: {e}")
        return None

def normalize_entity_name(name: str) -> str:
    """
    Performs Entity Resolution (ER) by normalizing organization names.
    Removes corporate suffixes and standardizes casing.
    """
    if not name: return ""
    # Standardize casing
    name = name.strip().upper()
    # Remove common corporate suffixes
    suffixes = [r"\bPVT\b", r"\bLTD\b", r"\bLIMITED\b", r"\bINC\b", r"\bCORP\b", r"\bCORPORATION\b", r"\bLLP\b"]
    for suffix in suffixes:
        name = re.sub(suffix, "", name)
    # Remove extra whitespace
    name = " ".join(name.split())
    return name

def translate_to_triplets(all_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Translates raw source data into Subject-Predicate-Object triplets.
    Implements cross-source correlation logic.
    """
    triplets = []
    
    # Store mechanisms and therapeutic areas to create cross-layer links
    mechanisms_map = {} # mechanism_id -> clinical_trial_id
    
    # Layer 1: Patents
    for record in all_data.get("layer1_patent", []):
        subj_id = normalize_entity_name(record.get("title", "Unknown Patent"))
        triplets.append({
            "subject_label": "Patent", "subject_id": subj_id, 
            "subject_props": {"name": record.get("title"), "date": record.get("date"), "url": record.get("source_url")},
            "relation": "FILED_IN",
            "object_label": "Country", "object_id": "India", "object_props": {"name": "India"}
        })

    # Layer 2: NDAP (Infrastructure)
    for record in all_data.get("layer2_ndap", []):
        district = record.get("district")
        state = record.get("state")
        triplets.append({
            "subject_label": "District", "subject_id": district, "subject_props": {"name": district, "state": state, "facilities": record.get("facility_count")},
            "relation": "LOCATED_IN",
            "object_label": "State", "object_id": state, "object_props": {"name": state}
        })

    # Layer 3: Market (OpenAlex Institutions)
    for record in all_data.get("layer3_tracxn", []):
        company = normalize_entity_name(record.get("startup"))
        triplets.append({
            "subject_label": "Company", "subject_id": company, "subject_props": {"name": record.get("startup"), "funding_usd": record.get("total_funding_usd")},
            "relation": "OPERATES_IN",
            "object_label": "Sector", "object_id": "Healthcare", "object_props": {"name": "Healthcare"}
        })

    # Layer 5: Regulatory (CTRI)
    for record in all_data.get("layer5_ddrs", []):
        trial_id = record.get("nct_id")
        sponsor = normalize_entity_name(record.get("sponsor"))
        summary = record.get("summary", "").lower()
        
        trial_props = {
            "name": record.get("title"),
            "phases": record.get("phases"),
            "trial_type": record.get("trial_type", "Interventional"),
            "mechanism": record.get("mechanism", "Standard")
        }
        
        # Link Sponsor to Trial (Deduplicated Sponsor)
        triplets.append({
            "subject_label": "Company", "subject_id": sponsor, "subject_props": {"name": record.get("sponsor")},
            "relation": "SPONSORS",
            "object_label": "ClinicalTrial", "object_id": trial_id, "object_props": trial_props
        })
        
        # Correlation: Link to Mechanism
        mech = record.get("mechanism")
        if mech and mech != "Standard":
            triplets.append({
                "subject_label": "ClinicalTrial", "subject_id": trial_id, "subject_props": trial_props,
                "relation": "UTILIZES",
                "object_label": "Mechanism", "object_id": mech, "object_props": {"name": mech}
            })

    # Layer 6: Co-funding (BIRAC)
    for record in all_data.get("layer6_cofunding", []):
        company = normalize_entity_name(record.get("recipient_company"))
        funder = normalize_entity_name(record.get("funder_name"))
        
        # Cross-Source Link: If this company is also sponsoring a trial, Neo4j will automatically 
        # merge the nodes because the 'subject_id' is normalized.
        triplets.append({
            "subject_label": "Funder", "subject_id": funder, "subject_props": {"name": record.get("funder_name")},
            "relation": "FUNDED",
            "object_label": "Company", "object_id": company, "object_props": {"name": record.get("recipient_company")}
        })

    return triplets

def process_and_push_triplets(all_data: Dict[str, List[Dict[str, Any]]]):
    """
    Main entry point for the graph intelligence engine.
    Performs translation, de-duplication, and Neo4j push.
    """
    triplets = translate_to_triplets(all_data)
    
    driver = _get_neo4j_driver()
    if not driver:
        logger.error("No Neo4j driver available. Aborting push.")
        return
        
    try:
        with driver.session() as session:
            for t in triplets:
                query = (
                    f"MERGE (s:{t['subject_label']} {{id: $subj_id}}) "
                    f"SET s += $subj_props "
                    f"MERGE (o:{t['object_label']} {{id: $obj_id}}) "
                    f"SET o += $obj_props "
                    f"MERGE (s)-[:{t['relation']}]->(o)"
                )
                session.run(query, 
                            subj_id=t["subject_id"], subj_props=t["subject_props"],
                            obj_id=t["object_id"], obj_props=t["object_props"])
        logger.info(f"Successfully pushed {len(triplets)} normalized triplets to Neo4j.")
    except Exception as e:
        logger.error(f"Failed to push triplets: {e}")
    finally:
        driver.close()
