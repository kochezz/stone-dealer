"""
Density Analysis Module for Zambia Mining App
Provides functions for resource density scoring, ranking, and clustering
"""

import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

def calculate_density_score(df, commodity=None):
    """
    Calculate resource density score for each site
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    commodity : str, optional
        Filter by specific commodity (e.g., 'Copper')
    
    Returns:
    --------
    DataFrame with added Density_Score column
    """
    
    # Filter by commodity if specified
    if commodity and commodity != 'All':
        df_work = df[df['Primary_Commodity'] == commodity].copy()
    else:
        df_work = df.copy()
    
    # Initialize scores dataframe
    scores = pd.DataFrame(index=df_work.index)
    
    # Component 1: Reserve presence (40 points)
    # Sites with documented reserves get full points
    scores['reserve_score'] = df_work['Reserves'].notna().astype(int) * 40
    
    # Component 2: Activity status (30 points)
    # Active sites are more valuable
    status_map = {
        'Active': 30,
        'Active (Small Mining)': 25,
        'Feasibility Evaluation': 20,
        'Local Mining': 18,
        'Dormant': 10,
        'Dewatering': 8,
        'Unknown': 5,
        'Inactive': 0,
        'Inactive Showing': 0,
        'Flooded/Percolation Plant': 5,
        'Mined By ZCCM': 12
    }
    scores['status_score'] = df_work['Status'].map(status_map).fillna(5)
    
    # Component 3: Multi-commodity bonus (15 points)
    # Sites with multiple commodities have diversification value
    scores['commodity_score'] = (
        (df_work['Commodity_2'].notna().astype(int) * 10) +
        (df_work['Commodity_3'].notna().astype(int) * 5)
    )
    
    # Component 4: Geological classification confidence (15 points)
    # Well-documented geology indicates better understanding
    scores['geology_score'] = df_work['Geology_Classification'].notna().astype(int) * 15
    
    # Calculate total density score (0-100)
    df_work['Density_Score'] = scores.sum(axis=1)
    
    # Add score to original dataframe (for filtered cases)
    df.loc[df_work.index, 'Density_Score'] = df_work['Density_Score']
    
    return df

def rank_sites_by_density(df, commodity='All', n=10, mode='top'):
    """
    Rank sites by density score
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data with Density_Score
    commodity : str
        Filter by commodity
    n : int
        Number of sites to return
    mode : str
        'top' for highest scores, 'bottom' for lowest
    
    Returns:
    --------
    DataFrame with top/bottom N sites
    """
    
    # Ensure density scores are calculated
    if 'Density_Score' not in df.columns:
        df = calculate_density_score(df, commodity)
    
    # Filter by commodity if needed
    if commodity and commodity != 'All':
        df_work = df[df['Primary_Commodity'] == commodity].copy()
    else:
        df_work = df.copy()
    
    # Sort based on mode
    ascending = (mode == 'bottom')
    df_sorted = df_work.sort_values('Density_Score', ascending=ascending)
    
    return df_sorted.head(n)

def categorize_by_density(df):
    """
    Categorize sites into density tiers
    
    Returns:
    --------
    DataFrame with added Density_Category column
    """
    
    if 'Density_Score' not in df.columns:
        df = calculate_density_score(df)
    
    # Create categories based on score ranges
    df['Density_Category'] = pd.cut(
        df['Density_Score'],
        bins=[0, 20, 40, 60, 80, 100],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'],
        include_lowest=True
    )
    
    return df

def create_density_clusters(df, eps_km=20, min_samples=5, commodity=None):
    """
    Identify resource clusters using DBSCAN spatial clustering
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    eps_km : float
        Maximum distance between sites in same cluster (km)
    min_samples : int
        Minimum sites required to form a cluster
    commodity : str, optional
        Filter by commodity before clustering
    
    Returns:
    --------
    Tuple of (df with Cluster_ID, cluster_stats DataFrame)
    """
    
    # Filter by commodity if specified
    if commodity and commodity != 'All':
        df_work = df[df['Primary_Commodity'] == commodity].copy()
    else:
        df_work = df.copy()
    
    # Get coordinates
    coords = df_work[['Latitude', 'Longitude']].values
    
    # DBSCAN clustering
    # eps in degrees: roughly 1 degree = 111 km at equator
    eps_degrees = eps_km / 111.0
    clustering = DBSCAN(eps=eps_degrees, min_samples=min_samples).fit(coords)
    
    # Add cluster labels
    df_work['Cluster_ID'] = clustering.labels_
    
    # Update original dataframe
    df.loc[df_work.index, 'Cluster_ID'] = df_work['Cluster_ID']
    
    # Calculate cluster statistics
    cluster_stats = []
    for cluster_id in df_work['Cluster_ID'].unique():
        if cluster_id == -1:  # Skip noise points (not in any cluster)
            continue
        
        cluster_data = df_work[df_work['Cluster_ID'] == cluster_id]
        
        # Calculate cluster metrics
        stats = {
            'Cluster_ID': int(cluster_id),
            'Site_Count': len(cluster_data),
            'Center_Lat': float(cluster_data['Latitude'].mean()),
            'Center_Lon': float(cluster_data['Longitude'].mean()),
            'Dominant_Commodity': cluster_data['Primary_Commodity'].mode()[0] if len(cluster_data) > 0 else 'Mixed',
            'Avg_Density_Score': float(cluster_data['Density_Score'].mean()) if 'Density_Score' in cluster_data.columns else 0,
            'Province': cluster_data['Province'].mode()[0] if len(cluster_data) > 0 else 'Unknown',
            'District': cluster_data['Clean_District'].mode()[0] if len(cluster_data) > 0 else 'Unknown'
        }
        cluster_stats.append(stats)
    
    cluster_stats_df = pd.DataFrame(cluster_stats)
    
    # Sort by site count
    if len(cluster_stats_df) > 0:
        cluster_stats_df = cluster_stats_df.sort_values('Site_Count', ascending=False)
    
    return df, cluster_stats_df

def get_density_statistics(df, commodity='All'):
    """
    Get summary statistics for density analysis
    
    Returns:
    --------
    Dictionary with statistics
    """
    
    if 'Density_Score' not in df.columns:
        df = calculate_density_score(df, commodity)
    
    if commodity and commodity != 'All':
        df_work = df[df['Primary_Commodity'] == commodity]
    else:
        df_work = df
    
    stats = {
        'total_sites': len(df_work),
        'avg_score': float(df_work['Density_Score'].mean()),
        'median_score': float(df_work['Density_Score'].median()),
        'max_score': float(df_work['Density_Score'].max()),
        'min_score': float(df_work['Density_Score'].min()),
        'std_score': float(df_work['Density_Score'].std()),
        'high_density_count': len(df_work[df_work['Density_Score'] >= 80]),
        'medium_density_count': len(df_work[(df_work['Density_Score'] >= 40) & (df_work['Density_Score'] < 80)]),
        'low_density_count': len(df_work[df_work['Density_Score'] < 40])
    }
    
    return stats
