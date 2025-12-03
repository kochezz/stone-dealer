import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- Configuration Constants ---
DATA_FILENAME = "zambia_mining_app_data_final.csv"  # Updated to use cleaned dataset
CHINGOLA_COORDS = (-12.5333, 27.8500)
CHINGOLA_NAME = "Chingola Base"

# --- Page Configuration ---
st.set_page_config(
    page_title="Zambia Mining Site Planner",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="⛏️"
)

# --- Custom CSS for better styling ---
st.markdown("""
    <style>
    /* Remove any conflicting styles that might hide metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: inherit !important;
    }
    div[data-testid="stMetricLabel"] {
        color: inherit !important;
    }
    div[data-testid="stMetricDelta"] {
        color: inherit !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Load Data Function ---
@st.cache_data
def load_data(file_path):
    """Loads the cleaned mining data."""
    try:
        df = pd.read_csv(file_path)
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        return df.dropna(subset=['Latitude', 'Longitude'])
    except FileNotFoundError:
        st.error(f"❌ Data file '{file_path}' not found. Please ensure it's in the same directory as app.py.")
        return pd.DataFrame()

# --- Helper Functions ---
def create_multi_property_map(df_filtered, base_coords, base_name):
    """Creates a map showing all filtered properties plus the base location."""
    
    if df_filtered.empty:
        # Show only base if no properties match filter
        fig = px.scatter_mapbox(
            pd.DataFrame({
                'lat': [base_coords[0]],
                'lon': [base_coords[1]],
                'name': [base_name],
                'type': ['Base']
            }),
            lat='lat',
            lon='lon',
            hover_name='name',
            color='type',
            color_discrete_map={'Base': 'green'},
            zoom=5,
            height=600,
            mapbox_style="carto-positron"
        )
    else:
        # Combine base and filtered properties
        base_df = pd.DataFrame({
            'lat': [base_coords[0]],
            'lon': [base_coords[1]],
            'name': [base_name],
            'type': ['Base'],
            'commodity': [''],
            'province': [''],
            'distance': [0]
        })
        
        properties_df = pd.DataFrame({
            'lat': df_filtered['Latitude'].values,
            'lon': df_filtered['Longitude'].values,
            'name': df_filtered['Property_Name'].values,
            'type': ['Property'] * len(df_filtered),
            'commodity': df_filtered['Primary_Commodity'].values,
            'province': df_filtered['Province'].values,
            'distance': df_filtered['Distance_From_Chingola_km'].values
        })
        
        map_df = pd.concat([base_df, properties_df], ignore_index=True)
        
        # Create custom hover text
        map_df['hover_text'] = map_df.apply(
            lambda row: f"<b>{row['name']}</b><br>" + 
                       (f"Commodity: {row['commodity']}<br>Province: {row['province']}<br>Distance: {row['distance']:.0f} km" 
                        if row['type'] == 'Property' else "Base of Operations"),
            axis=1
        )
        
        # Create map with color coding
        fig = px.scatter_mapbox(
            map_df,
            lat='lat',
            lon='lon',
            hover_name='hover_text',
            color='type',
            color_discrete_map={'Base': '#00C853', 'Property': '#FF5722'},
            zoom=5.5,
            height=600,
            mapbox_style="carto-positron",
            size=[15 if t == 'Base' else 8 for t in map_df['type']]
        )
        
        fig.update_traces(
            hovertemplate='%{hovertext}<extra></extra>',
            marker=dict(opacity=0.8)
        )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255,255,255,0.8)"
        )
    )
    
    return fig

def get_commodity_color(commodity):
    """Returns a color for each commodity type."""
    color_map = {
        'Copper': '#FF5722',
        'Diamond': '#2196F3',
        'Gold': '#FFD700',
        'Iron': '#795548',
        'Zinc': '#9E9E9E',
        'Mangawese': '#4CAF50',
        'Beryl': '#00BCD4',
        'Emerald': '#4CAF50',
        'Nickel': '#607D8B'
    }
    return color_map.get(commodity, '#9C27B0')

# --- Main Application ---
def run_app():
    
    # Load data
    df = load_data(DATA_FILENAME)
    
    if df.empty:
        st.stop()
    
    # --- Header Section ---
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title("⛏️ Zambia Mining Site Planner")
        st.markdown("**Base:** Chingola, Copperbelt Province")
    
    with col2:
        st.metric("Total Properties", f"{len(df)}")
    
    with col3:
        st.metric("Provinces", f"{df['Province'].nunique()}")
    
    st.markdown("---")
    
    # --- Sidebar Filters ---
    with st.sidebar:
        st.header("🔍 Filter Properties")
        
        # Filter 1: Province
        st.markdown("### 📍 Location")
        selected_provinces = st.multiselect(
            "Province",
            options=sorted(df['Province'].unique()),
            default=[],
            help="Filter by Zambian province"
        )
        
        # Filter 2: District (dependent on province)
        if selected_provinces:
            available_districts = df[df['Province'].isin(selected_provinces)]['Clean_District'].unique()
        else:
            available_districts = df['Clean_District'].unique()
        
        selected_districts = st.multiselect(
            "District",
            options=sorted(available_districts),
            default=[],
            help="Filter by district within selected province(s)"
        )
        
        st.markdown("---")
        
        # Filter 3: Commodity
        st.markdown("### ⚒️ Commodity")
        selected_commodities = st.multiselect(
            "Primary Commodity",
            options=sorted(df['Primary_Commodity'].dropna().unique()),
            default=[],
            help="Filter by primary mineral commodity"
        )
        
        st.markdown("---")
        
        # Filter 4: Status
        st.markdown("### 📊 Status")
        selected_statuses = st.multiselect(
            "Property Status",
            options=sorted(df['Status'].unique()),
            default=[],
            help="Filter by property operational status"
        )
        
        st.markdown("---")
        
        # Filter 5: Distance Range
        st.markdown("### 📏 Distance from Base")
        max_distance = st.slider(
            "Maximum Distance (km)",
            min_value=0,
            max_value=int(df['Distance_From_Chingola_km'].max()),
            value=int(df['Distance_From_Chingola_km'].max()),
            step=50,
            help="Filter properties within this distance from Chingola"
        )
        
        # Clear filters button
        st.markdown("---")
        if st.button("🔄 Clear All Filters", use_container_width=True):
            st.rerun()
    
    # --- Apply Filters ---
    df_filtered = df.copy()
    
    if selected_provinces:
        df_filtered = df_filtered[df_filtered['Province'].isin(selected_provinces)]
    
    if selected_districts:
        df_filtered = df_filtered[df_filtered['Clean_District'].isin(selected_districts)]
    
    if selected_commodities:
        df_filtered = df_filtered[df_filtered['Primary_Commodity'].isin(selected_commodities)]
    
    if selected_statuses:
        df_filtered = df_filtered[df_filtered['Status'].isin(selected_statuses)]
    
    df_filtered = df_filtered[df_filtered['Distance_From_Chingola_km'] <= max_distance]
    
    # --- Summary Statistics Cards ---
    st.subheader(f"📊 Summary Statistics ({len(df_filtered)} Properties)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        delta_value = len(df_filtered) - len(df) if len(df_filtered) != len(df) else None
        st.metric(
            label="Filtered Sites",
            value=f"{len(df_filtered)}",
            delta=f"{delta_value} from total" if delta_value else None
        )
    
    with col2:
        if not df_filtered.empty:
            avg_distance = df_filtered['Distance_From_Chingola_km'].mean()
            st.metric("Avg Distance", f"{avg_distance:.0f} km")
        else:
            st.metric("Avg Distance", "N/A")
    
    with col3:
        if not df_filtered.empty:
            avg_time = df_filtered['Travel_Time_From_Chingola_Hours'].mean()
            st.metric("Avg Travel Time", f"{avg_time:.1f} hrs")
        else:
            st.metric("Avg Travel Time", "N/A")
    
    with col4:
        unique_commodities = df_filtered['Primary_Commodity'].nunique() if not df_filtered.empty else 0
        st.metric("Commodities", unique_commodities)
    
    with col5:
        unique_provinces = df_filtered['Province'].nunique() if not df_filtered.empty else 0
        st.metric("Provinces", unique_provinces)
    
    st.markdown("---")
    
    # --- Main Content Area: Map and Charts ---
    tab1, tab2, tab3 = st.tabs(["🗺️ Map View", "📈 Analytics", "📋 Data Table"])
    
    with tab1:
        st.subheader("Geographic Distribution")
        
        if df_filtered.empty:
            st.warning("⚠️ No properties match the current filters. Showing base location only.")
        else:
            st.info(f"📍 Displaying {len(df_filtered)} properties on the map")
        
        # Create and display the multi-property map
        map_fig = create_multi_property_map(df_filtered, CHINGOLA_COORDS, CHINGOLA_NAME)
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Quick stats below map
        if not df_filtered.empty:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                nearest = df_filtered.nsmallest(1, 'Distance_From_Chingola_km').iloc[0]
                st.markdown(f"**🎯 Nearest Property**")
                st.markdown(f"{nearest['Property_Name']}")
                st.markdown(f"📏 {nearest['Distance_From_Chingola_km']:.0f} km away")
            
            with col2:
                farthest = df_filtered.nlargest(1, 'Distance_From_Chingola_km').iloc[0]
                st.markdown(f"**🚀 Farthest Property**")
                st.markdown(f"{farthest['Property_Name']}")
                st.markdown(f"📏 {farthest['Distance_From_Chingola_km']:.0f} km away")
            
            with col3:
                top_commodity = df_filtered['Primary_Commodity'].value_counts().iloc[0]
                top_commodity_name = df_filtered['Primary_Commodity'].value_counts().index[0]
                st.markdown(f"**⚒️ Top Commodity**")
                st.markdown(f"{top_commodity_name}")
                st.markdown(f"📊 {top_commodity} properties")
    
    with tab2:
        st.subheader("Analytics Dashboard")
        
        if df_filtered.empty:
            st.warning("⚠️ No data to display. Adjust your filters.")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                # Commodity Distribution
                st.markdown("#### Commodity Distribution")
                commodity_counts = df_filtered['Primary_Commodity'].value_counts().head(10)
                fig_commodity = px.bar(
                    x=commodity_counts.values,
                    y=commodity_counts.index,
                    orientation='h',
                    labels={'x': 'Number of Properties', 'y': 'Commodity'},
                    color=commodity_counts.values,
                    color_continuous_scale='Viridis'
                )
                fig_commodity.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_commodity, use_container_width=True)
                
                # Status Distribution
                st.markdown("#### Property Status")
                status_counts = df_filtered['Status'].value_counts()
                fig_status = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    hole=0.4
                )
                fig_status.update_layout(
                    height=350,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_status, use_container_width=True)
            
            with col2:
                # Province Distribution
                st.markdown("#### Province Distribution")
                province_counts = df_filtered['Province'].value_counts()
                fig_province = px.bar(
                    x=province_counts.values,
                    y=province_counts.index,
                    orientation='h',
                    labels={'x': 'Number of Properties', 'y': 'Province'},
                    color=province_counts.values,
                    color_continuous_scale='Blues'
                )
                fig_province.update_layout(
                    showlegend=False,
                    height=400,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_province, use_container_width=True)
                
                # Distance Distribution
                st.markdown("#### Distance from Base Distribution")
                fig_distance = px.histogram(
                    df_filtered,
                    x='Distance_From_Chingola_km',
                    nbins=20,
                    labels={'Distance_From_Chingola_km': 'Distance (km)', 'count': 'Number of Properties'}
                )
                fig_distance.update_layout(
                    showlegend=False,
                    height=350,
                    margin=dict(l=0, r=0, t=30, b=0)
                )
                st.plotly_chart(fig_distance, use_container_width=True)
    
    with tab3:
        st.subheader("Property Data Table")
        
        if df_filtered.empty:
            st.warning("⚠️ No properties match the current filters.")
        else:
            st.markdown(f"*Displaying {len(df_filtered)} of {len(df)} total properties*")
            
            # Display table with selection
            display_columns = [
                'Property_Name',
                'Province',
                'Clean_District',
                'Primary_Commodity',
                'Status',
                'Distance_From_Chingola_km',
                'Travel_Time_From_Chingola_Hours'
            ]
            
            st.dataframe(
                df_filtered[display_columns].style.format({
                    'Distance_From_Chingola_km': '{:.0f} km',
                    'Travel_Time_From_Chingola_Hours': '{:.1f} hrs'
                }),
                use_container_width=True,
                hide_index=True,
                selection_mode="single-row",
                key="property_table",
                height=400
            )
            
            # Property Detail Section
            if "property_table" in st.session_state and st.session_state.property_table.get('selection', {}).get('rows'):
                selected_idx = st.session_state.property_table['selection']['rows'][0]
                selected_property = df_filtered.iloc[selected_idx]
                
                st.markdown("---")
                st.subheader(f"📍 {selected_property['Property_Name']}")
                
                # Property details in organized columns
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown("**Location**")
                    st.markdown(f"Province: {selected_property['Province']}")
                    st.markdown(f"District: {selected_property['Clean_District']}")
                    st.markdown(f"Coordinates: ({selected_property['Latitude']:.4f}, {selected_property['Longitude']:.4f})")
                
                with col2:
                    st.markdown("**Distance & Travel**")
                    st.markdown(f"Distance: {selected_property['Distance_From_Chingola_km']:.0f} km")
                    st.markdown(f"Travel Time: {selected_property['Travel_Time_From_Chingola_Hours']:.1f} hrs")
                    st.markdown(f"Status: {selected_property['Status']}")
                
                with col3:
                    st.markdown("**Commodities**")
                    st.markdown(f"Primary: {selected_property['Primary_Commodity']}")
                    if pd.notna(selected_property['Commodity_2']):
                        st.markdown(f"Secondary: {selected_property['Commodity_2']}")
                    if pd.notna(selected_property['Commodity_3']):
                        st.markdown(f"Tertiary: {selected_property['Commodity_3']}")
                
                with col4:
                    st.markdown("**Geology**")
                    st.markdown(f"Classification:")
                    st.markdown(f"*{selected_property['Geology_Classification']}*")
                
                # Detailed descriptions
                with st.expander("📖 View Detailed Information"):
                    st.markdown("**Location Description:**")
                    st.write(selected_property['District/Town'])
                    
                    st.markdown("**Reserve Information:**")
                    st.write(selected_property['Reserves'])
                    
                    st.markdown("**Geological Description:**")
                    st.write(selected_property['Geology_Description'])
                
                # Mini map for selected property
                st.markdown("#### Property Location Map")
                mini_map_data = pd.DataFrame({
                    'lat': [CHINGOLA_COORDS[0], selected_property['Latitude']],
                    'lon': [CHINGOLA_COORDS[1], selected_property['Longitude']],
                    'name': [CHINGOLA_NAME, selected_property['Property_Name']],
                    'type': ['Base', 'Property']
                })
                
                mini_fig = px.scatter_mapbox(
                    mini_map_data,
                    lat='lat',
                    lon='lon',
                    hover_name='name',
                    color='type',
                    color_discrete_map={'Base': '#00C853', 'Property': '#FF5722'},
                    zoom=6,
                    height=400,
                    mapbox_style="carto-positron"
                )
                
                # Add line connecting base to property
                mini_fig.add_trace(go.Scattermapbox(
                    lon=[CHINGOLA_COORDS[1], selected_property['Longitude']],
                    lat=[CHINGOLA_COORDS[0], selected_property['Latitude']],
                    mode='lines',
                    line=dict(width=2, color='blue'),
                    name='Route',
                    hoverinfo='skip'
                ))
                
                mini_fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(mini_fig, use_container_width=True)
    
    # --- Footer ---
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Zambia Mining Site Assessment Planner | Base: Chingola, Copperbelt Province</p>
            <p style='font-size: 0.9em;'>Data includes 239 mining properties • 27 commodities • 10 provinces</p>
        </div>
    """, unsafe_allow_html=True)

# --- Run Application ---
if __name__ == "__main__":
    run_app()
