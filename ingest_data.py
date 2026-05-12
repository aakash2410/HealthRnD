import os
import concurrent.futures
from backend.graph.graph_builder import process_and_push_triplets
from backend.ingestion.layer1_patents import fetch_indian_patents_2026
from backend.ingestion.layer2_ndap import fetch_ndap_health_infrastructure
from backend.ingestion.layer3_market import fetch_tracxn_data
from backend.ingestion.layer5_regulatory import fetch_ddrs_api
from backend.ingestion.layer6_cofunding import fetch_cofunding_data
from backend.core.logger import get_logger

logger = get_logger(__name__)

def run_huge_ingestion_2026():
    """
    Executes a parallelized, high-volume ingestion of 2026 Indian Healthcare data.
    STRICTLY LIVE. ZERO DUMMY FALLBACKS.
    """
    logger.info("Starting HUGE PARALLEL INGESTION for India 2026...")
    
    # Task mapping for parallel execution
    tasks = {
        "layer1_patent": fetch_indian_patents_2026,
        "layer2_ndap": fetch_ndap_health_infrastructure,
        "layer3_tracxn": fetch_tracxn_data,
        "layer5_ddrs": fetch_ddrs_api,
        "layer6_cofunding": fetch_cofunding_data
    }
    
    all_data = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_layer = {executor.submit(func): layer for layer, func in tasks.items()}
        for future in concurrent.futures.as_completed(future_to_layer):
            layer = future_to_layer[future]
            try:
                data = future.result()
                all_data[layer] = data
                logger.info(f"Successfully fetched {len(data)} LIVE records from {layer}")
            except Exception as e:
                logger.error(f"Layer {layer} failed live ingestion: {e}")
                all_data[layer] = []

    # Push to Neo4j
    total_records = sum(len(v) for v in all_data.values())
    if total_records > 0:
        logger.info(f"Processing {total_records} LIVE records into Knowledge Graph...")
        process_and_push_triplets(all_data)
        logger.info("HUGE 2026 INGESTION COMPLETE.")
    else:
        logger.warning("No live data was found during this run. Zero records pushed to graph.")

if __name__ == "__main__":
    run_huge_ingestion_2026()
