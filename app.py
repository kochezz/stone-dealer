import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import streamlit_authenticator as stauth
import copy # <--- Make sure this is imported at the top

# --- AUTHENTICATION CONFIG (Fixed) ---
try:
    # 1. Fetch secrets
    # We use copy.deepcopy() to ensure the authenticator can modify the dict 
    # (e.g., for hashing) without crashing on the read-only st.secrets.
    if 'credentials' not in st.secrets:
        raise KeyError("Missing '[credentials]' section in secrets.toml")
        
    if 'cookie' not in st.secrets:
        raise KeyError("Missing '[cookie]' section in secrets.toml")

    credentials = copy.deepcopy(st.secrets['credentials'])
    cookie = copy.deepcopy(st.secrets['cookie'])
    
    # 2. Setup Authenticator
    authenticator = stauth.Authenticate(
        credentials,
        cookie['name'],
        cookie['key'],
        cookie['expiry_days'],
    )
except Exception as e:
    # This will now print the EXACT error to the screen so we can fix it
    st.error(f"Authentication Error: {e}")
    st.info("Check your Streamlit Cloud Secrets to ensure they match the TOML format below.")
    st.stop()
# --- Configuration Constants ---
DATA_FILENAME = "zambia_mining_app_data.csv" 
CHINGOLA_COORDS = (-12.5333, 27.8500)
CHINGOLA_NAME = "Chingola (Base of Operations)"

# --- Layout and Setup ---
st.set_page_config(
    page_title="Zambia Mining Site Assessment Planner",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AUTHENTICATION CONFIG (Restored) ---
# This block attempts to load secrets for password protection.
# If running locally, ensure .streamlit/secrets.toml exists.
# If running on cloud, ensure Secrets are configured in the dashboard.
try:
    auth_config = {
        'credentials': st.secrets['credentials'],
        'cookie': st.secrets['cookie']
    }
    
    authenticator = stauth.Authenticate(
        auth_config['credentials'],
        auth_config['cookie']['name'],
        auth_config['cookie']['key'],
        auth_config['cookie']['expiry_days'],
    )
except Exception as e:
    st.error("Authentication Error: Could not load secrets.")
    st.info("Please ensure you have a .streamlit/secrets.toml file (local) or Secrets configured (cloud).")
    st.stop()

# --- Function to Load Data ---
@st.cache_data
def load_data(file_path):
    """Loads the processed data and performs final type casting."""
    try:
        df = pd.read_csv(file_path)
        
        # Ensure coordinates are numeric
        df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        
        # Fill missing text fields to avoid errors in filters
        df['Province'] = df['Province'].fillna('Unknown')
        df['District/Town'] = df['District/Town'].fillna('Unknown')
        df['Primary_Commodity'] = df['Primary_Commodity'].fillna('Unknown')
        
        return df.dropna(subset=['Latitude', 'Longitude'])
    
    except FileNotFoundError:
        st.error(f"Error: Data file '{DATA_FILENAME}' not found.")
        return pd.DataFrame()

# --- MAIN APPLICATION LOGIC ---
def main_dashboard():
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

    # 1. Province Filter (From New File)
    selected_provinces = st.sidebar.multiselect(
        "Filter by Province:",
        options=sorted(df['Province'].unique()),
        default=[]
    )

    # 2. District Filter (Dynamic based on Province)
    if selected_provinces:
        available_districts = df[df['Province'].isin(selected_provinces)]['District/Town'].unique()
    else:
        available_districts = df['District/Town'].unique()

    selected_locales = st.sidebar.multiselect(
        "Filter by District/Town:",
        options=sorted(available_districts),
        default=[]
    )

    # 3. Commodity Filter
    selected_commodities = st.sidebar.multiselect(
        "Filter by Primary Commodity:",
        options=sorted(df['Primary_Commodity'].unique()),
        default=[]
    )

    # --- Apply Filters ---
    df_filtered = df.copy()
    
    if selected_provinces:
        df_filtered = df_filtered[df_filtered['Province'].isin(selected_provinces)]
        
    if selected_locales:
        df_filtered = df_filtered[df_filtered['District/Town'].isin(selected_locales)]
        
    if selected_commodities:
        df_filtered = df_filtered[df_filtered['Primary_Commodity'].isin(selected_commodities)]

    # --- Display Filtered Table ---
    st.subheader(f"Filtered Properties ({len(df_filtered)} Sites)")
    st.caption("Select a row below to populate the map and detail panels.")

    # Table View (Includes Province)
    table_columns = [
        'Property_Name', 
        'Province', 
        'District/Town', 
        'Primary_Commodity', 
        'Status', 
        'Distance_From_Chingola_km',
        'Travel_Time_From_Chingola_Hours'
    ]
    
    existing_cols = [c for c in table_columns if c in df_filtered.columns]

    selected_rows = st.dataframe(
        df_filtered[existing_cols].style.format({
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
        selected_site = df_filtered.iloc[selected_index]
        
        col_map, col_logistics = st.columns([1, 1])

        with col_map:
            st.subheader(f"📍 {selected_site['Property_Name']}")
            
            map_data = pd.DataFrame({
                'lat': [CHINGOLA_COORDS[0], selected_site['Latitude']],
                'lon': [CHINGOLA_COORDS[1], selected_site['Longitude']],
                'name': [CHINGOLA_NAME, selected_site['Property_Name']],
                'color': ['Base', 'Site'] 
            })

            fig = px.scatter_mapbox(
                map_data,
                lat="lat",
                lon="lon",
                hover_name="name",
                color="color",
                color_discrete_map={'Base': '#00FF00', 'Site': '#FF0000'},
                zoom=5,
                height=400,
                mapbox_style="carto-positron"
            )
            
            center_lat = (CHINGOLA_COORDS[0] + selected_site['Latitude']) / 2
            center_lon = (CHINGOLA_COORDS[1] + selected_site['Longitude']) / 2
            fig.update_layout(mapbox_center={"lat": center_lat, "lon": center_lon})
            
            st.plotly_chart(fig, use_container_width=True)

        with col_logistics:
            st.subheader("📊 Logistics & Location")
            st.markdown(f"**Province:** {selected_site.get('Province', 'Unknown')}")
            st.markdown(f"**District:** {selected_site.get('District/Town', 'Unknown')}")
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Distance", f"{selected_site['Distance_From_Chingola_km']:.0f} km")
            c2.metric("Est. Time", f"{selected_site['Travel_Time_From_Chingola_Hours']:.1f} hrs")
            st.info(f"**Status:** {selected_site.get('Status', 'Unknown')}")

        st.markdown("---")
        st.subheader("💎 Mineralogy & Geology")
        col_mineral, col_geology = st.columns(2)
        with col_mineral:
            st.markdown("**Commodities:**")
            st.markdown(f"- **Primary:** {selected_site.get('Primary_Commodity', '-')}")
            st.markdown(f"- **Secondary:** {selected_site.get('Commodity_2', '-')}")
        with col_geology:
            st.markdown("**Geological Assessment:**")
            st.caption(f"**Description:** {selected_site.get('Geology_Description', 'No description available.')}")
    else:
        st.info("Select a site from the table above to visualize its location and planning details.")

# --- LOGIN CONTROL FLOW ---
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f'Welcome, **{name}**')
    main_dashboard()
elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password')