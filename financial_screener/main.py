#!/usr/bin/env python3
"""
Financial Screener - A utility to fetch financial data from screener.in

Usage:
    python main.py SYMBOL
    
Example:
    python main.py TATAMOTORS
"""

import sys
import logging
import click
import requests
from scraper import ScreenerScraper
from extractor import FinancialDataExtractor
from formatter import FinancialDataFormatter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@click.command()
@click.argument('symbol', required=True)
@click.option('--delay', default=1, help='Delay between requests in seconds (default: 1)')
@click.option('--consolidated/--standalone', default=True, help='Use consolidated or standalone financial data (default: consolidated)')
def main(symbol, delay, consolidated):
    """
    Fetch financial data for a given trading symbol from screener.in
    
    SYMBOL is the trading symbol of the company (e.g., TATAMOTORS, VBL, RELIANCE)
    """
    logger.info(f"Fetching financial data for symbol: {symbol}")
    
    try:
        # Initialize the scraper
        scraper = ScreenerScraper(delay=delay)
        
        # Get the company page
        company_page = scraper.get_company_page(symbol, consolidated)
        
        if not company_page:
            print(f"\n{'=' * 50}")
            print(f"ERROR: Could not find company page for symbol: {symbol}")
            print(f"{'=' * 50}")
            print("\nPossible reasons:")
            print("1. The symbol may be incorrect")
            print("2. The company may not be listed on screener.in")
            print("3. The website structure may have changed")
            print("\nSuggestions:")
            print("- Check if the symbol is correct")
            print("- Try using the full company name")
            print("- Try increasing the delay between requests (--delay option)")
            print(f"{'=' * 50}\n")
            sys.exit(1)
        
        # Extract financial data
        extractor = FinancialDataExtractor(company_page)
        
        # Get company name
        company_name = extractor.company_name
        logger.info(f"Found company: {company_name}")
        
        # Extract required metrics
        roe_data = extractor.extract_roe()
        growth_data = extractor.extract_growth("Sales Growth")
        quarterly_data = extractor.extract_quarterly_revenue_profit()
        peg_ratio = extractor.extract_peg()
        
        # Get all ratios for additional metrics
        all_ratios = extractor.extract_ratios(peg_ratio)
        
        # Format and display the results
        formatter = FinancialDataFormatter(company_name)
        # Pass the extractor instance to the formatter's namespace
        formatter.extractor = extractor
        summary = formatter.format_summary(roe_data, growth_data, quarterly_data, peg_ratio)
        
        print(summary)
        
    except requests.exceptions.ConnectionError:
        print(f"\n{'=' * 50}")
        print(f"ERROR: Connection Error")
        print(f"{'=' * 50}")
        print("\nFailed to connect to screener.in. Please check your internet connection.")
        print(f"{'=' * 50}\n")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"\n{'=' * 50}")
        print(f"ERROR: Timeout Error")
        print(f"{'=' * 50}")
        print("\nThe request to screener.in timed out. Please try again later or increase the delay.")
        print(f"{'=' * 50}\n")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"\n{'=' * 50}")
        print(f"ERROR: HTTP Error: {e}")
        print(f"{'=' * 50}")
        print("\nAn HTTP error occurred while accessing screener.in.")
        print("This could be due to rate limiting or changes in the website structure.")
        print("\nSuggestions:")
        print("- Try increasing the delay between requests (--delay option)")
        print("- Try again later")
        print(f"{'=' * 50}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n{'=' * 50}")
        print(f"ERROR: An unexpected error occurred: {e}")
        print(f"{'=' * 50}")
        print("\nPlease report this issue with the following details:")
        print(f"Symbol: {symbol}")
        print(f"Error: {str(e)}")
        print(f"{'=' * 50}\n")
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
