"""
Formatter module for presenting financial data in a readable format
"""

import logging
from tabulate import tabulate

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialDataFormatter:
    """
    A class to format financial data for display
    """
    
    def __init__(self, company_name):
        """
        Initialize with company name
        
        Args:
            company_name (str): Name of the company
        """
        self.company_name = company_name
    
    def format_roe(self, roe_data):
        """
        Format ROE data
        
        Args:
            roe_data (dict): ROE values by year
            
        Returns:
            str: Formatted ROE information
        """
        if not roe_data:
            return "ROE: Data not available"
        
        headers = ["Metric"] + list(roe_data.keys())
        rows = [["ROE"] + [roe_data[year] for year in roe_data.keys()]]
        
        return "\n" + tabulate(rows, headers=headers, tablefmt="grid")
    
    def format_growth(self, growth_data):
        """
        Format growth data
        
        Args:
            growth_data (dict): Growth values by year
            
        Returns:
            str: Formatted growth information
        """
        if not growth_data:
            return "3-Year Growth: Data not available"
        
        headers = ["Metric"] + list(growth_data.keys())
        rows = [["Growth"] + [growth_data[year] for year in growth_data.keys()]]
        
        return "\n" + tabulate(rows, headers=headers, tablefmt="grid")
    
    def format_quarterly_data(self, quarterly_data):
        """
        Format quarterly revenue and profit data
        
        Args:
            quarterly_data (dict): Dictionary with revenue and profit data
            
        Returns:
            str: Formatted quarterly information
        """
        if not quarterly_data or not quarterly_data["Revenue"] or not quarterly_data["Net Profit"]:
            return "Quarterly Data: Not available"
        
        # Get the last two quarters
        revenue_quarters = list(quarterly_data["Revenue"].keys())
        if len(revenue_quarters) >= 2:
            last_two_quarters = revenue_quarters[-2:]
        else:
            last_two_quarters = revenue_quarters
        
        headers = ["Metric"] + last_two_quarters
        rows = []
        
        # Add revenue row
        revenue_row = ["Revenue"]
        for quarter in last_two_quarters:
            revenue_row.append(quarterly_data["Revenue"].get(quarter, "N/A"))
        rows.append(revenue_row)
        
        # Add net profit row
        profit_row = ["Net Profit"]
        for quarter in last_two_quarters:
            profit_row.append(quarterly_data["Net Profit"].get(quarter, "N/A"))
        rows.append(profit_row)
        
        return "\n" + tabulate(rows, headers=headers, tablefmt="grid")
    
    def format_peg(self, peg_ratio):
        """
        Format PEG ratio
        
        Args:
            peg_ratio (float): PEG ratio value
            
        Returns:
            str: Formatted PEG information
        """
        if peg_ratio is None:
            return "PEG Ratio: Not available"
        
        return f"PEG Ratio: {peg_ratio:.2f}"
    
    def format_additional_metrics(self, ratios):
        """
        Format additional metrics from the ratios dictionary
        
        Args:
            ratios (dict): Dictionary of financial ratios
            
        Returns:
            str: Formatted additional metrics
        """
        if not ratios:
            return "Additional Metrics: Not available"
        
        # Define the metrics we want to display
        target_metrics = [
            "Stock P/E",
            "Industry P/E",
            "Compounded Sales Growth",
            "Compounded Profit Growth",
            "PEG Ratio"
        ]
        
        # Create a table for the metrics
        headers = ["Metric", "Value"]
        rows = []
        
        for metric in target_metrics:
            if metric in ratios:
                rows.append([metric, ratios[metric]])
        
        if not rows:
            return "Additional Metrics: Not available"
        
        return "\n" + tabulate(rows, headers=headers, tablefmt="grid")
    
    def format_summary(self, roe_data, growth_data, quarterly_data, peg_ratio):
        """
        Format a complete summary of the financial data
        
        Args:
            roe_data (dict): ROE values by year
            growth_data (dict): Growth values by year
            quarterly_data (dict): Dictionary with revenue and profit data
            peg_ratio (float): PEG ratio value
            
        Returns:
            str: Formatted summary
        """
        # Extract additional metrics from the extractor
        from extractor import FinancialDataExtractor
        ratios = {}
        
        # If we have a PEG ratio, add it to the ratios
        if peg_ratio is not None:
            ratios["PEG Ratio"] = f"{peg_ratio:.2f}"
        
        # Try to get the ratios from the extractor
        try:
            # Use the extractor instance that was passed to us
            if hasattr(self, 'extractor'):
                # Get the ratios
                all_ratios = self.extractor.extract_ratios()
                
                # Add the ratios we're interested in
                for key in ["Stock P/E", "Industry P/E", "Compounded Sales Growth", "Compounded Profit Growth"]:
                    if key in all_ratios:
                        ratios[key] = all_ratios[key]
        except Exception as e:
            logger.error(f"Error getting additional metrics: {e}")
        
        summary = [
            f"\n{'=' * 50}",
            f"Financial Summary for {self.company_name}",
            f"{'=' * 50}",
            "\nROE (Return on Equity):",
            self.format_roe(roe_data),
            "\nLast Two Quarters Revenue and Profit:",
            self.format_quarterly_data(quarterly_data),
            "\nKey Metrics:",
            self.format_additional_metrics(ratios),
            f"\n{'=' * 50}\n"
        ]
        
        return "\n".join(summary)
