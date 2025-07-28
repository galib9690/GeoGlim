# GeoGlim

🌍 **Python package for geological dataset processing with spatial clipping capabilities**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/badge/PyPI-coming%20soon-orange.svg)](https://pypi.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

GeoGlim is a Python package that provides seamless access to global geological datasets with powerful spatial clipping capabilities. Extract and process geological data for any area of interest worldwide through a simple Python API.

### 🔬 Supported Datasets

- **GLiM** (Global Lithological Map): Rock type classifications worldwide
- **GLHYMPS** (Global Hydrogeology and Porosity): Groundwater characteristics and porosity data

### ✨ Key Features

- 🐍 **Simple Python API** - Easy integration into your workflow
- 🗺️ **Spatial Clipping** - Extract data for any area of interest
- 📁 **Multiple Formats** - GeoJSON, Shapefile, and GeoPackage output
- 📊 **Accurate Calculations** - Proper area measurements in square kilometers
- 🌐 **Global Coverage** - Access worldwide geological datasets
- ⚡ **High Performance** - Optimized for large dataset processing

## 🚀 Installation

```bash
# Install from PyPI (coming soon)
pip install geoglim

# Currently available: Install from source
pip install git+https://github.com/galib9690/GeoGlim.git
```

> **Note**: The simple `pip install geoglim` and client API shown below are **coming soon**. For current usage, see [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md).

## 📖 Quick Start *(coming soon)*

### Basic Usage *(coming soon)*

```python
import geoglim
from shapely.geometry import box

# Create a client
client = geoglim.Client()

# Define your area of interest (AOI)
aoi = box(-74.1, 40.7, -73.9, 40.8)  # Manhattan, NYC

# Clip GLiM data
glim_data = client.clip_glim(aoi, output_format='geojson')

# Clip GLHYMPS data  
glhymps_data = client.clip_glhymps(aoi, output_format='geojson')

# Save results
glim_data.to_file('manhattan_geology.geojson', driver='GeoJSON')
glhymps_data.to_file('manhattan_hydrogeology.geojson', driver='GeoJSON')
```

### Advanced Usage

```python
import geoglim
import geopandas as gpd

# Initialize client
client = geoglim.Client()

# Load your study area from a file
study_area = gpd.read_file('my_study_area.shp')

# Get geological data with metadata
result = client.clip_glim(
    geometry=study_area.geometry[0],
    output_format='gpkg',
    include_metadata=True
)

# Calculate areas properly in km²
result['area_km2'] = result.to_crs('EPSG:3857').area / 1_000_000

# Analyze lithology distribution
lithology_stats = result.groupby('Litho')['area_km2'].sum()
print(lithology_stats)
```

## 📊 Data Analysis Examples

### Geological Analysis

```python
# Analyze rock types in your area
rock_types = glim_data['Litho'].value_counts()
print("Rock types found:")
print(rock_types)

# Calculate total area by rock type
glim_data['area_km2'] = geoglim.calculate_area_km2(glim_data)
area_by_rock = glim_data.groupby('Litho')['area_km2'].sum()
```

### Hydrogeological Analysis

```python
# Analyze porosity distribution
porosity_stats = glhymps_data['Porosity'].describe()
print("Porosity statistics:")
print(porosity_stats)

# Find high porosity areas
high_porosity = glhymps_data[glhymps_data['Porosity'] > 0.3]
```

## 🗺️ Visualization

```python
import matplotlib.pyplot as plt

# Plot geological map
fig, ax = plt.subplots(figsize=(12, 8))
glim_data.plot(column='Litho', ax=ax, legend=True, cmap='tab20')
ax.set_title('Geological Map')
plt.show()

# Plot hydrogeological properties
fig, ax = plt.subplots(figsize=(12, 8))
glhymps_data.plot(column='Porosity', ax=ax, legend=True, cmap='Blues')
ax.set_title('Porosity Distribution')
plt.show()
```

## 📚 API Reference

### Client Class

```python
class Client:
    def __init__(self, api_url=None):
        """Initialize GeoGlim client"""
        
    def clip_glim(self, geometry, output_format='geojson', **kwargs):
        """Clip GLiM dataset to specified geometry"""
        
    def clip_glhymps(self, geometry, output_format='geojson', **kwargs):
        """Clip GLHYMPS dataset to specified geometry"""
        
    def get_dataset_info(self, dataset_name):
        """Get information about available datasets"""
```

### Utility Functions

```python
def calculate_area_km2(gdf):
    """Calculate accurate areas in square kilometers"""
    
def create_aoi_from_coordinates(lon_min, lat_min, lon_max, lat_max):
    """Create area of interest from bounding box coordinates"""
    
def validate_geometry(geometry):
    """Validate input geometry for clipping operations"""
```

## 📦 Dependencies

- **GeoPandas** (≥0.13.0) - Geospatial data processing
- **Shapely** (≥2.0.0) - Geometric operations
- **Requests** (≥2.31.0) - HTTP client
- **Pandas** (≥1.5.0) - Data manipulation

## 🤝 Contributing 

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation (coming soon)

If you use GeoGlim in your research, please cite:

```bibtex
@software{galib2025geoglim,
  author = {Mohammad Galib, et al.},
  title = {GeoGlim: Python package for geological dataset processing},
  url = {https://github.com/galib9690/GeoGlim},
  year = {2025}
}
```

## 🙏 Acknowledgments

### Data Sources & Credits

#### GLiM (Global Lithological Map Database v1.0)
- Jens Hartmann & Nils Moosdorf (2012). *The new global lithological map database GLiM: A representation of rock properties at the Earth surface.* Geochemical, Geophys. Geosys., 13, Q12004. [DOI:10.1029/2012GC004370](https://doi.org/10.1029/2012GC004370)
- Gridded version: GLiM v1.0 (0.5°) on PANGAEA. [DOI:10.1594/PANGAEA.788537](https://doi.org/10.1594/PANGAEA.788537)

#### GLHYMPS (Global Hydrogeology and Porosity Map)
- Gleeson, T. et al. (2014). *A global hydrogeological map (GLHYMPS) based on permeability and porosity.* Geophys. Res. Lett., 41(10), 3891–3898. [DOI:10.1002/2014GL059856](https://doi.org/10.1002/2014GL059856)
- Dataset DOI: [10.5683/SP2/DLGXYO](https://doi.org/10.5683/SP2/DLGXYO)

**Note**: GeoGlim will be hosted on the I-GUIDE platform with backend storage via MinIO. Full datasets are stored securely and accessed internally for processing requests.

## 📞 Contact

**Mohammad Galib**
- Email: mgalib@purdue.edu
- GitHub: [@galib9690](https://github.com/galib9690)

---

📖 **For local development setup, see [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md)**
