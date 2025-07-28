"""
GeoGlim Python Client Package
Easy access to geological datasets through the GeoGlim API
"""

from .client import GeoGlimClient
from .exceptions import GeoGlimError, DatasetNotFoundError, ClippingError

__version__ = "1.0.0"
__author__ = "Mohammad Galib"

__all__ = [
    "GeoGlimClient",
    "GeoGlimError", 
    "DatasetNotFoundError",
    "ClippingError"
]
