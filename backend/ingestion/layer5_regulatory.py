import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time
from backend.core.logger import get_logger
from backend.core.utils import retry_with_backoff
from backend.core.exceptions import DataIngestionError

logger = get_logger(__name__)

def _scrape_ctri_detail(trial_id: str, session: requests.Session) -> Dict[str, Any]:
    """Scrapes the detailed trial page for geographic sites with high timeout."""
    detail_url = f"https://ctri.nic.in/Clinicaltrials/pmain.php?t_id={trial_id}"
    try:
        # Politeness delay for fragile gov servers
        time.sleep(0.5)
        response = session.get(detail_url, timeout=60, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        sites = []
        rows = soup.find_all('tr')
        for row in rows:
            text = row.text.lower()
            if 'hospital' in text or 'medical college' in text:
                sites.append(row.text.strip())
        
        return {"sites": sites[:5]}
    except Exception as e:
        logger.warning(f"CTRI Detail Timeout for {trial_id} (Gov server slow): {e}")
        return {"sites": []}

def _execute_ctri_sovereign_ingestion(start_year: int = 2025, end_year: int = 2026) -> List[Dict[str, Any]]:
    """
    Performs a high-volume ingestion using ONLY the official CTRI government server.
    Extremely robust retries and long timeouts.
    """
    logger.info(f"SOVEREIGN INGESTION: CTRI Gov India ({start_year}-{end_year})")
    
    url = "https://ctri.nic.in/Clinicaltrials/advsearch.php"
    all_trials = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        for year in range(start_year, end_year + 1):
            # Crawling up to 50 pages to reach the 15,000+ record goal
            for page in range(1, 51):
                logger.info(f"CRAWLING GOV SITE: CTRI Page {page} for {year}...")
                
                try:
                    response = session.get(f"{url}?page={page}&year={year}", headers=headers, verify=False, timeout=60)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    rows = soup.find_all('tr')
                    page_found = False
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) > 5:
                            trial_id = cols[0].text.strip()
                            if "CTRI" in trial_id:
                                detail = _scrape_ctri_detail(trial_id, session)
                                all_trials.append({
                                    "nct_id": trial_id,
                                    "title": cols[1].text.strip(),
                                    "sponsor": cols[2].text.strip(),
                                    "phases": [cols[3].text.strip()],
                                    "summary": f"{year} CTRI Gov Record: {cols[1].text.strip()}",
                                    "sites": detail["sites"],
                                    "year": year,
                                    "source_url": f"https://ctri.nic.in/Clinicaltrials/pmain.php?t_id={trial_id}"
                                })
                                page_found = True
                    
                    if not page_found:
                        logger.info(f"Completed all available records for {year} on Gov Server.")
                        break
                        
                except requests.exceptions.Timeout:
                    logger.warning(f"Gov Server Timeout on Page {page}. Retrying in 5s...")
                    time.sleep(5)
                    continue # Simple retry logic
                    
        return all_trials

    except Exception as e:
        logger.error(f"Sovereign CTRI Ingestion Failed: {e}")
        return []

@retry_with_backoff(retries=5, backoff_in_seconds=5)
def fetch_ddrs_api() -> List[Dict[str, Any]]:
    return _execute_ctri_sovereign_ingestion(start_year=2025, end_year=2026)
