import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- CONFIGURATION CONSTANTS ---
ROOT_FOLDER = r"C:\Users\willi\OneDrive\Documents\COVEX\PYTHON"
DATA_FILENAME = os.path.join(ROOT_FOLDER, "zambia_mining_app_data.csv")
CHINGOLA_COORDS = (-12.5333, 27.8500)
CHINGOLA_NAME = "Chingola (Base of Operations)"

# --- AUTHENTICATION CONFIG ---
# 1. DEFINE YOUR CREDENTIALS HERE
# NOTE: The password 'adminpass' is used below.
# You MUST replace the hash with a hash generated for your chosen password.
# To generate a new hash, run this command in your terminal:
# python -c "import streamlit_authenticator as stauth; print(stauth.Hasher(['YOUR_SECURE_PASSWORD']).generate())"
# Then copy the output string (the list of hashes) into the HASHED_PASSWORDS list below.
HASHED_PASSWORDS = ['HASHED_PASSWORD_FOR_YOUR_ADMIN_USER'] # Placeholder - REPLACE THIS!
USERNAMES = ['willi']
NAMES = ['Mining Engineer']

# 2. Setup the Authenticator
authenticator = stauth.Authenticate(
    names=NAMES,
    usernames=USERNAMES,
    passwords=HASHED_PASSWORDS,
    cookie_name='mine_planner_cookie',
    key='random_signature_key',
    cookie_expiry_days=30
)

# --- Function to Load Data (with Caching) ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        return df.dropna(subset=['Latitude', 'Longitude'])
    except FileNotFoundError:
        st.error("Error: Data file not found. Ensure 'zambia_mining_app_data.csv' is in the root folder.")
        return pd.DataFrame()

# --- MAIN APPLICATION LOGIC ---

def run_app():
    """Contains the entire dashboard layout and functionality."""
    
    df = load_data(DATA_FILENAME)

    if df.empty:
        return

    # --- Title and Header ---
    st.title("🇿🇲 Mining Site Assessment Planner")
    st.markdown("### Base of Operations: **Chingola**")
    st.markdown("""
        Use the sidebar filters to select properties for viability assessment.
        Select a row in the table below to view travel logistics and details.
    """)

    # --- Sidebar Filters ---
    st.sidebar.header("🗺️ Filter Properties")

    selected_locales = st.sidebar.multiselect(
        "Filter by District/Town (Locale):",
        options=df['District/Town'].unique(),
        default=[]
    )

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

    selected_rows = st.dataframe(
        df_filtered[[
            'Property_Name', 
            'District/Town', 
            'Primary_Commodity', 
            'Status', 
            'Distance_From_Chingola_km',
            'Travel_Time_From_Chingola_Hours'
        ]].style.format({
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
        selected_index = selected_rows['selection']['rows'][0]
        selected_site = df_filtered.loc[selected_index]
        
        col_map, col_logistics = st.columns([1, 1])

        with col_map:
            st.subheader(f"Map View: {selected_site['Property_Name']}")
            
            map_data = pd.DataFrame({
                'lat': [CHINGOLA_COORDS[0], selected_site['Latitude']],
                'lon': [CHINGOLA_COORDS[1], selected_site['Longitude']],
                'name': [CHINGOLA_NAME, selected_site['Property_Name']],
                'color': ['#00FF00', '#FF0000']
            })

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
                mapbox_style="carto-positron"
            )
            
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

# --- Authentication Logic ---
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.markdown(f'Welcome, **{name}**')
    run_app()
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')