import geopandas as gpd
import json
from io import StringIO
from typing import Union
from fastapi import HTTPException

def validate_geojson_file(contents: bytes) -> gpd.GeoDataFrame:
    """
    Validate and parse uploaded GeoJSON file
    
    Args:
        contents: Raw file contents as bytes
        
    Returns:
        GeoDataFrame with validated geometry
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Decode bytes to string
        geojson_str = contents.decode('utf-8')
        
        # Parse JSON
        geojson_data = json.loads(geojson_str)
        
        # Basic GeoJSON structure validation
        if not isinstance(geojson_data, dict):
            raise ValueError("GeoJSON must be a JSON object")
        
        if "type" not in geojson_data:
            raise ValueError("GeoJSON must have a 'type' field")
        
        # Convert to GeoDataFrame
        gdf = gpd.read_file(StringIO(geojson_str))
        
        # Validate geometry
        if gdf.empty:
            raise ValueError("GeoJSON contains no features")
        
        if not all(gdf.geometry.is_valid):
            raise ValueError("GeoJSON contains invalid geometries")
        
        # Check for proper CRS (add default if missing)
        if gdf.crs is None:
            gdf = gdf.set_crs("EPSG:4326")  # Assume WGS84 if no CRS
        
        return gdf
        
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid GeoJSON file: {str(e)}"
        )

def validate_area_size(gdf: gpd.GeoDataFrame, max_area: float) -> bool:
    """
    Validate that the total area doesn't exceed limits
    
    Args:
        gdf: GeoDataFrame to check
        max_area: Maximum allowed area in square units of the CRS
        
    Returns:
        True if area is within limits
        
    Raises:
        HTTPException: If area exceeds limits
    """
    try:
        # Calculate total area
        if gdf.crs.is_geographic:
            # For geographic CRS, convert to appropriate projected CRS for area calculation
            gdf_proj = gdf.to_crs("EPSG:3857")  # Web Mercator for rough area calculation
            total_area = gdf_proj.geometry.area.sum()
        else:
            total_area = gdf.geometry.area.sum()
        
        # Convert to km² for comparison
        area_km2 = total_area / 1_000_000  # Assuming meters
        
        if area_km2 > max_area:
            raise HTTPException(
                status_code=413,
                detail=f"Area too large: {area_km2:.1f} km². Max allowed: {max_area} km²"
            )
        
        return True
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Area validation failed: {str(e)}"
        )
