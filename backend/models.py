from pydantic import BaseModel
from typing import Optional, Literal
from enum import Enum

class DatasetType(str, Enum):
    GLIM = "glim"
    GLHYMPS = "glhymps"

class OutputFormat(str, Enum):
    GEOJSON = "geojson"
    SHAPEFILE = "shapefile"
    GPKG = "gpkg"

class HealthResponse(BaseModel):
    status: str
    datasets_available: dict
    api_version: str = "1.0.0-local"
    hosting: str = "local"

class ClipRequest(BaseModel):
    dataset: DatasetType
    output_format: OutputFormat = OutputFormat.GEOJSON

class DatasetInfo(BaseModel):
    dataset: str
    path: str
    crs: str
    columns: list
    geometry_type: str
    sample_feature_count: int
    available: bool
    hosting: str = "local"
