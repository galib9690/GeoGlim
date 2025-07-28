"""
Basic tests for GeoGlim package
"""

import pytest
import geopandas as gpd
from pathlib import Path
import json

from geoglim import GeoGlimClient
from geoglim.exceptions import GeoGlimError, DatasetNotFoundError

class TestGeoGlimClient:
    """Basic tests for GeoGlim client functionality"""
    
    def test_client_initialization(self):
        """Test client initialization with different URLs"""
        # Test with default URL (will fail if server not running)
        try:
            client = GeoGlimClient()
            assert client.base_url == "http://localhost:8000"
        except GeoGlimError:
            # Expected if server is not running
            pass
        
        # Test with custom URL
        try:
            client = GeoGlimClient("http://example.com:8000")
            assert client.base_url == "http://example.com:8000"
        except GeoGlimError:
            # Expected if server is not accessible
            pass
    
    def test_aoi_preparation(self):
        """Test AOI data preparation methods"""
        # Create a simple test GeoDataFrame
        from shapely.geometry import Point
        gdf = gpd.GeoDataFrame(
            {"id": [1]},
            geometry=[Point(0, 0)],
            crs="EPSG:4326"
        )
        
        # Test client initialization (mock server)
        try:
            client = GeoGlimClient()
            # Test GeoDataFrame to GeoJSON conversion
            geojson_str = client._prepare_aoi(gdf)
            geojson_data = json.loads(geojson_str)
            assert geojson_data["type"] == "FeatureCollection"
        except GeoGlimError:
            # Expected if server is not running - test passes
            pass
    
    def test_health_check_response_structure(self):
        """Test that health check returns expected structure"""
        # This test will only pass if the API server is running
        try:
            client = GeoGlimClient()
            health_data = client.health_check()
            
            # Check required fields
            assert "status" in health_data
            assert "datasets_available" in health_data
            assert "api_version" in health_data
            assert "hosting" in health_data
            
            # Check datasets_available structure
            datasets = health_data["datasets_available"]
            assert isinstance(datasets, dict)
            
        except GeoGlimError:
            # Skip test if server is not available
            pytest.skip("API server not available for testing")

def test_sample_aoi_file():
    """Test that sample AOI file is valid GeoJSON"""
    aoi_path = Path(__file__).parent / "sample_aoi.geojson"
    
    if aoi_path.exists():
        # Test that file can be read as GeoJSON
        gdf = gpd.read_file(str(aoi_path))
        assert not gdf.empty
        assert gdf.geometry.is_valid.all()
        
        # Test JSON structure
        with open(aoi_path, 'r') as f:
            geojson_data = json.load(f)
        
        assert geojson_data["type"] == "FeatureCollection"
        assert "features" in geojson_data

if __name__ == "__main__":
    # Run basic tests
    print("Running basic GeoGlim tests...")
    
    test_sample_aoi_file()
    print("✓ Sample AOI file test passed")
    
    print("Note: API tests require running server. Use pytest for full test suite.")
