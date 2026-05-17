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
        return {"publications": 0, "trials": 0, "funding": 0, "companies": 0, "plot_data": []}
    
    try:
        with driver.session() as session:
            # 1. Technical Merit (Patents)
            patent_count = session.run("MATCH (n:Patent) RETURN count(n) as count").single()["count"]
            
            # 2. Clinical Readiness (Trials)
            trial_count = session.run("MATCH (n:ClinicalTrial) RETURN count(n) as count").single()["count"]
            
            # 3. Market Viability (Funding)
            funding_sum = session.run("MATCH ()-[r:FUNDED]->() RETURN sum(r.grant_amount_usd) as total").single()["total"] or 0
            if funding_sum == 0:
                funding_sum = session.run("MATCH (n) WHERE n.funding_usd IS NOT NULL RETURN sum(n.funding_usd) as total").single()["total"] or 0
            
            # 4. Total Entities
            entity_count = session.run("MATCH (n) RETURN count(n) as count").single()["count"]
            
            # 5. Plot Data
            plot_query = """
            MATCH (c)
            WHERE c.funding_usd IS NOT NULL OR labels(c)[0] = 'Company'
            RETURN c.id as name, c.funding_usd as funding, labels(c) as type
            LIMIT 100
            """
            plot_result = session.run(plot_query)
            plot_data = []
            for record in plot_result:
                funding = record["funding"] or 500000
                plot_data.append({
                    "name": record["name"],
                    "x": 20, # Default maturity
                    "y": min(funding / 1000000, 100),
                    "size": 5
                })
            
            return {
                "publications": patent_count,
                "trials": trial_count,
                "funding": funding_sum,
                "companies": entity_count,
                "plot_data": plot_data
            }
    except Exception as e:
        logger.error(f"Dashboard metrics query failed: {e}")
        return {"publications": 0, "trials": 0, "funding": 0, "companies": 0, "plot_data": []}
    finally:
        driver.close()

def get_scouting_signals():
    driver = _get_neo4j_driver()
    if not driver: return []
    try:
        with driver.session() as session:
            query = "MATCH (c:Entity) OPTIONAL MATCH (c)-[r]-() RETURN c.id as name, count(r) as signal_score ORDER BY signal_score DESC LIMIT 5"
            result = session.run(query)
            return [{"name": r["name"], "score": r["signal_score"], "type": "Entity"} for r in result]
    finally:
        driver.close()

def get_all_entities():
    driver = _get_neo4j_driver()
    if not driver: return []
    try:
        with driver.session() as session:
            query = "MATCH (c) RETURN COALESCE(c.name, c.id) as name, labels(c)[0] as type LIMIT 50"
            result = session.run(query)
            return [{"name": r["name"], "type": r["type"]} for r in result]
    finally:
        driver.close()
