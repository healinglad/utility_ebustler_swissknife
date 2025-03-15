"""
Scraper module for fetching data from screener.in
"""

import requests
from bs4 import BeautifulSoup
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScreenerScraper:
    """
    A class to handle scraping operations from screener.in
    """
    
    BASE_URL = "https://www.screener.in"
    SEARCH_URL = f"{BASE_URL}/search/"
    COMPANY_URL = f"{BASE_URL}/company/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    def __init__(self, delay=1):
        """
        Initialize the scraper with optional delay between requests
        
        Args:
            delay (int): Delay in seconds between requests to avoid rate limiting
        """
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)
        self.delay = delay
    
    def _make_request(self, url, params=None):
        """
        Make an HTTP request with error handling and rate limiting
        
        Args:
            url (str): URL to request
            params (dict, optional): Query parameters
            
        Returns:
            requests.Response: Response object
        """
        try:
            time.sleep(self.delay)  # Add delay to avoid rate limiting
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            if response.status_code == 404:
                logger.error("Symbol not found or page doesn't exist")
            elif response.status_code == 429:
                logger.error("Rate limited. Try increasing the delay between requests")
            raise
        except requests.exceptions.ConnectionError:
            logger.error("Connection Error. Check your internet connection")
            raise
        except requests.exceptions.Timeout:
            logger.error("Timeout Error")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {e}")
            raise
    
    def search_symbol(self, symbol):
        """
        Search for a company by its trading symbol
        
        Args:
            symbol (str): Trading symbol to search for
            
        Returns:
            str: URL of the company page if found, None otherwise
        """
        logger.info(f"Searching for symbol: {symbol}")
        
        # Try direct company URL with consolidated view first
        try:
            direct_url = f"{self.COMPANY_URL}{symbol}/consolidated/"
            logger.info(f"Trying direct consolidated URL: {direct_url}")
            response = self._make_request(direct_url)
            
            # If we get here, the direct URL worked
            logger.info(f"Found company page via direct consolidated URL: {direct_url}")
            return direct_url
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.info(f"Direct consolidated URL not found, trying standalone: {symbol}")
            else:
                # For other HTTP errors, re-raise
                raise
        
        # Try direct company URL without consolidated view
        try:
            direct_url = f"{self.COMPANY_URL}{symbol}/"
            logger.info(f"Trying direct standalone URL: {direct_url}")
            response = self._make_request(direct_url)
            
            # If we get here, the direct URL worked
            logger.info(f"Found company page via direct standalone URL: {direct_url}")
            return direct_url
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.info(f"Direct standalone URL not found, trying search: {symbol}")
            else:
                # For other HTTP errors, re-raise
                raise
        
        # If direct URLs fail, try search
        try:
            params = {"q": symbol}
            response = self._make_request(self.SEARCH_URL, params)
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find the first search result
            search_results = soup.select(".results-list a")
            
            if not search_results:
                logger.warning(f"No results found for symbol: {symbol}")
                return None
            
            # Get the URL of the first result
            company_url = search_results[0]['href']
            logger.info(f"Found company page via search: {company_url}")
            
            return f"{self.BASE_URL}{company_url}"
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error during search: {e}")
            return None
    
    def get_company_page(self, symbol, consolidated=True):
        """
        Get the company page HTML for a given symbol
        
        Args:
            symbol (str): Trading symbol
            consolidated (bool): Whether to use consolidated financial data (default: True)
            
        Returns:
            BeautifulSoup: Parsed HTML of the company page
        """
        logger.info(f"Getting company page for {symbol} (consolidated: {consolidated})")
        
        # Try direct company URL with the appropriate view first
        try:
            if consolidated:
                direct_url = f"{self.COMPANY_URL}{symbol}/consolidated/"
                logger.info(f"Trying direct consolidated URL: {direct_url}")
            else:
                direct_url = f"{self.COMPANY_URL}{symbol}/"
                logger.info(f"Trying direct standalone URL: {direct_url}")
                
            response = self._make_request(direct_url)
            
            # If we get here, the direct URL worked
            logger.info(f"Found company page via direct URL: {direct_url}")
            return BeautifulSoup(response.text, 'lxml')
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.info(f"Direct URL not found, trying search: {symbol}")
            else:
                # For other HTTP errors, re-raise
                raise
        
        # If direct URL fails, fall back to search
        company_url = self.search_symbol(symbol)
        
        if not company_url:
            return None
        
        logger.info(f"Fetching company page: {company_url}")
        response = self._make_request(company_url)
        
        return BeautifulSoup(response.text, 'lxml')
