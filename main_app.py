import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
import io
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Dashboard Pembangunan Aceh",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Modern Blue Theme CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    .main {
        padding: 0;
        background: linear-gradient(180deg, #f0f9ff 0%, #ffffff 100%);
    }
    
    /* Sidebar Enhanced Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        width: 320px;
    }
    
    section[data-testid="stSidebar"] > div {
        padding: 2rem 1.5rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label {
        color: white !important;
        font-size: 14px !important;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        color: white;
        backdrop-filter: blur(10px);
        border-radius: 10px;
    }
    
    section[data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: white !important;
        font-weight: 500;
    }
    
    /* Sidebar Cards */
    .sidebar-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    }
    
    .sidebar-card h3 {
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .sidebar-card p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        line-height: 1.6;
        margin: 0.5rem 0;
        text-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }
    
    .sidebar-card .info-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    }
    
    .sidebar-card .info-label {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .sidebar-card .info-value {
        color: white;
        font-weight: 700;
        font-size: 0.9rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 10px 40px rgba(30, 64, 175, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 6s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1) rotate(0deg); opacity: 0.5; }
        50% { transform: scale(1.1) rotate(180deg); opacity: 0.8; }
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        text-align: center;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .main-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 2;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e40af, #3b82f6, #60a5fa);
        border-radius: 20px 20px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(30, 64, 175, 0.2);
        border-color: #3b82f6;
    }
    
    .metric-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6, #1e40af);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(30, 64, 175, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin: 0.5rem 0;
        font-family: 'Inter', sans-serif;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        line-height: 1.4;
    }
    
    .metric-change {
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.75rem;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        display: inline-block;
    }
    
    .positive {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #166534;
    }
    
    .negative {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #991b1b;
    }
    
    /* Sector Grid */
    .sector-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .sector-card {
        background: white;
        border-radius: 24px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 2px solid #e2e8f0;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
    }
    
    .sector-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #1e40af, #3b82f6, #60a5fa);
        transform: scaleX(0);
        transition: transform 0.4s ease;
    }
    
    .sector-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 60px rgba(30, 64, 175, 0.25);
        border-color: #3b82f6;
    }
    
    .sector-card:hover::before {
        transform: scaleX(1);
    }
    
    .sector-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    
    .sector-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .sector-desc {
        font-size: 1rem;
        color: #64748b;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .sector-status {
        display: inline-block;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-available {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3);
    }
    
    .status-coming {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 2.5rem;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        margin-bottom: 2rem;
        border: 1px solid #e2e8f0;
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #1e40af, #3b82f6, #60a5fa);
        border-radius: 24px 24px 0 0;
    }
    
    .chart-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif;
        text-align: center;
    }
    
    /* Upload Section */
    .upload-section {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        border: 3px dashed #3b82f6;
        border-radius: 24px;
        padding: 4rem;
        text-align: center;
        margin: 3rem 0;
        transition: all 0.3s ease;
    }
    
    .upload-section:hover {
        border-color: #1e40af;
        background: linear-gradient(135deg, #dbeafe, #bfdbfe);
    }
    
    .upload-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        color: #3b82f6;
    }
    
    .upload-title {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif;
    }
    
    .upload-desc {
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af, #3b82f6);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 16px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(30, 64, 175, 0.4);
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        background: rgba(59, 130, 246, 0.1);
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 2rem;
    }
    
    /* Data Tables */
    .stDataFrame > div {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
    }
    
    /* Section Titles */
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin: 4rem 0 2rem 0;
        text-align: center;
        font-family: 'Inter', sans-serif;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 4px;
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_sector' not in st.session_state:
    st.session_state.selected_sector = 'beranda'
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = {}

# Configuration
SECTORS = {
    "beranda": {
        "name": "Beranda",
        "icon": "🏠",
        "description": "Dashboard utama pembangunan Aceh",
        "available": True
    },
    "geografis": {
        "name": "Geografis",
        "icon": "🗺️",
        "description": "Kondisi geografis dan wilayah Aceh",
        "available": True
    },
    "listrik_gas_air": {
        "name": "Listrik, Gas & Air",
        "icon": "⚡",
        "description": "Infrastruktur energi dan utilitas",
        "available": True
    },
    "perdagangan": {
        "name": "Perdagangan",
        "icon": "🛒",
        "description": "Aktivitas perdagangan dan komersial",
        "available": True
    },
    "inflasi_harga": {
        "name": "Inflasi & Harga",
        "icon": "💰",
        "description": "Indeks harga dan tingkat inflasi",
        "available": True
    },
    "neraca_regional": {
        "name": "Neraca Regional",
        "icon": "📊",
        "description": "PDRB dan indikator ekonomi regional",
        "available": True
    },
    "penduduk": {
        "name": "Penduduk",
        "icon": "👥",
        "description": "Demografi dan ketenagakerjaan",
        "available": True
    },
    "sosial": {
        "name": "Sosial",
        "icon": "❤️",
        "description": "Kesehatan dan kesejahteraan",
        "available": True
    },
}

# Load datasets function
@st.cache_data
def load_datasets():
    """Load all available datasets"""
    try:
        datasets = {}
        file_mappings = {
            'pdrb': 'PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv',
            'growth': 'Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv',
            'sector_migas': 'Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv',
            'sector_nonmigas': 'Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv',
            'expenditure': 'Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv',
            'percapita': 'PDRB Per Kapita Aceh 10.6.csv',
            'regional_contrib': 'Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv',
            'percapita_kab': 'PDRB Per Kapita Kabupaten atau Kota 10.8.csv'
        }
        
        for key, filename in file_mappings.items():
            try:
                datasets[key] = pd.read_csv(f'data neraca regional/{filename}', sep=';')
            except:
                pass
        
        return datasets
    except Exception as e:
        st.error(f"Error loading datasets: {e}")
        return {}

def format_number(value, format_type="number"):
    """Format numbers for display"""
    if pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
    except:
        return str(value)
    
    if format_type == "currency":
        if abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}K"
        else:
            return f"{value:.0f}"
    elif format_type == "percentage":
        return f"{value:.2f}%"
    else:
        return f"{value:,.0f}"

def create_metric_card(icon, value, label, change=None, change_type="positive"):
    """Create a metric card HTML"""
    change_html = ""
    if change:
        change_class = "positive" if change_type == "positive" else "negative"
        change_html = f'<div class="metric-change {change_class}">{change}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {change_html}
    </div>
    """

def auto_generate_charts(df, file_name):
    """Auto-generate appropriate charts based on data structure"""
    charts = []
    
    # Detect column types
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Look for common patterns
    year_cols = [col for col in df.columns if 'tahun' in col.lower() or 'year' in col.lower()]
    time_cols = [col for col in df.columns if any(word in col.lower() for word in ['date', 'time', 'periode'])]
    
    # Chart 1: Time series if year column exists
    if year_cols and numeric_cols:
        year_col = year_cols[0]
        for num_col in numeric_cols[:3]:  # Limit to first 3 numeric columns
            try:
                if df[year_col].dtype in ['int64', 'float64'] and df[num_col].dtype in ['int64', 'float64']:
                    fig = px.line(df, x=year_col, y=num_col, 
                                title=f"Trend {num_col} over {year_col}")
                    fig.update_layout(height=400)
                    charts.append(("line", f"Trend {num_col}", fig))
            except:
                continue
    
    # Chart 2: Bar chart for categorical vs numeric
    if categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        try:
            # Get latest data or aggregate
            if len(df) > 50:
                df_sample = df.groupby(cat_col)[num_col].mean().reset_index().head(15)
            else:
                df_sample = df.head(15)
            
            fig = px.bar(df_sample, x=cat_col, y=num_col,
                        title=f"{num_col} by {cat_col}")
            fig.update_layout(height=400, xaxis_tickangle=-45)
            charts.append(("bar", f"{num_col} by {cat_col}", fig))
        except:
            pass
    
    # Chart 3: Distribution chart
    if numeric_cols:
        num_col = numeric_cols[0]
        try:
            fig = px.histogram(df, x=num_col, nbins=20,
                             title=f"Distribution of {num_col}")
            fig.update_layout(height=400)
            charts.append(("histogram", f"Distribution {num_col}", fig))
        except:
            pass
    
    # Chart 4: Correlation heatmap if multiple numeric columns
    if len(numeric_cols) > 2:
        try:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                          title="Correlation Matrix")
            fig.update_layout(height=400)
            charts.append(("heatmap", "Correlation Matrix", fig))
        except:
            pass
    
    return charts

def show_beranda(datasets):
    """Enhanced homepage without highlights section"""
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Dashboard Pembangunan Provinsi Aceh</h1>
        <p class="main-subtitle">Visualisasi Data Pembangunan Multi-Sektor (1958-2014)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    if datasets:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'pdrb' in datasets:
                latest_pdrb = datasets['pdrb'][datasets['pdrb']['tahun'] == datasets['pdrb']['tahun'].max()]
                total_pdrb = latest_pdrb['PDRB ADHB'].sum()
                st.markdown(create_metric_card(
                    "💰", 
                    format_number(total_pdrb, 'currency'),
                    "Total PDRB ADHB (Juta Rupiah)",
                    "Tahun 2013",
                    "positive"
                ), unsafe_allow_html=True)
        
        with col2:
            if 'growth' in datasets:
                avg_growth = datasets['growth']['pertumbuhan ekonomi'].mean()
                st.markdown(create_metric_card(
                    "📈",
                    format_number(avg_growth, 'percentage'),
                    "Rata-rata Pertumbuhan",
                    "Periode 1976-2013",
                    "positive"
                ), unsafe_allow_html=True)
        
        with col3:
            if 'percapita' in datasets:
                latest_pc = datasets['percapita'][datasets['percapita']['tahun'] == datasets['percapita']['tahun'].max()]
                avg_pc = latest_pc['ADHB'].mean()
                st.markdown(create_metric_card(
                    "👥",
                    format_number(avg_pc),
                    "PDRB Per Kapita",
                    "Tahun 2013",
                    "positive"
                ), unsafe_allow_html=True)
        
        with col4:
            if 'regional_contrib' in datasets:
                kab_count = datasets['regional_contrib']['bps_nama_kabupaten_kota'].nunique()
                st.markdown(create_metric_card(
                    "🗺️",
                    str(kab_count),
                    "Kabupaten/Kota",
                    "Wilayah Administratif"
                ), unsafe_allow_html=True)
    
    # Sector Navigation
    st.markdown('<h2 class="section-title">Eksplorasi Sektor Pembangunan</h2>', unsafe_allow_html=True)
    
    # Create sector grid
    st.markdown('<div class="sector-grid">', unsafe_allow_html=True)
    
    cols = st.columns(3)
    sectors_list = [k for k, v in SECTORS.items() if k != 'beranda']
    
    for i, sector_key in enumerate(sectors_list):
        sector = SECTORS[sector_key]
        col_idx = i % 3
        
        with cols[col_idx]:
            status_class = "status-available" if sector["available"] else "status-coming"
            status_text = "✅ Tersedia" if sector["available"] else "🔄 Coming Soon"
            
            st.markdown(f"""
            <div class="sector-card">
                <div class="sector-icon">{sector["icon"]}</div>
                <div class="sector-title">{sector["name"]}</div>
                <div class="sector-desc">{sector["description"]}</div>
                <div class="sector-status {status_class}">{status_text}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if sector["available"]:
                if st.button(f"Buka {sector['name']}", key=f"btn_{sector_key}"):
                    st.session_state.selected_sector = sector_key
                    st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_neraca_regional(datasets):
    """Show Enhanced Neraca Regional dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Neraca Regional Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif PDRB dan Indikator Ekonomi Regional (1975-2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trend Analysis", "🗺️ Regional Analysis", "📋 Data Tables"])
    
    with tab1:
        # Key metrics row
        if 'pdrb' in datasets:
            latest = datasets['pdrb'][datasets['pdrb']['tahun'] == datasets['pdrb']['tahun'].max()]
            migas = latest[latest['migas dan non migas'] == 'Migas']['PDRB ADHB'].iloc[0]
            nonmigas = latest[latest['migas dan non migas'] == 'NonMigas']['PDRB ADHB'].iloc[0]
            total = migas + nonmigas
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(create_metric_card("💰", format_number(total, 'currency'), "Total PDRB ADHB", "Juta Rupiah (2013)"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("⛽", format_number(migas, 'currency'), "PDRB Migas", "Juta Rupiah (2013)"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("🏭", format_number(nonmigas, 'currency'), "PDRB Non-Migas", "Juta Rupiah (2013)"), unsafe_allow_html=True)
            
            with col4:
                ratio = (migas / total) * 100
                st.markdown(create_metric_card("📊", f"{ratio:.1f}%", "Kontribusi Migas", "dari Total PDRB"), unsafe_allow_html=True)
        
        # Main overview charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'pdrb' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Evolusi PDRB ADHB (1975-2013)</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['pdrb'], x='tahun', y='PDRB ADHB', 
                            color='migas dan non migas',
                            color_discrete_map={'Migas': '#1e40af', 'NonMigas': '#3b82f6'},
                            title="",
                            labels={'PDRB ADHB': 'PDRB ADHB (Juta Rupiah)', 'tahun': 'Tahun'})
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                fig.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'pdrb' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 PDRB ADHK (Harga Konstan)</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['pdrb'], x='tahun', y='PDRB ADHK', 
                            color='migas dan non migas',
                            color_discrete_map={'Migas': '#dc2626', 'NonMigas': '#16a34a'},
                            title="",
                            labels={'PDRB ADHK': 'PDRB ADHK (Juta Rupiah)', 'tahun': 'Tahun'})
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                fig.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Growth comparison
        col1, col2 = st.columns(2)
        
        with col1:
            if 'growth' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Pertumbuhan Ekonomi (%)</h3>', unsafe_allow_html=True)
                
                fig = px.bar(datasets['growth'], x='tahun', y='pertumbuhan ekonomi',
                           color='migas dan non migas',
                           color_discrete_map={'Migas': '#1e40af', 'NonMigas': '#3b82f6'},
                           title="",
                           labels={'pertumbuhan ekonomi': 'Pertumbuhan (%)', 'tahun': 'Tahun'})
                fig.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'percapita' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">👥 PDRB Per Kapita</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['percapita'], x='tahun', y='ADHB', 
                            color='migas dan non migas',
                            color_discrete_map={'Migas': '#7c3aed', 'NonMigas': '#059669'},
                            title="",
                            labels={'ADHB': 'PDRB Per Kapita ADHB (Juta Rupiah)', 'tahun': 'Tahun'})
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                fig.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📈 Analisis Tren Komprehensif</h2>', unsafe_allow_html=True)
        
        # Sector contributions with migas
        col1, col2 = st.columns(2)
        
        with col1:
            if 'sector_migas' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🏭 Kontribusi Sektor (Dengan Migas)</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['sector_migas'], x='tahun', y='kontribusi PDRB',
                            color='kelompok sektor dengan migas',
                            title="",
                            labels={'kontribusi PDRB': 'Kontribusi (%)', 'tahun': 'Tahun'})
                fig.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'sector_nonmigas' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🌾 Kontribusi Sektor (Non-Migas)</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['sector_nonmigas'], x='tahun', y='kontribusi PDRB',
                            color='kelompok sektor dengan non migas',
                            title="",
                            labels={'kontribusi PDRB': 'Kontribusi (%)', 'tahun': 'Tahun'})
                fig.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Expenditure analysis
        if 'expenditure' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">💰 Kontribusi PDRB Menurut Kelompok Pengeluaran</h3>', unsafe_allow_html=True)
            
            fig = px.area(datasets['expenditure'], x='tahun', y='kontribusi PDRB',
                        color='kelompok pengeluaran',
                        title="",
                        labels={'kontribusi PDRB': 'Kontribusi (%)', 'tahun': 'Tahun'})
            fig.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Comparative trend analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if 'pdrb' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">⚖️ Rasio PDRB ADHB vs ADHK</h3>', unsafe_allow_html=True)
                
                df_ratio = datasets['pdrb'].copy()
                df_ratio['ratio'] = df_ratio['PDRB ADHB'] / df_ratio['PDRB ADHK']
                
                fig = px.line(df_ratio, x='tahun', y='ratio',
                            color='migas dan non migas',
                            color_discrete_map={'Migas': '#dc2626', 'NonMigas': '#16a34a'},
                            title="",
                            labels={'ratio': 'Rasio ADHB/ADHK', 'tahun': 'Tahun'})
                fig.update_traces(line=dict(width=3), marker=dict(size=6))
                fig.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'growth' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Volatilitas Pertumbuhan</h3>', unsafe_allow_html=True)
                
                # Calculate rolling average
                df_growth = datasets['growth'].copy()
                df_growth = df_growth.sort_values(['migas dan non migas', 'tahun'])
                df_growth['rolling_avg'] = df_growth.groupby('migas dan non migas')['pertumbuhan ekonomi'].rolling(window=3, center=True).mean().reset_index(0, drop=True)
                
                fig = go.Figure()
                
                for category in df_growth['migas dan non migas'].unique():
                    df_cat = df_growth[df_growth['migas dan non migas'] == category]
                    color = '#1e40af' if category == 'Migas' else '#3b82f6'
                    
                    fig.add_trace(go.Scatter(
                        x=df_cat['tahun'], y=df_cat['pertumbuhan ekonomi'],
                        mode='lines+markers', name=f'{category} (Aktual)',
                        line=dict(color=color, width=2, dash='dot'),
                        opacity=0.6
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=df_cat['tahun'], y=df_cat['rolling_avg'],
                        mode='lines', name=f'{category} (Trend)',
                        line=dict(color=color, width=3)
                    ))
                
                fig.update_layout(height=400, showlegend=True,
                                xaxis_title="Tahun", yaxis_title="Pertumbuhan (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🗺️ Analisis Regional Mendalam</h2>', unsafe_allow_html=True)
        
        if 'regional_contrib' in datasets:
            # Time series selector
            years_available = sorted(datasets['regional_contrib']['tahun'].unique())
            selected_year = st.selectbox("Pilih Tahun untuk Analisis:", years_available, 
                                       index=len(years_available)-1)
            
            regional_data = datasets['regional_contrib'][datasets['regional_contrib']['tahun'] == selected_year]
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown(f'<h3 class="chart-title">🏆 Kontribusi Regional PDRB ({selected_year})</h3>', unsafe_allow_html=True)
                
                # Sort by total contribution
                regional_summary = regional_data.groupby('bps_nama_kabupaten_kota')['kontribusi PDRB'].sum().reset_index()
                regional_summary = regional_summary.sort_values('kontribusi PDRB', ascending=True).tail(15)
                
                fig = px.bar(regional_summary, x='kontribusi PDRB', y='bps_nama_kabupaten_kota',
                           orientation='h',
                           title="",
                           labels={'kontribusi PDRB': 'Kontribusi (%)', 'bps_nama_kabupaten_kota': 'Kabupaten/Kota'},
                           color='kontribusi PDRB',
                           color_continuous_scale='Blues')
                fig.update_layout(height=600, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown(f'<h3 class="chart-title">📊 Top 10 Kontributor ({selected_year})</h3>', unsafe_allow_html=True)
                
                top_contributors = regional_data.groupby('bps_nama_kabupaten_kota')['kontribusi PDRB'].sum().reset_index()
                top_contributors = top_contributors.nlargest(10, 'kontribusi PDRB')
                top_contributors['Ranking'] = range(1, len(top_contributors) + 1)
                
                # Display as formatted table
                for idx, row in top_contributors.iterrows():
                    rank_color = "#1e40af" if row['Ranking'] <= 3 else "#64748b"
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.5rem 0; border-left: 4px solid {rank_color}; background: #f8fafc;">
                        <strong>#{row['Ranking']} {row['bps_nama_kabupaten_kota']}</strong><br>
                        <span style="color: #64748b;">Kontribusi: {row['kontribusi PDRB']:.2f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Regional comparison over time
        if 'regional_contrib' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📈 Evolusi Kontribusi Regional Top 8 Kabupaten/Kota</h3>', unsafe_allow_html=True)
            
            # Get top 8 contributors in latest year
            latest_year = datasets['regional_contrib']['tahun'].max()
            latest_regional = datasets['regional_contrib'][datasets['regional_contrib']['tahun'] == latest_year]
            top_8 = latest_regional.groupby('bps_nama_kabupaten_kota')['kontribusi PDRB'].sum().nlargest(8).index
            
            regional_evolution = datasets['regional_contrib'][
                datasets['regional_contrib']['bps_nama_kabupaten_kota'].isin(top_8)
            ].groupby(['tahun', 'bps_nama_kabupaten_kota'])['kontribusi PDRB'].sum().reset_index()
            
            fig = px.line(regional_evolution, x='tahun', y='kontribusi PDRB',
                        color='bps_nama_kabupaten_kota',
                        title="",
                        labels={'kontribusi PDRB': 'Kontribusi (%)', 'tahun': 'Tahun'})
            fig.update_traces(line=dict(width=3), marker=dict(size=6))
            fig.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Per capita regional analysis
        if 'percapita_kab' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">💰 PDRB Per Kapita Regional (Top 10)</h3>', unsafe_allow_html=True)
            
            latest_pc = datasets['percapita_kab'][datasets['percapita_kab']['tahun'] == datasets['percapita_kab']['tahun'].max()]
            top_pc = latest_pc.nlargest(10, 'kontribusi PDRB')
            
            fig = px.bar(top_pc, x='bps_nama_kabupaten_kota', y='kontribusi PDRB',
                       color='migas dan non migas',
                       color_discrete_map={'Migas': '#1e40af', 'NonMigas': '#3b82f6'},
                       title="",
                       labels={'kontribusi PDRB': 'PDRB Per Kapita (Juta Rupiah)', 'bps_nama_kabupaten_kota': 'Kabupaten/Kota'})
            fig.update_layout(height=500, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📋 Data Tables & Export</h2>', unsafe_allow_html=True)
        
        # Dataset selector
        dataset_options = {
            "PDRB ADHB & ADHK": "pdrb",
            "Pertumbuhan Ekonomi": "growth", 
            "Sektor dengan Migas": "sector_migas",
            "Sektor Non-Migas": "sector_nonmigas",
            "Kelompok Pengeluaran": "expenditure",
            "Per Kapita Provinsi": "percapita",
            "Kontribusi Regional": "regional_contrib",
            "Per Kapita Regional": "percapita_kab"
        }
        
        selected_dataset = st.selectbox("Pilih Dataset untuk Ditampilkan:", 
                                      list(dataset_options.keys()))
        
        dataset_key = dataset_options[selected_dataset]
        
        if dataset_key in datasets:
            df = datasets[dataset_key]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"#### 📊 {selected_dataset}")
                st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
            
            with col2:
                # Download button
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"aceh_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                # Filter option
                show_filtered = st.checkbox("Filter Data", value=False)
            
            # Display data
            if show_filtered and 'tahun' in df.columns:
                year_range = st.slider("Pilih Range Tahun:", 
                                     int(df['tahun'].min()), 
                                     int(df['tahun'].max()),
                                     (int(df['tahun'].min()), int(df['tahun'].max())))
                filtered_df = df[(df['tahun'] >= year_range[0]) & (df['tahun'] <= year_range[1])]
                st.dataframe(filtered_df, use_container_width=True, height=400)
            else:
                st.dataframe(df, use_container_width=True, height=400)
        
        else:
            st.error(f"Dataset '{selected_dataset}' tidak tersedia.")

def show_geografis(datasets):
    """Enhanced Geographical Sector dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🗺️ Sektor Geografis Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Kondisi Geografis, Administratif, dan Klimatologi (2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load geographical datasets
    geo_datasets = load_geographical_data()
    
    # Tabs for different geographical views
    tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Administratif", "🌍 Penggunaan Lahan", "🌡️ Klimatologi", "📊 Data & Analisis"])
    
    with tab1:
        show_administrative_analysis(geo_datasets)
    
    with tab2:
        show_land_use_analysis(geo_datasets)
    
    with tab3:
        show_climate_analysis(geo_datasets)
    
    with tab4:
        show_geographical_data_tables(geo_datasets)

@st.cache_data
def load_geographical_data():
    """Load geographical datasets from the provided data"""
    datasets = {}
    
    # Administrative data
    admin_data = [
        ["Simeulue", "Sinabang", 10, 29, 138],
        ["Aceh Singkil", "Singkil", 11, 16, 116],
        ["Aceh Selatan", "Tapaktuan", 18, 43, 260],
        ["Aceh Tenggara", "Kutacane", 16, 51, 385],
        ["Aceh Timur", "Idi", 24, 53, 511],
        ["Aceh Tengah", "Takengon", 14, 18, 295],
        ["Aceh Barat", "Meulaboh", 12, 32, 322],
        ["Aceh Besar", "Kota Jantho", 23, 68, 604],
        ["Pidie", "Sigli", 23, 94, 727],
        ["Bireuen", "Bireuen", 17, 75, 609],
        ["Aceh Utara", "Lhoksukon", 27, 67, 852],
        ["Aceh Barat Daya", "Blangpidie", 9, 20, 132],
        ["Gayo Lues", "Blangkejeren", 11, 25, 136],
        ["Aceh Tamiang", "Karang Baru", 12, 27, 213],
        ["Nagan Raya", "Suka Makmue", 10, 30, 222],
        ["Aceh Jaya", "Calang", 9, 21, 172],
        ["Bener Meriah", "Simpang Tiga Redelong", 10, 11, 232],
        ["Pidie Jaya", "Meureudu", 8, 34, 222],
        ["Banda Aceh", "Banda Aceh", 9, 17, 90],
        ["Sabang", "Sabang", 2, 7, 18],
        ["Langsa", "Langsa", 5, 6, 66],
        ["Lhokseumawe", "Lhokseumawe", 4, 9, 68],
        ["Subulussalam", "Subulussalam", 5, 8, 74]
    ]
    
    datasets['administrative'] = pd.DataFrame(admin_data, columns=['Kabupaten_Kota', 'Ibukota', 'Kecamatan', 'Mukim', 'Gampong'])
    
    # Land use data
    land_use_data = [
        ["Perkampungan", 125439, 2.21],
        ["Industri", 3928, 0.07],
        ["Pertambangan", 198000, 3.49],
        ["Persawahan", 397512, 7.00],
        ["Pertanian tanah kering semusim", 139049, 2.45],
        ["Kebun", 305624, 5.38],
        ["Perkebunan besar", 200680, 3.53],
        ["Perkebunan rakyat", 800401, 14.10],
        ["Padang rumput alang-alang semak", 232023, 4.09],
        ["Hutan (lebat belukar sejenis)", 2270080, 39.99],
        ["Perairan Darat", 206741, 3.64],
        ["Tanah Terbuka Tandus Rusak", 8433, 0.15],
        ["Lainnya", 789171, 13.90]
    ]
    
    datasets['land_use'] = pd.DataFrame(land_use_data, columns=['Penggunaan', 'Luas_Ha', 'Persentase'])
    
    # Climate data
    climate_data = [
        ["Januari", 23.1, 283.3, 84],
        ["Februari", 23.0, 136.1, 84],
        ["Maret", 23.2, 89.7, 83],
        ["April", 23.5, 106.2, 83],
        ["Mei", 23.3, 131.1, 81],
        ["Juni", 23.3, 167.2, 74],
        ["Juli", 22.3, 83.8, 73],
        ["Agustus", 22.2, 40.4, 77],
        ["September", 22.0, 164.6, 74],
        ["Oktober", 22.3, 56.6, 82],
        ["November", 22.2, 149.8, 86],
        ["Desember", 22.8, 214.8, 87]
    ]
    
    datasets['climate'] = pd.DataFrame(climate_data, columns=['Bulan', 'Suhu_Celsius', 'Curah_Hujan_mm', 'Kelembaban_Persen'])
    
    # Population data
    population_data = [
        ["Simeulue", 20145, 41744, 41429, 83173, 46],
        ["Aceh Singkil", 24903, 56987, 53719, 110706, 60],
        ["Aceh Selatan", 48970, 107131, 102940, 210071, 50],
        ["Aceh Tenggara", 43747, 95646, 90437, 186083, 45],
        ["Aceh Timur", 87994, 200875, 192260, 393135, 72],
        ["Aceh Tengah", 46900, 94711, 91022, 185733, 42],
        ["Aceh Barat", 46247, 95983, 91476, 187459, 68],
        ["Aceh Besar", 87793, 195269, 188208, 383477, 132],
        ["Pidie", 99656, 199198, 199248, 398446, 126],
        ["Bireuen", 95779, 208956, 204861, 413817, 230],
        ["Aceh Utara", 130035, 279122, 277434, 556556, 207],
        ["Aceh Barat Daya", 30335, 67942, 65249, 131191, 71],
        ["Gayo Lues", 20827, 43551, 40960, 84511, 15],
        ["Aceh Tamiang", 62929, 136729, 127691, 264420, 125],
        ["Nagan Raya", 38178, 76662, 72934, 149596, 42],
        ["Aceh Jaya", 22660, 43715, 42193, 85908, 22],
        ["Bener Meriah", 33935, 66775, 65224, 131999, 69],
        ["Pidie Jaya", 36194, 71250, 69519, 140769, 148],
        ["Banda Aceh", 60033, 123106, 126176, 249282, 4451],
        ["Sabang", 8355, 16469, 15722, 32191, 264],
        ["Langsa", 35027, 79187, 77824, 157011, 773],
        ["Lhokseumawe", 41188, 91212, 90764, 181976, 1189],
        ["Subulussalam", 15469, 37441, 34973, 71414, 62]
    ]
    
    datasets['population'] = pd.DataFrame(population_data, 
                                        columns=['Kabupaten_Kota', 'Rumah_Tangga', 'Penduduk_Laki', 
                                               'Penduduk_Perempuan', 'Total_Penduduk', 'Kepadatan_per_km2'])
    
    return datasets

def show_administrative_analysis(datasets):
    """Show administrative division analysis"""
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🏛️ Analisis Pembagian Administratif</h2>', unsafe_allow_html=True)
    
    if 'administrative' in datasets and 'population' in datasets:
        admin_df = datasets['administrative']
        pop_df = datasets['population']
        
        # Key metrics
        total_kabkota = len(admin_df)
        total_kecamatan = admin_df['Kecamatan'].sum()
        total_mukim = admin_df['Mukim'].sum()
        total_gampong = admin_df['Gampong'].sum()
        total_population = pop_df['Total_Penduduk'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("🏛️", str(total_kabkota), "Kabupaten/Kota", "Wilayah Administratif"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("🏢", str(total_kecamatan), "Total Kecamatan", f"Rata-rata: {total_kecamatan/total_kabkota:.1f}"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("🏘️", str(total_mukim), "Total Mukim", f"Rata-rata: {total_mukim/total_kabkota:.1f}"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_metric_card("🏠", str(total_gampong), "Total Gampong/Desa", f"Rata-rata: {total_gampong/total_kabkota:.1f}"), unsafe_allow_html=True)
        
        # Administrative structure comparison
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📊 Jumlah Kecamatan per Kabupaten/Kota</h3>', unsafe_allow_html=True)
            
            # Sort by kecamatan count
            admin_sorted = admin_df.sort_values('Kecamatan', ascending=True).tail(15)
            
            fig = px.bar(admin_sorted, x='Kecamatan', y='Kabupaten_Kota',
                        orientation='h',
                        color='Kecamatan',
                        color_continuous_scale='Blues',
                        title="")
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🏘️ Struktur Mukim dan Gampong</h3>', unsafe_allow_html=True)
            
            # Create stacked bar for top 12 kabupaten
            top_admin = admin_df.nlargest(12, 'Gampong')
            
            fig = go.Figure()
            fig.add_trace(go.Bar(name='Mukim', x=top_admin['Kabupaten_Kota'], y=top_admin['Mukim'], 
                               marker_color='#3b82f6'))
            fig.add_trace(go.Bar(name='Gampong', x=top_admin['Kabupaten_Kota'], y=top_admin['Gampong'], 
                               marker_color='#1e40af'))
            
            fig.update_layout(barmode='group', height=500,
                            xaxis_title="Kabupaten/Kota", yaxis_title="Jumlah",
                            xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Population density analysis
        if 'population' in datasets:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">👥 Kepadatan Penduduk per Km²</h3>', unsafe_allow_html=True)
                
                # Top 10 most dense areas
                dense_areas = pop_df.nlargest(10, 'Kepadatan_per_km2')
                
                fig = px.bar(dense_areas, x='Kepadatan_per_km2', y='Kabupaten_Kota',
                            orientation='h',
                            color='Kepadatan_per_km2',
                            color_continuous_scale='Reds',
                            title="")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">⚖️ Distribusi Gender Penduduk</h3>', unsafe_allow_html=True)
                
                # Gender distribution for top populated areas
                top_pop = pop_df.nlargest(8, 'Total_Penduduk')
                
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Laki-laki', x=top_pop['Kabupaten_Kota'], y=top_pop['Penduduk_Laki'],
                               marker_color='#3b82f6'))
                fig.add_trace(go.Bar(name='Perempuan', x=top_pop['Kabupaten_Kota'], y=top_pop['Penduduk_Perempuan'],
                               marker_color='#ec4899'))
                
                fig.update_layout(barmode='group', height=400,
                                xaxis_title="Kabupaten/Kota", yaxis_title="Jumlah Penduduk",
                                xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

def show_land_use_analysis(datasets):
    """Show land use analysis"""
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🌍 Analisis Penggunaan Lahan Provinsi Aceh</h2>', unsafe_allow_html=True)
    
    if 'land_use' in datasets:
        land_df = datasets['land_use']
        
        # Key metrics
        total_area = land_df['Luas_Ha'].sum()
        forest_area = land_df[land_df['Penggunaan'] == 'Hutan (lebat belukar sejenis)']['Luas_Ha'].iloc[0]
        agriculture_keywords = ['Persawahan', 'Pertanian tanah kering semusim', 'Kebun', 'Perkebunan besar', 'Perkebunan rakyat']
        agriculture_area = land_df[land_df['Penggunaan'].isin(agriculture_keywords)]['Luas_Ha'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("🌍", format_number(total_area), "Total Luas (Ha)", "Provinsi Aceh"), unsafe_allow_html=True)
        
        with col2:
            forest_pct = (forest_area/total_area) * 100
            st.markdown(create_metric_card("🌲", f"{forest_pct:.1f}%", "Tutupan Hutan", format_number(forest_area) + " Ha"), unsafe_allow_html=True)
        
        with col3:
            agri_pct = (agriculture_area/total_area) * 100
            st.markdown(create_metric_card("🌾", f"{agri_pct:.1f}%", "Lahan Pertanian", format_number(agriculture_area) + " Ha"), unsafe_allow_html=True)
        
        with col4:
            other_area = total_area - forest_area - agriculture_area
            other_pct = (other_area/total_area) * 100
            st.markdown(create_metric_card("🏘️", f"{other_pct:.1f}%", "Penggunaan Lain", format_number(other_area) + " Ha"), unsafe_allow_html=True)
        
        # Land use visualizations
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🥧 Distribusi Penggunaan Lahan</h3>', unsafe_allow_html=True)
            
            # Create pie chart
            fig = px.pie(land_df, values='Luas_Ha', names='Penggunaan',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=600, showlegend=True,
                            legend=dict(orientation="v", yanchor="middle", y=0.5))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📊 Top 10 Penggunaan Lahan</h3>', unsafe_allow_html=True)
            
            # Top land uses
            top_land_use = land_df.nlargest(10, 'Luas_Ha')
            
            fig = px.bar(top_land_use, x='Luas_Ha', y='Penggunaan',
                        orientation='h',
                        color='Persentase',
                        color_continuous_scale='Greens')
            fig.update_layout(height=600, showlegend=False,
                            xaxis_title="Luas (Ha)", yaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed breakdown
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">📈 Persentase Penggunaan Lahan Detail</h3>', unsafe_allow_html=True)
        
        # Sort by percentage
        land_sorted = land_df.sort_values('Persentase', ascending=True)
        
        fig = px.bar(land_sorted, x='Persentase', y='Penggunaan',
                    orientation='h',
                    color='Persentase',
                    color_continuous_scale='Viridis',
                    text='Persentase')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(height=500, showlegend=False,
                        xaxis_title="Persentase (%)", yaxis_title="Jenis Penggunaan")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_climate_analysis(datasets):
    """Show climate analysis"""
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🌡️ Analisis Klimatologi Banda Aceh 2013</h2>', unsafe_allow_html=True)
    
    if 'climate' in datasets:
        climate_df = datasets['climate']
        
        # Calculate key metrics
        avg_temp = climate_df['Suhu_Celsius'].mean()
        max_temp = climate_df['Suhu_Celsius'].max()
        min_temp = climate_df['Suhu_Celsius'].min()
        total_rainfall = climate_df['Curah_Hujan_mm'].sum()
        avg_humidity = climate_df['Kelembaban_Persen'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_metric_card("🌡️", f"{avg_temp:.1f}°C", "Suhu Rata-rata", f"Range: {min_temp:.1f}-{max_temp:.1f}°C"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_metric_card("🌧️", f"{total_rainfall:.0f} mm", "Total Curah Hujan", "Tahun 2013"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_metric_card("💧", f"{avg_humidity:.1f}%", "Kelembaban Rata-rata", "Relatif Tinggi"), unsafe_allow_html=True)
        
        with col4:
            # Find wettest month
            wettest_month = climate_df.loc[climate_df['Curah_Hujan_mm'].idxmax(), 'Bulan']
            wettest_rainfall = climate_df['Curah_Hujan_mm'].max()
            st.markdown(create_metric_card("☔", wettest_month, "Bulan Terbasah", f"{wettest_rainfall:.1f} mm"), unsafe_allow_html=True)
        
        # Climate trends
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🌡️ Tren Suhu Bulanan 2013</h3>', unsafe_allow_html=True)
            
            fig = px.line(climate_df, x='Bulan', y='Suhu_Celsius',
                         markers=True,
                         line_shape='spline')
            fig.update_traces(line=dict(color='#dc2626', width=3), marker=dict(size=8))
            fig.update_layout(height=400,
                            xaxis_title="Bulan", yaxis_title="Suhu (°C)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🌧️ Curah Hujan Bulanan 2013</h3>', unsafe_allow_html=True)
            
            fig = px.bar(climate_df, x='Bulan', y='Curah_Hujan_mm',
                        color='Curah_Hujan_mm',
                        color_continuous_scale='Blues')
            fig.update_layout(height=400, showlegend=False,
                            xaxis_title="Bulan", yaxis_title="Curah Hujan (mm)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Multi-variable analysis
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">📊 Analisis Klimat Multi-Variabel</h3>', unsafe_allow_html=True)
        
        # Create subplot with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add temperature line
        fig.add_trace(
            go.Scatter(x=climate_df['Bulan'], y=climate_df['Suhu_Celsius'],
                      name="Suhu (°C)", line=dict(color='red', width=3)),
            secondary_y=False,
        )
        
        # Add humidity line
        fig.add_trace(
            go.Scatter(x=climate_df['Bulan'], y=climate_df['Kelembaban_Persen'],
                      name="Kelembaban (%)", line=dict(color='blue', width=3)),
            secondary_y=True,
        )
        
        # Add rainfall bars
        fig.add_trace(
            go.Bar(x=climate_df['Bulan'], y=climate_df['Curah_Hujan_mm'],
                  name="Curah Hujan (mm)", opacity=0.6, marker_color='lightblue'),
            secondary_y=False,
        )
        
        # Set x-axis title
        fig.update_xaxes(title_text="Bulan")
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Suhu (°C) / Curah Hujan (mm)", secondary_y=False)
        fig.update_yaxes(title_text="Kelembaban (%)", secondary_y=True)
        
        fig.update_layout(height=500, hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Climate correlation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🔗 Korelasi Suhu vs Kelembaban</h3>', unsafe_allow_html=True)
            
            fig = px.scatter(climate_df, x='Suhu_Celsius', y='Kelembaban_Persen',
                           size='Curah_Hujan_mm', hover_name='Bulan',
                           color='Curah_Hujan_mm', color_continuous_scale='Viridis')
            fig.update_layout(height=400,
                            xaxis_title="Suhu (°C)", yaxis_title="Kelembaban (%)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📈 Pola Musiman Klimat</h3>', unsafe_allow_html=True)
            
            # Normalize data for comparison
            climate_norm = climate_df.copy()
            climate_norm['Suhu_Norm'] = (climate_norm['Suhu_Celsius'] - climate_norm['Suhu_Celsius'].min()) / (climate_norm['Suhu_Celsius'].max() - climate_norm['Suhu_Celsius'].min())
            climate_norm['Hujan_Norm'] = (climate_norm['Curah_Hujan_mm'] - climate_norm['Curah_Hujan_mm'].min()) / (climate_norm['Curah_Hujan_mm'].max() - climate_norm['Curah_Hujan_mm'].min())
            climate_norm['Kelembaban_Norm'] = (climate_norm['Kelembaban_Persen'] - climate_norm['Kelembaban_Persen'].min()) / (climate_norm['Kelembaban_Persen'].max() - climate_norm['Kelembaban_Persen'].min())
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=climate_norm['Bulan'], y=climate_norm['Suhu_Norm'],
                                   mode='lines+markers', name='Suhu (Norm)', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=climate_norm['Bulan'], y=climate_norm['Hujan_Norm'],
                                   mode='lines+markers', name='Curah Hujan (Norm)', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=climate_norm['Bulan'], y=climate_norm['Kelembaban_Norm'],
                                   mode='lines+markers', name='Kelembaban (Norm)', line=dict(color='green')))
            
            fig.update_layout(height=400, yaxis_title="Nilai Ternormalisasi (0-1)",
                            xaxis_title="Bulan")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

def show_geographical_data_tables(datasets):
    """Show geographical data tables with analysis"""
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📊 Data & Analisis Geografis</h2>', unsafe_allow_html=True)
    
    # Dataset selector
    dataset_options = {
        "Pembagian Administratif": "administrative",
        "Penggunaan Lahan": "land_use", 
        "Data Klimatologi": "climate",
        "Data Kependudukan": "population"
    }
    
    selected_dataset = st.selectbox("Pilih Dataset untuk Analisis:", 
                                  list(dataset_options.keys()))
    
    dataset_key = dataset_options[selected_dataset]
    
    if dataset_key in datasets:
        df = datasets[dataset_key]
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"#### 📊 {selected_dataset}")
            st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
        
        with col2:
            # Download button
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, sep=';')
            st.download_button(
                label="💾 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"aceh_geografis_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            show_summary = st.checkbox("Tampilkan Ringkasan", value=True)
        
        # Display data
        st.dataframe(df, use_container_width=True, height=400)
        
        if show_summary:
            st.markdown("### 📈 Analisis & Insights")
            
            if dataset_key == "administrative":
                show_administrative_insights(df, datasets['population'])
            elif dataset_key == "land_use":
                show_land_use_insights(df)
            elif dataset_key == "climate":
                show_climate_insights(df)
            elif dataset_key == "population":
                show_population_insights(df)

def show_administrative_insights(admin_df, pop_df):
    """Show administrative insights"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4>🏛️ Insights Pembagian Administratif</h4>', unsafe_allow_html=True)
    
    # Calculate insights
    total_kab = len(admin_df[admin_df['Kabupaten_Kota'].str.contains('Kabupaten')])
    total_kota = len(admin_df[admin_df['Kabupaten_Kota'].str.contains('Kota')])
    
    # Administrative efficiency metrics
    admin_df['Gampong_per_Kecamatan'] = admin_df['Gampong'] / admin_df['Kecamatan']
    admin_df['Mukim_per_Kecamatan'] = admin_df['Mukim'] / admin_df['Kecamatan']
    
    most_efficient = admin_df.loc[admin_df['Gampong_per_Kecamatan'].idxmax()]
    least_efficient = admin_df.loc[admin_df['Gampong_per_Kecamatan'].idxmin()]
    
    # Merge with population for density analysis
    merged_df = admin_df.merge(pop_df, on='Kabupaten_Kota', how='inner')
    merged_df['Penduduk_per_Gampong'] = merged_df['Total_Penduduk'] / merged_df['Gampong']
    
    insights = [
        f"🏛️ **Struktur Administratif**: {total_kab} Kabupaten dan {total_kota} Kota",
        f"🏢 **Total Kecamatan**: {admin_df['Kecamatan'].sum()} kecamatan dengan rata-rata {admin_df['Kecamatan'].mean():.1f} per kabupaten/kota",
        f"🏘️ **Total Mukim**: {admin_df['Mukim'].sum()} mukim dengan rata-rata {admin_df['Mukim'].mean():.1f} per kabupaten/kota",
        f"🏠 **Total Gampong**: {admin_df['Gampong'].sum()} gampong/desa dengan rata-rata {admin_df['Gampong'].mean():.1f} per kabupaten/kota",
        f"⚡ **Efisiensi Tertinggi**: {most_efficient['Kabupaten_Kota']} ({most_efficient['Gampong_per_Kecamatan']:.1f} gampong per kecamatan)",
        f"📊 **Kepadatan Gampong**: Rata-rata {merged_df['Penduduk_per_Gampong'].mean():.0f} penduduk per gampong",
        f"🎯 **Variasi Ukuran**: Rentang kecamatan dari {admin_df['Kecamatan'].min()} hingga {admin_df['Kecamatan'].max()} per wilayah"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_land_use_insights(land_df):
    """Show land use insights"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4>🌍 Insights Penggunaan Lahan</h4>', unsafe_allow_html=True)
    
    # Calculate key insights
    total_area = land_df['Luas_Ha'].sum()
    forest_pct = land_df[land_df['Penggunaan'] == 'Hutan (lebat belukar sejenis)']['Persentase'].iloc[0]
    
    # Agriculture calculation
    agriculture_uses = ['Persawahan', 'Pertanian tanah kering semusim', 'Kebun', 'Perkebunan besar', 'Perkebunan rakyat']
    total_agri = land_df[land_df['Penggunaan'].isin(agriculture_uses)]['Persentase'].sum()
    
    # Top uses
    top_3_uses = land_df.nlargest(3, 'Persentase')
    conservation_area = forest_pct + land_df[land_df['Penggunaan'] == 'Padang rumput alang-alang semak']['Persentase'].iloc[0]
    
    insights = [
        f"🌲 **Dominasi Hutan**: {forest_pct:.1f}% dari total luas Aceh masih berupa hutan, menunjukkan potensi konservasi yang tinggi",
        f"🌾 **Sektor Pertanian**: {total_agri:.1f}% lahan digunakan untuk berbagai jenis pertanian dan perkebunan",
        f"🏆 **Penggunaan Terbesar**: {top_3_uses.iloc[0]['Penggunaan']} ({top_3_uses.iloc[0]['Persentase']:.1f}%), diikuti {top_3_uses.iloc[1]['Penggunaan']} ({top_3_uses.iloc[1]['Persentase']:.1f}%)",
        f"🌿 **Area Konservasi**: Sekitar {conservation_area:.1f}% lahan berupa hutan dan area alami",
        f"🏭 **Industri & Pertambangan**: {land_df[land_df['Penggunaan']=='Industri']['Persentase'].iloc[0]:.2f}% industri dan {land_df[land_df['Penggunaan']=='Pertambangan']['Persentase'].iloc[0]:.1f}% pertambangan",
        f"🏘️ **Pemukiman**: {land_df[land_df['Penggunaan']=='Perkampungan']['Persentase'].iloc[0]:.1f}% untuk perkampungan dan pemukiman",
        f"💧 **Perairan**: {land_df[land_df['Penggunaan']=='Perairan Darat']['Persentase'].iloc[0]:.1f}% berupa perairan darat (kolam, danau, rawa)",
        f"🌱 **Potensi Pembangunan**: {land_df[land_df['Penggunaan']=='Lainnya']['Persentase'].iloc[0]:.1f}% lahan masih tersedia untuk pengembangan"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_climate_insights(climate_df):
    """Show climate insights"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4>🌡️ Insights Klimatologi</h4>', unsafe_allow_html=True)
    
    # Calculate climate statistics
    avg_temp = climate_df['Suhu_Celsius'].mean()
    temp_range = climate_df['Suhu_Celsius'].max() - climate_df['Suhu_Celsius'].min()
    total_rainfall = climate_df['Curah_Hujan_mm'].sum()
    avg_humidity = climate_df['Kelembaban_Persen'].mean()
    
    # Seasonal analysis
    wet_months = climate_df[climate_df['Curah_Hujan_mm'] > climate_df['Curah_Hujan_mm'].mean()]
    dry_months = climate_df[climate_df['Curah_Hujan_mm'] < climate_df['Curah_Hujan_mm'].mean()]
    
    wettest_month = climate_df.loc[climate_df['Curah_Hujan_mm'].idxmax()]
    driest_month = climate_df.loc[climate_df['Curah_Hujan_mm'].idxmin()]
    
    # Temperature-humidity correlation
    correlation = climate_df['Suhu_Celsius'].corr(climate_df['Kelembaban_Persen'])
    
    insights = [
        f"🌡️ **Stabilitas Suhu**: Suhu rata-rata {avg_temp:.1f}°C dengan variasi rendah ({temp_range:.1f}°C), menunjukkan iklim tropis yang stabil",
        f"🌧️ **Curah Hujan Tinggi**: Total {total_rainfall:.0f}mm per tahun, termasuk kategori iklim tropis basah",
        f"💧 **Kelembaban Tinggi**: Rata-rata {avg_humidity:.1f}%, konsisten dengan iklim tropis lembab",
        f"☔ **Musim Basah**: {wettest_month['Bulan']} adalah bulan terbasah ({wettest_month['Curah_Hujan_mm']:.1f}mm)",
        f"🌞 **Musim Kering**: {driest_month['Bulan']} adalah bulan terkering ({driest_month['Curah_Hujan_mm']:.1f}mm)",
        f"📊 **Pola Musiman**: {len(wet_months)} bulan basah vs {len(dry_months)} bulan relatif kering",
        f"🔗 **Korelasi Iklim**: Korelasi suhu-kelembaban {correlation:.3f} (korelasi negatif lemah)",
        f"🌍 **Klasifikasi Iklim**: Iklim tropis monsun dengan curah hujan tinggi dan suhu stabil sepanjang tahun"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_population_insights(pop_df):
    """Show population insights"""
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h4>👥 Insights Kependudukan</h4>', unsafe_allow_html=True)
    
    # Calculate population statistics
    total_pop = pop_df['Total_Penduduk'].sum()
    total_households = pop_df['Rumah_Tangga'].sum()
    avg_household_size = total_pop / total_households
    
    # Gender analysis
    total_male = pop_df['Penduduk_Laki'].sum()
    total_female = pop_df['Penduduk_Perempuan'].sum()
    gender_ratio = (total_male / total_female) * 100
    
    # Density analysis
    avg_density = pop_df['Kepadatan_per_km2'].mean()
    highest_density = pop_df.loc[pop_df['Kepadatan_per_km2'].idxmax()]
    lowest_density = pop_df.loc[pop_df['Kepadatan_per_km2'].idxmin()]
    
    # Population distribution
    urban_areas = pop_df[pop_df['Kabupaten_Kota'].str.contains('Kota')]
    rural_areas = pop_df[pop_df['Kabupaten_Kota'].str.contains('Kabupaten')]
    
    urban_pop = urban_areas['Total_Penduduk'].sum()
    rural_pop = rural_areas['Total_Penduduk'].sum()
    urbanization_rate = (urban_pop / total_pop) * 100
    
    insights = [
        f"👥 **Total Penduduk**: {total_pop:,} jiwa tersebar di 23 kabupaten/kota",
        f"🏠 **Rumah Tangga**: {total_households:,} rumah tangga dengan rata-rata {avg_household_size:.1f} jiwa per rumah tangga",
        f"⚖️ **Rasio Gender**: {gender_ratio:.1f} laki-laki per 100 perempuan (relatif seimbang)",
        f"🏙️ **Tingkat Urbanisasi**: {urbanization_rate:.1f}% penduduk tinggal di kota-kota",
        f"📊 **Kepadatan Rata-rata**: {avg_density:.0f} jiwa per km²",
        f"🏆 **Terpadat**: {highest_density['Kabupaten_Kota']} ({highest_density['Kepadatan_per_km2']:,.0f} jiwa/km²)",
        f"🌿 **Terjarang**: {lowest_density['Kabupaten_Kota']} ({lowest_density['Kepadatan_per_km2']:.0f} jiwa/km²)",
        f"🏘️ **Distribusi**: {len(rural_areas)} kabupaten (rural) vs {len(urban_areas)} kota (urban)",
        f"📈 **Konsentrasi**: 3 daerah terpadat menampung {pop_df.nlargest(3, 'Total_Penduduk')['Total_Penduduk'].sum()/total_pop*100:.1f}% total penduduk"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Helper function for creating metric cards (use the same from main_app.py)
def create_metric_card(icon, value, label, change=None, change_type="positive"):
    """Create a metric card HTML"""
    change_html = ""
    if change:
        change_class = "positive" if change_type == "positive" else "negative"
        change_html = f'<div class="metric-change {change_class}">{change}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {change_html}
    </div>
    """

def format_number(value, format_type="number"):
    """Format numbers for display"""
    if pd.isna(value):
        return "N/A"
    
    try:
        value = float(value)
    except:
        return str(value)
    
    if format_type == "currency":
        if abs(value) >= 1e6:
            return f"{value/1e6:.1f}M"
        elif abs(value) >= 1e3:
            return f"{value/1e3:.1f}K"
        else:
            return f"{value:.0f}"
    elif format_type == "percentage":
        return f"{value:.2f}%"
    else:
        return f"{value:,.0f}"
    
@st.cache_data
def load_listrik_gas_air_datasets():
    """Load Listrik, Gas & Air datasets from uploaded documents"""
    datasets = {}
    
    # Arun NGL Data (Gas Alam Cair dan Kondensat)
    arun_data = [
        [1980, 9897778, 22454164],
        [1982, 10755607, 26615433],
        [1983, 11622537, 29915143],
        [1984, 15522160, 36802133],
        [1986, 17483963, 37281258],
        [1988, 22841227, 42209729],
        [1989, 23862509, 45357329],
        [1990, 24504000, 44500000],
        [1991, 25925691, 42886072],
        [1992, 26750906, 41146796],
        [1993, 27050625, 38818931],
        [1994, 27570548, 33492310],
        [1995, 25269280, 31891187],
        [1996, 24970444, 29154098],
        [1997, 25525153, 22379342],
        [1998, 24096892, 17870331],
        [1999, 24259488, 15459482],
        [2000, 14751040, 10307130],
        [2001, 14821473, 10332836],
        [2002, 14067484, 9224552],
        [2003, 14309099, 9374944],
        [2004, 12875597, 7857508],
        [2005, 9340583, 5108894],
        [2006, 9340583, 5108894],
        [2007, 6224063, 3196150],
        [2008, 5192521, 2511720],
        [2009, 4790922, 2068082],
        [2010, 4212914, 1908076],
        [2011, 2588156, 1571217],
        [2012, 1956014, 1226421]
    ]
    
    datasets['arun'] = pd.DataFrame(arun_data, columns=['Tahun', 'LNG_m3', 'Kondensat_Barrel'])
    
    # PLN Data (simplified - key years)
    pln_data = [
        [1968, 8832, 8426, None, 39942],
        [1969, 10796, 8469, 8800, 100165],
        [1970, 13140, 8640, 10459, 119984],
        [1975, 21351, 12963, 19650, 402783],
        [1980, 52253, 27851, 37432, 1967786],
        [1985, 106247, 68813, 72121, 8351635],
        [1990, 238812, 180548, 177384, 23856207],
        [1995, 394078, 334206, 324977, 56095660],
        [2000, 150633, 565468, 506310, 130515072],
        [2005, 147193, 665957, 698932, 306769615],
        [2010, 206987, 987027, 1491936, 929737238],
        [2013, 74113, 1127469, 1815030, 1329291874]
    ]
    
    datasets['pln'] = pd.DataFrame(pln_data, columns=['Tahun', 'Produksi_Listrik_000kWh', 'Jumlah_Langganan', 'Listrik_Terjual_000kWh', 'Nilai_Penjualan_000Rp'])
    
    # Water Company Data
    water_data = [
        [1997, 1342, 1036, 77],
        [1998, 1253, 845, 67],
        [1999, 1335, 881, 65],
        [2000, 1910, 1152, 60],
        [2001, 1887, 1152, 61],
        [2002, 2141, 1304, 61],
        [2003, 2171, 1316, 61],
        [2004, 1865, 1236, 66],
        [2005, 2370, 1480, 62],
        [2007, 1444, 1151, 79],
        [2008, 1444, 1151, 79],
        [2010, 1379, 877, 64],
        [2011, 1926, 1632, 85],
        [2012, 1537, 1024, 67],
        [2013, 1836, 1212, 69]
    ]
    
    datasets['water'] = pd.DataFrame(water_data, columns=['Tahun', 'Produksi_Potensial_lps', 'Produksi_Efektif_lps', 'Efektivitas_Persen'])
    
    return datasets

def show_listrik_gas_air(datasets=None):
    """Enhanced Listrik, Gas & Air dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">⚡ Sektor Listrik, Gas & Air Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Infrastruktur Utilitas dan Energi (1968-2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the datasets
    if datasets is None:
        datasets = load_listrik_gas_air_datasets()
    
    # Tabs for different utilities
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⛽ Gas & LNG", "⚡ Listrik PLN", "💧 Air Minum"])
    
    with tab1:
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'arun' in datasets:
                total_lng = datasets['arun']['LNG_m3'].sum()
                st.markdown(create_metric_card("⛽", format_number(total_lng), "Total Produksi LNG", "m³ (1980-2012)"), unsafe_allow_html=True)
        
        with col2:
            if 'pln' in datasets:
                latest_customers = datasets['pln']['Jumlah_Langganan'].iloc[-1]
                st.markdown(create_metric_card("⚡", format_number(latest_customers), "Pelanggan PLN", "Tahun 2013"), unsafe_allow_html=True)
        
        with col3:
            if 'water' in datasets:
                avg_efficiency = datasets['water']['Efektivitas_Persen'].mean()
                st.markdown(create_metric_card("💧", f"{avg_efficiency:.1f}%", "Efisiensi Air Rata-rata", "1997-2013"), unsafe_allow_html=True)
        
        with col4:
            # Calculate total energy infrastructure value
            if 'pln' in datasets:
                latest_revenue = datasets['pln']['Nilai_Penjualan_000Rp'].iloc[-1]
                st.markdown(create_metric_card("💰", format_number(latest_revenue, 'currency'), "Revenue PLN 2013", "000 Rupiah"), unsafe_allow_html=True)
        
        # Overview comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'arun' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">⛽ Trend Produksi Gas Arun</h3>', unsafe_allow_html=True)
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Scatter(x=datasets['arun']['Tahun'], y=datasets['arun']['LNG_m3'],
                             name="LNG (m³)", line=dict(color='#1e40af', width=3)),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=datasets['arun']['Tahun'], y=datasets['arun']['Kondensat_Barrel'],
                             name="Kondensat (Barrel)", line=dict(color='#dc2626', width=3)),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Tahun")
                fig.update_yaxes(title_text="LNG (m³)", secondary_y=False)
                fig.update_yaxes(title_text="Kondensat (Barrel)", secondary_y=True)
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'pln' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">⚡ Pertumbuhan Pelanggan PLN</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['pln'], x='Tahun', y='Jumlah_Langganan',
                            title="",
                            labels={'Jumlah_Langganan': 'Jumlah Pelanggan', 'Tahun': 'Tahun'})
                fig.update_traces(line=dict(color='#f59e0b', width=3), marker=dict(size=8))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Utilities efficiency comparison
        if 'water' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">💧 Efisiensi Produksi Air Minum</h3>', unsafe_allow_html=True)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=datasets['water']['Tahun'], y=datasets['water']['Produksi_Potensial_lps'],
                       name="Produksi Potensial", marker_color='#3b82f6', opacity=0.7),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Bar(x=datasets['water']['Tahun'], y=datasets['water']['Produksi_Efektif_lps'],
                       name="Produksi Efektif", marker_color='#1e40af'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=datasets['water']['Tahun'], y=datasets['water']['Efektivitas_Persen'],
                          name="Efektivitas (%)", line=dict(color='#dc2626', width=3),
                          mode='lines+markers'),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Tahun")
            fig.update_yaxes(title_text="Produksi (liter/detik)", secondary_y=False)
            fig.update_yaxes(title_text="Efektivitas (%)", secondary_y=True)
            fig.update_layout(height=500, barmode='group')
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">⛽ Analisis Gas Alam Cair PT. Arun NGL</h2>', unsafe_allow_html=True)
        
        if 'arun' in datasets:
            # Production metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_lng = datasets['arun']['LNG_m3'].sum()
            total_kondensat = datasets['arun']['Kondensat_Barrel'].sum()
            peak_lng_year = datasets['arun'].loc[datasets['arun']['LNG_m3'].idxmax(), 'Tahun']
            peak_lng_value = datasets['arun']['LNG_m3'].max()
            
            with col1:
                st.markdown(create_metric_card("⛽", format_number(total_lng), "Total LNG", "m³ (1980-2012)"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("🛢️", format_number(total_kondensat), "Total Kondensat", "Barrel"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("📈", str(int(peak_lng_year)), "Puncak Produksi LNG", f"{format_number(peak_lng_value)} m³"), unsafe_allow_html=True)
            
            with col4:
                avg_lng = datasets['arun']['LNG_m3'].mean()
                st.markdown(create_metric_card("📊", format_number(avg_lng), "Rata-rata LNG/Tahun", "m³"), unsafe_allow_html=True)
            
            # Detailed production analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Produksi LNG Tahunan</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['arun'], x='Tahun', y='LNG_m3',
                             color_discrete_sequence=['#1e40af'],
                             title="",
                             labels={'LNG_m3': 'Produksi LNG (m³)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🛢️ Produksi Kondensat Tahunan</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['arun'], x='Tahun', y='Kondensat_Barrel',
                             color_discrete_sequence=['#dc2626'],
                             title="",
                             labels={'Kondensat_Barrel': 'Produksi Kondensat (Barrel)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Production decline analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📉 Analisis Penurunan Produksi</h3>', unsafe_allow_html=True)
            
            # Calculate year-over-year change
            arun_analysis = datasets['arun'].copy()
            arun_analysis['LNG_Change'] = arun_analysis['LNG_m3'].pct_change() * 100
            arun_analysis['Kondensat_Change'] = arun_analysis['Kondensat_Barrel'].pct_change() * 100
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=arun_analysis['Tahun'], y=arun_analysis['LNG_Change'],
                               name='Perubahan LNG (%)', marker_color='#3b82f6'))
            fig.add_trace(go.Bar(x=arun_analysis['Tahun'], y=arun_analysis['Kondensat_Change'],
                               name='Perubahan Kondensat (%)', marker_color='#ef4444'))
            
            fig.update_layout(height=400, barmode='group',
                            xaxis_title="Tahun", yaxis_title="Perubahan (%)",
                            title="Perubahan Produksi Year-over-Year")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Analysis insights
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Analisis & Insights Produksi Gas Arun</h4>', unsafe_allow_html=True)
            
            # Calculate key insights
            decline_start = 1994  # Peak production year
            recent_years = datasets['arun'][datasets['arun']['Tahun'] >= 2000]
            avg_decline = recent_years['LNG_m3'].mean()
            
            insights = [
                f"📈 **Periode Puncak**: Produksi LNG mencapai puncak pada tahun {peak_lng_year} dengan {format_number(peak_lng_value)} m³",
                f"📉 **Tren Penurunan**: Sejak 1994, terjadi penurunan produksi yang signifikan hingga 2012",
                f"⛽ **Total Kontribusi**: PT. Arun NGL memproduksi total {format_number(total_lng)} m³ LNG dan {format_number(total_kondensat)} barrel kondensat",
                f"🛢️ **Rasio Produksi**: Rata-rata rasio kondensat terhadap LNG sekitar {(total_kondensat/total_lng)*1000:.2f} barrel per 1000 m³ LNG",
                f"📊 **Fase Operasi**: Data menunjukkan 3 fase - pertumbuhan (1980-1993), puncak (1993-1999), dan penurunan (2000-2012)",
                f"🔄 **Dampak Ekonomi**: Penurunan produksi mempengaruhi kontribusi sektor migas terhadap PDRB Aceh",
                f"⚠️ **Missing Data**: Beberapa tahun tidak memiliki data (1981, 1985, 1987) yang mungkin terkait masalah operasional"
            ]
            
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">⚡ Analisis Sektor Kelistrikan PLN</h2>', unsafe_allow_html=True)
        
        if 'pln' in datasets:
            # PLN metrics
            col1, col2, col3, col4 = st.columns(4)
            
            latest_data = datasets['pln'].iloc[-1]
            first_data = datasets['pln'].iloc[0]
            
            with col1:
                growth_customers = ((latest_data['Jumlah_Langganan'] - first_data['Jumlah_Langganan']) / first_data['Jumlah_Langganan']) * 100
                st.markdown(create_metric_card("👥", format_number(latest_data['Jumlah_Langganan']), "Total Pelanggan 2013", f"Growth: {growth_customers:.0f}%"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("⚡", format_number(latest_data['Listrik_Terjual_000kWh']), "Listrik Terjual 2013", "000 kWh"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("💰", format_number(latest_data['Nilai_Penjualan_000Rp'], 'currency'), "Revenue 2013", "Juta Rupiah"), unsafe_allow_html=True)
            
            with col4:
                if latest_data['Listrik_Terjual_000kWh'] and latest_data['Jumlah_Langganan']:
                    consumption_per_customer = latest_data['Listrik_Terjual_000kWh'] / latest_data['Jumlah_Langganan'] * 1000
                    st.markdown(create_metric_card("🔌", f"{consumption_per_customer:.0f}", "kWh/Pelanggan", "Rata-rata 2013"), unsafe_allow_html=True)
            
            # PLN development charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Pertumbuhan Pelanggan PLN</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['pln'], x='Tahun', y='Jumlah_Langganan',
                            markers=True,
                            color_discrete_sequence=['#f59e0b'],
                            title="")
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Jumlah Pelanggan")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">💰 Perkembangan Pendapatan</h3>', unsafe_allow_html=True)
                
                fig = px.bar(datasets['pln'], x='Tahun', y='Nilai_Penjualan_000Rp',
                           color_discrete_sequence=['#10b981'],
                           title="")
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Nilai Penjualan (000 Rupiah)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Production vs Sales analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">⚡ Produksi vs Penjualan Listrik</h3>', unsafe_allow_html=True)
            
            # Filter data where both production and sales are available
            pln_complete = datasets['pln'].dropna(subset=['Produksi_Listrik_000kWh', 'Listrik_Terjual_000kWh'])
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=pln_complete['Tahun'], y=pln_complete['Produksi_Listrik_000kWh'],
                                   name='Produksi Listrik', line=dict(color='#3b82f6', width=3),
                                   mode='lines+markers'))
            fig.add_trace(go.Scatter(x=pln_complete['Tahun'], y=pln_complete['Listrik_Terjual_000kWh'],
                                   name='Listrik Terjual', line=dict(color='#ef4444', width=3),
                                   mode='lines+markers'))
            
            fig.update_layout(height=400,
                            xaxis_title="Tahun", yaxis_title="Listrik (000 kWh)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # PLN Analysis insights
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Analisis & Insights Sektor Kelistrikan</h4>', unsafe_allow_html=True)
            
            # Calculate growth rates
            customer_cagr = ((latest_data['Jumlah_Langganan'] / first_data['Jumlah_Langganan']) ** (1/45)) - 1
            
            insights = [
                f"📈 **Pertumbuhan Spektakuler**: Pelanggan PLN tumbuh dari {format_number(first_data['Jumlah_Langganan'])} (1968) menjadi {format_number(latest_data['Jumlah_Langganan'])} (2013)",
                f"📊 **CAGR Pelanggan**: Pertumbuhan rata-rata {customer_cagr*100:.1f}% per tahun selama 45 tahun",
                f"💰 **Ekspansi Revenue**: Nilai penjualan mencapai {format_number(latest_data['Nilai_Penjualan_000Rp'], 'currency')} ribu rupiah pada 2013",
                f"⚡ **Elektrifikasi Massal**: Konsumsi listrik per pelanggan rata-rata {consumption_per_customer:.0f} kWh/tahun pada 2013",
                f"🏗️ **Pembangunan Infrastruktur**: Peningkatan drastis kapasitas produksi untuk memenuhi demand yang terus tumbuh",
                f"🌍 **Dampak Pembangunan**: Elektrifikasi menjadi fondasi penting pembangunan ekonomi dan sosial Aceh",
                f"📉 **Anomali Data**: Penurunan produksi di tahun-tahun terakhir mungkin terkait efisiensi atau perubahan metodologi pencatatan"
            ]
            
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">💧 Analisis Perusahaan Air Minum</h2>', unsafe_allow_html=True)
        
        if 'water' in datasets:
            # Water metrics
            col1, col2, col3, col4 = st.columns(4)
            
            avg_efficiency = datasets['water']['Efektivitas_Persen'].mean()
            max_potential = datasets['water']['Produksi_Potensial_lps'].max()
            max_effective = datasets['water']['Produksi_Efektif_lps'].max()
            best_efficiency = datasets['water']['Efektivitas_Persen'].max()
            
            with col1:
                st.markdown(create_metric_card("💧", f"{avg_efficiency:.1f}%", "Efisiensi Rata-rata", "1997-2013"), unsafe_allow_html=True)
            
            with col2:
                st.markdown(create_metric_card("🚿", f"{max_potential}", "Kapasitas Maksimal", "liter/detik"), unsafe_allow_html=True)
            
            with col3:
                st.markdown(create_metric_card("📊", f"{max_effective}", "Produksi Efektif Puncak", "liter/detik"), unsafe_allow_html=True)
            
            with col4:
                best_year = datasets['water'].loc[datasets['water']['Efektivitas_Persen'].idxmax(), 'Tahun']
                st.markdown(create_metric_card("🏆", f"{best_efficiency}%", f"Efisiensi Terbaik", f"Tahun {int(best_year)}"), unsafe_allow_html=True)
            
            # Water production analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">💧 Kapasitas vs Produksi Efektif</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['water']['Tahun'], y=datasets['water']['Produksi_Potensial_lps'],
                                       name='Kapasitas Potensial', fill='tonexty',
                                       line=dict(color='#60a5fa'), mode='lines+markers'))
                fig.add_trace(go.Scatter(x=datasets['water']['Tahun'], y=datasets['water']['Produksi_Efektif_lps'],
                                       name='Produksi Efektif', fill='tozeroy',
                                       line=dict(color='#1e40af'), mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Produksi (liter/detik)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Tren Efektivitas</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['water'], x='Tahun', y='Efektivitas_Persen',
                            markers=True,
                            color_discrete_sequence=['#dc2626'],
                            title="")
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Efektivitas (%)")
                fig.add_hline(y=avg_efficiency, line_dash="dash", 
                            annotation_text=f"Rata-rata: {avg_efficiency:.1f}%")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Efficiency analysis
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📊 Analisis Efisiensi & Kapasitas Utilisasi</h3>', unsafe_allow_html=True)
            
            # Calculate capacity utilization
            water_analysis = datasets['water'].copy()
            water_analysis['Kapasitas_Tidak_Terpakai'] = water_analysis['Produksi_Potensial_lps'] - water_analysis['Produksi_Efektif_lps']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=water_analysis['Tahun'], y=water_analysis['Produksi_Efektif_lps'],
                               name='Produksi Efektif', marker_color='#1e40af'))
            fig.add_trace(go.Bar(x=water_analysis['Tahun'], y=water_analysis['Kapasitas_Tidak_Terpakai'],
                               name='Kapasitas Tidak Terpakai', marker_color='#ef4444', opacity=0.6))
            
            fig.update_layout(barmode='stack', height=400,
                            xaxis_title="Tahun", yaxis_title="Kapasitas (liter/detik)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Water sector insights
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Analisis & Insights Sektor Air Minum</h4>', unsafe_allow_html=True)
            
            # Calculate key insights
            efficiency_trend = datasets['water']['Efektivitas_Persen'].iloc[-3:].mean() - datasets['water']['Efektivitas_Persen'].iloc[:3].mean()
            avg_waste = 100 - avg_efficiency
            total_potential = datasets['water']['Produksi_Potensial_lps'].sum()
            total_effective = datasets['water']['Produksi_Efektif_lps'].sum()
            
            insights = [
                f"💧 **Efisiensi Rata-rata**: {avg_efficiency:.1f}% dengan {avg_waste:.1f}% kapasitas tidak optimal",
                f"📈 **Tren Efisiensi**: {'Meningkat' if efficiency_trend > 0 else 'Menurun'} {abs(efficiency_trend):.1f} poin dalam periode terakhir",
                f"🏆 **Performa Terbaik**: Efisiensi tertinggi {best_efficiency}% dicapai pada tahun {int(best_year)}",
                f"📊 **Kapasitas Maksimal**: Produksi potensial tertinggi {max_potential} liter/detik",
                f"💪 **Realisasi Terbaik**: Produksi efektif tertinggi {max_effective} liter/detik",
                f"⚠️ **Tantangan Operasional**: Fluktuasi efisiensi menunjukkan adanya kendala teknis atau operasional",
                f"🔄 **Potensi Optimasi**: Rata-rata {avg_waste:.1f}% kapasitas belum termanfaatkan optimal",
                f"📋 **Data Gaps**: Beberapa tahun (2006, 2009) tidak memiliki data yang dapat mempengaruhi analisis tren",
                f"🎯 **Target Improvement**: Potensi peningkatan efisiensi menuju 85%+ berdasarkan performa terbaik yang pernah dicapai"
            ]
            
            for insight in insights:
                st.markdown(f"- {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Data tables and export section
    with st.expander("📋 Data Tables & Export"):
        dataset_selector = st.selectbox(
            "Pilih Dataset:",
            ["Gas Alam Cair (Arun)", "Listrik PLN", "Air Minum"],
            key="listrik_gas_air_selector"
        )
        
        if dataset_selector == "Gas Alam Cair (Arun)":
            selected_df = datasets['arun']
            filename = "aceh_gas_arun"
        elif dataset_selector == "Listrik PLN":
            selected_df = datasets['pln']
            filename = "aceh_listrik_pln"
        else:
            selected_df = datasets['water']
            filename = "aceh_air_minum"
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.dataframe(selected_df, use_container_width=True, height=400)
        
        with col2:
            # Download button
            csv_buffer = io.StringIO()
            selected_df.to_csv(csv_buffer, index=False, sep=';')
            st.download_button(
                label="💾 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"{filename}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Data summary
            st.markdown("#### 📊 Ringkasan Data")
            st.metric("Total Records", len(selected_df))
            st.metric("Periode", f"{selected_df['Tahun'].min()}-{selected_df['Tahun'].max()}")
            
            # Data quality info
            missing_years = []
            year_range = range(int(selected_df['Tahun'].min()), int(selected_df['Tahun'].max()) + 1)
            for year in year_range:
                if year not in selected_df['Tahun'].values:
                    missing_years.append(year)
            
            if missing_years:
                st.warning(f"Missing data: {', '.join(map(str, missing_years))}")
            else:
                st.success("✅ Data lengkap")

# Function to update the main sector selection in main_app.py
def update_show_listrik_gas_air_section():
    """
    Replace the existing show_data_upload_section call for listrik_gas_air with this:
    """
    # In your main() function, replace this line:
    # show_data_upload_section(st.session_state.selected_sector)
    
    # With this condition:
    if st.session_state.selected_sector == "listrik_gas_air":
        show_listrik_gas_air()
    else:
        show_data_upload_section(st.session_state.selected_sector)
        
@st.cache_data
def load_perdagangan_datasets():
    """Load Perdagangan (Trade) datasets from uploaded documents"""
    datasets = {}
    
    # 1. Export by Commodity (2009-2013)
    ekspor_komoditi_data = [
        [2009, 192, 88658, 12, 1049157, 1138019],
        [2010, 1465, 20479, 2999, 1334308, 1359251],
        [2011, 384, 58429, 18445, 1406333, 1483591],
        [2012, 139, 49855, 10161, 1197244, 1257399],
        [2013, 50694, 5838, 27079, 879359, 962970]
    ]
    
    datasets['ekspor_komoditi'] = pd.DataFrame(ekspor_komoditi_data, 
                                               columns=['Tahun', 'Pertanian', 'Industri', 'Pertambangan', 'Migas', 'Total_Ekspor'])
    
    # 2. Export by Port (2009-2013)
    ekspor_pelabuhan_data = [
        ['Blang Lancang (Arun)', 1034977, 1326272, 1406333, 1197244, 831714],
        ['Krueng Geukeuh', 87829, 22961, 58852, 49812, 7],
        ['Susoh', 14, 0, 0, 5166, 0],
        ['Meulaboh', 23, 1392, 17698, 3530, 23375],
        ['Ulee Lheue', 0, 0, 8, 1507, 71359],
        ['Lainnya', 15176, 8626, 700, 140, 36515]
    ]
    
    pelabuhan_df = pd.DataFrame(ekspor_pelabuhan_data, 
                                columns=['Pelabuhan', '2009', '2010', '2011', '2012', '2013'])
    
    # Melt to long format for easier visualization
    datasets['ekspor_pelabuhan'] = pd.melt(pelabuhan_df, 
                                           id_vars=['Pelabuhan'], 
                                           var_name='Tahun', 
                                           value_name='Nilai_Ekspor')
    datasets['ekspor_pelabuhan']['Tahun'] = datasets['ekspor_pelabuhan']['Tahun'].astype(int)
    
    # 3. Trade Balance (1959-2013) - Using sample data for key years
    neraca_perdagangan_data = [
        [1959, 42344, 0, 42344],
        [1965, 11030, 942, 10088],
        [1970, 13090, 1399, 11691],
        [1975, 24595, 84, 24511],
        [1980, 1898583, 21361, 1877222],
        [1985, 2864827, 251560, 2613267],
        [1990, 2979073, 88059, 2891014],
        [1995, 2562374, 75031, 2487343],
        [2000, 1806083, 70319, 1735764],
        [2005, 2072415, 18414, 2054001],
        [2009, 1138019, 115718, 1022301],
        [2010, 1359251, 38388, 1320863],
        [2011, 1483591, 114045, 1369546],
        [2012, 1257399, 85316, 1172083],
        [2013, 962970, 11130, 951840]
    ]
    
    datasets['neraca_perdagangan'] = pd.DataFrame(neraca_perdagangan_data, 
                                                  columns=['Tahun', 'Ekspor', 'Impor', 'Neraca_Perdagangan'])
    
    # 4. Import by Country (2009-2013)
    impor_negara_data = [
        ['Tiongkok', 2708, 12334, 63929, 43002, 665],
        ['Singapura', 72275, 4925, 18722, 21905, 8701],
        ['Thailand', 1188, 4812, 11049, 13906, 530],
        ['Vietnam', 0, 7052, 15497, 3819, 0],
        ['Malaysia', 27840, 7573, 4534, 2070, 1234],
        ['Lainnya', 11707, 1692, 314, 614, 0]
    ]
    
    negara_df = pd.DataFrame(impor_negara_data, 
                             columns=['Negara', '2009', '2010', '2011', '2012', '2013'])
    
    # Melt to long format
    datasets['impor_negara'] = pd.melt(negara_df, 
                                       id_vars=['Negara'], 
                                       var_name='Tahun', 
                                       value_name='Nilai_Impor')
    datasets['impor_negara']['Tahun'] = datasets['impor_negara']['Tahun'].astype(int)
    
    # 5. Import by Commodity (2009-2013)
    impor_komoditi_data = [
        [2009, 473, 23609, 6906, 84730, 115718],
        [2010, 11174, 7391, 3591, 16232, 38388],
        [2011, 25796, 5271, 3658, 79320, 114045],
        [2012, 16226, 2304, 5063, 61723, 85316],
        [2013, 81, 1080, 6000, 3969, 11130]
    ]
    
    datasets['impor_komoditi'] = pd.DataFrame(impor_komoditi_data, 
                                              columns=['Tahun', 'Pertanian', 'Pertambangan', 'Migas', 'Industri', 'Total_Impor'])
    
    return datasets

def show_perdagangan():
    """Enhanced Perdagangan dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">🛒 Sektor Perdagangan Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Ekspor, Impor, dan Neraca Perdagangan (1959-2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the datasets
    datasets = load_perdagangan_datasets()
    
    # Tabs for different trade aspects
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📤 Ekspor", "📥 Impor", "⚖️ Neraca Perdagangan", "📋 Data Tables"])
    
    with tab1:
        # Key trade metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ekspor_komoditi' in datasets:
                total_ekspor_2013 = datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2013]['Total_Ekspor'].iloc[0]
                st.markdown(create_metric_card("📤", format_number(total_ekspor_2013, 'currency'), "Total Ekspor 2013", "Ribu USD"), unsafe_allow_html=True)
        
        with col2:
            if 'impor_komoditi' in datasets:
                total_impor_2013 = datasets['impor_komoditi'][datasets['impor_komoditi']['Tahun'] == 2013]['Total_Impor'].iloc[0]
                st.markdown(create_metric_card("📥", format_number(total_impor_2013, 'currency'), "Total Impor 2013", "Ribu USD"), unsafe_allow_html=True)
        
        with col3:
            if 'neraca_perdagangan' in datasets:
                neraca_2013 = datasets['neraca_perdagangan'][datasets['neraca_perdagangan']['Tahun'] == 2013]['Neraca_Perdagangan'].iloc[0]
                st.markdown(create_metric_card("⚖️", format_number(neraca_2013, 'currency'), "Surplus Perdagangan 2013", "Ribu USD"), unsafe_allow_html=True)
        
        with col4:
            if 'ekspor_komoditi' in datasets:
                migas_dominance = (datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2013]['Migas'].iloc[0] / 
                                  datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2013]['Total_Ekspor'].iloc[0]) * 100
                st.markdown(create_metric_card("🛢️", f"{migas_dominance:.1f}%", "Dominasi Migas", "dari Total Ekspor 2013"), unsafe_allow_html=True)
        
        # Overview visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'ekspor_komoditi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📤 Tren Ekspor Total (2009-2013)</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['ekspor_komoditi'], x='Tahun', y='Total_Ekspor',
                            markers=True,
                            color_discrete_sequence=['#1e40af'],
                            title="",
                            labels={'Total_Ekspor': 'Total Ekspor (Ribu USD)', 'Tahun': 'Tahun'})
                fig.update_traces(line=dict(width=4), marker=dict(size=10))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'impor_komoditi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📥 Tren Impor Total (2009-2013)</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['impor_komoditi'], x='Tahun', y='Total_Impor',
                            markers=True,
                            color_discrete_sequence=['#dc2626'],
                            title="",
                            labels={'Total_Impor': 'Total Impor (Ribu USD)', 'Tahun': 'Tahun'})
                fig.update_traces(line=dict(width=4), marker=dict(size=10))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Trade balance overview
        if 'neraca_perdagangan' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">⚖️ Neraca Perdagangan Historis (1959-2013)</h3>', unsafe_allow_html=True)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=datasets['neraca_perdagangan']['Tahun'], y=datasets['neraca_perdagangan']['Ekspor'],
                         name="Ekspor", line=dict(color='#10b981', width=3), mode='lines+markers'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=datasets['neraca_perdagangan']['Tahun'], y=datasets['neraca_perdagangan']['Impor'],
                         name="Impor", line=dict(color='#ef4444', width=3), mode='lines+markers'),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Bar(x=datasets['neraca_perdagangan']['Tahun'], y=datasets['neraca_perdagangan']['Neraca_Perdagangan'],
                       name="Neraca", marker_color='#3b82f6', opacity=0.6),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Tahun")
            fig.update_yaxes(title_text="Ekspor & Impor (Ribu USD)", secondary_y=False)
            fig.update_yaxes(title_text="Neraca Perdagangan (Ribu USD)", secondary_y=True)
            fig.update_layout(height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📤 Analisis Ekspor Mendalam</h2>', unsafe_allow_html=True)
        
        # Export metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ekspor_komoditi' in datasets:
                total_ekspor_5yr = datasets['ekspor_komoditi']['Total_Ekspor'].sum()
                st.markdown(create_metric_card("💰", format_number(total_ekspor_5yr, 'currency'), "Total Ekspor 2009-2013", "Ribu USD"), unsafe_allow_html=True)
        
        with col2:
            if 'ekspor_komoditi' in datasets:
                migas_total = datasets['ekspor_komoditi']['Migas'].sum()
                migas_share = (migas_total / total_ekspor_5yr) * 100
                st.markdown(create_metric_card("🛢️", f"{migas_share:.1f}%", "Kontribusi Migas", "5 Tahun"), unsafe_allow_html=True)
        
        with col3:
            if 'ekspor_pelabuhan' in datasets:
                arun_total = datasets['ekspor_pelabuhan'][datasets['ekspor_pelabuhan']['Pelabuhan'] == 'Blang Lancang (Arun)']['Nilai_Ekspor'].sum()
                arun_share = (arun_total / total_ekspor_5yr) * 100
                st.markdown(create_metric_card("🚢", f"{arun_share:.1f}%", "Dominasi Pelabuhan Arun", "dari Total Ekspor"), unsafe_allow_html=True)
        
        with col4:
            if 'ekspor_komoditi' in datasets:
                decline_rate = ((datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2013]['Total_Ekspor'].iloc[0] - 
                               datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2009]['Total_Ekspor'].iloc[0]) / 
                               datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2009]['Total_Ekspor'].iloc[0]) * 100
                st.markdown(create_metric_card("📉", f"{decline_rate:.1f}%", "Perubahan 2009-2013", "Tren Ekspor"), unsafe_allow_html=True)
        
        # Export by commodity analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if 'ekspor_komoditi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📦 Ekspor Berdasarkan Komoditas</h3>', unsafe_allow_html=True)
                
                # Melt data for better visualization
                ekspor_melt = pd.melt(datasets['ekspor_komoditi'], 
                                     id_vars=['Tahun'], 
                                     value_vars=['Pertanian', 'Industri', 'Pertambangan', 'Migas'],
                                     var_name='Komoditas', value_name='Nilai')
                
                fig = px.area(ekspor_melt, x='Tahun', y='Nilai', color='Komoditas',
                            title="",
                            labels={'Nilai': 'Nilai Ekspor (Ribu USD)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'ekspor_komoditi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🥧 Komposisi Ekspor 2013</h3>', unsafe_allow_html=True)
                
                ekspor_2013 = datasets['ekspor_komoditi'][datasets['ekspor_komoditi']['Tahun'] == 2013]
                komoditas_data = {
                    'Komoditas': ['Pertanian', 'Industri', 'Pertambangan', 'Migas'],
                    'Nilai': [ekspor_2013['Pertanian'].iloc[0], ekspor_2013['Industri'].iloc[0], 
                             ekspor_2013['Pertambangan'].iloc[0], ekspor_2013['Migas'].iloc[0]]
                }
                komposisi_df = pd.DataFrame(komoditas_data)
                
                fig = px.pie(komposisi_df, values='Nilai', names='Komoditas',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Export by port analysis
        if 'ekspor_pelabuhan' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🚢 Ekspor Berdasarkan Pelabuhan (2009-2013)</h3>', unsafe_allow_html=True)
            
            # Filter out zero values for better visualization
            ekspor_pelabuhan_filtered = datasets['ekspor_pelabuhan'][datasets['ekspor_pelabuhan']['Nilai_Ekspor'] > 0]
            
            fig = px.bar(ekspor_pelabuhan_filtered, x='Tahun', y='Nilai_Ekspor', color='Pelabuhan',
                        title="",
                        labels={'Nilai_Ekspor': 'Nilai Ekspor (Ribu USD)', 'Tahun': 'Tahun'})
            fig.update_layout(height=500, barmode='stack')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Export insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Ekspor</h4>', unsafe_allow_html=True)
        
        insights_ekspor = [
            f"🛢️ **Dominasi Migas**: Sektor migas mendominasi dengan {migas_share:.1f}% dari total ekspor 2009-2013",
            f"📉 **Tren Menurun**: Ekspor total menurun {abs(decline_rate):.1f}% dari 2009 ke 2013",
            f"🚢 **Konsentrasi Pelabuhan**: Pelabuhan Blang Lancang (Arun) menguasai {arun_share:.1f}% total ekspor",
            f"🌾 **Diversifikasi Pertanian**: Ekspor pertanian melonjak dari 192 ribu USD (2009) menjadi 50.694 ribu USD (2013)",
            f"⛏️ **Volatilitas Pertambangan**: Ekspor pertambangan sangat fluktuatif, tertinggi di 2011 (18.445 ribu USD)",
            f"🏭 **Penurunan Industri**: Ekspor industri menurun drastis dari puncak 88.658 ribu USD (2009) ke 5.838 ribu USD (2013)",
            f"🎯 **Ketergantungan Tinggi**: Ekonomi ekspor sangat bergantung pada harga komoditas migas global",
            f"📊 **Pola Siklus**: Data menunjukkan pola siklus komoditas dengan puncak di 2011 dan penurunan setelahnya"
        ]
        
        for insight in insights_ekspor:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📥 Analisis Impor Mendalam</h2>', unsafe_allow_html=True)
        
        # Import metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'impor_komoditi' in datasets:
                total_impor_5yr = datasets['impor_komoditi']['Total_Impor'].sum()
                st.markdown(create_metric_card("💸", format_number(total_impor_5yr, 'currency'), "Total Impor 2009-2013", "Ribu USD"), unsafe_allow_html=True)
        
        with col2:
            if 'impor_negara' in datasets:
                china_total = datasets['impor_negara'][datasets['impor_negara']['Negara'] == 'Tiongkok']['Nilai_Impor'].sum()
                china_share = (china_total / total_impor_5yr) * 100
                st.markdown(create_metric_card("🇨🇳", f"{china_share:.1f}%", "Kontribusi Tiongkok", "dari Total Impor"), unsafe_allow_html=True)
        
        with col3:
            if 'impor_komoditi' in datasets:
                industri_total = datasets['impor_komoditi']['Industri'].sum()
                industri_share = (industri_total / total_impor_5yr) * 100
                st.markdown(create_metric_card("🏭", f"{industri_share:.1f}%", "Impor Industri", "5 Tahun"), unsafe_allow_html=True)
        
        with col4:
            if 'impor_komoditi' in datasets:
                impor_decline = ((datasets['impor_komoditi'][datasets['impor_komoditi']['Tahun'] == 2013]['Total_Impor'].iloc[0] - 
                                datasets['impor_komoditi'][datasets['impor_komoditi']['Tahun'] == 2009]['Total_Impor'].iloc[0]) / 
                                datasets['impor_komoditi'][datasets['impor_komoditi']['Tahun'] == 2009]['Total_Impor'].iloc[0]) * 100
                st.markdown(create_metric_card("📉", f"{impor_decline:.1f}%", "Penurunan Impor", "2009-2013"), unsafe_allow_html=True)
        
        # Import by commodity
        col1, col2 = st.columns(2)
        
        with col1:
            if 'impor_komoditi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📦 Impor Berdasarkan Komoditas</h3>', unsafe_allow_html=True)
                
                impor_melt = pd.melt(datasets['impor_komoditi'], 
                                   id_vars=['Tahun'], 
                                   value_vars=['Pertanian', 'Pertambangan', 'Migas', 'Industri'],
                                   var_name='Komoditas', value_name='Nilai')
                
                fig = px.bar(impor_melt, x='Tahun', y='Nilai', color='Komoditas',
                           title="",
                           labels={'Nilai': 'Nilai Impor (Ribu USD)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400, barmode='stack')
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'impor_negara' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🌏 Impor Berdasarkan Negara</h3>', unsafe_allow_html=True)
                
                # Aggregate by country
                impor_by_country = datasets['impor_negara'].groupby('Negara')['Nilai_Impor'].sum().reset_index()
                impor_by_country = impor_by_country.sort_values('Nilai_Impor', ascending=True)
                
                fig = px.bar(impor_by_country, x='Nilai_Impor', y='Negara',
                           orientation='h',
                           color='Nilai_Impor',
                           color_continuous_scale='Reds',
                           title="")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Import trends by country
        if 'impor_negara' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📈 Tren Impor Berdasarkan Negara (2009-2013)</h3>', unsafe_allow_html=True)
            
            # Filter major importers
            major_countries = ['Tiongkok', 'Singapura', 'Thailand', 'Malaysia']
            impor_major = datasets['impor_negara'][datasets['impor_negara']['Negara'].isin(major_countries)]
            
            fig = px.line(impor_major, x='Tahun', y='Nilai_Impor', color='Negara',
                        markers=True,
                        title="",
                        labels={'Nilai_Impor': 'Nilai Impor (Ribu USD)', 'Tahun': 'Tahun'})
            fig.update_traces(line=dict(width=3), marker=dict(size=8))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Import insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Impor</h4>', unsafe_allow_html=True)
        
        insights_impor = [
            f"📉 **Penurunan Drastis**: Total impor turun {abs(impor_decline):.1f}% dari 115.718 ribu USD (2009) ke 11.130 ribu USD (2013)",
            f"🇨🇳 **Dominasi Tiongkok**: Tiongkok berkontribusi {china_share:.1f}% dari total impor dengan fluktuasi tinggi",
            f"🏭 **Impor Industri**: Produk industri mendominasi struktur impor dengan kontribusi {industri_share:.1f}%",
            f"🌾 **Volatilitas Pertanian**: Impor pertanian sangat fluktuatif, tertinggi di 2011 (25.796 ribu USD)",
            f"🇸🇬 **Peran Singapura**: Singapura sebagai hub regional penting, terutama untuk produk olahan",
            f"⛽ **Impor Migas**: Impor migas relatif stabil menunjukkan kebutuhan domestik yang konsisten",
            f"🎯 **Konsentrasi Regional**: 80%+ impor berasal dari negara-negara Asia Tenggara dan Asia Timur",
            f"📊 **Pola Kontrasiklik**: Penurunan impor sejalan dengan penurunan aktivitas ekonomi domestik"
        ]
        
        for insight in insights_impor:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">⚖️ Analisis Neraca Perdagangan Historis</h2>', unsafe_allow_html=True)
        
        if 'neraca_perdagangan' in datasets:
            # Trade balance metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_surplus = datasets['neraca_perdagangan']['Neraca_Perdagangan'].mean()
                st.markdown(create_metric_card("💰", format_number(avg_surplus, 'currency'), "Rata-rata Surplus", "Historis"), unsafe_allow_html=True)
            
            with col2:
                max_surplus = datasets['neraca_perdagangan']['Neraca_Perdagangan'].max()
                max_year = datasets['neraca_perdagangan'].loc[datasets['neraca_perdagangan']['Neraca_Perdagangan'].idxmax(), 'Tahun']
                st.markdown(create_metric_card("📈", format_number(max_surplus, 'currency'), f"Surplus Tertinggi", f"Tahun {int(max_year)}"), unsafe_allow_html=True)
            
            with col3:
                recent_trend = datasets['neraca_perdagangan'].tail(3)['Neraca_Perdagangan'].mean()
                st.markdown(create_metric_card("📊", format_number(recent_trend, 'currency'), "Rata-rata 2011-2013", "Ribu USD"), unsafe_allow_html=True)
            
            with col4:
                export_import_ratio = (datasets['neraca_perdagangan'][datasets['neraca_perdagangan']['Tahun'] == 2013]['Ekspor'].iloc[0] / 
                                     datasets['neraca_perdagangan'][datasets['neraca_perdagangan']['Tahun'] == 2013]['Impor'].iloc[0])
                st.markdown(create_metric_card("⚖️", f"{export_import_ratio:.1f}x", "Rasio Ekspor:Impor", "Tahun 2013"), unsafe_allow_html=True)
            
            # Historical trade balance analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Evolusi Neraca Perdagangan (1959-2013)</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['neraca_perdagangan'], x='Tahun', y='Neraca_Perdagangan',
                            color_discrete_sequence=['#10b981'],
                            title="",
                            labels={'Neraca_Perdagangan': 'Neraca Perdagangan (Ribu USD)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Rasio Ekspor vs Impor</h3>', unsafe_allow_html=True)
                
                # Calculate ratio over time
                neraca_analysis = datasets['neraca_perdagangan'].copy()
                neraca_analysis['Ratio'] = neraca_analysis['Ekspor'] / neraca_analysis['Impor'].replace(0, 1)
                
                fig = px.line(neraca_analysis, x='Tahun', y='Ratio',
                            markers=True,
                            color_discrete_sequence=['#3b82f6'],
                            title="",
                            labels={'Ratio': 'Rasio Ekspor/Impor', 'Tahun': 'Tahun'})
                fig.add_hline(y=1, line_dash="dash", annotation_text="Break Even")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Trade performance by periods
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📈 Performa Perdagangan Berdasarkan Periode</h3>', unsafe_allow_html=True)
            
            # Define historical periods
            periods = {
                'Pra-Migas (1959-1970)': (1959, 1970),
                'Era Boom Migas (1975-1985)': (1975, 1985),
                'Stabilisasi (1990-2000)': (1990, 2000),
                'Era Modern (2005-2013)': (2005, 2013)
            }
            
            period_analysis = []
            for period_name, (start, end) in periods.items():
                period_data = datasets['neraca_perdagangan'][
                    (datasets['neraca_perdagangan']['Tahun'] >= start) & 
                    (datasets['neraca_perdagangan']['Tahun'] <= end)
                ]
                if not period_data.empty:
                    avg_export = period_data['Ekspor'].mean()
                    avg_import = period_data['Impor'].mean()
                    avg_surplus = period_data['Neraca_Perdagangan'].mean()
                    
                    period_analysis.append({
                        'Periode': period_name,
                        'Rata-rata Ekspor': avg_export,
                        'Rata-rata Impor': avg_import,
                        'Rata-rata Surplus': avg_surplus
                    })
            
            period_df = pd.DataFrame(period_analysis)
            period_melt = pd.melt(period_df, 
                                id_vars=['Periode'], 
                                value_vars=['Rata-rata Ekspor', 'Rata-rata Impor', 'Rata-rata Surplus'],
                                var_name='Indikator', value_name='Nilai')
            
            fig = px.bar(period_melt, x='Periode', y='Nilai', color='Indikator',
                        title="",
                        labels={'Nilai': 'Nilai (Ribu USD)', 'Periode': 'Periode'})
            fig.update_layout(height=500, barmode='group', xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Trade balance insights
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Analisis & Insights Neraca Perdagangan</h4>', unsafe_allow_html=True)
            
            insights_neraca = [
                f"💰 **Surplus Konsisten**: Aceh mempertahankan surplus perdagangan sejak 1965 hingga 2013",
                f"📈 **Puncak Era Migas**: Surplus tertinggi {format_number(max_surplus, 'currency')} ribu USD dicapai tahun {int(max_year)}",
                f"⚖️ **Rasio Sehat**: Rasio ekspor:impor {export_import_ratio:.1f}:1 pada 2013 menunjukkan ekonomi yang berorientasi ekspor",
                f"🛢️ **Ketergantungan Komoditas**: Fluktuasi neraca perdagangan sangat dipengaruhi harga minyak dan gas global",
                f"📊 **Tren Menurun**: Meski surplus, tren cenderung menurun dari puncak era 1980-1990an",
                f"🌍 **Dampak Global**: Krisis global 2008-2009 mempengaruhi performa perdagangan regional",
                f"🎯 **Potensi Diversifikasi**: Perlunya diversifikasi ekspor untuk mengurangi ketergantungan pada migas",
                f"📈 **Resiliensi**: Meski mengalami penurunan, surplus perdagangan tetap positif menunjukkan daya saing ekonomi Aceh"
            ]
            
            for insight in insights_neraca:
                st.markdown(f"- {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📋 Data Tables & Export Perdagangan</h2>', unsafe_allow_html=True)
        
        # Dataset selector
        dataset_options = {
            "Ekspor Berdasarkan Komoditas": "ekspor_komoditi",
            "Ekspor Berdasarkan Pelabuhan": "ekspor_pelabuhan",
            "Neraca Perdagangan Historis": "neraca_perdagangan",
            "Impor Berdasarkan Negara": "impor_negara",
            "Impor Berdasarkan Komoditas": "impor_komoditi"
        }
        
        selected_dataset = st.selectbox("Pilih Dataset untuk Ditampilkan:", 
                                      list(dataset_options.keys()))
        
        dataset_key = dataset_options[selected_dataset]
        
        if dataset_key in datasets:
            df = datasets[dataset_key]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"#### 📊 {selected_dataset}")
                st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
            
            with col2:
                # Download button
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"aceh_perdagangan_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                show_summary = st.checkbox("Tampilkan Ringkasan", value=True)
            
            # Display data
            st.dataframe(df, use_container_width=True, height=400)
            
            if show_summary:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📈 Statistik Dasar")
                    if 'Tahun' in df.columns:
                        st.metric("Periode Data", f"{df['Tahun'].min()}-{df['Tahun'].max()}")
                    
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        for col in numeric_cols[:3]:  # Show first 3 numeric columns
                            if col != 'Tahun':
                                avg_val = df[col].mean()
                                st.metric(f"Rata-rata {col}", f"{format_number(avg_val, 'currency')} ribu USD")
                
                with col2:
                    st.markdown("#### 🔍 Insights Data")
                    
                    if dataset_key == "ekspor_komoditi":
                        insights = [
                            "Migas mendominasi ekspor Aceh",
                            "Tren penurunan ekspor 2009-2013",
                            "Pertanian menunjukkan pertumbuhan signifikan"
                        ]
                    elif dataset_key == "impor_negara":
                        insights = [
                            "Tiongkok dan Singapura sebagai mitra utama",
                            "Konsentrasi impor dari Asia Tenggara",
                            "Fluktuasi tinggi berdasarkan kondisi global"
                        ]
                    elif dataset_key == "neraca_perdagangan":
                        insights = [
                            "Surplus perdagangan konsisten sejak 1965",
                            "Puncak surplus era boom migas",
                            "Resiliensi ekonomi yang berorientasi ekspor"
                        ]
                    else:
                        insights = [
                            "Data menunjukkan pola perdagangan yang dinamis",
                            "Fluktuasi terkait kondisi ekonomi global",
                            "Potensi untuk diversifikasi lebih lanjut"
                        ]
                    
                    for insight in insights:
                        st.markdown(f"• {insight}")
        
        else:
            st.error(f"Dataset '{selected_dataset}' tidak tersedia.")

# Function to update the SECTORS configuration in main_app.py
def update_perdagangan_sector():
    """
    Update the SECTORS configuration in main_app.py:
    
    "perdagangan": {
        "name": "Perdagangan",
        "icon": "🛒",
        "description": "Aktivitas perdagangan dan komersial",
        "available": True  # Change from False to True
    }
    """
    pass

# Add to main() function in main_app.py
def update_main_function_for_perdagangan():
    """
    Add this condition to your main() function:
    
    elif st.session_state.selected_sector == "perdagangan":
        show_perdagangan()
    """
    pass

# Add this function to your main_app.py file

@st.cache_data
def load_inflasi_harga_datasets():
    """Load Inflasi & Harga datasets from uploaded documents"""
    datasets = {}
    
    # 1. Historical Inflation Data (1980-2013)
    inflasi_historis_data = [
        [1980, 21.33, 21.25, None, 15.97],
        [1981, 5.94, 6.20, None, 7.09],
        [1982, 3.26, 16.87, None, 9.69],
        [1983, 19.06, 12.84, None, 11.46],
        [1984, 8.74, 5.86, None, 8.76],
        [1985, -0.48, 2.93, None, 4.31],
        [1986, 14.47, 18.54, None, 8.83],
        [1987, 8.95, 9.18, None, 8.90],
        [1988, 4.85, 10.62, None, 5.47],
        [1989, 8.25, 6.19, None, 5.97],
        [1990, 8.85, 10.12, None, 9.53],
        [1991, 6.87, 8.42, None, 9.52],
        [1992, 2.24, 5.15, None, 4.94],
        [1993, 9.83, 9.49, None, 9.77],
        [1994, 8.97, 13.27, None, 9.24],
        [1995, 9.16, 11.16, None, 8.64],
        [1996, 6.66, 3.45, None, 6.47],
        [1997, 9.90, 8.44, None, 11.05],
        [1998, 79.01, 79.66, None, 77.63],
        [1999, 5.57, 6.61, 4.98, 2.01],
        [2000, 10.57, 8.73, 9.59, 1.94],
        [2001, 16.60, 11.67, 14.03, 12.55],
        [2002, 10.14, 10.99, 10.55, 10.03],
        [2003, 3.50, 4.53, 4.03, None],
        [2004, 6.97, 7.36, 7.08, 6.40],
        [2005, 41.11, 17.57, 34.88, 17.11],
        [2006, 9.54, 11.47, 9.98, 6.60],
        [2007, 11.00, 4.18, 9.41, 6.59],
        [2008, 10.27, 13.78, 11.92, 11.06],
        [2009, 3.50, 3.96, 3.72, 2.78],
        [2010, 4.64, 7.19, 5.86, 6.96],
        [2011, 3.32, 3.55, 3.43, 3.79],
        [2012, 0.66, 0.39, 0.22, 1.79],
        [2013, 6.39, 8.27, 7.31, 8.38]
    ]
    
    datasets['inflasi_historis'] = pd.DataFrame(inflasi_historis_data, 
                                               columns=['Tahun', 'Banda_Aceh', 'Lhokseumawe', 'Aceh', 'Nasional'])
    
    # 2. Detailed Inflation by Expenditure Groups (2013-2014)
    # Sample key data points for visualization
    inflasi_kelompok_data = [
        ['2013', 'Banda Aceh', 11.82, 5.05, 2.86, -0.82, 2.90, 4.33, 10.85, 6.39],
        ['2013', 'Lhokseumawe', 18.39, 2.75, 2.60, 0.25, 2.26, 4.64, 10.81, 8.27],
        ['2013', 'Aceh', 15.04, 3.94, 2.73, -0.36, 2.63, 4.49, 10.83, 7.31],
        ['2013', 'Nasional', 11.35, 7.45, 6.22, 0.52, 3.70, 3.91, 15.36, 8.38],
        ['Jan 2014', 'Banda Aceh', 4.98, 0.08, 2.00, 0.80, 0.13, 0.41, 0.68, 1.85],
        ['Jan 2014', 'Lhokseumawe', 5.89, 0.57, 2.40, 0.59, 0.36, 0.23, 0.24, 2.42],
        ['Jan 2014', 'Aceh', 4.76, 0.68, 2.71, 1.32, 0.57, 0.86, 0.56, 2.23],
        ['Feb 2014', 'Banda Aceh', -2.15, 0.15, -0.21, 0.44, 0.00, 0.33, 0.04, -0.45],
        ['Mar 2014', 'Banda Aceh', -3.43, 0.40, 0.26, 0.41, 0.10, 0.86, 0.10, -0.52],
        ['Jun 2014', 'Aceh', 0.28, 0.10, 0.25, 0.91, 0.04, 0.31, 0.14, 0.27]
    ]
    
    datasets['inflasi_kelompok'] = pd.DataFrame(inflasi_kelompok_data, 
                                               columns=['Periode', 'Lokasi', 'Bahan_Makanan', 'Makanan_Jadi', 
                                                       'Perumahan', 'Sandang', 'Kesehatan', 'Pendidikan', 
                                                       'Rekreasi', 'Inflasi_Umum'])
    
    # 3. Farmer Terms of Trade (2008-2013)
    ntp_data = [
        [2008, 110.38, 111.99, 98.64],
        [2009, 118.42, 118.70, 99.76],
        [2010, 127.51, 122.45, 104.12],
        [2011, 133.38, 127.88, 104.30],
        [2012, 137.16, 131.71, 104.14],
        [2013, 141.46, 137.13, 103.16]
    ]
    
    datasets['ntp'] = pd.DataFrame(ntp_data, 
                                  columns=['Tahun', 'Indeks_Terima', 'Indeks_Bayar', 'NTP'])
    
    # 4. Farmer Price Index by Subsector (2008-2013)
    it_subsektor_data = [
        [2008, 106.66, 110.81, 117.78, 109.87, 110.40, 110.38],
        [2009, 120.89, 117.81, 123.08, 115.89, 116.02, 118.42],
        [2010, 132.04, 126.97, 142.16, 120.36, 121.87, 127.51],
        [2011, 140.61, 132.53, 149.96, 123.56, 127.22, 133.38],
        [2012, 150.72, 133.41, 149.47, 127.21, 128.46, 137.16],
        [2013, 156.69, 137.33, 153.17, 130.73, 129.26, 141.46]
    ]
    
    datasets['it_subsektor'] = pd.DataFrame(it_subsektor_data, 
                                           columns=['Tahun', 'Tanaman_Pangan', 'Hortikultura', 
                                                   'Perkebunan_Rakyat', 'Peternakan', 'Perikanan', 'IT_Total'])
    
    # 5. Construction Cost Index (2003-2014)
    ikk_data = [
        [2003, 96.27],
        [2005, 119.10],
        [2006, 143.51],
        [2007, 163.60],
        [2008, 197.60],
        [2009, 221.00],
        [2010, 92.45],
        [2011, 92.56],
        [2012, 91.23],
        [2013, 91.61],
        [2014, 93.54]
    ]
    
    datasets['ikk'] = pd.DataFrame(ikk_data, columns=['Tahun', 'IKK'])
    
    # 6. Construction Cost Index by Regency 2014
    ikk_kab_data = [
        ['Simeulue', 112.83],
        ['Aceh Singkil', 106.38],
        ['Aceh Selatan', 89.93],
        ['Aceh Tenggara', 91.98],
        ['Aceh Timur', 101.12],
        ['Aceh Tengah', 103.33],
        ['Aceh Barat', 100.28],
        ['Aceh Besar', 91.00],
        ['Pidie', 92.18],
        ['Bireuen', 101.25],
        ['Aceh Utara', 108.34],
        ['Aceh Barat Daya', 96.46],
        ['Gayo Lues', 89.12],
        ['Aceh Tamiang', 96.75],
        ['Nagan Raya', 119.46],
        ['Aceh Jaya', 98.82],
        ['Bener Meriah', 99.66],
        ['Pidie Jaya', 93.21],
        ['Banda Aceh', 102.26],
        ['Sabang', 99.30],
        ['Langsa', 93.06],
        ['Lhokseumawe', 105.71],
        ['Subulussalam', 75.83]
    ]
    
    datasets['ikk_kab'] = pd.DataFrame(ikk_kab_data, columns=['Kabupaten_Kota', 'IKK'])
    
    # 7. Monthly Inflation Trends (2014) - Sample data
    inflasi_bulanan_data = [
        ['Jan 2014', 2.23, 1.07],
        ['Feb 2014', -0.84, 0.26],
        ['Mar 2014', -0.65, 0.08],
        ['Apr 2014', -0.08, -0.02],
        ['May 2014', 0.80, 0.16],
        ['Jun 2014', 0.27, 0.43],
        ['Jul 2014', 0.73, 0.93],
        ['Aug 2014', 0.21, 0.47],
        ['Sep 2014', 0.49, 0.27],
        ['Oct 2014', 0.48, 0.47],
        ['Nov 2014', 1.35, 1.50]
    ]
    
    datasets['inflasi_bulanan'] = pd.DataFrame(inflasi_bulanan_data, 
                                              columns=['Bulan', 'Aceh', 'Nasional'])
    
    return datasets

def show_inflasi_harga():
    """Enhanced Inflasi & Harga dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">💰 Sektor Inflasi dan Harga Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Inflasi, Nilai Tukar Petani, dan Indeks Harga (1980-2014)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the datasets
    datasets = load_inflasi_harga_datasets()
    
    # Tabs for different price indicators (7 datasets = 5 main tabs)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Inflasi Historis", "🌾 Nilai Tukar Petani", "🏗️ Indeks Konstruksi", "📋 Data Tables"])
    
    with tab1:
        # Key inflation metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'inflasi_historis' in datasets:
                inflasi_2013 = datasets['inflasi_historis'][datasets['inflasi_historis']['Tahun'] == 2013]['Aceh'].iloc[0]
                st.markdown(create_metric_card("📈", f"{inflasi_2013:.2f}%", "Inflasi Aceh 2013", "Year-on-Year"), unsafe_allow_html=True)
        
        with col2:
            if 'ntp' in datasets:
                ntp_2013 = datasets['ntp'][datasets['ntp']['Tahun'] == 2013]['NTP'].iloc[0]
                st.markdown(create_metric_card("🌾", f"{ntp_2013:.2f}", "Nilai Tukar Petani", "2013"), unsafe_allow_html=True)
        
        with col3:
            if 'ikk' in datasets:
                ikk_2014 = datasets['ikk'][datasets['ikk']['Tahun'] == 2014]['IKK'].iloc[0]
                st.markdown(create_metric_card("🏗️", f"{ikk_2014:.2f}", "Indeks Konstruksi", "2014"), unsafe_allow_html=True)
        
        with col4:
            if 'inflasi_historis' in datasets:
                avg_inflasi = datasets['inflasi_historis']['Aceh'].mean()
                st.markdown(create_metric_card("📊", f"{avg_inflasi:.2f}%", "Rata-rata Inflasi", "1999-2013"), unsafe_allow_html=True)
        
        # Overview visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'inflasi_historis' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Perbandingan Inflasi Regional</h3>', unsafe_allow_html=True)
                
                # Filter data with complete records
                inflasi_clean = datasets['inflasi_historis'].dropna(subset=['Aceh', 'Nasional'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=inflasi_clean['Tahun'], y=inflasi_clean['Aceh'],
                                       name='Aceh', line=dict(color='#1e40af', width=3),
                                       mode='lines+markers'))
                fig.add_trace(go.Scatter(x=inflasi_clean['Tahun'], y=inflasi_clean['Nasional'],
                                       name='Nasional', line=dict(color='#dc2626', width=3),
                                       mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Inflasi (%)",
                                title="")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'ntp' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🌾 Tren Nilai Tukar Petani</h3>', unsafe_allow_html=True)
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Scatter(x=datasets['ntp']['Tahun'], y=datasets['ntp']['Indeks_Terima'],
                             name="Indeks Diterima", line=dict(color='#10b981', width=3)),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=datasets['ntp']['Tahun'], y=datasets['ntp']['Indeks_Bayar'],
                             name="Indeks Dibayar", line=dict(color='#f59e0b', width=3)),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=datasets['ntp']['Tahun'], y=datasets['ntp']['NTP'],
                             name="NTP", line=dict(color='#ef4444', width=4)),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Tahun")
                fig.update_yaxes(title_text="Indeks", secondary_y=False)
                fig.update_yaxes(title_text="NTP", secondary_y=True)
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Sectoral price analysis
        if 'it_subsektor' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🏭 Indeks Harga Subsektor Pertanian (2008-2013)</h3>', unsafe_allow_html=True)
            
            fig = go.Figure()
            colors = ['#1e40af', '#dc2626', '#10b981', '#f59e0b', '#8b5cf6']
            subsectors = ['Tanaman_Pangan', 'Hortikultura', 'Perkebunan_Rakyat', 'Peternakan', 'Perikanan']
            
            for i, sector in enumerate(subsectors):
                fig.add_trace(go.Scatter(
                    x=datasets['it_subsektor']['Tahun'], 
                    y=datasets['it_subsektor'][sector],
                    name=sector.replace('_', ' '),
                    line=dict(color=colors[i], width=3),
                    mode='lines+markers'
                ))
            
            fig.update_layout(height=500,
                            xaxis_title="Tahun", yaxis_title="Indeks",
                            title="")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📈 Analisis Inflasi Historis (1980-2013)</h2>', unsafe_allow_html=True)
        
        if 'inflasi_historis' in datasets:
            # Historical inflation metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                max_inflasi = datasets['inflasi_historis']['Aceh'].max()
                max_year = datasets['inflasi_historis'].loc[datasets['inflasi_historis']['Aceh'].idxmax(), 'Tahun']
                st.markdown(create_metric_card("🔥", f"{max_inflasi:.2f}%", "Inflasi Tertinggi", f"Tahun {int(max_year)}"), unsafe_allow_html=True)
            
            with col2:
                min_inflasi = datasets['inflasi_historis']['Aceh'].min()
                min_year = datasets['inflasi_historis'].loc[datasets['inflasi_historis']['Aceh'].idxmin(), 'Tahun']
                st.markdown(create_metric_card("❄️", f"{min_inflasi:.2f}%", "Inflasi Terendah", f"Tahun {int(min_year)}"), unsafe_allow_html=True)
            
            with col3:
                volatility = datasets['inflasi_historis']['Aceh'].std()
                st.markdown(create_metric_card("📊", f"{volatility:.2f}%", "Volatilitas Inflasi", "Standar Deviasi"), unsafe_allow_html=True)
            
            with col4:
                recent_avg = datasets['inflasi_historis'].tail(5)['Aceh'].mean()
                st.markdown(create_metric_card("⏰", f"{recent_avg:.2f}%", "Rata-rata 2009-2013", "5 Tahun Terakhir"), unsafe_allow_html=True)
            
            # Historical analysis charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Evolusi Inflasi Kota-Kota Utama</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['inflasi_historis']['Tahun'], 
                                       y=datasets['inflasi_historis']['Banda_Aceh'],
                                       name='Banda Aceh', line=dict(color='#1e40af', width=2)))
                fig.add_trace(go.Scatter(x=datasets['inflasi_historis']['Tahun'], 
                                       y=datasets['inflasi_historis']['Lhokseumawe'],
                                       name='Lhokseumawe', line=dict(color='#dc2626', width=2)))
                
                # Highlight crisis periods
                fig.add_vrect(x0=1997, x1=1999, fillcolor="red", opacity=0.2, 
                            annotation_text="Krisis Asia", annotation_position="top left")
                fig.add_vrect(x0=2005, x1=2006, fillcolor="orange", opacity=0.2,
                            annotation_text="Krisis BBM", annotation_position="top right")
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Inflasi (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Distribusi Inflasi per Dekade</h3>', unsafe_allow_html=True)
                
                # Create decade analysis
                inflasi_copy = datasets['inflasi_historis'].copy()
                inflasi_copy['Dekade'] = (inflasi_copy['Tahun'] // 10) * 10
                dekade_stats = inflasi_copy.groupby('Dekade')['Aceh'].agg(['mean', 'std', 'min', 'max']).reset_index()
                dekade_stats['Dekade'] = dekade_stats['Dekade'].astype(str) + 's'
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=dekade_stats['Dekade'], y=dekade_stats['mean'],
                                   name='Rata-rata', marker_color='#3b82f6'))
                fig.add_trace(go.Scatter(x=dekade_stats['Dekade'], y=dekade_stats['max'],
                                       name='Maksimum', mode='markers', marker_color='#ef4444',
                                       marker_size=10))
                
                fig.update_layout(height=400,
                                xaxis_title="Dekade", yaxis_title="Inflasi (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Monthly inflation patterns (2014)
            if 'inflasi_bulanan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📅 Pola Inflasi Bulanan 2014</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=datasets['inflasi_bulanan']['Bulan'], 
                                   y=datasets['inflasi_bulanan']['Aceh'],
                                   name='Aceh', marker_color='#1e40af'))
                fig.add_trace(go.Scatter(x=datasets['inflasi_bulanan']['Bulan'], 
                                       y=datasets['inflasi_bulanan']['Nasional'],
                                       name='Nasional', line=dict(color='#dc2626', width=3),
                                       mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Bulan", yaxis_title="Inflasi (%)",
                                xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Inflation insights
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h4>🔍 Analisis & Insights Inflasi Historis</h4>', unsafe_allow_html=True)
            
            insights_inflasi = [
                f"🔥 **Hiperinflasi 1998**: Krisis moneter menyebabkan inflasi ekstrem {max_inflasi:.1f}% akibat depresiasi rupiah",
                f"❄️ **Deflasi 1985**: Pernah mengalami deflasi {abs(min_inflasi):.1f}% terkait penurunan harga komoditas",
                f"📊 **Volatilitas Tinggi**: Standar deviasi {volatility:.1f}% menunjukkan fluktuasi inflasi yang signifikan",
                f"⚡ **Shock 2005**: Inflasi {datasets['inflasi_historis'][datasets['inflasi_historis']['Tahun']==2005]['Aceh'].iloc[0]:.1f}% akibat kenaikan harga BBM bersubsidi",
                f"🎯 **Stabilisasi Modern**: Rata-rata inflasi 2009-2013 hanya {recent_avg:.1f}% menunjukkan stabilitas makroekonomi",
                f"🏙️ **Perbedaan Regional**: Lhokseumawe umumnya mengalami inflasi lebih tinggi dibanding Banda Aceh",
                f"🌍 **Korelasi Global**: Inflasi Aceh berkorelasi dengan tren nasional namun dengan volatilitas lebih tinggi",
                f"📈 **Pola Siklus**: Inflasi mengikuti siklus ekonomi global dengan periode tinggi di era 1980an dan krisis"
            ]
            
            for insight in insights_inflasi:
                st.markdown(f"- {insight}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🌾 Analisis Nilai Tukar Petani & Harga Pertanian</h2>', unsafe_allow_html=True)
        
        # NTP metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ntp' in datasets:
                ntp_trend = datasets['ntp']['NTP'].iloc[-1] - datasets['ntp']['NTP'].iloc[0]
                st.markdown(create_metric_card("📈", f"{ntp_trend:+.2f}", "Perubahan NTP", "2008-2013"), unsafe_allow_html=True)
        
        with col2:
            if 'ntp' in datasets:
                avg_ntp = datasets['ntp']['NTP'].mean()
                st.markdown(create_metric_card("⚖️", f"{avg_ntp:.2f}", "Rata-rata NTP", "2008-2013"), unsafe_allow_html=True)
        
        with col3:
            if 'ntp' in datasets:
                favorable_years = len(datasets['ntp'][datasets['ntp']['NTP'] > 100])
                st.markdown(create_metric_card("✅", f"{favorable_years}/6", "Tahun Menguntungkan", "NTP > 100"), unsafe_allow_html=True)
        
        with col4:
            if 'it_subsektor' in datasets:
                best_sector = datasets['it_subsektor'].iloc[-1][['Tanaman_Pangan', 'Hortikultura', 'Perkebunan_Rakyat']].idxmax()
                st.markdown(create_metric_card("🏆", best_sector.replace('_', ' '), "Sektor Terbaik", "2013"), unsafe_allow_html=True)
        
        # NTP analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'ntp' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Komponen Nilai Tukar Petani</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=datasets['ntp']['Tahun'], y=datasets['ntp']['Indeks_Terima'],
                                   name='Indeks Diterima', marker_color='#10b981', opacity=0.8))
                fig.add_trace(go.Bar(x=datasets['ntp']['Tahun'], y=datasets['ntp']['Indeks_Bayar'],
                                   name='Indeks Dibayar', marker_color='#ef4444', opacity=0.8))
                
                fig.update_layout(height=400, barmode='group',
                                xaxis_title="Tahun", yaxis_title="Indeks")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'ntp' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">⚖️ Tren Nilai Tukar Petani</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['ntp']['Tahun'], y=datasets['ntp']['NTP'],
                                       mode='lines+markers', line=dict(color='#3b82f6', width=4),
                                       marker=dict(size=8)))
                fig.add_hline(y=100, line_dash="dash", annotation_text="Break Even (NTP=100)")
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="NTP")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Sectoral price index analysis
        if 'it_subsektor' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🏭 Perbandingan Indeks Harga Subsektor</h3>', unsafe_allow_html=True)
            
            # Create subsektor comparison for latest year
            latest_data = datasets['it_subsektor'].iloc[-1]
            sectors = ['Tanaman_Pangan', 'Hortikultura', 'Perkebunan_Rakyat', 'Peternakan', 'Perikanan']
            values = [latest_data[sector] for sector in sectors]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[s.replace('_', ' ') for s in sectors],
                y=values,
                marker_color=['#1e40af', '#dc2626', '#10b981', '#f59e0b', '#8b5cf6']
            ))
            
            fig.update_layout(height=400,
                            xaxis_title="Subsektor", yaxis_title="Indeks (2013)",
                            xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Farmer welfare insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Kesejahteraan Petani</h4>', unsafe_allow_html=True)
        
        if 'ntp' in datasets:
            ntp_2013 = datasets['ntp'][datasets['ntp']['Tahun'] == 2013]['NTP'].iloc[0]
            best_year = datasets['ntp'].loc[datasets['ntp']['NTP'].idxmax(), 'Tahun']
            best_ntp = datasets['ntp']['NTP'].max()
            
            insights_ntp = [
                f"📈 **Tren Positif**: NTP meningkat dari 98.64 (2008) menjadi {ntp_2013:.2f} (2013), menunjukkan perbaikan kesejahteraan",
                f"🏆 **Puncak Kesejahteraan**: NTP tertinggi {best_ntp:.2f} dicapai pada tahun {int(best_year)}",
                f"⚖️ **Kondisi Menguntungkan**: NTP > 100 selama 4 dari 6 tahun, menunjukkan daya beli petani yang membaik",
                f"🌾 **Perkebunan Unggul**: Subsektor perkebunan rakyat menunjukkan indeks tertinggi (153.17 di 2013)",
                f"🐄 **Stabilitas Peternakan**: Sektor peternakan menunjukkan pertumbuhan paling stabil dan konsisten",
                f"📊 **Gap Harga**: Selisih indeks yang diterima vs dibayar petani menunjukkan margin kesejahteraan yang tipis",
                f"🎯 **Potensi Peningkatan**: Masih ada ruang untuk meningkatkan NTP melalui peningkatan produktivitas dan efisiensi",
                f"💪 **Resiliensi**: Petani Aceh menunjukkan kemampuan adaptasi yang baik terhadap fluktuasi harga"
            ]
            
            for insight in insights_ntp:
                st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🏗️ Analisis Indeks Kemahalan Konstruksi</h2>', unsafe_allow_html=True)
        
        # Construction cost metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ikk' in datasets:
                ikk_2014 = datasets['ikk'][datasets['ikk']['Tahun'] == 2014]['IKK'].iloc[0]
                st.markdown(create_metric_card("🏗️", f"{ikk_2014:.2f}", "IKK Aceh 2014", "Indeks"), unsafe_allow_html=True)
        
        with col2:
            if 'ikk_kab' in datasets:
                max_ikk_kab = datasets['ikk_kab']['IKK'].max()
                max_kab = datasets['ikk_kab'].loc[datasets['ikk_kab']['IKK'].idxmax(), 'Kabupaten_Kota']
                st.markdown(create_metric_card("📈", f"{max_ikk_kab:.2f}", "IKK Tertinggi", max_kab), unsafe_allow_html=True)
        
        with col3:
            if 'ikk_kab' in datasets:
                min_ikk_kab = datasets['ikk_kab']['IKK'].min()
                min_kab = datasets['ikk_kab'].loc[datasets['ikk_kab']['IKK'].idxmin(), 'Kabupaten_Kota']
                st.markdown(create_metric_card("📉", f"{min_ikk_kab:.2f}", "IKK Terendah", min_kab), unsafe_allow_html=True)
        
        with col4:
            if 'ikk_kab' in datasets:
                avg_ikk = datasets['ikk_kab']['IKK'].mean()
                st.markdown(create_metric_card("📊", f"{avg_ikk:.2f}", "Rata-rata IKK", "Semua Kab/Kota"), unsafe_allow_html=True)
        
        # Construction cost analysis
        col1, col2 = st.columns(2)
        
        with col1:
            if 'ikk' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Evolusi Indeks Kemahalan Konstruksi</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['ikk'], x='Tahun', y='IKK',
                            markers=True,
                            color_discrete_sequence=['#1e40af'],
                            title="")
                fig.update_traces(line=dict(width=4), marker=dict(size=8))
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="IKK")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'ikk_kab' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🗺️ IKK Berdasarkan Kabupaten/Kota 2014</h3>', unsafe_allow_html=True)
                
                # Sort for better visualization
                ikk_sorted = datasets['ikk_kab'].sort_values('IKK', ascending=True).tail(15)
                
                fig = px.bar(ikk_sorted, x='IKK', y='Kabupaten_Kota',
                           orientation='h',
                           color='IKK',
                           color_continuous_scale='Blues',
                           title="")
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Regional IKK distribution
        if 'ikk_kab' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📊 Distribusi IKK Regional</h3>', unsafe_allow_html=True)
            
            # Create categories
            ikk_categories = datasets['ikk_kab'].copy()
            ikk_categories['Kategori'] = pd.cut(ikk_categories['IKK'], 
                                              bins=[0, 90, 100, 110, float('inf')],
                                              labels=['Rendah (<90)', 'Sedang (90-100)', 'Tinggi (100-110)', 'Sangat Tinggi (>110)'])
            
            category_counts = ikk_categories['Kategori'].value_counts()
            
            fig = px.pie(values=category_counts.values, names=category_counts.index,
                        color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444', '#7c3aed'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Construction cost insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Kemahalan Konstruksi</h4>', unsafe_allow_html=True)
        
        if 'ikk' in datasets and 'ikk_kab' in datasets:
            insights_ikk = [
                f"🏗️ **Stabilitas Recent**: IKK provinsi {ikk_2014:.2f} pada 2014 menunjukkan stabilisasi setelah fluktuasi 2008-2009",
                f"📈 **Disparitas Regional**: Gap IKK antara {max_kab} ({max_ikk_kab:.2f}) dan {min_kab} ({min_ikk_kab:.2f}) mencapai {max_ikk_kab-min_ikk_kab:.2f} poin",
                f"🌊 **Efek Tsunami**: Lonjakan IKK 2008-2009 terkait rekonstruksi pasca tsunami dengan puncak 221.00",
                f"📊 **Rebase 2010**: Penurunan drastis IKK 2010 akibat pergantian tahun dasar metodologi perhitungan",
                f"🏝️ **Pulau Terpencil**: Simeulue dan Nagan Raya menunjukkan IKK tertinggi karena biaya transportasi material",
                f"🏙️ **Urban vs Rural**: Kota-kota besar relatif lebih efisien dibanding kabupaten terpencil",
                f"🎯 **Mayoritas Normal**: {len(ikk_categories[ikk_categories['IKK'] <= 100])}/{len(ikk_categories)} kabupaten/kota memiliki IKK di bawah 100",
                f"⚖️ **Implikasi Fiskal**: Variasi IKK signifikan untuk perencanaan anggaran pembangunan infrastruktur regional"
            ]
            
            for insight in insights_ikk:
                st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📋 Data Tables & Export</h2>', unsafe_allow_html=True)
        
        # Dataset selector
        dataset_options = {
            "Inflasi Historis (1980-2013)": "inflasi_historis",
            "Inflasi Bulanan (2014)": "inflasi_bulanan",
            "Inflasi Kelompok Pengeluaran": "inflasi_kelompok",
            "Nilai Tukar Petani": "ntp",
            "Indeks Subsektor Pertanian": "it_subsektor",
            "Indeks Kemahalan Konstruksi": "ikk",
            "IKK Kabupaten/Kota": "ikk_kab"
        }
        
        selected_dataset = st.selectbox("Pilih Dataset untuk Ditampilkan:", 
                                      list(dataset_options.keys()))
        
        dataset_key = dataset_options[selected_dataset]
        
        if dataset_key in datasets:
            df = datasets[dataset_key]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"#### 📊 {selected_dataset}")
                st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
            
            with col2:
                # Download button
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"aceh_inflasi_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                show_summary = st.checkbox("Tampilkan Ringkasan", value=True)
            
            # Display data
            st.dataframe(df, use_container_width=True, height=400)
            
            if show_summary:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📈 Statistik Dasar")
                    if 'Tahun' in df.columns:
                        st.metric("Periode Data", f"{df['Tahun'].min()}-{df['Tahun'].max()}")
                    
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        for col in numeric_cols[:3]:  # Show first 3 numeric columns
                            if col != 'Tahun':
                                avg_val = df[col].mean()
                                if 'inflasi' in dataset_key.lower() or 'ntp' in dataset_key.lower():
                                    st.metric(f"Rata-rata {col}", f"{avg_val:.2f}{'%' if 'inflasi' in col.lower() else ''}")
                                else:
                                    st.metric(f"Rata-rata {col}", f"{avg_val:.2f}")
                
                with col2:
                    st.markdown("#### 🔍 Insights Data")
                    
                    if dataset_key == "inflasi_historis":
                        insights = [
                            "Periode hiperinflasi 1998 sebagai outlier ekstrem",
                            "Stabilitas makroekonomi pasca 2010",
                            "Korelasi dengan tren inflasi nasional"
                        ]
                    elif dataset_key == "ntp":
                        insights = [
                            "NTP di atas 100 menunjukkan kondisi menguntungkan petani",
                            "Tren peningkatan kesejahteraan petani 2008-2013",
                            "Fluktuasi mengikuti dinamika harga komoditas"
                        ]
                    elif dataset_key == "ikk":
                        insights = [
                            "Lonjakan signifikan era rekonstruksi pasca tsunami",
                            "Stabilisasi IKK setelah pergantian metodologi",
                            "Disparitas regional yang signifikan"
                        ]
                    else:
                        insights = [
                            "Data menunjukkan dinamika harga yang kompleks",
                            "Pola inflasi dipengaruhi faktor eksternal",
                            "Tren jangka panjang menuju stabilitas"
                        ]
                    
                    for insight in insights:
                        st.markdown(f"• {insight}")
        
        else:
            st.error(f"Dataset '{selected_dataset}' tidak tersedia.")

# Update the SECTORS configuration in main_app.py
def update_inflasi_harga_sector():
    """
    Update the SECTORS configuration in main_app.py:
    
    "inflasi_harga": {
        "name": "Inflasi dan Harga",
        "icon": "💰",
        "description": "Indeks harga dan tingkat inflasi",
        "available": True  # Change from False to True
    }
    """
    pass

# Add to main() function in main_app.py
def update_main_function_for_inflasi_harga():
    """
    Add this condition to your main() function:
    
    elif st.session_state.selected_sector == "inflasi_harga":
        show_inflasi_harga()
    """
    pass

# Add this function to your main_app.py file

@st.cache_data
def load_penduduk_datasets():
    """Load Penduduk & Ketenagakerjaan datasets from uploaded documents"""
    datasets = {}
    
    # 1. Population by Gender and Density (1956-2013)
    populasi_data = [
        [1956, None, None, 1288810, None, 23],
        [1961, 822165, 806835, 1629000, 101.90, 29],
        [1970, 996687, 978102, 1974789, 101.90, 35],
        [1980, 1314905, 1295623, 2610528, 101.49, 46],
        [1990, 1716994, 1698843, 3415837, 101.07, 60],
        [2000, 1974567, 1954667, 3929234, 101.02, 69],
        [2010, 2248952, 2245458, 4494410, 100.16, 79],
        [2013, 2397194, 2394730, 4791924, 100.10, 84]
    ]
    
    datasets['populasi'] = pd.DataFrame(populasi_data, 
                                       columns=['Tahun', 'Laki_laki', 'Perempuan', 'Total', 'Sex_Ratio', 'Kepadatan'])
    
    # 2. Labor Force Participation (1971-2013)
    ketenagakerjaan_data = [
        [1971, 644319, 68565, 712884, 1078626, 1791510, 9.62, 39.79],
        [1980, 832520, 13896, 846416, 959557, 1805973, 1.64, 46.87],
        [1990, 1275053, 36904, 1311957, 1152795, 2464752, 2.81, 53.23],
        [2000, 1452258, 149652, 1601910, 990322, 2592232, 9.34, 61.80],
        [2007, 1570761, 171424, 1742185, 1062423, 2804608, 9.84, 62.12],
        [2010, 1776254, 162265, 1938519, 1130131, 3068650, 8.37, 63.17],
        [2013, 1824586, 209521, 2034107, 1242836, 3276943, 10.30, 62.07]
    ]
    
    datasets['ketenagakerjaan'] = pd.DataFrame(ketenagakerjaan_data, 
                                              columns=['Tahun', 'Bekerja', 'Pengangguran', 'Angkatan_Kerja', 
                                                      'Bukan_Angkatan_Kerja', 'Total_Populasi', 'TPT', 'TPAK'])
    
    # 3. Unemployment by Education Level (1971-2013)
    pengangguran_pendidikan_data = [
        [1971, 2.10, 11.00, 11.70, 25.30, 2.60, 9.62],
        [1980, 1.10, 1.70, 1.80, 3.90, 0.40, 2.81],
        [1990, 1.10, 1.60, 3.30, 8.10, 7.90, 2.81],
        [1998, 4.80, 7.00, 14.50, 35.50, 34.70, 12.32],
        [2007, 6.42, 6.80, 8.85, 16.28, 8.23, 9.84],
        [2010, 2.89, 4.70, 6.65, 14.51, 10.15, 8.37],
        [2013, 3.67, 5.70, 10.01, 16.21, 10.29, 10.30]
    ]
    
    datasets['pengangguran_pendidikan'] = pd.DataFrame(pengangguran_pendidikan_data, 
                                                       columns=['Tahun', 'Tidak_Sekolah', 'SD', 'SMP', 'SMA', 'PT', 'TPT_Total'])
    
    # 4. Employment by Age Group (1971-2013)
    pekerja_umur_data = [
        [1971, 3.47, 10.47, 25.26, 24.58, 32.49, 3.73],
        [1980, 3.11, 10.63, 27.47, 23.10, 28.63, 7.06],
        [1990, 3.29, 10.39, 27.05, 25.04, 27.21, 7.02],
        [2000, None, 4.10, 25.07, 28.70, 36.04, 6.09],
        [2007, None, 4.10, 25.07, 28.70, 36.04, 6.09],
        [2010, None, 3.67, 25.14, 29.32, 34.97, 6.89],
        [2013, None, 3.41, 23.71, 29.43, 36.60, 6.85]
    ]
    
    datasets['pekerja_umur'] = pd.DataFrame(pekerja_umur_data, 
                                           columns=['Tahun', 'Umur_10_14', 'Umur_15_19', 'Umur_20_29', 
                                                   'Umur_30_39', 'Umur_40_59', 'Umur_60_Plus'])
    
    # 5. Employment by Education Level (1971-2013)
    pekerja_pendidikan_data = [
        [1971, 414122, 149747, 49991, 28497, 1962, 644319],
        [1980, 218862, 309672, 57902, 51468, 4162, 642066],
        [1990, 528197, 387829, 163399, 167635, 27993, 1275053],
        [2000, 172020, 472028, 414806, 372477, 139430, 1570761],
        [2007, 172020, 472028, 414806, 372477, 139430, 1570761],
        [2010, 272232, 419764, 395171, 483689, 205398, 1776254],
        [2013, 222660, 437643, 383632, 537997, 242654, 1824586]
    ]
    
    datasets['pekerja_pendidikan'] = pd.DataFrame(pekerja_pendidikan_data, 
                                                  columns=['Tahun', 'Tidak_Sekolah', 'SD', 'SMP', 'SMA', 'PT', 'Total'])
    
    # 6. Infant Mortality Rate (1971-2010)
    imr_data = [
        [1971, 155, 131, 143],
        [1980, 102, 85, 93],
        [1990, 65, 52, 58],
        [2000, 46, 35, 40],
        [2010, 32, 24, 28]
    ]
    
    datasets['imr'] = pd.DataFrame(imr_data, columns=['Tahun', 'Laki_laki', 'Perempuan', 'Total'])
    
    return datasets

def show_penduduk():
    """Enhanced Penduduk & Ketenagakerjaan dashboard with comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">👥 Sektor Penduduk dan Ketenagakerjaan Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Demografi, Ketenagakerjaan, dan Kesejahteraan Sosial (1956-2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the datasets
    datasets = load_penduduk_datasets()
    
    # Tabs for different demographic aspects (6 datasets = 4 main tabs)
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Demografi", "💼 Ketenagakerjaan", "📋 Data Tables"])
    
    with tab1:
        # Key demographic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'populasi' in datasets:
                populasi_2013 = datasets['populasi'][datasets['populasi']['Tahun'] == 2013]['Total'].iloc[0]
                st.markdown(create_metric_card("👥", format_number(populasi_2013), "Total Populasi 2013", "Jiwa"), unsafe_allow_html=True)
        
        with col2:
            if 'ketenagakerjaan' in datasets:
                tpt_2013 = datasets['ketenagakerjaan'][datasets['ketenagakerjaan']['Tahun'] == 2013]['TPT'].iloc[0]
                st.markdown(create_metric_card("💼", f"{tpt_2013:.1f}%", "Tingkat Pengangguran", "2013"), unsafe_allow_html=True)
        
        with col3:
            if 'ketenagakerjaan' in datasets:
                tpak_2013 = datasets['ketenagakerjaan'][datasets['ketenagakerjaan']['Tahun'] == 2013]['TPAK'].iloc[0]
                st.markdown(create_metric_card("📈", f"{tpak_2013:.1f}%", "Partisipasi Angkatan Kerja", "2013"), unsafe_allow_html=True)
        
        with col4:
            if 'imr' in datasets:
                imr_2010 = datasets['imr'][datasets['imr']['Tahun'] == 2010]['Total'].iloc[0]
                st.markdown(create_metric_card("👶", f"{imr_2010}", "Angka Kematian Bayi", "per 1000 kelahiran (2010)"), unsafe_allow_html=True)
        
        # Overview visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            if 'populasi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">👥 Pertumbuhan Populasi Aceh</h3>', unsafe_allow_html=True)
                
                # Clean data for visualization
                pop_clean = datasets['populasi'].dropna(subset=['Total'])
                
                fig = px.area(pop_clean, x='Tahun', y='Total',
                             color_discrete_sequence=['#1e40af'],
                             title="",
                             labels={'Total': 'Jumlah Penduduk', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'ketenagakerjaan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">💼 Tren Tingkat Pengangguran</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['ketenagakerjaan'], x='Tahun', y='TPT',
                             markers=True,
                             color_discrete_sequence=['#dc2626'],
                             title="",
                             labels={'TPT': 'Tingkat Pengangguran (%)', 'Tahun': 'Tahun'})
                fig.update_traces(line=dict(width=3), marker=dict(size=8))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Employment structure overview + 7th visualization
        col1, col2 = st.columns(2)
        
        with col1:
            if 'pekerja_pendidikan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🎓 Struktur Pekerja Berdasarkan Pendidikan (2013)</h3>', unsafe_allow_html=True)
                
                latest_employment = datasets['pekerja_pendidikan'][datasets['pekerja_pendidikan']['Tahun'] == 2013].iloc[0]
                education_data = {
                    'Pendidikan': ['Tidak/Belum Sekolah', 'SD', 'SMP', 'SMA', 'Perguruan Tinggi'],
                    'Jumlah': [latest_employment['Tidak_Sekolah'], latest_employment['SD'], 
                              latest_employment['SMP'], latest_employment['SMA'], latest_employment['PT']]
                }
                education_df = pd.DataFrame(education_data)
                
                fig = px.bar(education_df, x='Pendidikan', y='Jumlah',
                            color='Jumlah',
                            color_continuous_scale='Blues',
                            title="",
                            labels={'Jumlah': 'Jumlah Pekerja', 'Pendidikan': 'Tingkat Pendidikan'})
                fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # 7th Visualization: Labor Force Participation Rate Trend
            if 'ketenagakerjaan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Tren Tingkat Partisipasi Angkatan Kerja</h3>', unsafe_allow_html=True)
                
                fig = px.area(datasets['ketenagakerjaan'], x='Tahun', y='TPAK',
                             color_discrete_sequence=['#10b981'],
                             title="",
                             labels={'TPAK': 'TPAK (%)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">👥 Analisis Demografi Mendalam</h2>', unsafe_allow_html=True)
        
        # Demographic metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'populasi' in datasets:
                growth_rate = ((datasets['populasi'][datasets['populasi']['Tahun'] == 2013]['Total'].iloc[0] - 
                               datasets['populasi'][datasets['populasi']['Tahun'] == 1956]['Total'].iloc[0]) / 
                               datasets['populasi'][datasets['populasi']['Tahun'] == 1956]['Total'].iloc[0]) * 100
                st.markdown(create_metric_card("📈", f"{growth_rate:.0f}%", "Pertumbuhan Total", "1956-2013"), unsafe_allow_html=True)
        
        with col2:
            if 'populasi' in datasets:
                density_2013 = datasets['populasi'][datasets['populasi']['Tahun'] == 2013]['Kepadatan'].iloc[0]
                st.markdown(create_metric_card("🏘️", f"{density_2013}", "Kepadatan 2013", "jiwa/km²"), unsafe_allow_html=True)
        
        with col3:
            if 'populasi' in datasets:
                sex_ratio_2013 = datasets['populasi'][datasets['populasi']['Tahun'] == 2013]['Sex_Ratio'].iloc[0]
                st.markdown(create_metric_card("⚖️", f"{sex_ratio_2013:.1f}", "Sex Ratio 2013", "Laki-laki per 100 perempuan"), unsafe_allow_html=True)
        
        with col4:
            if 'imr' in datasets:
                imr_decline = datasets['imr'].iloc[0]['Total'] - datasets['imr'].iloc[-1]['Total']
                st.markdown(create_metric_card("📉", f"-{imr_decline}", "Penurunan IMR", "1971-2010"), unsafe_allow_html=True)
        
        # Demographic analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'populasi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">👫 Komposisi Gender Populasi</h3>', unsafe_allow_html=True)
                
                pop_clean = datasets['populasi'].dropna(subset=['Laki_laki', 'Perempuan'])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=pop_clean['Tahun'], y=pop_clean['Laki_laki'],
                                       name='Laki-laki', line=dict(color='#3b82f6', width=3),
                                       mode='lines+markers'))
                fig.add_trace(go.Scatter(x=pop_clean['Tahun'], y=pop_clean['Perempuan'],
                                       name='Perempuan', line=dict(color='#ec4899', width=3),
                                       mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Jumlah Penduduk")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'populasi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🏘️ Kepadatan Penduduk</h3>', unsafe_allow_html=True)
                
                fig = px.bar(datasets['populasi'].dropna(subset=['Kepadatan']), 
                           x='Tahun', y='Kepadatan',
                           color='Kepadatan',
                           color_continuous_scale='Oranges',
                           title="",
                           labels={'Kepadatan': 'Kepadatan (jiwa/km²)', 'Tahun': 'Tahun'})
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Health indicators
        if 'imr' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">👶 Perkembangan Angka Kematian Bayi</h3>', unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=datasets['imr']['Tahun'], y=datasets['imr']['Laki_laki'],
                                   name='Laki-laki', line=dict(color='#3b82f6', width=3),
                                   mode='lines+markers'))
            fig.add_trace(go.Scatter(x=datasets['imr']['Tahun'], y=datasets['imr']['Perempuan'],
                                   name='Perempuan', line=dict(color='#ec4899', width=3),
                                   mode='lines+markers'))
            fig.add_trace(go.Scatter(x=datasets['imr']['Tahun'], y=datasets['imr']['Total'],
                                   name='Total', line=dict(color='#10b981', width=4),
                                   mode='lines+markers'))
            
            fig.update_layout(height=400,
                            xaxis_title="Tahun", yaxis_title="Kematian per 1000 Kelahiran")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Demographic insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Demografi</h4>', unsafe_allow_html=True)
        
        insights_demografi = [
            f"📈 **Pertumbuhan Pesat**: Populasi tumbuh {growth_rate:.0f}% dari 1,3 juta (1956) menjadi 4,8 juta (2013)",
            f"🏘️ **Urbanisasi**: Kepadatan meningkat dari 23 jiwa/km² (1956) menjadi {density_2013} jiwa/km² (2013)",
            f"⚖️ **Keseimbangan Gender**: Sex ratio relatif seimbang di {sex_ratio_2013:.1f}, menunjukkan distribusi gender yang normal",
            f"👶 **Kemajuan Kesehatan**: Angka Kematian Bayi turun drastis {imr_decline} poin dari 143 (1971) menjadi 28 (2010)",
            f"🎯 **Bonus Demografi**: Struktur usia menunjukkan potensi bonus demografi dengan populasi usia produktif yang besar",
            f"📊 **Pola Pertumbuhan**: Pertumbuhan populasi mengikuti tren nasional dengan akselerasi pascakemerdekaan",
            f"🌍 **Standar Internasional**: Penurunan IMR mencerminkan peningkatan layanan kesehatan maternal dan neonatal",
            f"🎗️ **Dampak Tsunami**: Data 2004-2005 menunjukkan dampak tsunami terhadap komposisi demografis"
        ]
        
        for insight in insights_demografi:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">💼 Analisis Ketenagakerjaan Komprehensif</h2>', unsafe_allow_html=True)
        
        # Employment metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ketenagakerjaan' in datasets:
                bekerja_2013 = datasets['ketenagakerjaan'][datasets['ketenagakerjaan']['Tahun'] == 2013]['Bekerja'].iloc[0]
                st.markdown(create_metric_card("💼", format_number(bekerja_2013), "Penduduk Bekerja", "2013"), unsafe_allow_html=True)
        
        with col2:
            if 'pengangguran_pendidikan' in datasets:
                sma_unemployment = datasets['pengangguran_pendidikan'][datasets['pengangguran_pendidikan']['Tahun'] == 2013]['SMA'].iloc[0]
                st.markdown(create_metric_card("🎓", f"{sma_unemployment:.1f}%", "Pengangguran SMA", "2013"), unsafe_allow_html=True)
        
        with col3:
            if 'pekerja_umur' in datasets:
                prime_age = datasets['pekerja_umur'][datasets['pekerja_umur']['Tahun'] == 2013]['Umur_30_39'].iloc[0]
                st.markdown(create_metric_card("👨‍💼", f"{prime_age:.1f}%", "Pekerja Usia 30-39", "Prime Working Age"), unsafe_allow_html=True)
        
        with col4:
            if 'pekerja_pendidikan' in datasets:
                pt_workers = datasets['pekerja_pendidikan'][datasets['pekerja_pendidikan']['Tahun'] == 2013]['PT'].iloc[0]
                st.markdown(create_metric_card("🎓", format_number(pt_workers), "Pekerja Berpendidikan Tinggi", "2013"), unsafe_allow_html=True)
        
        # Employment analysis charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'ketenagakerjaan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Angkatan Kerja vs Bukan Angkatan Kerja</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=datasets['ketenagakerjaan']['Tahun'], 
                                   y=datasets['ketenagakerjaan']['Angkatan_Kerja'],
                                   name='Angkatan Kerja', marker_color='#10b981'))
                fig.add_trace(go.Bar(x=datasets['ketenagakerjaan']['Tahun'], 
                                   y=datasets['ketenagakerjaan']['Bukan_Angkatan_Kerja'],
                                   name='Bukan Angkatan Kerja', marker_color='#ef4444'))
                
                fig.update_layout(height=400, barmode='stack',
                                xaxis_title="Tahun", yaxis_title="Jumlah Penduduk")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if 'pengangguran_pendidikan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🎓 Pengangguran Berdasarkan Pendidikan</h3>', unsafe_allow_html=True)
                
                # Get 2013 data for education unemployment
                unemployment_2013 = datasets['pengangguran_pendidikan'][datasets['pengangguran_pendidikan']['Tahun'] == 2013].iloc[0]
                education_unemployment = {
                    'Tingkat Pendidikan': ['Tidak Sekolah', 'SD', 'SMP', 'SMA', 'Perguruan Tinggi'],
                    'Tingkat Pengangguran': [unemployment_2013['Tidak_Sekolah'], unemployment_2013['SD'],
                                           unemployment_2013['SMP'], unemployment_2013['SMA'], unemployment_2013['PT']]
                }
                unemployment_df = pd.DataFrame(education_unemployment)
                
                fig = px.bar(unemployment_df, x='Tingkat Pendidikan', y='Tingkat Pengangguran',
                           color='Tingkat Pengangguran',
                           color_continuous_scale='Reds',
                           title="",
                           labels={'Tingkat Pengangguran': 'Pengangguran (%)', 'Tingkat Pendidikan': 'Pendidikan'})
                fig.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Age structure of workforce
        if 'pekerja_umur' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">👥 Struktur Usia Pekerja (2013)</h3>', unsafe_allow_html=True)
            
            latest_age_structure = datasets['pekerja_umur'][datasets['pekerja_umur']['Tahun'] == 2013].iloc[0]
            age_data = {
                'Kelompok Usia': ['15-19', '20-29', '30-39', '40-59', '60+'],
                'Persentase': [latest_age_structure['Umur_15_19'], latest_age_structure['Umur_20_29'],
                              latest_age_structure['Umur_30_39'], latest_age_structure['Umur_40_59'],
                              latest_age_structure['Umur_60_Plus']]
            }
            age_df = pd.DataFrame(age_data)
            
            fig = px.pie(age_df, values='Persentase', names='Kelompok Usia',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Employment education trends
        if 'pekerja_pendidikan' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">📈 Tren Pekerja Berdasarkan Pendidikan</h3>', unsafe_allow_html=True)
            
            # Melt data for easier visualization
            education_melt = pd.melt(datasets['pekerja_pendidikan'], 
                                   id_vars=['Tahun'], 
                                   value_vars=['Tidak_Sekolah', 'SD', 'SMP', 'SMA', 'PT'],
                                   var_name='Pendidikan', value_name='Jumlah')
            
            fig = px.line(education_melt, x='Tahun', y='Jumlah', color='Pendidikan',
                         markers=True,
                         title="",
                         labels={'Jumlah': 'Jumlah Pekerja', 'Tahun': 'Tahun'})
            fig.update_traces(line=dict(width=3), marker=dict(size=6))
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Employment insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Ketenagakerjaan</h4>', unsafe_allow_html=True)
        
        insights_kerja = [
            f"💼 **Ekspansi Tenaga Kerja**: Jumlah pekerja tumbuh dari 644 ribu (1971) menjadi {format_number(bekerja_2013)} (2013)",
            f"📈 **Partisipasi Tinggi**: TPAK mencapai {tpak_2013:.1f}% menunjukkan partisipasi angkatan kerja yang solid",
            f"🎓 **Paradoks Pendidikan**: Pengangguran SMA ({sma_unemployment:.1f}%) lebih tinggi dari lulusan SD, menunjukkan skills mismatch",
            f"👨‍💼 **Dominasi Usia Produktif**: Pekerja usia 40-59 tahun mendominasi dengan {datasets['pekerja_umur'][datasets['pekerja_umur']['Tahun'] == 2013]['Umur_40_59'].iloc[0]:.1f}% dari total",
            f"📊 **Transformasi Struktural**: Pekerja berpendidikan tinggi meningkat dari 1.962 (1971) menjadi {format_number(pt_workers)} (2013)",
            f"⚡ **Dampak Krisis**: TPT mencapai puncak 12,32% saat krisis 1998, menunjukkan kerentanan ekonomi",
            f"🎯 **Target Produktif**: Mayoritas pekerja berada di usia prime (20-59 tahun) dengan total 89,74%",
            f"📉 **Penurunan Pekerja Anak**: Pekerja usia 15-19 turun dari 10,47% (1971) menjadi 3,41% (2013)",
            f"🔄 **Siklus Ekonomi**: Fluktuasi TPT mengikuti siklus ekonomi global dan domestik"
        ]
        
        for insight in insights_kerja:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📋 Data Tables & Export</h2>', unsafe_allow_html=True)
        
        # Dataset selector
        dataset_options = {
            "Populasi dan Kepadatan": "populasi",
            "Ketenagakerjaan Utama": "ketenagakerjaan", 
            "Pengangguran Berdasarkan Pendidikan": "pengangguran_pendidikan",
            "Pekerja Berdasarkan Usia": "pekerja_umur",
            "Pekerja Berdasarkan Pendidikan": "pekerja_pendidikan",
            "Angka Kematian Bayi (IMR)": "imr"
        }
        
        selected_dataset = st.selectbox("Pilih Dataset untuk Ditampilkan:", 
                                      list(dataset_options.keys()))
        
        dataset_key = dataset_options[selected_dataset]
        
        if dataset_key in datasets:
            df = datasets[dataset_key]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"#### 📊 {selected_dataset}")
                st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
            
            with col2:
                # Download button
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"aceh_penduduk_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                show_summary = st.checkbox("Tampilkan Ringkasan", value=True)
            
            # Display data
            st.dataframe(df, use_container_width=True, height=400)
            
            if show_summary:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📈 Statistik Dasar")
                    if 'Tahun' in df.columns:
                        st.metric("Periode Data", f"{df['Tahun'].min():.0f}-{df['Tahun'].max():.0f}")
                    
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        for col in numeric_cols[:3]:  # Show first 3 numeric columns
                            if col != 'Tahun':
                                avg_val = df[col].mean()
                                if 'Total' in col or 'Jumlah' in col:
                                    st.metric(f"Rata-rata {col}", format_number(avg_val))
                                elif 'TPT' in col or 'TPAK' in col or any(x in col for x in ['Ratio', 'Kepadatan']):
                                    st.metric(f"Rata-rata {col}", f"{avg_val:.1f}")
                                else:
                                    st.metric(f"Rata-rata {col}", f"{avg_val:,.0f}")
                
                with col2:
                    st.markdown("#### 🔍 Insights Data")
                    
                    if dataset_key == "populasi":
                        insights = [
                            "Pertumbuhan populasi konsisten selama 6 dekade",
                            "Kepadatan meningkat seiring urbanisasi",
                            "Sex ratio relatif seimbang dan stabil"
                        ]
                    elif dataset_key == "ketenagakerjaan":
                        insights = [
                            "TPAK meningkat menunjukkan partisipasi yang baik",
                            "TPT fluktuatif mengikuti kondisi ekonomi",
                            "Angkatan kerja tumbuh seiring pertumbuhan populasi"
                        ]
                    elif dataset_key == "pengangguran_pendidikan":
                        insights = [
                            "Pengangguran tertinggi pada lulusan SMA",
                            "Skills mismatch antara pendidikan dan kebutuhan pasar",
                            "Pengangguran terdidik menjadi tantangan struktural"
                        ]
                    elif dataset_key == "imr":
                        insights = [
                            "Penurunan IMR menunjukkan kemajuan kesehatan",
                            "Gender gap dalam kematian bayi konsisten",
                            "Pencapaian mendekati target MDGs"
                        ]
                    else:
                        insights = [
                            "Data menunjukkan transformasi demografis",
                            "Pola mengikuti tren pembangunan nasional", 
                            "Indikator positif pembangunan manusia"
                        ]
                    
                    for insight in insights:
                        st.markdown(f"• {insight}")
        
        else:
            st.error(f"Dataset '{selected_dataset}' tidak tersedia.")

# Update the SECTORS configuration in main_app.py
def update_penduduk_sector():
    """
    Update the SECTORS configuration in main_app.py:
    
    "penduduk": {
        "name": "Penduduk dan Ketenagakerjaan",
        "icon": "👥",
        "description": "Demografi dan ketenagakerjaan",
        "available": True  # Change from False to True
    }
    """
    pass

# Add to main() function in main_app.py
def update_main_function_for_penduduk():
    """
    Add this condition to your main() function:
    
    elif st.session_state.selected_sector == "penduduk":
        show_penduduk()
    """
    pass

# Add this function to your main_app.py file

@st.cache_data
def load_sosial_datasets():
    """Load Sosial & Kesejahteraan datasets from uploaded documents"""
    datasets = {}
    
    # 1. Education Completion by Level (1971-2013) - Sample key years
    pendidikan_tamat_data = [
        [1971, 66, 26, 4, 1, 0],
        [1980, 43, 29, 14, 11, 1],
        [1990, 32, 33, 17, 15, 3],
        [2000, 26, 30, 21, 19, 4],
        [2010, 22, 27, 21, 24, 6],
        [2013, 20, 28, 20, 25, 7]
    ]
    
    datasets['pendidikan_tamat'] = pd.DataFrame(pendidikan_tamat_data, 
                                               columns=['Tahun', 'Belum_Tamat_SD', 'SD', 'SMP', 'SMA', 'PT'])
    
    # 2. Literacy Rate (1971-2013) - Key years
    buta_huruf_data = [
        [1971, 76.91, 53.92, 65.28, 31.98],
        [1980, 80.48, 64.64, 72.56, 25.43],
        [1990, 90.32, 79.79, 85.03, 12.64],
        [2000, 95.70, 89.46, 92.55, 6.03],
        [2010, 97.41, 93.77, 95.56, 2.74],
        [2013, 98.23, 95.06, 96.64, 2.89]
    ]
    
    datasets['buta_huruf'] = pd.DataFrame(buta_huruf_data, 
                                         columns=['Tahun', 'Laki_Melek', 'Perempuan_Melek', 'Total_Melek', 'Buta_Huruf'])
    
    # 3. Health Facilities (1989-2013)
    fasilitas_kesehatan_data = [
        [1989, 20, 153, 518, 115],
        [1995, 23, 212, 714, 203],
        [2000, 26, 218, 766, 217],
        [2005, 34, 272, 798, 255],
        [2010, 49, 316, 951, 336],
        [2013, 50, 334, 964, 361]
    ]
    
    datasets['fasilitas_kesehatan'] = pd.DataFrame(fasilitas_kesehatan_data, 
                                                   columns=['Tahun', 'Rumah_Sakit', 'Puskesmas', 'Pustu', 'Pusling'])
    
    # 4. Health Personnel (1971-2013)
    tenaga_kesehatan_data = [
        [1971, 37, 1, 4, 19, 107],
        [1980, 37, 1, 8, 112, 142],
        [1990, 469, 56, 136, 308, 350],
        [2000, 203, 40, 86, 1572, 1513],
        [2010, 830, 302, 173, 6702, 6137],
        [2013, 795, 440, 195, 4924, 9761]
    ]
    
    datasets['tenaga_kesehatan'] = pd.DataFrame(tenaga_kesehatan_data, 
                                               columns=['Tahun', 'Dokter_Umum', 'Dokter_Spesialis', 'Dokter_Gigi', 'Perawat', 'Bidan'])
    
    # 5. Child Immunization (2004-2013)
    imunisasi_data = [
        [2004, 74.9, 75.1, 83.2, 74.2, 64.0],
        [2005, 65.78, 63.7, 86.9, 56.58, 51.45],
        [2009, 85.32, 83.17, 85.5, 74.08, 77.8],
        [2010, 87.12, 84.7, 87.67, 74.25, 79.92],
        [2011, 87.26, 84.78, 87.2, 74.15, 79.4],
        [2013, 87.8, 84.4, 84.9, 74.43, 79.8]
    ]
    
    datasets['imunisasi'] = pd.DataFrame(imunisasi_data, 
                                        columns=['Tahun', 'BCG', 'DPT', 'Polio', 'Campak', 'Hepatitis_B'])
    
    # 6. School Infrastructure - General Schools (1971-2012)
    sekolah_umum_data = [
        [1971, 868, 185217, 4996, 167, 23335, 897],
        [1985, 2748, 508440, 19818, 439, 127709, 8136],
        [1995, 3158, 549914, 25542, 474, 135664, 9390],
        [2005, 3291, 547436, 27252, 585, 195955, 10714],
        [2010, 3323, 519956, 46852, 885, 201403, 20293],
        [2012, 3353, 496193, 47789, 956, 199693, 21686]
    ]
    
    datasets['sekolah_umum'] = pd.DataFrame(sekolah_umum_data, 
                                           columns=['Tahun', 'SD_Sekolah', 'SD_Murid', 'SD_Guru', 'SMP_Sekolah', 'SMP_Murid', 'SMP_Guru'])
    
    # 7. Religious Schools (1972-2011)
    sekolah_agama_data = [
        [1972, 528, 109820, 2597, 59, 3580, 157],
        [1985, 514, 88475, 3607, 108, 20516, 1344],
        [1995, 538, 91610, 3669, 159, 32037, 2571],
        [2005, 537, 114507, 8185, 281, 65645, 5900],
        [2010, 566, 114683, 10827, 345, 76817, 7007],
        [2011, 565, 120912, 11049, 452, 72418, 6877]
    ]
    
    datasets['sekolah_agama'] = pd.DataFrame(sekolah_agama_data, 
                                            columns=['Tahun', 'MI_Sekolah', 'MI_Murid', 'MI_Guru', 'MTs_Sekolah', 'MTs_Murid', 'MTs_Guru'])
    
    # 8. Birth Assistance (1992-2013) - Sample years
    bantuan_kelahiran_data = [
        [1992, 3.2, 33.75, 56.61, 2.41, 2.39],
        [1999, 4.98, 61.78, 29.8, 1.18, 0.52],
        [2005, 8.67, 67.39, 20.18, 2.14, 0.77],
        [2010, 11.45, 75.16, 12.56, 0.22, 0.05],
        [2013, 12.86, 78.96, 7.76, 0.17, 0.1]
    ]
    
    datasets['bantuan_kelahiran'] = pd.DataFrame(bantuan_kelahiran_data, 
                                                columns=['Tahun', 'Dokter', 'Bidan', 'Lainnya', 'Perawat', 'Dukun'])
    
    # 9. Income Distribution & Gini Ratio (1984-2013)
    gini_ratio_data = [
        [1984, 25.56, 39.03, 35.41, 0.255],
        [1990, 26.75, 39.31, 33.94, 0.223],
        [1999, 25.0, 38.8, 36.2, 0.251],
        [2005, 20.51, 37.13, 42.36, 0.327],
        [2010, 21.9, 38.66, 39.44, 0.294],
        [2013, 20.83, 35.6, 43.57, 0.305]
    ]
    
    datasets['gini_ratio'] = pd.DataFrame(gini_ratio_data, 
                                         columns=['Tahun', 'Rendah_40', 'Sedang_40', 'Tinggi_20', 'Gini_Ratio'])
    
    # 10. Current Education Enrollment (1995-2013) - Sample years
    pendidikan_sedang_data = [
        [1995, 8.82, 11.7, 6.73, 5.21, 67.54],
        [2000, 4.13, 8.32, 7.39, 10.21, 69.94],
        [2005, 5.51, 9.12, 8.35, 8.63, 68.38],
        [2010, 4.2, 8.72, 7.05, 9.83, 70.21],
        [2013, 2.83, 8.43, 7.56, 10.37, 70.81]
    ]
    
    datasets['pendidikan_sedang'] = pd.DataFrame(pendidikan_sedang_data, 
                                                columns=['Tahun', 'Tidak_Sekolah', 'SD', 'SMP', 'SMA_PT', 'Tidak_Sekolah_Lagi'])
    
    # 11. Human Development Index (1990-2013)
    ipm_data = [
        [1990, None, None, None, None, 61.9],
        [1999, 67.7, 93.1, 7.2, 662.8, 65.3],
        [2005, 68.0, 96.0, 8.4, 588.9, 69.0],
        [2010, 68.7, 96.88, 8.81, 611.42, 71.7],
        [2013, 69.4, 97.04, 9.02, 621.4, 73.5]
    ]
    
    datasets['ipm'] = pd.DataFrame(ipm_data, 
                                  columns=['Tahun', 'Harapan_Hidup', 'Melek_Huruf', 'Lama_Sekolah', 'Daya_Beli', 'IPM'])
    
    return datasets

def show_sosial():
    """Enhanced Sosial & Kesejahteraan dashboard with 11 comprehensive visualizations"""
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">❤️ Sektor Sosial dan Kesejahteraan Provinsi Aceh</h1>
        <p class="main-subtitle">Analisis Komprehensif Pendidikan, Kesehatan, dan Pembangunan Manusia (1971-2013)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load the datasets
    datasets = load_sosial_datasets()
    
    # Tabs for different social aspects (11 datasets across tabs)
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎓 Pendidikan", "🏥 Kesehatan", "📋 Data Tables"])
    
    with tab1:
        # Key social welfare metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'ipm' in datasets:
                ipm_2013 = datasets['ipm'][datasets['ipm']['Tahun'] == 2013]['IPM'].iloc[0]
                st.markdown(create_metric_card("📈", f"{ipm_2013:.1f}", "Indeks Pembangunan Manusia", "2013"), unsafe_allow_html=True)
        
        with col2:
            if 'buta_huruf' in datasets:
                melek_huruf_2013 = datasets['buta_huruf'][datasets['buta_huruf']['Tahun'] == 2013]['Total_Melek'].iloc[0]
                st.markdown(create_metric_card("📚", f"{melek_huruf_2013:.1f}%", "Tingkat Melek Huruf", "2013"), unsafe_allow_html=True)
        
        with col3:
            if 'tenaga_kesehatan' in datasets:
                total_dokter_2013 = (datasets['tenaga_kesehatan'][datasets['tenaga_kesehatan']['Tahun'] == 2013]['Dokter_Umum'].iloc[0] + 
                                    datasets['tenaga_kesehatan'][datasets['tenaga_kesehatan']['Tahun'] == 2013]['Dokter_Spesialis'].iloc[0])
                st.markdown(create_metric_card("👨‍⚕️", f"{total_dokter_2013:,}", "Total Dokter", "2013"), unsafe_allow_html=True)
        
        with col4:
            if 'gini_ratio' in datasets:
                gini_2013 = datasets['gini_ratio'][datasets['gini_ratio']['Tahun'] == 2013]['Gini_Ratio'].iloc[0]
                st.markdown(create_metric_card("⚖️", f"{gini_2013:.3f}", "Gini Ratio", "Ketimpangan 2013"), unsafe_allow_html=True)
        
        # Overview visualizations (4 charts)
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 1: Human Development Index Trend
            if 'ipm' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📈 Perkembangan Indeks Pembangunan Manusia</h3>', unsafe_allow_html=True)
                
                fig = px.line(datasets['ipm'].dropna(subset=['IPM']), x='Tahun', y='IPM',
                            markers=True,
                            color_discrete_sequence=['#10b981'],
                            title="",
                            labels={'IPM': 'Indeks Pembangunan Manusia', 'Tahun': 'Tahun'})
                fig.update_traces(line=dict(width=4), marker=dict(size=10))
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization 2: Literacy Progress
            if 'buta_huruf' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📚 Perkembangan Tingkat Melek Huruf</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['buta_huruf']['Tahun'], y=datasets['buta_huruf']['Laki_Melek'],
                                       name='Laki-laki', line=dict(color='#3b82f6', width=3),
                                       mode='lines+markers'))
                fig.add_trace(go.Scatter(x=datasets['buta_huruf']['Tahun'], y=datasets['buta_huruf']['Perempuan_Melek'],
                                       name='Perempuan', line=dict(color='#ec4899', width=3),
                                       mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Tingkat Melek Huruf (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 3: Income Distribution
            if 'gini_ratio' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">💰 Distribusi Pendapatan dan Gini Ratio</h3>', unsafe_allow_html=True)
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Bar(x=datasets['gini_ratio']['Tahun'], y=datasets['gini_ratio']['Rendah_40'],
                          name="40% Terbawah", marker_color='#ef4444', opacity=0.7),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(x=datasets['gini_ratio']['Tahun'], y=datasets['gini_ratio']['Gini_Ratio'],
                             name="Gini Ratio", line=dict(color='#1e40af', width=3),
                             mode='lines+markers'),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Tahun")
                fig.update_yaxes(title_text="Persentase Pendapatan (%)", secondary_y=False)
                fig.update_yaxes(title_text="Gini Ratio", secondary_y=True)
                fig.update_layout(height=400)
                
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization 4: Health Personnel Growth
            if 'tenaga_kesehatan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">👨‍⚕️ Pertumbuhan Tenaga Kesehatan</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['tenaga_kesehatan']['Tahun'], y=datasets['tenaga_kesehatan']['Dokter_Umum'],
                                       name='Dokter Umum', line=dict(color='#10b981', width=3), mode='lines+markers'))
                fig.add_trace(go.Scatter(x=datasets['tenaga_kesehatan']['Tahun'], y=datasets['tenaga_kesehatan']['Bidan'],
                                       name='Bidan', line=dict(color='#f59e0b', width=3), mode='lines+markers'))
                fig.add_trace(go.Scatter(x=datasets['tenaga_kesehatan']['Tahun'], y=datasets['tenaga_kesehatan']['Perawat'],
                                       name='Perawat', line=dict(color='#8b5cf6', width=3), mode='lines+markers'))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Jumlah Tenaga Kesehatan")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🎓 Analisis Sektor Pendidikan</h2>', unsafe_allow_html=True)
        
        # Education metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'sekolah_umum' in datasets:
                total_sd_2012 = datasets['sekolah_umum'][datasets['sekolah_umum']['Tahun'] == 2012]['SD_Sekolah'].iloc[0]
                st.markdown(create_metric_card("🏫", f"{total_sd_2012:,}", "Sekolah Dasar", "2012"), unsafe_allow_html=True)
        
        with col2:
            if 'sekolah_umum' in datasets:
                murid_sd_2012 = datasets['sekolah_umum'][datasets['sekolah_umum']['Tahun'] == 2012]['SD_Murid'].iloc[0]
                st.markdown(create_metric_card("👨‍🎓", format_number(murid_sd_2012), "Murid SD", "2012"), unsafe_allow_html=True)
        
        with col3:
            if 'pendidikan_tamat' in datasets:
                pt_2013 = datasets['pendidikan_tamat'][datasets['pendidikan_tamat']['Tahun'] == 2013]['PT'].iloc[0]
                st.markdown(create_metric_card("🎓", f"{pt_2013}%", "Lulusan Perguruan Tinggi", "2013"), unsafe_allow_html=True)
        
        with col4:
            if 'sekolah_agama' in datasets:
                mi_2011 = datasets['sekolah_agama'][datasets['sekolah_agama']['Tahun'] == 2011]['MI_Sekolah'].iloc[0]
                st.markdown(create_metric_card("🕌", f"{mi_2011}", "Madrasah Ibtidaiyah", "2011"), unsafe_allow_html=True)
        
        # Education analysis charts (3 visualizations)
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 5: Education Completion Levels
            if 'pendidikan_tamat' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📊 Tingkat Pendidikan yang Diselesaikan</h3>', unsafe_allow_html=True)
                
                # Create stacked area chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['pendidikan_tamat']['Tahun'], y=datasets['pendidikan_tamat']['Belum_Tamat_SD'],
                                       fill='tozeroy', name='Belum Tamat SD', line=dict(color='#ef4444')))
                fig.add_trace(go.Scatter(x=datasets['pendidikan_tamat']['Tahun'], y=datasets['pendidikan_tamat']['SD'],
                                       fill='tonexty', name='SD', line=dict(color='#f59e0b')))
                fig.add_trace(go.Scatter(x=datasets['pendidikan_tamat']['Tahun'], y=datasets['pendidikan_tamat']['SMP'],
                                       fill='tonexty', name='SMP', line=dict(color='#10b981')))
                fig.add_trace(go.Scatter(x=datasets['pendidikan_tamat']['Tahun'], y=datasets['pendidikan_tamat']['SMA'],
                                       fill='tonexty', name='SMA', line=dict(color='#3b82f6')))
                fig.add_trace(go.Scatter(x=datasets['pendidikan_tamat']['Tahun'], y=datasets['pendidikan_tamat']['PT'],
                                       fill='tonexty', name='Perguruan Tinggi', line=dict(color='#8b5cf6')))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Persentase (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization 6: School Infrastructure Development
            if 'sekolah_umum' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🏫 Perkembangan Infrastruktur Sekolah</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=datasets['sekolah_umum']['Tahun'], y=datasets['sekolah_umum']['SD_Sekolah'],
                                   name='Sekolah Dasar', marker_color='#3b82f6', opacity=0.8))
                fig.add_trace(go.Bar(x=datasets['sekolah_umum']['Tahun'], y=datasets['sekolah_umum']['SMP_Sekolah'],
                                   name='Sekolah Menengah', marker_color='#10b981', opacity=0.8))
                
                fig.update_layout(height=400, barmode='group',
                                xaxis_title="Tahun", yaxis_title="Jumlah Sekolah")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Visualization 7: Religious Education
        if 'sekolah_agama' in datasets:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown('<h3 class="chart-title">🕌 Perkembangan Pendidikan Agama</h3>', unsafe_allow_html=True)
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Bar(x=datasets['sekolah_agama']['Tahun'], y=datasets['sekolah_agama']['MI_Sekolah'],
                      name="Madrasah Ibtidaiyah", marker_color='#10b981', opacity=0.7),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=datasets['sekolah_agama']['Tahun'], y=datasets['sekolah_agama']['MI_Murid'],
                         name="Murid MI", line=dict(color='#dc2626', width=3),
                         mode='lines+markers'),
                secondary_y=True,
            )
            
            fig.update_xaxes(title_text="Tahun")
            fig.update_yaxes(title_text="Jumlah Sekolah", secondary_y=False)
            fig.update_yaxes(title_text="Jumlah Murid", secondary_y=True)
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Education insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Pendidikan</h4>', unsafe_allow_html=True)
        
        insights_pendidikan = [
            f"🎓 **Transformasi Pendidikan**: Lulusan PT meningkat dari 0% (1971) menjadi {datasets['pendidikan_tamat'][datasets['pendidikan_tamat']['Tahun']==2013]['PT'].iloc[0]}% (2013)",
            f"📚 **Pemberantasan Buta Huruf**: Tingkat melek huruf naik dari 65,28% (1971) menjadi {datasets['buta_huruf'][datasets['buta_huruf']['Tahun']==2013]['Total_Melek'].iloc[0]:.1f}% (2013)",
            f"🏫 **Ekspansi Infrastruktur**: Sekolah dasar tumbuh dari 868 (1971) menjadi {datasets['sekolah_umum'][datasets['sekolah_umum']['Tahun']==2012]['SD_Sekolah'].iloc[0]:,} unit (2012)",
            f"👩‍🎓 **Gender Gap**: Kesenjangan melek huruf gender menurun dari 22,99 poin (1971) menjadi 3,17 poin (2013)",
            f"🕌 **Pendidikan Agama**: Madrasah tetap berperan penting dengan {datasets['sekolah_agama'][datasets['sekolah_agama']['Tahun']==2011]['MI_Sekolah'].iloc[0]} MI dan ribuan murid",
            f"📈 **Kualitas Guru**: Rasio guru-murid SD membaik dari 1:37 (1971) menjadi 1:10 (2012)",
            f"🎯 **Akses Pendidikan**: Persentase yang tidak bersekolah turun dari 66% (1971) menjadi 20% (2013)",
            f"⚖️ **Pemerataan**: Masih terdapat kesenjangan akses pendidikan antara daerah urban dan rural"
        ]
        
        for insight in insights_pendidikan:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">🏥 Analisis Sektor Kesehatan</h2>', unsafe_allow_html=True)
        
        # Health metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'fasilitas_kesehatan' in datasets:
                puskesmas_2013 = datasets['fasilitas_kesehatan'][datasets['fasilitas_kesehatan']['Tahun'] == 2013]['Puskesmas'].iloc[0]
                st.markdown(create_metric_card("🏥", f"{puskesmas_2013}", "Puskesmas", "2013"), unsafe_allow_html=True)
        
        with col2:
            if 'tenaga_kesehatan' in datasets:
                bidan_2013 = datasets['tenaga_kesehatan'][datasets['tenaga_kesehatan']['Tahun'] == 2013]['Bidan'].iloc[0]
                st.markdown(create_metric_card("👩‍⚕️", f"{bidan_2013:,}", "Bidan", "2013"), unsafe_allow_html=True)
        
        with col3:
            if 'imunisasi' in datasets:
                avg_imunisasi_2013 = datasets['imunisasi'][datasets['imunisasi']['Tahun'] == 2013][['BCG', 'DPT', 'Polio', 'Campak']].mean().mean()
                st.markdown(create_metric_card("💉", f"{avg_imunisasi_2013:.1f}%", "Rata-rata Imunisasi", "2013"), unsafe_allow_html=True)
        
        with col4:
            if 'bantuan_kelahiran' in datasets:
                medis_2013 = datasets['bantuan_kelahiran'][datasets['bantuan_kelahiran']['Tahun'] == 2013]['Dokter'].iloc[0] + datasets['bantuan_kelahiran'][datasets['bantuan_kelahiran']['Tahun'] == 2013]['Bidan'].iloc[0]
                st.markdown(create_metric_card("🤱", f"{medis_2013:.1f}%", "Persalinan Tenaga Medis", "2013"), unsafe_allow_html=True)
        
        # Health analysis charts (4 visualizations)
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 8: Health Facilities Development
            if 'fasilitas_kesehatan' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🏥 Perkembangan Fasilitas Kesehatan</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=datasets['fasilitas_kesehatan']['Tahun'], y=datasets['fasilitas_kesehatan']['Rumah_Sakit'],
                                   name='Rumah Sakit', marker_color='#dc2626'))
                fig.add_trace(go.Bar(x=datasets['fasilitas_kesehatan']['Tahun'], y=datasets['fasilitas_kesehatan']['Puskesmas'],
                                   name='Puskesmas', marker_color='#10b981'))
                fig.add_trace(go.Bar(x=datasets['fasilitas_kesehatan']['Tahun'], y=datasets['fasilitas_kesehatan']['Pustu'],
                                   name='Pustu', marker_color='#3b82f6'))
                
                fig.update_layout(height=400, barmode='group',
                                xaxis_title="Tahun", yaxis_title="Jumlah Fasilitas")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization 9: Child Immunization Coverage
            if 'imunisasi' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">💉 Cakupan Imunisasi Balita</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                colors = ['#1e40af', '#dc2626', '#10b981', '#f59e0b', '#8b5cf6']
                vaccines = ['BCG', 'DPT', 'Polio', 'Campak', 'Hepatitis_B']
                
                for i, vaccine in enumerate(vaccines):
                    fig.add_trace(go.Scatter(
                        x=datasets['imunisasi']['Tahun'], 
                        y=datasets['imunisasi'][vaccine],
                        name=vaccine,
                        line=dict(color=colors[i], width=3),
                        mode='lines+markers'
                    ))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Cakupan Imunisasi (%)")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Visualization 10: Birth Assistance Quality
            if 'bantuan_kelahiran' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">🤱 Kualitas Bantuan Persalinan</h3>', unsafe_allow_html=True)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=datasets['bantuan_kelahiran']['Tahun'], y=datasets['bantuan_kelahiran']['Dokter'],
                                       fill='tozeroy', name='Dokter', line=dict(color='#1e40af')))
                fig.add_trace(go.Scatter(x=datasets['bantuan_kelahiran']['Tahun'], y=datasets['bantuan_kelahiran']['Bidan'],
                                       fill='tonexty', name='Bidan', line=dict(color='#10b981')))
                fig.add_trace(go.Scatter(x=datasets['bantuan_kelahiran']['Tahun'], y=datasets['bantuan_kelahiran']['Lainnya'],
                                       fill='tonexty', name='Lainnya (Non-Medis)', line=dict(color='#ef4444')))
                
                fig.update_layout(height=400,
                                xaxis_title="Tahun", yaxis_title="Persentase Bantuan Persalinan")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Visualization 11: Current Education Status
            if 'pendidikan_sedang' in datasets:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<h3 class="chart-title">📚 Status Pendidikan Saat Ini</h3>', unsafe_allow_html=True)
                
                # Create pie chart for 2013 education status
                latest_education = datasets['pendidikan_sedang'][datasets['pendidikan_sedang']['Tahun'] == 2013].iloc[0]
                education_status = {
                    'Status': ['Tidak Sekolah', 'SD', 'SMP', 'SMA/PT', 'Tidak Sekolah Lagi'],
                    'Persentase': [latest_education['Tidak_Sekolah'], latest_education['SD'],
                                  latest_education['SMP'], latest_education['SMA_PT'], latest_education['Tidak_Sekolah_Lagi']]
                }
                education_df = pd.DataFrame(education_status)
                
                fig = px.pie(education_df, values='Persentase', names='Status',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Health insights
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h4>🔍 Analisis & Insights Kesehatan</h4>', unsafe_allow_html=True)
        
        insights_kesehatan = [
            f"🏥 **Ekspansi Fasilitas**: Puskesmas tumbuh dari 153 (1989) menjadi {datasets['fasilitas_kesehatan'][datasets['fasilitas_kesehatan']['Tahun']==2013]['Puskesmas'].iloc[0]} unit (2013)",
            f"👩‍⚕️ **Ledakan Tenaga Medis**: Bidan meningkat drastis dari 107 (1971) menjadi {datasets['tenaga_kesehatan'][datasets['tenaga_kesehatan']['Tahun']==2013]['Bidan'].iloc[0]:,} (2013)",
            f"💉 **Cakupan Imunisasi**: Rata-rata cakupan imunisasi mencapai {avg_imunisasi_2013:.1f}% dengan Polio tertinggi",
            f"🤱 **Revolusi Persalinan**: Bantuan persalinan medis (dokter+bidan) naik dari 36,95% (1992) menjadi {medis_2013:.1f}% (2013)",
            f"📈 **Akselerasi Pascatsunami**: Periode 2005-2010 menunjukkan pembangunan kesehatan yang pesat",
            f"⚕️ **Spesialisasi Medis**: Dokter spesialis bertambah dari 1 (1971) menjadi 440 (2013)",
            f"🎯 **Fokus Preventif**: Program imunisasi menunjukkan komitmen pada kesehatan preventif",
            f"🌍 **Standar WHO**: Cakupan imunisasi mendekati standar WHO untuk beberapa jenis vaksin",
            f"📍 **Disparitas Regional**: Masih terdapat kesenjangan akses layanan kesehatan antarwilayah"
        ]
        
        for insight in insights_kesehatan:
            st.markdown(f"- {insight}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">📋 Data Tables & Export</h2>', unsafe_allow_html=True)
        
        # Dataset selector
        dataset_options = {
            "Indeks Pembangunan Manusia": "ipm",
            "Tingkat Pendidikan yang Ditamatkan": "pendidikan_tamat",
            "Tingkat Melek Huruf": "buta_huruf",
            "Fasilitas Kesehatan": "fasilitas_kesehatan",
            "Tenaga Kesehatan": "tenaga_kesehatan",
            "Imunisasi Balita": "imunisasi",
            "Sekolah Umum": "sekolah_umum",
            "Sekolah Agama": "sekolah_agama",
            "Bantuan Persalinan": "bantuan_kelahiran",
            "Distribusi Pendapatan (Gini)": "gini_ratio",
            "Status Pendidikan Saat Ini": "pendidikan_sedang"
        }
        
        selected_dataset = st.selectbox("Pilih Dataset untuk Ditampilkan:", 
                                      list(dataset_options.keys()))
        
        dataset_key = dataset_options[selected_dataset]
        
        if dataset_key in datasets:
            df = datasets[dataset_key]
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"#### 📊 {selected_dataset}")
                st.markdown(f"**Records**: {len(df):,} | **Columns**: {len(df.columns)}")
            
            with col2:
                # Download button
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False, sep=';')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv_buffer.getvalue(),
                    file_name=f"aceh_sosial_{dataset_key}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                show_summary = st.checkbox("Tampilkan Ringkasan", value=True)
            
            # Display data
            st.dataframe(df, use_container_width=True, height=400)
            
            if show_summary:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 📈 Statistik Dasar")
                    if 'Tahun' in df.columns:
                        st.metric("Periode Data", f"{df['Tahun'].min():.0f}-{df['Tahun'].max():.0f}")
                    
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        for col in numeric_cols[:3]:  # Show first 3 numeric columns
                            if col != 'Tahun':
                                avg_val = df[col].mean()
                                if 'IPM' in col:
                                    st.metric(f"Rata-rata {col}", f"{avg_val:.1f}")
                                elif any(x in col for x in ['Persen', 'Ratio', 'Melek']):
                                    st.metric(f"Rata-rata {col}", f"{avg_val:.1f}%")
                                else:
                                    st.metric(f"Rata-rata {col}", f"{avg_val:,.0f}")
                
                with col2:
                    st.markdown("#### 🔍 Insights Data")
                    
                    if dataset_key == "ipm":
                        insights = [
                            "IPM Aceh konsisten meningkat dari 61.9 (1990)",
                            "Komponen pendidikan menunjukkan perbaikan signifikan",
                            "Daya beli relatif stabil dengan tren positif"
                        ]
                    elif dataset_key == "pendidikan_tamat":
                        insights = [
                            "Transformasi dari masyarakat berpendidikan rendah",
                            "Lulusan PT meningkat pesat dalam 4 dekade",
                            "Masih ada tantangan akses pendidikan dasar"
                        ]
                    elif dataset_key == "buta_huruf":
                        insights = [
                            "Keberhasilan program pemberantasan buta huruf",
                            "Gender gap terus mengecil dari waktu ke waktu",
                            "Target literasi universal hampir tercapai"
                        ]
                    elif dataset_key == "tenaga_kesehatan":
                        insights = [
                            "Pertumbuhan eksponensial tenaga kesehatan",
                            "Bidan menjadi tulang punggung layanan maternal",
                            "Spesialisasi medis berkembang pesat"
                        ]
                    else:
                        insights = [
                            "Data menunjukkan perbaikan berkelanjutan",
                            "Tren positif dalam pembangunan manusia",
                            "Masih ada ruang perbaikan dan pemerataan"
                        ]
                    
                    for insight in insights:
                        st.markdown(f"• {insight}")
        
        else:
            st.error(f"Dataset '{selected_dataset}' tidak tersedia.")

# Update the SECTORS configuration in main_app.py
def update_sosial_sector():
    """
    Update the SECTORS configuration in main_app.py:
    
    "sosial": {
        "name": "Sosial dan Kesejahteraan Rakyat",
        "icon": "❤️",
        "description": "Kesehatan, pendidikan, dan kesejahteraan",
        "available": True  # Change from False to True
    }
    """
    pass

# Add to main() function in main_app.py
def update_main_function_for_sosial():
    """
    Add this condition to your main() function:
    
    elif st.session_state.selected_sector == "sosial":
        show_sosial()
    """
    pass
    
def show_data_upload_section(sector_key):
    """Show data upload section for new sectors"""
    sector = SECTORS[sector_key]
    
    st.markdown(f"""
    <div class="main-header">
        <h1 class="main-title">{sector['icon']} {sector['name']}</h1>
        <p class="main-subtitle">{sector['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown("""
    <div class="upload-section">
        <div class="upload-icon">📤</div>
        <h2 class="upload-title">Upload Data untuk Sektor Ini</h2>
        <p class="upload-desc">Upload multiple file CSV untuk membuat visualisasi otomatis. 
        File akan diproses dan menghasilkan chart yang sesuai dengan struktur data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Pilih file CSV (multiple files allowed)",
        type=['csv'],
        accept_multiple_files=True,
        key=f"upload_{sector_key}",
        help="Upload multiple CSV files. Sistem akan otomatis membuat visualisasi berdasarkan struktur data."
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file berhasil diupload!")
        
        # Process each file
        for i, file in enumerate(uploaded_files):
            try:
                # Read CSV with different separators
                try:
                    df = pd.read_csv(file, sep=';', encoding='utf-8')
                except:
                    try:
                        df = pd.read_csv(file, sep=',', encoding='utf-8')
                    except:
                        df = pd.read_csv(file, sep=';', encoding='latin1')
                
                # Store in session state
                if sector_key not in st.session_state.uploaded_data:
                    st.session_state.uploaded_data[sector_key] = {}
                
                st.session_state.uploaded_data[sector_key][file.name] = df
                
                # Create expandable section for each file
                with st.expander(f"📊 {file.name} - {len(df)} rows × {len(df.columns)} columns", expanded=i==0):
                    
                    # Data preview
                    st.markdown("#### 📋 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Data info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rows", len(df))
                    with col2:
                        st.metric("Total Columns", len(df.columns))
                    with col3:
                        numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
                        st.metric("Numeric Columns", numeric_cols)
                    
                    # Auto-generate visualizations
                    st.markdown("#### 📈 Auto-Generated Visualizations")
                    
                    charts = auto_generate_charts(df, file.name)
                    
                    if charts:
                        # Display charts in grid
                        if len(charts) >= 2:
                            chart_cols = st.columns(2)
                            for idx, (chart_type, title, fig) in enumerate(charts[:4]):  # Max 4 charts
                                with chart_cols[idx % 2]:
                                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                                    st.plotly_chart(fig, use_container_width=True)
                                    st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            for chart_type, title, fig in charts:
                                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                                st.plotly_chart(fig, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("📊 Tidak dapat menghasilkan chart otomatis untuk data ini. Data mungkin memerlukan preprocessing khusus.")
                    
                    # Download processed data
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False, sep=';')
                    st.download_button(
                        label="💾 Download Processed Data",
                        data=csv_buffer.getvalue(),
                        file_name=f"processed_{file.name}",
                        mime="text/csv",
                        use_container_width=True
                    )
            
            except Exception as e:
                st.error(f"❌ Error processing {file.name}: {str(e)}")
    
    # Implementation Guide
    st.markdown('<h2 class="section-title">📚 Panduan Implementasi Dashboard Sektor</h2>', unsafe_allow_html=True)
    
    # Rules and guidelines
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="chart-container">
            <h3 class="chart-title">🎯 Rules untuk Data Upload</h3>
            <div style="padding: 1rem;">
                <h4>📁 Format File:</h4>
                <ul>
                    <li>Format: <code>.csv</code></li>
                    <li>Separator: <code>;</code> (semicolon) atau <code>,</code> (comma)</li>
                    <li>Encoding: UTF-8 atau Latin-1</li>
                    <li>Header: Baris pertama berisi nama kolom</li>
                </ul>
                
                <h4>📊 Struktur Data yang Optimal:</h4>
                <ul>
                    <li><strong>Kolom tahun/waktu:</strong> Untuk trend analysis</li>
                    <li><strong>Kolom kategori:</strong> Untuk grouping dan comparison</li>
                    <li><strong>Kolom numerik:</strong> Untuk perhitungan dan visualisasi</li>
                    <li><strong>Konsistensi nama:</strong> Standar penamaan kolom</li>
                </ul>
                
                <h4>🔧 Auto-Processing Features:</h4>
                <ul>
                    <li>✅ Deteksi otomatis tipe data</li>
                    <li>✅ Generate chart berdasarkan pola data</li>
                    <li>✅ Time series untuk data temporal</li>
                    <li>✅ Distribution analysis untuk data numerik</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="chart-container">
            <h3 class="chart-title">🚀 Chart Auto-Generation Logic</h3>
            <div style="padding: 1rem;">
                <h4>📈 Chart Types Generated:</h4>
                <ul>
                    <li><strong>Line Chart:</strong> Jika ada kolom tahun + numerik</li>
                    <li><strong>Bar Chart:</strong> Kategori vs numerik</li>
                    <li><strong>Histogram:</strong> Distribusi data numerik</li>
                    <li><strong>Heatmap:</strong> Korelasi antar variabel numerik</li>
                </ul>
                
                <h4>🎨 Best Practices:</h4>
                <ul>
                    <li>Satu file = satu tema/topik data</li>
                    <li>Maksimal 15 kategori untuk bar chart</li>
                    <li>Data sampel dibatasi untuk performa</li>
                    <li>Chart disesuaikan dengan ukuran data</li>
                </ul>
                
                <h4>📝 Contoh Struktur Data:</h4>
                <pre style="background: #f8fafc; padding: 1rem; border-radius: 8px; font-size: 0.8rem;">
tahun;kategori;nilai;persentase
2010;Sektor A;1000;25.5
2010;Sektor B;1500;37.5
2011;Sektor A;1200;28.5
2011;Sektor B;1800;42.8</pre>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    if 'selected_sector' not in st.session_state:
        st.session_state.selected_sector = 'beranda'
    if 'uploaded_data' not in st.session_state:
        st.session_state.uploaded_data = {}
    
    # Load datasets
    datasets = load_datasets()
    
    # Enhanced Modern Sidebar
    with st.sidebar:
        # Logo and Title
        st.markdown("""
        <div class="sidebar-card">
            <h3>🏛️ Dashboard Pembangunan Aceh</h3>
            <p>Visualisasi data pembangunan multi-sektor dengan teknologi interaktif modern</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sector Selection
        st.markdown("""
        <div class="sidebar-card">
            <h3>🎯 Navigasi Sektor</h3>
            <p>Pilih sektor untuk analisis mendalam dan visualisasi komprehensif</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create sector options with better formatting
        sector_options = []
        sector_keys = []
        
        for key, sector in SECTORS.items():
            if sector["available"]:
                display_name = f"{sector['name']}"
            else:
                display_name = f"{sector['name']}"
            sector_options.append(display_name)
            sector_keys.append(key)
        
        # Find current index
        try:
            current_index = sector_keys.index(st.session_state.selected_sector)
        except ValueError:
            current_index = 0
        
        # Selectbox
        selected_display = st.selectbox(
            "Pilih Sektor Analisis:",
            sector_options,
            index=current_index,
            key="sector_selector"
        )
        
        # Update session state
        selected_key = sector_keys[sector_options.index(selected_display)]
        if selected_key != st.session_state.selected_sector:
            st.session_state.selected_sector = selected_key
            st.rerun()
        
        # Current sector info
        current_sector = SECTORS[st.session_state.selected_sector]
        st.markdown(f"""
        <div class="sidebar-card">
            <h3>{current_sector['icon']} Sektor Aktif</h3>
            <p><strong>{current_sector['name']}</strong></p>
            <p>{current_sector['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Data statistics
        if datasets:
            total_datasets = len(datasets)
            total_rows = sum(len(df) for df in datasets.values())
            
            st.markdown(f"""
            <div class="sidebar-card">
                <h3>📊 Statistik Data</h3>
                <div class="info-item">
                    <span class="info-label">Dataset Tersedia</span>
                    <span class="info-value">{total_datasets}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Total Records</span>
                    <span class="info-value">{total_rows:,}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Periode Data</span>
                    <span class="info-value">1958-2014</span>
                </div>
                <div class="info-item">
                    <span class="info-label">Wilayah</span>
                    <span class="info-value">23 Kab/Kota</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Implementation status
        available_count = sum(1 for s in SECTORS.values() if s["available"])
        total_count = len(SECTORS)
        progress = (available_count/total_count*100)
        
        st.markdown(f"""
        <div class="sidebar-card">
            <h3>🎯 Status Implementasi</h3>
            <div class="info-item">
                <span class="info-label">Sektor Tersedia</span>
                <span class="info-value">{available_count}/{total_count}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Progress</span>
                <span class="info-value">{progress:.0f}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    # Main Content Area
    if st.session_state.selected_sector == "beranda":
        show_beranda(datasets)
    elif st.session_state.selected_sector == "neraca_regional":
        show_neraca_regional(datasets)
    elif st.session_state.selected_sector == "geografis":  
        show_geografis(datasets)
    elif st.session_state.selected_sector == "listrik_gas_air":
        show_listrik_gas_air()
    elif st.session_state.selected_sector == "perdagangan":
        show_perdagangan()
    elif st.session_state.selected_sector == "inflasi_harga":
        show_inflasi_harga()
    elif st.session_state.selected_sector == "penduduk":
        show_penduduk()
    elif st.session_state.selected_sector == "sosial":
        show_sosial()
    else:
        # Show upload section for other sectors
        show_data_upload_section(st.session_state.selected_sector)
    
    # Enhanced Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%); 
                border-radius: 24px; margin-top: 4rem; color: white; position: relative; overflow: hidden;'>
        <div style='position: relative; z-index: 2;'>
            <h3 style='color: white; margin-bottom: 1rem; font-weight: 800; font-size: 1.8rem;'>Dashboard Pembangunan Provinsi Aceh</h3>
            <p style='font-size: 1.2rem; margin-bottom: 1rem; opacity: 0.9;'><strong>UPTD Statistik Diskominsa Aceh</strong></p>
            <p style='margin-bottom: 0.5rem; opacity: 0.8;'>Sumber Data: Open Data Aceh | Publikasi "Pembangunan Aceh dari Masa ke Masa"</p>
            <p style='margin-bottom: 1rem; opacity: 0.8;'>Visualisasi Data Pembangunan Multi-Sektor (1958-2014)</p>
            <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 2rem;'>
                <span style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;'>📊 Interactive Analytics</span>
                <span style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;'>🚀 Auto-Visualization</span>
                <span style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;'>📈 Real-time Processing</span>
            </div>
            <p style='font-size: 0.9rem; margin-top: 2rem; opacity: 0.7;'>© 2024 - Powered by Streamlit & Plotly</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    