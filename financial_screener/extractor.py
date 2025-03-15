"""
Extractor module for parsing financial data from screener.in HTML
"""

import logging
import re
from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialDataExtractor:
    """
    A class to extract financial data from screener.in HTML
    """
    
    def __init__(self, soup):
        """
        Initialize with BeautifulSoup object of the company page
        
        Args:
            soup (BeautifulSoup): Parsed HTML of the company page
        """
        self.soup = soup
        self.company_name = self._extract_company_name()
        
    def _extract_company_name(self):
        """
        Extract the company name from the page
        
        Returns:
            str: Company name
        """
        try:
            # Try to find the company name in the h1 tag
            company_name = self.soup.select_one("h1.company-name")
            if company_name:
                return company_name.text.strip()
            
            # Try to find the company name in the title tag
            title = self.soup.select_one("title")
            if title:
                title_text = title.text.strip()
                # Title format is usually "Company Name: Stock Price Quote"
                if ":" in title_text:
                    return title_text.split(":")[0].strip()
                return title_text
            
            # Try to find the company name in any prominent heading
            for heading in self.soup.select("h1, h2, h3"):
                if heading.text.strip() and "screener" not in heading.text.lower():
                    return heading.text.strip()
            
            logger.warning("Could not extract company name")
            return "Unknown Company"
        except (AttributeError, TypeError) as e:
            logger.warning(f"Error extracting company name: {e}")
            return "Unknown Company"
    
    def _extract_table_data(self, table_id):
        """
        Extract data from a specific table
        
        Args:
            table_id (str): ID or selector of the table to extract
            
        Returns:
            dict: Dictionary with row names as keys and lists of values
        """
        try:
            table = self.soup.select_one(table_id)
            if not table:
                logger.warning(f"Table not found: {table_id}")
                return {}
            
            # Extract headers (years/quarters)
            headers = [th.text.strip() for th in table.select("thead th")[1:]]  # Skip first header (row names)
            
            data = {}
            # Extract rows
            for row in table.select("tbody tr"):
                cells = row.select("td")
                if not cells:
                    continue
                
                row_name = cells[0].text.strip()
                row_values = [cell.text.strip() for cell in cells[1:]]
                
                # Ensure we have the same number of values as headers
                row_values = row_values[:len(headers)]
                while len(row_values) < len(headers):
                    row_values.append("")
                
                data[row_name] = dict(zip(headers, row_values))
            
            return data
        except Exception as e:
            logger.error(f"Error extracting table data: {e}")
            return {}
    
    def extract_annual_data(self):
        """
        Extract annual financial data
        
        Returns:
            dict: Annual financial data
        """
        logger.info("Extracting annual financial data")
        return self._extract_table_data("#profit-loss")
    
    def extract_quarterly_data(self):
        """
        Extract quarterly financial data
        
        Returns:
            dict: Quarterly financial data
        """
        logger.info("Extracting quarterly financial data")
        return self._extract_table_data("#quarters")
    
    def extract_ratios(self, peg_ratio=None):
        """
        Extract key financial ratios
        
        Args:
            peg_ratio (float, optional): PEG ratio to include in the results
            
        Returns:
            dict: Financial ratios
        """
        logger.info("Extracting financial ratios")
        ratios = {}
        
        try:
            # Extract ratios from the ratios section
            ratio_sections = self.soup.select(".company-ratios .flex-row")
            
            for section in ratio_sections:
                for item in section.select(".flex-item"):
                    label_elem = item.select_one(".name")
                    value_elem = item.select_one(".value")
                    
                    if label_elem and value_elem:
                        label = label_elem.text.strip()
                        value = value_elem.text.strip()
                        ratios[label] = value
            
            # Extract specific metrics the user wants
            target_metrics = [
                "Stock P/E", "P/E", "PE", "PE Ratio",
                "Industry P/E", "Industry PE", "Sector P/E", "Sector PE",
                "Compounded Sales Growth", "Sales Growth",
                "Compounded Profit Growth", "Profit Growth",
                "PEG Ratio", "PEG"
            ]
            
            # If we couldn't find all target metrics in the company-ratios section, try other sections
            if not all(any(metric in key for key in ratios) for metric in ["P/E", "Growth", "PEG"]):
                logger.info("Not all target metrics found in company-ratios section, trying alternative sections")
                
                # Try to find ratios in the data-table sections
                tables = self.soup.select("table.data-table")
                for table in tables:
                    # Check if this table has ratio data
                    header = table.select_one("thead th")
                    if header and any(word in header.text for word in ["Ratio", "Valuation", "Growth", "PE", "P/E"]):
                        for row in table.select("tbody tr"):
                            cells = row.select("td")
                            if len(cells) >= 2:
                                label = cells[0].text.strip()
                                value = cells[1].text.strip()
                                if any(metric in label for metric in target_metrics):
                                    ratios[label] = value
                
                # Try to find ratios in any div with ratio-like labels
                all_elements = self.soup.select("div, span, p, td, th")
                for elem in all_elements:
                    text = elem.text.strip()
                    if any(metric in text for metric in target_metrics):
                        # Try to split the text into label and value
                        parts = text.split(":")
                        if len(parts) == 2:
                            label = parts[0].strip()
                            value = parts[1].strip()
                            ratios[label] = value
                        else:
                            # Try to find a nearby element with the value
                            next_elem = elem.find_next_sibling()
                            if next_elem and next_elem.text.strip():
                                value = next_elem.text.strip()
                                ratios[text] = value
                            else:
                                # Try parent's next sibling
                                parent = elem.parent
                                if parent:
                                    next_parent = parent.find_next_sibling()
                                    if next_parent and next_parent.text.strip():
                                        value = next_parent.text.strip()
                                        ratios[text] = value
            
            # Extract ROE specifically
            if not any("ROE" in key for key in ratios):
                roe_elements = self.soup.find_all(text=lambda text: text and "ROE" in text)
                for elem in roe_elements:
                    parent = elem.parent
                    if parent:
                        # Try to find a value near this element
                        next_elem = parent.find_next_sibling()
                        if next_elem and next_elem.text.strip():
                            ratios["ROE"] = next_elem.text.strip()
                        else:
                            # Try to find a value in a nearby element
                            value_elem = parent.find_next("span") or parent.find_next("div")
                            if value_elem and value_elem.text.strip():
                                ratios["ROE"] = value_elem.text.strip()
            
            # Clean up and normalize ratio names
            normalized_ratios = {}
            for key, value in ratios.items():
                # Skip values that are just "Alerts" or empty
                if value.strip() in ["Alerts", ""]:
                    continue
                
                # Clean up the value - extract just the numeric part if it's a long text
                cleaned_value = value
                if len(value) > 50:  # If it's a long text, try to extract just the numeric part
                    # Try to find a numeric value at the beginning of the text
                    match = re.search(r'^\s*(\d+\.?\d*)', value)
                    if match:
                        cleaned_value = match.group(1)
                    else:
                        # Try to find any numeric value in the text
                        match = re.search(r'(\d+\.?\d*)', value)
                        if match:
                            cleaned_value = match.group(1)
                        else:
                            # Skip this value if we can't extract a numeric part
                            continue
                
                # Clean up growth values
                if "Growth" in key and ":" in cleaned_value:
                    parts = cleaned_value.split(":")
                    if len(parts) >= 2:
                        cleaned_value = parts[1].strip()
                
                # Normalize Stock P/E variations
                if any(pe_term in key for pe_term in ["Stock P/E", "P/E", "PE Ratio"]) and "Industry" not in key and "Sector" not in key:
                    normalized_ratios["Stock P/E"] = cleaned_value
                # Normalize Industry P/E variations
                elif any(pe_term in key for pe_term in ["Industry P/E", "Sector P/E", "Industry PE", "Sector PE"]):
                    normalized_ratios["Industry P/E"] = cleaned_value
                # Normalize Compounded Sales Growth variations
                elif any(growth_term in key for growth_term in ["Compounded Sales Growth", "Sales Growth"]) and "Quarterly" not in key:
                    normalized_ratios["Compounded Sales Growth"] = cleaned_value
                # Normalize Compounded Profit Growth variations
                elif any(growth_term in key for growth_term in ["Compounded Profit Growth", "Profit Growth"]) and "Quarterly" not in key:
                    normalized_ratios["Compounded Profit Growth"] = cleaned_value
                # Normalize PEG Ratio variations
                elif any(peg_term in key for peg_term in ["PEG Ratio", "PEG"]):
                    normalized_ratios["PEG Ratio"] = cleaned_value
                # Keep ROE as is
                elif "ROE" in key or "Return on Equity" in key:
                    normalized_ratios["ROE"] = cleaned_value
                # Keep other ratios as is
                else:
                    normalized_ratios[key] = cleaned_value
                    
            # Try to find specific metrics directly from the page if they're missing
            if "Stock P/E" not in normalized_ratios:
                pe_elements = self.soup.find_all(text=lambda text: text and "P/E" in text and "Industry" not in text and "Sector" not in text)
                for elem in pe_elements:
                    parent = elem.parent
                    if parent:
                        # Try to find a value near this element
                        next_elem = parent.find_next_sibling()
                        if next_elem and next_elem.text.strip() and next_elem.text.strip() != "Alerts":
                            normalized_ratios["Stock P/E"] = next_elem.text.strip()
                            break
                            
            if "PEG Ratio" not in normalized_ratios and peg_ratio is not None:
                normalized_ratios["PEG Ratio"] = f"{peg_ratio:.2f}"
            
            logger.info(f"Found ratios: {normalized_ratios}")
            return normalized_ratios
        except Exception as e:
            logger.error(f"Error extracting ratios: {e}")
            return {}
    
    def extract_roe(self):
        """
        Extract Return on Equity (ROE) values
        
        Returns:
            dict: ROE values for available years
        """
        logger.info("Extracting ROE data")
        annual_data = self.extract_annual_data()
        
        # Look for ROE in the annual data
        for key in annual_data:
            if "ROE" in key or "Return on Equity" in key:
                return annual_data[key]
        
        # If not found in annual data, check ratios
        ratios = self.extract_ratios()
        for key in ratios:
            if "ROE" in key or "Return on Equity" in key:
                logger.info(f"Found ROE in ratios: {key} = {ratios[key]}")
                return {"Latest": ratios[key]}
        
        # Try to find ROE in any text on the page
        roe_elements = self.soup.find_all(text=lambda text: text and "ROE" in text)
        if roe_elements:
            for elem in roe_elements:
                parent = elem.parent
                if parent:
                    # Try to find a value near this element
                    value_elem = parent.find_next("span") or parent.find_next("div")
                    if value_elem and value_elem.text.strip():
                        value = value_elem.text.strip()
                        logger.info(f"Found ROE in page text: {value}")
                        return {"Latest": value}
        
        logger.warning("ROE data not found")
        return {}
    
    def extract_growth(self, metric="Sales Growth"):
        """
        Extract growth metrics
        
        Args:
            metric (str): Name of the growth metric to extract
            
        Returns:
            dict: Growth values for available years
        """
        logger.info(f"Extracting {metric} data")
        annual_data = self.extract_annual_data()
        
        # Look for the growth metric in the annual data
        for key in annual_data:
            if metric in key:
                return annual_data[key]
        
        logger.warning(f"{metric} data not found")
        return {}
    
    def extract_quarterly_revenue_profit(self):
        """
        Extract revenue and profit from quarterly data
        
        Returns:
            dict: Dictionary with revenue and profit for quarters
        """
        logger.info("Extracting quarterly revenue and profit")
        quarterly_data = self.extract_quarterly_data()
        
        result = {
            "Revenue": {},
            "Net Profit": {}
        }
        
        # Look for revenue and profit in quarterly data
        for key in quarterly_data:
            if "Revenue" in key or "Sales" in key:
                result["Revenue"] = quarterly_data[key]
            elif "Net Profit" in key or "PAT" in key:
                result["Net Profit"] = quarterly_data[key]
        
        return result
    
    def extract_peg(self):
        """
        Extract or calculate PEG ratio
        
        Returns:
            float: PEG ratio if available, None otherwise
        """
        logger.info("Extracting/calculating PEG ratio")
        ratios = self.extract_ratios()
        
        # Check if PEG is directly available
        for key in ratios:
            if "PEG" in key:
                try:
                    return float(ratios[key].replace(',', ''))
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert PEG value to float: {ratios[key]}")
                    return None
        
        # If not, try to calculate it from PE and growth rate
        pe_ratio = None
        growth_rate = None
        
        # Extract PE ratio
        for key in ratios:
            if "P/E" in key or "PE Ratio" in key or "PE" == key:
                try:
                    # Remove any non-numeric characters except decimal point
                    pe_value = ''.join(c for c in ratios[key] if c.isdigit() or c == '.')
                    pe_ratio = float(pe_value)
                    logger.info(f"Found PE ratio: {pe_ratio}")
                    break
                except (ValueError, TypeError):
                    logger.warning(f"Could not convert PE value to float: {ratios[key]}")
        
        # If PE ratio not found in ratios, try to find it in the page text
        if pe_ratio is None:
            pe_elements = self.soup.find_all(text=lambda text: text and ("P/E" in text or "PE" in text))
            if pe_elements:
                for elem in pe_elements:
                    parent = elem.parent
                    if parent:
                        # Try to find a value near this element
                        value_elem = parent.find_next("span") or parent.find_next("div")
                        if value_elem and value_elem.text.strip():
                            try:
                                pe_value = ''.join(c for c in value_elem.text.strip() if c.isdigit() or c == '.')
                                pe_ratio = float(pe_value)
                                logger.info(f"Found PE ratio in page text: {pe_ratio}")
                                break
                            except (ValueError, TypeError):
                                continue
        
        # Extract growth rate
        growth_data = self.extract_growth("Sales Growth")
        if growth_data:
            # Get the most recent growth rate
            recent_year = list(growth_data.keys())[-1]
            growth_value = growth_data[recent_year]
            
            try:
                # Remove % sign and convert to float
                growth_rate = float(growth_value.replace('%', '').replace(',', '')) / 100
                logger.info(f"Found growth rate: {growth_rate}")
            except (ValueError, TypeError):
                logger.warning(f"Could not convert growth value to float: {growth_value}")
        
        # If growth rate not found, try to find it in the page text
        if growth_rate is None:
            growth_elements = self.soup.find_all(text=lambda text: text and "Growth" in text)
            if growth_elements:
                for elem in growth_elements:
                    parent = elem.parent
                    if parent:
                        # Try to find a value near this element
                        value_elem = parent.find_next("span") or parent.find_next("div")
                        if value_elem and value_elem.text.strip():
                            try:
                                growth_value = ''.join(c for c in value_elem.text.strip() if c.isdigit() or c == '.' or c == '%')
                                if '%' in growth_value:
                                    growth_value = growth_value.replace('%', '')
                                    growth_rate = float(growth_value) / 100
                                else:
                                    growth_rate = float(growth_value) / 100
                                logger.info(f"Found growth rate in page text: {growth_rate}")
                                break
                            except (ValueError, TypeError):
                                continue
        
        # Calculate PEG if we have both PE and growth rate
        if pe_ratio is not None and growth_rate is not None and growth_rate > 0:
            peg = pe_ratio / (growth_rate * 100)  # Convert growth rate to percentage
            logger.info(f"Calculated PEG ratio: {peg}")
            return peg
        
        logger.warning("Could not calculate PEG ratio")
        return None
