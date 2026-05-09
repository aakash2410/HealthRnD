import requests
from typing import List, Dict, Any
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

def _execute_ndap_request() -> List[Dict[str, Any]]:
    """Executes the request to NDAP/data.gov.in open APIs."""
    logger.info("Executing NDAP API request.")
    
    # We will simulate calling the data.gov.in API for NFHS-5 data
    # (Since actual NDAP requires specific dataset IDs that change, we use a public proxy approach)
    # Using a placeholder open API URL structure that data.gov.in uses
    
    api_key = "public_mock_key" # Normally loaded from env if required by data.gov.in
    url = "https://api.data.gov.in/resource/dummy_nfhs5_dataset"
    params = {
        "api-key": api_key,
        "format": "json",
        "limit": 100
    }
    
    try:
        # In a real environment, this hits the live URL. 
        # For our architecture demo without a valid data.gov.in key, we will simulate the JSON response
        # to guarantee the spatial aggregator receives valid data to process.
        
        # response = requests.get(url, params=params, timeout=10)
        # response.raise_for_status()
        # return response.json().get("records", [])
        
        logger.warning("Using mocked NDAP JSON response for local testing.")
        return [
            {
                "state": "Maharashtra", "district": "Mumbai", 
                "nfhs5_score": 0.82, "population": 12000000,
                "rural_healthcare_centers": 45, "infant_mortality_rate": 18.2,
                "diabetic_prevalence_percent": 11.4
            },
            {
                "state": "Maharashtra", "district": "Pune", 
                "nfhs5_score": 0.76, "population": 3100000,
                "rural_healthcare_centers": 112, "infant_mortality_rate": 22.4,
                "diabetic_prevalence_percent": 9.8
            },
            {
                "state": "Maharashtra", "district": "Mumbai", 
                "nfhs5_score": 0.85, "population": 12000000, 
                "rural_healthcare_centers": 45, "infant_mortality_rate": 17.9,
                "diabetic_prevalence_percent": 11.6
            },
            {
                "state": "Karnataka", "district": "Bangalore", 
                "nfhs5_score": 0.88, "population": 8400000,
                "rural_healthcare_centers": 34, "infant_mortality_rate": 15.3,
                "diabetic_prevalence_percent": 12.1
            }
        ]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Error during NDAP API extraction: {e}")
        raise DataIngestionError(f"NDAP HTTP Error: {e}") from e

def _aggregate_spatially(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregates data spatially down to the district level."""
    logger.info("Aggregating NDAP data spatially by district.")
    
    # Simulating PostGIS spatial grouping locally using basic Python dictionaries
    aggregated_data = {}
    
    for record in data:
        district = record.get("district")
        if not district:
            continue
            
        if district not in aggregated_data:
            aggregated_data[district] = {
                "state": record.get("state"),
                "district": district,
                "total_records": 0,
                "cumulative_nfhs5_score": 0.0,
                "population": record.get("population", 0)
            }
            
        # Accumulate scores for averaging
        aggregated_data[district]["total_records"] += 1
        aggregated_data[district]["cumulative_nfhs5_score"] += record.get("nfhs5_score", 0.0)
        
    # Calculate final averages
    final_results = []
    for district, metrics in aggregated_data.items():
        avg_score = metrics["cumulative_nfhs5_score"] / metrics["total_records"] if metrics["total_records"] > 0 else 0
        final_results.append({
            "state": metrics["state"],
            "district": district,
            "avg_nfhs5_score": round(avg_score, 3),
            "population": metrics["population"],
            "source_url": f"https://data.gov.in/search?title={district}+health"
        })
        
    logger.info(f"Aggregated {len(data)} raw records into {len(final_results)} districts.")
    return final_results

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def fetch_ndap_data() -> List[Dict[str, Any]]:
    """
    Fetches Primary Population Census and NFHS-5 CAB indicators via NDAP APIs.
    """
    try:
        raw_data = _execute_ndap_request()
        return _aggregate_spatially(raw_data)
    except Exception as e:
        logger.error(f"Failed to fetch NDAP data: {e}")
        raise DataIngestionError(f"NDAP data fetching failed: {e}") from e
