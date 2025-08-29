import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import streamlit as st
from config import COLOR_SCHEMES, CHART_CONFIG, DATA_VALIDATION
import io
import base64

def format_number(value, format_type="currency"):
    """Enhanced number formatting for display"""
    if pd.isna(value) or value is None:
        return "N/A"
    
    try:
        value = float(value)
    except (ValueError, TypeError):
        return "N/A"
    
    if format_type == "currency":
        if abs(value) >= 1000000000:
            return f"{value/1000000000:.1f}T"
        elif abs(value) >= 1000000:
            return f"{value/1000000:.1f}M"
        elif abs(value) >= 1000:
            return f"{value/1000:.1f}K"
        else:
            return f"{value:.1f}"
    elif format_type == "percentage":
        return f"{value:.2f}%"
    elif format_type == "decimal":
        return f"{value:.3f}"
    elif format_type == "growth":
        sign = "+" if value > 0 else ""
        return f"{sign}{value:.2f}%"
    else:
        return f"{value:,.0f}"

def create_enhanced_line_chart(df, x_col, y_col, group_col=None, title="", color_scheme="primary"):
    """Create enhanced line chart with animations and styling"""
    fig = go.Figure()
    
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["primary"])
    
    if group_col and group_col in df.columns:
        groups = df[group_col].unique()
        for i, group in enumerate(groups):
            group_data = df[df[group_col] == group].sort_values(x_col)
            
            fig.add_trace(go.Scatter(
                x=group_data[x_col],
                y=group_data[y_col],
                mode='lines+markers',
                name=str(group),
                line=dict(
                    color=colors[i % len(colors)], 
                    width=3,
                    shape='spline'
                ),
                marker=dict(
                    size=8,
                    color=colors[i % len(colors)],
                    line=dict(width=2, color='white')
                ),
                hovertemplate=f'<b>{group}</b><br>%{{x}}: %{{y:,.2f}}<extra></extra>'
            ))
    else:
        df_sorted = df.sort_values(x_col)
        fig.add_trace(go.Scatter(
            x=df_sorted[x_col],
            y=df_sorted[y_col],
            mode='lines+markers',
            line=dict(
                color=colors[0], 
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=8,
                color=colors[0],
                line=dict(width=2, color='white')
            ),
            hovertemplate='%{x}: %{y:,.2f}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=CHART_CONFIG["title_font_size"], family=CHART_CONFIG["font_family"])
        ),
        xaxis_title=x_col.title().replace('_', ' '),
        yaxis_title=y_col.title().replace('_', ' '),
        height=CHART_CONFIG["height"],
        font_family=CHART_CONFIG["font_family"],
        template=CHART_CONFIG["template"],
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_enhanced_bar_chart(df, x_col, y_col, title="", orientation="vertical", color_scheme="primary"):
    """Create enhanced bar chart with styling"""
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["primary"])
    
    if orientation == "horizontal":
        fig = go.Figure(data=[go.Bar(
            y=df[x_col],
            x=df[y_col],
            orientation='h',
            marker=dict(
                color=colors[0],
                line=dict(color='white', width=1)
            ),
            hovertemplate='<b>%{y}</b><br>Value: %{x:,.2f}<extra></extra>'
        )])
        fig.update_layout(xaxis_title=y_col.title(), yaxis_title=x_col.title())
    else:
        fig = go.Figure(data=[go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker=dict(
                color=colors[0],
                line=dict(color='white', width=1)
            ),
            hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>'
        )])
        fig.update_layout(xaxis_title=x_col.title(), yaxis_title=y_col.title())
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=CHART_CONFIG["title_font_size"], family=CHART_CONFIG["font_family"])
        ),
        height=CHART_CONFIG["height"],
        font_family=CHART_CONFIG["font_family"],
        template=CHART_CONFIG["template"]
    )
    
    return fig

def create_pie_chart(df, labels_col, values_col, title="", color_scheme="sector_colors"):
    """Create enhanced pie chart"""
    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["sector_colors"])
    
    fig = go.Figure(data=[go.Pie(
        labels=df[labels_col],
        values=df[values_col],
        hole=0.4,
        marker=dict(
            colors=colors[:len(df)],
            line=dict(color='white', width=2)
        ),
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Value: %{value:,.2f}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=CHART_CONFIG["title_font_size"], family=CHART_CONFIG["font_family"])
        ),
        height=CHART_CONFIG["height"],
        font_family=CHART_CONFIG["font_family"],
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    
    return fig

def create_area_chart(df, x_col, y_cols, title="", stacked=True):
    """Create stacked or unstacked area chart"""
    fig = go.Figure()
    
    colors = COLOR_SCHEMES["sector_colors"]
    
    for i, col in enumerate(y_cols):
        if col in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x_col],
                y=df[col],
                mode='lines',
                stackgroup='one' if stacked else None,
                name=col,
                fill='tonexty' if stacked else 'tozeroy',
                line=dict(
                    color=colors[i % len(colors)],
                    width=2
                ),
                hovertemplate=f'<b>{col}</b><br>%{{x}}: %{{y:,.2f}}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=CHART_CONFIG["title_font_size"], family=CHART_CONFIG["font_family"])
        ),
        xaxis_title=x_col.title(),
        yaxis_title="Values" if not stacked else "Percentage (%)",
        height=CHART_CONFIG["height"],
        font_family=CHART_CONFIG["font_family"],
        template=CHART_CONFIG["template"],
        hovermode='x unified'
    )
    
    return fig

def create_correlation_heatmap(df, columns, title="Correlation Matrix"):
    """Create correlation heatmap"""
    # Calculate correlation matrix
    corr_matrix = df[columns].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.around(corr_matrix.values, decimals=2),
        texttemplate="%{text}",
        textfont={"size": 12},
        showscale=True,
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=CHART_CONFIG["title_font_size"], family=CHART_CONFIG["font_family"])
        ),
        height=CHART_CONFIG["height"],
        font_family=CHART_CONFIG["font_family"]
    )
    
    return fig

def calculate_growth_rate(df, value_col, period_col):
    """Calculate period-over-period growth rate"""
    df = df.sort_values(period_col).copy()
    df['growth_rate'] = df[value_col].pct_change() * 100
    df['growth_rate_abs'] = df[value_col].diff()
    return df

def calculate_cagr(start_value, end_value, years):
    """Calculate compound annual growth rate"""
    if start_value <= 0 or end_value <= 0 or years <= 0:
        return 0
    return (((end_value / start_value) ** (1 / years)) - 1) * 100

def calculate_statistics(series):
    """Calculate comprehensive statistics for a series"""
    if series.empty or series.isna().all():
        return {
            'count': 0,
            'mean': 0,
            'median': 0,
            'std': 0,
            'min': 0,
            'max': 0,
            'q25': 0,
            'q75': 0,
            'latest': 0,
            'earliest': 0,
            'total_change': 0,
            'avg_annual_change': 0
        }
    
    stats = {
        'count': len(series.dropna()),
        'mean': series.mean(),
        'median': series.median(),
        'std': series.std(),
        'min': series.min(),
        'max': series.max(),
        'q25': series.quantile(0.25),
        'q75': series.quantile(0.75),
        'latest': series.iloc[-1] if not series.empty else 0,
        'earliest': series.iloc[0] if not series.empty else 0
    }
    
    # Calculate changes
    stats['total_change'] = stats['latest'] - stats['earliest']
    stats['avg_annual_change'] = stats['total_change'] / (stats['count'] - 1) if stats['count'] > 1 else 0
    
    return stats

def filter_data_by_year(df, year_col, start_year, end_year):
    """Filter dataframe by year range with validation"""
    if year_col not in df.columns:
        return df
    
    # Convert to numeric if needed
    df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
    
    # Filter
    mask = (df[year_col] >= start_year) & (df[year_col] <= end_year)
    return df[mask]

def validate_data_quality(df, data_type):
    """Enhanced data quality validation"""
    issues = []
    warnings = []
    
    if df.empty:
        issues.append("Dataset is empty")
        return {'issues': issues, 'warnings': warnings, 'status': 'error'}
    
    # Check required columns
    required_cols = DATA_VALIDATION['required_columns'].get(data_type, [])
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        issues.append(f"Missing required columns: {missing_cols}")
    
    # Check for missing values
    missing_values = df.isnull().sum()
    critical_missing = missing_values[missing_values > len(df) * 0.5]
    if not critical_missing.empty:
        issues.append(f"High missing values (>50%): {critical_missing.to_dict()}")
    
    moderate_missing = missing_values[(missing_values > 0) & (missing_values <= len(df) * 0.5)]
    if not moderate_missing.empty:
        warnings.append(f"Moderate missing values: {moderate_missing.to_dict()}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        warnings.append(f"Duplicate rows found: {duplicates}")
    
    # Check data types and ranges
    for col, expected_type in DATA_VALIDATION.get('data_types', {}).items():
        if col in df.columns:
            if expected_type == 'int':
                non_int = df[col].apply(lambda x: not str(x).replace('-', '').isdigit() if pd.notna(x) else False).sum()
                if non_int > 0:
                    warnings.append(f"Non-integer values in {col}: {non_int} rows")
            elif expected_type == 'float':
                non_numeric = pd.to_numeric(df[col], errors='coerce').isna().sum() - df[col].isna().sum()
                if non_numeric > 0:
                    warnings.append(f"Non-numeric values in {col}: {non_numeric} rows")
    
    # Determine overall status
    if issues:
        status = 'error'
    elif warnings:
        status = 'warning'
    else:
        status = 'good'
    
    return {'issues': issues, 'warnings': warnings, 'status': status}

def create_data_summary_table(df):
    """Create data summary table"""
    summary_data = []
    
    for col in df.select_dtypes(include=[np.number]).columns:
        stats = calculate_statistics(df[col])
        summary_data.append({
            'Column': col,
            'Count': stats['count'],
            'Mean': f"{stats['mean']:.2f}",
            'Std': f"{stats['std']:.2f}",
            'Min': f"{stats['min']:.2f}",
            'Max': f"{stats['max']:.2f}",
            'Latest': f"{stats['latest']:.2f}"
        })
    
    return pd.DataFrame(summary_data)

def export_data_to_excel(dataframes_dict, filename="aceh_dashboard_data.xlsx"):
    """Export multiple dataframes to Excel file"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for sheet_name, df in dataframes_dict.items():
            # Clean sheet name (Excel has restrictions)
            clean_name = sheet_name.replace('/', '_').replace('\\', '_')[:31]
            df.to_excel(writer, sheet_name=clean_name, index=False)
    
    output.seek(0)
    return output

def create_download_link(data, filename, file_format="csv"):
    """Create download link for data"""
    if file_format.lower() == "csv":
        csv = data.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV</a>'
    elif file_format.lower() == "excel":
        # data should be BytesIO object for Excel
        b64 = base64.b64encode(data.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}.xlsx">Download Excel</a>'
    
    return href

def detect_outliers(series, method='iqr', threshold=1.5):
    """Enhanced outlier detection"""
    if series.empty or series.isna().all():
        return []
    
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        outliers = series[(series < lower_bound) | (series > upper_bound)]
    elif method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        outliers = series[z_scores > threshold]
    else:
        return []
    
    return outliers.index.tolist()

def create_trend_indicators(df, value_col, period_col):
    """Create trend indicators and analysis"""
    df_sorted = df.sort_values(period_col)
    
    # Calculate moving averages
    df_sorted['ma_3'] = df_sorted[value_col].rolling(window=3, center=True).mean()
    df_sorted['ma_5'] = df_sorted[value_col].rolling(window=5, center=True).mean()
    
    # Calculate trend direction
    recent_periods = 3
    if len(df_sorted) >= recent_periods:
        recent_data = df_sorted.tail(recent_periods)
        trend_slope = np.polyfit(range(recent_periods), recent_data[value_col], 1)[0]
        
        if trend_slope > 0:
            trend_direction = "Increasing"
        elif trend_slope < 0:
            trend_direction = "Decreasing"
        else:
            trend_direction = "Stable"
    else:
        trend_direction = "Insufficient data"
    
    return df_sorted, trend_direction

def format_large_numbers(value):
    """Format large numbers for better readability"""
    if pd.isna(value):
        return "N/A"
    
    abs_value = abs(value)
    if abs_value >= 1e12:
        return f"{value/1e12:.1f}T"
    elif abs_value >= 1e9:
        return f"{value/1e9:.1f}B"
    elif abs_value >= 1e6:
        return f"{value/1e6:.1f}M"
    elif abs_value >= 1e3:
        return f"{value/1e3:.1f}K"
    else:
        return f"{value:.0f}"

def create_comparison_table(df, group_col, value_cols, agg_func='mean'):
    """Create comparison table across groups"""
    if agg_func == 'mean':
        comparison = df.groupby(group_col)[value_cols].mean()
    elif agg_func == 'sum':
        comparison = df.groupby(group_col)[value_cols].sum()
    elif agg_func == 'latest':
        comparison = df.groupby(group_col)[value_cols].last()
    else:
        comparison = df.groupby(group_col)[value_cols].agg(agg_func)
    
    return comparison.round(2)