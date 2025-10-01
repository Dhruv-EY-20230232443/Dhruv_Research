import streamlit as st
import pandas as pd
import os
from pathlib import Path
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="Research Portal",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Premium dark theme CSS with smooth animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Space Grotesk', sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Dark gradient background with particle effect */
    .main {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
        overflow-x: hidden;
    }
    
    /* Animated background overlay */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 107, 107, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 20%, rgba(72, 219, 251, 0.1) 0%, transparent 50%);
        pointer-events: none;
        animation: float 20s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    /* Smooth fade-in animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(120, 119, 198, 0.4); }
        50% { box-shadow: 0 0 40px rgba(120, 119, 198, 0.6); }
    }
    
    .fade-in { animation: fadeInUp 0.8s ease-out; }
    
    /* Typography */
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #7877c6 50%, #48dbfb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -2px;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        color: #a0a0b0;
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out;
    }
    
    /* Premium glass-morphism cards */
    .glass-card {
        background: rgba(26, 26, 46, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        margin: 2rem 0;
        animation: fadeInUp 0.8s ease-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
        transition: left 0.5s;
    }
    
    .glass-card:hover::before {
        left: 100%;
    }
    
    /* Premium buttons with gradient and glow */
    .stButton > button {
        background: linear-gradient(135deg, #7877c6 0%, #48dbfb 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 3rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 8px 24px rgba(120, 119, 198, 0.4);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(120, 119, 198, 0.6);
    }
    
    /* Stylish inputs */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(120, 119, 198, 0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        color: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #7877c6;
        box-shadow: 0 0 20px rgba(120, 119, 198, 0.4);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div, .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(120, 119, 198, 0.3);
        border-radius: 12px;
        color: white;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(26, 26, 46, 0.5);
        padding: 12px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        color: #a0a0b0;
        background: transparent;
        border: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(120, 119, 198, 0.3), rgba(72, 219, 251, 0.3));
        color: white;
        border: 2px solid rgba(120, 119, 198, 0.5);
        box-shadow: 0 4px 16px rgba(120, 119, 198, 0.3);
    }
    
    /* Metrics with glow effect */
    .stMetric {
        background: rgba(120, 119, 198, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(120, 119, 198, 0.3);
        animation: fadeIn 0.6s ease-out;
    }
    
    .stMetric:hover {
        background: rgba(120, 119, 198, 0.2);
        border-color: rgba(120, 119, 198, 0.5);
        transform: scale(1.02);
    }
    
    /* Dataframe dark theme */
    .dataframe {
        background: rgba(10, 10, 10, 0.6) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(120, 119, 198, 0.2) !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(72, 219, 155, 0.2);
        border: 1px solid rgba(72, 219, 155, 0.5);
        border-radius: 12px;
        color: #48db9b;
        animation: fadeIn 0.5s ease-out;
    }
    
    .stError {
        background: rgba(255, 107, 107, 0.2);
        border: 1px solid rgba(255, 107, 107, 0.5);
        border-radius: 12px;
        color: #ff6b6b;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Loading spinner */
    .stSpinner > div {
        border-color: #7877c6 transparent transparent transparent !important;
    }
    
    /* Filter badges */
    .filter-badge {
        display: inline-block;
        background: linear-gradient(135deg, #7877c6, #48dbfb);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        animation: slideInRight 0.4s ease-out;
        box-shadow: 0 4px 12px rgba(120, 119, 198, 0.3);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(120, 119, 198, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(120, 119, 198, 0.3);
        color: white;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(120, 119, 198, 0.2);
        border-color: rgba(120, 119, 198, 0.5);
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7877c6, #48dbfb);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #48dbfb, #7877c6);
    }
    
    /* Status indicator */
    .status-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #48db9b;
        margin-right: 8px;
        animation: glow 2s ease-in-out infinite;
    }
    
    /* Info cards for stats */
    .stat-card {
        background: rgba(120, 119, 198, 0.1);
        border: 2px solid rgba(120, 119, 198, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .stat-card:hover {
        background: rgba(120, 119, 198, 0.2);
        border-color: rgba(120, 119, 198, 0.5);
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(120, 119, 198, 0.3);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #7877c6, #48dbfb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #a0a0b0;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: rgba(26, 26, 46, 0.5);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(120, 119, 198, 0.3);
    }
    
    /* Code/monospace text */
    code {
        font-family: 'JetBrains Mono', monospace;
        background: rgba(120, 119, 198, 0.2);
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        color: #48dbfb;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None
if 'excel_data' not in st.session_state:
    st.session_state.excel_data = None
if 'filters_config' not in st.session_state:
    st.session_state.filters_config = {}
if 'stage' not in st.session_state:
    st.session_state.stage = 'login'
if 'active_filters' not in st.session_state:
    st.session_state.active_filters = {}
if 'data_insights' not in st.session_state:
    st.session_state.data_insights = {}
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

def authenticate(email):
    """Authenticate user with @ey.com email"""
    return email.strip().lower().endswith('@in.ey.com')

def get_excel_files():
    """Get all Excel files in the current directory"""
    excel_files = []
    for file in Path('.').glob('*.xlsx'):
        if not file.name.startswith('~'):
            excel_files.append(file.name)
    return sorted(excel_files)

def load_excel_file(filename):
    """Load Excel file with all sheets"""
    try:
        excel_file = pd.ExcelFile(filename)
        data = {}
        for sheet_name in excel_file.sheet_names:
            data[sheet_name] = pd.read_excel(filename, sheet_name=sheet_name)
        return data
    except Exception as e:
        st.error(f"⚠️ Error loading file: {str(e)}")
        return None

def calculate_insights(data):
    """Calculate data insights for visualization"""
    insights = {}
    for sheet_name, df in data.items():
        insights[sheet_name] = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'numeric_columns': len(df.select_dtypes(include=['number']).columns),
            'text_columns': len(df.select_dtypes(include=['object']).columns),
            'missing_values': df.isnull().sum().sum(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        }
    return insights

def create_overview_chart(insights):
    """Create an overview visualization of all sheets"""
    sheet_names = list(insights.keys())
    rows = [insights[sheet]['total_rows'] for sheet in sheet_names]
    cols = [insights[sheet]['total_columns'] for sheet in sheet_names]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Rows',
        x=sheet_names,
        y=rows,
        marker=dict(
            color='rgba(120, 119, 198, 0.7)',
            line=dict(color='rgba(120, 119, 198, 1)', width=2)
        )
    ))
    
    fig.add_trace(go.Bar(
        name='Columns',
        x=sheet_names,
        y=cols,
        marker=dict(
            color='rgba(72, 219, 251, 0.7)',
            line=dict(color='rgba(72, 219, 251, 1)', width=2)
        )
    ))
    
    fig.update_layout(
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Space Grotesk', size=12, color='white'),
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def apply_filter(df, column, filter_values):
    """Apply filter to dataframe"""
    if filter_values and len(filter_values) > 0:
        return df[df[column].isin(filter_values)]
    return df

# ============================================================================
# LOGIN PAGE
# ============================================================================
if not st.session_state.authenticated:
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        st.markdown("<h1 class='main-title'>🔬 Research Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Next-generation data exploration platform</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        email = st.text_input(
            "Email Address",
            placeholder="your.name@in.ey.com",
            key="email_input",
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 ACCESS PORTAL", use_container_width=True):
            if authenticate(email):
                st.session_state.authenticated = True
                st.session_state.user_email = email
                st.session_state.stage = 'file_selection'
                st.success(f"✨ Welcome aboard, {email.split('@')[0]}!")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("⚠️ Access denied. Please use your @in.ey.com email address.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Status indicator
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align: center; color: #a0a0b0;'>"
            "<span class='status-dot'></span>All systems operational"
            "</div>",
            unsafe_allow_html=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FILE SELECTION PAGE
# ============================================================================
elif st.session_state.stage == 'file_selection':
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    # Header with user info
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 class='main-title'>📚 Research Library</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Select your dataset to begin exploration</p>", unsafe_allow_html=True)
    with col2:
        if st.session_state.user_email:
            st.markdown(
                f"<div style='text-align: right; color: #48dbfb; margin-top: 2rem;'>"
                f"👤 {st.session_state.user_email.split('@')[0]}"
                f"</div>",
                unsafe_allow_html=True
            )
    
    excel_files = get_excel_files()
    
    if not excel_files:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.warning("⚠️ No Excel files found in the repository.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # File stats
        st.markdown(f"<div class='stat-label'>AVAILABLE DATASETS</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='stat-number'>{len(excel_files)}</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        selected_file = st.selectbox(
            "Choose your research file",
            excel_files,
            key="file_selector"
        )
        
        # Show file info
        if selected_file:
            file_path = Path(selected_file)
            file_size = file_path.stat().st_size / 1024 / 1024  # MB
            file_modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f"<div class='stat-card'>"
                    f"<div style='color: #a0a0b0; font-size: 0.9rem;'>FILE SIZE</div>"
                    f"<div style='color: white; font-size: 1.5rem; font-weight: 600; margin-top: 0.5rem;'>"
                    f"{file_size:.2f} MB</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    f"<div class='stat-card'>"
                    f"<div style='color: #a0a0b0; font-size: 0.9rem;'>LAST MODIFIED</div>"
                    f"<div style='color: white; font-size: 1.5rem; font-weight: 600; margin-top: 0.5rem;'>"
                    f"{file_modified.strftime('%d %b')}</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    f"<div class='stat-card'>"
                    f"<div style='color: #a0a0b0; font-size: 0.9rem;'>FORMAT</div>"
                    f"<div style='color: white; font-size: 1.5rem; font-weight: 600; margin-top: 0.5rem;'>"
                    f"XLSX</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("🔍 EXPLORE DATA", use_container_width=True):
                st.session_state.selected_file = selected_file
                st.session_state.stage = 'filter_setup'
                time.sleep(0.3)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FILTER SETUP PAGE
# ============================================================================
elif st.session_state.stage == 'filter_setup':
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-title'>⚙️ Configure Filters</h1>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='subtitle'>Customizing view for: <code>{st.session_state.selected_file}</code></p>",
        unsafe_allow_html=True
    )
    
    # Load Excel data
    if st.session_state.excel_data is None:
        with st.spinner("🔄 Loading data..."):
            st.session_state.excel_data = load_excel_file(st.session_state.selected_file)
            if st.session_state.excel_data:
                st.session_state.data_insights = calculate_insights(st.session_state.excel_data)
    
    if st.session_state.excel_data:
        # Show data overview
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        st.markdown("### 📊 Data Overview")
        
        # Create visualization
        fig = create_overview_chart(st.session_state.data_insights)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary stats
        total_rows = sum(insight['total_rows'] for insight in st.session_state.data_insights.values())
        total_sheets = len(st.session_state.excel_data)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{total_sheets}</div>"
                f"<div class='stat-label'>Sheets</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{total_rows:,}</div>"
                f"<div class='stat-label'>Total Rows</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col3:
            total_cols = sum(insight['total_columns'] for insight in st.session_state.data_insights.values())
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{total_cols}</div>"
                f"<div class='stat-label'>Total Columns</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        with col4:
            total_memory = sum(insight['memory_usage'] for insight in st.session_state.data_insights.values())
            st.markdown(
                f"<div class='stat-card'>"
                f"<div class='stat-number'>{total_memory:.1f}</div>"
                f"<div class='stat-label'>MB in Memory</div>"
                f"</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filter configuration
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        st.markdown("### 🎯 Filter Configuration")
        
        apply_filters = st.radio(
            "Would you like to apply filters to the data?",
            ["No filters - show all data", "Yes - configure custom filters"],
            key="filter_choice"
        )
        
        if apply_filters == "Yes - configure custom filters":
            st.markdown("<br>", unsafe_allow_html=True)
            
            filters_config = {}
            
            for sheet_name, df in st.session_state.excel_data.items():
                with st.expander(f"📄 {sheet_name} ({len(df)} rows)", expanded=False):
                    columns = df.columns.tolist()
                    selected_columns = st.multiselect(
                        f"Select filter columns for {sheet_name}",
                        columns,
                        key=f"filter_{sheet_name}"
                    )
                    if selected_columns:
                        filters_config[sheet_name] = selected_columns
            
            st.session_state.filters_config = filters_config
        else:
            st.session_state.filters_config = {}
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("📈 VIEW DATA", use_container_width=True):
                st.session_state.stage = 'data_view'
                time.sleep(0.3)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# DATA VIEW PAGE
# ============================================================================
elif st.session_state.stage == 'data_view':
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    # Header with navigation
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("<h1 class='main-title'>📊 Data Explorer</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subtitle'><code>{st.session_state.selected_file}</code></p>", unsafe_allow_html=True)
    with col2:
        if st.button("◀ Back", use_container_width=True):
            st.session_state.stage = 'file_selection'
            st.session_state.selected_file = None
            st.session_state.excel_data = None
            st.session_state.filters_config = {}
            st.session_state.active_filters = {}
            st.session_state.data_insights = {}
            st.rerun()
    
    if st.session_state.excel_data:
        sheet_names = list(st.session_state.excel_data.keys())
        
        # Create tabs for sheets
        tabs = st.tabs([f"📄 {name}" for name in sheet_names])
        
        for idx, (tab, sheet_name) in enumerate(zip(tabs, sheet_names)):
            with tab:
                df = st.session_state.excel_data[sheet_name].copy()
                original_count = len(df)
                
                # Show filters for this sheet if configured
                if sheet_name in st.session_state.filters_config:
                    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                    st.markdown("### 🔍 Active Filters")
                    
                    filter_columns = st.session_state.filters_config[sheet_name]
                    
                    # Initialize active filters for this sheet if not exists
                    if sheet_name not in st.session_state.active_filters:
                        st.session_state.active_filters[sheet_name] = {}
                    
                    # Create filter columns
                    num_filters = len(filter_columns)
                    filter_cols = st.columns(min(num_filters, 3))
                    
                    for col_idx, filter_col in enumerate(filter_columns):
                        with filter_cols[col_idx % 3]:
                            unique_values = df[filter_col].dropna().unique().tolist()
                            
                            selected_values = st.multiselect(
                                filter_col,
                                unique_values,
                                key=f"active_filter_{sheet_name}_{filter_col}",
                                default=st.session_state.active_filters[sheet_name].get(filter_col, [])
                            )
                            
                            st.session_state.active_filters[sheet_name][filter_col] = selected_values
                            
                            # Apply filter
                            if selected_values:
                                df = apply_filter(df, filter_col, selected_values)
                    
                    # Clear filters button
                    if any(st.session_state.active_filters[sheet_name].values()):
                        if st.button("🔄 Clear All Filters", key=f"clear_{sheet_name}"):
                            st.session_state.active_filters[sheet_name] = {}
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # Data statistics card
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(
                        f"<div class='stat-card'>"
                        f"<div class='stat-number'>{len(df):,}</div>"
                        f"<div class='stat-label'>Rows Displayed</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    filtered_pct = (len(df) / original_count * 100) if original_count > 0 else 0
                    st.markdown(
                        f"<div class='stat-card'>"
                        f"<div class='stat-number'>{filtered_pct:.1f}%</div>"
                        f"<div class='stat-label'>Data Shown</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                with col3:
                    active_filter_count = sum(
                        1 for filters in st.session_state.active_filters.get(sheet_name, {}).values() 
                        if filters
                    )
                    st.markdown(
                        f"<div class='stat-card'>"
                        f"<div class='stat-number'>{active_filter_count}</div>"
                        f"<div class='stat-label'>Active Filters</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                with col4:
                    st.markdown(
                        f"<div class='stat-card'>"
                        f"<div class='stat-number'>{len(df.columns)}</div>"
                        f"<div class='stat-label'>Columns</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Quick insights
                if len(df) > 0:
                    st.markdown("### 📈 Quick Insights")
                    
                    # Find numeric columns for insights
                    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                    
                    if numeric_cols:
                        insight_cols = st.columns(min(len(numeric_cols), 4))
                        
                        for i, col in enumerate(numeric_cols[:4]):
                            with insight_cols[i]:
                                avg_val = df[col].mean()
                                st.markdown(
                                    f"<div style='background: rgba(120, 119, 198, 0.1); "
                                    f"padding: 1rem; border-radius: 12px; "
                                    f"border: 1px solid rgba(120, 119, 198, 0.3);'>"
                                    f"<div style='color: #a0a0b0; font-size: 0.8rem;'>{col}</div>"
                                    f"<div style='color: white; font-size: 1.3rem; font-weight: 600; margin-top: 0.5rem;'>"
                                    f"{avg_val:,.2f}</div>"
                                    f"<div style='color: #48dbfb; font-size: 0.8rem;'>Average</div>"
                                    f"</div>",
                                    unsafe_allow_html=True
                                )
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        # Create a simple chart for the first numeric column
                        if len(numeric_cols) > 0:
                            chart_col = numeric_cols[0]
                            
                            # Create distribution chart
                            fig = go.Figure()
                            
                            fig.add_trace(go.Histogram(
                                x=df[chart_col],
                                marker=dict(
                                    color='rgba(120, 119, 198, 0.7)',
                                    line=dict(color='rgba(120, 119, 198, 1)', width=1)
                                ),
                                name=chart_col
                            ))
                            
                            fig.update_layout(
                                title=f"Distribution of {chart_col}",
                                template='plotly_dark',
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(family='Space Grotesk', size=12, color='white'),
                                height=300,
                                margin=dict(l=40, r=40, t=60, b=40),
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Data table
                st.markdown("### 📋 Data Table")
                
                # Search functionality
                search_term = st.text_input(
                    "🔍 Search in table",
                    key=f"search_{sheet_name}",
                    placeholder="Type to search..."
                )
                
                if search_term:
                    # Search across all columns
                    mask = df.astype(str).apply(
                        lambda x: x.str.contains(search_term, case=False, na=False)
                    ).any(axis=1)
                    df = df[mask]
                    st.info(f"Found {len(df)} matching rows")
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=500
                )
                
                # Download button
                st.markdown("<br>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 2])
                with col2:
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Filtered Data",
                        data=csv,
                        file_name=f"{sheet_name}_filtered.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer with timestamp
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='text-align: center; color: #7C7C8C; font-size: 0.85rem;'>"
        f"Last updated: {datetime.now().strftime('%d %B %Y, %H:%M:%S')} | "
        f"<span class='status-dot'></span>Session active"
        f"</div>",
        unsafe_allow_html=True
    )

