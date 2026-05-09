import sys
from backend.ingestion.layer1_pubmed import fetch_pubmed_data, fetch_patent_data
from backend.ingestion.layer2_clinical import scrape_ctri, fetch_ctg_data

def test_layer1():
    print("=== Testing Layer 1: PubMed ===")
    query = "diabetes AND machine learning"
    try:
        pubmed_results = fetch_pubmed_data(query)
        print(f"Success! Retrieved {len(pubmed_results)} PubMed articles.")
        for res in pubmed_results[:2]:
            print(f"  - {res.get('title')}")
    except Exception as e:
        print(f"Layer 1 PubMed Error: {e}")

    print("\n=== Testing Layer 1: Patents ===")
    try:
        patent_results = fetch_patent_data()
        print(f"Success! Retrieved Patent Mock: {patent_results}")
    except Exception as e:
        print(f"Layer 1 Patent Error: {e}")

def test_layer2():
    print("\n=== Testing Layer 2: CTRI Selenium Scraper ===")
    ctri_data = []
    try:
        ctri_data = scrape_ctri()
        print(f"Success! Scraped CTRI data: {ctri_data}")
    except Exception as e:
        print(f"Layer 2 CTRI Error: {e}")
        
    print("\n=== Testing Layer 2: ClinicalTrials.gov ===")
    try:
        # Mocking CTRI output to contain valid NCT IDs for the API test
        mock_ctri_input = [{"raw_text": "Cross-reference: NCT04516317 and NCT01234567"}]
        ctg_results = fetch_ctg_data(mock_ctri_input)
        print(f"Success! Retrieved {len(ctg_results)} CTG records.")
        for res in ctg_results:
            print(f"  - {res}")
    except Exception as e:
        print(f"Layer 2 CTG Error: {e}")

if __name__ == "__main__":
    print("Starting Integration Tests...")
    test_layer1()
    test_layer2()
    print("\nTests Completed.")
