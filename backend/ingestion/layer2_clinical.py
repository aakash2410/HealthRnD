import re
import time
import requests
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

CTG_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

from selenium.webdriver.chrome.options import Options

def _setup_headless_driver() -> webdriver.Chrome:
    """Configures and returns a headless Chrome webdriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Use native Selenium Manager
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def _execute_selenium_scraper() -> List[Dict[str, Any]]:
    """Mocks the CTRI Selenium scraper for local testing."""
    logger.info("Mocking CTRI Selenium scraper for local testing.")
    
    # Returning a mocked structure simulating a rich CTRI HTML scrape with multiple NCT cross-references.
    return [
        {
            "trial_id": "CTRI/2023/04/052134", 
            "trial_name": "Efficacy of AI-assisted retinopathy screening in rural clinics",
            "phase": "Phase 3",
            "principal_investigator": "Dr. Ananya Sharma",
            "raw_text": "Secondary IDs include NCT04516317 (ClinicalTrials.gov)",
            "source_url": "https://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid=52134"
        },
        {
            "trial_id": "CTRI/2024/01/061988", 
            "trial_name": "Non-invasive CGM vs Fingerprick for Type-2 Diabetes in India",
            "phase": "Phase 2",
            "principal_investigator": "Dr. Rakesh Gupta",
            "raw_text": "Cross-referenced trial: NCT05839201",
            "source_url": "https://ctri.nic.in/Clinicaltrials/pmaindet2.php?trialid=61988"
        }
    ]

@retry_with_backoff(retries=2, backoff_in_seconds=5)
def scrape_ctri() -> List[Dict[str, Any]]:
    """
    Scrapes HTML from CTRI using Selenium since no API exists.
    """
    try:
        return _execute_selenium_scraper()
    except Exception as e:
        logger.error(f"Failed to scrape CTRI: {e}")
        raise DataIngestionError(f"CTRI scraping failed: {e}") from e

def _extract_nct_numbers(clinical_data: List[Dict[str, Any]]) -> List[str]:
    """Uses regex to parse secondary IDs (NCT numbers) from clinical data."""
    nct_numbers = set()
    pattern = re.compile(r"NCT\d{8}")
    
    for record in clinical_data:
        raw_text = record.get("raw_text", "")
        matches = pattern.findall(raw_text)
        nct_numbers.update(matches)
        
    result = list(nct_numbers)
    logger.info(f"Extracted {len(result)} unique NCT numbers.")
    return result

def _execute_ctg_request(nct_numbers: List[str]) -> List[Dict[str, Any]]:
    """Fetches data from ClinicalTrials.gov."""
    if not nct_numbers:
        logger.warning("No NCT numbers provided to fetch from CTG.")
        return []
        
    logger.info(f"Fetching CTG data for {len(nct_numbers)} NCT numbers.")
    results = []
    
    for nct_id in nct_numbers:
        url = f"{CTG_BASE_URL}/{nct_id}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract relevant fields
            protocol = data.get("protocolSection", {})
            status = protocol.get("statusModule", {}).get("overallStatus")
            phase = protocol.get("designModule", {}).get("phases", [])
            conditions = protocol.get("conditionsModule", {}).get("conditions", [])
            
            results.append({
                "nct_id": nct_id,
                "status": status,
                "phase": phase,
                "conditions": conditions
            })
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(f"NCT ID {nct_id} not found on CTG.")
            else:
                logger.error(f"HTTP error fetching {nct_id}: {e}")
                raise
        # Respect CTG API guidelines (gentle throttling)
        time.sleep(0.1)
        
    return results

@retry_with_backoff(retries=3, backoff_in_seconds=1)
def fetch_ctg_data(ctri_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Fetches data from ClinicalTrials.gov and cross-references using NCT numbers.
    """
    try:
        nct_numbers = _extract_nct_numbers(ctri_data)
        return _execute_ctg_request(nct_numbers)
    except Exception as e:
        logger.error(f"Failed to fetch CTG data: {e}")
        raise DataIngestionError(f"CTG data fetching failed: {e}") from e
