import requests
from typing import List, Dict, Any
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

def _execute_clinical_trials_api() -> List[Dict[str, Any]]:
    """Fetches real clinical trial data from ClinicalTrials.gov v2 REST API."""
    logger.info("Executing ClinicalTrials.gov v2 API request.")
    
    url = "https://clinicaltrials.gov/api/v2/studies"
    params = {
        "query.term": "health AND India",
        "pageSize": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        parsed_results = []
        studies = data.get("studies", [])
        for study in studies:
            protocol = study.get("protocolSection", {})
            ident = protocol.get("identificationModule", {})
            sponsors = protocol.get("sponsorCollaboratorsModule", {})
            design = protocol.get("designModule", {})
            
            nct_id = ident.get("nctId", "Unknown")
            title = ident.get("briefTitle", "Unknown Title")
            lead_sponsor = sponsors.get("leadSponsor", {}).get("name", "Unknown Sponsor")
            phases = design.get("phases", ["Unknown Phase"])
            
            parsed_results.append({
                "nct_id": nct_id,
                "title": title,
                "sponsor": lead_sponsor,
                "phases": phases,
                "source_url": f"https://clinicaltrials.gov/study/{nct_id}"
            })
            
        return parsed_results
    except Exception as e:
        logger.error(f"HTTP Error querying ClinicalTrials.gov: {e}")
        return []

@retry_with_backoff(retries=2, backoff_in_seconds=5)
def scrape_sugam_pdfs() -> List[Dict[str, Any]]:
    return []

@retry_with_backoff(retries=2, backoff_in_seconds=2)
def fetch_ddrs_api() -> List[Dict[str, Any]]:
    """
    Replaces DDRS mock API with ClinicalTrials.gov real data API.
    """
    try:
        return _execute_clinical_trials_api()
    except Exception as e:
        logger.error(f"Failed to fetch clinical trial data: {e}")
        raise DataIngestionError(f"Clinical trial ingestion failed: {e}") from e
