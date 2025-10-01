import streamlit as st
import pandas as pd
import os
from pathlib import Path
import time

# Page configuration
st.set_page_config(
    page_title="Research Portal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalistic design with animations
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
        padding: 2rem;
    }
    
    /* Fade in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: #2E2E38;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        animation: fadeIn 0.8s ease-out;
    }
    
    .subtitle {
        font-size: 1rem;
        font-weight: 400;
        color: #7C7C8C;
        margin-bottom: 3rem;
        animation: fadeIn 1s ease-out;
    }
    
    /* Card styling */
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02), 0 12px 24px rgba(0, 0, 0, 0.03);
        margin: 2rem 0;
        animation: fadeIn 0.8s ease-out;
        border: 1px solid rgba(0, 0, 0, 0.03);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #2E2E38 0%, #1a1a24 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(46, 46, 56, 0.15);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 46, 56, 0.25);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1.5px solid #E8E8ED;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2E2E38;
        box-shadow: 0 0 0 3px rgba(46, 46, 56, 0.1);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        border-radius: 8px;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 8px !important;
        overflow: hidden;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        color: #7C7C8C;
        background-color: transparent;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #2E2E38;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Success/Error message styling */
    .stSuccess, .stError {
        border-radius: 8px;
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #E8E8ED, transparent);
        margin: 2rem 0;
    }
    
    /* Filter badge */
    .filter-badge {
        display: inline-block;
        background: #2E2E38;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
        animation: fadeIn 0.4s ease-out;
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

def authenticate(email):
    """Authenticate user with @ey.com email"""
    return email.strip().lower().endswith('@ey.com')

def get_excel_files():
    """Get all Excel files in the current directory"""
    excel_files = []
    for file in Path('.').glob('*.xlsx'):
        if not file.name.startswith('~'):  # Exclude temporary files
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
        st.error(f"Error loading file: {str(e)}")
        return None

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
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        st.markdown("<h1 class='main-title'>Research Portal</h1>", unsafe_allow_html=True)
        st.markdown("<p class='subtitle'>Secure access to research insights</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        email = st.text_input(
            "Email Address",
            placeholder="your.name@ey.com",
            key="email_input"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Access Portal", use_container_width=True):
            if authenticate(email):
                st.session_state.authenticated = True
                st.session_state.stage = 'file_selection'
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("⚠️ Access denied. Please use your @ey.com email address.")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# FILE SELECTION PAGE
# ============================================================================
elif st.session_state.stage == 'file_selection':
    st.markdown("<div class='fade-in'>", unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-title'>Select Research</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Choose the research file you want to explore</p>", unsafe_allow_html=True)
    
    excel_files = get_excel_files()
    
    if not excel_files:
        st.warning("⚠️ No Excel files found in the repository.")
    else:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        selected_file = st.selectbox(
            "Available Research Files",
            excel_files,
            key="file_selector"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 3])
        
        with col2:
            if st.button("Continue", use_container_width=True):
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
    
    st.markdown("<h1 class='main-title'>Configure Filters</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>Setting up filters for: {st.session_state.selected_file}</p>", unsafe_allow_html=True)
    
    # Load Excel data
    if st.session_state.excel_data is None:
        with st.spinner("Loading data..."):
            st.session_state.excel_data = load_excel_file(st.session_state.selected_file)
    
    if st.session_state.excel_data:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        
        apply_filters = st.radio(
            "Would you like to apply filters to the data?",
            ["No, show all data", "Yes, configure filters"],
            key="filter_choice"
        )
        
        if apply_filters == "Yes, configure filters":
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Select columns to filter by sheet")
            
            filters_config = {}
            
            for sheet_name, df in st.session_state.excel_data.items():
                with st.expander(f"📄 {sheet_name}", expanded=True):
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
        
        col1, col2, col3 = st.columns([3, 1, 3])
        
        with col2:
            if st.button("Show Data", use_container_width=True):
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
    
    st.markdown("<h1 class='main-title'>Research Data</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subtitle'>{st.session_state.selected_file}</p>", unsafe_allow_html=True)
    
    if st.session_state.excel_data:
        sheet_names = list(st.session_state.excel_data.keys())
        
        # Create tabs for sheets
        tabs = st.tabs(sheet_names)
        
        for idx, (tab, sheet_name) in enumerate(zip(tabs, sheet_names)):
            with tab:
                df = st.session_state.excel_data[sheet_name].copy()
                
                # Show filters for this sheet if configured
                if sheet_name in st.session_state.filters_config:
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    st.markdown("#### 🔍 Active Filters")
                    
                    filter_columns = st.session_state.filters_config[sheet_name]
                    
                    # Initialize active filters for this sheet if not exists
                    if sheet_name not in st.session_state.active_filters:
                        st.session_state.active_filters[sheet_name] = {}
                    
                    filter_cols = st.columns(len(filter_columns))
                    
                    for col_idx, filter_col in enumerate(filter_columns):
                        with filter_cols[col_idx]:
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
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                
                # Display data
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Total Rows", len(df))
                with col2:
                    active_filter_count = sum(
                        1 for filters in st.session_state.active_filters.get(sheet_name, {}).values() 
                        if filters
                    )
                    if active_filter_count > 0:
                        st.markdown(
                            f"<div class='filter-badge'>{active_filter_count} filter(s) active</div>",
                            unsafe_allow_html=True
                        )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    height=500
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Logout button
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← Back to File Selection"):
        st.session_state.stage = 'file_selection'
        st.session_state.selected_file = None
        st.session_state.excel_data = None
        st.session_state.filters_config = {}
        st.session_state.active_filters = {}
        st.rerun()
