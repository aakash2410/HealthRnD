"""
Domain-specific exceptions for the Healthcare platform.
"""

class BaseHealthcareError(Exception):
    """Base exception for all healthcare platform errors."""
    pass

class DataIngestionError(BaseHealthcareError):
    """Raised when data ingestion from a source fails."""
    pass

class RateLimitExceededError(DataIngestionError):
    """Raised when an external API rate limit is exceeded."""
    pass

class ModelInferenceError(BaseHealthcareError):
    """Raised when ML model prediction or processing fails."""
    pass

class GraphConnectionError(BaseHealthcareError):
    """Raised when connecting to or querying the graph database fails."""
    pass
