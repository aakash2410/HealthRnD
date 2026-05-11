import sys
import logging
from backend.ingestion.layer1_pubmed import fetch_patent_data
from backend.ingestion.layer3_market import fetch_tracxn_data
from backend.ingestion.layer5_regulatory import fetch_ddrs_api
from backend.ingestion.layer6_cofunding import fetch_cofunding_data
from backend.graph.graph_builder import generate_bkg_triplets, push_to_neo4j

logging.basicConfig(level=logging.INFO)

print("Fetching data from layers...")
patents = fetch_patent_data()
tracxn = fetch_tracxn_data()
ddrs = fetch_ddrs_api()
cofunding = fetch_cofunding_data()

all_triplets = []
all_triplets.extend(generate_bkg_triplets(patents, "layer1_patent"))
all_triplets.extend(generate_bkg_triplets(tracxn, "layer3_tracxn"))
all_triplets.extend(generate_bkg_triplets(ddrs, "layer5_ddrs"))
all_triplets.extend(generate_bkg_triplets(cofunding, "layer6_cofunding"))

print(f"Pushing {len(all_triplets)} triplets to Neo4j...")
push_to_neo4j(all_triplets)
print("Done.")
