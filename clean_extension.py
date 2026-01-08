import pandas as pd
import numpy as np
import math
import os


# --- CONFIGURATION ---
# Updated Input File Path (Using raw string 'r' to handle backslashes)
INPUT_FILE = r"C:\Users\willi\OneDrive\Documents\COVEX\Cleaned 2\covex_restructured_csv_file_last_200.xlsx"

# The output file will be saved in the same folder as this script
OUTPUT_FILE = "covex_cleaned_extension.csv"

# Base coordinates for calculations
CHINGOLA_COORDS = (-12.5333, 27.8500)

# --- 1. Coordinate Conversion (DMS to Decimal Degrees) ---
def dms_to_dd(dms_str):
    if pd.isna(dms_str):
        return np.nan
    # Clean string: remove symbols, extra spaces
    dms_str = str(dms_str).upper().replace('°', ' ').replace("'", ' ').replace('"', ' ').strip()
    parts = dms_str.split()
    if not parts:
        return np.nan
    
    try:
        # Extract numeric parts
        nums = [float(x) for x in parts if x.replace('.','',1).isdigit()]
        if not nums: return np.nan
        
        degrees = nums[0]
        minutes = nums[1] if len(nums) > 1 else 0
        seconds = nums[2] if len(nums) > 2 else 0
        
        dd = degrees + minutes/60 + seconds/3600
        
        # Determine direction (S/W are negative)
        direction = parts[-1] if parts[-1] in ['N', 'S', 'E', 'W'] else ''
        if direction in ['S', 'W'] or (direction == '' and len(parts)>1 and parts[1] in ['S', 'W']):
             dd = -dd
        elif direction == '' and 'S' in dms_str: 
             dd = -dd
        return dd
    except:
        return np.nan

# --- 2. Location Standardization Logic ---
district_province_map = {
    'Kitwe': 'Copperbelt', 'Ndola': 'Copperbelt', 'Mufulira': 'Copperbelt', 'Chingola': 'Copperbelt', 
    'Chililabombwe': 'Copperbelt', 'Luanshya': 'Copperbelt', 'Kalulushi': 'Copperbelt', 
    'Solwezi': 'North-Western', 'Mwinilunga': 'North-Western', 'Kasempa': 'North-Western', 
    'Kabompo': 'North-Western', 'Zambezi': 'North-Western', 'Mufumbwe': 'North-Western', 
    'Kabwe': 'Central', 'Mkushi': 'Central', 'Mukushi': 'Central', 'Serenje': 'Central', 
    'Mumbwa': 'Central', 'Kapiri Mposhi': 'Central', 'Chibombo': 'Central',
    'Mansa': 'Luapula', 'Nchelenge': 'Luapula', 'Kawambwa': 'Luapula', 'Mwense': 'Luapula', 
    'Samfya': 'Luapula', 'Mweru': 'Luapula',
    'Kasama': 'Northern', 'Mbala': 'Northern', 'Mporokoso': 'Northern', 'Kaputa': 'Northern', 
    'Luwingu': 'Northern', 'Senga Hill': 'Northern',
    'Chinsali': 'Muchinga', 'Isoka': 'Muchinga', 'Mpika': 'Muchinga', 'Nakonde': 'Muchinga', 
    'Mafinga': 'Muchinga', 'Shiwang\'andu': 'Muchinga',
    'Chipata': 'Eastern', 'Lundazi': 'Eastern', 'Petauke': 'Eastern', 'Katete': 'Eastern', 
    'Nyimba': 'Eastern', 'Mambwe': 'Eastern',
    'Choma': 'Southern', 'Livingstone': 'Southern', 'Mazabuka': 'Southern', 'Monze': 'Southern',
    'Mongu': 'Western', 'Kaoma': 'Western', 'Sesheke': 'Western',
    'Lusaka': 'Lusaka', 'Kafue': 'Lusaka', 'Chongwe': 'Lusaka', 'Rufunsa': 'Lusaka'
}

def standardize_location(row):
    text = str(row['District/Town'])
    found_district = None
    province = "Unknown"
    
    # Check map for matches
    for dist, prov in district_province_map.items():
        if dist.lower() in text.lower():
            found_district = dist
            province = prov
            break
            
    # Fallback: Use original text if no match found
    if not found_district:
        found_district = text.title() 
    
    return pd.Series([found_district, province])

# --- 3. Travel Calculation (Haversine) ---
def calc_logistics(row):
    if pd.isna(row['Latitude']) or pd.isna(row['Longitude']):
        return pd.Series([np.nan, np.nan])
    
    # Haversine formula
    lat1, lon1 = CHINGOLA_COORDS
    lat2, lon2 = row['Latitude'], row['Longitude']
    R = 6371.0 # km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dist_km = R * c
    
    time_hr = dist_km / 70.0 # 70 km/h assumption
    return pd.Series([dist_km, time_hr])

# --- MAIN EXECUTION ---
try:
    print(f"Loading data from: {INPUT_FILE}")
    # Load Excel file
    df = pd.read_excel(INPUT_FILE)
    
    # 1. Rename Columns to Match Master Standard
    print("Standardizing column names...")
    df.rename(columns={
        'Property Name': 'Property_Name',
        'Locale': 'District/Town',
        'Distance From Nearest Center': 'Distance_Nearest_Center_km',
        'Geology Classification': 'Geology_Classification',
        'Geology Description': 'Geology_Description',
        'Commodity 1, 2, 3': 'Commodities_Combined' 
    }, inplace=True)

    # 2. Process Coordinates
    print("Converting coordinates...")
    df['Latitude'] = df['Latitude'].apply(dms_to_dd)
    df['Longitude'] = df['Longitude'].apply(dms_to_dd)

    # 3. Split Commodities
    print("Splitting commodities...")
    def split_commodities(val):
        parts = str(val).split(',') if pd.notna(val) else []
        return pd.Series([
            parts[0].strip() if len(parts) > 0 else None,
            parts[1].strip() if len(parts) > 1 else None,
            parts[2].strip() if len(parts) > 2 else None
        ])
    df[['Primary_Commodity', 'Commodity_2', 'Commodity_3']] = df['Commodities_Combined'].apply(split_commodities)

    # 4. Text Cleaning (Typos)
    print("Cleaning text typos...")
    replacements = {
        'Mxushi': 'Mukushi', 'Kasenpa': 'Kasempa', 'Kitme': 'Kitwe', 
        'Bisects': 'dissects', 'Muniilunga': 'Mwinilunga', 'Mainilunga': 'Mwinilunga',
        'Kabowpo': 'Kabompo', 'Solwezi': 'Solwezi', 'Solvezi': 'Solwezi',
        'Ameru': 'Mweru', 'Mneru': 'Mweru', 'Wanitpa': 'Wantipa', 'Tanganyixa': 'Tanganyika',
        'Nodla': 'Ndola', 'Copperbellt': 'Copperbelt', 'Copperselt': 'Copperbelt',
        'Luangua': 'Luangwa', 'Numbwa': 'Mumbwa', 'Nunbua': 'Mumbwa', 'Broken Hill': 'Kabwe',
        'Serga Hill': 'Senga Hill'
    }
    for col in df.select_dtypes(include=['object']):
        for wrong, right in replacements.items():
            df[col] = df[col].astype(str).str.replace(wrong, right, regex=True, case=False)

    # 5. Geolocation Standardization
    print("Aligning geolocation data...")
    loc_data = df.apply(standardize_location, axis=1)
    df['District/Town_Original'] = df['District/Town']
    df['District/Town'] = loc_data[0]
    df['Province'] = loc_data[1]

    # 6. Logistics
    print("Calculating travel logistics...")
    df[['Distance_From_Chingola_km', 'Travel_Time_From_Chingola_Hours']] = df.apply(calc_logistics, axis=1)

    # 7. Final Column Alignment
    final_cols = [
        'Property_Name', 'Latitude', 'Longitude', 'District/Town', 'Distance_Nearest_Center_km',
        'Primary_Commodity', 'Commodity_2', 'Commodity_3', 'Status', 'Reserves',
        'Geology_Classification', 'Geology_Description', 'Distance_From_Chingola_km',
        'Travel_Time_From_Chingola_Hours', 'Province', 'District/Town_Original'
    ]
    
    # Ensure all columns exist
    for c in final_cols:
        if c not in df.columns: df[c] = None
            
    df_final = df[final_cols]
    
    # SAVE
    df_final.to_csv(OUTPUT_FILE, index=False)
    print(f"SUCCESS! Cleaned file saved as: {OUTPUT_FILE}")
    print(f"Total entries processed: {len(df_final)}")
    print(df_final.head())

except FileNotFoundError:
    print(f"Error: Could not find input file at:\n{INPUT_FILE}\nPlease double-check the path.")
except Exception as e:
    print(f"An error occurred: {e}")