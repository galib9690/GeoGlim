from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import geopandas as gpd
import tempfile
import logging
from pathlib import Path
import json
import os

from .config import *
from .models import *
from .services.clip_service import ClipService
from .utils.validation import validate_geojson_file

# Setup logging for local development
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GeoGlim API - Local Development",
    description="Local geological dataset clipping API",
    version="1.0.0-local"
)

# Enable CORS for local development
if ENABLE_CORS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Initialize services
clip_service = ClipService()

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Check API health and dataset availability"""
    datasets_status = {
        "glim": is_dataset_available("glim"),
        "glhymps": is_dataset_available("glhymps")
    }
    
    logger.info(f"Health check - Datasets: {datasets_status}")
    
    return HealthResponse(
        status="healthy" if any(datasets_status.values()) else "no_datasets",
        datasets_available=datasets_status
    )

@app.post("/clip/{dataset}")
async def clip_dataset(
    dataset: DatasetType,
    geojson_file: UploadFile = File(...),
    output_format: OutputFormat = Query(OutputFormat.GEOJSON)
):
    """
    Clip dataset to the provided area of interest (AOI)
    
    **Local Development Version**
    - Reads datasets from local backend/data/ folder
    - Supports GLiM and GLHYMPS datasets
    - Returns clipped data in requested format
    """
    try:
        logger.info(f"Clipping request: {dataset.value} -> {output_format.value}")
        
        # Check if dataset exists locally
        if not is_dataset_available(dataset.value):
            raise HTTPException(
                status_code=404, 
                detail=f"Dataset {dataset.value} not found in local storage. "
                       f"Please ensure files are in backend/data/ folder."
            )
        
        # Validate uploaded file
        contents = await geojson_file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {MAX_FILE_SIZE/1024/1024:.1f}MB"
            )
        
        # Parse and validate AOI
        aoi_gdf = validate_geojson_file(contents)
        logger.info(f"AOI loaded: {len(aoi_gdf)} features")
        
        # Perform clipping
        result_gdf, temp_file_path = clip_service.clip_data(
            dataset=dataset.value,
            aoi=aoi_gdf,
            output_format=output_format.value
        )
        
        logger.info(f"Clipping complete: {len(result_gdf)} features returned")
        
        # Return the clipped file
        filename = f"{dataset.value}_clipped.{output_format.value}"
        return FileResponse(
            temp_file_path,
            media_type='application/octet-stream',
            filename=filename,
            headers={"X-Feature-Count": str(len(result_gdf))}
        )
        
    except Exception as e:
        logger.error(f"Clipping error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Clipping failed: {str(e)}")

@app.get("/datasets/{dataset}/info")
async def get_dataset_info(dataset: DatasetType):
    """Get basic information about a dataset"""
    if not is_dataset_available(dataset.value):
        raise HTTPException(
            status_code=404,
            detail=f"Dataset {dataset.value} not available locally"
        )
    
    return clip_service.get_dataset_info(dataset.value)

# For local development - run with: python -m uvicorn backend.main:app --reload
if __name__ == "__main__":
    import uvicorn
    print(f"Starting GeoGlim API locally on {API_HOST}:{API_PORT}")
    print(f"Data directory: {DATA_DIR}")
    print(f"GLiM available: {is_dataset_available('glim')}")
    print(f"GLHYMPS available: {is_dataset_available('glhymps')}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
