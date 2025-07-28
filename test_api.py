#!/usr/bin/env python3
"""
Simple test script for GeoGlim API
This script demonstrates how to use the GeoGlim API without installing the geoglim package
"""

import requests
import json
import geopandas as gpd
from shapely.geometry import box
import tempfile
import os

def test_health_check():
    """Test the API health check endpoint"""
    print("=== Testing API Health Check ===")
    
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API Status: {data['status']}")
            print(f"✓ API Version: {data['api_version']}")
            print(f"✓ Hosting: {data['hosting']}")
            print("✓ Available Datasets:")
            for dataset, available in data['datasets_available'].items():
                status = "✓ Available" if available else "✗ Not Available"
                print(f"  - {dataset.upper()}: {status}")
            return True
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to API: {e}")
        return False

def test_dataset_clipping():
    """Test dataset clipping with a simple AOI"""
    print("\n=== Testing Dataset Clipping ===")
    
    # Create a simple test AOI around New York City
    print("Creating test AOI around New York City...")
    test_aoi = gpd.GeoDataFrame(
        {"name": ["NYC Test Area"]},
        geometry=[box(-74.1, 40.6, -73.8, 40.9)],  # NYC bounding box
        crs="EPSG:4326"
    )
    
    # Save AOI to temporary GeoJSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
        test_aoi.to_file(f.name, driver='GeoJSON')
        geojson_path = f.name
    
    try:
        # Test clipping GLHYMPS dataset
        print("Testing GLHYMPS dataset clipping...")
        
        with open(geojson_path, 'rb') as f:
            files = {'geojson_file': ('test_aoi.geojson', f, 'application/json')}
            params = {'output_format': 'geojson'}
            
            response = requests.post(
                "http://localhost:8000/clip/glhymps",
                files=files,
                params=params
            )
            
            if response.status_code == 200:
                # Save the result
                output_path = "glhymps_clipped_nyc.geojson"
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                
                # Check the result
                result_gdf = gpd.read_file(output_path)
                print(f"✓ GLHYMPS clipping successful!")
                print(f"  - Features returned: {len(result_gdf)}")
                print(f"  - Output saved to: {output_path}")
                print(f"  - Columns: {', '.join(result_gdf.columns[:5])}...")
                
                # Clean up
                os.unlink(output_path)
                
            else:
                print(f"✗ GLHYMPS clipping failed: {response.status_code}")
                print(f"  Error: {response.text}")
        
        # Test clipping GLiM dataset
        print("\nTesting GLiM dataset clipping...")
        
        with open(geojson_path, 'rb') as f:
            files = {'geojson_file': ('test_aoi.geojson', f, 'application/json')}
            params = {'output_format': 'geojson'}
            
            response = requests.post(
                "http://localhost:8000/clip/glim",
                files=files,
                params=params
            )
            
            if response.status_code == 200:
                # Save the result
                output_path = "glim_clipped_nyc.geojson"
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                
                # Check the result
                result_gdf = gpd.read_file(output_path)
                print(f"✓ GLiM clipping successful!")
                print(f"  - Features returned: {len(result_gdf)}")
                print(f"  - Output saved to: {output_path}")
                print(f"  - Columns: {', '.join(result_gdf.columns[:5])}...")
                
                # Clean up
                os.unlink(output_path)
                
            else:
                print(f"✗ GLiM clipping failed: {response.status_code}")
                print(f"  Error: {response.text}")
                
    except Exception as e:
        print(f"✗ Error during clipping test: {e}")
    
    finally:
        # Clean up temporary file
        if os.path.exists(geojson_path):
            os.unlink(geojson_path)

def test_dataset_info():
    """Test getting dataset information"""
    print("\n=== Testing Dataset Information ===")
    
    for dataset in ['glim', 'glhymps']:
        try:
            response = requests.get(f"http://localhost:8000/datasets/{dataset}/info")
            if response.status_code == 200:
                info = response.json()
                print(f"✓ {dataset.upper()} Dataset Info:")
                print(f"  - Path: {info.get('path', 'N/A')}")
                print(f"  - CRS: {info.get('crs', 'N/A')}")
                print(f"  - Geometry Type: {info.get('geometry_type', 'N/A')}")
                if 'columns' in info:
                    print(f"  - Columns: {', '.join(info['columns'][:5])}...")
            else:
                print(f"✗ {dataset.upper()} info failed: {response.status_code}")
        except Exception as e:
            print(f"✗ Error getting {dataset} info: {e}")

if __name__ == "__main__":
    print("GeoGlim API Test Script")
    print("=" * 50)
    
    # Test API health
    if test_health_check():
        # Test dataset information
        test_dataset_info()
        
        # Test clipping functionality
        test_dataset_clipping()
        
        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        print("\nYour GeoGlim API is running successfully!")
        print("You can now:")
        print("1. Visit http://localhost:8000/docs for interactive API documentation")
        print("2. Use the API endpoints to clip geological datasets")
        print("3. Access GLiM and GLHYMPS datasets for your research")
    else:
        print("\n✗ API is not responding. Make sure the server is running:")
        print("  python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload")
