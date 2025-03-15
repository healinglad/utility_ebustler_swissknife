# Financial Screener

A utility to fetch financial data from screener.in for Indian stocks, available as both a command-line tool and a GUI desktop widget.

## Features

- Search for a company by its trading symbol on screener.in
- Extract financial parameters for the last 3 years
- Provide key metrics:
  - Return on Equity (ROE)
  - 3-year growth rates
  - Last two quarters' revenue and net profits
  - Price/Earnings to Growth (PEG) ratio

## Installation

1. Clone the repository or download the source code
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Command-Line Usage

Run the utility from the command line, providing a trading symbol as an argument:

```bash
python main.py SYMBOL
```

For example, to get financial data for Tata Motors:

```bash
python main.py TATAMOTORS
```

## GUI Usage

Run the GUI application to use the desktop widget:

```bash
python gui.py
```

The GUI provides a user-friendly interface where you can:
- Enter a stock symbol and search for its financial data
- View the results in a persistent window
- Adjust delay settings and toggle between consolidated/standalone data
- Clear results and perform multiple searches

### Using the GUI

1. Enter a stock symbol in the "Symbol" field (e.g., TATAMOTORS)
2. Optionally adjust the delay time (in seconds) to avoid rate limiting
3. Choose between consolidated or standalone financial data
4. Click "Search" or press Enter to fetch the data
5. View the results in the text area
6. Use "Clear" to reset the results for a new search

### Options

- `--delay`: Set the delay between requests in seconds (default: 1)
- `--consolidated/--standalone`: Use consolidated or standalone financial data (default: consolidated)

```bash
# Increase delay between requests
python main.py TATAMOTORS --delay 2

# Use standalone (non-consolidated) financial data
python main.py TATAMOTORS --standalone
```

## Example Output

```
==================================================
Financial Summary for Tata Motors Ltd
==================================================

ROE (Return on Equity):

+-------+--------+--------+--------+
| Metric | Mar 22 | Mar 23 | Mar 24 |
+=======+========+========+========+
| ROE    | 12.5%  | 15.2%  | 18.7%  |
+-------+--------+--------+--------+

3-Year Growth:

+--------+--------+--------+--------+
| Metric  | Mar 22 | Mar 23 | Mar 24 |
+========+========+========+========+
| Growth  | 8.2%   | 12.4%  | 15.8%  |
+--------+--------+--------+--------+

Last Two Quarters Revenue and Profit:

+------------+-------------+-------------+
| Metric     | Dec 23      | Mar 24      |
+============+=============+=============+
| Revenue    | 12,452 Cr   | 13,768 Cr   |
+------------+-------------+-------------+
| Net Profit | 1,451 Cr    | 1,875 Cr    |
+------------+-------------+-------------+

PEG Ratio: 1.25

==================================================
```

## Requirements

- Python 3.6+
- Internet connection
- Required Python packages (see requirements.txt)

## Limitations

- The utility relies on the structure of screener.in website, which may change over time
- Some financial data may not be available for all companies
- Rate limiting may be applied by screener.in for frequent requests

## License

MIT License
