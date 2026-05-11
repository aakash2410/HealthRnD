import requests
from typing import List, Dict, Any
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

def _execute_nih_reporter_api() -> List[Dict[str, Any]]:
    """Fetches real grant/co-funding data from the NIH RePORTER API."""
    logger.info("Executing NIH RePORTER API request.")
    
    url = "https://api.reporter.nih.gov/v2/projects/search"
    payload = {
        "criteria": {
            "advanced_text_search": {
                "operator": "and",
                "search_text": "global health technology"
            }
        },
        "limit": 10
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        parsed_results = []
        for result in data.get("results", []):
            parsed_results.append({
                "grant_id": result.get("project_num"),
                "funder_name": result.get("agency_ic_admin", {}).get("name", "NIH"),
                "funder_type": "Government",
                "recipient_company": result.get("org_name", "Unknown Org"),
                "recipient_type": "Research Institution / Startup",
                "grant_amount_usd": result.get("award_amount", 0),
                "date_awarded": result.get("award_notice_date", "2024-01-01"),
                "program_title": result.get("project_title", "Unknown Project"),
                "source_url": f"https://reporter.nih.gov/project-details/{result.get('appl_id')}"
            })
            
        return parsed_results
    except Exception as e:
        logger.error(f"HTTP Error querying NIH RePORTER: {e}")
        return []

@retry_with_backoff(retries=2, backoff_in_seconds=3)
def fetch_cofunding_data() -> List[Dict[str, Any]]:
    """
    Replaces BMGF/BIRAC mock data with NIH RePORTER real data API.
    """
    try:
        return _execute_nih_reporter_api()
    except Exception as e:
        logger.error(f"Failed to fetch co-funding data: {e}")
        raise DataIngestionError(f"Co-funding ingestion failed: {e}") from e
