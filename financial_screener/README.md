# Financial Screener Utility

This utility fetches financial data from [screener.in](https://www.screener.in/) for Indian stocks. It provides both a command-line interface and a GUI desktop widget.

## Features

-   Fetches ROE (Return on Equity) for the last 3 years.
-   Provides revenue and net profit for the last two quarters.
-   Displays key financial metrics:
    -   Stock P/E
    -   Industry P/E
    -   Compounded Sales Growth
    -   Compounded Profit Growth
    -   PEG Ratio
-   Handles error cases with user-friendly messages.
-   Supports both consolidated and standalone financial data.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/healinglad/financial-screener-utility.git
    cd financial-screener-utility
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r financial_screener/requirements.txt
    ```

## Usage

### Command-Line Interface

```bash
# On Linux/macOS
./financial_screener.sh SYMBOL

# On Windows
./financial_screener.bat SYMBOL
```

Replace `SYMBOL` with the stock symbol (e.g., `TATAMOTORS`, `VBL`, `RELIANCE`).

**Options:**

-   `--delay SECONDS`: Delay between requests in seconds (default: 1).
-   `--consolidated` / `--standalone`: Use consolidated or standalone financial data (default: consolidated).
-   `--help`: Show help message.

### GUI Desktop Widget

```bash
# On Linux/macOS
./financial_screener_gui.sh

# On Windows
./financial_screener_gui.bat
```

The GUI allows you to enter a stock symbol, adjust the delay, toggle between consolidated and standalone data, and view the results.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License

Copyright (c) 2025 [Your Name or Organization Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
