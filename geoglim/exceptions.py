"""
Custom exceptions for GeoGlim package
"""

class GeoGlimError(Exception):
    """Base exception for GeoGlim package"""
    pass

class DatasetNotFoundError(GeoGlimError):
    """Raised when a requested dataset is not found or not available"""
    pass

class ClippingError(GeoGlimError):
    """Raised when a clipping operation fails"""
    pass

class ValidationError(GeoGlimError):
    """Raised when input validation fails"""
    pass

class APIError(GeoGlimError):
    """Raised when API communication fails"""
    pass
