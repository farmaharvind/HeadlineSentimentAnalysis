# Sentiment Analysis for Multiple Tickers

This web application allows users to input stock ticker symbols, analyze sentiment based on recent news headlines, and view sentiment distribution. It utilizes **FinancialBERT** for sentiment analysis and **Yahoo Finance** to fetch news headlines.

## Features

* **Input Multiple Tickers**: Accepts a list of ticker symbols to analyze
* **Sentiment Analysis**: Uses FinancialBERT to analyze the sentiment of recent headlines for each ticker
* **Sentiment Distribution Visualization**: Displays a pie chart of positive, neutral, and negative sentiment proportions for each ticker
* **Skew Indicator**: Shows sentiment skew in green for positive and red for negative
* **Invalid Ticker Handling**: Notifies if a ticker symbol is invalid or has no available data

## Installation

### Prerequisites
* Python 3.6 or higher
* `pip` (Python package manager)

### Required Packages
Install the following packages by running:

```bash
pip install flask yfinance pandas transformers plotly
```

## Usage

### Step 1: Start the Application
Run the application using the following command:

```bash
python app.py
```

This will start the Flask server, typically on `http://127.0.0.1:5000`.

### Step 2: Access the Web Interface
Open a web browser and go to `http://127.0.0.1:5000`. You'll see the main interface.

### Step 3: Enter Stock Tickers
* Enter one or multiple ticker symbols (comma-separated)
* Click **Analyze** to process the sentiment analysis

### Step 4: View Results
* The app displays sentiment skew for each ticker (Positive, Negative, or Neutral)
* Each ticker's sentiment distribution is visualized in a pie chart
* Invalid tickers or tickers without news data will be flagged as "Invalid Ticker"

## Project Structure
```
.
├── app.py           # Main application file
├── templates/
│   └── index.html   # HTML template for the web interface
└── README.md        # Project documentation
```

## Code Overview
* `app.py`: Main application file containing logic to fetch news headlines, analyze sentiment, calculate skew, and serve results on a web interface
* `index.html`: HTML template for rendering the user interface with results, skew labels, and pie charts for sentiment distribution

## Example Output
1. **Ticker**: `META`
   * **Skew**: Positive (in green) or Negative (in red)
   * **Sentiment Breakdown**: Pie chart with percentage distribution
2. **Invalid Ticker**: An error message is displayed for invalid tickers

## Dependencies
* **Flask**: Used to create a web server and serve HTML templates
* **yfinance**: Used to fetch recent news headlines for the given ticker symbols
* **Transformers (FinancialBERT)**: Pre-trained model used to classify sentiment of headlines
* **Plotly**: Generates pie charts for visualizing sentiment distribution

## Known Limitations
* **News Availability**: If a ticker has no recent news, it will be marked as "Invalid Ticker"
* **API Limitations**: Yahoo Finance might have rate limits or restrictions on news data retrieval
