#!/usr/bin/env python3
"""
Financial Screener GUI - A desktop widget to view financial data from screener.in
"""

import sys
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import logging
from io import StringIO
import contextlib

from scraper import ScreenerScraper
from extractor import FinancialDataExtractor
from formatter import FinancialDataFormatter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RedirectText:
    """
    A class to redirect stdout to a tkinter Text widget
    """
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = StringIO()

    def write(self, string):
        self.buffer.write(string)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Auto-scroll to the end

    def flush(self):
        pass

class FinancialScreenerApp:
    """
    A simple GUI application for the Financial Screener
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Screener")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set the icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Create a queue for thread-safe communication
        self.queue = queue.Queue()
        
        self.create_widgets()
        self.center_window()
        
    def create_widgets(self):
        """Create the GUI widgets"""
        # Create a frame for the input controls
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        # Symbol input
        ttk.Label(input_frame, text="Symbol:").pack(side=tk.LEFT, padx=(0, 5))
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(input_frame, textvariable=self.symbol_var, width=15)
        self.symbol_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.symbol_entry.focus()
        
        # Delay input
        ttk.Label(input_frame, text="Delay (sec):").pack(side=tk.LEFT, padx=(0, 5))
        self.delay_var = tk.StringVar(value="1")
        delay_spinbox = ttk.Spinbox(input_frame, from_=0.5, to=5, increment=0.5, 
                                    textvariable=self.delay_var, width=5)
        delay_spinbox.pack(side=tk.LEFT, padx=(0, 10))
        
        # Consolidated/Standalone option
        self.consolidated_var = tk.BooleanVar(value=True)
        consolidated_check = ttk.Checkbutton(input_frame, text="Consolidated", 
                                            variable=self.consolidated_var)
        consolidated_check.pack(side=tk.LEFT, padx=(0, 10))
        
        # Search button
        self.search_button = ttk.Button(input_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Clear button
        clear_button = ttk.Button(input_frame, text="Clear", command=self.clear_results)
        clear_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create a frame for the output
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a scrolled text widget for the output
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, 
                                                    width=80, height=20, font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Create a status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind the Enter key to the search button
        self.root.bind("<Return>", lambda event: self.search())
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def search(self):
        """Search for the symbol and display the results"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showerror("Error", "Please enter a symbol")
            return
        
        # Clear previous results
        self.clear_results()
        
        # Update status
        self.status_var.set(f"Searching for {symbol}...")
        
        # Disable the search button
        self.search_button.config(state=tk.DISABLED)
        
        # Start a new thread for the search
        threading.Thread(target=self._search_thread, args=(symbol,), daemon=True).start()
        
        # Start checking the queue
        self.root.after(100, self.check_queue)
        
    def _search_thread(self, symbol):
        """Thread function to perform the search"""
        try:
            # Redirect stdout to capture print output
            old_stdout = sys.stdout
            sys.stdout = RedirectText(self.output_text)
            
            # Get the delay and consolidated options
            try:
                delay = float(self.delay_var.get())
            except ValueError:
                delay = 1.0
                
            consolidated = self.consolidated_var.get()
            
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
                print("- Try increasing the delay between requests")
                print(f"{'=' * 50}\n")
                self.queue.put(("error", f"Could not find company page for symbol: {symbol}"))
                return
            
            # Extract financial data
            extractor = FinancialDataExtractor(company_page)
            
            # Get company name
            company_name = extractor.company_name
            
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
            
            self.queue.put(("success", f"Found data for {company_name}"))
            
        except Exception as e:
            print(f"\n{'=' * 50}")
            print(f"ERROR: An unexpected error occurred: {e}")
            print(f"{'=' * 50}")
            print("\nPlease try again or check your internet connection.")
            print(f"{'=' * 50}\n")
            self.queue.put(("error", f"An error occurred: {str(e)}"))
            
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            
    def check_queue(self):
        """Check the queue for messages from the search thread"""
        try:
            message_type, message = self.queue.get(block=False)
            
            if message_type == "success":
                self.status_var.set(message)
            elif message_type == "error":
                self.status_var.set(f"Error: {message}")
                
            # Re-enable the search button
            self.search_button.config(state=tk.NORMAL)
            
        except queue.Empty:
            # Queue is empty, check again later
            self.root.after(100, self.check_queue)
            
    def clear_results(self):
        """Clear the results text widget"""
        self.output_text.delete(1.0, tk.END)
        self.status_var.set("Ready")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = FinancialScreenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
