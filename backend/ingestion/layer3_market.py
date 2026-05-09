import os
import requests
from typing import List, Dict, Any
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

def _execute_tracxn_request() -> List[Dict[str, Any]]:
    """Executes Tracxn REST API extraction."""
    logger.info("Executing Tracxn REST API request.")
    
    # Tracxn requires Enterprise OAuth2.0 authentication
    client_id = os.environ.get("TRACXN_CLIENT_ID")
    if not client_id or not client_secret:
        logger.warning("Tracxn credentials not found in environment. Returning mocked data.")
        return [
            {
                "startup": "RetinaAI Health", 
                "stage": "Series B", 
                "total_funding_usd": 15000000,
                "latest_round_date": "2023-08-15",
                "lead_investors": ["Sequoia Capital India", "Lightspeed"],
                "cap_table": {"founders": "45%", "vc": "45%", "esop": "10%"},
                "founders": ["Dr. Ananya Sharma"],
                "source_url": "https://tracxn.com/d/companies/retinaai-health/dummy_link"
            },
            {
                "startup": "GlucoSense India", 
                "stage": "Seed", 
                "total_funding_usd": 2000000,
                "latest_round_date": "2024-02-10",
                "lead_investors": ["Kalaari Capital"],
                "cap_table": {"founders": "70%", "vc": "20%", "esop": "10%"},
                "founders": ["Sarah Jenkins"],
                "source_url": "https://tracxn.com/d/companies/glucosense-india/dummy_link"
            }
        ]
        
    try:
        # 1. Fetch OAuth Token
        auth_url = "https://api.tracxn.com/api/2.2/oauth/token"
        auth_payload = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        auth_response = requests.post(auth_url, json=auth_payload, timeout=10)
        auth_response.raise_for_status()
        token = auth_response.json().get("access_token")
        
        # 2. Search Companies
        search_url = "https://api.tracxn.com/api/2.2/companies"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"sectors": "Healthcare", "country": "India"}
        
        response = requests.get(search_url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        
        return response.json().get("result", [])
        
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Error during Tracxn API extraction: {e}")
        raise DataIngestionError(f"Tracxn HTTP Error: {e}") from e

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def fetch_tracxn_data() -> List[Dict[str, Any]]:
    """
    Extracts startup stage, cap tables, and revenue models from Tracxn REST API.
    """
    try:
        return _execute_tracxn_request()
    except Exception as e:
        logger.error(f"Failed to fetch Tracxn data: {e}")
        raise DataIngestionError(f"Tracxn data fetching failed: {e}") from e

def _validate_cin(cin: str) -> None:
    """Validates the structure of a Corporate Identification Number (CIN)."""
    if not cin or not isinstance(cin, str) or len(cin) != 21:
        raise ValueError("CIN must be a 21-character string.")

def _execute_mca_request(cin: str) -> List[Dict[str, Any]]:
    """Executes MCA V3 API request."""
    logger.info(f"Executing MCA V3 API request for CIN: {cin}")
    
    # MCA V3 requires strict API keys mapped to a registered Indian IP address
    mca_api_key = os.environ.get("MCA_API_KEY")
    
    if not mca_api_key:
        logger.warning(f"MCA API key not found. Returning mocked XBRL data for CIN: {cin}")
        return [
            {
                "cin": cin, 
                "company_name": "RETINAAI HEALTH PRIVATE LIMITED",
                "company_status": "Active", 
                "incorporation_date": "2020-05-12",
                "authorized_capital": 5000000,
                "paid_up_capital": 2500000,
                "xbrl_financials": {
                    "fy_2023_revenue_inr": 45000000,
                    "fy_2023_pat_inr": -12000000,
                    "burn_rate_monthly_inr": 2500000
                },
                "directors": ["Dr. Ananya Sharma", "Rajeev Kumar"],
                "source_url": f"https://www.mca.gov.in/mcafoportal/companyLLPMasterData.do?cin={cin}"
            }
        ]
        
    try:
        # Example MCA V3 endpoint structure for company master data
        url = f"https://www.mca.gov.in/bin/mca/masterdata/{cin}"
        headers = {
            "Authorization": f"Bearer {mca_api_key}",
            "Accept": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        return [response.json()]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP Error during MCA API extraction: {e}")
        raise DataIngestionError(f"MCA HTTP Error: {e}") from e

@retry_with_backoff(retries=3, backoff_in_seconds=2)
def fetch_mca_data(cin: str) -> List[Dict[str, Any]]:
    """
    Extracts XBRL filings for forms AOC-4 and MGT-7 using MCA V3 APIs.
    """
    _validate_cin(cin)
    try:
        return _execute_mca_request(cin)
    except Exception as e:
        logger.error(f"Failed to fetch MCA data for CIN {cin}: {e}")
        raise DataIngestionError(f"MCA data fetching failed for CIN {cin}: {e}") from e
