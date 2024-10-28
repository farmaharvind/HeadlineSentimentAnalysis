from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go

# Load the FinancialBERT model and tokenizer for sentiment analysis
model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
sentiment_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

app = Flask(__name__)

def fetch_news_headlines(ticker_symbol):
    """Fetches news headlines for the given stock ticker symbol using yfinance."""
    ticker = yf.Ticker(ticker_symbol)
    stock_info = ticker.news

    if not stock_info:
        return [], False  # Return empty list if no data found and mark ticker as invalid
    
    # Extract and return only the headlines
    return [item['title'] for item in stock_info], True

def analyze_sentiment(headlines):
    """Analyzes sentiment for each headline using FinancialBERT."""
    results = sentiment_pipeline(headlines)
    sentiment_data = [{"headline": headline, "sentiment": result['label'], "confidence": result['score']} 
                      for headline, result in zip(headlines, results)]
    return pd.DataFrame(sentiment_data)

def calculate_sentiment_skew(sentiment_df):
    """Determines the skew based on proportions of positive, neutral, and negative sentiments with custom thresholds."""
    if sentiment_df.empty:
        return "No data", 0, 0, 0

    # Count each sentiment
    positive_count = len(sentiment_df[sentiment_df["sentiment"] == "positive"])
    neutral_count = len(sentiment_df[sentiment_df["sentiment"] == "neutral"])
    negative_count = len(sentiment_df[sentiment_df["sentiment"] == "negative"])
    
    # Calculate proportions
    total = len(sentiment_df)
    positive_ratio = positive_count / total
    neutral_ratio = neutral_count / total
    negative_ratio = negative_count / total

    # Skew logic
    if positive_ratio >= 0.25:
        skew = "Slightly Positive" if neutral_ratio > positive_ratio else "Positive"
    elif negative_ratio >= 0.25:
        skew = "Slightly Negative" if neutral_ratio > negative_ratio else "Negative"
    else:
        skew = "Neutral"
    
    # Return skew and sentiment percentages
    return skew, positive_ratio * 100, neutral_ratio * 100, negative_ratio * 100

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    charts = {}

    if request.method == "POST":
        tickers = request.form.get("tickers").upper().split(",")
        
        for ticker in tickers:
            ticker = ticker.strip()
            headlines, valid = fetch_news_headlines(ticker)
            if not valid:
                results.append({"Ticker": ticker, "Skew": "Invalid Ticker"})
                continue

            # Analyze sentiment for each headline and get DataFrame with details
            sentiment_df = analyze_sentiment(headlines)
            
            # Calculate skew and sentiment percentages
            skew, percent_positive, percent_neutral, percent_negative = calculate_sentiment_skew(sentiment_df)
            results.append({
                "Ticker": ticker,
                "Skew": skew,
                "Percent Positive": percent_positive,
                "Percent Neutral": percent_neutral,
                "Percent Negative": percent_negative
            })
            
            # Generate pie chart for sentiment distribution
            fig = px.pie(
                names=["Positive", "Neutral", "Negative"],
                values=[percent_positive, percent_neutral, percent_negative],
                title=f"{ticker} Sentiment Distribution"
            )
            fig.update_traces(marker=dict(colors=['green', 'gray', 'red']))
            charts[ticker] = pio.to_html(fig, full_html=False)

    return render_template("index.html", results=results, charts=charts)

if __name__ == "__main__":
    app.run(debug=True)
