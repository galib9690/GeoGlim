import os
from pathlib import Path

# Local data paths - UPDATE THESE FOR YOUR PC
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# Dataset paths (local files)
GLIM_PATH = DATA_DIR / "LiMW_GIS_2015.gdb" / "LiMW_GIS 2015.gdb"
GLHYMPS_PATH = DATA_DIR / "GLHYMPS" / "GLHYMPS.shp"

# API settings for local development
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB for local testing
ALLOWED_FORMATS = ["geojson", "shapefile", "gpkg"]

# Performance settings (conservative for local PC)
MAX_CLIP_AREA = 500000  # 500,000 km² max
ENABLE_CORS = True  # For local web testing

# Cloud migration settings (for future use)
USE_CLOUD_STORAGE = False  # Set to True when migrating
CLOUD_DATA_URL = None      # Will be configured later
DATABASE_URL = None        # For future database hosting

def get_data_path(dataset_name: str) -> Path:
    """Get dataset path - easily configurable for cloud migration"""
    if USE_CLOUD_STORAGE:
        # Future: return cloud URL or database connection
        raise NotImplementedError("Cloud storage not yet configured")
    
    # Local file paths
    paths = {
        "glim": GLIM_PATH,
        "glhymps": GLHYMPS_PATH
    }
    return paths.get(dataset_name.lower())

def is_dataset_available(dataset_name: str) -> bool:
    """Check if dataset is available locally"""
    path = get_data_path(dataset_name)
    return path and path.exists()
