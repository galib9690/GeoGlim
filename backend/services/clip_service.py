import geopandas as gpd
import tempfile
from pathlib import Path
from typing import Tuple
import logging

from ..config import get_data_path, is_dataset_available

logger = logging.getLogger(__name__)

class ClipService:
    """Simple clipping service for local development"""
    
    def __init__(self):
        self._dataset_cache = {}  # Simple cache for loaded data
    
    def clip_data(
        self, 
        dataset: str, 
        aoi: gpd.GeoDataFrame,
        output_format: str
    ) -> Tuple[gpd.GeoDataFrame, str]:
        """Clip dataset to AOI - optimized for local files"""
        
        # Load dataset (with simple caching)
        if dataset not in self._dataset_cache:
            dataset_path = get_data_path(dataset)
            logger.info(f"Loading {dataset} from {dataset_path}")
            
            if dataset == "glim":
                # GLiM is in FileGDB format - need to specify layer
                full_data = gpd.read_file(str(dataset_path), layer="GLiM_export")
            else:
                # GLHYMPS is shapefile
                full_data = gpd.read_file(str(dataset_path))
            
            # Simple caching for local development
            self._dataset_cache[dataset] = full_data
            logger.info(f"Loaded {dataset}: {len(full_data)} features")
        else:
            full_data = self._dataset_cache[dataset]
            logger.info(f"Using cached {dataset} data")
        
        # Ensure CRS compatibility
        if aoi.crs != full_data.crs:
            logger.info(f"Reprojecting AOI from {aoi.crs} to {full_data.crs}")
            aoi = aoi.to_crs(full_data.crs)
        
        # Perform spatial intersection
        logger.info("Performing spatial clipping...")
        clipped = gpd.overlay(full_data, aoi, how="intersection")
        logger.info(f"Clipping result: {len(clipped)} features")
        
        # Save to temporary file
        temp_file_path = self._save_result(clipped, output_format)
        
        return clipped, temp_file_path
    
    def _save_result(self, gdf: gpd.GeoDataFrame, format: str) -> str:
        """Save GeoDataFrame to temporary file"""
        format_config = {
            "geojson": {"suffix": ".geojson", "driver": "GeoJSON"},
            "shapefile": {"suffix": ".shp", "driver": "ESRI Shapefile"},
            "gpkg": {"suffix": ".gpkg", "driver": "GPKG"}
        }
        
        config = format_config[format]
        temp_file = tempfile.NamedTemporaryFile(
            suffix=config["suffix"], 
            delete=False
        )
        
        gdf.to_file(temp_file.name, driver=config["driver"])
        return temp_file.name
    
    def get_dataset_info(self, dataset: str) -> dict:
        """Get basic dataset information"""
        dataset_path = get_data_path(dataset)
        
        # Read just a few rows to get structure info
        if dataset == "glim":
            # GLiM is in FileGDB format - need to specify layer
            sample_gdf = gpd.read_file(str(dataset_path), layer="GLiM_export", rows=5)
        else:
            # GLHYMPS is shapefile
            sample_gdf = gpd.read_file(str(dataset_path), rows=5)
        
        return {
            "dataset": dataset,
            "path": str(dataset_path),
            "crs": str(sample_gdf.crs),
            "columns": list(sample_gdf.columns),
            "geometry_type": str(sample_gdf.geometry.iloc[0].geom_type),
            "sample_feature_count": len(sample_gdf),
            "available": True,
            "hosting": "local"
        }
