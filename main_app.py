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
        "available": False
    },
    "pemerintahan": {
        "name": "Pemerintahan",
        "icon": "🏛️",
        "description": "Struktur dan administrasi pemerintahan",
        "available": False
    },
    "pertanian": {
        "name": "Pertanian",
        "icon": "🌾",
        "description": "Sektor pertanian dan perkebunan",
        "available": False
    },
    "listrik_gas_air": {
        "name": "Listrik, Gas & Air",
        "icon": "⚡",
        "description": "Infrastruktur energi dan utilitas",
        "available": False
    },
    "industri": {
        "name": "Industri",
        "icon": "🏭",
        "description": "Sektor industri dan manufaktur",
        "available": False
    },
    "perdagangan": {
        "name": "Perdagangan",
        "icon": "🛒",
        "description": "Aktivitas perdagangan dan komersial",
        "available": False
    },
    "inflasi_harga": {
        "name": "Inflasi & Harga",
        "icon": "💰",
        "description": "Indeks harga dan tingkat inflasi",
        "available": False
    },
    "transportasi": {
        "name": "Transportasi",
        "icon": "🚗",
        "description": "Infrastruktur transportasi dan pariwisata",
        "available": False
    },
    "neraca_regional": {
        "name": "Neraca Regional",
        "icon": "📊",
        "description": "PDRB dan indikator ekonomi regional",
        "available": True
    },
    "keuangan": {
        "name": "Keuangan",
        "icon": "🏦",
        "description": "Sektor keuangan dan investasi",
        "available": False
    },
    "penduduk": {
        "name": "Penduduk",
        "icon": "👥",
        "description": "Demografi dan ketenagakerjaan",
        "available": False
    },
    "sosial": {
        "name": "Sosial",
        "icon": "❤️",
        "description": "Kesehatan dan kesejahteraan",
        "available": False
    },
    "perumahan": {
        "name": "Perumahan",
        "icon": "🏘️",
        "description": "Kondisi perumahan dan permukiman",
        "available": False
    }
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
                datasets[key] = pd.read_csv(f'data/{filename}', sep=';')
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
                display_name = f"✅ {sector['name']}"
            else:
                display_name = f"⏳ {sector['name']}"
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
            <p>Terus dikembangkan dengan fitur upload otomatis untuk sektor baru</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class="sidebar-card">
            <h3>⚡ Quick Actions</h3>
            <p>Navigasi cepat ke fitur utama dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.selected_sector = "beranda"
                st.rerun()
        with col2:
            if st.button("📊 Neraca", use_container_width=True):
                st.session_state.selected_sector = "neraca_regional"
                st.rerun()
    
    # Main Content Area
    if st.session_state.selected_sector == "beranda":
        show_beranda(datasets)
    elif st.session_state.selected_sector == "neraca_regional":
        show_neraca_regional(datasets)
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