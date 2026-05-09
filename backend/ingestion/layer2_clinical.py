def scrape_ctri():
    """
    Scrapes HTML from CTRI using Selenium since no API exists.
    Must be scheduled to run every 4 weeks.
    """
    print("Scraping CTRI data...")
    # TODO: Implement Selenium scraper
    # TODO: Dump to local SQLite/PostgreSQL
    return []

def fetch_ctg_data():
    """
    Fetches data from ClinicalTrials.gov and cross-references using NCT numbers.
    """
    print("Fetching ClinicalTrials.gov data...")
    # TODO: Implement Regex parsing for NCT numbers
    # TODO: Map CTRI fields to CTG protocol definitions
    return []
