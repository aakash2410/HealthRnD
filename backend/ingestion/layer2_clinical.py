import re
import time
import requests
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

CTG_BASE_URL = "https://clinicaltrials.gov/api/v2/studies"

def _setup_headless_driver() -> webdriver.Chrome:
    """Configures and returns a headless Chrome webdriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Masking as a regular browser to avoid basic blocks
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Use native Selenium Manager instead of external webdriver_manager
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def _execute_selenium_scraper() -> List[Dict[str, Any]]:
    """Runs Selenium to scrape CTRI HTML."""
    logger.info("Executing CTRI Selenium scraper.")
    driver = None
    try:
        driver = _setup_headless_driver()
        
        # CTRI advanced search page (as an example entry point)
        url = "https://ctri.nic.in/Clinicaltrials/advsearch.php"
        driver.get(url)
        
        # Adding a slight delay to allow scripts to load if any
        time.sleep(2)
        
        # Scrape the page source
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # TODO: Implement robust form submission to get actual listings
        # For this skeleton, we are parsing the initial HTML to find standard elements
        # CTRI tables usually contain "Trial Name" and various IDs
        
        # Mocking the parsed text output since CTRI requires active POST requests to view trials
        scraped_text = soup.get_text()
        
        logger.info(f"Successfully scraped CTRI main page. Length: {len(scraped_text)}")
        
        # Since hitting the actual database requires filling search forms,
        # we return a mocked structure containing text that will simulate an NCT cross-reference.
        return [{"trial_id": "CTRI/2023/123", "raw_text": "Secondary IDs include NCT01234567"}]
        
    finally:
        if driver:
            driver.quit()

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
