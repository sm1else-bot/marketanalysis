import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from utils.stock_data import get_stock_data, get_company_info
from utils.technical_analysis import calculate_technical_indicators, get_indicator_plots
from utils.ui_components import create_price_chart, display_metric_card, render_company_info, display_news_section
from utils.news_fetcher import get_stock_news

# Page configuration
st.set_page_config(
    page_title="TLW/UI Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>Stock Market Analysis - TLW/UI</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)
# Load custom CSS
with open("styles/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# Sidebar
with st.sidebar:
    st.title("Stock Analysis")
    search_query = st.text_input("Search Stocks", 
                                placeholder="Enter stock symbol (e.g., RELIANCE, TCS)")

    exchange = st.radio("Exchange", ["NSE", "BSE"])

    # Date range selector
    st.subheader("Date Range")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    selected_start_date = st.date_input("Start Date", start_date)
    selected_end_date = st.date_input("End Date", end_date)

    timeframe = st.selectbox(
        "Timeframe",
        ["1d", "1h", "15m", "5m"],
        help="Select data timeframe (daily, hourly, or minutes)"
    )

    st.subheader("Watchlist")
    for symbol in st.session_state.watchlist:
        if st.button(f"📌 {symbol}"):
            st.session_state.watchlist.remove(symbol)
            st.rerun(scope="fragment")

# Default title
if not search_query:
    st.title("<-- Search for Stocks")

if search_query:
    symbol = search_query.upper()
    if exchange == "BSE":
        symbol = f"{symbol}.BO"
    else:
        symbol = f"{symbol}.NS"

    # Add to watchlist button
    if symbol not in st.session_state.watchlist:
        if st.button("Add to Watchlist"):
            st.session_state.watchlist.append(symbol)
            st.rerun(scope="fragment")

    # Fetch stock data with selected date range and timeframe
    df, stock_info = get_stock_data(
        symbol,
        start=selected_start_date,
        end=selected_end_date,
        interval=timeframe
    )

    if df is not None and not df.empty and stock_info is not None:
        # Update title with stock name
        company_name = stock_info.get('longName', symbol)
        st.title(f"{company_name} ({symbol})")

        # Calculate current price and daily change
        current_price = df['Close'].iloc[-1]
        prev_price = df['Close'].iloc[-2]
        price_change = ((current_price - prev_price) / prev_price) * 100

        # Display current price and change
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", 
                     f"₹{current_price:.2f}", 
                     f"{price_change:+.2f}%")

        # Calculate and display technical indicators
        df = calculate_technical_indicators(df)
        indicator_plots = get_indicator_plots(df)

        # Create and display interactive chart
        fig = create_price_chart(df, indicator_plots)
        st.plotly_chart(fig, use_container_width=True)

        # Add chart instructions
        with st.expander("📐 Drawing Tools Help"):
            st.markdown("""
            ### How to use drawing tools:
            1. Click on the drawing tools in the chart toolbar
            2. Draw trend lines, shapes, or annotations on the chart
            3. Use the eraser tool to remove drawings
            4. Double-click to finish drawing

            Available tools:
            - Line: Draw trend lines and support/resistance levels
            - Open/Closed Path: Draw custom shapes and patterns
            - Circle/Rectangle: Highlight specific areas
            - Eraser: Remove drawings
            """)

        # Display company information
        company_info = get_company_info(stock_info)
        render_company_info(company_info)

        # Fetch and display news
        news_items = get_stock_news(company_name)
        display_news_section(news_items)

    else:
        st.error(f"Could not find data for {symbol}. Please check if the symbol is correct and try again.")

# Auto-refresh every 5 minutes
time.sleep(300)
st.rerun(scope="app")
