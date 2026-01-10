import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import hashlib
import os

# Import Phase 1 modules
from density_analysis import (
    calculate_density_score,
    rank_sites_by_density,
    categorize_by_density,
    create_density_clusters,
    get_density_statistics
)
from geological_analysis import (
    identify_mineral_belts,
    create_trend_lines,
    analyze_geology_patterns,
    calculate_vein_statistics,
    get_geological_summary,
    identify_geological_provinces
)
from accessibility import (
    calculate_accessibility_score,
    rank_by_accessibility,
    get_accessibility_statistics,
    calculate_infrastructure_index,
    identify_infrastructure_gaps,
    calculate_regional_accessibility
)

# --- Configuration Constants ---
DATA_FILENAME = "zambia_mining_data_final_cleaned.csv"
CHINGOLA_COORDS = (-12.5333, 27.8500)
CHINGOLA_NAME = "Chingola Base"

# --- Password Configuration ---
APP_PASSWORD = os.environ.get("APP_PASSWORD", "mulimakwenda")

# --- Authentication Functions ---
def check_password():
    """Returns `True` if the user has entered the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256(APP_PASSWORD.encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1>⛏️ Zambia Mining Intelligence Platform</h1>
                <p style='color: #666; font-size: 1.2em;'>Business Enterprise Data Analytics</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔒 Authentication Required")
            st.text_input(
                "Enter Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter your password"
            )
            st.info("💡 Contact administrator for access credentials")
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("""
            <div style='text-align: center; padding: 50px;'>
                <h1>⛏️ Zambia Mining Intelligence Platform</h1>
                <p style='color: #666; font-size: 1.2em;'>Vilagio Trading Limited</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🔒 Authentication Required")
            st.text_input(
                "Enter Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter your password"
            )
            st.error("❌ Incorrect password. Please try again.")
            st.info("💡 Contact administrator for access credentials")
        return False
    
    else:
        return True

# --- Page Configuration ---
st.set_page_config(
    page_title="Zambia Mining Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⛏️"
)

# --- Check Authentication ---
if not check_password():
    st.stop()

# --- Custom CSS ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E40AF;
        text-align: center;
        padding: 20px 0;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1E40AF;
    }
    .insight-box {
        background-color: #EFF6FF;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load and Process Data ---
@st.cache_data
def load_data():
    """Load and process the mining dataset"""
    try:
        df = pd.read_csv(DATA_FILENAME)
        
        # Calculate all scores
        df = calculate_density_score(df)
        df = categorize_by_density(df)
        df = calculate_accessibility_score(df)
        df = calculate_infrastructure_index(df)
        
        return df
    except FileNotFoundError:
        st.error(f"❌ Data file '{DATA_FILENAME}' not found. Please ensure the file is in the same directory as the app.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

# Load data
df = load_data()

# --- Sidebar Filters ---
st.sidebar.markdown("## 🎯 Filters & Controls")

# Tab selector
view_mode = st.sidebar.radio(
    "View Mode",
    ["📊 Overview", "🗺️ Site Explorer", "💎 Geological Analysis", "🚗 Accessibility"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Commodity & Location")

# Commodity filter
all_commodities = ['All'] + sorted(df['Primary_Commodity'].unique().tolist())
selected_commodity = st.sidebar.selectbox(
    "Primary Commodity",
    all_commodities,
    help="Filter sites by commodity type"
)

# Province filter
selected_provinces = st.sidebar.multiselect(
    "Province",
    options=sorted(df['Province'].unique()),
    default=[],
    help="Filter by province (leave empty for all)"
)

# District filter
if selected_provinces:
    available_districts = df[df['Province'].isin(selected_provinces)]['Clean_District'].unique()
else:
    available_districts = df['Clean_District'].unique()

selected_districts = st.sidebar.multiselect(
    "District",
    options=sorted([d for d in available_districts if pd.notna(d)]),
    default=[],
    help="Filter by district within selected province(s)"
)

# Status filter
selected_statuses = st.sidebar.multiselect(
    "Status",
    options=sorted(df['Status'].unique()),
    default=[],
    help="Filter by site status"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎚️ Density Controls")

# Density mode
density_mode = st.sidebar.radio(
    "Display Mode",
    ["All Sites", "Top Sites", "Bottom Sites"],
    help="Filter sites by density ranking"
)

# Number of sites slider (only if not "All Sites")
if density_mode != "All Sites":
    n_sites_density = st.sidebar.slider(
        "Number of Sites",
        min_value=10,
        max_value=min(100, len(df)),
        value=20,
        step=10,
        help="Select how many sites to display"
    )
else:
    n_sites_density = len(df)

# Show clusters
show_clusters = st.sidebar.checkbox("Show Density Clusters", value=False)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚗 Accessibility Controls")

# Accessibility filter
min_accessibility = st.sidebar.slider(
    "Min Accessibility Score",
    min_value=0,
    max_value=100,
    value=0,
    help="Filter sites by minimum accessibility (0=poor, 100=excellent)"
)

# --- Apply Filters ---
df_filtered = df.copy()

# Apply commodity filter
if selected_commodity != 'All':
    df_filtered = df_filtered[df_filtered['Primary_Commodity'] == selected_commodity]

# Apply province filter
if selected_provinces:
    df_filtered = df_filtered[df_filtered['Province'].isin(selected_provinces)]

# Apply district filter
if selected_districts:
    df_filtered = df_filtered[df_filtered['Clean_District'].isin(selected_districts)]

# Apply status filter
if selected_statuses:
    df_filtered = df_filtered[df_filtered['Status'].isin(selected_statuses)]

# Apply accessibility filter
df_filtered = df_filtered[df_filtered['Accessibility_Score'] >= min_accessibility]

# Apply density mode filter
if density_mode == "Top Sites":
    df_filtered = rank_sites_by_density(df_filtered, selected_commodity, n_sites_density, mode='top')
elif density_mode == "Bottom Sites":
    df_filtered = rank_sites_by_density(df_filtered, selected_commodity, n_sites_density, mode='bottom')

# --- Main Content ---

if view_mode == "📊 Overview":
    # OVERVIEW TAB
    st.markdown("<h1 class='main-header'>⛏️ Portfolio Overview</h1>", unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sites", len(df_filtered))
    
    with col2:
        active_sites = len(df_filtered[df_filtered['Status'] == 'Active'])
        active_pct = (active_sites / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.metric("Active Sites", f"{active_sites} ({active_pct:.0f}%)")
    
    with col3:
        avg_density = df_filtered['Density_Score'].mean()
        st.metric("Avg Density Score", f"{avg_density:.1f}/100")
    
    with col4:
        avg_access = df_filtered['Accessibility_Score'].mean()
        st.metric("Avg Access Score", f"{avg_access:.1f}/100")
    
    st.markdown("---")
    
    # Charts row
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Commodity Distribution")
        commodity_counts = df_filtered['Primary_Commodity'].value_counts().head(10)
        fig_commodity = px.bar(
            x=commodity_counts.index,
            y=commodity_counts.values,
            labels={'x': 'Commodity', 'y': 'Number of Sites'},
            color=commodity_counts.values,
            color_continuous_scale='Blues'
        )
        fig_commodity.update_layout(showlegend=False, height=350)
        st.plotly_chart(fig_commodity, use_container_width=True)
    
    with col2:
        st.markdown("#### 🗺️ Geographic Distribution")
        province_counts = df_filtered['Province'].value_counts()
        fig_province = px.pie(
            values=province_counts.values,
            names=province_counts.index,
            hole=0.4
        )
        fig_province.update_layout(height=350)
        st.plotly_chart(fig_province, use_container_width=True)
    
    # Top districts
    st.markdown("#### 🏆 Top Districts by Site Count")
    top_districts = df_filtered['Clean_District'].value_counts().head(10)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_districts = px.bar(
            x=top_districts.values,
            y=top_districts.index,
            orientation='h',
            labels={'x': 'Number of Sites', 'y': 'District'},
            color=top_districts.values,
            color_continuous_scale='Viridis'
        )
        fig_districts.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_districts, use_container_width=True)
    
    with col2:
        st.markdown("##### District Statistics")
        for i, (district, count) in enumerate(top_districts.head(5).items(), 1):
            st.markdown(f"**{i}. {district}**: {count} sites")
    
    # Density vs Accessibility scatter
    st.markdown("#### 💎 Resource Quality vs Accessibility")
    
    fig_scatter = px.scatter(
        df_filtered,
        x='Accessibility_Score',
        y='Density_Score',
        color='Primary_Commodity',
        size='Density_Score',
        hover_name='Property_Name',
        hover_data=['Province', 'Clean_District', 'Status'],
        labels={
            'Accessibility_Score': 'Accessibility Score',
            'Density_Score': 'Density Score'
        }
    )
    
    # Add quadrant lines
    fig_scatter.add_hline(y=60, line_dash="dash", line_color="gray", opacity=0.5)
    fig_scatter.add_vline(x=60, line_dash="dash", line_color="gray", opacity=0.5)
    
    # Add quadrant labels
    fig_scatter.add_annotation(x=80, y=80, text="Priority Targets", showarrow=False, font=dict(size=12, color="green"))
    fig_scatter.add_annotation(x=30, y=80, text="Infrastructure Needed", showarrow=False, font=dict(size=12, color="orange"))
    fig_scatter.add_annotation(x=80, y=30, text="Quick Wins", showarrow=False, font=dict(size=12, color="blue"))
    fig_scatter.add_annotation(x=30, y=30, text="Low Priority", showarrow=False, font=dict(size=12, color="gray"))
    
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

elif view_mode == "🗺️ Site Explorer":
    # SITE EXPLORER TAB
    st.markdown("<h1 class='main-header'>🗺️ Site Explorer</h1>", unsafe_allow_html=True)
    
    # Map controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        map_color = st.selectbox(
            "Color By",
            ["Density Category", "Access Category", "Primary Commodity", "Status", "Province"],
            help="Choose how to color the markers"
        )
    
    with col2:
        map_size = st.selectbox(
            "Size By",
            ["Density Score", "Accessibility Score", "Uniform"],
            help="Choose what determines marker size"
        )
    
    with col3:
        if show_clusters and len(df_filtered) > 5:
            df_with_clusters, cluster_stats = create_density_clusters(
                df_filtered, 
                commodity=selected_commodity if selected_commodity != 'All' else None
            )
            st.info(f"📍 {len(cluster_stats)} clusters identified")
        else:
            df_with_clusters = df_filtered.copy()
    
    # Prepare map data
    df_map = df_with_clusters.copy()
    
    # Set color column
    color_map_dict = None
    if map_color == "Density Category":
        color_col = "Density_Category"
        color_map_dict = {
            'Very Low': '#3B82F6',
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444',
            'Very High': '#7C3AED'
        }
    elif map_color == "Access Category":
        color_col = "Access_Category"
        color_map_dict = {
            'Poor': '#EF4444',
            'Fair': '#F59E0B',
            'Good': '#3B82F6',
            'Excellent': '#10B981'
        }
    elif map_color == "Primary Commodity":
        color_col = "Primary_Commodity"
    elif map_color == "Status":
        color_col = "Status"
    else:
        color_col = "Province"
    
    # Set size column
    if map_size == "Density Score":
        size_col = "Density_Score"
    elif map_size == "Accessibility Score":
        size_col = "Accessibility_Score"
    else:
        size_col = None
    
    # Create map
    fig_map = px.scatter_mapbox(
        df_map,
        lat='Latitude',
        lon='Longitude',
        color=color_col,
        color_discrete_map=color_map_dict,
        size=size_col if size_col else None,
        size_max=20,
        hover_name='Property_Name',
        hover_data={
            'Province': True,
            'Clean_District': True,
            'Primary_Commodity': True,
            'Density_Score': ':.0f',
            'Accessibility_Score': ':.0f',
            'Status': True,
            'Latitude': ':.4f',
            'Longitude': ':.4f',
            color_col: False,
            size_col: False if size_col else None
        },
        zoom=5.5,
        center={"lat": -14.5, "lon": 28.5},
        height=700
    )
    
    fig_map.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(100, 100, 100, 0.8)",
            borderwidth=2,
            font=dict(size=13, color='black'),
            title=dict(text=f"<b>{map_color}</b>", font=dict(size=14, color='black')),
            itemsizing='constant'
        )
    )
    
    # Add Chingola base marker
    fig_map.add_trace(
        go.Scattermapbox(
            lat=[CHINGOLA_COORDS[0]],
            lon=[CHINGOLA_COORDS[1]],
            mode='markers',
            marker=dict(size=15, color='red', symbol='star'),
            name='Chingola Base',
            hovertext=CHINGOLA_NAME
        )
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Site statistics
    st.markdown("#### 📊 Filtered Sites Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sites Displayed", len(df_map))
    
    with col2:
        high_density = len(df_map[df_map['Density_Score'] >= 80])
        st.metric("High Density", high_density)
    
    with col3:
        high_access = len(df_map[df_map['Accessibility_Score'] >= 80])
        st.metric("Excellent Access", high_access)
    
    with col4:
        priority_sites = len(df_map[(df_map['Density_Score'] >= 60) & (df_map['Accessibility_Score'] >= 60)])
        st.metric("Priority Sites", priority_sites)

elif view_mode == "💎 Geological Analysis":
    # GEOLOGICAL ANALYSIS TAB
    st.markdown("<h1 class='main-header'>💎 Geological Intelligence</h1>", unsafe_allow_html=True)
    
    # Geological controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        analysis_commodity = st.selectbox(
            "Analyze Commodity",
            all_commodities,
            help="Select commodity for vein/belt analysis"
        )
    
    with col2:
        show_trend_lines = st.checkbox("Show Trend Lines", value=True)
    
    # Dual map view
    tab1, tab2 = st.tabs(["📍 Site Distribution", "🗺️ Geological Patterns"])
    
    with tab1:
        # Standard site map - LARGER for better visibility
        df_geo = df_filtered.copy() if analysis_commodity == 'All' else df_filtered[df_filtered['Primary_Commodity'] == analysis_commodity]
        
        fig_geo1 = px.scatter_mapbox(
            df_geo,
            lat='Latitude',
            lon='Longitude',
            color='Primary_Commodity',
            size='Density_Score',
            size_max=15,
            hover_name='Property_Name',
            hover_data=['Province', 'Clean_District', 'Geology_Classification'],
            zoom=5.5,
            center={"lat": -14.5, "lon": 28.5},
            height=750  # Increased from 600 to 750
        )
        
        fig_geo1.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.02,
                bgcolor="rgba(255, 255, 255, 0.95)",
                bordercolor="rgba(100, 100, 100, 0.8)",
                borderwidth=2,
                font=dict(size=13, color='black'),
                title=dict(text="<b>Commodity</b>", font=dict(size=14, color='black')),
                itemsizing='constant'
            )
        )
        
        st.plotly_chart(fig_geo1, use_container_width=True)
    
    with tab2:
        # Geological patterns map - SIMPLIFIED LEGEND for better visibility
        df_geo = df_filtered.copy() if analysis_commodity == 'All' else df_filtered[df_filtered['Primary_Commodity'] == analysis_commodity]
        
        # Group similar geology types to reduce legend items
        def simplify_geology(geo_class):
            if pd.isna(geo_class):
                return 'Unknown'
            geo_lower = str(geo_class).lower()
            if 'stratiform' in geo_lower:
                return 'Stratiform Deposits'
            elif 'vein' in geo_lower or 'shear' in geo_lower:
                return 'Vein/Shear Deposits'
            elif 'supergene' in geo_lower:
                return 'Supergene Enriched'
            elif 'sediment' in geo_lower:
                return 'Sedimentary Deposits'
            elif 'breccia' in geo_lower:
                return 'Breccia-Hosted'
            elif 'hydrothermal' in geo_lower:
                return 'Hydrothermal'
            elif 'volcanogenic' in geo_lower:
                return 'Volcanogenic'
            else:
                return 'Other Deposits'
        
        df_geo['Geology_Simplified'] = df_geo['Geology_Classification'].apply(simplify_geology)
        
        fig_geo2 = px.scatter_mapbox(
            df_geo,
            lat='Latitude',
            lon='Longitude',
            color='Geology_Simplified',
            hover_name='Property_Name',
            hover_data={
                'Primary_Commodity': True, 
                'Province': True,
                'Geology_Classification': True,  # Show full detail on hover
                'Geology_Simplified': False
            },
            zoom=5.5,
            center={"lat": -14.5, "lon": 28.5},
            height=750,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        # Add trend lines if requested
        if show_trend_lines:
            commodities_to_analyze = [analysis_commodity] if analysis_commodity != 'All' else ['Copper', 'Gold', 'Iron']
            
            colors = {'Copper': 'red', 'Gold': 'gold', 'Iron': 'orange', 'Diamond': 'cyan'}
            
            for commodity in commodities_to_analyze:
                if commodity in df['Primary_Commodity'].values:
                    trend = create_trend_lines(df, commodity)
                    
                    if trend:
                        fig_geo2.add_trace(
                            go.Scattermapbox(
                                lat=[trend['start_lat'], trend['end_lat']],
                                lon=[trend['start_lon'], trend['end_lon']],
                                mode='lines',
                                line=dict(width=4, color=colors.get(commodity, 'red')),
                                name=f'{commodity} Belt Trend',
                                hoverinfo='name',
                                showlegend=True
                            )
                        )
        
        fig_geo2.update_layout(
            mapbox_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.02,
                bgcolor="rgba(255, 255, 255, 0.95)",  # More opaque background
                bordercolor="rgba(100, 100, 100, 0.8)",
                borderwidth=2,
                font=dict(size=13, color='black'),  # Larger, black text
                title=dict(text="<b>Geology & Trends</b>", font=dict(size=14, color='black')),
                itemsizing='constant'
            )
        )
        
        st.plotly_chart(fig_geo2, use_container_width=True)
    
    # Geological insights - COMPACT METRICS ONLY (always visible)
    if analysis_commodity != 'All':
        belt_info = identify_mineral_belts(df, analysis_commodity)
        
        if belt_info:
            st.markdown("#### 🔬 Belt Metrics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Sites in Belt", belt_info['site_count'])
            
            with col2:
                st.metric("Belt Bearing", f"{belt_info['bearing']:.0f}°")
            
            with col3:
                st.metric("Belt Length", f"{belt_info['length_km']:.0f} km")
            
            with col4:
                st.metric("Linearity", f"{belt_info['linearity']:.0%}")
    
    # Detailed analysis in expanders (collapsed by default)
    with st.expander("📊 Detailed Belt Analysis", expanded=False):
        if analysis_commodity != 'All':
            belt_info = identify_mineral_belts(df, analysis_commodity)
            
            if belt_info:
                st.markdown(f"""
                **{analysis_commodity} Belt Analysis:**
                
                The {analysis_commodity} deposits show a **{('strong' if belt_info['linearity'] > 0.7 else 'moderate')} linear pattern**, 
                trending at **{belt_info['bearing']:.0f}° (bearing)** over approximately **{belt_info['length_km']:.0f} km**. 
                
                This pattern suggests {('a well-defined mineral belt' if belt_info['linearity'] > 0.7 else 'scattered deposits with some alignment')}.
                
                **Key Characteristics:**
                - **Linearity Index**: {belt_info['linearity']:.2f} (0=scattered, 1=perfectly linear)
                - **Center Point**: {belt_info['center_lat']:.4f}°, {belt_info['center_lon']:.4f}°
                - **Variance Explained**: {belt_info['variance_explained']:.1f}% of spatial variation
                """)
        else:
            st.info("Select a specific commodity to view detailed belt analysis")
    
    # Geology patterns table in expander
    with st.expander("🧪 Geological Formation Details", expanded=False):
        geology_patterns = analyze_geology_patterns(df_filtered)
        
        if len(geology_patterns) > 0:
            st.dataframe(
                geology_patterns.head(10),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No geological formation patterns to display for current filters")

elif view_mode == "🚗 Accessibility":
    # ACCESSIBILITY TAB
    st.markdown("<h1 class='main-header'>🚗 Accessibility Analysis</h1>", unsafe_allow_html=True)
    
    # Accessibility metrics
    col1, col2, col3, col4 = st.columns(4)
    
    access_stats = get_accessibility_statistics(df_filtered)
    
    with col1:
        st.metric("Avg Access Score", f"{access_stats['avg_accessibility']:.1f}/100")
    
    with col2:
        st.metric("Excellent Access", access_stats['excellent_count'])
    
    with col3:
        st.metric("Good Access", access_stats['good_count'])
    
    with col4:
        avg_distance = access_stats.get('avg_distance_chingola')
        if avg_distance:
            st.metric("Avg Distance (Chingola)", f"{avg_distance:.0f} km")
    
    # Accessibility map
    st.markdown("#### 🗺️ Accessibility Map")
    
    fig_access = px.scatter_mapbox(
        df_filtered,
        lat='Latitude',
        lon='Longitude',
        color='Access_Category',
        color_discrete_map={
            'Excellent': '#10B981',
            'Good': '#3B82F6',
            'Fair': '#F59E0B',
            'Poor': '#EF4444'
        },
        size='Accessibility_Score',
        size_max=20,
        hover_name='Property_Name',
        hover_data={
            'Accessibility_Score': ':.0f',
            'Distance_From_Chingola_km': ':.1f',
            'Province': True,
            'Clean_District': True,
            'Access_Category': False
        },
        zoom=5.5,
        center={"lat": -14.5, "lon": 28.5},
        height=700  # Increased from 600 for consistency
    )
    
    fig_access.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255, 255, 255, 0.95)",
            bordercolor="rgba(100, 100, 100, 0.8)",
            borderwidth=2,
            font=dict(size=13, color='black'),
            title=dict(text="<b>Accessibility</b>", font=dict(size=14, color='black')),
            itemsizing='constant'
        )
    )
    
    # Add Chingola
    fig_access.add_trace(
        go.Scattermapbox(
            lat=[CHINGOLA_COORDS[0]],
            lon=[CHINGOLA_COORDS[1]],
            mode='markers',
            marker=dict(size=15, color='red', symbol='star'),
            name='Chingola Base',
            hovertext=CHINGOLA_NAME
        )
    )
    
    st.plotly_chart(fig_access, use_container_width=True)
    
    # Regional accessibility
    st.markdown("#### 📊 Regional Accessibility Statistics")
    
    province_stats, district_stats = calculate_regional_accessibility(df_filtered)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Top Provinces by Accessibility")
        st.dataframe(
            province_stats[['Province', 'Avg_Access_Score', 'Site_Count']].head(10),
            use_container_width=True,
            hide_index=True
        )
    
    with col2:
        st.markdown("##### Top Districts by Accessibility")
        st.dataframe(
            district_stats[['Clean_District', 'Province', 'Avg_Access_Score', 'Site_Count']].head(10),
            use_container_width=True,
            hide_index=True
        )
    
    # Infrastructure gaps
    st.markdown("#### ⚠️ Infrastructure Development Opportunities")
    st.markdown("High-value sites with poor accessibility that would benefit from infrastructure development")
    
    gap_sites = identify_infrastructure_gaps(df_filtered, threshold=60)
    
    if len(gap_sites) > 0:
        st.dataframe(
            gap_sites.head(10),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No significant infrastructure gaps identified in the filtered dataset.")

# --- Footer ---
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Zambia Mining Intelligence Platform | BEDA</p>
        <p>Phase 1: Density Analysis • Geological Mapping • Accessibility Assessment</p>
    </div>
""", unsafe_allow_html=True)
