import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="Dashboard Pembangunan Aceh",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .section-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 3rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 4px solid #3498db;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(90deg, #e74c3c, #f39c12);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 1.5rem;
        transform: translateY(0);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.3s ease;
        opacity: 0;
    }
    
    .metric-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
    }
    
    .metric-card:hover::before {
        opacity: 1;
        animation: shimmer 1.5s ease-in-out;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) rotate(45deg); }
        100% { transform: translateX(100%) rotate(45deg); }
    }
    
    .metric-value {
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
        line-height: 1.4;
    }
    
    .chart-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2.5rem;
        border: 1px solid rgba(0,0,0,0.05);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    }
    
    .chart-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
    }
    
    .sidebar-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #3498db;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    
    .sidebar-title {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .stats-overview {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(116, 185, 255, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stats-overview::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .sector-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .sector-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .sector-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff7675, #fd79a8, #fdcb6e);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .sector-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .sector-card:hover::before {
        transform: scaleX(1);
    }
    
    .table-container {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    .stSelectbox > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sector definitions
SECTORS = {
    "overview": {
        "name": "Dashboard Umum",
        "icon": "🏠",
        "description": "Ringkasan statistik pembangunan Aceh"
    },
    "sejarah": {
        "name": "Sejarah", 
        "icon": "📖",
        "description": "Sejarah Aceh"
    },
    "geografis": {
        "name": "Geografis", 
        "icon": "🗺️",
        "description": "Kondisi geografis dan wilayah"
    },
    "pemerintahan": {
        "name": "Pemerintahan",
        "icon": "🏛️", 
        "description": "Struktur dan administrasi pemerintahan"
    },
    "pertanian": {
        "name": "Pertanian",
        "icon": "🌾",
        "description": "Sektor pertanian dan perkebunan"
    },
    "listrik_gas_air": {
        "name": "Listrik, Gas, dan Air",
        "icon": "⚡",
        "description": "Infrastruktur energi dan air"
    },
    "industri": {
        "name": "Industri",
        "icon": "🏭",
        "description": "Sektor industri dan manufaktur"
    },
    "perdagangan": {
        "name": "Perdagangan",
        "icon": "🛒",
        "description": "Aktivitas perdagangan dan komersial"
    },
    "inflasi_harga": {
        "name": "Inflasi dan Harga",
        "icon": "💰",
        "description": "Indeks harga dan inflasi"
    },
    "transportasi": {
        "name": "Transportasi, Telekomunikasi, dan Pariwisata",
        "icon": "🚗",
        "description": "Infrastruktur transportasi dan pariwisata"
    },
    "neraca_regional": {
        "name": "Neraca Regional",
        "icon": "📊",
        "description": "PDRB dan indikator ekonomi regional"
    },
    "keuangan": {
        "name": "Keuangan, Perbankan, dan Investasi",
        "icon": "🏦",
        "description": "Sektor keuangan dan investasi"
    },
    "penduduk": {
        "name": "Penduduk dan Ketenagakerjaan",
        "icon": "👥",
        "description": "Demografi dan ketenagakerjaan"
    },
    "sosial": {
        "name": "Sosial dan Kesejahteraan Rakyat",
        "icon": "❤️",
        "description": "Kesehatan, pendidikan, dan kesejahteraan"
    },
    "perumahan": {
        "name": "Perumahan",
        "icon": "🏘️",
        "description": "Kondisi perumahan dan permukiman"
    }
}

# Load data function
@st.cache_data
def load_data():
    """Load and process all dataset files"""
    try:
        data_dict = {
            'pdrb': pd.read_csv('data/PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv', sep=';'),
            'growth': pd.read_csv('data/Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv', sep=';'),
            'sector_migas': pd.read_csv('data/Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv', sep=';'),
            'sector_nonmigas': pd.read_csv('data/Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv', sep=';'),
            'expenditure': pd.read_csv('data/Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv', sep=';'),
            'percapita': pd.read_csv('data/PDRB Per Kapita Aceh 10.6.csv', sep=';'),
            'regional_contrib': pd.read_csv('data/Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv', sep=';'),
            'percapita_kab': pd.read_csv('data/PDRB Per Kapita Kabupaten atau Kota 10.8.csv', sep=';')
        }
        return data_dict
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def show_overview_dashboard():
    """Display overview dashboard with general statistics"""
    st.markdown('<h1 class="main-header">Dashboard Pembangunan Provinsi Aceh</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Visualisasi Data Pembangunan Multi-Sektor dari Masa ke Masa (1975-2013)</p>', unsafe_allow_html=True)
    
    # Overview stats
    st.markdown("""
    <div class="stats-overview">
        <h2 style="margin-bottom: 2rem; font-size: 2.5rem; font-weight: 700;">Statistik Umum Pembangunan Aceh</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; margin-top: 2rem;">
            <div>
                <div style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">39</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">Tahun Data Historis</div>
            </div>
            <div>
                <div style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">14</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">Sektor Pembangunan</div>
            </div>
            <div>
                <div style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">23</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">Kabupaten/Kota</div>
            </div>
            <div>
                <div style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">1975-2013</div>
                <div style="font-size: 1.2rem; opacity: 0.9;">Periode Data</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sector grid
    st.markdown('<h2 class="section-header">Pilih Sektor untuk Analisis Mendalam</h2>', unsafe_allow_html=True)
    
    # Create grid for sectors (excluding overview)
    sectors_list = [(k, v) for k, v in SECTORS.items() if k != "overview"]
    
    cols = st.columns(3)
    for i, (sector_key, sector_info) in enumerate(sectors_list):
        col_idx = i % 3
        with cols[col_idx]:
            if sector_key == "neraca_regional":
                if st.button(f"{sector_info['icon']} {sector_info['name']}", key=f"btn_{sector_key}", use_container_width=True):
                    st.session_state.selected_sector = sector_key
                    st.rerun()
                st.caption(sector_info['description'])
            else:
                st.button(f"{sector_info['icon']} {sector_info['name']}", key=f"btn_{sector_key}", disabled=True, use_container_width=True)
                st.caption(f"{sector_info['description']} (Coming Soon)")

def create_pdrb_chart(data, title):
    """Create PDRB chart"""
    migas_data = data[data['migas dan non migas'] == 'Migas'].copy()
    nonmigas_data = data[data['migas dan non migas'] == 'NonMigas'].copy()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('PDRB Atas Dasar Harga Berlaku (ADHB)', 'PDRB Atas Dasar Harga Konstan (ADHK)'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # ADHB
    fig.add_trace(
        go.Scatter(x=migas_data['tahun'], y=migas_data['PDRB ADHB'], 
                  name='Migas ADHB', line=dict(color='#e74c3c', width=3),
                  marker=dict(size=6)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=nonmigas_data['tahun'], y=nonmigas_data['PDRB ADHB'],
                  name='Non-Migas ADHB', line=dict(color='#3498db', width=3),
                  marker=dict(size=6)),
        row=1, col=1
    )
    
    # ADHK
    fig.add_trace(
        go.Scatter(x=migas_data['tahun'], y=migas_data['PDRB ADHK'],
                  name='Migas ADHK', line=dict(color='#e67e22', width=3),
                  marker=dict(size=6)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=nonmigas_data['tahun'], y=nonmigas_data['PDRB ADHK'],
                  name='Non-Migas ADHK', line=dict(color='#2980b9', width=3),
                  marker=dict(size=6)),
        row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        showlegend=True,
        title_text=title,
        title_x=0.5,
        title_font_size=18,
        font_family="Poppins"
    )
    
    fig.update_xaxes(title_text="Tahun")
    fig.update_yaxes(title_text="Nilai (Juta Rupiah)")
    
    return fig

def create_growth_chart(data, title):
    """Create economic growth chart"""
    migas_growth = data[data['migas dan non migas'] == 'Migas'].copy()
    nonmigas_growth = data[data['migas dan non migas'] == 'NonMigas'].copy()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=migas_growth['tahun'], 
        y=migas_growth['pertumbuhan ekonomi'],
        mode='lines+markers',
        name='Pertumbuhan Sektor Migas',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=nonmigas_growth['tahun'], 
        y=nonmigas_growth['pertumbuhan ekonomi'],
        mode='lines+markers',
        name='Pertumbuhan Sektor Non-Migas',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8),
        fill='tonexty',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="rgba(0,0,0,0.3)", 
                  annotation_text="Baseline (0%)", annotation_position="right")
    
    fig.update_layout(
        title=title,
        xaxis_title="Tahun",
        yaxis_title="Tingkat Pertumbuhan (%)",
        height=500,
        hovermode='x unified',
        font_family="Poppins",
        showlegend=True
    )
    
    return fig

def create_sector_contribution_chart(data, title_suffix, sector_col):
    """Create sector contribution chart"""
    sectors = data[sector_col].unique()
    
    fig = go.Figure()
    colors = px.colors.qualitative.Set3
    
    for i, sector in enumerate(sectors):
        sector_data = data[data[sector_col] == sector]
        fig.add_trace(go.Scatter(
            x=sector_data['tahun'],
            y=sector_data['kontribusi PDRB'],
            mode='lines+markers',
            name=sector,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=6),
            stackgroup='one' if 'Pengeluaran' not in title_suffix else None
        ))
    
    fig.update_layout(
        title=f"Kontribusi {title_suffix} terhadap PDRB Provinsi Aceh",
        xaxis_title="Tahun",
        yaxis_title="Kontribusi (%)",
        height=500,
        hovermode='x unified',
        font_family="Poppins"
    )
    
    return fig

def create_percapita_chart(data, title):
    """Create per capita chart"""
    migas_pc = data[data['migas dan non migas'] == 'Migas'].copy()
    nonmigas_pc = data[data['migas dan non migas'] == 'NonMigas'].copy()
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('PDRB Per Kapita ADHB', 'PDRB Per Kapita ADHK')
    )
    
    fig.add_trace(
        go.Scatter(x=migas_pc['tahun'], y=migas_pc['ADHB'], name='Migas ADHB',
                  line=dict(color='#e74c3c', width=3), marker=dict(size=6)), row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=nonmigas_pc['tahun'], y=nonmigas_pc['ADHB'], name='Non-Migas ADHB',
                  line=dict(color='#3498db', width=3), marker=dict(size=6)), row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=migas_pc['tahun'], y=migas_pc['ADHK'], name='Migas ADHK',
                  line=dict(color='#e67e22', width=3), marker=dict(size=6)), row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=nonmigas_pc['tahun'], y=nonmigas_pc['ADHK'], name='Non-Migas ADHK',
                  line=dict(color='#2980b9', width=3), marker=dict(size=6)), row=1, col=2
    )
    
    fig.update_layout(
        height=500,
        title_text=title,
        title_x=0.5,
        font_family="Poppins"
    )
    
    fig.update_xaxes(title_text="Tahun")
    fig.update_yaxes(title_text="Nilai Per Kapita (Juta Rupiah)")
    
    return fig

def create_regional_chart(data, title, value_col):
    """Create regional contribution chart"""
    # Get latest year data
    latest_year = data['tahun'].max()
    latest_data = data[data['tahun'] == latest_year]
    
    migas_data = latest_data[latest_data['migas dan non migas'] == 'Migas']
    nonmigas_data = latest_data[latest_data['migas dan non migas'] == 'NonMigas']
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f'Kontribusi Migas ({latest_year})', f'Kontribusi Non-Migas ({latest_year})'),
        specs=[[{"type": "bar"}, {"type": "bar"}]]
    )
    
    fig.add_trace(
        go.Bar(x=migas_data['bps_nama_kabupaten_kota'], y=migas_data[value_col],
               name='Migas', marker_color='#e74c3c'), row=1, col=1
    )
    
    fig.add_trace(
        go.Bar(x=nonmigas_data['bps_nama_kabupaten_kota'], y=nonmigas_data[value_col],
               name='Non-Migas', marker_color='#3498db'), row=1, col=2
    )
    
    fig.update_layout(
        height=600,
        title_text=title,
        title_x=0.5,
        font_family="Poppins"
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig

def show_neraca_regional_dashboard(data_dict, year_range):
    """Display Neraca Regional dashboard with all 8 charts"""
    st.markdown('<h1 class="section-header">📊 Neraca Regional Provinsi Aceh</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analisis Komprehensif Produk Domestik Regional Bruto dan Indikator Ekonomi</p>', unsafe_allow_html=True)
    
    # Filter data by year range
    filtered_data = {}
    for key, df in data_dict.items():
        if 'tahun' in df.columns:
            filtered_data[key] = df[(df['tahun'] >= year_range[0]) & (df['tahun'] <= year_range[1])]
        else:
            filtered_data[key] = df
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate metrics from filtered data
    pdrb_data = filtered_data['pdrb']
    latest_year_data = pdrb_data[pdrb_data['tahun'] == pdrb_data['tahun'].max()]
    
    migas_adhb = latest_year_data[latest_year_data['migas dan non migas'] == 'Migas']['PDRB ADHB'].iloc[0] if not latest_year_data.empty else 0
    nonmigas_adhb = latest_year_data[latest_year_data['migas dan non migas'] == 'NonMigas']['PDRB ADHB'].iloc[0] if not latest_year_data.empty else 0
    total_pdrb = migas_adhb + nonmigas_adhb
    
    growth_data = filtered_data['growth']
    avg_growth = growth_data['pertumbuhan ekonomi'].mean() if not growth_data.empty else 0
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{total_pdrb:,.0f}</div>
            <div class="metric-label">Total PDRB ADHB<br>(Juta Rupiah)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{avg_growth:.2f}%</div>
            <div class="metric-label">Rata-rata<br>Pertumbuhan Ekonomi</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        migas_contribution = (migas_adhb / total_pdrb * 100) if total_pdrb > 0 else 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{migas_contribution:.1f}%</div>
            <div class="metric-label">Kontribusi Sektor<br>Migas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        nonmigas_contribution = (nonmigas_adhb / total_pdrb * 100) if total_pdrb > 0 else 0
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-value">{nonmigas_contribution:.1f}%</div>
            <div class="metric-label">Kontribusi Sektor<br>Non-Migas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Chart 1: PDRB ADHB & ADHK
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">10.1 Produk Domestik Regional Bruto (PDRB) Atas Dasar Harga Berlaku dan Konstan dengan Migas dan Non-Migas</h3>', unsafe_allow_html=True)
    pdrb_fig = create_pdrb_chart(filtered_data['pdrb'], "PDRB Provinsi Aceh: Migas vs Non-Migas")
    st.plotly_chart(pdrb_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 2: Economic Growth
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">10.2 Pertumbuhan Ekonomi Aceh Sektor Migas dan Non-Migas</h3>', unsafe_allow_html=True)
    growth_fig = create_growth_chart(filtered_data['growth'], "Pertumbuhan Ekonomi Provinsi Aceh")
    st.plotly_chart(growth_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 3 & 4: Sector Contributions (side by side)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">10.3 Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas</h3>', unsafe_allow_html=True)
        sector_migas_fig = create_sector_contribution_chart(
            filtered_data['sector_migas'], "Kelompok Sektor Dengan Migas", 'kelompok sektor dengan migas'
        )
        st.plotly_chart(sector_migas_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">10.4 Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas</h3>', unsafe_allow_html=True)
        sector_nonmigas_fig = create_sector_contribution_chart(
            filtered_data['sector_nonmigas'], "Kelompok Sektor Non-Migas", 'kelompok sektor dengan non migas'
        )
        st.plotly_chart(sector_nonmigas_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 5: Expenditure Contribution
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">10.5 Kontribusi PDRB Menurut Kelompok Pengeluaran</h3>', unsafe_allow_html=True)
    expenditure_fig = create_sector_contribution_chart(
        filtered_data['expenditure'], "Kelompok Pengeluaran", 'kelompok pengeluaran'
    )
    st.plotly_chart(expenditure_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 6: Per Capita PDRB
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h3 class="chart-title">10.6 PDRB Per Kapita Aceh</h3>', unsafe_allow_html=True)
    percapita_fig = create_percapita_chart(filtered_data['percapita'], "PDRB Per Kapita Provinsi Aceh")
    st.plotly_chart(percapita_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chart 7 & 8: Regional Analysis (side by side)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">10.7 Kontribusi Kabupaten/Kota terhadap PDRB</h3>', unsafe_allow_html=True)
        regional_contrib_fig = create_regional_chart(
            filtered_data['regional_contrib'], "Kontribusi Regional terhadap PDRB", 'kontribusi PDRB'
        )
        st.plotly_chart(regional_contrib_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<h3 class="chart-title">10.8 PDRB Per Kapita Kabupaten/Kota</h3>', unsafe_allow_html=True)
        percapita_kab_fig = create_regional_chart(
            filtered_data['percapita_kab'], "PDRB Per Kapita Regional", 'kontribusi PDRB'
        )
        st.plotly_chart(percapita_kab_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Data Tables Section
    st.markdown('<h2 class="section-header">Data Tables</h2>', unsafe_allow_html=True)
    
    # Create tabs for different data tables
    tab1, tab2, tab3, tab4 = st.tabs([
        "PDRB Data", "Pertumbuhan & Kontribusi", "Per Kapita", "Data Regional"
    ])
    
    with tab1:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Tabel PDRB ADHB dan ADHK")
        pdrb_pivot = filtered_data['pdrb'].pivot_table(
            index='tahun', 
            columns='migas dan non migas', 
            values=['PDRB ADHB', 'PDRB ADHK'], 
            aggfunc='sum'
        )
        st.dataframe(pdrb_pivot, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Tabel Pertumbuhan Ekonomi")
        growth_pivot = filtered_data['growth'].pivot_table(
            index='tahun', 
            columns='migas dan non migas', 
            values='pertumbuhan ekonomi'
        )
        st.dataframe(growth_pivot, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Kontribusi Sektor dengan Migas")
        st.dataframe(filtered_data['sector_migas'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Kontribusi Sektor Non-Migas")
        st.dataframe(filtered_data['sector_nonmigas'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Kontribusi Kelompok Pengeluaran")
        st.dataframe(filtered_data['expenditure'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("PDRB Per Kapita Provinsi")
        st.dataframe(filtered_data['percapita'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("PDRB Per Kapita Kabupaten/Kota")
        st.dataframe(filtered_data['percapita_kab'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        st.subheader("Kontribusi Regional")
        st.dataframe(filtered_data['regional_contrib'], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize session state
    if 'selected_sector' not in st.session_state:
        st.session_state.selected_sector = 'overview'
    
    # Load data
    with st.spinner('Memuat data...'):
        data_dict = load_data()
    
    if data_dict is None:
        st.error("Gagal memuat data. Pastikan file CSV tersedia di folder 'data/'")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="sidebar-title">🎛️ Kontrol Dashboard</h3>', unsafe_allow_html=True)
        
        # Sector selection
        sector_options = [(key, value['name']) for key, value in SECTORS.items()]
        sector_names = [name for _, name in sector_options]
        sector_keys = [key for key, _ in sector_options]
        
        current_index = sector_keys.index(st.session_state.selected_sector) if st.session_state.selected_sector in sector_keys else 0
        
        selected_sector_name = st.selectbox(
            "Pilih Sektor Analisis:",
            sector_names,
            index=current_index
        )
        
        # Update session state based on selection
        selected_sector_key = sector_keys[sector_names.index(selected_sector_name)]
        if selected_sector_key != st.session_state.selected_sector:
            st.session_state.selected_sector = selected_sector_key
            st.rerun()
        
        # Year range selector (only for neraca_regional)
        if st.session_state.selected_sector == 'neraca_regional':
            st.markdown("---")
            year_range = st.slider(
                "Rentang Tahun Analisis:", 
                min_value=1975, 
                max_value=2013, 
                value=(1975, 2013),
                step=1
            )
        else:
            year_range = (1975, 2013)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Info section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="sidebar-title">ℹ️ Informasi Dashboard</h3>', unsafe_allow_html=True)
        
        if st.session_state.selected_sector in SECTORS:
            sector_info = SECTORS[st.session_state.selected_sector]
            st.markdown(f"**Sektor Aktif:** {sector_info['icon']} {sector_info['name']}")
            st.markdown(f"**Deskripsi:** {sector_info['description']}")
        
        st.markdown("---")
        st.markdown("""
        **Sumber Data:** BPS Provinsi Aceh & BAPPEDA Aceh
        
        **Periode Data:** 1975-2013
        
        **Update Terakhir:** Desember 2024
        
        **Status Sektor:**
        - ✅ Neraca Regional (Tersedia)
        - ⏳ 13 Sektor Lainnya (Coming Soon)
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content based on selected sector
    if st.session_state.selected_sector == 'overview':
        show_overview_dashboard()
    elif st.session_state.selected_sector == 'neraca_regional':
        show_neraca_regional_dashboard(data_dict, year_range)
    else:
        # Coming soon page for other sectors
        sector_info = SECTORS[st.session_state.selected_sector]
        st.markdown('<h1 class="main-header">🚧 Coming Soon</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="subtitle">Sektor {sector_info["icon"]} {sector_info["name"]} sedang dalam pengembangan</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stats-overview">
            <h2 style="margin-bottom: 2rem;">Sektor Ini Akan Segera Tersedia</h2>
            <p style="font-size: 1.2rem; opacity: 0.9;">
                Kami sedang mengembangkan visualisasi data untuk sektor ini. 
                Sementara waktu, Anda dapat mengeksplorasi data Neraca Regional yang sudah tersedia.
            </p>
            <br>
        """, unsafe_allow_html=True)
        
        if st.button("🏠 Kembali ke Dashboard Umum", key="back_to_overview"):
            st.session_state.selected_sector = 'overview'
            st.rerun()
        
        if st.button("📊 Lihat Neraca Regional", key="goto_neraca"):
            st.session_state.selected_sector = 'neraca_regional'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 30px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 15px; margin-top: 3rem;'>
        <h3 style='color: #2c3e50; margin-bottom: 1rem;'>Dashboard Pembangunan Provinsi Aceh</h3>
        <p style='font-size: 1.1rem; margin-bottom: 0.5rem;'><strong>Dikembangkan untuk UPTD Statistik Diskominsa Aceh</strong></p>
        <p style='margin-bottom: 0.5rem;'>Data Source: BPS Provinsi Aceh & BAPPEDA Aceh</p>
        <p style='margin-bottom: 1rem;'>Visualisasi Data Pembangunan Multi-Sektor dari Masa ke Masa (1975-2013)</p>
        <p style='font-size: 0.9rem; color: #7f8c8d;'>© 2024 - Interactive Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()