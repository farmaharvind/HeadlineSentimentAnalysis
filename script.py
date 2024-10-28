import yfinance as yf
import pandas as pd
import requests
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

# Load the FinancialBERT model and tokenizer for sentiment analysis
model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def fetch_news_headlines(ticker_symbol):
    """Fetches news headlines for the given stock ticker symbol using yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    stock_info = ticker.news

    # Check if news data was retrieved
    if not stock_info:
        print(f"No news data found for ticker: {ticker_symbol}")
        return pd.DataFrame()  # Return empty DataFrame if no data found

    # Extract headlines from the news data
    headlines = [item['title'] for item in stock_info]
    return headlines

def analyze_sentiment(headlines):
    """Analyzes sentiment for each headline using FinancialBERT."""
    # Use the sentiment pipeline to analyze each headline
    results = sentiment_pipeline(headlines)
    # Combine headlines with their sentiment analysis results
    sentiment_data = [{"Headline": headline, "Sentiment": result['label'], "Confidence": result['score']} 
                      for headline, result in zip(headlines, results)]
    return pd.DataFrame(sentiment_data)

# Example usage
ticker_symbol = "META"  # Change this symbol as needed
headlines = fetch_news_headlines(ticker_symbol)

if headlines:
    sentiment_df = analyze_sentiment(headlines)
    print(sentiment_df)  # Display the headlines with their sentiment analysis