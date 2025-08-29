# Enhanced Configuration file for Aceh Development Dashboard

# App settings
APP_TITLE = "Dashboard Pembangunan Provinsi Aceh"
APP_ICON = "🏛️"
APP_LAYOUT = "wide"
APP_VERSION = "2.0"

# Data settings
DATA_PATH = "data/"
YEAR_RANGE = (1975, 2013)

# Complete sector mapping with detailed information
SECTORS = {
    "overview": {
        "name": "Dashboard Umum",
        "icon": "🏠",
        "description": "Ringkasan statistik pembangunan Aceh",
        "bab": "Home",
        "available": True
    },
    "geografis": {
        "name": "Geografis", 
        "icon": "🗺️",
        "description": "Kondisi geografis dan wilayah",
        "bab": "BAB II",
        "available": False
    },
    "pemerintahan": {
        "name": "Pemerintahan",
        "icon": "🏛️", 
        "description": "Struktur dan administrasi pemerintahan",
        "bab": "BAB III",
        "available": False
    },
    "pertanian": {
        "name": "Pertanian",
        "icon": "🌾",
        "description": "Sektor pertanian dan perkebunan",
        "bab": "BAB IV",
        "available": False
    },
    "listrik_gas_air": {
        "name": "Listrik, Gas, dan Air",
        "icon": "⚡",
        "description": "Infrastruktur energi dan air",
        "bab": "BAB V",
        "available": False
    },
    "industri": {
        "name": "Industri",
        "icon": "🏭",
        "description": "Sektor industri dan manufaktur",
        "bab": "BAB VI",
        "available": False
    },
    "perdagangan": {
        "name": "Perdagangan",
        "icon": "🛒",
        "description": "Aktivitas perdagangan dan komersial",
        "bab": "BAB VII",
        "available": False
    },
    "inflasi_harga": {
        "name": "Inflasi dan Harga",
        "icon": "💰",
        "description": "Indeks harga dan inflasi",
        "bab": "BAB VIII",
        "available": False
    },
    "transportasi": {
        "name": "Transportasi, Telekomunikasi, dan Pariwisata",
        "icon": "🚗",
        "description": "Infrastruktur transportasi dan pariwisata",
        "bab": "BAB IX",
        "available": False
    },
    "neraca_regional": {
        "name": "Neraca Regional",
        "icon": "📊",
        "description": "PDRB dan indikator ekonomi regional",
        "bab": "BAB X",
        "available": True
    },
    "keuangan": {
        "name": "Keuangan, Perbankan, dan Investasi",
        "icon": "🏦",
        "description": "Sektor keuangan dan investasi",
        "bab": "BAB XI",
        "available": False
    },
    "penduduk": {
        "name": "Penduduk dan Ketenagakerjaan",
        "icon": "👥",
        "description": "Demografi dan ketenagakerjaan",
        "bab": "BAB XII",
        "available": False
    },
    "sosial": {
        "name": "Sosial dan Kesejahteraan Rakyat",
        "icon": "❤️",
        "description": "Kesehatan, pendidikan, dan kesejahteraan",
        "bab": "BAB XIII",
        "available": False
    },
    "perumahan": {
        "name": "Perumahan",
        "icon": "🏘️",
        "description": "Kondisi perumahan dan permukiman",
        "bab": "BAB XIV",
        "available": False
    }
}

# Data type mapping for Neraca Regional - Complete dataset information
NERACA_REGIONAL_DATA_TYPES = {
    "pdrb_adhb_adhk": {
        "code": "10.1",
        "title": "PDRB ADHB dan ADHK dengan Migas dan Non-Migas",
        "file": "PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv",
        "icon": "📈",
        "description": "Produk Domestik Regional Bruto Atas Dasar Harga Berlaku dan Konstan",
        "period": "1975-2013",
        "classification": "Migas dan Non Migas",
        "unit": "Juta Rupiah"
    },
    "pertumbuhan_ekonomi": {
        "code": "10.2",
        "title": "Pertumbuhan Ekonomi Aceh Migas dan Non-Migas",
        "file": "Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv",
        "icon": "📊",
        "description": "Tingkat pertumbuhan ekonomi sektor migas dan non-migas",
        "period": "1975-2013",
        "classification": "Migas dan Non Migas",
        "unit": "%"
    },
    "kontribusi_sektor_migas": {
        "code": "10.3",
        "title": "Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas",
        "file": "Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv",
        "icon": "🥧",
        "description": "Kontribusi berbagai sektor terhadap PDRB dengan migas",
        "period": "1969-2013",
        "classification": "Kelompok Sektor dengan Migas",
        "unit": "%"
    },
    "kontribusi_sektor_nonmigas": {
        "code": "10.4",
        "title": "Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas",
        "file": "Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv",
        "icon": "🏭",
        "description": "Kontribusi berbagai sektor terhadap PDRB non-migas",
        "period": "1975-2013",
        "classification": "Kelompok Sektor dengan Non Migas",
        "unit": "%"
    },
    "kontribusi_pengeluaran": {
        "code": "10.5",
        "title": "Kontribusi PDRB Menurut Kelompok Pengeluaran",
        "file": "Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv",
        "icon": "💸",
        "description": "Kontribusi kelompok pengeluaran terhadap PDRB",
        "period": "1969-2013",
        "classification": "Kelompok Pengeluaran",
        "unit": "%"
    },
    "pdrb_per_kapita": {
        "code": "10.6",
        "title": "PDRB Per Kapita Aceh",
        "file": "PDRB Per Kapita Aceh 10.6.csv",
        "icon": "👥",
        "description": "PDRB per kapita penduduk Aceh",
        "period": "1975-2013",
        "classification": "Migas dan Non Migas",
        "unit": "Juta Rupiah"
    },
    "kontribusi_regional": {
        "code": "10.7",
        "title": "Kontribusi Kabupaten/Kota terhadap PDRB",
        "file": "Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv",
        "icon": "🗺️",
        "description": "Kontribusi kabupaten/kota terhadap PDRB",
        "period": "2000-2013",
        "classification": "Migas dan Non Migas",
        "unit": "%"
    },
    "pdrb_per_kapita_kab": {
        "code": "10.8",
        "title": "PDRB Per Kapita Kabupaten/Kota",
        "file": "PDRB Per Kapita Kabupaten atau Kota 10.8.csv",
        "icon": "🏘️",
        "description": "PDRB per kapita tingkat kabupaten/kota",
        "period": "2000-2013",
        "classification": "Migas dan Non Migas",
        "unit": "Juta Rupiah"
    }
}

# Enhanced color schemes
COLOR_SCHEMES = {
    "primary": [
        "#e74c3c", "#3498db", "#2ecc71", "#f39c12", 
        "#9b59b6", "#1abc9c", "#34495e", "#e67e22"
    ],
    "migas_nonmigas": ["#e74c3c", "#3498db"],
    "gradient_red": ["#ff7675", "#fd79a8"],
    "gradient_blue": ["#74b9ff", "#0984e3"],
    "gradient_green": ["#00b894", "#00cec9"],
    "sector_colors": [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", 
        "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
        "#FF8A80", "#82B1FF", "#B39DDB", "#A5D6A7"
    ],
    "regional_colors": [
        "#3498db", "#e74c3c", "#2ecc71", "#f39c12",
        "#9b59b6", "#1abc9c", "#e67e22", "#34495e"
    ]
}

# Enhanced chart configuration
CHART_CONFIG = {
    "height": 500,
    "height_large": 600,
    "height_small": 400,
    "margin": {"l": 60, "r": 60, "t": 100, "b": 60},
    "font_family": "Poppins, sans-serif",
    "title_font_size": 20,
    "axis_font_size": 14,
    "legend_font_size": 12,
    "template": "plotly_white"
}

# Regional data - Complete list of Kabupaten/Kota in Aceh
KABUPATEN_KOTA = [
    {"kode": 1101, "nama": "Kabupaten Simeulue"},
    {"kode": 1102, "nama": "Kabupaten Aceh Singkil"},
    {"kode": 1103, "nama": "Kabupaten Aceh Selatan"},
    {"kode": 1104, "nama": "Kabupaten Aceh Tenggara"},
    {"kode": 1105, "nama": "Kabupaten Aceh Timur"},
    {"kode": 1106, "nama": "Kabupaten Aceh Tengah"},
    {"kode": 1107, "nama": "Kabupaten Aceh Barat"},
    {"kode": 1108, "nama": "Kabupaten Aceh Besar"},
    {"kode": 1109, "nama": "Kabupaten Pidie"},
    {"kode": 1110, "nama": "Kabupaten Bireuen"},
    {"kode": 1111, "nama": "Kabupaten Aceh Utara"},
    {"kode": 1112, "nama": "Kabupaten Aceh Barat Daya"},
    {"kode": 1113, "nama": "Kabupaten Gayo Lues"},
    {"kode": 1114, "nama": "Kabupaten Aceh Tamiang"},
    {"kode": 1115, "nama": "Kabupaten Nagan Raya"},
    {"kode": 1116, "nama": "Kabupaten Aceh Jaya"},
    {"kode": 1117, "nama": "Kabupaten Bener Meriah"},
    {"kode": 1118, "nama": "Kabupaten Pidie Jaya"},
    {"kode": 1171, "nama": "Kota Banda Aceh"},
    {"kode": 1172, "nama": "Kota Sabang"},
    {"kode": 1173, "nama": "Kota Langsa"},
    {"kode": 1174, "nama": "Kota Lhokseumawe"},
    {"kode": 1175, "nama": "Kota Subulussalam"}
]

# Database and API settings (for future expansion)
DATABASE_CONFIG = {
    "enabled": False,
    "host": "localhost",
    "port": 5432,
    "database": "aceh_development",
    "user": "dashboard_user",
    "password": ""
}

# Analytics and tracking
ANALYTICS_CONFIG = {
    "google_analytics": "",
    "track_usage": False,
    "session_timeout": 3600
}

# Export settings
EXPORT_CONFIG = {
    "formats": ["CSV", "Excel", "PDF"],
    "max_rows": 10000,
    "include_charts": True
}

# Performance settings
PERFORMANCE_CONFIG = {
    "cache_ttl": 3600,  # 1 hour
    "max_cache_size": 100,
    "lazy_loading": True
}

# UI/UX settings
UI_CONFIG = {
    "theme": "light",
    "animations": True,
    "responsive": True,
    "sidebar_default": "expanded"
}

# Data validation rules
DATA_VALIDATION = {
    "required_columns": {
        "pdrb": ["tahun", "migas dan non migas", "PDRB ADHB", "PDRB ADHK"],
        "growth": ["tahun", "migas dan non migas", "pertumbuhan ekonomi"],
        "sector": ["tahun", "kontribusi PDRB"],
        "percapita": ["tahun", "migas dan non migas", "ADHB", "ADHK"],
        "regional": ["tahun", "bps_nama_kabupaten_kota", "kontribusi PDRB"]
    },
    "data_types": {
        "tahun": "int",
        "PDRB ADHB": "float",
        "PDRB ADHK": "float",
        "pertumbuhan ekonomi": "float",
        "kontribusi PDRB": "float"
    },
    "value_ranges": {
        "tahun": (1969, 2013),
        "pertumbuhan ekonomi": (-100, 200),
        "kontribusi PDRB": (0, 100)
    }
}