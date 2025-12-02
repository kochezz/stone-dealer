import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

# --- Configuration Constants (CLEANED FOR CLOUD DEPLOYMENT) ---
# The app will look for this file in the same directory as app.py on GitHub.
DATA_FILENAME = "zambia_mining_app_data.csv" 

CHINGOLA_COORDS = (-12.5333, 27.8500)
CHINGOLA_NAME = "Chingola (Base of Operations)"

# --- Layout and Setup ---
st.set_page_config(
    page_title="Zambia Mining Site Assessment Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Function to Load Data (with Caching) ---
@st.cache_data
def load_data(file_path):
    """Loads the processed data and performs final type casting."""
    try:
        # Load the CSV file from the application's root directory
        df = pd.read_csv(file_path)
        
        # Ensure coordinates are numeric floats for mapping (crucial!)
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        
        # Drop any rows that failed conversion
        return df.dropna(subset=['Latitude', 'Longitude'])
    
    except FileNotFoundError:
        # Display a clear error message that instructs the user on fixing deployment
        st.error("Error: Data file 'zambia_mining_app_data.csv' not found in the GitHub repository root.")
        st.info("Please ensure the CSV file is committed and pushed to the same folder as app.py.")
        return pd.DataFrame()

# --- MAIN APPLICATION LOGIC ---

def run_app():
    """Contains the entire dashboard layout and functionality."""
    
    df = load_data(DATA_FILENAME)

    if df.empty:
        st.stop()

    # --- Title and Header ---
    st.title("🇿🇲 Mining Site Assessment Planner")
    st.markdown("### Base of Operations: **Chingola**")
    st.markdown("""
        Use the sidebar filters to select properties for viability assessment.
        Select a row in the table below to view travel logistics and details.
    """)

    # --- Sidebar Filters ---
    st.sidebar.header("🗺️ Filter Properties")

    # Filter 1: District/Town (Locale)
    selected_locales = st.sidebar.multiselect(
        "Filter by District/Town (Locale):",
        options=df['District/Town'].unique(),
        default=[]
    )

    # Filter 2: Primary Commodity 
    selected_commodities = st.sidebar.multiselect(
        "Filter by Primary Commodity:",
        options=df['Primary_Commodity'].unique(),
        default=[]
    )

    # Apply Filters
    df_filtered = df.copy()
    if selected_locales:
        df_filtered = df_filtered[df_filtered['District/Town'].isin(selected_locales)]
    if selected_commodities:
        df_filtered = df_filtered[df_filtered['Primary_Commodity'].isin(selected_commodities)]

    # --- Display Filtered Table ---
    st.subheader(f"Filtered Properties ({len(df_filtered)} Sites)")
    st.caption("Select a row below to populate the map and detail panels.")

    # Display table with selection enabled
    table_columns = [
        'Property_Name', 
        'District/Town', 
        'Primary_Commodity', 
        'Status', 
        'Distance_From_Chingola_km',
        'Travel_Time_From_Chingola_Hours'
    ]
    
    selected_rows = st.dataframe(
        df_filtered[table_columns].style.format({
            'Distance_From_Chingola_km': '{:.0f} km',
            'Travel_Time_From_Chingola_Hours': '{:.1f} hrs'
        }),
        use_container_width=True,
        hide_index=True,
        selection_mode="single",
        key="site_table"
    )

    # --- Conditional Detail Panels ---
    if selected_rows and selected_rows['selection']['rows']:
        # Get the index of the selected row
        selected_index = selected_rows['selection']['rows'][0]
        selected_site = df_filtered.loc[selected_index]
        
        col_map, col_logistics = st.columns([1, 1])

        with col_map:
            st.subheader(f"Map View: {selected_site['Property_Name']}")
            
            # Prepare data for map plotting (Chingola + Selected Site)
            map_data = pd.DataFrame({
                'lat': [CHINGOLA_COORDS[0], selected_site['Latitude']],
                'lon': [CHINGOLA_COORDS[1], selected_site['Longitude']],
                'name': [CHINGOLA_NAME, selected_site['Property_Name']],
                'color': ['#00FF00', '#FF0000'] # Green for base, Red for site
            })

            # Plotting the map using Plotly for better aesthetics and control 
            fig = px.scatter_mapbox(
                map_data,
                lat="lat",
                lon="lon",
                hover_name="name",
                color="color",
                color_discrete_map={
                    "#00FF00": "green",
                    "#FF0000": "red"
                },
                zoom=5,
                height=400,
                mapbox_style="carto-positron" # Neutral map style
            )
            
            # Center the map between the two points for better visualization
            center_lat = (CHINGOLA_COORDS[0] + selected_site['Latitude']) / 2
            center_lon = (CHINGOLA_COORDS[1] + selected_site['Longitude']) / 2
            fig.update_layout(
                mapbox_center={"lat": center_lat, "lon": center_lon}
            )
            
            st.plotly_chart(fig, use_container_width=True)

        with col_logistics:
            st.subheader("Travel Logistics & Status")
            
            distance_km = selected_site['Distance_From_Chingola_km']
            travel_hrs = selected_site['Travel_Time_From_Chingola_Hours']
            
            st.metric(
                label="Distance (Straight Line)", 
                value=f"{distance_km:.0f} km"
            )
            st.metric(
                label="Est. Travel Time (Road)",
                value=f"{travel_hrs:.1f} hours",
                help="Assumes an average road speed of 70 km/h."
            )
            st.markdown(f"**Current Status:** {selected_site['Status']}")
            st.markdown(f"**Reserves:** {selected_site['Reserves']}")


        # --- Detail View ---
        st.markdown("---")
        st.subheader(f"Mineralogy & Geology Details")
        
        col_mineral, col_geology = st.columns(2)
        
        with col_mineral:
            st.markdown("**Mineral Commodities:**")
            st.markdown(f"- **Primary:** {selected_site['Primary_Commodity']}")
            st.markdown(f"- **Secondary:** {selected_site['Commodity_2']}")
            st.markdown(f"- **Tertiary:** {selected_site['Commodity_3']}")

        with col_geology:
            st.markdown("**Geological Assessment:**")
            st.markdown(f"**Classification:** {selected_site['Geology_Classification']}")
            st.markdown(f"**Description:** {selected_site['Geology_Description']}")
            
    else:
        st.info("Select a site from the table above to visualize its location and planning details.")

# --- Run the application ---
run_app()