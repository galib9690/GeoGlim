"""
Basic usage examples for GeoGlim package
"""

import geopandas as gpd
from pathlib import Path
from geoglim import GeoGlimClient
from geoglim.exceptions import GeoGlimError, DatasetNotFoundError, ClippingError

def example_health_check():
    """Example: Check API health and available datasets"""
    print("=== GeoGlim Health Check Example ===")
    
    try:
        # Initialize client
        client = GeoGlimClient("http://localhost:8000")
        
        # Check health
        health_data = client.health_check()
        print(f"API Status: {health_data['status']}")
        print(f"API Version: {health_data['api_version']}")
        print(f"Hosting: {health_data['hosting']}")
        
        # Check available datasets
        datasets = health_data['datasets_available']
        print("\nAvailable Datasets:")
        for dataset, available in datasets.items():
            status = "✓ Available" if available else "✗ Not Available"
            print(f"  {dataset}: {status}")
            
    except GeoGlimError as e:
        print(f"Error: {e}")
        print("Make sure the GeoGlim API server is running on localhost:8000")

def example_dataset_info():
    """Example: Get dataset information"""
    print("\n=== Dataset Information Example ===")
    
    try:
        client = GeoGlimClient("http://localhost:8000")
        
        # Get info for available datasets
        for dataset_name in ["glim", "glhymps"]:
            try:
                info = client.get_dataset_info(dataset_name)
                print(f"\n{dataset_name.upper()} Dataset Info:")
                print(f"  Path: {info['path']}")
                print(f"  CRS: {info['crs']}")
                print(f"  Geometry Type: {info['geometry_type']}")
                print(f"  Columns: {', '.join(info['columns'][:5])}...")  # Show first 5 columns
                
            except DatasetNotFoundError:
                print(f"\n{dataset_name.upper()}: Dataset not available locally")
                
    except GeoGlimError as e:
        print(f"Error: {e}")

def example_simple_clipping():
    """Example: Simple dataset clipping with sample AOI"""
    print("\n=== Simple Clipping Example ===")
    
    try:
        client = GeoGlimClient("http://localhost:8000")
        
        # Use the sample AOI file
        sample_aoi_path = Path(__file__).parent.parent / "tests" / "sample_aoi.geojson"
        
        if not sample_aoi_path.exists():
            print("Sample AOI file not found. Creating a simple test area...")
            # Create a simple test area around New York City
            from shapely.geometry import box
            test_gdf = gpd.GeoDataFrame(
                {"name": ["Test Area"]},
                geometry=[box(-74.1, 40.6, -73.8, 40.9)],
                crs="EPSG:4326"
            )
        else:
            test_gdf = gpd.read_file(sample_aoi_path)
        
        # Try clipping GLiM dataset
        try:
            print("Attempting to clip GLiM dataset...")
            result = client.clip_dataset(
                dataset="glim",
                aoi=test_gdf,
                output_format="geojson"
            )
            print(f"✓ GLiM clipping successful: {len(result)} features returned")
            print(f"  Columns: {', '.join(result.columns[:5])}...")
            
        except DatasetNotFoundError:
            print("✗ GLiM dataset not available")
        except ClippingError as e:
            print(f"✗ GLiM clipping failed: {e}")
        
        # Try clipping GLHYMPS dataset
        try:
            print("\nAttempting to clip GLHYMPS dataset...")
            result = client.clip_dataset(
                dataset="glhymps",
                aoi=test_gdf,
                output_format="geojson"
            )
            print(f"✓ GLHYMPS clipping successful: {len(result)} features returned")
            print(f"  Columns: {', '.join(result.columns[:5])}...")
            
        except DatasetNotFoundError:
            print("✗ GLHYMPS dataset not available")
        except ClippingError as e:
            print(f"✗ GLHYMPS clipping failed: {e}")
            
    except GeoGlimError as e:
        print(f"Error: {e}")

def example_advanced_clipping():
    """Example: Advanced clipping with output file saving"""
    print("\n=== Advanced Clipping Example ===")
    
    try:
        client = GeoGlimClient("http://localhost:8000")
        
        # Create a custom AOI
        from shapely.geometry import Point
        
        # Create a buffer around a point (e.g., around a city)
        point = Point(-73.935242, 40.730610)  # New York City coordinates
        buffer_gdf = gpd.GeoDataFrame(
            {"city": ["New York City"], "buffer_km": [10]},
            geometry=[point.buffer(0.1)],  # ~10km buffer in degrees
            crs="EPSG:4326"
        )
        
        print("Created custom AOI around New York City")
        
        # Clip dataset and save to file
        try:
            output_path = Path("nyc_geology.gpkg")
            result = client.clip_dataset(
                dataset="glim",
                aoi=buffer_gdf,
                output_format="gpkg",
                output_path=output_path
            )
            
            print(f"✓ Advanced clipping successful!")
            print(f"  Features: {len(result)}")
            print(f"  Output saved to: {output_path}")
            print(f"  CRS: {result.crs}")
            
            # Show some statistics
            if len(result) > 0:
                print(f"  Geometry types: {result.geometry.geom_type.value_counts().to_dict()}")
                
        except DatasetNotFoundError:
            print("✗ Dataset not available for advanced clipping")
        except ClippingError as e:
            print(f"✗ Advanced clipping failed: {e}")
            
    except GeoGlimError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    """
    Run all examples
    
    To use these examples:
    1. Start the GeoGlim API server:
       python -m uvicorn backend.main:app --reload
    
    2. Ensure datasets are available in backend/data/ folder:
       - LiMW_GIS_2015.gdb (GLiM dataset)
       - GLHYMPS.shp (GLHYMPS dataset)
    
    3. Run this script:
       python examples/basic_usage.py
    """
    
    print("GeoGlim Package - Basic Usage Examples")
    print("=" * 50)
    
    # Run all examples
    example_health_check()
    example_dataset_info()
    example_simple_clipping()
    example_advanced_clipping()
    
    print("\n" + "=" * 50)
    print("Examples complete!")
    print("\nNext steps:")
    print("1. Download GLiM and GLHYMPS datasets to backend/data/ folder")
    print("2. Start the API server: python -m uvicorn backend.main:app --reload")
    print("3. Use the GeoGlim client in your own projects!")
