import pandas as pd
import numpy as np

def calculate_technical_indicators(df):
    """Calculate various technical indicators"""
    # Moving Averages
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['MA200'] = df['Close'].rolling(window=200).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Bollinger Bands
    df['BB_middle'] = df['Close'].rolling(window=20).mean()
    df['BB_upper'] = df['BB_middle'] + 2*df['Close'].rolling(window=20).std()
    df['BB_lower'] = df['BB_middle'] - 2*df['Close'].rolling(window=20).std()
    
    return df

def get_indicator_plots(df):
    """Generate technical indicator plots configuration"""
    return [
        {
            'name': 'Price and Moving Averages',
            'traces': [
                {'y': df['Close'], 'name': 'Price', 'line': {'color': '#ffffff'}},
                {'y': df['MA20'], 'name': 'MA20', 'line': {'color': '#f6c85f'}},
                {'y': df['MA50'], 'name': 'MA50', 'line': {'color': '#8f5fe8'}},
                {'y': df['MA200'], 'name': 'MA200', 'line': {'color': '#4ecdc4'}}
            ]
        },
        {
            'name': 'RSI',
            'traces': [
                {'y': df['RSI'], 'name': 'RSI', 'line': {'color': '#f6c85f'}},
            ],
            'yaxis': {'range': [0, 100]}
        },
        {
            'name': 'MACD',
            'traces': [
                {'y': df['MACD'], 'name': 'MACD', 'line': {'color': '#4ecdc4'}},
                {'y': df['Signal_Line'], 'name': 'Signal Line', 'line': {'color': '#f6c85f'}}
            ]
        }
    ]
