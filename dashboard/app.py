"""
Sports-Fashion Intersection Analytics Dashboard
Interactive dashboard showing the data-driven intersection of sports and fashion
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Sports-Fashion Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    base_path = Path(__file__).parent.parent / 'data' / 'processed'
    
    return {
        'tenniscore': pd.read_csv(base_path / 'tenniscore_processed.csv'),
        'market': pd.read_csv(base_path / 'market_combined.csv'),
        'trends': pd.read_csv(base_path / 'trends_processed.csv'),
        'challengers': pd.read_csv(base_path / 'challengers_processed.csv'),
        'summary': pd.read_csv(base_path / 'summary_stats.csv')
    }

data = load_data()

# Convert date columns
data['trends']['date'] = pd.to_datetime(data['trends']['date'])
data['challengers']['date'] = pd.to_datetime(data['challengers']['date'])

# Header
st.markdown('<div class="main-header"> Sports Meets Fashion </div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Data-Driven Analysis of the Sports-Fashion Intersection</div>', unsafe_allow_html=True)

# Key Metrics
st.markdown("### Key Insights")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Tenniscore Peak Growth",
        f"{int(data['summary']['tenniscore_peak_growth'][0])}%",
        "Post-Challengers Release"
    )

with col2:
    st.metric(
        "Women's Sportswear 2024",
        f"${data['summary']['market_2024_billion'][0]:.1f}B",
        f"+{data['summary']['market_growth_rate'][0]:.1f}% CAGR"
    )

with col3:
    st.metric(
        "Projected 2033 Market",
        f"${data['summary']['market_2033_billion'][0]:.0f}B",
        "157% Growth"
    )

with col4:
    st.metric(
        "Challengers Media Value",
        f"${data['summary']['challengers_media_value_million'][0]:.1f}M",
        "Zendaya Press Tour"
    )

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    " Challengers Effect",
    " Market Growth",
    " World Cup 2026",
    " Data Explorer"
])

# TAB 1: Challengers Effect
with tab1:
    st.markdown("## The 'Challengers' Effect on Tenniscore Fashion")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tenniscore search trends
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=data['trends']['date'],
            y=data['trends']['tenniscore'],
            name='Tenniscore',
            line=dict(color='#ff6b6b', width=3),
            fill='tozeroy'
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=data['trends']['date'],
            y=data['trends']['tennis_skirt'],
            name='Tennis Skirt',
            line=dict(color='#4ecdc4', width=2)
        ))
        
        # Add Challengers release marker
        # Add vertical line
        fig_trends.add_shape(
            type="line",
            x0='2024-04-26',
            x1='2024-04-26',
            y0=0,
            y1=1,
            yref='paper',
            line=dict(color="orange", width=2, dash="dash")
        )

        # Add annotation
        fig_trends.add_annotation(
            x='2024-04-26',
            y=1,
            yref='paper',
            text="Challengers Release",
            showarrow=False,
            yanchor='bottom',
            xanchor='right'
        )
        
        fig_trends.update_layout(
            title="Google Trends: Tenniscore Search Volume",
            xaxis_title="Date",
            yaxis_title="Search Interest (Indexed)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        # Sales growth by item
        top_items = data['tenniscore'].groupby('item')['yoy_growth_pct'].mean().sort_values(ascending=False).head(10)
        
        fig_sales = px.bar(
            x=top_items.values,
            y=top_items.index,
            orientation='h',
            title="Top Tenniscore Items by YoY Growth",
            labels={'x': 'Year-over-Year Growth (%)', 'y': 'Item'},
            color=top_items.values,
            color_continuous_scale='Reds'
        )
        
        fig_sales.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_sales, use_container_width=True)
    
    # Demographic breakdown
    st.markdown("### 👥 Growth by Demographic")
    
    demo_data = data['tenniscore'].groupby('demographic')['demo_growth_pct'].mean().sort_values(ascending=False)
    
    fig_demo = px.bar(
        x=demo_data.index,
        y=demo_data.values,
        title="Average Growth Rate by Generation",
        labels={'x': 'Demographic', 'y': 'Average Growth (%)'},
        color=demo_data.values,
        color_continuous_scale='Blues'
    )
    
    st.plotly_chart(fig_demo, use_container_width=True)
    
    # Key insights
    st.markdown("### Key Findings")
    st.markdown("""
    - **Skorts** led growth at **134% YoY**, driven by Gen Z (+213%)
    - **Adult tennis lesson searches** surged **+245%** after Challengers release
    - **Social media posts** about tenniscore reached **4,500 in May 2024** (+18% YoY)
    - **Zendaya's press tour** generated **$42.5M in media value**
    - **All age groups** adopted the trend, including Baby Boomers (+125% mini pleated skirts)
    """)

# TAB 2: Market Growth
with tab2:
    st.markdown("## Women's Sportswear Market Trajectory")
    
    # Market size over time
    fig_market = go.Figure()
    
    # Historical data
    historical = data['market'][data['market']['segment'] != 'forecast']
    forecast = data['market'][data['market']['segment'] == 'forecast']
    
    fig_market.add_trace(go.Scatter(
        x=historical['year'],
        y=historical['market_value_billion_usd'],
        name='Historical',
        mode='lines+markers',
        line=dict(color='#2ecc71', width=3),
        marker=dict(size=8)
    ))
    
    fig_market.add_trace(go.Scatter(
        x=forecast['year'],
        y=forecast['market_value_billion_usd'],
        name='Forecast',
        mode='lines+markers',
        line=dict(color='#3498db', width=3, dash='dash'),
        marker=dict(size=8)
    ))
    
    fig_market.update_layout(
        title="Women's Sportswear Market Size (2019-2033)",
        xaxis_title="Year",
        yaxis_title="Market Value (Billion USD)",
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig_market, use_container_width=True)
    
    # Jersey market
    col1, col2 = st.columns(2)
    
    with col1:
        fig_jersey = px.line(
            data['market'],
            x='year',
            y='sports_jersey_market_billion_usd',
            title='Sports Jersey Market Growth',
            markers=True
        )
        fig_jersey.update_traces(line_color='#e74c3c', line_width=3)
        st.plotly_chart(fig_jersey, use_container_width=True)
    
    with col2:
        # Growth breakdown
        st.markdown("### Growth Drivers")
        st.markdown("""
        **Market Dynamics:**
        - Base market: **$92.5B (2023)** → **$250B (2033)**
        - CAGR: **7.0%** over forecast period
        - Women's jersey sales: **+40% in 2022** (Men's World Cup year)
        - Custom jersey demand: **+30%** (personalization trend)
        
        **Key Segments:**
        - Athleisure integration
        - Performance fabrics
        - Sustainable materials
        - Celebrity collaborations
        """)
    
    # Market insights
    st.info(" The women's sportswear market is experiencing accelerated growth driven by increased sports participation, athleisure trends, and the blurring lines between athletic and everyday fashion.")

# TAB 3: World Cup 2026
with tab3:
    st.markdown("## World Cup 2026: Fashion Impact Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Soccer jersey trend
        fig_soccer = go.Figure()
        
        fig_soccer.add_trace(go.Scatter(
            x=data['trends']['date'],
            y=data['trends']['soccer_jersey'],
            name='Soccer Jersey',
            line=dict(color='#9b59b6', width=3),
            fill='tozeroy'
        ))
        
        fig_soccer.add_trace(go.Scatter(
            x=data['trends']['date'],
            y=data['trends']['football_kit'],
            name='Football Kit',
            line=dict(color='#f39c12', width=2)
        ))
        
        # Add World Cup marker
        # Add vertical line
        fig_soccer.add_shape(
            type="line",
            x0='2026-06-11',
            x1='2026-06-11',
            y0=0,
            y1=1,
            yref='paper',
            line=dict(color="green", width=2, dash="dash")
        )

        # Add annotation
        fig_soccer.add_annotation(
            x='2026-06-11',
            y=1,
            yref='paper',
            text="World Cup Kickoff",
            showarrow=False,
            yanchor='bottom',
            xanchor='right'
        )
                
        fig_soccer.update_layout(
            title="Soccer Jersey Search Trends (Building to WC 2026)",
            xaxis_title="Date",
            yaxis_title="Search Interest",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_soccer, use_container_width=True)
    
    with col2:
        # Market projections
        wc_impact = data['market'][data['market']['year'].isin([2025, 2026, 2027])]
        
        fig_wc_market = px.bar(
            wc_impact,
            x='year',
            y='football_jersey_market_billion_usd',
            title='Football Jersey Market (2025-2027)',
            labels={'football_jersey_market_billion_usd': 'Market Size ($B)'},
            color='year',
            color_continuous_scale='Greens'
        )
        
        st.plotly_chart(fig_wc_market, use_container_width=True)
    
    # Predictions
    st.markdown("### 2026 World Cup Fashion Predictions")
    
    pred_col1, pred_col2 = st.columns(2)
    
    with pred_col1:
        st.markdown("""
        **Expected Trends:**
        -  **USA jersey sales**: 500K-1M units in first month
        - **Tournament spike**: +40% sales during event
        - **Vintage jerseys**: Continued "blokecore" streetwear trend
        - **Retro designs**: 1994 WC nostalgia (last US-hosted)
        """)
    
    with pred_col2:
        st.markdown("""
        **Market Impact:**
        -  **Jersey market**: $7.5B (2025) → $8.2B (2026)
        -  **North America**: 35% regional share
        -  **Women's kits**: Expected +30-40% growth
        -  **E-commerce**: 42% of sales (vs 58% retail)
        """)
    
    # Case study
    st.markdown("### 📚 Historical Context")
    st.markdown("""
    **Similar Pop Culture × Sports Moments:**
    - **Challengers (2024)**: +245% tennis lesson searches, +134% skort sales
    - **Barbie (2023)**: Method dressing movement, pink fashion surge
    - **The Last Dance (2020)**: Vintage Jordan jersey resale boom
    
    **World Cup 2026 is positioned to replicate this pattern** with:
    - 48-team format (largest ever)
    - US/Canada/Mexico co-hosting
    - Increased media coverage
    - Growing US soccer fanbase
    """)

# TAB 4: Data Explorer
with tab4:
    st.markdown("## Explore the Data")
    
    dataset_choice = st.selectbox(
        "Select Dataset",
        ["Tenniscore Sales", "Market Growth", "Google Trends", "Challengers Impact"]
    )
    
    if dataset_choice == "Tenniscore Sales":
        st.dataframe(data['tenniscore'], use_container_width=True)
        st.download_button(
            "Download CSV",
            data['tenniscore'].to_csv(index=False),
            "tenniscore_sales.csv",
            "text/csv"
        )
    
    elif dataset_choice == "Market Growth":
        st.dataframe(data['market'], use_container_width=True)
        st.download_button(
            "Download CSV",
            data['market'].to_csv(index=False),
            "market_growth.csv",
            "text/csv"
        )
    
    elif dataset_choice == "Google Trends":
        st.dataframe(data['trends'], use_container_width=True)
        st.download_button(
            "Download CSV",
            data['trends'].to_csv(index=False),
            "google_trends.csv",
            "text/csv"
        )
    
    else:  # Challengers Impact
        st.dataframe(data['challengers'], use_container_width=True)
        st.download_button(
            "Download CSV",
            data['challengers'].to_csv(index=False),
            "challengers_impact.csv",
            "text/csv"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Data Sources: Google Trends, Clearpay/Afterpay, WeArisma, Market Research Reports</p>
    <p>Built with Streamlit | Data Engineering Portfolio Project</p>
</div>
""", unsafe_allow_html=True)
