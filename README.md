# Dashboard Pembangunan Provinsi Aceh

Dashboard interaktif berbasis web untuk visualisasi data pembangunan Provinsi Aceh dari masa ke masa (1975-2013). Dashboard ini dikembangkan menggunakan Streamlit dan menyediakan analisis komprehensif terhadap berbagai aspek pembangunan daerah.

## 🚀 Fitur Utama

- **Visualisasi Interaktif**: Grafik dan chart dinamis dengan Plotly
- **Multi-Sektor Analysis**: Analisis 14 sektor pembangunan (saat ini tersedia Neraca Regional)
- **Filter Temporal**: Kontrol rentang tahun untuk analisis periode tertentu
- **Responsive Design**: Tampilan optimal di desktop, tablet, dan mobile
- **Real-time Analytics**: Perhitungan statistik dan trend secara real-time
- **Export Data**: Kemampuan ekspor data dan visualisasi

## 📊 Data yang Tersedia

### Neraca Regional (Tersedia)
1. **PDRB ADHB & ADHK** - Produk Domestik Regional Bruto
2. **Pertumbuhan Ekonomi** - Tingkat pertumbuhan sektor migas dan non-migas
3. **Kontribusi Sektor** - Kontribusi berbagai sektor terhadap PDRB
4. **PDRB Per Kapita** - PDRB per kapita penduduk
5. **Kontribusi Regional** - Kontribusi kabupaten/kota terhadap PDRB

### Sektor Lain (Coming Soon)
- Pertanian
- Listrik, Gas, dan Air
- Industri
- Perdagangan
- Dan 7 sektor lainnya

## 🛠️ Instalasi dan Setup

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package installer)

### Langkah Instalasi

1. **Clone atau download project ini**
```bash
git clone [repository-url]
cd aceh-development-dashboard
```

2. **Jalankan script setup otomatis**
```bash
python setup.py
```

Atau lakukan instalasi manual:

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Buat sample data**
```bash
python data_processor.py
```

5. **Jalankan aplikasi**
```bash
streamlit run main_app.py
```

Dashboard akan tersedia di: `http://localhost:8501`

## 📁 Struktur Project

```
aceh-development-dashboard/
├── main_app.py              # Aplikasi utama Streamlit
├── config.py                # Konfigurasi dan pengaturan
├── utils.py                 # Fungsi utilitas dan helper
├── data_processor.py        # Pemrosesan dan generasi data
├── requirements.txt         # Dependencies Python
├── setup.py                 # Script setup otomatis
├── README.md               # Dokumentasi ini
└── data/                   # Direktori data CSV
    ├── PDRB_ADHB_ADHK.csv
    ├── pertumbuhan_ekonomi.csv
    ├── kontribusi_sektor_migas.csv
    ├── kontribusi_sektor_nonmigas.csv
    ├── kontribusi_pengeluaran.csv
    ├── pdrb_per_kapita.csv
    ├── kontribusi_kabupaten_kota.csv
    └── pdrb_per_kapita_kabupaten.csv
```

## 🎯 Cara Penggunaan

### 1. Navigasi Dashboard
- **Sidebar**: Pilih sektor dan atur rentang tahun
- **Header**: Tombol jenis data untuk navigasi cepat
- **Main Area**: Visualisasi dan tabel data

### 2. Filter Data
- Gunakan slider tahun untuk memfilter periode analisis
- Pilih jenis data dengan tombol di header
- Gunakan tabs untuk membandingkan sub-kategori

### 3. Interpretasi Visualisasi
- **Line Charts**: Menunjukkan trend temporal
- **Bar Charts**: Perbandingan antar kategori
- **Pie Charts**: Proporsi kontribusi
- **Heatmaps**: Analisis regional

## 🔧 Kustomisasi

### Menambah Data Baru
1. Tambahkan file CSV ke folder `data/`
2. Update `config.py` untuk mapping data baru
3. Buat fungsi visualisasi di `utils.py`
4. Update `main_app.py` untuk UI baru

### Mengubah Tampilan
1. Edit `CUSTOM_CSS` di `config.py`
2. Modifikasi `COLOR_SCHEMES` untuk skema warna
3. Update `CHART_CONFIG` untuk pengaturan grafik

## 📈 Fitur Visualisasi

### Grafik Tersedia
- **Time Series Analysis**: Analisis trend temporal
- **Comparison Charts**: Perbandingan kategori
- **Multi-line Charts**: Perbandingan multi-variabel
- **Stacked Area Charts**: Kontribusi kumulatif
- **Regional Heatmaps**: Analisis spasial
- **Box Plots**: Analisis distribusi

### Metrik Statistik
- Rata-rata, median, standar deviasi
- Nilai minimum dan maksimum
- Tingkat pertumbuhan (CAGR)
- Analisis korelasi
- Deteksi outlier

## 🌐 Deploy ke Production

### Streamlit Cloud
1. Upload project ke GitHub
2. Connect ke Streamlit Cloud
3. Deploy dengan satu klik

### Heroku
1. Buat `Procfile`:
```
web: sh setup.sh && streamlit run main_app.py
```
2. Deploy via Heroku CLI atau GitHub integration

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "main_app.py"]
```

## 🤝 Kontribusi

1. Fork project ini
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📄 Lisensi

Project ini dikembangkan untuk UPTD Statistik Diskominsa Aceh. Menggunakan data dari BPS Provinsi Aceh dan BAPPEDA Aceh.

## 📞 Support

Untuk bantuan teknis atau pertanyaan:
- Email: [your-email@domain.com]
- GitHub Issues: [repository-url]/issues

## 🙏 Acknowledgments

- **BPS Provinsi Aceh** - Sumber data statistik
- **BAPPEDA Aceh** - Data pembangunan daerah
- **UPTD Statistik Diskominsa Aceh** - Sponsor project
- **Streamlit Community** - Framework visualization

---

**Dashboard Pembangunan Provinsi Aceh** - Visualisasi Data Pembangunan dari Masa ke Masa