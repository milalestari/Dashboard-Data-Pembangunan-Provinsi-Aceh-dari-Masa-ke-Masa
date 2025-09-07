import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_sample_data():
    """Create comprehensive sample data files for Aceh Development Dashboard"""
    
    print("=" * 70)
    print("CREATING ACEH DEVELOPMENT DASHBOARD SAMPLE DATA")
    print("=" * 70)
    
    # Create data directory
    if not os.path.exists('data'):
        os.makedirs('data')
        print("✓ Created 'data' directory")
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # 1. PDRB ADHB dan ADHK data (1975-2013)
    print("\n1. Generating PDRB ADHB & ADHK data...")
    years = list(range(1975, 2014))
    pdrb_data = []
    
    # Base values for 1975
    base_migas_adhb = 192133.61
    base_migas_adhk = 192133.61
    base_nonmigas_adhb = 160389.88
    base_nonmigas_adhk = 160389.88
    
    for year in years:
        year_index = year - 1975
        
        # Migas data with volatility (affected by oil prices)
        if year_index == 0:
            migas_adhb, migas_adhk = base_migas_adhb, base_migas_adhk
            nonmigas_adhb, nonmigas_adhk = base_nonmigas_adhb, base_nonmigas_adhk
        else:
            # Oil boom periods (higher growth) vs normal periods
            oil_boom = year in [1979, 1980, 1981, 2005, 2006, 2007, 2008]
            crisis_period = year in [1998, 1999, 2009]
            
            if oil_boom:
                migas_growth = np.random.normal(25, 15)  # High growth during oil boom
            elif crisis_period:
                migas_growth = np.random.normal(-10, 20)  # Negative growth during crisis
            else:
                migas_growth = np.random.normal(8, 12)  # Normal growth
                
            nonmigas_growth = np.random.normal(5.5, 4)  # More stable growth
            
            # Calculate values
            prev_migas_adhb = pdrb_data[-2]['PDRB ADHB'] if len(pdrb_data) >= 2 else base_migas_adhb
            prev_nonmigas_adhb = pdrb_data[-1]['PDRB ADHB'] if len(pdrb_data) >= 1 else base_nonmigas_adhb
            
            migas_adhb = prev_migas_adhb * (1 + migas_growth/100)
            nonmigas_adhb = prev_nonmigas_adhb * (1 + nonmigas_growth/100)
            
            # ADHK grows more slowly (real terms)
            migas_adhk = migas_adhb * (0.7 + 0.3 * (1 + year_index * 0.02))
            nonmigas_adhk = nonmigas_adhb * (0.8 + 0.2 * (1 + year_index * 0.015))
        
        pdrb_data.extend([
            {
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'migas dan non migas': 'Migas', 
                'PDRB ADHB': max(0, migas_adhb), 
                'PDRB ADHK': max(0, migas_adhk),
                'satuan': 'Juta Rupiah'
            },
            {
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'migas dan non migas': 'NonMigas', 
                'PDRB ADHB': max(0, nonmigas_adhb), 
                'PDRB ADHK': max(0, nonmigas_adhk),
                'satuan': 'Juta Rupiah'
            }
        ])
    
    pd.DataFrame(pdrb_data).to_csv('data neraca regional/PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv', sep=';', index=False)
    print("✓ PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv created")
    
    # 2. Economic Growth data (1976-2013)
    print("\n2. Generating Economic Growth data...")
    growth_data = []
    
    for i, year in enumerate(years[1:], 1):  # Start from 1976
        prev_migas = pdrb_data[(i-1)*2]['PDRB ADHK']  # Previous year migas ADHK
        curr_migas = pdrb_data[i*2]['PDRB ADHK']      # Current year migas ADHK
        prev_nonmigas = pdrb_data[(i-1)*2+1]['PDRB ADHK']
        curr_nonmigas = pdrb_data[i*2+1]['PDRB ADHK']
        
        migas_growth = ((curr_migas - prev_migas) / prev_migas) * 100 if prev_migas > 0 else 0
        nonmigas_growth = ((curr_nonmigas - prev_nonmigas) / prev_nonmigas) * 100 if prev_nonmigas > 0 else 0
        
        growth_data.extend([
            {
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'migas dan non migas': 'Migas', 
                'pertumbuhan ekonomi': migas_growth, 
                'satuan': '%'
            },
            {
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'migas dan non migas': 'NonMigas', 
                'pertumbuhan ekonomi': nonmigas_growth, 
                'satuan': '%'
            }
        ])
    
    pd.DataFrame(growth_data).to_csv('data neraca regional/Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv', sep=';', index=False)
    print("✓ Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv created")
    
    # 3. Sector contribution with migas (1969-2013)
    print("\n3. Generating Sector Contribution (Migas) data...")
    sectors_migas = ['Primer', 'Sekunder', 'Tersier']
    sector_migas_data = []
    
    migas_years = list(range(1969, 2014))
    for year in migas_years:
        # Economic structure evolution over time
        if year < 1980:
            # Early period - agriculture dominated
            primer_base, sekunder_base, tersier_base = 65, 15, 20
        elif year < 1990:
            # Oil boom period - secondary sector grows
            primer_base, sekunder_base, tersier_base = 55, 25, 20
        elif year < 2000:
            # Diversification period
            primer_base, sekunder_base, tersier_base = 45, 30, 25
        else:
            # Modern period - services grow
            primer_base, sekunder_base, tersier_base = 35, 30, 35
        
        # Add some realistic variation
        primer = max(20, primer_base + np.random.normal(0, 5))
        sekunder = max(10, sekunder_base + np.random.normal(0, 4))
        tersier = max(15, tersier_base + np.random.normal(0, 3))
        
        # Normalize to 100%
        total = primer + sekunder + tersier
        primer = (primer / total) * 100
        sekunder = (sekunder / total) * 100
        tersier = (tersier / total) * 100
        
        contributions = [primer, sekunder, tersier]
        
        for i, sector in enumerate(sectors_migas):
            sector_migas_data.append({
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'kelompok sektor dengan migas': sector, 
                'kontribusi PDRB': contributions[i], 
                'satuan': '%'
            })
    
    pd.DataFrame(sector_migas_data).to_csv('data neraca regional/Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv', sep=';', index=False)
    print("✓ Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv created")
    
    # 4. Sector contribution non-migas (1975-2013)
    print("\n4. Generating Sector Contribution (Non-Migas) data...")
    sectors_nonmigas = ['Pertanian', 'Pertambangan & Penggalian', 'Konstruksi', 'Perdagangan, Hotel, & Restoran']
    sector_nonmigas_data = []
    
    for year in years:
        # Realistic sector evolution
        year_progress = (year - 1975) / (2013 - 1975)
        
        # Agriculture declines over time
        pertanian = 35 - (year_progress * 15) + np.random.normal(0, 3)
        # Mining varies with commodity cycles
        pertambangan = 20 + np.random.normal(0, 8)
        # Construction grows with development
        konstruksi = 8 + (year_progress * 5) + np.random.normal(0, 2)
        # Trade/services grow over time
        perdagangan = 12 + (year_progress * 8) + np.random.normal(0, 3)
        
        # Ensure positive values and reasonable proportions
        pertanian = max(15, min(50, pertanian))
        pertambangan = max(5, min(35, pertambangan))
        konstruksi = max(3, min(20, konstruksi))
        perdagangan = max(5, min(25, perdagangan))
        
        contributions = [pertanian, pertambangan, konstruksi, perdagangan]
        
        for i, sector in enumerate(sectors_nonmigas):
            sector_nonmigas_data.append({
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'kelompok sektor dengan non migas': sector, 
                'kontribusi PDRB': contributions[i], 
                'satuan': '%'
            })
    
    pd.DataFrame(sector_nonmigas_data).to_csv('data neraca regional/Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv', sep=';', index=False)
    print("✓ Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv created")
    
    # 5. Expenditure contribution (1969-2013)
    print("\n5. Generating Expenditure Contribution data...")
    expenditure_types = ['Konsumsi Rumah Tangga', 'Konsumsi Pemerintah', 'PMTB', 'Net Ekspor']
    expenditure_data = []
    
    exp_years = list(range(1969, 2014))
    for year in exp_years:
        year_progress = (year - 1969) / (2013 - 1969)
        
        # Consumption patterns change over time
        konsumsi_rt = 55 + np.random.normal(0, 5)  # Household consumption
        konsumsi_gov = 12 + (year_progress * 5) + np.random.normal(0, 2)  # Government grows
        pmtb = 15 + (year_progress * 3) + np.random.normal(0, 3)  # Investment
        net_ekspor = 18 + np.random.normal(0, 10)  # Export varies with commodities
        
        # Ensure positive values
        konsumsi_rt = max(40, min(70, konsumsi_rt))
        konsumsi_gov = max(8, min(25, konsumsi_gov))
        pmtb = max(10, min(25, pmtb))
        net_ekspor = max(5, min(40, net_ekspor))
        
        contributions = [konsumsi_rt, konsumsi_gov, pmtb, net_ekspor]
        
        for i, exp_type in enumerate(expenditure_types):
            expenditure_data.append({
                'bps_kode_provinsi': 11, 
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year,
                'kelompok pengeluaran': exp_type, 
                'kontribusi PDRB': contributions[i], 
                'satuan': '%'
            })
    
    pd.DataFrame(expenditure_data).to_csv('data neraca regional/Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv', sep=';', index=False)
    print("✓ Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv created")
    
    # 6. Per capita PDRB (1975-2013)
    print("\n6. Generating Per Capita PDRB data...")
    percapita_data = []
    
    # Base population and growth assumptions
    base_population = 2800000  # ~2.8 million in 1975
    pop_growth_rate = 0.015    # 1.5% annually
    
    for year in years:
        year_index = year - 1975
        population = base_population * ((1 + pop_growth_rate) ** year_index)
        
        # Get total PDRB for the year
        year_pdrb = [item for item in pdrb_data if item['tahun'] == year]
        migas_pdrb = next(item['PDRB ADHB'] for item in year_pdrb if item['migas dan non migas'] == 'Migas')
        nonmigas_pdrb = next(item['PDRB ADHB'] for item in year_pdrb if item['migas dan non migas'] == 'NonMigas')
        migas_pdrb_k = next(item['PDRB ADHK'] for item in year_pdrb if item['migas dan non migas'] == 'Migas')
        nonmigas_pdrb_k = next(item['PDRB ADHK'] for item in year_pdrb if item['migas dan non migas'] == 'NonMigas')
        
        # Calculate per capita (in millions since PDRB is in million rupiah)
        migas_adhb_pc = migas_pdrb / population
        migas_adhk_pc = migas_pdrb_k / population
        nonmigas_adhb_pc = nonmigas_pdrb / population
        nonmigas_adhk_pc = nonmigas_pdrb_k / population
        
        percapita_data.extend([
            {
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year, 
                'migas dan non migas': 'Migas',
                'ADHB': migas_adhb_pc, 
                'ADHK': migas_adhk_pc, 
                'satuan': 'Juta Rupiah'
            },
            {
                'bps_nama_provinsi': 'Aceh', 
                'tahun': year, 
                'migas dan non migas': 'NonMigas',
                'ADHB': nonmigas_adhb_pc, 
                'ADHK': nonmigas_adhk_pc, 
                'satuan': 'Juta Rupiah'
            }
        ])
    
    pd.DataFrame(percapita_data).to_csv('data neraca regional/PDRB Per Kapita Aceh 10.6.csv', sep=';', index=False)
    print("✓ PDRB Per Kapita Aceh 10.6.csv created")
    
    # 7. Regional contribution (2000-2013) - Kabupaten/Kota level
    print("\n7. Generating Regional Contribution data...")
    kabupaten_list = [
        'Kabupaten Simeulue', 'Kabupaten Aceh Singkil', 'Kabupaten Aceh Selatan', 
        'Kabupaten Aceh Tenggara', 'Kabupaten Aceh Timur', 'Kabupaten Aceh Tengah',
        'Kabupaten Aceh Barat', 'Kabupaten Aceh Besar', 'Kabupaten Pidie',
        'Kabupaten Bireuen', 'Kabupaten Aceh Utara', 'Kota Banda Aceh', 
        'Kota Sabang', 'Kota Langsa', 'Kota Lhokseumawe'
    ]
    
    regional_data = []
    regional_years = list(range(2000, 2014))
    
    # Define economic characteristics for different regions
    region_profiles = {
        'Kota Banda Aceh': {'migas_base': 15, 'nonmigas_base': 18, 'type': 'urban'},
        'Kota Lhokseumawe': {'migas_base': 25, 'nonmigas_base': 12, 'type': 'industrial'},
        'Kota Langsa': {'migas_base': 8, 'nonmigas_base': 10, 'type': 'urban'},
        'Kota Sabang': {'migas_base': 3, 'nonmigas_base': 4, 'type': 'tourism'},
        'Kabupaten Aceh Utara': {'migas_base': 20, 'nonmigas_base': 15, 'type': 'industrial'},
        'Kabupaten Aceh Timur': {'migas_base': 12, 'nonmigas_base': 14, 'type': 'agriculture'},
        'Kabupaten Aceh Besar': {'migas_base': 8, 'nonmigas_base': 12, 'type': 'mixed'},
        'Kabupaten Pidie': {'migas_base': 6, 'nonmigas_base': 8, 'type': 'agriculture'},
        'Kabupaten Bireuen': {'migas_base': 5, 'nonmigas_base': 7, 'type': 'agriculture'}
    }
    
    for year in regional_years:
        for kab in kabupaten_list:
            kode_kab = 1101 + kabupaten_list.index(kab)
            
            # Get base contribution or use default
            if kab in region_profiles:
                profile = region_profiles[kab]
                migas_base = profile['migas_base']
                nonmigas_base = profile['nonmigas_base']
            else:
                # Default for remaining kabupaten
                migas_base = np.random.uniform(1, 5)
                nonmigas_base = np.random.uniform(3, 8)
            
            # Add year-over-year variation
            year_factor = 1 + (year - 2000) * 0.02  # Slight growth over time
            migas_contrib = migas_base * year_factor * (1 + np.random.normal(0, 0.1))
            nonmigas_contrib = nonmigas_base * year_factor * (1 + np.random.normal(0, 0.08))
            
            # Ensure reasonable bounds
            migas_contrib = max(0.5, min(30, migas_contrib))
            nonmigas_contrib = max(1, min(25, nonmigas_contrib))
            
            regional_data.extend([
                {
                    'bps_kode_provinsi': 11, 
                    'bps_nama_provinsi': 'Aceh',
                    'bps_kode_kabupaten_kota': kode_kab, 
                    'bps_nama_kabupaten_kota': kab,
                    'tahun': year, 
                    'migas dan non migas': 'Migas', 
                    'kontribusi PDRB': migas_contrib, 
                    'satuan': '%'
                },
                {
                    'bps_kode_provinsi': 11, 
                    'bps_nama_provinsi': 'Aceh',
                    'bps_kode_kabupaten_kota': kode_kab, 
                    'bps_nama_kabupaten_kota': kab,
                    'tahun': year, 
                    'migas dan non migas': 'NonMigas', 
                    'kontribusi PDRB': nonmigas_contrib, 
                    'satuan': '%'
                }
            ])
    
    pd.DataFrame(regional_data).to_csv('data neraca regional/Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv', sep=';', index=False)
    print("✓ Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv created")
    
    # 8. Per capita Kabupaten/Kota (2000-2013)
    print("\n8. Generating Regional Per Capita data...")
    percapita_kab_data = []
    
    # Population estimates for different regions (in thousands)
    population_estimates = {
        'Kota Banda Aceh': 250, 'Kota Lhokseumawe': 180, 'Kota Langsa': 150,
        'Kota Sabang': 30, 'Kabupaten Aceh Besar': 350, 'Kabupaten Aceh Utara': 550,
        'Kabupaten Aceh Timur': 400, 'Kabupaten Pidie': 420, 'Kabupaten Bireuen': 380
    }
    
    for year in regional_years:
        for kab in kabupaten_list:
            kode_kab = 1101 + kabupaten_list.index(kab)
            
            # Get population estimate or use default
            base_pop = population_estimates.get(kab, np.random.uniform(200, 400))
            year_factor = 1 + (year - 2000) * 0.012  # Population growth
            population = base_pop * year_factor * 1000  # Convert to actual numbers
            
            # Get regional PDRB contribution and calculate per capita
            region_contrib = [item for item in regional_data 
                            if item['bps_nama_kabupaten_kota'] == kab and item['tahun'] == year]
            
            if region_contrib:
                migas_contrib = next(item['kontribusi PDRB'] for item in region_contrib 
                                   if item['migas dan non migas'] == 'Migas')
                nonmigas_contrib = next(item['kontribusi PDRB'] for item in region_contrib 
                                      if item['migas dan non migas'] == 'NonMigas')
                
                # Estimate regional PDRB based on provincial total and contribution
                year_pdrb_data = [item for item in pdrb_data if item['tahun'] == year]
                provincial_migas = next(item['PDRB ADHB'] for item in year_pdrb_data 
                                      if item['migas dan non migas'] == 'Migas')
                provincial_nonmigas = next(item['PDRB ADHB'] for item in year_pdrb_data 
                                         if item['migas dan non migas'] == 'NonMigas')
                
                regional_migas = provincial_migas * (migas_contrib / 100)
                regional_nonmigas = provincial_nonmigas * (nonmigas_contrib / 100)
                
                migas_pc = regional_migas / population
                nonmigas_pc = regional_nonmigas / population
                
                percapita_kab_data.extend([
                    {
                        'bps_kode_provinsi': 11, 
                        'bps_nama_provinsi': 'Aceh',
                        'bps_kode_kabupaten_kota': kode_kab, 
                        'bps_nama_kabupaten_kota': kab,
                        'tahun': year, 
                        'migas dan non migas': 'Migas', 
                        'kontribusi PDRB': migas_pc, 
                        'satuan': 'Juta Rupiah'
                    },
                    {
                        'bps_kode_provinsi': 11, 
                        'bps_nama_provinsi': 'Aceh',
                        'bps_kode_kabupaten_kota': kode_kab, 
                        'bps_nama_kabupaten_kota': kab,
                        'tahun': year, 
                        'migas dan non migas': 'NonMigas', 
                        'kontribusi PDRB': nonmigas_pc, 
                        'satuan': 'Juta Rupiah'
                    }
                ])
    
    pd.DataFrame(percapita_kab_data).to_csv('data neraca regional/PDRB Per Kapita Kabupaten atau Kota 10.8.csv', sep=';', index=False)
    print("✓ PDRB Per Kapita Kabupaten atau Kota 10.8.csv created")
    
    # Summary
    print("\n" + "=" * 70)
    print("DATA GENERATION COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nFiles created in 'data neraca regional/' directory:")
    print("1. ✓ PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv - PDRB data (1975-2013)")
    print("2. ✓ Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv - Economic growth (1976-2013)")
    print("3. ✓ Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv - Sector contribution with oil/gas (1969-2013)")
    print("4. ✓ Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv - Sector contribution without oil/gas (1975-2013)")
    print("5. ✓ Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv - Expenditure contribution (1969-2013)")
    print("6. ✓ PDRB Per Kapita Aceh 10.6.csv - Per capita PDRB (1975-2013)")
    print("7. ✓ Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv - Regional contribution (2000-2013)")
    print("8. ✓ PDRB Per Kapita Kabupaten atau Kota 10.8.csv - Regional per capita (2000-2013)")
    
    print(f"\nTotal data points generated: {len(pdrb_data) + len(growth_data) + len(sector_migas_data) + len(sector_nonmigas_data) + len(expenditure_data) + len(percapita_data) + len(regional_data) + len(percapita_kab_data):,}")
    print("\nData characteristics:")
    print("- Realistic economic trends and volatility")
    print("- Historical events reflected (oil booms, crises)")
    print("- Regional economic diversity")
    print("- Consistent cross-dataset relationships")
    print("- Ready for dashboard visualization")
    
    return True

def validate_generated_data():
    """Validate the generated data files"""
    print("\n" + "=" * 50)
    print("VALIDATING GENERATED DATA")
    print("=" * 50)
    
    files_to_check = [
        'data neraca regional/PDRB ADHB dan ADHK dengan Migas dan Non-Migas 10.1.csv',
        'data neraca regional/Pertumbuhan Ekonomi Aceh Migas dan Non-Migas 10.2.csv', 
        'data neraca regional/Kontribusi PDRB Menurut Kelompok Sektor Dengan Migas 10.3.csv',
        'data neraca regional/Kontribusi PDRB Aceh Menurut Kelompok Sektor Non-Migas 10.4.csv',
        'data neraca regional/Kontribusi PDRB Menurut Kelompok Pengeluaran 10.5.csv',
        'data neraca regional/PDRB Per Kapita Aceh 10.6.csv',
        'data neraca regional/Kontribusi Kabupaten atau Kota terhadap PDRB 10.7.csv',
        'data neraca regional/PDRB Per Kapita Kabupaten atau Kota 10.8.csv'
    ]
    
    validation_results = {}
    
    for file_path in files_to_check:
        filename = file_path.split('/')[-1]
        try:
            df = pd.read_csv(file_path, sep=';')
            validation_results[filename] = {
                'exists': True,
                'rows': len(df),
                'columns': len(df.columns),
                'date_range': None,
                'issues': []
            }
            
            # Check for date range if 'tahun' column exists
            if 'tahun' in df.columns:
                min_year = df['tahun'].min()
                max_year = df['tahun'].max()
                validation_results[filename]['date_range'] = f"{min_year}-{max_year}"
            
            # Check for missing values
            missing_values = df.isnull().sum().sum()
            if missing_values > 0:
                validation_results[filename]['issues'].append(f"{missing_values} missing values")
            
            # Check for negative values in key columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if col != 'pertumbuhan ekonomi' and (df[col] < 0).any():
                    negative_count = (df[col] < 0).sum()
                    validation_results[filename]['issues'].append(f"{negative_count} negative values in {col}")
            
            print(f"✓ {filename}: {validation_results[filename]['rows']} rows, {validation_results[filename]['columns']} columns")
            if validation_results[filename]['date_range']:
                print(f"  Date range: {validation_results[filename]['date_range']}")
            if validation_results[filename]['issues']:
                print(f"  Issues: {', '.join(validation_results[filename]['issues'])}")
            
        except Exception as e:
            validation_results[filename] = {
                'exists': False,
                'error': str(e)
            }
            print(f"✗ {filename}: Error - {e}")
    
    print("\nValidation completed!")
    return validation_results

if __name__ == "__main__":
    # Generate sample data
    success = create_sample_data()
    
    if success:
        # Validate the generated data
        validate_generated_data()
        
        print("\n" + "=" * 70)
        print("READY TO LAUNCH DASHBOARD!")
        print("=" * 70)
        print("Run: streamlit run main_app.py")
        print("Or use: python run_dashboard.py")
    else:
        print("Data generation failed!")