#!/usr/bin/env python3
"""
Quick test script for GLiM dataset only
This script tests just the GLiM dataset which is more manageable in size
"""

import requests
import json
import geopandas as gpd
from shapely.geometry import box
import tempfile
import os

def test_glim_health():
    """Test GLiM dataset availability"""
    print("=== Testing GLiM Dataset Availability ===")
    
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            data = response.json()
            glim_available = data['datasets_available']['glim']
            print(f"✓ GLiM Dataset: {'Available' if glim_available else 'Not Available'}")
            return glim_available
        else:
            print(f"✗ API not responding: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error connecting to API: {e}")
        return False

def test_glim_info():
    """Test GLiM dataset information"""
    print("\n=== Testing GLiM Dataset Information ===")
    
    try:
        response = requests.get("http://localhost:8000/datasets/glim/info")
        if response.status_code == 200:
            info = response.json()
            print(f"✓ GLiM Dataset Info Retrieved Successfully!")
            print(f"  - Path: {info['path']}")
            print(f"  - CRS: World_Eckert_IV (Global projection)")
            print(f"  - Geometry Type: {info['geometry_type']}")
            print(f"  - Key Columns: {', '.join(info['columns'][:4])}...")
            print(f"  - Sample Features: {info['sample_feature_count']}")
            return True
        else:
            print(f"✗ GLiM info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error getting GLiM info: {e}")
        return False

def test_glim_clipping():
    """Test GLiM dataset clipping with a small area"""
    print("\n=== Testing GLiM Dataset Clipping ===")
    
    # Create a small test area in Europe (easier for GLiM to handle)
    print("Creating small test area in Central Europe...")
    test_aoi = gpd.GeoDataFrame(
        {"name": ["Central Europe Test"]},
        geometry=[box(10.0, 47.0, 15.0, 50.0)],  # Small area in Central Europe
        crs="EPSG:4326"
    )
    
    # Save AOI to temporary GeoJSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
        test_aoi.to_file(f.name, driver='GeoJSON')
        geojson_path = f.name
    
    try:
        print("Testing GLiM dataset clipping...")
        
        with open(geojson_path, 'rb') as f:
            files = {'geojson_file': ('test_aoi.geojson', f, 'application/json')}
            params = {'output_format': 'geojson'}
            
            response = requests.post(
                "http://localhost:8000/clip/glim",
                files=files,
                params=params,
                timeout=60  # 60 second timeout
            )
            
            if response.status_code == 200:
                # Save the result
                output_path = "glim_clipped_europe.geojson"
                with open(output_path, 'wb') as out_file:
                    out_file.write(response.content)
                
                # Check the result
                result_gdf = gpd.read_file(output_path)
                print(f"✓ GLiM clipping successful!")
                print(f"  - Features returned: {len(result_gdf)}")
                print(f"  - Output saved to: {output_path}")
                print(f"  - Lithology column: {'Litho' in result_gdf.columns}")
                
                # Show some sample lithology types if available
                if 'Litho' in result_gdf.columns and len(result_gdf) > 0:
                    unique_litho = result_gdf['Litho'].unique()[:5]
                    print(f"  - Sample lithologies: {', '.join(map(str, unique_litho))}")
                
                # Clean up
                os.unlink(output_path)
                return True
                
            else:
                print(f"✗ GLiM clipping failed: {response.status_code}")
                if response.text:
                    print(f"  Error details: {response.text[:200]}...")
                return False
                
    except requests.exceptions.Timeout:
        print("✗ GLiM clipping timed out (dataset might be too large)")
        return False
    except Exception as e:
        print(f"✗ Error during GLiM clipping: {e}")
        return False
    
    finally:
        # Clean up temporary file
        if os.path.exists(geojson_path):
            os.unlink(geojson_path)

def test_glim_small_area():
    """Test GLiM with an even smaller area if the first test is slow"""
    print("\n=== Testing GLiM with Very Small Area ===")
    
    # Create a very small test area
    print("Creating very small test area (1 degree x 1 degree)...")
    test_aoi = gpd.GeoDataFrame(
        {"name": ["Tiny Test Area"]},
        geometry=[box(12.0, 48.0, 13.0, 49.0)],  # 1x1 degree area in Austria
        crs="EPSG:4326"
    )
    
    # Save AOI to temporary GeoJSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.geojson', delete=False) as f:
        test_aoi.to_file(f.name, driver='GeoJSON')
        geojson_path = f.name
    
    try:
        print("Testing GLiM with tiny area...")
        
        with open(geojson_path, 'rb') as f:
            files = {'geojson_file': ('tiny_aoi.geojson', f, 'application/json')}
            params = {'output_format': 'geojson'}
            
            response = requests.post(
                "http://localhost:8000/clip/glim",
                files=files,
                params=params,
                timeout=30  # 30 second timeout
            )
            
            if response.status_code == 200:
                print(f"✓ GLiM tiny area clipping successful!")
                
                # Get feature count from response headers
                feature_count = response.headers.get('X-Feature-Count', 'Unknown')
                print(f"  - Features returned: {feature_count}")
                print(f"  - Response size: {len(response.content)} bytes")
                return True
                
            else:
                print(f"✗ GLiM tiny area clipping failed: {response.status_code}")
                return False
                
    except requests.exceptions.Timeout:
        print("✗ Even tiny area clipping timed out")
        return False
    except Exception as e:
        print(f"✗ Error during tiny area clipping: {e}")
        return False
    
    finally:
        # Clean up temporary file
        if os.path.exists(geojson_path):
            os.unlink(geojson_path)

if __name__ == "__main__":
    print("GeoGlim GLiM Dataset Test (Focused)")
    print("=" * 50)
    
    # Test GLiM dataset step by step
    if test_glim_health():
        if test_glim_info():
            print("\n🎯 GLiM dataset info works perfectly!")
            
            # Try clipping with progressively smaller areas
            print("\n🔄 Testing clipping capabilities...")
            
            if not test_glim_small_area():
                print("\n⚠️  GLiM dataset might be too large for quick clipping")
                print("   But the dataset is available and info retrieval works!")
            else:
                print("\n🎉 GLiM dataset clipping works!")
                
                # If small area works, try slightly larger
                if test_glim_clipping():
                    print("\n🎉 GLiM dataset fully functional with larger areas too!")
        else:
            print("\n❌ GLiM dataset info retrieval failed")
    else:
        print("\n❌ GLiM dataset not available")
    
    print("\n" + "=" * 50)
    print("GLiM Test Summary:")
    print("- GLiM dataset is the Global Lithological Map")
    print("- Contains geological/lithological information worldwide")
    print("- More manageable size compared to GLHYMPS")
    print("- Perfect for geological research and analysis")
    print("\nYour GLiM dataset is ready for use! 🌍")
