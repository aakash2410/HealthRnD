import os
from neo4j import GraphDatabase, Driver
from backend.core.logger import get_logger

logger = get_logger(__name__)

def _get_neo4j_driver():
    uri = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
    user = os.environ.get("NEO4J_USER", "neo4j")
    password = os.environ.get("NEO4J_PASSWORD", "password")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        return driver
    except Exception as e:
        logger.warning(f"Neo4j query driver connection failed: {e}")
        return None

def get_dashboard_metrics():
    driver = _get_neo4j_driver()
    if not driver:
        return {"publications": 0, "trials": 0, "funding": 0, "companies": 0}
    
    with driver.session() as session:
        # Technical Merit (Publications/Patents)
        pub_count = session.run("MATCH (n:Publication) RETURN count(n) as count").single()["count"]
        patent_count = session.run("MATCH (n:Patent) RETURN count(n) as count").single()["count"]
        
        # Clinical Readiness (Trials)
        trial_count = session.run("MATCH (n:ClinicalTrial) RETURN count(n) as count").single()["count"]
        
        # Market Viability (Funding)
        funding_sum = session.run("MATCH ()-[r:FUNDED]->() RETURN sum(r.grant_amount_usd) as total").single()["total"] or 0
        
        # Total Entities
        company_count = session.run("MATCH (n:Company) RETURN count(n) as count").single()["count"]
        
        # Plot Data (Funding vs Clinical Phase)
        plot_query = """
        MATCH (c:Company)-[:SPONSORS]->(t:ClinicalTrial)
        RETURN c.id as name, c.funding_usd as funding, t.phases as phases
        LIMIT 20
        """
        plot_result = session.run(plot_query)
        plot_data = []
        phase_map = {"Phase I": 1, "Phase II": 2, "Phase III": 3, "Phase IV": 4, "AYUSH": 1.5}
        
        for record in plot_result:
            # Map phases list to a maturity score
            phases = record["phases"] or []
            max_phase = 0
            for p in phases:
                max_phase = max(max_phase, phase_map.get(p, 0))
            
            if record["funding"] and max_phase > 0:
                plot_data.append({
                    "name": record["name"],
                    "x": max_phase * 25, # Normalized for 100% scale
                    "y": min(record["funding"] / 1000000, 100), # Normalized in $M, capped for plot
                    "size": 3 + (max_phase * 2)
                })

        driver.close()
        return {
            "publications": pub_count + patent_count,
            "trials": trial_count,
            "funding": funding_sum,
            "companies": company_count,
            "plot_data": plot_data
        }

def get_scouting_signals():
    driver = _get_neo4j_driver()
    if not driver:
        return []
    
    with driver.session() as session:
        # Fetch companies with most connections as "signals"
        query = """
        MATCH (c:Company)
        OPTIONAL MATCH (c)-[r]-()
        RETURN c.id as name, count(r) as signal_score, labels(c) as type
        ORDER BY signal_score DESC
        LIMIT 5
        """
        result = session.run(query)
        signals = []
        for record in result:
            signals.append({
                "name": record["name"],
                "score": record["signal_score"],
                "type": record["type"][0] if record["type"] else "Entity"
            })
        driver.close()
        return signals

def get_all_entities():
    driver = _get_neo4j_driver()
    if not driver:
        return []
    
    with driver.session() as session:
        query = """
        MATCH (c)-[r]->()
        RETURN c.id as name, labels(c) as type, r.verified as verified, r.confidence as confidence
        LIMIT 50
        """
        result = session.run(query)
        entities = []
        for record in result:
            entities.append({
                "name": record["name"],
                "type": record["type"][0] if record["type"] else "Entity",
                "verified": record["verified"] or False,
                "confidence": record["confidence"] or 0.0
            })
        driver.close()
        return entities
