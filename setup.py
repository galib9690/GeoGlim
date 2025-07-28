from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
try:
    long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else "GeoGlim - Geological dataset processing package"
except Exception:
    long_description = "GeoGlim - Geological dataset processing package"

# Read version from package
version = "1.0.0"

setup(
    name="geoglim",
    version=version,
    author="Mohammad Galib",
    author_email="mgalib@purdue.edu",
    description="Python package for geological dataset processing with local hosting and spatial clipping",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galib9690/GeoGlim",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Hydrology",
        "Topic :: Scientific/Engineering :: Geology",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.22.0",
        "geopandas>=0.13.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "shapely>=2.0.0",
        "pandas>=1.5.0",
        "fiona>=1.8.0",
        "pyproj>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.24.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "geoglim-server=backend.main:main",
        ],
    },
    include_package_data=True,
    keywords="geology, GIS, spatial, datasets, GLiM, GLHYMPS, clipping, FastAPI",
    project_urls={
        "Bug Reports": "https://github.com/galib9690/GeoGlim/issues",
        "Source": "https://github.com/galib9690/GeoGlim",
        "Documentation": "https://github.com/galib9690/GeoGlim/wiki",
    },
)
