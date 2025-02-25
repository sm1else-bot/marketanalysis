import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_price_chart(df, indicator_plots):
    """Create an interactive price chart with technical indicators"""
    fig = make_subplots(rows=3, cols=1, 
                        shared_xaxes=True,
                        row_heights=[0.5, 0.25, 0.25],
                        vertical_spacing=0.05,
                        subplot_titles=('Price and Moving Averages', 'RSI', 'MACD'))

    # Main price chart
    for trace in indicator_plots[0]['traces']:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=trace['y'],
            name=trace['name'],
            line=trace['line']
        ), row=1, col=1)

    # RSI
    fig.add_trace(go.Scatter(
        x=df.index,
        y=indicator_plots[1]['traces'][0]['y'],
        name='RSI',
        line=indicator_plots[1]['traces'][0]['line']
    ), row=2, col=1)

    # Add RSI overbought/oversold lines
    fig.add_hline(y=70, line_dash="dash", line_color="#ff4b4b", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#00ff7f", row=2, col=1)

    # MACD
    for trace in indicator_plots[2]['traces']:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=trace['y'],
            name=trace['name'],
            line=trace['line']
        ), row=3, col=1)

    # Update layout with drawing tools
    fig.update_layout(
        height=800,
        template='plotly_dark',
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        margin=dict(t=30, l=50, r=50, b=50),
        dragmode='drawline',  # Enable line drawing by default
    )

    # Add drawing tools
    fig.update_layout(
        modebar=dict(
            add=[
                'drawline',
                'drawopenpath',
                'drawclosedpath',
                'drawcircle',
                'drawrect',
                'eraseshape'
            ]
        )
    )

    # Update y-axes titles
    fig.update_yaxes(title_text="Price (₹)", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)

    return fig

def display_metric_card(label, value, delta=None):
    """Display a metric card with optional delta"""
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"**{label}**")
    with col2:
        if delta:
            delta_color = "positive-value" if float(delta.strip('%')) > 0 else "negative-value"
            st.markdown(f"<div style='text-align: right;'>{value} <span class='{delta_color}'>({delta})</span></div>", 
                       unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align: right;'>{value}</div>", unsafe_allow_html=True)

def render_company_info(info):
    """Render company information section"""
    st.markdown("### Company Information")
    for key, value in info.items():
        display_metric_card(key, value)

def display_news_section(news_items):
    """Display news section with recent articles"""
    st.markdown("### Recent News")
    if not news_items:
        st.info("No recent news found for this company.")
        return

    for item in news_items:
        with st.container():
            st.markdown(f"""
            <div style='background-color: #262730; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                <h4>{item['headline']}</h4>
                <p style='color: #888888; font-size: 0.8rem;'>{item['source']}</p>
            </div>
            """, unsafe_allow_html=True)