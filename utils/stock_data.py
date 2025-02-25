import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol, start=None, end=None, interval='1d'):
    """Fetch stock data from Yahoo Finance"""
    # Add .NS or .BO suffix if not present
    if not (symbol.endswith('.NS') or symbol.endswith('.BO')):
        symbol = f"{symbol}.NS"  # Default to NSE

    try:
        stock = yf.Ticker(symbol)
        df = stock.history(start=start, end=end, interval=interval)
        return df, stock.info
    except Exception as e:
        return None, None

def format_large_number(number):
    """Format large numbers to human readable format"""
    if number >= 1e9:
        return f"₹{number/1e9:.2f}B"
    elif number >= 1e7:
        return f"₹{number/1e7:.2f}Cr"
    elif number >= 1e5:
        return f"₹{number/1e5:.2f}L"
    else:
        return f"₹{number:.2f}"

def get_company_info(stock_info):
    """Extract relevant company information"""
    if not stock_info:
        return {}

    return {
        "Market Cap": format_large_number(stock_info.get('marketCap', 0)),
        "52 Week High": format_large_number(stock_info.get('fiftyTwoWeekHigh', 0)),
        "52 Week Low": format_large_number(stock_info.get('fiftyTwoWeekLow', 0)),
        "P/E Ratio": f"{stock_info.get('trailingPE', 0):.2f}",
        "Volume": format_large_number(stock_info.get('volume', 0)),
        "Sector": stock_info.get('sector', 'N/A'),
        "Industry": stock_info.get('industry', 'N/A')
    }