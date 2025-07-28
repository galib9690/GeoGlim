# GeoGlim - Local Development Setup

🏠 **Local hosting and development guide for GeoGlim**

This guide covers setting up and running GeoGlim locally with your own datasets. This is the current development version before the package is hosted publicly.

## 📋 Overview

The local development version allows you to:
- Host geological datasets on your local machine
- Run the FastAPI server locally
- Test and develop the package before public deployment
- Work with your own dataset files

## 🚀 Quick Setup

### Prerequisites

- Python 3.8 or higher
- Git
- At least 10GB free disk space (for datasets)

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/galib9690/GeoGlim.git
cd GeoGlim

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

### 2. Download Datasets

Download the required datasets and place them in the `backup/data/` directory:

#### GLiM Dataset
- **Source**: [PANGAEA Data Publisher](https://doi.org/10.1594/PANGAEA.788537)
- **Paper**: [DOI:10.1029/2012GC004370](https://doi.org/10.1029/2012GC004370)
- **File**: `glim_wgs84_0point5deg.shp` (and associated files)
- **Size**: ~500MB
- **Location**: `backup/data/glim/`

#### GLHYMPS Dataset
- **Source**: [Scholars Portal Dataverse](https://doi.org/10.5683/SP2/DLGXYO)
- **Paper**: [DOI:10.1002/2014GL059856](https://doi.org/10.1002/2014GL059856)
- **File**: `GLHYMPS.shp` (and associated files)
- **Size**: ~2GB
- **Location**: `backup/data/glhymps/`

### 3. Configure Data Paths

Update the file paths in `backend/config.py`:

```python
# backend/config.py
DATASETS = {
    "glim": {
        "path": "backup/data/glim/glim_wgs84_0point5deg.shp",
        "available": True
    },
    "glhymps": {
        "path": "backup/data/glhymps/GLHYMPS.shp", 
        "available": True
    }
}
```

### 4. Start the Local Server

```bash
# Start the FastAPI server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The server will be available at: `http://localhost:8000`

## 📖 Local Usage

### API Endpoints

Once the server is running:

- **Health Check**: `GET http://localhost:8000/`
- **Dataset Info**: `GET http://localhost:8000/datasets/{dataset_name}/info`
- **Clip Data**: `POST http://localhost:8000/clip/{dataset_name}`
- **API Docs**: `http://localhost:8000/docs`

### Using the Jupyter Notebook

```bash
# Start Jupyter
jupyter notebook

# Open the example notebook
# GeoGlim_Usage_Example.ipynb
```

The notebook contains complete examples for:
- Setting up areas of interest (AOI)
- Clipping both GLiM and GLHYMPS datasets
- Visualizing results with proper km² area calculations
- Analyzing geological and hydrogeological data

### Python Client Usage

```python
import requests
import geopandas as gpd
from shapely.geometry import box
import tempfile

# Define your area of interest
aoi = box(-74.1, 40.7, -73.9, 40.8)  # Manhattan, NYC
aoi_gdf = gpd.GeoDataFrame([1], geometry=[aoi], crs="EPSG:4326")

# Save AOI to temporary file
with tempfile.NamedTemporaryFile(suffix='.geojson', delete=False) as f:
    aoi_gdf.to_file(f.name, driver='GeoJSON')
    
    # Make clipping request
    with open(f.name, 'rb') as file:
        files = {'geojson_file': file}
        response = requests.post(
            'http://localhost:8000/clip/glim',
            files=files,
            params={'output_format': 'geojson'}
        )

# Save result
if response.status_code == 200:
    with open('result.geojson', 'wb') as f:
        f.write(response.content)
    
    # Load and analyze
    result = gpd.read_file('result.geojson')
    print(f"Found {len(result)} geological features")
```

## 🏗️ Project Structure

```
GeoGlim/
├── LOCAL_DEVELOPMENT.md        # This file
├── README.md                   # Main package documentation
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Package configuration
├── setup.py                   # Package setup
├── GeoGlim_Usage_Example.ipynb # Complete local examples
├── backend/                   # FastAPI server
│   ├── main.py               # API entry point
│   ├── config.py             # Configuration
│   └── services/             # Business logic
│       └── clip_service.py   # Clipping operations
├── geoglim/                  # Python package
│   ├── __init__.py
│   └── client.py             # Client library
├── backup/                   # Local data storage
│   └── data/                 # Dataset files
│       ├── glim/            # GLiM dataset
│       └── glhymps/         # GLHYMPS dataset
├── tests/                    # Test suite
│   ├── test_api.py          # API tests
│   └── test_glim_only.py    # GLiM-specific tests
└── examples/                 # Additional examples
```

## 🔧 Configuration

### Environment Variables

```bash
# Optional: Custom host and port
export GEOGLIM_HOST="127.0.0.1"
export GEOGLIM_PORT="8000"

# Optional: Custom data directory
export GEOGLIM_DATA_PATH="/path/to/your/datasets"
```

### Server Configuration

Edit `backend/config.py` to customize:

```python
# Server settings
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# Dataset paths
DATASETS = {
    "glim": {
        "path": "backup/data/glim/glim_wgs84_0point5deg.shp",
        "available": True,
        "description": "Global Lithological Map"
    },
    "glhymps": {
        "path": "backup/data/glhymps/GLHYMPS.shp",
        "available": True,
        "description": "Global Hydrogeology and Porosity"
    }
}
```

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific tests
python test_api.py
python test_glim_only.py

# Test with specific area
python -c "
import requests
response = requests.get('http://localhost:8000/')
print('Server status:', response.json())
"
```

### Test Data Clipping

```bash
# Test GLiM clipping
curl -X POST "http://localhost:8000/clip/glim" \
  -F "geojson_file=@test_area.geojson" \
  -F "output_format=geojson"

# Test GLHYMPS clipping  
curl -X POST "http://localhost:8000/clip/glhymps" \
  -F "geojson_file=@test_area.geojson" \
  -F "output_format=geojson"
```

## 🚀 Deployment Preparation

### For Future Cloud Deployment

1. **Update configuration** for production URLs
2. **Set up cloud storage** for datasets
3. **Configure authentication** if needed
4. **Update client library** to use production endpoints
5. **Package for PyPI** distribution

### Migration Checklist

- [ ] Upload datasets to cloud storage
- [ ] Update API endpoints in client
- [ ] Set up production server
- [ ] Configure domain and SSL
- [ ] Update documentation
- [ ] Publish to PyPI

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
```bash
# Check if port is in use
lsof -i :8000

# Use different port
python -m uvicorn backend.main:app --port 8001
```

**Dataset not found:**
```bash
# Check file paths
ls -la backup/data/glim/
ls -la backup/data/glhymps/

# Update paths in backend/config.py
```

**Memory issues with large datasets:**
```bash
# Increase available memory or use smaller test areas
# Monitor memory usage
htop
```

### Performance Tips

- Use smaller AOIs for testing
- Consider dataset indexing for faster queries
- Monitor memory usage with large datasets
- Use SSD storage for better I/O performance

## 📞 Support

For local development issues:
- Check the [Issues](https://github.com/galib9690/GeoGlim/issues) page
- Review the Jupyter notebook examples
- Test with smaller areas first

**Mohammad Galib**
- Email: mgalib@purdue.edu
- GitHub: [@galib9690](https://github.com/galib9690)

---

📖 **For the production package documentation, see [README.md](README.md)**
