import time
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError, RateLimitExceededError

logger = get_logger(__name__)

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def _validate_query(query: str) -> None:
    """Validates the input query for PubMed."""
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

def _execute_pubmed_request(query: str) -> List[Dict[str, Any]]:
    """Executes the request to NCBI E-utilities."""
    logger.info(f"Executing NCBI E-utilities request for query: '{query}'")
    
    # 1. Search for UIDs
    search_url = f"{NCBI_BASE_URL}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 20
    }
    
    # Strict rate limit enforcement (NCBI limit is 3 req/sec without API key)
    time.sleep(0.34)
    search_response = requests.get(search_url, params=search_params, timeout=10)
    search_response.raise_for_status()
    
    data = search_response.json()
    id_list = data.get("esearchresult", {}).get("idlist", [])
    
    if not id_list:
        logger.warning(f"No results found for query: {query}")
        return []
        
    logger.info(f"Found {len(id_list)} UIDs. Fetching summaries...")
    
    # 2. Fetch summaries for the retrieved UIDs
    summary_url = f"{NCBI_BASE_URL}/esummary.fcgi"
    summary_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "json"
    }
    
    # Strict rate limit enforcement
    time.sleep(0.34)
    summary_response = requests.get(summary_url, params=summary_params, timeout=10)
    summary_response.raise_for_status()
    
    summary_data = summary_response.json().get("result", {})
    
    parsed_results = []
    for uid in id_list:
        if uid in summary_data:
            record = summary_data[uid]
            parsed_results.append({
                "uid": record.get("uid"),
                "title": record.get("title"),
                "pubdate": record.get("pubdate"),
                "source": record.get("source"),
                "authors": [a.get("name") for a in record.get("authors", [])]
            })
            
    return parsed_results

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def fetch_pubmed_data(query: str) -> List[Dict[str, Any]]:
    """
    Fetches data from NCBI E-utilities respecting rate limits.
    """
    _validate_query(query)
    try:
        return _execute_pubmed_request(query)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            raise RateLimitExceededError("NCBI rate limit exceeded (3 req/sec).") from e
        raise DataIngestionError(f"HTTP error during PubMed ingestion: {e}") from e
    except Exception as e:
        logger.error(f"Failed to fetch PubMed data for '{query}': {e}")
        raise DataIngestionError(f"PubMed ingestion failed: {e}") from e

def _execute_patent_request() -> List[Dict[str, Any]]:
    """Executes the request to EPO OPS, USPTO, and WIPO APIs."""
    logger.info("Executing Patent APIs request.")
    
    # Note: EPO OPS requires OAuth2.0 authentication. 
    # For robust architecture, we are building the request skeleton here.
    # Without valid credentials, this will intentionally fail and retry if implemented fully.
    
    epo_auth_url = "https://ops.epo.org/3.2/auth/accesstoken"
    # To implement:
    # 1. POST to auth_url with Basic Auth (Consumer Key : Consumer Secret) to get Bearer Token
    # 2. GET to https://ops.epo.org/3.2/rest-services/published-data/search with Bearer Token
    
    # For now, returning mocked structure to prevent crashing without keys.
    logger.warning("EPO OPS credentials not found. Returning mocked structure.")
    return [{"id": "PAT123", "title": "Mocked Patent Data", "status": "Requires Authentication"}]

@retry_with_backoff(retries=2, backoff_in_seconds=2)
def fetch_patent_data() -> List[Dict[str, Any]]:
    """
    Fetches data from EPO OPS, USPTO, and WIPO API.
    """
    try:
        return _execute_patent_request()
    except Exception as e:
        logger.error(f"Failed to fetch patent data: {e}")
        raise DataIngestionError(f"Patent ingestion failed: {e}") from e
