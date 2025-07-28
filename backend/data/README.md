# Local Dataset Storage

This directory is for storing geological datasets on your local PC.

## Required Datasets

To use GeoGlim, place the following datasets in this folder:

### GLiM Dataset
- **File**: `LiMW_GIS_2015.gdb/` (FileGDB format)
- **Source**: https://doi.org/10.1594/GFZ.GEOFON.gfz2009cl1
- **Description**: Global Lithological Map

### GLHYMPS Dataset  
- **File**: `GLHYMPS.shp` (Shapefile format)
- **Source**: https://doi.org/10.1038/sdata.2017.89
- **Description**: Global Hydrogeology and Porosity

## Directory Structure

```
backend/data/
├── LiMW_GIS_2015.gdb/     # GLiM dataset (FileGDB)
├── GLHYMPS.shp            # GLHYMPS dataset (Shapefile)
├── GLHYMPS.shx            # Shapefile index
├── GLHYMPS.dbf            # Shapefile attributes
├── GLHYMPS.prj            # Shapefile projection
└── README.md              # This file
```

## Installation Instructions

1. Download the GLiM dataset from the GFZ Data Portal
2. Download the GLHYMPS dataset from Nature Scientific Data
3. Extract/copy the files to this directory
4. Restart the GeoGlim API server
5. Check the health endpoint to verify datasets are detected