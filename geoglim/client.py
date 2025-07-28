import requests
import geopandas as gpd
from pathlib import Path
from typing import Optional, Union, Dict, Any
import tempfile
import json
from io import StringIO

from .exceptions import GeoGlimError, DatasetNotFoundError, ClippingError

class GeoGlimClient:
    """
    Python client for GeoGlim API
    
    Provides easy access to geological datasets through the GeoGlim backend API.
    Supports both local development and future cloud deployments.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize GeoGlim client
        
        Args:
            base_url: Base URL of the GeoGlim API server
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        
        # Test connection on initialization
        try:
            self.health_check()
        except Exception as e:
            raise GeoGlimError(f"Failed to connect to GeoGlim API at {base_url}: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health and dataset availability
        
        Returns:
            Dictionary with health status and available datasets
            
        Raises:
            GeoGlimError: If API is not accessible
        """
        try:
            response = self.session.get(f"{self.base_url}/")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise GeoGlimError(f"Health check failed: {str(e)}")
    
    def get_dataset_info(self, dataset: str) -> Dict[str, Any]:
        """
        Get information about a dataset
        
        Args:
            dataset: Dataset name ('glim' or 'glhymps')
            
        Returns:
            Dictionary with dataset information
            
        Raises:
            DatasetNotFoundError: If dataset is not available
            GeoGlimError: If API request fails
        """
        try:
            response = self.session.get(f"{self.base_url}/datasets/{dataset}/info")
            
            if response.status_code == 404:
                raise DatasetNotFoundError(f"Dataset '{dataset}' not found or not available")
            
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            if "404" in str(e):
                raise DatasetNotFoundError(f"Dataset '{dataset}' not found")
            raise GeoGlimError(f"Failed to get dataset info: {str(e)}")
    
    def clip_dataset(
        self,
        dataset: str,
        aoi: Union[str, Path, gpd.GeoDataFrame],
        output_format: str = "geojson",
        output_path: Optional[Union[str, Path]] = None
    ) -> gpd.GeoDataFrame:
        """
        Clip a dataset to an Area of Interest (AOI)
        
        Args:
            dataset: Dataset name ('glim' or 'glhymps')
            aoi: Area of Interest - can be:
                - Path to GeoJSON file
                - GeoDataFrame object
                - GeoJSON string
            output_format: Output format ('geojson', 'shapefile', 'gpkg')
            output_path: Optional path to save the result file
            
        Returns:
            GeoDataFrame with clipped data
            
        Raises:
            DatasetNotFoundError: If dataset is not available
            ClippingError: If clipping operation fails
            GeoGlimError: If API request fails
        """
        try:
            # Prepare AOI data
            aoi_data = self._prepare_aoi(aoi)
            
            # Prepare request
            files = {
                'geojson_file': ('aoi.geojson', aoi_data, 'application/json')
            }
            params = {
                'output_format': output_format
            }
            
            # Make request
            response = self.session.post(
                f"{self.base_url}/clip/{dataset}",
                files=files,
                params=params
            )
            
            # Handle errors
            if response.status_code == 404:
                raise DatasetNotFoundError(f"Dataset '{dataset}' not found or not available")
            elif response.status_code == 413:
                raise ClippingError("File or area too large for processing")
            elif response.status_code >= 400:
                error_detail = response.json().get("detail", "Unknown error")
                raise ClippingError(f"Clipping failed: {error_detail}")
            
            response.raise_for_status()
            
            # Save response to temporary file
            temp_file = tempfile.NamedTemporaryFile(
                suffix=f".{output_format}", 
                delete=False
            )
            
            with open(temp_file.name, 'wb') as f:
                f.write(response.content)
            
            # Read result as GeoDataFrame
            result_gdf = gpd.read_file(temp_file.name)
            
            # Save to specified output path if provided
            if output_path:
                result_gdf.to_file(str(output_path))
            
            return result_gdf
            
        except (DatasetNotFoundError, ClippingError):
            raise
        except Exception as e:
            raise ClippingError(f"Clipping operation failed: {str(e)}")
    
    def _prepare_aoi(self, aoi: Union[str, Path, gpd.GeoDataFrame]) -> str:
        """
        Prepare AOI data for API request
        
        Args:
            aoi: Area of Interest in various formats
            
        Returns:
            GeoJSON string ready for upload
            
        Raises:
            GeoGlimError: If AOI cannot be processed
        """
        try:
            if isinstance(aoi, gpd.GeoDataFrame):
                # Convert GeoDataFrame to GeoJSON string
                return aoi.to_json()
            
            elif isinstance(aoi, (str, Path)):
                path = Path(aoi)
                if path.exists():
                    # Read from file
                    gdf = gpd.read_file(str(path))
                    return gdf.to_json()
                else:
                    # Assume it's a GeoJSON string
                    # Validate by parsing
                    json.loads(str(aoi))
                    return str(aoi)
            
            else:
                raise ValueError(f"Unsupported AOI type: {type(aoi)}")
                
        except Exception as e:
            raise GeoGlimError(f"Failed to prepare AOI data: {str(e)}")
    
    def list_available_datasets(self) -> Dict[str, bool]:
        """
        List all available datasets
        
        Returns:
            Dictionary mapping dataset names to availability status
        """
        health_data = self.health_check()
        return health_data.get("datasets_available", {})
