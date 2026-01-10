"""
Geological Analysis Module for Zambia Mining App
Provides functions for vein mapping, trend analysis, and geological pattern identification
"""

import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from shapely.geometry import LineString, Point, Polygon

def identify_mineral_belts(df, commodity, buffer_km=30):
    """
    Identify linear mineral belts for a specific commodity using PCA
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    commodity : str
        Commodity to analyze (e.g., 'Copper')
    buffer_km : float
        Buffer distance for belt width estimation
    
    Returns:
    --------
    Dictionary with belt characteristics or None if insufficient data
    """
    
    # Filter to specific commodity
    commodity_sites = df[df['Primary_Commodity'] == commodity].copy()
    
    if len(commodity_sites) < 3:
        return None
    
    # Get coordinates (lon, lat for consistency)
    coords = commodity_sites[['Longitude', 'Latitude']].values
    
    # PCA to find principal direction of variation
    pca = PCA(n_components=2)
    pca.fit(coords)
    
    # Principal direction vector (represents belt strike)
    direction = pca.components_[0]
    
    # Calculate bearing (0-360 degrees, where 0 = North, 90 = East)
    bearing_rad = np.arctan2(direction[1], direction[0])
    bearing = (90 - np.degrees(bearing_rad)) % 360  # Convert to compass bearing
    
    # Project points onto principal axis to measure extent
    transformed = pca.transform(coords)
    
    # Belt dimensions
    length_deg = transformed[:, 0].max() - transformed[:, 0].min()
    width_deg = transformed[:, 1].max() - transformed[:, 1].min()
    
    # Convert to km (approximate: 1 degree ≈ 111 km)
    length_km = length_deg * 111
    width_km = width_deg * 111
    
    # Calculate explained variance (how linear the pattern is)
    linearity = pca.explained_variance_ratio_[0]
    
    return {
        'commodity': commodity,
        'bearing': float(bearing),
        'length_km': float(length_km),
        'width_km': float(width_km),
        'site_count': len(commodity_sites),
        'center_lat': float(commodity_sites['Latitude'].mean()),
        'center_lon': float(commodity_sites['Longitude'].mean()),
        'linearity': float(linearity),  # 0-1, higher = more linear
        'variance_explained': float(pca.explained_variance_ratio_[0] * 100)
    }

def create_trend_lines(df, commodity, extension_factor=1.2):
    """
    Create trend line coordinates for visualization
    
    Parameters:
    -----------
    df : DataFrame
        Mining sites data
    commodity : str
        Commodity to analyze
    extension_factor : float
        How much to extend line beyond data points (1.0 = exact fit, 1.2 = 20% extension)
    
    Returns:
    --------
    Dictionary with start and end coordinates, or None
    """
    
    commodity_sites = df[df['Primary_Commodity'] == commodity]
    
    if len(commodity_sites) < 2:
        return None
    
    coords = commodity_sites[['Longitude', 'Latitude']].values
    
    # PCA for trend direction
    pca = PCA(n_components=1)
    pca.fit(coords)
    
    # Mean point (center of belt)
    mean_point = coords.mean(axis=0)
    
    # Direction vector
    direction = pca.components_[0]
    
    # Calculate extent
    projected = pca.transform(coords)
    max_distance = np.max(np.abs(projected))
    
    # Create line endpoints
    start_point = mean_point - direction * max_distance * extension_factor
    end_point = mean_point + direction * max_distance * extension_factor
    
    return {
        'start_lon': float(start_point[0]),
        'start_lat': float(start_point[1]),
        'end_lon': float(end_point[0]),
        'end_lat': float(end_point[1]),
        'commodity': commodity,
        'center_lon': float(mean_point[0]),
        'center_lat': float(mean_point[1])
    }

def analyze_geology_patterns(df):
    """
    Analyze patterns in geological formations
    
    Returns:
    --------
    DataFrame with geological pattern statistics
    """
    
    patterns = []
    
    # Group by geology type
    for geology_type in df['Geology_Classification'].dropna().unique():
        geology_sites = df[df['Geology_Classification'] == geology_type]
        
        if len(geology_sites) < 3:
            continue
        
        # Get commodity distribution
        commodity_dist = geology_sites['Primary_Commodity'].value_counts().to_dict()
        top_commodity = geology_sites['Primary_Commodity'].mode()[0] if len(geology_sites) > 0 else 'Unknown'
        
        # Get province distribution
        province_dist = geology_sites['Province'].value_counts().to_dict()
        top_province = geology_sites['Province'].mode()[0] if len(geology_sites) > 0 else 'Unknown'
        
        # Calculate spatial extent
        lat_range = geology_sites['Latitude'].max() - geology_sites['Latitude'].min()
        lon_range = geology_sites['Longitude'].max() - geology_sites['Longitude'].min()
        spatial_extent_km = np.sqrt((lat_range * 111)**2 + (lon_range * 111)**2)
        
        pattern = {
            'Geology_Type': geology_type,
            'Site_Count': len(geology_sites),
            'Top_Commodity': top_commodity,
            'Commodity_Diversity': len(commodity_dist),
            'Top_Province': top_province,
            'Avg_Latitude': float(geology_sites['Latitude'].mean()),
            'Avg_Longitude': float(geology_sites['Longitude'].mean()),
            'Spatial_Extent_km': float(spatial_extent_km)
        }
        
        patterns.append(pattern)
    
    patterns_df = pd.DataFrame(patterns)
    
    # Sort by site count
    if len(patterns_df) > 0:
        patterns_df = patterns_df.sort_values('Site_Count', ascending=False)
    
    return patterns_df

def calculate_vein_statistics(df, commodity):
    """
    Calculate detailed statistics for a commodity vein/belt
    
    Returns:
    --------
    Dictionary with vein statistics
    """
    
    commodity_sites = df[df['Primary_Commodity'] == commodity]
    
    if len(commodity_sites) < 2:
        return None
    
    # Get belt information
    belt_info = identify_mineral_belts(df, commodity)
    
    if not belt_info:
        return None
    
    # Additional statistics
    stats = {
        **belt_info,
        'active_sites': len(commodity_sites[commodity_sites['Status'] == 'Active']),
        'provinces_covered': commodity_sites['Province'].nunique(),
        'districts_covered': commodity_sites['Clean_District'].nunique(),
        'avg_density_score': float(commodity_sites['Density_Score'].mean()) if 'Density_Score' in commodity_sites.columns else None,
        'geology_types': commodity_sites['Geology_Classification'].nunique()
    }
    
    return stats

def get_geological_summary(df):
    """
    Get overall geological summary statistics
    
    Returns:
    --------
    Dictionary with summary statistics
    """
    
    summary = {
        'total_geology_types': df['Geology_Classification'].nunique(),
        'most_common_geology': df['Geology_Classification'].mode()[0] if len(df) > 0 else 'Unknown',
        'sites_with_geology_data': df['Geology_Classification'].notna().sum(),
        'geology_coverage_percent': float((df['Geology_Classification'].notna().sum() / len(df)) * 100)
    }
    
    # Top geology types
    top_geologies = df['Geology_Classification'].value_counts().head(5).to_dict()
    summary['top_geology_types'] = top_geologies
    
    return summary

def identify_geological_provinces(df, min_sites=10):
    """
    Identify major geological provinces based on commodity and geology patterns
    
    Returns:
    --------
    DataFrame with geological province information
    """
    
    provinces = []
    
    # Group by actual province and dominant commodity
    for province in df['Province'].unique():
        province_data = df[df['Province'] == province]
        
        if len(province_data) < min_sites:
            continue
        
        # Get dominant characteristics
        dominant_commodity = province_data['Primary_Commodity'].mode()[0] if len(province_data) > 0 else 'Mixed'
        dominant_geology = province_data['Geology_Classification'].mode()[0] if province_data['Geology_Classification'].notna().sum() > 0 else 'Unknown'
        
        province_info = {
            'Province': province,
            'Site_Count': len(province_data),
            'Dominant_Commodity': dominant_commodity,
            'Dominant_Geology': dominant_geology,
            'Commodity_Diversity': province_data['Primary_Commodity'].nunique(),
            'Geology_Diversity': province_data['Geology_Classification'].nunique(),
            'Center_Lat': float(province_data['Latitude'].mean()),
            'Center_Lon': float(province_data['Longitude'].mean()),
            'Active_Sites': len(province_data[province_data['Status'] == 'Active'])
        }
        
        provinces.append(province_info)
    
    provinces_df = pd.DataFrame(provinces)
    
    # Sort by site count
    if len(provinces_df) > 0:
        provinces_df = provinces_df.sort_values('Site_Count', ascending=False)
    
    return provinces_df

def calculate_commodity_concentration(df, commodity):
    """
    Calculate geographic concentration index for a commodity
    Higher values indicate more concentrated/clustered distribution
    
    Returns:
    --------
    Float between 0 and 1 (higher = more concentrated)
    """
    
    commodity_sites = df[df['Primary_Commodity'] == commodity]
    
    if len(commodity_sites) < 2:
        return None
    
    coords = commodity_sites[['Latitude', 'Longitude']].values
    
    # Calculate pairwise distances
    from scipy.spatial.distance import pdist
    distances = pdist(coords)
    
    # Normalized concentration index
    # Lower average distance = higher concentration
    avg_distance = np.mean(distances)
    
    # Get maximum possible distance in Zambia (approximate)
    max_distance = 10.0  # degrees (roughly 1100 km)
    
    concentration = 1 - (avg_distance / max_distance)
    
    return float(max(0, min(1, concentration)))
