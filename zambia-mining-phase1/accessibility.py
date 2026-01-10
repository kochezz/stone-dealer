"""
Accessibility Analysis Module for Zambia Mining App
Provides functions for calculating and analyzing site accessibility
"""

import pandas as pd
import numpy as np

def calculate_accessibility_score(df):
    """
    Calculate comprehensive accessibility score for each site
    
    Score components (0-100):
    - Distance from Chingola base (40 points)
    - Travel time from Chingola (30 points)
    - Distance to nearest center (20 points)
    - Province infrastructure rating (10 points)
    
    Returns:
    --------
    DataFrame with added Accessibility_Score and Access_Category columns
    """
    
    scores = pd.DataFrame(index=df.index)
    
    # Component 1: Distance from Chingola (40 points, inverse scoring)
    # Closer sites get higher scores
    if 'Distance_From_Chingola_km' in df.columns:
        max_distance = df['Distance_From_Chingola_km'].max()
        if max_distance > 0:
            scores['chingola_distance_score'] = (
                40 * (1 - df['Distance_From_Chingola_km'] / max_distance)
            )
        else:
            scores['chingola_distance_score'] = 40
    else:
        scores['chingola_distance_score'] = 20  # Default neutral score
    
    # Component 2: Travel time (30 points, inverse scoring)
    if 'Travel_Time_From_Chingola_Hours' in df.columns:
        max_time = df['Travel_Time_From_Chingola_Hours'].max()
        if max_time > 0:
            scores['travel_time_score'] = (
                30 * (1 - df['Travel_Time_From_Chingola_Hours'] / max_time)
            )
        else:
            scores['travel_time_score'] = 30
    else:
        scores['travel_time_score'] = 15  # Default neutral score
    
    # Component 3: Distance to nearest center (20 points, inverse scoring)
    if 'Distance_Nearest_Center_km' in df.columns:
        max_center_dist = df['Distance_Nearest_Center_km'].max()
        if max_center_dist > 0:
            scores['nearest_center_score'] = (
                20 * (1 - df['Distance_Nearest_Center_km'].fillna(max_center_dist) / max_center_dist)
            )
        else:
            scores['nearest_center_score'] = 20
    else:
        scores['nearest_center_score'] = 10  # Default neutral score
    
    # Component 4: Province infrastructure rating (10 points)
    # Based on general infrastructure development in each province
    province_scores = {
        'Copperbelt Province': 10,    # Best infrastructure (historical mining)
        'Lusaka Province': 9,           # Capital region, good roads
        'Central Province': 7,          # Moderate infrastructure
        'Southern Province': 6,         # Decent infrastructure
        'Northern Province': 5,         # Developing infrastructure
        'Eastern Province': 5,          # Developing infrastructure
        'Muchinga Province': 4,         # Limited infrastructure
        'North-Western Province': 4,   # Remote, limited infrastructure
        'Luapula Province': 3,          # Remote, limited infrastructure
        'Western Province': 3           # Remote, limited infrastructure
    }
    scores['province_infrastructure_score'] = df['Province'].map(province_scores).fillna(5)
    
    # Calculate total accessibility score (0-100)
    df['Accessibility_Score'] = scores.sum(axis=1)
    
    # Categorize accessibility
    df['Access_Category'] = pd.cut(
        df['Accessibility_Score'],
        bins=[0, 40, 60, 80, 100],
        labels=['Poor', 'Fair', 'Good', 'Excellent'],
        include_lowest=True
    )
    
    return df

def rank_by_accessibility(df, n=20, ascending=False):
    """
    Get top N sites by accessibility score
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites with Accessibility_Score
    n : int
        Number of sites to return
    ascending : bool
        False for most accessible (default), True for least accessible
    
    Returns:
    --------
    DataFrame with top/bottom N sites
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    return df.nlargest(n, 'Accessibility_Score') if not ascending else df.nsmallest(n, 'Accessibility_Score')

def get_accessibility_statistics(df, by_province=False):
    """
    Get accessibility statistics
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites with accessibility scores
    by_province : bool
        If True, return stats by province
    
    Returns:
    --------
    Dictionary or DataFrame with statistics
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    if not by_province:
        # Overall statistics
        stats = {
            'total_sites': len(df),
            'avg_accessibility': float(df['Accessibility_Score'].mean()),
            'median_accessibility': float(df['Accessibility_Score'].median()),
            'max_accessibility': float(df['Accessibility_Score'].max()),
            'min_accessibility': float(df['Accessibility_Score'].min()),
            'excellent_count': len(df[df['Access_Category'] == 'Excellent']),
            'good_count': len(df[df['Access_Category'] == 'Good']),
            'fair_count': len(df[df['Access_Category'] == 'Fair']),
            'poor_count': len(df[df['Access_Category'] == 'Poor']),
            'avg_distance_chingola': float(df['Distance_From_Chingola_km'].mean()) if 'Distance_From_Chingola_km' in df.columns else None,
            'avg_travel_time': float(df['Travel_Time_From_Chingola_Hours'].mean()) if 'Travel_Time_From_Chingola_Hours' in df.columns else None
        }
        return stats
    else:
        # Statistics by province
        province_stats = []
        
        for province in df['Province'].unique():
            province_data = df[df['Province'] == province]
            
            stats = {
                'Province': province,
                'Site_Count': len(province_data),
                'Avg_Accessibility': float(province_data['Accessibility_Score'].mean()),
                'Excellent_Sites': len(province_data[province_data['Access_Category'] == 'Excellent']),
                'Good_Sites': len(province_data[province_data['Access_Category'] == 'Good']),
                'Fair_Sites': len(province_data[province_data['Access_Category'] == 'Fair']),
                'Poor_Sites': len(province_data[province_data['Access_Category'] == 'Poor'])
            }
            
            province_stats.append(stats)
        
        return pd.DataFrame(province_stats).sort_values('Avg_Accessibility', ascending=False)

def calculate_infrastructure_index(df):
    """
    Calculate a more detailed infrastructure index
    Combines multiple factors for comprehensive assessment
    
    Returns:
    --------
    DataFrame with Infrastructure_Index column
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    # Infrastructure index components
    components = pd.DataFrame(index=df.index)
    
    # 1. Accessibility score (50%)
    components['accessibility'] = df['Accessibility_Score'] * 0.5
    
    # 2. Activity status (25%) - Active sites likely have better infrastructure
    status_weights = {
        'Active': 25,
        'Active (Small Mining)': 20,
        'Feasibility Evaluation': 15,
        'Local Mining': 15,
        'Dormant': 10,
        'Unknown': 5,
        'Inactive': 0
    }
    components['activity'] = df['Status'].map(status_weights).fillna(5)
    
    # 3. District development (15%) - Based on number of sites (proxy for infrastructure)
    district_counts = df['Clean_District'].value_counts()
    df['District_Site_Count'] = df['Clean_District'].map(district_counts)
    max_district_count = df['District_Site_Count'].max()
    components['district_development'] = 15 * (df['District_Site_Count'] / max_district_count)
    
    # 4. Reserve presence (10%) - Sites with reserves more likely to have infrastructure
    components['reserve_presence'] = df['Reserves'].notna().astype(int) * 10
    
    # Calculate total infrastructure index (0-100)
    df['Infrastructure_Index'] = components.sum(axis=1)
    
    # Clean up temporary column
    df = df.drop('District_Site_Count', axis=1)
    
    return df

def identify_infrastructure_gaps(df, threshold=40):
    """
    Identify high-value sites with poor accessibility
    These represent infrastructure development opportunities
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    threshold : int
        Accessibility score threshold (below this = poor access)
    
    Returns:
    --------
    DataFrame with infrastructure gap sites
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    if 'Density_Score' not in df.columns:
        # Import and calculate if needed
        from density_analysis import calculate_density_score
        df = calculate_density_score(df)
    
    # High value but poor accessibility
    gap_sites = df[
        (df['Accessibility_Score'] < threshold) &
        (df['Density_Score'] >= 60)  # High density = high value
    ].copy()
    
    # Calculate potential value gain from infrastructure improvement
    gap_sites['Access_Gap'] = threshold - gap_sites['Accessibility_Score']
    gap_sites['Infrastructure_Priority'] = gap_sites['Density_Score'] * gap_sites['Access_Gap']
    
    # Sort by priority
    gap_sites = gap_sites.sort_values('Infrastructure_Priority', ascending=False)
    
    return gap_sites[[
        'Property_Name', 'Province', 'Clean_District', 'Primary_Commodity',
        'Density_Score', 'Accessibility_Score', 'Access_Gap', 'Infrastructure_Priority',
        'Latitude', 'Longitude'
    ]]

def calculate_regional_accessibility(df):
    """
    Calculate average accessibility by region (province/district)
    
    Returns:
    --------
    Tuple of (province_stats, district_stats) DataFrames
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    # Province-level statistics
    province_stats = df.groupby('Province').agg({
        'Accessibility_Score': ['mean', 'median', 'min', 'max', 'count'],
        'Distance_From_Chingola_km': 'mean',
        'Travel_Time_From_Chingola_Hours': 'mean'
    }).round(2)
    
    province_stats.columns = [
        'Avg_Access_Score', 'Median_Access_Score', 'Min_Access_Score', 
        'Max_Access_Score', 'Site_Count', 'Avg_Distance_km', 'Avg_Travel_Hours'
    ]
    province_stats = province_stats.sort_values('Avg_Access_Score', ascending=False)
    
    # District-level statistics (top 20)
    district_stats = df.groupby('Clean_District').agg({
        'Accessibility_Score': ['mean', 'count'],
        'Province': 'first'
    }).round(2)
    
    district_stats.columns = ['Avg_Access_Score', 'Site_Count', 'Province']
    district_stats = district_stats[district_stats['Site_Count'] >= 3]  # Only districts with 3+ sites
    district_stats = district_stats.sort_values('Avg_Access_Score', ascending=False).head(20)
    
    return province_stats.reset_index(), district_stats.reset_index()

def create_accessibility_clusters(df, score_threshold=60):
    """
    Identify clusters of accessible sites
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    score_threshold : int
        Minimum accessibility score to include
    
    Returns:
    --------
    DataFrame with accessible site clusters
    """
    
    if 'Accessibility_Score' not in df.columns:
        df = calculate_accessibility_score(df)
    
    # Filter to accessible sites
    accessible_sites = df[df['Accessibility_Score'] >= score_threshold].copy()
    
    # Group by district to identify accessible hubs
    district_access = accessible_sites.groupby('Clean_District').agg({
        'Property_Name': 'count',
        'Accessibility_Score': 'mean',
        'Latitude': 'mean',
        'Longitude': 'mean',
        'Province': 'first'
    }).round(2)
    
    district_access.columns = [
        'Site_Count', 'Avg_Access_Score', 'Center_Lat', 'Center_Lon', 'Province'
    ]
    
    # Only include districts with multiple accessible sites
    district_access = district_access[district_access['Site_Count'] >= 3]
    district_access = district_access.sort_values('Site_Count', ascending=False)
    
    return district_access.reset_index()
